"""Does ArduPilot's unsigned-accept exemption follow the *channel index* or the *link type*?

ArduPilot's `accept_unsigned_callback` (GCS_Signing.cpp) accepts any unsigned frame on
MAVLINK_COMM_0 on the assumption that channel 0 is USB. Upstream issue #34489 / PR #34780
(unmerged as of Nov 2026) note that on boards where SERIAL0 is not USB the exemption is
wrong. This script measures it in SITL by moving the *transport* of channel 0 and
channel 1 independently and observing whether an unsigned PARAM_REQUEST_READ is answered
while a signing key is active:

  A  ch0 = TCP, ch1 = TCP            baseline (same as results/conformance)
  B  ch0 = UDP, ch1 = TCP            channel 0 over a network transport
  C  ch0 = TCP, ch1 = UDP            channel 1 over the same network transport
  D  ch0 = TCP, ch1 = TCP MAVLink 1  SERIAL1_PROTOCOL=1: a MAVLink 1 port under a key

If the exemption follows the index, B accepts unsigned on ch0 and C rejects unsigned on
ch1 although both are UDP. D measures the documented "MAVLink 1 ports are not protected".

Read-only probes only (PARAM_REQUEST_READ) plus the reversible SETUP_SIGNING provisioning
step, against a local SITL that this script starts and stops itself.

    python scripts/ch0_configs.py --ardupilot ~/sitl/ardupilot --out results/ch0-configs
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

import labkit
from conformance import _probe_read
from mavaudit.model.configs import BY_NAME
from mavaudit.model.semantics import READ, Frame, State, step

UDP0, UDP1 = 14600, 14601
TCP0, TCP1 = 5760, 5762

CONFIGS = {
    "A-ch0tcp-ch1tcp": {"serial0": None, "serial1": "tcp:2", "extra": {},
                        "ch0": f"tcp:127.0.0.1:{TCP0}", "ch1": f"tcp:127.0.0.1:{TCP1}"},
    "B-ch0udp-ch1tcp": {"serial0": f"udpclient:127.0.0.1:{UDP0}", "serial1": "tcp:2", "extra": {},
                        "ch0": f"udpin:127.0.0.1:{UDP0}", "ch1": f"tcp:127.0.0.1:{TCP1}"},
    "C-ch0tcp-ch1udp": {"serial0": None, "serial1": f"udpclient:127.0.0.1:{UDP1}", "extra": {},
                        "ch0": f"tcp:127.0.0.1:{TCP0}", "ch1": f"udpin:127.0.0.1:{UDP1}"},
    "D-ch0tcp-ch1mav1": {"serial0": None, "serial1": "tcp:2", "extra": {"SERIAL1_PROTOCOL": 1},
                         "ch0": f"tcp:127.0.0.1:{TCP0}", "ch1": f"tcp:127.0.0.1:{TCP1}", "ch1_v1": True},
}


def probe(cfg: dict, link: str, signed: bool, key):
    """Read probe; on a MAVLink 1 port the probe itself is sent as MAVLink 1 (pymavlink
    picks the wire version from the MAVLINK20 environment variable at connection time).
    A MAVLink 1 frame cannot carry a signature, so `signed` is forced False there."""
    from pymavlink import mavutil
    if cfg.get(f"{link}_v1"):
        saved = os.environ.pop("MAVLINK20", None)
        mavutil.set_dialect("all")
        try:
            return _probe_read(cfg[link], False, None)
        finally:
            if saved is not None:
                os.environ["MAVLINK20"] = saved
            mavutil.set_dialect("all")
    return _probe_read(cfg[link], signed, key)


def predict(policy, link: str, signed: bool, keyed: bool) -> bool:
    st = State(key="K" if keyed else None, clock=2_000_000)
    fr = Frame(link, (9, 9) if not signed else (1, 1), READ, signed=signed,
               key="K" if signed else None, ts=2_000_050, link_id=1)
    return step(policy, st, fr).accepted


def start_sitl(ap: Path, workdir: Path, cfg: dict) -> subprocess.Popen:
    defaults = [str(ap / "Tools/autotest/default_params/copter.parm")]
    if cfg["extra"]:
        extra = workdir / "extra.parm"
        extra.write_text("".join(f"{k} {v}\n" for k, v in cfg["extra"].items()))
        defaults.append(str(extra))
    cmd = [str(ap / "build/sitl/bin/arducopter"), "--model", "+", "--speedup", "1", "-I0", "-w",
           "--defaults", ",".join(defaults), "--serial1", cfg["serial1"]]
    if cfg["serial0"]:
        cmd += ["--serial0", cfg["serial0"]]
    log = open(workdir / "sitl.log", "w")
    proc = subprocess.Popen(cmd, cwd=workdir, stdout=log, stderr=subprocess.STDOUT)
    if cfg["ch0"].startswith("tcp:"):
        labkit.wait_tcp(TCP0)
    else:
        time.sleep(3)
    return proc


def run_config(name: str, cfg: dict, ap: Path, policy) -> dict:
    workdir = Path(tempfile.mkdtemp(prefix=f"ap-{name}-"))
    key = labkit.lab_key()
    proc = start_sitl(ap, workdir, cfg)
    cases = []
    try:
        # SITL boots once SERIAL0 has a peer; one unkeyed read on ch0 also settles that.
        for link in ("ch0", "ch1"):
            obs = probe(cfg, link, False, None)
            cases.append({"state": "unkeyed", "link": link, "transport": cfg[link].split(":")[0],
                          "wire": 1 if cfg.get(f"{link}_v1") else 2, "signed": False, "predicted": predict(policy, link, False, False),
                          "observed": obs})
        labkit.provision_signing(cfg["ch0"], key)
        for link in ("ch0", "ch1"):
            for signed in ((False,) if cfg.get(f"{link}_v1") else (False, True)):
                obs = probe(cfg, link, signed, key if signed else None)
                cases.append({"state": "keyed", "link": link, "transport": cfg[link].split(":")[0],
                              "wire": 1 if cfg.get(f"{link}_v1") else 2, "signed": signed, "predicted": predict(policy, link, signed, True),
                              "observed": obs})
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
    for c in cases:
        c["agree"] = c["predicted"] == c["observed"]
    return {"config": name, "serial0": cfg["serial0"] or "tcp:0 (default)", "serial1": cfg["serial1"],
            "extra_params": cfg["extra"], "cases": cases,
            "agree": sum(c["agree"] for c in cases), "total": len(cases)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ardupilot", type=Path, required=True)
    p.add_argument("--policy", default="ardupilot-4.7.2")
    p.add_argument("--out", type=Path, default=labkit.REPO / "results/ch0-configs")
    p.add_argument("--only", nargs="*")
    a = p.parse_args()
    policy = BY_NAME[a.policy]
    a.out.mkdir(parents=True, exist_ok=True)
    results = {"stack": "ArduPilot Copter SITL", "source_rev": labkit.git_rev(a.ardupilot),
               "policy": a.policy, "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "configs": []}
    for name, cfg in CONFIGS.items():
        if a.only and name not in a.only:
            continue
        r = run_config(name, cfg, a.ardupilot, policy)
        results["configs"].append(r)
        print(name, f"{r['agree']}/{r['total']}",
              [(c["state"], c["link"], c["transport"], f"v{c['wire']}", c["signed"], c["observed"]) for c in r["cases"]])
        (a.out / "ch0-configs.json").write_text(json.dumps(results, indent=2))
        time.sleep(2)


if __name__ == "__main__":
    main()
