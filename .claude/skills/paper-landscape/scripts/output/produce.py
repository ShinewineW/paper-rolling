"""Atomic dual-output orchestrator (OT-5) — public entrypoint.

`produce_outputs(md_path, candidate, ledger)` builds branch2 (ai_package) FIRST,
then branch1 (person_vault) DERIVED from it, in a STAGING directory; runs the
ARA Seal-1 validator + the branch1 忠实门 (锚点门, ADR-0012); and only on full success
moves BOTH into their vaults under one shared key (OT-5: both or neither).
Re-processing the same paper-identity deletes any prior same-identity entries
first (OT-2). Naming is deterministic (OT-3).

The hub (Chunk 3/5) supplies the analyzer bundle via the injected
`resolve_analysis` callable (a per-paper Agent-tool seam, passed as a keyword
argument). The contract is `produce_outputs(md_path, candidate, ledger, *,
resolve_analysis) -> ProduceResult(key=...)`.
"""

from __future__ import annotations

import shutil
import tempfile
import threading
from collections.abc import Callable
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from scripts.output.ara_schema import validate_ara_tree
from scripts.output.branch1_llm import write_branch1_llm
from scripts.output.branch1_report import AnchorGateError, write_branch1
from scripts.output.branch2_ara import write_branch2
from scripts.output.naming import find_existing_entries, vault_key
from scripts.paths import EngineAbort, ara_is_nonempty


@dataclass(frozen=True)
class ProduceResult:
    """Outcome of one dual-output run."""

    key: str
    person_path: Path
    ai_path: Path
    # The branch2 analyzer bundle that produced this run, surfaced so a branch1-only
    # G3 re-emit can reuse the branch2 SSOT without re-sampling the analyzer (ADR-0009).
    analysis: dict | None = None


class ProduceGateBlocked(Exception):
    """G2 hard-blocked the staged branch2 BEFORE branch1/promotion (OT-5 holds).

    Carries the blocking verdict so the spoke can record the reason, and the
    staged dir (parent of `ai/`) so the spoke can preserve the failure scene
    instead of letting `finally` delete the staged branch2 products (audit F).
    """

    def __init__(self, verdict: Any, *, staged_dir: Path | None = None) -> None:
        self.verdict = verdict
        self.staged_dir = staged_dir
        super().__init__("branch2 hard-blocked by the G2 data-fidelity gate")


class StructuralSealFailed(Exception):
    """branch2 failed the Seal-1 structural validator BEFORE branch1/promotion.

    Replaces the former bare ValueError (audit F / R1 Finding 1): carries the
    structural errors + the staged dir (parent of `ai/`) so the spoke can
    preserve the failure scene rather than let `finally` delete it. The failure
    root is branch2 → revival re-runs the whole branch2 chain.
    """

    def __init__(self, errors: list[str], *, staged_dir: Path | None = None) -> None:
        self.errors = errors
        self.staged_dir = staged_dir
        super().__init__(f"branch2 failed Seal-1: {'; '.join(errors[:5])}")


class SpokeCancelled(Exception):
    """The per-paper guard abandoned this spoke (stall budget exceeded) BEFORE
    promotion, so produce_outputs aborted without touching either real vault.

    A daemon spoke that overran its wall-clock budget keeps running (Python can't
    kill threads); this lets it bail out at the last safe point — right before the
    atomic vault promotion — so a late finisher never writes products the hub has
    already recorded as failed (Codex R17 stall-isolation gap). Staging is cleaned
    up in produce_outputs' `finally`.
    """


