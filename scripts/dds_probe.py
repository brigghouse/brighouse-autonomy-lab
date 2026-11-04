"""Is the second control plane (uXRCE-DDS) authenticated? A passive measurement.

PX4's own documentation states that "the DDS transport is unauthenticated and reaches
uORB directly, so the DDS network must be kept isolated", and the uxrce_dds_client module
is included in SITL and most firmware by default. MAVLink message signing does not apply
to this path: a key provisioned over MAVLink protects MAVLink links only.

This probe measures the consequence without sending the flight controller anything. We
bind the agent's UDP port and listen, then decode the DDS-XRCE session header and
submessage header of whatever arrives. What the flight controller emits is a repeated
GET_INFO submessage (id 0x02) addressed to OBJECTID_AGENT (0xfffd), carried in a session
with SESSION_ID_NONE_WITHOUT_CLIENT_KEY: agent discovery, sent to whichever local process
holds the port, with no credential, key or challenge preceding it, and with no means for
the client to authenticate the agent that answers (micro XRCE-DDS in PX4 does not
implement DDS-Security).

Deliberate limits. We never answer, so no session is established, no DDS entity is
created, and no topic is read or written. This is *detection*, not exploitation: we
record that the offer arrives unauthenticated, not that we consumed it. Whether a full
agent could then read or write uORB topics follows from PX4's own documentation ("the DDS
transport is unauthenticated and reaches uORB directly"); we do not demonstrate it.

    python scripts/dds_probe.py --port 8888 --seconds 25 --out results/dds
"""

from __future__ import annotations

import argparse
import json
import socket
import time
from pathlib import Path

# DDS-XRCE (OMG) wire constants we decode.
SUBMESSAGE_IDS = {0x00: "CREATE_CLIENT", 0x01: "CREATE", 0x02: "GET_INFO", 0x03: "DELETE",
                  0x04: "STATUS_AGENT", 0x05: "STATUS", 0x06: "INFO", 0x07: "READ_DATA",
                  0x08: "WRITE_DATA", 0x09: "DATA", 0x0A: "ACKNACK", 0x0B: "HEARTBEAT"}
OBJECTID_AGENT = b"\xff\xfd"
SESSION_ID_NONE_WITHOUT_CLIENT_KEY = 0x80


def decode(dg: bytes) -> dict | None:
    """Decode the XRCE session header and the first submessage header. None if it does
    not look like XRCE at all."""
    if len(dg) < 8:
        return None
    session_id, stream_id = dg[0], dg[1]
    seq = int.from_bytes(dg[2:4], "little")
    sub_id, flags = dg[4], dg[5]
    length = int.from_bytes(dg[6:8], "little")
    # Strict: a zero-length submessage, or one whose declared length overruns the
    # datagram, is not something we will count as XRCE. Unrelated UDP traffic (an
    # all-zero datagram, say) would otherwise decode as a valid-looking submessage and
    # inflate the finding. Checked by a test.
    if sub_id not in SUBMESSAGE_IDS or length == 0 or 8 + length > len(dg):
        return None
    payload = dg[8:8 + length]
    out = {"session_id": hex(session_id), "stream_id": hex(stream_id), "sequence": seq,
           "submessage": SUBMESSAGE_IDS[sub_id], "payload_len": length,
           "session_without_client_key": session_id == SESSION_ID_NONE_WITHOUT_CLIENT_KEY}
    if len(payload) >= 4:
        out["target_object"] = payload[2:4].hex()
        out["targets_agent"] = payload[2:4] == OBJECTID_AGENT
    return out


