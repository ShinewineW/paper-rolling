# .claude/skills/paper-landscape/scripts/spoke.py
"""Production per-paper spoke — wires the binding pipeline (WIRING-1 fix).

The HUB injects a `SpokeFn` per paper; this module builds the concrete one that
runs the design's pipeline IN ORDER:

    ingest (tier-1 -> tier-2)
      -> branch2 (ARA, inside produce_outputs)
        -> G2 data-fidelity gate   (AFTER branch2, BEFORE branch1)
          -> branch1 (person report, inside produce_outputs)
            -> G3 seal gate         (AFTER both branches, bounded retry)
              -> done

G2 is wired THROUGH produce_outputs (the only place that holds the staged
branch2 before branch1), so a G2 hard block aborts before any promotion (OT-5:
nothing reaches the real vault). G3 runs after promotion under the bounded
gate-runner; on a persistent block the runner quarantines and the spoke reports
a failure. The spoke NEVER writes the ledger (single-writer invariant: the hub
records `result.person_vault_path` / `ai_package_path` verbatim from what
produce_outputs returned — it never re-derives a key).
"""

from __future__ import annotations

import json
import shutil
from collections.abc import Callable
from pathlib import Path

from scripts.audit.equation_fidelity import count_display_math_blocks
from scripts.audit.g2_data_fidelity import run_g2
from scripts.audit.g3_seal import run_g3
from scripts.audit.gate_runner import run_with_budget
from scripts.audit.types import EntailmentJudgeFn, RigorScoreFn, SkepticVoteFn
from scripts.hub import SpokeFn, SpokeResult, _candidate_key
from scripts.ingest.ingest import IngestFailed, IngestResult, ingest, quarantine
from scripts.output.branch1_report import AnchorGateError
from scripts.output.produce import ProduceGateBlocked, ProduceResult, produce_outputs
from scripts.paths import FAILURE_AUDIT_BLOCK, FAILURE_CONVERT_ERROR


def _synthesize_content_list(md_path: Path) -> Path:
    """Write a synthetic content_list.json next to the MD for tier-1 conversions.

    Tier-1 (pandoc) emits no content_list.json, but G3's mechanical equation gate
    compares the MD's `$$` display-block count against typed formula blocks in
    content_list.json UNCONDITIONALLY. For a trusted tier-1 conversion we make
    the gate a faithful pass-through by emitting exactly one `{"type":"equation"}`
    entry per `$$` block in the MD (count parity => no false equation mismatch).
    """
    md_text = md_path.read_text(encoding="utf-8")
    n = count_display_math_blocks(md_text)
    blocks = [{"type": "equation"} for _ in range(n)]
    path = md_path.with_name("content_list.json")
    path.write_text(json.dumps(blocks), encoding="utf-8")
    return path


