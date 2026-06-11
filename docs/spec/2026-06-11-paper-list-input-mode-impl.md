# 指定列表输入模式(auto_discover)实现计划

> **日期**: 2026-06-11
> **状态**: 活跃
> **作者**: ShinewineW + Claude Opus 4.8
> **基准版本**: `paper-rolling@22dfef2`
> **目的**: 给引擎加第二种输入模态「指定列表」(关闭自发查找、只跑操作者给的论文),与现有「自发查找」二元切换,落实 ADR-0010。
> 范围: `.claude/skills/paper-landscape/scripts/{campaign.py, discovery/discover.py, adapters.py, hub.py, run_campaign.py}` + `config/campaign.yaml.example` + 对应 `tests/`

---

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a binary `auto_discover` campaign switch so a campaign either auto-discovers papers by topic (current) OR processes only the operator-supplied `force_include` list (new), paged by `n_per_tick`.

**Architecture:** One boolean `auto_discover` on `CampaignConfig` (default `True` = current behavior). When `False`, `discovery/discover.py::discover` short-circuits to return only the normalized `force_include` papers (no source fan-out, no LLM query-expansion); the hub stops auto-raising `n_target` for forced papers so the list pages across `/loop` ticks; flipping the switch re-fires the Hard Gate. `skip_set` respect and self-pagination are unchanged (free). The list-identity-change re-gate (ADR-0010) is the last, deferrable task.

**Tech Stack:** Python 3.13, `uv`, `pytest`, frozen `@dataclass`, PyYAML. Run tests with `uv run pytest`; lint with `uv run ruff check .claude/skills/paper-landscape/scripts/`.

---

## Background the engineer needs (read first)

- The engine is composed at runtime (no `__main__` runs a campaign). `run_campaign(...)` wires seams and calls `run_campaign_tick` → `run_tick`. Read `.claude/skills/paper-landscape/SKILL.md` §"Wiring the model seams" + §"Invoke the engine (quickstart)".
- **`force_include`** already exists end-to-end: Hard-Gate-validated (`campaign.py::_validate_force_include`), carried on `CampaignConfig`, threaded into `build_discover(force_include=...)`, normalized by `discovery/discover.py::_build_forced` (marks each `forced=True`, `discovery_sources=["forced"]`), prepended to the candidate pool. This task reuses that plumbing — the only new behavior is "discovery OFF + don't auto-raise N".
- **PYTHONPATH gotcha:** module CLIs need `PYTHONPATH=.claude/skills/paper-landscape`; `uv run pytest` already sets pythonpath via `pyproject.toml`.
- ADR-0010 (`docs/adr/0010-paper-list-input-mode.md`) and `CONTEXT.md` (`自发查找` / `指定列表` / `topic`) are the source of truth for terminology + decisions.

## File Structure

| File | Responsibility | Change |
|---|---|---|
| `campaign.py` | `CampaignConfig` schema + Hard Gate (`gate_needed`, `write_campaign`, `load_campaign`) | add `auto_discover` field + flip re-gate + (Task 5) fingerprint |
| `discovery/discover.py` | `discover` orchestrator (aliased `_discover` in adapters) + `_build_forced` normalizer | short-circuit to list-only when `auto_discover=False` |
| `adapters.py` | `build_discover` seam factory | accept + forward `auto_discover` |
| `hub.py` | `run_tick` / `run_campaign_tick` | don't auto-raise `n_target` in list mode; thread `auto_discover` |
| `run_campaign.py` | `run_campaign` driver | forward `requested_auto_discover` for the flip re-gate |
| `config/campaign.yaml.example` | shipped template | document `auto_discover` |
| `tests/{test_campaign,discovery/test_discover,test_hub}.py` | tests | one per task |

---

## Chunk 1: Core list mode (Tasks 1–4 — ships a working feature)

### Task 1: `auto_discover` field on `CampaignConfig`

**Files:**
- Modify: `.claude/skills/paper-landscape/scripts/campaign.py` (`CampaignConfig`, `load_campaign`)
- Test: `tests/test_campaign.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_campaign.py`:

