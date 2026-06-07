# .claude/skills/paper-landscape/scripts/run_campaign.py
"""Production campaign DRIVER — the deterministic wiring made CODE (GATE-1 fix).

`make_spoke(...)` and `run_campaign_tick(...)` exist, but nothing in production
composed them and SKILL.md only described the wiring in prose. Prose wiring is
unenforceable: a lazy runtime could pass always-pass seams and silently neuter
the adversarial guarantees (G2 number-fabrication hard-block + G3 6-dim seal).
This module turns the composition into a single executable entry point so the
ONLY thing left to the runtime agent is constructing the four LLM-backed seams.

The `/loop` tick drives `run_campaign(...)`:

    Ledger(workspace)                            # single-writer processed-state
      -> make_spoke(seams + http/run_cli)        # per-paper gated pipeline
        -> with ledger.acquire():                # LS-1 single-writer lock (fail fast)
             run_campaign_tick(discover, spoke)  # gate-check -> LS-4 self-heal
                                                 #   -> batch -> landscape

The four model seams are provider-agnostic injected callables (NO LLM call is
hard-coded here). In production EACH seam MUST be backed by an INDEPENDENT
Agent-tool invocation (a fresh sub-agent per call), so the audit votes are not
correlated with the generator that produced the numbers:

  - resolve_analysis  — the analyzer sub-agent that reads the frozen {ID}.md and
                        returns the ARA bundle branch2/branch1/landscapes consume
                        (see SKILL.md "Wiring the model seams" for the exact shape,
                        including the headline_metric / headline_value /
                        params_million keys landscapes needs).
  - skeptic_votes     — the G2 ground-truth-isolated skeptic. Each vote is an
                        INDEPENDENT Agent-tool invocation that sees ONLY the
                        candidate numbers + the source MD — NEVER the evidence
                        file / answer key / any rubric. The multi-vote majority is
                        what hard-blocks a fabricated number; correlation with the
                        generator would defeat that, hence the isolation MUST.
  - rigor_scores      — the G3 6-dim rigor reviewer. The rubric is held PRIVATELY
                        by the seam implementation (private-rubric rule) and never
                        appears in any generator prompt.
  - entailment_judge  — the G3 type-aware entailment check (claim + linked
                        experiment text -> (entailed, reason)).

The composition is deterministic and fully testable with fake seams (see
tests/test_run_campaign.py and tests/test_spoke.py); production swaps in the
four Agent-tool-backed seams without touching this file.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from scripts.audit.types import EntailmentJudgeFn, RigorScoreFn, SkepticVoteFn
from scripts.audit_config import AuditConfig, load_audit_config
from scripts.hub import DiscoverFn, TickResult, run_campaign_tick
from scripts.ledger.store import Ledger
from scripts.spoke import make_spoke


def run_campaign(
    *,
    workspace: Path,
    discover: DiscoverFn,
    resolve_analysis: Callable,
    skeptic_votes: SkepticVoteFn,
    rigor_scores: RigorScoreFn,
    entailment_judge: EntailmentJudgeFn,
    http: Callable,
    run_cli: Callable,
    cross_model_votes: SkepticVoteFn | None = None,
    cross_model_sample: float = 0.0,
    empirical_classifier: Callable | None = None,
    audit_config: AuditConfig | None = None,
    requested_topic: str | None = None,
    requested_n: int | None = None,
) -> TickResult:
    """Run one /loop campaign tick end-to-end (gates included).

    Builds the single-writer ledger, composes the per-paper gated spoke with the
    four injected model seams, and dispatches one `run_campaign_tick` — returning
    its `TickResult` (hub counts + the regenerated landscape). The wiring is CODE
    so the adversarial guarantees cannot be bypassed by prose drift: every run
    goes through G2 (number-fabrication hard-block) and G3 (6-dim seal).

    Args:
        workspace: The paper-rolling workspace root (holds `corpus/`, `_ledger/`,
            `person_vault/`, `ai_package/`, `landscapes/`, `config/`).
        discover: `DiscoverFn = (topic: str, n: int) -> list[dict]`. Returns the
            ranked candidate pool (over-pulled ~2-3×N so failures can backfill).
            In production this is the discovery layer, not an LLM seam.
        resolve_analysis: `(md_path: Path, candidate: dict) -> dict`. The analyzer
            sub-agent's ARA bundle for one paper. MUST be an INDEPENDENT Agent-tool
            invocation. Return shape: the analysis bundle branch2_ara/branch1 and
            the landscapes comparator consume — including the headline keys
            `headline_metric` (str), `headline_value` (float), `params_million`
            (float). See SKILL.md "Wiring the model seams".
        skeptic_votes: `SkepticVoteFn` (audit/types.py). The G2 ground-truth-
            isolated skeptic: receives ONLY `(numbers, source_md, claim_context)`
            and returns one `SkepticVote` per number. MUST be an INDEPENDENT
            Agent-tool invocation per call and MUST NEVER see the evidence
            file / answer key / any rubric (ground-truth isolation). The multi-vote
            majority is what hard-blocks fabricated numbers.
        rigor_scores: `RigorScoreFn` (audit/types.py). The G3 6-dim rigor reviewer:
            receives the ARA text bundle, returns per-dimension scores + findings.
            MUST be an INDEPENDENT Agent-tool invocation; the rubric is held
            PRIVATELY by the implementation (private-rubric rule) and never appears
            in any generator prompt.
        entailment_judge: `EntailmentJudgeFn` (audit/types.py). The G3 type-aware
            entailment check: `(claim, experiment_text) -> (entailed, reason)`.
            MUST be an INDEPENDENT Agent-tool invocation.
        http: HTTP fetch seam `(url) -> (status, body)` used by ingest (Tier 1
            arXiv-HTML download). Provider-agnostic injected callable.
        run_cli: CLI runner seam `(argv, cwd) -> result` used by ingest (Tier 2
            MinerU / pandoc). Provider-agnostic injected callable.
        requested_topic: Optional topic for this tick. If it differs from the
            locked `config/campaign.yaml`, the campaign Hard Gate re-fires.
        requested_n: Optional per-tick N. If it differs from the locked config,
            the Hard Gate re-fires.

    Returns:
        TickResult(hub=HubResult, landscape=LandscapeResult).

    Raises:
        GateRequired: If no campaign is locked (or topic/N changed) — the harness
            catches this and runs the HITL campaign-setup gate, then retries.
    """
    workspace = Path(workspace)
    ledger = Ledger(workspace)
    # Operator-tunable audit knobs (config/audit.yaml; defaults if absent). These
    # trade adversarial strictness against token cost / quarantine rate.
    cfg = audit_config or load_audit_config(workspace)
    spoke = make_spoke(
        workspace=workspace,
        http=http,
        run_cli=run_cli,
        resolve_analysis=resolve_analysis,
        skeptic_votes=skeptic_votes,
        rigor_scores=rigor_scores,
        entailment_judge=entailment_judge,
        ledger=ledger,
        cross_model_votes=cross_model_votes,
        cross_model_sample=cross_model_sample,
        empirical_classifier=empirical_classifier,
        n_skeptics=cfg.skeptic_votes,
        max_gate_rounds=cfg.max_gate_rounds,
        g2_tolerant=cfg.data_fidelity_tolerant,
        g2_max_unconfirmed=cfg.data_fidelity_max_unconfirmed,
        g2_max_unconfirmed_ratio=cfg.data_fidelity_max_unconfirmed_ratio,
    )
    # LS-1 single-writer lock: hold _ledger/.lock for the whole tick so a second
    # concurrent instance fails fast (LedgerLockError) instead of racing the
    # single-writer ledger. The lock belongs at the production driver entry — NOT
    # inside run_campaign_tick, which the hub tests call directly with their own
    # ledger.
    with ledger.acquire():
        return run_campaign_tick(
            workspace=workspace,
            ledger=ledger,
            discover=discover,
            spoke=spoke,
            requested_topic=requested_topic,
            requested_n=requested_n,
        )


_USAGE = """\
run_campaign — the paper-landscape v2 production campaign DRIVER (composition).

