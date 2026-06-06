"""Atomic dual-output: both vaults or neither (OT-5); overwrite by identity (OT-2)."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.output.produce import produce_outputs
from scripts.output.ara_schema import validate_ara_tree


def test_produce_writes_both_vaults_with_same_key(tmp_path, candidate, ledger, md_path):
    result = produce_outputs(md_path, candidate, ledger, root=tmp_path)
    person = tmp_path / "person_vault" / result.key
    ai = tmp_path / "ai_package" / result.key
    assert person.is_dir() and ai.is_dir()
    assert result.key.startswith("2026-06-05_DiffusionDrive_")
    assert (person / "report.md").exists()
    assert validate_ara_tree(ai / "ara") == []


def test_produce_is_atomic_neither_on_branch1_failure(
    tmp_path, candidate, ledger, md_path, monkeypatch
):
    import scripts.output.produce as prod

    def boom(*a, **k):
        raise RuntimeError("branch1 blew up")

    monkeypatch.setattr(prod, "write_branch1", boom)
    with pytest.raises(RuntimeError):
        produce_outputs(md_path, candidate, ledger, root=tmp_path)
    # OT-5: neither vault holds a partial entry.
    assert not (tmp_path / "person_vault").exists() or not any(
        (tmp_path / "person_vault").iterdir()
    )
    assert not (tmp_path / "ai_package").exists() or not any((tmp_path / "ai_package").iterdir())


def test_reprocess_overwrites_prior_identity_entry(tmp_path, candidate, ledger, md_path):
    r1 = produce_outputs(md_path, candidate, ledger, root=tmp_path)
    # Simulate a later run on a different intake date, same paper identity.
    ledger._intake = __import__("datetime").date(2026, 7, 1)
    r2 = produce_outputs(md_path, candidate, ledger, root=tmp_path)
    assert r1.key != r2.key  # date prefix refreshed
    # Exactly ONE entry per identity per vault (OT-2).
    person_entries = list((tmp_path / "person_vault").iterdir())
    ai_entries = list((tmp_path / "ai_package").iterdir())
    assert len(person_entries) == 1
    assert len(ai_entries) == 1
    assert person_entries[0].name == r2.key


def test_produce_records_code_ref_in_ledger(tmp_path, candidate, ledger, md_path):
    result = produce_outputs(md_path, candidate, ledger, root=tmp_path)
    assert result.key in ledger.code_refs
