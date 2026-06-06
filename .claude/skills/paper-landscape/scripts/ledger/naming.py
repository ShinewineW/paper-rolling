"""Version / identity idempotency keys for the ledger (OT-1, no LLM).

This module owns the two ledger idempotency keys — `identity_key` (vault dedup /
overwrite, version-STRIPPED) and `version_key` (version-AWARE skip key). They are
a DIFFERENT concern from vault NAMING: the single live vault-key authority is
`scripts.output.naming.vault_key`.

NOTE — these helpers are SUPERSEDED on the live path (retained because they are
plan-built and unit-tested). The live ledger keys its rows by the hub-derived
candidate key (arxiv_id→doi→title, see `hub._candidate_key` / `store.record`),
not by these helpers; live vault naming is `scripts.output.naming.vault_key`.
"""

from __future__ import annotations

import hashlib
import re

_ARXIV_VERSION_RE = re.compile(r"v\d+$")


def _strip_arxiv_version(arxiv_id: str) -> str:
    """Drop a trailing vN from an arXiv id, leaving the base identity."""
    return _ARXIV_VERSION_RE.sub("", arxiv_id)


def identity_key(arxiv_id: str | None, doi: str | None) -> str:
    """Identity key for vault dedup/overwrite (version-STRIPPED).

    arxiv_id base wins; else a stable short hash of the DOI (so the key is
    filesystem-safe regardless of DOI slashes). One of the two must be set.

    Raises:
        ValueError: if both arxiv_id and doi are None/empty.
    """
    if arxiv_id:
        return _strip_arxiv_version(arxiv_id)
    if doi:
        digest = hashlib.sha256(doi.encode("utf-8")).hexdigest()[:12]
        return f"doi-{digest}"
    raise ValueError("identity_key requires arxiv_id or doi")


def version_key(arxiv_id: str | None, arxiv_version: str | None, doi: str | None) -> str:
    """Version-aware idempotency key: arxiv_id@version (primary) | doi (fallback).

    A v1→v2 revision yields a DIFFERENT key, so the revised paper is not in the
    skip-set and gets reprocessed (§3.2).

    Raises:
        ValueError: if neither an arxiv_id nor a doi is supplied.
    """
    if arxiv_id:
        base = _strip_arxiv_version(arxiv_id)
        ver = arxiv_version or ""
        return f"{base}{ver}"
    if doi:
        return doi
    raise ValueError("version_key requires arxiv_id or doi")
