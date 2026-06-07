from __future__ import annotations

import json

import pytest
from scripts.llm.jsonparse import extract_json, repair_json_escapes


def test_plain_object() -> None:
    assert extract_json('{"a": 1, "b": "x"}') == {"a": 1, "b": "x"}


def test_fenced_json() -> None:
    assert extract_json('```json\n{"a": 1}\n```') == {"a": 1}


def test_latex_invalid_escape_is_repaired() -> None:
    # The deepseek analyzer failure: LaTeX inside a JSON string with a lone
    # backslash (`\m`, `\m`, `\b`...) -> json.loads raises "Invalid \escape".
    bad = '{"algorithm": "$\\mathcal{L} = \\mathbb{E}[\\epsilon]$"}'
    # sanity: raw json.loads would choke on \m / \m (\\e is valid-ish but \m isn't)
    out = extract_json(bad)
    assert out["algorithm"] == "$\\mathcal{L} = \\mathbb{E}[\\epsilon]$"


def test_valid_escapes_preserved() -> None:
    # Legitimate JSON escapes (\n, \", \\) must NOT be doubled.
    out = extract_json(r'{"s": "line1\nline2 \"q\" \\ done"}')
    assert out["s"] == 'line1\nline2 "q" \\ done'


def test_prose_wrapped_array() -> None:
    assert extract_json("Here you go: [1, 2, 3] hope that helps") == [1, 2, 3]


def test_repair_only_doubles_bad_backslashes() -> None:
    assert repair_json_escapes(r'"\mathbf"') == r'"\\mathbf"'
    assert repair_json_escapes(r'"\n\t\\"') == r'"\n\t\\"'  # valid escapes untouched


def test_unparseable_raises() -> None:
    with pytest.raises(ValueError, match="no JSON value found"):
        extract_json("just prose, no json here")


def test_repair_does_not_over_escape_valid_backslash_pairs():
    # The bug that crashed the analyzer: a valid escaped backslash (\\mathbf) must
    # NOT be turned into \\\mathbf. Pairwise scan keeps valid pairs intact.
    s = r'{"d":"x\\y"}'
    assert repair_json_escapes(s) == s
    assert json.loads(repair_json_escapes(s))["d"] == "x\\y"


def test_repair_recovers_mixed_valid_and_lone_latex():
    # Real failure: escaped \\mathbf / \\mathbb (valid) + lone \! \in (invalid).
    s = r'{"d":"$\\mathbf{w} \!\in \\mathbb{R}$"}'
    with pytest.raises(json.JSONDecodeError):
        json.loads(s)  # lone \! is an invalid JSON escape
    assert extract_json(s)["d"] == r"$\mathbf{w} \!\in \mathbb{R}$"
