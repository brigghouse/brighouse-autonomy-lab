"""Orchestrate the live model-based conformance run against the three built stacks.

Starts each SITL on fixed ports, runs scripts/conformance.py with the matching policy,
stops the SITL, and writes results/conformance/. Must run when no other process holds
the SITL ports (i.e. after the longitudinal study finishes).

    python scripts/run_conformance_all.py --ardupilot ~/sitl/ardupilot \
        --px4-118 ~/sitl/px4 --px4-117 ~/sitl/px4-117 --out results/conformance
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import labkit  # noqa: E402
from conformance import run as conf_run  # noqa: E402


def start_ardupilot(ap: Path):
    workdir = Path(tempfile.mkdtemp(prefix="ap-conf-"))
    binary = ap / "build/sitl/bin/arducopter"
    cmd = [str(binary), "--model", "+", "--speedup", "1", "-I0", "-w",
           "--defaults", str(ap / "Tools/autotest/default_params/copter.parm"), "--serial1", "tcp:2"]
    log = open(workdir / "sitl.log", "w")
    proc = subprocess.Popen(cmd, cwd=workdir, stdout=log, stderr=subprocess.STDOUT)
    labkit.wait_tcp(5760)
    time.sleep(3)
    return proc


def start_px4(px4: Path):
    rootfs = Path(tempfile.mkdtemp(prefix="px4-conf-"))
    build = px4 / "build/px4_sitl_default"
    env = dict(os.environ, PX4_SIM_MODEL="sihsim_quadx", HEADLESS="1")
    log = open(rootfs / "px4.log", "w")
    proc = subprocess.Popen([str(build / "bin/px4"), "-d", str(build / "etc"), "-w", str(rootfs)],
                            cwd=rootfs, env=env, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    time.sleep(22)
    return proc, rootfs


def stop(proc):
    try:
        proc.terminate()
        proc.wait(timeout=12)
    except Exception:  # noqa: BLE001
        try:
            os.kill(proc.pid, signal.SIGKILL)
        except Exception:  # noqa: BLE001
            pass


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ardupilot", type=Path)
    p.add_argument("--px4-118", type=Path)
    p.add_argument("--px4-117", type=Path)
    p.add_argument("--out", type=Path, default=Path("results/conformance"))
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    summary = {}

    if a.ardupilot:
        proc = start_ardupilot(a.ardupilot)
        try:
            r = conf_run("ardupilot", "tcp:127.0.0.1:5760", "tcp:127.0.0.1:5762",
                         "ardupilot-4.7.2", a.out)
            summary["ardupilot-4.7.2"] = {k: r[k] for k in ("agreement", "cases_total", "cases_agree")}
        finally:
            stop(proc)
        time.sleep(3)

    for name, pth, policy in (("px4-1.18", a.px4_118, "px4-1.18"), ("px4-1.17", a.px4_117, "px4-1.17")):
        if not pth:
            continue
        proc, _ = start_px4(pth)
        try:
            r = conf_run("px4", "udpin:127.0.0.1:14550", "udpin:127.0.0.1:14540", policy, a.out)
            summary[name] = {k: r[k] for k in ("agreement", "cases_total", "cases_agree")}
        finally:
            stop(proc)
        time.sleep(3)

    (a.out / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
