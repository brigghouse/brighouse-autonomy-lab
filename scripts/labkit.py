"""Shared helpers for the reproducible SITL experiments.

Everything here talks only to simulators on 127.0.0.1. Provisioning a signing key is
the *defender's* configuration step (what a manufacturer or operator does), done over
the local simulated link.
"""

from __future__ import annotations

import hashlib
import re
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

os.environ.setdefault("MAVLINK20", "1")
from pymavlink import mavutil  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from mavaudit import cli as mavaudit_cli  # noqa: E402

LAB_PASSPHRASE = "brighouse-lab-demo-key"  # demo key for simulators only


def lab_key(passphrase: str = LAB_PASSPHRASE) -> bytes:
    return hashlib.sha256(passphrase.encode()).digest()


def mavlink_timestamp() -> int:
    """MAVLink signing timestamp: 10 µs units since 2015-01-01 00:00:00 UTC."""
    return int((time.time() - 1420070400) * 100_000)


def wait_tcp(port: int, timeout: float = 60.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket() as s:
            s.settimeout(1)
            if s.connect_ex(("127.0.0.1", port)) == 0:
                return
        time.sleep(0.5)
    raise TimeoutError(f"port {port} not listening")


def wait_heartbeat(conn, timeout: float = 30.0):
    hb = conn.wait_heartbeat(timeout=timeout)
    if hb is None:
        raise TimeoutError("no heartbeat")
    return hb


def provision_signing(connection: str, key: bytes, target_system: int = 1, target_component: int = 1,
                      signed: bool = False) -> None:
    """Send SETUP_SIGNING over a local simulated link (defender configuration step).
    If `signed` is true the request itself is signed with `key` (needed by stacks that
    only accept key changes from an already-keyed peer)."""
    conn = mavutil.mavlink_connection(connection, source_system=255, dialect="all")
    wait_heartbeat(conn)
    if signed:
        conn.setup_signing(key, sign_outgoing=True)
    for _ in range(3):
        conn.mav.setup_signing_send(target_system, target_component, list(key), mavlink_timestamp())
        time.sleep(0.3)
    time.sleep(1.0)
    conn.close()


def audit(target: str, out: Path, duration: float = 15.0) -> dict:
    rc = mavaudit_cli.main(["scan", "--target", target, "--duration", str(duration),
                            "--active-probe", "--out", str(out)])
    report = json.loads(Path(f"{out}.json").read_text())
    report["_exit_code"] = rc
    return report


def keyed_check(target: str, key: bytes, seconds: float = 8.0) -> dict:
    """Connect WITH the key and count frames whose signature verifies (sanity check)."""
    conn = mavutil.mavlink_connection(target, source_system=254, dialect="all")
    conn.setup_signing(key, sign_outgoing=True, allow_unsigned_callback=lambda mav, msgid: True)
    good = total = unknown = 0
    deadline = time.time() + seconds
    while time.time() < deadline:
        m = conn.recv_match(blocking=True, timeout=0.5)
        if m is None or m.get_type() == "BAD_DATA":
            continue
        if m.get_type().startswith("UNKNOWN_"):
            # pymavlink cannot verify signatures of message IDs missing from its dialect
            unknown += 1
            continue
        total += 1
        good += int(m.get_signed())
    conn.close()
    return {"frames_decoded": total, "valid_signatures": good, "unknown_msgid_frames_skipped": unknown}


def git_rev(path: Path) -> str:
    try:
        sha = subprocess.check_output(["git", "-C", str(path), "rev-parse", "--short=12", "HEAD"], text=True).strip()
        tags = subprocess.check_output(["git", "-C", str(path), "tag", "--points-at", "HEAD"], text=True).split()
        versioned = [t for t in tags if re.search(r"\d+\.\d+", t)][:3]
        return f"{','.join(versioned) or 'untagged'}@{sha}"
    except Exception:
        return "unknown"


def summarise(report: dict) -> dict:
    eps = [e for e in report["endpoints"] if e["autopilot"] in ("ardupilot", "px4")]
    ep = eps[0] if eps else None
    return {
        "exit_code": report.get("_exit_code"),
        "frames": ep["frames"] if ep else 0,
        "signed_frames": ep["signed_frames"] if ep else 0,
        "v1_frames": ep["v1_frames"] if ep else 0,
        "unsigned_types": ep["unsigned_types"] if ep else [],
        "firmware": ep["firmware"] if ep else None,
        "ftp_advertised": ep["ftp_advertised"] if ep else None,
        "unsigned_probe_answered": (report.get("unsigned_probe") or {}).get("answered"),
        "findings": sorted({f["id"] for f in report["findings"]}),
    }
