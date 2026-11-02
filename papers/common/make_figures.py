"""Generate all figures for the papers from results/ and the formal model.

    python papers/common/make_figures.py

Writes PDFs into papers/common/figures/. Every figure is derived from committed data
(results/*/summary.json, results/model/model-results.json); nothing is hand-drawn.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
FIG = HERE / "figures"
FIG.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))
import figstyle  # noqa: E402
from figstyle import COL1, COL2, PALETTE, save  # noqa: E402

figstyle.apply()
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402


def load(name):
    return json.loads((REPO / "results" / name / "summary.json").read_text())


# ---------------------------------------------------------------- Fig 1: default posture
def fig_default_posture():
    stacks = [("ArduPilot 4.7.2", "ardupilot-4.7.2", ["E1-default-serial0", "E1-default-serial1"]),
              ("PX4 1.17.0", "px4-1.17.0", ["E3-default-gcs", "E3-default-onboard"]),
              ("PX4 1.18.0-rc1", "px4-1.18.0-rc1", ["E3-default-gcs", "E3-default-onboard"])]
    labels, signed_frac, answered, ftp = [], [], [], []
    for title, folder, runs in stacks:
        d = load(folder)["runs"]
        for r in runs:
            s = d[r]
            labels.append(f"{title}\n{r.split('-')[-1]}")
            signed_frac.append(100.0 * s["signed_frames"] / max(s["frames"], 1))
            answered.append(s["unsigned_probe_answered"])
            ftp.append(bool(s["ftp_advertised"]))
    fig, ax = plt.subplots(figsize=(COL2, 2.2))
    x = np.arange(len(labels))
    ax.bar(x, signed_frac, color=PALETTE[2], width=0.6, label="signed frames (%)")
    for i, (a, f) in enumerate(zip(answered, ftp)):
        marks = []
        if a:
            marks.append("unsigned read answered")
        if f:
            marks.append("FTP exposed")
        ax.text(i, 3, "\n".join("[x] " + m for m in marks), ha="center", va="bottom",
                fontsize=5.5, color=PALETTE[1])
    ax.set_ylim(0, 100)
    ax.set_ylabel("signed frames (% of total)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=6)
    ax.set_title("Default configuration: no stack signs by default; all answer unauthenticated requests")
    save(fig, FIG / "fig_default_posture.pdf")


# ---------------------------------------------------------------- Fig 2: before/after provisioning
def fig_provisioning():
    rows = [("ArduPilot 4.7.2 SERIAL0 (ch0)", "ardupilot-4.7.2", "E1-default-serial0", "E2-signed-serial0"),
            ("ArduPilot 4.7.2 SERIAL1", "ardupilot-4.7.2", "E1-default-serial1", "E2-signed-serial1"),
            ("PX4 1.17.0 GCS", "px4-1.17.0", "E3-default-gcs", "E4-signed-gcs"),
            ("PX4 1.18.0-rc1 GCS", "px4-1.18.0-rc1", "E3-default-gcs", "E4-signed-gcs")]
    fig, ax = plt.subplots(figsize=(COL2, 2.4))
    y = np.arange(len(rows))
    for i, (label, folder, before, after) in enumerate(rows):
        d = load(folder)["runs"]
        b, a = d[before], d[after]
        pre = 100.0 * b["signed_frames"] / max(b["frames"], 1)
        post = 100.0 * a["signed_frames"] / max(a["frames"], 1)
        ax.plot([pre, post], [i, i], color="#bbbbbb", lw=4, solid_capstyle="round", zorder=1)
        ax.scatter(pre, i, color=PALETTE[1], zorder=3, s=30, label="default" if i == 0 else None)
        ax.scatter(post, i, color=PALETTE[3], zorder=3, s=30, label="after provisioning" if i == 0 else None)
        if a["unsigned_probe_answered"]:
            ax.annotate("still answers\nunsigned", (post, i), textcoords="offset points",
                        xytext=(8, 0), va="center", fontsize=5.5, color=PALETTE[4])
    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in rows], fontsize=6.5)
    ax.set_xlim(-3, 115)
    ax.set_xlabel("signed outbound frames (%)")
    ax.set_title("Provisioning a key: PX4 1.17 unaffected; ArduPilot ch0 signs yet still accepts unsigned input")
    ax.legend(loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.32))
    save(fig, FIG / "fig_provisioning.pdf")


# ---------------------------------------------------------------- Fig 3: passive vs active
def fig_passive_vs_active():
    d = load("ardupilot-4.7.2")["runs"]
    s0, s1 = d["E2-signed-serial0"], d["E2-signed-serial1"]
    fig, ax = plt.subplots(figsize=(COL1, 2.1))
    cats = ["SERIAL0\n(ch0, trusted)", "SERIAL1\n(untrusted)"]
    passive = [100.0 * s0["signed_frames"] / s0["frames"], 100.0 * s1["signed_frames"] / s1["frames"]]
    active = [s0["unsigned_probe_answered"], s1["unsigned_probe_answered"]]
    x = np.arange(2)
    ax.bar(x, passive, width=0.5, color=PALETTE[2])
    for i, a in enumerate(active):
        ax.annotate("active probe:\n" + ("ANSWERED\n(unprotected)" if a else "ignored\n(protected)"),
                    (i, 50), ha="center", va="center", fontsize=6,
                    color=PALETTE[4] if a else PALETTE[3], weight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(cats, fontsize=7)
    ax.set_ylim(0, 105)
    ax.set_ylabel("signed frames (%)")
    ax.set_title("Passive view vs active probe\n(ArduPilot 4.7.2, signing enabled)", fontsize=7.5)
    save(fig, FIG / "fig_passive_vs_active.pdf")


# ---------------------------------------------------------------- Fig 4: model property matrix
def fig_model_matrix():
    data = json.loads((REPO / "results/model/model-results.json").read_text())
    rows = data["rows"]
    policies = sorted({r["policy"] for r in rows})
    scenarios = []
    for r in rows:
        if r["scenario"] not in scenarios:
            scenarios.append(r["scenario"])
    props = ["P1", "P2", "P3", "P4", "P5", "P6"]
    # one subplot per property is overkill; make a composite: rows=policy×scenario, cols=props
    labels = [f"{r['policy']} / {r['scenario'][:28]}" for r in rows]
    M = np.array([[1 if r[p] else 0 for p in props] for r in rows])
    failure = np.array([1, 1, 1, 0, 0, 0])  # P1-3 bad, P4-6 exposure
    fig, ax = plt.subplots(figsize=(COL2, 0.22 * len(rows) + 0.8))
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if M[i, j]:
                color = PALETTE[4] if failure[j] else PALETTE[1]
                ax.scatter(j, i, marker="s", s=70, color=color)
            else:
                ax.scatter(j, i, marker=".", s=8, color="#cccccc")
    ax.set_xticks(range(len(props)))
    ax.set_xticklabels(props)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=5.5)
    ax.set_xlim(-0.5, len(props) - 0.5)
    ax.set_ylim(-0.5, len(labels) - 0.5)
    ax.invert_yaxis()
    ax.grid(True, which="both", lw=0.3, alpha=0.3)
    ax.set_title("Model exploration: security failures (red) and exposure facts (orange)", fontsize=7.5)
    save(fig, FIG / "fig_model_matrix.pdf")


if __name__ == "__main__":
    fig_default_posture()
    fig_provisioning()
    fig_passive_vs_active()
    fig_model_matrix()
    print("all figures written to", FIG)
