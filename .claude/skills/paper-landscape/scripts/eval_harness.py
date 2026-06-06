"""Eval harness (ROADMAP C1): MEASURE the G2 number-fidelity gate's catch rate.

Builds labeled fixture ARA packages — some carrying a FABRICATED evidence number
(absent from the frozen source MD), some clean — runs G2 with a given skeptic
seam, and reports precision / recall / F1 of the block decision against the
labels. This turns "we have an adversarial gate" into "the gate catches
fabrication at rate X with no false blocks", so the guarantee is measurable, not
just asserted (paper-qa / STORM benchmark style).

The harness is seam-parameterized: run it with the production cross-model skeptic
to measure the REAL catch rate, or with the built-in oracle skeptic to verify the
gate's plumbing. CLI: `python -m scripts.eval_harness`.
"""

from __future__ import annotations

import tempfile
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from scripts.audit.g2_data_fidelity import run_g2
from scripts.audit.types import SkepticVote, SkepticVoteFn


@dataclass(frozen=True)
class EvalCase:
    name: str
    ai_package_dir: Path  # the entry dir (parent of ara/)
    md_path: Path
    should_block: bool  # ground-truth label


@dataclass(frozen=True)
class EvalReport:
    total: int
    tp: int  # fabrication correctly blocked
    fp: int  # clean paper wrongly blocked
    fn: int  # fabrication missed
    tn: int  # clean paper correctly passed

    @property
    def precision(self) -> float:
        denom = self.tp + self.fp
        return self.tp / denom if denom else 1.0

    @property
    def recall(self) -> float:
        denom = self.tp + self.fn
        return self.tp / denom if denom else 1.0

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if (p + r) else 0.0


def oracle_skeptic(numbers, source_md, claim_context):
    """A perfect skeptic: a number is 'found' iff it literally occurs in the MD."""
    return tuple(SkepticVote(number=n, found_in_source=(n in source_md)) for n in numbers)


def _write_case(
    root: Path, name: str, *, evidence_numbers: list[str], source_numbers: list[str]
) -> EvalCase:
    ara = root / "ai_package" / name / "ara"
    (ara / "logic").mkdir(parents=True)
    (ara / "evidence" / "tables").mkdir(parents=True)
    (ara / "logic" / "claims.md").write_text("# Claims\n", encoding="utf-8")
    rows = "\n".join(f"| M{i} | {v} |" for i, v in enumerate(evidence_numbers))
    (ara / "evidence" / "tables" / "main.md").write_text(
        "| Model | Score |\n|---|---|\n" + rows + "\n", encoding="utf-8"
    )
    md = root / f"{name}.md"
    md.write_text("Results: " + ", ".join(source_numbers) + ".\n", encoding="utf-8")
    should_block = not set(evidence_numbers).issubset(set(source_numbers))
    return EvalCase(name=name, ai_package_dir=ara.parent, md_path=md, should_block=should_block)


def build_number_fidelity_fixtures(root: Path) -> list[EvalCase]:
    """A small labeled corpus: clean papers + papers with a fabricated number."""
    root = Path(root)
    return [
        _write_case(
            root, "clean_a", evidence_numbers=["0.61", "0.52"], source_numbers=["0.61", "0.52"]
        ),
        _write_case(root, "clean_b", evidence_numbers=["28.4"], source_numbers=["28.4", "24.6"]),
        _write_case(root, "fab_a", evidence_numbers=["0.99"], source_numbers=["0.61"]),
        _write_case(root, "fab_b", evidence_numbers=["28.4", "99.9"], source_numbers=["28.4"]),
    ]


def evaluate_g2(
    cases: Sequence[EvalCase], *, skeptic_votes: SkepticVoteFn, n_skeptics: int = 3
) -> EvalReport:
    """Run G2 over labeled cases and score block-decision vs ground truth."""
    tp = fp = fn = tn = 0
    for c in cases:
        blocked = run_g2(
            c.ai_package_dir, c.md_path, skeptic_votes=skeptic_votes, n_skeptics=n_skeptics
        ).blocked
        if c.should_block:
            tp += blocked
            fn += not blocked
        else:
            fp += blocked
            tn += not blocked
    return EvalReport(total=len(cases), tp=tp, fp=fp, fn=fn, tn=tn)


if __name__ == "__main__":
    import sys

    with tempfile.TemporaryDirectory() as d:
        report = evaluate_g2(build_number_fidelity_fixtures(Path(d)), skeptic_votes=oracle_skeptic)
    print(
        f"G2 number-fidelity eval ({report.total} cases): "
        f"precision={report.precision:.2f} recall={report.recall:.2f} f1={report.f1:.2f} "
        f"(tp={report.tp} fp={report.fp} fn={report.fn} tn={report.tn})"
    )
    sys.exit(0)
