# 终审修订层 实现计划 — ADR-0013

> **日期**: 2026-06-14
> **状态**: 草稿(设计经 `/mp-grill-me` 七题定稿;依据 ADR-0013)
> **作者**: Claude (Opus 4.8) + ShinewineW
> **基准版本**: `paper-rolling@main`(HEAD)
> **目的**: 落地一个**可选的、操作者触发的**「终审修订」层——一轮 `/loop` 跑完后,主会话用 Workflow 派每篇一个 Opus 子 agent,对已发布产物对照源 MD 做「修订或回炉」:小瑕疵直接外科修,无基底的(读错论文/整体胡说/重写级)降级到失败现场走 branch2 复活赛。把"机器门过了"提升到"最强模型确认/修订过了"。
> 范围: 引擎 `.claude/skills/paper-landscape/scripts/`(新增 `output/final_review.py` + `demote.py`,微调 `status.py`)+ 一个新的可选 skill / workflow 编排。**不改**双门 / 封印 / 发布的既有硬逻辑。

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** 给引擎加一个 ADR-0013 描述的「终审修订」可选收尾层:引擎侧两个纯函数模块(终审标记 `final_review.json` 的读写/批次扫描;已发布产物→失败现场的降级 `demote_to_scene`)+ status 的终审态surfacing + 一个主会话 Workflow 编排(逐篇 Opus agent 自改、机械回归、FAIL 走复活赛)。

**Architecture:** 引擎只提供**确定性纯函数**(标记、降级),与现有"纯核 + 注入 seam"一致;**非确定的修订判断**全在主会话派出的 Opus 子 agent 里(各自独立上下文)。账本/失败现场/复活赛只由主会话**串行**写(单写者 LS-1 不变量)。FAIL 复用 ADR-0007/0009 的复活赛(branch2 根 = 重分析)+ ADR-0011 的失败现场(ARA 留存)。

**Tech Stack:** Python 3.12 / pytest / ruff(引擎);Workflow 工具(JS 编排脚本)+ Agent 工具(逐篇 Opus 修订 agent)。

---

## 锁定的设计决策(grilling 七题定稿,实现须严格遵循)

1. **全文件可改**:子 agent 可改 `person_vault/<key>/report.md`(+ 重生 `report.html`)与 `ai_package/<key>/ara/` 全部文件。
2. **改了封印内容 → 信任 + 盖来源章,不重跑 G3**:写 `final_review.json`(verdict=revised + provenance),不重跑最终门;`passes_seal2` 布尔保持不动(provenance 说明它是终审前快照)。
3. **「度」= 基底 vs 瓦砾**,agent 自判,存疑偏 REVISE;FAIL **只**三类:① 读错论文 ② 整体胡说 ③ 重写级。
4. **FAIL → 走复活赛**:`demote_to_scene` 把已发布产物降级成 **branch2 根**失败现场 → `revive_all` **重新分析**(不复用坏 ARA)。
5. **REVISE 后跑纯机械回归**(`check_ara_bundle` + status 合规),**不是 LLM 验收**;挂了重试一次,再挂升级 FAIL。
6. **编排**:agent 各自上下文**自己改**(pin Opus + 高 effort);主会话只编排 + 收结构化结果 + 串行做账本/现场/复活赛。
7. **是验收层不是门**:可选、操作者触发、**不接进 `/loop`**;默认关。

---

## 文件结构(改动地图)

| 文件 | 职责 | 动作 |
|------|------|------|
| `.claude/skills/paper-landscape/scripts/output/final_review.py` | 终审标记 `final_review.json` 的读 / 写 / 批次扫描(纯确定性) | **新建** |
| `.claude/skills/paper-landscape/scripts/demote.py` | 已发布产物 → branch2 根失败现场 的降级(主会话串行调) | **新建** |
| `.claude/skills/paper-landscape/scripts/status.py` | `collect()` 每条记录加 `final_reviewed` 字段 + 卡片/JSON surfacing | **微调** |
| `tests/output/test_final_review.py` | Task 1 测试 | **新建** |
| `tests/test_demote.py` | Task 2 测试 | **新建** |
| `tests/test_status.py` | Task 3 测试(追加) | **追加** |
| `.claude/skills/paper-landscape/sub-skills/final-review.md` | 终审修订 skill:编排步骤 + 逐篇 agent prompt + 输出 schema | **新建** |
| `README.md` / `docs/INDEX.md` / `.claude/CLAUDE.md` | 文档同步(入口 + 治理登记 + 不变量) | **微调** |

