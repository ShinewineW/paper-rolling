"""批次复活驱动:branch 级重放、复用上游、先写 ledger 后删现场、看门狗、崩溃恢复。"""

from __future__ import annotations

import json
from pathlib import Path

from scripts.hub import _candidate_key
from scripts.ledger.store import Ledger
from scripts.output.branch2_ara import write_branch2
from scripts.revival import _load_scenes, revive_all

# Reuse the spoke test's bundle + bench seams (审计 D5: 散装 seam,非 fake_seams_*).
from test_spoke import (
    _ANALYSIS,
    _CANDIDATE,
    _SOURCE_MD,
    _all_found_skeptic,
    _entailed,
    _good_rigor,
    _low_rigor,
    _resolve_analysis,
)

_KEY = "2026-06-09_DiffusionDrive_2411.15139"


def _seams(*, rigor_scores=_good_rigor):
    return {
        "resolve_analysis": _resolve_analysis,
        "skeptic_votes": _all_found_skeptic,
        "rigor_scores": rigor_scores,
        "entailment_judge": _entailed,
        "write_report": None,  # deterministic write_branch1 path
    }


def _write_md(tmp_path: Path) -> Path:
    corpus = tmp_path / "corpus" / "DiffusionDrive"
    corpus.mkdir(parents=True, exist_ok=True)
    md = corpus / "DiffusionDrive.md"
    md.write_text(_SOURCE_MD, encoding="utf-8")
    return md


