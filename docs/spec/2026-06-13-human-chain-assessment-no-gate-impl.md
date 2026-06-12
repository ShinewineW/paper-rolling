# 人链报告改「评价」、不设硬门 实现计划 — ADR-0012(rev)

> **日期**: 2026-06-13
> **状态**: 已落地(main `9ea1178..8e8a364` + oh-my-codex 修复 `50b125f`/`e528588`)
> **作者**: Claude (Opus 4.8) + ShinewineW
> **基准版本**: `paper-rolling@main`(HEAD)
> **目的**: 把 branch1(理解阅读)的「忠实门」从**硬门**改成**不拦截的开篇「评价」**:唯一真值参照=已验证 ARA、退役整套 MD 锚点机制、branch1 永不失败。ARA 侧(结构门/数字门/最终门)严谨硬关不动。

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** branch1 报告不再被任何忠实性检查硬拦;改为机器确定性核出"报告里不在 ARA 的数字"+ 本地 claude-code(haiku)判官写一段语义点评,合成「## 评价」作为报告第一章节;退役 MD 锚点机制;ARA 仍是被严格守住的 source of truth。

**Architecture:** 真值参照从源 MD 翻成已验证 ARA(`load_ara_bundle` 的数字集)。`branch1_gate` 从"返回硬拦 findings 并触发 `AnchorGateError`"改为"产出 `## 评价` 文本块、永不抛错"。`faithfulness_judge` seam 从"返回 faithful 布尔裁决"改写为"返回一段中文语义点评 prose、fail-soft"。两条 branch1 产出路径(`write_branch1_llm` / `write_branch1`)把「评价」**前置为首节**。退役:`anchor_lint.lint_text` 调用、核心结论块与 `_ground_report` 的 `<!--ref-->` 锚定、G3 对 branch1 的 `check_branch1_md_anchors`。移除 branch1 的 `AnchorGateError` 硬拦、`_failed/` 现场、复活根。

**Tech Stack:** Python 3.13、`uv run pytest`(pythonpath 预置)、`ruff`。无新依赖。判官路由 `config/llm.yaml: faithfulness → claude-code`(tier=fast → claude-haiku-4-5),不变。

---

## 工程师须先读(背景)

- **ADR-0012(rev)** `docs/adr/0012-*.md` 是本计划落地的决策。**ADR-0008** 修订:锚点门退役为「评价」,规范门只剩三道。
- **当前 branch1 自门控**在 `scripts/output/branch1_gate.py::check_report_faithfulness`(返回 hard-block findings)+ 两条产出路径里的 `raise AnchorGateError`:
  - LLM 路径 `scripts/output/branch1_llm.py::write_branch1_llm`(组装 → `check_report_faithfulness` → `raise`,见 `:304-318`;另有图形完整性 `raise`,见 `:319-331`)。
  - 确定性路径 `scripts/output/branch1_report.py::write_branch1`(`:250-262`)。
- **真值参照机制**:`branch1_gate` 现在对**源 MD** 核对(`unconfirmed_report_numbers(report, source_md)`)。新设计改对 **ARA**:复用 `scripts/audit/g3_seal.py::load_ara_bundle(ara_dir)`(已 public)+ `scripts/audit/ara_tree.py::source_value_set` / `number_present`。
- **判官 seam**:`scripts/llm/seams.py::faithfulness_judge(report_text, ara_dir) -> dict`,经 `_ask_json(seam="faithfulness", tier="fast")`。`config/llm.yaml` 路由 `faithfulness → claude-code`(haiku),保持。
- **ARA 的 AUDIT_FLAGS**:数字门 tolerant 时把存疑数字写进 `ai_package/{key}/ara/AUDIT_FLAGS.md`(在 branch1 之前就生成,可直接读)。
- **锚点机制(退役对象)**:`scripts/output/anchor_lint.py`(`lint_text` / `unanchored_empirical_lines` / `_is_empirical_assertion`)、`scripts/audit/anchor_resolution.py::check_branch1_md_anchors`、`branch1_report.py::_anchor`/`_find_in_md`、`branch1_llm.py::_claims_block` 的 `_anchor` 调用 + `_ground_report`/`_ground_line`。
- **运行**:`uv run pytest`;lint:`uv run ruff check .claude/skills/paper-landscape/scripts/ tests/`。

## 文件改动总览

| 文件 | 改动 | 责任 |
|---|---|---|
| `scripts/output/branch1_gate.py` | 重写 | (b) 改对 ARA 出"事实清单";新增 `build_assessment` 出「评价」文本;删除 `check_report_faithfulness`/`lint_text` 依赖(Task 1,3) |
| `scripts/llm/seams.py` | 改写 `faithfulness_judge` | 从"裁决"→"写语义点评 prose",fail-soft(Task 2) |
| `scripts/output/branch1_llm.py` | 改 | 调 `build_assessment` 前置首节;删 `AnchorGateError`(忠实)+ 核心结论/stray 锚定 + 图形硬拦改 flag(Task 3,4,6) |
| `scripts/output/branch1_report.py` | 改 | 确定性路径同样前置「评价」、删 `AnchorGateError`(Task 3) |
| `scripts/audit/g3_seal.py` | 改 | 删 branch1 anchor-resolution 子检查(Task 5) |
| `scripts/output/produce.py` | 改 | 删 `stage_branch1` 的 judge 守卫 + `except AnchorGateError`(Task 6) |
| `scripts/spoke.py` | 改 | 删 branch1 的 `AnchorGateError` → `_pre_promote_scene`(Task 6) |
| `scripts/revival.py` | 改 | 删 branch1 复活根(Task 6) |
| `tests/...` | 增改 | 镜像每处 |
| `scripts/output/anchor_lint.py` / `scripts/audit/anchor_resolution.py` | 留为死代码 | 不再被门调用;本计划不删文件(单测仍在),仅断开调用 |

---

## 既有测试迁移地图(必读 — 退役的是「行为」,不是签名)

