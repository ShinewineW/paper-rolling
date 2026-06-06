"""Ledger — HUB single-writer processed-state store (§3, LS-1..4, OT-2).

processed_ledger.yaml is append-only; every write goes through a temp file +
os.rename so a crash mid-write never corrupts the ledger (LS-2). The HUB is
the only writer (single-writer invariant, logging.md); spokes never call
record_status.
"""

from __future__ import annotations

import os
import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

import yaml

# Negative-cache TTL by failure class (§3.2). not_indexed_yet re-attempted
# after the OpenAlex-lag estimate; below_threshold re-checked after citation
# growth; convert_error is transient.
_NEGATIVE_TTL_DAYS = {
    "not_indexed_yet": 21,
    "below_threshold": 90,
    "convert_error": 1,
}

# Statuses that count as "successfully processed" for skip purposes.
_DONE = "done"


class LedgerLockError(RuntimeError):
    """Raised when a second instance cannot acquire the ledger lock (LS-1)."""


def _now() -> datetime:
    return datetime.now(UTC)


def _iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_iso(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


class Ledger:
    """Append-only processed-state ledger rooted at a topic directory."""

    def __init__(self, topic_dir: Path) -> None:
        self.topic_dir = Path(topic_dir)
        self.ledger_dir = self.topic_dir / "_ledger"
        self.ledger_path = self.ledger_dir / "processed_ledger.yaml"
        self.lock_path = self.ledger_dir / ".lock"
        self._lock_fd: int | None = None

    # -- raw load/append ----------------------------------------------------

    def load_entries(self) -> list[dict]:
        """Return all ledger rows in append order (empty if no file)."""
        if not self.ledger_path.exists():
            return []
        with self.ledger_path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data.get("processed", []) or []

    def _atomic_write(self, entries: list[dict]) -> None:
        """LS-2: write to a temp file in the same dir, then os.rename (atomic)."""
        self.ledger_dir.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=self.ledger_dir, prefix="processed_ledger.", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                yaml.safe_dump({"processed": entries}, f, sort_keys=False, allow_unicode=True)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, self.ledger_path)  # atomic rename on POSIX
        except BaseException:
            if os.path.exists(tmp):
                os.unlink(tmp)
            raise

    def record_status(
        self,
        key: str,
        *,
        status: str,
        md_sha256: str | None = None,
        failure_class: str | None = None,
        retry_after: str | None = None,
        person_vault_path: str | None = None,
        ai_package_path: str | None = None,
    ) -> None:
        """Append one status row for `key` (append-only, §3.2 status states).

        Statuses: discovered | converted | analyzed | done | failed | deferred.
        """
        entries = self.load_entries()
        entries.append(
            {
                "key": key,
                "md_sha256": md_sha256,
                "status": status,
                "failure_class": failure_class,
                "retry_after": retry_after,
                "person_vault_path": person_vault_path,
                "ai_package_path": ai_package_path,
                "processed_at": _iso(_now()),
            }
        )
        self._atomic_write(entries)

    # -- skip-set + drift + invalidate (§3.2) -------------------------------

    def _latest_by_key(self) -> dict[str, dict]:
        """Latest (last-appended) row per key — the effective current state."""
        latest: dict[str, dict] = {}
        for row in self.load_entries():
            latest[row["key"]] = row
        return latest

    def load_skip_set(self, now: datetime | None = None) -> set[str]:
        """§3.2 Step-0 key-only skip: done & not rescinded & retry not elapsed.

        A deferred row with a future retry_after is also skipped (negative
        cache still warm); once retry_after elapses the key drops out so it is
        re-fetched (OT-2 / R7 — never permanently suppressed).
        """
        now = now or _now()
        skip: set[str] = set()
        for key, row in self._latest_by_key().items():
            if row.get("rescinded_at"):
                continue
            ra = row.get("retry_after")
            retry_pending = ra is not None and now < _parse_iso(ra)
            if row["status"] == _DONE:
                skip.add(key)
            elif row["status"] == "deferred" and retry_pending:
                skip.add(key)
        return skip

    # --- consumer-facing API (Round 5 F3: hub + Chunk 4 call these names) ----
    def skip_set(self) -> set[str]:
        """Alias the hub uses (no-arg); delegates to load_skip_set()."""
        return self.load_skip_set()

    def record(self, key: str, *, status: str, **kwargs) -> None:
        """Alias the hub uses; delegates to record_status() (same kwargs:
        md_sha256/failure_class/retry_after/person_vault_path/ai_package_path)."""
        self.record_status(key, status=status, **kwargs)

    def intake_date(self) -> datetime.date:
        """Vault entries are keyed by ingest day (双输出-D5); Chunk 4 reads this."""
        return _now().date()

    def record_code_ref(self, key: str, path: str) -> None:
        """Remember where a paper's code_ref.md pointer was written (Chunk 4)."""
        self._code_refs = getattr(self, "_code_refs", {})
        self._code_refs[key] = path

    def entries(self) -> list[dict]:
        """Alias the hub/watchdog use (Round 6 F1); delegates to load_entries()."""
        return self.load_entries()

    def non_done_keys(self) -> list[str]:
        """Keys whose latest status is not 'done' — watchdog re-fire candidates (Round 6 F1)."""
        return [k for k, row in self._latest_by_key().items() if row["status"] != _DONE]

    def has_sha_drift(self, key: str, current_md_sha256: str) -> bool:
        """§3.2 hash-on-fetch: True iff key exists and its stored hash differs."""
        row = self._latest_by_key().get(key)
        if row is None or row.get("md_sha256") is None:
            return False
        return row["md_sha256"] != current_md_sha256

    def invalidate(self, key: str) -> bool:
        """Force-reprocess: write rescinded_at onto the latest unrescinded row.

        Soft-delete (audit-replayable). Returns True if a row was rescinded.
        """
        entries = self.load_entries()
        for row in reversed(entries):
            if row["key"] == key and not row.get("rescinded_at"):
                row["rescinded_at"] = _iso(_now())
                self._atomic_write(entries)
                return True
        return False

    def retry_after_for(self, failure_class: str | None, now: datetime) -> str | None:
        """§3.2 negative-cache TTL by failure class; None classes get no TTL."""
        days = _NEGATIVE_TTL_DAYS.get(failure_class or "")
        if days is None:
            return None
        return _iso(now + timedelta(days=days))
