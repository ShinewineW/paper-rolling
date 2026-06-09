# .claude/skills/paper-landscape/scripts/audit_config.py
"""User-tunable audit knobs (trade strictness vs cost), loaded from
``config/audit.yaml``.

The adversarial audit (G2 number-fidelity + G3 seal) is deliberately strict, but
strictness costs tokens (more skeptic votes, more re-emit rounds) and can
quarantine an otherwise-good paper over a single mis-transcribed number. These
knobs let the operator dial that trade WITHOUT editing engine code or the locked
campaign Hard Gate (``config/campaign.yaml`` stays the topic/N decision; this is
separate, operational tuning).

Every field has a safe default, so ``config/audit.yaml`` is OPTIONAL — absent or
partial, the defaults below apply. The defaults favor a LIGHT, tolerant run; an
operator who wants the original maximal-strictness behavior sets
``mode: strict`` and raises ``skeptic_votes`` / ``max_gate_rounds``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

AUDIT_CONFIG_REL = Path("config") / "audit.yaml"

_VALID_MODES = ("tolerant", "strict")


@dataclass(frozen=True)
class AuditConfig:
    """Resolved audit knobs. Immutable; build via :func:`load_audit_config`.

    Attributes:
        skeptic_votes: Number of independent G2 skeptic passes per paper. ODD
            values give a clean majority (1 = single pass; 3 = best-of-three).
            Higher = stricter + more tokens.
        max_gate_rounds: How many times a blocked gate re-emits the offending
            branch before the paper is quarantined. 1 = no retry.
        g2_blind_retry_rounds: Independent G2 number-gate blind-retry budget — how
            many times a G2 hard-block re-runs the analyzer (fresh sampling, no
            rubric injection) before quarantine. Separate from max_gate_rounds
            (the content-gate re-emit budget). 1 = one blind retry. (ADR-0006)
        data_fidelity_tolerant: When True, a small number of unconfirmed evidence
            numbers (within the limits below) are FLAGGED but do NOT block the
            paper. When False (strict), any unconfirmed number hard-blocks it.
        data_fidelity_max_unconfirmed: Tolerant mode only — absolute ceiling on
            how many unconfirmed numbers may be tolerated.
        data_fidelity_max_unconfirmed_ratio: Tolerant mode only — the unconfirmed
            count must also stay within this fraction of all checked numbers.
    """

    skeptic_votes: int = 1
    max_gate_rounds: int = 1
    g2_blind_retry_rounds: int = 1  # 数字门盲重试预算（独立于内容门 max_gate_rounds，ADR-0006）
    data_fidelity_tolerant: bool = True
    data_fidelity_max_unconfirmed: int = 5
    data_fidelity_max_unconfirmed_ratio: float = 0.2

    def __post_init__(self) -> None:
        if self.skeptic_votes < 1:
            raise ValueError(f"skeptic_votes must be >= 1, got {self.skeptic_votes}")
        if self.max_gate_rounds < 1:
            raise ValueError(f"max_gate_rounds must be >= 1, got {self.max_gate_rounds}")
        if self.data_fidelity_max_unconfirmed < 0:
            raise ValueError(
                f"data_fidelity.max_unconfirmed must be >= 0, "
                f"got {self.data_fidelity_max_unconfirmed}"
            )
        if not 0.0 <= self.data_fidelity_max_unconfirmed_ratio <= 1.0:
            raise ValueError(
                "data_fidelity.max_unconfirmed_ratio must be in [0.0, 1.0], "
                f"got {self.data_fidelity_max_unconfirmed_ratio}"
            )


def load_audit_config(workspace: Path) -> AuditConfig:
    """Load ``config/audit.yaml`` from the workspace, or defaults if absent.

    Args:
        workspace: The paper-rolling workspace root.

    Returns:
        The resolved :class:`AuditConfig`.

    Raises:
        ValueError: The file exists but carries an invalid value (e.g. an unknown
            ``mode`` or an out-of-range knob) — fail fast rather than silently
            mis-tune the gate.
    """
    path = Path(workspace) / AUDIT_CONFIG_REL
    if not path.exists():
        return AuditConfig()

    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError(f"{AUDIT_CONFIG_REL} must be a YAML mapping, got {type(raw).__name__}")

    df = raw.get("data_fidelity") or {}
    if not isinstance(df, dict):
        raise ValueError("audit.yaml 'data_fidelity' must be a mapping")
    mode = df.get("mode", "tolerant")
    if mode not in _VALID_MODES:
        raise ValueError(f"data_fidelity.mode must be one of {_VALID_MODES}, got {mode!r}")

    defaults = AuditConfig()
    return AuditConfig(
        skeptic_votes=int(raw.get("skeptic_votes", defaults.skeptic_votes)),
        max_gate_rounds=int(raw.get("max_gate_rounds", defaults.max_gate_rounds)),
        g2_blind_retry_rounds=int(raw.get("g2_blind_retry_rounds", defaults.g2_blind_retry_rounds)),
        data_fidelity_tolerant=(mode == "tolerant"),
        data_fidelity_max_unconfirmed=int(
            df.get("max_unconfirmed", defaults.data_fidelity_max_unconfirmed)
        ),
        data_fidelity_max_unconfirmed_ratio=float(
            df.get("max_unconfirmed_ratio", defaults.data_fidelity_max_unconfirmed_ratio)
        ),
    )
