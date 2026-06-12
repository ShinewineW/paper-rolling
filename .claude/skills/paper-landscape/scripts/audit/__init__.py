"""Audit gates for paper-landscape v2.

G1 is deleted (ADR-0001: authority is multi-signal scoring, no citation hard gate).
G2 = data-fidelity adversarial gate (runs AFTER branch2 / BEFORE branch1, hard-blocks
fabrication). G3 = branch1 presence (G3R0) + type-aware entailment + 6-dim rigor seal +
equation fidelity (runs AFTER branches, blocks + re-emits on hard failure). ADR-0012 rev
retired the branch1<->MD anchor-resolution sub-check (branch1 carries no anchors).
"""

from __future__ import annotations

from scripts.audit.types import (
    ClaimRecord,
    ClaimType,
    Finding,
    GateOutcome,
    GateVerdict,
    Severity,
    SkepticVote,
)

__all__ = [
    "ClaimRecord",
    "ClaimType",
    "Finding",
    "GateOutcome",
    "GateVerdict",
    "Severity",
    "SkepticVote",
]
