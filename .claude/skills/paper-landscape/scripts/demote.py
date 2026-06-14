# .claude/skills/paper-landscape/scripts/demote.py
"""已发布产物 → 失败现场 的降级(ADR-0013 #4)。

终审修订判一篇为 FAIL(读错论文 / 整体胡说 / 重写级 = 无可信基底)时,把它从 vault
收回一个 **branch2 根**失败现场,让复活赛**重新分析**(而非在坏 ARA 上重写报告)。
这是发布之后唯一的"打回"转换——发布本身仍原子。**只由主会话串行调**(写账本 =
单写者 LS-1,调用方须持锁)。
"""

from __future__ import annotations

import glob
import json
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

import yaml

from scripts.audit.equation_fidelity import count_display_math_blocks
from scripts.engine_version import current_commit
from scripts.failure_scene import FAILED_REL, write_scene
from scripts.hub import _candidate_key
from scripts.paths import FAILURE_AUDIT_BLOCK


def _find_one(pattern: str) -> Path | None:
    hits = sorted(glob.glob(pattern))
    return Path(hits[0]) if hits else None


def _find_corpus_md(ws: Path, idbase: str) -> Path | None:
    """corpus 目录名是 `{arxiv_id}{version}_{Name}` 或 `{doi-hash}_{Name}`(ingest 口径),
    arXiv 带版本(v2 等)时 `{idbase}_*` glob 会漏 → 用正则匹配 idbase + 可选版本 + `_`。"""
    pat = re.compile(rf"^{re.escape(idbase)}(v\d+)?_")
    for d in sorted(glob.glob(str(ws / "corpus" / "*"))):
        dp = Path(d)
        if dp.is_dir() and pat.match(dp.name):
            md = dp / f"{dp.name}.md"
            if md.exists():
                return md
    return None


def _candidate_from_paper(ara: Path) -> dict:
    """从 ara/PAPER.md frontmatter 还原 revival 需要的 candidate 字段。

    复活赛 write_branch2(经 stage_branch2)以**下标**取 candidate["title"]/["year"](必填),
    其余 .get(authors/venue/doi/arxiv_id)。故 year 必须始终在字典里(缺则 None,渲染为 null,
    不 KeyError)。arxiv_id 只接受真 arXiv id(YYMM.NNNNN)或 None —— 绝不把裸 DOI 放进
    arxiv_id,否则 identity_base/vault_key 会把它当身份基,DOI-only 论文复活会改键。
    """
    txt = (ara / "PAPER.md").read_text(encoding="utf-8")
    fm = yaml.safe_load(txt.split("---", 2)[1]) if txt.startswith("---") else {}
    fm = fm or {}
    doi = str(fm.get("doi") or "")
    arxiv_id = doi[len("arXiv:") :] if doi.startswith("arXiv:") else None
    if arxiv_id is None:
        key = str(fm.get("key") or "")
        arxiv_id = key if re.fullmatch(r"\d{4}\.\d{4,5}", key) else None
    return {
        "title": fm.get("title") or ara.parent.name,
        "arxiv_id": arxiv_id,
        "doi": fm.get("doi"),
        "year": fm.get("year"),
        "authors": list(fm.get("authors") or []),
        "venue": fm.get("venue"),
    }


def _ensure_content_list(md: Path) -> Path:
    """corpus 缺 content_list.json 时按 tier-1 同款合成 count-parity 版本并返回其路径。

    复活赛的 G3 equation 门会无条件读 `scene/content_list.json`(revival 传现场原值给
    run_g3),缺它会 FileNotFoundError 兜成 error、不重分析。MD 已在 ingest 过门、此处只
    重分析不重转换,故按 MD 的 $$ 块数造等量 equation 条目(与引擎 tier-1 合成口径一致)。
    """
    cl = md.with_name("content_list.json")
    if not cl.exists():
        n = count_display_math_blocks(md.read_text(encoding="utf-8"))
        cl.write_text(json.dumps([{"type": "equation"} for _ in range(n)]), encoding="utf-8")
    return cl


def demote_to_scene(
    workspace: Path,
    idbase: str,
    *,
    ledger: Any,
    category: str,
    reason: str,
) -> Path:
    """把已发布产物 idbase 降级成 branch2 根失败现场,账本记 deferred。返回现场目录。

    Raises:
        FileNotFoundError: 找不到该 idbase 的已发布产物 / 源 MD。
        FileExistsError: 该 vault key 已有 `_failed/` 现场(demote 是建、不是 append)。
    """
    ws = Path(workspace)
    ai = _find_one(str(ws / "ai_package" / f"*_{idbase}"))
    pv = _find_one(str(ws / "person_vault" / f"*_{idbase}"))
    md = _find_corpus_md(ws, idbase)  # 版本感知:arXiv `{id}v2_*` 也能命中
    if ai is None or pv is None or md is None:
        raise FileNotFoundError(
            f"demote: missing product/MD for {idbase} (ai={ai}, pv={pv}, md={md})"
        )
    ara = ai / "ara"
    candidate = _candidate_from_paper(ara)
    scene_key = ai.name  # 现场名 = vault key(同 _g3_to_scene;ledger_key 仍 idbase)
    if (ws / FAILED_REL / scene_key).exists():
        # demote 是「建」不是「append」:write_scene 撞名会把产物并进既有现场(那是复活再失败
        # 的语义),故撞名直接 fail-loud,先让操作者解决既有现场。
        raise FileExistsError(
            f"demote: a _failed scene already exists for {scene_key}; resolve/revive it first"
        )
    content_list = _ensure_content_list(md)  # 复活赛 G3 需现场恒有 content_list.json
    ledger_key = _candidate_key(candidate)  # 与 hub 同口径还原账本键(DOI-only 也对)
    observation = f"终审修订 FAIL({category}):{reason} —— 无可信基底,回炉重分析"

    # 组装 staged_dir(write_scene 会把 ai/person move 进现场)。关键(审计 R15 / ADR-0011):
    # 临时目录必须落在 workspace/_failed/ 内(gitignored),不是系统 /tmp —— 同 _g3_to_scene。
    # 不包 try/finally:write_scene 成功时自己消费 staged;失败时把 staged 留在
    # _failed/.scene-*(产物在内、可恢复)、异常上抛。绝不在 finally 里 rmtree(staged)——
    # 那会在 write_scene 失败时把已 move 出 vault 的产物一起删掉(原 vault 也已空 → 永久丢失)。
    (ws / FAILED_REL).mkdir(parents=True, exist_ok=True)
    staged = Path(tempfile.mkdtemp(dir=str(ws / FAILED_REL), prefix=".scene-"))
    shutil.move(str(ai), str(staged / "ai"))  # staged/ai/ara/...  ← 与现场 ai/ 布局一致
    shutil.move(str(pv), str(staged / "person"))  # staged/person/report.md
    scene = write_scene(
        workspace=ws,
        key=scene_key,
        ledger_key=ledger_key,
        failed_gate="结构门",  # + target=="ara" → branch2 根 → 复活赛重分析
        findings=[{"target": "ara", "observation": observation}],
        engine_commit=current_commit(ws),
        candidate=candidate,
        md_path=md,
        content_list_path=content_list,
        analysis=None,  # branch2 根从 MD 重分析,不复用旧 analysis
        staged_dir=staged,
    )
    ledger.record(
        ledger_key, status="deferred", failure_class=FAILURE_AUDIT_BLOCK, retry_after=None
    )
    return scene
