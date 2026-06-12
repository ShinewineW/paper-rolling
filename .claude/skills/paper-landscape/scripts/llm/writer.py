# .claude/skills/paper-landscape/scripts/llm/writer.py
"""Human-chain writer: turn the gated ARA into a vivid, fluent Chinese report.

The "two chains from one source" model: the ARA (ai_package) is the dense,
structured, AI-facing distillation; THIS module is the human-facing chain — a
section-by-section writer that reads the (already G2/G3-gated) ARA + frozen MD and
produces flowing, illustrative Chinese prose. It is provider-agnostic: the caller
passes an ``LLMProvider`` (explicitly routed per config/llm.yaml — no default), so
the human chain can run on, e.g., deepseek/qwen while the analyzer stays on Claude.

Grounding discipline (so the report passes the branch1 忠实门, ADR-0012 / 吸收-D1):
sections MAY write performance numbers in natural prose, but every number must be a
real value from the ARA/source (the 忠实门 verifies grounding mechanically + an LLM
judge); numbers/equations/proper-nouns stay verbatim. The assembler runs the real
忠实门 (kept anchor-form lint + (b) grounding + (c) judge) afterward; the engine
核心结论 block is still mechanically anchored.
"""

from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from scripts.llm.jsonparse import extract_json
from scripts.llm.providers import LLMProvider

# Cap embedded ARA source per section so a prompt stays bounded.
_SRC_CAP = 24_000

# Reference-distilled writing rules (mined from docs/reference/) injected into
# every writer prompt — see references/human-report-writing.md.
_INJECTION_CACHE: str | None = None


def _injection() -> str:
    """The INJECT:START..INJECT:END block from references/human-report-writing.md,
    prepended to every section prompt so the writer follows the reference-grounded
    rules. Empty (writer still runs) if the doc is missing."""
    global _INJECTION_CACHE
    if _INJECTION_CACHE is None:
        doc = Path(__file__).resolve().parents[2] / "references" / "human-report-writing.md"
        text = doc.read_text(encoding="utf-8") if doc.exists() else ""
        m = re.search(r"<!--\s*INJECT:START\s*-->(.*?)<!--\s*INJECT:END\s*-->", text, re.S)
        _INJECTION_CACHE = m.group(1).strip() if m else ""
    return _INJECTION_CACHE or ""


_CONSTRAINTS = (
    "硬约束(违反会让报告失真或被接地门拦下):\n"
    "1. 中文,流畅、生动,像一篇优秀的中文技术博客/深度科普;可用恰当比喻"
    "(标注“直觉,非严格对应”)。务必把“为什么这么做、解决了什么痛点、机制如何”讲透,杜绝空话套话。\n"
    "2. 忠实:只用下面给出的 ARA 事实内容,绝不编造。专有名词(模型名、指标名、数据集名、"
    "硬件名等,以上面事实源中实际出现的为准)与公式 "
    "$$...$$ 一律保留原样,不要翻译;切勿照抄本说明里的举例字样。\n"
    "3. 数字忠实(ADR-0012):叙述里可以自然地写性能数字,但每个数字都必须是 ARA/源文里真实"
    "出现的值——绝不编造、绝不张冠李戴(把某系统的得分安到另一个系统头上)。不确定就用定性语言。"
    "切勿把本条写作规则本身抄进报告正文。\n"
    "4. 篇幅写足:这一节要充分展开(目标 350–800 中文字,按内容深浅)。\n"
    "5. 只输出本节正文,以指定的二级标题 “## ...” 开头;不要写其它节、不要写整篇标题、"
    "不要写代码围栏以外的解释。"
)

