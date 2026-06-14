# paper-rolling

> Autonomous AI paper-knowledge-processing engine — the `paper-landscape` v2 workspace.
> License: **CC-BY-NC 4.0** (research-only; see `LICENSE` and `NOTICE`).

`paper-rolling` is a standalone, self-contained git workspace that surveys, ingests,
analyzes, and dual-publishes deep-learning / computer-vision / autonomous-driving /
robotics research papers. It is **both an engine and a product**: the engine lives in
`.claude/skills/paper-landscape/`, and every run accumulates knowledge artifacts
(`corpus/`, `person_vault/`, `ai_package/`, `landscapes/`) directly into this repo.

Given a confirmed research topic, each daily tick discovers authoritative + latest
papers (multi-signal OR ranking), ingests them (arXiv-HTML → MinerU), and emits
**two** products per paper — a human-facing Chinese illustrated report
(`person_vault/`) and an AI-facing ARA knowledge pack (`ai_package/`) — each gated by
adversarial audits, plus cross-paper `landscapes/`. This is **not** a general
installable skill: it hard-assumes the paper-rolling workspace layout.

## Handoff orientation (read this first)

If you are taking this over with no prior context:

- The engine is pure, deterministic, dependency-injected Python under
  `.claude/skills/paper-landscape/scripts/`. There is **no `__main__`** that runs a
  campaign — the runtime (a Claude Code agent) composes the pipeline by calling
  `run_campaign(...)` and supplying the seams (see **Entry points** below).
- The runtime injects the **seams** — everything LLM-backed or I/O-backed lives
  outside the pure core. These are: three **infrastructure adapters** the driver
  supplies (`discover`, `http`, `run_cli`), and the **seven LLM-backed seams**
  (`resolve_analysis`, `skeptic_votes`, `rigor_scores`, `entailment_judge`,
  `expand_llm`, `write_report`, `faithfulness_judge`) **+ the optional `web_search`**
  T4 code-repo-discovery seam — all routed via `config/llm.yaml`, which pins each
  seam's provider and its `tier`/`effort`/`timeout`. Their exact contracts are in
  `SKILL.md` → "Wiring the model seams" (and "The injected seams" below).
- Tests are the executable spec. Start at `tests/test_spoke.py` (full per-paper
  pipeline with fake seams) and `tests/test_run_campaign.py` (the driver).
- To **extend** the engine (new source / tier / gate / branch / cross-paper step),
  read `docs/guides/EXTENDING.md`. Why the architecture is shaped the way it is —
  including which seams are abstracted vs kept concrete — is recorded in
  `docs/adr/`. The full documentation map is `docs/INDEX.md`.

## File-tree / module map

### Engine — `.claude/skills/paper-landscape/`

```
SKILL.md          the skill contract: Hard Gate, /loop cadence, pipeline order,
                  model-seam wiring (authoritative spec for the runtime agent)
references/       engine reference docs
sub-skills/       sub-skill definitions
scripts/          the engine code (packages below)
```

`scripts/` top-level modules:

| Module | Purpose |
|--------|---------|
| `paths.py` | Cross-module layout constants: the vault-branch set (`VAULT_BRANCHES` / `VAULT_BRANCH_PATH_FIELDS`), the `FAILURE_*` classes, and `repo_root`. (NOT the vault-keying authority — that is `output/naming.py`.) |
| `campaign.py` | Campaign Hard Gate (中枢-D1): `CampaignConfig`, `write_campaign`, `gate_needed`, `load_campaign`. |
| `hub.py` | Hub-spoke orchestration (single ledger writer): `run_tick`, `run_campaign_tick`, `Watchdog`, `GateRequired`. Runs LS-4 self-heal before the batch. |
| `spoke.py` | `make_spoke(...)` — the per-paper gated pipeline (ingest → branch2 → G2 → branch1 → G3), serial within one paper. |
| `run_campaign.py` | The production DRIVER: composes `Ledger → make_spoke(seams) → (LS-1 lock) run_campaign_tick`. The `/loop` entry point. |
| `failure_scene.py` | `write_scene(...)` — self-contained failure-scene writer (ADR-0007): a gate hard-fail preserves the staged products + revival inputs into a gitignored `_failed/<key>/`, via crash-safe `.new`/`.old` atomic rename. |
| `revival.py` | Batch-revival driver (`revive_all`, CLI `-m scripts.revival`): scans `_failed/`, branch-level replay reusing upstream products, promote→record→delete; the SECOND legitimate ledger writer (holds the LS-1 lock, mutually exclusive with `/loop`). |
| `engine_version.py` | `current_commit(...)` — engine short-hash for failure-scene diagnostics (not a reuse key). |
| `landscapes.py` | Cross-paper synthesis (corpus-batch-comparator): regenerates `landscapes/{topic}/INDEX.md` + `report.md`. |

