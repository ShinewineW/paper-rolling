# ARA 删除安全(失败现场单向汇)实现计划

> **日期**: 2026-06-12
> **状态**: 活跃
> **作者**: ShinewineW（+ Claude Opus 4.8）
> **基准版本**: `paper-rolling@76faef7`
> **目的**: 落实 ADR-0011 —— 任何代码路径都不得反射式 `rm` 一个已生成的 ARA;失败/abort 时一律移入 `_failed/`，而"本就该删的"（可再生临时物 / person_vault / 空壳孤儿）不受影响。
> 范围: `scripts/paths.py`、`scripts/output/produce.py`、`scripts/spoke.py`、`scripts/ledger/store.py` + 对应 tests。

---

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让"失败就删 ARA"的几处路径改为"失败就把 ARA 移进 `_failed/`"，token-expensive 的 ARA 永不无声蒸发，而廉价/空壳目录照常删。

**Architecture:** 引入一个纯路径 litmus `ara_is_nonempty(ara_dir)`（`paths.py`，LLM-agnostic 核心），所有删除站点用它区分"含非空 ARA → 移现场" vs "不含 → 照常 rm"。两个真缺口：(A) `produce_outputs` 的 `finally` 在 `EngineAbort`（如 Qwen 审计端点掉线）时删掉刚建好的 staged ARA；(B) `ledger` 的 `consistency_check` / `crash_resume_sweep` 对 `ai_package` 孤儿无条件 rm。门控失败三条路径（结构门/数字门/锚点门）**已经**通过 `write_scene` 保留现场，无需改。

**Tech Stack:** Python 3.x、pytest、`uv run pytest`、ruff。复用既有 `scripts/failure_scene.py::write_scene`（已实现"原子换入 + 最新覆盖 + 内存快照防丢"）。

---

## 前置事实（已验证，落地前先读这几处）

- `paths.py`：已含 `EngineAbort`、`VAULT_BRANCHES`、`AI_PACKAGE_DIRNAME`、`PERSON_VAULT_DIRNAME`。litmus 放这里零新依赖。
- `failure_scene.py`：`FAILED_REL = Path("_failed")`；`write_scene(*, workspace, key, ledger_key, failed_gate, findings, engine_commit, candidate, md_path, content_list_path, analysis, staged_dir)` 已做原子换入 + append attempts。
- `produce.py:351-359`：`except (StructuralSealFailed, ProduceGateBlocked, AnchorGateError)` 设 `handed_off=True` 保留 staging；`EngineAbort` **不在**元组里 → `finally` 删 staging（缺口 A）。
- `spoke.py`：`content_list_path`（行 134）、`cand_key = _candidate_key(candidate)`（行 198）、`current_commit`、`write_scene`、`ing.md_path` 在 g2_round 循环处均在作用域。g2_round 循环 235-269 已 catch 三种门异常。
- `store.py`：`from scripts import paths` 已在；`consistency_check`（268-307）与 `crash_resume_sweep`（245-264）对 `ai_package` 孤儿/非 done 路径无条件 `shutil.rmtree`（缺口 B）。
- **不改项（已验证）**：`identity_base`（naming.py:59）在 ids 全空时 `raise ValueError`，故 `find_existing_entries` 的 `endswith(f"_{idbase}")` 不会退化成 match-all → idbase footgun 结构上不存在，依 *No Over-Defensive Code* 不加守卫。（**Codex R1 修订**：`spoke.py:393-412` 的 G3 re-emit 处置原标"无需改"是错的 —— 它是 `rm`-before-`write_scene`，违反本计划自己的 scene-before-rm 规则，且 ADR-0011 明列它为 reflex-rm 站点；G3 段的 `try` 也漏 catch `EngineAbort`。两者均在 Task 2 Step 8/9 修复。）

---

## Task 1: `ara_is_nonempty` litmus（共享原语）

**Files:**
- Modify: `.claude/skills/paper-landscape/scripts/paths.py`（在 `repo_root()` 之前插入）
- Test: `tests/test_paths_ara_litmus.py`（新建）

- [ ] **Step 1: 写失败测试**

