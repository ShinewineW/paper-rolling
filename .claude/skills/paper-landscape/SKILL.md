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
parallel, but **serial within one paper** (branch2 emits before branch1):

1. **discover** — `scripts/discover.py`: multi-signal OR ranking (ADR-0001),
   over-pull 2–3×N candidate pool.
2. **ingest** — `scripts/convert_pdf.py`: arXiv-HTML (Tier 1) → MinerU (Tier 2);
   both fail → quarantine to `_failed/` (吸收-D6). Produces `corpus/{ID}/{ID}.md`
   + `.md_contract.json`.
3. **ledger** — `scripts/ledger.py`: version-aware skip + hash-on-fetch; the hub
   is the **only** writer (`processed_ledger.yaml`, atomic append).
4. **branch2** — ARA compiler: `ai_package/{date}_{Name}/ara/` (AI knowledge
   pack; exact numbers only under `evidence/`).
5. **branch1** — illustration author: `person_vault/{date}_{Name}/` (Chinese
   report; Mermaid redraw + derivation + loss explainer; every empirical claim
   anchored to the MD via `<!--ref-->` markers, 吸收-D1).
6. **G2 / G3** — audit gates: G2 (number/claim fidelity, adversarial multi-vote,
   hard-block on fabrication) runs **after branch2, before branch1** (on branch2's staged ARA evidence); G3
   (branch1↔MD consistency + equation fidelity + 6-dim rigor seal) runs **after
   branches**. Hard failures block + re-emit (max N rounds → escalate / flag for
   human).
7. **landscapes** — `scripts/landscapes.py` (corpus-batch-comparator): after the
   batch, regenerate `landscapes/{topic}/INDEX.md` + `report.md` (unified metric
   tables, efficiency, trends).

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
