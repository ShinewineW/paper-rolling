# .claude/skills/paper-landscape/scripts/output/branch1_llm.py
r"""branch1 (human report) via the LLM writer seam — the rich, vivid Chinese path.

When produce_outputs is given a ``write_report`` seam, the human report is WRITTEN
by an LLM (per config/llm.yaml writer routing) from the gated ARA, instead of the
thin deterministic write_branch1. This module then GROUNDS it deterministically:

  - a mechanically-anchored ``## 核心结论`` block (claim statements with every
    MD-present number three-layer-anchored),
  - the REAL evidence tables rendered verbatim (exact numbers live here),
  - a whole-report grounding pass (anchor any stray empirical number to the MD),
  - the SAME three-layer anchor hard-gate as write_branch1 (吸收-D1) — an
    unanchored empirical claim raises AnchorGateError before promotion.

So the rich LLM prose keeps loose performance numbers OUT of sentences (they live
in tables / anchored conclusions), staying faithful + gate-passing.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from scripts.output.anchor_lint import _is_empirical_assertion, lint_text
from scripts.output.branch1_report import AnchorGateError, _anchor, _find_in_md

_NUM = re.compile(r"\d+(?:\.\d+)?")
_FENCE = re.compile(r"^```")


def _claims_block(ara_dir: Path, md_text: str) -> str:
    """核心结论 — claim statements with every MD-present number anchored."""
    claims_md = ara_dir / "logic" / "claims.md"
    statements = (
        re.findall(r"(?m)^\s*[-*]?\s*\*\*Statement\*\*[:：]\s*(.+)$", claims_md.read_text("utf-8"))
        if claims_md.exists()
        else []
    )
    out = ["## 核心结论", "", "> 每条结论后的隐形锚点把数字回链到论文原文(忠实性保证)。", ""]
    if not statements:
        out.append("(未解析到结论)")
        return "\n".join(out)
    for i, st in enumerate(statements, 1):
        sentence = st.strip()
        for n in _NUM.findall(sentence):
            window = _find_in_md(md_text, n)
            if window:
                sentence += _anchor(window)
        out.append(f"{i}. {sentence}")
    return "\n".join(out)


def _evidence_tables(ara_dir: Path) -> str:
    """Render the real gated evidence tables verbatim (exact numbers live here)."""
    tdir = ara_dir / "evidence" / "tables"
    out = ["### 实验数据表(原始数值,引自论文)", ""]
    if tdir.is_dir():
        for f in sorted(tdir.glob("*.md")):
            # Demote the table file's own `# Title` so the report keeps one H1.
            out.append(re.sub(r"(?m)^#\s+", "#### ", f.read_text("utf-8").strip()))
            out.append("")
    return "\n".join(out)


def _ground_line(line: str, md_text: str) -> str:
    """Anchor every MD-present number on an empirical line lacking a ref."""
    if "<!--ref:" in line or not _is_empirical_assertion(re.sub(r"<!--.*?-->", "", line)):
        return line
    anchored = line
    for n in _NUM.findall(line):
        window = _find_in_md(md_text, n)
        if window:
            anchored += _anchor(window)
    return anchored


def _ground_report(report: str, md_text: str) -> str:
    """Grounding safety net: anchor stray empirical sentences (skip code/tables)."""
    out: list[str] = []
    in_fence = False
    for line in report.splitlines():
        if _FENCE.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        out.append(
            line if (in_fence or line.lstrip().startswith("|")) else _ground_line(line, md_text)
        )
    return "\n".join(out)


def _html(title: str, markdown: str) -> str:
    """Self-contained HTML: marked.js renders the MD, mermaid.js the diagrams."""
    md_js = json.dumps(markdown)
    return (
        "<!doctype html><html lang=zh><head><meta charset=utf-8>"
        "<meta name=viewport content='width=device-width,initial-scale=1'>"
        f"<title>{title} — 深度解读</title>"
        "<script src='https://cdn.jsdelivr.net/npm/marked/marked.min.js'></script>"
        "<script type=module>import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';"
        "mermaid.initialize({startOnLoad:false,theme:'dark'});window.__mermaid=mermaid;</script>"
        "<style>body{background:#0d1117;color:#e6edf3;font-family:-apple-system,'Segoe UI',sans-serif;"  # noqa: E501
        "line-height:1.8;max-width:860px;margin:0 auto;padding:3rem 1.5rem}"
        "h1{border-bottom:2px solid #30363d}h2{margin-top:2.5rem;color:#79c0ff}h3{color:#a5d6ff}"
        "pre{background:#161b22;padding:1rem;border-radius:8px;overflow:auto}"
        "table{border-collapse:collapse;width:100%;margin:1rem 0;font-size:.9em}"
        "td,th{border:1px solid #30363d;padding:.4rem .6rem}th{background:#161b22}"
        ".mermaid{background:#161b22;border-radius:8px;padding:1rem;margin:1rem 0}</style></head>"
        "<body><div id=doc></div>"
        f"<script>const md={md_js};document.getElementById('doc').innerHTML=marked.parse(md);"
        "document.querySelectorAll('code.language-mermaid').forEach(c=>{"
        "const d=document.createElement('div');d.className='mermaid';d.textContent=c.textContent;"
        "c.closest('pre').replaceWith(d);});"
        "window.addEventListener('load',()=>window.__mermaid&&window.__mermaid.run());</script>"
        "</body></html>"
    )


def write_branch1_llm(
    person_dir: Path,
    candidate: Any,
    ara_dir: Path,
    md_path: Path,
    write_report: Any,
    *,
    key: str | None = None,
) -> None:
    """Write the LLM human report into ``person_dir`` (report.md + report.html).

    Calls the ``write_report`` seam (gated ARA -> vivid Chinese sections), stitches
    a mechanically-anchored 核心结论 + the real evidence tables + the sections,
    grounds the whole thing, and HARD-GATES on the three-layer anchor lint.

    Raises:
        AnchorGateError: the composed report failed the three-layer citation gate.
    """
    title = candidate["title"]
    key = key or person_dir.name
    md_text = md_path.read_text(encoding="utf-8")
    sections = write_report(ara_dir)  # {section_id: markdown}

    parts: list[str] = [
        f"# {title} — 深度解读",
        "",
        f"> 面向人类读者的深度解读(中文)。事实源与配对的 AI 知识包 `ai_package/{key}/ara/` 同源,均已通过数据保真审计。",  # noqa: E501
        "",
        _claims_block(ara_dir, md_text),
    ]
    for sid in sorted(sections):
        parts.append("")
        parts.append(str(sections[sid]).strip())
        if sid.startswith("06"):  # append the gated tables after 实验与对比
            parts.append("")
            parts.append(_evidence_tables(ara_dir))

    report = _ground_report("\n".join(parts) + "\n", md_text)
    violations = lint_text(report)
    if violations:
        raise AnchorGateError(
            "branch1 (LLM) failed three-layer citation gate (吸收-D1): "
            + "; ".join(v.message for v in violations[:5])
        )

    person_dir.mkdir(parents=True, exist_ok=True)
    (person_dir / "report.md").write_text(report, encoding="utf-8")
    (person_dir / "report.html").write_text(_html(title, report), encoding="utf-8")
