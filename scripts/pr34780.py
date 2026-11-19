"""Does ArduPilot PR #34780 close the channel-0 signing exemption (issue #34489)?

PR #34780 changes `accept_unsigned_callback()` so that channel 0 is exempt from MAVLink 2
signing only when its port reports `is_usb()`. In SITL the PR makes SERIAL0 stand in for
USB (`is_usb()` is `_portNumber == 0`), so SITL can exercise the fix only where channel 0
is *not* SERIAL0. That happens when SERIAL0 does not speak MAVLink: channel 0 is then the
lowest-numbered MAVLink port, here SERIAL1 -- the situation the PR description calls "the
exemption silently moves to the next MAVLink port, typically the telemetry radio".

We run the same read probe as results/ch0-configs (liveness + signed positive control, so
a negative is an observed rejection, not a timeout) against two builds of the same
ArduPilot master commit, with and without the four PR commits applied:

  A  SERIAL0 = TCP (MAVLink), ch1 = SERIAL1 TCP       documented SITL workflow, must not change
  B  SERIAL0 = UDP (MAVLink), ch1 = SERIAL1 TCP       SITL keeps SERIAL0 trusted whatever the transport
  E  SERIAL0_PROTOCOL = -1;  ch0 = SERIAL1 TCP, ch1 = SERIAL2 TCP    the case the PR fixes
  F  SERIAL0_PROTOCOL = -1;  ch0 = SERIAL1 UDP, ch1 = SERIAL2 TCP    same, over a network transport

What SITL cannot show: the Linux HAL path (Bebop, Disco), where the PR returns
`is_usb() == false` for every port. That needs a Linux board build and is out of scope.

Read-only probes (PARAM_REQUEST_READ) plus the reversible SETUP_SIGNING step, against a
local SITL started and stopped by this script.

    python scripts/pr34780.py --master ~/ap-master --pr ~/ap-pr --out results/pr34780
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import subprocess
import tempfile
import time
from pathlib import Path

import labkit
from ch0_configs import _case, probe
from mavaudit.model.configs import ARDUPILOT_472

UDP0, UDP1 = 14600, 14601

CONFIGS = {
    "A-ser0tcp": {"serials": {0: None, 1: "tcp:2"}, "extra": {},
                  "ch0": "tcp:127.0.0.1:5760", "ch1": "tcp:127.0.0.1:5762",
                  "ch0_port": "SERIAL0"},
    "B-ser0udp": {"serials": {0: f"udpclient:127.0.0.1:{UDP0}", 1: "tcp:2"}, "extra": {},
                  "ch0": f"udpin:127.0.0.1:{UDP0}", "ch1": "tcp:127.0.0.1:5762",
                  "ch0_port": "SERIAL0"},
    "E-ser0off-ch0ser1tcp": {"serials": {0: "tcp:0", 1: "tcp:2", 2: "tcp:3"},
                             "extra": {"SERIAL0_PROTOCOL": -1, "SERIAL2_PROTOCOL": 2},
                             "ch0": "tcp:127.0.0.1:5762", "ch1": "tcp:127.0.0.1:5763",
                             "ch0_port": "SERIAL1"},
    "F-ser0off-ch0ser1udp": {"serials": {0: "tcp:0", 1: f"udpclient:127.0.0.1:{UDP1}", 2: "tcp:3"},
                             "extra": {"SERIAL0_PROTOCOL": -1, "SERIAL2_PROTOCOL": 2},
                             "ch0": f"udpin:127.0.0.1:{UDP1}", "ch1": "tcp:127.0.0.1:5763",
                             "ch0_port": "SERIAL1"},
}


def policy_for(build: str, cfg: dict):
    """master: channel 0 is trusted whatever port it is (ARDUPILOT_472).
    PR: channel 0 is trusted only when it is the port SITL reports as USB, i.e. SERIAL0."""
    if build == "master" or cfg["ch0_port"] == "SERIAL0":
        return dataclasses.replace(ARDUPILOT_472, name=f"{build}-ch0-trusted")
    return dataclasses.replace(ARDUPILOT_472, name=f"{build}-no-trusted-link", trusted=frozenset())


def start_sitl(ap: Path, workdir: Path, cfg: dict) -> subprocess.Popen:
    defaults = [str(ap / "Tools/autotest/default_params/copter.parm")]
    if cfg["extra"]:
        extra = workdir / "extra.parm"
        extra.write_text("".join(f"{k} {v}\n" for k, v in cfg["extra"].items()))
        defaults.append(str(extra))
    cmd = [str(ap / "build/sitl/bin/arducopter"), "--model", "+", "--speedup", "1", "-I0", "-w",
           "--defaults", ",".join(defaults)]
    for n, dev in cfg["serials"].items():
        if dev:
            cmd += [f"--serial{n}", dev]
    log = open(workdir / "sitl.log", "w")
    proc = subprocess.Popen(cmd, cwd=workdir, stdout=log, stderr=subprocess.STDOUT)
    if cfg["ch0"].startswith("tcp:"):
        labkit.wait_tcp(int(cfg["ch0"].rsplit(":", 1)[1]))
    else:
        time.sleep(3)
    return proc


def run_config(build: str, name: str, cfg: dict, ap: Path) -> dict:
    policy = policy_for(build, cfg)
    workdir = Path(tempfile.mkdtemp(prefix=f"ap-{build}-{name}-"))
    key = labkit.lab_key()
    proc = start_sitl(ap, workdir, cfg)
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
    for c in cases:
        c["agree"] = None if c["verdict"] == "inconclusive" else c["predicted"] == c["observed"]
    decided = [c for c in cases if c["agree"] is not None]
    keyed_unsigned = {c["link"]: c["verdict"] for c in cases
                      if c["state"] == "keyed" and not c["signed"]}
    return {"build": build, "config": name, "ch0_port": cfg["ch0_port"],
            "serials": {f"SERIAL{k}": v or "tcp:0 (default)" for k, v in cfg["serials"].items()},
            "extra_params": cfg["extra"], "policy": policy.name,
            "keyed_unsigned_read": keyed_unsigned, "cases": cases,
            "agree": sum(c["agree"] for c in decided), "total": len(decided),
            "inconclusive": len(cases) - len(decided)}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--master", type=Path, required=True)
    p.add_argument("--pr", type=Path, required=True)
    p.add_argument("--out", type=Path, default=labkit.REPO / "results/pr34780")
    p.add_argument("--only", nargs="*")
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    res = {"stack": "ArduPilot Copter SITL", "pr": "ArduPilot/ardupilot#34780",
           "master_rev": labkit.git_rev(a.master), "pr_rev": labkit.git_rev(a.pr),
           "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "runs": []}
    for build, ap in (("master", a.master), ("pr34780", a.pr)):
        for name, cfg in CONFIGS.items():
            if a.only and name not in a.only:
                continue
            r = run_config(build, name, cfg, ap)
            res["runs"].append(r)
            print(build, name, f"{r['agree']}/{r['total']}", "inconclusive", r["inconclusive"],
                  r["keyed_unsigned_read"], flush=True)
            (a.out / "pr34780.json").write_text(json.dumps(res, indent=2))
            time.sleep(2)


if __name__ == "__main__":
    main()