```python
# tests/test_paths_ara_litmus.py
from scripts.paths import ara_is_nonempty


def test_nonempty_ara_dir_true(tmp_path):
    ara = tmp_path / "ara"
    (ara / "logic").mkdir(parents=True)
    (ara / "PAPER.md").write_text("x", encoding="utf-8")
    assert ara_is_nonempty(ara) is True


def test_empty_ara_dir_false(tmp_path):
    ara = tmp_path / "ara"
    ara.mkdir()
    assert ara_is_nonempty(ara) is False


def test_missing_ara_dir_false(tmp_path):
    assert ara_is_nonempty(tmp_path / "ara") is False


def test_dir_with_only_empty_subdir_false(tmp_path):
    ara = tmp_path / "ara"
    (ara / "logic").mkdir(parents=True)  # 子目录但无文件
    assert ara_is_nonempty(ara) is False
```

- [ ] **Step 2: 跑测试确认失败**

Run: `uv run pytest tests/test_paths_ara_litmus.py -v`
Expected: FAIL — `ImportError: cannot import name 'ara_is_nonempty'`

- [ ] **Step 3: 实现 litmus**

在 `paths.py` 中 `def repo_root()` 之前插入：

```python
def ara_is_nonempty(ara_dir: Path) -> bool:
    """True iff ``ara_dir`` is an existing directory holding at least one FILE —
    the litmus for "this dir holds a token-expensive ARA worth preserving"
    (ADR-0011). An absent or file-empty ``ara/`` means nothing was built, so the
    enclosing dir is safe to hard-delete ("该删的不受影响")."""
    ara_dir = Path(ara_dir)
    return ara_dir.is_dir() and any(p.is_file() for p in ara_dir.rglob("*"))
```

- [ ] **Step 4: 跑测试确认通过**

Run: `uv run pytest tests/test_paths_ara_litmus.py -v`
Expected: PASS（4 passed）

- [ ] **Step 5: lint + commit**

```bash
uv run ruff check .claude/skills/paper-landscape/scripts/paths.py
git add .claude/skills/paper-landscape/scripts/paths.py tests/test_paths_ara_litmus.py
git commit -m "feat(paths): ara_is_nonempty litmus for ADR-0011 delete safety"
```

---

## Task 2: abort 时保留刚建好的 ARA（缺口 A，头号修复）

`produce_outputs` 在 `EngineAbort` 且 staging 已含 ARA 时，把 `staging` 挂到异常上并 `handed_off=True`（不让 finally 删）；`spoke` 的 g2_round 循环 catch `EngineAbort`，用现场写入器保留，再**重新抛出**（tick 仍中止，成本护栏不变）。

**Files:**
- Modify: `.claude/skills/paper-landscape/scripts/output/produce.py`（import + `except` 块）
- Modify: `.claude/skills/paper-landscape/scripts/spoke.py`（import + g2_round 循环 except 链）
- Test: `tests/output/test_produce.py`（追加）

- [ ] **Step 1: 写失败测试（produce 层：abort 后 staging 不被删、且挂到异常上）**

追加到 `tests/output/test_produce.py`（复用该文件既有的 ledger fake / candidate fixture 风格；下面用 monkeypatch 让 ARA 树「建成且过 Seal-1」，避免依赖真分析 bundle）：

```python
import pytest
from pathlib import Path
from scripts.paths import EngineAbort
import scripts.output.produce as produce_mod


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
            md, candidate, _Ledger(), root=tmp_path,
            resolve_analysis=lambda *a, **k: {"ok": 1},
            g2_gate=abort_gate,
        )
    staged = getattr(ei.value, "staged_dir", None)
    assert staged is not None, "EngineAbort must carry staged_dir when an ARA was built"
    assert (Path(staged) / "ai" / "ara" / "PAPER.md").exists(), "built ARA must survive the abort"


def test_engineabort_before_ara_built_still_cleans(tmp_path, monkeypatch):
    # analyzer transport down → ARA 没建 → staging 无 ARA → 仍然清理，不挂 staged_dir。
    md = tmp_path / "x.md"; md.write_text("src", encoding="utf-8")
    candidate = {"title": "T", "arxiv_id": "2509.00002", "doi": None}

    class _Ledger:
        def intake_date(self):
            import datetime
            return datetime.date(2026, 6, 12)

    def abort_resolve(*a, **k):
        raise EngineAbort("analyzer backend down")

    with pytest.raises(EngineAbort) as ei:
        produce_mod.produce_outputs(
            md, candidate, _Ledger(), root=tmp_path,
            resolve_analysis=abort_resolve, g2_gate=lambda _x: None,
        )
    assert getattr(ei.value, "staged_dir", None) is None
```

