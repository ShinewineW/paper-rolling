# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`paper-rolling` is **both an engine and a product**. The engine — a pure,
deterministic, dependency-injected Python pipeline — lives entirely under
`.claude/skills/paper-landscape/scripts/`. Every run accumulates knowledge
artifacts (`corpus/`, `person_vault/`, `ai_package/`, `landscapes/`) directly
into this same repo. It is **not** a general installable skill; it hard-assumes
the paper-rolling workspace layout.

Three documents are authoritative — read them before non-trivial work; do not
re-derive their content here:
- **`README.md`** — full module map, entry points, env/services, gotchas.
- **`.claude/skills/paper-landscape/SKILL.md`** — the runtime contract: Hard
  Gate, `/loop` cadence, pipeline order, and **"Wiring the model seams"** (exact
  seam input/output shapes).
- **`docs/INDEX.md`** — documentation map **and governance rules** for `docs/`.

## Commands

```bash
uv sync --group dev                 # set up the project-local .venv
uv run pytest                       # full suite — THE executable spec (pythonpath preconfigured)
uv run pytest tests/test_spoke.py -v          # one file
uv run pytest tests/test_spoke.py::test_name  # one test
uv run pytest -k discovery          # by keyword
uv run ruff check .claude/skills/paper-landscape/scripts/   # lint the ENGINE source
```

"Green pytest + clean ruff on the engine source" is the only validation gate —
there is no separate `validate` target. `pyproject.toml` excludes the dual-chain
products (`ai_package/`, `person_vault/`) from ruff, but `docs/handoff/` driver
scripts are intentionally NOT excluded and still carry lint noise — so scope the
gate to the engine source (and `tests/` if checking tests), not `ruff check .`
repo-wide.

**PYTHONPATH gotcha:** `uv run pytest` works without setup (`pyproject.toml` sets
`pythonpath = [".claude/skills/paper-landscape"]`). But the standalone module
CLIs are **not** on that path — invoke them with the prefix:
`PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.<module>`
(e.g. `scripts.preflight`, `scripts.run_campaign`, `scripts.invalidate`,
`scripts.output.anchor_lint`, `scripts.bibliography`). Run `scripts.preflight`
first — it gates on `pandoc` + `mineru` being installed.

## Architecture: the seam-injection model (the key mental model)

The engine is a **pure core composed at runtime**. There is **no `__main__` that
runs a campaign** — a Claude Code agent (the runtime) calls `run_campaign(...)`
and **injects the seams**. Everything LLM-backed or I/O-backed lives outside the
pure core:

- **3 infrastructure adapters** the driver supplies: `discover`, `http`, `run_cli`.
- **6 LLM-backed seams**, all routed through `config/llm.yaml` via
  `scripts/llm/seams.py::build_seams()`: `resolve_analysis` (analyzer),
  `skeptic_votes` (G2), `rigor_scores` (G3), `entailment_judge` (G3),
  `expand_llm` (discovery), `write_report` (human-chain writer, optional).

Each LLM seam **MUST** be an **independent Agent-tool invocation** (a fresh
sub-agent per call) so audit votes stay statistically uncorrelated with the
generator they're auditing — this ground-truth isolation is the core integrity
property. The G2 skeptic sees only candidate numbers + source MD (never the
answer key / rubric); the G3 rigor rubric is held privately by the seam.

**Composition flow** (`scripts/run_campaign.py`, the `/loop` driver):
`Ledger → make_spoke(seams) → (LS-1 lock) run_campaign_tick`. Invoking the module
directly prints usage and exits — it is intentionally not a silent no-op.

### Per-paper pipeline (the "spoke")

`make_spoke(...)` runs serially per paper: **ingest → branch2 (ARA) → G2 →
branch1 (human report) → G3**. Two products per paper, published **atomically
(both-or-neither)**: the AI-facing ARA pack (`ai_package/`) and the human-facing
Chinese illustrated report (`person_vault/`), 1:1 keyed. Two adversarial gates
guard them: **G2** = data/number fidelity (hard-blocks fabrication via multi-vote
skeptic); **G3** = seal (anchor + equation fidelity + entailment + 6-dim rigor).

### Discovery & ingest

