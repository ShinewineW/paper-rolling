# Wiring the model seams — how the runtime agent composes the engine

This is the authoritative wiring contract for the `paper-landscape` Claude Code
skill. The engine under `scripts/` is **deterministic Python**; it contains **no
standalone `main()` and no hard-coded LLM call**. At runtime the host agent (the
`/paper-landscape` skill, or a daily `/loop` tick) *composes* the pipeline by
**injecting callables** into one entry point. Do not add a CLI driver and do not
hard-code a provider — the seams are provider-agnostic by design.

Running `scripts/run_campaign.py` directly only prints `_USAGE` and exits 0 (a
direct invocation is deliberately not a silent no-op).

## The entry point

`run_campaign(...)` in `scripts/run_campaign.py` is a *composition* function, not
a CLI:

```
run_campaign(*, workspace, discover, resolve_analysis, skeptic_votes,
             rigor_scores, entailment_judge, http, run_cli,
             cross_model_votes=None, cross_model_sample=0.0,
             empirical_classifier=None, write_report=None,
             faithfulness_judge=None,
             repo_resolver=None, requested_topic=None,
             requested_n=None, requested_auto_discover=None,
             max_concurrent=5) -> TickResult
```

`max_concurrent` is how many papers' spokes run in PARALLEL per tick (serial
within a paper). Each paper's analyzer fans out across whatever the `analyzer`
seam routes to, so with a `round_robin` of claude-code + codex and
`max_concurrent=2` you get ~5 `claude -p` + 5 `codex exec` in flight. Per-backend
concurrency is each provider's own `max_concurrent` in `config/llm.yaml`.

It deterministically wires `Ledger(workspace)` → `make_spoke(...)` →
(LS-1 lock `ledger.acquire()`) → `run_campaign_tick(...)`, and returns
`TickResult(hub=HubResult, landscape=LandscapeResult)`. The LS-1 single-writer
lock lives at this production entry — not inside `run_campaign_tick`, which hub
tests call directly with their own ledger.

The wiring is CODE precisely so prose drift can't bypass the adversarial
guarantees (G2 number-fabrication hard-block + G3 6-dim seal): every run goes
through both gates regardless of which seams the agent supplies.

## The injected callables — 8 to run_campaign, two kinds

`run_campaign(...)` takes **eight** injected callables, of two distinct kinds (a
ninth LLM seam — the query-expansion `llm` — is used to *build* the `discover`
adapter before composition, not passed to `run_campaign`; the optional human-chain
`write_report` writer is passed separately).

### (A) 5 LLM seams — agent-provided, each an INDEPENDENT Agent-tool invocation

Each of these **MUST** be backed by a *fresh sub-agent per call* (an independent
Agent-tool invocation), so audit votes are uncorrelated with the generator that
produced the numbers. Correlation would let a lazy runtime pass always-pass seams
and silently neuter G2/G3.

1. **`resolve_analysis(md_path: Path, candidate: dict) -> dict`** — the analyzer.
   Reads the frozen `corpus/{ID}/{ID}.md` + discovery `candidate` dict; returns
   the ARA bundle that branch2 (`branch2_ara`), branch1, and the `landscapes`
   comparator consume. **MUST** include the headline keys the cross-paper table
   needs: `headline_metric` (str), `headline_value` (float), `params_million`
   (float) — a paper missing them is dropped from the landscape table.
   The per-role HOW lives in `sub-skills/analyze-paper/SKILL.md`.

2. **`skeptic_votes(numbers, source_md, claim_context) -> tuple[SkepticVote, ...]`**
   — the G2 ground-truth-isolated skeptic (`SkepticVoteFn`, `scripts/audit/types.py`).
   Returns exactly one `SkepticVote(number, found_in_source, note="")` per input
   number. The per-role HOW lives in `sub-skills/g2-skeptic/SKILL.md`.

3. **`rigor_scores(ara_bundle: dict[str, str]) -> dict`** — the G3 6-dim rigor
   reviewer (`RigorScoreFn`, `scripts/audit/types.py`). Returns
   `{"dimensions": {dim_key: {"score": int 1–5, "strengths": [...],
   "weaknesses": [...], "suggestions": [...]}}, "findings": [...]}` over the six
   `DIMENSION_KEYS`. The per-role HOW lives in `sub-skills/g3-rigor-reviewer/SKILL.md`.

4. **`entailment_judge(claim: ClaimRecord, experiment_text: str) -> tuple[bool, str]`**
   — the G3 type-aware entailment check (`EntailmentJudgeFn`, `scripts/audit/types.py`).
   Returns `(entailed, reason)`. The per-role HOW lives in
   `sub-skills/entailment-judge/SKILL.md`.

