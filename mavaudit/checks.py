"""Observation and findings logic.

The auditor never needs the signing key. It inspects frame headers:
- MAVLink 1 frames start with 0xFE and cannot carry a signature.
- MAVLink 2 frames start with 0xFD; bit 0 of incompat_flags marks a signed frame.

CRA mapping refers to Regulation (EU) 2024/2847, Annex I, Part I, point 2.
It is the author's technical interpretation, not legal advice.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict

from .advisories import decode_version, matching

MAVLINK_IFLAG_SIGNED = 0x01
CAP_FTP = 32
CAP_MAVLINK2 = 8192

AUTOPILOTS = {0: "generic", 3: "ardupilot", 8: "invalid", 12: "px4"}

SEVERITY_ORDER = {"info": 0, "low": 1, "medium": 2, "high": 3}


@dataclass
class EndpointStats:
    sysid: int
    compid: int
    frames: int = 0
    v1_frames: int = 0
    v2_frames: int = 0
    signed_frames: int = 0
    autopilot: str | None = None
    mav_type: int | None = None
    msg_types: set[str] = field(default_factory=set)
    unsigned_types: set[str] = field(default_factory=set)
    type_counts: dict[str, int] = field(default_factory=dict)
    capabilities: int | None = None
    firmware: str | None = None
    firmware_tuple: tuple[int, int, int] | None = None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["msg_types"] = sorted(self.msg_types)
        d["unsigned_types"] = sorted(self.unsigned_types)
        d["firmware_tuple"] = list(self.firmware_tuple) if self.firmware_tuple else None
        d["ftp_advertised"] = bool(self.capabilities and self.capabilities & CAP_FTP)
        return d


@dataclass
class Finding:
    id: str
    severity: str  # info | low | medium | high
    title: str
    detail: str
    endpoint: str
    cra_refs: list[str]
    recommendation: str
    advisories: list[dict] = field(default_factory=list)


class Observer:
    """Accumulates statistics from parsed pymavlink messages."""

    def __init__(self) -> None:
        self.endpoints: dict[tuple[int, int], EndpointStats] = {}

    def observe(self, msg) -> None:
        if msg.get_type() == "BAD_DATA":
            return
        buf = msg.get_msgbuf()
        sysid, compid = msg.get_srcSystem(), msg.get_srcComponent()
        # Unknown message types carry no parsed header; read the ids from the raw frame.
        if buf and len(buf) > 6:
            if buf[0] == 0xFD:
                sysid, compid = buf[5], buf[6]
            elif buf[0] == 0xFE:
                sysid, compid = buf[3], buf[4]
        ep = self.endpoints.setdefault((sysid, compid), EndpointStats(sysid, compid))
        ep.frames += 1
        mtype = msg.get_type()
        ep.msg_types.add(mtype)
        ep.type_counts[mtype] = ep.type_counts.get(mtype, 0) + 1
        signed = False
        if buf and buf[0] == 0xFE:
            ep.v1_frames += 1
        else:
            ep.v2_frames += 1
            if buf and len(buf) > 2 and buf[2] & MAVLINK_IFLAG_SIGNED:
                ep.signed_frames += 1
                signed = True
        if not signed:
            ep.unsigned_types.add(mtype)
        if mtype == "HEARTBEAT":
            ep.autopilot = AUTOPILOTS.get(msg.autopilot, f"id{msg.autopilot}")
            ep.mav_type = msg.type
        elif mtype == "AUTOPILOT_VERSION":
            ep.capabilities = int(msg.capabilities)
            major, minor, patch, vtype = decode_version(msg.flight_sw_version)
            ep.firmware_tuple = (major, minor, patch)
            ep.firmware = f"{major}.{minor}.{patch} (type {vtype})"


def _vehicle(ep: EndpointStats) -> bool:
    return ep.autopilot in ("ardupilot", "px4")


def evaluate(observer: Observer, unsigned_probe: dict | None = None) -> list[Finding]:
    """Turn observations into findings. unsigned_probe: {"sysid":..,"answered":bool,"param":..}."""
    findings: list[Finding] = []
    for (sysid, compid), ep in sorted(observer.endpoints.items()):
        name = f"{sysid}/{compid}"
        if ep.frames == 0:
            continue
        if ep.v1_frames:
            findings.append(Finding(
                "MAV-001", "medium", "MAVLink 1 traffic observed",
                f"{ep.v1_frames}/{ep.frames} frames are MAVLink 1, which has no signing support.",
                name, ["Annex I.I.2(b) secure by default", "Annex I.I.2(f) integrity"],
                "Force MAVLink 2 on all links (e.g. ArduPilot SERIALn_PROTOCOL=2) and enable signing.",
                matching(ep.autopilot, "v1"),
            ))
        unsigned = ep.frames - ep.signed_frames
        if ep.signed_frames == 0:
            findings.append(Finding(
                "MAV-002", "high", "No signed MAVLink frames",
                f"0/{ep.frames} frames carry a MAVLink 2 signature. Commands and telemetry "
                "on this link have no cryptographic integrity or origin authentication.",
                name, ["Annex I.I.2(b) secure by default", "Annex I.I.2(d) protection from unauthorised access",
                       "Annex I.I.2(f) integrity of data and commands"],
                "Enable MAVLink 2 message signing with a per-vehicle key and a key-provisioning process.",
                matching(ep.autopilot, "unsigned") if _vehicle(ep) else [],
            ))
        elif unsigned:
            findings.append(Finding(
                "MAV-003", "medium", "Mixed signed and unsigned frames",
                f"{unsigned}/{ep.frames} frames are unsigned while others are signed "
                f"(unsigned types: {', '.join(sorted(ep.unsigned_types))}). "
                "Check whether the receiver accepts unsigned messages.",
                name, ["Annex I.I.2(f) integrity"],
                "Reject unsigned messages except the minimum allowed by the signing spec (e.g. RADIO_STATUS).",
            ))
        probe_here = bool(unsigned_probe and unsigned_probe.get("answered")
                          and unsigned_probe.get("sysid") == sysid and unsigned_probe.get("compid", compid) == compid)
        if ep.capabilities is not None and ep.capabilities & CAP_FTP and (ep.signed_frames == 0 or probe_here):
            findings.append(Finding(
                "MAV-006", "high", "MAVLink FTP advertised on an unsigned link",
                "The vehicle advertises MAV_PROTOCOL_CAPABILITY_FTP and this link accepts unauthenticated peers, "
                "so the file-transfer service is reachable without the signing key.",
                name, ["Annex I.I.2(d) protection from unauthorised access", "Annex I.I.2(j) limit attack surface"],
                "Enable signing; disable or restrict MAVLink FTP in production builds where not needed.",
                matching(ep.autopilot, "ftp_unsigned", ep.firmware_tuple),
            ))
        if ep.firmware:
            findings.append(Finding(
                "MAV-007", "info", "Firmware version identified",
                f"{ep.autopilot} firmware {ep.firmware}. Track it against vendor advisories and the SBOM.",
                name, ["Annex I.I.2(a) no known exploitable vulnerabilities", "Annex I.II.1 SBOM"],
                "Keep firmware on a supported release and monitor advisories (NVD, vendor GHSA).",
            ))
        findings.append(Finding(
            "MAV-004", "info", "No link-layer confidentiality",
            "MAVLink signing provides integrity only; payloads (position, mission, parameters) "
            "are sent in clear unless the radio link is encrypted.",
            name, ["Annex I.I.2(e) confidentiality"],
            "Use an encrypted datalink (e.g. AES-capable radio) or a VPN/tunnel for IP links; assess per threat model.",
        ))
    if unsigned_probe and unsigned_probe.get("answered"):
        ep = observer.endpoints.get((unsigned_probe.get("sysid"), unsigned_probe.get("compid", 1)))
        note = ""
        if ep is not None and ep.frames and ep.signed_frames == ep.frames:
            note = (" Note: every frame sent by the vehicle on this link is signed, so a passive check "
                    "alone would wrongly suggest the link is protected (typical of a signing-exempt "
                    "port such as USB/console).")
        findings.append(Finding(
            "MAV-005", "high", "Vehicle answers unsigned requests",
            f"An unsigned PARAM_REQUEST_READ ({unsigned_probe.get('param')}) was answered by system "
            f"{unsigned_probe.get('sysid')} with {unsigned_probe.get('response')}. Unsigned peers are "
            "served by the parameter protocol, so they can at least read configuration." + note,
            f"{unsigned_probe.get('sysid')}/{unsigned_probe.get('compid', 1)}",
            ["Annex I.I.2(d) protection from unauthorised access", "Annex I.I.2(j) limit attack surface"],
            "Enable signing on the vehicle so unsigned messages are rejected.",
        ))
    return findings


def max_severity(findings: list[Finding]) -> str:
    if not findings:
        return "info"
    return max((f.severity for f in findings), key=lambda s: SEVERITY_ORDER[s])
