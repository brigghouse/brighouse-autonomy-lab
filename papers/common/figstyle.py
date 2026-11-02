"""Shared matplotlib style for IEEE-column figures.

Vector PDF output, Type-1/TrueType fonts embedded, grayscale-safe palettes, no chartjunk.
Single-column width is 3.5 in; double-column 7.16 in (IEEEtran).
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

COL1, COL2 = 3.5, 7.16  # IEEE column widths in inches

# Grayscale-safe, colour-blind-friendly categorical palette (Okabe-Ito subset).
PALETTE = ["#000000", "#E69F00", "#56B4E9", "#009E73", "#CC79A7", "#0072B2"]
GRAYS = ["#222222", "#777777", "#bbbbbb"]


def apply():
    plt.rcParams.update({
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "pdf.fonttype": 42,       # embed TrueType, not Type-3
        "ps.fonttype": 42,
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 8,
        "axes.titlesize": 8,
        "axes.labelsize": 8,
        "legend.fontsize": 7,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.linewidth": 0.4,
        "grid.alpha": 0.4,
        "lines.linewidth": 1.2,
        "lines.markersize": 4,
        "legend.frameon": False,
    })


def save(fig, path):
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)
