from __future__ import annotations

from pathlib import Path

from scripts.audit.g2_data_fidelity import (
    extract_claim_registry,
    extract_numbers,
    run_g2,
)
from scripts.audit.types import SkepticVote


def _make_ai_package(tmp_path: Path) -> Path:
    """Build a minimal ai_package with one evidence table + one claim."""
    root = tmp_path / "ai_package" / "2026-06-05_Transformer_170603762"
    ara = root / "ara"
    (ara / "logic").mkdir(parents=True)
    (ara / "evidence" / "tables").mkdir(parents=True)
    (ara / "logic" / "claims.md").write_text(
        "## C01: Outperforms RNN baseline\n\n"
        "**Statement**: Our model reaches a BLEU of 28.4, outperforming the RNN baseline.\n"
        "**Proof**: E01\n",
        encoding="utf-8",
    )
    (ara / "evidence" / "tables" / "main.md").write_text(
        "| Model | BLEU |\n|---|---|\n| RNN | 24.6 |\n| Ours | 28.4 |\n",
        encoding="utf-8",
    )
    return ara


def test_extract_numbers_pulls_decimals_and_ints() -> None:
    nums = extract_numbers("BLEU of 28.4 beats 24.6 over 3 runs.")
    assert "28.4" in nums and "24.6" in nums and "3" in nums


def test_extract_claim_registry_reads_claims_md(tmp_path: Path) -> None:
    ara = _make_ai_package(tmp_path)
    registry = extract_claim_registry(ara)
    assert len(registry) == 1
    assert registry[0].claim_id == "C01"
    assert "28.4" in registry[0].numbers
    assert registry[0].proof_experiment_ids == ("E01",)


def test_run_g2_passes_when_every_number_grounds_in_source(tmp_path: Path) -> None:
    ara = _make_ai_package(tmp_path)
    md = tmp_path / "src.md"
    md.write_text("The model achieves a BLEU of 28.4 versus 24.6 for the RNN.\n", encoding="utf-8")

    def honest_skeptic(numbers, source_md, claim_context):
        return tuple(SkepticVote(number=n, found_in_source=(n in source_md)) for n in numbers)

    verdict = run_g2(ara.parent, md, skeptic_votes=honest_skeptic, n_skeptics=3)
    assert verdict.blocked is False


def test_run_g2_hard_blocks_a_fabricated_number(tmp_path: Path) -> None:
    """A number present in evidence but absent from the source MD = fabrication."""
    ara = _make_ai_package(tmp_path)
    # Source MD does NOT contain 28.4 — the evidence table fabricated it.
    md = tmp_path / "src.md"
    md.write_text(
        "The model achieves a BLEU of 24.6 (no improvement reported).\n", encoding="utf-8"
    )

    def honest_skeptic(numbers, source_md, claim_context):
        return tuple(SkepticVote(number=n, found_in_source=(n in source_md)) for n in numbers)

    verdict = run_g2(ara.parent, md, skeptic_votes=honest_skeptic, n_skeptics=3)
    assert verdict.blocked is True
    hard = verdict.hard_findings[0]
    assert "28.4" in hard.observation
    assert hard.is_hard_block is True


def test_run_g2_uses_majority_vote_not_single_skeptic(tmp_path: Path) -> None:
    """1 skeptic crying fabrication out of 3 does NOT block (majority must agree)."""
    ara = _make_ai_package(tmp_path)
    md = tmp_path / "src.md"
    md.write_text("BLEU of 28.4 versus 24.6.\n", encoding="utf-8")

    calls = {"n": 0}

    def flaky_skeptic(numbers, source_md, claim_context):
        calls["n"] += 1
        # The 2nd skeptic invocation falsely claims 28.4 is missing; the other
        # two correctly find it. Majority (2/3) = present, so no block.
        lies = calls["n"] == 2
        return tuple(
            SkepticVote(
                number=n,
                found_in_source=(False if (lies and n == "28.4") else (n in source_md)),
            )
            for n in numbers
        )

    verdict = run_g2(ara.parent, md, skeptic_votes=flaky_skeptic, n_skeptics=3)
    assert calls["n"] == 3
    assert verdict.blocked is False


def test_run_g2_skeptic_seam_never_receives_evidence_path(tmp_path: Path) -> None:
    """Ground-truth isolation: the skeptic seam gets candidate numbers + source
    text only, never a handle to the evidence file (the 'answer')."""
    ara = _make_ai_package(tmp_path)
    md = tmp_path / "src.md"
    md.write_text("BLEU of 28.4 versus 24.6.\n", encoding="utf-8")

    seen_args: list[tuple] = []

    def spy_skeptic(numbers, source_md, claim_context):
        seen_args.append((numbers, source_md, claim_context))
        return tuple(SkepticVote(number=n, found_in_source=True) for n in numbers)

    run_g2(ara.parent, md, skeptic_votes=spy_skeptic, n_skeptics=1)
    for _numbers, source_md, claim_context in seen_args:
        assert isinstance(source_md, str)
        # source_md is the MD ground truth, not the evidence table content.
        assert "| Ours |" not in source_md
        assert str(ara) not in claim_context
