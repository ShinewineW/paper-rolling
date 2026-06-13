# 0011 — ARA 永不反射式删除;失败现场是单向汇

> **Status**: accepted

No code path may `rm` a generated ARA (the `AI知识库` pack). On **any** failure or
abort, a directory that holds a non-empty ARA is **moved** to `_failed/<key>/`
(gitignored, debug-only, latest-one overwrites the prior) instead of deleted —
via the `failure_scene` snapshot-then-atomic-replace pattern, scene-before-rm. The
`失败现场` is a **one-way sink**: a **gate-failed** ARA flows IN for human debugging
and never flows back OUT to a product, to git history, or to the next generation —
revival of a gate-failed root always re-samples a fresh analyzer, never reusing the
failed ARA.

## Why

The ARA is the **only** token-expensive product (the analyzer runs grounded on
codex/claude over papers that are now very long). Everything else is cheap to
regenerate: `理解阅读`/branch1 is the cheap Qwen writer and is derived from the
ARA; scenes and temp dirs are scratch. Yet several failure/abort paths reflexively
`rm` the staged-but-unpromoted ARA (e.g. `produce_outputs`' `finally` on an
`EngineAbort` when the Qwen audit endpoint drops) or a promoted ARA — burning the
analyzer spend with **no recoverable trace**. Preserving the ARA is for **debugging**
the expensive artifact, NOT for avoiding a re-burn. A gate-failed ARA must never be
reused or served: reuse is a poisoning vector (a `数字门`-failed ARA carries
fabricated numbers), and "不能毒化历史" is the governing constraint.

## Considered options (rejected)

- **L2 — ARA versioning (keep ≥1 past version).** Rejected. It protects the
  already-promoted vault ARA against an overwrite, but cannot save the
  just-built-but-unverified ARA killed by an `EngineAbort` (a first run has no prior
  version, and on a reprocess the "past version" is the *old* ARA, not the freshly
  paid-for one). The lived pain — a Qwen-abort discarding the fresh ARA — is left
  unaddressed by versioning. Scope kept to L1, plus the vault/landscape/publish
  integration cost is avoided.
- **L1+ — reuse the abort/unverified ARA (persist the analysis bundle so revival
  re-renders without re-sampling).** Rejected. Any reuse path is a poisoning
  surface, and reliably classifying "abort/unverified" vs "gate-failed" is itself a
  risk that can misfire. Re-burning a fresh analyzer on revival is accepted as the
  price of a **zero-poisoning** guarantee. Preservation = debug only.

## Boundary (explicitly untouched)

- **ADR-0007's branch1-only reuse stays.** When only the branch1 G3R0 root fails
  (`最终门`: branch1 `report.md` missing; `锚点门` itself retired per ADR-0012 rev),
  the branch2 SSOT it reuses **passed `数字门`+`结构门`** — it is a *good* ARA, not a
  failed one, so reusing it is not "failed-ARA reuse" and is not poisoning. The
  one-way-sink rule applies **only to gate-failed ARAs** (`数字门`/`结构门`, or
  `最终门` rooted in branch2 rigor/entailment).
- **The cost guard is unchanged.** `EngineAbort` still aborts the whole tick (do not
  keep building ARAs that can't be gated when the audit endpoint is down). This
  decision only stops the abort from **losing** the ARA already built.

## Consequences

- A shared discard-or-preserve primitive encodes the **litmus** — *contains a
  non-empty ARA → move to `失败现场`; otherwise → `rm` freely* — plus scene-before-rm
  ordering. The reflex-`rm` sites route through it: `produce_outputs`' `finally`
  (EngineAbort with a built ARA), the **`SpokeCancelled` stall path** (a cancel
  before/during promotion now preserves the built ARA — pre-promotion staging is kept,
  a mid-promotion ARA is moved BACK to `staging/ai` rather than `rm`'d — and the spoke
  scenes it as `最终门`+`report.md` root so revival reuses it; previously this path
  reflex-deleted the ARA, the one documented residual, now closed), the spoke's G3
  re-emit product removal, and `consistency_check`'s orphan prune of `ai_package/`
  (asymmetric — a `person_vault/`
  orphan, an empty/garbage `ai_package/` orphan, `.clones`, and atomic-write temp
  files are still hard-deleted: "该删的不受影响"). An ARA-bearing orphan is moved to
  `_failed/_orphans/<name>/` (latest-one wins) — a new, gitignored layout slot.
- `_failed/<key>/` holds at most one (latest) scene per paper — bounded, gitignored,
  machine-local.
- Separate, out-of-scope follow-up: scenes currently pass `analysis=None`, which may
  blunt ADR-0007's intended branch1-rooted reuse (forcing a re-sample). To verify
  independently — NOT part of this delete-safety change.
