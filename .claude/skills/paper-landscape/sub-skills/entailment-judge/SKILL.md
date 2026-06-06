---
name: entailment-judge
description: The type-aware claim<->evidence entailment judge backing the entailment_judge seam in G3 (吸收-D8).
---

# entailment-judge (entailment_judge seam role)

This sub-skill is the **independent sub-agent** that backs the `entailment_judge`
seam — one of the 4 LLM seams injected into `run_campaign(...)`. It is consumed
**only by G3** (`scripts/audit/g3_seal.py::run_g3`, part (b) type-aware
entailment) via `scripts/audit/entailment.py::check_entailment`.

Per the engine's seam discipline, **each call is a fresh, independent Agent-tool
invocation** so the audit verdict stays uncorrelated with the branch2 generator
(`resolve_analysis`) that wrote the claims and experiments. See sibling
`../analyze-paper/SKILL.md` for that generator.

## Contract

Protocol `EntailmentJudgeFn` (`scripts/audit/types.py`):

```python
def entailment_judge(claim: ClaimRecord, experiment_text: str) -> tuple[bool, str]:
    ...   # (entailed, reason)
```

- `claim` is a `ClaimRecord` (`scripts/audit/types.py`): `claim_id`, `statement`,
  `claim_type: ClaimType`, `numbers`, `proof_experiment_ids`.
- `experiment_text` is the section text of ONE linked experiment, parsed from
  `logic/experiments.md` by `g3_seal._parse_experiments` (keyed on the `## E\d{2,}:`
  header). The judge only ever sees a single claim + a single experiment's text.
- Return `(entailed, reason)`. When `entailed is False`, `reason` is surfaced into
  `Finding.reasoning` (`check_entailment` falls back to `"experiment design does not
  match claim type"` only if `reason` is empty).

`check_entailment` calls the judge per `(claim, exp_id)` pair, **skipping claims
with no `proof_experiment_ids`** (a coverage matter, not entailment) and **skipping
`ClaimType.UNKNOWN`** (no design requirement). A dangling `exp_id` not present in
`experiments.md` is hard-blocked *before* the judge runs (`EN..`, MAJOR).

## Type-aware bar (吸收-D8)

The judge's strictness is calibrated by `claim.claim_type`. The required experiment
design per type is the table in `scripts/audit/entailment.py::REQUIRED_DESIGN`
(exposed via `required_design_for`):

| ClaimType        | required design                  |
|------------------|----------------------------------|
| `causal`         | `ablation` (isolating)           |
| `generalization` | `heterogeneous test conditions`  |
| `improvement`    | `baseline`                       |
| `descriptive`    | `representative sampling`        |
| `scoping`        | `declared bounds`                |
| `unknown`        | — (no requirement; not judged)   |

The judge must verify the linked experiment **exhibits the design its claim type
demands** — a `causal` claim needs an isolating ablation (a stronger bar) before
it entails, whereas a `descriptive` claim only needs representative sampling. The
6 values are exactly `ClaimType` in `scripts/audit/types.py`.

## Verdict mechanics

When the judge returns `entailed=False`, `check_entailment` emits a
`Finding(severity=Severity.MAJOR, is_hard_block=True)` with id `EN{nn}` targeting
`logic/claims.md:{claim_id}`. A hard-block finding makes the `GateVerdict.blocked`,
which makes the HUB re-emit the offending branch under the bounded retry owned by
`scripts/audit/gate_runner.run_with_budget`.

## Ground-truth isolation

The required-design rubric is the seam's **private** knowledge — it lives in the
judge's prompt, never in any generator prompt (mirrors `RigorScoreFn` /
`SkepticVoteFn` isolation in `scripts/audit/types.py`).

## Relation to C4 (`empirical_classifier`)

`run_g3` also accepts an optional `empirical_classifier: Callable[[str], bool]`
(ROADMAP C4), which is a **separate** seam feeding the branch1 anchor check's
empirical-sentence detection in `scripts/audit/anchor_resolution.py::check_branch1_md_anchors`
(defaulting to the `_is_empirical_performance` metric-cue heuristic). That C4 slot
is where a trained NLI / factual-consistency classifier plugs in. `entailment_judge`
is the distinct **LLM/heuristic entailment path** over claims↔experiments — do not
conflate the two.