**复用既有(不改)**:`failure_scene.write_scene`、`revival.revive_all`(branch2 根重分析)、`output/check_ara_bundle.check_bundle`、`output/branch1_llm._html`、`ledger.store.Ledger`、`engine_version.current_commit`、`status.{_report_compliant,_ara_sealed,_idbase}`。

---

## Chunk 1:引擎确定性支持(终审标记 + 降级)

### Task 1:终审标记模块 `final_review.py`

承载 ADR-0013 决策 #2(provenance)+ #5(幂等批次)。纯确定性、无 LLM、无网络。

**Files:**
- Create: `.claude/skills/paper-landscape/scripts/output/final_review.py`
- Test: `tests/output/test_final_review.py`

参考既有同目录文件的 import 风格(`output/check_ara_bundle.py` 用 `from __future__ import annotations` + `import json` + `from pathlib import Path`)。

- [ ] **Step 1:写失败测试** — `tests/output/test_final_review.py`

```python
from __future__ import annotations

import json
from pathlib import Path

from scripts.output.final_review import (
    is_reviewed,
    read_marker,
    unreviewed_compliant_keys,
    write_marker,
)


def _ara(tmp_path: Path, entry: str) -> Path:
    ara = tmp_path / "ai_package" / entry / "ara"
    ara.mkdir(parents=True)
    return ara


def test_write_then_read_marker_roundtrips(tmp_path: Path) -> None:
    ara = _ara(tmp_path, "2026-06-14_X_1111.11111")
    write_marker(ara, verdict="revised", edits=["report.md: 清掉思维链残留"], date="2026-06-14")
    assert is_reviewed(ara) is True
    m = read_marker(ara)
    assert m["verdict"] == "revised"
    assert m["by"] == "main-session-opus"
    assert m["date"] == "2026-06-14"
    assert m["edits"] == ["report.md: 清掉思维链残留"]
    # 落盘文件就在 ara/final_review.json
    assert json.loads((ara / "final_review.json").read_text(encoding="utf-8"))["verdict"] == "revised"


def test_clean_marker_has_no_edits(tmp_path: Path) -> None:
    ara = _ara(tmp_path, "2026-06-14_Y_2222.22222")
    write_marker(ara, verdict="clean", edits=[], date="2026-06-14")
    assert read_marker(ara)["verdict"] == "clean"
    assert read_marker(ara)["edits"] == []


def test_is_reviewed_false_when_absent(tmp_path: Path) -> None:
    ara = _ara(tmp_path, "2026-06-14_Z_3333.33333")
    assert is_reviewed(ara) is False
    assert read_marker(ara) is None


def test_write_marker_rejects_unknown_verdict(tmp_path: Path) -> None:
    import pytest

    ara = _ara(tmp_path, "2026-06-14_W_4444.44444")
    with pytest.raises(ValueError, match="verdict"):
        write_marker(ara, verdict="failed", edits=[], date="2026-06-14")  # FAIL 不写 marker


def test_unreviewed_compliant_keys_filters(tmp_path: Path, monkeypatch) -> None:
    # 批次 = 合规、且没有 final_review.json 的已发布产物。
    # compliant 判定打桩(避免在本单测里铺一整套 report/seal 夹具)。
    import scripts.output.final_review as fr

    compliant = {"1111.11111", "5555.55555"}  # 这两篇合规;6666 不合规
    monkeypatch.setattr(fr, "_compliant_idbases", lambda ws: compliant)
    _ara(tmp_path, "2026-06-14_A_1111.11111")  # 合规 + 无 marker  -> 入批
    b = _ara(tmp_path, "2026-06-14_B_5555.55555")  # 合规 + 有 marker -> 跳过
    write_marker(b, verdict="clean", edits=[], date="2026-06-14")
    _ara(tmp_path, "2026-06-14_C_6666.66666")  # 不合规 -> 不入批
    assert unreviewed_compliant_keys(tmp_path) == ["1111.11111"]
```

