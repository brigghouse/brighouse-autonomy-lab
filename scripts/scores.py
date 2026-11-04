"""Compute secure-by-default scores for every measured configuration and for the
longitudinal releases, and emit a table + figure.

    python scripts/scores.py
"""

from __future__ import annotations

import json
import time
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "papers" / "common"))
from mavaudit.score import SCORE_VERSION, score_summary_run  # noqa: E402


def control_plane_for(stack: str, version_hint: str) -> dict | None:
    """The dds_probe observation for a build, if one was recorded (A1: provenance).
    Returns None when we never probed that build, which makes its score a lower bound."""
    d = REPO / "results" / "dds"
    if not d.exists():
        return None
    for f in sorted(d.glob("dds-*.json")):
        r = json.loads(f.read_text())
        if r.get("stack") != stack:
            continue
        v = str(r.get("version", ""))
        if version_hint and version_hint not in v and v not in version_hint:
            continue
        # An inconclusive capture earns nothing. Zero datagrams cannot distinguish "no
        # second plane is offered" from "we listened on the wrong port, or too late", and
        # crediting it turned absence of evidence into eight points -- which was enough to
        # reorder two stacks in a published table. Found by an independent reviewer.
        if r.get("inconclusive"):
            return None
        return {"unauthenticated": bool(r.get("unauthenticated_agent_discovery")),
                "detail": (f"{r.get('xrce_datagrams', 0)} XRCE datagrams, "
                           f"{r.get('submessage_counts')} on port {r.get('port')} "
                           f"({f.name})")}
    return None

# Cross-sectional configs: (label, folder, run, model-policy)
CONFIGS = [
    ("ArduPilot 4.7.2 ch0 default", "ardupilot-4.7.2", "E1-default-serial0", "ardupilot-4.7.2"),
    ("ArduPilot 4.7.2 ch0 signed", "ardupilot-4.7.2", "E2-signed-serial0", "ardupilot-4.7.2"),
    ("ArduPilot 4.7.2 SERIAL1 signed", "ardupilot-4.7.2", "E2-signed-serial1", "ardupilot-4.7.2"),
    ("PX4 1.17 GCS default", "px4-1.17.0", "E3-default-gcs", "px4-1.17"),
    ("PX4 1.17 GCS provisioned", "px4-1.17.0", "E4-signed-gcs", "px4-1.17"),
    ("PX4 1.18 GCS default", "px4-1.18.0-rc1", "E3-default-gcs", "px4-1.18"),
    ("PX4 1.18 GCS signed", "px4-1.18.0-rc1", "E4-signed-gcs", "px4-1.18"),
]


def cross_section():
    rows = []
    for label, folder, run, policy in CONFIGS:
        f = REPO / "results" / folder / "summary.json"
        if not f.exists():
            continue
        d = json.loads(f.read_text())["runs"].get(run)
        if not d:
            continue
        stack = "ardupilot" if folder.startswith("ardupilot") else "px4"
        hint = folder.split("-", 1)[1] if "-" in folder else ""
        s = score_summary_run(d, policy, control_plane=control_plane_for(stack, hint))
        rows.append({"label": label, "score": s["score"], "grade": s["grade"], "policy": policy,
                     "lower_bound": bool(s.get("lower_bound"))})
    # ideal target
    ideal = score_summary_run({"frames": 100, "signed_frames": 100, "v1_frames": 0,
                               "ftp_advertised": False, "unsigned_probe_answered": False,
                               "firmware": "x"}, "ideal-oob-provisioning", link_confidential=True,
                              control_plane={"unauthenticated": False,
                                             "detail": "model target: no secondary plane"})
    rows.append({"label": "IDEAL (model target)", "score": ideal["score"], "grade": ideal["grade"],
                 "policy": "ideal-oob-provisioning"})
    return sorted(rows, key=lambda r: -r["score"])