```python
def test_campaign_config_auto_discover_defaults_true_and_round_trips(tmp_path):
    from scripts.campaign import CampaignConfig, load_campaign, write_campaign

    # Default preserves current behavior.
    cfg = CampaignConfig(topic="world model survey", n_per_tick=5, is_ad_domain=True)
    assert cfg.auto_discover is True

    # list-mode value survives a write→load round trip.
    listed = CampaignConfig(
        topic="my reading list on world models",
        n_per_tick=5,
        is_ad_domain=True,
        force_include=[{"arxiv_id": "2407.01392", "title": "DiffusionForcing"}],
        auto_discover=False,
    )
    write_campaign(tmp_path, listed)
    loaded = load_campaign(tmp_path)
    assert loaded is not None
    assert loaded.auto_discover is False
    assert loaded.force_include[0]["arxiv_id"] == "2407.01392"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_campaign.py::test_campaign_config_auto_discover_defaults_true_and_round_trips -v`
Expected: FAIL — `TypeError: __init__() got an unexpected keyword argument 'auto_discover'`.

- [ ] **Step 3: Add the field**

In `campaign.py`, the `CampaignConfig` dataclass currently ends:

```python
    topic: str
    n_per_tick: int
    is_ad_domain: bool
    force_include: list[dict] = field(default_factory=list)
```

Replace with (add ONE line — `auto_discover`):

```python
    topic: str
    n_per_tick: int
    is_ad_domain: bool
    force_include: list[dict] = field(default_factory=list)
    # 指定列表 mode (ADR-0010): True = 自发查找 (discover by topic, force_include adds on
    # top); False = 指定列表 (discovery OFF, force_include IS the whole work set).
    auto_discover: bool = True
```

`write_campaign` needs NO change — it serializes via `asdict(cfg)`, which now includes `auto_discover`.

- [ ] **Step 4: Make `load_campaign` read it**

In `campaign.py::load_campaign`, the return currently is:

```python
    return CampaignConfig(
        topic=data["topic"],
        n_per_tick=int(data["n_per_tick"]),
        is_ad_domain=bool(data["is_ad_domain"]),
        force_include=list(data.get("force_include") or []),
    )
```

Replace with (add the `auto_discover=` line; `.get(..., True)` keeps old configs working):

```python
    return CampaignConfig(
        topic=data["topic"],
        n_per_tick=int(data["n_per_tick"]),
        is_ad_domain=bool(data["is_ad_domain"]),
        force_include=list(data.get("force_include") or []),
        auto_discover=bool(data.get("auto_discover", True)),
    )
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/test_campaign.py::test_campaign_config_auto_discover_defaults_true_and_round_trips -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/paper-landscape/scripts/campaign.py tests/test_campaign.py
git commit -m "feat(campaign): add auto_discover field (默认 True，向后兼容)"
```

---

### Task 2: List-mode short-circuit in discovery

**Files:**
- Modify: `.claude/skills/paper-landscape/scripts/discovery/discover.py` (`_discover`)
- Modify: `.claude/skills/paper-landscape/scripts/adapters.py` (`build_discover`)
- Test: `tests/discovery/test_discover.py`

**Data-flow note:** the orchestrator is the module-level `discover(campaign_config, sources, llm)` in `discovery/discover.py` (⚠️ `adapters.py` imports it **aliased** as `_discover` — the real name in `discover.py` is `discover`; edit/import that). `campaign_config` is a plain `dict` (built in `build_discover.discover()`); `sources` is a dict of source objects with `.search()`; `llm` is the query-expansion callable. `_build_forced(entries)` (same module, ~line 200) turns `force_include` dicts into candidate dicts marked `forced=True`. In list mode we return `_build_forced(...)` and touch neither `sources` nor `llm`.

- [ ] **Step 1: Write the failing test**

Append to `tests/discovery/test_discover.py`:

