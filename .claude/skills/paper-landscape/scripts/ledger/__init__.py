"""paper-landscape corpus ledger: idempotency + long-range stability.

Live API: `Ledger` / `LedgerLockError` / `overwrite_vault_entry` (store) + the
`corpus` record helpers — these are what the hub drives. The `naming` re-exports
(`derive_name`/`identity_key`/`vault_entry_name`/`version_key`) are SUPERSEDED on
the live path and retained only for their tests; live naming/keying uses
`scripts.output.naming.vault_key` + the hub-derived candidate key (see the
`ledger/naming.py` module docstring).
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
