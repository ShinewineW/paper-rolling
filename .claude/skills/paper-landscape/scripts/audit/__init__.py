"""Audit gates for paper-landscape v2.

G1 is deleted (ADR-0001: authority is multi-signal scoring, no citation hard gate).
G2 = data-fidelity adversarial gate (runs AFTER branch2 / BEFORE branch1, hard-blocks
fabrication). G3 = branch1<->MD anchor resolution + type-aware entailment + 6-dim
rigor seal (runs AFTER branches, blocks + re-emits on hard failure).
"""

from __future__ import annotations

from scripts.audit.types import (
    ClaimRecord,
    Finding,
    GateOutcome,
    GateVerdict,
    Severity,
    SkepticVote,
)

__all__ = [
    "ClaimRecord",
    "Finding",
    "GateOutcome",
    "GateVerdict",
    "Severity",
    "SkepticVote",
]