- [ ] **Step 2: 跑测试确认失败**

Run: `uv run pytest tests/output/test_produce.py::test_engineabort_after_ara_built_preserves_staging -v`
Expected: FAIL —— `staged_dir` 为 None（当前 finally 已删 staging）。

- [ ] **Step 3a: 改 `produce.py` —— import EngineAbort + litmus**

`produce.py` 顶部 import 区（`from scripts.output.naming import find_existing_entries, vault_key` 之后）新增一行：

```python
from scripts.paths import EngineAbort, ara_is_nonempty
```

- [ ] **Step 3b: 改 `produce.py` —— except/finally 块**

把 `produce_outputs` 结尾（当前 351-359）的 OLD 替换为 NEW：

OLD:
```python
    except (StructuralSealFailed, ProduceGateBlocked, AnchorGateError):
        # A gate hard-failed: its exception carries `staging` (the failure scene),
        # so do NOT let `finally` delete it. SpokeCancelled + success keep this
        # False, so their staging is still cleaned up (no temp leak).
        handed_off = True
        raise
    finally:
        if not handed_off:
            shutil.rmtree(staging, ignore_errors=True)
```

NEW:
```python
    except (StructuralSealFailed, ProduceGateBlocked, AnchorGateError):
        # A gate hard-failed: its exception carries `staging` (the failure scene),
        # so do NOT let `finally` delete it. SpokeCancelled + success keep this
        # False, so their staging is still cleaned up (no temp leak).
        handed_off = True
        raise
    except EngineAbort as exc:
        # ADR-0011: a transport abort (e.g. the Qwen audit endpoint dropped) must
        # NOT let `finally` delete a built-but-unverified ARA. If the staged branch2
        # ARA exists, hand `staging` to the spoke (which scenes it) via the same
        # `staged_dir` attribute the gate exceptions use, then re-raise so the tick
        # still aborts (cost guard unchanged). An abort BEFORE the ARA is built
        # (analyzer transport down) leaves no ARA → fall through to the finally rm.
        if ara_is_nonempty(staging / "ai" / "ara"):
            exc.staged_dir = staging
            handed_off = True
        raise
    finally:
        if not handed_off:
            shutil.rmtree(staging, ignore_errors=True)
```

- [ ] **Step 4: 跑 produce 测试确认通过**

Run: `uv run pytest tests/output/test_produce.py -k engineabort -v`
Expected: PASS（2 passed）

- [ ] **Step 5: 改 `spoke.py` —— import EngineAbort**

`spoke.py:48` 的 OLD → NEW：

OLD:
```python
from scripts.paths import FAILURE_AUDIT_BLOCK, FAILURE_CONVERT_ERROR
```

NEW:
```python
from scripts.paths import FAILURE_AUDIT_BLOCK, FAILURE_CONVERT_ERROR, EngineAbort
```

- [ ] **Step 6: 改 `spoke.py` —— 定义 `_abort_scene` 现场写入器（DRY，g2 + G3 两处复用）**

在 `_pre_promote_scene` 定义**之后**、g2_round 循环（235）**之前**，于 `spoke()` 函数体内新增本地 helper（同缩进；它引用的 `cand_key`/`ing`/`content_list_path`/`candidate`/`workspace`/`current_commit`/`write_scene` 在此处均已在作用域）：

```python
        def _abort_scene(exc) -> None:
            # ADR-0011: a transport abort (EngineAbort) anywhere in produce / G3 may
            # carry a built-but-unverified staged ARA (produce_outputs attached
            # `staged_dir`). Scene it so the paid-for ARA survives for debug; the
            # caller then RE-RAISES so the tick still aborts (cost guard unchanged).
            # No staged_dir (abort before the ARA was built) → nothing to preserve.
            staged = getattr(exc, "staged_dir", None)
            if staged is None:
                return
            write_scene(
                workspace=workspace,
                key=cand_key,
                ledger_key=cand_key,
                failed_gate="传输中断",
                findings=[{"target": "ara", "observation": str(exc)}],
                engine_commit=current_commit(workspace),
                candidate=candidate,
                md_path=ing.md_path,
                content_list_path=content_list_path,
                analysis=None,
                staged_dir=staged,
            )
```

