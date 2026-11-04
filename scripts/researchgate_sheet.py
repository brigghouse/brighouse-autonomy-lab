"""Generate the ResearchGate submission sheet from the papers' own LaTeX.

The previous sheet was typed by hand and went stale: it still carried Paper 2's
withdrawn primacy claim weeks after the .tex had dropped it, so the text to paste
into the abstract field contradicted the PDF underneath it. Generated now.

    python scripts/researchgate_sheet.py > /tmp/COMO-SUBIR.md
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = [
    ("paper1-signing", "paper1-signing.pdf"),
    ("paper2-longitudinal", "paper2-longitudinal.pdf"),
    ("paper3-formal", "paper3-formal.pdf"),
    ("paper4-score", "paper4-score.pdf"),
]


def detex(s: str) -> str:
    s = re.sub(r"%.*", "", s)
    # Drop citation/label commands WITH their argument first. Stripping the command
    # alone leaves the bib keys in the prose, which is what the hand-written sheet did.
    s = re.sub(r"\\(cite|citep|citet|label|ref|footnote)\{[^{}]*\}", "", s)
    s = s.replace("\\\\", " ")  # LaTeX line breaks in titles
    s = re.sub(r"\\(emph|textbf|textit|code|textsf|mathsf|text)\{([^{}]*)\}", r"\2", s)
    s = re.sub(r"\\\$|\$", "", s)
    s = s.replace("``", '"').replace("''", '"')
    s = s.replace("---", "\u2014").replace("--", "\u2013").replace("~", " ")
    s = re.sub(r"\\&", "&", s)
    s = re.sub(r"\\[a-zA-Z]+\s*", "", s)
    s = re.sub(r"[{}]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def field(tex: str, env: str) -> str:
    m = re.search(r"\\begin\{%s\}(.*?)\\end\{%s\}" % (env, env), tex, re.S)
    return detex(m.group(1)) if m else ""


def braced(tex: str, cmd: str) -> str:
    i = tex.find("\\" + cmd + "{")
    if i < 0:
        return ""
    j = i + len(cmd) + 2
    depth, out = 1, []
    while j < len(tex) and depth:
        c = tex[j]
        depth += (c == "{") - (c == "}")
        if depth:
            out.append(c)
        j += 1
    return detex("".join(out))


def main() -> int:
    out = ["# ResearchGate \u2014 qu\u00e9 subir y qu\u00e9 pegar en cada campo", "",
           "**Generado por `scripts/researchgate_sheet.py` desde los `.tex`.** No lo edites a",
           "mano: la versi\u00f3n anterior estaba escrita a mano y se qued\u00f3 desfasada \u2014 segu\u00eda",
           "llevando la reivindicaci\u00f3n de primac\u00eda que el Paper 2 ya hab\u00eda retirado, as\u00ed que el",
           "abstract que ibas a pegar contradec\u00eda al PDF de debajo.", "",
           "Cuatro preprints, en este orden.", "",
           "**Tipo:** Preprint. **No** \"Article\" \u2014 no est\u00e1n revisados por pares, y marcarlos",
           "como art\u00edculo es exactamente lo que nos quita la credibilidad que buscamos.", "",
           "**Aviso real:** ResearchGate da DOI a los preprints, pero si luego quieres mandar",
           "alguno a arXiv o a una conferencia, mira su pol\u00edtica de preprints antes. La mayor\u00eda",
           "de conferencias IEEE lo permiten; algunas revistas no.", ""]

    for d, pdf in PAPERS:
        tex = (ROOT / "papers" / d / "main.tex").read_text(encoding="utf-8")
        title = braced(tex, "title")
        abstract = field(tex, "abstract")
        kw = braced(tex, "IEEEkeywords") or field(tex, "IEEEkeywords")
        out += ["---", "", f"## {pdf}", "", "**T\u00edtulo:**", "", f"> {title}", "",
                "**Abstract:**", "", f"> {abstract}", ""]
        if kw:
            out += ["**Keywords:**", "", f"> {kw}", ""]

    out += ["---", "", "## Despu\u00e9s de subir", "",
            "Los DOIs que emita ResearchGate van a cuatro sitios, y los cuatro est\u00e1n",
            "escritos esperando: la p\u00e1gina de producto, el `README.md` del repo, el comentario",
            "en el issue de ArduPilot, y los 4 mensajes de LinkedIn.", ""]
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
