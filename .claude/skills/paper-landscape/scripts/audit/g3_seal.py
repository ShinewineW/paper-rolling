"""G3 — branch1<->MD + type-aware entailment + 6-dim rigor seal (audit-D1, single pass).

Runs AFTER the dual-output branches. Three parts, all run; the verdict is the
union of their findings (which blocks iff any hard finding fires):
  (a) anchor resolution  — every empirical sentence in person_vault/report.md
      resolves to a real MD span (吸收-D1 K4 fix);
  (b) type-aware entailment — every claim's experiment design matches its claim
      type (吸收-D8);
  (c) 6-dim rigor seal — Seal Level 2; level2_report.json is written into the
      ai_package; grade < Weak Accept is a hard block (吸收-D7).

On a hard verdict the HUB re-emits the offending branch (gate_runner owns the
bounded retry). The level2_report.json is always written — even on a low-grade
block — because the grade IS the evidence for the block.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from pathlib import Path

from scripts.audit.anchor_resolution import check_branch1_md_anchors
from scripts.audit.ara_tree import extract_claim_registry, find_ara_dir
from scripts.audit.entailment import check_entailment
from scripts.audit.equation_fidelity import check_equation_fidelity
from scripts.audit.rigor_rubric import score_rigor
from scripts.audit.types import (
    EntailmentJudgeFn,
    Finding,
    GateVerdict,
    RigorScoreFn,
    Severity,
)

_EXP_HEADER = re.compile(r"^##\s+(E\d{2,}):", re.MULTILINE)


def _parse_experiments(ara_dir: Path) -> dict[str, str]:
    """Map experiment ID -> its section text from logic/experiments.md."""
    exp_md = ara_dir / "logic" / "experiments.md"
    if not exp_md.exists():
        return {}
    text = exp_md.read_text(encoding="utf-8")
    headers = list(_EXP_HEADER.finditer(text))
    out: dict[str, str] = {}
    for i, m in enumerate(headers):
        start = m.start()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        out[m.group(1)] = text[start:end]
    return out


def _load_ara_bundle(ara_dir: Path) -> dict[str, str]:
    """Read the ARA text files the rigor reviewer reads, in fixed order."""
    bundle: dict[str, str] = {}
    for rel in (
        "PAPER.md",
        "logic/claims.md",
        "logic/experiments.md",
        "logic/problem.md",
        "logic/concepts.md",
        "logic/solution/architecture.md",
        "trace/exploration_tree.yaml",
        "evidence/README.md",
    ):
        path = ara_dir / rel
        if path.exists():
            bundle[rel] = path.read_text(encoding="utf-8")
    return bundle


def _artifact_name(ai_package_entry: Path) -> str:
    return ai_package_entry.name


def run_g3(
    person_vault_entry: Path,
    ai_package_entry: Path,
    md_path: Path,
    content_list_path: Path,
    *,
    rigor_scores: RigorScoreFn,
    entailment_judge: EntailmentJudgeFn,
    empirical_classifier: Callable[[str], bool] | None = None,
) -> GateVerdict:
    """Run the four-part G3 seal for one paper; write level2_report.json.

    `empirical_classifier` (ROADMAP C4): optional injected classifier for the
    branch1 anchor check's empirical-sentence detection; defaults to the metric-
    cue heuristic. Production may plug a trained NLI / factual-consistency model.
    """
    ara_dir = find_ara_dir(ai_package_entry)
    findings: list[Finding] = []

    # (d) MECHANICAL equation fidelity (Round 15 #3 — wire the built gate):
    # content_list.json typed formula blocks vs `$$` blocks in the MD. No LLM.
    # Hard-blocks a count mismatch (garbled-equation ingest).
    findings.extend(check_equation_fidelity(md_path, content_list_path).findings)

    # (a) branch1 <-> MD anchor resolution. A MISSING branch1 report.md is a HARD
    # block: with no report there is nothing to seal, so passing it would let the
    # paper seal on an empty human branch (the audit found this silent pass).
    report_md = person_vault_entry / "report.md"
    if report_md.exists():
        findings.extend(
            check_branch1_md_anchors(report_md, md_path, is_empirical=empirical_classifier).findings
        )
    else:
        findings.append(
            Finding(
                finding_id="G3R0",
                severity=Severity.CRITICAL,
                target=str(report_md),
                observation="missing branch1 report.md — cannot seal",
                is_hard_block=True,
                reasoning="G3 seals the branch1 human report against the MD; with no "
                "report.md there is no branch1 to anchor-check, so the paper must NOT seal.",
                suggestion="Re-emit branch1 so person_vault/{key}/report.md exists, then re-run.",
            )
        )

    # (b) type-aware entailment.
    claims = extract_claim_registry(ara_dir)
    experiments = _parse_experiments(ara_dir)
    findings.extend(check_entailment(claims, experiments, judge=entailment_judge).findings)

    # (c) 6-dim rigor seal — always write the report.
    report = score_rigor(
        _load_ara_bundle(ara_dir),
        artifact_name=_artifact_name(ai_package_entry),
        rigor_scores=rigor_scores,
    )
    (ara_dir / "level2_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if not report["overall"]["passes_seal2"]:
        findings.append(
            Finding(
                finding_id="SEAL2",
                severity=Severity.CRITICAL,
                target=str((ara_dir / "level2_report.json").name),
                observation=(
                    f"ARA Seal Level 2 grade {report['overall']['grade']!r} is "
                    f"below Weak Accept (mean {report['overall']['mean_score']})"
                ),
                is_hard_block=True,
                reasoning="The cognitive terminal seal failed; the AI package is not trustworthy.",
                suggestion="Address the level2_report.json findings and re-emit branch2.",
            )
        )

    return GateVerdict(gate="G3", findings=tuple(findings))
