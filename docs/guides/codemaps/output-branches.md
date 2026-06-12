# Output Branches (Branch2 + Branch1) 代码地图

> **范围**: `scripts/output/` — branch1_llm.py, branch1_report.py, branch2_ara.py, ara_schema.py, naming.py, figures.py, produce.py
> **最后更新**: 2026-06-08
> **关键特性**: 双链原子产出 (OT-5)、LLM 写入人链、图形策展、vault 命名权威

<!-- Generated: 2026-06-08 | Files scanned: 9 | Token estimate: ~3500 -->

## 高层输出结构

```
per-paper spoke:
    ↓
branch2 (ARA compiler)
    ├─ input: analysis dict (from resolve_analysis seam)
    ├─ compile: ara/claims/, ara/evidence/, ara/AUDIT_FLAGS.md
    └─ output: ai_package/{key}/ara/ (staging)
         │
         ├─ claims/
         │  └─ O1.md, O2.md, ...  (individual claims)
         │
         ├─ evidence/
         │  └─ claim_O1/table.csv, figure.png, ...
         │
         └─ PAPER.md  (frontmatter + overview)
    ↓
G2 gate (data-fidelity on evidence)
    ↓ (pass)
branch1 (human report)
    ├─ LLM-written path (if write_report seam provided):
    │  ├─ write_report(ara, figures) → vivid Chinese sections
    │  ├─ build core-conclusions (mechanically grounded, <!--ref--> anchored)
    │  ├─ 忠实门 (ADR-0012): (b) prose numbers grounded vs MD + (c) judge
    │  ├─ curate figures (arch mandatory + top-N results)
    │  ├─ self-contained HTML (MathJax + mermaid + base64)
    │  └─ output: person_vault/{key}/report.html
    │
    └─ thin deterministic path (if no write_report):
       ├─ format analysis → markdown template
       ├─ 忠实门 (ADR-0012): kept anchor-form lint + (b) grounding
       └─ output: person_vault/{key}/report.md
    ↓
G3 gate (seal: anchor + eq fidelity + rigor + entailment)
    ↓ (pass)
promote both (OT-5 atomic)
    ├─ move ai_package/{key}/ from staging to real vault
    ├─ move person_vault/{key}/ from staging to real vault
    └─ hub.mark_done(key, person_path, ai_path)
```

---

## 模块拓扑

### `scripts/output/naming.py` — Vault key authority

**核心函数**：

```python
def vault_key(candidate: dict, intake_date: str) -> str:
    """THE single live vault-key authority.
    
    Returns a DETERMINISTIC key that uniquely identifies the paper's vault entry.
    Format: {intake_date}_{canonical_name}_{arxiv_id_base}
    
    Example: "20260608_Hinton_etal_1706"
             (June 8, 2026 intake; Hinton et al.; arxiv 1706.xxxxx)
    
    MUST be called once per paper and never re-derived elsewhere.
    Hub stores this key in the ledger so spoke returns it, hub uses it.
    """
    
    # 1. Intake date (from ledger.intake_date())
    intake_dt = intake_date or datetime.now().strftime("%Y%m%d")
    
    # 2. Canonical name (first 1-3 author last names, sanitized)
    authors = candidate.get("authors", [])
    if len(authors) == 1:
        name_part = authors[0].split()[-1]  # Last name
    elif len(authors) == 2:
        name_part = f"{authors[0].split()[-1]}_{authors[1].split()[-1]}"
    else:
        name_part = f"{authors[0].split()[-1]}_etal"
    
    name_part = _sanitize_name(name_part)  # Remove non-alphanum
    
    # 3. arxiv_id base (first 4 digits = year or next 4 = sequence)
    arxiv_id = candidate.get("arxiv_id", "unknown")
    arxiv_base = arxiv_id.replace(".", "")[:4]  # "1706" from "1706.xxxxx"
    
    key = f"{intake_dt}_{name_part}_{arxiv_base}"
    return key

def derive_name(candidate: dict, ledger: Ledger) -> str:
    """Wrapper: calls vault_key with ledger's intake_date()."""
    return vault_key(candidate, ledger.intake_date())

def find_existing_entries(key: str, workspace: Path) -> tuple[Path | None, Path | None]:
    """Find existing person_vault + ai_package entries for a key.
    
    Useful for detecting re-ingestion or cache hits.
    """
    person_base = workspace / "person_vault"
    ai_base = workspace / "ai_package"
    
    person_matches = list(person_base.glob(f"{key}*"))
    ai_matches = list(ai_base.glob(f"{key}*"))
    
    return (person_matches[0] if person_matches else None,
            ai_matches[0] if ai_matches else None)
```

**关键约束**：
- Deterministic: 同一论文 = 相同 key（reproducible）
- Never re-derived: 只有 `derive_name()` 调用 `vault_key()` 一次
- Hub stores + reuses: hub 从 spoke 返回值读 key，不重新计算

