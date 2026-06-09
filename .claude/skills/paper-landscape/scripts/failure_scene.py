"""自包含失败现场写入器（ADR-0007 修订 / CONTEXT.md 失败现场）。

门控失败时不删产物，连同复活所需的全部上游引用（candidate/md_path/content_list/
analysis/ledger_key）一起移入 `_failed/<key>/`，供人工排查与批次复活赛复用。
`_failed/` gitignored —— 现场是本地诊断 scratch，不是产物。
"""

from __future__ import annotations

import json
import os  # 审计 R15:os.replace 原子换入现场
import shutil
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

FAILED_REL = Path("_failed")


def _iso_now() -> str:
    """UTC ISO 时间戳，供 attempt 历史记录（角度 4）。"""
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass(frozen=True)
class SceneManifest:
    key: str
    ledger_key: str  # = hub 的 _candidate_key（与 vault key 不同命名空间，复活据此回写）
    failed_gate: str  # 最近一次:结构门/数字门/锚点门/最终门
    findings: list[dict]  # 最近一次的 hard_findings
    engine_commit: str  # 仅诊断:最近一次在哪个引擎版本挂的(不参与复用判定,ADR-0007)
    candidate: dict  # write_branch2/vault_key 需要
    md_path: str  # run_g3/stage_branch2 需要（绝对路径）
    analysis: dict | None  # 已通过的 analyzer bundle（下游失败时复用，免重跑 analyzer）
    attempts: list[dict]  # 失败演化轨迹(角度 4):每条 {ts, engine_commit, failed_gate, findings}


def write_scene(
    *,
    workspace: Path,
    key: str,
    ledger_key: str,
    failed_gate: str,
    findings: list[dict[str, Any]],
    engine_commit: str,
    candidate: dict,
    md_path: Path,
    content_list_path: Path | None,
    analysis: dict | None,
    staged_dir: Path | None,
) -> Path:
    """写自包含现场到 `_failed/<key>/`，返回现场目录。再失败时 **追加** attempt 历史(角度 4)。"""
    scene = Path(workspace) / FAILED_REL / key
    # 角度 4:再失败不覆盖历史——先读出已有 attempts，append 本次，再重建现场。
    prior_attempts: list[dict] = []
    old_manifest = scene / "scene.json"
    if old_manifest.exists():
        try:
            prior_attempts = json.loads(old_manifest.read_text(encoding="utf-8")).get(
                "attempts", []
            )
        except (ValueError, OSError):
            prior_attempts = []
    this_attempt = {
        "ts": _iso_now(),
        "engine_commit": engine_commit,
        "failed_gate": failed_gate,
        "findings": findings,
    }

    # 审计 R3 Finding 2:复活在「不过 → append 历史」时,content_list_path 往往**就是**
    # `scene/content_list.json`(复活从现场读它)。下面的 rmtree(scene) 会先把源删掉,
    # 随后 copy2 因源不存在而跳过 → 更新后的现场丢失 content_list、不再自包含。
    # 故在 rmtree 之前把字节快照进内存,删后从快照写回(对 source 在不在 scene 内都安全)。
    content_bytes: bytes | None = None
    if content_list_path is not None and Path(content_list_path).exists():
        content_bytes = Path(content_list_path).read_bytes()

    # 审计 R15/R16 BLOCKER 1:旧写法 rmtree(scene) 后逐步重建——崩在中途会**抹掉唯一现场**
    # (而 ledger 已 deferred 永久 skip → 论文彻底丢)。改为
    # **sibling 临时目录建满 + 原子 rename 换入**:
    #   _failed/.<key>.new/ 里把 scene.json + ai/ + person/ + content_list.json 全部落齐,
    #   再用 os.replace 换入 _failed/<key>/。临时目录与 scene 同在 _failed/(同一文件系统)→
    #   rename 是元数据操作、原子。
    #   ⚠️ POSIX 无原子目录"交换",两次 rename(old→.old, new→canonical)之间有一个亚毫秒窗口
    #   canonical 缺席。该窗口由 `_recover_interrupted_scenes`(revival.py,_load_scenes 入口调用)
    #   **补偿**:canonical 缺失时从 `.new`(完整新现场,优先)或 `.old`(完整旧现场)恢复。
    #   不变量:`.new` 仅在完整建满后才触发首个 rename → 任一崩溃点 {canonical,.new,.old}
    #   至少一个是完整现场、可恢复 → 现场永不丢失(审计 R16)。
    base = Path(workspace) / FAILED_REL
    scene_new = base / f".{key}.new"
    if scene_new.exists():
        shutil.rmtree(scene_new)
    scene_new.mkdir(parents=True, exist_ok=True)

    manifest = SceneManifest(
        key=key,
        ledger_key=ledger_key,
        failed_gate=failed_gate,
        findings=findings,
        engine_commit=engine_commit,
        candidate=candidate,
        md_path=str(md_path),
        analysis=analysis,
        attempts=[*prior_attempts, this_attempt],
    )
    (scene_new / "scene.json").write_text(
        json.dumps(asdict(manifest), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if staged_dir is not None and staged_dir.exists():
        for sub in ("ai", "person"):
            src = staged_dir / sub
            if src.exists():
                shutil.move(str(src), str(scene_new / sub))
        shutil.rmtree(staged_dir, ignore_errors=True)
    if content_bytes is not None:  # R3:从内存快照写回(源可能在旧 scene 内)
        (scene_new / "content_list.json").write_bytes(content_bytes)

    # 原子换入:旧 scene 先 rename 到 .old,新 scene rename 到位,再删 .old。
    scene_old = base / f".{key}.old"
    if scene_old.exists():
        shutil.rmtree(scene_old)
    if scene.exists():
        os.replace(str(scene), str(scene_old))  # 原子
    os.replace(str(scene_new), str(scene))  # 原子
    if scene_old.exists():
        shutil.rmtree(scene_old, ignore_errors=True)
    return scene
