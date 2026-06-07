# Discovery & authority model

The discovery layer turns a campaign topic into a ranked list of authoritative
candidates. Entry point: `discover(campaign_config, sources, llm)` in
`scripts/discovery/discover.py`. It returns plain candidate dicts (see the
`_INTERFACE_FIELDS` projection); no LLM analysis happens here — discovery is
NOT one of the four LLM audit seams (see `../SKILL.md`). The one LLM call inside
discovery is the query-expansion seam `llm` threaded into
`scripts.discovery.query_expand.expand_queries(topic, llm=...)`.

## Pipeline (discover body)

1. **Query expansion** — `expand_queries(topic, llm=llm)`, then a second round
   seeded from any `ai_keywords` harvested off HF candidates
   (`expand_queries(topic, llm=llm, ai_keywords=...)`); the extra queries fan
   only into OpenAlex via `_run_openalex`.
2. **Fan across sources** — iterate `_SEARCH_SOURCES` (below). Each source call
   is wrapped in `_safe_source`: a source raising `HttpUnavailable` is treated
   as MISSING (returns `[]`), never fatal — one source down must not abort the
   tick.
3. **Dedup** — `dedup_candidates(raw)` (see [Dedup](#dedup)).
4. **DBLP venue enrichment** — for merged candidates with no `venue`, query
   `dblp.venue_for_title(title)`; a confirmed venue lets the S2 signal fire.
   DBLP is intentionally NOT in `_SEARCH_SOURCES` (per-candidate enrichment, not
   query fan-out).
5. **Retraction drop + authority filter** — drop `cand.get("is_retracted")`,
   then `score_authority`; drop when `not any(signals.values())`.
6. **Rank + over-pull** — sort by `authority_score` descending, cap at
   `top_k * overfetch_factor` (`overfetch_factor` default `3`).

## ADR-0001: multi-signal OR, no citation gate

See `../../../../docs/adr/0001-multi-signal-authority-no-citation-gate.md`.

There is **no citation hard floor**. The earlier design gated on `cited_by_count
>= 500`, which structurally excludes the *latest* work and over-weights age.
ADR-0001 supersedes it: a candidate is authoritative if it fires **any** of four
OR-combined signals, scored by `score_authority` in
`scripts/discovery/authority.py`:

- **S1 cite** (`s1_cite`): `cites >= _S1_CITE_FLOOR` (1000) **or** velocity
  `>= _S1_VELOCITY_FLOOR` (100.0 cites/year). `_velocity = cites / max(age, 1)`.
- **S2 venue** (`s2_venue`): `candidate["venue"]` matches the venue allowlist
  (substring, case-insensitive; DBLP-confirmable).
- **S3 institution** (`s3_institution`): any `candidate["institutions"]` entry
  matches the institution whitelist.
- **S4 heat** (`s4_heat`): `github_stars >= _S4_STARS_FLOOR` (300) **or**
  `upvotes >= _S4_UPVOTES_FLOOR` (50).

Composite score: S1 +3.0, S2 +2.5, S3 +2.0, S4 +1.5, plus a capped velocity
bonus `min(velocity / 100.0, 3.0)`, then a recency multiplier
`1.0 + max(0, year - (current_year - 5)) * 0.05` so the latest authoritative
work is not buried under classics. **Why no gate:** citation count is one signal
among four — a 0-citation paper from a whitelisted lab (S3) or a hot repo (S4)
survives. Quality control moves downstream (over-pull + dedup + the G2/G3 audit
gates), not to a discovery-time cutoff.

## Authority whitelists (`is_ad_domain`)

`score_authority(candidate, config)` selects whitelists from
`config["is_ad_domain"]` (**defaults to `True`** when absent, preserving the
historical behaviour):

- **GENERAL always applied** — `GENERAL_VENUE_ALLOWLIST` (NeurIPS, ICML, ICLR,
  CVPR, ICCV, ECCV, AAAI, TPAMI, IJCV) and `GENERAL_INSTITUTION_WHITELIST`
  (Google, DeepMind, Meta, FAIR, NVIDIA, OpenAI, …).
- **AD/robotics extra only when `is_ad_domain`** — `AD_VENUE_ALLOWLIST` (ICRA,
  IROS, CoRL, RSS, RA-L, T-RO) and `AD_INSTITUTION_WHITELIST` (Waymo, Tesla,
  Wayve, …).
- `DEFAULT_VENUE_ALLOWLIST = GENERAL_VENUE_ALLOWLIST + AD_VENUE_ALLOWLIST`;
  likewise `DEFAULT_INSTITUTION_WHITELIST`. The DEFAULT (general+AD) set is the
  one used when `is_ad_domain` is true.
- An explicit `config["venue_allowlist"]` / `config["institution_whitelist"]`
  overrides outright (selected before the GENERAL/AD logic runs).

## Retraction (ROADMAP B1)

`OpenAlexSource._to_candidate` sets `"is_retracted": bool(work.get(
"is_retracted", False))` from the OpenAlex `/works` flag. `dedup.py` keeps it in
`_FIRST_FIELDS` so a retraction from any source survives merge (first-non-falsy
wins). `discover` then skips any candidate with a truthy `is_retracted`.

## Dedup

`dedup_candidates` (`scripts/discovery/dedup.py`) runs two passes:

1. **Exact-key folding** — key = `_doi_key` (`doi:<lower>`) else `_arxiv_key`
   (`arxiv:<id><version>`); same key → `merge_pair`.
2. **Title-similarity consolidation** — over keyed survivors + keyless records,
   merge when `_keys_compatible(a, b)` **and** `_titles_match(a, b)`. This
   catches the DOI-only (OpenAlex) ⨉ arXiv-only record of the same paper that
   never collide in pass 1 (different key types).

`_keys_compatible` returns `True` unless the two records carry a *conflicting
same-type* hard identifier — two different DOIs, or two different
**versioned** arxiv ids (`arxiv_id + arxiv_version`) — so v1 and v2 stay
distinct. `_titles_match` uses `similarity` from `scripts.discovery._text` with
a `+0.05` same-year bonus against `THRESHOLD`. `merge_pair` is best-of-each:
`_MAX_FIELDS` (cited_by_count, influential_citation_count, github_stars,
upvotes) keep the larger value; `_FIRST_FIELDS` take the first non-null; list
fields (institutions, ai_keywords, discovery_sources) union order-stable.

## Over-pull (why 2–3×N)

`N` is the count of *successfully processed* papers, and downstream stages
(ingest, gates) can drop candidates. `discover` returns up to
`top_k * overfetch_factor` so failures backfill from spares rather than starving
the tick.

## `_SEARCH_SOURCES` registry — adding a source

`_SEARCH_SOURCES` is an extensible tuple of `(key, adapter)` (ADR-0002). `discover`
fans expanded queries across it in order; each `_run_<name>(source, queries,
cfg)` adapter owns its source's search params (date floor, page size), keeping
`discover`'s body source-agnostic. Current entries: `openalex`, `s2`, `arxiv`,
`hf_papers`. To add a source (drop-in, no `discover`-body edit):

1. Write a source class exposing `.search(topic, ...) -> Iterable[dict]`.
2. Add a `_run_<name>(source, queries, cfg)` adapter.
3. Append `("<key>", _run_<name>)` to `_SEARCH_SOURCES`; `<key>` is the dict key
   production wiring registers the source under in `sources`.

See `docs/guides/EXTENDING.md`. The OpenAlex `/works` recipe (default.search,
`cursor=*` deep pagination, `cited_by_count:>{min_cites-1}` as page-breadth-only,
not a gate) is documented in `OpenAlexSource.search`.

## Force-include (中枢-D1): mandatory papers

`campaign_config["force_include"]` is a list of papers the user requires regardless
of discovery. Each entry is validated at the Hard Gate (`campaign._validate_force_include`)
on **two axes** — it must carry (1) an *ingestible source* the engine can fetch
(`arxiv_id` or `oa_pdf_url`; a bare `doi` is rejected — there is no DOI→PDF resolver)
and (2) a *distinct identity* (`arxiv_id` / `doi` / `title`; an `oa_pdf_url`-only
entry must add a `title` so two entries can't collapse into one corpus dir / ledger
key). `_build_forced` projects each (marking `forced=True` +
`discovery_sources=["forced"]`; a title-less entry falls back to a *unique* id —
`arxiv_id` → `doi` → `oa_pdf_url` — never a shared sentinel) and `discover()`
**prepends** them to the pool, **bypassing the authority any-signal filter** —
force-include is mandatory, not signal-authoritative.

They are deduped against discovery by `_identity_tokens` (version-stripped arXiv id
/ lowercased DOI / `oa_pdf_url` / normalized title): a forced paper discovery also
found appears once, and discovery's ingest-enabling metadata (`oa_pdf_url`,
`arxiv_version`, `doi`, real `title`, `venue`, `year`) is **merged into** the forced
entry (filling only fields the forced entry lacks) before the discovered duplicate
is dropped — so the enriched forced version wins.

The hub raises `n_target` to `max(N, forced_pending)` — where `forced_pending`
counts only forced papers **not already in the ledger skip-set** — so every
not-yet-done forced paper is **attempted** this tick without a done forced paper
inflating the discovered backfill. Forced papers still pass through ingest + G2 + G3
(mandatory ≠ gate-exempt); one whose ingest fails quarantines like any failed
ingest. Wired via `build_discover(force_include=CampaignConfig.force_include)`.
