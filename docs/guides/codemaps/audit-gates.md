# Adversarial Audit Gates (G2 + G3) 代码地图

> **范围**: `scripts/audit/` — types, g2_data_fidelity, g3_seal, entailment, rigor_rubric, gate_runner
> **最后更新**: 2026-06-13
> **关键特性**: G2 两层数字门（Layer-1 代码核对存在性 → Layer-2 multi-vote skeptic 判语义变换）硬门、G3 检查（G3R0 branch1 存在性 + entailment + 6 维 rigor + equation;ADR-0012 rev 退役 branch1 锚点解析）、失败保留现场不删 ARA (ADR-0011)

<!-- Generated: 2026-06-08 | Files scanned: 10 | Token estimate: ~3500 -->

## 高层结构

```
Per-paper spoke:

  branch2 built (ai_package/{key}/ara/)
           ↓
  ┌─ G2: Data Fidelity Gate ──────────────────────────┐
  │                                                     │
  │  Input: staged branch2 ARA (claims + evidence)    │
  │                                                     │
  │  Logic (two-layer):                                │
  │  ├─ Extract critical numbers from evidence tables │
  │  ├─ Layer 1 (CODE): value present in source MD?   │
  │  │  └─ confirm by canonical-float match           │
  │  │     (28.40==28.4); NOT sent to the LLM         │
  │  ├─ Layer 2 (LLM): only NOT-present numbers escala│
  │  │  └─ skeptic_votes(seam) × N_votes (independent)│
  │  │     judges trivial-transform derivability      │
  │  ├─ Multi-vote majority on escalated: found?      │
  │  └─ Hard block if majority says "NOT found"       │
  │     (fabrication detector)                        │
  │                                                     │
  │  Output: GateVerdict (pass/hard_block)             │
  │                                                     │
  └─────────────┬──────────────────────────────────────┘
                │
           (if fail)
                ↓
    bounded_gate_runner:
    ├─ Re-emit (branch2 → G2) up to max_gate_rounds
    ├─ If still fail → 保留 _failed/<key>/ 现场 (staged ARA 不删, ADR-0007/0011)
    └─ (pass → continue)
                ↓
  branch1 built (person_vault/{key}/)
    (thin renderer OR LLM-written)
                ↓
  ┌─ G3: Seal Gate ────────────────────────────────────┐
  │                                                     │
  │  Input: staged branch2 + branch1 + corpus/{ID}.md │
  │                                                     │
  │  Logic:                                             │
  │  ├─ anchor-lint: three-layer consistency         │
  │  │  (equation → claim → evidence table)           │
  │  ├─ equation-fidelity: content_list.json count    │
  │  ├─ entailment-judge: semantic claim validity     │
  │  └─ rigor-rubric: 6-dim assessment (D1-D6)        │
  │                                                     │
  │  Output: GateVerdict                               │
  │                                                     │
  └─────────────┬──────────────────────────────────────┘
                │
           (if fail)
                ↓
    bounded_gate_runner:
    ├─ Re-emit (branch1 → G3) up to max_gate_rounds
    ├─ If still fail → quarantine
    └─ (pass → promote both vaults)
```

---

## 模块拓扑

### `scripts/audit/types.py` — Audit vocabulary

**核心类**：

```python
class Severity(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

class Finding:
    """A single audit finding (severity, description, evidence)."""
    severity: Severity
    finding_type: str  # "anchor_mismatch", "unverified_number", ...
    description: str
    evidence: str | None  # quote from source or number

class SkepticVote:
    """One skeptic's opinion on a number."""
    number: str          # the number in question
    found_in_source: bool  # did you find it in the MD?
    note: str = ""       # explain your reasoning

class GateVerdict:
    """Gate result: pass or hard_block."""
    is_pass: bool
    is_hard_block: bool = False  # True = must quarantine (不能重新执行)
    findings: list[Finding] = []
    severity_max: Severity = Severity.INFO

# Type aliases for seam signatures
SkepticVoteFn = Callable[[tuple[str, ...], str, str], tuple[SkepticVote, ...]]
RigorScoreFn = Callable[[dict], dict]
EntailmentJudgeFn = Callable[[ClaimRecord, str], tuple[bool, str]]

class ClaimRecord:
    """A single claim extracted from branch1."""
    claim_text: str
    claim_id: str  # claim_O1, claim_O2, ...
    numbers: list[str]  # [5.2, 87%, ...]
    source_md_anchor: str  # MD section reference
```