def _write_audit_flags(ara_dir: Path, verdict: Any) -> None:
    """Record G2's tolerated (non-blocking) data-fidelity findings in the pack.

    Written only in tolerant mode, when the gate kept the paper despite a few
    unverified numbers (config/audit.yaml). Lands as `ara/AUDIT_FLAGS.md` so the
    miss is visible alongside the knowledge pack instead of silently absorbed.
    """
    lines = [
        "# Audit flags — tolerated data-fidelity findings",
        "",
        "These numbers were NOT confirmed in the source MD but fell within the "
        "configured tolerance, so the paper was kept and flagged (not blocked). "
        "Review before trusting them.",
        "",
    ]
    for f in verdict.findings:
        lines.append(f"- **[{f.severity.value}] {f.finding_id}** — {f.observation}")
        if f.suggestion:
            lines.append(f"  - _suggestion_: {f.suggestion}")
    (ara_dir / "AUDIT_FLAGS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 审计 §5-附1: reflow a visible banner into PAPER.md so tolerated-but-unconfirmed
    # numbers aren't buried only in AUDIT_FLAGS.md. Appended after branch2 wrote it.
    paper_md = ara_dir / "PAPER.md"
    if paper_md.exists() and verdict.findings:
        # Surface the actual suspect numbers (carried in each finding's observation),
        # not just the finding IDs — a reader must see WHICH number is unconfirmed
        # in the body, not have to open AUDIT_FLAGS.md to learn it (Codex S2-R1).
        bullets = "\n".join(f"> - **{f.finding_id}**:{f.observation}" for f in verdict.findings)
        banner = (
            f"\n> ⚠️ **数据保真存疑(容差内放行)**:本包有 {len(verdict.findings)} 处数字"
            "未被 G2 skeptic 多数确认,引用相关数字前请先核对源文——\n"
            f"{bullets}\n"
            ">\n"
            "> 详见 [AUDIT_FLAGS.md](AUDIT_FLAGS.md)。\n"
        )
        paper_md.write_text(paper_md.read_text(encoding="utf-8") + banner, encoding="utf-8")


def stage_branch2(
    staging: Path,
    candidate: Any,
    md_path: Path,
    *,
    resolve_analysis: Callable[..., dict],
    repo_resolver: Callable | None = None,
    prior_failure: str | None = None,
    analysis: dict | None = None,
) -> tuple[Path, dict]:
    """Stage branch2 (ARA) into ``staging/ai/ara`` and run Seal-1; return (stage_ai, analysis).

    The 'fresh' for a G2 blind retry / branch2 re-emit comes from RE-CALLING
    resolve_analysis (a new analyzer sampling), not from re-rendering a cached
    bundle (audit E). ``repo_resolver`` MUST thread through to write_branch2 or a
    re-emit silently loses code-link resolution (audit R10 — T2b/T4).

    Pass a pre-computed ``analysis`` to REUSE the branch2 SSOT (a branch1-only G3
    re-emit re-renders from it — no analyzer re-sample, ADR-0009).

    Raises:
        StructuralSealFailed: the staged ARA failed Seal-1 (carries ``staging``).
    """
    stage_ai = staging / "ai" / "ara"
    if analysis is None:
        # audit R5 Finding 1: only pass prior_failure when set — an older analyzer
        # fake takes (md_path, candidate) only and would TypeError on an extra kwarg.
        extra = {"prior_failure": prior_failure} if prior_failure is not None else {}
        analysis = resolve_analysis(md_path, candidate, **extra)
    write_branch2(stage_ai, candidate, analysis, md_path=md_path, repo_resolver=repo_resolver)
    ara_errors = validate_ara_tree(stage_ai)
    if ara_errors:
        raise StructuralSealFailed(ara_errors, staged_dir=staging)
    return stage_ai, analysis


def stage_branch1(
    staging: Path,
    candidate: Any,
    stage_ai: Path,
    md_path: Path,
    write_report: Callable[..., dict] | None,
    analysis: dict,
    key: str,
    *,
    prior_failure: str | None = None,
    faithfulness_judge: Any = None,
    report_tolerant: bool = True,
    report_max_unconfirmed: int = 5,
    report_max_unconfirmed_ratio: float = 0.2,
) -> None:
    """Stage branch1 (human report) into ``staging/person``, self-gating on the
    忠实门 (ADR-0012).

    The deterministic ``write_branch1`` fallback (write_report=None) is preserved
    (audit R4 Finding 2 — test_produce monkeypatches it). AnchorGateError carries
    ``staging`` so callers that bypass produce_outputs (G3 branch1 re-emit, revival)
    still get a self-contained scene (audit R4 Finding 1).

    Raises:
        AnchorGateError: the report failed the 忠実门.
    """
    stage_person = staging / "person"
    try:
        if write_report is not None:
            # audit R5 Finding 1: conditional kwarg keeps older write_report fakes working.
            extra = {"prior_failure": prior_failure} if prior_failure is not None else {}
            write_branch1_llm(
                stage_person,
                candidate,
                stage_ai,
                md_path,
                write_report,
                key=key,
                faithfulness_judge=faithfulness_judge,
                report_tolerant=report_tolerant,
                report_max_unconfirmed=report_max_unconfirmed,
                report_max_unconfirmed_ratio=report_max_unconfirmed_ratio,
                **extra,
            )
        else:
            write_branch1(
                stage_person,
                candidate,
                stage_ai,
                md_path,
                analysis,
                key=key,
                faithfulness_judge=faithfulness_judge,
                report_tolerant=report_tolerant,
                report_max_unconfirmed=report_max_unconfirmed,
                report_max_unconfirmed_ratio=report_max_unconfirmed_ratio,
            )
    except AnchorGateError as exc:
        exc.staged_dir = staging
        raise


def promote(
    staging: Path,
    key: str,
    *,
    candidate: Any,
    ledger: Any,
    person_vault: Path,
    ai_package: Path,
    cancel: threading.Event | None = None,
) -> ProduceResult:
    """Atomically promote staged products into both vaults (OT-2 overwrite, OT-5
    both-or-neither). cancel re-checks REVERT a promotion abandoned mid-commit
    (Codex R18/R19/R20). Returns the ProduceResult (shared key + both final paths)."""
    person_dest = person_vault / key
    ai_dest = ai_package / key
    person_vault.mkdir(parents=True, exist_ok=True)
    ai_package.mkdir(parents=True, exist_ok=True)
    for prior in find_existing_entries(person_vault, candidate["arxiv_id"], candidate["doi"]):
        shutil.rmtree(prior, ignore_errors=True)
    for prior in find_existing_entries(ai_package, candidate["arxiv_id"], candidate["doi"]):
        shutil.rmtree(prior, ignore_errors=True)
    if person_dest.exists():
        shutil.rmtree(person_dest)
    if ai_dest.exists():
        shutil.rmtree(ai_dest)
    shutil.move(str(staging / "person"), str(person_dest))
    shutil.move(str(staging / "ai"), str(ai_dest))

    # B2 / Codex R18+R19+R20: REVERT on a cancel landing in either durable-step
    # window (the moves, then the code-ref note). store.consistency_check prunes any
    # orphan vault dir (no `done` row) at the next tick start, so it self-heals.
    if cancel is not None and cancel.is_set():
        shutil.rmtree(person_dest, ignore_errors=True)
        shutil.rmtree(ai_dest, ignore_errors=True)
        raise SpokeCancelled("spoke cancelled during vault promotion (stall budget exceeded)")
    ledger.record_code_ref(key, str(ai_dest / "ara" / "src/code_ref.md"))
    if cancel is not None and cancel.is_set():
        shutil.rmtree(person_dest, ignore_errors=True)
        shutil.rmtree(ai_dest, ignore_errors=True)
        raise SpokeCancelled("spoke cancelled after vault promotion (stall budget exceeded)")
    return ProduceResult(key=key, person_path=person_dest, ai_path=ai_dest)


def produce_outputs(
    md_path: Path,
    candidate: Any,
    ledger: Any,
    root: Path | None = None,
    *,
    resolve_analysis: Callable[..., dict],
    g2_gate: Callable[[Path], Any] | None = None,
    write_report: Callable[..., dict] | None = None,
    cancel: threading.Event | None = None,
    repo_resolver: Callable | None = None,
    reuse_analysis: dict | None = None,
    prior_failure_analyzer: str | None = None,
    prior_failure_branch1: str | None = None,
    faithfulness_judge: Any = None,
    report_tolerant: bool = True,
    report_max_unconfirmed: int = 5,
    report_max_unconfirmed_ratio: float = 0.2,
) -> ProduceResult:
    """Produce branch2 + branch1 atomically into the two top-level vaults.

    Args:
        md_path: Frozen {ID}.md (the MD-only truth base + anchor target).
        candidate: Discovery record (carries identity + metadata).
        ledger: Ledger; provides `intake_date()` and `record_code_ref(key, path)`.
        root: Workspace root containing `person_vault/` and `ai_package/`.
              Defaults to the current working directory.
        resolve_analysis: Injected per-paper seam `(md_path, candidate) -> dict`
              returning the analyzer bundle. Passed as a keyword (no module-global
              state) so concurrent spokes never share/mutate one analyzer.
        g2_gate: Optional G2 data-fidelity gate, called with the staged ai ENTRY
              dir (parent of `ara/`) AFTER branch2 + Seal-1 and BEFORE branch1.
              A blocked verdict raises ProduceGateBlocked, aborting before any
              promotion (OT-5). The return is typed `Any` so output never hard-
              imports audit (avoids a cross-chunk import cycle). Default None
              keeps the gate out of the path entirely (backward-compatible).
        cancel: Optional stall-abort signal from the hub's per-paper guard. If it
              is set by the time both gates pass, promotion is skipped (raises
              SpokeCancelled) so a daemon spoke abandoned for overrunning its
              wall-clock budget never writes to the real vault (Codex R17).

    Returns:
        ProduceResult with the shared vault key and both final paths.

    Raises:
        ProduceGateBlocked: G2 hard-blocked the staged branch2 (nothing promoted).
        StructuralSealFailed: branch2 failed the Seal-1 structural validator.
        AnchorGateError: branch1's 忠实门 (锚点门, ADR-0012) hard-failed.
        Exception: Any other failure aborts BEFORE either vault is touched (OT-5).
    """
    root = (root or Path.cwd()).resolve()
    person_vault = root / "person_vault"
    ai_package = root / "ai_package"

    key = vault_key(
        intake=ledger.intake_date(),
        title=candidate["title"],
        arxiv_id=candidate["arxiv_id"],
        doi=candidate["doi"],
    )
    # Stage in a temp dir; promote only after both gates pass. A gate hard-fail
    # carries `staging` in its exception so the spoke can preserve it as a failure
    # scene; `handed_off` then tells `finally` NOT to delete it (audit F). Success
    # and SpokeCancelled keep it False → staging is cleaned up.
    staging = Path(tempfile.mkdtemp(prefix="paper-rolling-stage-"))
    handed_off = False
    try:
        stage_ai, analysis = stage_branch2(
            staging,
            candidate,
            md_path,
            resolve_analysis=resolve_analysis,
            repo_resolver=repo_resolver,
            prior_failure=prior_failure_analyzer,
            analysis=reuse_analysis,
        )

        # G2 (after branch2, before branch1): adversarial data-fidelity gate on the
        # staged ARA. A hard block aborts BEFORE branch1/promotion (OT-5 holds).
        if g2_gate is not None:
            verdict = g2_gate(staging / "ai")  # staged ai ENTRY dir (parent of ara/)
            if verdict.blocked:
                raise ProduceGateBlocked(verdict, staged_dir=staging)
            # Tolerant mode: mark the tolerated (non-blocking) numbers in the pack.
            if verdict.findings:
                _write_audit_flags(stage_ai, verdict)

        stage_branch1(
            staging,
            candidate,
            stage_ai,
            md_path,
            write_report,
            analysis,
            key,
            prior_failure=prior_failure_branch1,
            faithfulness_judge=faithfulness_judge,
            report_tolerant=report_tolerant,
            report_max_unconfirmed=report_max_unconfirmed,
            report_max_unconfirmed_ratio=report_max_unconfirmed_ratio,
        )

        # Last safe point before any real-vault write (Codex R17): if the guard
        # already abandoned this spoke, skip promotion; the `finally` cleans staging.
        if cancel is not None and cancel.is_set():
            raise SpokeCancelled("spoke cancelled before vault promotion (stall budget exceeded)")

        result = promote(
            staging,
            key,
            candidate=candidate,
            ledger=ledger,
            person_vault=person_vault,
            ai_package=ai_package,
            cancel=cancel,
        )
        # Surface the branch2 bundle so a branch1-only G3 re-emit can reuse it.
        return replace(result, analysis=analysis)
    except (StructuralSealFailed, ProduceGateBlocked, AnchorGateError):
        # A gate hard-failed: its exception carries `staging` (the failure scene),
        # so do NOT let `finally` delete it. SpokeCancelled + success keep this
        # False, so their staging is still cleaned up (no temp leak).
        handed_off = True
        raise
    except EngineAbort as exc:
        # ADR-0011: a transport abort (e.g. the Qwen audit endpoint dropped) must
        # NOT let `finally` delete a built-but-unverified ARA. If the staged branch2
        # ARA exists, hand `staging` to the spoke (which scenes it) via the same
        # `staged_dir` attribute the gate exceptions use, then re-raise so the tick
        # still aborts (cost guard unchanged). An abort BEFORE the ARA is built
        # (analyzer transport down) leaves no ARA → fall through to the finally rm.
        if ara_is_nonempty(staging / "ai" / "ara"):
            exc.staged_dir = staging
            handed_off = True
        raise
    finally:
        if not handed_off:
            shutil.rmtree(staging, ignore_errors=True)
