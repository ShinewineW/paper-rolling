# Extending paper-rolling

> **创建日期**: 2026-06-06
> **更新日期**: 2026-06-07
> **适用环境**: `~/Coding/paper-rolling/` 仓库；扩展引擎前阅读；改动后保持 `uv run pytest` 绿 + `uv run ruff check .` 干净。

---

How to add capabilities **within the paper vertical**. Cross-vertical extension
(news, other content domains) is deliberately out of scope until a real second
vertical exists — see [ADR-0002](adr/0002-extend-on-rule-of-three.md).

Two seams are already **abstracted** (adding is a drop-in); the rest are kept
**concrete** on purpose (rule-of-three not yet met) and documented here so you
know exactly what to touch when the time comes. Always: add a regression test
and keep `uv run pytest` green + `uv run ruff check .` clean.

All paths below are under `.claude/skills/paper-landscape/scripts/`.

---

## Add a discovery source — DROP-IN ✅

The fan-out is registry-driven (`discovery/discover.py`, `_SEARCH_SOURCES`).

1. Write `discovery/<name>.py` with a class exposing
   `.search(topic, ...) -> Iterable[candidate-dict]` (copy `discovery/openalex.py`;
   emit the `_INTERFACE_FIELDS` keys + a `discovery_sources` entry).
2. Add a `_run_<name>(source, queries, cfg)` adapter in `discover.py` (copy
   `_run_s2`); it owns the source's per-source search params (date floor, page size).
3. Append `("<key>", _run_<name>)` to `_SEARCH_SOURCES`.
4. Register the source object under `"<key>"` in the production wiring (the SKILL
   Chunk-5 `sources` dict).

`authority.py` / `dedup.py` need no change — scoring is multi-signal OR over the
already-normalized fields. (DBLP is a venue-*enrichment* source, queried per
candidate after dedup — not part of the search fan-out.)

## Add an authority signal — DROP-IN ✅

Edit `discovery/authority.py::score_authority`: compute the new boolean, add it to
the `signals` dict + the composite `score +=` ladder, add any threshold constant.
The any-signal filter in `discover.py` picks it up automatically.

## Add an audit check inside G2 or G3 — DROP-IN ✅

Write a checker returning `GateVerdict` findings (shared vocab in `audit/types.py`)
and `findings.extend(...)` it inside `audit/g2_data_fidelity.py::run_g2` or
`audit/g3_seal.py::run_g3`. Read the ARA tree via `audit/ara_tree.py`
(`find_ara_dir`, `extract_claim_registry`) — do not reach into another gate's
internals.

## Add a model seam (a new injected LLM callable) — SMALL EDIT

1. Define a `*Fn` Protocol in `audit/types.py` (copy `SkepticVoteFn`).
2. Thread the callable through `spoke.py::make_spoke(...)` and
   `run_campaign.py::run_campaign(...)` as an explicit keyword (every seam is a
   parameter — never a module global; see `produce.py::produce_outputs`).
3. Document its contract + the "independent Agent-tool invocation" requirement in
   `SKILL.md` → *Wiring the model seams*.

## Add a cross-paper analysis step — SMALL EDIT

`landscapes.py` is a pure read-side aggregator over `ai_package/*/ara/PAPER.md`.

1. Write `generate_<x>(workspace, topic) -> <X>Result` (copy `generate_landscapes`).
2. Append one call in `hub.py::run_campaign_tick` after `generate_landscapes`, and
   add its result to the `TickResult` dataclass.

**Frontmatter contract (read this):** the cross-paper layer can only aggregate
fields carried in `PAPER.md` frontmatter. A new cross-paper signal therefore needs
*two* hops: the analyzer seam (`resolve_analysis`) must emit it **and**
`output/branch2_ara.py::_paper_md` must mirror it into the frontmatter. Add it in
both places or the aggregator will never see it.

---

## Deferred seams — kept concrete on purpose (ADR-0002)

These are **not** abstracted (rule-of-three not met). Adding one is a local edit
today; extract a framework only when a 3rd real instance arrives.

### Add an ingest tier / converter — LOCAL EDIT (n=2)

`ingest/ingest.py::ingest()` is a hardcoded `Tier-1 → Tier-2 → raise IngestFailed`
try/except chain. To add Tier-3:
1. Write `ingest/tier3_<x>.py` with `run_tier3(...)` + a `Tier3Failed` exception
   (copy `ingest/tier2_mineru.py`).
2. Insert another `try/except` block in `ingest()` after the Tier-2 block, and
   extend the tier-id bookkeeping in `_finalize` (`tier = 1 if pandoc else 2`).

When a 3rd tier lands, consider modelling tiers as an ordered list of
`(name, runner, failure_exc)` and deriving `tier` from the winning index.

### Add an output branch — REQUIRES REFACTOR (n=2)

Only the branch **set** is centralized today (`paths.py::VAULT_BRANCHES` +
`VAULT_BRANCH_PATH_FIELDS`, which the ledger self-heal and watchdog already
iterate). The **producer** is still written for exactly two co-promoted branches.
To add `branch3`:
1. Write `output/branch3_<x>.py::write_branch3(...)`.
2. Add its dir-name + path-field to `paths.py::VAULT_BRANCHES` (the completeness
   checks then cover it automatically).
3. In `output/produce.py::produce_outputs`: stage it, decide its gate ordering,
   and extend the atomic promotion block (currently two-or-neither) to
   N-or-neither; grow `ProduceResult` (currently `person_path`/`ai_path`).
4. Record its path in the ledger row (`store.record` call in `hub.py`).

Before doing this, settle the open questions a 2nd branch can't answer: is the new
branch co-promoted under the same vault key, atomic with the others, and which
gates apply? Those answers are what justify generalizing the promotion loop.