---

### `scripts/audit/g2_data_fidelity.py` — Number-fidelity gate

**核心函数**：

```python
def g2_gate(
    stage_ai: Path,
    skeptic_votes: Callable[[tuple[str, ...], str, str], tuple[SkepticVote, ...]],
    config: dict,  # from config/audit.yaml
) → GateVerdict:
    """G2: Data-fidelity adversarial gate (two-layer).

    Layer 1 (deterministic, CODE): a number whose VALUE is present in the source
    MD is confirmed by canonical-float match — never sent to the LLM, which is
    unreliable at this mechanical "is the number present" task and false-flagged
    verbatim-present numbers. Layer 2 (LLM skeptic): only numbers NOT mechanically
    present escalate; the multi-vote skeptic judges the semantic question (is it
    derivable via a trivial transform?). Hard-blocks if the majority says
    "I didn't find this number".

    Tolerance mode (config/audit.yaml data_fidelity.mode: tolerant):
    - A few unverified numbers are FLAGGED but paper is kept.
    - Beyond max_unconfirmed OR max_unconfirmed_ratio → hard-block anyway.
    """
    
    # 1. Load ARA from staged branch2
    ara = load_ara_from_staging(stage_ai)
    
    # 2. Extract all numbers from evidence tables
    numbers = _extract_numbers_from_evidence(ara)  # e.g., ["87.5", "5.2e-4", ...]
    if not numbers:
        return GateVerdict(is_pass=True)  # No numbers, no check
    
    # 3. Read source MD (ground truth)
    source_md = (Path(ara["_md_path"])).read_text()

    # 4. Layer 1 (CODE): confirm present-by-value numbers; escalate the rest.
    source_values = {float(t) for t in extract_numbers(source_md)}
    escalated = tuple(n for n in numbers if float(n) not in source_values)

    # 5. Layer 2 (LLM): multi-vote skeptic on the ESCALATED set only (independent
    #    calls, uncorrelated with generator). Skipped entirely if escalated is empty.
    n_votes = config.get("skeptic_votes", 1)
    votes = []
    for vote_idx in range(n_votes) if escalated else ():
        vote_result = skeptic_votes(
            numbers=escalated,                # only numbers code could NOT confirm
            source_md=source_md[:200_000],  # capped at 200k chars
            claim_context=f"Paper claim (vote {vote_idx + 1}/{n_votes})",
        )
        votes.extend(vote_result)
    
    # 6. Tally by majority (Layer-1-confirmed numbers skipped — present by construction)
    findings = []
    unconfirmed_count = 0
    for num in escalated:
        votes_for_num = [v for v in votes if v.number == num]
        confirmed_count = sum(1 for v in votes_for_num if v.found_in_source)
        majority_found = confirmed_count > len(votes_for_num) / 2
        
        if not majority_found:
            unconfirmed_count += 1
            findings.append(Finding(
                severity=Severity.WARNING,
                finding_type="unverified_number",
                description=f"Number '{num}' not verified in source (votes: {votes_for_num})",
            ))
    
    # 7. Decision based on mode
    mode = config.get("data_fidelity", {}).get("mode", "tolerant")
    max_unconfirmed = config.get("data_fidelity", {}).get("max_unconfirmed", 5)
    max_ratio = config.get("data_fidelity", {}).get("max_unconfirmed_ratio", 0.2)
    
    if mode == "strict":
        # ANY unconfirmed → hard-block
        is_hard_block = unconfirmed_count > 0
    else:  # tolerant
        # Tolerate up to max_unconfirmed AND max_ratio
        is_hard_block = (
            unconfirmed_count > max_unconfirmed
            or unconfirmed_count > len(numbers) * max_ratio
        )
    
    # 8. Write audit flags
    if findings:
        _write_audit_flags(stage_ai, findings)
    
    return GateVerdict(
        is_pass=not is_hard_block,
        is_hard_block=is_hard_block,
        findings=findings,
        severity_max=Severity.CRITICAL if is_hard_block else Severity.WARNING,
    )

def _extract_numbers_from_evidence(ara: dict) -> list[str]:
    """Pull all numbers from ara/evidence/ tables."""
    # 遍历 ara/evidence/ 中的所有 claim 和表格
    # 提取数值（浮点数、百分比、科学计数法等）
    # 返回 deduplicated 列表
```

