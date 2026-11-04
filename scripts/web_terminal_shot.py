#!/usr/bin/env python3
"""Render the terminal figure for the product page from a REAL mavaudit run.

This script exists because the previous figure did not come from one. It showed a
`secure-by-default score ... grade D` line, and mavaudit's CLI has never emitted a score
from `scan` -- there is one subcommand and `cli.py` contains no scoring. The line had been
composited in, while CREDITS.md stated the text was verbatim tool output. On a page whose
argument is "evidence, not guesswork", that was the worst thing on it.

So: run the tool, capture stdout, render those bytes and nothing else. The score belongs to
`scripts/scores.py` and is shown by the chart underneath the figure, which is where a number
the CLI does not print should live.

    python scripts/web_terminal_shot.py --input run.txt --out assets/mavaudit-report.png
"""
import argparse, html, pathlib, subprocess, sys

TEMPLATE = """<!doctype html><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:transparent;font:13.5px/1.62 ui-monospace,"SF Mono",Menlo,Consolas,monospace}}
.win{{width:1180px;background:#070d18;border:1px solid #16304d;border-radius:12px;overflow:hidden;
  box-shadow:0 24px 70px rgba(0,0,0,.6)}}
.bar{{display:flex;align-items:center;gap:8px;padding:11px 16px;background:#0b1626;
  border-bottom:1px solid #16304d}}
.dot{{width:11px;height:11px;border-radius:50%}}
.t{{margin-left:10px;color:#6B7D93;font-size:12px;letter-spacing:.04em}}
pre{{padding:20px 24px 24px;color:#C6D4E6;white-space:pre-wrap;word-break:break-word}}
.c{{color:#9DEAF4}} .hi{{color:#FFB4A2;font-weight:600}} .ok{{color:#9FE8B5}}
.dim{{color:#6B7D93}} .b{{color:#F7FBFF;font-weight:600}}
</style><div class="win"><div class="bar">
<span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span>
<span class="dot" style="background:#28c840"></span><span class="t">{title}</span></div>
<pre>{body}</pre></div>"""


def markup(text: str) -> str:
    out = []
    for line in text.splitlines():
        e = html.escape(line)
        if line.startswith("$"):
            e = f'<span class="c">{e}</span>'
        elif "[HIGH]" in line:
            e = e.replace("[HIGH]", '<span class="hi">[HIGH]</span>')
            e = f'<span class="b">{e}</span>'
        elif "[INFO]" in line:
            e = e.replace("[INFO]", '<span class="ok">[INFO]</span>')
        elif line.startswith("- ") or line.startswith("_"):
            e = f'<span class="dim">{e}</span>'
        out.append(e)
    return "\n".join(out)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=pathlib.Path, required=True,
                   help="file holding the verbatim stdout of a mavaudit run")
    p.add_argument("--out", type=pathlib.Path, required=True)
    p.add_argument("--title", default="mavaudit — ArduPilot 4.7.2 (SITL, read-only)")
    a = p.parse_args()
    body = markup(a.input.read_text().rstrip())
    tmp = pathlib.Path("/tmp/_term.html")
    tmp.write_text(TEMPLATE.format(title=html.escape(a.title), body=body))
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch(args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": 1240, "height": 900}, device_scale_factor=2)
        pg.goto(tmp.as_uri()); pg.wait_for_timeout(400)
        pg.locator(".win").screenshot(path=str(a.out), omit_background=True)
        b.close()
    print(f"wrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
