"""G2 — data-fidelity adversarial gate (audit-D1).

Runs AFTER branch2 (on its staged ARA evidence), BEFORE branch1. Extracts every
numerical claim from the
ai_package evidence/claims into a Claim Registry, then runs an ADVERSARIAL
MULTI-VOTE: N skeptic invocations independently judge whether each number
appears in the source MD (the ground truth). A number that the MAJORITY of
skeptics cannot find in the source is a fabricated/mis-transcribed value and is
a HARD BLOCK — dirty data must never enter the knowledge base (the highest
poisoning-risk point).

Ground-truth isolation: the skeptic seam receives ONLY the candidate numbers +
the source MD text + a short claim context string. It never receives the
evidence file (the "answer key") nor a rubric. The seam is injected so the gate
is deterministic and testable; production wires it to N separate Agent-tool
invocations.
"""

from __future__ import annotations

import re
from pathlib import Path

from scripts.audit.ara_tree import extract_claim_registry, extract_numbers, find_ara_dir
from scripts.audit.types import (
    Finding,
    GateVerdict,
    Severity,
    SkepticVote,
    SkepticVoteFn,
)

# A markdown table separator row (| --- | --- |) — carries no data.
_TABLE_SEP = re.compile(r"^\|[\s:|-]+\|$")
# Provenance LOCATORS (Table 1 / §4 / Section 9 / Figure 2 / Eq 3 / Appendix A1).
# These are references, NOT evidence/metric values — strip them before counting
# so an honest skeptic does not hard-block a clean paper on a locator digit that
# happens to be absent from the source MD (Codex Round-10/11).
_LOCATOR = re.compile(
    r"(?i)(?:\b(?:tables?|tab|sections?|sec|figures?|fig|equations?|eq|appendix|app)\.?\s*|§\s*)\d+"
)


def _collect_evidence_numbers(ara_dir: Path) -> tuple[str, ...]:
    """Metric numbers in evidence-table DATA CELLS + claim statements — the
    candidates that MUST ground in the source MD.

    Deliberately scopes to the actual evidence VALUES and excludes provenance
    METADATA (Codex Round-10/11): only the markdown table DATA rows under
    evidence/tables/ are read (the per-table `# title` / `- **Source**` locator /
    `- **Caption**` lines and the evidence/README.md index are skipped), and
    locator references (Table 1 / §4 / Section 9 …) are stripped — so a locator
    digit absent from the source MD never false-blocks a clean paper, while a
    fabricated METRIC value in a data cell is still caught."""
    seen: list[str] = []

    def _add(text: str) -> None:
        for n in extract_numbers(_LOCATOR.sub(" ", text)):
            if n not in seen:
                seen.append(n)

    tables_dir = ara_dir / "evidence" / "tables"
    if tables_dir.exists():
        for md_file in sorted(tables_dir.glob("*.md")):
            in_data = False
            for line in md_file.read_text(encoding="utf-8").splitlines():
                stripped = line.strip()
                if not stripped.startswith("|"):
                    in_data = False  # left the table (# title / - Source / - Caption / blank)
                    continue
                if _TABLE_SEP.match(stripped):
                    in_data = True  # the `| --- |` separator: rows AFTER it are DATA
                    continue
                # Only DATA rows (after the separator). The HEADER row (before it)
                # is skipped — a column label can be a numeric metric name like
                # `Recall@10` / `mAP@0.5`, which is NOT an evidence value and must
                # not be verified against the source MD (Codex Round-12).
                if in_data:
                    _add(stripped)
    for rec in extract_claim_registry(ara_dir):
        _add(rec.statement)
    return tuple(seen)


def _insufficiently_confirmed(
    votes_per_round: list[tuple[SkepticVote, ...]], number: str, n_skeptics: int
) -> bool:
    """True iff `number` is NOT affirmatively confirmed present by a strict
    majority of the n_skeptics rounds — i.e. the gate must hard-block it.

    Fails CLOSED: missing votes, absent votes, and a malformed skeptic seam that
    returns no/partial votes ALL count as "not confirmed", so a misbehaving
    verifier can never silently pass an unverified (possibly fabricated) number.
    A number passes only when a strict majority of the EXPECTED rounds each
    affirmatively report it found in the source MD.
    """
    found = 0
    for round_votes in votes_per_round:
        for v in round_votes:
            if v.number == number and v.found_in_source:
                found += 1
                break  # at most one affirmative confirmation per round
    return found * 2 <= n_skeptics


