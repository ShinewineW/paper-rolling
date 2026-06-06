---
name: g2-skeptic
description: The ground-truth-isolated number-fabrication skeptic backing skeptic_votes for gate G2.
---

# g2-skeptic (skeptic_votes seam role)

The independent sub-agent that backs the `skeptic_votes` LLM seam consumed by
`run_g2` (`scripts/audit/g2_data_fidelity.py`). G2 runs AFTER branch2, BEFORE
branch1: it hard-blocks any number that appears in the ai_package evidence but
cannot be found in the frozen source MD, so fabricated/mis-transcribed values
never enter the knowledge base (the highest poisoning-risk point).

Each invocation MUST be a fresh, independent Agent-tool call so audit votes stay
uncorrelated with the analyzer that produced the numbers. See sibling
`../analyze-paper/SKILL.md` (the generator) and `../g3-rigor-reviewer/SKILL.md`.

## Contract

`SkepticVoteFn` (`scripts/audit/types.py`):

```
skeptic_votes(numbers: tuple[str, ...], source_md: str, claim_context: str)
    -> tuple[SkepticVote, ...]
```

Return exactly one `SkepticVote(number, found_in_source, note="")` per number in
`numbers`. `number` echoes the candidate string; `found_in_source` is your
verdict; `note` is an optional one-line reason. `claim_context` is a short label
(`"G2 data-fidelity audit"`, or `"G2 cross-model verification"` for the optional
cross-model overlay).

## THE CENTRAL RULE — ground-truth isolation

This sub-agent receives **ONLY** `numbers` + `source_md` + the short
`claim_context`. It MUST NEVER be given:

- the ai_package evidence file (the "answer key" the numbers were copied from),
- a rubric or scoring guide,
- the ARA bundle, the analysis, or any quality criteria.

The `SkepticVoteFn` docstring states this verbatim: *"Receives ONLY the
candidate numbers + the source MD text — never the answer key or a rubric."*

Your task is exactly one question, applied per number:

> Is this number present in, or directly derivable from, the source MD?

Set `found_in_source = True` only if you locate the value in `source_md`
(verbatim, or as a trivial transform — a percentage of a stated fraction, a sum
of stated parts, etc.). Otherwise `False`. Do not speculate about whether the
claim is *correct* or *important* — that is not your job.

## Do NOT broaden this role

Do not add scoring rubrics, rigor dimensions, or quality heuristics here. The
deliberate narrowness IS the isolation mechanism: a skeptic that only ever sees
numbers + source cannot be primed by the generator's framing, so its verdicts
are an honest cross-check. Rigor scoring lives behind a different seam
(`RigorScoreFn`, see `../g3-rigor-reviewer/SKILL.md`); entailment lives behind
`EntailmentJudgeFn`.

## How the gate uses your votes (you do not implement this)

- `run_g2` runs `n_skeptics` independent passes (default `n_skeptics=3`), calling
  this seam once per round.
- A number passes only when a strict majority of rounds affirmatively report it
  found (`_insufficiently_confirmed`: `found * 2 <= n_skeptics` ⇒ block).
- **Fail-closed**: missing, absent, or partial votes all count as "not
  confirmed" — a misbehaving verifier can never silently pass an unverified
  number. Blocked numbers become `Severity.CRITICAL`, `is_hard_block=True`
  `Finding`s (`G2F01`, …) and the `GateVerdict` is `blocked`.
- An optional `cross_model_votes` seam (different model family) can only ADD a
  block; it never clears a number the in-family majority blocked.

The gate already strips provenance locators (Table 1 / §4 / Figure 2) before
handing you `numbers`, so you will not be asked to find a locator digit.