---

### `scripts/output/branch2_ara.py` — ARA compiler (AI-facing)

**核心函数**：

```python
def write_branch2(
    stage_ai: Path,
    analysis: dict,
    candidate: dict,
    key: str,
) → None:
    """Compile the ARA (AI-facing knowledge pack) from analysis dict.
    
    ARA Structure:
      {key}/ara/
      ├─ PAPER.md           # Frontmatter + overview
      ├─ claims/
      │  ├─ O1.md           # Original observation 1
      │  ├─ O2.md
      │  └─ ...
      ├─ evidence/
      │  ├─ claim_O1/
      │  │  ├─ table.csv
      │  │  ├─ figure.png
      │  │  └─ extraction_notes.md
      │  └─ claim_O2/
      │     └─ ...
      ├─ AUDIT_FLAGS.md     # G2 findings + warnings
      └─ index.json         # Manifest
    """
    
    # Ensure staging dir
    ara_dir = stage_ai / "ara"
    ara_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Write PAPER.md (frontmatter + overview)
    paper_md = f"""---
key: {key}
arxiv_id: {candidate.get('arxiv_id')}
doi: {candidate.get('doi')}
title: {candidate.get('title')}
authors: {candidate.get('authors')}
year: {candidate.get('year')}
venue: {candidate.get('venue')}
---

# {candidate.get('title')}

## Overview

{analysis.get('overview', '')}

## Problem Statement

{analysis.get('problem', '')}
"""
    (ara_dir / "PAPER.md").write_text(paper_md)
    
    # 2. Write claims/
    claims_dir = ara_dir / "claims"
    claims_dir.mkdir(exist_ok=True)
    
    for claim_id, claim_text in analysis.get("claims", {}).items():
        claim_file = claims_dir / f"{claim_id}.md"
        claim_file.write_text(f"# {claim_id}\n\n{claim_text}")
    
    # 3. Write evidence/
    evidence_dir = ara_dir / "evidence"
    evidence_dir.mkdir(exist_ok=True)
    
    for claim_id, evidence_tables in analysis.get("evidence_tables", {}).items():
        claim_ev_dir = evidence_dir / f"claim_{claim_id}"
        claim_ev_dir.mkdir(exist_ok=True)
        
        # Evidence is structured (table.csv, figure.png, notes.md)
        for table_name, table_data in evidence_tables.items():
            table_file = claim_ev_dir / f"{table_name}.csv"
            # Write table_data as CSV
            table_file.write_text(_dict_to_csv(table_data))
    
    # 4. Write AUDIT_FLAGS.md (placeholder; G2 fills in)
    (ara_dir / "AUDIT_FLAGS.md").write_text("# Audit Flags\n\n(Empty before G2)\n")
    
    # 5. Write index.json (manifest)
    index = {
        "key": key,
        "arxiv_id": candidate.get("arxiv_id"),
        "claims_count": len(analysis.get("claims", {})),
        "evidence_count": len(analysis.get("evidence_tables", {})),
        "generated_at": datetime.now().isoformat(),
    }
    (ara_dir / "index.json").write_text(json.dumps(index, indent=2))
```

**关键特性**：
- **Deterministic**: Analysis dict → fixed ARA structure
- **Evidence tables only**: No loose numbers in prose (all in tables)
- **AUDIT_FLAGS placeholder**: G2 填充
- **manifest (index.json)**: Cross-reference friendly

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
    faithfulness_judge: Callable | None = None,  # branch1 忠实门 (c), ADR-0012
) → None:
    """Render branch1 (human report) deterministically from analysis.
    
    This is the THIN path: analysis → markdown template.
    No LLM involved; 100% reproducible.
    
    Used when write_report seam is NOT provided (default fallback).
    """
    
    # Build markdown
    report = f"""# {candidate.get('title')}

**Authors**: {', '.join(candidate.get('authors', []))}
**Year**: {candidate.get('year')}
**arXiv**: {candidate.get('arxiv_id')}

## Core Conclusions

{analysis.get('overview', '')}

## Problem

{analysis.get('problem', '')}

## Methods

{analysis.get('algorithm', '')}

## Results

{analysis.get('results', '')}

## Related Work

{analysis.get('related_work', '')}
"""
    
    # branch1 忠实门 (ADR-0012): kept anchor-form lint (engine 核心结论 block) +
    # (b) mechanical prose-number grounding vs source MD + (c) optional judge.
    # Prose may carry numbers; only an UNGROUNDED number (or judge drift) blocks.
    hard = check_report_faithfulness(report, md_text, ara_dir, judge=faithfulness_judge)
    if hard:
        raise AnchorGateError(f"忠实门: {[f.observation for f in hard]}")
    
    # Write
    (stage_person / "report.md").write_text(report)
    
    # Metadata
    metadata = {
        "key": key,
        "title": candidate.get("title"),
        "arxiv_id": candidate.get("arxiv_id"),
        "generated_method": "thin_deterministic",
        "generated_at": datetime.now().isoformat(),
    }
    (stage_person / "metadata.json").write_text(json.dumps(metadata))
