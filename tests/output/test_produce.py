"""Atomic dual-output: both vaults or neither (OT-5); overwrite by identity (OT-2)."""

from __future__ import annotations

import pytest
from scripts.output.ara_schema import validate_ara_tree
from scripts.output.produce import produce_outputs


def test_produce_writes_both_vaults_with_same_key(tmp_path, candidate, ledger, md_path, analyzer):
    result = produce_outputs(md_path, candidate, ledger, root=tmp_path, resolve_analysis=analyzer)
    person = tmp_path / "person_vault" / result.key
    ai = tmp_path / "ai_package" / result.key
    assert person.is_dir() and ai.is_dir()
    assert result.key.startswith("2026-06-05_DiffusionDrive_")
    assert (person / "report.md").exists()
    assert validate_ara_tree(ai / "ara") == []


def test_produce_is_atomic_neither_on_branch1_failure(
    tmp_path, candidate, ledger, md_path, analyzer, monkeypatch
):
    import scripts.output.produce as prod

    def boom(*a, **k):
        raise RuntimeError("branch1 blew up")

    monkeypatch.setattr(prod, "write_branch1", boom)
    with pytest.raises(RuntimeError):
        produce_outputs(md_path, candidate, ledger, root=tmp_path, resolve_analysis=analyzer)
    # OT-5: neither vault holds a partial entry.
    assert not (tmp_path / "person_vault").exists() or not any(
        (tmp_path / "person_vault").iterdir()
    )
    assert not (tmp_path / "ai_package").exists() or not any((tmp_path / "ai_package").iterdir())


def test_reprocess_overwrites_prior_identity_entry(tmp_path, candidate, ledger, md_path, analyzer):
    r1 = produce_outputs(md_path, candidate, ledger, root=tmp_path, resolve_analysis=analyzer)
    # Simulate a later run on a different intake date, same paper identity.
    ledger._intake = __import__("datetime").date(2026, 7, 1)
    r2 = produce_outputs(md_path, candidate, ledger, root=tmp_path, resolve_analysis=analyzer)
    assert r1.key != r2.key  # date prefix refreshed
    # Exactly ONE entry per identity per vault (OT-2).
    person_entries = list((tmp_path / "person_vault").iterdir())
    ai_entries = list((tmp_path / "ai_package").iterdir())
    assert len(person_entries) == 1
    assert len(ai_entries) == 1
    assert person_entries[0].name == r2.key


def test_produce_records_code_ref_in_ledger(tmp_path, candidate, ledger, md_path, analyzer):
    result = produce_outputs(md_path, candidate, ledger, root=tmp_path, resolve_analysis=analyzer)
    assert result.key in ledger.code_refs


def test_produce_aborts_before_promotion_when_cancelled(
    tmp_path, candidate, ledger, md_path, analyzer
):
    """Codex R17 stall-isolation: if the per-paper guard's cancel is already set
    by the time both gates pass, produce_outputs must NOT promote to the vault —
    a stalled-then-resumed daemon spoke leaves no products behind (OT-5 holds)."""
    import threading

    from scripts.output.produce import SpokeCancelled

    cancel = threading.Event()
    cancel.set()
    with pytest.raises(SpokeCancelled):
        produce_outputs(
            md_path,
            candidate,
            ledger,
            root=tmp_path,
            resolve_analysis=analyzer,
            cancel=cancel,
        )
    # Neither vault holds a partial entry.
    assert not (tmp_path / "person_vault").exists() or not any(
        (tmp_path / "person_vault").iterdir()
    )
    assert not (tmp_path / "ai_package").exists() or not any((tmp_path / "ai_package").iterdir())


def test_produce_uses_passed_resolve_analysis_not_a_global(
    tmp_path, candidate, ledger, md_path, analysis
):
    """The analyzer seam is a parameter (no module global): the passed callable
    is the one invoked, and produce.py exposes no mutable `resolve_analysis`
    global. Foundation review: threaded spokes must not race a shared analyzer.
    """
    import scripts.output.produce as prod

    assert not hasattr(prod, "resolve_analysis")  # the mutable module global was removed

    calls = []

    def spy(md, cand):
        calls.append((md, cand))
        return analysis

    produce_outputs(md_path, candidate, ledger, root=tmp_path, resolve_analysis=spy)
    assert calls == [(md_path, candidate)]
