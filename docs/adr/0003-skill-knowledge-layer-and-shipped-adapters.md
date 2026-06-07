# 3. The skill's logic is a knowledge layer (references/ + sub-skills/); ship deterministic infra adapters, keep LLM seams agent-provided

- Status: Accepted — 2026-06-07. Decision #3 ("keep the LLM seams
  agent-provided, never as code") is **narrowed by ADR-0004**: the seam is a
  synchronous injected callable whose default transport is a locked-down
  `claude -p` adapter (with a direct-API alternative), so the LLM seams now ship
  as adapters too. The knowledge layer and the shipped infra adapters below stand.

## Context

paper-landscape is a **Claude Code skill**, not a standalone app. A cross-model
completion audit (Codex, finding **W1**) flagged it as "not runnable without
writing adapter code" and rated that BLOCKING. An earlier pass overruled W1 as
"optional polish." Two facts then forced a re-examination: (1) six ≥20k★ domain
repos + the three provenance skill-repos were cloned into `docs/reference/`,
giving real evidence of how research skills are actually built; and (2) the
owner's acceptance test sharpened to **invoke-and-go** — enter the workspace,
invoke `/paper-landscape`, and it processes papers.

Inspecting the cloned skills settled the underlying question:

- `AI-Research-SKILLs`: 98 skills, **91 `references/` dirs, 0 `scripts/`** — pure
  knowledge; the agent IS the implementation.
- `academic-research-skills`: 4 skills, 25 reference docs + a 12-file `agents/`
  team; 1 `scripts/` dir.
- Our skill: 52 `.py` files, **empty `references/`, empty `sub-skills/`** — the
  inverse of the field norm.

## Decision

**Verdict on the seam claims (correct).** The four LLM seams (`resolve_analysis`,
`skeptic_votes`, `rigor_scores`, `entailment_judge`, plus discovery's
query-expansion `llm`) are **agent-provided at runtime, not code** — confirmed by
the pure-knowledge skills above. Hard-coding them would be wrong. The three infra
adapters (`http`, `run_cli`, `discover`) are deterministic I/O that must be Python
callables (the agent's WebFetch/Bash are tools, not Python fn args).

**Verdict on the audit's W1 (a real signal, wrong prescription).** Its remedy —
"write scaffolding / a runnable `main()`" — is wrong for the skill model (no
reference skill ships a standalone runner; the host agent orchestrates), so that
overrule stands. But its *smell* was real and was under-weighted: with an empty
`references/`/`sub-skills/` and no shipped infra adapters, the agent had only
SKILL.md prose to wire every seam and would re-improvise `http`/`discover`
plumbing every run. W1 correctly sensed incompleteness; it misattributed it to
missing application code rather than a missing skill knowledge layer.

**Remedy (built).**
1. Externalize the agent-facing logic into a **knowledge layer**: `references/`
   (7 docs: wiring-the-seams, ara-schema, discovery-and-authority, ingest-fidelity,
   naming-and-ledger, landscapes, glossary) + `sub-skills/` (4 LLM-seam roles:
   analyze-paper, g2-skeptic, g3-rigor-reviewer, entailment-judge). A per-seam
   sub-skill also *enforces* isolation — the g2-skeptic role carries no rubric.
2. **Ship the deterministic infra adapters** as tested factories
   (`scripts/adapters.py`: `build_http` / `build_run_cli` / `build_discover`), so
   invoking the skill only requires constructing the LLM seams. This is W1's
   "wiring" done the right way: deterministic glue as code, LLM work as the agent.
3. Keep the LLM seams **injected/agent-provided**, never hard-coded.

## Consequences

- **Invoke-and-go**: enter `~/Coding/paper-rolling/`, invoke `/paper-landscape`,
  lock the campaign (Hard Gate), and a `/loop` tick runs — the agent builds the 4
  LLM seams (+ `expand_llm`); `build_http()`/`build_run_cli()`/`build_discover(...)`
  supply the rest. Quickstart in `SKILL.md`.
- **W1 is resolved** (this ADR supersedes the "optional polish" stance): the
  adapters ship, so "not runnable" no longer holds. `docs/guides/ROADMAP.md` W1 updated.
- **Intentional asymmetry**: LLM seams are injected (agent), infra adapters are
  shipped code. A maintainer who wonders why discovery wiring is code but the
  skeptic is not should read this ADR + `references/wiring-the-seams.md`.
- The `references/` + `sub-skills/` layer is now the primary place skill behavior
  is specified; `scripts/` stays the deterministic substrate it composes.