> 本重构**退役了 branch1 的整套失败语义**(branch1 能失败 / 锚点门是门 / 判官返回 dict 裁决 / AnchorGateError / branch1 复活根 / "缺 judge 即 abort" 守卫)。下表列出的既有测试**断言的正是这些被退役的行为**,落地时**必须按"新行为"逐一改写/删除**——它们不是"签名漂移",`uv run pytest` 收集期就会因 ImportError/AttributeError 或语义反转而红。每个 Task 的"改测"步骤回指此表。

| 文件:测试 | 旧断言(被退役) | 新动作 / 期望 |
|---|---|---|
| `tests/output/test_branch1_gate.py:3` import | `from ... import check_report_faithfulness, unconfirmed_report_numbers` | 改为 `from scripts.output.branch1_gate import prose_numbers, ungrounded_report_numbers, build_assessment`(两个旧符号已删,否则收集期 ImportError 整文件挂) |
| 同文件 `test_grounded_prose_numbers_pass` / `test_anchor_comment_payloads_are_not_parsed_as_numbers` / `test_list_index_and_locators_are_not_data_numbers` / `test_invented_prose_number_is_flagged` / `test_arxiv_id_and_doi_in_prose_are_not_data_numbers` / `test_inline_code_vault_path_is_not_a_data_number` / `test_real_metric_decimal_is_not_mistaken_for_an_arxiv_id` / `test_table_rows_and_code_fences_are_skipped`(:6-69,共 8 个) | 都调 `unconfirmed_report_numbers(report, md)`(旧 2 参/对 MD) | **改写**:这 8 个考的其实是 `prose_numbers` 的剥离逻辑(anchor payload/表格/行内 code/arXiv id/locator),而 `prose_numbers` **保持不变** → 直接断言 `prose_numbers(report)` 的输出(**无需 ARA fixture**)。"是否落源"的语义交给少量新的 `ungrounded_report_numbers(report, ara_dir)` 测(Task 1)。 |
| 同文件:`test_gate_passes_faithful_report` / `test_gate_blocks_systematic_invented_numbers` / `test_gate_tolerates_a_single_miss_when_tolerant` / `test_gate_ratio_loosens_large_reports_but_floor_protects_small` / `test_gate_strict_blocks_a_single_miss` / `test_gate_blocks_on_judge_drift` | 调 `check_report_faithfulness(...)` 期望 hard-block findings / `AnchorGateError` | **全部重写**为新 API:`ungrounded_report_numbers(report, ara_dir)`(对 ARA)断言事实清单;`build_assessment(...)` 断言**永不抛**、`## 评价` 含机器事实/判官点评。"systematic invented numbers" 这类改为断言它们**出现在评价里**而非拦截。 |
| 同文件 fake judges `_ok_judge`/`_drift_judge`(:62-67 一带) | 旧 2 参 `(report_text, ara_dir)` 返回 `{"faithful":..,"findings":..}` | 改新签名 `(report_text, ara_dir, *, ungrounded=None)` 返回 `str`(语义点评) |
| `tests/llm/test_seams.py` `test_faithfulness_judge_fails_closed_on_seam_error` / `test_faithfulness_judge_normalizes_response`(:14-55) | monkeypatch `_ask_json`,断言返回 dict 的 `["faithful"]`/`["findings"]`、seam 出错 fail-**closed** | 改为 monkeypatch `_ask_text`,断言返回 **`str`**、seam 出错 fail-**soft**(返回中性句、不抛)。`test_build_seams_includes_faithfulness_judge`(查 key 在)**保留**。 |
| `tests/output/test_branch1.py` `test_deterministic_path_honors_a_supplied_judge`(:79-95) | `write_branch1` + `_drift_judge` 下 `pytest.raises(AnchorGateError)` 且 judge 调用一次 | 改为**断言不抛**、report 产出、判官点评进 `## 评价`;`_drift_judge`(:85)改新签名返回 str |
| 同文件 `test_report_passes_anchor_lint`(:11)、`test_branch1_prose_is_domain_agnostic_no_hardcoded_diffusion`(:136 末)、`test_unanchored_prose_number_no_longer_raises_gate_error`(:65) | 末尾 `assert lint_text(report) == []` / 锚点相关 | 退役锚点后报告无 `<!--ref-->`;改为断言 `"<!--ref" not in report`。**仅删对 `<!--ref-->`/`<!--anchor:` 的断言** |
| 同文件 `test_report_uses_unified_classdef_palette`(:20) `assert "classDef" in report` | — | **保留不动**:`classDef` 来自 `_mermaid_redraw`/`_CLASSDEF`,**不在退役范围**(classDef 与锚点是两套机制,只退役锚点)。切勿误删 |
| `tests/output/test_branch1_llm.py:52` `test_write_branch1_llm_assembles_grounded_report` | `assert "<!--anchor:" in report` | **改写**:Task 4 删核心结论锚定 + `_ground_report` 后报告无 `<!--anchor:`;改为 `assert "<!--anchor:" not in report`(或断言 `## 评价` 首节存在)。(:48 `## 核心结论`、:49 `28.4`、:51 表格断言仍成立,留) |
| `tests/output/test_branch1_llm.py:11` import + `:161/167`(图形 mandatory/missing) | `from ... import AnchorGateError` + `pytest.raises(AnchorGateError, match="core method/model-structure figure")` | Task 6 图形改 flag 后:**断言报告仍写出** + `## 评价` 含"缺图"提示,不再 raise;改完文件内无 AnchorGateError 用例 → **删 `:11` 的 import**(否则 ruff F401) |
| `tests/test_spoke.py` `test_g3_branch1_reemit_hits_anchor_lands_scene`(:864)、`test_g3_branch1_root_reuses_branch2`(:938) | monkeypatch `g3.check_branch1_md_anchors`,断言 `status=='failed'`、`failed_gate=='锚点门'`、_failed 现场 / branch1 复活根 | **删除**(锚点门退役、branch1 不再失败、不再是复活根)。其 `from ... import AnchorGateError`(:865)、monkeypatch(:873/:945)随之移除。若想保留"branch1 G3 根"覆盖,改为针对"缺 report.md"(G3R0)那条仍在的硬错。 |
| 同文件 `test_spoke_branch1_blocks_on_judge_drift`(:1125-1161)+ `_drift_judge`(:1138) | `_drift_judge` 返回 `faithful=False` → `status=='failed'` + `FAILURE_AUDIT_BLOCK` | **重写**:branch1 永不拦 → 断言 spoke **成功晋升(status done)**,drift 只体现在 `## 评价`;`_drift_judge` 改新签名返回 str |
| `tests/output/test_produce.py:208` `test_llm_writer_without_faithfulness_judge_aborts_loudly` | `pytest.raises(ValueError, match="faithfulness_judge")`(守卫专测) | **删除**(守卫移除;judge 现在可选、fail-soft、不再 abort——有意取消的不变量) |
| `tests/test_revival.py:140` `test_revive_anchor_gate_scene_promotes` | seed `failed_gate='锚点门'` + `findings target=report.md`,断言 branch1 复活复用 ARA → `done`、scene 消失 | **改写到 G3R0**:锚点门退役,但 branch1 复活仍服务 G3R0(缺 report.md)。改 seed `failed_gate='最终门'` + finding target 指向**不存在的 report.md**,断言复活重发 branch1 后晋升 `done`、scene 消失。(若不在 revival 支持 G3R0 恢复则删除并标注理由——但 Task 6 决定**保留** G3R0,故改写) |
| `tests/audit/test_g3_seal.py` `test_run_g3_blocks_on_unresolvable_branch1_anchor`(及其 `_build_paper(good=False)` 分支) | 注入不可解析锚点 → G3 blocked | **删除/改写**:G3 不再做 branch1 锚点解析。新增穿过删除点的回归见 Task 5。 |
| `tests/test_examples.py:69` | `assert lint_text(...) == []` | 核对前置 `## 评价` blockquote(`>` 开头)不被 anchor lint 视为违例(应仍 `[]`);否则改断言 |

