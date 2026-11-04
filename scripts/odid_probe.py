"""Does the autopilot accept Remote ID messages from an unauthenticated peer?

ArduPilot carries an OpenDroneID subsystem (ASTM F3411 Remote ID) that takes its identity
and operator data over MAVLink, from a ground station or a Remote ID module. The question
this probe answers is narrow and measurable: *who is allowed to set it?*

The observable is ArduPilot's own pre-arm check, which fails with a different message
depending on how far the Remote ID state has been populated:

    DID_ENABLE must be 1  ->  UA_TYPE required in BasicID  ->  operator location must be set
    ->  ARM_STATUS not available  ->  SYSTEM not available  ->  (good to arm)

Each message the autopilot *accepts* advances that text to the next rung. So sending one
Remote ID message and watching the pre-arm text change is a read-only test of acceptance:
we never arm, we never command anything, we read a status string the vehicle already emits.

Scope. We run against a local simulator that this script starts and stops. The Remote ID
messages we send are the ones a legitimate ground station or module sends; the point is not
that they do something dangerous on their own, but that the vehicle takes them from a peer
that has presented no credential. The radio side of Remote ID -- what an observer actually
receives over Bluetooth or Wi-Fi -- is not measured here and needs hardware we do not have.

    python scripts/odid_probe.py --ardupilot ~/sitl/ardupilot --out results/odid
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
import time
from pathlib import Path

import labkit
from pymavlink import mavutil

TCP0, TCP1 = 5760, 5762
# DID_OPTIONS bit 0 = EnforcePreArmChecks (AP_OpenDroneID.h, Options enum)
ENFORCE_PREARM = 1


def start_sitl(ap: Path, workdir: Path) -> subprocess.Popen:
    cmd = [str(ap / "build/sitl/bin/arducopter"), "--model", "+", "--speedup", "1", "-I0", "-w",
           "--defaults", str(ap / "Tools/autotest/default_params/copter.parm"),
           "--serial1", "tcp:2"]
    log = open(workdir / "sitl.log", "w")
    proc = subprocess.Popen(cmd, cwd=workdir, stdout=log, stderr=subprocess.STDOUT,
                            start_new_session=True)
    labkit.wait_tcp(TCP0)
    return proc


def set_param(conn, name: str, value: float, ptype=mavutil.mavlink.MAV_PARAM_TYPE_INT32):
    """Configure our own simulator. Not part of the measurement: this is the setup a
    manufacturer would ship with Remote ID switched on."""
    conn.mav.param_set_send(1, 1, name.encode(), value, ptype)
    deadline = time.time() + 5
    while time.time() < deadline:
        m = conn.recv_match(type="PARAM_VALUE", blocking=True, timeout=0.5)
        if m is not None and m.param_id.strip("\x00") == name:
            return float(m.param_value)
    return None


def prearm_text(conn, timeout: float = 14.0) -> str | None:
    """Read the pre-arm failure text the vehicle emits. Read-only: we ask the vehicle to
    run its own checks and report, we do not arm and we change nothing."""
    conn.mav.command_long_send(1, 1, mavutil.mavlink.MAV_CMD_RUN_PREARM_CHECKS,
                               0, 0, 0, 0, 0, 0, 0, 0)
    deadline = time.time() + timeout
    seen = []
    while time.time() < deadline:
        m = conn.recv_match(type="STATUSTEXT", blocking=True, timeout=0.5)
        if m is None:
            continue
        txt = m.text.strip() if isinstance(m.text, str) else m.text.decode(errors="replace").strip()
        seen.append(txt)
        if "PreArm" in txt or "ODID" in txt:
            return txt
    return seen[-1] if seen else None


ZERO20 = [0] * 20


def _pad20(text: str) -> list[int]:
    b = text.encode()[:20]
    return list(b) + [0] * (20 - len(b))


def send_basic_id(conn, uas_id: str = "PROBE-ID-0000000000"):
    conn.mav.open_drone_id_basic_id_send(
        1, 1, ZERO20,
        mavutil.mavlink.MAV_ODID_ID_TYPE_SERIAL_NUMBER,
        mavutil.mavlink.MAV_ODID_UA_TYPE_HELICOPTER_OR_MULTIROTOR,
        _pad20(uas_id))


def send_system(conn, lat=473977418, lon=85455938):
    conn.mav.open_drone_id_system_send(
        1, 1, ZERO20,
        mavutil.mavlink.MAV_ODID_OPERATOR_LOCATION_TYPE_TAKEOFF,
        mavutil.mavlink.MAV_ODID_CLASSIFICATION_TYPE_EU,
        lat, lon, 1, 0, 0.0, 0.0,
        mavutil.mavlink.MAV_ODID_CATEGORY_EU_OPEN,
        mavutil.mavlink.MAV_ODID_CLASS_EU_CLASS_1,
        0.0, 0)


def connect(target: str, sysid: int, key: bytes | None = None):
    conn = mavutil.mavlink_connection(target, source_system=sysid, dialect="all")
    conn.wait_heartbeat(timeout=30)
    if key is not None:
        conn.setup_signing(key, sign_outgoing=True, allow_unsigned_callback=lambda m, i: True)
    return conn


def wait_for_odid_prearm(conn, timeout: float = 180.0) -> str | None:
    """A freshly booted simulator fails its sensor pre-arms first (accelerometers, EKF,
    AHRS), which masks the Remote ID check behind them. Poll until the vehicle's first
    complaint IS the Remote ID one; only then is the observable usable. If it never gets
    there, the measurement is void and we say so rather than reading a masked result."""
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        last = prearm_text(conn)
        if last and "OpenDroneID" in last:
            return last
        time.sleep(3)
    return None


def run(ap: Path, out: Path) -> dict:
    workdir = Path(tempfile.mkdtemp(prefix="odid-"))
    proc = start_sitl(ap, workdir)
    rec: dict = {"stack": "ardupilot", "version": "4.7.2",
                 "source_rev": labkit.git_rev(ap), "steps": [],
                 "recorded_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    try:
        cfg = connect(f"tcp:127.0.0.1:{TCP0}", 250)
        rec["did_enable"] = set_param(cfg, "DID_ENABLE", 1)
        rec["did_options"] = set_param(cfg, "DID_OPTIONS", ENFORCE_PREARM)
        time.sleep(2)
        def step(label, conn=None):
            t = prearm_text(cfg)
            rec["steps"].append({"step": label, "prearm": t})
            print(f"  {label:62s} -> {t}", flush=True)
            return t

        settled = wait_for_odid_prearm(cfg)
        rec["settled_to_odid_prearm"] = settled is not None
        if settled is None:
            rec["void"] = ("the vehicle never reached the Remote ID pre-arm check within "
                           "the timeout: sensor checks stayed in front of it, so any "
                           "reading here would be masked. No result is claimed.")
            print("  VOID: never reached the OpenDroneID pre-arm check", flush=True)
            return rec
        print(f"  settled: {settled}", flush=True)
        rec["steps"].append({"step": "baseline, Remote ID enabled, nothing sent",
                             "prearm": settled})

        # --- UNKEYED: an unsigned peer on an ordinary link ---
        att = connect(f"tcp:127.0.0.1:{TCP1}", 77)
        send_basic_id(att)
        time.sleep(1.5)
        step("unkeyed: BASIC_ID from an unsigned peer on ch1")
        send_system(att)
        time.sleep(1.5)
        step("unkeyed: SYSTEM (operator location) from the same peer")
        att.close()

        # --- KEYED: provision a key over the console, then try the same from ch1 ---
        # SITL's TCP console accepts one peer at a time, so we provision over the
        # connection we already hold rather than opening a second one.
        key = labkit.lab_key()
        for _ in range(3):
            cfg.mav.setup_signing_send(1, 1, list(key), labkit.mavlink_timestamp())
            time.sleep(0.3)
        time.sleep(1.5)
        cfg.setup_signing(key, sign_outgoing=True, allow_unsigned_callback=lambda m, i: True)
        # move the operator location so that an accepted SYSTEM is distinguishable
        att2 = connect(f"tcp:127.0.0.1:{TCP1}", 78)
        send_system(att2, lat=100000000, lon=100000000)
        time.sleep(1.5)
        step("keyed: SYSTEM from an unsigned peer on ch1 (non-exempt)")
        att2.close()

        # --- KEYED, but on the exempt console channel ---
        att3 = connect(f"tcp:127.0.0.1:{TCP0}", 79)
        send_system(att3, lat=200000000, lon=200000000)
        time.sleep(1.5)
        step("keyed: SYSTEM from an unsigned peer on ch0 (exempt)")
        att3.close()
        cfg.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()

    rec["not_measured"] = [
        "the Remote ID radio broadcast itself (Bluetooth / Wi-Fi): needs a receiver we do "
        "not have. This measures only the MAVLink path that sets the data",
        "whether a conformant observer would accept the resulting broadcast",
        "any Remote ID module's own firmware",
    ]
    out.mkdir(parents=True, exist_ok=True)
    (out / "odid-ardupilot-4.7.2.json").write_text(json.dumps(rec, indent=2))
    return rec


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ardupilot", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    r = run(a.ardupilot, a.out)
    print(json.dumps({"did_enable": r.get("did_enable"), "did_options": r.get("did_options")},
                     indent=2))
    print(f"  recorded {len(r['steps'])} steps")


if __name__ == "__main__":
    main()