- [ ] **Step 7: 改 `spoke.py` —— g2_round 循环追加 except EngineAbort**

在 g2_round 循环的 `except AnchorGateError as exc:` 处理块**之后**、`assert produced is not None` 之前，追加（与其它 except 同缩进，属于同一个 `try`，行 236 的 try）：

```python
            except EngineAbort as exc:
                # ADR-0011: pre-promote transport abort with a built ARA → scene it,
                # then re-raise (tick still aborts; cost guard unchanged).
                _abort_scene(exc)
                raise
```

> 注：给 g2_round 的 `try` 加一个 except，**不是**新开 try。`break`/`continue`/其它 except 不变。

- [ ] **Step 8: 改 `spoke.py` —— G3 段同样覆盖 EngineAbort（Codex R1 Finding 2）**

G3 的 `try`（行 369）当前只 catch `_Unfixable` + 三种门异常 —— `EngineAbort`（来自 re-emit 的 `_attempt()`，经 `run_with_budget → on_reemit → _reemit_for_g3`）**漏网**，会把 re-emit 已建好的 staged ARA 遗留在 `/tmp`、不入 `_failed/`。在 `except _Unfixable as exc:`（行 384）**之前**追加（同 `try`，同缩进）：

```python
        except EngineAbort as exc:
            # ADR-0011 (Codex R1): an EngineAbort during a G3 re-emit's _attempt()
            # carries the re-emit's built staged ARA — scene it, then re-raise so the
            # tick still aborts. Without this the staged ARA is orphaned in /tmp.
            _abort_scene(exc)
            raise
```

- [ ] **Step 9: 改 `spoke.py` —— G3 re-emit 失败处置改为 scene-before-rm（Codex R1 Finding 1）**

把 G3 re-emit 下游门失败处置（行 387-412）从「先 rm `produced.*` 再 `write_scene`」**重排为「先 `write_scene` 再 rm」**，使一次 `write_scene` 异常不会两头空（若 `write_scene` 抛错，`produced.*` 残留，下个 tick 的 `consistency_check`（Task 3）会保住它）。

OLD（行 387-412）:
```python
        except (StructuralSealFailed, ProduceGateBlocked, AnchorGateError) as exc:
            # A re-emitted branch hit its own downstream gate before re-promotion.
            # `produced` still points at the PRIOR round's promoted product (the
            # _on_g3_reemit assignment never completed) — remove it so a G3-failed
            # product never lingers in the vault, then land the matching scene from
            # the re-emit's staged_dir (audit R3 Finding 1).
            shutil.rmtree(produced.person_path, ignore_errors=True)
            shutil.rmtree(produced.ai_path, ignore_errors=True)
            gate = {
                "StructuralSealFailed": "结构门",
                "ProduceGateBlocked": "数字门",
                "AnchorGateError": "锚点门",
            }[type(exc).__name__]
            write_scene(
                workspace=workspace,
                key=produced.key,
                ledger_key=cand_key,
                failed_gate=gate,
                findings=_findings_of(exc),
                engine_commit=current_commit(workspace),
                candidate=candidate,
                md_path=ing.md_path,
                content_list_path=content_list_path,
                analysis=None,
                staged_dir=getattr(exc, "staged_dir", None),
            )
```

NEW:
```python
        except (StructuralSealFailed, ProduceGateBlocked, AnchorGateError) as exc:
            # A re-emitted branch hit its own downstream gate before re-promotion.
            # `produced` still points at the PRIOR round's promoted product (the
            # _on_g3_reemit assignment never completed). ADR-0011 scene-before-rm:
            # land the re-emit scene FIRST, THEN remove the prior promoted product
            # from the vault — a write_scene failure can no longer lose both (and if
            # it throws, produced.* lingers and consistency_check preserves it).
            gate = {
                "StructuralSealFailed": "结构门",
                "ProduceGateBlocked": "数字门",
                "AnchorGateError": "锚点门",
            }[type(exc).__name__]
            write_scene(
                workspace=workspace,
                key=produced.key,
                ledger_key=cand_key,
                failed_gate=gate,
                findings=_findings_of(exc),
                engine_commit=current_commit(workspace),
                candidate=candidate,
                md_path=ing.md_path,
                content_list_path=content_list_path,
                analysis=None,
                staged_dir=getattr(exc, "staged_dir", None),
            )
            shutil.rmtree(produced.person_path, ignore_errors=True)
            shutil.rmtree(produced.ai_path, ignore_errors=True)
```