def listen(port: int, seconds: float, bind_host: str = "127.0.0.1") -> dict:
    """Bind the agent port and record what arrives. Loopback only."""
    if bind_host not in ("127.0.0.1", "::1", "localhost"):
        raise ValueError(f"loopback only, refusing to bind {bind_host!r}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((bind_host, port))
    sock.settimeout(1.0)
    deadline = time.time() + seconds
    datagrams, peers, samples, kinds = 0, set(), [], {}
    unauth_count = 0
    while time.time() < deadline:
        try:
            data, addr = sock.recvfrom(4096)
        except socket.timeout:
            continue
        datagrams += 1
        peers.add(f"{addr[0]}:{addr[1]}")
        d = decode(data)
        if d is None:
            kinds["undecoded"] = kinds.get("undecoded", 0) + 1
            continue
        kinds[d["submessage"]] = kinds.get(d["submessage"], 0) + 1
        # The finding is computed over EVERY decoded datagram, not over a sample. An
        # earlier version kept only the first three and derived the headline from those,
        # so a capture whose first three datagrams were not agent-targeted would have
        # reported "no finding" with the evidence sitting in the discarded remainder.
        # Found by an independent reviewer.
        if d.get("session_without_client_key") and d.get("targets_agent"):
            unauth_count += 1
        if len(samples) < 3:
            d["raw_prefix_hex"] = data[:16].hex()
            samples.append(d)
    sock.close()
    xrce = sum(v for k, v in kinds.items() if k != "undecoded")
    unauth = unauth_count > 0
    return {
        "port": port,
        "listened_seconds": seconds,
        "datagrams_received": datagrams,
        "xrce_datagrams": xrce,
        "submessage_counts": kinds,
        "peers": sorted(peers),
        "samples": samples,
        "agent_discovery_datagrams": unauth_count,
        # The finding, stated as what we observed and nothing more.
        "unauthenticated_agent_discovery": unauth,
        # A capture with no traffic at all is not evidence of authentication: it is
        # equally consistent with nothing listening, the wrong port, or a bind that
        # happened after the client gave up. Flagged rather than reported as a negative.
        "inconclusive": datagrams == 0,
        "inconclusive_reason": (None if datagrams else
                                "no datagrams at all: cannot distinguish an absent or "
                                "authenticated service from a probe that listened on the "
                                "wrong port or started too late"),
        "note": ("an unauthenticated listener on the configured agent port receives "
                 "repeated XRCE agent-discovery submessages from the flight controller, "
                 "in a session with no client key; no credential, key or challenge "
                 "precedes them. We did not answer, so no session was established and no "
                 "topic was read or written."),
        "why_it_matters": ("this is a second control plane that reaches uORB directly, and "
                           "a MAVLink signing key does not apply to it: provisioning "
                           "SETUP_SIGNING protects MAVLink links only. A deployment that "
                           "has 'enabled signing' may still expose this path."),
        "not_measured": ["whether a full agent could then read or write uORB topics "
                         "(not attempted: that would require answering)",
                         "DDS-Security (the OMG standard) is not implemented by "
                         "micro XRCE-DDS in PX4; we did not test it",
                         "whether a remote (non-loopback) peer can reach the port in a "
                         "given deployment: that is an integrator's network question"],
    }


def param_present(mav_target: str, name: str, timeout: float = 8.0):
    """Is a parameter exposed by this build? Recorded because a claim about whether a
    subsystem is compiled in ought to rest on a check that is in the artefact, not on one
    the author ran once by hand. Found missing by an independent reviewer."""
    try:
        from pymavlink import mavutil
        conn = mavutil.mavlink_connection(mav_target, source_system=246, dialect="all")
        conn.wait_heartbeat(timeout=20)
        conn.mav.param_request_read_send(1, 1, name.encode(), -1)
        deadline = time.time() + timeout
        while time.time() < deadline:
            m = conn.recv_match(type="PARAM_VALUE", blocking=True, timeout=0.5)
            if m is not None and m.param_id.strip("\x00") == name:
                conn.close()
                return {"present": True, "value": float(m.param_value)}
        conn.close()
        return {"present": False, "value": None,
                "caveat": "absence of a reply within the timeout, not proof of absence"}
    except Exception as e:  # noqa: BLE001
        return {"present": None, "error": repr(e)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8888)
    p.add_argument("--seconds", type=float, default=25.0)
    p.add_argument("--stack", default="px4")
    p.add_argument("--version", default="unknown")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--param-check", help="MAVLink target to ask for --param-name")
    p.add_argument("--param-name", default="DDS_ENABLE")
    a = p.parse_args()
    r = listen(a.port, a.seconds)
    if a.param_check:
        r["parameter_check"] = {a.param_name: param_present(a.param_check, a.param_name)}
    r["stack"] = a.stack
    r["version"] = a.version
    r["recorded_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / f"dds-{a.stack}-{a.version}.json").write_text(json.dumps(r, indent=2))
    print(json.dumps({k: r[k] for k in ("stack", "version", "datagrams_received",
                                        "xrce_datagrams", "submessage_counts",
                                        "unauthenticated_agent_discovery", "peers")}, indent=2))


if __name__ == "__main__":
    main()
