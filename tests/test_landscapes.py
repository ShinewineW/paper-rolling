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


def _write_paper_raw(workspace: Path, entry: str, body: str) -> None:
    ara = workspace / "ai_package" / entry / "ara"
    ara.mkdir(parents=True, exist_ok=True)
    (ara / "PAPER.md").write_text(body, encoding="utf-8")


def test_load_paper_summary_derives_year_from_arxiv_key_when_null(tmp_path: Path):
    # Paper-list (force_include) papers carry no year → frontmatter year: null. The
    # aggregator must NOT crash; it derives the year from the arXiv key's YYMM prefix.
    _write_paper_raw(
        tmp_path,
        "2026-06-13_p_2606.12987",
        "---\nkey: '2606.12987'\ntitle: T\nyear: null\n"
        "headline_metric: mAP\nheadline_value: 1.0\nparams_million: 2.0\n---\n",
    )
    s = load_paper_summary(tmp_path, "2026-06-13_p_2606.12987")
    assert s.year == 2026  # 2606.* -> 2026, no crash


def test_generate_landscapes_tolerates_null_year(tmp_path: Path):
    # End-to-end: a corpus whose papers all have year: null must still produce a
    # landscape (regression for the 2026-06-14 int(None) crash in the WAM test run).
    _write_paper_raw(
        tmp_path,
        "2026-06-13_a_2606.12987",
        "---\nkey: '2606.12987'\ntitle: A\nyear: null\n"
        "headline_metric: L2\nheadline_value: 0.5\nparams_million: 3.0\n---\n",
    )
    _write_paper_raw(
        tmp_path,
        "2026-06-13_b_2604.04198",
        "---\nkey: '2604.04198'\ntitle: B\nyear: null\n"
        "headline_metric: L2\nheadline_value: 0.6\nparams_million: 4.0\n---\n",
    )
    res = generate_landscapes(tmp_path, topic="t", generated_on="2026-06-14")
    assert res.paper_count == 2 and res.report_path.exists()


def test_has_headline_skips_paper_with_null_metric(tmp_path: Path):
    # A null headline_value must SKIP the paper (no float(None) crash), not abort the tick.
    _write_paper_raw(
        tmp_path,
        "2026-06-13_x_2606.00001",
        "---\nkey: '2606.00001'\ntitle: X\nyear: 2026\n"
        "headline_metric: mAP\nheadline_value: null\nparams_million: 1.0\n---\n",
    )
    res = generate_landscapes(tmp_path, topic="t", generated_on="2026-06-14")
    assert res.paper_count == 0  # skipped, did not crash


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


def test_generate_landscapes_stamps_injected_date_not_hardcoded(tmp_path: Path):
    # Codex R17: the report date must be injectable, not a fixed 2026-06-05 that
    # every daily-regenerated report would carry.
    _write_paper(
        tmp_path, "p0", title="MethodA", year=2025, metric="mAP", value=48.0, params_m=90.0
    )
    generate_landscapes(tmp_path, topic="3d detection", generated_on="2099-12-31")
    index = (tmp_path / "landscapes" / "3d-detection" / "INDEX.md").read_text(encoding="utf-8")
    report = (tmp_path / "landscapes" / "3d-detection" / "report.md").read_text(encoding="utf-8")
    assert "2099-12-31" in index and "2099-12-31" in report
    assert "2026-06-05" not in index and "2026-06-05" not in report


def test_generate_landscapes_empty_corpus_is_safe(tmp_path: Path):
    out = generate_landscapes(tmp_path, topic="empty topic")
    assert out.paper_count == 0
    index = (tmp_path / "landscapes" / "empty-topic" / "INDEX.md").read_text(encoding="utf-8")
    assert "0" in index
