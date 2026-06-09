# Engine Core Pipeline 代码地图

> **范围**: `scripts/{campaign,hub,spoke,run_campaign}.py` + `scripts/output/{produce,branch1_llm,branch1_report}.py`
> **最后更新**: 2026-06-08
> **关键特性**: Per-paper gated pipeline、双链原子产出、LLM writer 集成

<!-- Generated: 2026-06-08 | Files scanned: 8 | Token estimate: ~4000 -->

## 高层流程

```
┌─ Campaign Hard Gate (HITL, 一次性) ─────────────────────┐
│  CampaignConfig(topic, n_per_tick, force_include, ...)  │
│  写入 config/campaign.yaml（锁定）                      │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─ /loop Daily Tick (自动) ────────────────────────────────┐
│                                                           │
│  1. load_campaign(config/campaign.yaml)                 │
│  2. run_campaign(workspace, seams, discover, ...)      │
│     ↓                                                   │
│     a. Ledger(workspace) — single writer, LS-1 .lock  │
│     b. discover() — multi-source ranking, 2-3×N pool  │
│     c. ingest() — Tier-1 HTML / Tier-2 MinerU         │
│     d. Per-paper spoke loop (max-N parallel):         │
│        ├─ branch2 (ARA compiler)                      │
│        ├─ G2 gate (数据保真, skeptic multi-vote)      │
│        ├─ branch1 (人链 + 接地) OR thin (确定性)      │
│        ├─ G3 gate (anchor lint + 6-dim seal)         │
│        └─ promote both-or-neither (OT-5)             │
│     e. landscape sync (跨论文指标表)                 │
│                                                       │
└───────────────────────────────────────────────────────┘
                       ↓
            person_vault/ + ai_package/
            (产品，每日积累)
```

---

## 模块拓扑

### `scripts/campaign.py` — Hard Gate & Config

**核心类**：

```python
class CampaignConfig:
    topic: str                  # 精确的研究主题（非模糊）
    n_per_tick: int             # 每个 /loop tick 成功处理的论文数
    is_ad_domain: bool          # True = 启用 AD/robotics 权威白名单
    force_include: list[dict]   # 强制处理的论文列表
        # 每个 dict：{arxiv_id OR oa_pdf_url, doi, title}
        # 必须有可摄入源 + 不同身份

def write_campaign(root: Path, config: CampaignConfig) → None
    # 将 config 序列化为 config/campaign.yaml
    # 如果已存在 → 检查是否改变 topic/n_per_tick
    # 改变 → 触发 Hard Gate（用户确认）

def load_campaign(root: Path) → CampaignConfig | None
    # 读 config/campaign.yaml
    # 不存在 → 返回 None（Hard Gate 会 raise GateRequired）

def gate_needed(current: CampaignConfig, new_config: CampaignConfig) → bool
    # 比较 topic + n_per_tick，确定是否需要重新 gate
```

**关键约束**：
- Topic 不能是单个词（必须有范围上下文）
- N_per_tick 必须是正整数
- force_include 中的每项必须可摄入（arxiv_id 或 oa_pdf_url）
- 缺少任何关键字段 → `GateError`

---

### `scripts/hub.py` — Single-writer ledger & orchestration

**核心类**：

```python
class Ledger:
    _path: Path = None
    _lock: Lock = None
    
    def __init__(root: Path):
        # 打开 _ledger/processed_ledger.yaml（atomic append）
        # 获取 LS-1 .lock（排斥式，单 writer）
        # 失败 → LedgerLockError（另一个进程正在运行）

    def acquire() → None:
        # 获得写锁，hold 整个 tick

    def consistency_check() → None:
        # LS-4：启动时验证每个 done paper 有 person_vault/ 和 ai_package/
        # 缺少 → 降级为 re-process（漂移自愈）

    def mark_done(key: str, person_path: str, ai_path: str) → None:
        # 原子附加 ledger 行：status:done, vault paths, timestamps

    def mark_failed(key: str, reason: str) → None:
        # status:failed → write _failed/{key}.md

def run_campaign_tick(...) → TickResult:
    # 实际的每日 tick 逻辑
    # 接受 Ledger（hub 已获取）+ seams + discover
    # 返回 TickResult(papers_done, papers_failed, landscape_result)

def Watchdog(...):
    # 有界守护，重新启动停止的 paper（stall budget）
    # 检测：纸条在 branch2 或 branch1 阶段花费超过 X 分钟
    # 重新尝试，最多 N 轮，然后隔离
```

