"""Atomic dual-output orchestrator (OT-5) — public entrypoint.

`produce_outputs(md_path, candidate, ledger)` builds branch2 (ai_package) FIRST,
then branch1 (person_vault) DERIVED from it, in a STAGING directory; runs the
ARA Seal-1 validator + the three-layer anchor gate; and only on full success
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
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.output.ara_schema import validate_ara_tree
from scripts.output.branch1_llm import write_branch1_llm
from scripts.output.branch1_report import write_branch1
from scripts.output.branch2_ara import write_branch2
from scripts.output.naming import find_existing_entries, vault_key


@dataclass(frozen=True)
class ProduceResult:
    """Outcome of one dual-output run."""

    key: str
    person_path: Path
    ai_path: Path


class ProduceGateBlocked(Exception):
    """G2 hard-blocked the staged branch2 BEFORE branch1/promotion (OT-5 holds).

    Carries the blocking verdict so the spoke can record the reason; nothing has
    reached either real vault when this is raised.
    """

    def __init__(self, verdict: Any) -> None:
        self.verdict = verdict
        super().__init__("branch2 hard-blocked by the G2 data-fidelity gate")


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


def produce_outputs(
    md_path: Path,
    candidate: Any,
    ledger: Any,
    root: Path | None = None,
    *,
    resolve_analysis: Callable[[Path, Any], dict],
    g2_gate: Callable[[Path], Any] | None = None,
    write_report: Callable[..., dict] | None = None,
    cancel: threading.Event | None = None,
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
    analysis = resolve_analysis(md_path, candidate)

    # Stage everything in a temp dir; promote only after both gates pass.
    staging = Path(tempfile.mkdtemp(prefix="paper-rolling-stage-"))
    try:
        stage_ai = staging / "ai" / "ara"
        stage_person = staging / "person"
        write_branch2(stage_ai, candidate, analysis, md_path=md_path)

        ara_errors = validate_ara_tree(stage_ai)
        if ara_errors:
            raise ValueError(f"branch2 failed Seal-1: {'; '.join(ara_errors[:5])}")

        # G2 (after branch2, before branch1): adversarial data-fidelity gate on
        # the staged ARA evidence. A hard block aborts BEFORE branch1 and any
        # promotion, so OT-5 holds (nothing reaches the real vault).
        if g2_gate is not None:
            verdict = g2_gate(staging / "ai")  # staged ai ENTRY dir (parent of ara/)
            if verdict.blocked:
                raise ProduceGateBlocked(verdict)
            # Tolerant mode: G2 returned non-blocking (advisory) data-fidelity
            # findings. The paper is kept, but the tolerated numbers are MARKED in
            # the pack so the miss is visible downstream rather than silently
            # absorbed (config/audit.yaml data_fidelity.mode: tolerant).
            if verdict.findings:
                _write_audit_flags(stage_ai, verdict)

        # branch1 derives from branch2 and self-gates on the anchor lint;
        # any unanchored empirical claim raises AnchorGateError here. `key` is
        # the shared vault key so branch1 links to the paired ai_package.
        # With a `write_report` seam, the human report is LLM-written (vivid
        # Chinese sections + grounded assembly); else the deterministic thin
        # renderer. Both pass the SAME three-layer anchor hard-gate.
        if write_report is not None:
            write_branch1_llm(stage_person, candidate, stage_ai, md_path, write_report, key=key)
        else:
            write_branch1(stage_person, candidate, stage_ai, md_path, analysis, key=key)

        # B2 / Codex R17: last safe point before any real-vault write. If the
        # per-paper guard already abandoned this spoke (stall budget exceeded), a
        # late-finishing daemon thread must NOT promote products the hub has
        # recorded as failed — bail out; the `finally` cleans staging.
        if cancel is not None and cancel.is_set():
            raise SpokeCancelled("spoke cancelled before vault promotion (stall budget exceeded)")

        # Both gates passed → promote atomically. Remove prior same-identity
        # entries first (OT-2), then move staging into place.
        #
        # SEAM (ADR-0002, deferred): this promotion is written for exactly TWO
        # co-promoted branches (person + ai). Only the branch SET is centralized
        # (paths.VAULT_BRANCHES); generalizing this block to N-or-neither awaits a
        # real 3rd branch — see docs/guides/EXTENDING.md "Add an output branch".
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
        shutil.move(str(stage_person), str(person_dest))
        shutil.move(str(staging / "ai"), str(ai_dest))

        # B2 / Codex R18+R19: REVERT the promotion if the guard fired during any
        # durable step. There is one cancel re-check after EACH such step (the
        # moves, then the code-ref ledger note), so a cancel landing in either
        # window undoes both vault dirs. This closes both reproduced races
        # (slow shutil.move, slow record_code_ref). On revert the (idempotent)
        # code-ref note may already be appended — harmless: landscapes scan vault
        # dirs, not code-ref notes, and the next-tick reconciliation (see
        # store.consistency_check) prunes any vault dir not backed by a `done`
        # row regardless.
        #
        # RESIDUAL (Codex R20): once promotion succeeds here, the vault dirs exist
        # for the rest of the abandoned worker's life — not just until this
        # function returns, but through the spoke's post-promotion G3 pass too.
        # So a stalled worker can briefly leave a promoted vault for a paper the
        # hub has recorded `failed`. This is the irreducible cost of cancelling a
        # non-killable thread mid-commit; it is NOT reproducible by app-code delay
        # injection beyond this point, and store.consistency_check prunes any such
        # orphan (vault dir without a complete `done` row) at the next tick start,
        # so it self-heals within one tick (eventual consistency). A literal
        # zero-residual would require moving promotion out of the spoke thread into
        # the single-writer hub (a larger change; ADR if pursued).
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
    finally:
        shutil.rmtree(staging, ignore_errors=True)
