# 0006 — Gate-retry feedback boundary: content gates adapt, G2 stays blind

> **Status**: accepted

When a paper fails a gate, the bounded re-emit (`max_gate_rounds`) becomes a
real correction loop instead of today's blind re-run (`on_reemit=lambda i:
_attempt()`, which discards the round index and re-runs with identical input).
The gate's structured `GateVerdict.hard_findings` (target + observation) is
threaded back into the regenerating seam's prompt — **but only for content
gates**. G2 (number-fidelity) is deliberately excluded from feedback and gets a
**blind** retry only.

## Why the split

- **Content gates** (G3 anchor/equation/entailment, the branch1 忠实门 — ADR-0012,
  formerly the unanchored-claim gate) fail on *how a true thing is expressed* —
  e.g. (pre-ADR-0012) a claim with no `<!--ref-->`; the 忠实门 now instead flags an
  ungrounded prose number or a misattribution. These are un-gameable: feeding
  the finding back ("anchor this claim or cut it") lets the **generator** of the
  failed branch self-correct, and the auditor re-verifies independently. The fix
  *is* the goal. (The feedback **target** is dispatched by root, per ADR-0009:
  anchor → branch1 writer; rigor/entailment → branch2 analyzer. The same
  bounded-rounds Goodhart guard applies to both.)
- **G2** fails on *whether a number is real* — present in the source MD or not.
  Feeding the verdict back leaks the answer: the skeptic's failure record names
  the near-value ("113.9 absent; source has 119.5"), so a feedback retry would
  hand the generator the target and it would simply write 119.5 to pass. We
  could not distinguish a genuine re-derivation from laundering a fabrication.
  That collapses G2 — the knowledge base's anti-poisoning firewall — from inside.

## What G2 gets instead

A **blind** retry: re-run branch2 fresh, skeptic re-checks independently, no
near-value hint. Sampling-variance hallucinations self-heal; the isolation
invariant (skeptic sees only candidate numbers + source MD, never the answer)
is preserved. On budget exhaustion → `_failed/<key>/` scene. Persistent G2
failure points at a deeper root the analyzer cannot fix — garbled MinerU
extraction (→ re-ingest) or a value that lives only in a figure — which the
scene records for human/next-round triage.

## Consequences

- `on_reemit` signature must carry the verdict (today it is `Callable[[int],
  None]`); `_attempt` must accept feedback findings; content seams must accept
  and incorporate them.
- Feeding findings back is bounded by `max_gate_rounds` precisely because each
  round is another draw against a probabilistic auditor — too many rounds erode
  the gate via repeated sampling. Keep the budget small.
- Only `Finding.observation` (the symptom) is ever fed back — never the private
  rigor rubric / scoring prompt, preserving "the G3 rigor rubric is held
  privately by the seam."