This module is NOT runnable on its own: `run_campaign(...)` is a composition
entry point, not a CLI. It deterministically wires
    Ledger -> make_spoke(seams) -> (LS-1 lock) run_campaign_tick
and runs one /loop tick of the campaign (discover -> ingest -> branch2 -> G2 ->
branch1 -> G3 -> landscapes), with the adversarial guarantees (G2 number-
fabrication hard-block + G3 6-dim seal) baked into code.

The runtime agent (the /paper-landscape skill or the daily /loop tick) MUST call
run_campaign(...) and supply SEVEN injected callables — it cannot be invoked
blindly from the shell:

  discover           — the discovery layer (topic, n) -> ranked candidate pool
  resolve_analysis   — model seam #1: the analyzer sub-agent (ARA bundle)
  skeptic_votes      — model seam #2: the G2 ground-truth-isolated skeptic
  rigor_scores       — model seam #3: the G3 6-dim rigor reviewer
  entailment_judge   — model seam #4: the G3 type-aware entailment judge
  http               — HTTP fetch seam used by ingest (Tier-1 arXiv-HTML)
  run_cli            — CLI runner seam used by ingest (Tier-2 MinerU / pandoc)

The FOUR model seams MUST each be backed by an INDEPENDENT Agent-tool invocation
(a fresh sub-agent per call) so the audit votes are uncorrelated with the
generator. See SKILL.md "Wiring the model seams" for the exact contract of each.

Running this file directly does nothing but print this message — that is by
design (a direct invocation is not a silent no-op).\
"""


if __name__ == "__main__":
    import sys

    print(_USAGE)
    sys.exit(0)
