"""批次复活驱动(ADR-0007 修订 / ADR-0009 修订)。

扫 _failed/ 所有自包含现场,branch 级重放:无条件复用上游已通过产物(基调-D2),
只重跑失败 branch;过则晋升+回写原 ledger_key 行+删现场,不过则更新现场。是 hub
之外第二个合法 ledger 写者,CLI 入口持 LS-1 锁(与 /loop tick 互斥)。per-scene
失败隔离 + 看门狗,可稳定长程自动化运行。
"""

from __future__ import annotations

import json
import os  # 审计 R16:崩溃恢复 os.replace
import shutil  # copy-not-move staging / 清理 temp
import sys
import tempfile
import threading  # 审计 R13:per-scene 看门狗用 daemon 线程 + cancel Event
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.audit.g2_data_fidelity import run_g2
from scripts.audit.g3_seal import run_g3
from scripts.audit_config import load_audit_config
from scripts.engine_version import current_commit
from scripts.failure_scene import FAILED_REL, write_scene
from scripts.output.branch1_report import AnchorGateError
from scripts.output.naming import vault_key
from scripts.output.produce import (
    ProduceGateBlocked,
    StructuralSealFailed,
    promote,
    stage_branch1,
    stage_branch2,
)


def _log(msg: str) -> None:
    """与 seams.py 同款 stderr 行日志(引擎无统一 logger 模块,审计 R1 Finding 6)。"""
    print(f"[revival] {msg}", file=sys.stderr, flush=True)


@dataclass(frozen=True)
class RevivalResult:
    key: str
    ledger_key: str
    status: str  # done | failed | error | manual(纯 ingest 根,需人工 re-ingest,审计 R15)
    failed_gate: str | None


def _classify_roots(findings: list[dict]) -> set[str]:
    """按 Finding.target 文件级归属(与 spoke._classify 同口径,ADR-0009 表)。"""
    roots: set[str] = set()
    for f in findings:
        t = str(f.get("target", ""))
        if t.endswith("report.md"):
            roots.add("branch1")
        elif t.endswith("level2_report.json") or "claims.md" in t.split(":")[0]:
            roots.add("branch2")
        elif t == "ara":
            # 结构门(Seal-1)失败的 finding target 是字面量 "ara"(spoke 写场时所记)。
            # 结构门是 branch2 根:复活时重跑整条 branch2(重调一次 analyzer,带结构错误
            # 反馈) —— spoke.py 注释明示 "Revival re-runs the whole branch2 chain"。
            # 必须早于下面的 ingest 兜底,否则结构门现场会被误判为 ingest 根 → manual,
            # 连一次复活重摇都拿不到。
            roots.add("branch2")
        else:
            roots.add("ingest")
    return roots


def _recover_interrupted_scenes(base: Path) -> None:
    """审计 R16:POSIX 无原子目录交换,write_scene 的两次 os.replace 之间崩溃会让
    canonical `<key>` 暂缺、完整现场落在 `.<key>.new`(目标新现场)或 `.<key>.old`(旧现场)。
    启动时补偿:canonical 缺失且 temp 带有效 scene.json → rename temp→canonical
    (**优先 `.new`**=本次目标;次选 `.old`=旧完整现场)。canonical 在场则 temp 是可清理残留。

    关键不变量:`.new` 仅在**完整建满后**才触发首个 rename,故"canonical 缺失"时 `.new`
    必然完整;由此任一崩溃点 {canonical, .new, .old} 至少有一个是完整现场、可恢复。
    """
    if not base.exists():
        return
    for suffix in (".new", ".old"):  # .new 优先于 .old
        for tmp in base.glob(f".*{suffix}"):
            key = tmp.name[1 : -len(suffix)]  # ".<key>.new" → "<key>"
            canonical = base / key
            if canonical.exists():
                continue
            if (tmp / "scene.json").exists():
                os.replace(str(tmp), str(canonical))  # 恢复完整现场到 canonical
                _log(f"recovered interrupted scene {key} from {tmp.name}")
    for suffix in (".new", ".old"):  # 清理 canonical 已在后的残留 temp
        for tmp in base.glob(f".*{suffix}"):
            shutil.rmtree(tmp, ignore_errors=True)
    # `.scene-*`(最终门 staged 中转)若残留=write_scene 前崩溃,内含 ai/person 但无
    # scene.json、不可自动恢复;仅 _log 提醒人工(产物仍在 _failed/ 子树内)。
    for orphan in base.glob(".scene-*"):
        _log(f"orphaned pre-write staging {orphan.name} (products under _failed/, manual triage)")