> 落地纪律:**caller-first**——先去掉调用方传的 kwargs/旧签名,或在同一提交里成组改,避免任何中间态 `TypeError`。每个 Task 完成后跑该 Task 涉及文件的 `pytest`,全部 Task 后跑全量。

---

## Chunk 1: (b) 改对 ARA + 判官改写「点评」

### Task 1: (b) 数字核对改对 ARA 数字集,只产事实

**Files:**
- Modify: `.claude/skills/paper-landscape/scripts/output/branch1_gate.py`
- Test: `tests/output/test_branch1_gate.py`

- [ ] **Step 1: 写失败测试** — 追加到 `tests/output/test_branch1_gate.py`:

```python
def test_ungrounded_vs_ara_uses_ara_not_md(tmp_path) -> None:
    # 真值参照 = ARA,不是源 MD。报告里 28.4 在 ARA、99.9 不在 → 只 99.9 算未落源。
    # 手搓最小 ARA,正好覆盖 load_ara_bundle 读取的 PAPER.md + logic/claims.md。
    from scripts.output.branch1_gate import ungrounded_report_numbers
    ara = tmp_path / "ara"
    (ara / "logic").mkdir(parents=True)
    (ara / "logic" / "claims.md").write_text("**Statement**: reaches 28.4 NDS", encoding="utf-8")
    (ara / "PAPER.md").write_text("headline_value: 28.4", encoding="utf-8")
    report = "本文达到 28.4 NDS,另有 99.9 凭空数字。"
    assert ungrounded_report_numbers(report, ara) == ["99.9"]
```
> 注:`load_ara_bundle`(`g3_seal.py`)读固定相对路径集(PAPER.md / logic/claims.md / evidence/…);上面的最小 ARA 足以让它提到 28.4。**不要** import 未用的 `write_branch2`(会触发 ruff F401)。若要更贴近真实 ARA,可改用 `write_branch2(ara, candidate, analysis)` + 既有 fixtures。

- [ ] **Step 2: 运行确认失败**

Run: `uv run pytest tests/output/test_branch1_gate.py::test_ungrounded_vs_ara_uses_ara_not_md -q`
Expected: FAIL — `cannot import name 'ungrounded_report_numbers'`。

- [ ] **Step 3: 在 `branch1_gate.py` 顶部 import 只【加】ARA 读取器(不删 lint_text/Finding/Severity)**

> **关键(每任务 checkpoint 必须保持绿)**:`check_report_faithfulness` 到 **Task 3** 才删,它现在仍用 `lint_text`/`Finding`/`Severity`/`Callable`。**本 Task 不要动这三个 import**,否则 Task 1 末尾 `check_report_faithfulness` → NameError(pytest 红)+ ruff F821。它们的删除挪到 **Task 3 Step 3**(随 `check_report_faithfulness` 一起)。

OLD(`:14-16`):
```python
from scripts.audit.ara_tree import extract_numbers, number_present, source_value_set
from scripts.audit.types import Finding, Severity
from scripts.output.anchor_lint import lint_text
```
NEW(**仅新增** `load_ara_bundle`;其余原样保留):
```python
from scripts.audit.ara_tree import extract_numbers, number_present, source_value_set
from scripts.audit.g3_seal import load_ara_bundle
from scripts.audit.types import Finding, Severity
from scripts.output.anchor_lint import lint_text
```

- [ ] **Step 4: 加 `ara_value_set` + `ungrounded_report_numbers`,删 `unconfirmed_report_numbers`**

在 `prose_numbers` 之后,替换原 `unconfirmed_report_numbers`:

OLD(`:81-84`):
```python
def unconfirmed_report_numbers(report_text: str, source_md: str) -> list[str]:
    """Prose numbers whose VALUE is NOT present in `source_md`. Order-preserving."""
    source_values = source_value_set(source_md)
    return [n for n in prose_numbers(report_text) if not number_present(n, source_values)]
```
NEW:
```python
def ara_value_set(ara_dir: Path) -> set[float]:
    """The distinct numeric VALUES present in the verified ARA bundle (claims +
    evidence tables + logic). The branch1 「评价」 grounds report prose numbers
    against THIS — the ARA is the writer's only source and the verified SoT, so a
    report number absent here is what we surface (ADR-0012 rev)."""
    bundle = load_ara_bundle(ara_dir)
    return source_value_set("\n".join(bundle.values()))


def ungrounded_report_numbers(report_text: str, ara_dir: Path) -> list[str]:
    """Report prose numbers whose VALUE is NOT present in the verified ARA.
    Order-preserving, deterministic — produces FACTS for the 「评价」, never blocks."""
    vals = ara_value_set(ara_dir)
    return [n for n in prose_numbers(report_text) if not number_present(n, vals)]
```

- [ ] **Step 5: 跑测试** — `uv run pytest tests/output/test_branch1_gate.py -q`;Expected: PASS(新测 + 既有 prose_numbers 测;依赖 `source_md` 的旧测在 Task 3 一并改)。

- [ ] **Step 6: lint + commit**

```bash
uv run ruff check .claude/skills/paper-landscape/scripts/output/branch1_gate.py tests/output/
git add .claude/skills/paper-landscape/scripts/output/branch1_gate.py tests/output/test_branch1_gate.py
git commit -m "feat(branch1): (b) ground report numbers against the ARA, produce facts (ADR-0012 rev)"
```

---

### Task 2: 判官 seam 改写为「写语义点评」(fail-soft)

**Files:**
- Modify: `.claude/skills/paper-landscape/scripts/llm/seams.py`(`faithfulness_judge`)
- Test: `tests/llm/test_seams.py`

判官**不再返回裁决**,改为返回一段中文语义点评 prose;数字事实由 (b) 机器提供,故判官 prompt 收到"已知未落源数字清单"作为上下文。**永不 raise、永不拦**:seam 出错 → 返回中性兜底句。

- [ ] **Step 1: 写失败测试** — 追加到 `tests/llm/test_seams.py`:

```python
def test_faithfulness_judge_returns_prose_and_failsoft(monkeypatch, tmp_path) -> None:
    from scripts.llm import seams
    (tmp_path / "logic").mkdir(parents=True)
    (tmp_path / "logic" / "claims.md").write_text("**Statement**: x", encoding="utf-8")
    # 正常:返回 prose
    monkeypatch.setattr(seams, "_ask_text", lambda *a, **k: "整体与知识包一致,无实质误导。")
    note = seams.faithfulness_judge("报告正文", tmp_path, ungrounded=["99.9"])
    assert isinstance(note, str) and "一致" in note
    # seam 出错:fail-soft,返回兜底 str,不抛
    def _boom(*a, **k):
        raise RuntimeError("provider down")
    monkeypatch.setattr(seams, "_ask_text", _boom)
    note2 = seams.faithfulness_judge("报告正文", tmp_path, ungrounded=[])
    assert isinstance(note2, str)  # 不抛错
```

> 先决:`seams.py` 需有一个返回**纯文本**的 helper `_ask_text`(对照现有 `_ask_json`)。若不存在,本 Task Step 3 先加它(用同一 provider 路由,返回原始 message 文本)。

- [ ] **Step 2: 运行确认失败**

Run: `uv run pytest tests/llm/test_seams.py::test_faithfulness_judge_returns_prose_and_failsoft -q`
Expected: FAIL(签名不符 / `_ask_text` 不存在)。

- [ ] **Step 3:(如缺)加 `_ask_text`** — 在 `_ask_json` 旁:

```python
def _ask_text(prompt: str, *, seam: str, tier: str = "fast", timeout: float = 600.0,
              effort: str = "medium") -> str:
    """Like _ask_json but returns the raw text (for prose seams like the 评价)."""
    return _provider_for(seam).complete(prompt, tier=tier, timeout=timeout, effort=effort)
```
> 读 `_ask_json` 确认 `_provider_for(seam).complete(...)` 的真实签名后对齐(参数名/是否有 effort)。

- [ ] **Step 4: 改写 `faithfulness_judge`**

OLD:整段 `def faithfulness_judge(report_text, ara_dir) -> dict:`(返回 `{"faithful":..., "findings":...}`)。
NEW:
```python
def faithfulness_judge(report_text: str, ara_dir: Path, *, ungrounded: list[str] | None = None) -> str:
    """branch1 「评价」(c) 语义层(ADR-0012 rev):写一段读者向的中文点评,对照已验证
    ARA 指出实质误导(张冠李戴/夸大/矛盾)。**不裁决、不拦**;数字事实由 (b) 机器供给,这里
    作为上下文。Fail-soft:seam 出错返回中性句。"""
    bundle = load_ara_bundle(ara_dir)
    ara_text = "\n\n".join(f"=== {name} ===\n{text}" for name, text in bundle.items())
    if len(ara_text) > _MD_CHAR_CAP:
        ara_text = ara_text[:_MD_CHAR_CAP] + "\n[...TRUNCATED...]"
    nums = "、".join(ungrounded or []) or "(无)"
    _log("faithfulness: writing 评价 (report ↔ ARA)")
    prompt = (
        "你在为一篇中文科普报告写一段简短「忠实性评价」(给读者看)。已验证知识包(ARA)是真值。"
        "只点出会让读者**实质误导**的地方:把某系统的指标安到别的系统、夸大到 ARA 不支持、"
        "或与 ARA 矛盾。不要挑措辞/取整/定性表达。机器已另行核出"报告里不在 ARA 的数字":"
        f"{nums}——你不必复述这串,只在它们确实造成误导时点评。\n"
        "用 2-4 句中文,客观、给读者拿捏。若整体忠实,就说整体与知识包一致。\n\n"
        "=== 已验证 ARA ===\n" + ara_text + "\n=== END ARA ===\n\n"
        "=== 报告 ===\n" + report_text + "\n=== END 报告 ==="
    )
    try:
        note = _ask_text(prompt, seam="faithfulness", tier="fast", timeout=600.0, effort="medium")
    except Exception as exc:  # noqa: BLE001 — 永不拦:任何 seam 故障都降级为中性句
        _log(f"faithfulness: seam error, neutral note: {exc}")
        return "(判官不可用,本节仅含机器核对结果。)"
    return note.strip() or "整体与已验证知识包一致。"
```

