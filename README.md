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
  supplies (`discover`, `http`, `run_cli`), and the **LLM-backed seams** — the
  four analysis/audit callables (`resolve_analysis`, `skeptic_votes`,
  `rigor_scores`, `entailment_judge`) **plus** the query-expansion `llm` used
  inside the `discover` callable. Their exact contracts are in `SKILL.md` →
  "Wiring the model seams".
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
| `landscapes.py` | Cross-paper synthesis (corpus-batch-comparator): regenerates `landscapes/{topic}/INDEX.md` + `report.md`. |

`scripts/discovery/` — multi-source discovery + multi-signal OR authority ranking:

| Module | Purpose |
|--------|---------|
| `discover.py` | Orchestration / HUB-facing entry: expand → sources → dedup → DBLP venue enrichment → authority filter → rank. |
| `query_expand.py` | LLM query expansion + OpenAlex topic anchoring (D-发现-6). |
| `openalex.py` | OpenAlex source (uses the polite-pool `mailto`, D-发现-2). |
| `s2.py` | Semantic Scholar source. |
| `arxiv_src.py` | arXiv source (category-restricted). |
| `hf_papers.py` | Hugging Face Papers source (placeholder HF token; `HF_TOKEN` env or anonymous fallback, D-发现-4). |
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
| `branch1_report.py` | branch1 illustrated Chinese report (derived from branch2). |
| `naming.py` | **The single live vault-key authority**: `vault_key`, `derive_name`, `identity_base`, `find_existing_entries`. |
| `ara_schema.py` | ARA Seal Level 1 structural validator. |
| `anchor_lint.py` | Three-layer citation anchor lint (HARD gate) + the anchor-lint CLI. |
| `code_ref.py` | Shallow code analysis with clone-delete-pointer hygiene. |

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

### Data dirs (the accumulated product + transient inputs)

| Dir | Contents |
|-----|----------|
| `corpus/{ID}/` | source + intermediate: `{ID}.md` + `.md_contract.json` (tracked); `{ID}.pdf`, `images/`, `content_list.json` (gitignored, regenerable) |
| `person_vault/{key}/` | human-facing illustrated reports, keyed `{date}_{Name}_{idbase}` |
| `ai_package/{key}/` | AI-facing ARA knowledge packs, same key (1:1 with person_vault) |
| `landscapes/{topic}/` | cross-paper synthesis (`INDEX.md` + `report.md`) |
| `_ledger/` | `processed_ledger.yaml` (single-writer) + `.lock` |
| `_failed/` | per-paper failure records for manual follow-up |
| `config/` | `campaign.yaml.example` (shipped template). The Hard Gate writes the live `campaign.yaml` (locked `topic` / `n_per_tick` / `is_ad_domain`) on first run; a fresh clone has no live config, so the gate fires. |

## Develop / run / test / lint

```bash
uv sync --group dev      # set up the venv
uv run pytest            # run the test suite (the executable spec)
uv run ruff check .      # lint (repo-wide)
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
   a CLI: the runtime agent must supply `discover`, `http`, `run_cli`, and the **four
   model seams**. See `SKILL.md` → "Wiring the model seams" for the exact contract.
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

## The injected seams

The composition is CODE; the runtime injects the seams. Two infrastructure
adapters + a network client are supplied to `run_campaign(...)` — **`discover`**
(the discovery callable, built over the query-expansion `llm` + the source
clients), **`http`**, and **`run_cli`** — and the LLM-backed analysis/audit
callables below. Note there are **five** LLM-backed seams in total: the
query-expansion `llm` (inside `discover`) plus the four here. Each of the four
**MUST** be an **independent Agent-tool invocation** (a fresh sub-agent per call)
so audit votes stay uncorrelated with the generator. `SKILL.md` → "Wiring the
model seams" documents the exact input/output shape of each:

- **`resolve_analysis(md_path, candidate) -> dict`** — the analyzer sub-agent that
  reads the frozen `{ID}.md` and returns the ARA bundle (incl. `headline_metric` /
  `headline_value` / `params_million` the landscape table needs).
- **`skeptic_votes(numbers, source_md, claim_context) -> tuple[SkepticVote, ...]`** —
  the G2 ground-truth-isolated skeptic (sees only the candidate numbers + source MD;
  never the evidence/answer key/rubric). Multi-vote majority hard-blocks fabrication.
- **`rigor_scores(ara_bundle) -> dict`** — the G3 6-dim rigor reviewer (rubric held
  privately by the seam, never in any generator prompt).
- **`entailment_judge(claim, experiment_text) -> tuple[bool, str]`** — the G3
  type-aware entailment check.

## Key dependencies / external services / env

- **`pandoc`** (Tier-1 ingest): `brew install pandoc` / GitHub release binary.
  Converts MathML → LaTeX `$$` in `--to gfm`.
- **`mineru`** (Tier-2 ingest): `uv pip install -U "mineru[core]"` into the shared
  venv. CPU backend (`-b pipeline`); first run downloads multi-GB model weights.
- **OpenAlex polite pool**: a non-secret `mailto` email (D-发现-2) lifts the rate
  limit. Configured via the OpenAlex source's `polite_email`.
- **Hugging Face Papers**: the source ships a **placeholder** HF token
  (`HF_READONLY_TOKEN` in `scripts/discovery/hf_papers.py`, D-发现-4). Set
  `HF_TOKEN` (env, read first) or replace the placeholder with a fine-grained
  READ-ONLY token to raise the rate; with the placeholder unchanged, HF requests
  go out **anonymously** (no Authorization header).
- **API sources**: OpenAlex, Semantic Scholar, arXiv, DBLP, HF Papers — all reached
  through the shared throttled HTTP client (polite pacing).

## What gets tracked vs ignored (基调-D2)

Git tracks **products** (derived knowledge): converted `corpus/{ID}/{ID}.md`,
`.md_contract.json`, `person_vault/`, `ai_package/`, `_ledger/`, `landscapes/`, the
engine + `config/`. Git **ignores inputs** (regenerable): original `*.pdf`, MinerU
`images/` dumps, `content_list.json`, `.cache/`, `.env`, the venv.

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

- Test suite: **green** (`uv run pytest` passes; the count moves as fixes land).
- Lint: **clean** (`uv run ruff check .` → "All checks passed!").
- Quality history: the engine passed internal adversarial review and a cross-model
  (Codex) acceptance audit; the findings from that audit are fixed in the current
  tree.
