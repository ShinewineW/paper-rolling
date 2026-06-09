# .claude/skills/paper-landscape/scripts/llm/analyzer.py
r"""Chunked parallel ANALYZER — split the heavy ARA fact-extraction into parallel
sub-calls instead of one monolithic long-output request.

The monolithic analyzer emits a ~20-key JSON bundle in ONE call (~10k+ output
tokens, minutes of held connection) — slow and FRAGILE: a provider wobble or a
proxy drop on that long-lived big-output request kills the whole analysis (it
failed 4/4 on opencode). The fact source is naturally composed of separable
aspects, so we split it into 5 chunks and run them CONCURRENTLY (works on any
provider — claude -p subprocesses and HTTP calls both parallelize). Each chunk:
full MD in (large input is fine), only its own keys out (small output → fast,
short connection, independently retryable). Merge → the same bundle.

Referential integrity: claims / experiments / evidence_tables / related_work
cross-reference C#/E# ids (G3 entailment hard-blocks a dangling proof ref), so
they are kept TOGETHER in one chunk; exploration_tree's id refs are internal to
its own chunk. The other chunks are self-contained prose/lists.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from scripts.llm.jsonparse import extract_json
from scripts.llm.providers import LLMProvider

_MD_CHAR_CAP = 200_000

# Required analyzer-bundle keys (ara-schema.md). Missing key -> spoke fails.
REQUIRED_ARA_KEYS = (
    "overview",
    "problem",
    "claims",
    "concepts",
    "experiments",
    "related_work",
    "architecture",
    "algorithm",
    "constraints",
    "heuristics",
    "configs_training",
    "configs_model",
    "environment",
    "execution_stub",
    "exploration_tree",
    "evidence_tables",
    "innovations",
    "headline_metric",
    "headline_value",
    "params_million",
)

_RULES = """\
纪律(下游硬门会强制,违反会被硬阻断或隔离,务必照做):
0. 语言=简体中文:所有叙述/解释字段(overview/problem/claims.statement+interpretation+
   falsification/concepts.definition+interpretation+boundary/architecture/algorithm 解释/
   constraints/heuristics.desc+rationale/experiments.title+procedure+expected/
   related_work.what_changed+why/exploration_tree 各节 title+description+lesson+hypothesis+
   failure_mode+choice+trigger/math_intuition/loss_highlight/trend/证据表 caption)一律中文。
   保留原样不翻译:数字与单位、公式 $$...$$、代码标识符与 innovations.grep、专有名词
   (模型/方法/指标/数据集/硬件名,以本文 MD 中实际出现的为准,勿照抄本说明里的举例字样)、
   citation key/DOI、用作锚点的英文源短语。不要在任何字段留整句英文。
1. 忠于原文:每个 claim 与数字都要能在下面的 MD 中找到来源,不要引入外部知识。
2. 精确数字只出现在 evidence_tables(和 headline_*),逐字照抄 MD,绝不臆造/四舍五入
   (MD 里是什么小数就逐字照抄,带小数点的值不得四舍五入成整数);不要把模型名规模后缀里的
   数字当成指标值;experiments[].expected 用方向性措辞(只说优劣方向),不写具体数值。
   不确定是否在 MD 里就省略。
3. math_intuition / loss_highlight / trend 不含任何性能数字。
4. headline_value 必须是 MD 文本里真实出现的数字。
5. 公式保真:只**逐字转录论文显式给出**的公式($$...$$)。论文若未给出某公式(例如没有显式
   训练损失/目标函数),就写明"论文未给出显式损失公式"并仅作定性描述,**严禁自行构造、合成、
   补全或"还原"论文中不存在的公式**。严格区分训练期与推理期:只在推理期使用的融合/加权项
   (例如只在推理阶段才施加的加权/逐元素调制项)不得写进训练目标公式。
6. 区分原述与推断:凡论文未显式陈述、由你分析推断得到的结论(例如某个由你推断而非论文
   明述的结构性假设),必须在该字段内标注"(分析推断,论文未显式声明)",不得伪装成论文原文结论。
7. 不要过度具体化:论文未点名的具体型号/产品/工具名一律不要替读者补全(论文写 a VLM 就写
   某 VLM(引用),不要补全成某个具体厂商模型名);数量与硬件规格以论文原文为准,不要把某一用途的子集
   数量当成总量(例如把某子模块占用的设备数误当成集群总设备数)。同一份产物内同一实体的
   名称/数值必须前后一致。
8. JSON 合法性(关键):字符串值内**绝对不要使用 ASCII 双引号 "**——它会提前终止 JSON 字符串、
   导致解析失败。需要引用词语时一律用中文引号「」或『』(把需要强调的词组整体放进「」内)。
   字符串内的反斜杠一律转义为 \\\\。
