"""Read-only corpus status — the engine's external state surface.

Answers "where does every paper stand right now?" without the ledger lock, without
any LLM, deterministically from the filesystem + ledger. Safe to run at any time
(including mid-run, while a /loop tick or revival holds the LS-1 lock) because it
only READS. Built for humans and external observers (CI, a dashboard):

    PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.status
    PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.status --json

Per-paper state (keyed by idbase = arXiv id), most-to-least done:
  compliant   — promoted AND report opens with 「## 评价」, carries no <!--ref/anchor-->,
                and the ARA is sealed (level2_report.json passes_seal2). The bar.
  done-stale  — promoted (both vaults) but NOT compliant: a pre-ADR-0012-rev report
                (no 评价 / has retired anchors) or an unsealed ARA (no level2_report).
  failed      — a preserved _failed/ scene (quarantined; ARA may be complete).
  ingested    — corpus MD exists but no product yet (not processed).
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from pathlib import Path

import yaml

_ARXIV = re.compile(r"\d{4}\.\d{4,5}")


def _idbase(name: str) -> str:
    """arXiv-id idbase, extracted BY PATTERN so it works regardless of naming order:
    a vault key (`date_Name_<id>`, id is the suffix), a corpus dir (`<id>_Name`, id is
    the prefix), or a bare-id scene (`<id>`). Falls back to the last `_` segment (DOI keys)."""
    m = _ARXIV.search(name)
    return m.group(0) if m else name.rsplit("_", 1)[-1]


def _ledger_latest(workspace: Path) -> dict[str, dict]:
    """Latest ledger row per key, read lock-free (append-only; last write wins)."""
    f = workspace / "_ledger" / "processed_ledger.yaml"
    if not f.exists():
        return {}
    doc = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    out: dict[str, dict] = {}
    for row in doc.get("processed", []):
        if isinstance(row, dict) and row.get("key"):
            out[str(row["key"])] = row  # later rows overwrite earlier → latest wins
    return out


def _report_compliant(report_md: Path) -> bool:
    if not report_md.exists():
        return False
    t = report_md.read_text(encoding="utf-8")
    return "## 评价" in t and "<!--ref:" not in t and "<!--anchor:" not in t


def _ara_sealed(ai_dir: Path) -> bool:
    l2 = ai_dir / "ara" / "level2_report.json"
    if not l2.exists():
        return False
    try:
        return bool(
            json.loads(l2.read_text(encoding="utf-8")).get("overall", {}).get("passes_seal2")
        )
    except (ValueError, OSError):
        return False


def collect(workspace: Path) -> list[dict]:
    """One record per paper (keyed by idbase), classified by current state."""
    ws = workspace
    led = _ledger_latest(ws)
    pv = {
        _idbase(Path(d).name): Path(d)
        for d in glob.glob(str(ws / "person_vault" / "*"))
        if Path(d).is_dir() and not Path(d).name.startswith("_")
    }
    ai = {
        _idbase(Path(d).name): Path(d)
        for d in glob.glob(str(ws / "ai_package" / "*"))
        if Path(d).is_dir() and not Path(d).name.startswith("_")
    }
    failed = {
        _idbase(Path(d).name): Path(d)
        for d in glob.glob(str(ws / "_failed" / "*"))
        if Path(d).is_dir() and Path(d).name != "_orphans"
    }
    corpus = {
        _idbase(Path(d).name): Path(d)
        for d in glob.glob(str(ws / "corpus" / "*"))
        if Path(d).is_dir()
    }

    recs: list[dict] = []
    for ib in sorted(set(pv) | set(ai) | set(failed) | set(corpus)):
        if ib in pv and ib in ai:
            sealed = _ara_sealed(ai[ib])
            compliant = _report_compliant(pv[ib] / "report.md") and sealed
            state = "compliant" if compliant else "done-stale"
            detail = (
                ""
                if compliant
                else ("unsealed-ARA" if not sealed else "stale-report(no 评价/anchors)")
            )
            recs.append({"idbase": ib, "key": pv[ib].name, "state": state, "detail": detail})
        elif ib in failed:
            recs.append(
                {
                    "idbase": ib,
                    "key": failed[ib].name,
                    "state": "failed",
                    "detail": "preserved _failed scene",
                }
            )
        elif ib in corpus:
            recs.append(
                {
                    "idbase": ib,
                    "key": corpus[ib].name,
                    "state": "ingested",
                    "detail": "corpus MD, no product yet",
                }
            )
        else:  # in pv XOR ai only — an orphan half-pair
            recs.append(
                {
                    "idbase": ib,
                    "key": (pv[ib].name if ib in pv else ai[ib].name),
                    "state": "orphan",
                    "detail": "person_vault/ai_package not paired",
                }
            )
    for r in recs:  # enrich with the engine's own recorded status (latest ledger row)
        r["ledger"] = (led.get(r["idbase"]) or {}).get("status")
    return recs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="paper-rolling corpus status (read-only)")
    ap.add_argument("--workspace", default=".")
    ap.add_argument("--json", action="store_true", help="machine-readable JSON")
    args = ap.parse_args(argv)
    recs = collect(Path(args.workspace))

    order = ["compliant", "done-stale", "failed", "ingested", "orphan"]
    counts = {s: sum(1 for r in recs if r["state"] == s) for s in order}
    counts = {s: n for s, n in counts.items() if n}

    if args.json:
        print(
            json.dumps(
                {"total": len(recs), "counts": counts, "papers": recs}, ensure_ascii=False, indent=2
            )
        )
        return 0

    print(f"paper-rolling status — {len(recs)} papers\n")
    for r in sorted(recs, key=lambda r: (order.index(r["state"]), r["idbase"])):
        mark = {
            "compliant": "✅",
            "done-stale": "⚠️ ",
            "failed": "❌",
            "ingested": "·",
            "orphan": "‼️ ",
        }.get(r["state"], "?")
        det = f"  ({r['detail']})" if r["detail"] else ""
        print(f"  {mark} {r['state']:11} {r['idbase']:14} {r['key'][:46]}{det}")
    print("\n" + "  ".join(f"{s}={n}" for s, n in counts.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
