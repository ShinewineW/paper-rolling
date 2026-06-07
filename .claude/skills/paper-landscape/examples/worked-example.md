# Worked example — one paper, end to end

> **ILLUSTRATIVE.** The paper, its id, and every number below are **synthetic**,
> shown only to make the pipeline's inputs/outputs concrete. Do not cite. The ARA
> bundle here is the same instance as [`sample-ara-bundle.json`](sample-ara-bundle.json);
> the output shapes match [`../templates/`](../templates/); the rules cited live in
> [`../references/`](../references/).

Synthetic paper: *"Latent World Models for Sample-Efficient Robotic Planning"*,
arXiv `2403.04567` (illustrative), 2024. Headline: **87.3% success_rate, 42.0 M params.**

The hub drives `discover → ingest → ledger → branch2 → G2 → branch1 → G3 → landscapes`
(`SKILL.md` "Full pipeline order"). Each stage below shows what crosses the seam.

---

## 0. Campaign locked (Hard Gate, once)

`config/campaign.yaml` → `topic: "world models for planning"`, `n_per_tick: 5`,
`is_ad_domain: false`. Until this exists `run_campaign` raises `GateRequired`.

## 1. discover(topic, n) → candidate

`build_discover(llm=expand_llm, is_ad_domain=False)("world models for planning", 5)`
returns a ranked pool; one candidate (the deterministic discovery layer, not an LLM seam):

```json
{
  "arxiv_id": "2403.04567", "doi": null,
  "title": "Latent World Models for Sample-Efficient Robotic Planning",
  "year": 2024, "venue": "NeurIPS", "authors": ["Chen, ..."],
  "oa_pdf_url": "https://arxiv.org/pdf/2403.04567",
  "github_repo": "https://github.com/example/latent-world-models",
  "discovery_sources": ["openalex", "arxiv"], "authority_score": 0.81, "is_retracted": false
}
```
<!-- branch2 reads candidate: arxiv_id, doi, github_repo, title, venue, year, authors. -->


Authority fired on venue + institution signals (ADR-0001: any-signal OR, no citation gate).

## 2. ingest → frozen MD

Tier-1 (arXiv-HTML → pandoc) succeeds → `corpus/2403.04567/2403.04567.md` +
`.md_contract.json` + a synthesized `content_list.json`. Equation/table survival
ratios pass (`references/ingest-fidelity.md`). Vault key (sole authority,
`scripts/output/naming.py`): `2026-06-07_Chen_2403.04567` = `{ingest-date}_{Name}_{idbase}`,
`idbase = identity_base("2403.04567") = "2403.04567"` (version stripped).

## 3. resolve_analysis(md_path, candidate) → ARA bundle  [LLM seam #1]

A fresh analyzer sub-agent reads the frozen MD and returns the bundle in
[`sample-ara-bundle.json`](sample-ara-bundle.json) — note the **required** headline
keys `headline_metric: "success_rate"`, `headline_value: 87.3`, `params_million: 42.0`,
and that exact figures sit under `evidence_tables`, not in prose. Role:
[`../sub-skills/analyze-paper/SKILL.md`](../sub-skills/analyze-paper/SKILL.md);
schema: [`../references/ara-schema.md`](../references/ara-schema.md).

## 4. branch2 → ai_package/{key}/ara/PAPER.md

The bundle is written into the AI knowledge pack (template:
[`../templates/ara-paper.md`](../templates/ara-paper.md)). Frontmatter excerpt:

```yaml
schema_version: "1.0"
key: 2403.04567
domain: world models / model-based reinforcement learning
keywords: [latent dynamics model, imagination rollout, value-equivalent prediction]
headline_metric: success_rate
headline_value: 87.3
params_million: 42.0
```

## 5. G2 data-fidelity gate  [LLM seam #2 — runs AFTER branch2, BEFORE branch1]

`run_g2` extracts the candidate numbers from the staged ARA evidence
(`["87.3", "12.4", "74.9", "42.0", "15", "256", ...]`) and calls `skeptic_votes`
`n_skeptics=3` times. Each skeptic sees **only** the numbers + the source MD —
never the answer key (`../sub-skills/g2-skeptic/SKILL.md`):

```
skeptic_votes(("87.3","12.4","74.9"), source_md, "main results") ->
  (SkepticVote("87.3", found_in_source=True),
   SkepticVote("12.4", found_in_source=True),
   SkepticVote("74.9", found_in_source=True))
```

All confirmed by majority → **pass**, branch1 proceeds. *Counter-case*: had the
analyzer written `91.0%` (absent from the MD), the majority would vote
`found_in_source=False` → `ProduceGateBlocked`, nothing promoted (OT-5),
`_failed/{key}.md` written, hub backfills the next candidate.

## 6. branch1 → person_vault/{key}/report.md  [anchored]

The illustrated Chinese report (template:
[`../templates/branch1-report.md`](../templates/branch1-report.md); quality bar:
[`../references/branch1-quality.md`](../references/branch1-quality.md)). The
abstract weave anchors every grounded number:

```markdown
## 摘要翻译
本文方法取得 87.3<!--ref:r1--><!--anchor:quote:87.3--> 的成功率,较最强 model-free 基线提升 12.4<!--ref:r2--><!--anchor:quote:12.4--> 个点。
```

`### 数学方法` / `### Loss 亮点解释` stay number-free (from `math_intuition` /
`loss_highlight`), so they make no performance claim and pass the anchor gate.

## 7. G3 seal  [LLM seams #3 + #4 — after both branches]

`rigor_scores(ara_bundle)` returns the 6 `DIMENSION_KEYS`
(`../sub-skills/g3-rigor-reviewer/SKILL.md`):

```
D1_evidence_relevance:4  D2_falsifiability:4  D3_scope_calibration:4
D4_argument_coherence:4  D5_exploration_integrity:3  D6_methodological_rigor:4
```

mean = 3.83, min = 3 → grade **Accept** → `passes_seal2 = true`. `entailment_judge`
confirms C1 (an `improvement` claim) is entailed by experiment E1. Anchor lint passes.
`level2_report.json` is written; the seal holds. (Had the grade been < Weak Accept,
`run_g3` returns a blocked `GateVerdict` carrying a hard-block `SEAL2` finding, and
the bounded `run_with_budget` re-emits, then quarantines.)

## 8. landscapes → cross-paper row

After the batch, `landscapes.py` reads this PAPER.md's headline frontmatter into the
unified table (template: [`../templates/landscape.md`](../templates/landscape.md)):

```
| 论文 | 年份 | 主指标 | 数值 | 参数量(M) | 效率(指标/M) |
| Latent World Models ... | 2024 | success_rate | 87.3 | 42.0 | 2.0786 |
```

efficiency = `round(87.3 / 42.0, 4) = 2.0786`. A PAPER.md missing any headline key
would be silently dropped from this table — which is why step 3's bundle MUST carry them.