"""

# id conventions shared across chunks so cross-refs resolve after merge.
_IDS = (
    'ID 约定(跨块一致):claims 用 "C1","C2"...;experiments 用 "E1","E2"...;'
    "claims[].proof / evidence_basis 引用 E# id;evidence_tables[].claims 与 "
    'related_work[].claims 引用 C# id;exploration_tree 节点 id 如 "Q1"/"D1"/"E1" 仅在本树内自引用。'
)

# Each chunk: (id, keys it must emit, the JSON-schema fragment for those keys).
_CHUNKS: tuple[tuple[str, tuple[str, ...], str], ...] = (
    (
        "framing",
        (
            "overview",
            "problem",
            "trend",
            "math_intuition",
            "loss_highlight",
            "headline_metric",
            "headline_value",
            "params_million",
        ),
        """- overview: str — 2-4 句方法的 what/why。
- problem: object {observations:[{id,statement,evidence,implication}],
    gaps:[{id,statement,why_fail,caused_by,attempts:[...]}],
    insight:{statement,derived_from,enables}, assumptions:[str,...]}
- trend: str — 一句话定位本文。
- math_intuition: str — 通俗类比,无数字。
- loss_highlight: {direction, mechanism, baseline} — 无数字。
- headline_metric: str — 论文头条指标名(以本文 MD 中实际出现的主指标名为准)。
- headline_value: float — 其数值,必须在 MD 文本中真实出现。
- params_million: float — 代表性模型规模(百万参数)。""",
    ),
    (
        "logic",
        ("claims", "experiments", "evidence_tables", "related_work"),
        """- claims: [{id:"C1",title,statement,status,tags:[...],falsification,proof:["E1"],
    evidence_basis:["E1"],interpretation}, ...]  (tags: improvement|causal|
    generalization|descriptive|scoping)
- experiments: [{id:"E1",title,verifies:["C1"],setup:{model,hardware,dataset,system},
    procedure:[...],metrics:[...],expected:"<方向性措辞,无精确数字>",
    baselines:[...],dependencies:[...]}, ...]  (Seal-1 需要 >= 3 个 experiment)
- evidence_tables: [{name,headers:[...],rows:[[...]],caption,source,claims:["C1"]}, ...]
    — 唯一可出现精确数字处,逐字照抄 MD。Seal-1 需要 >= 1 张表,headers 非空、>= 1 行、
    source 非空(如 "Table 3")。
- related_work: [{id:"R1",cite,doi,type,what_changed,why,claims:["C1"],adopted:[...]}, ...]
内部一致性:claims 的 proof/evidence_basis 必须引用本块 experiments 里真实存在的 E# id;
evidence_tables.claims 与 related_work.claims 引用本块 claims 里真实存在的 C# id(不得悬空)。""",
    ),
    (
        "concepts",
        ("concepts",),
        """- concepts: [{name,definition,notation,related:[...],interpretation,boundary}, ...]
    (Seal-1 需要 >= 5 个 concept)""",
    ),
    (
        "solution",
        ("architecture", "algorithm", "heuristics", "innovations", "execution_stub", "constraints"),
        """- architecture: str — pipeline 以 "A -> B -> C ..." 的散文描述。
- algorithm: str — 关键目标/损失。**只逐字转录论文显式给出的公式**($$...$$);论文若无显式
    损失/目标公式,写明"论文未给出显式损失公式"并仅定性描述,严禁自行构造或合成公式;
    严格区分训练期与推理期(勿把推理期才用的融合/加权项写进训练目标)。
- heuristics: [{id,desc,rationale,sensitivity,bounds,code_ref,source}, ...]
- innovations: [{name, grep:"<类代码标识符 token>"}, ...]
- execution_stub: str — 核心循环的简短可运行 python 草图。
- constraints: str — markdown 无序列表的局限。""",
    ),
    (
        "engineering",
        ("configs_training", "configs_model", "environment", "exploration_tree"),
        """- configs_training: [{name,value,rationale,range,sensitivity,source}, ...]
- configs_model: [{name,value,rationale,range,sensitivity,source}, ...]
- environment: object {python,framework,hardware,deps:[...],seeds}
- exploration_tree: [ node, ... ] — 研究 DAG。严格 schema(Seal-1 会校验):
    * >= 8 个节点;>= 1 个 type=\"decision\" 且 >= 1 个 type=\"dead_end\"。
    * 每个节点必有:id(如 "Q1")、type(question|decision|experiment|dead_end|pivot)、
      title(非空)、support_level("explicit" 论文明述,否则 "inferred")。
    * support_level=="explicit" 的节点还必须有 source_refs:非空短引用列表(如 ["Sec 3.1"])。
    * 按 type 的额外必填:question->description;experiment->result(方向性,无精确数字);
      dead_end->hypothesis+failure_mode+lesson;decision->choice+alternatives;
      pivot->from+to+trigger。
    * 可选:children(嵌套节点列表)、also_depends_on(必须指向树内已存在的节点 id)。""",
    ),
)


def _revision_block(prior_failure: str | None) -> str:
    """ADR-0009 branch2 feedback: a downstream-gate block re-extracts with this
    cue (default None → empty, original prompt unchanged)."""
    if not prior_failure:
        return ""
    return f"【上一稿被下游门控拦下,请据此重新抽取(更严格核对源文数字/锚点)】\n{prior_failure}\n\n"


