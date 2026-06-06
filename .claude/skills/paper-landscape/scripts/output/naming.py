"""Deterministic vault naming + identity keys.

OT-3: `{Name}` derives from the arXiv title by a FIXED algorithm — no LLM
improvisation — so keys stay stable across runs and branch1↔branch2 pairing
never breaks. OT-1: vault key = `{intake_date}_{Name}_{idbase}` is unique even
when same-day same-shortname collide. OT-2: re-processing locates the prior
entry by identity (arxiv base id || DOI short-hash), ignoring its date prefix.
"""

from __future__ import annotations

import datetime
import hashlib
import re
from pathlib import Path

_KEEP = re.compile(r"[A-Za-z0-9]+")
_NAME_MAX = 60


def derive_name(title: str) -> str:
    """Derive a stable CamelCase `{Name}` from a paper title.

    Algorithm: take the substring before the first colon (the conventional
    paper short-name), tokenize on any non-alphanumeric run, CamelCase the
    tokens, truncate to 60 chars. Deterministic and idempotent.

    Args:
        title: Raw paper title.

    Returns:
        CamelCase identifier, never empty.

    Raises:
        ValueError: If the title yields no alphanumeric tokens.
    """
    head = title.split(":", 1)[0]
    tokens = _KEEP.findall(head)
    if not tokens:
        tokens = _KEEP.findall(title)
    if not tokens:
        raise ValueError(f"title yields empty Name: {title!r}")
    name = "".join(tok[:1].upper() + tok[1:] for tok in tokens)
    return name[:_NAME_MAX]


def identity_base(arxiv_id: str | None, doi: str | None) -> str:
    """Canonical paper-identity key: arXiv base id, else DOI short hash.

    The arXiv id is taken WITHOUT version suffix (identity, not idempotency).
    """
    if arxiv_id:
        # Strip ONLY a trailing version (v\d+$). A naive split("v") would also cut
        # old-style IDs like "solv-int/9901001v1" at the first 'v' → "sol" (Codex R16).
        return re.sub(r"v\d+$", "", arxiv_id)
    if doi:
        digest = hashlib.sha256(doi.strip().lower().encode("utf-8")).hexdigest()[:8]
        return f"doi-{digest}"
    raise ValueError("identity_base requires arxiv_id or doi")


def vault_key(
    intake: datetime.date,
    title: str,
    arxiv_id: str | None,
    doi: str | None,
) -> str:
    """Build the unique vault entry key `{YYYY-MM-DD}_{Name}_{idbase}` (OT-1)."""
    return f"{intake.isoformat()}_{derive_name(title)}_{identity_base(arxiv_id, doi)}"


def find_existing_entries(
    vault_dir: Path,
    arxiv_id: str | None,
    doi: str | None,
) -> list[Path]:
    """Locate prior vault entries for this identity, ignoring date prefix (OT-2).

    Matches any `*_{idbase}` directory so an earlier-dated entry of the same
    paper can be deleted and rewritten with the current intake date.
    """
    if not vault_dir.exists():
        return []
    idbase = identity_base(arxiv_id, doi)
    return sorted(p for p in vault_dir.iterdir() if p.is_dir() and p.name.endswith(f"_{idbase}"))
