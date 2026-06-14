# .claude/skills/paper-landscape/scripts/output/final_review.py
"""终审标记 final_review.json —— 终审修订层的 sidecar(ADR-0013 #2/#5)。

每个被终审过的已发布产物,在 ai_package/<key>/ara/ 旁放一个 final_review.json:
  {date, verdict: clean|revised, by, edits}

双重用途:
  (1) provenance:REVISED 改了封印内容后不重跑 G3,此 marker 即来源章,
      使 passes_seal2 不再是对旧内容的沉默断言;
  (2) 幂等键:下一轮终审跳过已带 marker 的产物。

FAILED 产物不写 marker(降级 + 复活赛重分析 → 全新产物)。纯确定性,无 LLM/网络。
"""

from __future__ import annotations

import glob
import json
from pathlib import Path

MARKER_NAME = "final_review.json"
_VALID_VERDICTS = ("clean", "revised")
_BY = "main-session-opus"


def write_marker(ara_dir: Path, *, verdict: str, edits: list[str], date: str) -> Path:
    """写终审标记到 `<ara_dir>/final_review.json`,返回其路径。

    verdict 必须是 clean|revised —— FAILED 不写 marker(降级走复活赛)。
    `date` 由调用方注入(引擎脚本里 Date.now 不可用:时间戳一律外部传入)。
    """
    if verdict not in _VALID_VERDICTS:
        raise ValueError(f"verdict must be one of {_VALID_VERDICTS}, got {verdict!r}")
    marker = Path(ara_dir) / MARKER_NAME
    marker.write_text(
        json.dumps(
            {"date": date, "verdict": verdict, "by": _BY, "edits": list(edits)},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return marker


def read_marker(ara_dir: Path) -> dict | None:
    """读终审标记;不存在/损坏/非 dict(如 `[]`)返回 None。"""
    marker = Path(ara_dir) / MARKER_NAME
    if not marker.is_file():
        return None
    try:
        data = json.loads(marker.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return None
    return data if isinstance(data, dict) else None


def is_reviewed(ara_dir: Path) -> bool:
    """是否已被有效终审(marker 存在且 verdict 合法);{}/损坏 marker 视作未终审。"""
    m = read_marker(ara_dir)
    return bool(m and m.get("verdict") in _VALID_VERDICTS)


def _compliant_idbases(workspace: Path) -> set[str]:
    """合规产物的 idbase 集合 —— 复用 status 的内容判定(不重复造轮子)。

    不按 ledger_diverged 过滤:status 用文件系统 idbase 匹配账本行,DOI-only 产物的账本键是
    safe-keyed 裸 DOI(`_candidate_key`)、与文件系统的 `doi-<hash>` idbase 不一致,会被误判
    ledger_diverged=True 而漏掉(oh-my-review R6)。发散篇进批至多是白干(CLEAN/REVISE 的 marker
    会在 /loop 重处理时丢失),FAIL→demote 反而让账本收敛——都不破坏正确性。
    """
    from scripts.status import collect

    return {r["idbase"] for r in collect(Path(workspace)) if r["state"] == "compliant"}


def unreviewed_compliant_keys(workspace: Path) -> list[str]:
    """终审批次:合规且未带 final_review.json 的已发布产物 idbase(排序、确定)。"""
    from scripts.status import _idbase  # 函数级 import:回避 status→final_review 反向引用

    compliant = _compliant_idbases(workspace)
    out: list[str] = []
    for ai in sorted(glob.glob(str(Path(workspace) / "ai_package" / "*"))):
        d = Path(ai)
        if d.name.startswith("_"):
            continue
        ib = _idbase(d.name)
        if ib in compliant and not is_reviewed(d / "ara"):
            out.append(ib)
    return out