- [ ] **Step 2:跑测试确认失败**

Run: `uv run pytest tests/output/test_final_review.py -q`
Expected: FAIL(`ModuleNotFoundError: scripts.output.final_review`)。

- [ ] **Step 3:实现 `final_review.py`**

```python
# .claude/skills/paper-landscape/scripts/output/final_review.py
"""终审标记 final_review.json —— 终审修订层的 sidecar(ADR-0013 #2/#5)。

每个被终审过的已发布产物在 ai_package/<key>/ara/ 旁置一个 final_review.json:
  {date, verdict: clean|revised, by, edits}
双重用途:(1) REVISED 产物的 provenance(「G3 封印 → 终审修订」,使 passes_seal2 不再是对旧
内容的沉默断言);(2) 幂等键——下一轮终审跳过已带 marker 的产物。FAILED 产物不写 marker
(它会被降级 + 复活赛重分析 → 全新产物)。纯确定性,无 LLM/网络。
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

    verdict 必须是 clean|revised —— FAILED 不写 marker(降级走复活赛)。`date` 由调用方注入
    (引擎脚本里 Date.now 不可用的约定:时间戳一律外部传入)。
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
    """读终审标记;不存在或损坏返回 None。"""
    marker = Path(ara_dir) / MARKER_NAME
    if not marker.is_file():
        return None
    try:
        return json.loads(marker.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return None


def is_reviewed(ara_dir: Path) -> bool:
    """该产物是否已被终审(带有效 marker)。"""
    return read_marker(ara_dir) is not None


def _compliant_idbases(workspace: Path) -> set[str]:
    """合规产物的 idbase 集合 —— 复用 status 的内容判定(不重复造轮子)。"""
    from scripts.status import collect

    return {r["idbase"] for r in collect(Path(workspace)) if r["state"] == "compliant"}


def unreviewed_compliant_keys(workspace: Path) -> list[str]:
    """终审批次 = 合规、且尚未带 final_review.json 的已发布产物的 idbase(排序、确定)。"""
    from scripts.status import _idbase  # 函数级 import:回避 status<->final_review 的模块级循环依赖

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
```

- [ ] **Step 4:跑测试确认通过**

Run: `uv run pytest tests/output/test_final_review.py -q`
Expected: PASS(5 passed)。

- [ ] **Step 5:lint + 提交**

```bash
uv run ruff check .claude/skills/paper-landscape/scripts/output/final_review.py tests/output/test_final_review.py
git add .claude/skills/paper-landscape/scripts/output/final_review.py tests/output/test_final_review.py
git commit -m "feat(final-review): final_review.json marker (provenance + idempotency) for ADR-0013"
```

---

### Task 2:降级模块 `demote.py`(已发布产物 → branch2 根失败现场)

承载 ADR-0013 决策 #4。这是**新转换**:发布原本原子、从无"发布后打回"。`demote_to_scene` 把一个
已发布产物收进 `_failed/<idbase>/`、写成 **branch2 根**现场(`failed_gate="结构门"`、finding
`target="ara"`),并把账本记为 deferred(audit-block、无 TTL,等显式复活赛)。**只由主会话串行调**。

**Files:**
- Create: `.claude/skills/paper-landscape/scripts/demote.py`
- Test: `tests/test_demote.py`

> 关键依据(已核对源码):`failure_scene.write_scene(*, workspace, key, ledger_key, failed_gate,
> findings, engine_commit, candidate, md_path, content_list_path, analysis, staged_dir)` 会把
> `staged_dir/ai` 与 `staged_dir/person` **move** 进 `_failed/<key>/`。`revival._classify_roots`:
> finding `target=="ara"` → branch2 根;`revival._revive_one` 对非 ingest、非 `最终门`-branch1 的
> 现场走 `stage_branch2`(**重跑分析器**,不复用旧 ARA)。所以 `failed_gate="结构门"` + finding
> `target="ara"` 精确路由到"重分析"。