**关键不变式**：
- 只有 hub 写 ledger（LS-1 排斥式）
- Spoke 不写 ledger，只返回 `(person_path, ai_path)`
- Hub 从 spoke 返回值而不是重新派生 keys → 无重名风险

---

### `scripts/spoke.py` — Per-paper gated pipeline

**核心函数**：

```python
def make_spoke(
    md_path: Path,
    candidate: dict,
    ledger: Ledger,
    root: Path,
    *,
    resolve_analysis: Callable[[Path, dict], dict],
    skeptic_votes: Callable[[...], tuple[SkepticVote, ...]],
    rigor_scores: Callable[[dict], dict],
    entailment_judge: Callable[[...], tuple[bool, str]],
    write_report: Callable[..., dict] | None = None,
    cancel: threading.Event | None = None,
) → SpokeFn:
    """Build the production spoke that runs the full gated pipeline per paper.
    
    Returns a callable that:
      1. ingest(md_path, candidate) → frozen {ID}.md
      2. branch2(analysis) → ai_package/{key}/ara/
      3. G2(branch2) → pass/fail
      4. branch1(analysis, write_report) → person_vault/{key}/
      5. G3(branch1) → pass/fail
      6. promote or quarantine
    """
    
    # The spoke is SERIAL within one paper (branch2 → G2 → branch1 → G3)
    # but max-N spokes run in parallel (hub manages pool)
    # Every gate failure is caught + escalated to bounded_gate_runner
    # which re-emits up to max_gate_rounds, then quarantine
```

**Pipeline order** (serial within one paper):

```
1. ingest(md_path, candidate)
   ├─ Tier-1: arXiv HTML → pandoc → GFM
   ├─ Tier-2: PDF → MinerU → MD + images/
   └─ Produces: corpus/{ID}/{ID}.md + .md_contract.json

2. branch2 = produce_outputs(..., resolve_analysis, ...)
   ├─ Call: resolve_analysis(md_path, candidate) → ARA bundle
   ├─ ARA compiler: ara/claims/, ara/evidence/, ara/AUDIT_FLAGS.md
   └─ Stages to ai_package/{key}/ara/ (not yet promoted)

3. G2 = g2_data_fidelity(branch2)
   ├─ Multi-vote skeptic: verify critical numbers against MD
   ├─ Hard block on fabrication (majority votes unconfirmed)
   ├─ Tolerant mode: flag + downgrade instead of hard-block (per audit.yaml)
   └─ Failure → re-emit (bounded_gate_runner) or quarantine

4. branch1 = write_branch1_llm(..., write_report) OR write_branch1(...)
   ├─ If write_report: LLM-written vivid Chinese + figures + grounded assembly
   ├─ Else: thin deterministic markdown (from analysis)
   ├─ Every empirical number THREE-LAYER anchored to MD
   ├─ Anchors: equation → claim → evidence table (吸收-D1)
   └─ Stages to person_vault/{key}/ (not yet promoted)

5. G3 = seal_gate(branch1, branch2, md_path)
   ├─ anchor-lint: three-layer consistency check
   ├─ Equation fidelity: content_list.json count vs claims
   ├─ Entailment: claim vs experiment text semantically sound
   ├─ 6-dim rigor rubric (D1-D6)
   └─ Failure → re-emit or quarantine

6. promote both-or-neither (OT-5)
   ├─ If both pass: move ai_package + person_vault to real vaults
   ├─ Else: delete staging dirs (nothing reaches the vault)
```

**关键参数**：
- `resolve_analysis` — LLM seam（分析器）
- `skeptic_votes` — LLM seam（G2 multi-vote）
- `rigor_scores` — LLM seam（G3 6-dim）
- `entailment_judge` — LLM seam（G3 蕴含）
- `write_report` — LLM seam (可选，人链)；None = 使用 thin 确定性
- `cancel` — threading.Event，如果设置 → abort spoke（stall timeout）

---

### `scripts/run_campaign.py` — Composition driver

