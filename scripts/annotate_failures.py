"""Annotate longitudinal build failures with their reason (one-off helper)."""
import json
from pathlib import Path

REASON = ("toolchain: pre-4.5 ArduPilot does not build on current Ubuntu 24.04 - its bundled "
          "waf needs Python<=3.10 (imp, rU-mode), the UAVCAN code generator needs Python<=3.9 "
          "(collections.MutableSequence), and the C++ still fails on modern GCC "
          "(e.g. std::uint16_t without <cstdint> in CANSocketIface.cpp)")

idx = Path("results/longitudinal/index.json")
d = json.loads(idx.read_text())
for k, v in d.items():
    if k.startswith("ardupilot") and v.get("build") in ("build failed", "configure failed"):
        v["failure_reason"] = REASON
idx.write_text(json.dumps(d, indent=2))
print("annotated:", [k for k in d if "failure_reason" in d[k]])
