"""Thin CLI entry for /paper-landscape-invalidate (force-reprocess).

Run as ``python -m scripts.invalidate <key>... --topic-dir <dir>``. The logic
lives in ``scripts.ledger.store.main``; this wrapper exists so the documented
command does NOT trigger the RuntimeWarning that ``python -m scripts.ledger.store``
emits (the ledger package ``__init__`` imports ``store``, so running ``store`` as
``__main__`` double-imports it — Codex R21).
"""

from __future__ import annotations

from scripts.ledger.store import main

if __name__ == "__main__":
    raise SystemExit(main())