- [ ] **Step 5: 更新 `build_seams`** — `faithfulness_judge` 仍以同名导出(签名变了,但 key 不变),确认返回 dict 里 `"faithfulness_judge": faithfulness_judge` 不动。

- [ ] **Step 6: 跑 + lint + commit**

```bash
uv run pytest tests/llm/ -q
uv run ruff check .claude/skills/paper-landscape/scripts/llm/ tests/llm/
git add .claude/skills/paper-landscape/scripts/llm/seams.py tests/llm/test_seams.py
git commit -m "feat(llm): faithfulness_judge writes a 评价 note (prose), fail-soft, never blocks (ADR-0012 rev)"
```

---

## Chunk 2: 合成「评价」首节 + 移除硬拦

### Task 3: `build_assessment` + 两条路径前置首节,删 `check_report_faithfulness`/`AnchorGateError`(忠实)

**Files:**
- Modify: `branch1_gate.py`(加 `build_assessment`,删 `check_report_faithfulness`)
- Modify: `branch1_llm.py`(`:304-318` 改)、`branch1_report.py`(`:250-262` 改)
- Test: `tests/output/test_branch1_gate.py`、`tests/output/test_branch1.py`

- [ ] **Step 1: 写失败测试**(branch1_gate):

```python
def test_build_assessment_is_facts_plus_note_never_raises(tmp_path) -> None:
    from scripts.output.branch1_gate import build_assessment
    (tmp_path / "logic").mkdir(parents=True)
    (tmp_path / "logic" / "claims.md").write_text("**Statement**: reaches 28.4", encoding="utf-8")
    (tmp_path / "PAPER.md").write_text("28.4", encoding="utf-8")
    report = "本文达到 28.4,另有 99.9。"
    def fake_judge(report_text, ara_dir, *, ungrounded=None):
        return "整体与知识包一致;99.9 未在知识包出现,读者留意。"
    md = build_assessment(report, tmp_path, judge=fake_judge)
    assert md.startswith("## 评价")
    assert "99.9" in md          # (b) 机器事实写死
    assert "整体与知识包一致" in md  # 判官语义
    # judge=None 也不抛、仍有机器事实
    md2 = build_assessment(report, tmp_path, judge=None)
    assert "## 评价" in md2 and "99.9" in md2
```

- [ ] **Step 2: 运行确认失败** — `uv run pytest tests/output/test_branch1_gate.py::test_build_assessment_is_facts_plus_note_never_raises -q` → FAIL。

- [ ] **Step 3: 在 `branch1_gate.py` 加 `build_assessment`,删 `check_report_faithfulness`**

删除整个 `check_report_faithfulness`(`:87-170`)。**随之删掉它独占的 import**(Task 1 故意留到这里删):`from scripts.output.anchor_lint import lint_text`、`from scripts.audit.types import Finding, Severity`、以及 `:11` 的 `from collections.abc import Callable`(仅 `check_report_faithfulness` 的 `judge: Callable[...]` 形参用过)。删后 `uv run ruff check` 验无 F401/F821(grep 确认这四个符号在 `branch1_gate.py` 内已无其他引用)。新增:
```python
def _read_audit_flags(ara_dir: Path) -> str:
    """ARA 自身在数字门 tolerant 下记下的存疑数字(若有),供「评价」一并披露。"""
    f = ara_dir / "AUDIT_FLAGS.md"
    return f.read_text(encoding="utf-8").strip() if f.exists() else ""


def build_assessment(report_text: str, ara_dir: "Path", *, judge=None) -> str:
    """branch1 开篇「评价」(ADR-0012 rev)— 永不抛、永不拦。
    机器确定性事实((b) 未落源数字 + 数字门 AUDIT_FLAGS)+ 判官语义点评,合成 `## 评价` 块。"""
    ungrounded = ungrounded_report_numbers(report_text, ara_dir)
    note = ""
    if judge is not None:
        try:
            note = str(judge(report_text, ara_dir, ungrounded=ungrounded)).strip()
        except Exception:  # noqa: BLE001 — 评价永不拦
            note = ""
    lines = ["## 评价", ""]
    if note:
        lines += [note, ""]
    if ungrounded:
        lines.append(
            "> 机器核对:以下正文数字未在已验证知识包(ARA)中找到,读者请留意——"
            + "、".join(ungrounded) + "。"
        )
    else:
        lines.append("> 机器核对:正文数字均可在已验证知识包(ARA)中对应。")
    flags = _read_audit_flags(ara_dir)
    if flags:
        lines += ["", "> 知识包自身另有数字门标记的存疑项(详见 ai_package 的 AUDIT_FLAGS.md)。"]
    return "\n".join(lines) + "\n"
```
> `judge` 的签名是 `(report_text, ara_dir, *, ungrounded)`(Task 2)。`Path` 已在文件 import。

**同时把 `_prepend_assessment` 也放进 `branch1_gate.py`(两条路径共用,避免两份漂移实现):**
```python
def _prepend_assessment(report: str, assessment: str) -> str:
    """把 `## 评价` 块插到 `# 标题` + 导读 blockquote 之后、首个内容之前。两条 branch1 路径共用。"""
    lines = report.splitlines()
    i = 0
    while i < len(lines) and not lines[i].startswith("# "):  # 跳到 H1
        i += 1
    i += 1
    while i < len(lines) and (not lines[i].strip() or lines[i].lstrip().startswith(">")):  # 跳空行+导读 >
        i += 1
    head, tail = lines[:i], lines[i:]
    return "\n".join(head) + "\n\n" + assessment.rstrip() + "\n\n" + "\n".join(tail) + "\n"
