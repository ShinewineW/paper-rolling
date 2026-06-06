"""Behavior tests for the vendored title-similarity module (similarity/THRESHOLD).

`discovery/_text.py` is the vendored ARS `_text_similarity.py` (CC-BY-NC) + an
alias trailer; these assertions pin its observable behavior (0.70 threshold,
punctuation-normalized SequenceMatcher ratio).
"""

from __future__ import annotations

import pytest

from scripts.discovery._text import THRESHOLD, normalize_title, similarity


def test_normalize_lowercases_and_punct_to_space():
    assert normalize_title("R.A.G.") == "r a g"


def test_normalize_collapses_whitespace():
    assert normalize_title("Attention   Is\tAll  You\nNeed") == "attention is all you need"


def test_identical_titles_score_one():
    assert similarity("Attention Is All You Need", "Attention Is All You Need") == 1.0


@pytest.mark.parametrize(
    ("a", "b", "expect_match"),
    [
        # ARS-captured: punctuation-only differences clear the 0.70 bar.
        ("Attention Is All You Need", "Attention is all you need!", True),
        ("R.A.G.", "RAG", True),
        (
            "BERT: Pre-training of Deep Bidirectional Transformers",
            "BERT Pre training of Deep Bidirectional Transformers",
            True,
        ),
        # Genuinely different titles fall below the bar.
        ("Attention Is All You Need", "Deep Residual Learning for Image Recognition", False),
    ],
)
def test_threshold_classification_matches_ars(a, b, expect_match):
    assert (similarity(a, b) >= THRESHOLD) is expect_match


def test_threshold_constant_is_070():
    assert THRESHOLD == 0.70
