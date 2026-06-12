# .claude/skills/paper-landscape/scripts/output/branch1_llm.py
r"""branch1 (human report) via the LLM writer seam — the rich, vivid Chinese path.

When produce_outputs is given a ``write_report`` seam, the human report is WRITTEN
by an LLM (per config/llm.yaml writer routing) from the gated ARA, instead of the
thin deterministic write_branch1. This module then GROUNDS it deterministically:

  - a mechanically-anchored ``## 核心结论`` block (claim statements with every
    MD-present number three-layer-anchored),
  - the REAL evidence tables rendered verbatim (exact numbers live here),
  - a whole-report grounding pass (anchor any stray empirical number to the MD),
  - the branch1 忠实门 (ADR-0012): anchor-form lint + tolerant prose-number
    grounding + optional LLM faithfulness judge, checked by branch1_gate before
    promotion.

So the rich LLM prose keeps loose performance numbers OUT of sentences (they live
in tables / anchored conclusions), staying faithful + gate-passing.
"""

from __future__ import annotations

import base64
import json
import re
from pathlib import Path
from typing import Any

from scripts.output.anchor_lint import _is_empirical_assertion
from scripts.output.branch1_gate import check_report_faithfulness
from scripts.output.branch1_report import AnchorGateError, _anchor, _find_in_md
from scripts.output.figures import Figure, copy_figures, is_architecture_caption

_NUM = re.compile(r"\d+(?:\.\d+)?")
_FENCE = re.compile(r"^```")

# Project IRON RULE: NO emoji in ANY report. Strip them (and a trailing space)
# deterministically in the assembler so style is uniform regardless of the writer
# model. Targets the emoji/pictograph/dingbat blocks; leaves CJK, math, and plain
# arrows (→ U+2192, used in prose/diagrams) untouched.
_EMOJI = re.compile(
    "[\U0001f1e6-\U0001f1ff\U0001f300-\U0001f5ff\U0001f600-\U0001f64f"
    "\U0001f680-\U0001f6ff\U0001f700-\U0001f77f\U0001f780-\U0001f7ff"
    "\U0001f800-\U0001f8ff\U0001f900-\U0001f9ff\U0001fa00-\U0001faff"
    "\U00002600-\U000026ff\U00002700-\U000027bf\U00002b00-\U00002bff"
    "\U00002300-\U000023ff\ufe0f\u200d]+[ \t]*"
)
# Mermaid 11 rejects unquoted node labels containing special chars (>, +, (), …).
_MERMAID_LABEL = re.compile(r"\[([^\]\n\"]+)\]")


def _strip_emoji(text: str) -> str:
    """Remove every emoji/pictograph (+ trailing space) — the no-emoji iron rule."""
    return _EMOJI.sub("", text)


def _quote_mermaid_labels(report: str) -> str:
    """Quote ``[label]`` node/subgraph labels inside ```mermaid blocks so labels
    with special chars (>, +, parentheses, …) parse under strict mermaid 11."""
    out: list[str] = []
    in_mermaid = False
    for line in report.splitlines():
        if line.strip().startswith("```"):
            in_mermaid = line.strip().startswith("```mermaid")
            out.append(line)
            continue
        if in_mermaid:
            line = _MERMAID_LABEL.sub(lambda m: f'["{m.group(1).strip()}"]', line)
        out.append(line)
    return "\n".join(out)


def _fig_block(figures: list[Figure], zh: dict[str, str], *, heading: str = "") -> str:
    """Render a group of original figures INLINE: each image followed by an italic
    Chinese caption (the science-pop gloss; falls back to the paper's own caption).
    Used to weave figures into the relevant sections (intro / method / results)."""
    out: list[str] = [heading] if heading else []
    for f in figures:
        out += ["", f"![]({f.ref})"]
        cap = (zh.get(f.ref) or f.caption or "").strip()
        if cap:
            out += ["", f"*{cap}*"]
    return "\n".join(out)


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


def _inline_images(markdown: str, img_dir: Path) -> str:
    """Replace ``![alt](images/HASH.ext)`` with base64 data URIs so the HTML is
    fully self-contained — original figures render anywhere (file://, moved, etc.),
    not subject to a browser's local-subresource sandbox."""

    def repl(m: re.Match) -> str:
        p = img_dir / m.group(2)
        if not p.is_file():
            return m.group(0)
        ext = p.suffix.lstrip(".").lower() or "jpeg"
        ext = "jpeg" if ext == "jpg" else ext
        b64 = base64.b64encode(p.read_bytes()).decode("ascii")
        return f"![{m.group(1)}](data:image/{ext};base64,{b64})"

    return re.sub(r"!\[([^\]]*)\]\((images/[^)\s]+)\)", repl, markdown)


