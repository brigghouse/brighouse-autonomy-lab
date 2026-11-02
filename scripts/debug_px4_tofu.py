"""Diagnostic: repeat the PX4 trust-on-first-use check step by step on a local SITL.

Starts PX4 v1.18 SITL, provisions the lab key, then after an unsigned re-key attempt
measures which key (original / other / none) the outbound frames verify with, sampled
several times over ~40 s. Local simulator only.
"""

from __future__ import annotations

import argparse
import json
import tempfile
import time
from pathlib import Path

import labkit
from run_px4 import start_px4


def sample(port, key, seconds=6.0):
    return labkit.keyed_check(f"udpin:127.0.0.1:{port}", key, seconds)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--px4", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    rootfs = Path(tempfile.mkdtemp(prefix="px4-tofu-"))
    key, other = labkit.lab_key(), labkit.lab_key("a-different-key")
    log = {}
    proc = start_px4(a.px4, rootfs)
    try:
        labkit.provision_signing("udpin:127.0.0.1:14550", key)
        log["after_provision_original"] = sample(14550, key)
        keyfile = rootfs / "mavlink" / "mavlink-signing-key.bin"
        before = keyfile.read_bytes()
        labkit.provision_signing("udpin:127.0.0.1:14550", other)
        log["key_file_changed"] = before != keyfile.read_bytes()
        for i in range(5):
            log[f"t{i}_original"] = sample(14550, key)
            log[f"t{i}_other"] = sample(14550, other)
    finally:
        proc.terminate()
        proc.wait(timeout=15)
    log["px4_log_signing_lines"] = [l.strip() for l in (rootfs / "px4.log").read_text().splitlines() if "sign" in l.lower()]
    a.out.write_text(json.dumps(log, indent=2))
    print(json.dumps(log, indent=2))


if __name__ == "__main__":
    main()
