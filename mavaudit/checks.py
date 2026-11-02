"""Observation and findings logic.

The auditor never needs the signing key. It inspects frame headers:
- MAVLink 1 frames start with 0xFE and cannot carry a signature.
- MAVLink 2 frames start with 0xFD; bit 0 of incompat_flags marks a signed frame.

CRA mapping refers to Regulation (EU) 2024/2847, Annex I, Part I, point 2.
It is the author's technical interpretation, not legal advice.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict

MAVLINK_IFLAG_SIGNED = 0x01

AUTOPILOTS = {0: "generic", 3: "ardupilot", 8: "invalid", 12: "px4"}

# Components that are not the vehicle itself (GCS etc.) are still reported.
MAV_TYPE_GCS = 6


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

    def to_dict(self) -> dict:
        d = asdict(self)
        d["msg_types"] = sorted(self.msg_types)
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


class Observer:
    """Accumulates statistics from parsed pymavlink messages."""

    def __init__(self) -> None:
        self.endpoints: dict[tuple[int, int], EndpointStats] = {}

    def observe(self, msg) -> None:
        if msg.get_type() == "BAD_DATA":
            return
        sysid, compid = msg.get_srcSystem(), msg.get_srcComponent()
        ep = self.endpoints.setdefault((sysid, compid), EndpointStats(sysid, compid))
        ep.frames += 1
        ep.msg_types.add(msg.get_type())
        buf = msg.get_msgbuf()
        if buf and buf[0] == 0xFE:
            ep.v1_frames += 1
        else:
            ep.v2_frames += 1
            header = getattr(msg, "_header", None)
            if header is not None and header.incompat_flags & MAVLINK_IFLAG_SIGNED:
                ep.signed_frames += 1
        if msg.get_type() == "HEARTBEAT":
            ep.autopilot = AUTOPILOTS.get(msg.autopilot, f"id{msg.autopilot}")
            ep.mav_type = msg.type


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
            ))
        elif unsigned:
            findings.append(Finding(
                "MAV-003", "medium", "Mixed signed and unsigned frames",
                f"{unsigned}/{ep.frames} frames are unsigned while others are signed. "
                "Check whether the receiver accepts unsigned messages.",
                name, ["Annex I.I.2(f) integrity"],
                "Reject unsigned messages except the minimum allowed by the signing spec (e.g. RADIO_STATUS).",
            ))
        findings.append(Finding(
            "MAV-004", "info", "No link-layer confidentiality",
            "MAVLink signing provides integrity only; payloads (position, mission, parameters) "
            "are sent in clear unless the radio link is encrypted.",
            name, ["Annex I.I.2(e) confidentiality"],
            "Use an encrypted datalink (e.g. AES-capable radio) or a VPN/tunnel for IP links; assess per threat model.",
        ))
    if unsigned_probe and unsigned_probe.get("answered"):
        findings.append(Finding(
            "MAV-005", "high", "Vehicle answers unsigned requests",
            f"An unsigned PARAM_REQUEST_READ for {unsigned_probe.get('param')!r} was answered by "
            f"system {unsigned_probe.get('sysid')}. Unsigned peers can at least read configuration.",
            f"{unsigned_probe.get('sysid')}/1",
            ["Annex I.I.2(d) protection from unauthorised access", "Annex I.I.2(j) limit attack surface"],
            "Enable signing on the vehicle so unsigned messages are rejected.",
        ))
    return findings
