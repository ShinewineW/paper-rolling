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


def test_evidence_readme_indexes_figure_captions_when_md_given(tmp_path, candidate, analysis):
    # P1-a: the ARA evidence layer must carry a figures INDEX (caption + source
    # ref, NO binary), so an AI reader knows what each figure shows. branch2
    # reuses the deterministic extract_figures() over the frozen MD.
    md = tmp_path / "src.md"
    md.write_text(
        "![](images/aaa.jpg)\n\nFigure 2: overall architecture of our model.\n\n"
        "![](images/bbb.jpg)\n\nFigure 5: qualitative results on the test set.\n",
        encoding="utf-8",
    )
    ara = tmp_path / "ara"
    write_branch2(ara, candidate, analysis, md_path=md)
    readme = (ara / "evidence/README.md").read_text(encoding="utf-8")
    assert "## Figures" in readme
    assert "overall architecture of our model" in readme  # caption surfaced
    assert "qualitative results on the test set" in readme
    assert "images/aaa.jpg" in readme  # source ref for provenance (no binary copied)
    assert not (ara / "evidence/figures").exists()  # caption-only: no binary dir


def test_write_branch2_uses_injected_repo_resolver(tmp_path, candidate, analysis):
    # Phase 2: the driver injects a repo_resolver (T2b/T4-wired). write_branch2 must
    # call it instead of the default — proven by a recording fake that returns [].
    seen = {}

    def fake_resolver(*, arxiv_id, md_path, candidate):  # noqa: ARG001
        seen["arxiv_id"] = arxiv_id
        return []

    ara = tmp_path / "ara"
    write_branch2(ara, candidate, analysis, repo_resolver=fake_resolver)
    assert seen["arxiv_id"] == candidate["arxiv_id"]  # injected resolver was called
    body = (ara / "src/code_ref.md").read_text(encoding="utf-8")
    assert "No public repository found" in body  # its [] result drove a not-found state
