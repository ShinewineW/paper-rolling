"""Deterministic naming + key helpers (OT-1/OT-3, no LLM).

The `Name` derivation is a FIXED algorithm so vault keys are stable across
runs — re-deriving the same arXiv title always yields the same entry name,
which is what keeps person_vault ↔ ai_package pairing intact (OT-3).

NOTE — SUPERSEDED on the live path (retained because it is plan-built and
unit-tested). The live pipeline does NOT call any helper in this module: the
ledger keys its rows by the hub-derived candidate key (arxiv_id→doi→title, see
`hub._candidate_key` / `store.record`), and live vault naming is
`scripts.output.naming.vault_key`. New callers should use `scripts.output.naming`
(naming/keying) — these helpers exist only for their own tests.
"""

from __future__ import annotations

import hashlib
import re

_NAME_MAX = 40
_ARXIV_VERSION_RE = re.compile(r"v\d+$")


def _strip_arxiv_version(arxiv_id: str) -> str:
    """Drop a trailing vN from an arXiv id, leaving the base identity."""
    return _ARXIV_VERSION_RE.sub("", arxiv_id)


def derive_name(title: str) -> str:
    """Derive the CamelCase {Name} segment from a paper title.

    Algorithm (deterministic, OT-3): hyphens/underscores → spaces, drop every
    non-alphanumeric char, split on whitespace, capitalize each token's first
    letter, concatenate, truncate to 40 chars. Empty result → "Untitled".

    NOTE — NOT the live vault-key authority. The live pipeline (produce_outputs
    → spoke → ledger.record) names entries via `scripts.output.naming.vault_key`
    / `derive_name`, which SPLIT the title on the first ':' (this one does NOT),
    yielding a DIFFERENT name for colon-titled papers. Pinned by its own test;
    use `scripts.output.naming` for any new caller. (`identity_key` /
    `version_key` below are likewise NOT called on the live path — the ledger
    keys rows by the hub-derived candidate key; see the module docstring.)

    Args:
        title: Raw paper title (typically the arXiv title).

    Returns:
        A non-empty CamelCase identifier of length <= 40.
    """
    # De-hyphenate first so "End-to-End" becomes three tokens, not one blob.
    spaced = re.sub(r"[-_]+", " ", title)
    # Keep only alphanumerics and spaces.
    cleaned = re.sub(r"[^0-9A-Za-z ]+", "", spaced)
    tokens = cleaned.split()
    camel = "".join(t[:1].upper() + t[1:] for t in tokens)
    if not camel:
        return "Untitled"
    return camel[:_NAME_MAX]


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


def vault_entry_name(ingest_date: str, title: str, arxiv_id: str | None, doi: str | None) -> str:
    """OT-1 vault entry name: {ingest_date}_{Name}_{identity}.

    `ingest_date` is the INGEST day (YYYY-MM-DD), never the publication date
    (双输出-D5). The identity suffix uniquifies same-day same-name papers.

    NOTE — NOT the live vault-key authority. The live pipeline (produce_outputs
    → spoke → ledger.record) builds the vault entry name with
    `scripts.output.naming.vault_key` (which splits the title on ':') and the
    ledger records the path produce_outputs returns verbatim — never this
    function. Pinned by its own test; use `scripts.output.naming.vault_key` for
    any new caller.
    """
    return f"{ingest_date}_{derive_name(title)}_{identity_key(arxiv_id, doi)}"
