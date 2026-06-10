"""ARA Seal-1 structural validity + exploration-tree support_level (吸收-D8)."""

from __future__ import annotations

import textwrap

from scripts.output.ara_schema import validate_ara_tree, validate_exploration_tree


def _good_tree() -> str:
    return textwrap.dedent(
        """\
        tree:
          - id: N01
            type: question
            support_level: explicit
            source_refs: ["§1"]
            title: root
            description: central question
            children:
              - id: N02
                type: experiment
                support_level: explicit
                source_refs: ["Table 2"]
                title: e1
                result: observed gain
              - id: N03
                type: dead_end
                support_level: inferred
                title: failed
                hypothesis: h
                failure_mode: f
                lesson: l
              - id: N04
                type: decision
                support_level: inferred
                title: d
                choice: A
                alternatives: ["B", "C"]
              - id: N05
                type: experiment
                support_level: explicit
                source_refs: ["§3"]
                title: e2
                result: r
              - id: N06
                type: experiment
                support_level: explicit
                source_refs: ["§4"]
                title: e3
                result: r
              - id: N07
                type: experiment
                support_level: explicit
                source_refs: ["§5"]
                title: e4
                result: r
              - id: N08
                type: question
                support_level: inferred
                title: q2
                description: follow-up
        """
    )


def test_valid_tree_passes() -> None:
    assert validate_exploration_tree(_good_tree()) == []


def test_missing_support_level_is_error() -> None:
    # Remove N02's support_level+source_refs lines WITH their exact indentation.
    bad = _good_tree().replace(
        '        support_level: explicit\n        source_refs: ["Table 2"]\n',
        "",
    )
    errors = validate_exploration_tree(bad)
    assert any("support_level" in e and "N02" in e for e in errors)


def test_explicit_node_without_source_refs_is_error() -> None:
    # Remove ONLY N02's source_refs line (keep support_level: explicit), with
    # exact indentation so the YAML stays well-formed.
    bad = _good_tree().replace('        source_refs: ["Table 2"]\n', "")
    errors = validate_exploration_tree(bad)
    assert any("source_refs" in e and "N02" in e for e in errors)


def test_fewer_than_8_nodes_is_error() -> None:
    small = textwrap.dedent(
        """\
        tree:
          - id: N01
            type: question
            support_level: inferred
            title: q
            description: d
        """
    )
    errors = validate_exploration_tree(small)
    assert any("at least 8" in e for e in errors)


def test_missing_dead_end_is_error() -> None:
    bad = (
        _good_tree()
        .replace("type: dead_end", "type: experiment")
        .replace("                hypothesis: h\n", "                result: r\n")
    )
    errors = validate_exploration_tree(bad)
    assert any("dead_end" in e for e in errors)


def test_validate_ara_tree_detects_missing_paper_md(tmp_path) -> None:
    errors = validate_ara_tree(tmp_path)
    assert any("PAPER.md" in e for e in errors)


def test_also_depends_on_string_reports_truthful_error() -> None:
    yaml_text = """
tree:
  - id: N1
    type: decision
    title: root
    support_level: inferred
    also_depends_on: "D1"
"""
    errors = validate_exploration_tree(yaml_text)
    joined = " ".join(errors)
    assert "also_depends_on must be a list" in joined
    assert '"D1"' in joined or "'D1'" in joined
    assert "unknown node 'D'" not in joined
    assert "unknown node '1'" not in joined
