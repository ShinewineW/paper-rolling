"""Atomic dual-output: both vaults or neither (OT-5); overwrite by identity (OT-2)."""

from __future__ import annotations

from pathlib import Path

import pytest
import scripts.output.produce as produce_mod
from scripts.output.ara_schema import validate_ara_tree
from scripts.output.produce import produce_outputs
from scripts.paths import EngineAbort


def test_produce_writes_both_vaults_with_same_key(tmp_path, candidate, ledger, md_path, analyzer):
    result = produce_outputs(md_path, candidate, ledger, root=tmp_path, resolve_analysis=analyzer)
    person = tmp_path / "person_vault" / result.key
    ai = tmp_path / "ai_package" / result.key
    assert person.is_dir() and ai.is_dir()
    assert result.key.startswith("2026-06-05_DiffusionDrive_")
    assert (person / "report.md").exists()
    assert validate_ara_tree(ai / "ara") == []


def test_produce_is_atomic_neither_on_branch1_failure(
    tmp_path, candidate, ledger, md_path, analyzer, monkeypatch
):
    import scripts.output.produce as prod

    def boom(*a, **k):
        raise RuntimeError("branch1 blew up")

    monkeypatch.setattr(prod, "write_branch1", boom)
    with pytest.raises(RuntimeError):
        produce_outputs(md_path, candidate, ledger, root=tmp_path, resolve_analysis=analyzer)
    # OT-5: neither vault holds a partial entry.
    assert not (tmp_path / "person_vault").exists() or not any(
        (tmp_path / "person_vault").iterdir()
    )
    assert not (tmp_path / "ai_package").exists() or not any((tmp_path / "ai_package").iterdir())


def test_reprocess_overwrites_prior_identity_entry(tmp_path, candidate, ledger, md_path, analyzer):
    r1 = produce_outputs(md_path, candidate, ledger, root=tmp_path, resolve_analysis=analyzer)
    # Simulate a later run on a different intake date, same paper identity.
    ledger._intake = __import__("datetime").date(2026, 7, 1)
    r2 = produce_outputs(md_path, candidate, ledger, root=tmp_path, resolve_analysis=analyzer)
    assert r1.key != r2.key  # date prefix refreshed
    # Exactly ONE entry per identity per vault (OT-2).
    person_entries = list((tmp_path / "person_vault").iterdir())
    ai_entries = list((tmp_path / "ai_package").iterdir())
    assert len(person_entries) == 1
    assert len(ai_entries) == 1
    assert person_entries[0].name == r2.key


def test_produce_records_code_ref_in_ledger(tmp_path, candidate, ledger, md_path, analyzer):
    result = produce_outputs(md_path, candidate, ledger, root=tmp_path, resolve_analysis=analyzer)
    assert result.key in ledger.code_refs


def test_produce_aborts_before_promotion_when_cancelled(
    tmp_path, candidate, ledger, md_path, analyzer
):
    """Codex R17 stall-isolation: if the per-paper guard's cancel is already set
    by the time both gates pass, produce_outputs must NOT promote to the vault —
    a stalled-then-resumed daemon spoke leaves no products behind (OT-5 holds)."""
    import threading

    from scripts.output.produce import SpokeCancelled

    cancel = threading.Event()
    cancel.set()
    with pytest.raises(SpokeCancelled):
        produce_outputs(
            md_path,
            candidate,
            ledger,
            root=tmp_path,
            resolve_analysis=analyzer,
            cancel=cancel,
        )
    # Neither vault holds a partial entry.
    assert not (tmp_path / "person_vault").exists() or not any(
        (tmp_path / "person_vault").iterdir()
    )
    assert not (tmp_path / "ai_package").exists() or not any((tmp_path / "ai_package").iterdir())


