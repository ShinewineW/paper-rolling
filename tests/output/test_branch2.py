"""branch2 ARA producer emits a Seal-1-valid tree (双输出-D4)."""

from __future__ import annotations

from scripts.output.ara_schema import validate_ara_tree
from scripts.output.branch2_ara import write_branch2


def test_write_branch2_passes_seal1(tmp_path, candidate, analysis):
    ara = tmp_path / "ara"
    write_branch2(ara, candidate, analysis)
    errors = validate_ara_tree(ara)
    assert errors == [], f"Seal-1 errors: {errors}"


def test_paper_md_has_schema_version(tmp_path, candidate, analysis):
    ara = tmp_path / "ara"
    write_branch2(ara, candidate, analysis)
    body = (ara / "PAPER.md").read_text(encoding="utf-8")
    assert "schema_version" in body
    assert "Layer Index" in body


def test_paper_md_carries_headline_frontmatter_for_landscapes(tmp_path, candidate, analysis):
    # The producer→consumer contract: branch2 frontmatter feeds landscapes.py.
    import yaml

    ara = tmp_path / "ara"
    write_branch2(ara, candidate, analysis)
    body = (ara / "PAPER.md").read_text(encoding="utf-8")
    fm = yaml.safe_load(body.split("---", 2)[1])
    assert fm["key"] == candidate["arxiv_id"]
    assert fm["headline_metric"] == analysis["headline_metric"]
    assert fm["headline_value"] == analysis["headline_value"]
    assert fm["params_million"] == analysis["params_million"]


def test_experiments_carry_no_exact_numbers(tmp_path, candidate, analysis):
    ara = tmp_path / "ara"
    write_branch2(ara, candidate, analysis)
    exp = (ara / "logic/experiments.md").read_text(encoding="utf-8")
    # Exact numbers live only in evidence/, never in experiments.md.
    assert "0.61" not in exp
    assert "0.52" not in exp


def test_evidence_table_holds_exact_numbers(tmp_path, candidate, analysis):
    ara = tmp_path / "ara"
    write_branch2(ara, candidate, analysis)
    ev = (ara / "evidence/tables/table1_nuscenes.md").read_text(encoding="utf-8")
    assert "0.61" in ev and "0.52" in ev
    assert "**Source**" in ev
