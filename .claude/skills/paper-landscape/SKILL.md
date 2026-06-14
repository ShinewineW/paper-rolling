---
name: paper-landscape
description: Autonomous paper-knowledge engine for the paper-rolling workspace. Discovers authoritative + latest papers (multi-signal OR ranking), ingests via arXiv-HTML→MinerU, and emits a human report (person_vault/) plus an AI knowledge pack (ai_package/) per paper, gated by adversarial audits. Use inside ~/Coding/paper-rolling/ to survey a field, build a SOTA landscape, or run a daily /loop research campaign.
license: CC-BY-NC-4.0
---

# paper-landscape (v2 — paper-rolling engine)

Project-specific engine for the `~/Coding/paper-rolling/` workspace. It turns a
confirmed research topic into a growing knowledge base: per-paper human reports
(`person_vault/`) + AI knowledge packs (`ai_package/`), plus cross-paper
landscapes. It is **not** a general installable skill — it hard-assumes the
paper-rolling workspace layout (`corpus/`, `_ledger/`, `person_vault/`,
`ai_package/`, `landscapes/`, `config/`).

## Knowledge layer (read on demand)

The agent-facing knowledge lives in `references/` (load the doc you need),
`sub-skills/` (one focused role per LLM seam), plus `examples/` + `templates/`:

- `references/wiring-the-seams.md` — how to compose + **invoke** the engine (start here).
- `references/ara-schema.md` — the ARA bundle `resolve_analysis` must return.
- `references/discovery-and-authority.md` · `ingest-fidelity.md` · `naming-and-ledger.md` · `landscapes.md` — per-subsystem depth.
- `references/branch1-quality.md` — quality bar + opening 「评价」 for the human report.
- `references/glossary.md` — domain terms.
- `sub-skills/{analyze-paper,g2-skeptic,g3-rigor-reviewer,entailment-judge}/` — the four sub-skill LLM-seam role docs (the branch1 「评价」 `faithfulness_judge` note-writer seam is routed via config without a role dir).
- `examples/worked-example.md` + `examples/sample-ara-bundle.json` — one paper end-to-end; the literal `resolve_analysis` output target.
- `templates/{ara-paper,branch1-report,landscape}.md` — the output skeletons branch2 / branch1 / landscapes write.

## Preflight — environment check (run FIRST) — MUST

Before the campaign gate or ANY processing, verify the machine has every external
prerequisite. A missing tool MUST be a loud STOP here — never a silent per-paper
skip later:

```bash
PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.preflight
```

It runs **three layers** and **exits non-zero** if anything is unhealthy, naming each fix:
- **presence** — runtime deps + `pandoc`/`mineru` on PATH (stdlib-only, so it reports even when deps are missing);
- **LLM config** — `config/llm.yaml` routing is complete, each routed provider's `api_key_env` is set, and every routed *API* provider answers a trivial **liveness** prompt (key + endpoint actually work). **Local agents** (`claude-code` / `codex`, incl. `round_robin` pool members) are **presence-only — never probed**: a gratuitous subprocess call risks IP-based account suspension, and the real analyzer workload exercises it anyway;
- **deep smoke** — `pandoc` and `mineru` actually convert a tiny bundled fixture and `mineru`'s products match a committed golden. The mineru smoke is **cached** (keyed on mineru version + fixture): first run pays ~75s (model load), later runs are instant. Flags: `--no-probe` (skip liveness), `--no-deep` (skip smoke), `--force-smoke` (ignore cache).

It also emits one **advisory** (non-blocking) line — `final-review:runtime`: which AI drives the engine (the engine never runs autonomously). A Claude-Code runtime is `[OK]` (terminal review runs via the main-session agent). A **non-Claude-Code runtime** (e.g. a pure-API driver) is a `[WARN]` — the terminal-review gate (ADR-0013) has **no autonomous reviewer**, so the operator must route a reviewer onto their own API provider or **skip terminal review deliberately**. It WARNs (never fails) so the situation is surfaced for the operator to decide, not silently absent.

The deep smoke exists because "installed" ≠ "works": `mineru` can be on PATH yet crash at first real use (missing `socksio` under a SOCKS proxy, or model download blocked) — the smoke catches that **before** any token is burned. **If it exits non-zero, STOP**: report what is unhealthy and the fix; do **not** proceed to the Hard Gate or ingest until it is all-green. Gate every run on it — `… -m scripts.preflight && <run the tick>`. mineru's environment (socksio + a reachable model mirror) is a known footgun — see `docs/guides/mineru-setup.md`.

