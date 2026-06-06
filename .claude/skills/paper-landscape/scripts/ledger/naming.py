"""Version / identity idempotency keys for the ledger (OT-1, no LLM).

This module owns the two ledger idempotency keys — `identity_key` (vault dedup /
overwrite, version-STRIPPED) and `version_key` (version-AWARE skip key). They are
a DIFFERENT concern from vault NAMING: the single live vault-key authority is
`scripts.output.naming.vault_key`.

NOTE — these helpers are SUPERSEDED on the live path (retained because they are
plan-built and unit-tested). The live ledger keys its rows by the hub-derived
candidate key (arxiv_id→doi→title, see `hub._candidate_key` / `store.record`),
not by these helpers; live vault naming is `scripts.output.naming.vault_key`.

Identity derivation has a SINGLE authority: `identity_key` delegates to
`scripts.output.naming.identity_base`, so there is exactly one arXiv-version-
strip rule and one DOI-hash algorithm/length across the whole tree (no latent
8-vs-12-hex divergence). `version_key` stays here — it is the version-AWARE skip
key, a distinct idempotency concern with no equivalent in output.naming.
"""

from __future__ import annotations

import re

from scripts.output.naming import identity_base

_ARXIV_VERSION_RE = re.compile(r"v\d+$")


def _strip_arxiv_version(arxiv_id: str) -> str:
    """Drop a trailing vN from an arXiv id, leaving the base identity."""
    return _ARXIV_VERSION_RE.sub("", arxiv_id)


def identity_key(arxiv_id: str | None, doi: str | None) -> str:
    """Identity key for vault dedup/overwrite (version-STRIPPED).

    Delegates to `scripts.output.naming.identity_base` (the single identity
    authority): arxiv_id base wins; else a stable short hash of the DOI (so the
    key is filesystem-safe regardless of DOI slashes). One of the two must be set.

    Raises:
        ValueError: if both arxiv_id and doi are None/empty.
    """
    return identity_base(arxiv_id, doi)


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