```

---

### `scripts/output/branch1_llm.py` — LLM-written human chain

**核心函数** (详见 llm-pipeline.md):

```python
def write_branch1_llm(
    stage_person: Path,
    candidate: dict,
    stage_ai: Path,
    md_path: Path,
    write_report: Callable,  # LLM seam
    key: str,
    faithfulness_judge: Callable | None = None,  # LLM seam — branch1 忠实门 (c), ADR-0012
) → None:
    """Render branch1 (human report) via LLM writer.
    
    LLM-written path: analysis → vivid Chinese prose (from write_report seam).
    Faithfulness-checked (ADR-0012): prose numbers grounded vs MD ((b)) + (c) judge;
    the engine 核心结论 block stays triple-anchored.
    """
    
    # 1. Load ARA + figures
    ara = load_ara_from_staging(stage_ai)
    figures = extract_figures(md_path.parent / "images/")
    curated_figs = curate_figures(ara, figures)
    
    # 2. Call LLM writer
    sections = write_report(ara=ara, figures=curated_figs)
    # sections = {
    #   "introduction": "系统提出了...",
    #   "methods": "我们的方法...",
    #   "results": "实验结果...",
    # }
    
    # 3. Build core-conclusions block (mechanically grounded)
    core_block = _build_core_conclusions(ara, md_path)
    
    # 4. Assemble report
    report = _assemble_report(
        title=candidate.get("title"),
        core_block=core_block,
        sections=sections,
        figures=curated_figs,
    )
    
    # 5. Anchor the engine 核心结论 block (so 最终门 resolves it); ADR-0012: prose
    #    numbers are GROUNDED vs MD by the 忠实门, not required to self-anchor.
    report = _ground_empirical_claims(report, md_path)
    
    # 6. Deterministic normalization
    report = _strip_emoji(report)  # 铁律：无 emoji
    report = _quote_mermaid_labels(report)
    
    # 7. branch1 忠实门 (ADR-0012): kept anchor-form lint + (b) prose-number
    #    grounding + (c) judge. Prose numbers allowed if grounded in the MD.
    hard = check_report_faithfulness(report, md_text, ara_dir, judge=faithfulness_judge)
    if hard:
        raise AnchorGateError(...)
    
    # 8. Convert to self-contained HTML
    html = _to_html_self_contained(report, figures=curated_figs)
    
    # 9. Write
    (stage_person / "report.html").write_text(html)
    
    metadata = {
        "key": key,
        "title": candidate.get("title"),
        "generated_method": "llm_vivid_chinese",
        "figures_curated": len(curated_figs),
        "generated_at": datetime.now().isoformat(),
    }
    (stage_person / "metadata.json").write_text(json.dumps(metadata))

def _build_core_conclusions(ara: dict, md_path: Path) -> str:
    """Build the 核心结论 block from ARA claims.
    
    Every claim statement is mechanically three-layer-anchored:
      claim_text <!--ref anchor_O1--> [equation → evidence → MD]
    """
    
    claims = ara.get("claims", {})
    lines = ["## 核心结论\n"]
    
    for claim_id, claim_text in claims.items():
        # Find evidence for this claim
        evidence = ara.get("evidence_tables", {}).get(claim_id, {})
        
        # Build anchor trail: claim → evidence → equation
        anchor_id = f"anchor_{claim_id}"
        eq_ref = f"equation_{claim_id}"
        
        # Three-layer anchor: <!--ref anchor_O1 to evidence_O1 to equation_5-->
        anchored_claim = f"{claim_text} <!--ref {anchor_id} to {eq_ref}-->"
        
        lines.append(f"- {anchored_claim}")
    
    return "\n".join(lines)
```

---

### `scripts/output/figures.py` — Figure curation

**核心函数**：

```python
class Figure:
    ref: str              # filepath or base64 key
    caption: str          # original caption
    category: str         # "architecture", "results", "ablation", ...
    confidence: float     # selection confidence

def extract_figures(images_dir: Path) -> list[Figure]:
    """Extract all figures from corpus/{ID}/images/."""
    
    figures = []
    for img_path in images_dir.glob("**/*.png"):
        # Infer category from filename
        category = _infer_category(img_path.name)
        
        # Read caption (from content_list.json or filename)
        caption = _read_caption(img_path, images_dir)
        
        figures.append(Figure(
            ref=f"../images/{img_path.relative_to(images_dir)}",
            caption=caption,
            category=category,
            confidence=_estimate_confidence(img_path),
        ))
    
    return figures