## Entry: the campaign Hard Gate (HITL, once per campaign) — MUST

The **first action after preflight passes** is a blocking **Hard Gate** (中枢-D1).
You MUST get explicit human confirmation of **topic + N per tick** (plus any
must-include papers), then lock them into `config/campaign.yaml`:

1. **Topic** — precise, not vague. If the user says something broad ("自动驾驶"),
   propose a narrowed scope and get confirmation. A vague single-term topic is
   rejected (`GateError`).
2. **N per tick** — the explicit number of papers to *successfully* process per
   `/loop` tick (the cost/disk ceiling). No number → no go.
3. **force_include** (optional) — papers the user says MUST be processed, not left
   to autonomous discovery. Each entry is a dict that needs **two** things and the
   gate rejects it (`GateError`) if either is missing: (a) an **ingestible source**
   the engine can actually fetch — an `arxiv_id` (HTML/PDF) or a direct `oa_pdf_url`
   (a bare `doi` is NOT ingestible — there is no DOI→PDF resolver), and (b) a
   **distinct identity** — `arxiv_id`, `doi`, or `title` (a `oa_pdf_url`-only entry
   must add a `title` so two entries can't collide into one corpus dir / ledger
   key). They are prepended to the pool, **bypass the authority filter**, and are
   all attempted this tick — but still go through ingest + G2 + G3 (mandatory ≠
   exempt from quality gates). If discovery independently finds a forced paper, the
   two are deduped to ONE entry and discovery's ingest metadata (PDF URL, venue,
   year) is **merged into** the forced entry.

```bash
# Establish the campaign (run once, human present). force_include is optional:
PYTHONPATH=.claude/skills/paper-landscape uv run python -c "from scripts.campaign import CampaignConfig, write_campaign; \
import pathlib; write_campaign(pathlib.Path('.'), \
CampaignConfig(topic='end-to-end AD trajectory prediction', n_per_tick=5, is_ad_domain=True, \
force_include=[{'arxiv_id': '2401.00001', 'title': 'A must-include paper'}]))"
```

Until `config/campaign.yaml` exists, `run_campaign_tick` raises `GateRequired`
and processing is blocked. Changing the topic or N re-fires the gate; a plain
`/loop` tick on an unchanged campaign **reads the config and re-gates not at all
— no re-gate** (吸收-D4). It runs autonomously. Flipping `auto_discover` also
re-fires the gate: `true` = 自发查找 (topic discovery, `force_include` adds on top);
`false` = 指定列表 (discovery OFF — `force_include` is the entire work set, paged
by `n_per_tick`; ADR-0010).

> **`is_ad_domain` wiring**: when you build the production `discover` seam, copy
> `CampaignConfig.is_ad_domain` into the discovery `config` dict. `score_authority`
> reads it to pick the authority whitelists — general AI/ML venues+labs always,
> plus the autonomous-driving/robotics extra set only when `is_ad_domain` is true.
> Omit it and the scorer defaults to the full (general+AD) set. **Likewise copy
> `CampaignConfig.force_include` into `build_discover(force_include=…)`** so the
> locked must-include papers enter the pool (front, authority-bypassed, deduped).

## Daily usage: /loop (the long-running cadence)

This engine is long-running. The recommended cadence is **daily** (once per day):

```
/loop 1d Continue the paper-rolling campaign. Read config/campaign.yaml and the
ledger. Run one tick: discover N new papers, process them through the pipeline,
update person_vault/ + ai_package/, regenerate landscapes/. Skip ledger-done
papers; backfill failures from the candidate pool. Never idle, never ask the user.
```

Each tick **incrementally** processes N *new* papers (ledger-`done` papers are
skipped; discovery over-pulls 2–3×N candidates so failures can be backfilled).
A per-tick **watchdog** (bounded, not a daemon) re-fires stalled or
falsely-claimed-done papers up to a re-fire budget, then stops.

## Zero mid-pipeline questions — MUST