- [ ] **Step 1:写失败测试** — `tests/test_demote.py`

```python
from __future__ import annotations

import json
from pathlib import Path

import yaml

from scripts.demote import demote_to_scene


class _FakeLedger:
    """最小账本替身:记录 record() 调用 + 提供 latest key 查询。"""

    def __init__(self, rows: list[dict]) -> None:
        self._rows = rows
        self.recorded: list[dict] = []

    def entries(self) -> list[dict]:
        return self._rows

    def record(self, key: str, **kw) -> None:
        self.recorded.append({"key": key, **kw})


def _publish(tmp_path: Path, idbase: str, name: str) -> None:
    full = f"2026-06-14_{name}_{idbase}"
    ara = tmp_path / "ai_package" / full / "ara"
    ara.mkdir(parents=True)
    (ara / "PAPER.md").write_text(
        f"---\nkey: '{idbase}'\ntitle: {name}\ndoi: arXiv:{idbase}\n---\n# x\n", encoding="utf-8"
    )
    (ara / "src").mkdir()
    (ara / "src" / "code_ref.md").write_text("# Code Reference\n", encoding="utf-8")
    pv = tmp_path / "person_vault" / full
    pv.mkdir(parents=True)
    (pv / "report.md").write_text("# r\n\n## 评价\n> ok\n", encoding="utf-8")
    corpus = tmp_path / "corpus" / f"{idbase}_{name}"
    corpus.mkdir(parents=True)
    (corpus / f"{idbase}_{name}.md").write_text("# paper md\n", encoding="utf-8")
    (corpus / "content_list.json").write_text("[]", encoding="utf-8")


def test_demote_moves_products_to_branch2_scene_and_records_deferred(tmp_path: Path) -> None:
    _publish(tmp_path, "1111.11111", "Foo")
    led = _FakeLedger([{"key": "1111.11111", "status": "done"}])

    demote_to_scene(
        tmp_path, "1111.11111", ledger=led, category="读错论文", reason="正文讲的是另一篇"
    )

    # 现场建立 + branch2 根
    scene = tmp_path / "_failed" / "1111.11111"
    manifest = json.loads((scene / "scene.json").read_text(encoding="utf-8"))
    assert manifest["failed_gate"] == "结构门"
    assert manifest["findings"][0]["target"] == "ara"
    assert "读错论文" in manifest["findings"][0]["observation"]
    # 产物被收进现场(ai/ara + person/report)、原 vault 已清空
    assert (scene / "ai" / "ara" / "PAPER.md").exists()
    assert (scene / "person" / "report.md").exists()
    assert not (tmp_path / "ai_package" / "2026-06-14_Foo_1111.11111").exists()
    assert not (tmp_path / "person_vault" / "2026-06-14_Foo_1111.11111").exists()
    # candidate 从 PAPER.md frontmatter 还原
    assert manifest["candidate"]["arxiv_id"] == "1111.11111"
    # 账本记 deferred(无 TTL,等复活赛)
    assert led.recorded == [
        {"key": "1111.11111", "status": "deferred", "failure_class": "audit_block", "retry_after": None}
    ]


def test_demote_raises_when_product_missing(tmp_path: Path) -> None:
    import pytest

    led = _FakeLedger([])
    with pytest.raises(FileNotFoundError):
        demote_to_scene(tmp_path, "9999.99999", ledger=led, category="整体胡说", reason="x")
```

- [ ] **Step 2:跑测试确认失败**

Run: `uv run pytest tests/test_demote.py -q`
Expected: FAIL(`ModuleNotFoundError: scripts.demote`)。

- [ ] **Step 3:实现 `demote.py`**

> 注:`current_commit(workspace)` 在测试的 tmp_path(非 git)下会走其内部容错返回占位 hash —
> 与现有现场写入路径一致,无需特殊处理。`engine_version.current_commit` 已是 fail-soft。

