# tests/llm/test_seams.py
from __future__ import annotations


def test_build_seams_includes_faithfulness_judge() -> None:
    # ADR-0012: branch1 忠实门 (c) is the 7th routed seam.
    from scripts.llm.config import SEAMS
    from scripts.llm.seams import build_seams

    assert "faithfulness" in SEAMS
    assert "faithfulness_judge" in build_seams()


def test_faithfulness_judge_fails_closed_on_seam_error(monkeypatch, tmp_path) -> None:
    # ADR-0012: a transport/RuntimeError from the judge seam must fail CLOSED.
    from scripts.llm import seams as S

    monkeypatch.setattr(S, "load_ara_bundle", lambda _d: {})

    def _boom(*_a, **_k):
        raise RuntimeError("endpoint down")

    monkeypatch.setattr(S, "_ask_json", _boom)
    verdict = S.faithfulness_judge("报告正文", tmp_path)
    assert verdict["faithful"] is False
    assert verdict["findings"]  # carries the error as a finding


def test_faithfulness_judge_normalizes_response(monkeypatch, tmp_path) -> None:
    from scripts.llm import seams as S

    monkeypatch.setattr(S, "load_ara_bundle", lambda _d: {"claims.md": "C01: x"})

    # malformed (no "faithful" key) -> fail closed
    monkeypatch.setattr(S, "_ask_json", lambda *_a, **_k: {"oops": 1})
    assert S.faithfulness_judge("r", tmp_path)["faithful"] is False

    # non-list findings -> normalized to []
    monkeypatch.setattr(
        S, "_ask_json", lambda *_a, **_k: {"faithful": True, "findings": "not-a-list"}
    )
    v = S.faithfulness_judge("r", tmp_path)
    assert v["faithful"] is True and v["findings"] == []

    # a real material-misleading verdict passes through
    monkeypatch.setattr(
        S,
        "_ask_json",
        lambda *_a, **_k: {
            "faithful": False,
            "findings": [{"claim": "x", "issue": "misattributed"}],
        },
    )
    v = S.faithfulness_judge("r", tmp_path)
    assert v["faithful"] is False and v["findings"][0]["issue"] == "misattributed"