After the entry gate, the **中段 (mid-pipeline) is fully autonomous** (中枢-D2):
the engine **MUST NOT** call `AskUserQuestion` or otherwise interrupt the user
mid-pipeline. Any ambiguity is self-resolved. There is no second confirmation
gate (no candidate-list approval) — the entry gate is the only HITL point.

## Full pipeline order (per tick)

The hub (single ledger writer) drives this order; spokes run max-N papers in
parallel, but **serial within one paper** (branch2 emits before branch1). The
ordinal sequence is discover → ingest → ledger → branch2 → **G2** → branch1 →
**G3** → landscapes (G2 sits between the branches; G3 after both):

1. **discover** — `scripts/discovery/discover.py`: multi-signal OR ranking
   (ADR-0001), over-pull 2–3×N candidate pool.
2. **ingest** — `scripts/ingest/ingest.py`: arXiv-HTML (Tier 1) → MinerU
   (Tier 2); both fail → quarantine to `_failed/` (吸收-D6). Produces
   `corpus/{ID}/{ID}.md` + `.md_contract.json`.
3. **ledger** — `scripts/ledger/store.py`: version-aware skip + hash-on-fetch;
   the hub is the **only** writer (`processed_ledger.yaml`, atomic append).
4. **branch2** — ARA compiler: `ai_package/{date}_{Name}_{idbase}/ara/` (AI
   knowledge pack; exact numbers only under `evidence/`).
5. **G2** — data-fidelity gate (number/claim fidelity, adversarial multi-vote,
   hard-block on fabrication): runs **after branch2, before branch1**, on
   branch2's staged ARA evidence. A hard block aborts before branch1 and any
   promotion (OT-5: nothing reaches the real vault).
6. **branch1** — illustration author: `person_vault/{date}_{Name}_{idbase}/`
   (Chinese report; Mermaid redraw + derivation + loss explainer). ADR-0012 rev: NO
   hard gate — the report opens with a non-blocking 「评价」 note ((b) report numbers
   not in the ARA + (c) an advisory LLM judge note); the 核心结论 block is plain prose
   (the `<!--ref-->` anchoring is retired). branch1 always publishes.
7. **G3** — seal gate (G3R0 branch1-presence + equation fidelity + 6-dim rigor
   seal): runs **after both branches**. Hard failures block + re-emit (max N
   rounds → escalate / flag for human).
8. **landscapes** — `scripts/landscapes.py` (corpus-batch-comparator): after the
   batch, regenerate `landscapes/{topic}/INDEX.md` + `report.md` (unified metric
   tables, efficiency, trends).

### Per-paper spoke

The per-paper pipeline (steps 2–7) is realized by `scripts/spoke.py`
`make_spoke(...)`, which composes ingest → branch2 → G2 → branch1 → G3 in order
via the bounded `gate_runner`. G2/branch1 are wired **through** `produce_outputs`
(the only place that holds the staged branch2 before branch1), so a G2 hard
block aborts before promotion; G3 runs after promotion under the bounded runner.
The spoke **never** writes the ledger (single-writer invariant): the hub records
the EXACT `person_vault_path` / `ai_package_path` that `produce_outputs` returns,
never a re-derived key.

## Wiring the model seams [MUST]

`make_spoke(...)` (and the `run_campaign(...)` driver that composes it) take five
**injected analysis/audit model seams** (the four analysis/G2/G3 seams below plus
the branch1 「评价」 (c) `faithfulness_judge` note-writer, item 5 — ADR-0012 rev). The composition is
CODE; the runtime injects everything LLM-backed or I/O-backed. Besides these, the
runtime also supplies the infrastructure adapters `discover` / `http` / `run_cli`,
and the `discover` callable is itself built over a further LLM-backed seam — the
query-expansion `llm` (`discovery.query_expand.expand_queries(topic, llm=...)`) —
and the optional human-chain `write_report` writer. Each analysis/audit seam below
**MUST** be backed by an **independent Agent-tool invocation** (a fresh sub-agent
per call) so the audit votes are uncorrelated with the generator that produced the
numbers. The entry point the `/loop` tick drives,
once the seams are constructed, is **`scripts/run_campaign.py`** →
`run_campaign(workspace, discover, resolve_analysis, skeptic_votes, rigor_scores,
entailment_judge, faithfulness_judge, http, run_cli, ...)`; it builds the ledger, wires the seams into
`make_spoke`, and calls `run_campaign_tick` (which raises `GateRequired` if the
campaign Hard Gate is not
satisfied). Do **not** hard-code an LLM call — the seams are provider-agnostic.
The **3 infra adapters ship as tested defaults** in `scripts/adapters.py`
(`build_http` / `build_run_cli` / `build_discover`) — so the runtime only
constructs the LLM seams (see "Invoke the engine (quickstart)" below). Full
contract: `references/wiring-the-seams.md`; per-role: `sub-skills/<role>/SKILL.md`.