def test_produce_reverts_promotion_when_cancelled_mid_move(
    tmp_path, candidate, ledger, md_path, analyzer
):
    """Codex R18: the post-promotion re-check must REVERT a promotion when the
    guard fires DURING the move (the single pre-check left a check-to-promotion
    race). A cancel that flips True only after the pre-check leaves NO vault dirs."""
    from scripts.output.produce import SpokeCancelled

    class _FlipCancel:
        def __init__(self):
            self.calls = 0

        def is_set(self):
            self.calls += 1
            return self.calls >= 2  # pre-check: not set; post-move check: set

    cancel = _FlipCancel()
    with pytest.raises(SpokeCancelled):
        produce_outputs(
            md_path,
            candidate,
            ledger,
            root=tmp_path,
            resolve_analysis=analyzer,
            cancel=cancel,
        )
    assert cancel.calls >= 2  # promotion happened between the two checks...
    # ...and was reverted: neither vault retains the promoted entry.
    assert not (tmp_path / "person_vault").exists() or not any(
        (tmp_path / "person_vault").iterdir()
    )
    assert not (tmp_path / "ai_package").exists() or not any((tmp_path / "ai_package").iterdir())


def test_produce_reverts_promotion_when_cancelled_after_code_ref(
    tmp_path, candidate, ledger, md_path, analyzer
):
    """Codex R19: a cancel landing during record_code_ref (AFTER the move-check)
    must still revert the promoted vault — the post-record re-check catches it."""
    from scripts.output.produce import SpokeCancelled

    class _FlipCancel:
        def __init__(self):
            self.calls = 0

        def is_set(self):
            self.calls += 1
            return self.calls >= 3  # pre-check + move-check: not set; post-record check: set

    cancel = _FlipCancel()
    with pytest.raises(SpokeCancelled):
        produce_outputs(
            md_path,
            candidate,
            ledger,
            root=tmp_path,
            resolve_analysis=analyzer,
            cancel=cancel,
        )
    assert cancel.calls >= 3  # the post-record-code-ref window was checked...
    # ...and the vault was reverted.
    assert not (tmp_path / "person_vault").exists() or not any(
        (tmp_path / "person_vault").iterdir()
    )
    assert not (tmp_path / "ai_package").exists() or not any((tmp_path / "ai_package").iterdir())


def test_produce_uses_passed_resolve_analysis_not_a_global(
    tmp_path, candidate, ledger, md_path, analysis
):
    """The analyzer seam is a parameter (no module global): the passed callable
    is the one invoked, and produce.py exposes no mutable `resolve_analysis`
    global. Foundation review: threaded spokes must not race a shared analyzer.
    """
    import scripts.output.produce as prod

    assert not hasattr(prod, "resolve_analysis")  # the mutable module global was removed

    calls = []

    def spy(md, cand):
        calls.append((md, cand))
        return analysis

    produce_outputs(md_path, candidate, ledger, root=tmp_path, resolve_analysis=spy)
    assert calls == [(md_path, candidate)]


def test_produce_gate_block_carries_staged_dir(tmp_path, candidate, ledger, md_path, analyzer):
    """审计 F / R1 Finding 2:G2 hard-block 时异常须携带 staged 父目录(含 ai/ara),供 spoke
    保全失败现场,不再被 finally 无条件删。既有成功/取消路径仍照常清理 staging。"""
    from scripts.output.produce import ProduceGateBlocked

    def blocking_gate(_ai_entry):
        class _Verdict:
            blocked = True
            findings = ()

        return _Verdict()

    with pytest.raises(ProduceGateBlocked) as ei:
        produce_outputs(
            md_path,
            candidate,
            ledger,
            root=tmp_path,
            resolve_analysis=analyzer,
            g2_gate=blocking_gate,
        )
    staged = ei.value.staged_dir
    assert staged is not None and staged.exists()
    assert (staged / "ai" / "ara").is_dir()  # branch2 产物完好,未被 finally 删
    # 未晋升:两 vault 空。
    assert not (tmp_path / "ai_package").exists() or not any((tmp_path / "ai_package").iterdir())
    assert not (tmp_path / "person_vault").exists() or not any(
        (tmp_path / "person_vault").iterdir()
    )


