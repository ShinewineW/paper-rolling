"""Ledger version/identity idempotency keys (OT-1).

Vault NAMING (`derive_name` / `vault_entry_name`) was removed — the single live
vault-key authority is `scripts.output.naming.vault_key`. What remains here are
the ledger's version/identity idempotency keys, a different concern.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

# Import the engine module by file path (greenfield package not yet installed).
_NAMING = (
    Path(__file__).resolve().parents[2] / ".claude/skills/paper-landscape/scripts/ledger/naming.py"
)
_spec = importlib.util.spec_from_file_location("naming", _NAMING)
naming = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(naming)


def test_identity_key_strips_arxiv_version():
    assert naming.identity_key(arxiv_id="2306.07349v3", doi=None) == "2306.07349"
    assert naming.identity_key(arxiv_id="2306.07349", doi=None) == "2306.07349"


def test_identity_key_doi_fallback_short_hash():
    k = naming.identity_key(arxiv_id=None, doi="10.1109/CVPR52688.2022.01164")
    assert k.startswith("doi-")
    assert len(k) == len("doi-") + 12  # 12-char short hash, OT-1


def test_version_key_keeps_version():
    assert naming.version_key("2306.07349", "v3", None) == "2306.07349v3"
    assert naming.version_key("2306.07349", "v1", None) == "2306.07349v1"


def test_version_key_doi_fallback():
    assert naming.version_key(None, None, "10.5555/x") == "10.5555/x"
