---
name: paper-landscape
description: >-
  Autonomous paper-knowledge engine for the paper-rolling workspace. Use when
  surveying SOTA, building a research knowledge base, or running a long-lived
  daily paper campaign. Triggers on "paper survey", "SOTA landscape", "调研论文",
  "paper-landscape". Project-specific — runs only inside ~/Coding/paper-rolling/.
allowed-tools: Bash Read Write Edit Glob Grep AskUserQuestion
---

# paper-landscape (v2) — autonomous paper-knowledge engine

This skill is the engine for the `paper-rolling` workspace. It discovers,
ingests, analyzes, and dual-publishes papers as accumulated knowledge products.
It is **project-specific** (基调-D3): it hard-assumes the workspace layout
(`corpus/` `_ledger/` `person_vault/` `ai_package/` `landscapes/` `_failed/`
`config/`) and is **not** a globally installable skill.

> Run only from the workspace root: `cd ~/Coding/paper-rolling` first.
> All on-disk layout is defined in `scripts/paths.py` — never hardcode paths.

## Entry: the campaign Hard Gate [MUST]

**[MUST] On a NEW or CHANGED campaign, the FIRST step is a blocking Hard Gate.**
You may not enter discovery / download / processing until the user has
**explicitly confirmed two things** (中枢-D1):

1. **Topic — precise, non-ambiguous.** If the user gives a vague topic
   (e.g. "autonomous driving"), you MUST propose a narrowed scope and get
   confirmation. Never start on a vague topic.
2. **Count — an explicit per-round paper number (`per_round_count`).** This is
   the success target AND the cost/disk ceiling for each round. No number → no go.

Both confirmations are written into `config/campaign.yaml` (吸收-D4). This Hard
Gate runs **once at campaign establishment** (a human is present), not on every
round. Use `AskUserQuestion` here, and ONLY here.

## Daily autonomous cadence: `/loop`

After the campaign is locked, schedule daily incremental runs:

```
/loop 1d /paper-landscape
```

Each `/loop` tick (吸收-D3 / 吸收-D4):
- Reads the locked `config/campaign.yaml` — **does NOT re-gate**.
- Incrementally processes `per_round_count` NEW papers (ledger-done papers are
  skipped; discovery over-pulls `candidate_multiplier × N` for back-fill).
- Runs **fully autonomously**: **[MUST] no mid-pipeline `AskUserQuestion`** after
  the gate (中枢-D2). Any problem is self-resolved; failures are skipped, recorded
  in `_failed/`, and back-filled from the candidate pool until N succeed or the
  pool is exhausted.
- A bounded round watchdog re-fires the hub if it stalls or the ledger has
  non-`done` papers the hub claims are complete; it stops when N are done or the
  pool empties (吸收-D3 — bounded, not a daemon).

Re-run the Hard Gate (re-invoke and confirm) ONLY to change the topic or count.

## Pipeline (high level)

`Step 0` ledger load + version-aware skip + crash-residue cleanup (LS-3) →
`Step 1` campaign params → `Step 2` discovery hub (multi-signal authority,
ADR-0001) → `Step 2.5` ingest (arXiv-HTML → MinerU, 摄取-D1; two-tier, failures
isolated to `_failed/`) → `Step 3` per-paper hub-spoke fan-out → `Step 4`
cross-paper synthesis → `Step 5` landscape report in `landscapes/`.

Per paper, the spoke is **strictly sequential** (§5.2 MUST): `ai_package` (ARA)
is produced first, then `person_vault` is derived from it; the two vaults are
written **atomically — same success or same failure** (OT-5). Cross-paper
parallelism (disjoint `{ID}` trees) is the only concurrency; the hub is the
single ledger writer (LS-1 `.lock`).

## Outputs

- `corpus/{ID}/{ID}.md` — converted full-text knowledge (tracked); pdf/images
  local-only (基调-D2).
- `ai_package/{date}_{Name}_{id}/ara/` — AI-facing ARA knowledge pack.
- `person_vault/{date}_{Name}_{id}/` — human-facing illustrated Chinese report.
- `_failed/` — per-paper failure records for manual follow-up.
- `landscapes/` — cross-paper synthesis reports.

Vault entries pair 1:1 across `person_vault/` and `ai_package/` by the same key
(双输出-D5); keys are deterministic (OT-3, never LLM-named) and collision-proof
(OT-1: `{intake_date}_{Name}_{arxiv_base_or_doi_hash}`).