def _cross_model_flags(cross_votes: tuple[SkepticVote, ...], number: str) -> bool:
    """True iff the cross-model verifier AFFIRMATIVELY voted `number` NOT found.

    The cross-model pass is a heterogeneous-family OVERLAY that can only ADD a
    block — catching a fabrication the in-family majority wrongly 'confirmed'
    (the conformity / premature-convergence failure mode of same-family voting,
    ROADMAP C2). It does NOT block on cross-model silence, so a partial/missing
    cross-model response cannot false-block a number the in-family vote cleared;
    the in-family check remains the fail-closed primary.
    """
    return any(v.number == number and not v.found_in_source for v in cross_votes)


def run_g2(
    ai_package_dir: Path,
    md_path: Path,
    *,
    skeptic_votes: SkepticVoteFn,
    n_skeptics: int = 3,
    cross_model_votes: SkepticVoteFn | None = None,
) -> GateVerdict:
    """Run the G2 data-fidelity gate for one paper's ai_package.

    `ai_package_dir` is the per-paper vault entry directory (containing `ara/`).
    `md_path` is the source MD (ground truth). Hard-blocks any evidence number
    NOT affirmatively confirmed present by a strict majority of skeptics — so the
    gate fails CLOSED if the skeptic seam misbehaves (returns no/partial votes).

    `cross_model_votes` (ROADMAP C2): an OPTIONAL second skeptic seam backed by a
    DIFFERENT model family. When supplied, a number is also blocked if the
    cross-model verifier disagrees (votes it missing) — catching fabrications the
    same-family majority's conformity bias let through. It only strengthens the
    gate; it never clears a number the in-family vote blocked.
    """
    ara_dir = find_ara_dir(ai_package_dir)
    source_md = md_path.read_text(encoding="utf-8")
    candidate_numbers = _collect_evidence_numbers(ara_dir)

    if not candidate_numbers:
        return GateVerdict(gate="G2", findings=())

    votes_per_round: list[tuple[SkepticVote, ...]] = []
    for _ in range(n_skeptics):
        votes_per_round.append(
            skeptic_votes(candidate_numbers, source_md, claim_context="G2 data-fidelity audit")
        )
    cross_votes: tuple[SkepticVote, ...] = ()
    if cross_model_votes is not None:
        cross_votes = tuple(
            cross_model_votes(
                candidate_numbers, source_md, claim_context="G2 cross-model verification"
            )
        )

    findings: list[Finding] = []
    for idx, number in enumerate(candidate_numbers, start=1):
        in_family_bad = _insufficiently_confirmed(votes_per_round, number, n_skeptics)
        cross_bad = _cross_model_flags(cross_votes, number)
        if in_family_bad or cross_bad:
            by = (
                "the cross-model verifier"
                if cross_bad and not in_family_bad
                else "a skeptic majority"
            )
            findings.append(
                Finding(
                    finding_id=f"G2F{idx:02d}",
                    severity=Severity.CRITICAL,
                    target=str(ara_dir.relative_to(ai_package_dir.parent)),
                    observation=(
                        f"evidence number {number!r} not confirmed present in the "
                        f"source MD by {by} — likely fabricated, mis-transcribed, "
                        f"or unverifiable"
                    ),
                    is_hard_block=True,
                    reasoning=(
                        "A number that appears in the AI package evidence but "
                        "not in the frozen source MD breaks the MD-only truth "
                        "chain and poisons the knowledge base."
                    ),
                    suggestion=(
                        "Re-extract the number from the source MD; if it is "
                        "genuinely absent, remove the claim/row before any "
                        "branch is emitted."
                    ),
                )
            )
    return GateVerdict(gate="G2", findings=tuple(findings))