```python
# .claude/skills/paper-landscape/scripts/demote.py
"""已发布产物 → 失败现场 的降级(ADR-0013 #4)。

终审修订判一篇为 FAIL(读错论文/整体胡说/重写级 = 无可信基底)时,把它从 vault 收回一个
**branch2 根**的失败现场,让复活赛**重新分析**(而非在坏 ARA 上重写报告)。这是发布之后唯一的
"打回"转换——发布本身仍是原子的。**只由主会话串行调**(写账本 = 单写者 LS-1;调用方须持锁)。
"""

from __future__ import annotations

import glob
import shutil
import tempfile
from pathlib import Path
from typing import Any

import yaml

from scripts.engine_version import current_commit
from scripts.failure_scene import write_scene
from scripts.status import _idbase


def _find_one(pattern: str) -> Path | None:
    hits = sorted(glob.glob(pattern))
    return Path(hits[0]) if hits else None


def _candidate_from_paper(ara: Path) -> dict:
    """从 ara/PAPER.md frontmatter 还原 candidate(title/arxiv_id/doi),口径同 reprocess 驱动。"""
    txt = (ara / "PAPER.md").read_text(encoding="utf-8")
    fm = yaml.safe_load(txt.split("---", 2)[1]) if txt.startswith("---") else {}
    fm = fm or {}
    doi = str(fm.get("doi") or "")
    arxiv = doi.replace("arXiv:", "") if doi.startswith("arXiv:") else (fm.get("key") or None)
    return {"title": fm.get("title") or ara.parent.name, "arxiv_id": arxiv, "doi": fm.get("doi")}


def _ledger_key_for(ledger: Any, idbase: str) -> str:
    """该 idbase 在账本里的 key(复活回写据此);默认就是 idbase。"""
    for row in ledger.entries():
        if isinstance(row, dict) and row.get("key") and _idbase(str(row["key"])) == idbase:
            return str(row["key"])
    return idbase


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
    """
    ws = Path(workspace)
    ai = _find_one(str(ws / "ai_package" / f"*_{idbase}"))
    pv = _find_one(str(ws / "person_vault" / f"*_{idbase}"))
    md = _find_one(str(ws / "corpus" / f"{idbase}_*" / f"{idbase}_*.md"))
    if ai is None or pv is None or md is None:
        raise FileNotFoundError(f"demote: missing product/MD for {idbase} (ai={ai}, pv={pv}, md={md})")
    ara = ai / "ara"
    candidate = _candidate_from_paper(ara)
    content_list = md.parent / "content_list.json"
    ledger_key = _ledger_key_for(ledger, idbase)

    # 组装 staged_dir:把已发布的 ai/person move 进临时结构(write_scene 再 move 进现场)。
    staged = Path(tempfile.mkdtemp(prefix="demote-stage-"))
    try:
        shutil.move(str(ai), str(staged / "ai"))  # staged/ai/ara/...  ← 与现场 ai/ 布局一致
        shutil.move(str(pv), str(staged / "person"))  # staged/person/report.md
        scene = write_scene(
            workspace=ws,
            key=idbase,
            ledger_key=ledger_key,
            failed_gate="结构门",  # + target=="ara" → branch2 根 → 复活赛重分析
            findings=[
                {
                    "target": "ara",
                    "observation": f"终审修订 FAIL({category}):{reason} —— 无可信基底,回炉重分析",
                }
            ],
            engine_commit=current_commit(ws),
            candidate=candidate,
            md_path=md,
            content_list_path=content_list if content_list.exists() else None,
            analysis=None,  # branch2 根从 MD 重分析,不复用旧 analysis
            staged_dir=staged,
        )
    finally:
        shutil.rmtree(staged, ignore_errors=True)

    ledger.record(ledger_key, status="deferred", failure_class="audit_block", retry_after=None)
    return scene
```

- [ ] **Step 4:跑测试确认通过**

Run: `uv run pytest tests/test_demote.py -q`
Expected: PASS(2 passed)。

- [ ] **Step 5:lint + 提交**

```bash
uv run ruff check .claude/skills/paper-landscape/scripts/demote.py tests/test_demote.py
git add .claude/skills/paper-landscape/scripts/demote.py tests/test_demote.py
git commit -m "feat(demote): demote published product to a branch2-root quarantine scene (ADR-0013 FAIL path)"
```

---

### Task 3:status 暴露终审态(轻量)

