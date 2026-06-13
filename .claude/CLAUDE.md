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

Behavioral rules (loaded every session) live in **`.claude/rules/`** —
`00-principles.md` is the control-plane index (load model + the always-loaded set).
Notably `failure-recovery.md`: on a mid-run failure, never `git checkout HEAD` /
reset to "protect" state — resume via the ledger + `_failed/` scenes + `revival.py`.

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

**State / progress / compliance: read it via `scripts.status`, never infer it from
directory existence.** `PYTHONPATH=.claude/skills/paper-landscape uv run python -m
scripts.status` (read-only, lock-free, no-LLM) prints a per-paper table; `--card`
renders an ASCII status card — use it for any "show progress" request; `--json` feeds
external tooling / CI. A paper is promoted-AND-compliant only on a content check, not
because `person_vault/`+`ai_package/` are paired: the ARA must pass the 最终门 level-2
seal (`passes_seal2`) and `report.md` must be new-form (opens with a 评价 section, no
retired `<!--ref/anchor-->`) AND free of ARA-not-loaded markers — a report that has the
评价 header but whose body is a wrong-paper hallucination (engine markers like
`未能读取已验证知识包(ARA)` / `(未解析到结论)`, or a `# ai_package` fallback H1) is its own
`corrupt-report` state, NEVER counted compliant (the bare 评价-present check false-passed
20 such reports on 2026-06-13).

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

`config/llm.yaml` routes each of the 6 seams to a provider. Four provider types
(none vendor-bound): `claude_code` (headless `claude -p`) and `codex_cli` (headless
`codex exec`, no-sandbox) are **local agents**; `openai_compatible` is any
OpenAI-compat API by `{base_url, models, api_key_env}`; `round_robin` is a composite
that alternates calls across `members` (e.g. claude-code + codex). Every seam is
wrapped in `StrictProvider`: on provider failure it raises `EngineAbort` (loud,
aborts the tick) with **no fallback** — a bad key / dead endpoint / wrong model
fails loudly instead of silently draining the Claude Code subscription.
`config/llm.yaml` is **required** and **every seam must be explicitly routed** (a
missing file or an unrouted seam is a hard error — no implicit default). **Concurrency
is per-provider**: each leaf provider sets its own `max_concurrent` (its own
semaphore) — a generous backend runs wide, a token-expensive one narrow; a
`round_robin` total = sum of member caps (claude 5 + codex 5 = 10-wide). `grounded`
mode requires a **grounded-capable** provider (a local agent, or a pool whose every
member is one) — enforced by `grounded_capable`, not by a name/base_url heuristic.
The active config routes the analyzer to `analyzer-pool` (round_robin claude-code +
codex, grounded) and the other 5 seams to `openai_compatible`, keys from `.env`.

## Non-obvious invariants (will bite you otherwise)

- **No hardcoded secrets — every token comes from the gitignored `.env`.** All API
  tokens/keys (`OPENCODE_API_KEY`, `HELLOROBOTAXI_API_KEY`, `HF_TOKEN`) are read
  from `.env`; source carries none. The former hardcoded HF token (D-发现-4
  exemption) was auto-revoked by Hugging Face the moment it hit public git history
  — it now lives only in `.env` (unset `HF_TOKEN` → anonymous HF). Reintroducing a
  hardcoded token is a regression; this is the standing project convention.
- **No silent fallback to the Claude Code subscription** (cost guard). The 6 LLM
  seams have **no default provider and no fallback**: a missing/failing/misconfigured
  provider aborts loudly (`EngineAbort`), surfacing the key/config problem instead
  of quietly degrading to `claude -p`. Reintroducing any default-to-`claude -p` or
  auto-fallback is a **cost regression** — it silently drains the paid main account
  — not a resilience feature. Standing convention.
- **Vault-key authority is `scripts/output/naming.py` ONLY.** Do not add ad-hoc
  naming helpers elsewhere — the divergent duplicates that lived in `paths.py` and
  `ledger/naming.py` were deliberately removed.
- **Single ledger writer (per lock holder).** `_ledger/processed_ledger.yaml` is
  append-only with an LS-1 `.lock`. Two writers exist — the hub (`/loop` tick) and
  the **批次复活赛 driver** (`scripts/revival.py`); both MUST hold the LS-1 lock, so
  they are mutually exclusive (a second start fails fast with `LedgerLockError`) and
  never race. Idempotency keys come from `ledger/naming.py`; vault keys come from
  `output/naming.py` — different concerns.
- **An ARA is never reflex-deleted** (ADR-0011, the one token-expensive product). On
  any failure/abort the staged ARA is MOVED to a `_failed/<key>/` scene (gated by
  `paths.ara_is_nonempty`), never `rm`'d; an `ai_package/` orphan holding a real ARA
  goes to `_failed/_orphans/`, not pruned. Cheap dirs (person_vault, empty shells,
  `.clones`, temp) are still hard-deleted. The `失败现场` is a one-way sink — a
  gate-failed ARA flows in for debug, never back out (revival re-samples). The
  `SpokeCancelled` (stall) path also preserves its built ARA now (moved back to
  staging, scened as `最终门`+`report.md` root for revival) — the former delete-on-stall
  residual is closed.
- **Tracked = products, ignored = regenerable inputs** (基调-D2): converted
  `corpus/{ID}/{ID}.md` + `.md_contract.json` + `content_list.json`, `person_vault/`,
  `ai_package/`, `_ledger/`, `landscapes/`, engine + `config/` are tracked; original
  `*.pdf`, MinerU `images/`, `.env`, `.venv` are ignored. (`content_list.json` moved to
  TRACKED: it is a small but real product — G3's equation gate needs it and it is NOT
  cheaply regenerable here (a MinerU re-run needs a high-RAM pod), so tracking it lets it
  survive worktree removal / fresh checkout. `images/` stay ignored — ~1.2 G for 24 papers
  would make the repo undistributable; figure durability is a separate out-of-repo backup.)
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

**Don't stack ADRs; keep ADRs + `CONTEXT.md` aligned to the code.** On an
architecture/decision change, do NOT append yet another ADR — first prune/merge the
existing ADRs and delete entries that no longer match the code, then fold the new
decision in; update `CONTEXT.md` to the current code state (rewrite/remove stale or
non-compliant terms). Never let ADRs / `CONTEXT.md` drift from the code.

## Tests are the executable spec

When unsure how the engine behaves, read tests before source. Start at
`tests/test_spoke.py` (full per-paper pipeline with fake seams) and
`tests/test_run_campaign.py` (the driver). Tests mirror the `scripts/` package
layout (`tests/discovery/`, `tests/ingest/`, `tests/llm/`, `tests/ledger/`). When
a test fails, fix the implementation, not the test — unless the test itself is
provably wrong.