`scripts/discovery/` — multi-source discovery + multi-signal OR authority ranking:

| Module | Purpose |
|--------|---------|
| `discover.py` | Orchestration / HUB-facing entry: expand → sources → dedup → DBLP venue enrichment → authority filter → rank. |
| `query_expand.py` | LLM query expansion + OpenAlex topic anchoring (D-发现-6). |
| `openalex.py` | OpenAlex source (uses the polite-pool `mailto`, D-发现-2). |
| `s2.py` | Semantic Scholar source. |
| `arxiv_src.py` | arXiv source (category-restricted). |
| `hf_papers.py` | Hugging Face Papers source. READ-ONLY `HF_TOKEN` from the gitignored `.env` only — nothing hardcoded; unset → anonymous (D-发现-4). |
| `dblp.py` | DBLP venue-authority source (`venue_for_title`) — enrichment, feeds the S2 venue signal. |
| `authority.py` | Multi-signal OR authority scorer (ADR-0001): S1 cite / S2 venue / S3 institution / S4 heat. |
| `dedup.py` | Cross-source dedup + field merge (D-发现-7). |
| `crosscheck.py` | DOI cross-check. |
| `contamination.py` | Preprint / unreviewed trust flag (吸收-D2). |
| `cache.py` | Persistent verification cache for the resolvers. |
| `http_client.py` | HUB-owned throttled HTTP client (polite-pool pacing). |
| `_text.py` | Shared title-similarity + retry-budget helpers. |

`scripts/ingest/` — 2-tier PDF→MD with the MD-only contract:

| Module | Purpose |
|--------|---------|
| `ingest.py` | Orchestrator: Tier-1 → Tier-2 → quarantine; writes `.md_contract.json`. |
| `tier1_html.py` | Tier-1: arXiv official HTML (LaTeXML) → GFM via `pandoc`. |
| `tier2_mineru.py` | Tier-2: download PDF + MinerU CLI (CPU) → MD + `images/` + `content_list.json`. |
| `contract.py` | MD-only contract: provenance record + content hashing + equation-block counting. |

`scripts/llm/` — pluggable LLM provider layer + seam factory:

| Module | Purpose |
|--------|---------|
| `providers.py` | `LLMProvider` protocol + 4 provider types: `ClaudeCodeProvider` (claude -p) & `CodexCliProvider` (codex exec, no-sandbox) — **local agents** (`grounded_capable`); `OpenAICompatibleProvider` (any OpenAI-compat API); `RoundRobinProvider` (composite — alternates calls across member providers, e.g. claude+codex → 10-wide). Each leaf owns a **per-instance `max_concurrent` semaphore** (per-provider cap, not global). `StrictProvider` wraps every routed provider → on failure raises `EngineAbort`, **no fallback** (a bad key/endpoint fails loud, never silently drains the Claude Code subscription). |
| `config.py` | `LLMConfig` from `config/llm.yaml` (**required**; every seam must be explicitly routed — no default provider): loads per-seam provider routing + execution modes (inline / grounded / agent_team). |
| `seams.py` | `build_seams()` factory: constructs the 7 LLM seams (analyzer, skeptic, rigor, entailment, expand, writer, faithfulness) with provider routing + `StrictProvider` (no-fallback) wrapping. |
| `analyzer.py` | `analyze_chunked(...)` — grounded analyzer (chunks large MD, parallel analyst calls, formula-fidelity discipline). |
| `writer.py` | `write_human_sections(...)` + `curate_figures(...)` — human-chain LLM writer (vivid Chinese prose + selective figure curation: mandatory arch + top-N results). |
| `jsonparse.py` | `extract_json(...)` — tolerant JSON extraction (handles code fences, LaTeX escapes, leading prose). |