def make_spoke(
    *,
    workspace: Path,
    http,
    run_cli,
    resolve_analysis: Callable,
    skeptic_votes: SkepticVoteFn,
    rigor_scores: RigorScoreFn,
    entailment_judge: EntailmentJudgeFn,
    ledger,
    now=None,
    n_skeptics: int = 3,
    max_gate_rounds: int = 2,
) -> SpokeFn:
    """Build the production SpokeFn that runs the full gated pipeline per paper.

    All model-facing decisions are injected seams (resolve_analysis / skeptic /
    rigor / entailment) so the pipeline is deterministic and testable; production
    wires them to Agent-tool invocations.
    """
    workspace = Path(workspace)
    failed_dir = workspace / "_failed"

    def spoke(candidate: dict) -> SpokeResult:
        source_url = candidate.get("oa_pdf_url")

        # 1. Ingest (tier-1 -> tier-2). On total failure: quarantine + report.
        try:
            ing: IngestResult = ingest(candidate, workspace, http=http, run_cli=run_cli, now=now)
        except IngestFailed as exc:
            quarantine(candidate, workspace, reason=str(exc), attempted_tiers=[1, 2])
            return SpokeResult(
                status="failed",
                person_vault_path=None,
                ai_package_path=None,
                failure_class=FAILURE_CONVERT_ERROR,
                failure_reason=str(exc),
                source_url=source_url,
                attempted_tier="1,2",
            )

        # 2. content_list.json: tier-2 emits one; tier-1 needs a synthetic stand-in.
        content_list_path = ing.content_list_path or _synthesize_content_list(ing.md_path)

        # 3. Wire G2 into produce_outputs (runs after branch2, before branch1).
        def _g2(stage_ai_entry: Path):
            return run_g2(
                stage_ai_entry,
                ing.md_path,
                skeptic_votes=skeptic_votes,
                n_skeptics=n_skeptics,
            )

        # 4. The analyzer seam is passed as a parameter (no module-global
        #    mutation) so concurrent spokes never share one analyzer.
        def _attempt() -> ProduceResult:
            return produce_outputs(
                ing.md_path,
                candidate,
                ledger,
                root=workspace,
                resolve_analysis=resolve_analysis,
                g2_gate=_g2,
            )

        # 5. branch2 -> G2 -> branch1. A G2 hard block aborts before promotion.
        try:
            produced = _attempt()
        except ProduceGateBlocked as exc:
            key = _candidate_key(candidate)
            reason = "G2 data-fidelity hard-block: " + "; ".join(
                f.observation for f in exc.verdict.hard_findings[:3]
            )
            failed_dir.mkdir(parents=True, exist_ok=True)
            (failed_dir / f"{key}.md").write_text(
                f"# Quarantined: {key}\n\n- **gate**: G2\n- **reason**: {reason}\n",
                encoding="utf-8",
            )
            return SpokeResult(
                status="failed",
                person_vault_path=None,
                ai_package_path=None,
                failure_class=FAILURE_AUDIT_BLOCK,
                failure_reason=reason,
                source_url=source_url,
                attempted_tier=str(ing.tier),
            )
        except AnchorGateError as exc:
            # branch1's self-anchor lint hard-failed (an empirical claim could not
            # be grounded in the MD). This happens in staging, BEFORE promotion, so
            # nothing reached the vault (OT-5). Quarantine instead of letting the
            # exception escape and crash the unattended /loop tick (中枢-D2 failure
            # isolation): the hub then skips this paper and back-fills the next.
            key = _candidate_key(candidate)
            reason = f"branch1 three-layer anchor hard-gate: {exc}"
            failed_dir.mkdir(parents=True, exist_ok=True)
            (failed_dir / f"{key}.md").write_text(
                f"# Quarantined: {key}\n\n- **gate**: branch1-anchor\n- **reason**: {reason}\n",
                encoding="utf-8",
            )
            return SpokeResult(
                status="failed",
                person_vault_path=None,
                ai_package_path=None,
                failure_class=FAILURE_AUDIT_BLOCK,
                failure_reason=reason,
                source_url=source_url,
                attempted_tier=str(ing.tier),
            )

        # 6. G3 seal (after both branches), bounded. On re-emit, rebuild branches.
        def _g3():
            return run_g3(
                produced.person_path,
                produced.ai_path,
                ing.md_path,
                content_list_path,
                rigor_scores=rigor_scores,
                entailment_judge=entailment_judge,
            )

        outcome = run_with_budget(
            _g3,
            max_rounds=max_gate_rounds,
            on_reemit=lambda i: _attempt(),
            failed_dir=failed_dir,
            key=produced.key,
            paper_meta={
                "arxiv_id": candidate.get("arxiv_id"),
                "title": candidate.get("title"),
                "source_url": source_url,
                "tier": ing.tier,
            },
        )
        if outcome.escalated:
            # G3 ran AFTER produce_outputs already promoted both vaults. The seal
            # failed for the whole budget, so this paper is unprocessable
            # (中枢-D2): REMOVE the promoted products so a failed-seal paper does
            # NOT pollute ai_package/ or the cross-paper landscape (which scans
            # ai_package/*/ara/PAPER.md). The _failed/{key}.md record was already
            # written by run_with_budget. Idempotent: ignore_errors covers a prior
            # re-emit having already swapped the dirs.
            shutil.rmtree(produced.person_path, ignore_errors=True)
            shutil.rmtree(produced.ai_path, ignore_errors=True)
            return SpokeResult(
                status="failed",
                person_vault_path=None,
                ai_package_path=None,
                failure_class=FAILURE_AUDIT_BLOCK,
                failure_reason="G3 seal hard-block exhausted budget",
                source_url=source_url,
                attempted_tier=str(ing.tier),
            )

        # 7. Success — return produce_outputs' EXACT paths (no re-derivation).
        return SpokeResult(
            status="done",
            person_vault_path=str(produced.person_path),
            ai_package_path=str(produced.ai_path),
            failure_class=None,
            failure_reason=None,
            source_url=source_url,
            attempted_tier=str(ing.tier),
        )

    return spoke