**核心函数**：

```python
def run_campaign(
    workspace: str,
    *,
    discover: Callable[...],  # infra adapter
    resolve_analysis: Callable,  # LLM seam
    skeptic_votes: Callable,  # LLM seam
    rigor_scores: Callable,  # LLM seam
    entailment_judge: Callable,  # LLM seam
    write_report: Callable | None = None,  # LLM seam (optional)
    http: Callable,  # infra adapter
    run_cli: Callable,  # infra adapter
    cross_model_votes: dict | None = None,  # future
    cross_model_sample: float = 0.0,  # future
    empirical_classifier: Callable | None = None,  # future
    requested_topic: str | None = None,  # override for gate
    requested_n: int | None = None,  # override for gate
) → TickResult:
    """
    The COMPOSITION entry point. Wires:
      Ledger(workspace) 
        → Ledger.acquire() [LS-1 lock]
        → run_campaign_tick(ledger, discover, seams, ...)
        → [Ledger.release()]
        → TickResult
    
    If campaign Hard Gate not satisfied → raises GateRequired.
    If LLM two-layer fallback fails → raises EngineAbort.
    """
    
    # Load locked campaign config (or None if not set yet)
    campaign = load_campaign(Path(workspace))
    if not campaign or requested_topic or requested_n:
        raise GateRequired("Campaign needs HITL setup")
    
    # Acquire single-writer lock
    ledger = Ledger(Path(workspace))
    with ledger.acquire():
        
        # Run the tick
        return run_campaign_tick(
            workspace=workspace,
            ledger=ledger,
            discover=discover,
            resolve_analysis=resolve_analysis,
            skeptic_votes=skeptic_votes,
            rigor_scores=rigor_scores,
            entailment_judge=entailment_judge,
            write_report=write_report,
            http=http,
            run_cli=run_cli,
        )
```

**关键约束**：
- 由 /loop tick 调用（不是独立 CLI）
- Hard Gate 只在 campaign 改变时触发
- 平面锁保护整个 tick 的 ledger
- 无中管道问题（AskUserQuestion 禁止）

---

### `scripts/output/produce.py` — Atomic dual-output (OT-5)

**核心函数**：

```python
def produce_outputs(
    md_path: Path,
    candidate: dict,
    ledger: Ledger,
    root: Path | None = None,
    *,
    resolve_analysis: Callable[[Path, dict], dict],
    g2_gate: Callable[[Path], GateVerdict] | None = None,
    write_report: Callable[..., dict] | None = None,
    cancel: threading.Event | None = None,
) → ProduceResult:
    """Produce branch2 + branch1 atomically.
    
    Both branches are built in staging directories.
    G2 runs on staged branch2 (before branch1).
    G3 runs on both (after promotion? NO — runs on staged both).
    
    Success: promote both simultaneously.
    Failure (G2 or G3): delete both staging dirs (atomic: nothing reaches vault).
    """
    
    key = derive_name(candidate, ledger)  # vault key
    stage_ai = Path(f"_stage_{key}_ai/")
    stage_person = Path(f"_stage_{key}_person/")
    
    try:
        # Call analyzer → branch2
        analysis = resolve_analysis(md_path, candidate)
        write_branch2(stage_ai, analysis, candidate, key=key)
        
        # G2 gate (hard block before branch1)
        if g2_gate:
            verdict = g2_gate(stage_ai)
            if verdict.is_hard_block:
                raise GateFailure("G2 hard block")
        
        # branch1: LLM-written OR thin deterministic
        if write_report is not None:
            write_branch1_llm(
                stage_person, candidate, stage_ai, md_path,
                write_report, key=key
            )
        else:
            write_branch1(stage_person, candidate, stage_ai, md_path, analysis, key=key)
        
        # G3 gate (hard block, may re-emit via bounded_gate_runner)
        # [gate_runner handles retry logic]
        
        # Both pass → promote
        promote_staging(stage_person, stage_ai, key)
        return ProduceResult(person_path=..., ai_path=...)
        
    finally:
        # Cleanup staging even on failure
        shutil.rmtree(stage_ai, ignore_errors=True)
        shutil.rmtree(stage_person, ignore_errors=True)
```