`scripts/ledger/` — single-writer processed-state + idempotency:

| Module | Purpose |
|--------|---------|
| `store.py` | `Ledger` (append-only YAML, atomic write, LS-1 `.lock`, LS-3 crash-resume, LS-4 `consistency_check`), `LedgerLockError`, `overwrite_vault_entry`, the `/paper-landscape-invalidate` CLI. |
| `corpus.py` | `corpus.jsonl` — the discovered-paper known set. |
| `naming.py` | Ledger version/identity idempotency keys: `identity_key`, `version_key`. (NOT vault naming.) |

`scripts/output/` — atomic dual-output (OT-5):

| Module | Purpose |
|--------|---------|
| `produce.py` | `produce_outputs(...)` — builds branch2 then branch1 in staging, runs gates, promotes both-or-neither. |
| `branch2_ara.py` | branch2 ARA producer (runs first). |
| `branch1_llm.py` | branch1 LLM-written human chain (vivid Chinese sections + grounded assembly + figure curation + self-contained HTML). Wired via optional `write_report` seam. |
| `branch1_report.py` | branch1 thin deterministic renderer (fallback when no `write_report` seam; from analysis → markdown template). |
| `branch1_gate.py` | branch1 opening 「评价」 (ADR-0012 rev): `build_assessment` assembles a NON-blocking `## 评价` note — (b) report prose numbers not in the verified **ARA** (says "未核对" if the ARA is unreadable, never a false all-clear) + (c) an advisory fail-soft LLM judge note + the ARA's `AUDIT_FLAGS` body. NEVER raises; prepended by both branch1 paths. branch1 has no hard gate. |
| `naming.py` | **The single live vault-key authority**: `vault_key`, `derive_name`, `identity_base`, `find_existing_entries`. |
| `ara_schema.py` | ARA Seal Level 1 structural validator. |
| `anchor_lint.py` | Three-layer citation anchor lint (HARD gate) + the anchor-lint CLI. |
| `figures.py` | Original-figure inventory: extract `(ref, caption)` from the MD; flag the architecture figure; copy selected images (branch1). |
| `code_ref.py` | code_ref pointer: clone-verify ordered repo candidates → state (`found` / `searched-not-found` / `author-declared-closed` / `unreachable`), clone-delete hygiene. `found` cites SOURCE locations only; unresolved innovations are OMITTED (never `_not found_` rows). |
| `repo_resolve.py` | code_ref repo-resolution cascade (highest-trust-first): T2a offline PwC `is_official` + **T1a paper-declared** (author "our code is at X" → official trust) + T1b paper-text grep + discovery + T2b HF-live (repo + linked HF artifacts) + T4 websearch; `make_repo_resolver()` composes the production resolver. |
| `pwc_lookup.py` | T2a offline `arxiv_id → official repo` lookup over the shipped gzipped Papers-with-Code `is_official` table. |
| `check_ara_bundle.py` | ARA bundle regression gate (审计 §6.1): code_ref three-state + evidence tables + review↔tables drift. Importable `check_bundle` + sweep CLI. |

`scripts/audit/` — the adversarial gates:

| Module | Purpose |
|--------|---------|
| `types.py` | Shared audit vocabulary: `Finding`, `GateVerdict`, `Severity`, `ClaimRecord`, the seam Protocols. |
| `ara_tree.py` | Canonical read layer over a paper's `ara/` tree (claim registry, dir lookup); shared by G2 + G3 (ADR-0002). |
| `g2_data_fidelity.py` | G2 data-fidelity gate (number/claim fidelity, multi-vote skeptic, hard-block on fabrication). |
| `g3_seal.py` | G3 seal: branch1↔MD anchors + equation fidelity + type-aware entailment + 6-dim rigor. |
| `equation_fidelity.py` | Mechanical equation-block count check (no LLM). |
| `entailment.py` | Type-aware entailment table check. |
| `anchor_resolution.py` | branch1↔MD anchor resolution. |
| `rigor_rubric.py` | 6-dim rigor rubric (ARA Seal Level 2). |
| `gate_runner.py` | Bounded gate runner: max-N rounds, then quarantine + flag. |

`scripts/tools/` — offline maintenance scripts (NOT runtime; run via `uv run <path>`):

| Script | Purpose |
|--------|---------|
| `build_pwc_table.py` | Build the shipped `data/pwc_official_arxiv2repo.tsv.gz` from the Papers-with-Code `is_official` dump (offline; uses duckdb). |
| `rescan_code_ref.py` | Offline spot-check of code_ref resolution (T1+T2a) over the local `corpus/`. |

`data/` — shipped engine data (tracked): `pwc_official_arxiv2repo.tsv.gz` — the
offline `arxiv_id → official repo` lookup (T2a), read with stdlib gzip at runtime.

### Data dirs (the accumulated product + transient inputs)