1. **`resolve_analysis(md_path, candidate) -> dict`** — the analyzer sub-agent.
   - **Input**: the frozen `corpus/{ID}/{ID}.md` path + the discovery `candidate`
     dict (identity + metadata).
   - **Output**: the ARA analysis bundle that `branch2_ara` / `branch1` and the
     `landscapes` comparator consume (`overview`, `problem`, `claims`, `concepts`,
     `experiments`, `related_work`, `architecture`, `algorithm`, `heuristics`,
     `configs_training`, `configs_model`, `environment`, `execution_stub`,
     `innovations`, `exploration_tree`, `evidence_tables`, …). It
     **MUST** include the headline-metric keys the landscape table needs:
     `headline_metric` (str, e.g. `"NDS"`), `headline_value` (float), and
     `params_million` (float) — without them branch2's `PAPER.md` frontmatter is
     dropped from the cross-paper table.
   - **MUST**: an independent Agent-tool invocation.

2. **`skeptic_votes(numbers, source_md, claim_context) -> tuple[SkepticVote, ...]`**
   — the G2 ground-truth-isolated skeptic (`SkepticVoteFn` in
   `scripts/audit/types.py`).
   - **Input**: the candidate `numbers` (tuple of stringified values), the raw
     `source_md` text, and a short `claim_context` string. **Ground-truth
     isolation [MUST]**: the seam **NEVER** receives the evidence file / answer
     key / any rubric — only the candidate numbers + the source MD.
   - **Output**: exactly one `SkepticVote(number, found_in_source, note="")` per
     input number. One **independent** vote per number; G2 runs `n_skeptics`
     independent passes and the **multi-vote majority** is what hard-blocks a
     fabricated number. Correlation with the generator would defeat the block,
     hence the isolation MUST.
   - **MUST**: an independent Agent-tool invocation per call.

3. **`rigor_scores(ara_bundle) -> dict`** — the G3 6-dim rigor reviewer
   (`RigorScoreFn` in `scripts/audit/types.py`).
   - **Input**: the ARA text bundle (`dict[str, str]`).
   - **Output**: `{"dimensions": {dimension_key: {"score": int (1–5),
     "strengths": [...], "weaknesses": [...], "suggestions": [...]}}, "findings":
     [...]}` covering all six `DIMENSION_KEYS`
     (D1_evidence_relevance … D6_methodological_rigor).
   - **Private-rubric [MUST]**: the scoring rubric is held **privately** by the
     seam implementation and **never** appears in any generator prompt
     (ground-truth isolation). An independent Agent-tool invocation.

4. **`entailment_judge(claim, experiment_text) -> tuple[bool, str]`** — the G3
   type-aware entailment check (`EntailmentJudgeFn` in `scripts/audit/types.py`).
   - **Input**: a `ClaimRecord` + the linked experiment text.
   - **Output**: `(entailed: bool, reason: str)`.
   - **MUST**: an independent Agent-tool invocation.

