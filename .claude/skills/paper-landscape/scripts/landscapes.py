# .claude/skills/paper-landscape/scripts/landscapes.py
"""Cross-paper synthesis — corpus-batch-comparator (§4 STEP4/5, kept from v1).

Reads each paper's ai_package ARA PAPER.md frontmatter (title/year/headline
metric/params) and emits a topic landscape:
  landscapes/{topic-slug}/INDEX.md  — per-paper navigation, newest-first
  landscapes/{topic-slug}/report.md — unified metric table + efficiency + trends

This is a pure read-side aggregator: it never writes the ledger or vaults.
"""

from __future__ import annotations

import datetime
import re
from dataclasses import dataclass
from pathlib import Path

import yaml


def slugify(topic: str) -> str:
    """Deterministic topic -> directory slug (kebab-case, ascii-safe)."""
    s = topic.strip().lower()
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", s)
    return s.strip("-") or "topic"


@dataclass(frozen=True)
class PaperSummary:
    key: str
    title: str
    year: int
    headline_metric: str
    headline_value: float
    params_million: float


@dataclass(frozen=True)
class LandscapeResult:
    paper_count: int
    index_path: Path
    report_path: Path


def _read_frontmatter(paper_md: Path) -> dict:
    text = paper_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def load_paper_summary(workspace: Path, entry_name: str) -> PaperSummary:
    """Load one ai_package entry (e.g. '2026-06-05_p0') into a PaperSummary."""
    paper_md = Path(workspace) / "ai_package" / entry_name / "ara" / "PAPER.md"
    fm = _read_frontmatter(paper_md)
    return PaperSummary(
        key=str(fm["key"]),
        title=str(fm["title"]),
        year=int(fm["year"]),
        headline_metric=str(fm["headline_metric"]),
        headline_value=float(fm["headline_value"]),
        params_million=float(fm["params_million"]),
    )


_HEADLINE_KEYS = ("key", "headline_metric", "headline_value", "params_million")


def _has_headline_frontmatter(paper_md: Path) -> bool:
    """True iff PAPER.md carries the headline-metric keys the comparator needs.

    A branch2 PAPER.md without headline metrics (no leaderboard number to
    aggregate) is skipped from the cross-paper table rather than crashing the
    read-side aggregator (the entry still lives in the vault; it just has no
    metric row in the landscape).
    """
    fm = _read_frontmatter(paper_md)
    return all(k in fm for k in _HEADLINE_KEYS)


def _collect(workspace: Path) -> list[PaperSummary]:
    ai_root = Path(workspace) / "ai_package"
    if not ai_root.exists():
        return []
    summaries: list[PaperSummary] = []
    for entry in sorted(ai_root.iterdir()):
        paper_md = entry / "ara" / "PAPER.md"
        if not paper_md.exists() or not _has_headline_frontmatter(paper_md):
            continue
        summaries.append(load_paper_summary(workspace, entry.name))
    return summaries


def _efficiency(s: PaperSummary) -> float:
    if s.params_million <= 0:
        return 0.0
    return round(s.headline_value / s.params_million, 4)


def _render_index(topic: str, papers: list[PaperSummary], generated_on: str) -> str:
    lines = [
        f"# {topic} — 论文索引",
        "",
        f"> 生成日期: {generated_on} | 共 {len(papers)} 篇论文",
        ">",
        "> [完整全景报告](report.md)",
        "",
        "---",
        "",
        "## 快速导航（按年份倒序）",
        "",
        "| # | 论文 | 年份 | 主指标 |",
        "|---|------|------|--------|",
    ]
    for i, s in enumerate(sorted(papers, key=lambda p: (-p.year, p.title)), 1):
        lines.append(f"| {i} | {s.title} | {s.year} | {s.headline_metric}={s.headline_value} |")
    lines.append("")
    return "\n".join(lines)


def _render_report(topic: str, papers: list[PaperSummary], generated_on: str) -> str:
    ordered = sorted(papers, key=lambda p: (-p.year, p.title))
    lines = [
        f"# {topic} — 全景对比报告",
        "",
        f"> 共 {len(papers)} 篇论文 | 生成日期 {generated_on}",
        "",
        "## 一、统一指标对比表",
        "",
        "| 论文 | 年份 | 主指标 | 数值 | 参数量(M) | 效率(指标/M) |",
        "|------|------|--------|------|-----------|--------------|",
    ]
    for s in ordered:
        lines.append(
            f"| {s.title} | {s.year} | {s.headline_metric} | {s.headline_value} "
            f"| {s.params_million} | {_efficiency(s)} |"
        )
    lines += ["", "## 二、效率分析（efficiency）", ""]
    if ordered:
        best = max(ordered, key=_efficiency)
        lines.append(
            f"最高效率: **{best.title}** （{best.headline_metric}/M = {_efficiency(best)}）。"
        )
    else:
        lines.append("（无论文）")
    lines += ["", "## 三、趋势（trend，按年份）", ""]
    if ordered:
        chron = sorted(papers, key=lambda p: p.year)
        first, last = chron[0], chron[-1]
        delta = round(last.headline_value - first.headline_value, 4)
        lines.append(
            f"{first.year}（{first.headline_value}）→ {last.year}（{last.headline_value}），"
            f"{first.headline_metric} 变化 {delta:+}。"
        )
    else:
        lines.append("（无论文）")
    lines.append("")
    return "\n".join(lines)


def generate_landscapes(
    workspace: Path, *, topic: str, generated_on: str | None = None
) -> LandscapeResult:
    """Generate landscapes/{slug}/INDEX.md + report.md for the corpus.

    `generated_on` stamps the report (ISO date); it defaults to today's date so a
    daily /loop tick writes the current date instead of a fixed one (Codex R17).
    Callers may inject a fixed value for deterministic output.
    """
    generated_on = generated_on or datetime.date.today().isoformat()
    papers = _collect(workspace)
    slug = slugify(topic)
    out_dir = Path(workspace) / "landscapes" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    index_path = out_dir / "INDEX.md"
    report_path = out_dir / "report.md"
    index_path.write_text(_render_index(topic, papers, generated_on), encoding="utf-8")
    report_path.write_text(_render_report(topic, papers, generated_on), encoding="utf-8")
    return LandscapeResult(paper_count=len(papers), index_path=index_path, report_path=report_path)
