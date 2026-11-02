"""Command line entry point.

Examples (simulator on the same machine):
    python -m mavaudit scan --target udpin:127.0.0.1:14550 --duration 15
    python -m mavaudit scan --target udpin:127.0.0.1:14550 --active-probe --out report
"""

from __future__ import annotations

import argparse
import sys
import time

from pymavlink import mavutil

from . import report as rpt
from .checks import Observer, evaluate
from .safety import ScopeError, check_scope

PROBE_PARAMS = {"ardupilot": "SYSID_THISMAV", "px4": "MAV_SYS_ID"}


def _unsigned_probe(conn, observer: Observer, timeout: float = 3.0) -> dict | None:
    """Send one unsigned, read-only PARAM_REQUEST_READ to the first autopilot seen."""
    vehicles = [ep for ep in observer.endpoints.values() if ep.autopilot in PROBE_PARAMS]
    if not vehicles:
        return None
    ep = vehicles[0]
    param = PROBE_PARAMS[ep.autopilot]
    conn.mav.param_request_read_send(ep.sysid, ep.compid, param.encode(), -1)
    deadline = time.time() + timeout
    while time.time() < deadline:
        msg = conn.recv_match(type="PARAM_VALUE", blocking=True, timeout=0.5)
        if msg is not None and msg.get_srcSystem() == ep.sysid:
            return {"sysid": ep.sysid, "param": param, "answered": True}
    return {"sysid": ep.sysid, "param": param, "answered": False}


def scan(args) -> int:
    try:
        check_scope(args.target, args.authorized, args.scope_ref)
    except ScopeError as e:
        print(f"[scope] {e}", file=sys.stderr)
        return 2

    conn = mavutil.mavlink_connection(args.target, source_system=args.source_system, dialect="ardupilotmega")
    conn.mav.robust_parsing = True
    observer = Observer()
    end = time.time() + args.duration
    while time.time() < end:
        msg = conn.recv_match(blocking=True, timeout=0.5)
        if msg is not None:
            observer.observe(msg)

    probe = _unsigned_probe(conn, observer) if args.active_probe else None
    findings = evaluate(observer, probe)
    report = rpt.build(args.target, args.duration, observer, findings, args.scope_ref, probe)

    if args.out:
        with open(f"{args.out}.json", "w", encoding="utf-8") as fh:
            fh.write(rpt.to_json(report))
        with open(f"{args.out}.md", "w", encoding="utf-8") as fh:
            fh.write(rpt.to_markdown(report))
        print(f"Wrote {args.out}.json and {args.out}.md")
    else:
        print(rpt.to_markdown(report))
    if not observer.endpoints:
        print("No MAVLink traffic observed. Is the simulator running and the port right?", file=sys.stderr)
        return 1
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="mavaudit", description="Defensive MAVLink configuration auditor")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan", help="Observe a MAVLink link and report security findings")
    s.add_argument("--target", required=True, help="pymavlink connection string, e.g. udpin:127.0.0.1:14550")
    s.add_argument("--duration", type=float, default=10.0, help="Observation window in seconds")
    s.add_argument("--active-probe", action="store_true",
                   help="Send ONE unsigned read-only PARAM_REQUEST_READ to test whether unsigned requests are answered")
    s.add_argument("--source-system", type=int, default=250, help="System ID used by mavaudit (default 250)")
    s.add_argument("--authorized", action="store_true", help="Target is covered by written authorisation")
    s.add_argument("--scope-ref", help="Engagement / authorisation reference recorded in the report")
    s.add_argument("--out", help="Write <out>.json and <out>.md instead of printing")
    args = p.parse_args(argv)
    return scan(args)


if __name__ == "__main__":
    sys.exit(main())