**关键特性**：
- **Multi-vote majority** — 默认 1 次（可调 3 次多数投票）
- **Ground-truth isolation** — Skeptic 只看候选数字 + 源 MD，不看 ARA 或答案键
- **Tolerance mode** — 默认允许部分未验证数字（< max_unconfirmed 或 < 20%）
- **Hard-block on fabrication** — 多数票说"未找到"→ 隔离，不重新执行

---

### `scripts/audit/g3_seal.py` — Seal gate (anchor + rigor + entailment)

**核心函数**：

```python
def g3_gate(
    stage_person: Path,  # branch1
    stage_ai: Path,      # branch2 (for comparison)
    md_path: Path,       # source truth
    entailment_judge: Callable,
    rigor_scores: Callable,
) → GateVerdict:
    """G3: Seal gate — presence check (G3R0) + equation fidelity + entailment + 6-dim rigor rubric.
    
    Runs AFTER both branches are built (before promotion).
    Hard blocks on structural violations.
    NOTE (ADR-0012): anchor resolution on branch1 PROSE is RETIRED. Only the engine's
    own ARA 核心结论 block (if it carries anchors) gets resolved; branch1 is plain prose.
    """
    
    findings = []
    
    # 1. G3R0: branch1 presence check (hard requirement)
    branch1_path = stage_person / "report.html"  # or .md
    if not branch1_path.exists():
        return GateVerdict(
            is_pass=False,
            is_hard_block=True,
            findings=[Finding(
                severity=Severity.CRITICAL,
                finding_type="branch1_missing",
                description="branch1 report.html not found",
            )],
            severity_max=Severity.CRITICAL,
        )
    
    # 2. Equation fidelity
    ara = load_ara_from_staging(stage_ai)
    md = md_path.read_text()
    
    eq_count_claimed = ara.get("eq_count_claimed", 0)
    eq_count_source = len(re.findall(r"^\$\$.*?\$\$$", md, re.MULTILINE))
    
    if eq_count_claimed != eq_count_source:
        findings.append(Finding(
            severity=Severity.WARNING,
            finding_type="equation_fidelity_mismatch",
            description=f"Claimed {eq_count_claimed} equations, found {eq_count_source} in MD",
        ))
    
    # 3. Entailment: sample claims and check if semantically sound
    claims = ara.get("claims", {})  # {claim_id: claim_text, ...}
    for claim_id, claim_text in list(claims.items())[:5]:  # sample
        # Find the experiment text linked to this claim
        experiment_text = _find_experiment_for_claim(ara, claim_id, md)
        if experiment_text:
            entails, reason = entailment_judge(claim_text, experiment_text)
            if not entails:
                findings.append(Finding(
                    severity=Severity.WARNING,
                    finding_type="entailment_mismatch",
                    description=f"{claim_id}: claim not entailed by experiment ({reason})",
                ))
    
    # 4. 6-dim rigor rubric
    ara_bundle = ara.get("text_bundle", {})
    rigor_result = rigor_scores(ara_bundle)
    # rigor_result = {dimensions: {D1: {score, strengths, weaknesses, ...}, ...}, findings: [...]}
    findings.extend(rigor_result.get("findings", []))
    
    # Determine pass/fail based on findings severity
    severity_max = max([f.severity for f in findings], default=Severity.INFO)
    is_hard_block = severity_max in (Severity.ERROR, Severity.CRITICAL)
    
    return GateVerdict(
        is_pass=not is_hard_block,
        is_hard_block=is_hard_block,
        findings=findings,
        severity_max=severity_max,
    )
```

