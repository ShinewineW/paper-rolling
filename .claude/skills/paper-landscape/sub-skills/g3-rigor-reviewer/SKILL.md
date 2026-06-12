---
name: g3-rigor-reviewer
description: The 6-dimension rigor reviewer backing the rigor_scores seam for the G3 ARA Seal Level 2.
---

# g3-rigor-reviewer (rigor_scores seam role)

The independent sub-agent backing the **`rigor_scores`** seam (`RigorScoreFn`,
`scripts/audit/types.py`). It is the *cognitive terminal seal* — Seal Level 2 of
the ARA — and **owns the private rubric** below. It is one of the 5 LLM seams
injected into `run_campaign`; see `../../scripts/run_campaign.py`.

## Contract

```
rigor_scores(ara_bundle: dict[str, str]) -> {
  "dimensions": { dim_key: {
      "score": int 1-5, "strengths":[...], "weaknesses":[...], "suggestions":[...]
  } },
  "findings": [...]
}
```

- `ara_bundle` is assembled by `g3_seal._load_ara_bundle` in fixed order:
  `PAPER.md`, `logic/claims.md`, `logic/experiments.md`, `logic/problem.md`,
  `logic/concepts.md`, `logic/solution/architecture.md`,
  `trace/exploration_tree.yaml`, `evidence/README.md` (missing files are dropped).
- You MUST return a `"score"` (int 1-5) for **all six** `DIMENSION_KEYS`
  (`scripts/audit/rigor_rubric.py`): `D1_evidence_relevance`,
  `D2_falsifiability`, `D3_scope_calibration`, `D4_argument_coherence`,
  `D5_exploration_integrity`, `D6_methodological_rigor`. `score_rigor` reads
  `dimensions[k]["score"]` for each key — a missing key is a hard error.
- `findings` are advisory notes; `score_rigor` copies them verbatim into
  `level2_report.json`. They are NOT the block lever — the **grade** is.

## How the score becomes a block

`score_rigor` → `compute_grade(scores)` (grade map below) → sets
`overall.passes_seal2 = grade in {"Strong Accept","Accept","Weak Accept"}`.
`run_g3` always writes `<ara>/level2_report.json` (the grade IS the evidence),
then if `not passes_seal2` raises the hard-block finding `SEAL2`
(`Severity.CRITICAL`). Hub re-emits branch2 under `gate_runner.run_with_budget`.

```
Strong Accept | mean >= 4.5 AND no dimension < 3
Accept        | mean >= 3.8 AND no dimension < 2
Weak Accept   | mean >= 3.0 AND no dimension < 2
Weak Reject   | mean >= 2.0 AND (mean < 3.0 OR any dimension < 2)
Reject        | mean < 2.0 OR any dimension = 1
```

## PRIVATE-RUBRIC rule [MUST]

This rubric is **ground-truth isolated**: it MUST NEVER appear in any
generator/analyzer prompt (`resolve_analysis`, `query_expand`, branch1/branch2
authoring). If the generator knows the scoring anchors it games them. The
rubric lives ONLY here, held privately by this seam. Each `rigor_scores` call
is a **fresh, independent Agent-tool invocation** — uncorrelated with the
generator that produced the bundle.

## The 6 dimensions (private rubric — semantic checks, read the whole bundle)

- **D1_evidence_relevance** — Does cited evidence support each claim *in
  substance*? Type-aware entailment (causal→ablation, generalization→
  heterogeneous, improvement→baseline, descriptive→sampling, scoping→bounds);
  evidence sufficiency. 5 = type-appropriate for every claim; 1 = majority cite
  irrelevant experiments.
- **D2_falsifiability** — Are criteria actionable, non-trivial, scope-matched,
  independently testable? 5 = specific + actionable + matches scope for every
  claim; 1 = meaningless criteria across claims.
- **D3_scope_calibration** — Claims assert exactly what evidence supports.
  Over-claiming (critical if extreme), under-claiming, assumption explicitness,
  generalization boundaries, qualifier consistency. 5 = precise scope +
  explicit assumptions + stated limits; 1 = pervasive scope mismatch.
- **D4_argument_coherence** — Coherent arc observations→gaps→insight→solution→
  claims→evidence; cross-layer consistency; every gap addressed. 5 = clear arc,
  all gaps addressed; 1 = layers tell different stories.
- **D5_exploration_integrity** — `exploration_tree.yaml` faithful: concrete
  dead-ends, real decision rationale, no claim advocating a dead_end/pivot
  (critical), genuine negatives not post-hoc. 5 = rich tree + genuine negatives;
  1 = tree contradicts claims / pure post-hoc.
- **D6_methodological_rigor** — Baseline adequacy, ablation coverage,
  statistical reporting, metric-claim alignment, reproducibility signals. 5 =
  comprehensive baselines + ablations + statistical rigor; 1 = no baselines, no
  ablations, metrics don't match claims.

Per-dimension Checks tables, scoring anchors 2–4, and `Severity` definitions
(`critical`/`major`/`minor`/`suggestion`) — see the credited source below; match
its semantics exactly.

## Relation to siblings

- `D1_evidence_relevance` overlaps the standalone **type-aware entailment** check
  in `run_g3` (the `entailment_judge` seam, `../entailment-judge/SKILL.md`) —
  here it is one rigor score; there it is a per-claim hard check.
- Number fabrication is NOT this seam's job: that is G2's skeptic seam
  (`../g2-skeptic/SKILL.md`), run BEFORE branch1.

## Credit

Dimension semantics, scoring anchors, grade map, and severity taxonomy ported
(MIT) from
`../../../../../docs/reference/AI-Research-SKILLs/22-agent-native-research-artifact/rigor-reviewer/references/review-dimensions.md`.
Read it to align the dimension semantics before scoring.