def test_llm_writer_without_faithfulness_judge_aborts_loudly(
    tmp_path, candidate, ledger, md_path, analyzer
):
    """Codex R16 (Final fresh-eyes gate): wiring the rich LLM writer (write_report)
    without a faithfulness_judge would silently disable the (c) 忠实门 layer in every
    production path (config routes the writer seam). stage_branch1 now aborts loudly
    on that misconfiguration instead of running judge=None (ADR-0012 + fail-loud)."""

    def fake_write_report(ara_dir, *, md_path=None, outdir=None):  # noqa: ARG001
        return {"sections": {}, "figures": []}

    with pytest.raises(ValueError, match="faithfulness_judge"):
        produce_outputs(
            md_path,
            candidate,
            ledger,
            root=tmp_path,
            resolve_analysis=analyzer,
            write_report=fake_write_report,
            faithfulness_judge=None,
        )
    # OT-5: nothing promoted.
    assert not (tmp_path / "person_vault").exists() or not any(
        (tmp_path / "person_vault").iterdir()
    )
    assert not (tmp_path / "ai_package").exists() or not any((tmp_path / "ai_package").iterdir())


def test_branch2_reemit_threads_repo_resolver(tmp_path, candidate, ledger, md_path, analyzer):
    """审计 R10:branch2 re-emit(prior_failure_analyzer)必须把注入的 repo_resolver
    透传到 write_branch2,不回退默认(否则丢 T2b/T4 码链解析)。"""
    calls = []

    def counting_resolver(*a, **k):
        calls.append((a, k))
        return []  # no repos resolved (signature-compatible counting fake)

    def analyzer_pf(md, cand, *, prior_failure=None):
        return analyzer(md, cand)  # reuse the fixture bundle; accept the re-emit kwarg

    produce_outputs(
        md_path,
        candidate,
        ledger,
        root=tmp_path,
        resolve_analysis=analyzer_pf,
        repo_resolver=counting_resolver,
        prior_failure_analyzer="上一稿 rigor 不足,请更严格核对源文数字",
    )
    assert calls, "branch2 re-emit 未调用注入的 repo_resolver(回退默认 = R10 回归)"


def test_engineabort_after_ara_built_preserves_staging(tmp_path, monkeypatch):
    # 让 branch2 渲染出一个非空 ARA 并过 Seal-1（不依赖真 analyzer bundle）。
    def fake_write_branch2(stage_ai, candidate, analysis, *, md_path, repo_resolver=None):
        Path(stage_ai).mkdir(parents=True, exist_ok=True)
        (Path(stage_ai) / "PAPER.md").write_text("ara", encoding="utf-8")

    monkeypatch.setattr(produce_mod, "write_branch2", fake_write_branch2)
    monkeypatch.setattr(produce_mod, "validate_ara_tree", lambda _stage_ai: [])

    md = tmp_path / "x.md"
    md.write_text("src", encoding="utf-8")
    candidate = {"title": "T", "arxiv_id": "2509.00001", "doi": None}

    class _Ledger:
        def intake_date(self):
            import datetime

            return datetime.date(2026, 6, 12)

        def record_code_ref(self, *a, **k): ...

    def abort_gate(_ai_entry):
        raise EngineAbort("qwen audit endpoint down")

    with pytest.raises(EngineAbort) as ei:
        produce_mod.produce_outputs(
            md,
            candidate,
            _Ledger(),
            root=tmp_path,
            resolve_analysis=lambda *a, **k: {"ok": 1},
            g2_gate=abort_gate,
        )
    staged = getattr(ei.value, "staged_dir", None)
    assert staged is not None, "EngineAbort must carry staged_dir when an ARA was built"
    assert (Path(staged) / "ai" / "ara" / "PAPER.md").exists(), "built ARA must survive the abort"


def test_engineabort_before_ara_built_still_cleans(tmp_path, monkeypatch):
    # analyzer transport down → ARA 没建 → staging 无 ARA → 仍然清理，不挂 staged_dir。
    md = tmp_path / "x.md"
    md.write_text("src", encoding="utf-8")
    candidate = {"title": "T", "arxiv_id": "2509.00002", "doi": None}

    class _Ledger:
        def intake_date(self):
            import datetime

            return datetime.date(2026, 6, 12)

    def abort_resolve(*a, **k):
        raise EngineAbort("analyzer backend down")

    with pytest.raises(EngineAbort) as ei:
        produce_mod.produce_outputs(
            md,
            candidate,
            _Ledger(),
            root=tmp_path,
            resolve_analysis=abort_resolve,
            g2_gate=lambda _x: None,
        )
    assert getattr(ei.value, "staged_dir", None) is None
