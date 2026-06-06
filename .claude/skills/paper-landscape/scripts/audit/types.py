"""Shared audit types: verdicts, findings, severity, claim records.

Frozen dataclasses + enums used across G2, equation-fidelity, and G3 so the
gates speak one vocabulary. A verdict is `blocked` iff it carries at least one
hard-block finding (audit-D1: fabrication / structural failures are
non-acknowledgeable hard blocks; access/soft findings are advisory).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class Severity(Enum):
    """Rigor-reviewer severity taxonomy (review-dimensions.md)."""

    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    SUGGESTION = "suggestion"

    @property
    def rank(self) -> int:
        return {
            Severity.SUGGESTION: 0,
            Severity.MINOR: 1,
            Severity.MAJOR: 2,
            Severity.CRITICAL: 3,
        }[self]


class ClaimType(Enum):
    """Claim types for the type-aware entailment table (review-dimensions.md D1)."""

    CAUSAL = "causal"
    GENERALIZATION = "generalization"
    IMPROVEMENT = "improvement"
    DESCRIPTIVE = "descriptive"
    SCOPING = "scoping"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Finding:
    """A single audit finding. `is_hard_block` marks fabrication/structural
    failures that the spoke may NOT acknowledge away (audit-D1)."""

    finding_id: str
    severity: Severity
    target: str
    observation: str
    is_hard_block: bool = False
    reasoning: str = ""
    suggestion: str = ""

    def as_dict(self) -> dict[str, object]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity.value,
            "target": self.target,
            "observation": self.observation,
            "is_hard_block": self.is_hard_block,
            "reasoning": self.reasoning,
            "suggestion": self.suggestion,
        }


@dataclass(frozen=True)
class GateVerdict:
    """Result of running one gate. `blocked` is derived, never set directly."""

    gate: str
    findings: tuple[Finding, ...] = ()

    @property
    def hard_findings(self) -> tuple[Finding, ...]:
        return tuple(f for f in self.findings if f.is_hard_block)

    @property
    def blocked(self) -> bool:
        return len(self.hard_findings) > 0

    def as_dict(self) -> dict[str, object]:
        return {
            "gate": self.gate,
            "blocked": self.blocked,
            "findings": [f.as_dict() for f in self.findings],
        }


@dataclass(frozen=True)
class ClaimRecord:
    """One row of the G2 Claim Registry: a claim + the exact numbers it asserts
    + the experiment IDs that should ground it."""

    claim_id: str
    statement: str
    claim_type: ClaimType
    numbers: tuple[str, ...] = ()
    proof_experiment_ids: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, object]:
        return {
            "claim_id": self.claim_id,
            "statement": self.statement,
            "claim_type": self.claim_type.value,
            "numbers": list(self.numbers),
            "proof_experiment_ids": list(self.proof_experiment_ids),
        }


@dataclass(frozen=True)
class GateOutcome:
    """Outcome of a bounded gate-runner loop (gate_runner.run_with_budget)."""

    passed: bool
    escalated: bool
    rounds_used: int
    failed_path: str | None = None
    final_verdict: GateVerdict | None = None


@dataclass(frozen=True)
class SkepticVote:
    """One skeptic's verdict on one (number, claim, source) triple."""

    number: str
    found_in_source: bool
    note: str = ""


class SkepticVoteFn(Protocol):
    """Ground-truth-isolated skeptic seam. Receives ONLY the candidate numbers
    + the source MD text — never the answer key or a rubric. Returns one vote
    per number. Injected so tests use a deterministic fake."""

    def __call__(
        self, numbers: tuple[str, ...], source_md: str, claim_context: str
    ) -> tuple[SkepticVote, ...]: ...


class EntailmentJudgeFn(Protocol):
    """Seam for the type-aware entailment check. Receives a claim + its linked
    experiment text; returns (entailed, reason)."""

    def __call__(self, claim: ClaimRecord, experiment_text: str) -> tuple[bool, str]: ...


class RigorScoreFn(Protocol):
    """Seam for the 6-dim rigor reviewer. Receives the ARA text bundle; returns
    {dimension_key: (score:int, strengths, weaknesses, suggestions)} + raw
    findings. Rubric is held privately by the implementation (ground-truth
    isolation) and never appears in any generator prompt."""

    def __call__(self, ara_bundle: dict[str, str]) -> dict[str, object]: ...