def _html(title: str, markdown: str, img_dir: Path) -> str:
    """Self-contained light-theme HTML: marked.js renders the MD, mermaid the
    diagrams; original figures are inlined as base64 (no external files)."""
    md_js = json.dumps(_inline_images(markdown, img_dir))
    return (
        "<!doctype html><html lang=zh><head><meta charset=utf-8>"
        "<meta name=viewport content='width=device-width,initial-scale=1'>"
        f"<title>{title} — 深度解读</title>"
        "<script src='https://cdn.jsdelivr.net/npm/marked/marked.min.js'></script>"
        "<script>window.MathJax={startup:{typeset:false},"
        "tex:{inlineMath:[['$','$'],['\\\\(','\\\\)']],displayMath:[['$$','$$'],['\\\\[','\\\\]']]},"
        "options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script>"
        "<script src='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'></script>"
        "<script type=module>import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';"
        "mermaid.initialize({startOnLoad:false,theme:'default',securityLevel:'loose'});"
        "window.__mermaid=mermaid;</script>"
        "<style>body{background:#ffffff;color:#1f2328;font-family:-apple-system,'Segoe UI',sans-serif;"  # noqa: E501
        "line-height:1.8;max-width:860px;margin:0 auto;padding:3rem 1.5rem}"
        "h1{border-bottom:2px solid #d0d7de;padding-bottom:.3rem}"
        "h2{margin-top:2.5rem;color:#0969da}h3{color:#0a3069}h4{color:#0a3069}"
        "a{color:#0969da}pre{background:#f6f8fa;padding:1rem;border-radius:8px;overflow:auto}"
        "code{background:#eff1f3;padding:.1rem .3rem;border-radius:4px}"
        "pre code{background:none;padding:0}"
        "blockquote{color:#57606a;border-left:.25rem solid #d0d7de;margin:1rem 0;padding:0 1rem}"
        "img{max-width:100%;height:auto;border:1px solid #d0d7de;border-radius:6px;"
        "margin:1rem 0;display:block}"
        "figcaption,em{color:#57606a}"
        "table{border-collapse:collapse;width:100%;margin:1rem 0;font-size:.9em}"
        "td,th{border:1px solid #d0d7de;padding:.4rem .6rem}th{background:#f6f8fa}"
        ".mermaid{background:#f6f8fa;border-radius:8px;padding:1rem;margin:1rem 0}</style></head>"
        "<body><div id=doc></div>"
        f"<script>const md={md_js};"
        # Protect $$..$$ / $..$ from marked (which would mangle \\ and _ in LaTeX),
        # render markdown, then restore the raw math for MathJax to typeset.
        "const store=[];"
        "let src=md.replace(/\\$\\$([\\s\\S]+?)\\$\\$/g,function(m){store.push(m);"
        "return '@@M'+(store.length-1)+'@@';})"
        ".replace(/\\$([^\\n$]+?)\\$/g,function(m){store.push(m);"
        "return '@@M'+(store.length-1)+'@@';});"
        "let html=marked.parse(src).replace(/@@M(\\d+)@@/g,function(_,i){return store[i];});"
        "document.getElementById('doc').innerHTML=html;"
        "document.querySelectorAll('code.language-mermaid').forEach(function(c){"
        "var d=document.createElement('div');d.className='mermaid';d.textContent=c.textContent;"
        "c.closest('pre').replaceWith(d);});"
        "window.addEventListener('load',function(){"
        "if(window.__mermaid){window.__mermaid.run({suppressErrors:true});}"
        "if(window.MathJax&&MathJax.typesetPromise){MathJax.typesetPromise();}});</script>"
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
    prior_failure: str | None = None,
    faithfulness_judge: Any = None,
    report_tolerant: bool = True,
    report_max_unconfirmed: int = 5,
    report_max_unconfirmed_ratio: float = 0.2,
) -> None:
    """Write the LLM human report into ``person_dir`` (report.md + report.html).

    Calls the ``write_report`` seam (gated ARA -> vivid Chinese sections), stitches
    a mechanically-anchored 核心结论 + the real evidence tables + the sections,
    grounds the whole thing, and HARD-GATES on the 忠实门 (ADR-0012).

    Raises:
        AnchorGateError: the composed report failed the 忠实門.
    """
    title = candidate["title"]
    key = key or person_dir.name
    md_text = md_path.read_text(encoding="utf-8")

    # 审计 R5 Finding 1: only forward prior_failure when set, so an older injected
    # write_report fake/seam (without the param) stays TypeError-free on the happy
    # path — only an actual feedback re-emit requires the seam to know prior_failure.
    extra = {"prior_failure": prior_failure} if prior_failure is not None else {}
    result = write_report(ara_dir, md_path=md_path, **extra)
    # Tolerate the older flat {id: md} shape; the seam now returns sections+figures.
    sections = result.get("sections", result) if isinstance(result, dict) else result
    figures_meta = result.get("figures", []) if isinstance(result, dict) else []

    # SELECTIVE paper guided-tour: embed the CURATED original figures (mandatory
    # core method/structure diagram + a few representative result figures), NOT all.
    # Copy the referenced images into the vault so report.md / report.html resolve.
    person_dir.mkdir(parents=True, exist_ok=True)
    selected = [f for f in figures_meta if f.get("include")]
    figs = [Figure(ref=f["ref"], caption=f.get("caption", "")) for f in selected]
    copied = copy_figures(figs, md_path.parent, person_dir)
    zh = {f["ref"]: f.get("zh", "") for f in selected}

    # Group figures by role (doc order preserved) for SECTION-AWARE placement:
    # the overall架构图 sets the tone right after 导读; the structure sub-figures
    # sit with 方法与架构; result figures form a showcase after 实验.
    role_of = {f["ref"]: f.get("role", "other") for f in selected}
    arch = [f for f in copied if role_of.get(f.ref) == "architecture"]
    results = [f for f in copied if role_of.get(f.ref) != "architecture"]
    primary_arch, rest_arch = arch[:1], arch[1:]

    parts: list[str] = [
        f"# {title} — 深度解读",
        "",
        f"> 面向人类读者的深度解读(中文)。事实源与配对的 AI 知识包 `ai_package/{key}/ara/` 同源,均已通过数据保真审计。",  # noqa: E501
        "",
        _claims_block(ara_dir, md_text),
    ]
    emitted: set[str] = set()

    def _place(group: list[Figure], heading: str) -> None:
        if not group:
            return
        parts.append("")
        parts.append(_fig_block(group, zh, heading=heading))
        emitted.update(f.ref for f in group)

    for sid in sorted(sections):
        parts.append("")
        parts.append(str(sections[sid]).strip())
        if sid.startswith("01"):  # 初始定调:总体架构图紧跟导读
            _place(primary_arch, "**论文总体架构(原图):**")
        elif sid.startswith("04"):  # 方法论:模型结构与子图紧跟方法
            _place(rest_arch, "**模型结构与关键子图(原图):**")
        elif sid.startswith("06"):  # 实验:表格 + 效果示例
            parts.append("")
            parts.append(_evidence_tables(ara_dir))
            _place(results, "**效果示例(论文原图):**")
    # Backstop: any copied figure not yet placed (e.g. a section was missing) —
    # keep completeness by appending it so the mandatory figures never vanish.
    leftover = [f for f in copied if f.ref not in emitted]
    if leftover:
        parts.append("")
        parts.append(_fig_block(leftover, zh, heading="## 其余论文原图"))

    assembled = _strip_emoji("\n".join(parts) + "\n")  # no-emoji iron rule
    assembled = _quote_mermaid_labels(assembled)  # make LLM mermaid parse-safe
    report = _ground_report(assembled, md_text)
    hard = check_report_faithfulness(
        report,
        md_text,
        ara_dir,
        judge=faithfulness_judge,
        tolerant=report_tolerant,
        max_unconfirmed=report_max_unconfirmed,
        max_unconfirmed_ratio=report_max_unconfirmed_ratio,
    )
    if hard:
        raise AnchorGateError(
            "branch1 (LLM) report failed 忠实门 (ADR-0012): "
            + "; ".join(f.observation for f in hard[:5])
        )
    # Every SELECTED figure must be embedded...
    missing = [f.ref for f in copied if f"({f.ref})" not in report]
    if missing:
        raise AnchorGateError(f"branch1 (LLM) missing selected figures: {missing}")
    # ...and MANDATORY: the core method / model-structure figure must be present.
    copied_refs = {f.ref for f in copied}
    arch_in = any(f.get("role") == "architecture" and f["ref"] in copied_refs for f in selected)
    paper_has_arch = any(is_architecture_caption(f.get("caption", "")) for f in figures_meta)
    if paper_has_arch and not arch_in:
        raise AnchorGateError(
            "branch1 (LLM): the core method/model-structure figure is mandatory "
            "but none was embedded"
        )

    (person_dir / "report.md").write_text(report, encoding="utf-8")
    (person_dir / "report.html").write_text(_html(title, report, person_dir), encoding="utf-8")