让 `scripts.status` 能一眼看出"哪些合规产物还没终审"。每条合规记录加 `final_reviewed` 布尔。

**Files:**
- Modify: `.claude/skills/paper-landscape/scripts/status.py`(在 `collect()` 末尾的 enrich 循环里加一字段;`render_card` 里加一行)
- Test: `tests/test_status.py`(追加)

- [ ] **Step 1:写失败测试** — 追加到 `tests/test_status.py`

```python
def test_collect_marks_final_reviewed(tmp_path: Path) -> None:
    # 合规产物带 final_review.json → final_reviewed True;不带 → False。
    from scripts.output.final_review import write_marker

    ws = tmp_path
    _compliant_pair(ws, "2026-01-01_A_1111.11111")  # 复用本文件已有的 helper
    _compliant_pair(ws, "2026-01-01_B_2222.22222")
    write_marker(ws / "ai_package" / "2026-01-01_A_1111.11111" / "ara",
                 verdict="clean", edits=[], date="2026-06-14")
    recs = {r["idbase"]: r for r in collect(ws)}
    assert recs["1111.11111"]["final_reviewed"] is True
    assert recs["2222.22222"]["final_reviewed"] is False
```

- [ ] **Step 2:跑测试确认失败**

Run: `uv run pytest tests/test_status.py::test_collect_marks_final_reviewed -q`
Expected: FAIL(`KeyError: 'final_reviewed'`)。

- [ ] **Step 3:实现** — 在 `status.py` 的 `collect()` enrich 循环(当前为 `for r in recs:` 设 `ledger`/`ledger_diverged` 那段)末尾,追加 `final_reviewed`:

OLD(`collect()` enrich 循环现状,锚点):
```python
        synced = led_status == "done" and not led_row.get("rescinded_at")
        r["ledger_diverged"] = r["state"] == "compliant" and not synced
    return recs
```
NEW:
```python
        synced = led_status == "done" and not led_row.get("rescinded_at")
        r["ledger_diverged"] = r["state"] == "compliant" and not synced
        # 终审态:合规产物是否已带 final_review.json(ADR-0013)。仅对成对产物有意义。
        from scripts.output.final_review import is_reviewed

        ai_dir = ai.get(r["idbase"])
        r["final_reviewed"] = bool(ai_dir and is_reviewed(ai_dir / "ara"))
    return recs
```
> 注:`ai` 是 `collect()` 里已构造的 `{idbase: Path(ai_package/<key>)}` 字典(见函数前半段);此处直接复用,无需重新 glob。

(可选 surfacing)在 `render_card` 的 funnel 行后加一行"终审 N/总数",非必须,留给实现者按版面决定。

- [ ] **Step 4:跑测试确认通过**

Run: `uv run pytest tests/test_status.py -q`
Expected: PASS(全绿,含新用例)。

- [ ] **Step 5:lint + 提交**

```bash
uv run ruff check .claude/skills/paper-landscape/scripts/status.py tests/test_status.py
git add .claude/skills/paper-landscape/scripts/status.py tests/test_status.py
git commit -m "feat(status): surface final_reviewed (终审态) per compliant product (ADR-0013)"
```

- [ ] **Step 6:全量回归**

Run: `uv run pytest -q && uv run ruff check .claude/skills/paper-landscape/scripts/ tests/`
Expected: 全绿 + All checks passed。

---

## Chunk 2:主会话编排(skill + workflow + 逐篇 agent 契约)

> 这部分是**主会话运行时**的编排(Workflow + Agent 工具),不是 pytest 单测对象。验证靠 Chunk 1
> 的引擎单测 + 一次**真实小批次烟测**(在一两篇已发布产物上跑通 CLEAN/REVISE/FAIL 三条路)。

### Task 4:逐篇终审 agent 的契约(prompt + 输出 schema)

定稿"喂给每个 Opus 子 agent"的修订契约。规则**蒸馏进 prompt**(agent 不需要对话史)。

- [ ] **Step 1:在 `sub-skills/final-review.md` 里固化输出 schema**