5. **`faithfulness_judge(report_text: str, ara_dir: Path) -> dict`** — the branch1
   忠实门 (c) judge (ADR-0012). Compares the human report against the verified ARA;
   returns `{"faithful": bool, "findings": [{"claim": str, "issue": str}, ...]}` and
   fails CLOSED (malformed/empty → `faithful=False`). Ground-truth-isolated from the
   `write_report` writer (routed at tier=fast → a model ≠ the writer's). No sub-skill
   role dir — it is a config-routed judge. **MANDATORY when `write_report` is wired**
   (every production path): wiring the LLM writer without this judge aborts loudly so
   the (c) gate is never silently skipped; optional only on the no-LLM deterministic path.

### (B) 3 infra adapters — real I/O, NOT LLM seams

6. **`http(url) -> (status, body)`** — Tier-1 arXiv-HTML fetch (used by ingest).
7. **`run_cli(argv, cwd) -> result`** — Tier-2 MinerU / pandoc subprocess.
8. **`discover(topic: str, n: int) -> list[dict]`** — the discovery layer
   (`DiscoverFn`). It is **not** an LLM seam, though internally it is built over a
   query-expansion LLM seam: `scripts/discovery/query_expand.expand_queries(topic, llm=...)`.
   It returns the ranked candidate pool, over-pulled ~2–3×N so failures backfill.

**Why `http` / `run_cli` / `discover` are Python callables, not the agent's tools.**
The agent's WebFetch and Bash are *tools*, not Python objects — a tool cannot be
passed as a Python function argument. The engine calls a Python function; so each
infra adapter is a Python callable matching the signature above.

### Shipped default adapters — the deterministic plumbing is already wired [READY]

Because the three infra adapters are pure deterministic I/O (no LLM), there is no
reason to re-improvise them per run. `scripts/adapters.py` ships tested defaults:

```python
from scripts.adapters import build_http, build_run_cli, build_discover

http     = build_http()                    # requests-based; honors env proxies
run_cli  = build_run_cli()                 # subprocess.run -> CompletedProcess
discover = build_discover(                  # wires OpenAlex / S2 / arXiv / DBLP / HF
    llm=expand_llm,                         #   the ONE LLM-backed input (see below)
    is_ad_domain=campaign.is_ad_domain,
    polite_email=None,                      #   optional OpenAlex polite-pool email
    force_include=campaign.force_include,   #   must-include papers (front, authority-bypassed)
)
```

`build_discover` needs exactly one LLM-backed input — `llm`, the query-expansion
seam (`prompt -> list[str]`, itself an independent Agent-tool invocation); all
other discovery work is deterministic API wiring. Override any adapter by passing
your own callable to `run_campaign(...)` (e.g. wrap the agent's WebFetch in an
`http(url) -> (status, body)` of your own).

### (C) Optional: `repo_resolver` — code_ref repo-resolution cascade (P0)

`repo_resolver(*, arxiv_id, md_path, candidate) -> list[RepoCandidate]` produces
the ordered repo candidates branch2 clone-verifies for `src/code_ref.md`. Omit it
→ the engine uses the pure offline default (`resolve_repo_candidates`: T1 grep of
the paper MD + T2a the shipped Papers-with-Code `is_official` table). To extend
coverage to post-PwC-freeze papers, inject the composed production resolver:

```python
from scripts.output.repo_resolve import make_repo_resolver

repo_resolver = make_repo_resolver(            # T2b HF-live ON (deterministic, free)
    web_search=my_websearch,                   # OPTIONAL T4: enable long-tail websearch
)                                              #   a callable (query:str)->list[str]
```

`make_repo_resolver()` always wires **T2b** (`hf_official_repo`, a live
`api/papers/{id}` lookup reusing the `.env` HF token). **T4** activates only when
you pass `web_search` — a callable that runs an Agent WebSearch and returns the
result strings (the engine extracts github URLs from them). Every candidate, from
any tier, still passes the same clone-verification gate in `build_code_ref`
(official → accept on clone; search → must match arxiv_id/title or an innovation
symbol), so a wrong/reimplementation link is rejected, never linked.

**Net runtime job to make the workspace go**: construct the 5 LLM seams (+ the
query-expansion `llm`, + the optional `write_report` writer), call `build_http()` / `build_run_cli()` / `build_discover(...)`
for the rest, optionally `make_repo_resolver(...)`, and invoke `run_campaign(...)`.
That is the entire wiring — see SKILL.md "Invoke the engine (quickstart)".

## Independence + isolation invariants [MUST]

- **Fresh sub-agent per call** for all five LLM seams (uncorrelated audit votes).
- **Skeptic ground-truth isolation**: `skeptic_votes` sees ONLY `numbers` +
  `source_md` + `claim_context` — NEVER the evidence file / answer key / any
  rubric. G2 runs `n_skeptics` independent passes (default `n_skeptics=3`,
  `make_spoke`) and the **multi-vote majority hard-blocks** a fabricated number.
- **Rigor private rubric**: the scoring rubric is held privately by the
  `rigor_scores` implementation and never appears in any generator prompt.
- The analyzer seam is passed *as a parameter* (no module-global mutation) so
  concurrent spokes never share one analyzer.

## Where the seams flow inside the spoke

`make_spoke(...)` (`scripts/spoke.py`) runs, per paper, in order:
`ingest` → branch2 → **G2** → branch1 → **G3**. G2 is wired *through*
`produce_outputs` (the only place holding the staged branch2 before branch1) via
`run_g2(stage_ai_entry, md_path, skeptic_votes=..., n_skeptics=..., cross_model_votes=...)`,
so a `ProduceGateBlocked` aborts before promotion. G3 runs after both branches
under the bounded `run_with_budget(...)` (`max_gate_rounds=2`), calling
`run_g3(person_path, ai_path, md_path, content_list_path, rigor_scores=...,
entailment_judge=..., empirical_classifier=...)`. The spoke **never** writes the
ledger; the hub records the exact `person_vault_path` / `ai_package_path`
`produce_outputs` returned. See SKILL.md "Full pipeline order (per tick)" for the full tick.

## Campaign Hard Gate + cadence — one line each

- **Hard Gate**: `run_campaign_tick` raises `GateRequired` until `config/campaign.yaml`
  is locked (topic + N per tick); changing topic or N re-fires it — the harness
  catches `GateRequired` and runs the HITL setup gate, then retries.
- **Cadence**: a `/loop 1d ...` tick drives `run_campaign(...)` once per day,
  processing N new papers and skipping ledger-`done` ones, fully autonomously.