5. **`faithfulness_judge(report_text, ara_dir, *, ungrounded=None) -> str`** — the
   branch1 「评价」 (c) note-writer (ADR-0012 rev). Writes a reader-facing Chinese prose
   faithfulness note comparing the human report against the verified ARA. ADVISORY —
   it does NOT block; branch1 always publishes.
   - **Input**: the composed Chinese `report_text` + the staged `ara/` dir + the (b)
     `ungrounded` number fact list (context).
   - **Output**: a Chinese prose `str` (the 评价's semantic note). Fail-SOFT — any
     seam/ARA error degrades to a neutral note, it never raises.
   - **SHOULD**: an independent Agent-tool invocation, ground-truth-isolated from the
     `write_report` writer (routed at tier=fast → a model ≠ the writer's).
   - **OPTIONAL on every path**: omit it (or on seam error) and the opening 「评价」 still
     publishes with its machine number-facts, just without the prose note.

## Invoke the engine (quickstart)

Run the **Preflight** gate first (above) and only proceed if it is all-green. The
infra plumbing ships; the runtime only constructs the LLM seams, then calls
`run_campaign(...)`. Run with `PYTHONPATH=.claude/skills/paper-landscape`:

```python
from pathlib import Path
from scripts.campaign import load_campaign
from scripts.run_campaign import run_campaign
from scripts.adapters import build_http, build_run_cli, build_discover

# Load the LOCKED campaign so is_ad_domain + force_include come from
# config/campaign.yaml — NEVER hardcode them here (that silently drops the
# Hard-Gate decision). load_campaign returns None until the campaign is locked;
# run_campaign then raises GateRequired, which the harness turns into the HITL
# setup gate. is_ad_domain defaults to True (AD whitelists) when not yet locked.
campaign = load_campaign(Path("."))

# The SEVEN LLM seams are provider-routed + StrictProvider-wrapped (NO fallback — a
# failing provider raises EngineAbort, never silently uses the Claude Code sub); build them
# from config/llm.yaml via build_seams() (see references/wiring-the-seams.md). Each
# is an independent provider call (ground-truth isolation preserved). write_report
# is the human-chain writer — pass it so branch1 produces the RICH LLM report
# (figures + sections); omit it and branch1 falls back to the thin renderer.
# faithfulness_judge is the branch1 「评价」 (c) note-writer seam (report ↔ ARA, ADR-0012
# rev) — advisory + fail-soft, never blocks; omit it and the 评价 just skips the prose note.
from scripts.llm.seams import build_seams
from scripts.output.repo_resolve import make_repo_resolver

seams = build_seams()
result = run_campaign(
    workspace=".",
    resolve_analysis=seams["resolve_analysis"],
    skeptic_votes=seams["skeptic_votes"],
    rigor_scores=seams["rigor_scores"],
    entailment_judge=seams["entailment_judge"],
    write_report=seams["write_report"],  # DEFAULT: rich LLM human chain
    faithfulness_judge=seams["faithfulness_judge"],  # branch1 「评价」 (c) note, ADR-0012 rev
    discover=build_discover(
        llm=seams["expand_llm"],
        is_ad_domain=campaign.is_ad_domain if campaign else True,
        force_include=campaign.force_include if campaign else [],
        auto_discover=campaign.auto_discover if campaign else True,
    ),
    http=build_http(),
    run_cli=build_run_cli(),
    # code_ref repo resolution (P0). ALL FOUR tiers on: T2a PwC + T1 paper-text +
    # discovery + T2b HF-live (always) + T4 websearch via the optional `web_search`
    # seam (routed in config/llm.yaml → a fresh sub-agent WebSearch per UNRESOLVED
    # paper; long-tail only, fail-soft). seams["web_search"] is a no-op [] if the
    # optional seam is unrouted, so this line is always safe.
    repo_resolver=make_repo_resolver(web_search=seams["web_search"]),
)
```

`run_campaign` raises `GateRequired` until `config/campaign.yaml` is locked (the
campaign Hard Gate above) — establish the campaign once, then a `/loop` tick just
runs this. `build_seams()` constructs all seven provider-routed LLM seams (analysis,
skeptic, rigor, entailment, expand, writer, faithfulness); the agent only loads the
campaign and calls `run_campaign(...)`.

## Failure handling (中枢-D2)

- **Whole-paper unprocessable** (download all-fail / both ingest tiers fail /
  audit hard-block unresolved after N rounds) → skip, write a small tracked
  record to `_failed/{key}.md`, mark `status: failed` in the ledger, and
  **backfill** the next pool candidate until N done or the pool is exhausted.
- **Local degradation** (garbled equations, no OSS code) → do **not** skip; tag
  + downgrade (suppress unreliable derivation, flag) and keep the paper.

## Stability invariants (long-program hardening)

- Single ledger writer (hub only); `_ledger/.lock` rejects a second instance.
- Startup consistency check: every `done` paper must have both a `person_vault/`
  and an `ai_package/` entry; missing → downgrade to re-process (drift self-heal).
- Vault entry key = `{入库日期}_{Name}_{arxivid_base}` (deterministic `Name`,
  no LLM ad-hoc naming) → 1:1 person↔ai pairing, stable across runs.
