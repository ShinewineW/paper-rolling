# 终审修订层 实现计划 — ADR-0013

> **日期**: 2026-06-14
> **状态**: 已归档(设计已落地并合并;ADR-0013 终审层已对全部 33 篇语料执行完毕 — 见 README 现状段)
> **作者**: Claude (Opus 4.8) + ShinewineW
> **基准版本**: `paper-rolling@main`(HEAD)
> **目的**: 落地一个**可选的、操作者触发的**「终审修订」层——一轮 `/loop` 跑完后,主会话用 Workflow 派每篇一个 Opus 子 agent,对已发布产物对照源 MD 做「修订或回炉」:小瑕疵直接外科修,无基底的(读错论文/整体胡说/重写级)降级到失败现场走 branch2 复活赛。把"机器门过了"提升到"最强模型确认/修订过了"。
> 范围: 引擎 `.claude/skills/paper-landscape/scripts/`(新增 `output/final_review.py` + `demote.py`,微调 `status.py`)+ 一个新的可选 skill / workflow 编排。**不改**双门 / 封印 / 发布的既有硬逻辑。

> **For agentic workers:** REQUIRED SUB-SKILL: use the `subagent-driven-development` skill (this session's name — no `superpowers:` prefix) to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** 给引擎加一个 ADR-0013 描述的「终审修订」可选收尾层:引擎侧两个纯函数模块(终审标记 `final_review.json` 的读写/批次扫描;已发布产物→失败现场的降级 `demote_to_scene`)+ status 的终审态surfacing + 一个主会话 Workflow 编排(逐篇 Opus agent 自改、机械回归、FAIL 走复活赛)。

**Architecture:** 引擎只提供**确定性纯函数**(标记、降级),与现有"纯核 + 注入 seam"一致;**非确定的修订判断**全在主会话派出的 Opus 子 agent 里(各自独立上下文)。账本/失败现场/复活赛只由主会话**串行**写(单写者 LS-1 不变量)。FAIL 复用 ADR-0007/0009 的复活赛(branch2 根 = 重分析)+ ADR-0011 的失败现场(ARA 留存)。

**Tech Stack:** Python 3.11+ / pytest / ruff(引擎,`line-length=100`,**E501 按显示宽度计** ⇒ CJK 字符算 2 列)+ Workflow 工具(JS 编排脚本)+ Agent 工具(逐篇 Opus 修订 agent)。

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
| `.claude/skills/paper-landscape/scripts/demote.py` | 已发布产物 → branch2 根失败现场 的降级(主会话串行调;账本键还原复用 `hub._candidate_key`) | **新建** |
| `.claude/skills/paper-landscape/scripts/revival.py` | `revive_all` 加向后兼容 `only_keys` 范围参数(终审 FAIL 只复活本批,不碰既有积压) | **微调** |
| `.claude/skills/paper-landscape/scripts/status.py` | `collect()` 每条记录加 `final_reviewed` 字段 + 卡片/JSON surfacing | **微调** |
| `tests/output/test_final_review.py` | Task 1 测试 | **新建** |
| `tests/test_demote.py` | Task 2 测试 | **新建** |
| `tests/test_revival.py` | Task 2b 测试(追加) | **追加** |
| `tests/test_status.py` | Task 3 测试(追加) | **追加** |
| `.claude/skills/paper-landscape/sub-skills/final-review/SKILL.md` | 终审修订 sub-skill(**目录 + `SKILL.md` + YAML frontmatter `name`/`description`**,同 `g2-skeptic`/`g3-rigor-reviewer` 等既有 sub-skill 约定):编排步骤 + 逐篇 agent prompt + 输出 schema | **新建** |
| `README.md` / `docs/INDEX.md` / `.claude/CLAUDE.md` | 文档同步(入口 + 治理登记 + 不变量) | **微调** |

**复用既有(不改)**:`failure_scene.write_scene`、`output/check_ara_bundle.check_bundle`、`output/branch1_llm._html`、`ledger.store.Ledger`、`engine_version.current_commit`、`hub._candidate_key`(账本键口径)、`audit.equation_fidelity.count_display_math_blocks`、`status.{collect,_report_compliant,_ara_sealed,_idbase}`。`revival.revive_all` 仅加一个向后兼容的 `only_keys` 可选参数(Task 2b),其 branch2 重分析硬逻辑不动。

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
    data = json.loads((ara / "final_review.json").read_text(encoding="utf-8"))
    assert data["verdict"] == "revised"


def test_clean_marker_has_no_edits(tmp_path: Path) -> None:
    ara = _ara(tmp_path, "2026-06-14_Y_2222.22222")
    write_marker(ara, verdict="clean", edits=[], date="2026-06-14")
    assert read_marker(ara)["verdict"] == "clean"
    assert read_marker(ara)["edits"] == []


def test_is_reviewed_false_when_absent(tmp_path: Path) -> None:
    ara = _ara(tmp_path, "2026-06-14_Z_3333.33333")
    assert is_reviewed(ara) is False
    assert read_marker(ara) is None


def test_is_reviewed_false_for_empty_or_invalid_marker(tmp_path: Path) -> None:
    # 非阻断:{}/verdict 非法/非 dict 的 marker 不得算"已终审"(坏写入不能永久跳过该篇)。
    ara = _ara(tmp_path, "2026-06-14_V_7777.77777")
    for bad in ("{}", '{"verdict": "bogus"}', "[]", "[1, 2]"):
        (ara / "final_review.json").write_text(bad, encoding="utf-8")
        assert is_reviewed(ara) is False
    # 非 dict JSON 经 read_marker 归一为 None(is_reviewed 不会对 list 调 .get → 不崩)
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
```

- [ ] **Step 4:跑测试确认通过**

Run: `uv run pytest tests/output/test_final_review.py -q`
Expected: PASS(6 passed)。

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
>
> 两个易踩点(本计划据源码补正,审阅确认):
> 1. **staging 必须落在 `workspace/_failed/` 内,不是系统 `/tmp`** —— 与 `spoke._g3_to_scene`
>    同款(审计 R15 / ADR-0011)。demote 先把已发布 ARA `move` 进 staging;若 `move`→`write_scene`
>    之间崩溃,放 `/tmp` 会让这份 token 贵的 ARA 滞留在现场恢复(`_recover_interrupted_scenes`
>    只扫 `_failed/`)扫不到的地方、而原 vault 目录已被 move 走、ledger 仍是旧 `done` → 下个 tick 的
>    `consistency_check` 把行降级 `convert_error`,论文 + ARA **永久丢失**。故 staging 用
>    `tempfile.mkdtemp(dir=str(ws / FAILED_REL), prefix=".scene-")`。
> 2. **复活赛重分析有 READINESS 前置**:`revival._revive_one` 在路由前先跑
>    `corpus_readiness_problems(md_path)`,corpus 的 `images/`(gitignored)缺失/不全时**直接判
>    `manual`(需 re-ingest)、不重分析**。本机 images 在场,烟测可过;跨机 / 纯 checkout 须先确认
>    corpus images 完整(见 Task 5 前置 + DoD)。

- [ ] **Step 1:写失败测试** — `tests/test_demote.py`

```python
from __future__ import annotations

import json
from pathlib import Path

from scripts.demote import _candidate_from_paper, demote_to_scene


class _FakeLedger:
    """最小账本替身:只记录 record() 调用(demote 用 _candidate_key 还原键,不查账本)。"""

    def __init__(self) -> None:
        self.recorded: list[dict] = []

    def record(self, key: str, **kw) -> None:
        self.recorded.append({"key": key, **kw})


def _publish(
    tmp_path: Path, idbase: str, name: str, *, doi: str | None = None, version: str = ""
) -> None:
    full = f"2026-06-14_{name}_{idbase}"
    ara = tmp_path / "ai_package" / full / "ara"
    ara.mkdir(parents=True)
    doi_line = f"doi: {doi}\n" if doi else f"doi: arXiv:{idbase}\n"
    (ara / "PAPER.md").write_text(
        f"---\nkey: '{idbase}'\ntitle: {name}\nyear: 2024\nauthors:\n- A. Author\n"
        f"{doi_line}---\n# x\n",
        encoding="utf-8",
    )
    (ara / "src").mkdir()
    (ara / "src" / "code_ref.md").write_text("# Code Reference\n", encoding="utf-8")
    pv = tmp_path / "person_vault" / full
    pv.mkdir(parents=True)
    (pv / "report.md").write_text("# r\n\n## 评价\n> ok\n", encoding="utf-8")
    cdir = f"{idbase}{version}_{name}"  # ingest 口径:arXiv 带版本 → {id}{version}_{Name}
    corpus = tmp_path / "corpus" / cdir
    corpus.mkdir(parents=True)
    (corpus / f"{cdir}.md").write_text("# paper md\n", encoding="utf-8")
    (corpus / "content_list.json").write_text("[]", encoding="utf-8")


def test_demote_moves_products_to_branch2_scene_and_records_deferred(tmp_path: Path) -> None:
    _publish(tmp_path, "1111.11111", "Foo")
    led = _FakeLedger()

    demote_to_scene(
        tmp_path, "1111.11111", ledger=led, category="读错论文", reason="正文讲的是另一篇"
    )

    # 现场建立 + branch2 根(现场名 = vault key,同 _g3_to_scene 约定)
    scene = tmp_path / "_failed" / "2026-06-14_Foo_1111.11111"
    manifest = json.loads((scene / "scene.json").read_text(encoding="utf-8"))
    assert manifest["failed_gate"] == "结构门"
    assert manifest["findings"][0]["target"] == "ara"
    assert "读错论文" in manifest["findings"][0]["observation"]
    # 产物被收进现场(ai/ara + person/report)、原 vault 已清空
    assert (scene / "ai" / "ara" / "PAPER.md").exists()
    assert (scene / "person" / "report.md").exists()
    assert not (tmp_path / "ai_package" / "2026-06-14_Foo_1111.11111").exists()
    assert not (tmp_path / "person_vault" / "2026-06-14_Foo_1111.11111").exists()
    # candidate 带齐 write_branch2._paper_md 需要的字段(title/year 是必填下标)
    cand = manifest["candidate"]
    assert cand["arxiv_id"] == "1111.11111"
    assert cand["year"] == 2024
    assert cand["title"] == "Foo"
    assert cand["authors"] == ["A. Author"]
    # 账本记 deferred(无 TTL,等复活赛);键 = _candidate_key(candidate)
    assert led.recorded == [
        {
            "key": "1111.11111",
            "status": "deferred",
            "failure_class": "audit_block",
            "retry_after": None,
        }
    ]


def test_demote_doi_only_records_under_safe_keyed_ledger_key(tmp_path: Path) -> None:
    # B2:DOI-only 产物记账本须用 _candidate_key(safe-keyed 裸 DOI),不是 doi-hash idbase。
    _publish(tmp_path, "doi-1a2b3c4d", "Qux", doi="10.1234/qux")
    led = _FakeLedger()
    demote_to_scene(tmp_path, "doi-1a2b3c4d", ledger=led, category="整体胡说", reason="编的")
    assert led.recorded[0]["key"] == "10.1234_qux"  # 同 hub._candidate_key


def test_demote_finds_versioned_corpus_md(tmp_path: Path) -> None:
    # B1(R6):arXiv 带版本的 corpus(`{id}v2_Name`)也要能被找到,否则 FAIL 路径起不来。
    _publish(tmp_path, "2401.00001", "Foo", version="v2")
    led = _FakeLedger()
    scene = demote_to_scene(tmp_path, "2401.00001", ledger=led, category="读错论文", reason="x")
    assert (scene / "scene.json").exists()
    assert led.recorded[0]["key"] == "2401.00001"


def test_demote_raises_when_product_missing(tmp_path: Path) -> None:
    import pytest

    led = _FakeLedger()
    with pytest.raises(FileNotFoundError):
        demote_to_scene(tmp_path, "9999.99999", ledger=led, category="整体胡说", reason="x")


def test_demote_candidate_doi_only_keeps_arxiv_id_none(tmp_path: Path) -> None:
    # Final 轮:DOI-only 产物不得把裸 DOI 放进 arxiv_id(identity_base 会把任何非空 arxiv_id
    # 当身份基 → 复活改键)。也确认 year 被还原(write_branch2 必填)。
    full = "2026-06-14_Qux_doi-1a2b3c4d"
    ara = tmp_path / "ai_package" / full / "ara"
    ara.mkdir(parents=True)
    (ara / "PAPER.md").write_text(
        "---\nkey: 'doi-1a2b3c4d'\ntitle: Qux\nyear: 2023\ndoi: 10.1234/qux\n---\n# x\n",
        encoding="utf-8",
    )
    c = _candidate_from_paper(ara)
    assert c["arxiv_id"] is None
    assert c["doi"] == "10.1234/qux"
    assert c["year"] == 2023


def test_demote_synthesizes_content_list_when_corpus_lacks_it(tmp_path: Path) -> None:
    # F3:corpus 缺 content_list.json 的产物也必须降级出带 content_list.json 的现场
    # (复活赛 G3 的 equation 门要读它),并就地补回 corpus。
    _publish(tmp_path, "2222.22222", "Bar")
    (tmp_path / "corpus" / "2222.22222_Bar" / "content_list.json").unlink()
    led = _FakeLedger()
    scene = demote_to_scene(tmp_path, "2222.22222", ledger=led, category="整体胡说", reason="编的")
    assert (scene / "content_list.json").exists()
    assert (tmp_path / "corpus" / "2222.22222_Bar" / "content_list.json").exists()


def test_demote_preserves_products_under_failed_if_write_scene_raises(
    tmp_path: Path, monkeypatch
) -> None:
    # F2 数据安全:write_scene 在 move 之后抛错时,产物必须留存于 _failed/(可恢复),
    # 绝不被 finally 清理删掉;ledger 不前进(record 仅在 write_scene 成功后执行)。
    import pytest

    _publish(tmp_path, "3333.33333", "Baz")
    led = _FakeLedger()

    def _boom(**kw):
        raise RuntimeError("write_scene blew up after the moves")

    monkeypatch.setattr("scripts.demote.write_scene", _boom)
    with pytest.raises(RuntimeError):
        demote_to_scene(tmp_path, "3333.33333", ledger=led, category="重写级", reason="x")
    assert not (tmp_path / "ai_package" / "2026-06-14_Baz_3333.33333").exists()
    survivors = list((tmp_path / "_failed").rglob("PAPER.md"))
    assert survivors, "products must survive under _failed/ when write_scene fails"
    assert led.recorded == []
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

    write_branch2._paper_md 以**下标**取 candidate["title"] 与 candidate["year"](必填),
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
```

- [ ] **Step 4:跑测试确认通过**

Run: `uv run pytest tests/test_demote.py -q`
Expected: PASS(7 passed)。

- [ ] **Step 5:lint + 提交**

```bash
uv run ruff check .claude/skills/paper-landscape/scripts/demote.py tests/test_demote.py
git add .claude/skills/paper-landscape/scripts/demote.py tests/test_demote.py
git commit -m "feat(demote): demote published product to a branch2-root quarantine scene (ADR-0013 FAIL path)"
```

---

### Task 2b:`revival.py` 加 `only_keys` 复活范围(微调,终审 FAIL 只复活本批)

承载 oh-my-review Round-5 阻断:`revive_all` 跑 `_load_scenes` **全量** `_failed/`,终审 FAIL 调它会
顺带把 `_failed/` 里**无关的既有积压**也复活(scope 越界,可能改写操作者没打算碰的失败篇)。加一个
**向后兼容**的 `only_keys` 限定——默认 `None` = 全量(既有调用方 / 14+ 既有测试行为不变)。

**Files:**
- Modify: `.claude/skills/paper-landscape/scripts/revival.py`(`revive_all` 加 `only_keys` 参数 + 循环过滤)
- Test: `tests/test_revival.py`(追加 1 例)

- [ ] **Step 1:写失败测试** — 追加到 `tests/test_revival.py`

```python
def test_revive_all_only_keys_scopes_to_subset(tmp_path, monkeypatch):
    # only_keys 限定后,_load_scenes 里不在集合内的现场被跳过(本批 FAIL 不碰无关积压)。
    import scripts.revival as rv

    seen: list[str] = []
    monkeypatch.setattr(rv, "_load_scenes", lambda ws: [
        (tmp_path / "_failed" / "A", {"ledger_key": "A", "failed_gate": "结构门"}),
        (tmp_path / "_failed" / "B", {"ledger_key": "B", "failed_gate": "结构门"}),
    ])
    monkeypatch.setattr(rv, "_run_revive_guarded", lambda ws, sd, mf, *a, **k: (
        seen.append(sd.name) or rv.RevivalResult(sd.name, mf["ledger_key"], "done", "结构门")))
    res = rv.revive_all(workspace=tmp_path, ledger=object(), seams={}, only_keys={"B"})
    assert seen == ["B"] and [r.key for r in res] == ["B"]
```

- [ ] **Step 2:跑测试确认失败** — `uv run pytest tests/test_revival.py::test_revive_all_only_keys_scopes_to_subset -q`(`TypeError: unexpected keyword 'only_keys'`)。

- [ ] **Step 3:实现** — `revive_all` 签名末尾加 `only_keys: set[str] | None = None`,循环首行加过滤:

OLD(锚点):
```python
    results: list[RevivalResult] = []
    for scene_dir, manifest in _load_scenes(workspace):
        try:
```
NEW:
```python
    results: list[RevivalResult] = []
    for scene_dir, manifest in _load_scenes(workspace):
        if only_keys is not None and scene_dir.name not in only_keys:
            continue  # 不在本批范围,跳过(默认 None = 全量,既有调用方行为不变)
        try:
```
docstring 补一句:`only_keys`:仅重放现场名在此集合内的篇(终审 FAIL 只复活本批降级的产物,不碰
`_failed/` 既有无关积压);None = 全量(既有行为)。

- [ ] **Step 4:跑测试 + 提交**

```bash
uv run pytest tests/test_revival.py -q
uv run ruff check .claude/skills/paper-landscape/scripts/revival.py tests/test_revival.py
git add .claude/skills/paper-landscape/scripts/revival.py tests/test_revival.py
git commit -m "feat(revival): optional only_keys to scope revive_all to a subset (ADR-0013 terminal-review batch)"
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

- [ ] **Step 3:实现** — 在 `status.py` 的 `collect()` enrich 循环里给每条记录加 `final_reviewed`。`is_reviewed` 的函数级 import 提到循环**外**(只 import 一次,不在 `for` 体内逐条执行)。

3a. 把 import 放在 enrich 循环之前(锚点 = `for r in recs:` 那行):

OLD:
```python
    for r in recs:  # enrich with the engine's own recorded status (latest ledger row)
        led_row = led.get(r["idbase"]) or {}
```
NEW:
```python
    # 终审态(ADR-0013):合规产物是否已带 final_review.json。函数级 import 提到循环外,
    # 既避开 status↔final_review 的模块级耦合,又不在 for 体内逐条 import。
    from scripts.output.final_review import is_reviewed

    for r in recs:  # enrich with the engine's own recorded status (latest ledger row)
        led_row = led.get(r["idbase"]) or {}
```

3b. 在同一循环末尾(`r["ledger_diverged"] = ...` 之后)追加两行:

OLD(锚点):
```python
        synced = led_status == "done" and not led_row.get("rescinded_at")
        r["ledger_diverged"] = r["state"] == "compliant" and not synced
    return recs
```
NEW:
```python
        synced = led_status == "done" and not led_row.get("rescinded_at")
        r["ledger_diverged"] = r["state"] == "compliant" and not synced
        ai_dir = ai.get(r["idbase"])  # 仅成对产物有 ai 目录;失败/孤儿/待入库为 None
        r["final_reviewed"] = bool(ai_dir and is_reviewed(ai_dir / "ara"))
    return recs
```
> 注:`ai` 是 `collect()` 里已构造的 `{idbase: Path(ai_package/<key>)}` 字典(见函数前半段);此处直接复用,无需重新 glob。`is_reviewed` 在循环外只 import 一次。

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

- [ ] **Step 1:在 `sub-skills/final-review/SKILL.md` 里固化输出 schema**

```json
{
  "idbase": "string",
  "verdict": "clean | revised | failed",
  "edits": ["string, 每条=改了哪个文件/要点(verdict=revised 时非空)"],
  "fail_category": "读错论文 | 整体胡说 | 重写级 | null(仅 verdict=failed 时填)",
  "fail_reason": "string | null(一句话,仅 failed)"
}
```

- [ ] **Step 2:固化逐篇 agent prompt 模板**(每个 agent 用;注入变量:`{idbase}`、`{md_path}`、`{report_md}`、`{report_html}`、`{ara_dir}`、`{today}` —— 其中 `{today}` 由主会话/编排注入当天日期(如 `2026-06-14`),引擎脚本与 Workflow 脚本都**不可**用 `Date.now`/`new Date()`)

```
你是对单篇已发布论文产物做「终审修订」的资深审稿人,用最强能力 + 怀疑精神。读盘,不信任何分数。
目的是【改,不是判】:小瑕疵你直接外科修;只有无可信基底时才判失败。定位是【修订,不是重写】。

论文: {idbase}
文件(绝对路径,全部可读可改):
- 源 MD(基底/ground truth,只读基准): {md_path}
- 人链报告: {report_md}   (+ 改完用引擎 _html 重生 {report_html})
- AI 知识库 ARA 目录: {ara_dir}  真实布局(已核对):
    · PAPER.md（元数据 frontmatter）
    · logic/  → claims.md(论断)、concepts.md、experiments.md、problem.md、related_work.md、solution/
    · evidence/tables/  → 数字证据表(.md)
    · src/code_ref.md  → 码链三态指针
    · trace/、AUDIT_FLAGS.md、level2_report.json（封印报告，含 passes_seal2）
  （没有顶层 claims/ 目录——claims.md 在 logic/ 下;动手前先 `ls {ara_dir}` 核对）

步骤:
1. 读源 MD + 人链报告 + ARA,逐项对照。
2. 判 verdict:
   - REVISE(默认,存疑偏这个): 论文身份对、整体方法叙事对,只是局部有错(数字、码链 prose、
     表格错位、漏旗标/漏图、内部矛盾、思维链残留、个别 claim 偏差)——【全文件可改,含 ARA 封印内容】,
     直接下笔外科修。改完 report.md 必须用引擎 _html 重生 report.html(img_dir = report.md
     所在目录 = person_vault/<key>/,图片在其 images/ 下)。用 `uv run python`(裸 `python` 不在
     PATH);标题取首个 `# ` H1,取不到则退回目录名(别让 .group 在无 H1 时崩)。**必须单行
     `-c`**(多行缩进体会触发 IndentationError):
       PYTHONPATH=.claude/skills/paper-landscape uv run python -c "import re; from pathlib import Path; from scripts.output.branch1_llm import _html; d=Path('{report_md}').parent; md=(d/'report.md').read_text('utf-8'); m=re.search(r'^#\\s+(.+)$', md, re.M); t=(m.group(1).strip() if m else d.name); (d/'report.html').write_text(_html(t, md, d), encoding='utf-8')"
   - FAIL(只三类,确信才判): ① 读错论文(讲的是另一篇) ② 整体胡说(核心方法/claims 是编的、不在源文)
     ③ 重写级(现有产物是瓦砾不是基底,修=重写整段叙事)。FAIL 时【不改任何文件】,只返回判决。
   判据 = 「基底 vs 瓦砾」:能在站得住的基底上打补丁→REVISE;没有基底→FAIL。
3. 若 REVISE: 改完跑【纯机械回归】(决策 #5,不是 LLM 验收)——**两道都要过**:
   (a) ARA bundle 结构:
       `PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.output.check_ara_bundle {ara_dir}`
   (b) status 合规(权威判定——覆盖 报告合规 + ARA 封印 `passes_seal2` + 非 corrupt;`check_ara_bundle`
       不查这些。单行 `-c`,assert 失败即回归失败):
       PYTHONPATH=.claude/skills/paper-landscape uv run python -c "from pathlib import Path; from scripts.status import collect; r=[x for x in collect(Path('.')) if x['idbase']=='{idbase}']; assert r and r[0]['state']=='compliant', 'NOT compliant: '+str(r)"
   编辑时务必保住这些不变量(否则 (b) 会挂):report.md 仍以 `# <标题> — 深度解读` 这一行 H1
   开篇(别删/移 H1,否则 report.html 重生取不到标题),导读 blockquote 之后保留 `## 评价` 段;无
   `<!--ref:-->`/`<!--anchor:-->`;无 ARA-未读入标记(「未能读取已验证知识包(ARA)」「(未解析到
   结论)」、回退标题 `# ai_package`);`level2_report.json` 仍是合法 JSON 且 `passes_seal2` 不变
   (改了封印内容不重跑 G3,靠 final_review.json 盖来源章——决策 #2)。
   - 两道都过 → 写终审标记(date 用注入的 {today};edits 列你改了哪些文件/要点;**单行 `-c`**):
       PYTHONPATH=.claude/skills/paper-landscape uv run python -c "from pathlib import Path; from scripts.output.final_review import write_marker; write_marker(Path('{ara_dir}'), verdict='revised', edits=['report.md: …'], date='{today}')"
     返回 {verdict:"revised", edits:[...]}。
   - 任一道挂了 → 改崩了(结构破损,非内容)→ 重试修一次;再挂 → 返回 {verdict:"failed",
     fail_category:"重写级", fail_reason:"机械回归无法通过"}(不写 marker)。
4. 若 CLEAN(无需改): 同款**单行** incantation 写标记,但 verdict='clean'、edits=[]:
       PYTHONPATH=.claude/skills/paper-landscape uv run python -c "from pathlib import Path; from scripts.output.final_review import write_marker; write_marker(Path('{ara_dir}'), verdict='clean', edits=[], date='{today}')"
   返回 {verdict:"clean"}。
5. 若 FAIL: 不改任何文件、不写 marker,返回 {verdict:"failed", fail_category, fail_reason}。

只返回上面 schema 的 JSON。你的编辑发生在你自己的上下文里;主会话只收这个 JSON。
```

> provenance(ADR-0013 #2):改了封印内容**不重跑 G3**;`final_review.json`(verdict=revised)即来源章,
> `passes_seal2` 布尔保持原值。这条写进 prompt 的"REVISE"说明里。

### Task 5:终审修订 skill 的编排(主会话 + Workflow)

- [ ] **Step 1:写 `sub-skills/final-review/SKILL.md`**(目录形式;文件开头加 YAML frontmatter `name: final-review` + 一句 `description`,同既有 sub-skill)—— 编排步骤(主会话执行):

```
## 终审修订(可选,操作者一轮跑完后触发;默认关)

前置:不接进 /loop;需要主会话有强模型(Opus + 高 effort)。没有就跳过。

1. 定批次:默认(**单行 `-c`**,勿换行——`from X import` 断行会 SyntaxError):
   `PYTHONPATH=.claude/skills/paper-landscape uv run python -c "from pathlib import Path; from scripts.output.final_review import unreviewed_compliant_keys; print(unreviewed_compliant_keys(Path('.')))"`
   (合规 + 未终审的 idbase 列表);也可由操作者显式给一个 idbase 子集。空 → 直接结束。

   FAIL 路径前置:demote → 复活赛重分析依赖 corpus 的 `images/`(gitignored)在场。
   `revival._revive_one` 先跑 `corpus_readiness_problems`,images 缺/不全时判 `manual`(需
   re-ingest)、不重分析。跨机 / 纯 checkout 上先确认 corpus 完整(`scripts.status` /
   `scripts.preflight`),不全就先 re-ingest 再跑 FAIL 收尾。

2. 跑 Workflow(pipeline over 批次,每篇一个 agent):
   - 每个 `agent(...)` 用 Task 4 的 prompt + schema;**pin model=opus + 足够 effort**;
     不同篇只碰各自文件 → 并行安全(无需 worktree)。
   - prompt 的 `{today}` 由主会话注入当天日期;若用 Workflow 脚本,经 `args` 传入(脚本不可用 Date.now)。
   - agent 自己改 + 自跑机械回归 + 写 final_review.json(CLEAN/REVISED)或返回 FAILED。
   - 主会话只收每篇的结构化 JSON,**不载入论文全文**。

3. 主会话串行收尾(单写者 LS-1)。**显式持一把锁、复用同一个 Ledger 实例**,整段包住 demote +
   revive_all(demote 的 `record` 与 `revive_all` 都不自锁、靠调用方持锁;两个 Ledger 实例会让第二
   次 `acquire()` 抛 LedgerLockError)。镜像 `revival.py` 的 `__main__` 装配:

       from pathlib import Path
       from scripts.ledger.store import Ledger
       from scripts.llm.seams import build_seams
       from scripts.output.repo_resolve import make_repo_resolver   # R10:复活也要码链解析
       from scripts.demote import demote_to_scene
       from scripts.revival import revive_all

       ws = Path(".")
       led = Ledger(ws)
       seams = build_seams()
       resolver = make_repo_resolver(web_search=seams.get("web_search"))
       # failed = [(idbase, fail_category, fail_reason), ...] —— 取自各篇 verdict=="failed"
       with led.acquire():                      # LS-1:整段一把锁
           scenes = [
               demote_to_scene(ws, idbase, ledger=led, category=cat, reason=why)
               for idbase, cat, why in failed
           ]
           res = revive_all(                    # 只复活本批降级的现场(branch2 根)→ 重封印 → 重发布
               workspace=ws, ledger=led, seams=seams,
               repo_resolver=resolver, human_directive=None,
               only_keys={s.name for s in scenes},  # 关键:不碰 _failed/ 既有无关积压
           )

   - 复活后的新产物**不带** final_review.json → 下一轮终审会再覆盖它。
   - `res` 里 `status=="manual"` 的篇(corpus images 缺)= 没重分析成功、ledger 仍 deferred,
     需 re-ingest 后再来;**单独汇报,别计入"已重发布"**。
   - REVISED/CLEAN 的篇:agent 已写好 marker,无需主会话动账本。

4. 收尾报告:CLEAN / REVISED / FAILED(→ 复活 done / manual 各几篇)+ `status --card`。
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
git add README.md docs/INDEX.md .claude/CLAUDE.md .claude/skills/paper-landscape/sub-skills/final-review/SKILL.md
git commit -m "docs(final-review): skill orchestration + README/INDEX/CLAUDE/ADR-0013 wiring"
```

---

## 验证(DoD)

- Chunk 1:`uv run pytest -q` 全绿(含 test_final_review / test_demote / test_status 新用例)+ ruff 干净。
- Chunk 2:一次真实小批次烟测——挑 1 篇制造一个小瑕疵 → 终审应 REVISE 修好 + 写 marker + 机械回归过;
  (可选)挑 1 篇人为破坏成"读错论文" → 终审应 FAIL → demote → 复活赛重分析出新产物。**前置**:该篇
  corpus 的 `images/` 须在场(本机已在场);否则 `revival._revive_one` 会判 `manual`(需 re-ingest)、
  不重分析——那是预期的跨机行为(images 为 gitignored),不是 bug。烟测须在 images 完整的本机上跑,
  并把 `RevivalResult.status=="manual"` 与 `"done"` 分开汇报。
- 不变量复核:`/loop` 路径**完全不依赖**终审修订(headless 自动化不破);账本只主会话串行写;
  `check_ara_bundle` 27+/0;status 0 divergence。

## 关键风险与对策

- **agent 改崩文件**:Task 4 的机械回归(check_ara_bundle + 合规)挡住;再挂升级 FAIL。
- **并行 agent 抢账本**:设计上 agent **绝不**碰账本/现场/复活赛——只主会话串行做(LS-1)。
- **降级转换出错**(发布后打回是新路径):Task 2 的两条单测锁住"产物入现场 + 原 vault 清空 + branch2 根 + 账本 deferred";`write_scene` 的原子换入(`.new`/`.old`)保证现场不丢。
- **复活在坏 ARA 上重写**(最隐蔽):靠现场 `target="ara"`(branch2 根)强制重分析——Task 2 单测断言了 `findings[0].target=="ara"` + `failed_gate=="结构门"`。

---

## Review Log

### Round 1
**Reviewer**: Codex (gpt-5.5, xhigh) | **Type**: Initial Review

Verified against live source: `write_scene` signature/move behavior, `target=="ara"`→branch2 routing, `revive_all`/`stage_branch2`, `Ledger.acquire`, `status.collect`, `vault_key`, `_html`, `check_bundle`. Baseline healthy (`uv run pytest -q` = 614 passed; engine+tests ruff clean).

Findings:
1. demote.py import block fails Ruff `I001` (blank line between `import yaml` and `from scripts...`).
2. `demote_to_scene` `finally: shutil.rmtree(staged)` is not data-safe — monkeypatching `write_scene` to raise after the moves left the original `ai_package`/`person_vault` gone AND `_failed/` empty.
3. FAIL revival unsound for products whose corpus lacks `content_list.json` — demote passes `content_list_path=None`, but revival calls G3 with `scene/content_list.json` unconditionally (`revival.py:350` → `equation_fidelity.py:43`). 4 current products affected: 2604.04198, 2503.14492, 2603.27287, 2606.12987.
4. Prompt `uv run python -c "` snippets have indented Python bodies → `IndentationError: unexpected indent`.
5. Skill path `sub-skills/final-review.md` diverges from the repo convention `sub-skills/<name>/SKILL.md` + frontmatter; `superpowers:subagent-driven-development` not present in session.

**Verdict**: REVISIONS NEEDED

---

### Response to Round 1
**Responder**: Claude Code

**Findings addressed**: 5 (4 ACCEPTED, 1 REJECTED)

1. **demote.py I001 import block**
   - Verdict: REJECTED
   - Evidence: a scratch-setup artifact. `scripts/__init__.py` exists, so at the real path Ruff classifies `scripts.*` as first-party (separate group from third-party `yaml`); the blank line between groups is *required* isort style. The existing `ledger/store.py` has the identical structure (stdlib / blank / `import yaml` / blank / `from scripts…`) and is Ruff-clean. I wrote the exact import block to `.claude/skills/paper-landscape/scripts/_f1probe.py` (real package path) → `uv run ruff check` = **All checks passed!**; and the /tmp copy with `__init__.py` markers also passes. The I001 only appears when the file is linted outside the `scripts` package.
   - Action: none (block is correct at the real path).

2. **`finally: rmtree(staged)` data-loss** (excellent catch)
   - Verdict: ACCEPTED
   - Evidence: confirmed — `write_scene` consumes `staged` on success (`failure_scene.py:117`), but on a `write_scene` exception after the two `shutil.move`s the products sit in `staged` and the `finally` deletes them while the originals are already moved out → permanent loss. The precedent `spoke._g3_to_scene` has **no** `finally` cleanup for exactly this reason.
   - Action: removed the `try/finally`; `write_scene` consumes `staged` on success, and on failure `staged` (with products) is left under `_failed/.scene-*` (recoverable) and the exception propagates — mirroring `_g3_to_scene`. Added regression test `test_demote_preserves_products_under_failed_if_write_scene_raises` (monkeypatches `write_scene` to raise, asserts products survive under `_failed/` + ledger not advanced). Validated: 4/4 demote tests pass, ruff clean.

3. **content_list.json missing → revival errors**
   - Verdict: ACCEPTED
   - Evidence: confirmed all 4 cited products lack `content_list.json` (4/32 corpus dirs; 28 tracked). revival passes the scene path (not the None-tolerant `cl`) to `run_g3`, so a scene without it raises `FileNotFoundError` → error, not re-analysis.
   - Action: added `_ensure_content_list(md)` — when corpus lacks `content_list.json`, synthesize a count-parity stand-in (`count_display_math_blocks` from `scripts.audit.equation_fidelity`, same口径 as the engine's tier-1 `_synthesize_content_list`; the MD already passed the ingest equation gate, re-analysis doesn't re-convert). demote now always passes an existing `content_list_path`. Added test `test_demote_synthesizes_content_list_when_corpus_lacks_it`. Validated.

4. **`python -c` IndentationError**
   - Verdict: ACCEPTED
   - Evidence: confirmed — an indented `-c` body raises `IndentationError: unexpected indent`.
   - Action: converted all three multi-line `-c` incantations (html-regen, marker-write ×2, batch-definition) to single-line semicolon form. Validated the single-line html-regen end-to-end (produced a 130 KB report.html, exit 0) and the marker-write form parses (only the expected "module not yet created" error, which Task 1 resolves).

5. **Skill path + sub-skill reference**
   - Verdict: ACCEPTED
   - Evidence: confirmed existing sub-skills are `<name>/SKILL.md` with `name`/`description` frontmatter (e.g. `g2-skeptic/SKILL.md`); the available skill is `subagent-driven-development` (no `superpowers:` prefix).
   - Action: changed all `sub-skills/final-review.md` → `sub-skills/final-review/SKILL.md`, documented the dir+frontmatter convention in the file-map and Task 5 Step 1, and corrected the line-10 reference.

**Spec body updated**: Yes
**Open issues remaining**: 0 (finding 1 is REJECTED with real-path ruff evidence)

---

### Round 2
**Reviewer**: Codex (gpt-5.5, xhigh) | **Type**: Focused Review

Round-1 findings rechecked: Finding 1 rejection **adequate** (ruff import ordering clean at the real package path; `--stdin-filename .../demote.py --select I` probe passed); Findings 2-3 **fixed** (staging cleanup no longer data-losing; `_ensure_content_list` matches tier-1 synthesis); Finding 4 **fixed** (single-line `-c`); Finding 5 **fixed** (sub-skill `<name>/SKILL.md` + frontmatter). Validation: `uv run pytest -q` = 614 passed; engine+tests ruff clean; embedded `final_review.py`/`demote.py`/test snippets ruff clean.

New finding:
1. Medium: the REVISE regression doesn't mechanically prove `status == compliant`. Decision #5 (spec:26) requires `check_ara_bundle + status 合规`, but the prompt only ran `check_ara_bundle` + manual report-structure checks. `check_ara_bundle` doesn't validate `level2_report.json` parse / `passes_seal2` — that lives in `status._ara_sealed` (status.py:92). Add a `scripts.status.collect` assertion that the idbase is `state == "compliant"` before the marker write.

**Verdict**: REVISIONS NEEDED

---

### Response to Round 2
**Responder**: Claude Code

**Findings addressed**: 1 (1 ACCEPTED)

1. **REVISE regression missing the status-compliant gate**
   - Verdict: ACCEPTED
   - Evidence: confirmed — `check_ara_bundle.check_bundle` only inspects `src/code_ref.md` / `evidence/tables/` / a `level2_report.json` drift substring; it never parses `level2_report.json` nor checks `passes_seal2`. That (plus report-compliant + non-corrupt) is exactly `status.collect`'s `state == "compliant"`. The prompt's prose checks approximated report-compliance but omitted the sealing check, so a REVISE that broke `level2_report.json` JSON or flipped `passes_seal2` would pass the old regression yet be non-compliant — violating locked decision #5 ("check_ara_bundle + status 合规").
   - Action: made the REVISE regression two explicit gates — (a) `check_ara_bundle`, (b) a single-line authoritative `assert collect(Path('.'))[idbase].state == "compliant"` (covers report-compliant + `passes_seal2` + non-corrupt). Listed the invariants to preserve (incl. `level2_report.json` stays valid JSON with unchanged `passes_seal2`). Failure of either gate → retry once → else FAIL. Validated the assertion incantation (passes for a real compliant idbase `1803.10122`; raises `AssertionError` for an absent one).

**Spec body updated**: Yes
**Open issues remaining**: 0

---

### Round 3
**Reviewer**: Codex (gpt-5.5, xhigh) | **Type**: Focused Review

No blocking findings. The Round-2 fix is adequate: the spec now requires both gates before a REVISED marker write (`check_ara_bundle` + a `status.collect(... state=="compliant")` assertion). Verified `status.collect` covers report compliance, corrupt-report exclusion, and `_ara_sealed`/`passes_seal2`, while `check_ara_bundle` remains the bundle regression gate. Re-ran the single-line assertion against real idbase `1803.10122` (passed) and an absent idbase (AssertionError as expected).

**Verdict**: APPROVED

---

### Response to Round 3
**Responder**: Claude Code

No findings to address (Codex confirmed all resolved). Proceeding to the Final fresh-eyes gate review per the loop protocol.

**Open issues remaining**: 0

---

### Round 4
**Reviewer**: Codex (gpt-5.5, xhigh) | **Type**: Final Review (fresh-eyes gate)

**Finding** (Blocking): `_candidate_from_paper()` reconstructs only `title/arxiv_id/doi`, but `revive_all` routes branch2 scenes into `stage_branch2` → `write_branch2._paper_md`, which reads `candidate["year"]` as a required subscript (branch2_ara.py:60). So `demote → revive_all` would `KeyError` instead of re-analyzing/republishing. Also: DOI-only reconstruction must not put a raw DOI into `arxiv_id` — `vault_key()`/`identity_base()` treat any non-empty `arxiv_id` as the identity base (naming.py:47).

**Verdict**: REJECTED

---

### Response to Round 4
**Responder**: Claude Code

**Findings addressed**: 1 blocker + 1 sub-issue (both ACCEPTED) — sharp fresh-eyes catch.

1. **`candidate["year"]` KeyError on the FAIL→revival path**
   - Verdict: ACCEPTED
   - Evidence: confirmed `write_branch2._paper_md` (branch2_ara.py:53-74) takes `candidate["title"]` AND `candidate["year"]` as required subscripts (the rest `.get`). `_candidate_from_paper` omitted `year`, so a real demote→`revive_all`→`stage_branch2` would `KeyError`. Real PAPER.md frontmatter carries `year` (27/32; 5 are null).
   - Action: `_candidate_from_paper` now recovers the full candidate `write_branch2` needs — `title`, `year`, `authors`, `venue`, `doi`, `arxiv_id`. `year` is always a present key (value from frontmatter or `None` → renders as `null`, never KeyError). Added `import re`. Validated against all 32 real PAPER.md: 32/32 have `title` + a present `year` key; the recovered candidate satisfies the required subscripts.

2. **DOI-only `arxiv_id` pollution**
   - Verdict: ACCEPTED
   - Evidence: confirmed — the old `else (fm.get("key") or None)` would put a DOI-only paper's `key` (the raw DOI) into `arxiv_id`; `identity_base` then treats it as the identity base, changing the revived vault key.
   - Action: `arxiv_id` is now ONLY a real arXiv id (`\d{4}\.\d{4,5}` from `doi: arXiv:…` or a matching `key`) else `None`, so a DOI-only paper falls through to `identity_base(None, doi)` = `doi-<hash>`. Validated: synthetic DOI-only → `arxiv_id=None`, `identity_base="doi-5c0e00dc"`. Added tests `test_demote_candidate_doi_only_keeps_arxiv_id_none` and `year`/`authors` assertions in the move test (5 demote tests, all pass, ruff clean).

**Spec body updated**: Yes
**Open issues remaining**: 0

---

### Round 5
**Reviewer**: Codex (gpt-5.5, xhigh) | **Type**: Final Review (fresh-eyes gate)

Two blockers:
1. The FAIL orchestration calls `revive_all`, but `revive_all` loads EVERY scene under `_failed/` (`_load_scenes`), so an optional final-review pass would mutate unrelated deferred work.
2. `demote_to_scene` reconstructs the wrong ledger key for DOI-only papers: hub keys come from `_candidate_key()` (`_safe_key(arxiv_id or doi)`), but the vault/status idbase is `doi-<hash>`; `_ledger_key_for` compares `_idbase(row["key"])` to the idbase, so DOI-only demotion records/revives under `doi-<hash>` while the real raw-DOI ledger row goes stale (revival writes `done` back to `manifest["ledger_key"]`).

Non-blocking: exclude `ledger_diverged` products from the default batch; validate marker schema so `{}` isn't treated as reviewed.

**Verdict**: REJECTED

---

### Response to Round 5
**Responder**: Claude Code

**Findings addressed**: 2 blockers + 2 non-blocking (all ACCEPTED).

1. **`revive_all` revives the whole `_failed/` backlog**
   - Verdict: ACCEPTED
   - Evidence: confirmed `revive_all` iterates all `_load_scenes(workspace)` with no scope filter.
   - Action: added a backward-compatible `only_keys: set[str] | None = None` param to `revive_all` (default `None` = current behavior; all 11 existing revival tests stay green) that skips scenes whose `scene_dir.name ∉ only_keys`. The orchestration collects the demoted scene dirs and passes `only_keys={s.name for s in scenes}`, so the FAIL pass revives ONLY its own demotions. New task **Task 2b** + test `test_revive_all_only_keys_scopes_to_subset` (validated; revival.py ruff-clean). File-map + "复用既有" updated (revive_all = 微调, only an additive optional param; branch2 logic untouched).

2. **DOI-only ledger key mismatch**
   - Verdict: ACCEPTED
   - Evidence: confirmed `_candidate_key` (hub.py:99) = `_safe_key(key or arxiv_id or doi or title)`; for DOI-only that's `_safe_key("10.1234/qux")="10.1234_qux"`, while `_ledger_key_for` returned the `doi-<hash>` idbase.
   - Action: removed `_ledger_key_for`; demote now sets `ledger_key = _candidate_key(candidate)` (imported from hub) — the exact key the hub recorded, for both arXiv (`1111.11111`) and DOI-only (`10.1234_qux`). Validated against both; added `test_demote_doi_only_records_under_safe_keyed_ledger_key`.

3. **(non-blocking) exclude `ledger_diverged` from the batch**
   - Verdict: ACCEPTED
   - Action: `_compliant_idbases` now filters `state=="compliant" AND not ledger_diverged` — a divergent product is about to be reprocessed/pruned by `/loop`, so terminally reviewing it is wasted + racy.

4. **(non-blocking) marker schema `{}` treated as reviewed**
   - Verdict: ACCEPTED
   - Action: `is_reviewed` now requires `read_marker(...).get("verdict") in (clean|revised)` — a `{}`/verdict-less/corrupt marker no longer counts as reviewed (so a bad write can't permanently skip a paper). Added `test_is_reviewed_false_for_empty_or_invalid_marker`. `read_marker` stays raw (provenance display).

Validated all together at real paths: 12 demote+final_review tests pass, revival suite green, ruff clean.

**Spec body updated**: Yes
**Open issues remaining**: 0

---

### Round 6
**Reviewer**: Codex (gpt-5.5, xhigh) | **Type**: Final Review (fresh-eyes gate)

Two blockers:
1. `demote_to_scene` can't find the source MD for **versioned** arXiv corpus entries: ingest names corpus `{arxiv_id}{version}_{ShortName}` (ingest.py `_paper_id`), but the demote lookup globs `{idbase}_*/{idbase}_*.md` — a corpus `2401.00001v2_Title/...` with vault key `..._2401.00001` raises `FileNotFoundError`, so the FAIL path can't run.
2. DOI-only compliant products are silently excluded from the default batch: the `not ledger_diverged` filter drops them because `status.collect` matches ledger rows by filesystem idbase (`doi-<hash>`) while the DOI-only hub ledger key is the safe raw DOI (`_candidate_key`) → reproduced as `ledger=None, ledger_diverged=True`.

(Confirmed the branch2 routing `target=="ara"` → branch2 is otherwise sound.)

**Verdict**: REJECTED

---

### Response to Round 6
**Responder**: Claude Code

**Findings addressed**: 2 blockers (both ACCEPTED).

1. **Versioned-corpus MD lookup**
   - Verdict: ACCEPTED
   - Evidence: confirmed `_paper_id` emits `{arxiv_id}{version}_{ShortName}`; `_idbase("2401.00001v2_Title")="2401.00001"` but the `{idbase}_*` glob misses it (the version sits between idbase and `_`).
   - Action: added `_find_corpus_md(ws, idbase)` matching corpus dirs by regex `^{re.escape(idbase)}(v\d+)?_` (handles arXiv plain + versioned AND DOI-only `doi-<hash>_Name`, with no over-match across distinct idbases). demote now uses it for the MD lookup. Validated the matcher across plain/versioned/DOI-only/near-miss (4/4); added `test_demote_finds_versioned_corpus_md` (a `2401.00001v2_Foo` corpus). The vault `*_{idbase}` globs are unaffected (vault keys carry the version-stripped `identity_base`).

2. **DOI-only false-exclusion from the batch**
   - Verdict: ACCEPTED
   - Evidence: confirmed — a synthetic DOI-only compliant product surfaces as `ledger_diverged=True` because `status.collect` can't map its safe-keyed ledger key to the `doi-<hash>` filesystem idbase. My Round-5 `not ledger_diverged` filter therefore dropped all DOI-only products.
   - Action: reverted `_compliant_idbases` to `state == "compliant"` (no divergence filter), with a docstring explaining the DOI-only status-matching limitation and why including a divergent product is safe (at worst a CLEAN/REVISE marker lost on the next `/loop` reprocess; a FAIL→demote on a divergent product actually converges the ledger). This re-includes DOI-only products and trades away only the minor (non-blocking) divergence optimization.

Validated the EXACT spec code blocks (extracted verbatim from this file): ruff clean + 13 tests pass (7 demote incl. versioned-corpus + DOI-only-ledger-key; 6 final_review incl. `{}`-marker).

**Spec body updated**: Yes
**Open issues remaining**: 0

---

### Round 7
**Reviewer**: Codex (gpt-5.5, xhigh) | **Type**: Final Review (fresh-eyes gate)

No blocker findings. Verified the risky contracts against the live engine: `target=="ara"` → branch2 routing; revival readiness short-circuits missing corpus to `manual` before LLM work; `write_scene` consumes `staged_dir/{ai,person}` in the demote layout; candidate reconstruction covers the real required subscripts (`title`/`year`); single-ledger-instance lock discipline matches `store.py`. Validation: `uv run pytest tests/test_revival.py tests/test_status.py tests/test_failure_scene.py -q` = 25 passed.

One non-blocking hardening note: `read_marker()` should treat non-dict JSON (e.g. `[]`) as invalid so `is_reviewed()` never calls `.get()` on a list.

**Verdict**: APPROVED

---

### Response to Round 7
**Responder**: Claude Code

No blockers. Incorporated the non-blocking hardening (cheap, real edge): `read_marker` now returns `None` for non-dict JSON (`return data if isinstance(data, dict) else None`), so a `[1, 2]`-shaped marker can't reach `is_reviewed`'s `.get()` (AttributeError). Extended `test_is_reviewed_false_for_empty_or_invalid_marker` to cover `[]`/`[1, 2]`. Re-validated the verbatim spec blocks: ruff clean + 13 tests pass.

**Loop outcome**: APPROVED at Round 7 (Final fresh-eyes gate). 7 rounds (Initial + 3 Focused + 3 Final), budget 12. Every Codex finding across the loop was verified against the engine and fixed (or rejected with real-path evidence — only the Round-1 import-I001, a scratch-only artifact); each code change was validated at real paths (ruff + pytest) before transcription.
