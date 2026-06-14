"""Read-only corpus status — the engine's external state surface.

Answers "where does every paper stand right now?" without the ledger lock, without
any LLM, deterministically from the filesystem + ledger. Safe to run at any time
(including mid-run, while a /loop tick or revival holds the LS-1 lock) because it
only READS. Built for humans and external observers (CI, a dashboard):

    PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.status
    PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.status --json

Per-paper state (keyed by idbase = arXiv id), most-to-least done:
  compliant      — promoted AND report opens with 「## 评价」, carries no <!--ref/anchor-->,
                   and the ARA is sealed (level2_report.json passes_seal2). The bar.
  corrupt-report — promoted but the report body is an ARA-not-loaded FAILURE (wrong-paper
                   hallucination): carries the engine's ARA-not-loaded markers or the
                   fallback `# ai_package` H1. Strictly worse than done-stale and NEVER
                   counted compliant — a bare "评价-present" check false-passed exactly
                   these (the 2026-06-13 regression). Re-emit required.
  done-stale     — promoted (both vaults) but NOT compliant: a pre-ADR-0012-rev report
                   (no 评价 / has retired anchors) or an unsealed ARA (no level2_report).
  failed         — a preserved _failed/ scene (quarantined; ARA may be complete).
  ingested       — corpus MD exists but no product yet (not processed).

Each paired record also carries `sealed` (ARA passes_seal2) so external tooling and the
card can show finer pipeline progress (ARA-sealed vs report-compliant), not just a binary.
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


# Engine-deterministic ARA-not-loaded fingerprints (copied verbatim from
# branch1_gate.py / branch1_llm.py so the substring match is exact). A report carrying
# any of these — or the fallback "# ai_package" H1 — is a wrong-paper hallucination,
# NOT a compliant product; the bare 评价-present check missed exactly these.
_ARA_NOT_LOADED = (
    "未能读取已验证知识包(ARA)",
    "已验证知识包(ARA)未提供",
    "已验证知识包(ARA)为空",
    "(未解析到结论)",
)


def _report_corrupt(report_md: Path) -> bool:
    """True if the report is an ARA-not-loaded failure body (wrong-paper hallucination)."""
    if not report_md.exists():
        return False
    t = report_md.read_text(encoding="utf-8")
    if any(m in t for m in _ARA_NOT_LOADED):
        return True
    return t.lstrip().startswith("# ai_package")  # title fell back to the parent dir name


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
            report_md = pv[ib] / "report.md"
            sealed = _ara_sealed(ai[ib])
            if _report_corrupt(report_md):
                # Strictly worse than done-stale and NEVER compliant: a wrong-paper
                # hallucination body (the 2026-06-13 blind spot). Must be re-emitted.
                state, detail = "corrupt-report", "ARA-not-loaded body (wrong-paper hallucination)"
            else:
                compliant = _report_compliant(report_md) and sealed
                state = "compliant" if compliant else "done-stale"
                detail = (
                    ""
                    if compliant
                    else ("unsealed-ARA" if not sealed else "stale-report(no 评价/anchors)")
                )
            recs.append(
                {
                    "idbase": ib,
                    "key": pv[ib].name,
                    "state": state,
                    "detail": detail,
                    "sealed": sealed,
                }
            )
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
    # 终审态(ADR-0013):合规产物是否已带 final_review.json。函数级 import 提到循环外,
    # 既避开 status↔final_review 的模块级耦合,又不在 for 体内逐条 import。
    from scripts.output.final_review import is_reviewed

    for r in recs:  # enrich with the engine's own recorded status (latest ledger row)
        led_row = led.get(r["idbase"]) or {}
        led_status = led_row.get("status")
        r["ledger"] = led_status
        # Ledger↔product divergence (Codex R1): a published+compliant product is
        # "ledger-synced" ONLY if its latest ledger row is a LIVE `done` row. A non-`done`
        # status OR a `done` row that was rescinded (invalidated for reprocess) both leave
        # the key OUT of skip_set — so the next /loop tick reprocesses it AND
        # consistency_check may prune its vault dirs (ADR-0011 keeps the ARA, but
        # person_vault is rebuilt). Surface it so an "all green" status never hides a paper
        # the engine is about to redo. (Rescinded-done was the 2026-06-11 blind spot.)
        synced = led_status == "done" and not led_row.get("rescinded_at")
        r["ledger_diverged"] = r["state"] == "compliant" and not synced
        ai_dir = ai.get(r["idbase"])  # 仅成对产物有 ai 目录;失败/孤儿/待入库为 None
        r["final_reviewed"] = bool(ai_dir and is_reviewed(ai_dir / "ara"))
    return recs


def _dw(s: str) -> int:
    """Display width: CJK / fullwidth code points occupy 2 terminal columns, so box
    borders line up when labels mix Chinese and ASCII. Box-drawing glyphs are width-1."""
    w = 0
    for ch in s:
        o = ord(ch)
        w += (
            2
            if (
                0x1100 <= o <= 0x115F
                or 0x2E80 <= o <= 0xA4CF
                or 0xAC00 <= o <= 0xD7A3
                or 0xF900 <= o <= 0xFAFF
                or 0xFE30 <= o <= 0xFE4F
                or 0xFF00 <= o <= 0xFF60
                or 0xFFE0 <= o <= 0xFFE6
                or 0x20000 <= o <= 0x3FFFD
            )
            else 1
        )
    return w


def _short(key: str) -> str:
    """Human-ish short name from a vault/scene key: drop the date prefix + id, keep
    the title slug; fall back to the bare id when there is no title (bare-id scenes)."""
    s = re.sub(r"^\d{4}-\d{2}-\d{2}_", "", key)
    s = _ARXIV.sub("", s).strip("_")
    return s[:22] if s else key


_GLYPH = {
    "compliant": "#",
    "corrupt-report": "X",
    "done-stale": ":",
    "failed": "x",
    "ingested": ".",
    "orphan": "!",
}
_ZH = {
    "compliant": "合规",
    "corrupt-report": "内容损坏",
    "done-stale": "待处理",
    "failed": "失败",
    "ingested": "待入库",
    "orphan": "孤儿",
}
# Pipeline order, most→least done. corrupt-report sits right after compliant: it is a
# promoted-but-broken product that must surface at the top as needing action.
_ORDER = ["compliant", "corrupt-report", "done-stale", "failed", "ingested", "orphan"]


def render_card(recs: list[dict], *, width: int = 60) -> str:
    """ASCII status card — the canonical at-a-glance progress view (stacked bar +
    bucket legend + actionable detail). Deterministic; safe to render any time."""
    order = _ORDER
    counts = {s: sum(1 for r in recs if r["state"] == s) for s in order}
    total = len(recs) or 1

    def row(content: str) -> str:  # pad content to the inner width, account for CJK
        pad = max(0, width - _dw(content))
        return "│" + content + " " * pad + "│"

    bar_w = width - 6
    bar = ""
    for s in order:
        bar += _GLYPH[s] * round(counts[s] / total * bar_w)
    bar = (bar + "." * bar_w)[:bar_w]  # pad/clip to exact width

    head_l = "  paper-rolling · 语料合规态"
    head_r = f"{len(recs)} 篇  "
    head = head_l + " " * max(1, width - _dw(head_l) - _dw(head_r)) + head_r

    legend = "   " + "   ".join(f"{_GLYPH[s]} {_ZH[s]} {counts[s]}" for s in order if counts[s])

    # Pipeline funnel — finer than the binary bar: how far the corpus got down the
    # stages (ARA sealed → report compliant), so progress is visible mid-run.
    sealed_n = sum(1 for r in recs if r.get("sealed"))
    reviewed_n = sum(1 for r in recs if r.get("final_reviewed"))
    funnel = (
        f"  进度     入库 {len(recs)} · ARA密封 {sealed_n} · "
        f"报告合规 {counts['compliant']} · 终审 {reviewed_n}"
    )

    lines = [
        "╭" + "─" * width + "╮",
        row(head),
        "├" + "─" * width + "┤",
        row("  [" + bar + "]"),
        row(legend),
        "├" + "─" * width + "┤",
        row(funnel),
        "├" + "─" * width + "┤",
    ]

    # actionable detail
    corrupt = [_short(r["key"]) for r in recs if r["state"] == "corrupt-report"]
    if corrupt:
        lines.append(row(f"  ⚠ 内容损坏 {len(corrupt)}  须重发(正文非本论文/ARA 未读入)"))
    stale = [r for r in recs if r["state"] == "done-stale"]
    if stale:
        uns = sum(1 for r in stale if r["detail"] == "unsealed-ARA")
        rep = len(stale) - uns
        bits = []
        if rep:
            bits.append(f"旧报告重发 {rep}")
        if uns:
            bits.append(f"ARA 未密封 {uns}")
        lines.append(row("  待处理   " + " · ".join(bits)))
    failed = [_short(r["key"]) for r in recs if r["state"] == "failed"]
    if failed:
        label, indent = "  失败     ", " " * _dw("  失败     ")
        cur = label
        for nm in failed:
            sep = "" if cur in (label, indent) else " · "
            if _dw(cur + sep + nm) > width - 1:
                lines.append(row(cur))
                cur = indent + nm
            else:
                cur += sep + nm
        lines.append(row(cur))
    diverged = [r for r in recs if r.get("ledger_diverged")]
    if diverged:
        lines.append(row(f"  ⚠ 账本未同步 {len(diverged)}  合规但 ledger≠done(会被重跑/清理)"))
    if not stale and not failed and not corrupt and not diverged:
        lines.append(row("  全部合规 ✓"))
    lines.append("╰" + "─" * width + "╯")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="paper-rolling corpus status (read-only)")
    ap.add_argument("--workspace", default=".")
    ap.add_argument("--json", action="store_true", help="machine-readable JSON")
    ap.add_argument("--card", action="store_true", help="ASCII status card (at-a-glance)")
    args = ap.parse_args(argv)
    recs = collect(Path(args.workspace))

    order = _ORDER
    counts = {s: sum(1 for r in recs if r["state"] == s) for s in order}
    counts = {s: n for s, n in counts.items() if n}

    if args.card:
        print(render_card(recs))
        return 0

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
            "corrupt-report": "💥",
            "done-stale": "⚠️ ",
            "failed": "❌",
            "ingested": "·",
            "orphan": "‼️ ",
        }.get(r["state"], "?")
        det = f"  ({r['detail']})" if r["detail"] else ""
        if r.get("ledger_diverged"):
            det += f"  ⚠ ledger={r['ledger']}≠done"
        print(f"  {mark} {r['state']:14} {r['idbase']:14} {r['key'][:46]}{det}")
    print("\n" + "  ".join(f"{s}={n}" for s, n in counts.items()))
    diverged = [r for r in recs if r.get("ledger_diverged")]
    if diverged:
        keys = ", ".join(r["idbase"] for r in diverged)
        print(
            f"\n⚠ {len(diverged)} compliant product(s) with ledger≠done ({keys}) — the next "
            "/loop tick will reprocess AND consistency_check will prune their vault dirs. "
            "Reconcile the ledger (append a done row) or invalidate explicitly."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
