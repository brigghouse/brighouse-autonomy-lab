"""JSON and Markdown report rendering."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone

from . import __version__

DISCLAIMER = (
    "CRA references map findings to Regulation (EU) 2024/2847 Annex I as a technical "
    "interpretation; they are not legal advice or a conformity assessment."
)


def build(target: str, duration: float, observer, findings, scope_ref: str | None, probe) -> dict:
    return {
        "tool": "mavaudit",
        "version": __version__,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "target": target,
        "scope_ref": scope_ref,
        "duration_s": duration,
        "unsigned_probe": probe,
        "endpoints": [ep.to_dict() for _, ep in sorted(observer.endpoints.items())],
        "findings": [asdict(f) for f in findings],
        "disclaimer": DISCLAIMER,
    }


def to_json(report: dict) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False)


def to_markdown(report: dict) -> str:
    lines = [
        "# mavaudit report",
        "",
        f"- Target: `{report['target']}`",
        f"- Scope reference: {report['scope_ref'] or 'lab / private network'}",
        f"- Generated (UTC): {report['generated_utc']}",
        f"- Observation window: {report['duration_s']} s",
        "",
        "## Endpoints",
        "",
        "| sysid/compid | autopilot | frames | MAVLink 1 | MAVLink 2 | signed |",
        "|---|---|---|---|---|---|",
    ]
    for ep in report["endpoints"]:
        lines.append(
            f"| {ep['sysid']}/{ep['compid']} | {ep['autopilot'] or '-'} | {ep['frames']} | "
            f"{ep['v1_frames']} | {ep['v2_frames']} | {ep['signed_frames']} |"
        )
    lines += ["", "## Findings", ""]
    if not report["findings"]:
        lines.append("No findings.")
    for f in report["findings"]:
        lines += [
            f"### {f['id']} [{f['severity'].upper()}] {f['title']} ({f['endpoint']})",
            "",
            f["detail"],
            "",
            f"- CRA: {'; '.join(f['cra_refs'])}",
            f"- Recommendation: {f['recommendation']}",
            "",
        ]
    lines += ["---", "", f"_{report['disclaimer']}_", ""]
    return "\n".join(lines)