```

- [ ] **Step 4: LLM 路径前置首节,删硬拦** — `branch1_llm.py`

OLD(`:302-318`):
```python
    assembled = _strip_emoji("\n".join(parts) + "\n")  # no-emoji iron rule
    assembled = _quote_mermaid_labels(assembled)  # make LLM mermaid parse-safe
    report = _ground_report(assembled, md_text)
    hard = check_report_faithfulness(
        report, md_text, ara_dir, judge=faithfulness_judge,
        tolerant=report_tolerant, max_unconfirmed=report_max_unconfirmed,
        max_unconfirmed_ratio=report_max_unconfirmed_ratio,
    )
    if hard:
        raise AnchorGateError(
            "branch1 (LLM) report failed 忠实门 (ADR-0012): "
            + "; ".join(f.observation for f in hard[:5])
        )
```
NEW(去掉 `_ground_report`——见 Task 4;先合成正文,再把「评价」前置为首节):
```python
    assembled = _strip_emoji("\n".join(parts) + "\n")  # no-emoji iron rule
    assembled = _quote_mermaid_labels(assembled)  # make LLM mermaid parse-safe
    body = assembled
    assessment = build_assessment(body, ara_dir, judge=faithfulness_judge)
    # 「评价」紧跟标题/导读 blockquote 之后作为首节;正文其余不变。
    report = _prepend_assessment(body, assessment)
```
更新 import(`branch1_llm.py:27-29`)——用 branch1_gate 的共用 `_prepend_assessment`,不在本文件再写一份:
```python
from scripts.output.branch1_gate import _prepend_assessment, build_assessment
```
> 删去 `check_report_faithfulness` import。`AnchorGateError` 的 import 去留**由 Task 6 Step 1 终结**:Task 6 把图形完整性的 `raise AnchorGateError` 改成 flag 后,本文件不再 raise 它 → 同时删掉 `from scripts.output.branch1_report import AnchorGateError`(否则 ruff F401)。`faithfulness_judge` 形参仍在(上游透传)。`report_tolerant/max_unconfirmed/ratio` 形参变未用 → **从签名删,并同步整条调用级联**(精确清单见 Task 6 Step 0)。

- [ ] **Step 5: 确定性路径同样前置** — `branch1_report.py::write_branch1`

OLD(`:248-262`):
```python
    report = "\n".join(sections) + "\n"

    hard = check_report_faithfulness(
        report, md_text, ara_dir, judge=faithfulness_judge,
        tolerant=report_tolerant, max_unconfirmed=report_max_unconfirmed,
        max_unconfirmed_ratio=report_max_unconfirmed_ratio,
    )
    if hard:
        raise AnchorGateError(
            "branch1 report failed 忠实门 (ADR-0012): " + "; ".join(f.observation for f in hard[:5])
        )
```
NEW(用 branch1_gate 的共用 `build_assessment` + `_prepend_assessment`,**无占位行**):
```python
    body = "\n".join(sections) + "\n"
    assessment = build_assessment(body, ara_dir, judge=faithfulness_judge)
    report = _prepend_assessment(body, assessment)
```
顶部 import 改:`from scripts.output.branch1_gate import _prepend_assessment, build_assessment`(删 `check_report_faithfulness`)。
> 同步删 `write_branch1` 的 `report_tolerant/max_unconfirmed/ratio` 未用形参——级联清单见 Task 6 Step 0。

- [ ] **Step 6: 跑受影响测试 + 改旧测**

旧测里凡断言"未落源数字 → `AnchorGateError`/hard-block"的(`test_branch1_gate.py` 的 `test_gate_blocks_*`、`test_branch1.py::test_deterministic_path_honors_a_supplied_judge`)**改写**为新语义:不抛错、`## 评价` 含相应机器事实/判官点评。
Run: `uv run pytest tests/output/ -q` → 修到 PASS。

- [ ] **Step 7: lint + commit**

```bash
uv run ruff check .claude/skills/paper-landscape/scripts/output/ tests/output/
git add .claude/skills/paper-landscape/scripts/output/ tests/output/
git commit -m "feat(branch1): assemble opening 评价 (facts + judge note), drop the faithfulness hard-block (ADR-0012 rev)"
```

---

### Task 4: 退役核心结论块 + stray 锚定

**Files:** Modify `branch1_llm.py`;Test `tests/output/test_branch1.py` / `test_branch1_llm.py`

- [ ] **Step 1: 写测试** — 报告里**不再出现** `<!--ref` 锚点:
```python
def test_report_carries_no_ref_anchors(tmp_path, candidate, analysis, md_path):
    from scripts.output.branch1_report import write_branch1
    from scripts.output.branch2_ara import write_branch2
    ara = tmp_path / "ara"; write_branch2(ara, candidate, analysis)
    person = tmp_path / "person"; write_branch1(person, candidate, ara, md_path, analysis)
    assert "<!--ref" not in (person / "report.md").read_text(encoding="utf-8")
```
- [ ] **Step 2: 运行确认失败**(当前核心结论块带锚点)。
- [ ] **Step 3:(LLM 路径)`_claims_block` 去锚定** — `branch1_llm.py::_claims_block` 删 `for n in _NUM.findall(...) ... sentence += _anchor(window)` 循环;`out` 的"隐形锚点"提示句改为普通说明或删。结论行 `out.append(f"{i}. {sentence}")` 保留(无锚点)。
- [ ] **Step 3b:(确定性路径)`_body_with_anchors` 去锚定** — **关键:确定性路径的锚点不在 `_claims_block`,而在 `branch1_report.py::_body_with_anchors`(:163-188)**。删其 `nums = re.findall(...)` 后的 `for n in nums: window = _find_in_md(md_text, n); if window: sentence += _anchor(window)` 循环(`:176-179` 一带),令 `## 摘要翻译` 不带锚点。测试 Task 4 Step 1 跑的是**确定性 `write_branch1`**,故没有这步该测必挂(workflow MAJOR)。
- [ ] **Step 4: 删 `_ground_report` 调用与定义 + 死的锚点辅助** — `write_branch1_llm` 不再调 `_ground_report`(Task 3 已去);删 `branch1_llm.py` 的 `_ground_report`/`_ground_line` 定义 + `_is_empirical_assertion` import。**`_anchor`/`_find_in_md`**:Step 3 + 3b 之后,`branch1_llm` 不再用(删其 import);`branch1_report.py` 里 `_anchor`/`_find_in_md` 若仅服务 `_body_with_anchors`(grep 确认 `_mermaid_redraw` 等不依赖)则一并删定义。每删一个 import/def 后 `uv run ruff check` 验证无 F401/未定义。
- [ ] **Step 5: 跑测试** — `uv run pytest tests/output/ -q` PASS(改掉断言 `classDef`/anchors 的旧测)。
- [ ] **Step 6: lint + commit** `git commit -m "feat(branch1): retire core-block + stray <!--ref--> anchoring (ADR-0012 rev)"`