**关键不变式**：
- 两个分支都在 staging 目录构建（_stage_{key}_ai, _stage_{key}_person）
- G2 运行在 staged branch2 上（branch1 还未构建）
- G3 运行在 staged 两个分支上（或 hub 的 after-promotion copy？TBD）
- 任何硬门失败 → 删除两个 staging 目录（Nothing reaches vault）
- Hub 从 ProduceResult 而不是重新派生 key

---

### `scripts/output/branch1_llm.py` — LLM-written human chain

**核心函数**：

```python
def write_branch1_llm(
    stage_person: Path,
    candidate: dict,
    stage_ai: Path,
    md_path: Path,
    write_report: Callable[..., dict],
    key: str,
) → None:
    """生成 branch1（人链 LLM 写入版本）。
    
    Flow:
      1. 从 stage_ai/ara/ 读 ARA bundle
      2. 调用 write_report(ara, figures) → {section: rich_markdown, ...}
      3. 组装 report（header + sections + grounded assembly）
      4. EMOJI 剥离 + mermaid 标签引用
      5. 三层 anchor-lint（门控）
      6. 图形策展（强制 arch + 部分结果）
      7. 转换为白主题自包含 HTML（MathJax + mermaid）
      8. 写 person_vault/{key}/report.html + metadata.json
    """
    
    # Load ARA from staged branch2
    ara = load_ara_from_staging(stage_ai)
    
    # Extract figures from corpus/{ID}/images/
    figures = extract_figures(md_path.parent / "images/")
    curated_figs = curate_figures(ara, figures)  # arch mandatory + top-N
    
    # Call LLM writer
    sections = write_report(ara=ara, figures=curated_figs)
    
    # Build core block: 核心结论（mechanically grounded）
    core_block = _build_core_conclusions(ara, md_path)
    
    # Assemble report
    report = f"""
# {candidate.get("title", "Paper")}

## 核心结论

{core_block}

## Introduction

{sections.get("introduction", "")}

## Methods

{sections.get("methods", "")}

## Results & Discussion

{sections.get("results", "")}
...
"""
    
    # Whole-report grounding pass (any stray empirical number → anchor)
    report = _ground_empirical_claims(report, md_path)
    
    # Strip emoji + quote mermaid labels
    report = _strip_emoji(report)
    report = _quote_mermaid_labels(report)
    
    # Three-layer anchor-lint (hard gate)
    try:
        lint_result = lint_text(report, md_path)
        if lint_result.has_unanchored:
            raise AnchorGateError(f"Unanchored claims: {lint_result.details}")
    except AnchorGateError as e:
        # Re-raise for spoke to handle via bounded_gate_runner
        raise
    
    # Convert to self-contained HTML (MathJax + mermaid 11)
    html = _to_html_self_contained(report, figures=curated_figs)
    
    # Write outputs
    (stage_person / "report.html").write_text(html)
    (stage_person / "metadata.json").write_text(json.dumps({
        "key": key,
        "title": candidate.get("title"),
        "arxiv_id": candidate.get("arxiv_id"),
        "figures_curated": len(curated_figs),
        "generated_at": datetime.now().isoformat(),
    }))
```

**关键特性**：
- **LLM-generated**: 来自 write_report seam（路由到 config/llm.yaml 中的提供商）
- **Vivid prose**: 不是数据 → markdown 的机械映射，而是活泼的叙述
- **Core block**: механически 从 ARA 派生（claim statement + three-layer anchors）
- **Grounded assembly**: 全报告扫描任何实证数字，确保都锚定到 MD
- **Emoji stripping**: 确定性去除所有表情符号（项目铁律）
- **Figure curation**: 架构图强制，选中几个高优结果图
- **Self-contained HTML**: 所有图 base64 inlined，MathJax 嵌入，独立可浏览

---

### `scripts/output/branch1_report.py` — Thin deterministic renderer

**核心函数**：

