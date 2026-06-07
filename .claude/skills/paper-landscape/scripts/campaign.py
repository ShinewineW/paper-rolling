# .claude/skills/paper-landscape/scripts/campaign.py
"""Campaign Hard Gate (中枢-D1 / 吸收-D4).

The Hard Gate confirms topic + per-tick N exactly ONCE, when the campaign is
established (a human is present), and locks the decision into
``config/campaign.yaml``. Daily ``/loop`` ticks read the locked config and run
autonomously — they do NOT re-gate. Only changing the topic or N re-fires the
gate.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

CAMPAIGN_REL = Path("config") / "campaign.yaml"


class GateError(ValueError):
    """Raised when the campaign gate inputs are vague or invalid."""


def _validate_topic(topic: str) -> str:
    topic = (topic or "").strip()
    # "不容模糊": a precise topic must be more than a single bare term.
    if len(topic) < 8 or len(topic.split()) < 2:
        raise GateError(
            f"topic {topic!r} is too vague — confirm a precise, narrowed topic "
            "(more than one term) before the campaign starts"
        )
    return topic


def _validate_n(n_per_tick: int) -> int:
    if not isinstance(n_per_tick, int) or n_per_tick < 1:
        raise GateError(f"n_per_tick {n_per_tick!r} must be a positive integer")
    return n_per_tick


# A force-included paper needs (1) an INGESTIBLE source the engine can actually
# fetch — an arXiv id (HTML/PDF) or a direct PDF URL; a bare DOI is NOT ingestible
# (there is no DOI->PDF resolver) — AND (2) a distinct IDENTITY so two entries
# never collide into one corpus dir / ledger key (中枢-D1; a doi still helps dedup
# but cannot stand alone, and an oa_pdf_url-only entry must add a title).
_INGESTIBLE_KEYS = ("arxiv_id", "oa_pdf_url")
_IDENTITY_KEYS = ("arxiv_id", "doi", "title")


def _validate_force_include(entries: list) -> list:
    """Validate each force-include entry (中枢-D1: confirmed at the Hard Gate)."""
    if not isinstance(entries, list):
        raise GateError(f"force_include must be a list, got {type(entries).__name__}")
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            raise GateError(f"force_include[{i}] must be a dict, got {type(e).__name__}")
        if not any(e.get(k) for k in _INGESTIBLE_KEYS):
            raise GateError(
                f"force_include[{i}] needs an ingestible source — arxiv_id or "
                f"oa_pdf_url (a bare DOI cannot be fetched)"
            )
        if not any(e.get(k) for k in _IDENTITY_KEYS):
            raise GateError(
                f"force_include[{i}] needs a distinct identity — arxiv_id, doi, or "
                f"title (an oa_pdf_url-only entry must add a title to avoid collisions)"
            )
    return entries


@dataclass(frozen=True)
class CampaignConfig:
    """The locked campaign decision: topic + per-tick N + AD-domain flag, plus an
    optional list of force-included papers (must-process, beyond autonomous
    discovery — 中枢-D1)."""

    topic: str
    n_per_tick: int
    is_ad_domain: bool
    force_include: list[dict] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Reads-only validation (frozen dataclass — no field assignment here).
        _validate_topic(self.topic)
        _validate_n(self.n_per_tick)
        _validate_force_include(self.force_include)


def load_campaign(workspace: Path) -> CampaignConfig | None:
    """Return the locked CampaignConfig, or None if no campaign established yet."""
    path = Path(workspace) / CAMPAIGN_REL
    if not path.exists():
        return None
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return CampaignConfig(
        topic=data["topic"],
        n_per_tick=int(data["n_per_tick"]),
        is_ad_domain=bool(data["is_ad_domain"]),
        force_include=list(data.get("force_include") or []),
    )


def write_campaign(workspace: Path, cfg: CampaignConfig) -> None:
    """Lock the campaign decision to config/campaign.yaml (HITL-confirmed)."""
    path = Path(workspace) / CAMPAIGN_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(asdict(cfg), allow_unicode=True, sort_keys=True),
        encoding="utf-8",
    )


def gate_needed(
    workspace: Path,
    *,
    requested_topic: str | None,
    requested_n: int | None,
) -> bool:
    """True if the Hard Gate must fire before processing.

    Fires when (a) no campaign exists (first-time), or (b) the caller requests a
    topic/N that differs from the locked config. A bare /loop tick
    (requested_topic and requested_n both None) on an established campaign never
    re-gates.
    """
    cfg = load_campaign(workspace)
    if cfg is None:
        return True
    if requested_topic is not None and requested_topic.strip() != cfg.topic:
        return True
    if requested_n is not None and requested_n != cfg.n_per_tick:
        return True
    return False