---

## Chunk 3: 退役 G3 锚点解析 + 移除 branch1 失败路径

### Task 5: G3 去掉 branch1 anchor-resolution 子检查

**Files:** Modify `scripts/audit/g3_seal.py`(`:103-118` 的 `check_branch1_md_anchors`);Test `tests/audit/test_g3_seal.py`

- [ ] **Step 1: 写真正穿过删除点的回归测试** — **注意**:一份"无锚点"的报告在删除前就已 PASS(`check_branch1_md_anchors` 只 flag *已存在但解析不了* 的锚点),所以"无锚点不被拦"验证不到行为变化。必须构造一份**带不可解析 `<!--ref-->` 锚点**的 report.md,断言**删子检查后 G3 不再 block**(其余 entailment/rigor/equation 仍正常):
```python
def test_g3_no_longer_blocks_on_unresolvable_branch1_anchor(tmp_path):
    # ADR-0012 rev:G3 退役 branch1 锚点解析。带"源 MD 里找不到的锚点引文"的报告,
    # 过去会被 (a) 子检查 hard-block,现在不应再因此 block。
    # (用既有 test_g3_seal fixtures 造一份 good ARA + entailment/rigor/equation 都过的场景,
    #  仅在 report.md 注入一个 <!--ref:quote:NONEXISTENT--> 锚点。)
    ...  # 复用 test_g3_seal.py 既有 _build_paper 辅助,report.md 注入不可解析锚点
    verdict = run_g3(...)
    assert verdict.blocked is False  # run_g3 verdict 暴露 .blocked;不再因锚点解析被拦
```
- [ ] **Step 2: 删既有反向测** — 删除/改写 `tests/audit/test_g3_seal.py::test_run_g3_blocks_on_unresolvable_branch1_anchor`(它断言的正是被退役的行为)及其 `_build_paper(good=False)` 分支(见测试迁移地图)。运行确认新测在删代码前**失败**(它依赖删除点生效)。
- [ ] **Step 3: 删 (a) 子检查(精确行)** — `g3_seal.py`:删 `:24` 的 `from scripts.audit.anchor_resolution import check_branch1_md_anchors`;删 `:108` 的 `findings.extend(check_branch1_md_anchors(report_md, md_path).findings)`。**保留**"report.md 缺失 → 硬错"那半(`:109-121` 一带);把 `if report_md.exists(): <extend> else: <missing-hard>` 简化为只剩 missing-hard 分支(报告存在时无 anchor 检查)。读 `:100-121` 精确切割。
- [ ] **Step 4: 跑** `uv run pytest tests/audit/ -q` PASS;`uv run ruff check` 无 F401(anchor_resolution import 已删)。
- [ ] **Step 5: commit** `git commit -m "feat(audit): G3 drops the branch1 anchor-resolution sub-check (ADR-0012 rev)"`

---

### Task 6: 移除 branch1 硬拦/现场/复活根 + 图形完整性改 flag

**Files:** `branch1_llm.py`、`branch1_report.py`、`produce.py`、`spoke.py`、`revival.py`;Tests 见迁移地图。
**核心不变量(落地后必须成立)**:退役锚点解析后,**唯一**仍以 `report.md` 为根的 G3 硬错是 **G3R0(report.md 缺失)**(`g3_seal` 的该 finding `target=str(report_md)` 仍以 `report.md` 结尾)。因此:
- `spoke._classify` 与 `revival._classify_roots` **都保留** `target.endswith("report.md") → branch1` 臂(**仅**服务 G3R0)。
- branch1-reemit / branch1 复活**仅由 G3R0 触发**(即"最终门 + branch1 in roots"),不再由已退役的 `锚点门` 或锚点解析触发。
- 其余 G3 硬错(entailment/rigor/equation)根在 ARA → 重跑 branch2。
**两侧(spoke/revival)处置必须对称**:删了一侧的 branch1 臂会让 G3R0 在另一侧被误判(revival 会落 ingest 桶 → 早退 manual,破坏可恢复的"缺报告"复活)。

- [ ] **Step 0: 删除 `report_tolerant/report_max_unconfirmed/report_max_unconfirmed_ratio` 整条调用级联(caller-first,一次成组)** — 这三个 kwarg 3 层透传,只删叶子会让中间层 `TypeError`。逐处删:
  1. `spoke.py:187-189` → `produce_outputs(...)` 的传参(源自 `g2_tolerant/g2_max_unconfirmed`)。
  2. `produce.py` `produce_outputs` 形参(`:299-301`)+ 它转发给 `stage_branch1` 的调用(`:381-383`)。
  3. `produce.py` `stage_branch1` 形参(`:173-175`)+ 两处转发(`:218-220` LLM、`:232-234` 确定性)。
  4. `revival.py` 两处 `stage_branch1(...)` 调用(`:309-311`、`:344-346`)。
  5. `branch1_llm.py::write_branch1_llm` 与 `branch1_report.py::write_branch1` 形参(Task 3 已标)。
  验证:`grep -rn "report_tolerant\|report_max_unconfirmed" .claude/skills/paper-landscape/scripts/ tests/` 在已删代码外**零命中**。
