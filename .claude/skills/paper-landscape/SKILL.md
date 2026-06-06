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

The agent-facing knowledge lives in `references/` (load the doc you need) and
`sub-skills/` (one focused role per LLM seam — what a fresh sub-agent loads):

- `references/wiring-the-seams.md` — how to compose + **invoke** the engine (start here).
- `references/ara-schema.md` — the ARA bundle `resolve_analysis` must return.
- `references/discovery-and-authority.md` · `ingest-fidelity.md` · `naming-and-ledger.md` · `landscapes.md` — per-subsystem depth.
- `references/glossary.md` — domain terms.
- `sub-skills/{analyze-paper,g2-skeptic,g3-rigor-reviewer,entailment-judge}/` — the four independent LLM-seam roles.

## Entry: the campaign Hard Gate (HITL, once per campaign) — MUST

The **first action** on a new campaign is a blocking **Hard Gate** (中枢-D1).
You MUST get explicit human confirmation of **two** things, then lock them into
`config/campaign.yaml`:

1. **Topic** — precise, not vague. If the user says something broad ("自动驾驶"),
   propose a narrowed scope and get confirmation. A vague single-term topic is
   rejected (`GateError`).
2. **N per tick** — the explicit number of papers to *successfully* process per
   `/loop` tick (the cost/disk ceiling). No number → no go.

```bash
# Establish the campaign (run once, human present):
PYTHONPATH=.claude/skills/paper-landscape uv run python -c "from scripts.campaign import CampaignConfig, write_campaign; \
import pathlib; write_campaign(pathlib.Path('.'), \
CampaignConfig(topic='end-to-end AD trajectory prediction', n_per_tick=5, is_ad_domain=True))"
```

Until `config/campaign.yaml` exists, `run_campaign_tick` raises `GateRequired`
and processing is blocked. Changing the topic or N re-fires the gate; a plain
`/loop` tick on an unchanged campaign **reads the config and re-gates not at all
— no re-gate** (吸收-D4). It runs autonomously.

> **`is_ad_domain` wiring**: when you build the production `discover` seam, copy
> `CampaignConfig.is_ad_domain` into the discovery `config` dict. `score_authority`
> reads it to pick the authority whitelists — general AI/ML venues+labs always,
> plus the autonomous-driving/robotics extra set only when `is_ad_domain` is true.
> Omit it and the scorer defaults to the full (general+AD) set.

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
   (Chinese report; Mermaid redraw + derivation + loss explainer; every
   empirical claim anchored to the MD via `<!--ref-->` markers, 吸收-D1).
7. **G3** — seal gate (branch1↔MD consistency + equation fidelity + 6-dim rigor
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

`make_spoke(...)` (and the `run_campaign(...)` driver that composes it) take four
**injected analysis/audit model seams**. The composition is CODE; the runtime
injects everything LLM-backed or I/O-backed. Besides these four, the runtime also
supplies the infrastructure adapters `discover` / `http` / `run_cli`, and the
`discover` callable is itself built over a **fifth** LLM-backed seam — the
query-expansion `llm` (`discovery.query_expand.expand_queries(topic, llm=...)`).
Each of the four below **MUST** be backed by an **independent Agent-tool
invocation** (a fresh sub-agent per call) so the audit votes are uncorrelated with
the generator that produced the numbers. The entry point the `/loop` tick drives,
once the seams are constructed, is **`scripts/run_campaign.py`** →
`run_campaign(workspace, discover, resolve_analysis, skeptic_votes, rigor_scores,
entailment_judge, http, run_cli, ...)`; it builds the ledger, wires the seams into
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

## Invoke the engine (quickstart)

The infra plumbing ships; the runtime only constructs the LLM seams, then calls
`run_campaign(...)`. Run with `PYTHONPATH=.claude/skills/paper-landscape`:

```python
from scripts.run_campaign import run_campaign
from scripts.adapters import build_http, build_run_cli, build_discover

# resolve_analysis / skeptic_votes / rigor_scores / entailment_judge / expand_llm
# are each an INDEPENDENT Agent-tool invocation — construct per
# references/wiring-the-seams.md + sub-skills/<role>/SKILL.md.
result = run_campaign(
    workspace=".",
    resolve_analysis=resolve_analysis,
    skeptic_votes=skeptic_votes,
    rigor_scores=rigor_scores,
    entailment_judge=entailment_judge,
    discover=build_discover(llm=expand_llm, is_ad_domain=True),  # is_ad_domain from campaign.yaml
    http=build_http(),
    run_cli=build_run_cli(),
)
```

`run_campaign` raises `GateRequired` until `config/campaign.yaml` is locked (the
campaign Hard Gate above) — establish the campaign once, then a `/loop` tick just
runs this. The four LLM seams + `expand_llm` are the only things the agent builds.

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
