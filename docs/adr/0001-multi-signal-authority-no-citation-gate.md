# 1. Multi-signal OR authority, no citation hard gate

- Status: Accepted — back-filled 2026-06-06 to resolve the in-code `ADR-0001`
  references (`scripts/discovery/authority.py`). The decision itself predates
  this file; its full rationale lives in
  `docs/specs/2026-06-05-paper-landscape-v2-impl.md` (skills_workspace).

## Context

Discovery must surface the *latest* authoritative work — including recent
preprints and high-impact papers that have not yet accumulated citations. An
earlier design gated candidates on a citation floor (`>= 500`), which
structurally excludes new work and over-weights age.

## Decision

No citation hard gate. A candidate is authoritative if it fires **any** of four
OR-combined signals (`scripts/discovery/authority.py`):

- **S1** citation count or citation velocity (cites/age),
- **S2** top-venue match (DBLP-confirmable),
- **S3** whitelisted authoring institution,
- **S4** heat (GitHub stars / HF upvotes).

A composite, recency-weighted score then ranks the survivors. Citation count is
one signal among four, never a floor.

## Consequences

- A 0-citation paper from a whitelisted lab (S3) or a hot repo (S4) survives;
  a stale high-cite paper is not auto-privileged beyond the signal it fires.
- Quality control moves **downstream** (over-fetch + dedup + the G2/G3 audit
  gates), not to a discovery-time citation cutoff.
- Whitelists and thresholds are tunable via campaign config; the AD/robotics
  whitelist extra is gated by `is_ad_domain` (see `authority.py`).
