"""The shipped examples/sample-ara-bundle.json is advertised (SKILL.md,
worked-example.md, analyze-paper sub-skill, ara-paper template) as THE literal
`resolve_analysis` output target. So it must survive the project's own gates —
otherwise an analyzer copying it would emit a bundle that hard-blocks at produce
time. This pins it: round-trip the real shipped bundle through write_branch2 +
the Seal-1 validator + write_branch1 + the anchor lint + the landscapes reader.
"""

from __future__ import annotations

import json
import pathlib

from scripts.landscapes import load_paper_summary
from scripts.output.anchor_lint import lint_text
from scripts.output.ara_schema import validate_ara_tree
from scripts.output.branch1_report import write_branch1
from scripts.output.branch2_ara import write_branch2

_REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
_BUNDLE = _REPO_ROOT / ".claude/skills/paper-landscape/examples/sample-ara-bundle.json"

_CANDIDATE = {
    "arxiv_id": "2301.04104",
    "doi": None,
    "github_repo": None,
    "title": "Mastering Diverse Domains through World Models",
    "year": 2023,
    "venue": None,
    "authors": ["Hafner, D."],
}
_KEY = "2026-06-08_Dreamer_2301.04104"


def _load_bundle() -> dict:
    bundle = json.loads(_BUNDLE.read_text(encoding="utf-8"))
    bundle.pop("_comment", None)  # the example label; real resolve_analysis output omits it
    return bundle


def test_sample_bundle_is_valid_json_with_headline_contract():
    bundle = _load_bundle()
    assert isinstance(bundle["headline_metric"], str)
    assert isinstance(bundle["headline_value"], float)
    assert isinstance(bundle["params_million"], float)


def test_shipped_sample_passes_seal1_and_full_round_trip(tmp_path):
    bundle = _load_bundle()
    ara = tmp_path / "ai_package" / _KEY / "ara"
    ara.mkdir(parents=True)
    person = tmp_path / "person_vault" / _KEY
    md = tmp_path / "corpus" / "2301.04104" / "2301.04104.md"
    md.parent.mkdir(parents=True)
    md.write_text(
        "# Mastering Diverse Domains through World Models\n"
        "One fixed configuration spans more than 150 tasks in 8 domains. "
        "On Minecraft Diamond it reaches a 9.1 episode return at 100M environment "
        "steps, versus 7.1 for the strongest baseline.\n",
        encoding="utf-8",
    )

    write_branch2(ara, _CANDIDATE, bundle)
    # The gate Codex + the manual proof both missed: Seal-1 runs at produce time
    # BEFORE G2, so the advertised example MUST pass it cleanly.
    assert validate_ara_tree(ara) == []

    write_branch1(person, _CANDIDATE, ara, md, bundle, key=_KEY)
    assert lint_text((person / "report.md").read_text(encoding="utf-8")) == []

    summary = load_paper_summary(tmp_path, _KEY)
    assert summary.headline_metric == "Minecraft Diamond Return"
    assert summary.headline_value == 9.1
    assert summary.params_million == 200.0
