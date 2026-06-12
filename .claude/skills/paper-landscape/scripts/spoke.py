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

import hashlib
import json
import shutil
import tempfile
from collections.abc import Callable
from pathlib import Path

from scripts.audit.equation_fidelity import count_display_math_blocks
from scripts.audit.g2_data_fidelity import run_g2
from scripts.audit.g3_seal import run_g3
from scripts.audit.gate_runner import run_with_budget
from scripts.audit.types import EntailmentJudgeFn, RigorScoreFn, SkepticVoteFn
from scripts.engine_version import current_commit
from scripts.failure_scene import FAILED_REL, write_scene
from scripts.hub import SpokeFn, SpokeResult, _candidate_key
from scripts.ingest.ingest import IngestFailed, IngestResult, ingest, quarantine
from scripts.output.branch1_report import AnchorGateError
from scripts.output.produce import (
    ProduceGateBlocked,
    ProduceResult,
    StructuralSealFailed,
    produce_outputs,
)
from scripts.paths import FAILURE_AUDIT_BLOCK, FAILURE_CONVERT_ERROR, EngineAbort


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


def _sampled(key: str, rate: float) -> bool:
    """Deterministic per-key sampling for the G2 cross-model pass (ROADMAP C2):
    True for ~`rate` of keys (≤0 never, ≥1 always), stable across runs so a paper
    is consistently sampled — bounds the extra cross-model cost to a fraction."""
    if rate <= 0:
        return False
    if rate >= 1:
        return True
    bucket = int(hashlib.sha256(key.encode("utf-8")).hexdigest(), 16) % 1000
    return bucket < rate * 1000


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
    g2_blind_retry_rounds: int = 1,
    cross_model_votes: SkepticVoteFn | None = None,
    cross_model_sample: float = 0.0,
    g2_tolerant: bool = False,
    g2_max_unconfirmed: int = 0,
    g2_max_unconfirmed_ratio: float = 0.0,
    write_report: Callable | None = None,
    faithfulness_judge: Callable | None = None,
    repo_resolver: Callable | None = None,
) -> SpokeFn:
    """Build the production SpokeFn that runs the full gated pipeline per paper.

    All model-facing decisions are injected seams (resolve_analysis / skeptic /
    rigor / entailment / faithfulness_judge — the branch1 忠实门 (c), ADR-0012) so
    the pipeline is deterministic and testable; production wires them to Agent-tool
    invocations.
    """
    workspace = Path(workspace)
    failed_dir = workspace / "_failed"

    def spoke(candidate: dict, *, cancel=None) -> SpokeResult:
        # `cancel` is the hub guard's stall-abort signal (threading.Event | None);
        # threaded into produce_outputs so a spoke abandoned for overrunning its
        # wall-clock budget aborts before promoting to the vault (Codex R17).
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
        #    A sampled fraction of papers also gets the cross-model verification
        #    overlay (ROADMAP C2) — a heterogeneous-family skeptic that catches
        #    fabrications the in-family majority's conformity bias let through.
        use_cross = (
            cross_model_votes
            if cross_model_votes is not None
            and _sampled(_candidate_key(candidate), cross_model_sample)
            else None
        )

        def _g2(stage_ai_entry: Path):
            return run_g2(
                stage_ai_entry,
                ing.md_path,
                skeptic_votes=skeptic_votes,
                n_skeptics=n_skeptics,
                cross_model_votes=use_cross,
                tolerant=g2_tolerant,
                max_unconfirmed=g2_max_unconfirmed,
                max_unconfirmed_ratio=g2_max_unconfirmed_ratio,
            )

        # 4. The analyzer seam is passed as a parameter (no module-global
        #    mutation) so concurrent spokes never share one analyzer.
        cached_analysis: dict | None = None

        def _attempt(
            *, prior_failure_branch1: str | None = None, prior_failure_analyzer: str | None = None
        ) -> ProduceResult:
            # prior_failure_analyzer routes to stage_branch2 (re-sample the analyzer);
            # prior_failure_branch1 routes to stage_branch1 (rewrite the report). A
            # branch1-only re-emit REUSES the cached branch2 SSOT — no analyzer
            # re-sample (ADR-0009); every other path (first attempt, G2 blind retry,
            # branch2 re-emit) re-samples fresh.
            nonlocal cached_analysis
            reuse = (
                cached_analysis
                if prior_failure_branch1 is not None and prior_failure_analyzer is None
                else None
            )
            result = produce_outputs(
                ing.md_path,
                candidate,
                ledger,
                root=workspace,
                resolve_analysis=resolve_analysis,
                g2_gate=_g2,
                write_report=write_report,
                faithfulness_judge=faithfulness_judge,
                report_tolerant=g2_tolerant,
                report_max_unconfirmed=g2_max_unconfirmed,
                report_max_unconfirmed_ratio=g2_max_unconfirmed_ratio,
                cancel=cancel,
                repo_resolver=repo_resolver,
                reuse_analysis=reuse,
                prior_failure_analyzer=prior_failure_analyzer,
                prior_failure_branch1=prior_failure_branch1,
            )
            cached_analysis = result.analysis
            return result

        # Scene helpers (audit F): a gate hard-block preserves the staged products
        # as a self-contained _failed/<key>/ scene (carrying every input revival
        # needs) instead of a throwaway note. ledger_key = the hub idempotency key
        # so the batch revival can flip the original ledger row to done.
        cand_key = _candidate_key(candidate)

        def _pre_promote_scene(*, failed_gate, findings, staged_dir, reason) -> SpokeResult:
            """A pre-promotion gate hard-failed: nothing reached the vault; preserve
            the staged products (in `staged_dir`) as a scene and report failed."""
            write_scene(
                workspace=workspace,
                key=cand_key,
                ledger_key=cand_key,
                failed_gate=failed_gate,
                findings=findings,
                engine_commit=current_commit(workspace),
                candidate=candidate,
                md_path=ing.md_path,
                content_list_path=content_list_path,
                analysis=None,
                staged_dir=staged_dir,
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

        def _abort_scene(exc) -> None:
            # ADR-0011: a transport abort (EngineAbort) anywhere in produce / G3 may
            # carry a built-but-unverified staged ARA (produce_outputs attached
            # `staged_dir`). Scene it so the paid-for ARA survives for debug; the
            # caller then RE-RAISES so the tick still aborts (cost guard unchanged).
            # No staged_dir (abort before the ARA was built) → nothing to preserve.
            staged = getattr(exc, "staged_dir", None)
            if staged is None:
                return
            write_scene(
                workspace=workspace,
                key=cand_key,
                ledger_key=cand_key,
                failed_gate="传输中断",
                findings=[{"target": "ara", "observation": str(exc)}],
                engine_commit=current_commit(workspace),
                candidate=candidate,
                md_path=ing.md_path,
                content_list_path=content_list_path,
                analysis=None,
                staged_dir=staged,
            )

        # 5. branch2 -> Seal-1 -> G2 -> branch1, with a G2 blind-retry budget. A
        #    number-gate hard block re-runs the analyzer (fresh sampling, NO verdict
        #    injection — ADR-0006) up to g2_blind_retry_rounds times; each intermediate
        #    block's staging is cleaned and the FINAL one becomes the 数字门 scene.
        #    (A bounded loop, not run_with_budget: the budget runner's gate->verdict
        #    contract can't both clean each intermediate staging AND preserve the last
        #    one for the scene — it has no notion of "final round". Behavior is
        #    identical: blind retry, no feedback, exhausted -> scene, no note.)
        produced: ProduceResult | None = None
        for g2_round in range(g2_blind_retry_rounds + 1):
            try:
                produced = _attempt()
                break
            except StructuralSealFailed as exc:
                # Seal-1 (structural) → root in branch2; not blind-retried (it would
                # fail identically). Revival re-runs the whole branch2 chain.
                return _pre_promote_scene(
                    failed_gate="结构门",
                    findings=[{"target": "ara", "observation": e} for e in exc.errors],
                    staged_dir=exc.staged_dir,
                    reason="branch2 Seal-1 structural hard-fail: " + "; ".join(exc.errors[:3]),
                )
            except ProduceGateBlocked as exc:
                # G2 data-fidelity hard block (staged ai/ only; branch1 not yet built).
                if g2_round < g2_blind_retry_rounds:
                    shutil.rmtree(exc.staged_dir, ignore_errors=True)  # clean; retry fresh
                    continue
                return _pre_promote_scene(
                    failed_gate="数字门",
                    findings=[f.as_dict() for f in exc.verdict.hard_findings],
                    staged_dir=exc.staged_dir,
                    reason="G2 data-fidelity hard-block: "
                    + "; ".join(f.observation for f in exc.verdict.hard_findings[:3]),
                )
            except AnchorGateError as exc:
                # branch1's 锚点门 — now the 忠实门 (ADR-0012: kept anchor-form lint +
                # (b) prose-number grounding + (c) judge) — hard-failed in staging
                # BEFORE promotion (OT-5). Preserve as a scene, not a tick crash.
                return _pre_promote_scene(
                    failed_gate="锚点门",
                    findings=[{"target": "report.md", "observation": str(exc)}],
                    staged_dir=getattr(exc, "staged_dir", None),
                    reason=f"branch1 锚点门 (忠实门) hard-block: {exc}",
                )
            except EngineAbort as exc:
                # ADR-0011: pre-promote transport abort with a built ARA → scene it,
                # then re-raise (tick still aborts; cost guard unchanged).
                _abort_scene(exc)
                raise
        assert produced is not None  # the loop either broke with a result or returned a scene

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

        def _g3_to_scene(verdict) -> SpokeResult:
            # The final gate runs AFTER promotion, so the products live in the vault.
            # Move them into a _failed/-internal staging dir (NOT /tmp: a crash
            # between the move and write_scene must leave them in the recoverable
            # gitignored scratch subtree, audit R15), then preserve as a scene.
            (workspace / FAILED_REL).mkdir(parents=True, exist_ok=True)
            scene_staging = Path(
                tempfile.mkdtemp(dir=str(workspace / FAILED_REL), prefix=".scene-")
            )
            shutil.move(str(produced.ai_path), str(scene_staging / "ai"))
            shutil.move(str(produced.person_path), str(scene_staging / "person"))
            write_scene(
                workspace=workspace,
                key=produced.key,
                ledger_key=cand_key,
                failed_gate="最终门",
                findings=[f.as_dict() for f in verdict.hard_findings],
                engine_commit=current_commit(workspace),
                candidate=candidate,
                md_path=ing.md_path,
                content_list_path=content_list_path,
                analysis=None,
                staged_dir=scene_staging,
            )
            return SpokeResult(
                status="failed",
                person_vault_path=None,
                ai_package_path=None,
                failure_class=FAILURE_AUDIT_BLOCK,
                failure_reason="G3 seal hard-block exhausted budget",
                source_url=source_url,
                attempted_tier=str(ing.tier),
            )

        # 6b. Branch-level G3 dispatch (ADR-0009): re-emit ONLY the failed branch,
        #     attributed by Finding.target. An ingest-rooted finding is unfixable by
        #     any engine re-run → scene immediately (don't burn the budget).
        class _Unfixable(Exception):  # noqa: N818 — local sentinel, not a public error type
            def __init__(self, verdict):
                self.verdict = verdict

        def _classify(verdict) -> set[str]:
            # M2: endswith / exact-suffix, not fragile substrings. Observed targets:
            # anchor→report.md (branch1); rigor→level2_report.json, entailment→
            # claims.md:<id> (branch2); equation→<id>.md (ingest — unfixable).
            roots: set[str] = set()
            for f in verdict.hard_findings:
                t = f.target
                if t.endswith("report.md"):
                    roots.add("branch1")
                elif t.endswith("level2_report.json") or "claims.md" in t.split(":")[0]:
                    roots.add("branch2")
                else:
                    roots.add("ingest")
            return roots

        def _findings_of(exc) -> list[dict]:
            if isinstance(exc, StructuralSealFailed):
                return [{"target": "ara", "observation": e} for e in exc.errors]
            if isinstance(exc, ProduceGateBlocked):
                return [f.as_dict() for f in exc.verdict.hard_findings]
            return [{"target": "report.md", "observation": str(exc)}]  # AnchorGateError

        def _reemit_for_g3(verdict) -> ProduceResult:
            roots = _classify(verdict)
            fb = "\n".join(f"- {f.target}: {f.observation}" for f in verdict.hard_findings)
            # audit R1 Finding 5: ANY ingest root (e.g. equation fidelity) is unfixable
            # by re-running a branch — bail to a scene rather than burn the whole budget
            # re-emitting a branch that can't move that finding. G3 aggregates equation
            # (ingest) + anchor (branch1) + entailment/rigor (branch2) into one verdict,
            # so a {ingest, branch1/branch2} mix is reachable.
            if "ingest" in roots:
                raise _Unfixable(verdict)
            if "branch2" in roots:
                return _attempt(
                    prior_failure_analyzer=fb
                )  # re-sample analyzer + downstream branch1
            return _attempt(prior_failure_branch1=fb)  # reuse branch2 SSOT, rewrite branch1 only

        def _on_g3_reemit(_i, verdict) -> None:
            # run_with_budget discards the callback's return value and `_g3` reads
            # `produced`, so rebind it here or round 2 re-seals the STALE product
            # (audit R2 Finding 1). _Unfixable propagates (the assignment never runs).
            nonlocal produced
            produced = _reemit_for_g3(verdict)

        try:
            outcome = run_with_budget(
                _g3,
                max_rounds=max_gate_rounds,
                on_reemit=_on_g3_reemit,
                write_quarantine_note=False,  # the spoke preserves its own scene; no note
                failed_dir=failed_dir,
                key=produced.key,
                paper_meta={
                    "arxiv_id": candidate.get("arxiv_id"),
                    "title": candidate.get("title"),
                    "source_url": source_url,
                    "tier": ing.tier,
                },
            )
        except EngineAbort as exc:
            # ADR-0011 (Codex R1): an EngineAbort during a G3 re-emit's _attempt()
            # carries the re-emit's built staged ARA — scene it, then re-raise so the
            # tick still aborts. Without this the staged ARA is orphaned in /tmp.
            _abort_scene(exc)
            raise
        except _Unfixable as exc:
            # An ingest-rooted G3 finding → don't spin the budget; land the 最终门 scene.
            return _g3_to_scene(exc.verdict)
        except (StructuralSealFailed, ProduceGateBlocked, AnchorGateError) as exc:
            # A re-emitted branch hit its own downstream gate before re-promotion.
            # `produced` still points at the PRIOR round's promoted product (the
            # _on_g3_reemit assignment never completed). ADR-0011 scene-before-rm:
            # land the re-emit scene FIRST, THEN remove the prior promoted product
            # from the vault — a write_scene failure can no longer lose both (and if
            # it throws, produced.* lingers and consistency_check preserves it).
            gate = {
                "StructuralSealFailed": "结构门",
                "ProduceGateBlocked": "数字门",
                "AnchorGateError": "锚点门",
            }[type(exc).__name__]
            write_scene(
                workspace=workspace,
                key=produced.key,
                ledger_key=cand_key,
                failed_gate=gate,
                findings=_findings_of(exc),
                engine_commit=current_commit(workspace),
                candidate=candidate,
                md_path=ing.md_path,
                content_list_path=content_list_path,
                analysis=None,
                staged_dir=getattr(exc, "staged_dir", None),
            )
            shutil.rmtree(produced.person_path, ignore_errors=True)
            shutil.rmtree(produced.ai_path, ignore_errors=True)
            return SpokeResult(
                status="failed",
                person_vault_path=None,
                ai_package_path=None,
                failure_class=FAILURE_AUDIT_BLOCK,
                failure_reason=f"G3 re-emit {gate} failed: {exc}",
                source_url=source_url,
                attempted_tier=str(ing.tier),
            )
        if outcome.escalated:
            # G3 seal failed the whole budget → preserve the promoted product as a
            # 最终门 scene (audit F) so revival can re-run the failed branch later.
            return _g3_to_scene(outcome.final_verdict)

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
