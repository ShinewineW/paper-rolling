# tests/test_landscapes.py
from pathlib import Path

from scripts.landscapes import PaperSummary, generate_landscapes, load_paper_summary


def _write_paper(
    workspace: Path, key: str, *, title: str, year: int, metric: str, value: float, params_m: float
) -> None:
    # Minimal ai_package fixture the comparator reads (基调-D2 layout).
    ara = workspace / "ai_package" / f"2026-06-05_{key}" / "ara"
    ara.mkdir(parents=True, exist_ok=True)
    (ara / "PAPER.md").write_text(
        "---\n"
        f"title: {title}\n"
        f"year: {year}\n"
        f"key: {key}\n"
        "schema_version: 1\n"
        f"headline_metric: {metric}\n"
        f"headline_value: {value}\n"
        f"params_million: {params_m}\n"
        "---\n",
        encoding="utf-8",
    )


def test_load_paper_summary(tmp_path: Path):
    _write_paper(
        tmp_path, "p0", title="MethodA", year=2024, metric="mAP", value=51.2, params_m=120.0
    )
    s = load_paper_summary(tmp_path, "2026-06-05_p0")
    assert s == PaperSummary(
        key="p0",
        title="MethodA",
        year=2024,
        headline_metric="mAP",
        headline_value=51.2,
        params_million=120.0,
    )


def test_generate_landscapes_writes_index_and_report(tmp_path: Path):
    _write_paper(
        tmp_path, "p0", title="MethodA", year=2023, metric="mAP", value=48.0, params_m=200.0
    )
    _write_paper(
        tmp_path, "p1", title="MethodB", year=2025, metric="mAP", value=55.0, params_m=90.0
    )

    out = generate_landscapes(tmp_path, topic="3d detection")

    index = (tmp_path / "landscapes" / "3d-detection" / "INDEX.md").read_text(encoding="utf-8")
    report = (tmp_path / "landscapes" / "3d-detection" / "report.md").read_text(encoding="utf-8")

    # INDEX lists both papers, newest first (trend ordering).
    assert "MethodB" in index and "MethodA" in index
    assert index.index("MethodB") < index.index("MethodA")
    # Unified metric table with both values.
    assert "55.0" in report and "48.0" in report
    # Efficiency column = metric per param (MethodB 55/90 is more efficient).
    assert "效率" in report or "efficiency" in report.lower()
    # Trend section present.
    assert "趋势" in report or "trend" in report.lower()
    assert out.paper_count == 2


def test_generate_landscapes_empty_corpus_is_safe(tmp_path: Path):
    out = generate_landscapes(tmp_path, topic="empty topic")
    assert out.paper_count == 0
    index = (tmp_path / "landscapes" / "empty-topic" / "INDEX.md").read_text(encoding="utf-8")
    assert "0" in index
