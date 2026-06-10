"""Ledger: atomic write, status states, version-aware skip, SHA drift,
negative-cache TTL, LS-1 lock, LS-3 crash-resume, LS-4 self-heal."""

from __future__ import annotations

import importlib.util
from datetime import UTC, datetime, timedelta
from pathlib import Path

_STORE = (
    Path(__file__).resolve().parents[2] / ".claude/skills/paper-landscape/scripts/ledger/store.py"
)
_spec = importlib.util.spec_from_file_location("store", _STORE)
store = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(store)

Ledger = store.Ledger
LedgerLockError = store.LedgerLockError


def _now():
    return datetime.now(UTC)


def _iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


# ---- LS-2 atomic write + status states -------------------------------------


def test_record_status_then_load_roundtrip(tmp_path):
    led = Ledger(tmp_path)
    led.record_status("1706.03762v5", status="done", md_sha256="abc")
    entries = led.load_entries()
    assert len(entries) == 1
    assert entries[0]["key"] == "1706.03762v5"
    assert entries[0]["status"] == "done"
    assert entries[0]["md_sha256"] == "abc"


def test_ledger_write_is_append_only(tmp_path):
    led = Ledger(tmp_path)
    led.record_status("k1", status="discovered")
    led.record_status("k1", status="converted")
    # Append-only: two rows for the same key, latest wins on read helpers.
    assert len(led.load_entries()) == 2


def test_atomic_write_leaves_no_temp_file(tmp_path):
    led = Ledger(tmp_path)
    led.record_status("k1", status="done", md_sha256="x")
    ledger_dir = tmp_path / "_ledger"
    leftovers = [p.name for p in ledger_dir.iterdir() if p.name != "processed_ledger.yaml"]
    # No .tmp residue; the lock file only exists inside acquire().
    assert all(not n.endswith(".tmp") for n in leftovers)


# ---- §3.2 version-aware skip-set -------------------------------------------


def test_skip_set_includes_done_unrescinded(tmp_path):
    led = Ledger(tmp_path)
    led.record_status("1706.03762v5", status="done", md_sha256="abc")
    assert "1706.03762v5" in led.load_skip_set()


def test_skip_set_excludes_non_done(tmp_path):
    led = Ledger(tmp_path)
    led.record_status("k1", status="analyzed")
    assert "k1" not in led.load_skip_set()


def test_version_revision_not_skipped(tmp_path):
    # v5 done; v6 is a DIFFERENT key → must NOT be in skip-set (reprocess).
    led = Ledger(tmp_path)
    led.record_status("1706.03762v5", status="done", md_sha256="abc")
    skip = led.load_skip_set()
    assert "1706.03762v5" in skip
    assert "1706.03762v6" not in skip


def test_skip_set_excludes_rescinded(tmp_path):
    led = Ledger(tmp_path)
    led.record_status("k1", status="done", md_sha256="abc")
    led.invalidate("k1")
    assert "k1" not in led.load_skip_set()


# ---- §3.2 hash-on-fetch drift ----------------------------------------------


def test_sha_drift_detected(tmp_path):
    led = Ledger(tmp_path)
    led.record_status("k1", status="done", md_sha256="abc")
    assert led.has_sha_drift("k1", "abc") is False
    assert led.has_sha_drift("k1", "DIFFERENT") is True


def test_sha_drift_unknown_key_is_not_drift(tmp_path):
    led = Ledger(tmp_path)
    assert led.has_sha_drift("never-seen", "abc") is False


# ---- §3.2 negative cache TTL -----------------------------------------------


def test_deferred_with_future_retry_is_skipped(tmp_path):
    led = Ledger(tmp_path)
    future = _iso(_now() + timedelta(days=21))
    led.record_status("k1", status="deferred", failure_class="not_indexed_yet", retry_after=future)
    assert "k1" in led.load_skip_set()


def test_deferred_with_elapsed_retry_is_not_skipped(tmp_path):
    led = Ledger(tmp_path)
    past = _iso(_now() - timedelta(days=1))
    led.record_status("k1", status="deferred", failure_class="not_indexed_yet", retry_after=past)
    assert "k1" not in led.load_skip_set()