- [ ] **Step 10: 写 spoke 层测试（abort 进现场后 re-raise）**

新建 `tests/test_spoke_abort_scene.py`（复用 `tests/test_spoke.py` 既有 fake 工厂；勿重复造）：

```python
import pytest
from pathlib import Path
from scripts.paths import EngineAbort
from scripts.hub import _candidate_key  # 现场按 _candidate_key(candidate) 落盘，不是 candidate["key"]
# 复用 tests/test_spoke.py 的既有装配（fake http/run_cli/ingest + 能产出 ARA 的 resolve），
# 把 skeptic_votes 换成抛 EngineAbort。


def test_abort_at_g2_preserves_scene_and_reraises(spoke_with_abort_g2, candidate, workspace):
    # spoke_with_abort_g2: make_spoke(...) 但 skeptic_votes 抛 EngineAbort
    with pytest.raises(EngineAbort):
        spoke_with_abort_g2(candidate)
    scene = workspace / "_failed" / _candidate_key(candidate)  # Codex R1 F3：用 _candidate_key
    assert (scene / "scene.json").exists()
    assert (scene / "ai" / "ara").is_dir()  # 刚建好的 ARA 进了现场
```

> 实现者：按 `tests/test_spoke.py` 现有 fixture 形态补 `spoke_with_abort_g2`/`candidate`/`workspace`（skeptic 用 `def _s(*a, **k): raise EngineAbort("qwen down")`）。这一步是集成验证；若装配成本过高，可只保留 Step 1 的 produce 层单测 + 下面的 ruff，集成留给 oh-my-codex 阶段。

> **Codex R2 建议（强烈推荐补，非阻断）**：除上面的 g2-abort 测试外，再加一条 **G3 re-emit 阶段 abort** 测试 —— 这正是 Step 8 修复的回归路径。装配：让 G3 首轮失败触发 re-emit（`rigor_scores`/`entailment_judge` 首轮判失败），且 re-emit 的 `_attempt()` 内 `skeptic_votes`/`rigor` 抛 `EngineAbort` → 断言 `_failed/<_candidate_key(candidate)>/` 现场被建出（staged ARA 没遗留 `/tmp`）、异常向上传播。Step 8 是 Round 1 抓出的缺口，单独覆盖它最稳。

- [ ] **Step 11: 跑全套 + lint + commit**

Run（做了 Step 10 才带 `tests/test_spoke_abort_scene.py`，否则去掉它）:
`uv run pytest tests/output/test_produce.py tests/test_spoke.py tests/test_spoke_abort_scene.py -v`
Expected: PASS（含新 abort 测试，旧测试不回归）

```bash
uv run ruff check .claude/skills/paper-landscape/scripts/output/produce.py .claude/skills/paper-landscape/scripts/spoke.py
git add .claude/skills/paper-landscape/scripts/output/produce.py .claude/skills/paper-landscape/scripts/spoke.py tests/
git commit -m "feat(produce,spoke): preserve built ARA on EngineAbort + scene-before-rm (ADR-0011)"
```

---

## Task 3: `consistency_check` 孤儿清除不对称（缺口 B，爆炸半径最大）

`ai_package` 孤儿且含非空 ARA → 移入 `_failed/_orphans/`；`person_vault` 孤儿、空壳 `ai_package` 孤儿 → 照常 rm。

**Files:**
- Modify: `.claude/skills/paper-landscape/scripts/ledger/store.py`（import + `consistency_check` 的 (b) 段）
- Test: `tests/ledger/test_store_consistency_preserve.py`（新建）

- [ ] **Step 1: 写失败测试**

