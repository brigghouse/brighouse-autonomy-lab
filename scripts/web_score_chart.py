"""Score chart for the web page, drawn from results/scores.json. Regenerate with:
   python /tmp/mkchart.py   (source of truth: the repo's recorded measurements)"""
import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = json.load(open("/home/claude/brighouse-autonomy-lab/results/scores/scores.json"))
rows = [r for r in d["cross_section"] if r["score"] is not None]
rows = sorted(rows, key=lambda r: r["score"])
labels = [r["label"].replace("ArduPilot 4.7.2", "ArduPilot 4.7.2\n").replace("PX4 1.1", "PX4 1.1")
          for r in rows]
scores = [r["score"] for r in rows]
BG, FG, MUT = "#02060D", "#F7FBFF", "#8FA3B8"
ACC, WARN, BAD = "#9DEAF4", "#F2C879", "#FF9D8A"
col = [ACC if s >= 75 else WARN if s >= 55 else BAD for s in scores]

fig, ax = plt.subplots(figsize=(8.6, 4.0), dpi=200)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
y = range(len(rows))
ax.barh(list(y), scores, color=col, height=.62)
ax.axvline(82, color=FG, lw=1, ls=(0, (4, 3)), alpha=.55)
ax.text(83.4, 1.15, "82 — the ceiling for\nMAVLink signing alone", color=FG, fontsize=8.5,
        va="center", alpha=.82)
for i, s in enumerate(scores):
    ax.text(s + 1.2, i, f"{s:.0f}", va="center", color=FG, fontsize=9.5, fontweight="bold")
ax.set_yticks(list(y)); ax.set_yticklabels(labels, color=MUT, fontsize=9)
ax.set_xlim(0, 108); ax.set_xticks([0, 25, 50, 75, 100])
ax.tick_params(colors=MUT, labelsize=8.5, length=0)
for sp in ax.spines.values(): sp.set_visible(False)
ax.grid(axis="x", color=FG, alpha=.07, lw=.8)
ax.set_axisbelow(True)
ax.set_xlabel("secure-by-default score (criteria v2) — measured 3 Nov 2026",
              color=MUT, fontsize=8.5, labelpad=9)
fig.tight_layout()
fig.savefig("/home/claude/assets/scores.png", facecolor=BG, bbox_inches="tight")
print("wrote assets/scores.png with", len(rows), "measured configurations")
