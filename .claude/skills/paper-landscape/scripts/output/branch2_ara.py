"""branch2 ARA producer — runs FIRST, branch1 derives from it (双输出-D4 适配2).

Serializes the analyzer-spoke `analysis` bundle into the ara-compiler schema
tree (adopted verbatim, MIT). Invariants enforced HERE so the tree passes
Seal-1 on self-check:
  * exact numbers live ONLY in evidence/ (experiments.md is directional);
  * claim Proof references experiment IDs (E01), not paths;
  * exploration_tree carries support_level on every node (吸收-D8).

OT-4: PAPER.md frontmatter carries `schema_version` so mixed-schema vaults
stay machine-distinguishable.

Analysis-bundle headline contract (consumed by landscapes.py): the bundle
carries three flat keys the analyzer fills as the paper's leaderboard headline
for cross-paper comparison — `headline_metric: str` (e.g. "NDS"),
`headline_value: float` (the paper's headline number), and `params_million:
float` (model size in millions). _paper_md mirrors them into the PAPER.md
frontmatter (plus the logical `key`) so the corpus-batch-comparator can build
the unified metric table without re-parsing evidence tables.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

import yaml

from scripts.output.code_ref import Innovation, build_code_ref
from scripts.output.figures import extract_figures, is_architecture_caption

SCHEMA_VERSION = "1.0"
ARA_VERSION = "1.0"


def _w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")


def _paper_md(candidate: dict, analysis: dict) -> str:
    # Round 1 F7: candidate is a plain dict — dict access, never attribute access.
    fm = {
        # Logical key for the cross-paper comparator (arxiv_id, DOI fallback).
        "key": candidate.get("arxiv_id") or candidate.get("doi"),
        "title": candidate["title"],
        "authors": list(candidate.get("authors", [])),
        "year": candidate["year"],
        "venue": candidate.get("venue"),
        "doi": candidate.get("doi") or f"arXiv:{candidate['arxiv_id']}",
        "ara_version": ARA_VERSION,
        "schema_version": SCHEMA_VERSION,
        # Analyzer supplies the paper's domain; "deep learning" is a neutral
        # fallback (never a fixed AD/diffusion stamp on an off-domain paper).
        "domain": analysis.get("domain", "deep learning"),
        "keywords": [c["name"] for c in analysis["concepts"][:8]],
        "claims_summary": [c["statement"] for c in analysis["claims"][:3]],
        # Headline contract → landscapes.py cross-paper metric table.
        "headline_metric": analysis["headline_metric"],
        "headline_value": analysis["headline_value"],
        "params_million": analysis["params_million"],
    }
    front = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).strip()
    claims = analysis["claims"]
    return (
        f"---\n{front}\n---\n\n"
        f"# {candidate['title']}\n\n"
        f"## Overview\n{analysis['overview']}\n\n"
        f"## Layer Index\n\n"
        f"### Cognitive Layer (`/logic`)\n"
        f"| File | Description |\n|------|-------------|\n"
        f"| [problem.md](logic/problem.md) | Observations → gaps → insight |\n"
        f"| [claims.md](logic/claims.md) | {len(claims)} falsifiable claims |\n"
        f"| [concepts.md](logic/concepts.md) | {len(analysis['concepts'])} concepts |\n"
        f"| [experiments.md](logic/experiments.md) | {len(analysis['experiments'])} experiments |\n\n"  # noqa: E501
        f"### Physical Layer (`/src`)\n"
        f"| File | Description |\n|------|-------------|\n"
        f"| [execution/core.py](src/execution/core.py) | Novel-contribution stub |\n"
        f"| [code_ref.md](src/code_ref.md) | Repo + pinned SHA + file:line map |\n\n"
        f"### Exploration Graph (`/trace`)\n"
        f"| File | Description |\n|------|-------------|\n"
        f"| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research DAG |\n\n"
        f"### Evidence (`/evidence`)\n"
        f"| File | Description |\n|------|-------------|\n"
        f"| [README.md](evidence/README.md) | Index of tables + figures |\n"
    )


def _problem_md(p: dict) -> str:
    # Observations -> O#, Gaps -> G# (own namespaces). The analyzer sometimes reuses
    # C#/E# here, colliding with claim/experiment IDs across layers; renumber
    # deterministically so cross-layer IDs never alias. (Obs/gap IDs aren't
    # referenced outside problem.md, so renumbering is safe.)
    out = ["# Problem Specification", "", "## Observations", ""]
    for i, o in enumerate(p["observations"], 1):
        out += [
            f"### O{i}: {o['statement'][:40]}",
            f"- **Statement**: {o['statement']}",
            f"- **Evidence**: {o['evidence']}",
            f"- **Implication**: {o['implication']}",
            "",
        ]
    out += ["## Gaps", ""]
    for i, g in enumerate(p["gaps"], 1):
        out += [
            f"### G{i}: {g['statement'][:40]}",
            f"- **Statement**: {g['statement']}",
            f"- **Caused by**: {g['caused_by']}",
            f"- **Existing attempts**: {g['attempts']}",
            f"- **Why they fail**: {g['why_fail']}",
            "",
        ]
    ins = p["insight"]
    out += [
        "## Key Insight",
        f"- **Insight**: {ins['statement']}",
        f"- **Derived from**: {ins['derived_from']}",
        f"- **Enables**: {ins['enables']}",
        "",
        "## Assumptions",
    ]
    out += [f"- {a}" for a in p["assumptions"]]
    return "\n".join(out)


def _claims_md(claims: list[dict]) -> str:
    out: list[str] = ["# Claims", ""]
    for c in claims:
        out += [
            f"## {c['id']}: {c['title']}",
            f"- **Statement**: {c['statement']}",
            f"- **Status**: {c['status']}",
            f"- **Falsification criteria**: {c['falsification']}",
            f"- **Proof**: [{', '.join(c['proof'])}]",
            f"- **Evidence basis**: {c['evidence_basis']}",
            f"- **Interpretation**: {c['interpretation'] or '(none)'}",
            f"- **Tags**: {c['tags']}",
            "",
        ]
    return "\n".join(out)


def _concepts_md(concepts: list[dict]) -> str:
    out: list[str] = ["# Concepts", ""]
    for c in concepts:
        out += [
            f"## {c['name']}",
            f"- **Notation**: {c['notation']}",
            f"- **Definition**: {c['definition']}",
            f"- **Boundary conditions**: {c['boundary']}",
            f"- **Related concepts**: {c['related']}",
            "",
        ]
    return "\n".join(out)


def _experiments_md(experiments: list[dict]) -> str:
    """Directional only — NO exact numbers (load-bearing invariant)."""
    out: list[str] = ["# Experiments", ""]
    for e in experiments:
        s = e["setup"]
        out += [
            f"## {e['id']}: {e['title']}",
            f"- **Verifies**: {', '.join(e['verifies'])}",
            "- **Setup**:",
            f"  - Model: {s['model']}",
            f"  - Hardware: {s['hardware']}",
            f"  - Dataset: {s['dataset']}",
            f"  - System: {s['system']}",
            "- **Procedure**:",
        ]
        out += [f"  {i}. {step}" for i, step in enumerate(e["procedure"], 1)]
        out += [
            f"- **Metrics**: {e['metrics']}",
            f"- **Expected outcome**: {e['expected']}",
            f"- **Baselines**: {e['baselines']}",
            f"- **Dependencies**: {e['dependencies']}",
            "",
        ]
    return "\n".join(out)


def _related_md(rw: list[dict]) -> str:
    out: list[str] = ["# Related Work", ""]
    for r in rw:
        out += [
            f"## {r['id']}: {r['cite']}",
            f"- **DOI**: {r['doi']}",
            f"- **Type**: {r['type']}",
            "- **Delta**:",
            f"  - What changed: {r['what_changed']}",
            f"  - Why: {r['why']}",
            f"- **Claims affected**: {r['claims']}",
            f"- **Adopted elements**: {r['adopted']}",
            "",
        ]
    return "\n".join(out)


def _heuristics_md(hs: list[dict]) -> str:
    out: list[str] = ["# Heuristics", ""]
    for h in hs:
        out += [
            f"## {h['id']}: {h['desc']}",
            f"- **Rationale**: {h['rationale']}",
            f"- **Sensitivity**: {h['sensitivity']}",
            f"- **Bounds**: {h['bounds']}",
            f"- **Code ref**: [{h['code_ref']}]",
            f"- **Source**: {h['source']}",
            "",
        ]
    return "\n".join(out)


def _configs_md(rows: list[dict]) -> str:
    out: list[str] = []
    for r in rows:
        out += [
            f"## {r['name']}",
            f"- **Value**: {r['value']}",
            f"- **Rationale**: {r['rationale']}",
            f"- **Search range**: {r['range']}",
            f"- **Sensitivity**: {r['sensitivity']}",
            f"- **Source**: {r['source']}",
            "",
        ]
    return "\n".join(out)


def _environment_md(env: dict) -> str:
    return (
        "# Environment\n"
        f"- **Python**: {env['python']}\n"
        f"- **Framework**: {env['framework']}\n"
        f"- **Hardware**: {env['hardware']}\n"
        f"- **Key dependencies**: {', '.join(env['deps'])}\n"
        f"- **Random seeds**: {env['seeds']}\n"
    )


def _evidence_table_md(t: dict) -> str:
    header = "| " + " | ".join(t["headers"]) + " |"
    sep = "| " + " | ".join("---" for _ in t["headers"]) + " |"
    rows = ["| " + " | ".join(r) + " |" for r in t["rows"]]
    return (
        f"# {t['name']}\n"
        f"- **Source**: {t['source']}\n"
        f'- **Caption**: "{t["caption"]}"\n\n' + "\n".join([header, sep, *rows]) + "\n"
    )


def _evidence_readme(tables: list[dict], figures: Sequence[Any] = ()) -> str:
    out = [
        "# Evidence Index",
        "",
        "## Tables",
        "| File | Source | Claims | Description |",
        "|------|--------|--------|-------------|",
    ]
    for t in tables:
        out.append(
            f"| [tables/{t['name']}.md](tables/{t['name']}.md) | {t['source']} | {t['claims']} | {t['caption']} |"  # noqa: E501
        )
    # P1-a: caption-only figure index (no binaries) — an AI reader learns what each
    # figure shows without loading the image; `Role` flags the core method diagram.
    if figures:
        out += [
            "",
            "## Figures",
            "| Source ref | Role | Caption |",
            "|------------|------|---------|",
        ]
        for f in figures:
            role = "architecture" if is_architecture_caption(f.caption) else "result"
            out.append(f"| `{f.ref}` | {role} | {f.caption} |")
    return "\n".join(out)


def write_branch2(
    ara_dir: Path, candidate: Any, analysis: dict, md_path: Path | None = None
) -> None:
    """Write the full branch2 ARA tree under `ara_dir`.

    `md_path` (optional): the frozen {ID}.md — when given, its original figures are
    indexed (caption + source ref, no binary) into evidence/README.md (P1-a).
    """
    _w(ara_dir / "PAPER.md", _paper_md(candidate, analysis))
    _w(ara_dir / "logic/problem.md", _problem_md(analysis["problem"]))
    _w(ara_dir / "logic/claims.md", _claims_md(analysis["claims"]))
    _w(ara_dir / "logic/concepts.md", _concepts_md(analysis["concepts"]))
    _w(ara_dir / "logic/experiments.md", _experiments_md(analysis["experiments"]))
    _w(ara_dir / "logic/related_work.md", _related_md(analysis["related_work"]))
    _w(ara_dir / "logic/solution/architecture.md", analysis["architecture"])
    _w(ara_dir / "logic/solution/algorithm.md", analysis["algorithm"])
    _w(ara_dir / "logic/solution/constraints.md", analysis["constraints"])
    _w(ara_dir / "logic/solution/heuristics.md", _heuristics_md(analysis["heuristics"]))
    _w(ara_dir / "src/configs/training.md", _configs_md(analysis["configs_training"]))
    _w(ara_dir / "src/configs/model.md", _configs_md(analysis["configs_model"]))
    _w(ara_dir / "src/environment.md", _environment_md(analysis["environment"]))
    _w(ara_dir / "src/execution/core.py", analysis["execution_stub"])

    tree_yaml = "# Exploration Tree\n" + yaml.safe_dump(
        {"tree": analysis["exploration_tree"]}, allow_unicode=True, sort_keys=False
    )
    _w(ara_dir / "trace/exploration_tree.yaml", tree_yaml)

    for t in analysis["evidence_tables"]:
        _w(ara_dir / f"evidence/tables/{t['name']}.md", _evidence_table_md(t))
    figures = extract_figures(md_path) if md_path is not None else []
    _w(ara_dir / "evidence/README.md", _evidence_readme(analysis["evidence_tables"], figures))

    # Shallow code analysis → pointer (clone deleted inside, 分析-D2). Use .get():
    # discovered papers may carry no github_repo / arxiv_id key (closed-source or
    # DOI-only) — None -> a "_not found_" code_ref, never a KeyError crash.
    build_code_ref(
        github_repo=candidate.get("github_repo"),
        innovations=[Innovation(name=i["name"], grep=i["grep"]) for i in analysis["innovations"]],
        out_path=ara_dir / "src/code_ref.md",
        clone_root=Path("/tmp/paper-repos"),
        idbase=candidate.get("arxiv_id") or candidate.get("doi") or "repo",
    )