```python
def test_discover_list_mode_returns_only_forced_without_touching_sources():
    from scripts.discovery.discover import discover

    def boom_llm(*a, **k):
        raise AssertionError("LLM query-expansion must NOT run in list mode")

    class BoomSource:
        def search(self, *a, **k):
            raise AssertionError("sources must NOT be queried in list mode")

    sources = {"openalex": BoomSource(), "s2": BoomSource(), "arxiv": BoomSource()}
    cfg = {
        "topic": "my world-model list",
        "top_k": 5,
        "auto_discover": False,
        "force_include": [
            {"arxiv_id": "2407.01392", "title": "DiffusionForcing"},
            {"arxiv_id": "1803.10122", "title": "WorldModels"},
        ],
    }

    out = discover(cfg, sources, boom_llm)

    assert [c["arxiv_id"] for c in out] == ["2407.01392", "1803.10122"]
    assert all(c.get("forced") for c in out)  # _build_forced marked them
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/discovery/test_discover.py::test_discover_list_mode_returns_only_forced_without_touching_sources -v`
Expected: FAIL — `AssertionError: LLM query-expansion must NOT run in list mode` (current `discover` always calls `expand_queries` first).

- [ ] **Step 3: Add the short-circuit at the top of `discover`**

In `discovery/discover.py`, in the module-level function **`discover`** (NOT `_discover` — that name only exists as `adapters.py`'s import alias), find this line (it sits just after the `topic`/`top_k`/`overfetch`/`cap` reads near the top of the body, ~line 89):

```python
    queries = expand_queries(topic, llm=llm)
```

Insert the short-circuit immediately ABOVE that line (it returns before any source/LLM work and uses none of the `topic`/`top_k` locals):

```python
    # 指定列表 mode (ADR-0010): discovery OFF — the work set IS force_include. Skip the
    # source fan-out + LLM query-expansion entirely; _build_forced normalizes + marks them.
    if not campaign_config.get("auto_discover", True):
        return _build_forced(campaign_config.get("force_include") or [])

    queries = expand_queries(topic, llm=llm)
```

- [ ] **Step 4: Forward `auto_discover` through `build_discover`**

In `adapters.py::build_discover`, the signature currently ends:

```python
    overfetch_factor: int = 3,
    force_include: list[dict[str, Any]] | None = None,
) -> Callable[[str, int], list[dict[str, Any]]]:
```

Replace with (add `auto_discover` param):

```python
    overfetch_factor: int = 3,
    force_include: list[dict[str, Any]] | None = None,
    auto_discover: bool = True,
) -> Callable[[str, int], list[dict[str, Any]]]:
```

Then in the inner `discover()`, the `campaign_config` dict currently ends:

```python
            "current_year": current_year,
            "force_include": list(force_include or []),
        }
```

Replace with (add the `auto_discover` key):

```python
            "current_year": current_year,
            "force_include": list(force_include or []),
            "auto_discover": auto_discover,
        }
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/discovery/test_discover.py::test_discover_list_mode_returns_only_forced_without_touching_sources -v`
Expected: PASS

- [ ] **Step 6: Run the discovery suite (no regression in auto mode)**

Run: `uv run pytest tests/discovery/ -q`
Expected: PASS (auto-mode tests untouched — default `auto_discover` absent in their cfg dicts defaults to `True`).

- [ ] **Step 7: Commit**

```bash
git add .claude/skills/paper-landscape/scripts/discovery/discover.py .claude/skills/paper-landscape/scripts/adapters.py tests/discovery/test_discover.py
git commit -m "feat(discovery): list mode 短路 — auto_discover=False 时只返回 force_include"
```

---

### Task 3: List-mode paging in the hub (don't auto-raise N)

**Files:**
- Modify: `.claude/skills/paper-landscape/scripts/hub.py` (`run_tick`, `run_campaign_tick`)
- Test: `tests/test_hub.py`

**Why:** In list mode every candidate is `forced`, so the existing `n_target = max(n_target, forced_pending)` would raise N to the whole list = one-shot. List mode must page, so we only auto-raise in auto-discovery mode.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_hub.py` (mirror the fixtures/helpers already used in that file for `run_tick`; this test uses a fake discover returning forced candidates and a counting spoke):

```python
def test_run_tick_list_mode_pages_and_does_not_raise_n(tmp_path):
    from scripts.hub import run_tick
    from scripts.ledger.store import Ledger

    forced = [
        {"arxiv_id": f"24{i:02d}.0000", "title": f"P{i}", "forced": True}
        for i in range(6)
    ]

    def discover(topic, n):
        return [dict(c) for c in forced]  # whole list, like 指定列表 _discover

    seen = []

    def spoke(candidate, *, cancel=None):
        from scripts.hub import SpokeResult

        seen.append(candidate["key"])
        return SpokeResult(
            status="done",
            person_vault_path=str(tmp_path / f"pv/{candidate['key']}"),
            ai_package_path=str(tmp_path / f"ai/{candidate['key']}"),
            failure_class=None,
            failure_reason=None,
            source_url=None,
            attempted_tier="reuse",
        )

    ledger = Ledger(tmp_path)
    hub = run_tick(
        workspace=tmp_path,
        topic="my list",
        n_target=2,
        ledger=ledger,
        discover=discover,
        spoke=spoke,
        auto_discover=False,
    )
    # list mode must respect n_target=2, NOT raise it to 6.
    assert len(seen) == 2
```

> Adjust `SpokeResult` field names to match the real dataclass in `hub.py` if they differ; read the `SpokeResult` definition at the top of `hub.py` first and mirror it exactly (the production spoke returns vault paths so the result counts as done).

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_hub.py::test_run_tick_list_mode_pages_and_does_not_raise_n -v`
Expected: FAIL — `TypeError: run_tick() got an unexpected keyword argument 'auto_discover'` (then, once param added but raise not gated, `assert len(seen) == 2` fails with 6).

- [ ] **Step 3: Add `auto_discover` to `run_tick` + gate the N-raise**

In `hub.py::run_tick`, the signature block currently:

```python
    discover: DiscoverFn,
    spoke: SpokeFn,
    max_concurrent: int = 5,
    watchdog: Watchdog | None = None,
) -> HubResult:
```

Replace with (add `auto_discover`):

```python
    discover: DiscoverFn,
    spoke: SpokeFn,
    max_concurrent: int = 5,
    watchdog: Watchdog | None = None,
    auto_discover: bool = True,
) -> HubResult:
```

Then the forced N-raise currently reads:

```python
    forced_pending = sum(1 for c in pool if c.get("forced") and c["key"] not in skip)
    n_target = max(n_target, forced_pending)
```

Replace with (only raise in 自发查找 mode — 指定列表 pages by n_target):

```python
    forced_pending = sum(1 for c in pool if c.get("forced") and c["key"] not in skip)
    if auto_discover:
        # 自发查找: must-includes must all be attempted this tick (中枢-D1).
        # 指定列表 (auto_discover=False): the list pages by n_per_tick (ADR-0010), do NOT raise.
        n_target = max(n_target, forced_pending)
```

- [ ] **Step 4: Forward `cfg.auto_discover` from `run_campaign_tick`**

In `hub.py::run_campaign_tick`, the `run_tick(...)` call currently:

```python
    hub = run_tick(
        workspace=workspace,
        topic=cfg.topic,
        n_target=cfg.n_per_tick,
        ledger=ledger,
        discover=discover,
        spoke=spoke,
        max_concurrent=max_concurrent,
        watchdog=watchdog,
    )
```

Replace with (add `auto_discover=cfg.auto_discover`):

```python
    hub = run_tick(
        workspace=workspace,
        topic=cfg.topic,
        n_target=cfg.n_per_tick,
        ledger=ledger,
        discover=discover,
        spoke=spoke,
        max_concurrent=max_concurrent,
        watchdog=watchdog,
        auto_discover=cfg.auto_discover,
    )
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/test_hub.py::test_run_tick_list_mode_pages_and_does_not_raise_n -v`
Expected: PASS

- [ ] **Step 6: Run the hub suite (auto mode unchanged)**

Run: `uv run pytest tests/test_hub.py -q`
Expected: PASS (auto-mode callers omit `auto_discover` → defaults `True` → existing raise behavior preserved).

- [ ] **Step 7: Commit**

```bash
git add .claude/skills/paper-landscape/scripts/hub.py tests/test_hub.py
git commit -m "feat(hub): list mode 按 n_per_tick 分页 — auto_discover=False 不抬 n_target"
```

---

### Task 4: Flipping `auto_discover` re-fires the Hard Gate

**Files:**
- Modify: `.claude/skills/paper-landscape/scripts/campaign.py` (`gate_needed`)
- Modify: `.claude/skills/paper-landscape/scripts/hub.py` (`run_campaign_tick`)
- Modify: `.claude/skills/paper-landscape/scripts/run_campaign.py` (`run_campaign`)
- Test: `tests/test_campaign.py`

**Caller trace (grep before changing the signature):** `gate_needed` is called only in `hub.py::run_campaign_tick`. `run_campaign_tick` is called only in `run_campaign.py::run_campaign`. Both get a new optional `requested_auto_discover` (default `None` = no change requested = never re-gates on its own). All existing callers passing nothing stay correct.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_campaign.py`:

```python
def test_gate_needed_refires_when_auto_discover_flips(tmp_path):
    from scripts.campaign import CampaignConfig, gate_needed, write_campaign

    write_campaign(
        tmp_path,
        CampaignConfig(topic="world model survey", n_per_tick=5, is_ad_domain=True),
    )
    # No requested change → no re-gate.
    assert gate_needed(tmp_path, requested_topic=None, requested_n=None,
                       requested_auto_discover=None) is False
    # Requesting list mode (flip True→False) → re-gate.
    assert gate_needed(tmp_path, requested_topic=None, requested_n=None,
                       requested_auto_discover=False) is True
    # Requesting the same value → no re-gate.
    assert gate_needed(tmp_path, requested_topic=None, requested_n=None,
                       requested_auto_discover=True) is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_campaign.py::test_gate_needed_refires_when_auto_discover_flips -v`
Expected: FAIL — `TypeError: gate_needed() got an unexpected keyword argument 'requested_auto_discover'`.

- [ ] **Step 3: Add `requested_auto_discover` to `gate_needed`**

In `campaign.py::gate_needed`, the signature:

```python
def gate_needed(
    workspace: Path,
    *,
    requested_topic: str | None,
    requested_n: int | None,
) -> bool:
```

Replace with:

```python
def gate_needed(
    workspace: Path,
    *,
    requested_topic: str | None,
    requested_n: int | None,
    requested_auto_discover: bool | None = None,
) -> bool:
```

Then the body, currently ending:

```python
    if requested_n is not None and requested_n != cfg.n_per_tick:
        return True
    return False
```

Replace with (add the `auto_discover` comparison before `return False`):

```python
    if requested_n is not None and requested_n != cfg.n_per_tick:
        return True
    if requested_auto_discover is not None and requested_auto_discover != cfg.auto_discover:
        return True
    return False
```

- [ ] **Step 4: Thread it through `run_campaign_tick`**

In `hub.py::run_campaign_tick`, the signature has `requested_topic` / `requested_n`. Add `requested_auto_discover: bool | None = None` to the signature (next to `requested_n`), and update the `gate_needed(...)` call:

OLD (the gate call near the top of `run_campaign_tick`):

```python
    if gate_needed(workspace, requested_topic=requested_topic, requested_n=requested_n):
```

NEW:

```python
    if gate_needed(
        workspace,
        requested_topic=requested_topic,
        requested_n=requested_n,
        requested_auto_discover=requested_auto_discover,
    ):
```

- [ ] **Step 5: Thread it through `run_campaign`**

In `run_campaign.py::run_campaign`, add `requested_auto_discover: bool | None = None` to the signature (next to `requested_n: int | None = None`), and in the `run_campaign_tick(...)` call inside the `with ledger.acquire():` block:

OLD:

```python
        return run_campaign_tick(
            workspace=workspace,
            ledger=ledger,
            discover=discover,
            spoke=spoke,
            requested_topic=requested_topic,
            requested_n=requested_n,
        )
```

NEW:

```python
        return run_campaign_tick(
            workspace=workspace,
            ledger=ledger,
            discover=discover,
            spoke=spoke,
            requested_topic=requested_topic,
            requested_n=requested_n,
            requested_auto_discover=requested_auto_discover,
        )
```

- [ ] **Step 6: Run test + full suite**

Run: `uv run pytest tests/test_campaign.py -q && uv run pytest -q`
Expected: PASS (all). Then `uv run ruff check .claude/skills/paper-landscape/scripts/` → `All checks passed!`

- [ ] **Step 7: Commit**

```bash
git add .claude/skills/paper-landscape/scripts/campaign.py .claude/skills/paper-landscape/scripts/hub.py .claude/skills/paper-landscape/scripts/run_campaign.py tests/test_campaign.py
git commit -m "feat(gate): 翻转 auto_discover 重锁 Hard Gate"
```

---

## Chunk 2: Docs + (deferrable) list-change re-gate

### Task 5: Docs + shipped template

**Files:**
- Modify: `config/campaign.yaml.example`
- Modify: `.claude/skills/paper-landscape/SKILL.md` (Hard Gate section + quickstart)
- Modify: `docs/guides/EXTENDING.md` (note the mode)

- [ ] **Step 1: Add `auto_discover` to the example template**

In `config/campaign.yaml.example`, after the `topic:` line, add:

```yaml
# auto_discover: true  = 自发查找 (discover by topic; force_include adds on top).
# auto_discover: false = 指定列表 (discovery OFF; force_include IS the whole work set, paged by n_per_tick).
auto_discover: true
```

- [ ] **Step 2: Update the SKILL.md quickstart so the runtime wires the toggle**

In `.claude/skills/paper-landscape/SKILL.md` §"Invoke the engine (quickstart)", the `build_discover(...)` call currently passes `is_ad_domain` + `force_include`. Add `auto_discover=campaign.auto_discover if campaign else True,` to that call, and in the Hard Gate section document that flipping `auto_discover` (or changing the list in list mode) re-fires the gate. Show:

```python
    discover=build_discover(
        llm=seams["expand_llm"],
        is_ad_domain=campaign.is_ad_domain if campaign else True,
        force_include=campaign.force_include if campaign else [],
        auto_discover=campaign.auto_discover if campaign else True,
    ),
```

- [ ] **Step 3: Note the mode in EXTENDING.md**

Add a short paragraph under the discovery section of `docs/guides/EXTENDING.md`: "Two input modes exist (ADR-0010): `auto_discover=True` (自发查找) and `auto_discover=False` (指定列表 — `force_include` is the whole set, discovery skipped). See `CONTEXT.md`."

- [ ] **Step 4: Commit**

```bash
git add config/campaign.yaml.example .claude/skills/paper-landscape/SKILL.md docs/guides/EXTENDING.md
git commit -m "docs(campaign): 文档化 auto_discover 两模式 + quickstart 接线"
```

---

### Task 6 (DEFERRABLE — MVP may stop after Task 5): list-identity-change re-gate

ADR-0010 wants editing the `force_include` identity-set (in list mode) to re-fire the Hard Gate, catching hand-edits to `campaign.yaml`. This needs a confirmed-fingerprint stored at `write_campaign` time and compared in `gate_needed`. **It is the one medium-complexity piece; Tasks 1–5 already deliver a working, safe feature (changing the list via the gate command is confirmed by construction). Implement this only if hand-edit detection is required.**

**Files:** `campaign.py` (`CampaignConfig` + `write_campaign` + `gate_needed`), `tests/test_campaign.py`.

- [ ] **Step 1: Write the failing test**

```python
def test_gate_needed_refires_when_list_identity_changes_in_list_mode(tmp_path):
    from scripts.campaign import CampaignConfig, gate_needed, load_campaign, write_campaign
    import yaml

    write_campaign(tmp_path, CampaignConfig(
        topic="my world-model list", n_per_tick=5, is_ad_domain=True,
        force_include=[{"arxiv_id": "2407.01392", "title": "DiffusionForcing"}],
        auto_discover=False,
    ))
    # Unchanged list → no re-gate.
    assert gate_needed(tmp_path, requested_topic=None, requested_n=None,
                       requested_auto_discover=None) is False
    # Hand-edit campaign.yaml to a different paper, leave fingerprint stale → re-gate.
    p = tmp_path / "config" / "campaign.yaml"
    data = yaml.safe_load(p.read_text())
    data["force_include"] = [{"arxiv_id": "1803.10122", "title": "WorldModels"}]
    p.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=True))
    assert gate_needed(tmp_path, requested_topic=None, requested_n=None,
                       requested_auto_discover=None) is True
