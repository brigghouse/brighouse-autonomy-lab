"""Turn results/longitudinal/index.json into a table, a timeline figure, and a
machine-readable summary. Works with partial data (reruns as builds complete).

    python scripts/longitudinal_report.py --index results/longitudinal/index.json \
        --out results/longitudinal --fig papers/common/figures/fig_longitudinal.pdf
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "papers" / "common"))


def parse_ver(ref: str):
    m = re.search(r"(\d+)\.(\d+)\.(\d+)", ref)
    return tuple(int(x) for x in m.groups()) if m else (0, 0, 0)


def classify(entry) -> dict:
    """Reduce one version's measurements to a signing-posture verdict."""
    stack = entry["stack"]
    ref = entry["ref"]
    if entry.get("build") != "ok":
        return {"stack": stack, "ref": ref, "ver": parse_ver(ref), "status": entry.get("build", "?"),
                "default_signed": None, "can_sign": None, "ch0_exempt": None}
    m = entry.get("measurements", {})
    # A build that produced no telemetry (e.g. PX4 SIH-model drift) is "built but not measured".
    default_probe = next((v for k, v in m.items() if k.startswith("default")), {})
    if not default_probe.get("frames"):
        return {"stack": stack, "ref": ref, "ver": parse_ver(ref), "status": "ok (not measured)",
                "default_signed": None, "can_sign": None, "ch0_exempt": None}
    default_key = next((k for k in m if k.startswith("default")), None)
    prov_key = next((k for k in m if k.startswith("provisioned")), None)
    default = m.get(default_key, {}) if default_key else {}
    prov = m.get(prov_key, {}) if prov_key else {}
    default_signed = bool(default.get("signed_frames", 0))
    can_sign = bool(prov.get("signed_frames", 0)) if prov else False
    # ch0/console exemption: signs outbound but still answers unsigned read after provisioning
    ch0_exempt = bool(prov.get("signed_frames", 0)) and bool(prov.get("unsigned_probe_answered"))
    keyed = prov.get("keyed_check") or {}
    return {"stack": stack, "ref": ref, "ver": parse_ver(ref), "status": "ok",
            "firmware": default.get("firmware"),
            "default_signed": default_signed, "can_sign": can_sign, "ch0_exempt": ch0_exempt,
            "valid_sig": keyed.get("valid_signatures"), "frames_decoded": keyed.get("frames_decoded")}


def table_md(rows) -> str:
    out = ["| Stack | Version | Build | Default signs | Signing works | Console exempt after provisioning |",
           "|---|---|---|---|---|---|"]
    yn = lambda v: "—" if v is None else ("yes" if v else "no")
    for r in rows:
        out.append(f"| {r['stack']} | {r['ref']} | {r['status']} | {yn(r['default_signed'])} | "
                   f"{yn(r['can_sign'])} | {yn(r['ch0_exempt'])} |")
    return "\n".join(out)


def table_tex(rows) -> str:
    yn = lambda v: "—" if v is None else ("y" if v else "n")
    head = ("\\begin{table}[t]\n\\caption{Signing posture by release "
            "(auto-generated).}\n\\label{tab:long}\n\\centering\\footnotesize\n"
            "\\begin{tabular}{@{}llccc@{}}\n\\toprule\nstack & version & avail & "
            "default-on & console-exempt \\\\\n\\midrule\n")
    body = "".join(f"{r['stack']} & {r['ref'].replace('_','-')} & {yn(r['can_sign'])} & "
                   f"{yn(r['default_signed'])} & {yn(r['ch0_exempt'])} \\\\\n" for r in rows)
    return head + body + "\\bottomrule\n\\end{tabular}\n\\end{table}\n"


def make_figure(rows, path):
    import figstyle  # noqa
    from figstyle import COL2, PALETTE, save
    figstyle.apply()
    import matplotlib.pyplot as plt

    stacks = ["ardupilot", "px4"]
    fig, axes = plt.subplots(1, 2, figsize=(COL2, 2.4), sharey=False)
    for ax, stack in zip(axes, stacks):
        srows = sorted([r for r in rows if r["stack"] == stack], key=lambda r: r["ver"])
        xs = [f"{r['ver'][0]}.{r['ver'][1]}.{r['ver'][2]}" for r in srows]
        x = range(len(srows))
        # three posture lines: can_sign, default_signs, console_exempt
        can = [1 if r["can_sign"] else 0 for r in srows]
        dflt = [1 if r["default_signed"] else 0 for r in srows]
        exempt = [1 if r["ch0_exempt"] else 0 for r in srows]
        failed = [i for i, r in enumerate(srows) if r["status"] != "ok"]
        ax.step(x, can, where="mid", color=PALETTE[3], label="signing available", lw=1.4)
        ax.step(x, dflt, where="mid", color=PALETTE[1], label="on by default", lw=1.4, linestyle="--")
        ax.step(x, exempt, where="mid", color=PALETTE[4], label="console exempt", lw=1.0, linestyle=":")
        for i in failed:
            ax.scatter(i, 0.5, marker="x", color="#999999", s=20)
        ax.set_xticks(list(x))
        ax.set_xticklabels(xs, rotation=90, fontsize=5)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["no", "yes"])
        ax.set_ylim(-0.2, 1.2)
        ax.set_title(stack, fontsize=8)
    axes[0].legend(loc="center left", bbox_to_anchor=(0, -0.55), ncol=3, fontsize=6)
    fig.suptitle("Evolution of signing posture across releases", fontsize=8, y=1.02)
    save(fig, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", type=Path, default=Path("results/longitudinal/index.json"))
    ap.add_argument("--out", type=Path, default=Path("results/longitudinal"))
    ap.add_argument("--fig", type=Path, default=Path("papers/common/figures/fig_longitudinal.pdf"))
    a = ap.parse_args()
    if not a.index.exists():
        print("no index yet:", a.index)
        return
    data = json.loads(a.index.read_text())
    rows = sorted((classify(v) for v in data.values()), key=lambda r: (r["stack"], r["ver"]))
    summary = {"generated": date.today().isoformat(), "versions": len(rows), "rows": rows}
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "summary.json").write_text(json.dumps(summary, indent=2, default=list))
    (a.out / "TABLE.md").write_text(table_md(rows) + "\n")
    tex = Path("papers/paper2-longitudinal/results_table.tex")
    if tex.parent.exists():
        tex.write_text(table_tex(rows))
    print(table_md(rows))
    try:
        a.fig.parent.mkdir(parents=True, exist_ok=True)
        make_figure(rows, a.fig)
    except Exception as e:  # noqa: BLE001
        print("figure skipped:", e)


if __name__ == "__main__":
    main()
