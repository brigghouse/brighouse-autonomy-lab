"""Longitudinal study: build many ArduPilot / PX4 releases, measure the default signing
posture and whether signing can be provisioned, then delete the tree to save disk.

    python scripts/longitudinal.py --work ~/sitl-long --out results/longitudinal \
        --ardupilot Copter-4.0.7 Copter-4.3.8 --px4 v1.13.3 v1.15.4

Per version it records: build success, default link posture (signed frames, unsigned
read answered, FTP advertised, firmware string), and the outcome of the defender
provisioning step. A failed build is recorded, not hidden. Local simulators only.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import labkit  # noqa: E402

import shutil as _sh
_OLD_WAF_PYTHON = next((p for p in [
    "/root/.local/share/uv/python/cpython-3.9-linux-x86_64-gnu/bin/python3.9",
    "/root/.local/share/uv/python/cpython-3.10-linux-x86_64-gnu/bin/python3.10",
    _sh.which("python3.9"), _sh.which("python3.10")] if p and __import__("os").path.exists(p)), None)

VOXL = ("libmodal-json", "libmodal-pipe", "boards/modalai/voxl2/libfc-sensor-api")


def sh(cmd, cwd, log, timeout=7200, env=None):
    with open(log, "a") as fh:
        fh.write(f"\n$ {' '.join(cmd)}\n")
        fh.flush()
        return subprocess.run(cmd, cwd=cwd, stdout=fh, stderr=subprocess.STDOUT, timeout=timeout, env=env).returncode


def clone(url, ref, dest, log, submodules=True):
    cmd = ["git", "clone", "-q", "--depth", "1", "--branch", ref]
    if submodules:
        cmd += ["--recurse-submodules", "--shallow-submodules"]
    cmd += [url, str(dest)]
    return sh(cmd, dest.parent, log, timeout=3600)


# ---------------------------------------------------------------- ArduPilot
def _waf_build(src, log, py):
    if sh([py, "waf", "configure", "--board", "sitl"], src, log) != 0:
        return "configure failed"
    if sh([py, "waf", "copter"], src, log) != 0:
        return "build failed"
    return "ok"


def build_ardupilot(ref, work, log):
    src = work / f"ardupilot-{ref}"
    if clone("https://github.com/ArduPilot/ardupilot.git", ref, src, log) != 0:
        return None, "clone failed"
    status = _waf_build(src, log, "python3")
    # Pre-4.5 fails on a current toolchain in layers: the bundled waf needs the `imp`
    # module (removed in Python 3.12) and `rU` open-mode (removed in 3.11), and the UAVCAN
    # code generator uses `collections.MutableSequence` (removed in 3.10). A full build of
    # those releases needs Python <= 3.9; retry with the archived interpreter.
    if status in ("configure failed", "build failed") and _OLD_WAF_PYTHON:
        with open(log) as fh:
            blog = fh.read()
        if any(x in blog for x in ("No module named 'imp'", "invalid mode: 'rUb'", "MutableSequence")):
            sh(["git", "clean", "-xfdq", "build"], src, log)
            st2 = _waf_build(src, log, _OLD_WAF_PYTHON)
            status = ("ok (python3.9)" if st2 == "ok" else st2)
    return src, status


def measure_ardupilot(src, out, duration):
    binary = src / "build/sitl/bin/arducopter"
    defaults = src / "Tools/autotest/default_params/copter.parm"
    workdir = Path(tempfile.mkdtemp(prefix="ap-long-"))
    cmd = [str(binary), "--model", "+", "--speedup", "1", "-I0", "-w", "--defaults", str(defaults)]
    logf = open(workdir / "sitl.log", "w")
    proc = subprocess.Popen(cmd, cwd=workdir, stdout=logf, stderr=subprocess.STDOUT)
    res = {}
    try:
        labkit.wait_tcp(5760)
        r = labkit.audit("tcp:127.0.0.1:5760", out / "default-serial0", duration)
        res["default-serial0"] = labkit.summarise(r)
        try:
            labkit.provision_signing("tcp:127.0.0.1:5760", labkit.lab_key())
            r = labkit.audit("tcp:127.0.0.1:5760", out / "provisioned-serial0", duration)
            res["provisioned-serial0"] = labkit.summarise(r)
            res["provisioned-serial0"]["keyed_check"] = labkit.keyed_check("tcp:127.0.0.1:5760", labkit.lab_key())
        except Exception as e:  # noqa: BLE001
            res["provision_error"] = repr(e)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
        shutil.copy(workdir / "sitl.log", out / "sitl.log")
    return res


# ---------------------------------------------------------------- PX4
def build_px4(ref, work, log):
    src = work / f"px4-{ref}"
    if clone("https://github.com/PX4/PX4-Autopilot.git", ref, src, log, submodules=False) != 0:
        return None, "clone failed"
    for s in VOXL:
        subprocess.run(["git", "config", f"submodule.{s}.update", "none"], cwd=src)
    if sh(["git", "submodule", "update", "--init", "--recursive", "--depth", "1", "-j", "4"], src, log, 3600) != 0:
        # old releases reference submodule commits that shallow fetch cannot reach: retry unshallow
        sh(["git", "submodule", "update", "--init", "--recursive", "-j", "4"], src, log, 3600)
    sh(["git", "submodule", "foreach", "--recursive", "-q", "git reset -q --hard HEAD"], src, log)
    if sh(["make", "px4_sitl_default"], src, log, timeout=7200) != 0:
        return src, "build failed"
    return src, "ok"


def measure_px4(src, out, duration, model):
    build = src / "build/px4_sitl_default"
    rootfs = Path(tempfile.mkdtemp(prefix="px4-long-"))
    env = dict(os.environ, PX4_SIM_MODEL=model, HEADLESS="1", PX4_SIMULATOR="none")
    logf = open(rootfs / "px4.log", "w")
    proc = subprocess.Popen([str(build / "bin/px4"), "-d", str(build / "etc"), "-w", str(rootfs)],
                            cwd=rootfs, env=env, stdout=logf, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    time.sleep(25)
    res = {}
    try:
        r = labkit.audit("udpin:127.0.0.1:14550", out / "default-gcs", duration)
        res["default-gcs"] = labkit.summarise(r)
        try:
            labkit.provision_signing("udpin:127.0.0.1:14550", labkit.lab_key())
            r = labkit.audit("udpin:127.0.0.1:14550", out / "provisioned-gcs", duration)
            res["provisioned-gcs"] = labkit.summarise(r)
            res["provisioned-gcs"]["keyed_check"] = labkit.keyed_check("udpin:127.0.0.1:14550", labkit.lab_key())
            keyfile = rootfs / "mavlink" / "mavlink-signing-key.bin"
            res["key_file_present"] = keyfile.exists()
        except Exception as e:  # noqa: BLE001
            res["provision_error"] = repr(e)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
        shutil.copy(rootfs / "px4.log", out / "px4.log")
    return res


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--work", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--ardupilot", nargs="*", default=[])
    p.add_argument("--px4", nargs="*", default=[])
    p.add_argument("--px4-model", default="sihsim_quadx")
    p.add_argument("--duration", type=float, default=12.0)
    p.add_argument("--keep", action="store_true", help="keep source trees")
    a = p.parse_args()
    a.work.mkdir(parents=True, exist_ok=True)
    a.out.mkdir(parents=True, exist_ok=True)
    index = a.out / "index.json"
    results = json.loads(index.read_text()) if index.exists() else {}

    jobs = [("ardupilot", r) for r in a.ardupilot] + [("px4", r) for r in a.px4]
    for stack, ref in jobs:
        key = f"{stack}:{ref}"
        if key in results and str(results[key].get("build", "")).startswith("ok") \
                and "measure_error" not in results[key]:
            continue
        out = a.out / f"{stack}-{ref}"
        out.mkdir(exist_ok=True)
        log = out / "build.log"
        t0 = time.time()
        entry = {"stack": stack, "ref": ref, "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        src, status = (build_ardupilot if stack == "ardupilot" else build_px4)(ref, a.work, log)
        entry["build"] = status
        entry["build_seconds"] = round(time.time() - t0)
        if src is not None:
            entry["source_rev"] = labkit.git_rev(src)
        if status.startswith("ok"):
            try:
                entry["measurements"] = (measure_ardupilot(src, out, a.duration) if stack == "ardupilot"
                                         else measure_px4(src, out, a.duration, a.px4_model))
            except Exception as e:  # noqa: BLE001
                entry["measure_error"] = repr(e)
        results[key] = entry
        index.write_text(json.dumps(results, indent=2))
        print(json.dumps(entry, indent=1), flush=True)
        if src is not None and not a.keep:
            shutil.rmtree(src, ignore_errors=True)


if __name__ == "__main__":
    main()