---

### `scripts/audit/anchor_resolution.py` — Three-layer anchor lint (RETIRED per branch1, survives for engine core block)

> **ADR-0012 (2026-06-13, landed):** the hard-gated `check_report_faithfulness` seam was DELETED.
> The per-prose-line anchor requirement on branch1 is GONE. The 理解阅读 branch1 is now
> plain prose (no <!--ref--> anchors required). Prose faithfulness moved to the optional
> non-blocking **评价** assessment in `branch1_gate.py::build_assessment()` — (b) mechanical
> number-grounding vs ara_value_set + (c) a config-routed LLM judge (advisory note, never blocks).
>
> What SURVIVES here: anchor RESOLUTION in the ARA's own engine 核心结论 block (the internal
> machine-generated block, not the branch1 prose). The pseudocode below illustrates the concept,
> retained only for reference on how the engine's own anchors are resolved by G3.

**三层锚定架构**：

```
Layer 1: Equation block (from source MD)
  e.g., "$$v = x + y$$" at line 42

Layer 2: Claim reference (from branch1 / branch2)
  e.g., "<!--ref anchor_E5 to equation_42-->"
  Claims velocity equals x + y

Layer 3: Evidence table (from ARA)
  e.g., ara/evidence/claim_O1/ contains
    numbers: [1.0, 2.0, 3.0]  ← 实际值
    source_equation: E5
```

**核心函数**：

```python
def lint_text(text: str, md_path: Path) -> LintResult:
    """Three-layer anchor check on engine 核心结论 block (if present) against source MD.

    NOTE (ADR-0012): branch1 prose is plain text (no anchors required). The anchors
    that G3 resolves are only those in the engine's own ARA 核心结论 block (the
    machine-generated internal summary). This function resolves those anchors to
    real MD spans. The per-number trace below illustrates the anchor-resolution concept.
    """
    
    md = md_path.read_text()
    findings = []
    has_unanchored = False
    
    # 1. Extract all empirical numbers from text
    empirical_nums = _find_empirical_numbers(text)
    
    # 2. For each number, trace the three-layer path
    for num, context in empirical_nums:
        # Find anchor marker near the number
        anchor_match = re.search(r"<!--ref\s+(\w+)-->", context)
        if not anchor_match:
            findings.append(Finding(
                severity=Severity.ERROR,
                finding_type="unanchored_number",
                description=f"Number '{num}' has no anchor marker",
            ))
            has_unanchored = True
            continue
        
        anchor_id = anchor_match.group(1)
        
        # Layer 1 → 2: Verify anchor_id is in claims/evidence
        claim_for_anchor = _find_claim_by_anchor(text, anchor_id)
        if not claim_for_anchor:
            findings.append(Finding(
                severity=Severity.ERROR,
                finding_type="anchor_claim_mismatch",
                description=f"Anchor {anchor_id} not linked to any claim",
            ))
            has_unanchored = True
            continue
        
        # Layer 2 → 3: Verify claim links to evidence
        evidence_for_claim = _find_evidence_for_claim(text, claim_for_anchor)
        if not evidence_for_claim:
            findings.append(Finding(
                severity=Severity.ERROR,
                finding_type="claim_evidence_mismatch",
                description=f"Claim '{claim_for_anchor[:50]}' not linked to evidence table",
            ))
            has_unanchored = True
            continue
        
        # Layer 3 → MD: Verify evidence table links back to source
        md_source = _find_md_source(md, evidence_for_claim)
        if not md_source:
            findings.append(Finding(
                severity=Severity.ERROR,
                finding_type="evidence_md_mismatch",
                description=f"Evidence table not found in source MD",
            ))
            has_unanchored = True
    
    return LintResult(
        has_unanchored=has_unanchored,
        findings=findings,
    )
```

