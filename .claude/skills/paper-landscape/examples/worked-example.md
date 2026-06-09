# Worked example — one paper, end to end

> **REAL EXAMPLE.** This walkthrough uses the best-scoring in-place ARA in the
> workspace — **DreamerV3** (*Mastering Diverse Domains through World Models*,
> arXiv `2301.04104`), Seal-2 grade **Strong Accept** (mean 4.67). Numbers are the
> paper's own. The ARA bundle here is the same instance as
> [`sample-ara-bundle.json`](sample-ara-bundle.json); the output shapes match
> [`../templates/`](../templates/); the rules cited live in
> [`../references/`](../references/). The frozen-MD excerpt is shortened for the
> walkthrough — the engine anchors against the full converted MD.

Paper: *"Mastering Diverse Domains through World Models"* (DreamerV3), arXiv
`2301.04104`, 2023. Headline: **9.1 Minecraft Diamond Return, 200.0 M params.**

The hub drives `discover → ingest → ledger → branch2 → G2 → branch1 → G3 → landscapes`
(`SKILL.md` "Full pipeline order"). Each stage below shows what crosses the seam.

---

## 0. Campaign locked (Hard Gate, once)

`config/campaign.yaml` → `topic: "world models for control"`, `n_per_tick: 5`,
`is_ad_domain: false`. Until this exists `run_campaign` raises `GateRequired`.

## 1. discover(topic, n) → candidate

`build_discover(llm=expand_llm, is_ad_domain=False)("world models for control", 5)`
returns a ranked pool; one candidate (the deterministic discovery layer, not an LLM seam):

```json
{
  "arxiv_id": "2301.04104", "doi": null,
  "title": "Mastering Diverse Domains through World Models",
  "year": 2023, "venue": null, "authors": ["Hafner, ..."],
  "oa_pdf_url": "https://arxiv.org/pdf/2301.04104",
  "github_repo": "https://github.com/danijar/dreamerv3",
  "discovery_sources": ["openalex", "arxiv"], "authority_score": 0.93, "is_retracted": false
}
```
<!-- branch2 reads candidate: arxiv_id, doi, github_repo, title, venue, year, authors. -->


Authority fired on institution + heat signals (ADR-0001: any-signal OR, no citation gate).

## 2. ingest → frozen MD

Tier-1 (arXiv-HTML → pandoc) succeeds → `corpus/2301.04104/2301.04104.md` +
`.md_contract.json` + a synthesized `content_list.json`. Equation/table survival
ratios pass (`references/ingest-fidelity.md`). Vault key (sole authority,
`scripts/output/naming.py`): `2026-06-08_Dreamer_2301.04104` = `{ingest-date}_{Name}_{idbase}`,
`idbase = identity_base("2301.04104") = "2301.04104"` (version stripped).

## 3. resolve_analysis(md_path, candidate) → ARA bundle  [LLM seam #1]

A fresh analyzer sub-agent reads the frozen MD and returns the bundle in
[`sample-ara-bundle.json`](sample-ara-bundle.json) — note the **required** headline
keys `headline_metric: "Minecraft Diamond Return"`, `headline_value: 9.1`,
`params_million: 200.0`, and that exact figures sit under `evidence_tables`, not in
prose. Role:
[`../sub-skills/analyze-paper/SKILL.md`](../sub-skills/analyze-paper/SKILL.md);
schema: [`../references/ara-schema.md`](../references/ara-schema.md).

## 4. branch2 → ai_package/{key}/ara/PAPER.md

The bundle is written into the AI knowledge pack (template:
[`../templates/ara-paper.md`](../templates/ara-paper.md)). Frontmatter excerpt:

```yaml
schema_version: "1.0"
key: 2301.04104
domain: model-based reinforcement learning / world models
keywords: [RSSM, symlog/symexp, symexp twohot loss, KL free bits, imagination training]
headline_metric: Minecraft Diamond Return
headline_value: 9.1
params_million: 200.0
```

## 5. G2 data-fidelity gate  [LLM seam #2 — runs AFTER branch2, BEFORE branch1]

`run_g2` extracts the candidate numbers from the staged ARA evidence
(`["9.1", "7.1", "100", "150", "200", "15", ...]`) and calls `skeptic_votes`
`n_skeptics=3` times. Each skeptic sees **only** the numbers + the source MD —
never the answer key (`../sub-skills/g2-skeptic/SKILL.md`):

```
skeptic_votes(("9.1","7.1","100"), source_md, "main results") ->
  (SkepticVote("9.1", found_in_source=True),
   SkepticVote("7.1", found_in_source=True),
   SkepticVote("100", found_in_source=True))
```

All confirmed by majority → **pass**, branch1 proceeds. *Counter-case*: had the
analyzer written `12.0` (absent from the MD), the majority would vote
`found_in_source=False` → `ProduceGateBlocked`, nothing promoted (OT-5),
`_failed/{key}.md` written, hub backfills the next candidate.

## 6. branch1 → person_vault/{key}/report.md  [anchored]

The illustrated Chinese report (template:
[`../templates/branch1-report.md`](../templates/branch1-report.md); quality bar:
[`../references/branch1-quality.md`](../references/branch1-quality.md)). The
claim weave anchors every grounded number into the frozen MD:

```markdown
## 摘要翻译
...在 Minecraft Diamond 上取得 9.1<!--ref:r-9-1--><!--anchor:quote:9.1--> 的回合回报,强于最强基线的 7.1<!--ref:r-7-1--><!--anchor:quote:7.1-->。
```

`### 数学方法` / `### Loss 亮点解释` stay number-free (from `math_intuition` /
`loss_highlight`), so they make no performance claim and pass the anchor gate.

## 7. G3 seal  [LLM seams #3 + #4 — after both branches]

`rigor_scores(ara_bundle)` returns the 6 `DIMENSION_KEYS`
(`../sub-skills/g3-rigor-reviewer/SKILL.md`):

```
D1_evidence_relevance:5  D2_falsifiability:4  D3_scope_calibration:5
D4_argument_coherence:5  D5_exploration_integrity:5  D6_methodological_rigor:4
```

mean = 4.67, min = 4 → grade **Strong Accept** → `passes_seal2 = true`.
`entailment_judge` confirms C1 (a `generalization` claim) is entailed by experiment
E1. Anchor lint passes. `level2_report.json` is written; the seal holds. (Had the
grade been < Weak Accept, `run_g3` returns a blocked `GateVerdict` carrying a
hard-block `SEAL2` finding, and the bounded `run_with_budget` re-emits, then
quarantines.)

## 8. landscapes → cross-paper row

After the batch, `landscapes.py` reads this PAPER.md's headline frontmatter into the
unified table (template: [`../templates/landscape.md`](../templates/landscape.md)):

```
| 论文 | 年份 | 主指标 | 数值 | 参数量(M) | 效率(指标/M) |
| Mastering Diverse Domains ... | 2023 | Minecraft Diamond Return | 9.1 | 200.0 | 0.0455 |
```

efficiency = `round(9.1 / 200.0, 4) = 0.0455`. A PAPER.md missing any headline key
would be silently dropped from this table — which is why step 3's bundle MUST carry them.
