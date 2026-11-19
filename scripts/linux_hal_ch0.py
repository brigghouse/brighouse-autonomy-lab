"""The Linux case of ArduPilot issue #34489, on the Linux HAL itself, master vs PR #34780.

Issue #34489 was opened for Linux boards (Parrot Bebop), where the documented start-up
command puts the Wi-Fi UDP link on SERIAL0 and so on MAVLink channel 0. SITL cannot show
that case: with PR #34780, SITL keeps SERIAL0 as its stand-in for USB. Here we build
ArduPilot for the generic Linux board (`./waf configure --board linux`) and run it on an
x86 host, with the same commit with and without the PR.

There is no sensor hardware, so the vehicle stops in AP_BoardConfig's config-error loop
("Baro: unable to initialise driver"). That loop keeps servicing MAVLink
(gcs().update_receive / update_send): the vehicle sends HEARTBEAT, answers
PARAM_REQUEST_READ and handles SETUP_SIGNING. The signing decision is taken while a frame
is parsed, in the MAVLink library's accept_unsigned_callback hook, before any
vehicle-state logic, so the stalled vehicle exercises the same acceptance path. The
limits section of results/linux-hal-ch0/README.md says what this does not show.

  L1  SERIAL0 = UDP (as on the Bebop), SERIAL1 = TCP
  L2  SERIAL0 = TCP, SERIAL1 = UDP              same transports, swapped

The vehicle's persistent storage (/var/lib/ardupilot, which holds parameters and the
signing key) is wiped before every run, so no key carries over between builds.
Run as root on a disposable host or container.

    python scripts/linux_hal_ch0.py --master ~/ap-master-linux --pr ~/ap-pr-linux \\
        --out results/linux-hal-ch0
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import labkit
from ch0_configs import _case, probe
from mavaudit.model.configs import ARDUPILOT_472, ARDUPILOT_PR34780_NON_USB

STATE_DIR = Path("/var/lib/ardupilot")

CONFIGS = {
    "L1-ser0udp-ser1tcp": {"args": ["--serial0", "udp:127.0.0.1:14650",
                                    "--serial1", "tcp:127.0.0.1:5771"],
                           "ch0": "udpin:127.0.0.1:14650", "ch1": "tcp:127.0.0.1:5771"},
    "L2-ser0tcp-ser1udp": {"args": ["--serial0", "tcp:127.0.0.1:5770",
                                    "--serial1", "udp:127.0.0.1:14651"],
                           "ch0": "tcp:127.0.0.1:5770", "ch1": "udpin:127.0.0.1:14651"},
}


def policy_for(build: str):
    # master trusts channel 0 whatever it is; with the PR no Linux port reports USB.
    return ARDUPILOT_472 if build == "master" else ARDUPILOT_PR34780_NON_USB


def start(binary: Path, workdir: Path, cfg: dict) -> subprocess.Popen:
    if STATE_DIR.exists():
        shutil.rmtree(STATE_DIR)
    log = open(workdir / "ardupilot.log", "w")
    proc = subprocess.Popen([str(binary), *cfg["args"]], cwd=workdir,
                            stdout=log, stderr=subprocess.STDOUT)
    for link in ("ch0", "ch1"):
        if cfg[link].startswith("tcp:"):
            labkit.wait_tcp(int(cfg[link].rsplit(":", 1)[1]))
    time.sleep(3)
    return proc


def run_config(build: str, name: str, cfg: dict, root: Path) -> dict:
    policy = policy_for(build)
    workdir = Path(tempfile.mkdtemp(prefix=f"aplinux-{build}-{name}-"))
    key = labkit.lab_key()
    proc = start(root / "build/linux/bin/arducopter", workdir, cfg)
    cases = []
    try:
        for link in ("ch0", "ch1"):
            r = probe(cfg, link, False, None)
            cases.append(_case(r, policy, cfg, link, state="unkeyed", signed=False, keyed=False))
        labkit.provision_signing(cfg["ch0"], key)
        for link in ("ch0", "ch1"):
            for signed in (False, True):
                r = probe(cfg, link, signed, key)
                cases.append(_case(r, policy, cfg, link, state="keyed", signed=signed, keyed=True))
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
    log = (workdir / "ardupilot.log").read_text(errors="replace")
    for c in cases:
        c["agree"] = None if c["verdict"] == "inconclusive" else c["predicted"] == c["observed"]
    decided = [c for c in cases if c["agree"] is not None]
    return {"build": build, "config": name, "args": cfg["args"], "policy": policy.name,
            "keyed_unsigned_read": {c["link"]: c["verdict"] for c in cases
                                    if c["state"] == "keyed" and not c["signed"]},
            "vehicle_log_tail": log[-600:],
            "cases": cases, "agree": sum(c["agree"] for c in decided),
            "total": len(decided), "inconclusive": len(cases) - len(decided)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--master", type=Path, required=True)
    p.add_argument("--pr", type=Path, required=True)
    p.add_argument("--out", type=Path, default=labkit.REPO / "results/linux-hal-ch0")
    p.add_argument("--name", default="linux-hal-ch0.json")
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    res = {"stack": "ArduPilot Copter, Linux HAL (--board linux) on an x86-64 host",
           "pr": "ArduPilot/ardupilot#34780",
           "master_rev": labkit.git_rev(a.master), "pr_rev": labkit.git_rev(a.pr),
           "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "runs": []}
    for build, root in (("master", a.master), ("pr34780", a.pr)):
        for name, cfg in CONFIGS.items():
            r = run_config(build, name, cfg, root)
            res["runs"].append(r)
            print(build, name, f"{r['agree']}/{r['total']}", "inconclusive", r["inconclusive"],
                  r["keyed_unsigned_read"], flush=True)
            (a.out / a.name).write_text(json.dumps(res, indent=2))
            time.sleep(2)


if __name__ == "__main__":
    main()
