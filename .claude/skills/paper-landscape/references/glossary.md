# paper-landscape glossary

<!-- Generated: 2026-06-13 | Updated: branch1 评价 (ADR-0012 rev), G3 components -->

> **范围**: `scripts/` 和 `SKILL.md` 的术语表。更新日期：2026-06-13（ADR-0012 rev 已实施）。

Project-specific terms for the paper-rolling engine. Symbols cite `scripts/` and `SKILL.md`. See sibling docs `wiring-the-seams.md`, `discovery-and-authority.md`, `ingest-fidelity.md`, `naming-and-ledger.md`, and `landscapes.md` for flow.

- **campaign** — A locked research run: `{topic, n_per_tick, is_ad_domain}` persisted in `config/campaign.yaml` (`scripts/campaign.py` `CampaignConfig` / `write_campaign`). One campaign = one topic surveyed incrementally over many ticks.
- **campaign Hard Gate (HITL)** — The single blocking human-in-the-loop point (中枢-D1). First action on a new campaign: confirm topic + N, then lock. A vague single-term topic is rejected (`GateError`); changing topic/N re-fires the gate. The only place the engine asks the user anything.
- **tick** — One incremental pass that processes N *new* papers. Ledger-`done` papers are skipped; failures backfilled from the over-pulled pool. Driven by `run_campaign_tick`; raises `GateRequired` if no campaign is locked.
- **/loop** — The long-running cadence (recommended `/loop 1d`) that fires one tick per day. "Never idle, never ask the user" — fully autonomous after the entry gate.
- **hub** — The orchestrator and the **single ledger writer**. Drives pipeline order, records the EXACT vault paths `produce_outputs` returned, runs the watchdog/consistency check.
- **spoke** — The per-paper worker (`scripts/spoke.py` `make_spoke`): composes ingest → branch2 → G2 → branch1 → G3 for one paper, serial within the paper. **Never** writes the ledger (single-writer invariant).
- **branch1** (`person_vault/`) — Human-facing Chinese report (Mermaid redraw + derivation + loss explainer). Prose may carry numbers in natural language, grounded in the ARA. The opening **`## 评价`** (ADR-0012 rev) surfaces ungrounded numbers and a judge's advisory note as a fail-soft assessment — it never blocks publication. The `## 核心结论` block is plain prose (RETIRED: no anchors, no `<!--ref-->` machinery, ADR-0012 rev).
- **branch2** (`ai_package/`) — AI-facing ARA knowledge pack; exact numbers live only under `evidence/`. Emitted **before** branch1.
- **ARA** — Agent-native Research Artifact: the structured analysis bundle `resolve_analysis` returns and `branch2`/`branch1`/`landscapes` consume. See the sibling `ara-schema.md` (schema origin: AI-Research-SKILLs ARA compiler, cloned under `docs/reference/`).
- **headline metric** — The cross-paper table keys the ARA bundle MUST carry: `headline_metric` (str), `headline_value` (float), `params_million` (float). A `PAPER.md` missing this frontmatter is dropped from the landscape table.
- **G2 (data-fidelity gate)** — `scripts/audit/g2_data_fidelity.py` `run_g2`. Runs **after branch2, before branch1**; adversarial multi-vote over numbers, fail-closed, hard-blocks fabrication before anything reaches the real vault.
- **G3 (seal gate)** — `scripts/audit/g3_seal.py` `run_g3`. Runs **after both branches**: **G3R0** (branch1 presence check) + type-aware entailment + 6-dim rigor seal + equation fidelity. Bounded retry via `scripts/audit/gate_runner.run_with_budget`. (RETIRED: anchor resolution — ADR-0012 rev.)
- **seam** — An injected callable the runtime supplies; composition is code, never a hard-coded LLM call. Two kinds: **LLM seams** (`resolve_analysis`, `skeptic_votes`, `rigor_scores`, `entailment_judge`, `faithfulness_judge` — each a fresh independent Agent-tool invocation; + the optional human-chain `write_report` writer) vs **infra adapters** (`discover`, `http`, `run_cli` — real I/O Python wrappers, not LLM). `discover` is itself built over the query-expansion LLM seam (`discovery.query_expand.expand_queries`).
- **ledger (single-writer)** — `_ledger/processed_ledger.yaml` (`scripts/ledger/store.py`): atomic-append, hub-only writer, `_ledger/.lock` (LS-1) rejects a second instance. Records each branch's recorded path field (`person_vault_path` / `ai_package_path`), never a re-derived key.
- **vault key** — The 1:1 person↔ai entry name `{入库日期}_{Name}_{idbase}`. Sole authority is `scripts/output/naming.py` `vault_key`; `paths.py` and the ledger never re-derive it.
- **idbase** — The version-stripped identity suffix in the vault key: `re.sub(r"v\d+$", "", arxiv_id)`, or a DOI-hash for non-arXiv papers.
- **quarantine (`_failed/`)** — When a paper is unprocessable it is parked in `_failed/` and the ledger row is marked `status: failed`, then the next pool candidate is backfilled. Two record shapes: both ingest tiers failing writes a JSON record `corpus/_failed/{ID}.json` (`scripts/ingest/ingest.py` `quarantine`, 吸收-D6 / 中枢-D2); a G2 hard-block or G3R0 missing-report writes a markdown record `_failed/{key}.md` (`scripts/spoke.py`, 中枢-D2). (branch1 no longer has a hard gate as of ADR-0012 rev.)
- **watchdog** — A bounded (not daemon) per-tick re-fire mechanism that re-runs stalled or falsely-`done` papers up to a budget, then stops (`hub._is_truly_done`).
- **over-pull** — Discovery fetches 2–3×N candidates so failed papers can be backfilled without re-discovering; ADR-0001 multi-signal OR ranking, no citation gate.
- **ground-truth isolation** — `skeptic_votes` sees ONLY the candidate `numbers` + raw `source_md` — never the evidence file, answer key, or rubric. Keeps audit votes uncorrelated with the generator, so the majority vote can actually block fabrication.
- **private rubric** — The `rigor_scores` 6-dim scoring rubric held privately by the seam and **never** placed in any generator prompt (same isolation principle as above).
- **content_list.json** — Per-paper block inventory (gitignored). Tier-2 (MinerU) emits it; Tier-1 synthesizes one `{"type":"equation"}` entry per `$$` display block. Drives equation/table fidelity gates.
- **.md_contract.json** — Tracked fidelity contract written beside `corpus/{ID}/{ID}.md`, asserting ingest survival ratios (`EQUATION_SURVIVAL_RATIO` / `TABLE_SURVIVAL_RATIO` = 0.5).
