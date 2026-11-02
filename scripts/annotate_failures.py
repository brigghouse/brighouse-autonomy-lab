"""Annotate longitudinal build/measure outcomes with reasons (one-off helper)."""
import json
from pathlib import Path

AP_REASON = ("toolchain cliff: pre-4.5 ArduPilot does not build on current Ubuntu 24.04 - the "
             "bundled waf needs Python<=3.10 (imp, rU-mode); the UAVCAN code generator needs "
             "Python<=3.9 (collections.MutableSequence); and the C++ still fails on modern GCC "
             "(e.g. std::uint16_t without <cstdint> in CANSocketIface.cpp)")
PX4_NOTE = ("builds on the current toolchain after patching the shallow-clone version script "
            "(NuttX-tag IndexError), but the uniform SIH harness (PX4_SIM_MODEL=sihsim_quadx) is "
            "not recognised by this release, which waits for an external simulator on TCP 4560 - a "
            "cross-version simulator-config drift, so no telemetry was captured")

idx = Path("results/longitudinal/index.json")
d = json.loads(idx.read_text())
for k, v in d.items():
    if k.startswith("ardupilot") and v.get("build") in ("build failed", "configure failed"):
        v["failure_reason"] = AP_REASON
    if k.startswith("px4") and v.get("build") == "ok" and not v.get("measurements", {}).get("default-gcs", {}).get("frames"):
        v["measure_note"] = PX4_NOTE
idx.write_text(json.dumps(d, indent=2))
print("annotated:", {k: ("fail" if "failure_reason" in v else "measnote" if "measure_note" in v else "ok")
                      for k, v in d.items()})