```python
# tests/ledger/test_store_consistency_preserve.py
from scripts.ledger.store import Ledger


def _make_ai_orphan(ws, name, *, with_ara):
    entry = ws / "ai_package" / name
    if with_ara:
        (entry / "ara").mkdir(parents=True)
        (entry / "ara" / "PAPER.md").write_text("x", encoding="utf-8")
    else:
        entry.mkdir(parents=True)  # 空壳
    return entry


def test_orphan_ai_with_ara_moved_not_deleted(tmp_path):
    led = Ledger(tmp_path)
    entry = _make_ai_orphan(tmp_path, "2026-06-12_T_2509.1", with_ara=True)
    # 无任何 done 行 → 它是孤儿
    led.consistency_check()
    assert not entry.exists(), "orphan must leave the vault"
    moved = tmp_path / "_failed" / "_orphans" / "2026-06-12_T_2509.1"
    assert (moved / "ara" / "PAPER.md").exists(), "ARA must be preserved, not deleted"


def test_orphan_empty_ai_still_deleted(tmp_path):
    led = Ledger(tmp_path)
    entry = _make_ai_orphan(tmp_path, "2026-06-12_T_2509.2", with_ara=False)
    led.consistency_check()
    assert not entry.exists()
    assert not (tmp_path / "_failed" / "_orphans" / "2026-06-12_T_2509.2").exists()


def test_orphan_person_vault_still_deleted(tmp_path):
    led = Ledger(tmp_path)
    entry = tmp_path / "person_vault" / "2026-06-12_T_2509.3"
    (entry / "report.md").parent.mkdir(parents=True)
    (entry / "report.md").write_text("r", encoding="utf-8")
    led.consistency_check()
    assert not entry.exists(), "person_vault orphan is cheap → still hard-deleted"
```

- [ ] **Step 2: 跑测试确认失败**

Run: `uv run pytest tests/ledger/test_store_consistency_preserve.py -v`
Expected: FAIL —— `test_orphan_ai_with_ara_moved_not_deleted`（当前被 rmtree，`_orphans` 不存在）。

- [ ] **Step 3a: 改 `store.py` —— import FAILED_REL**

`store.py` import 区（`from scripts import paths` 同侧）新增：

```python
from scripts.failure_scene import FAILED_REL
```

- [ ] **Step 3b: 改 `consistency_check` 的 (b) 段**

OLD（当前 299-307）:
```python
        # (b) prune any vault entry dir not claimed by a complete `done` row.
        for dirname, _field in paths.VAULT_BRANCHES:
            branch_dir = self.topic_dir / dirname
            if not branch_dir.exists():
                continue
            for entry in branch_dir.iterdir():
                if entry.is_dir() and entry.resolve() not in claimed:
                    shutil.rmtree(entry, ignore_errors=True)
        return demoted
```

NEW:
```python
        # (b) prune any vault entry dir not claimed by a complete `done` row.
        # ADR-0011: an ai_package orphan still holding a non-empty ARA is
        # token-expensive — MOVE it to _failed/_orphans/ (debug-preserve) rather
        # than rm. person_vault orphans (cheap, ARA-derived) and empty/garbage
        # ai_package orphans are still hard-deleted ("该删的不受影响").
        orphans_dir = self.topic_dir / FAILED_REL / "_orphans"
        for dirname, _field in paths.VAULT_BRANCHES:
            branch_dir = self.topic_dir / dirname
            if not branch_dir.exists():
                continue
            for entry in branch_dir.iterdir():
                if not entry.is_dir() or entry.resolve() in claimed:
                    continue
                if dirname == paths.AI_PACKAGE_DIRNAME and paths.ara_is_nonempty(entry / "ara"):
                    orphans_dir.mkdir(parents=True, exist_ok=True)
                    dest = orphans_dir / entry.name
                    if dest.exists():
                        shutil.rmtree(dest, ignore_errors=True)  # latest orphan wins
                    shutil.move(str(entry), str(dest))
                else:
                    shutil.rmtree(entry, ignore_errors=True)
        return demoted
```

- [ ] **Step 4: 跑测试确认通过**

Run: `uv run pytest tests/ledger/test_store_consistency_preserve.py -v`
Expected: PASS（3 passed）

- [ ] **Step 5: lint + commit**

```bash
uv run ruff check .claude/skills/paper-landscape/scripts/ledger/store.py
git add .claude/skills/paper-landscape/scripts/ledger/store.py tests/ledger/test_store_consistency_preserve.py
git commit -m "feat(ledger): preserve ai_package ARA orphans to _failed/_orphans (ADR-0011)"
```

---

## Task 4: `crash_resume_sweep` 同款 litmus（次要硬化）

非 done 行记录的 `ai_package_path` 若含非空 ARA → 移入 `_failed/_orphans/`，而非 rm。