def _load_scenes(workspace: Path) -> list[tuple[Path, dict]]:
    """逐个现场容错加载——损坏的 scene.json 跳过并 log,不连累整批(中枢-D2)。"""
    base = Path(workspace) / FAILED_REL
    _recover_interrupted_scenes(base)  # 审计 R16:先补偿崩溃中断的换入,再加载
    out: list[tuple[Path, dict]] = []
    if base.exists():
        for d in sorted(base.iterdir()):
            if d.name.startswith("."):  # 跳过 .<key>.new/.old/.scene-* 临时目录
                continue
            mf = d / "scene.json"
            if not (d.is_dir() and mf.exists()):
                continue
            try:
                out.append((d, json.loads(mf.read_text(encoding="utf-8"))))
            except (ValueError, OSError) as exc:  # 损坏/半写现场:跳过,不崩整批
                _log(f"skip corrupt scene {d.name}: {exc}")
    return out


def revive_all(
    *,
    workspace: Path,
    ledger: Any,
    seams: dict,
    repo_resolver: Any = None,  # 审计 R10:必须随 stage_branch2 透传
    stall_seconds: float | None = None,  # 审计 R13:per-scene wall-clock 看门狗
    human_directive: str | None = None,
) -> list[RevivalResult]:
    """branch 级重放每个现场。per-scene 隔离 + wall-clock 看门狗,可稳定长程自动化运行。

    `repo_resolver`:复用引擎 `make_repo_resolver()`。凡走 `stage_branch2` 的分支都必须
    把它传下去,否则 branch2 重生丢 T2b/T4 码链解析(R10)。
    """
    results: list[RevivalResult] = []
    for scene_dir, manifest in _load_scenes(workspace):
        try:
            results.append(
                _run_revive_guarded(
                    workspace,
                    scene_dir,
                    manifest,
                    ledger,
                    seams,
                    repo_resolver=repo_resolver,
                    human_directive=human_directive,
                    stall_seconds=stall_seconds,
                )
            )
        except Exception as exc:  # noqa: BLE001 — 隔离到单篇(看门狗之外的意外)
            _log(f"scene {scene_dir.name} errored, left in place: {exc}")
            results.append(
                RevivalResult(
                    key=scene_dir.name,
                    ledger_key=manifest.get("ledger_key", ""),
                    status="error",
                    failed_gate=manifest.get("failed_gate"),
                )
            )
    return results


def _run_revive_guarded(
    workspace,
    scene_dir,
    manifest,
    ledger,
    seams,
    *,
    repo_resolver=None,
    human_directive=None,
    stall_seconds=None,
) -> RevivalResult:
    """审计 R13:_revive_one 的 wall-clock 看门狗(hub `_run_spoke_guarded` 同款机制)。

    daemon worker 跑 _revive_one;主线程 join(timeout)。超时 → set cancel(promote 前重检,
    放弃 staging copy;copy-not-move 保证现场完好),记 error,继续下一篇。stall_seconds
    None/<=0 = 不设墙钟(交由注入 seam 自身超时)。
    """
    cancel = threading.Event()
    box: dict = {}

    def _worker() -> None:
        try:
            box["result"] = _revive_one(
                workspace,
                scene_dir,
                manifest,
                ledger,
                seams,
                repo_resolver=repo_resolver,
                cancel=cancel,
                human_directive=human_directive,
            )
        except Exception as exc:  # noqa: BLE001 — 隔离到单篇
            box["error"] = exc

    worker = threading.Thread(target=_worker, daemon=True)
    worker.start()
    worker.join(timeout=stall_seconds if stall_seconds and stall_seconds > 0 else None)
    if worker.is_alive():  # 超时:放弃这篇,现场留原地
        cancel.set()
        _log(f"scene {scene_dir.name} exceeded {stall_seconds}s, left in place")
        return RevivalResult(
            key=scene_dir.name,
            ledger_key=manifest.get("ledger_key", ""),
            status="error",
            failed_gate=manifest.get("failed_gate"),
        )
    if "error" in box:
        raise box["error"]  # 交给 revive_all 的 per-scene except 记 error
    return box["result"]


