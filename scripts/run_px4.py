"""Experiments E3 (default) and E4 (signing enabled) on PX4 SITL with the SIH simulator
(no Gazebo needed).

Usage:
    python scripts/run_px4.py --px4 ~/PX4-Autopilot --out results/px4

Links in PX4 SITL: "GCS" link sends to udp 14550, "Onboard" link sends to udp 14540.

E4 also re-checks the documented trust-on-first-use rule: once a key is provisioned, an
UNSIGNED SETUP_SIGNING carrying a different key must be rejected. This is a
conformance check of documented behaviour on our own simulator.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import labkit

LINKS = {"gcs": 14550, "onboard": 14540}


def start_px4(px4: Path, rootfs: Path) -> subprocess.Popen:
    build = px4 / "build/px4_sitl_default"
    env = dict(os.environ, PX4_SIM_MODEL="sihsim_quadx", HEADLESS="1")
    log = open(rootfs / "px4.log", "w")
    proc = subprocess.Popen([str(build / "bin/px4"), "-d", str(build / "etc"), "-w", str(rootfs)],
                            cwd=rootfs, env=env, stdout=log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    time.sleep(20)  # boot + SIH init
    return proc


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--px4", type=Path, required=True)
    p.add_argument("--out", type=Path, default=labkit.REPO / "results/px4")
    p.add_argument("--duration", type=float, default=15.0)
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    rootfs = Path(tempfile.mkdtemp(prefix="px4-rootfs-"))
    key = labkit.lab_key()
    other_key = labkit.lab_key("a-different-key")
    summary = {"stack": "PX4 (SIH)", "source_rev": labkit.git_rev(a.px4),
               "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "runs": {}}
    proc = start_px4(a.px4, rootfs)
    try:
        for name, port in LINKS.items():
            r = labkit.audit(f"udpin:127.0.0.1:{port}", a.out / f"E3-default-{name}", a.duration)
            summary["runs"][f"E3-default-{name}"] = labkit.summarise(r)

        # Defender step: provision the key over the GCS link (unsigned, as PX4 allows when no key exists).
        labkit.provision_signing(f"udpin:127.0.0.1:{LINKS['gcs']}", key)
        keyfile = rootfs / "mavlink" / "mavlink-signing-key.bin"
        summary["key_file_present"] = keyfile.exists()
        summary["key_file_size"] = keyfile.stat().st_size if keyfile.exists() else None

        for name, port in LINKS.items():
            r = labkit.audit(f"udpin:127.0.0.1:{port}", a.out / f"E4-signed-{name}", a.duration)
            summary["runs"][f"E4-signed-{name}"] = labkit.summarise(r)
            summary["runs"][f"E4-signed-{name}"]["keyed_check"] = labkit.keyed_check(
                f"udpin:127.0.0.1:{port}", key)

        # Trust-on-first-use conformance: an unsigned attempt to replace the key must fail.
        before = keyfile.read_bytes() if keyfile.exists() else None
        labkit.provision_signing(f"udpin:127.0.0.1:{LINKS['gcs']}", other_key)
        after = keyfile.read_bytes() if keyfile.exists() else None
        still_original = labkit.keyed_check(f"udpin:127.0.0.1:{LINKS['gcs']}", key)
        summary["tofu_unsigned_rekey"] = {
            "key_file_changed": before != after,
            "original_key_still_valid": still_original,
        }
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
        shutil.copy(rootfs / "px4.log", a.out / "px4.log")
    (a.out / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