```json
{
  "idbase": "string",
  "verdict": "clean | revised | failed",
  "edits": ["string, 每条=改了哪个文件/要点(verdict=revised 时非空)"],
  "fail_category": "读错论文 | 整体胡说 | 重写级 | null(仅 verdict=failed 时填)",
  "fail_reason": "string | null(一句话,仅 failed)"
}
```

- [ ] **Step 2:固化逐篇 agent prompt 模板**(每个 agent 用,`{idbase}/{paths}` 注入)

```
你是对单篇已发布论文产物做「终审修订」的资深审稿人,用最强能力 + 怀疑精神。读盘,不信任何分数。
目的是【改,不是判】:小瑕疵你直接外科修;只有无可信基底时才判失败。定位是【修订,不是重写】。

论文: {idbase}
文件(绝对路径,全部可读可改):
- 源 MD(基底/ground truth,只读基准): {md_path}
- 人链报告: {report_md}   (+ 改完用引擎 _html 重生 {report_html})
- AI 知识库 ARA 目录: {ara_dir}  (PAPER.md / claims/ / evidence/ / src/code_ref.md / level2_report.json)

步骤:
1. 读源 MD + 人链报告 + ARA,逐项对照。
2. 判 verdict:
   - REVISE(默认,存疑偏这个): 论文身份对、整体方法叙事对,只是局部有错(数字、码链 prose、
     表格错位、漏旗标/漏图、内部矛盾、思维链残留、个别 claim 偏差)——【全文件可改,含 ARA 封印内容】,
     直接下笔外科修。改完 report.md 必须用引擎 _html 重生 report.html,完整模板(img_dir = report.md
     所在目录 = person_vault/<key>/,图片在其 images/ 下):
       PYTHONPATH=.claude/skills/paper-landscape python -c "
       import re; from pathlib import Path; from scripts.output.branch1_llm import _html
       d = Path('{report_md}').parent
       md = (d/'report.md').read_text('utf-8')
       t = re.search(r'^#\\s+(.+)$', md, re.M).group(1).strip()
       (d/'report.html').write_text(_html(t, md, d), encoding='utf-8')"
   - FAIL(只三类,确信才判): ① 读错论文(讲的是另一篇) ② 整体胡说(核心方法/claims 是编的、不在源文)
     ③ 重写级(现有产物是瓦砾不是基底,修=重写整段叙事)。FAIL 时【不改任何文件】,只返回判决。
   判据 = 「基底 vs 瓦砾」:能在站得住的基底上打补丁→REVISE;没有基底→FAIL。
3. 若 REVISE: 改完跑一道【纯机械回归】(不是验收):
   `PYTHONPATH=.claude/skills/paper-landscape python -m scripts.output.check_ara_bundle {ara_dir}`
   且确认 report.md 仍以 `## 评价` 开篇、无 `<!--ref/anchor-->`、无 ARA-未读入标记。
   - 通过 → 写终审标记: 调 `scripts.output.final_review.write_marker({ara_dir}, verdict="revised",
     edits=[...], date="{today}")`,返回 {verdict:"revised", edits:[...]}。
   - 挂了 → 说明改崩了(结构破损,非内容)→ 重试修一次;再挂 → 返回 {verdict:"failed",
     fail_category:"重写级", fail_reason:"机械回归无法通过"}(不写 marker)。
4. 若 CLEAN(无需改): 写标记 verdict="clean", edits=[],返回 {verdict:"clean"}。
5. 若 FAIL: 不改任何文件、不写 marker,返回 {verdict:"failed", fail_category, fail_reason}。

只返回上面 schema 的 JSON。你的编辑发生在你自己的上下文里;主会话只收这个 JSON。
```

> provenance(ADR-0013 #2):改了封印内容**不重跑 G3**;`final_review.json`(verdict=revised)即来源章,
> `passes_seal2` 布尔保持原值。这条写进 prompt 的"REVISE"说明里。

### Task 5:终审修订 skill 的编排(主会话 + Workflow)

- [ ] **Step 1:写 `sub-skills/final-review.md`** —— 编排步骤(主会话执行):

```
## 终审修订(可选,操作者一轮跑完后触发;默认关)

前置:不接进 /loop;需要主会话有强模型(Opus + 高 effort)。没有就跳过。

