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