def longitudinal():
    idx = REPO / "results" / "longitudinal" / "index.json"
    if not idx.exists():
        return []
    data = json.loads(idx.read_text())
    rows = []
    for key, e in data.items():
        if not str(e.get("build", "")).startswith("ok"):
            continue
        m = e.get("measurements", {})
        dkey = next((k for k in m if k.startswith("default")), None)
        pkey = next((k for k in m if k.startswith("provisioned")), None)
        policy = "ardupilot-4.7.2" if e["stack"] == "ardupilot" else (
            "px4-1.18" if "1.18" in e["ref"] or "1.17" not in e["ref"] else "px4-1.17")
        cp = control_plane_for(e["stack"], e["ref"].split("-")[-1])
        d_default = score_summary_run(m[dkey], policy, control_plane=cp) if dkey else None
        d_prov = score_summary_run(m[pkey], policy, control_plane=cp) if pkey else None
        rows.append({"stack": e["stack"], "ref": e["ref"],
                     "default_score": d_default["score"] if d_default else None,
                     "provisioned_score": d_prov["score"] if d_prov else None,
                     "control_plane_measured": cp is not None})
    return rows


def main():
    out = REPO / "results" / "scores"
    out.mkdir(parents=True, exist_ok=True)
    cs = cross_section()
    lg = longitudinal()
    # The record carries its own date. Without it the figures that read this file had to
    # hard-code one, and a hard-coded date outlived its measurement on the very next re-run.
    (out / "scores.json").write_text(json.dumps(
        {"score_version": SCORE_VERSION,
         "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "cross_section": cs, "longitudinal": lg}, indent=2))

    lines = ["# Secure-by-default scores", "",
             f"Computed by `mavaudit.score`, criteria set **v{SCORE_VERSION}** (axioms: "
             "provenance, monotonicity, CRA-grounded weights). 0--100; grade A--E. Scores "
             "from different criteria versions are not comparable.", "",
             "v2 splits v1's single \"unauthenticated service exposure\" criterion into the "
             "MAVLink file-transfer surface (8) and a secondary control plane (8), measured "
             "by `scripts/dds_probe.py`. A build we never probed earns nothing for the "
             "latter and is marked as a lower bound.", "",
             "## Cross-section", "", "| Configuration | Score | Grade | |", "|---|---|---|---|"]
    for r in cs:
        flag = "lower bound (control plane not probed)" if r.get("lower_bound") else ""
        lines.append(f"| {r['label']} | {r['score']} | {r['grade']} | {flag} |")
    if lg:
        lines += ["", "## Longitudinal (per release)", "",
                  "| Stack | Version | Default | Provisioned (best link) | Control plane |",
                  "|---|---|---|---|---|"]
        for r in lg:
            cp = "probed" if r.get("control_plane_measured") else "not probed (lower bound)"
            lines.append(f"| {r['stack']} | {r['ref']} | {r['default_score']} | "
                         f"{r['provisioned_score']} | {cp} |")
    (out / "README.md").write_text("\n".join(lines) + "\n")

    # LaTeX table for paper 4
    tex = ["\\begin{table}[t]", "\\caption{Secure-by-default score of each measured configuration.}",
           "\\label{tab:scores}", "\\centering\\footnotesize", "\\begin{tabular}{@{}lcc@{}}",
           "\\toprule", "configuration & score & grade \\\\", "\\midrule"]
    for r in cs:
        tex.append(f"{r['label'].replace('&','\\&')} & {r['score']:.0f} & {r['grade']} \\\\")
    tex += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]
    p4 = REPO / "papers" / "paper4-score"
    if p4.exists():
        (p4 / "scores_table.tex").write_text("\n".join(tex))

    try:
        make_figure(cs, out)
    except Exception as e:  # noqa: BLE001
        print("figure skipped:", e)
    print("\n".join(lines[:16]))


def make_figure(cs, out):
    import figstyle
    from figstyle import COL1, PALETTE, save
    figstyle.apply()
    import matplotlib.pyplot as plt
    rows = list(reversed(cs))
    labels = [r["label"] for r in rows]
    scores = [r["score"] for r in rows]
    colors = [PALETTE[3] if s >= 75 else PALETTE[1] if s >= 55 else PALETTE[4] for s in scores]
    fig, ax = plt.subplots(figsize=(COL1, 2.6))
    y = range(len(rows))
    ax.barh(list(y), scores, color=colors)
    for i, s in enumerate(scores):
        ax.text(s + 1, i, f"{s:.0f}", va="center", fontsize=6)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=5.5)
    ax.set_xlim(0, 105)
    ax.set_xlabel("secure-by-default score")
    ax.set_title("Score discriminates posture (R4: ch0 signed < SERIAL1)", fontsize=7)
    save(fig, REPO / "papers" / "common" / "figures" / "fig_scores.pdf")


if __name__ == "__main__":
    main()
