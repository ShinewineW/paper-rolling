"""审计 §5-附1: tolerated G2 flags reflow a banner into PAPER.md, not only AUDIT_FLAGS."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from scripts.output.produce import _write_audit_flags


def _verdict(*findings):
    return SimpleNamespace(findings=list(findings))


def _flag(fid, obs):
    return SimpleNamespace(
        finding_id=fid,
        observation=obs,
        suggestion="re-extract",
        severity=SimpleNamespace(value="major"),
    )


def test_flags_reflow_into_paper_md(tmp_path: Path) -> None:
    ara = tmp_path / "ara"
    ara.mkdir()
    (ara / "PAPER.md").write_text("# Paper\n\n## Overview\nbody.\n", encoding="utf-8")
    _write_audit_flags(ara, _verdict(_flag("G2F13", "number '7' not confirmed in source MD")))

    assert (ara / "AUDIT_FLAGS.md").read_text(encoding="utf-8").count("G2F13") == 1
    paper = (ara / "PAPER.md").read_text(encoding="utf-8")
    assert "数据保真存疑" in paper  # banner present
    assert "G2F13" in paper  # the flagged id surfaced in the body
    # 审计 §5-附1 (Codex S2-R1): the actual suspect number/observation must surface
    # in PAPER.md itself, not only in AUDIT_FLAGS.md — the ID alone is not enough.
    assert "'7'" in paper  # the unconfirmed number itself
    assert "number '7' not confirmed in source MD" in paper  # the observation summary
    assert "AUDIT_FLAGS.md" in paper  # links to the detail