def _seed_scene(
    tmp_path: Path,
    ledger: Ledger,
    *,
    failed_gate: str,
    findings: list[dict],
    with_real_ara: bool = False,
    analysis: dict | None = None,
) -> tuple[Path, str]:
    """Hand-build a self-contained scene under _failed/<key>/.

    with_real_ara=True renders a valid branch2 ara (so a branch1 revival can REUSE
    it); otherwise a placeholder ai/ (branch2 revival re-generates it).
    """
    md = _write_md(tmp_path)
    scene = tmp_path / "_failed" / _KEY
    scene.mkdir(parents=True)
    (scene / "content_list.json").write_text(json.dumps([{"type": "equation"}]), encoding="utf-8")
    if with_real_ara:
        write_branch2(scene / "ai" / "ara", dict(_CANDIDATE), _ANALYSIS, md_path=md)
    else:
        (scene / "ai" / "ara").mkdir(parents=True)
    lk = _candidate_key(dict(_CANDIDATE))
    manifest = {
        "key": _KEY,
        "ledger_key": lk,
        "failed_gate": failed_gate,
        "findings": findings,
        "engine_commit": "seed",
        "candidate": dict(_CANDIDATE),
        "md_path": str(md),
        "analysis": analysis,
        "attempts": [
            {
                "ts": "seed",
                "engine_commit": "seed",
                "failed_gate": failed_gate,
                "findings": findings,
            }
        ],
    }
    (scene / "scene.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    ledger.record(lk, status="deferred", failure_class="audit_block", retry_after=None)
    return scene, lk


_RIGOR_FINDING = [
    {"target": "level2_report.json", "observation": "rigor below seal", "severity": "hard"}
]


def test_revive_promotes_and_clears_and_flips_ledger(tmp_path):
    led = Ledger(tmp_path)
    scene, lk = _seed_scene(tmp_path, led, failed_gate="最终门", findings=_RIGOR_FINDING)
    with led.acquire():
        res = revive_all(workspace=tmp_path, ledger=led, seams=_seams(rigor_scores=_good_rigor))
    assert res and res[0].status == "done"
    assert not scene.exists()  # 现场清除
    last = led.entries()[-1]
    assert last["key"] == lk and last["status"] == "done"  # 原 ledger 行翻 done
    assert lk in led.skip_set()


def test_revive_still_failing_updates_scene(tmp_path):
    led = Ledger(tmp_path)
    scene, lk = _seed_scene(tmp_path, led, failed_gate="最终门", findings=_RIGOR_FINDING)
    with led.acquire():
        res = revive_all(workspace=tmp_path, ledger=led, seams=_seams(rigor_scores=_low_rigor))
    assert res[0].status == "failed"
    assert (scene / "scene.json").exists()  # 现场保留
    m = json.loads((scene / "scene.json").read_text())
    assert len(m["attempts"]) == 2  # 角度 4:append 一条
    assert lk in led.skip_set()  # 仍 deferred(无 TTL)→ 仍 skip,等下次复活


def test_revive_threads_repo_resolver_into_branch2(tmp_path):
    led = Ledger(tmp_path)
    _seed_scene(tmp_path, led, failed_gate="最终门", findings=_RIGOR_FINDING)
    calls = []

    def counting_resolver(*a, **k):
        calls.append((a, k))
        return []

    with led.acquire():
        revive_all(
            workspace=tmp_path,
            ledger=led,
            seams=_seams(rigor_scores=_good_rigor),
            repo_resolver=counting_resolver,
        )
    assert calls, "复活 branch2 重生未调用注入的 repo_resolver(R10 回归)"


def test_revive_anchor_gate_scene_promotes(tmp_path):
    led = Ledger(tmp_path)
    # 锚点门 → branch1 root: reuse the real branch2 ara + the seeded analysis.
    scene, lk = _seed_scene(
        tmp_path,
        led,
        failed_gate="锚点门",
        findings=[{"target": "report.md", "observation": "unresolved anchor", "severity": "hard"}],
        with_real_ara=True,
        analysis=_ANALYSIS,
    )
    with led.acquire():
        res = revive_all(workspace=tmp_path, ledger=led, seams=_seams(rigor_scores=_good_rigor))
    assert res[0].status == "done"
    assert not scene.exists()
    last = led.entries()[-1]
    assert last["key"] == lk and last["status"] == "done"


def test_revive_watchdog_aborts_hung_scene(tmp_path):
    import time

    led = Ledger(tmp_path)
    scene, lk = _seed_scene(tmp_path, led, failed_gate="最终门", findings=_RIGOR_FINDING)

    def _hang(_bundle):
        time.sleep(60)  # never returns within the watchdog window

    with led.acquire():
        res = revive_all(
            workspace=tmp_path,
            ledger=led,
            seams=_seams(rigor_scores=_hang),
            stall_seconds=0.5,
        )
    assert res[0].status == "error"
    assert (scene / "scene.json").exists()  # 现场完好(copy-not-move)
    assert lk in led.skip_set()  # ledger 未动,仍 deferred


def test_revive_mixed_ingest_final_gate_is_manual(tmp_path):
    led = Ledger(tmp_path)
    scene, lk = _seed_scene(
        tmp_path,
        led,
        failed_gate="最终门",
        findings=[
            {
                "target": "2411.15139v1.md",
                "observation": "equation-block mismatch",
                "severity": "hard",
            },
            {"target": "level2_report.json", "observation": "rigor below seal", "severity": "hard"},
        ],
    )
    with led.acquire():
        res = revive_all(workspace=tmp_path, ledger=led, seams=_seams(rigor_scores=_good_rigor))
    assert res[0].status == "manual"  # 早于 branch 路由
    assert (scene / "scene.json").exists()  # 现场保留
    assert led.entries()[-1]["status"] == "deferred"  # ledger 未动


def test_load_scenes_recovers_crash_between_renames(tmp_path):
    base = tmp_path / "_failed"
    base.mkdir()
    # Crash state: canonical 'k1' missing; complete new scene in .k1.new (has scene.json).
    newd = base / ".k1.new"
    newd.mkdir()
    (newd / "scene.json").write_text('{"ledger_key":"1234.5678","attempts":[{}]}', encoding="utf-8")
    scenes = _load_scenes(tmp_path)
    assert (base / "k1" / "scene.json").exists()  # recovered to canonical
    assert not newd.exists()  # temp consumed
    assert any(d.name == "k1" for d, _ in scenes)  # discoverable for revival
    # Alt: canonical missing, only .k2.old (old complete scene) → also recovered.
    oldd = base / ".k2.old"
    oldd.mkdir()
    (oldd / "scene.json").write_text('{"ledger_key":"9.9","attempts":[{}]}', encoding="utf-8")
    _load_scenes(tmp_path)
    assert (base / "k2" / "scene.json").exists()