def test_negative_cache_ttl_by_failure_class(tmp_path):
    led = Ledger(tmp_path)
    now = _now()
    assert led.retry_after_for("not_indexed_yet", now) == _iso(now + timedelta(days=21))
    assert led.retry_after_for("convert_error", now) == _iso(now + timedelta(days=1))
    assert led.retry_after_for(None, now) is None


# ---- LS-1 concurrency lock --------------------------------------------------


def test_acquire_creates_and_releases_lock(tmp_path):
    led = Ledger(tmp_path)
    with led.acquire():
        assert led.lock_path.exists()
    # The lock FILE persists by design (its flock state IS the lock — never
    # unlinked, see acquire() docstring). What must hold after release is that
    # the lock is FREE: immediately re-acquirable.
    assert led.lock_path.exists()
    with led.acquire():
        assert led.lock_path.exists()


def test_second_instance_refused(tmp_path):
    led_a = Ledger(tmp_path)
    led_b = Ledger(tmp_path)
    with led_a.acquire():
        try:
            with led_b.acquire():
                raised = False
        except LedgerLockError:
            raised = True
        assert raised is True


def test_refused_contender_does_not_release_holders_lock(tmp_path):
    # Codex Round-2 regression: a refused second instance must NOT unlink the
    # lock file. If it did, a third instance would O_CREAT a fresh inode and
    # flock it successfully while the first still holds the original — two
    # concurrent writers. After ANY number of refusals, a new start must STILL
    # be refused while the original holder is active.
    holder = Ledger(tmp_path)
    with holder.acquire():
        second_refused = False
        try:
            with Ledger(tmp_path).acquire():
                pass
        except LedgerLockError:
            second_refused = True
        assert second_refused is True

        third_refused = False
        try:
            with Ledger(tmp_path).acquire():
                pass
        except LedgerLockError:
            third_refused = True
        assert third_refused is True


def test_lock_reusable_after_release(tmp_path):
    led = Ledger(tmp_path)
    with led.acquire():
        pass
    # A fresh acquire after clean release must succeed.
    with led.acquire():
        assert led.lock_path.exists()


# ---- LS-3 crash-resume sweep ------------------------------------------------


def test_crash_resume_cleans_partial_vault(tmp_path):
    led = Ledger(tmp_path)
    # A paper got to 'analyzed' (not done) and left half a vault entry + clone.
    pv = tmp_path / "person_vault" / "2026-06-05_Foo_1234.5678"
    pv.mkdir(parents=True)
    (pv / "report.md").write_text("partial", encoding="utf-8")
    clone = tmp_path / ".clones" / "1234.5678"
    clone.mkdir(parents=True)
    led.record_status(
        "1234.5678v1",
        status="analyzed",
        person_vault_path=str(pv),
    )
    removed = led.crash_resume_sweep()
    assert str(pv) in removed
    assert not pv.exists()
    assert not clone.exists()  # whole .clones dir swept


def test_crash_resume_keeps_done_artifacts(tmp_path):
    led = Ledger(tmp_path)
    pv = tmp_path / "person_vault" / "2026-06-05_Bar_9999.0000"
    pv.mkdir(parents=True)
    led.record_status("9999.0000v1", status="done", person_vault_path=str(pv))
    led.crash_resume_sweep()
    assert pv.exists()  # done rows are never swept


# ---- LS-4 startup consistency self-heal ------------------------------------


def test_consistency_check_demotes_done_missing_vault(tmp_path):
    led = Ledger(tmp_path)
    pv = tmp_path / "person_vault" / "2026-06-05_Baz_1111.2222"
    ai = tmp_path / "ai_package" / "2026-06-05_Baz_1111.2222"
    pv.mkdir(parents=True)
    # ai_package missing → inconsistent done row.
    led.record_status(
        "1111.2222v1",
        status="done",
        md_sha256="h",
        person_vault_path=str(pv),
        ai_package_path=str(ai),
    )
    demoted = led.consistency_check()
    assert "1111.2222v1" in demoted
    # Demoted key is no longer in the skip-set → will be reprocessed.
    assert "1111.2222v1" not in led.load_skip_set()


