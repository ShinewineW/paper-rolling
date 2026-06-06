"""Eval harness (ROADMAP C1): the G2 catch-rate measurement is itself trustworthy."""

from __future__ import annotations

from scripts.audit.types import SkepticVote
from scripts.eval_harness import build_number_fidelity_fixtures, evaluate_g2, oracle_skeptic


def test_eval_harness_oracle_skeptic_is_perfect(tmp_path):
    """With a perfect (oracle) skeptic, G2 catches every fabrication and never
    false-blocks a clean paper — precision == recall == 1.0."""
    cases = build_number_fidelity_fixtures(tmp_path)
    report = evaluate_g2(cases, skeptic_votes=oracle_skeptic)
    assert report.total == 4
    assert report.recall == 1.0  # every fabrication blocked
    assert report.precision == 1.0  # no clean paper blocked
    assert report.fn == 0 and report.fp == 0


def test_eval_harness_surfaces_a_blind_skeptic(tmp_path):
    """The harness MEASURES skeptic quality: a blind skeptic that always says
    'found' catches nothing — recall drops to 0.0 (proving the harness discriminates)."""
    cases = build_number_fidelity_fixtures(tmp_path)

    def blind_skeptic(numbers, source_md, claim_context):
        return tuple(SkepticVote(number=n, found_in_source=True) for n in numbers)

    report = evaluate_g2(cases, skeptic_votes=blind_skeptic)
    assert report.recall == 0.0  # blind skeptic misses every fabrication
    assert report.tp == 0
