# 0007 — Surgical re-emit: re-run only the failed branch, reuse upstream products

> **Status**: accepted
> **修订**: 2026-06-09 — 粒度定为 **branch 级**(非 section 级,见 ADR-0009 修订)。

A gate re-emit (and a 复活赛 replay) re-runs **only the branch that failed**,
reusing the already-passed upstream stage-products verbatim — it does NOT re-run
the whole spoke. Today `_attempt()` bundles branch2 → G2 → branch1 in one call,
so `on_reemit=lambda i: _attempt()` regenerates everything on a G3 failure. That
is rejected.

## Why

The dominant failure (G3 seal, 7/13 papers) is rooted in **branch1** (the writer
puts numbers in prose), yet a coarse re-emit also regenerates **branch2** — whose
SSOT pack already passed G2 and is fine. Two harms:

1. **Wasted tokens** — branch2 on a dense paper is the expensive half; re-running
   a good SSOT burns budget for nothing. Token thrift is a primary project value.
2. **Re-rolling a passed gate** — regenerating branch2 produces new numbers, so
   G2 is re-judged; a clean SSOT can newly *fail* G2, turning "only G3 failed"
   into "now G2 fails too." This contradicts ADR-0006's "G2 is never re-rolled
   without cause."

## Mechanism

Each stage stages its output to a stable per-key location. A re-emit reads the
upstream stages' staged outputs and re-runs only the failed **branch** (all of it):

- 最终门 root in branch1 (anchor) → re-run **branch1** (whole report, with G3
  feedback), reuse the staged branch2 SSOT.
- 最终门 root in branch2 (rigor/entailment) → re-run **branch2** (re-call the
  analyzer with feedback) + downstream branch1.
- 数字门 (G2) → re-run **branch2 blind** = re-call `resolve_analysis` (a fresh
  analyzer sample — NOT just the deterministic `write_branch2` renderer, which
  would reproduce the same bad numbers byte-for-byte; ADR-0006). branch1 hadn't run.

This is the SAME capability as the 失败现场 / 复活赛: "reuse passed stages, re-run
only the failed branch." Same-run re-emit and next-day post-fix replay share one
implementation — stage-product reuse is a first-class primitive, not duplicated.

## The scene is self-contained (revival input completeness)

`run_g3` needs `person_path / ai_path / md_path / content_list_path`; re-running
branch2 needs `candidate + analysis`. None can be reconstructed from a bare
`_failed/<key>/`. So the **scene persists every revival input**: `candidate` dict,
absolute `md_path`, `ledger_key` (= the `_candidate_key`, a DIFFERENT namespace
from the vault `key`), the analyzer bundle (`analysis`, so revival reuses it
instead of re-running the analyzer when the failed branch is downstream), and a
**copy of `content_list.json` into the scene** (it is gitignored/local, so a
pointer alone is lost). `engine_commit` is recorded as **diagnostic metadata
only** (which engine version the paper failed under, for human triage).

**Reuse is unconditional — forward-only, no staleness re-run.** An earlier draft
had revival compare `engine_commit` and re-run branch2 on any mismatch. That is
rejected: the engine changes on every commit, and an already-PASSED product is
never retroactively regenerated when the engine moves on (基调-D2 governs the
whole repo this way — tracked products are forward-compatible, not re-derived).
So revival reuses the scene's upstream passed products **as-is** and re-runs only
the failed branch with the current engine. (To apply an improved analyzer to an
already-passed SSOT, *re-process* the paper — `invalidate` + a normal `/loop`
tick — which is a different operation from 复活赛.)

## Consequence

`_attempt()` must be decomposed so branch2 and branch1 are independently
re-runnable, with branch2's staged product persisted (surviving a failure, so the
scene/revival can reuse it). The 复活赛 driver is a **second legitimate ledger
writer** besides the hub: it MUST take the LS-1 lock (`Ledger(workspace).acquire()`)
so it is mutually exclusive with a running `/loop` tick, and it writes status back
to the **original `ledger_key` row** (not the vault key) so a revived paper's
`deferred` row actually flips to `done`.
