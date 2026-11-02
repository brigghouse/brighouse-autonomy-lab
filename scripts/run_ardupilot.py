"""Experiments E1 (default) and E2 (signing enabled) on ArduPilot Copter SITL.

Usage:
    python scripts/run_ardupilot.py --ardupilot ~/ardupilot --out results/ardupilot

Ports: SERIAL0 = tcp 5760 (the port ArduPilot treats like the primary/USB console in
SITL), SERIAL1 = tcp 5762 (a telemetry port).
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

PORTS = {"serial0": 5760, "serial1": 5762}


def start_sitl(ap: Path, workdir: Path) -> subprocess.Popen:
    binary = ap / "build/sitl/bin/arducopter"
    cmd = [str(binary), "--model", "+", "--speedup", "1", "-I0", "-w",
           "--defaults", str(ap / "Tools/autotest/default_params/copter.parm"),
           "--serial1", "tcp:2"]
    log = open(workdir / "sitl.log", "w")
    proc = subprocess.Popen(cmd, cwd=workdir, stdout=log, stderr=subprocess.STDOUT)
    labkit.wait_tcp(PORTS["serial0"])
    return proc


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ardupilot", type=Path, required=True)
    p.add_argument("--out", type=Path, default=labkit.REPO / "results/ardupilot")
    p.add_argument("--duration", type=float, default=15.0)
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    workdir = Path(tempfile.mkdtemp(prefix="ap-sitl-"))
    key = labkit.lab_key()
    summary = {"stack": "ArduPilot Copter", "source_rev": labkit.git_rev(a.ardupilot),
               "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "runs": {}}
    proc = start_sitl(a.ardupilot, workdir)
    try:
        # SERIAL0 must be connected first; SITL waits for it before booting.
        for name in ("serial0", "serial1"):
            r = labkit.audit(f"tcp:127.0.0.1:{PORTS[name]}", a.out / f"E1-default-{name}", a.duration)
            summary["runs"][f"E1-default-{name}"] = labkit.summarise(r)

        labkit.provision_signing(f"tcp:127.0.0.1:{PORTS['serial0']}", key)

        for name in ("serial0", "serial1"):
            r = labkit.audit(f"tcp:127.0.0.1:{PORTS[name]}", a.out / f"E2-signed-{name}", a.duration)
            summary["runs"][f"E2-signed-{name}"] = labkit.summarise(r)
            summary["runs"][f"E2-signed-{name}"]["keyed_check"] = labkit.keyed_check(
                f"tcp:127.0.0.1:{PORTS[name]}", key)
    finally:
        proc.terminate()
        proc.wait(timeout=10)
        shutil.copy(workdir / "sitl.log", a.out / "sitl.log")
    (a.out / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
