# tests/llm/test_seams.py
from __future__ import annotations


def test_build_seams_includes_faithfulness_judge() -> None:
    # ADR-0012: branch1 忠实门 (c) is the 7th routed seam.
    from scripts.llm.config import SEAMS
    from scripts.llm.seams import build_seams

    assert "faithfulness" in SEAMS
    assert "faithfulness_judge" in build_seams()


def test_faithfulness_judge_returns_prose_note(monkeypatch, tmp_path) -> None:
    # ADR-0012 rev: the judge writes a Chinese 评价 note (str), not a verdict dict.
    from scripts.llm import seams as S

    monkeypatch.setattr(S, "load_ara_bundle", lambda _d: {"claims.md": "C01: x"})
    monkeypatch.setattr(S, "_ask_text", lambda *_a, **_k: "整体与知识包一致,无实质误导。")
    note = S.faithfulness_judge("报告正文", tmp_path, ungrounded=["99.9"])
    assert isinstance(note, str) and "一致" in note


def test_faithfulness_judge_fails_soft_on_seam_error(monkeypatch, tmp_path) -> None:
    # ADR-0012 rev: the judge NEVER blocks — any seam error degrades to a neutral
    # note (str), it does NOT raise and does NOT return a fail-closed verdict.
    from scripts.llm import seams as S

    monkeypatch.setattr(S, "load_ara_bundle", lambda _d: {})

    def _boom(*_a, **_k):
        raise RuntimeError("endpoint down")

    monkeypatch.setattr(S, "_ask_text", _boom)
    note = S.faithfulness_judge("报告正文", tmp_path, ungrounded=[])
    assert isinstance(note, str)  # neutral fallback, did not raise


def test_faithfulness_judge_empty_response_falls_back(monkeypatch, tmp_path) -> None:
    # An empty/whitespace seam reply still yields a non-empty note.
    from scripts.llm import seams as S

    monkeypatch.setattr(S, "load_ara_bundle", lambda _d: {"claims.md": "x"})
    monkeypatch.setattr(S, "_ask_text", lambda *_a, **_k: "   ")
    assert S.faithfulness_judge("r", tmp_path).strip()


def test_faithfulness_judge_none_response_falls_back(monkeypatch, tmp_path) -> None:
    # A None seam reply must NOT raise (no .strip() on None) — neutral note instead.
    from scripts.llm import seams as S

    monkeypatch.setattr(S, "load_ara_bundle", lambda _d: {"claims.md": "x"})
    monkeypatch.setattr(S, "_ask_text", lambda *_a, **_k: None)
    assert S.faithfulness_judge("r", tmp_path).strip()


def test_faithfulness_judge_fails_soft_when_ara_unreadable(monkeypatch, tmp_path) -> None:
    # The ARA read is INSIDE the fail-soft guard: a corrupt ARA degrades to a neutral
    # note, it does not raise (the judge never blocks the report).
    from scripts.llm import seams as S

    def _boom(_d):
        raise RuntimeError("corrupt ARA")

    monkeypatch.setattr(S, "load_ara_bundle", _boom)
    assert S.faithfulness_judge("r", tmp_path).strip()


class _FakeCfg:
    def __init__(self, provider):
        self._p = provider

    def resolve_optional(self, _seam):
        return self._p


def test_web_search_off_returns_empty_when_seam_unrouted(monkeypatch) -> None:
    from scripts.llm import seams as S

    monkeypatch.setattr(S, "_cfg", lambda: _FakeCfg(None))  # optional seam not routed → T4 off
    assert S.web_search("FastWAM official code") == []


def test_web_search_parses_urls_highest_first(monkeypatch) -> None:
    from scripts.llm import seams as S

    class _Prov:
        name = "fake"

        def complete(self, _prompt, **_kw):  # accepts tier/effort/timeout/tools
            return (
                "Found it:\nhttps://github.com/yuantianyuan01/FastWAM\n"
                "https://huggingface.co/yuanty/fastwam (model)\n"
                "dup https://github.com/yuantianyuan01/FastWAM."
            )

    monkeypatch.setattr(S, "_cfg", lambda: _FakeCfg(_Prov()))
    assert S.web_search("FastWAM") == [
        "https://github.com/yuantianyuan01/FastWAM",
        "https://huggingface.co/yuanty/fastwam",
    ]


def test_web_search_fails_soft_on_provider_error(monkeypatch) -> None:
    from scripts.llm import seams as S

    class _Prov:
        name = "fake"

        def complete(self, *_a, **_k):
            raise RuntimeError("provider/EngineAbort — must not propagate from an enrichment tier")

    monkeypatch.setattr(S, "_cfg", lambda: _FakeCfg(_Prov()))
    assert S.web_search("x") == []  # fail-soft: never aborts a tick
