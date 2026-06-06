# 2. Extend on rule-of-three; abstract the discovery-source seam, defer tier/branch frameworks

- Status: Accepted — 2026-06-06

## Context

paper-rolling is a publication-grade baseline meant to be extended *within the
paper vertical* — new discovery source, ingest tier, audit gate, output branch,
or cross-paper analysis. Cross-vertical use (news, other content domains) is
explicitly **deferred** until a real second vertical exists: abstracting a
generic engine-core/vertical split on `n = 1` would bake in the wrong seam.

Within the paper vertical there is a standing tension: extract reusable seams
early (or the foundation ossifies — 尾大不掉) vs. over-abstracting on too few
instances (and abstracting the wrong shape).

## Decision

Extract a reusable seam **now** only when **both** hold:
1. its shape is proven by **>= 3 real instances**, and
2. retrofitting it later would be **cross-file / expensive**.

Applying the rule:

- **EXTRACT now**
  - the **discovery-source seam** — 4 real sources (OpenAlex/S2/arXiv/HF) with
    divergent adapters; proven shape, and retrofitting touches `discover()`
    every time a source is added.
  - the **shared ara-tree read helper** — `_find_ara_dir` / `extract_claim_registry`
    are already shared across G2 and G3 (G3 imported G2's private symbol).
  - the **vault-branch set** — centralized so the person↔ai pairing is no longer
    hardcoded across `produce` / `paths` / `hub` / `ledger`.
- **DEFER (document the seam, do not abstract)**
  - the **ingest tier sequence** — `n = 2` (pandoc, MinerU); a 3rd tier is one
    local insertion in `ingest()`, not cross-file.
  - the **full output-branch writer/gating framework** — `n = 2`; a 3rd branch's
    shape (keying, atomic co-promotion, which gates apply) is unknown, so the
    producer's staging/promotion stays concrete. Only the branch *set* (above)
    is centralized.
  - the **cross-paper analysis framework** — `n = 1` (only landscapes).

## Consequences

- **Intentional asymmetry**: discovery sources sit behind a `Source` seam, but
  ingest tiers and output branches stay concrete. A future maintainer who finds
  this asymmetry should read this ADR before "fixing" it.
- `docs/EXTENDING.md` documents how to open each deferred seam when its
  rule-of-three threshold is reached.
- The cross-vertical engine-core/vertical split is out of scope until a concrete
  second vertical (e.g. news) actually lands.
