"""OT-2 overwrite-by-identity: one vault entry per paper identity."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_STORE = (
    Path(__file__).resolve().parents[2] / ".claude/skills/paper-landscape/scripts/ledger/store.py"
)
_spec = importlib.util.spec_from_file_location("store", _STORE)
store = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(store)


def test_overwrite_deletes_old_dated_folder(tmp_path):
    vault = tmp_path / "person_vault"
    old = vault / "2026-06-01_DiffusionDrive_2411.15139"
    old.mkdir(parents=True)
    (old / "report.md").write_text("v1", encoding="utf-8")

    new = store.overwrite_vault_entry(
        vault_dir=vault,
        identity="2411.15139",
        new_entry_name="2026-06-05_DiffusionDrive_2411.15139",
    )
    assert new == vault / "2026-06-05_DiffusionDrive_2411.15139"
    assert new.exists()
    assert not old.exists()  # old dated folder deleted
    # Exactly one entry for this identity (OT-2).
    matches = list(vault.glob("*_2411.15139"))
    assert len(matches) == 1


def test_overwrite_first_time_just_creates(tmp_path):
    vault = tmp_path / "person_vault"
    new = store.overwrite_vault_entry(
        vault_dir=vault,
        identity="9999.0000",
        new_entry_name="2026-06-05_Foo_9999.0000",
    )
    assert new.exists()
    assert list(vault.glob("*_9999.0000")) == [new]


def test_overwrite_ignores_other_identities(tmp_path):
    vault = tmp_path / "person_vault"
    other = vault / "2026-06-01_Bar_1111.2222"
    other.mkdir(parents=True)
    store.overwrite_vault_entry(
        vault_dir=vault,
        identity="2411.15139",
        new_entry_name="2026-06-05_DiffusionDrive_2411.15139",
    )
    assert other.exists()  # untouched — different identity


def test_overwrite_same_name_idempotent(tmp_path):
    # Reprocess on the SAME ingest day → same target name; must not error and
    # must end with one clean (empty) entry.
    vault = tmp_path / "person_vault"
    name = "2026-06-05_DiffusionDrive_2411.15139"
    first = store.overwrite_vault_entry(vault_dir=vault, identity="2411.15139", new_entry_name=name)
    (first / "stale.md").write_text("stale", encoding="utf-8")
    second = store.overwrite_vault_entry(
        vault_dir=vault, identity="2411.15139", new_entry_name=name
    )
    assert second == first
    assert second.exists()
    assert not (second / "stale.md").exists()  # rebuilt clean
    assert len(list(vault.glob("*_2411.15139"))) == 1