**Files:**
- Modify: `.claude/skills/paper-landscape/scripts/ledger/store.py`（`crash_resume_sweep`）
- Test: `tests/ledger/test_store_crash_resume_preserve.py`（新建）

- [ ] **Step 1: 写失败测试**

```python
# tests/ledger/test_store_crash_resume_preserve.py
from scripts.ledger.store import Ledger


def test_crash_resume_preserves_ai_ara(tmp_path):
    led = Ledger(tmp_path)
    ai = tmp_path / "ai_package" / "k1"
    (ai / "ara").mkdir(parents=True)
    (ai / "ara" / "PAPER.md").write_text("x", encoding="utf-8")
    # 非 done 行，记录了 ai_package_path
    led.record_status("k1", status="analyzed", ai_package_path=str(ai))
    led.crash_resume_sweep()
    assert not ai.exists()
    assert (tmp_path / "_failed" / "_orphans" / "k1" / "ara" / "PAPER.md").exists()


def test_crash_resume_deletes_person_path(tmp_path):
    led = Ledger(tmp_path)
    person = tmp_path / "person_vault" / "k2"
    person.mkdir(parents=True)
    (person / "report.md").write_text("r", encoding="utf-8")
    led.record_status("k2", status="analyzed", person_vault_path=str(person))
    led.crash_resume_sweep()
    assert not person.exists()  # 廉价 → 仍删
```

- [ ] **Step 2: 跑测试确认失败**

Run: `uv run pytest tests/ledger/test_store_crash_resume_preserve.py -v`
Expected: FAIL —— `test_crash_resume_preserves_ai_ara`（当前被 rmtree）。

- [ ] **Step 3: 改 `crash_resume_sweep`**

OLD（当前 252-264）:
```python
        removed: list[str] = []
        for _key, row in self._latest_by_key().items():
            if row["status"] == _DONE or row.get("rescinded_at"):
                continue
            for path_key in ("person_vault_path", "ai_package_path"):
                p = row.get(path_key)
                if p and Path(p).exists():
                    shutil.rmtree(p)
                    removed.append(p)
        clones = self.topic_dir / ".clones"
        if clones.exists():
            shutil.rmtree(clones)
        return removed
```

NEW:
```python
        removed: list[str] = []
        orphans_dir = self.topic_dir / FAILED_REL / "_orphans"
        for _key, row in self._latest_by_key().items():
            if row["status"] == _DONE or row.get("rescinded_at"):
                continue
            for path_key in ("person_vault_path", "ai_package_path"):
                p = row.get(path_key)
                if not (p and Path(p).exists()):
                    continue
                # ADR-0011: preserve a non-empty ai_package ARA (token-expensive);
                # person_vault + empty ARA dirs are still removed.
                if path_key == "ai_package_path" and paths.ara_is_nonempty(Path(p) / "ara"):
                    orphans_dir.mkdir(parents=True, exist_ok=True)
                    dest = orphans_dir / Path(p).name
                    if dest.exists():
                        shutil.rmtree(dest, ignore_errors=True)
                    shutil.move(p, str(dest))
                else:
                    shutil.rmtree(p)
                removed.append(p)
        clones = self.topic_dir / ".clones"
        if clones.exists():
            shutil.rmtree(clones)
        return removed
```

> 注：`paths` 已在 store.py import；`FAILED_REL` 由 Task 3 Step 3a 引入。若先做 Task 4，请同时加该 import。

- [ ] **Step 4: 跑测试确认通过**

Run: `uv run pytest tests/ledger/test_store_crash_resume_preserve.py -v`
Expected: PASS（2 passed）

- [ ] **Step 5: lint + commit**

```bash
uv run ruff check .claude/skills/paper-landscape/scripts/ledger/store.py
git add .claude/skills/paper-landscape/scripts/ledger/store.py tests/ledger/test_store_crash_resume_preserve.py
git commit -m "feat(ledger): preserve ai_package ARA on crash-resume sweep (ADR-0011)"
```

---

## 端到端验证

- [ ] **全套绿 + 引擎源 ruff 干净**（项目唯一验收门）

```bash
uv run pytest
uv run ruff check .claude/skills/paper-landscape/scripts/
```
Expected: 全 PASS；ruff 无 error。

