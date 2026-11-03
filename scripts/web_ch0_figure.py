"""Figure for the web page: does the exemption follow the channel index or the transport?
Drawn from results/ch0-configs/ch0-configs.json. Regenerate with this script."""
import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

d = json.load(open("/home/claude/brighouse-autonomy-lab/results/ch0-configs/ch0-configs.json"))
by = {c["config"]: c for c in d["configs"]}

def keyed(cfg, link):
    c = next(x for x in by[cfg]["cases"]
             if x["state"] == "keyed" and x["link"] == link and x["signed"] is False)
    return c["observed"], c["transport"].replace("udpin", "UDP").replace("tcp", "TCP"), c["wire"]

order = [("A-ch0tcp-ch1tcp", "A"), ("B-ch0udp-ch1tcp", "B"),
         ("C-ch0tcp-ch1udp", "C"), ("D-ch0tcp-ch1mav1", "D")]
BG, FG, MUT = "#02060D", "#F7FBFF", "#8FA3B8"
OPEN, SHUT = "#FF9D8A", "#9DEAF4"

fig, ax = plt.subplots(figsize=(9.0, 4.3), dpi=200)
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
ax.set_xlim(0, 10); ax.set_ylim(0, 4.9); ax.axis("off")

ax.text(0.15, 4.62, "Key active. An unsigned read arrives. Is it answered?",
        color=FG, fontsize=11.5, fontweight="bold")
ax.text(0.15, 4.28, "ArduPilot Copter 4.7.2 in simulation, 3 November 2026 — results/ch0-configs",
        color=MUT, fontsize=8.5)
ax.text(3.15, 3.85, "channel 0", color=MUT, fontsize=9, ha="center")
ax.text(6.9, 3.85, "channel 1", color=MUT, fontsize=9, ha="center")

for i, (cfg, letter) in enumerate(order):
    y = 3.1 - i * 0.78
    ax.text(0.15, y + .1, letter, color=FG, fontsize=11, fontweight="bold")
    for j, link in enumerate(("ch0", "ch1")):
        obs, transport, wire = keyed(cfg, link)
        x = 1.4 + j * 3.75
        col = OPEN if obs else SHUT
        ax.add_patch(FancyBboxPatch((x, y - .17), 3.1, .56, boxstyle="round,pad=0.02,rounding_size=0.1",
                                    facecolor=col, alpha=.14, edgecolor=col, linewidth=1.1))
        label = f"{transport}" + ("  ·  MAVLink 1" if wire == 1 else "")
        ax.text(x + .18, y + .17, label, color=FG, fontsize=9.5, va="center")
        ax.text(x + 2.92, y + .17, "answered" if obs else "rejected", color=col,
                fontsize=9.5, va="center", ha="right", fontweight="bold")

ax.text(0.15, 0.32, "B and C differ in one thing: which channel number carries the UDP link.",
        color=FG, fontsize=9.6)
ax.text(0.15, 0.02, "The decision flips with the number, not the transport. "
                    "If your radio sits on channel 0, that is your exposure.",
        color=MUT, fontsize=9.2)
fig.tight_layout()
fig.savefig("/home/claude/assets/ch0-finding.png", facecolor=BG, bbox_inches="tight")
print("wrote assets/ch0-finding.png")