def _chunk_prompt(
    cid: str,
    keys: tuple[str, ...],
    schema: str,
    title: str,
    aid: str,
    md: str,
    prior_failure: str | None = None,
) -> str:
    return (
        f"你是 paper-landscape 的 ANALYZER 子代理(分块:{cid})。读这篇论文,只产出一个 JSON 对象,"
        f"严格且仅包含这些 key:{list(keys)} —— 不要别的 key、不要任何解释文字。\n\n"
        f"{_revision_block(prior_failure)}"
        f"论文标识:title={title!r} arxiv_id={aid!r}\n\n"
        f"本块 JSON schema:\n{schema}\n\n{_IDS}\n\n{_RULES}\n"
        "=== 论文 MARKDOWN(唯一事实来源)===\n"
        f"{md}\n=== END ===\n"
    )


def _chunk_prompt_grounded(
    cid: str,
    keys: tuple[str, ...],
    schema: str,
    title: str,
    aid: str,
    md_path: str,
    prior_failure: str | None = None,
) -> str:
    """GROUNDED prompt: the agent READS the file itself (no embedded MD)."""
    return (
        f"你是 paper-landscape 的 ANALYZER 子代理(分块:{cid})。只产出一个 JSON 对象,"
        f"严格且仅包含这些 key:{list(keys)} —— 不要别的 key、不要任何解释文字。\n\n"
        f"{_revision_block(prior_failure)}"
        f"论文标识:title={title!r} arxiv_id={aid!r}\n"
        f"事实来源是这份冻结的论文 markdown 文件,**用 Read 读取它**(可用 Grep 定位/核对数字):\n"
        f"{md_path}\n\n"
        f"本块 JSON schema:\n{schema}\n\n{_IDS}\n\n{_RULES}\n"
        "务必先用 Read/Grep 实际查阅该文件;凡写入 evidence_tables / headline_value 的数字,"
        "先用 Grep 在该文件中确认其逐字存在再写入。\n"
        "查阅完成后,**直接以 `{` 开头输出该 JSON 对象**——不要任何前言、思考过程、解释,"
        "也不要 markdown 代码围栏。\n"
    )


def analyze_chunked(
    md_path: Path,
    candidate: dict,
    provider: LLMProvider,
    *,
    grounded: bool = False,
    timeout: float = 900.0,
    max_workers: int = 5,
    log=lambda _m: None,
    prior_failure: str | None = None,
) -> dict:
    """Run the 5 analyzer chunks CONCURRENTLY on `provider`; merge into one bundle.

    Each chunk emits only its own keys (small output). When ``grounded`` (claude-
    code only — needs local file tools), the chunk-agent READS the MD file itself
    (Read/Grep, grep-verifying numbers) with a tiny prompt — robust + faithful, no
    huge one-shot embed. Otherwise the (capped) MD is embedded inline. A chunk
    whose JSON won't parse is retried once. Returns the merged ARA bundle (caller
    does the required-key check + float coercion).
    """
    md_path = Path(md_path)
    title = candidate.get("title", "")
    aid = candidate.get("arxiv_id", "")
    md = ""
    if not grounded:
        md = md_path.read_text(encoding="utf-8")
        if len(md) > _MD_CHAR_CAP:
            log(f"analyzer: MD {len(md)} chars > cap, truncating to {_MD_CHAR_CAP}")
            md = md[:_MD_CHAR_CAP] + "\n\n[...TRUNCATED...]"
    tools = ("Read", "Grep", "Glob") if grounded else None

    def _one(chunk) -> dict:
        cid, keys, schema = chunk
        log(f"analyzer[{provider.name}] chunk={cid} keys={len(keys)} grounded={grounded}")
        if grounded:
            base = _chunk_prompt_grounded(
                cid, keys, schema, title, aid, str(md_path), prior_failure
            )
        else:
            base = _chunk_prompt(cid, keys, schema, title, aid, md, prior_failure)
        nudge = (
            "\n\n重要:只回复一个 JSON 值,不要散文、不要解释、不要 markdown 代码围栏。"
            "JSON 字符串里的每个反斜杠都必须转义成 \\\\(LaTeX 命令也一样,如 \\\\mathbf、"
            "\\\\times、\\\\theta),不要出现单个反斜杠。"
        )
        last: Exception | None = None
        for attempt in range(2):
            raw = provider.complete(
                base + (nudge if attempt else ""), tier="strong", timeout=timeout, tools=tools
            )
            try:
                obj = extract_json(raw)
                if isinstance(obj, dict):
                    return obj
                last = ValueError(f"chunk {cid} returned non-object")
            except ValueError as exc:
                last = exc
                log(f"analyzer chunk={cid} parse retry: {exc}")
        raise RuntimeError(f"analyzer chunk {cid!r} failed to parse: {last}")

    bundle: dict = {}
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        for obj in ex.map(_one, _CHUNKS):
            bundle.update(obj)
    return bundle