```python
def write_branch1(
    stage_person: Path,
    candidate: dict,
    stage_ai: Path,
    md_path: Path,
    analysis: dict,
    key: str,
) → None:
    """生成 branch1（确定性简版，从 analysis 直接派生）。
    
    NOT LLM-written；使用固定模板和分析数据。
    存在的原因：determinism + auditability（没有 LLM 随机性）。
    """
    
    # Build from analysis dict
    sections = {
        "introduction": analysis.get("overview", ""),
        "methods": analysis.get("algorithm", ""),
        "results": analysis.get("results", ""),
        ...
    }
    
    # Same three-layer anchor-lint gate
    report = _format_report(sections, analysis)
    lint_result = lint_text(report, md_path)
    if lint_result.has_unanchored:
        raise AnchorGateError(...)
    
    # Write
    (stage_person / "report.md").write_text(report)
```

**vs. LLM branch1**:
- write_branch1: 确定性，可审计，可重现
- write_branch1_llm: 生动，自然语言，可能有创意但不可重现

两者都通过相同的三层 anchor-lint 门，确保精度。

---

## 配置文件

### `config/campaign.yaml` — Locked campaign spec

```yaml
topic: "autonomous vehicle trajectory prediction with uncertainty quantification"
n_per_tick: 5
is_ad_domain: true
force_include:
  - arxiv_id: "2401.12345"
    title: "Must-include paper 1"
  - oa_pdf_url: "https://..."
    doi: "10.1234/..."
    title: "Must-include paper 2"
```

### `config/audit.yaml` — Audit tuning knobs

```yaml
skeptic_votes: 1          # G2: 1 次投票（默认）或 3 次多数
max_gate_rounds: 1        # 重新执行门多少次后隔离
data_fidelity:
  mode: tolerant          # strict 时任何未验证数字就硬门；tolerant 时标记 + 降级
  max_unconfirmed: 5
  max_unconfirmed_ratio: 0.2
```

---

## 数据流

### Campaign flow

```
/paper-landscape skill invoked
  ↓
Preflight: check pandoc, mineru, runtime deps
  ↓
Hard Gate (HITL):
  ├─ User confirms topic (precise, not vague)
  ├─ User confirms n_per_tick (explicit count)
  ├─ User optionally adds force_include papers
  └─ write_campaign(config/campaign.yaml) → locked
  ↓
/loop 1d repeats:
  ├─ load_campaign(config/campaign.yaml)
  ├─ run_campaign(..., seams, discover, ...)
  ├─ Ledger.acquire() [LS-1 lock]
  ├─ run_campaign_tick(...)
  ├─ Ledger.release()
  └─ Return TickResult (papers_done, papers_failed, landscape)
```

### Per-paper flow (spoke)

```
1. ingest
   corpus/{ID}/{ID}.md + .md_contract.json

2. branch2 (ARA)
   analysis = resolve_analysis(md_path, candidate)
   ai_package/{key}/ara/{claims,evidence}/
   (staging: _stage_{key}_ai)

3. G2 gate
   skeptic_votes(numbers, md, claim) × N → majority → pass/fail

4. branch1
   person_vault/{key}/report.html (or .md)
   (staging: _stage_{key}_person)

5. G3 gate
   anchor-lint + eq fidelity + entailment + 6-dim rubric

6. promote
   both staging → real vaults (OT-5 atomic)
   OR delete both (failures don't reach vault)

7. ledger
   hub.mark_done(key, person_path, ai_path)
```

---

## 关键不变式

1. **Single-writer ledger** — 只有 hub（持有 LS-1 lock）写 `processed_ledger.yaml`
2. **Per-paper serial** — 同一论文的分支 2 → G2 → 分支 1 → G3 严格按序
3. **Parallel spokes** — 不同论文的 spoke 可并行（hub 管理池）
4. **Atomic dual-output** — 分支 2 + 分支 1 同时成功或同时失败（都在 vault 或都不在）
5. **No mid-pipeline questions** — 无 AskUserQuestion（中段全自动）
6. **Bounded gate runner** — G2/G3 失败：最多重新执行 N 轮，然后隔离到 _failed/
7. **Deterministic naming** — vault 键 = `{intake_date}_{Name}_{idbase}`（不是 LLM ad-hoc）

---

## 相关文档

- `llm-pipeline.md` — 提供商层和 seam factory
- `audit-gates.md` — G2 + G3 详细实现
- `output-branches.md` — 两个分支的完整模式
- `SKILL.md` — 技能合约，硬门，wiring 示例
- `references/wiring-the-seams.md` — 7 个 seam 的签名和隔离

