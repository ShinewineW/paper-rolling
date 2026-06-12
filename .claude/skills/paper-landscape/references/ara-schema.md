# ARA bundle schema — the `resolve_analysis` output contract

The single `dict` that `resolve_analysis(md_path, candidate) -> dict` (the analyzer
LLM seam) MUST return. It is the **Agent-Native Research Artifact (ARA)** bundle:
`scripts/output/branch2_ara.py` writes it into `ai_package/{key}/ara/`,
`scripts/output/branch1_report.py` derives the human report from the same dict, and
`scripts/landscapes.py` reads the resulting `PAPER.md` frontmatter for the cross-paper
table. The directory layout it compiles into (PAPER.md + `logic/`, `src/`, `trace/`,
`evidence/`) is the upstream ARA schema — read
`../../../../docs/reference/AI-Research-SKILLs/22-agent-native-research-artifact/compiler/references/ara-schema.md`
for the field-level layer reference this skill aligns its terminology to.

Provider-agnostic: the host agent supplies this seam as a fresh Agent-tool sub-agent
per paper (see the engine entrypoint `scripts/run_campaign.py`).

## Keys actually consumed by the code

Grounded in `branch2_ara.py` and `branch1_report.py`. **Required** keys are accessed
with `analysis["..."]` (a missing key raises `KeyError` and fails the spoke);
**optional** keys are accessed with `analysis.get("...")` and have a built-in fallback.

### Required — `analysis["..."]`

| Key | Type | Consumed by → ARA file |
|-----|------|------------------------|
| `overview` | str | branch2 → `PAPER.md` `## Overview` |
| `problem` | (structured) | branch2 → `logic/problem.md` |
| `claims` | list[dict] | branch2 → `logic/claims.md`; each `claim["statement"]` |
| `concepts` | list[dict] | branch2 → `logic/concepts.md`; each `concept["name"]` |
| `experiments` | list[dict] | branch2 → `logic/experiments.md` |
| `related_work` | list[dict] | branch2 → `logic/related_work.md` |
| `architecture` | str | branch2 → `logic/solution/architecture.md`; branch1 mermaid |
| `algorithm` | str | branch2 → `logic/solution/algorithm.md`; branch1 `$$…$$` extract |
| `constraints` | str | branch2 → `logic/solution/constraints.md` |
| `heuristics` | list[dict] | branch2 → `logic/solution/heuristics.md` |
| `configs_training` | (structured) | branch2 → `src/configs/training.md` |
| `configs_model` | (structured) | branch2 → `src/configs/model.md` |
| `environment` | (structured) | branch2 → `src/environment.md` |
| `execution_stub` | str | branch2 → `src/execution/core.py` |
| `exploration_tree` | (YAML-able) | branch2 → `trace/exploration_tree.yaml` (`{"tree": …}`) |
| `evidence_tables` | list[dict] | branch2 → `evidence/tables/*` + `evidence/README.md`; each table needs `name`, `headers`, `rows`, `caption`, `source` (+ `claims` for the README index) |
| `innovations` | list[dict] | branch2 → code-ref; each needs `name` + `grep` |

### Optional — `analysis.get("...")` (fallback if absent)

| Key | Consumed by |
|-----|-------------|
| `domain` | branch2 frontmatter (`default "deep learning"`) |
| `math_intuition`, `math_toy_example` | branch1 math section |
| `loss_highlight` | branch1; sub-keys `direction`, `mechanism`, `baseline` |
| `trend` | branch1 trend section |

## Mandatory headline keys (HARD requirement)

```
headline_metric : str    # e.g. "NDS"
headline_value  : float
params_million  : float
```

These three are required `analysis["..."]` accesses in `branch2_ara.py` and are
written into the `PAPER.md` YAML frontmatter. `landscapes.py` checks
`_HEADLINE_KEYS = ("key", "headline_metric", "headline_value", "params_million")` via
`_has_headline_frontmatter`: a `PAPER.md` missing **any** of them is silently dropped
from the cross-paper landscape table (`landscapes/{topic}/INDEX.md` + `report.md`) —
the entry still lives in the vault, it just has no metric row. Emit them always.

## Fidelity rule — exact numbers ONLY under `evidence/`

Per the upstream ARA schema: `logic/experiments.md` carries declarative plans with
**directional/relative** expected outcomes only — never exact numbers. All exact cell
values live under `evidence_tables` → `evidence/tables/*`. This is what the G2
data-fidelity gate (`scripts/audit/g2_data_fidelity.py`) enforces with the
ground-truth-isolated `skeptic_votes` seam: numbers in the ARA bundle that are not
found in the source MD are hard-blocked as fabrication before promotion.

## See also

- [wiring-the-seams.md](./wiring-the-seams.md) — the five LLM seams (analyzer
  `resolve_analysis`, the G2 skeptic `skeptic_votes` over the numbers in this
  bundle, `rigor_scores` over the 6 `DIMENSION_KEYS`, `entailment_judge`, and the
  branch1 忠实门 `faithfulness_judge`).
- `../sub-skills/g2-skeptic/SKILL.md` — the skeptic gate over the numbers in this bundle.
- `../sub-skills/g3-rigor-reviewer/SKILL.md` — `rigor_scores` reads this same bundle over the 6 `DIMENSION_KEYS`.
- Engine composition + the injected seams: `../SKILL.md` and `wiring-the-seams.md`.

LICENSE: CC-BY-NC 4.0 (research-only).