---

### `scripts/audit/rigor_rubric.py` — 6-dimensional rigor assessment

**六个维度** (DIMENSION_KEYS):

```python
DIMENSION_KEYS = [
    "D1_evidence_relevance",        # Claims backed by empirical evidence?
    "D2_methodological_rigor",      # Experiment design sound?
    "D3_baselines_fairness",        # Fair comparison to SOTA?
    "D4_reproducibility_clarity",   # Can you reproduce it?
    "D5_generalization_scope",      # How general are the findings?
    "D6_clarity_presentation",      # Is the paper well-written?
]

class RigorScore:
    dimension: str
    score: int  # 1-5 (1=poor, 5=excellent)
    strengths: list[str]
    weaknesses: list[str]
    suggestions: list[str]
```

**核心函数**：

```python
def rigor_scores(ara_bundle: dict) -> dict:
    """Call the G3 rigor seam (LLM) to score the paper on six dimensions.
    
    Seam protocol:
      Input: ara_bundle (text dict, no numbers)
      Output: {
        dimensions: {
          D1_evidence_relevance: {score: 4, strengths: [...], weaknesses: [...], suggestions: [...]},
          ...
        },
        findings: [Finding(...), ...]
      }
    
    Rubric is PRIVATE to the seam (不在生成器 prompt 中出现).
    """
    # The seam receives only the text content, not the evidence tables
    # or numerical results. This ensures the rigor assessment is
    # based on the methodology + clarity, not the headline numbers.
```

---

### `scripts/audit/entailment.py` — Type-aware entailment check

**核心函数**：

```python
def entailment_judge(claim: str, experiment_text: str) -> tuple[bool, str]:
    """Semantic entailment: does the claim logically follow from the experiment?
    
    Example:
      Claim: "Our model achieves 95% accuracy on ImageNet."
      Experiment: "We evaluated on 50k validation images, achieving 95.0 ± 0.5 accuracy."
      → Entails: True, reason: "95% matches experiment result"
    
    Seam is called independently (not correlated with generator).
    """
    # Seam logic (private):
    # 1. Parse the claim type (numeric assertion? semantic claim?)
    # 2. Extract the key assertion (e.g., "95% accuracy")
    # 3. Search experiment text for supporting evidence
    # 4. Semantic match: does the evidence support the claim?
    # 5. Return (True, reason) or (False, reason)
```

---

### `scripts/audit/equation_fidelity.py` — Mechanical equation count check

**核心函数**：

```python
def check_equation_fidelity(md_path: Path, ara_bundle: dict) -> GateVerdict:
    """Mechanical check: did the analyzer claim the right number of equations?
    
    No LLM involved; just regex count.
    """
    
    md = md_path.read_text()
    
    # Count $$ blocks (LaTeX display math)
    eq_count_source = len(re.findall(r"^\$\$.*?\$\$$", md, re.MULTILINE | re.DOTALL))
    
    # Count from analyzer's ara_bundle
    eq_count_claimed = ara_bundle.get("eq_count_claimed", 0)
    
    if eq_count_source == eq_count_claimed:
        return GateVerdict(is_pass=True)
    else:
        return GateVerdict(
            is_pass=False,
            is_hard_block=False,  # Warning, not hard-block
            findings=[Finding(
                severity=Severity.WARNING,
                finding_type="equation_count_mismatch",
                description=f"Claimed {eq_count_claimed}, found {eq_count_source}",
            )],
        )
```

---

### `scripts/audit/gate_runner.py` — Bounded retry + escalation

**核心函数**：