- [ ] **回归核对**：`grep -rn "rmtree" .claude/skills/paper-landscape/scripts/` —— 确认剩余 rmtree 仅落在「可再生临时物 / person_vault / 空壳 / latest-orphan 覆盖」，无任何裸 rm 一个非空 `ara/`。

## 不在本计划（ADR-0011 已记，单独跟进）

- 现场 `analysis=None` 是否削弱 ADR-0007 的「锚点门好-ARA 复用」（可能逼复活赛重采样）——读 `revival.py` 单独验，不混入本次删除安全改动。

---

## Review Log

### Round 1 (Codex, Initial — REVISIONS NEEDED)

1. **Blocking**: spec contradicts ADR-0011 on the G3 re-emit cleanup path — `spoke.py:393-394` marked "无需改" but ADR-0011 lists "the spoke's G3 re-emit product removal" as a reflex-rm site that must route through preserve/move.
2. **Blocking**: `EngineAbort` during G3 re-emit is uncovered. `_attempt()` is also called from `_reemit_for_g3` (spoke.py:356) via `run_with_budget(on_reemit=...)`; the G3 `try` only catches `_Unfixable` + the three gate exceptions (spoke.py:384/387). A built staged ARA from a G3 re-emit abort is left in `/tmp`, not moved to `_failed/`.
3. **Test plan**: spoke integration test not executable — scene key is `_candidate_key(candidate)` (hub.py:99), not `candidate["key"]`; and the Task 2 run command omits the new `tests/test_spoke_abort_scene.py`.

Verified positives: OLD snippets match byte-for-byte; imports cycle-free; g2-loop variables in scope; `identity_base` guard-omission correct. Ran focused tests + ruff (passed).

### Response to Round 1 (Claude Code)

- **Finding 1 — PARTIALLY ACCEPTED.** Content-loss is in fact covered (latest-one-wins + Task 3's consistency_check backstop), so it is not "we lose an ARA". BUT the **rm-before-scene ordering** genuinely violates this plan's own scene-before-rm rule and the ADR's listing. Fixed by **reordering** (Task 2 Step 9): `write_scene` first, then `rmtree(produced.*)`. Updated the "不改项" note to retract the wrong "无需改".
- **Finding 2 — ACCEPTED.** Confirmed the G3 `try` (spoke.py:384/387) does not catch `EngineAbort`. Added Task 2 Step 8: an `except EngineAbort` on the G3 `try` calling the new shared `_abort_scene(exc)` helper, then re-raise. Refactored the g2-loop handler (Step 7) to use the same helper (DRY, Step 6 defines it).
- **Finding 3 — ACCEPTED.** Test now imports `_candidate_key` and asserts on `_candidate_key(candidate)` (Step 10); the run command (Step 11) includes `tests/test_spoke_abort_scene.py` (when Step 10 is implemented).

Change summary: Task 2 restructured from 8 → 11 steps — added `_abort_scene` DRY helper (Step 6), G3-section EngineAbort coverage (Step 8), scene-before-rm reorder of the G3 re-emit handler (Step 9); fixed the spoke test key + run command (Steps 10-11). No other tasks changed.

### Round 2 (Codex, Focused — APPROVED)

No blocking findings; the three Round-1 fixes verified against source:
- Step 6 `_abort_scene` correctly placed (after `_pre_promote_scene`, before the g2 loop); its referenced values are bound (spoke.py:198/200, `ing`/`content_list_path` earlier) and it is in scope for the later G3 `try` (spoke.py:369).
- Step 8 in scope: `EngineAbort` propagates `run_with_budget → on_reemit → _reemit_for_g3 → _attempt`; the new `except EngineAbort` on the G3 `try` catches the right frame before the staged ARA is lost.
- Step 9 correct: current handler is rm-before-scene (spoke.py:387); reorder to `write_scene` first satisfies ADR-0011 scene-before-rm.

Residual (non-blocking): prefer a dedicated G3 re-emit `EngineAbort` test (the Step-8 regression path), not only the g2 abort test. Ran two focused existing G3 tests — passed.

**Decision: APPROVED.**

### Response to Round 2 (Claude Code)

Accepted the residual advisory — added a "Codex R2 建议" note to Task 2 Step 10 specifying a dedicated G3 re-emit abort test (strongly recommended, non-blocking). No code-path changes. **Cross-model review converged: APPROVED in 2 rounds.**