- [ ] **Step 1: 图形完整性改 flag(branch1 永不抛)** — `branch1_llm.py:319-331` 三处 `raise AnchorGateError`(missing selected figures / mandatory arch figure)改为:把缺失信息**追加进 `## 评价`**(或 log)、续跑、不抛。改完本文件不再 raise `AnchorGateError` → **删 `branch1_llm.py` 顶部 `from scripts.output.branch1_report import AnchorGateError`**(ruff 验 F401)。测改(见迁移地图 test_branch1_llm 行):`:161/167` 从 `pytest.raises(AnchorGateError)` 改为断言报告写出 + `## 评价` 含缺图提示;改完文件内已无 AnchorGateError 用例 → **删 `:11` 的 `from scripts.output.branch1_report import AnchorGateError`**(ruff F401);另 `:52` 的 `assert "<!--anchor:" in report` 改 `not in`(Task 4 退役锚点)。
- [ ] **Step 2: `produce.py`(两处)** — (a) 删 `stage_branch1` 的 judge 守卫 `if write_report is not None and faithfulness_judge is None: raise ValueError(...)`;(b) 删 `stage_branch1` 的 `except AnchorGateError as exc: exc.staged_dir = ...; raise`(`:236` 一带);(c) **从 `:402` 的 `except (StructuralSealFailed, ProduceGateBlocked, AnchorGateError):` 元组里去掉 `AnchorGateError`**(branch1 不再产生它)。保留 `EngineAbort`/`StructuralSealFailed`/`ProduceGateBlocked`。grep 确认 produce 内 `AnchorGateError` 仅服务 branch1 后,删其 import。测删:`tests/output/test_produce.py::test_llm_writer_without_faithfulness_judge_aborts_loudly`(守卫专测,见迁移地图)。
- [ ] **Step 3: `spoke.py`(两处 handler + G3-reemit 决策)** — (a) 删 `except AnchorGateError as exc: ... _pre_promote_scene(failed_gate="锚点门", ...)`(`:287-295`);(b) **第二处** `except (StructuralSealFailed, ProduceGateBlocked, AnchorGateError)`(`:426-437`,G3 re-emit 路径)去掉 `AnchorGateError` + 删 `:436` 的 `{'AnchorGateError': '锚点门'}` 映射项 + `:377` 的相关注释;(c) **G3-reemit 的 branch1 分支(`_classify` :364 `report.md→branch1`、`_reemit_for_g3` :393 `prior_failure_branch1`)**:落地后唯一仍以 report.md 为根的 G3 硬错是"report.md 缺失"(G3R0,Task 5 保留)——**决策:保留这条 branch1-reemit 仅服务 G3R0**(缺报告时重跑 branch1),其余 branch1 触发已不存在;在代码注释里写明。两处 handler 都去掉 `AnchorGateError` 后,删 `from scripts.output.branch1_report import AnchorGateError`(`:41`,grep 确认无他用)。测删/改:`test_g3_branch1_reemit_hits_anchor_lands_scene`、`test_g3_branch1_root_reuses_branch2`、`test_spoke_branch1_blocks_on_judge_drift`(见迁移地图)。
- [ ] **Step 4: `revival.py`(对称保留 G3R0,删退役触发)** — (a) `_classify_roots`(`:51-69`)**保留** `target endswith 'report.md' → 'branch1'` 臂(服务 G3R0,与 spoke 对称);(b) `_revive_one` 的 `use_branch1` 门(`:254-258`)**改为仅** `failed_gate == '最终门' and 'branch1' in roots`——**删掉已退役的 `failed_gate == '锚点门'` 析取项**(branch1 不再产 锚点门 场景),**保留** branch1-only 复用分支(`:295-312`)服务 G3R0;(c) 删外层 `except AnchorGateError as exc: ... '锚点门'`(`:415-418`,锚点门已退役);(d) 删 `:27` 的 `from scripts.output.branch1_report import AnchorGateError`(grep 确认无他用)。保 branch2 重跑 + G2 盲重试 + ingest 根。读 `:51-71` + `:214-346` + `:410-420` 精确切割。
- [ ] **Step 5: `AnchorGateError` 类去留** — Step 1-4 后,grep `AnchorGateError` 全仓:若已**无任何 raise/except**,把 `branch1_report.py:41` 的 `class AnchorGateError` 标注为死代码(本计划保留定义、不删类,符合"留死代码"策略;如要删另起)。在计划/提交信息里写明最终处置。
- [ ] **Step 6: 全量跑** `uv run pytest -q` → 按**测试迁移地图**逐一改写/删除既有测(branch1 失败语义、judge dict、AnchorGateError、守卫、锚点解析);Expected green。
- [ ] **Step 7: lint(引擎+tests)+ commit** `git commit -m "feat(branch1): never hard-block — remove AnchorGateError path, _failed scene, revival root, tolerant cascade (ADR-0012 rev)"`

---

## 验收(全计划完成后)

- `uv run pytest` 全绿;`uv run ruff check .claude/skills/paper-landscape/scripts/ tests/` 干净。
- 报告产物含 `## 评价` 首节;`grep -c "<!--ref" person_vault/*/report.md` = 0(新产出)。
- branch1 在任何忠实性/锚点/图形问题下**都不再** raise / 进 `_failed/`。
- ARA 侧 `run_g2` / 结构门 / G3 的 entailment/rigor/equation **行为不变**(对照测试)。
- `config/llm.yaml: faithfulness → claude-code` 不变(判官写「评价」用 haiku)。

## 风险 / 已知边界

- **判官写的「评价」可能本身不准**:但它不拦,且数字事实是机器写死的;最坏是开篇点评措辞偏差,读者可对照 ARA。可后续多模型/投票加固(本计划不做)。
- **图形完整性降级为 flag**:缺核心架构图的报告会照常发布(带提示),不再硬拦——符合"人稿不设硬门",但确属质量放宽,记录在案。
- **anchor_lint / anchor_resolution 变死代码**:本计划只断调用、不删文件(单测仍在);如需删文件另起清理任务。
