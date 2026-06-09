"""ARA Seal Level 1 structural validator (双输出-D4) + exploration-tree
support_level enforcement (吸收-D8).

Adopts the ara-compiler validation-checklist.md as a blueprint (MIT). The
exploration-tree `support_level: explicit|inferred` field is promoted from
advisory to a Seal-1 MUST per 吸收-D8: reconstructed (inferred) nodes must not
masquerade as paper-explicit history, and every explicit node must cite
`source_refs`.

Reused by the branch2 producer (self-check before atomic landing) and by G3
(Chunk 5).
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

_NODE_TYPES = {"question", "decision", "experiment", "dead_end", "pivot"}
_TYPE_REQUIRED = {
    "question": ["description"],
    "experiment": ["result"],
    "dead_end": ["hypothesis", "failure_mode", "lesson"],
    "decision": ["choice", "alternatives"],
    "pivot": ["from", "to", "trigger"],
}

_MANDATORY_DIRS = ["logic", "logic/solution", "src", "src/configs", "trace", "evidence"]
_MANDATORY_FILES = [
    "PAPER.md",
    "logic/problem.md",
    "logic/claims.md",
    "logic/concepts.md",
    "logic/experiments.md",
    "logic/solution/architecture.md",
    "logic/solution/algorithm.md",
    "logic/solution/constraints.md",
    "logic/solution/heuristics.md",
    "logic/related_work.md",
    "src/configs/training.md",
    "src/configs/model.md",
    "src/environment.md",
    "trace/exploration_tree.yaml",
    "evidence/README.md",
]


def _walk(nodes: list, out: list[dict]) -> None:
    for node in nodes:
        if isinstance(node, dict):
            out.append(node)
            children = node.get("children")
            if isinstance(children, list):
                _walk(children, out)


def validate_exploration_tree(yaml_text: str) -> list[str]:
    """Validate trace/exploration_tree.yaml against Seal-1 + 吸收-D8.

    Returns a list of error strings; empty = PASS.
    """
    errors: list[str] = []
    try:
        data = yaml.safe_load(yaml_text)
    except yaml.YAMLError as exc:
        return [f"exploration_tree: invalid YAML: {exc}"]
    if not isinstance(data, dict) or "tree" not in data:
        return ["exploration_tree: missing top-level 'tree' key"]

    flat: list[dict] = []
    _walk(data["tree"], flat)

    if len(flat) < 8:
        errors.append(f"exploration_tree: needs at least 8 nodes, got {len(flat)}")
    types = [n.get("type") for n in flat]
    if "dead_end" not in types:
        errors.append("exploration_tree: at least 1 dead_end node required")
    if "decision" not in types:
        errors.append("exploration_tree: at least 1 decision node required")

    ids = {n.get("id") for n in flat}
    for node in flat:
        nid = node.get("id", "<no-id>")
        ntype = node.get("type")
        if ntype not in _NODE_TYPES:
            errors.append(f"{nid}: invalid type {ntype!r}")
            continue
        for field in ("id", "type", "title"):
            if not node.get(field):
                errors.append(f"{nid}: missing required field {field!r}")
        for field in _TYPE_REQUIRED.get(ntype, []):
            if field not in node:
                errors.append(f"{nid}: {ntype} node missing required field {field!r}")
        # 吸收-D8 — support_level is MUST.
        sl = node.get("support_level")
        if sl not in {"explicit", "inferred"}:
            errors.append(f"{nid}: support_level must be 'explicit' or 'inferred', got {sl!r}")
        elif sl == "explicit" and not node.get("source_refs"):
            errors.append(f"{nid}: explicit node must include source_refs")
        deps = node.get("also_depends_on", []) or []
        if isinstance(deps, str):
            errors.append(
                f"{nid}: also_depends_on must be a list of node ids, got string {deps!r} "
                f"(wrap a single id in a list, e.g. [{deps!r}])"
            )
            deps = []
        for dep in deps:
            if dep not in ids:
                errors.append(f"{nid}: also_depends_on references unknown node {dep!r}")
    return errors


def _field_check(path: Path, header_re: str, fields: list[str], label: str) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if not re.search(header_re, text, re.MULTILINE):
        errors.append(f"{label}: missing header pattern {header_re!r}")
    for f in fields:
        if f not in text:
            errors.append(f"{label}: missing field {f!r}")
    return errors


def validate_ara_tree(ara_dir: Path) -> list[str]:
    """Full ARA Seal-1 structural validation of a branch2 `ara/` directory."""
    errors: list[str] = []
    for d in _MANDATORY_DIRS:
        if not (ara_dir / d).is_dir():
            errors.append(f"missing directory {d}/")
    for f in _MANDATORY_FILES:
        p = ara_dir / f
        if not p.exists() or p.stat().st_size <= 10:
            errors.append(f"missing or empty file {f}")

    if (ara_dir / "logic/claims.md").exists():
        errors += _field_check(
            ara_dir / "logic/claims.md",
            r"^## C\d+",
            [
                "**Statement**",
                "**Status**",
                "**Falsification criteria**",
                "**Proof**",
                "**Evidence basis**",
            ],
            "claims.md",
        )
    if (ara_dir / "logic/experiments.md").exists():
        text = (ara_dir / "logic/experiments.md").read_text(encoding="utf-8")
        if len(re.findall(r"^## E\d+", text, re.MULTILINE)) < 3:
            errors.append("experiments.md: needs at least 3 E## blocks")
    if (ara_dir / "logic/concepts.md").exists():
        text = (ara_dir / "logic/concepts.md").read_text(encoding="utf-8")
        if len(re.findall(r"^## ", text, re.MULTILINE)) < 5:
            errors.append("concepts.md: needs at least 5 concept sections")

    tree_path = ara_dir / "trace/exploration_tree.yaml"
    if tree_path.exists():
        errors += [
            f"trace: {e}" for e in validate_exploration_tree(tree_path.read_text(encoding="utf-8"))
        ]

    tables = (
        list((ara_dir / "evidence/tables").glob("*.md"))
        if (ara_dir / "evidence/tables").is_dir()
        else []
    )
    figures = (
        list((ara_dir / "evidence/figures").glob("*.md"))
        if (ara_dir / "evidence/figures").is_dir()
        else []
    )
    if not tables and not figures:
        errors.append("evidence: needs at least 1 table or figure file")
    for ev in tables + figures:
        ev_text = ev.read_text(encoding="utf-8")
        if "|" not in ev_text:
            errors.append(f"evidence/{ev.name}: missing markdown table")
        if "**Source**" not in ev_text:
            errors.append(f"evidence/{ev.name}: missing **Source** field")
    return errors
