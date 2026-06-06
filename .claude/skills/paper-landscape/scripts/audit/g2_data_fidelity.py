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

from scripts.audit.types import (
    ClaimRecord,
    ClaimType,
    Finding,
    GateVerdict,
    Severity,
    SkepticVote,
    SkepticVoteFn,
)

# Matches integers and decimals (incl. signed/percent contexts). Captures the
# numeric token only; surrounding %/× are handled by the source text match.
_NUMBER = re.compile(r"-?\d+(?:\.\d+)?")
_CLAIM_HEADER = re.compile(r"^##\s+(C\d{2,}):\s*(.+?)\s*$", re.MULTILINE)
_PROOF_LINE = re.compile(r"\*\*Proof\*\*:\s*(.+)$", re.MULTILINE)
_EXP_ID = re.compile(r"E\d{2,}")

_CAUSAL = ("causes", "leads to", "enables", "because", "drives")
_GENERALIZATION = ("generalizes", "robust", "across", "transfers")
_IMPROVEMENT = ("outperform", "better", "improves", "beats", "exceeds", "surpass")
_SCOPING = ("when", "under conditions", "limited to", "only when")


def extract_numbers(text: str) -> tuple[str, ...]:
    """All distinct numeric tokens in `text`, order-preserving."""
    seen: list[str] = []
    for m in _NUMBER.finditer(text):
        tok = m.group(0)
        if tok not in seen:
            seen.append(tok)
    return tuple(seen)


def _infer_claim_type(statement: str) -> ClaimType:
    low = statement.lower()
    if any(k in low for k in _CAUSAL):
        return ClaimType.CAUSAL
    if any(k in low for k in _IMPROVEMENT):
        return ClaimType.IMPROVEMENT
    if any(k in low for k in _GENERALIZATION):
        return ClaimType.GENERALIZATION
    if any(k in low for k in _SCOPING):
        return ClaimType.SCOPING
    return ClaimType.DESCRIPTIVE


def extract_claim_registry(ara_dir: Path) -> tuple[ClaimRecord, ...]:
    """Parse logic/claims.md into a Claim Registry."""
    claims_md = ara_dir / "logic" / "claims.md"
    if not claims_md.exists():
        return ()
    text = claims_md.read_text(encoding="utf-8")
    headers = list(_CLAIM_HEADER.finditer(text))
    records: list[ClaimRecord] = []
    for i, m in enumerate(headers):
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        body = text[start:end]
        claim_id = m.group(1)
        statement = m.group(2)
        # Pull a fuller statement line if present.
        stmt_match = re.search(r"\*\*Statement\*\*:\s*(.+)$", body, re.MULTILINE)
        if stmt_match:
            statement = stmt_match.group(1).strip()
        proof_ids: tuple[str, ...] = ()
        proof = _PROOF_LINE.search(body)
        if proof:
            proof_ids = tuple(_EXP_ID.findall(proof.group(1)))
        records.append(
            ClaimRecord(
                claim_id=claim_id,
                statement=statement,
                claim_type=_infer_claim_type(statement),
                numbers=extract_numbers(statement),
                proof_experiment_ids=proof_ids,
            )
        )
    return tuple(records)


def _collect_evidence_numbers(ara_dir: Path) -> tuple[str, ...]:
    """Every number that appears in evidence/ tables + the claim statements.
    These are the candidates that MUST ground in the source MD."""
    seen: list[str] = []

    def _add(text: str) -> None:
        for n in extract_numbers(text):
            if n not in seen:
                seen.append(n)

    evidence = ara_dir / "evidence"
    if evidence.exists():
        for md_file in sorted(evidence.rglob("*.md")):
            _add(md_file.read_text(encoding="utf-8"))
    for rec in extract_claim_registry(ara_dir):
        for n in rec.numbers:
            if n not in seen:
                seen.append(n)
    return tuple(seen)


def _majority_says_missing(votes_per_round: list[tuple[SkepticVote, ...]], number: str) -> bool:
    """True iff a strict majority of skeptic rounds reported `number` NOT found."""
    missing = 0
    total = 0
    for round_votes in votes_per_round:
        for v in round_votes:
            if v.number == number:
                total += 1
                if not v.found_in_source:
                    missing += 1
    return total > 0 and missing * 2 > total


def run_g2(
    ai_package_dir: Path,
    md_path: Path,
    *,
    skeptic_votes: SkepticVoteFn,
    n_skeptics: int = 3,
) -> GateVerdict:
    """Run the G2 data-fidelity gate for one paper's ai_package.

    `ai_package_dir` is the per-paper vault entry directory (containing `ara/`).
    `md_path` is the source MD (ground truth). Hard-blocks any evidence number
    that the majority of skeptics cannot locate in the source.
    """
    ara_dir = _find_ara_dir(ai_package_dir)
    source_md = md_path.read_text(encoding="utf-8")
    candidate_numbers = _collect_evidence_numbers(ara_dir)

    if not candidate_numbers:
        return GateVerdict(gate="G2", findings=())

    votes_per_round: list[tuple[SkepticVote, ...]] = []
    for _ in range(n_skeptics):
        votes_per_round.append(
            skeptic_votes(candidate_numbers, source_md, claim_context="G2 data-fidelity audit")
        )

    findings: list[Finding] = []
    for idx, number in enumerate(candidate_numbers, start=1):
        if _majority_says_missing(votes_per_round, number):
            findings.append(
                Finding(
                    finding_id=f"G2F{idx:02d}",
                    severity=Severity.CRITICAL,
                    target=str(ara_dir.relative_to(ai_package_dir.parent)),
                    observation=(
                        f"evidence number {number!r} not found in source MD by "
                        f"majority skeptic vote — likely fabricated or "
                        f"mis-transcribed"
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


def _find_ara_dir(entry_dir: Path) -> Path:
    """Resolve the `ara/` directory under a vault entry. Accepts either the
    entry dir (…/{key}) or a dir already containing `ara/`."""
    if (entry_dir / "ara").is_dir():
        return entry_dir / "ara"
    children = [c for c in entry_dir.iterdir() if (c / "ara").is_dir()]
    if children:
        return children[0] / "ara"
    return entry_dir / "ara"
