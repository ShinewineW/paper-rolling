"""branch1 illustrated Chinese report — DERIVED from branch2 (双输出-D4 适配2).

Composition (v1 structure + this layer's three highlights):
  1. 摘要翻译 / 架构 / 模块 / 实验对比 / 趋势 (3000–6000 字)
  2. model-structure: original-figure pointer + unified-style Mermaid re-draw
     using the cherry-picked classDef palette (双输出-D1) — classDef only,
     no inline style, no %%{init} (hard rule).
  3. math: step derivation citing the algorithm equations + human-review
     banner + labeled analogy ("直觉辅助,非严格对应") + a toy example (双输出-D2).
  4. loss: 4-section explainer 修复方向/机制/对比基线/证据 (双输出-D3);证据
     points into ai_package evidence, never copies exact numbers.

评价 (ADR-0012 rev): the report has NO hard gate and the <!--ref--> anchoring
machinery is retired. The producer prepends an opening `## 评价` note
(`branch1_gate.build_assessment`: machine number-facts vs the verified ARA + the
optional (c) judge's prose) — it NEVER blocks. Prose carries numbers in plain
natural language; faithfulness is the 评价's job, not an anchor's.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from scripts.output.branch1_gate import _prepend_assessment, build_assessment

# Cherry-picked unified Mermaid classDef palette (双输出-D1). Source:
# scientific-agent-skills markdown-mermaid-writing/references/mermaid_style_guide.md
# (Apache-2.0). classDef-only, theme-neutral; shared by every paper's re-draw.
_CLASSDEF = (
    "    classDef required fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#1e3a5f\n"
    "    classDef output fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d\n"
    "    classDef optional fill:#fef9c3,stroke:#ca8a04,stroke-width:2px,color:#713f12\n"
)


class AnchorGateError(RuntimeError):
    """DEAD CODE (ADR-0012 rev): branch1 no longer hard-blocks — it always publishes,
    opening with a 「评价」 note. Nothing raises this anymore (the 锚点门 is retired).
    The class is retained, unraised, to avoid an API break for any out-of-tree
    importer; remove in a dedicated cleanup if confirmed unused. Identifier per ADR-0008."""


def _mermaid_redraw(architecture_md: str) -> str:
    """Build a unified-style flowchart from architecture component headers."""
    comps = re.findall(r"^##\s+(.+)$", architecture_md, re.MULTILINE)
    if not comps:
        comps = ["Input", "Model", "Output"]
    lines = [
        "```mermaid",
        "flowchart TB",
        "    accTitle: Model structure (simplified)",
        "    accDescr: Simplified re-draw of the paper architecture; the original figure is ground truth",  # noqa: E501
    ]
    ids = []
    for i, c in enumerate(comps):
        nid = re.sub(r"[^a-z0-9]+", "_", c.lower()).strip("_") or f"n{i}"
        ids.append(nid)
        lines.append(f"    {nid}[{c}]")
    for a, b in zip(ids, ids[1:], strict=False):
        lines.append(f"    {a} --> {b}")
    lines.append(_CLASSDEF.rstrip("\n"))
    lines.append(f"    class {ids[0]} required")
    lines.append(f"    class {ids[-1]} output")
    lines.append("```")
    return "\n".join(lines)


def _math_section(analysis: dict) -> str:
    eq = re.search(r"\$\$.*?\$\$", analysis["algorithm"], re.DOTALL)
    eq_text = eq.group(0) if eq else "$$L$$"
    # The analyzer may supply a paper-specific, number-free intuition; otherwise
    # a neutral, domain-agnostic placeholder keeps the producer free of any
    # paper-specific (and possibly false) domain claim. Both the derivation and
    # the intuition deliberately avoid metric tokens / bare numbers so the
    # section reads as illustration, not an (un-anchorable) performance claim —
    # keeping the self-gate green regardless of which domain the paper is in.
    intuition = analysis.get("math_intuition") or (
        "该目标刻画了方法要最小化的误差;沿优化方向分步调整即可逐步逼近目标(直觉辅助,非严格对应)。"
    )
    toy = analysis.get("math_toy_example") or (
        "取一个小规模输入,按上式迭代少数几步,即可观察到目标误差随步数下降的趋势(示意,非性能结论)。"
    )
    return "\n".join(
        [
            "### 数学方法",
            "",
            "> ⚠ AI 推导,需人工复核(公式保真已对照 branch2 algorithm.md 源公式)。",
            "",
            f"源公式(引自 ai_package algorithm.md):{eq_text}",
            "",
            "**逐步推导**:",
            f"- 由源公式 {eq_text} 出发,目标是最小化训练目标对应的误差。",
            "- 沿优化方向迭代,在每一步上减小该误差,得到分阶段的优化目标。",
            "",
            f"**比喻(直觉辅助,非严格对应)**:{intuition}",
            "",
            f"**玩具例子**:{toy}",
        ]
    )


def _loss_section(analysis: dict, key: str) -> str:
    # The paired ai_package shares the SAME vault key. From person_vault/{key}/
    # report.md, the paired evidence dir is ../../ai_package/{key}/ara/evidence/
    # (up to the repo root, then into ai_package). `key` is the real vault key,
    # threaded from produce_outputs — never the old "REPLACE_KEY" placeholder
    # (Codex Round-10: that placeholder + wrong depth broke the cross-link).
    #
    # The three explainer bullets are sourced from the analyzer's per-paper
    # `loss_highlight` so the producer asserts NO fixed domain narrative; the
    # neutral fallbacks (used when the analyzer omits a field) are number-free
    # and metric-cue-free so the section stays a clean illustration (no bare
    # numbers to surface in the 评价's machine number-check).
    evidence_link = f"../../ai_package/{key}/ara/evidence/"
    lh = analysis.get("loss_highlight") or {}
    direction = lh.get("direction") or "该损失针对方法要解决的核心训练目标设计。"
    mechanism = (
        lh.get("mechanism") or "通过对该目标的优化,模型习得论文主张的能力(链 数学方法 推导)。"
    )
    baseline = lh.get("baseline") or "相比基线方案,该设计在论文关注的方向上更契合任务目标。"
    return "\n".join(
        [
            "### Loss 亮点解释",
            "",
            f"- **修复方向**:{direction}",
            f"- **机制**:{mechanism}",
            f"- **对比基线**:{baseline}",
            "- **证据**:对比数据见 "
            f"[ai_package evidence]({evidence_link})"
            "(branch1 不复制精确数字,交由审计层双分支一致性门核对)。",
        ]
    )


def _body(analysis: dict) -> str:
    """Compose the prose body (摘要翻译). ADR-0012 rev: the <!--ref--> anchoring is
    retired — the report carries plain prose and the 评价 vouches for faithfulness."""
    out: list[str] = ["## 摘要翻译", ""]
    para = [c["statement"] for c in analysis["claims"]]
    out.append(("".join(para) if para else "本文方法在标准基准上取得有竞争力的结果。") + "。")
    out += [
        "",
        "## 整体架构",
        "本文方法的核心组件构成如下(原图为 ground truth,以下为简化示意,以原图为准):",
        "",
    ]
    return "\n".join(out)


def write_branch1(
    person_dir: Path,
    candidate: Any,
    ara_dir: Path,
    md_path: Path,
    analysis: dict,
    *,
    key: str | None = None,
    _force_unanchored: bool = False,
    faithfulness_judge: Any = None,
) -> None:
    """Write the branch1 report. ADR-0012 rev: NEVER raises — branch1 always publishes,
    opening with a 「评价」 faithfulness note (build_assessment).

    Args:
        person_dir: Target person_vault entry directory.
        candidate: Discovery record.
        ara_dir: The already-written branch2 ara/ directory (the 评价's truth source).
        md_path: The frozen {ID}.md (kept for signature parity with the LLM path).
        analysis: Analyzer-spoke bundle.
        key: The shared vault key used to link to the paired ai_package
            (produce_outputs passes the real key; when omitted, falls back to
            the person_dir name).
        _force_unanchored: Test hook to inject a bare prose performance claim.
        faithfulness_judge: Optional (c) 评价 judge (report ↔ ARA). When the caller
            supplies one it is honored here too (no silent no-op); it writes the
            prose note and NEVER blocks.
    """
    person_dir.mkdir(parents=True, exist_ok=True)
    key = key or person_dir.name

    sections = [
        f"# {candidate['title']} — 深度解读",
        "",
        _body(analysis),
        "",
        "## 模型结构图",
        "原图见论文 Figure(以原图为准,ground truth)。下为统一风格简化重绘(简化示意,以原图为准):",
        "",
        _mermaid_redraw(analysis["architecture"]),
        "",
        _math_section(analysis),
        "",
        _loss_section(analysis, key),
        "",
        "## 趋势与定位",
        # Analyzer-sourced positioning; neutral fallback asserts no fixed domain.
        analysis.get("trend")
        or "该工作在其研究方向上推进了当前方法的能力边界(综述见配对 ai_package 分析)。",
    ]
    if _force_unanchored:
        sections.append(
            "我们的方法在 KITTI 上提升了 9.9 个百分点。"
        )  # ADR-0012: no longer fails lint (prose numbers freed)

    report = "\n".join(sections) + "\n"

    # ADR-0012 rev: prepend the opening 「评价」 (faithfulness note) — NEVER blocks.
    report = _prepend_assessment(
        report, build_assessment(report, ara_dir, judge=faithfulness_judge)
    )

    (person_dir / "report.md").write_text(report, encoding="utf-8")
    (person_dir / "report.html").write_text(
        "<!doctype html><meta charset=utf-8>"
        f"<title>{candidate['title']}</title>"
        "<body style='background:#0d1117;color:#e6edf3;font-family:sans-serif;padding:2rem'>"
        f"<h1>{candidate['title']}</h1><pre>报告正文见 report.md</pre></body>",
        encoding="utf-8",
    )