def _revive_one(
    workspace,
    scene_dir,
    manifest,
    ledger,
    seams,
    *,
    repo_resolver=None,
    cancel=None,
    human_directive=None,
) -> RevivalResult:
    """branch 级重放一个现场:复用上游 → 只重跑失败 branch → 复核(staging)→ 过则
    晋升+先写 ledger 后删现场,不过则 append 现场(deferred 不变)。"""
    ledger_key = manifest.get("ledger_key", "")
    candidate = manifest["candidate"]
    md_path = Path(manifest["md_path"])
    failed_gate = manifest.get("failed_gate")
    findings = manifest.get("findings", [])
    content_list_path = scene_dir / "content_list.json"
    roots = _classify_roots(findings)

    # 审计 R18:只要混入任一 ingest 根(公式保真等),MD 本身坏,引擎内任何 branch 重跑都
    # 修不了 → 早于 branch 路由返回 manual(CLI 打印 invalidate 恢复命令)。
    if "ingest" in roots:
        return RevivalResult(
            key=scene_dir.name, ledger_key=ledger_key, status="manual", failed_gate=failed_gate
        )

    # 失败门 → 复活根:锚点门/最终门(branch1根)→ branch1;数字门/结构门/最终门(branch2根)→ branch2。
    src_ai = scene_dir / "ai"
    use_branch1 = (
        (failed_gate == "锚点门" or (failed_gate == "最终门" and "branch1" in roots))
        and ("branch2" not in roots)
        and src_ai.is_dir()
    )

    fb_body = "\n".join(f"- {f.get('target', '?')}: {f.get('observation', '')}" for f in findings)
    fb = "\n".join(x for x in (human_directive, fb_body) if x) or None

    cfg = load_audit_config(workspace)
    key = vault_key(
        intake=ledger.intake_date(),
        title=candidate["title"],
        arxiv_id=candidate.get("arxiv_id"),
        doi=candidate.get("doi"),
    )
    person_vault = Path(workspace) / "person_vault"
    ai_package = Path(workspace) / "ai_package"
    cl = content_list_path if content_list_path.exists() else None

    def _append_failed(gate: str, fnds: list[dict], staged: Path | None) -> RevivalResult:
        # 不过 → append attempt 到同一现场(角度 4),ledger 保持 deferred、不动。
        write_scene(
            workspace=Path(workspace),
            key=scene_dir.name,
            ledger_key=ledger_key,
            failed_gate=gate,
            findings=fnds,
            engine_commit=current_commit(workspace),
            candidate=candidate,
            md_path=md_path,
            content_list_path=cl,
            analysis=manifest.get("analysis"),
            staged_dir=staged,
        )
        return RevivalResult(
            key=scene_dir.name, ledger_key=ledger_key, status="failed", failed_gate=gate
        )

    staging = Path(tempfile.mkdtemp(prefix="revive-stage-"))
    try:
        if use_branch1:
            # 复用 branch2 SSOT —— COPY 不 move,现场保持完好直到 record(done) 成功(角度 1)。
            shutil.copytree(src_ai, staging / "ai")
            stage_ai = staging / "ai" / "ara"
            stage_branch1(
                staging,
                candidate,
                stage_ai,
                md_path,
                seams.get("write_report"),
                manifest.get("analysis"),
                key,
                prior_failure=fb,
            )
        else:
            # branch2 整条重跑:重调 analyzer(带反馈)+ G2 复核 + branch1(R10:透传 repo_resolver)。
            stage_ai, _analysis = stage_branch2(
                staging,
                candidate,
                md_path,
                resolve_analysis=seams["resolve_analysis"],
                repo_resolver=repo_resolver,
                prior_failure=fb,
            )
            g2 = run_g2(
                staging / "ai",
                md_path,
                skeptic_votes=seams["skeptic_votes"],
                n_skeptics=cfg.skeptic_votes,
                tolerant=cfg.data_fidelity_tolerant,
                max_unconfirmed=cfg.data_fidelity_max_unconfirmed,
                max_unconfirmed_ratio=cfg.data_fidelity_max_unconfirmed_ratio,
            )
            if g2.blocked:
                raise ProduceGateBlocked(g2, staged_dir=staging)
            stage_branch1(
                staging,
                candidate,
                stage_ai,
                md_path,
                seams.get("write_report"),
                _analysis,
                key,
                prior_failure=fb,
            )

        # 复核一律对 staging 跑、promote 只在通过后(审计 R2 Finding 3:严禁先 promote 再复核)。
        # 注:run_g3 收 content_list_path 原值(非上面 write_scene 用的 None-容忍 `cl`)——
        # check_equation_fidelity 需要一个**具体**路径,而 spoke 写出的现场恒有 content_list.json
        # (tier-1 合成 / tier-2 emit,write_scene 快照入现场)。仅 hand-built/损坏现场可能缺它,
        # 那种 FileNotFoundError 由 revive_all 的 per-scene except 兜成 error、现场完好(CR MED-1)。
        verdict = run_g3(
            staging / "person",
            staging / "ai",
            md_path,
            content_list_path,
            rigor_scores=seams["rigor_scores"],
            entailment_judge=seams["entailment_judge"],
        )
        if verdict.blocked:
            return _append_failed(
                failed_gate or "最终门", [f.as_dict() for f in verdict.hard_findings], staging
            )

        # 看门狗中止契约(角度 6 + R13):promote 前重检 cancel,放弃 staging copy;现场完好。
        if cancel is not None and cancel.is_set():
            return RevivalResult(
                key=scene_dir.name, ledger_key=ledger_key, status="error", failed_gate=failed_gate
            )

        result = promote(
            staging,
            key,
            candidate=candidate,
            ledger=ledger,
            person_vault=person_vault,
            ai_package=ai_package,
            cancel=cancel,
        )
        # 审计 sharp-edges/race:看门狗可能在 promote 返回后、record(done) 前才触发。一个被
        # 放弃(超时)的 daemon 绝不能在 driver 已记 error 之后还 record(done)+删现场。再重检
        # cancel:若已 set → 不写 ledger、不删现场(留 deferred + 完好现场),promote 刚晋升的
        # vault 产物成无 done 行的孤儿,由 consistency_check 下个 tick 剪除,自愈。
        if cancel is not None and cancel.is_set():
            return RevivalResult(
                key=scene_dir.name, ledger_key=ledger_key, status="error", failed_gate=failed_gate
            )
        # 先写 ledger 后删现场(sim-review 角度 1):崩在 record 前 → 现场完好(已 copy),
        # consistency_check 删 vault 孤儿后下轮从完好现场重来,自愈。
        ledger.record(
            ledger_key,
            status="done",
            person_vault_path=str(result.person_path),
            ai_package_path=str(result.ai_path),
        )
        shutil.rmtree(scene_dir, ignore_errors=True)
        return RevivalResult(
            key=scene_dir.name, ledger_key=ledger_key, status="done", failed_gate=failed_gate
        )
    # 注(CR LOW-1):promote 抛的 SpokeCancelled 不在此捕获——它故意逃逸到 revive_all 的
    # per-scene `except Exception` 兜成 error;promote 内部已 revert vault、copy-not-move 保证
    # 现场完好,与显式处理等价。下面三门是「重跑仍挂下游门」→ append 现场(deferred 不变)。
    except StructuralSealFailed as exc:
        return _append_failed(
            "结构门", [{"target": "ara", "observation": e} for e in exc.errors], exc.staged_dir
        )
    except ProduceGateBlocked as exc:
        return _append_failed(
            "数字门",
            [f.as_dict() for f in exc.verdict.hard_findings],
            getattr(exc, "staged_dir", staging),
        )
    except AnchorGateError as exc:
        return _append_failed(
            "锚点门",
            [{"target": "report.md", "observation": str(exc)}],
            getattr(exc, "staged_dir", staging),
        )
    finally:
        shutil.rmtree(staging, ignore_errors=True)