1. 定批次:默认
   `PYTHONPATH=.claude/skills/paper-landscape python -c "from scripts.output.final_review import
   unreviewed_compliant_keys; from pathlib import Path; print(unreviewed_compliant_keys(Path('.')))"`
   (合规 + 未终审的 idbase 列表);也可由操作者显式给一个 idbase 子集。空 → 直接结束。

2. 跑 Workflow(pipeline over 批次,每篇一个 agent):
   - 每个 `agent(...)` 用 Task 4 的 prompt + schema;**pin model=opus + 足够 effort**;
     不同篇只碰各自文件 → 并行安全(无需 worktree)。
   - agent 自己改 + 自跑机械回归 + 写 final_review.json(CLEAN/REVISED)或返回 FAILED。
   - 主会话只收每篇的结构化 JSON,**不载入论文全文**。

3. 主会话串行收尾(单写者 LS-1):对 verdict=="failed" 的每篇,持 LS-1 锁:
   - `demote_to_scene(ws, idbase, ledger=Ledger('.'), category=fail_category, reason=fail_reason)`
   - 全部降级完,在同一持锁段跑 `revive_all(...)` 重分析(branch2 根)→ 重封印 → 重发布;
     复活后的新产物**不带** final_review.json → 下一轮终审会再覆盖它。
   - REVISED/CLEAN 的篇:agent 已写好 marker,无需主会话动账本。

4. 收尾报告:CLEAN/REVISED/FAILED(→复活结果)各几篇 + status --card。
```

- [ ] **Step 2:把 demote + revival 的串行收尾固化成一个可调脚本(可选,降低编排出错)**

可在 `attn_sink/` 放一个一次性 driver(scratch),或直接由主会话按上面步骤手动编排。**不**新增引擎
CLI(保持引擎纯函数 + 主会话编排的分工)。

### Task 6:文档同步

- [ ] **Step 1:`README.md`** — 在"Entry points"加一条「终审修订(可选)」,注明默认关、操作者触发、不接进 /loop。
- [ ] **Step 2:`docs/INDEX.md`** — 在 `spec/` 现有文档表加本文件;ADR 区(自管理)已含 0013。
- [ ] **Step 3:`.claude/CLAUDE.md`** — 在"Non-obvious invariants"加一行:终审修订是**可选验收层、不接 /loop**;account/cost 守卫不破;agent 改内容、主会话碰账本。
- [ ] **Step 4:提交**

```bash
git add README.md docs/INDEX.md .claude/CLAUDE.md .claude/skills/paper-landscape/sub-skills/final-review.md
git commit -m "docs(final-review): skill orchestration + README/INDEX/CLAUDE/ADR-0013 wiring"
```

---

## 验证(DoD)

- Chunk 1:`uv run pytest -q` 全绿(含 test_final_review / test_demote / test_status 新用例)+ ruff 干净。
- Chunk 2:一次真实小批次烟测——挑 1 篇制造一个小瑕疵 → 终审应 REVISE 修好 + 写 marker + 机械回归过;
  (可选)挑 1 篇人为破坏成"读错论文" → 终审应 FAIL → demote → 复活赛重分析出新产物。
- 不变量复核:`/loop` 路径**完全不依赖**终审修订(headless 自动化不破);账本只主会话串行写;
  `check_ara_bundle` 27+/0;status 0 divergence。

## 关键风险与对策

- **agent 改崩文件**:Task 4 的机械回归(check_ara_bundle + 合规)挡住;再挂升级 FAIL。
- **并行 agent 抢账本**:设计上 agent **绝不**碰账本/现场/复活赛——只主会话串行做(LS-1)。
- **降级转换出错**(发布后打回是新路径):Task 2 的两条单测锁住"产物入现场 + 原 vault 清空 + branch2 根 + 账本 deferred";`write_scene` 的原子换入(`.new`/`.old`)保证现场不丢。
- **复活在坏 ARA 上重写**(最隐蔽):靠现场 `target="ara"`(branch2 根)强制重分析——Task 2 单测断言了 `findings[0].target=="ara"` + `failed_gate=="结构门"`。