- **Discovery** (`scripts/discovery/`): multi-source (OpenAlex / S2 / arXiv / DBLP
  / HF Papers) → dedup → **multi-signal OR authority ranking** (ADR-0001: cite OR
  venue OR institution OR heat; no single hard citation gate).
- **Ingest** (`scripts/ingest/`): 2-tier PDF→MD. Tier-1 = arXiv HTML via `pandoc`;
  Tier-2 = MinerU CLI (CPU). MD-only contract with provenance + equation-block
  hashing.

## LLM provider routing

`config/llm.yaml` routes each of the 6 seams to a provider. Two provider types
(neither vendor-bound): `claude_code` (headless `claude -p`, the bottom-line
default + mandatory fallback) and `openai_compatible` (any OpenAI-compat API by
`{base_url, models, api_key_env}`). Every seam is wrapped in `FallbackProvider`
(primary → claude-code fallback → `EngineAbort` if both fail), so a missing API
key degrades gracefully rather than crashing. The active config routes 5 seams to
the `opencode` provider, which reads `OPENCODE_API_KEY` from `.env` (gitignored).
Delete `config/llm.yaml` to route everything to `claude -p`.

## Non-obvious invariants (will bite you otherwise)

- **No hardcoded secrets — every token comes from the gitignored `.env`.** All API
  tokens/keys (`OPENCODE_API_KEY`, `HELLOROBOTAXI_API_KEY`, `HF_TOKEN`) are read
  from `.env`; source carries none. The former hardcoded HF token (D-发现-4
  exemption) was auto-revoked by Hugging Face the moment it hit public git history
  — it now lives only in `.env` (unset `HF_TOKEN` → anonymous HF). Reintroducing a
  hardcoded token is a regression; this is the standing project convention.
- **Vault-key authority is `scripts/output/naming.py` ONLY.** Do not add ad-hoc
  naming helpers elsewhere — the divergent duplicates that lived in `paths.py` and
  `ledger/naming.py` were deliberately removed.
- **Single ledger writer (per lock holder).** `_ledger/processed_ledger.yaml` is
  append-only with an LS-1 `.lock`. Two writers exist — the hub (`/loop` tick) and
  the **批次复活赛 driver** (`scripts/revival.py`); both MUST hold the LS-1 lock, so
  they are mutually exclusive (a second start fails fast with `LedgerLockError`) and
  never race. Idempotency keys come from `ledger/naming.py`; vault keys come from
  `output/naming.py` — different concerns.
- **Tracked = products, ignored = regenerable inputs** (基调-D2): converted
  `corpus/{ID}/{ID}.md` + `.md_contract.json`, `person_vault/`, `ai_package/`,
  `_ledger/`, `landscapes/`, engine + `config/` are tracked; original `*.pdf`,
  MinerU `images/`, `content_list.json`, `.env`, `.venv` are ignored.
- **Tier-1 equation fidelity is trusted, not verified** — only Tier-2 (MinerU)
  gets a real mechanical equation check; the pandoc path synthesizes a passing
  `content_list.json` by construction.
- **No mid-pipeline questions** during a `/loop` tick — all HITL happens once at
  the campaign Hard Gate (`config/campaign.yaml`).

## docs/ governance (enforced by docs/INDEX.md)

`docs/INDEX.md` is the governing index. Before adding any directory under `docs/`,
**register it in INDEX.md first**. Fixed conventions: design **and** impl plans go
to `spec/` (no `plans/` folder); `reference/` holds reference inputs (upstream
repos, blogs) — gitignored except their `INDEX.md`; `reports/` holds
point-in-time observations/audits of this repo; `adr/` is self-managed by the
`mp-grill-me` skill (exempt); `guides/codemaps/` holds the architecture maps
(code-awareness). Doc metadata follows
`~/.claude/rules/common/docs-metadata-standard.md`.

## Tests are the executable spec

When unsure how the engine behaves, read tests before source. Start at
`tests/test_spoke.py` (full per-paper pipeline with fake seams) and
`tests/test_run_campaign.py` (the driver). Tests mirror the `scripts/` package
layout (`tests/discovery/`, `tests/ingest/`, `tests/llm/`, `tests/ledger/`). When
a test fails, fix the implementation, not the test — unless the test itself is
provably wrong.
