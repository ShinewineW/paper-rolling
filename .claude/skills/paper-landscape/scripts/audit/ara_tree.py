"""Shared ARA-tree read helpers (audit-side).

The canonical read layer over a paper's `ara/` tree, used by BOTH audit gates
(G2 data-fidelity, G3 seal) and available to any future gate/analyzer. Promoted
out of `g2_data_fidelity` so gates no longer reach across each other's private
symbols (ADR-0002): G3 used to import G2's private `_find_ara_dir` /
`extract_claim_registry`, which coupled a refactor of one gate to the other.

Read-only: nothing here mutates the tree.
"""

from __future__ import annotations

import re
from pathlib import Path

from scripts.audit.types import ClaimRecord, ClaimType

# Matches integers and decimals. The `(?<![A-Za-z0-9])` lookbehind excludes
# digits glued to an identifier (claim/experiment IDs like C01, E02) so number
# extraction sees only real evidence/metric numbers — NOT structural artifacts.
# Without it, "C01" yielded "01", which an honest skeptic cannot find in the
# source MD, hard-blocking legitimate papers (Codex Round-10).
_NUMBER = re.compile(r"(?<![A-Za-z0-9])-?\d+(?:\.\d+)?")
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


def find_ara_dir(entry_dir: Path) -> Path:
    """Resolve the `ara/` directory under a vault entry. Accepts either the
    entry dir (…/{key}) or a dir already containing `ara/`."""
    if (entry_dir / "ara").is_dir():
        return entry_dir / "ara"
    children = [c for c in entry_dir.iterdir() if (c / "ara").is_dir()]
    if children:
        return children[0] / "ara"
    return entry_dir / "ara"