```python
def bounded_gate_runner(
    gate_fn: Callable[[], GateVerdict],
    max_rounds: int = 1,
    seam_name: str = "G2",
) → GateVerdict | None:
    """Run a gate up to max_rounds times, then quarantine if still failing.
    
    If gate_fn fails (hard_block), re-emit the branch (call the upstream
    rebuild) up to max_rounds - 1 additional times. If all rounds fail,
    escalate to quarantine.
    
    Returns: final GateVerdict if pass, None if quarantine.
    """
    
    for round_idx in range(max_rounds):
        verdict = gate_fn()
        
        if verdict.is_pass:
            return verdict
        
        if verdict.is_hard_block:
            if round_idx < max_rounds - 1:
                # Re-emit: rebuild the branch and try again
                # (caller does the rebuild, we just call gate_fn again)
                continue
            else:
                # Max rounds exhausted, escalate to quarantine
                return None  # Signal: quarantine this paper
        else:
            # Soft warning (not hard-block), pass anyway
            return verdict
    
    # Should not reach here, but just in case
    return None
```

**使用方式** (spoke 内):

```python
# G2 gate with retry
verdict_g2 = bounded_gate_runner(
    gate_fn=lambda: g2_gate(stage_ai, skeptic_votes, config),
    max_rounds=config.get("max_gate_rounds", 1),
    seam_name="G2",
)

if verdict_g2 is None:
    # 数字门 hard-block → spoke 把 staged ARA 保留成 _failed/<key>/ 现场 (不删, ADR-0011)
    preserve_scene(key, staged_dir, failed_gate="数字门")
    return
elif verdict_g2.is_hard_block:
    # Re-emit not exhausted yet (internal retry happened)
    pass
```

---

## 配置与常数

### `config/audit.yaml` — Audit tuning

```yaml
skeptic_votes: 1              # 默认 1 次投票；3 = 三投多数
max_gate_rounds: 1            # 重新执行门多少次后隔离
data_fidelity:
  mode: tolerant              # strict 或 tolerant
  max_unconfirmed: 5          # 最多允许的未验证数字
  max_unconfirmed_ratio: 0.2  # 或最多 20% 的检查数字
```

### 重要常数

| 常数 | 值 | 含义 |
|-----|---|----|
| `_MD_CHAR_CAP` | 200k | Skeptic/rigor seam 的输入 MD 字符上限（避免 OOM） |
| `max_gate_rounds` | 1 | 默认不重新执行；改 audit.yaml 为 2-3 以允许重试 |
| `max_unconfirmed` | 5 | Tolerant 模式允许最多 5 个未验证的数字 |
| `max_unconfirmed_ratio` | 0.2 | 或最多 20% 的已检查数字未验证 |

---

## 不变式与保证

1. **Ground-truth isolation** — G2 skeptic + G3 rigor 分别调用独立 seam，与生成器不相关
2. **Multi-vote majority** — G2 默认 1 次（可调 3 次）；多数决定是否验证
3. **Hard-block on fabrication** — 多数 skeptic 票说"未找到"→ 隔离，不重新执行
4. **G3 structure (ADR-0012)** — G3R0 (branch1 presence) + equation + entailment + rigor；不再对分支1 prose 进行逐行锚点检查（branch1 is plain prose; 评价 assessment is fail-soft diagnostic note）
5. **Branch1 never blocks** — 分支1 评价是进展笔记，不是 hard gate；ARA-side gates (结构门/Seal-1, G2, G3 entailment+rigor+equation) 保持硬门
6. **Bounded escalation** — G2/G3 失败最多重新执行 N 轮，然后隔离（无无限循环）
7. **Deterministic equation check** — 等式计数是机械的（regex），无 LLM 参与

---

## 相关文档

- `engine-core.md` — 门运行流程（spoke 中的顺序）
- `llm-pipeline.md` — Seam 工厂和提供商路由
- `references/ara-schema.md` — ARA bundle 格式
- `references/branch1-quality.md` — 锚定规范