```

- [ ] **Step 2: Run to verify it fails**

Run: `uv run pytest tests/test_campaign.py::test_gate_needed_refires_when_list_identity_changes_in_list_mode -v`
Expected: FAIL (returns False — no fingerprint check yet).

- [ ] **Step 3: Add a fingerprint helper + field**

In `campaign.py`, add near the validators:

```python
import hashlib
import json


def list_fingerprint(force_include: list[dict]) -> str:
    """Stable hash of the force_include IDENTITY set (order-independent).

    Identity = arxiv_id|doi|title per entry; changing which papers are listed
    changes this, but reordering / progress through the list does NOT.
    """
    ids = sorted(
        str(e.get("arxiv_id") or e.get("doi") or e.get("title") or "") for e in force_include
    )
    return hashlib.sha256(json.dumps(ids, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]
```

Add `confirmed_fingerprint: str = ""` as the last field of `CampaignConfig` (after `auto_discover`). In `load_campaign`, read `confirmed_fingerprint=str(data.get("confirmed_fingerprint", ""))`.

- [ ] **Step 4: Stamp the fingerprint at write time**

In `write_campaign`, before serializing, compute and embed the fingerprint so the locked config records what was confirmed. Replace the body:

OLD:

```python
    path.write_text(
        yaml.safe_dump(asdict(cfg), allow_unicode=True, sort_keys=True),
        encoding="utf-8",
    )
```

NEW:

```python
    data = asdict(cfg)
    data["confirmed_fingerprint"] = list_fingerprint(cfg.force_include)
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=True),
        encoding="utf-8",
    )
