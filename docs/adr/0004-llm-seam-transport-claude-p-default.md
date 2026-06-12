# 4. The LLM seam is a synchronous injected callable; default transport is locked-down `claude -p`, with a direct-API alternative; in-session Agent-tool only for interactive survey

- Status: Accepted — 2026-06-07. **部分被取代(2026-06-12 provider 路由重构)**:决策 #1
  (seam = 同步注入的 Python callable,非 in-session Agent-tool)与 #4(不可注入的 in-session
  sub-agent 不用于强制流水线)**仍有效**;但 #2"**默认传输 = `claude -p`**"已被**取代**——
  现状是 `config/llm.yaml` **必填、每个 seam 显式路由、无默认、无回退**(失败即 `EngineAbort`),
  详见 `.claude/CLAUDE.md`「LLM provider routing」。
- Amends: ADR-0003 (its decision #3 — "keep the LLM seams agent-provided, never as
  code" — is narrowed here; the other halves of 0003, the knowledge layer and the
  shipped infra adapters, stand unchanged).

## Context

ADR-0003 decided the four LLM seams (ADR-0012 later added a fifth,
`faithfulness_judge`) are "agent-provided at runtime, not code" and
that hard-coding them "would be wrong." That framing left one thing unresolved:
**what, mechanically, IS an agent-provided seam** at the point `run_campaign(...)`
calls it? The wiring contract (`SKILL.md`, `references/wiring-the-seams.md`,
`run_campaign.py` docstring) answered it three times with the phrase **"each LLM
seam MUST be backed by an independent Agent-tool invocation (a fresh sub-agent per
call)."** The only real campaign run to date (a scratch harness under
`attn_sink/cosmos_trial/`) instead realized the seams as headless **`claude -p`
subprocess** calls, and it failed 5/5 — which read as "`claude -p` is the wrong
mechanism."

Two structural facts, established by research (Claude Agent SDK / Claude Code docs
+ the vendored reference repos), force a sharper decision:

1. **A synchronous, gate-enforcing `run_campaign` requires the seam to be a Python
   callable.** Python launched under `uv run` (a Bash subprocess the host agent
   spawned) **cannot reach the host agent's Agent tool** — tool execution is
   one-directional, no reverse channel, no native yield/resume bridge. So a *real*
   in-session Agent-tool sub-agent **cannot** be injected into `run_campaign(...)`.
   Taken literally, "MUST be an Agent-tool invocation" is unsatisfiable together
   with the code-owned composition that is the engine's whole moat (G2/G3 ordering
   + the LS-1 single-writer ledger enforced by CODE, not prose).
2. **The reference paper-rolling drew its G2/G3 from does exactly what we do.**
   `academic-research-skills/scripts/claim_audit_pipeline.py` is "the executable
   face" of an agent prose contract: a deterministic pipeline with a
   **dependency-injected `judge_fn`/`retrieve_fn`** seam — fake in tests,
   "production wires a real client," fault classes `judge_api_error`/`judge_timeout`
   — i.e. an out-of-process model client, **not** an in-session sub-agent. No
   reference repo realizes an *enforced* pipeline with in-session Agent-tool seams;
   the pure-knowledge skills that are fully agent-driven have no gates to enforce.

A 10-dimension head-to-head (gate-enforcement, ground-truth isolation, headless
`/loop`, the 363-test fake-seam suite, blast radius, reversibility, cost,
auth/onboarding, ADR/reference fidelity, observability) scored the injected-callable
seam over the in-session Agent-tool seam **9–1**; the Agent-tool seam wins only on
auth/onboarding (it reuses the cloner's Claude Code session, no API key).

## Decision

**1. The seam's binding contract is a synchronous injected Python callable** — the
existing `resolve_analysis` / `SkepticVoteFn` / `RigorScoreFn` / `EntailmentJudgeFn`
signatures, unchanged. The MUST is the **isolation/independence property** (a fresh,
uncorrelated context per call; fail-closed; the G2 skeptic and G3 rubric never see
the answer key), **not** any particular host mechanism. "Independent Agent-tool
invocation" was describing that isolation property, and is reworded accordingly.

**2. Default transport = a locked-down `claude -p` adapter.** It reuses the
machine's Claude Code **subscription** auth (clone-and-go, no separate API key),
which is why it is the default for an open-source skill. "Locked-down" is required:
`claude -p` is a full agent, so the adapter MUST run it as a single-shot,
non-agentic call — all tools disabled, single turn, no cwd/`CLAUDE.md`/skills/MCP
pickup, an explicit system prompt — otherwise the agentic surface can break
determinism and (critically) the G2 skeptic's ground-truth isolation. The earlier
"`claude -p` is wrong" verdict is recorded as a **transport-hardening** problem
(rate-limit/auth/timeout/no-lockdown), **not** an architecture defect.

**3. Alternative transport = a direct Anthropic Messages-API adapter**, behind the
**same** injection point. It costs an `ANTHROPIC_API_KEY` (metered, separate from
the subscription) but unlocks prompt caching on the large static skeptic/rigor
system prompts, the Batch API for nightly `/loop` runs, schema-forced JSON, and
isolation that is airtight by construction. Operators pick the transport per
deployment; the engine never knows which is bound.

**4. The pure in-session Agent-tool sub-agent (乙) is NOT used for the enforced
pipeline.** It cannot be injected into the synchronous, gate-enforcing
`run_campaign` (fact 1 above), so its only in-process form hands gate ordering and
the single-writer ledger back to agent discretion — the exact "unenforceable prose
wiring" `run_campaign.py` exists to kill — and it cannot run unattended for
`/loop`. It is retained only as an *optional* interactive, human-in-the-loop
single-paper survey mode, where a human watches each gate decision.

**Net: this fully resolves W1** ("not runnable without writing adapter code"): the
LLM seams now ship as DI-callable adapters too — default `claude -p`, optional API —
exactly like the infra adapters (`build_http`/`build_run_cli`/`build_discover`),
which is the half of W1 ADR-0003 left open.

## Consequences

- **Contract docs reworded.** `SKILL.md` "Wiring the model seams", 
  `references/wiring-the-seams.md` §(A), and the `run_campaign.py` docstring change
  "MUST be backed by an independent Agent-tool invocation" → "MUST be a fresh,
  independent, isolated call (default transport: locked-down `claude -p`;
  alternative: Anthropic API) — realized as the injected Python callable." The
  isolation/private-rubric MUSTs are unchanged.
- **A production seam adapter ships.** The hardened `claude -p` seam (cleaned up
  from `attn_sink/cosmos_trial/seams.py`, with the lockdown flags + the skeptic
  isolation guarantee) moves into the skill as the default; an API adapter is the
  documented alternative. Constructing the seams stops being per-run improvisation.
- **README documents the auth gotcha.** Claude Code auth precedence: if
  `ANTHROPIC_API_KEY` is present in the env, `claude -p` uses it (metered API
  billing) and silently overrides subscription. The `claude -p` adapter / docs must
  make the subscription-vs-key choice explicit so a cloner is not billed by surprise.
- **The 0/5 trial run is re-interpreted**, not treated as an engine defect: it ran
  an un-hardened, un-locked-down `claude -p` harness. A real green campaign (≥1
  sealed paper) is re-run on the shipped hardened adapter before any `git push`.
- **The 363 fake-seam tests and the gate/ledger/hub substrate are untouched** — the
  decision changes only which callable is bound at the existing injection point.
- A maintainer who wonders "why `claude -p` and not pure API, and why not a real
  Agent-tool sub-agent" should read this ADR.