# (id, title, [ara source files relative to ara/], focus)
SECTIONS: tuple[tuple[str, str, tuple[str, ...], str], ...] = (
    (
        "01_导读",
        "一句话总结与导读",
        ("PAPER.md", "logic/problem.md"),
        "用 2-3 段给完全不熟悉这篇论文的读者一个有画面感的导读:一句话在做什么、为什么值得关心(解决了什么真实痛点)、最核心的一个 idea 是什么。开头给一句话 TL;DR(加粗)。",  # noqa: E501
    ),
    (
        "02_问题背景",
        "问题背景与动机",
        ("logic/problem.md",),
        "把 observations → gaps → insight 串成有逻辑的故事:观察到什么现象、现有方法卡在哪、由此得到的关键洞见是什么,让读者顺着推理理解'为什么需要这种设计'。",  # noqa: E501
    ),
    (
        "03_核心概念",
        "核心概念速览",
        ("logic/concepts.md",),
        "逐条讲解核心概念(每个:是什么、直觉怎么理解、在本方法里起什么作用),每个概念配一个生活化或工程化比喻。",
    ),
    (
        "04_方法与架构",
        "方法与整体架构",
        (
            "logic/solution/architecture.md",
            "logic/solution/heuristics.md",
            "logic/solution/algorithm.md",
        ),
        "讲清整体 pipeline:数据/条件如何流入、各模块各自做什么、如何组合。然后给一个真实反映该 pipeline 的 mermaid 流程图(flowchart TB,节点用论文真实组件名,不要用 Input/Model/Output 占位)。mermaid 必须放在 ```mermaid 代码块里,并在末尾附:\n    classDef required fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#1e3a5f\n    classDef output fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d\n    classDef optional fill:#fef9c3,stroke:#ca8a04,stroke-width:2px,color:#713f12\n并给首节点 class required、末节点 class output。",  # noqa: E501
    ),
    (
        "05_算法与推导",
        "算法目标与推导",
        ("logic/solution/algorithm.md",),
        "先原样给出源公式($$...$$),再用针对本论文具体损失的真实逐步推导讲解每一项含义与设计理由(不要写'由源公式出发、沿优化方向迭代'这种万能套话)。再给一个直觉比喻和一个具体小玩具例子。本节聚焦机制与推导而非跑分,无需堆砌 benchmark 性能数字(结构性数字如层数/维度可正常写)。",  # noqa: E501
    ),
    (
        "06_实验与对比",
        "实验设计与结果解读",
        ("logic/experiments.md", "evidence/README.md"),
        "讲清做了哪些关键实验、各验证什么、对照怎么设、用什么指标,然后解读主要发现。可以自然地写出关键性能数字(ADR-0012),但每个数字都必须是 ARA/源文里真实出现的值——绝不编造、绝不张冠李戴;不确定就用定性语言。系统还会在本节末自动附上精确数值表,合适处可写'(详见下方实验表)'。",  # noqa: E501
    ),
    (
        "07_相关工作",
        "相关工作与定位",
        ("logic/related_work.md",),
        "讲清建立在哪些前人方法之上、相对它们改了什么、为什么重要,说明它在研究谱系里的位置。",
    ),
    (
        "08_探索历程",
        "研究探索历程",
        ("trace/exploration_tree.yaml",),
        "把研究 DAG 叙事化:依次问了哪些问题、做了哪些关键决策、撞过哪些死胡同(dead_end)、学到什么、有无方向转变(pivot),展现真实探索路径。",  # noqa: E501
    ),
    (
        "09_复现要点",
        "工程与复现要点",
        (
            "src/configs/training.md",
            "src/configs/model.md",
            "src/environment.md",
            "src/code_ref.md",
        ),
        "面向想复现的工程师:模型规模与关键结构、训练关键超参与作用、运行环境/依赖、有无开源代码与入口。非性能数字(参数量、分辨率、GPU 数)可正常写。",  # noqa: E501
    ),
    (
        "10_局限与边界",
        "局限与适用边界",
        ("logic/solution/constraints.md",),
        "诚实讲清局限、假设前提、适用边界与已知失败模式,帮助读者判断它在自己场景下是否适用。",
    ),
    (
        "11_趋势与展望",
        "趋势定位与展望",
        ("PAPER.md", "logic/problem.md", "logic/related_work.md"),
        "从这篇工作出发,谈它在该技术路线上的定位与意义,以及指向的可能发展方向。保持有据,不空喊口号。",
    ),
)


def _read_sources(ara_dir: Path, rel_files: tuple[str, ...]) -> str:
    chunks: list[str] = []
    for rel in rel_files:
        p = ara_dir / rel
        if p.exists():
            text = p.read_text(encoding="utf-8")
            chunks.append(f"=== {rel} ===\n{text[:_SRC_CAP]}")
    return "\n\n".join(chunks)


