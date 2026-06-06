"""paper-landscape corpus ledger: idempotency + long-range stability.

Public API consumed by the hub (Chunk 5) and the dual-output layer (Chunk 4).
"""

from __future__ import annotations

from .corpus import CorpusRecord, append_record, load_records
from .naming import (
    derive_name,
    identity_key,
    vault_entry_name,
    version_key,
)
from .store import Ledger, LedgerLockError, overwrite_vault_entry

__all__ = [
    "CorpusRecord",
    "Ledger",
    "LedgerLockError",
    "append_record",
    "derive_name",
    "identity_key",
    "load_records",
    "overwrite_vault_entry",
    "vault_entry_name",
    "version_key",
]
