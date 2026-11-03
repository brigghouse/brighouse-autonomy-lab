"""What surface does a stock build expose to an unauthenticated peer, per release?

Not a rediscovery of known vulnerabilities (CVE-2026-32709 is an FTP path traversal,
CVE-2026-1579 unauthenticated shell access via SERIAL_CONTROL). The question here is
narrower and longitudinal: *how much surface does each release serve, by default, to a
peer that has presented no credential?* That is a property of the shipped configuration,
and it is what a conformance file has to state.

Three kinds of evidence, labelled as such because they are not equally strong:

  advertised  the endpoint's AUTOPILOT_VERSION capability bits say the protocol exists.
  answered    we asked and it replied. Strictly read-only: a PARAM_REQUEST_READ for one
              parameter, and an FTP ListDirectory, which reads a directory listing from
              our own simulator and writes nothing.
  static      found by inspecting the build on disk, not by talking to it. Used for the
              shell served over SERIAL_CONTROL, which we deliberately do not exercise:
              opening a shell is not a read-only probe, so we report only whether the
              module is compiled in.

    python scripts/surface_probe.py --target tcp:127.0.0.1:5760 --stack ardupilot \
        --version 4.7.2 --build-dir /path/to/build --out results/surface
"""

from __future__ import annotations

import argparse
import json
import struct
import subprocess
import time
from pathlib import Path

from pymavlink import mavutil

CAPS = {"ftp": 32, "mavlink2": 8192, "mission_int": 4, "flight_termination": 2048,
        "param_float": 2, "command_int": 8, "set_position_target": 256}

FTP_OPCODE_LIST = 3
FTP_ACK, FTP_NAK = 128, 129


def _ftp_list_payload(path: bytes = b"/", seq: int = 1) -> list[int]:
    """A ListDirectory request. Reads a directory listing; writes nothing."""
    data = path + b"\x00"
    hdr = struct.pack("<HBBBBBBI", seq, 0, FTP_OPCODE_LIST, len(data), 0, 0, 0, 0)
    buf = hdr + data
    return list(buf.ljust(251, b"\x00"))


def probe(target: str, timeout: float = 6.0) -> dict:
    if "127.0.0.1" not in target and "localhost" not in target:
        raise ValueError(f"local simulators only, refusing {target!r}")
    conn = mavutil.mavlink_connection(target, source_system=249, dialect="all")
    hb = conn.wait_heartbeat(timeout=30)
    out: dict = {"heartbeat": hb is not None, "advertised": {}, "answered": {}}

    # --- advertised: capability bits ---
    conn.mav.command_long_send(1, 1, mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE, 0,
                               mavutil.mavlink.MAVLINK_MSG_ID_AUTOPILOT_VERSION,
                               0, 0, 0, 0, 0, 0)
    deadline = time.time() + timeout
    caps = None
    while time.time() < deadline and caps is None:
        m = conn.recv_match(type="AUTOPILOT_VERSION", blocking=True, timeout=0.5)
        if m is not None:
            caps = int(m.capabilities)
    out["capabilities_raw"] = caps
    for name, bit in CAPS.items():
        out["advertised"][name] = None if caps is None else bool(caps & bit)

    # --- answered: one parameter read (read-only) ---
    conn.mav.param_request_read_send(1, 1, b"", 0)
    deadline, got = time.time() + timeout, False
    while time.time() < deadline and not got:
        m = conn.recv_match(type="PARAM_VALUE", blocking=True, timeout=0.5)
        if m is not None and int(getattr(m, "param_index", -2)) == 0:
            got = True
    out["answered"]["param_read"] = got

    # --- answered: FTP directory listing (read-only) ---
    conn.mav.file_transfer_protocol_send(0, 1, 1, _ftp_list_payload())
    deadline, ftp = time.time() + timeout, None
    while time.time() < deadline and ftp is None:
        m = conn.recv_match(type="FILE_TRANSFER_PROTOCOL", blocking=True, timeout=0.5)
        if m is None:
            continue
        p = bytes(m.payload)
        opcode, req_opcode = p[3], p[5]
        if req_opcode != FTP_OPCODE_LIST:
            continue
        if opcode == FTP_ACK:
            ftp = {"result": "ack", "entries_bytes": int(p[4])}
        elif opcode == FTP_NAK:
            ftp = {"result": "nak", "error_code": int(p[8]) if len(p) > 8 else None}
    out["answered"]["ftp_list"] = ftp
    conn.close()
    return out


def static_shell(build_dir: Path | None) -> dict:
    """Is a shell over SERIAL_CONTROL compiled into this build? Inspected, not exercised."""
    if build_dir is None or not build_dir.exists():
        return {"checked": False, "reason": "no build directory given"}
    hits = {}
    for name, needle in (("mavlink_shell", "mavlink_shell"),
                         ("serial_control", "SERIAL_CONTROL")):
        try:
            r = subprocess.run(["grep", "-rl", needle, str(build_dir)],
                               capture_output=True, text=True, timeout=120)
            hits[name] = bool(r.stdout.strip())
        except Exception as e:  # noqa: BLE001
            hits[name] = f"error: {e!r}"
    return {"checked": True, "method": "string search in build tree", "hits": hits,
            "note": "compiled-in only; we do not open a shell (not a read-only probe)"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--target", required=True)
    p.add_argument("--stack", required=True)
    p.add_argument("--version", required=True)
    p.add_argument("--build-dir", type=Path)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    r = probe(a.target)
    r.update({"stack": a.stack, "version": a.version, "target": a.target,
              "static": static_shell(a.build_dir),
              "recorded_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "evidence_kinds": {"advertised": "capability bits",
                                 "answered": "read-only request answered",
                                 "static": "build inspected, not exercised"},
              "not_measured": ["whether FTP can traverse paths or write (never attempted)",
                               "whether a shell can be opened (deliberately not attempted)",
                               "post-arming behaviour; all probes are on a disarmed vehicle"]})
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / f"surface-{a.stack}-{a.version}.json").write_text(json.dumps(r, indent=2))
    print(json.dumps({k: r[k] for k in ("stack", "version", "advertised", "answered")}, indent=2))


if __name__ == "__main__":
    main()
