"""Command line entry point.

Examples (simulator on the same machine):
    mavaudit scan --target udpin:127.0.0.1:14550 --duration 15
    mavaudit scan --target tcp:127.0.0.1:5760 --active-probe --out reports/E1
    mavaudit scan --target tcp:127.0.0.1:5760 --fail-on high      # CI gate
"""

from __future__ import annotations

import argparse
import sys
import time

from pymavlink import mavutil

from . import __version__
from . import report as rpt
from .checks import SEVERITY_ORDER, Observer, evaluate, max_severity
from .safety import ScopeError, check_scope

PROBE_AUTOPILOTS = ("ardupilot", "px4")
MAV_CMD_REQUEST_MESSAGE = 512
# "all" merges common, development, ardupilotmega and others, so PX4 and ArduPilot
# specific messages decode instead of appearing as UNKNOWN_<id>.
DIALECT = "all"
MSG_AUTOPILOT_VERSION = 148


def _count_type(observer: Observer, ep, mtype: str) -> int:
    return observer.endpoints[(ep.sysid, ep.compid)].type_counts.get(mtype, 0)


def _first_vehicle(observer: Observer):
    vehicles = [ep for ep in observer.endpoints.values() if ep.autopilot in PROBE_AUTOPILOTS]
    return vehicles[0] if vehicles else None


def _collect(conn, observer: Observer, seconds: float, want: str | None = None, sysid: int | None = None):
    """Read for `seconds`, feeding the observer. Return the first `want` message from `sysid`."""
    found = None
    deadline = time.time() + seconds
    while time.time() < deadline:
        msg = conn.recv_match(blocking=True, timeout=0.3)
        if msg is None:
            continue
        observer.observe(msg)
        if found is None and want and msg.get_type() == want and msg.get_srcSystem() == sysid:
            found = msg
    return found


def _active_checks(conn, observer: Observer) -> dict | None:
    """Two read-only, unsigned requests to the first autopilot seen:
    1. PARAM_REQUEST_READ for a harmless system-ID parameter.
    2. MAV_CMD_REQUEST_MESSAGE for AUTOPILOT_VERSION (firmware + capabilities).
    """
    ep = _first_vehicle(observer)
    if ep is None:
        return None
    # Request by index 0 so the probe does not depend on parameter names, which change
    # between releases (e.g. ArduPilot 4.7 renamed SYSID_THISMAV to MAV_SYSID).
    param = "index:0"
    before_err = _count_type(observer, ep, "PARAM_ERROR")
    conn.mav.param_request_read_send(ep.sysid, ep.compid, b"", 0)
    reply = _collect(conn, observer, 3.0, "PARAM_VALUE", ep.sysid)
    errored = _count_type(observer, ep, "PARAM_ERROR") > before_err
    answered = reply is not None or errored
    conn.mav.command_long_send(ep.sysid, ep.compid, MAV_CMD_REQUEST_MESSAGE, 0,
                               MSG_AUTOPILOT_VERSION, 0, 0, 0, 0, 0, 0)
    _collect(conn, observer, 2.0, "AUTOPILOT_VERSION", ep.sysid)
    response = "PARAM_VALUE" if reply is not None else ("PARAM_ERROR" if errored else None)
    return {"sysid": ep.sysid, "compid": ep.compid, "param": param, "answered": answered, "response": response}


def scan(args) -> int:
    try:
        check_scope(args.target, args.authorized, args.scope_ref)
    except ScopeError as e:
        print(f"[scope] {e}", file=sys.stderr)
        return 2

    conn = mavutil.mavlink_connection(args.target, source_system=args.source_system, dialect=DIALECT)
    conn.mav.robust_parsing = True
    observer = Observer()
    _collect(conn, observer, args.duration)

    probe = _active_checks(conn, observer) if args.active_probe else None
    findings = evaluate(observer, probe)
    report = rpt.build(args.target, args.duration, observer, findings, args.scope_ref, probe)

    if args.out:
        rpt.write(report, args.out)
        print(f"Wrote {args.out}.json and {args.out}.md")
    elif args.json:
        print(rpt.to_json(report))
    else:
        print(rpt.to_markdown(report))
    try:
        conn.close()
    except Exception:
        pass
    if not observer.endpoints:
        print("No MAVLink traffic observed. Is the simulator running and the port right?", file=sys.stderr)
        return 1
    if args.fail_on and SEVERITY_ORDER[max_severity(findings)] >= SEVERITY_ORDER[args.fail_on]:
        return 3
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="mavaudit", description="Defensive MAVLink configuration auditor")
    p.add_argument("--version", action="version", version=f"mavaudit {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan", help="Observe a MAVLink link and report security findings")
    s.add_argument("--target", required=True,
                   help="pymavlink connection string, e.g. udpin:127.0.0.1:14550 or tcp:127.0.0.1:5760")
    s.add_argument("--duration", type=float, default=10.0, help="Passive observation window in seconds")
    s.add_argument("--active-probe", action="store_true",
                   help="Send two unsigned, read-only requests (one parameter read, one AUTOPILOT_VERSION request)")
    s.add_argument("--source-system", type=int, default=250, help="System ID used by mavaudit (default 250)")
    s.add_argument("--authorized", action="store_true", help="Target is covered by written authorisation")
    s.add_argument("--scope-ref", help="Engagement / authorisation reference recorded in the report")
    s.add_argument("--out", help="Write <out>.json and <out>.md instead of printing")
    s.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    s.add_argument("--fail-on", choices=list(SEVERITY_ORDER), help="Exit 3 if any finding is at or above this severity")
    args = p.parse_args(argv)
    return scan(args)


if __name__ == "__main__":
    sys.exit(main())