def curate_figures(ara: dict, figures: list[Figure]) -> list[Figure]:
    """Select figures: MANDATORY architecture + top-N others.
    
    Strategy:
      1. Find architecture diagram (mandatory) → always include
      2. Find top-3 high-confidence result figures
      3. Avoid consecutive images (one can't be caption for previous)
    """
    
    curated = []
    
    # 1. Mandatory architecture
    arch_figs = [f for f in figures if f.category == "architecture"]
    if arch_figs:
        curated.append(arch_figs[0])  # Take first (usually best)
    
    # 2. Result figures (sorted by confidence)
    result_figs = sorted(
        [f for f in figures if f.category == "results"],
        key=lambda f: f.confidence,
        reverse=True,
    )
    
    # 3. Select top-N, avoiding consecutive
    selected_indices = set()
    for fig in result_figs:
        if len(curated) >= 4:  # Max 5 total (1 arch + 4 results)
            break
        
        fig_idx = figures.index(fig)
        # Check if adjacent to previous selection
        if not any(abs(fig_idx - prev_idx) == 1 for prev_idx in selected_indices):
            curated.append(fig)
            selected_indices.add(fig_idx)
    
    return curated

def is_architecture_caption(caption: str) -> bool:
    """Heuristic: is this caption describing an architecture diagram?"""
    arch_keywords = ["architecture", "pipeline", "network", "model", "flow", "diagram"]
    return any(kw in caption.lower() for kw in arch_keywords)

def copy_figures(
    curated_figs: list[Figure],
    source_dir: Path,
    target_dir: Path,
) → dict[str, str]:
    """Copy curated figures to staging and return {ref: base64_key}."""
    
    base64_map = {}
    
    for fig in curated_figs:
        src = source_dir / fig.ref
        if src.exists():
            # Base64 inline (for self-contained HTML)
            with open(src, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            
            # Key: figure reference
            key = fig.ref
            base64_map[key] = data
    
    return base64_map
```

---

### `scripts/output/ara_schema.py` — ARA structural validator

**核心函数**：

```python
def validate_ara(ara_dir: Path) -> bool:
    """Validate ARA directory structure (Seal Level 1)."""
    
    required_files = [
        "PAPER.md",
        "index.json",
        "AUDIT_FLAGS.md",
    ]
    
    required_dirs = [
        "claims/",
        "evidence/",
    ]
    
    # Check required files
    for f in required_files:
        if not (ara_dir / f).exists():
            raise ValueError(f"Missing {f}")
    
    # Check required dirs
    for d in required_dirs:
        if not (ara_dir / d).is_dir():
            raise ValueError(f"Missing {d}")
    
    # Validate claims/ entries
    claims_dir = ara_dir / "claims"
    for claim_file in claims_dir.glob("*.md"):
        claim_id = claim_file.stem
        # Verify corresponding evidence/
        evidence_dir = ara_dir / "evidence" / f"claim_{claim_id}"
        if not evidence_dir.exists():
            raise ValueError(f"Claim {claim_id} has no evidence dir")
    
    return True
```

---

## 配置与常数

| 常数 | 值 | 含义 |
|-----|---|----|
| `MAX_CURATED_FIGURES` | 5 | 强制 arch + 最多 4 个结果图 |
| `CONFIDENCE_THRESHOLD` | 0.7 | 图选中的置信度最低值 |
| `NO_EMOJI_IRON_RULE` | — | 所有报告必须无表情符号（确定性剥离） |
| `ANCHOR_DEPTH` | 3 | 三层锚定：数字 → 声明 → 证据 → MD |

---

## 关键不变式

1. **Single vault-key authority** — `naming.py` 中的 `vault_key()` 是唯一来源
2. **Atomic dual-output** — Branch2 + Branch1 同时成功或同时失败（OT-5）
3. **Deterministic naming** — Key = `{intake_date}_{Name}_{arxiv_base}`（可重现）
4. **忠实门 (ADR-0012)** — 正文数字允许自然书写，但必须机械落源到 MD（(b)）+ 不得相对 ARA 实质误导（(c) 判官）；引擎 `核心结论` 块仍保留 `<!--ref-->` 三层锚点
5. **Mandatory architecture** — Branch1 中强制包含架构图
6. **NO emoji** — 所有报告确定性剥离表情符号（项目铁律）
7. **Self-contained HTML** — Branch1 HTML 报告中的图片 base64 inline（不外链）

---

## 相关文档

- `engine-core.md` — Branch 构建在 spoke/produce 中的位置
- `llm-pipeline.md` — LLM writer seam 的路由
- `audit-gates.md` — G2/G3 门的触发点
- `references/ara-schema.md` — ARA bundle 格式详细规范
- `references/branch1-quality.md` — Branch1 质量标准 + 锚定规范

