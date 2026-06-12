from __future__ import annotations

from scripts.audit.ara_tree import extract_numbers, number_present, source_value_set


def test_extract_numbers_basic() -> None:
    assert extract_numbers("BLEU 28.4 and ratio 0.5") == ("28.4", "0.5")


def test_extract_numbers_excludes_identifiers() -> None:
    # C01 / E02 structural IDs must NOT yield "01" / "02"
    nums = extract_numbers("C01: BLEU 42.1, experiment E02 score 10")
    assert "01" not in nums and "02" not in nums
    assert "42.1" in nums and "10" in nums


def test_source_value_set_parses_distinct_values() -> None:
    vals = source_value_set("BLEU 28.4 vs 24.6; ratio 0.5 and 50%.")
    assert 28.4 in vals and 24.6 in vals and 0.5 in vals


def test_number_present_matches_by_value_not_form() -> None:
    vals = source_value_set("reaches 28.4 NDS over 1 run")
    assert number_present("28.40", vals) is True  # trailing zero
    assert number_present("1.0", vals) is True  # 1.0 == 1
    assert number_present("99.9", vals) is False  # absent
    assert number_present("not-a-number", vals) is False
