"""CitationCache: SQLite PK (key,resolver,query_form), 90-day TTL, invalidate."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from scripts.discovery.cache import TTL_DAYS, CitationCache


def test_put_then_get_roundtrips(tmp_path):
    db = CitationCache(path=str(tmp_path / "c.db"))
    db.put("1706.03762", "openalex", "default.search:transformer", {"cited_by_count": 134000})
    assert db.get("1706.03762", "openalex", "default.search:transformer") == {
        "cited_by_count": 134000
    }


def test_miss_returns_none(tmp_path):
    db = CitationCache(path=str(tmp_path / "c.db"))
    assert db.get("nope", "openalex", "q") is None


def test_pk_distinguishes_resolver_and_query_form(tmp_path):
    db = CitationCache(path=str(tmp_path / "c.db"))
    db.put("k", "openalex", "q1", {"v": 1})
    db.put("k", "s2", "q1", {"v": 2})
    db.put("k", "openalex", "q2", {"v": 3})
    assert db.get("k", "openalex", "q1") == {"v": 1}
    assert db.get("k", "s2", "q1") == {"v": 2}
    assert db.get("k", "openalex", "q2") == {"v": 3}


def test_expired_entry_is_a_miss(tmp_path):
    import sqlite3

    dbpath = str(tmp_path / "c.db")
    db = CitationCache(path=dbpath)
    db.put("k", "openalex", "q", {"v": 1})
    # The vendored VerificationCache has no _force_timestamp seam — age the row
    # by editing its real `verification_timestamp` column directly (Round 6 F2).
    stale = (datetime.now(UTC) - timedelta(days=TTL_DAYS + 1)).isoformat()
    with sqlite3.connect(dbpath) as conn:
        conn.execute(
            "UPDATE verification_cache SET verification_timestamp = ? "
            "WHERE citation_key = ? AND resolver_name = ? AND query_form = ?",
            (stale, "k", "openalex", "q"),
        )
    assert db.get("k", "openalex", "q") is None


def test_put_overwrites_same_key(tmp_path):
    db = CitationCache(path=str(tmp_path / "c.db"))
    db.put("k", "openalex", "q", {"v": 1})
    db.put("k", "openalex", "q", {"v": 99})
    assert db.get("k", "openalex", "q") == {"v": 99}


def test_invalidate_drops_all_rows_for_key(tmp_path):
    db = CitationCache(path=str(tmp_path / "c.db"))
    db.put("k", "openalex", "q", {"v": 1})
    db.put("k", "s2", "q", {"v": 2})
    db.invalidate("k")
    assert db.get("k", "openalex", "q") is None
    assert db.get("k", "s2", "q") is None