| Dir | Contents |
|-----|----------|
| `corpus/{ID}/` | source + intermediate: `{ID}.md` + `.md_contract.json` + `content_list.json` (tracked — `content_list.json` is a small product G3's equation gate needs, not cheaply regenerable here); `{ID}.pdf`, `images/` (gitignored, regenerable) |
| `person_vault/{key}/` | human-facing illustrated reports, keyed `{date}_{Name}_{idbase}` |
| `ai_package/{key}/` | AI-facing ARA knowledge packs, same key (1:1 with person_vault) |
| `landscapes/{topic}/` | cross-paper synthesis (`INDEX.md` + `report.md`) |
| `_ledger/` | `processed_ledger.yaml` (single-writer) + `.lock` |
| `_failed/` | per-paper failure records for manual follow-up |
| `config/` | `campaign.yaml` (locked topic / n_per_tick / force_include by Hard Gate); `llm.yaml` (per-seam provider routing + execution modes, **required** — every seam explicitly routed; no default provider, no silent `claude -p` fallback); `audit.yaml` (audit knobs: skeptic_votes, max_gate_rounds, data_fidelity tolerance, optional). |

## Develop / run / test / lint

```bash
uv sync --group dev      # set up the venv
uv run pytest            # run the test suite (the executable spec)
uv run ruff check .claude/skills/paper-landscape/scripts/   # lint the ENGINE source
# NB: scope ruff to the engine source (and tests/), NOT `ruff check .` repo-wide
# (docs/handoff/ is gitignored session scratch, outside the gate; see .claude/CLAUDE.md).
# Environment preflight — verify pandoc + mineru + runtime deps before a campaign
# (exit 1 + install hints if any is missing; the skill runs this FIRST as a gate):
PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.preflight
```

There is no `validate` target beyond the test suite + ruff; "green pytest + clean
ruff" is the validation gate.

## Entry points (everything triggerable)

1. **The `/paper-landscape` skill.** The primary entry — read
   `.claude/skills/paper-landscape/SKILL.md`. First invocation runs the campaign
   **Hard Gate** (HITL): you confirm a precise **topic** and a per-tick paper
   **count** (`n_per_tick`), locked into `config/campaign.yaml`.

   ```bash
   cd ~/Coding/paper-rolling
   # In Claude Code, invoke the workspace-local skill:
   /paper-landscape
   ```

2. **The daily `/loop` tick.** After the gate, schedule incremental daily runs; each
   tick processes N *new* papers autonomously (no mid-pipeline questions). Re-running
   the Hard Gate is only needed to change the topic or the per-tick count.

   ```bash
   /loop 1d /paper-landscape
   ```

3. **`run_campaign()` — the composition driver** (`scripts/run_campaign.py`). This is
   what the `/loop` tick actually drives. It composes
   `Ledger → make_spoke(seams) → (LS-1 lock) run_campaign_tick`. It is a function, not
   a CLI: the runtime agent must supply `discover`, `http`, `run_cli`, and the **five
   analysis/audit model seams** (incl. the branch1 「评价」 `faithfulness_judge` note-writer, ADR-0012 rev).
   See `SKILL.md` → "Wiring the model seams" for the exact contract.
   Invoking the module directly prints a usage message and exits (it is intentionally
   not a silent no-op):

   ```bash
   PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.run_campaign
   ```

4. **`/paper-landscape-invalidate` — force-reprocess CLI** (`scripts/invalidate.py`,
   wrapping `scripts.ledger.store.main`). Soft-deletes ledger rows so a paper is
   reprocessed next tick:

   ```bash
   PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.invalidate \
       <key>... --topic-dir .
   ```

5. **anchor-lint CLI** (`scripts/output/anchor_lint.py`). Lints citation anchors in a
   markdown report:

   ```bash
   PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.output.anchor_lint <file>...
   ```

6. **bibliography export CLI** (`scripts/bibliography.py`). Emits `references.bib`
   (BibTeX) + `references.csl.json` (CSL-JSON) for the sealed corpus:

   ```bash
   PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.bibliography --topic-dir .
   ```

7. **`scripts.status` — the read-only state surface** (`scripts/status.py`). The
   canonical "where does every paper stand?" view: per-paper compliance, the
   ARA-sealed → report-compliant funnel, and a ledger↔product divergence warning.
   Lock-free, no-LLM, safe to run any time (even mid-tick). **Read state from here —
   never infer it from directory existence.** `--card` renders an at-a-glance ASCII
   card; `--json` feeds CI / external tooling:

   ```bash
   PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.status [--card | --json]
   ```

8. **`scripts.preflight` — the environment gate** (`scripts/preflight.py`). Verifies
   `pandoc` + `mineru` + runtime deps before a campaign; exits 1 with install hints if
   any is missing. The skill runs this FIRST as a hard gate:

   ```bash
   PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.preflight
   ```

9. **`scripts.revival` — the batch-revival driver** (`scripts/revival.py`). Scans
   `_failed/`, replays each failed paper at branch granularity (reusing upstream
   products), and promotes→records→cleans. The SECOND legitimate ledger writer (holds
   the LS-1 lock, so it is mutually exclusive with a `/loop` tick):

   ```bash
   PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.revival
   ```

10. **`scripts.output.check_ara_bundle` — the ARA regression gate** (sweep CLI).
    Asserts, per published ARA, the code_ref three-state honesty (no `_not found_`
    rows, no non-source locations, no closed-source mislabel), non-empty evidence
    tables, and no review↔tables drift. Exits non-zero on any violation:

    ```bash
    PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.output.check_ara_bundle
    ```

11. **终审修订 (`final-review` sub-skill) — the OPTIONAL post-run revision layer**
    (ADR-0013; `sub-skills/final-review/SKILL.md` + engine `output/final_review.py` /
    `demote.py` / `revival.revive_all(only_keys=…)`). After a `/loop` run, the main
    session fans out one Opus sub-agent per published product to "revise or send back to
    the foundry" against the source MD: small flaws are surgically fixed in place
    (REVISE → a `final_review.json` marker), and products with no trustworthy base
    (read-wrong-paper / wholesale-fabrication / rewrite-grade) are demoted to a
    branch2-root failure scene and re-analyzed via the revival path (FAIL). **Default
    OFF, operator-triggered, NOT wired into `/loop`** — the engine side is pure
    deterministic functions, the revision judgment lives in the sub-agents, and the
    ledger / scenes / revival are written only by the main session (single-writer LS-1).
    Terminal-review state surfaces in `scripts.status` (`final_reviewed`).

## The injected seams

The composition is CODE; the runtime injects the seams. Three infrastructure
adapters are supplied to `run_campaign(...)` — **`discover`** (the discovery
callable, built over the query-expansion `llm` + the source clients), **`http`**,
and **`run_cli`** — plus the **seven LLM-backed seams** (+ the optional `web_search`
T4 code-repo-discovery seam), all routed via `config/llm.yaml` from
`scripts/llm.seams.build_seams()`, which also pins each seam's `tier`/`effort`/`timeout`
(the master config owns every model choice, not the code). Each LLM seam
**MUST** be an **independent Agent-tool invocation** (a fresh sub-agent per call)
so audit votes stay uncorrelated with the generator. `SKILL.md` → "Wiring the
model seams" documents the exact input/output shape of each:

- **`resolve_analysis(md_path, candidate) -> dict`** — the analyzer sub-agent (in
  grounded mode, reads frozen `{ID}.md` itself) that returns the ARA bundle (incl.
  `headline_metric` / `headline_value` / `params_million` landscape table needs).
- **`skeptic_votes(numbers, source_md, claim_context) -> tuple[SkepticVote, ...]`** —
  the G2 ground-truth-isolated skeptic (sees only the candidate numbers + source MD;
  never the evidence/answer key/rubric). Multi-vote majority hard-blocks fabrication.
- **`rigor_scores(ara_bundle) -> dict`** — the G3 6-dim rigor reviewer (rubric held
  privately by the seam, never in any generator prompt).
- **`entailment_judge(claim, experiment_text) -> tuple[bool, str]`** — the G3
  type-aware entailment check.
- **`expand_llm(topic) -> list[str]`** — the discovery query expander (cheap seam,
  converts a single topic into multiple search queries for multi-source discovery).
- **`write_report(ara_bundle, figures) -> dict`** — the human-chain LLM writer
  (optional; if provided, generates vivid Chinese prose + grounded assembly;
  if omitted, branch1 falls back to thin deterministic renderer).
- **`faithfulness_judge(report_text, ara_dir, *, ungrounded=None) -> str`** — the branch1
  「评价」 (c) note-writer (ADR-0012 rev): compares the human report against the verified
  ARA and returns a Chinese prose note. ADVISORY + fail-SOFT (any seam/ARA error → a
  neutral note; NEVER raises, NEVER blocks). Ground-truth-isolated from `write_report`
  (tier=fast → a model ≠ the writer's).

## Key dependencies / external services / env

- **`pandoc`** (Tier-1 ingest): `brew install pandoc` / GitHub release binary.
  Converts MathML → LaTeX `$$` in `--to gfm`.
- **`mineru`** (Tier-2 ingest): from the repo root (after `uv sync`),
  `uv pip install -U "mineru[core]"` — it installs into **this project's `.venv`**
  (uv's project-local env; there is no shared venv). CPU backend (`-b pipeline`).
  First run downloads multi-GB model weights into the **standard model cache**
  (`~/.cache/huggingface` by default, or `~/.cache/modelscope` via
  `MINERU_MODEL_SOURCE=modelscope`) — a user-level cache, never the project tree.
- **OpenAlex polite pool**: a non-secret `mailto` email (D-发现-2) lifts the rate
  limit. Configured via the OpenAlex source's `polite_email`.
- **Hugging Face Papers**: the source reads a **READ-ONLY `HF_TOKEN` from the
  gitignored `.env` only** (`scripts/discovery/hf_papers.py`, D-发现-4) — nothing is
  hardcoded in source (an earlier shipped constant was auto-revoked by HF once it
  hit public git history). Unset `HF_TOKEN` → HF requests fall back to **anonymous**
  (lower rate). `HF_TOKEN` also powers T2b live code_ref resolution (`api/papers/{id}`).
- **API sources**: OpenAlex, Semantic Scholar, arXiv, DBLP, HF Papers — all reached
  through the shared throttled HTTP client (polite pacing).

## What gets tracked vs ignored (基调-D2)

Git tracks **products** (derived knowledge): converted `corpus/{ID}/{ID}.md`,
`.md_contract.json`, `content_list.json` (a small but real product — G3's equation
gate needs it and a MinerU re-run needs a high-RAM pod, so it is NOT cheaply
regenerable here), `person_vault/`, `ai_package/`, `_ledger/`, `landscapes/`, the
engine + `config/`. Git **ignores inputs** (regenerable): original `*.pdf`, MinerU
`images/` dumps (~1.2 G for 24 papers — would make the repo undistributable),
`.cache/`, `.env`, the venv.

## Known limits / gotchas

- **Tier-1 equation gate is a trusted pass-through.** Only Tier-2 (MinerU, which emits
  `content_list.json`) has a real mechanical equation-fidelity check; the Tier-1
  (pandoc) path synthesizes a minimal `content_list.json` so the gate passes by
  construction. Treat Tier-1 equation fidelity as trusted, not verified.
- **LS-6: unbounded local growth is accepted.** Local original PDFs + image dumps +
  git-tracked branch1 figures grow without bound across long campaigns. There is **no
  capacity cap and no auto-archival** by design. Under disk pressure, prune
  `corpus/**/{*.pdf,images/}` manually — they are gitignored, regenerable inputs and
  removing them does not affect tracked products.
- **Research-only license.** CC-BY-NC 4.0 — non-commercial use only (see `LICENSE`,
  `NOTICE`).
- **Vault-key authority is `output/naming.py` only.** Do not reach for ad-hoc naming
  helpers elsewhere; the divergent duplicates that used to live in `paths.py` and
  `ledger/naming.py` were removed.

## Current status + validation

> Validated **2026-06-15** (commit moves as fixes land — re-run the commands below to
> re-verify; read live per-paper state from `scripts.status`, the authority).

- **Corpus: 33/33 papers compliant AND terminally reviewed** — every paper has a
  sealed ARA (G3 level-2 `passes_seal2`) AND a new-form human report (opens with
  `## 评价`, no retired anchors, no ARA-not-loaded body), and every code_ref is honest
  (no fabricated `_not found_` rows / non-source locations). The optional ADR-0013
  terminal-review layer is also **complete for all 33** (`final_reviewed` true; markers
  in `ai_package/*/ara/final_review.json`). Confirm with `… -m scripts.status --card`
  (read-only; its funnel shows `终审 33`) and `… -m scripts.output.check_ara_bundle`
  (regression gate → `33 bundle(s), 0 violation(s)`). The newest paper, DriveWAM
  (`2605.28544`), was added via a full normal-trigger pipeline run (ingest → ARA → G2 →
  report → G3 → publish → terminal review).
- **Test suite: green** — `uv run pytest` → **638 passed**.
- **Lint: clean** — `uv run ruff check .claude/skills/paper-landscape/scripts/ tests/`
  → "All checks passed!". NB: the gate is engine+tests-scoped, NOT repo-wide
  `ruff check .` (docs/handoff/ is gitignored session scratch, outside the gate — see
  `.claude/CLAUDE.md`).
- **Known non-defects** (normal, not gaps): some papers have **no public code repo**
  (e.g. OmniDreams' only release is FlashDreams, a serving stack, not the model) —
  `code_ref` honestly says "No public repository found"; not every paper open-sources
  code. Minor imperfections in a long human report are tolerated **and flagged** in
  the opening `## 评价` note. Tier-1 (pandoc) equation fidelity is trusted-not-verified
  by construction (see Known limits).
- **Quality history**: the engine passed internal adversarial review and repeated
  cross-model (Codex) acceptance audits; each audit's findings are fixed in the
  current tree.