def test_consistency_check_iterates_the_branch_field_set(tmp_path, monkeypatch):
    """consistency_check is driven by paths.VAULT_BRANCH_PATH_FIELDS (ADR-0002):
    extending the branch set makes the self-heal require the new branch too —
    with zero edit to consistency_check itself."""
    from scripts import paths

    led = Ledger(tmp_path)
    pv = tmp_path / "person_vault" / "2026-06-05_R_5555.6666"
    ai = tmp_path / "ai_package" / "2026-06-05_R_5555.6666"
    pv.mkdir(parents=True)
    ai.mkdir(parents=True)
    led.record_status(
        "5555.6666v1",
        status="done",
        md_sha256="h",
        person_vault_path=str(pv),
        ai_package_path=str(ai),
    )
    # Standard 2-branch set: the row is complete.
    assert led.consistency_check() == []
    # Add a 3rd branch field the row does not record → the SAME row is now
    # incomplete and demoted, proving the set is the single control point.
    monkeypatch.setattr(
        paths,
        "VAULT_BRANCH_PATH_FIELDS",
        paths.VAULT_BRANCH_PATH_FIELDS + ("slides_path",),
    )
    assert "5555.6666v1" in led.consistency_check()


def test_consistency_check_prunes_orphan_vault_dirs(tmp_path):
    """Codex R19 / B2 residual self-heal: a vault dir NOT backed by a complete
    `done` row (an orphan from a crash or a stalled-then-resumed spoke that
    promoted late) is pruned at tick start, so it never persists in the library."""
    led = Ledger(tmp_path)
    # A legit done paper: both halves on disk + a done row claiming them.
    pv = tmp_path / "person_vault" / "2026-06-05_Good_1.1"
    ai = tmp_path / "ai_package" / "2026-06-05_Good_1.1"
    pv.mkdir(parents=True)
    ai.mkdir(parents=True)
    led.record_status(
        "1.1v1",
        status="done",
        md_sha256="h",
        person_vault_path=str(pv),
        ai_package_path=str(ai),
    )
    # An ORPHAN: vault dirs on disk with NO done row pointing at them.
    orphan_pv = tmp_path / "person_vault" / "2026-06-05_Orphan_9.9"
    orphan_ai = tmp_path / "ai_package" / "2026-06-05_Orphan_9.9"
    orphan_pv.mkdir(parents=True)
    orphan_ai.mkdir(parents=True)

    led.consistency_check()

    assert pv.exists() and ai.exists()  # the legit done paper is kept
    assert not orphan_pv.exists()  # the orphan is pruned...
    assert not orphan_ai.exists()


def test_consistency_check_keeps_complete_done(tmp_path):
    led = Ledger(tmp_path)
    pv = tmp_path / "person_vault" / "2026-06-05_Q_3333.4444"
    ai = tmp_path / "ai_package" / "2026-06-05_Q_3333.4444"
    pv.mkdir(parents=True)
    ai.mkdir(parents=True)
    led.record_status(
        "3333.4444v1",
        status="done",
        md_sha256="h",
        person_vault_path=str(pv),
        ai_package_path=str(ai),
    )
    demoted = led.consistency_check()
    assert demoted == []
    assert "3333.4444v1" in led.load_skip_set()


# ---- /paper-landscape-invalidate CLI ---------------------------------------


def test_cli_invalidate_rescinds_key(tmp_path, capsys):
    led = Ledger(tmp_path)
    led.record_status("k1", status="done", md_sha256="abc")
    rc = store.main(["k1", "--topic-dir", str(tmp_path)])
    assert rc == 0
    assert "k1" not in Ledger(tmp_path).load_skip_set()


def test_cli_invalidate_unknown_key_errors(tmp_path):
    led = Ledger(tmp_path)
    led.record_status("k1", status="done", md_sha256="abc")
    rc = store.main(["does-not-exist", "--topic-dir", str(tmp_path)])
    assert rc == 2


def test_audit_deferred_no_ttl_enters_skip_set(tmp_path):
    # ADR-0007: an audit hard-block records deferred with NO retry_after → it must
    # skip UNCONDITIONALLY (wait for explicit batch revival, not a /loop auto-retry).
    led = Ledger(tmp_path)
    led.record("k1", status="deferred", failure_class="audit_block", retry_after=None)
    assert "k1" in led.skip_set()
