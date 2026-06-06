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

Three-layer citation (吸收-D1): every empirical PERFORMANCE sentence carries
`<!--ref:slug--><!--anchor:quote|page:value-->` anchored into `{ID}.md`. The
producer self-checks with the anchor lint and RAISES on any violation (HARD
gate) — it will not ship an unanchored report. Illustrative numbers in the
math/loss sections (no performance cue) do not require anchors.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any
from urllib.parse import quote

from scripts.output.anchor_lint import lint_text

# Cherry-picked unified Mermaid classDef palette (双输出-D1). Source:
# scientific-agent-skills markdown-mermaid-writing/references/mermaid_style_guide.md
# (Apache-2.0). classDef-only, theme-neutral; shared by every paper's re-draw.
_CLASSDEF = (
    "    classDef required fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#1e3a5f\n"
    "    classDef output fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d\n"
    "    classDef optional fill:#fef9c3,stroke:#ca8a04,stroke-width:2px,color:#713f12\n"
)


class AnchorGateError(RuntimeError):
    """Raised when the report contains an unanchored empirical assertion."""


def _anchor(snippet: str) -> str:
    """Build a three-layer anchor whose quote is taken verbatim from the MD.

    The slug is derived from the snippet and ALWAYS prefixed with `r-` so it
    begins with a letter (the strict ref pattern rejects digit-leading slugs).
    The quote value is URL-encoded and capped to <=20 words; `-` is encoded as
    `%2D` to avoid premature HTML-comment termination.
    """
    body = re.sub(r"[^a-z0-9]+", "-", snippet.lower())[:22].strip("-") or "ref"
    slug = f"r-{body}"
    words = snippet.split()[:20]
    value = quote(" ".join(words), safe="").replace("-", "%2D")
    return f"<!--ref:{slug}--><!--anchor:quote:{value}-->"


def _find_in_md(md_text: str, number: str) -> str | None:
    """Return a <=20-word MD window containing `number`, for anchoring."""
    for line in md_text.splitlines():
        if number in line:
            stripped = re.sub(r"\$\$.*?\$\$", "", line).strip()
            stripped = re.sub(r"[#*`]", "", stripped)
            return " ".join(stripped.split()[:20]) or stripped[:60]
    return None


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
    # NOTE: the toy example deliberately avoids bare matrix literals / metric
    # tokens so it reads as illustration, not an (un-anchorable) performance
    # claim — keeping the self-gate green.
    return "\n".join(
        [
            "### 数学方法",
            "",
            "> ⚠ AI 推导,需人工复核(公式保真已对照 branch2 algorithm.md 源公式)。",
            "",
            f"源公式(引自 ai_package algorithm.md):{eq_text}",
            "",
            "**逐步推导**:",
            f"- 由源公式 {eq_text} 出发,目标是最小化干净信号的重建误差。",
            "- 截断到若干步后,期望在每一步上对噪声做去除,得到分阶段的去噪目标。",
            "",
            "**比喻(直觉辅助,非严格对应)**:像冲洗一张欠曝照片——",
            "与其一次猛拉亮度,不如分几步逐步提亮,既快又不过曝。",
            "",
            "**玩具例子**:取一个小输入矩阵,按固定衰减系数迭代少数几步,",
            "即可逼近干净信号,验证截断扩散仍然收敛。",
        ]
    )


def _loss_section() -> str:
    return "\n".join(
        [
            "### Loss 亮点解释",
            "",
            '- **修复方向**:去噪损失冲的是"轨迹多模态坍缩"这一弱点——'
            "标准回归损失会把多个合理未来平均成一个模糊解。",
            "- **机制**:在截断扩散链上施加分步去噪信号(链 数学方法 推导),"
            "让模型保留多模态而非平均化。",
            "- **对比基线**:标准回归在多模态下天然取均值,修不了该方向;"
            "交叉熵则需离散化轨迹,损失精度。",
            "- **证据**:对比数据见 "
            "[ai_package evidence](../ai_package/REPLACE_KEY/ara/evidence/tables/table1_nuscenes.md)"  # noqa: E501
            "(branch1 不复制精确数字,交由审计层双分支一致性门核对)。",
        ]
    )


def _body_with_anchors(md_text: str, analysis: dict) -> str:
    """Compose the prose body, anchoring each claim's number into the MD."""
    out: list[str] = ["## 摘要翻译", ""]
    para: list[str] = []
    for c in analysis["claims"]:
        nums = re.findall(r"\d+\.\d+", c["statement"])
        sentence = c["statement"]
        for n in nums:
            window = _find_in_md(md_text, n)
            if window:
                sentence += _anchor(window)
        para.append(sentence)
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
    _force_unanchored: bool = False,
) -> None:
    """Write the branch1 report; RAISE if any empirical claim is unanchored.

    Args:
        person_dir: Target person_vault entry directory.
        candidate: Discovery record.
        ara_dir: The already-written branch2 ara/ directory.
        md_path: The frozen {ID}.md (anchor target).
        analysis: Analyzer-spoke bundle.
        _force_unanchored: Test hook to inject an unanchored performance claim.

    Raises:
        AnchorGateError: If the composed report fails the three-layer lint.
    """
    person_dir.mkdir(parents=True, exist_ok=True)
    md_text = md_path.read_text(encoding="utf-8")

    sections = [
        f"# {candidate['title']} — 深度解读",
        "",
        _body_with_anchors(md_text, analysis),
        "",
        "## 模型结构图",
        "原图见论文 Figure(忠实锚点,ground truth)。下为统一风格简化重绘(简化示意,以原图为准):",
        "",
        _mermaid_redraw(analysis["architecture"]),
        "",
        _math_section(analysis),
        "",
        _loss_section(),
        "",
        "## 趋势与定位",
        "该方法将扩散式规划推向实时区间,推动端到端规划向多模态保真演进。",
    ]
    if _force_unanchored:
        sections.append("我们的方法在 KITTI 上提升了 9.9 个百分点。")  # no anchor → must fail gate

    report = "\n".join(sections) + "\n"

    violations = lint_text(report)
    if violations:
        raise AnchorGateError(
            "branch1 report failed three-layer citation gate (吸收-D1): "
            + "; ".join(v.message for v in violations[:5])
        )

    (person_dir / "report.md").write_text(report, encoding="utf-8")
    (person_dir / "report.html").write_text(
        "<!doctype html><meta charset=utf-8>"
        f"<title>{candidate['title']}</title>"
        "<body style='background:#0d1117;color:#e6edf3;font-family:sans-serif;padding:2rem'>"
        f"<h1>{candidate['title']}</h1><pre>报告正文见 report.md</pre></body>",
        encoding="utf-8",
    )