def _section_prompt(title: str, focus: str, sources: str, prior_failure: str | None = None) -> str:
    inject = _injection()
    inject_block = f"{inject}\n\n" if inject else ""
    revision_block = (
        f"【上一稿被门控拦下,请据此整体修订(不删内容,按指引改写)】\n{prior_failure}\n\n"
        if prior_failure
        else ""
    )
    return (
        "你是一位资深的中文技术深度科普作者,正在撰写一篇论文'给人读'的深度解读报告中的一节。\n\n"
        f"{inject_block}"
        "下面是已经过事实校验的结构化事实源(你的事实基础):\n"
        f"{sources}\n\n"
        f"{revision_block}"
        f"【本节任务】{focus}\n\n"
        f"{_CONSTRAINTS}\n\n"
        f'现在写这一节,以 "## {title}" 开头。'
    )


def write_human_sections(
    ara_dir: Path,
    provider: LLMProvider,
    *,
    outdir: Path | None = None,
    max_workers: int = 6,
    timeout: float = 600.0,
    log=lambda _m: None,
    prior_failure: str | None = None,
) -> dict[str, str]:
    """Write every human-report section via ``provider``; return {id: markdown}.

    Sections are produced concurrently. If ``outdir`` is given, each section is
    also written to ``outdir/<id>.md`` (so the deterministic assembler can stitch
    them). The provider is whatever config routes the ``writer`` seam to.
    """
    ara_dir = Path(ara_dir)
    if outdir is not None:
        outdir.mkdir(parents=True, exist_ok=True)

    def _one(spec) -> tuple[str, str]:
        sid, title, rel_files, focus = spec
        log(f"writer[{provider.name}]: {sid}")
        prompt = _section_prompt(
            title, focus, _read_sources(ara_dir, rel_files), prior_failure=prior_failure
        )
        md = provider.complete(prompt, tier="strong", timeout=timeout).strip()
        if outdir is not None:
            (outdir / f"{sid}.md").write_text(md, encoding="utf-8")
        return sid, md

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        results = dict(ex.map(_one, SECTIONS))
    return results


def curate_figures(
    figures, provider: LLMProvider, *, title: str = "", timeout: float = 300.0
) -> dict[str, dict]:
    """CURATE original figures for the human report (selective, not all).

    `figures` is a list of objects with `.ref` and `.caption`. The model classifies
    each and decides inclusion:
      - role: "architecture" (core method / model-structure overview — MANDATORY),
        "result" (effect/quantitative figures — pick a FEW good ones), or "other".
      - include: architecture figures MUST be true; 2-4 representative result
        figures true; the rest (incl. tables/minor) false.
      - zh: a 1-3 句 Chinese science-pop gloss (for included figures).
    Returns {ref: {"role","include","zh"}}. On failure returns {} — the caller
    applies a caption-heuristic fallback so the core structure figure is still in.
    """
    figs = list(figures)
    if not figs:
        return {}
    lines = "\n".join(f"{i}. {f.caption}" for i, f in enumerate(figs))
    prompt = (
        f"论文《{title}》里有以下原图(序号 + 英文图注)。请为人审报告**策展**这些图(不是全选):\n"
        "- role:architecture(核心方法/模型结构总图)| result(效果/定量结果图)| other(其它)。\n"
        "- include:**架构/核心方法/结构总图必须 include=true**;result 类只挑 2-4 张最有代表性的"
        " include=true,其余(含次要图/纯表格截图)include=false。\n"
        "- zh:对 include=true 的图写一句到三句**中文**科普解说"
        "(通俗生动,专名/公式保留,无散落性能数字)。\n\n"
        f"{lines}\n\n"
        '只回复一个 JSON 对象,key 为序号字符串,value 为 {"role":..,"include":true/false,"zh":".."},'
        '例如 {"0":{"role":"architecture","include":true,"zh":"…"}}。'
    )
    try:
        out = extract_json(provider.complete(prompt, tier="fast", timeout=timeout))
    except (ValueError, RuntimeError):
        return {}
    if not isinstance(out, dict):
        return {}
    result: dict[str, dict] = {}
    for i, f in enumerate(figs):
        d = out.get(str(i)) or out.get(i)
        if isinstance(d, dict):
            result[f.ref] = {
                "role": str(d.get("role", "other")),
                "include": bool(d.get("include", False)),
                "zh": str(d.get("zh", "")).strip(),
            }
    return result