if __name__ == "__main__":
    import argparse

    from scripts.ledger.store import Ledger
    from scripts.llm.seams import build_seams
    from scripts.output.repo_resolve import make_repo_resolver  # R10:复活也要码链解析

    ap = argparse.ArgumentParser(description="批次复活赛:重放 _failed/ 所有现场")
    ap.add_argument("--workspace", default=".")
    ap.add_argument("--directive", default=None, help="可选:注入所有重放篇的一句人工指令")
    args = ap.parse_args()
    ws = Path(args.workspace)
    _ledger = Ledger(ws)
    # R10:构造与生产同款 repo_resolver(默认 T2b HF-live;对齐 run_campaign)。
    _resolver = make_repo_resolver()
    with _ledger.acquire():  # LS-1:与 /loop tick 互斥;整批持锁=复活期间 /loop 停摆
        _res = revive_all(
            workspace=ws,
            ledger=_ledger,
            seams=build_seams(),
            repo_resolver=_resolver,
            human_directive=args.directive,
        )
    _done = sum(1 for r in _res if r.status == "done")
    _errs = sum(1 for r in _res if r.status == "error")
    _manual = [r for r in _res if r.status == "manual"]
    print(f"复活:{_done}/{len(_res)} 晋升" + (f"({_errs} 篇出错已隔离)" if _errs else ""))
    if _manual:  # 审计 R15:ingest 根不可静默卡死,给可操作出口
        print(f"\n⚠️ {len(_manual)} 篇为 ingest 根(MD 公式损坏),引擎内不可自动修,需人工 re-ingest:")
        for r in _manual:
            print(
                f"  - {r.key}: python -m scripts.invalidate {r.ledger_key} "
                "--topic-dir <dir>  # 清 deferred 行后重转 PDF→下次 /loop 重处理"
            )
    sys.exit(0 if (_done or not _res) else 1)
