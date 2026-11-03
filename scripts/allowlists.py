"""Which messages does each stack accept *unsigned* even when a key is active?

Signing is only as strong as its exceptions. Both stacks keep a short allowlist, and
ArduPilot adds a blanket per-channel exemption. This extracts both from the source trees
rather than copying them into prose, so the record cannot drift from the code: the output
carries the file, the line and the matched text for each entry.

    python scripts/allowlists.py --ardupilot ~/sitl/ardupilot --px4 ~/sitl/px4 \
        --px4-old ~/sitl/px4-117 --out results/allowlists
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from pathlib import Path

MSG_ID = re.compile(r"MAVLINK_MSG_ID_([A-Z0-9_]+)")


def _rev(path: Path) -> str:
    try:
        return subprocess.run(["git", "-C", str(path), "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:  # noqa: BLE001
        return "unknown"


def extract(src: Path, rel: str, array_name: str) -> dict:
    """Pull the message ids out of a C array literal, keeping file:line provenance."""
    f = src / rel
    if not f.exists():
        return {"file": rel, "present": False,
                "note": "array not found in this tree (feature absent in this release)"}
    text = f.read_text(errors="replace")
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines) if array_name in ln and "[]" in ln), None)
    if start is None:
        return {"file": rel, "present": False, "note": f"{array_name} not found"}
    entries, comment = [], []
    for i in range(max(0, start - 4), start):
        if "//" in lines[i]:
            comment.append(lines[i].strip().lstrip("/ ").strip())
    for i in range(start, min(start + 40, len(lines))):
        for m in MSG_ID.finditer(lines[i]):
            entries.append({"message": m.group(1), "line": i + 1})
        if "};" in lines[i]:
            break
    return {"file": rel, "present": True, "array": array_name,
            "entries": entries, "source_comment": comment}


def channel_exemption(src: Path) -> dict:
    f = src / "libraries/GCS_MAVLink/GCS_Signing.cpp"
    if not f.exists():
        return {"present": False}
    lines = f.read_text(errors="replace").splitlines()
    i = next((k for k, ln in enumerate(lines) if "MAVLINK_COMM_0" in ln and "status ==" in ln), None)
    if i is None:
        return {"present": False}
    return {"present": True, "file": "libraries/GCS_MAVLink/GCS_Signing.cpp", "line": i + 1,
            "rationale_in_source": " ".join(ln.strip().lstrip("/ ").strip()
                                            for ln in lines[i + 1:i + 3] if "//" in ln),
            "effect": ("every message, not a list: any unsigned frame on channel 0 is "
                       "accepted. Measured in results/ch0-configs/ to follow the channel "
                       "index rather than the transport.")}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ardupilot", type=Path, required=True)
    p.add_argument("--px4", type=Path, required=True)
    p.add_argument("--px4-old", type=Path)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    out = {"recorded_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "method": "extracted from the source trees; file and line recorded per entry",
           "stacks": {}}
    out["stacks"]["ardupilot"] = {
        "rev": _rev(a.ardupilot),
        "allowlist": extract(a.ardupilot, "libraries/GCS_MAVLink/GCS_Signing.cpp", "accept_list"),
        "channel_exemption": channel_exemption(a.ardupilot)}
    out["stacks"]["px4"] = {
        "rev": _rev(a.px4),
        "allowlist": extract(a.px4, "src/modules/mavlink/mavlink_sign_control.cpp",
                             "unsigned_messages"),
        "channel_exemption": {"present": False,
                              "note": "no per-channel blanket exemption in this release"}}
    if a.px4_old:
        out["stacks"]["px4_previous_release"] = {
            "rev": _rev(a.px4_old),
            "allowlist": extract(a.px4_old, "src/modules/mavlink/mavlink_sign_control.cpp",
                                 "unsigned_messages"),
            "channel_exemption": {"present": False}}
    # The question this was built to answer, answered from the extracted data only.
    odid = []
    for name, st in out["stacks"].items():
        al = st["allowlist"]
        if al.get("present"):
            odid.append((name, any(e["message"].startswith("OPEN_DRONE_ID")
                                   for e in al["entries"])))
    out["open_drone_id_allowlisted"] = dict(odid)
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "allowlists.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2)[:1800])


if __name__ == "__main__":
    main()