```

- [ ] **Step 5: Compare in `gate_needed` (list mode only)**

In `gate_needed`, before `return False`, add:

```python
    # 指定列表 mode (ADR-0010): a changed list IDENTITY set since last confirmation
    # (incl. a hand-edit to campaign.yaml) re-fires the gate. Paging progress does not
    # change the identity set, so it does not re-gate.
    if not cfg.auto_discover and list_fingerprint(cfg.force_include) != cfg.confirmed_fingerprint:
        return True
    return False
```

- [ ] **Step 6: Run test + full suite + ruff**

Run: `uv run pytest tests/test_campaign.py -q && uv run pytest -q && uv run ruff check .claude/skills/paper-landscape/scripts/`
Expected: all PASS / clean.

- [ ] **Step 7: Commit**

```bash
git add .claude/skills/paper-landscape/scripts/campaign.py tests/test_campaign.py
git commit -m "feat(gate): 列表身份变更重锁(指纹检测,抓手改 campaign.yaml)"
```

---

## Final verification (after all tasks)

- [ ] `uv run pytest -q` → all green
- [ ] `uv run ruff check .claude/skills/paper-landscape/scripts/ tests/` → `All checks passed!`
- [ ] Manual smoke: write a list-mode campaign (`auto_discover=False`, `force_include=[…]`), confirm a tick processes only the list, paged by `n_per_tick`, and skips ledger-`done` entries.
- [ ] Confirm 自发查找 mode is byte-for-byte unchanged (default `auto_discover=True` everywhere).

## Notes / out of scope

- **OOM is NOT addressed here** (ADR-0010): a list paper not in `corpus/` ingests like discover mode; a heavy Tier-2 MinerU OOM quarantines that one paper. The pod-offload remains the ingest-layer workaround (`.claude/rules/ingest/remote-pod-offload.md`).
- **skip_set respect + self-pagination are unchanged** — no task touches them (they already do the right thing).
- After this lands, the 24-paper re-emit becomes: `invalidate` the 24 → set `auto_discover=False` + `force_include`=24 in `campaign.yaml` (Hard Gate) → set `CLAUDE_P_MAX_CONCURRENCY` low → `run_campaign`.
