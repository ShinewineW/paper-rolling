# 理解阅读忠实门(branch1)实现计划 — ADR-0012

> **日期**: 2026-06-12
> **状态**: 草稿
> **作者**: Claude (Opus 4.8) + ShinewineW
> **基准版本**: `paper-rolling@f64c9d4`
> **目的**: 把 branch1 锚点门从"逼 LLM 给每条经验正文自贴 `<!--ref-->`"重构为"机械落源(b)+ 语义判官(c)"两层忠实验收,终结 DiffusionForcing/Genie 那类内容满分却被形式门误杀的论文。
> 范围: `.claude/skills/paper-landscape/scripts/`(output / llm / audit),`config/llm.yaml`,`config/audit.yaml`,镜像 `tests/`

---

# 理解阅读忠实门 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace branch1's "every empirical prose line must carry a `<!--ref-->` anchor" gate with a two-layer faithfulness check — (b) tolerant mechanical number-grounding of the report against the source MD, and (c) a config-routed LLM judge comparing report↔ARA for material misleading — so a faithful 理解阅读 may carry numbers in natural prose.

**Architecture:** A faithful report's numbers are verified deterministically against the source MD (reusing 数字门's value-match helpers); semantic faithfulness (misattribution/overclaim) is judged by a NEW 7th LLM seam routed through `config/llm.yaml`, defaulted to a model ≠ the writer's. The prose `<!--ref-->` requirement is dropped from BOTH the branch1 lint and the G3 auditor; the engine-mechanical 核心结论 block keeps its anchors and 最终门 still resolves them. Both layers are content gates that feed findings back to the writer (ADR-0006) and raise `AnchorGateError` on hard-block (name unchanged per ADR-0008).

**Tech Stack:** Python 3.13, `uv run pytest`, `ruff`. No new dependencies.

---

## Background an engineer needs (read first)

- **ADR-0012** (`docs/adr/0012-anchor-gate-verifies-faithfulness-not-anchor-form.md`) is the decision this plan implements. **ADR-0006** governs the gate-feedback boundary (content gates adapt; 数字门 stays blind). **ADR-0008**: canonical gate name 锚点门 stays; code identifier `AnchorGateError` stays.
- **The two branch1 paths** (`scripts/output/produce.py:186-193`): production runs `write_branch1_llm` (LLM writer routed via the `write_report` seam); `write_branch1` is the deterministic fallback (`write_report=None`). **Both** compose a `report` string then call `lint_text(report)` and raise `AnchorGateError`. The new gate replaces that `lint_text(report)` call in both.
- **What `lint_text` does today** (`scripts/output/anchor_lint.py:151-208`): checks 1-3 validate `<!--ref-->` markers are well-formed / non-orphan (KEEP — these guard the engine's 核心结论 block anchors); check 4 (`unanchored_empirical_lines`) is the prose requirement we DROP.
- **The G3 mirror** (`scripts/audit/anchor_resolution.py::check_branch1_md_anchors`): check 1 resolves every anchor to a real MD span (KEEP); check 2 reuses the SAME `unanchored_empirical_lines` to demand prose anchors (DROP). The shared function is deliberately identical across the two gates, so both must change together.
- **数字门 helpers to reuse** (`scripts/audit/g2_data_fidelity.py`): `_source_value_set(md)->set[float]` and `_mechanically_present(num, vals)->bool`, plus `extract_numbers(text)` (public, in `scripts/audit/ara_tree.py`). Task 1 promotes the two private helpers to the shared `ara_tree` read layer so both 数字门 and the new gate use one copy.
- **Tolerant knobs** (`scripts/audit_config.py:53-58`): `data_fidelity_tolerant` / `data_fidelity_max_unconfirmed=5` / `data_fidelity_max_unconfirmed_ratio=0.2`. The (b) layer reuses these (the report is tolerant like 数字门).
- **Run tests:** `uv run pytest` (pythonpath preconfigured). Lint: `uv run ruff check .claude/skills/paper-landscape/scripts/ tests/`. Standalone module: prefix `PYTHONPATH=.claude/skills/paper-landscape`.

---

## File structure (what changes and why)

| File | Change | Responsibility |
|---|---|---|
| `scripts/audit/ara_tree.py` | +2 public fns | `source_value_set` / `number_present` — the shared number-grounding read layer (Task 1) |
| `scripts/audit/g2_data_fidelity.py` | edit imports | use the promoted helpers (Task 1) |
| `scripts/output/branch1_gate.py` | **new** | the branch1 faithfulness gate: kept-lint + (b) grounding + (c) judge → `list[Finding]` (Tasks 2, 5) |
| `scripts/output/anchor_lint.py` | remove check 4 | free prose in the branch1 lint (Task 3) |
| `scripts/audit/anchor_resolution.py` | remove check 2 | free prose in the G3 auditor (Task 3) |
| `scripts/llm/config.py` | +1 seam | register `faithfulness` seam (Task 4) |
| `scripts/llm/seams.py` | +1 seam fn | `faithfulness_judge` + `build_seams` entry (Task 4) |
| `scripts/output/branch1_report.py` | edit lint site | call the shared gate (Task 5) |
| `scripts/output/branch1_llm.py` | edit lint site | call the shared gate + receive judge (Task 5) |
| `scripts/output/produce.py` | thread judge | pass the judge seam into `write_branch1_llm` (Task 5) |
| `config/llm.yaml` | route seam | `faithfulness` → hellorobotaxi, judge uses tier=fast (qwen3.7-plus ≠ writer max) (Task 6) |
| `tests/...` | new/updated | mirror each source change |

---

## Chunk 1: Shared grounding + (b) mechanical layer + free prose

### Task 1: Promote the number-grounding helpers to `ara_tree`

**Files:**
- Modify: `.claude/skills/paper-landscape/scripts/audit/ara_tree.py` (add after `extract_numbers`, ~line 43)
- Modify: `.claude/skills/paper-landscape/scripts/audit/g2_data_fidelity.py:44-66` (the two helper defs + their call sites)
- Test: `tests/audit/test_ara_tree.py` (create if absent) + existing `tests/audit/test_g2_data_fidelity.py` must stay green

- [ ] **Step 1: Write the failing test** — append to `tests/audit/test_ara_tree.py` (create with the import header copied from `tests/audit/test_g2_data_fidelity.py:1-7` if the file does not exist):

```python
from scripts.audit.ara_tree import number_present, source_value_set


def test_source_value_set_parses_distinct_values() -> None:
    vals = source_value_set("BLEU 28.4 vs 24.6; ratio 0.5 and 50%.")
    assert 28.4 in vals and 24.6 in vals and 0.5 in vals


def test_number_present_matches_by_value_not_form() -> None:
    vals = source_value_set("reaches 28.4 NDS over 1 run")
    assert number_present("28.40", vals) is True   # trailing zero
    assert number_present("1.0", vals) is True      # 1.0 == 1
    assert number_present("99.9", vals) is False     # absent
    assert number_present("not-a-number", vals) is False
```

- [ ] **Step 2: Run it to verify it fails**

Run: `uv run pytest tests/audit/test_ara_tree.py -q`
Expected: FAIL — `ImportError: cannot import name 'number_present'`.

- [ ] **Step 3: Add the two public helpers to `ara_tree.py`** — insert immediately AFTER the `extract_numbers` function (after line 42, before `_infer_claim_type`):

```python
def source_value_set(text: str) -> set[float]:
    """The distinct numeric VALUES present in `text` (parsed from its number
    tokens). Lets a candidate number be confirmed BY VALUE — cosmetic forms match
    (28.40 == 28.4, 1.0 == 1) — without an LLM. Shared by 数字门 (G2) and the
    branch1 忠实门."""
    values: set[float] = set()
    for tok in extract_numbers(text):
        try:
            values.add(float(tok))
        except ValueError:
            continue
    return values


def number_present(number: str, source_values: set[float]) -> bool:
    """True iff `number`'s VALUE appears in `source_values`. Conservative: a
    non-numeric token or an absent value returns False, so a fabricated number is
    never confirmed mechanically — it escalates to the LLM layer."""
    try:
        return float(number) in source_values
    except ValueError:
        return False
```

- [ ] **Step 4: Repoint `g2_data_fidelity.py` to the promoted helpers** — at `scripts/audit/g2_data_fidelity.py`:

OLD (the import block, line 24):
```python
from scripts.audit.ara_tree import extract_claim_registry, extract_numbers, find_ara_dir
```
NEW:
```python
from scripts.audit.ara_tree import (
    extract_claim_registry,
    extract_numbers,
    find_ara_dir,
    number_present,
    source_value_set,
)
```

OLD (delete the two private defs, lines 142-167 — `_source_value_set` and `_mechanically_present`, the ones inserted by the G2 two-layer commit; they now live in ara_tree):
```python
def _source_value_set(source_md: str) -> set[float]:
    ...
    return values


def _mechanically_present(number: str, source_values: set[float]) -> bool:
    ...
    except ValueError:
        return False
```
NEW: *(removed — replaced by the ara_tree imports)*

OLD (inside `run_g2`, the two call sites — search for `_source_value_set(source_md)` and `_mechanically_present(n, source_values)`):
```python
    source_values = _source_value_set(source_md)
    escalated = tuple(n for n in candidate_numbers if not _mechanically_present(n, source_values))
```
NEW:
```python
    source_values = source_value_set(source_md)
    escalated = tuple(n for n in candidate_numbers if not number_present(n, source_values))
```

- [ ] **Step 5: Run the tests**

Run: `uv run pytest tests/audit/test_ara_tree.py tests/audit/test_g2_data_fidelity.py -q`
Expected: PASS (21 G2 tests + the 2 new ara_tree tests).

- [ ] **Step 6: Lint + commit**

Run: `uv run ruff check .claude/skills/paper-landscape/scripts/audit/ tests/audit/`
```bash
git add .claude/skills/paper-landscape/scripts/audit/ara_tree.py \
        .claude/skills/paper-landscape/scripts/audit/g2_data_fidelity.py \
        tests/audit/test_ara_tree.py
git commit -m "refactor(audit): promote number-grounding helpers to ara_tree (shared by G2 + branch1)"
```

---

### Task 2: (b) mechanical report-grounding — new `branch1_gate` module

**Files:**
- Create: `.claude/skills/paper-landscape/scripts/output/branch1_gate.py`
- Test: `tests/output/test_branch1_gate.py` (create)

The report's own evidence tables are the paper's figures, already gated by 数字门 on the ARA — so (b) skips table rows and code fences, exactly like `unanchored_empirical_lines` (`anchor_lint.py:142-144`). It grounds only PROSE numbers.

- [ ] **Step 1: Write the failing test** — create `tests/output/test_branch1_gate.py` (copy the import-header style from a neighbor like `tests/output/test_branch1_llm.py:1-8`; the package root is on pythonpath, so `from scripts.output.branch1_gate import ...`):

```python
from __future__ import annotations

from scripts.output.branch1_gate import unconfirmed_report_numbers


def test_grounded_prose_numbers_pass() -> None:
    md = "Our model reaches 28.4 NDS and uses 10% of the data."
    report = "本文模型达到 28.4 NDS,仅用 10% 数据训练。"
    assert unconfirmed_report_numbers(report, md) == []


def test_invented_prose_number_is_flagged() -> None:
    md = "Our model reaches 28.4 NDS."
    report = "本文模型达到 99.9 NDS(凭空数字)。"
    assert unconfirmed_report_numbers(report, md) == ["99.9"]


def test_table_rows_and_code_fences_are_skipped() -> None:
    md = "Only 28.4 appears in source."
    report = "\n".join([
        "| Model | Score |",
        "| Ours | 77.7 |",       # table cell — skipped (paper's own figure, G2-gated)
        "```",
        "x = 88.8",               # code fence — skipped
        "```",
        "正文里 28.4 是真的。",     # grounded prose number → ok
    ])
    assert unconfirmed_report_numbers(report, md) == []
```

- [ ] **Step 2: Run it to verify it fails**

Run: `uv run pytest tests/output/test_branch1_gate.py -q`
Expected: FAIL — `ModuleNotFoundError: scripts.output.branch1_gate`.

- [ ] **Step 3: Create `scripts/output/branch1_gate.py`** with the (b) layer:

```python
"""branch1 忠实门 (ADR-0012) — verify the 理解阅读 is FAITHFUL to its verified ARA,
not that prose carries `<!--ref-->` anchors. Two layers assembled here:
(b) mechanical number-grounding of the report against the source MD (this module),
(c) a config-routed LLM judge (report ↔ ARA), wired in Task 5. The report MAY
carry numbers in natural prose; only an UNGROUNDED prose number is suspect.
"""

from __future__ import annotations

import re

from scripts.audit.ara_tree import extract_numbers, number_present, source_value_set

_FENCE = re.compile(r"^\s*```")


def unconfirmed_report_numbers(report_text: str, source_md: str) -> list[str]:
    """Prose numbers in `report_text` whose VALUE is NOT present in `source_md`.

    Skips markdown table rows (the paper's own figures, gated by 数字门 on the ARA)
    and fenced code blocks (illustrative). Order-preserving, de-duplicated.
    """
    source_values = source_value_set(source_md)
    bad: list[str] = []
    in_fence = False
    for raw in report_text.splitlines():
        if _FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence or raw.lstrip().startswith("|"):
            continue
        for n in extract_numbers(raw):
            if n not in bad and not number_present(n, source_values):
                bad.append(n)
    return bad
```

- [ ] **Step 4: Run the tests**

Run: `uv run pytest tests/output/test_branch1_gate.py -q`
Expected: PASS (3 tests).

- [ ] **Step 5: Lint + commit**

Run: `uv run ruff check .claude/skills/paper-landscape/scripts/output/branch1_gate.py tests/output/test_branch1_gate.py`
```bash
git add .claude/skills/paper-landscape/scripts/output/branch1_gate.py tests/output/test_branch1_gate.py
git commit -m "feat(branch1): (b) mechanical report number-grounding (ADR-0012)"
```

---

### Task 3: Free prose — drop the `<!--ref-->`-per-line requirement

**Files:**
- Modify: `.claude/skills/paper-landscape/scripts/output/anchor_lint.py:197-206` (remove check 4)
- Modify: `.claude/skills/paper-landscape/scripts/audit/anchor_resolution.py` (remove check 2 of `check_branch1_md_anchors`)
- Test: `tests/output/test_anchor_lint.py`, `tests/audit/test_anchor_resolution.py`

> **Grep callers before changing behavior.** `unanchored_empirical_lines` is called in exactly two places (`anchor_lint.py:200`, `anchor_resolution.py` check 2). After this task it is called nowhere; leave the function defined (it is still unit-tested and may back a future trained classifier — ROADMAP C4) but unused by the gates. `_is_empirical_assertion` import in `branch1_llm.py:27` becomes unused → Task 5 removes it.

- [ ] **Step 1: Write the failing test** — add to `tests/output/test_anchor_lint.py`:

```python
def test_unanchored_prose_number_no_longer_fails_lint() -> None:
    # ADR-0012: prose may carry numbers; lint_text must NOT flag them.
    from scripts.output.anchor_lint import lint_text
    report = "本文模型在 KITTI 上提升了 9.9 个百分点。"  # prose %, no <!--ref-->
    assert lint_text(report) == []


def test_malformed_core_block_anchor_still_fails() -> None:
    # The KEPT checks still guard the engine 核心结论 block's anchors.
    from scripts.output.anchor_lint import lint_text
    assert lint_text("结论 <!--ref:boguskind:x--> 收尾。") != []
```

- [ ] **Step 2: Run it to verify the first test fails**

Run: `uv run pytest tests/output/test_anchor_lint.py::test_unanchored_prose_number_no_longer_fails_lint -v`
Expected: FAIL — lint currently returns one `unanchored empirical assertion` violation.

- [ ] **Step 3: Remove check 4 from `lint_text`** — at `anchor_lint.py`:

OLD (lines 197-208 — the check-4 block through the function's final `return`):
```python
    # 4. paper-rolling addition — unanchored empirical PERFORMANCE assertions
    #    hard-block, via the SHARED line-based scan (skips fences / ref-lines /
    #    table rows). Same function the G3 auditor uses, so branch1 and G3 agree.
    for lineno, prose in unanchored_empirical_lines(text):
        violations.append(
            AnchorViolation(
                lineno,
                f"unanchored empirical assertion (no <!--ref--> marker): {prose[:60]!r}",
            )
        )

    return violations
```
NEW:
```python
    # ADR-0012: prose no longer needs <!--ref--> — the 理解阅读 may carry numbers in
    # natural prose; faithfulness is checked by branch1_gate ((b) grounding + (c)
    # judge). Checks 1-3 above still validate the engine 核心结论 block's anchors.
    return violations
```

- [ ] **Step 4: Remove check 2 from the G3 auditor** — at `scripts/audit/anchor_resolution.py::check_branch1_md_anchors`, delete the block beginning `# 2. Every empirical PERFORMANCE LINE must carry an anchor` and its loop over `unanchored_empirical_lines(...)`, keeping check 1 (anchor resolution) and the final `return GateVerdict(...)`. Replace the deleted block's comment with:
```python
    # ADR-0012: prose-anchor requirement dropped — 最终门 only RESOLVES the anchors
    # present (the engine 核心结论 block); prose faithfulness is branch1_gate's job.
```
*(Read the function body first — `sed -n '/def check_branch1_md_anchors/,/^def /p' scripts/audit/anchor_resolution.py` — and confirm check 2 is the only remaining `unanchored_empirical_lines` user before deleting.)*

- [ ] **Step 5: Run the tests**

Run: `uv run pytest tests/output/test_anchor_lint.py tests/audit/test_anchor_resolution.py -q`
Expected: PASS. (Any existing test asserting "unanchored prose fails" is now obsolete — update it to assert the new freed behavior, citing ADR-0012, rather than deleting coverage.)

- [ ] **Step 6: Lint + commit**

```bash
git add .claude/skills/paper-landscape/scripts/output/anchor_lint.py \
        .claude/skills/paper-landscape/scripts/audit/anchor_resolution.py \
        tests/output/test_anchor_lint.py tests/audit/test_anchor_resolution.py
git commit -m "feat(branch1,audit): free prose — drop <!--ref-->-per-line requirement (ADR-0012)"
```

---

## Chunk 2: (c) judge seam + gate wiring + config

### Task 4: (c) faithfulness judge — the 7th LLM seam

**Files:**
- Modify: `.claude/skills/paper-landscape/scripts/llm/config.py:46` (SEAMS) and `:54-61` (_DEFAULT_MODES)
- Modify: `.claude/skills/paper-landscape/scripts/llm/seams.py` (new `faithfulness_judge` + `build_seams`)
- Test: `tests/llm/test_seams.py` (or the file that tests seams), `tests/llm/test_llm_providers.py` (config routing)

The judge is **ground-truth-isolated from the writer**: it runs at **tier=fast**, so when routed to `hellorobotaxi` it uses `qwen3.7-plus` — different from the writer's `qwen3.7-max` (strong). The isolation is a routing discipline (Task 6 sets the route), not a hardcode.

- [ ] **Step 1: Write the failing test** — add to the seams test file (e.g. `tests/llm/test_seams.py`; if none, create mirroring `tests/llm/test_llm_providers.py` header):

```python
def test_build_seams_includes_faithfulness_judge() -> None:
    # ADR-0012: branch1 忠实门 (c) is the 7th routed seam.
    from scripts.llm.config import SEAMS
    from scripts.llm.seams import build_seams
    assert "faithfulness" in SEAMS
    assert "faithfulness_judge" in build_seams()
```

- [ ] **Step 2: Run it to verify it fails**

Run: `uv run pytest tests/llm/test_seams.py::test_build_seams_includes_faithfulness_judge -v`
Expected: FAIL — `"faithfulness" not in SEAMS`.

- [ ] **Step 3: Register the seam in `config.py`** — at `scripts/llm/config.py`:

OLD (line 46):
```python
SEAMS = ("analyzer", "skeptic", "rigor", "entailment", "expand", "writer")
```
NEW:
```python
SEAMS = ("analyzer", "skeptic", "rigor", "entailment", "expand", "writer", "faithfulness")
```

OLD (the `_DEFAULT_MODES` dict, ending line 60-61):
```python
    "writer": "inline",
}
```
NEW:
```python
    "writer": "inline",
    "faithfulness": "inline",  # ADR-0012: branch1 忠实门 judge (report ↔ ARA)
}
```

- [ ] **Step 4: Add `faithfulness_judge` to `seams.py`** — insert a new seam function before `build_seams` (after `write_report`, ~line 391). It loads the ARA's claims + evidence and asks the judge whether the report MATERIALLY MISLEADS relative to that verified ARA. Reuse the existing `_ask_json` / `_provider_for` helpers (same ones `skeptic_votes`/`rigor_scores` use):

```python
def faithfulness_judge(report_text: str, ara_dir: Path) -> dict:
    """branch1 忠实门 (c): is the 理解阅读 FAITHFUL to its verified ARA? (ADR-0012)

    Ground-truth-isolated from the writer: routed to the `faithfulness` provider
    and run at tier=fast, so it is a DIFFERENT model than the writer (writer=strong).
    Bar = "would a reader be MATERIALLY MISLED" (clear misattribution / overclaim),
    NOT prose-precision nitpicks — rigor lives in the ARA; this is a light backstop.

    Returns {"faithful": bool, "findings": [{"claim": str, "issue": str}, ...]}.
    Fails CLOSED: a malformed/empty judge response => faithful=False.
    """
    bundle = load_ara_bundle(ara_dir)  # reuse g3_seal's reader (claims + evidence)
    ara_text = "\n\n".join(f"=== {name} ===\n{text}" for name, text in bundle.items())
    if len(ara_text) > _MD_CHAR_CAP:
        ara_text = ara_text[:_MD_CHAR_CAP] + "\n[...TRUNCATED...]"
    _log("faithfulness: judging report ↔ ARA")
    prompt = (
        "You verify a Chinese human-facing REPORT against a VERIFIED knowledge pack "
        "(the ARA: claims + evidence tables). The ARA is ground truth. Flag ONLY "
        "places where the REPORT would MATERIALLY MISLEAD a reader: a metric/number "
        "attributed to the wrong system, a result overstated beyond what the ARA "
        "supports, or a claim the ARA contradicts. Do NOT flag wording, style, "
        "rounding, or general qualitative phrasing.\n\n"
        'Return JSON: {"faithful": true|false, "findings": '
        '[{"claim": "<short quote from the report>", "issue": "<<=1 line>"}]}. '
        "faithful=true with an empty findings list means no material misleading.\n\n"
        "=== VERIFIED ARA ===\n" + ara_text + "\n=== END ARA ===\n\n"
        "=== REPORT ===\n" + report_text + "\n=== END REPORT ==="
    )
    try:
        obj = _ask_json(prompt, seam="faithfulness", tier="fast", timeout=600.0, effort="medium")
    except RuntimeError as exc:
        _log(f"faithfulness: seam error, failing closed: {exc}")
        return {"faithful": False, "findings": [{"claim": "", "issue": f"seam error: {exc}"}]}
    if not isinstance(obj, dict) or "faithful" not in obj:
        return {"faithful": False, "findings": [{"claim": "", "issue": "malformed judge response"}]}
    findings = obj.get("findings") if isinstance(obj.get("findings"), list) else []
    return {"faithful": bool(obj["faithful"]), "findings": findings}
```

> **Promote the ARA bundle reader first (avoids a ruff `PLC2701` private-import error).** The reader is `_load_ara_bundle` in `scripts/audit/g3_seal.py:55`. As a preceding sub-step, rename it to a public `load_ara_bundle` (update its 1-2 internal callers inside `g3_seal.py` — `grep -n _load_ara_bundle scripts/audit/g3_seal.py`), then import the public name at the top of `seams.py`: `from scripts.audit.g3_seal import load_ara_bundle`. Confirm `_ask_json` / `_provider_for` / `_log` / `_MD_CHAR_CAP` are module-level in `seams.py` (they are — used by `skeptic_votes`/`rigor_scores`).

OLD (`build_seams` return, lines 400-407):
```python
    return {
        "resolve_analysis": resolve_analysis,
        "skeptic_votes": skeptic_votes,
        "rigor_scores": rigor_scores,
        "entailment_judge": entailment_judge,
        "expand_llm": expand_llm,
        "write_report": write_report,
    }
```
NEW:
```python
    return {
        "resolve_analysis": resolve_analysis,
        "skeptic_votes": skeptic_votes,
        "rigor_scores": rigor_scores,
        "entailment_judge": entailment_judge,
        "expand_llm": expand_llm,
        "write_report": write_report,
        "faithfulness_judge": faithfulness_judge,
    }
```

- [ ] **Step 5: Run the tests**

Run: `uv run pytest tests/llm/ -q`
Expected: PASS — but note: existing config tests build `_full_seam_yaml()` routing only 6 seams; they will now FAIL "seam 'faithfulness' is not routed". Update the test helper `_full_seam_yaml` (`tests/llm/test_llm_providers.py:163-184`) to also route `faithfulness: opencode`. Re-run.

- [ ] **Step 6: Lint + commit**

```bash
git add .claude/skills/paper-landscape/scripts/llm/config.py \
        .claude/skills/paper-landscape/scripts/llm/seams.py \
        tests/llm/
git commit -m "feat(llm): faithfulness_judge — 7th seam, branch1 忠实门 (c) (ADR-0012)"
```

---

### Task 5: Assemble the gate + wire into both branch1 paths

**Files:**
- Modify: `.claude/skills/paper-landscape/scripts/output/branch1_gate.py` (add `check_report_faithfulness`)
- Modify: `.claude/skills/paper-landscape/scripts/output/branch1_report.py:241-246` (lint site → gate)
- Modify: `.claude/skills/paper-landscape/scripts/output/branch1_llm.py` (lint site → gate, accept judge, drop unused `_is_empirical_assertion` import)
- Modify: `.claude/skills/paper-landscape/scripts/output/produce.py:186-193` (thread judge seam)
- Test: `tests/output/test_branch1_gate.py`, `tests/output/test_branch1_llm.py`

`AnchorGateError` already carries the failure string; `Finding` (from `scripts/audit/types.py`) is the verdict unit (same as 数字门). The gate returns the **hard-block** findings; tolerant (b) misses and the (c) judge's findings each map to a Finding.

- [ ] **Step 1: Write the failing test** — add to `tests/output/test_branch1_gate.py`:

```python
from scripts.output.branch1_gate import check_report_faithfulness


def _ok_judge(report_text, ara_dir):
    return {"faithful": True, "findings": []}


def _drift_judge(report_text, ara_dir):
    return {"faithful": False, "findings": [{"claim": "88.1 是我们的", "issue": "实为 baseline"}]}


def test_gate_passes_faithful_report(tmp_path) -> None:
    md = "Our model reaches 28.4 NDS using 10% data."
    report = "本文达到 28.4 NDS,仅用 10% 数据。"
    hard = check_report_faithfulness(report, md, tmp_path, judge=_ok_judge,
                                     max_unconfirmed=5, max_unconfirmed_ratio=0.2)
    assert hard == []


def test_gate_blocks_systematic_invented_numbers(tmp_path) -> None:
    md = "Only 28.4 appears."
    report = "凭空: 11.1, 22.2, 33.3, 44.4, 55.5, 66.6 全是编的。"  # 6 ungrounded > max 5
    hard = check_report_faithfulness(report, md, tmp_path, judge=_ok_judge,
                                     max_unconfirmed=5, max_unconfirmed_ratio=1.0)
    assert hard and all(f.is_hard_block for f in hard)


def test_gate_tolerates_a_single_miss(tmp_path) -> None:
    md = "Real numbers 28.4 and 24.6 here."
    report = "28.4 与 24.6 是真的,只有 99.9 手滑。"  # 1 miss within tolerance
    hard = check_report_faithfulness(report, md, tmp_path, judge=_ok_judge,
                                     max_unconfirmed=5, max_unconfirmed_ratio=0.2)
    assert hard == []


def test_gate_blocks_on_judge_drift(tmp_path) -> None:
    md = "Our model reaches 28.4 NDS."
    report = "本文达到 28.4 NDS。"  # numbers fine; judge flags misattribution
    hard = check_report_faithfulness(report, md, tmp_path, judge=_drift_judge,
                                     max_unconfirmed=5, max_unconfirmed_ratio=0.2)
    assert hard and any("baseline" in f.observation for f in hard)
```

- [ ] **Step 2: Run it to verify it fails**

Run: `uv run pytest tests/output/test_branch1_gate.py -q`
Expected: FAIL — `cannot import name 'check_report_faithfulness'`.

- [ ] **Step 3: Add `check_report_faithfulness` to `branch1_gate.py`** — append (it imports `Finding`/`Severity` from `scripts/audit/types.py`; read that file to confirm `Finding`'s required fields — `finding_id, severity, target, observation, is_hard_block, reasoning, suggestion`, matching `g2_data_fidelity.py:220-245`):

```python
from collections.abc import Callable

from scripts.audit.types import Finding, Severity


def check_report_faithfulness(
    report_text: str,
    source_md: str,
    ara_dir: "Path",
    *,
    judge: Callable[[str, "Path"], dict] | None = None,
    max_unconfirmed: int = 5,
    max_unconfirmed_ratio: float = 0.2,
) -> list[Finding]:
    """The branch1 忠实门 (ADR-0012): kept anchor-form lint + (b) tolerant number
    grounding + (c) optional LLM judge. Returns the HARD-BLOCK findings (empty =
    pass). `judge` is the (c) seam; None (deterministic fallback path) skips it.
    """
    findings: list[Finding] = []

    # Kept anchor-form checks (well-formed engine 核心结论 block anchors).
    for v in lint_text(report_text):
        findings.append(Finding(
            finding_id=f"AF{len(findings) + 1:02d}", severity=Severity.CRITICAL,
            target="report.md", observation=v.message, is_hard_block=True,
            reasoning="A malformed/orphan <!--ref--> anchor breaks the core-block truth chain.",
            suggestion="Fix or remove the malformed anchor.",
        ))

    # (b) tolerant mechanical grounding of prose numbers.
    bad = unconfirmed_report_numbers(report_text, source_md)
    total = len(extract_numbers(report_text)) or 1
    grounding_hard = len(bad) > max_unconfirmed or len(bad) > max_unconfirmed_ratio * total
    for n in bad:
        findings.append(Finding(
            finding_id=f"AF{len(findings) + 1:02d}",
            severity=Severity.CRITICAL if grounding_hard else Severity.MAJOR,
            target="report.md",
            observation=f"prose number {n!r} not grounded in the source MD"
                        + ("" if grounding_hard else " [TOLERATED]"),
            is_hard_block=grounding_hard,
            reasoning="A report number absent from the source MD is narration drift.",
            suggestion="Re-state the number from the ARA, or cut the claim.",
        ))

    # (c) semantic faithfulness judge (LLM path only).
    if judge is not None:
        verdict = judge(report_text, ara_dir)
        if not verdict.get("faithful", False):
            for jf in verdict.get("findings", []) or [{"claim": "", "issue": "report materially misleads vs ARA"}]:
                findings.append(Finding(
                    finding_id=f"AF{len(findings) + 1:02d}", severity=Severity.CRITICAL,
                    target="report.md",
                    observation=f"materially misleading vs ARA: {jf.get('claim','')} — {jf.get('issue','')}",
                    is_hard_block=True,
                    reasoning="The human report misrepresents the verified ARA (misattribution/overclaim).",
                    suggestion="Correct the claim to match the ARA.",
                ))

    return [f for f in findings if f.is_hard_block]
```
Add the import at the top of `branch1_gate.py` (after the existing imports): `from scripts.output.anchor_lint import lint_text`.

- [ ] **Step 4: Run the gate tests**

Run: `uv run pytest tests/output/test_branch1_gate.py -q`
Expected: PASS (7 tests).

- [ ] **Step 5: Wire into the deterministic path** (`branch1_report.py`):

OLD (lines 241-246):
```python
    violations = lint_text(report)
    if violations:
        raise AnchorGateError(
            "branch1 report failed three-layer citation gate (吸收-D1): "
            + "; ".join(v.message for v in violations[:5])
        )
```
NEW:
```python
    hard = check_report_faithfulness(report, md_text, ara_dir, judge=None)
    if hard:
        raise AnchorGateError(
            "branch1 report failed 忠实门 (ADR-0012): "
            + "; ".join(f.observation for f in hard[:5])
        )
```
Update `branch1_report.py` imports: replace `from scripts.output.anchor_lint import lint_text` with `from scripts.output.branch1_gate import check_report_faithfulness` (confirm `lint_text` is not used elsewhere in the file first via `grep -n lint_text scripts/output/branch1_report.py`).

- [ ] **Step 6: Wire into the LLM path** (`branch1_llm.py`) — add a `judge` parameter and call the gate. Read `write_branch1_llm`'s signature + lint site first.

At the signature (line ~212), add a keyword param `faithfulness_judge=None` (after `write_report`). At the lint site (the `lint_text(report)` block near the end), replace exactly as in Step 5 but pass the judge:
```python
    hard = check_report_faithfulness(report, md_text, ara_dir, judge=faithfulness_judge)
    if hard:
        raise AnchorGateError(
            "branch1 (LLM) report failed 忠实门 (ADR-0012): "
            + "; ".join(f.observation for f in hard[:5])
        )
```
Update `branch1_llm.py:27` import — **`_is_empirical_assertion` is STILL used by `_ground_line` (line 119), so KEEP it**; only drop `lint_text`. Result:
```python
from scripts.output.anchor_lint import _is_empirical_assertion
from scripts.output.branch1_gate import check_report_faithfulness
```

- [ ] **Step 7: Thread the judge through `produce.py`** — the seam must reach `write_branch1_llm`. Read `produce.py:160-195` for how `write_report` is passed. At `produce.py:186-191`:

OLD:
```python
        if write_report is not None:
            # audit R5 Finding 1: conditional kwarg keeps older write_report fakes working.
            ...
            write_branch1_llm(
                stage_person, candidate, stage_ai, md_path, write_report, key=key, **extra
            )
```
NEW (pass the judge from `extra`/a new param — add `faithfulness_judge=None` to the enclosing function's signature and forward it):
```python
        if write_report is not None:
            write_branch1_llm(
                stage_person, candidate, stage_ai, md_path, write_report,
                key=key, faithfulness_judge=faithfulness_judge, **extra
            )
```
Trace upward: the enclosing `produce.py` function and `produce_outputs` (line 242) must accept `faithfulness_judge` and the spoke must pass `seams["faithfulness_judge"]`. Grep the call chain `grep -rn "produce_outputs\|write_report=" scripts/` and thread the new optional kwarg end-to-end (default None keeps every existing caller + test working).

- [ ] **Step 8: Run the affected tests**

Run: `uv run pytest tests/output/ -q`
Expected: PASS. Fix any `produce`/`branch1_llm` test that constructs the call without the new kwarg (it defaults None, so most pass unchanged).

- [ ] **Step 9: Lint + commit**

```bash
git add .claude/skills/paper-landscape/scripts/output/ tests/output/
git commit -m "feat(branch1): assemble 忠实门 (kept-lint + (b) + (c)) into both paths (ADR-0012)"
```

---

### Task 6: Route the seam + wire the spoke gate-retry feedback

**Files:**
- Modify: `config/llm.yaml` (route `faithfulness`)
- Modify: `.claude/skills/paper-landscape/scripts/spoke.py` (pass `faithfulness_judge` into produce; map its failure to 锚点门 — already mapped via `AnchorGateError`)
- Test: `tests/llm/test_llm_providers.py` (config loads with 7 seams), `tests/test_spoke.py`

- [ ] **Step 1: Write the failing test** — add to the config test:

```python
def test_config_routes_faithfulness_seam(tmp_path) -> None:
    from scripts.llm.config import load_llm_config
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "llm.yaml").write_text(_full_seam_yaml(), encoding="utf-8")
    cfg = load_llm_config(tmp_path)
    assert cfg.for_seam("faithfulness").name == "opencode"
```
(Task 4 Step 5 already added `faithfulness: opencode` to `_full_seam_yaml`; if not, add it now.)

- [ ] **Step 2: Run it to verify it passes or fails**

Run: `uv run pytest tests/llm/test_llm_providers.py::test_config_routes_faithfulness_seam -v`
Expected: PASS if `_full_seam_yaml` routes it (from Task 4), else FAIL → add the route.

- [ ] **Step 3: Route the real seam** — at `config/llm.yaml`, in the `seams:` block (after `writer:`), add:
```yaml
  faithfulness: hellorobotaxi   # branch1 忠实门 (c); judge runs tier=fast → qwen3.7-plus (≠ writer max), ADR-0012
```

- [ ] **Step 4: Pass the seam into the spoke's produce call** — read `spoke.py` around where `produce_outputs` / branch1 is invoked (grep `grep -n "produce\|write_report\|faithfulness" scripts/spoke.py`). The spoke already receives `write_report` from `seams`; add `faithfulness_judge=seams.get("faithfulness_judge")` alongside it and forward through the produce chain threaded in Task 5 Step 7. (`spoke.py:431` already maps `AnchorGateError` → `锚点门`, so the failure surface is unchanged.)

- [ ] **Step 5: Run the suite**

Run: `uv run pytest -q && uv run ruff check .claude/skills/paper-landscape/scripts/ tests/`
Expected: all green, ruff clean.

- [ ] **Step 6: Commit**

```bash
git add config/llm.yaml .claude/skills/paper-landscape/scripts/spoke.py tests/
git commit -m "feat(config,spoke): route faithfulness seam + wire 忠实门 judge into branch1 (ADR-0012)"
```

---

### Task 7: End-to-end integration through the spoke

**Files:**
- Test: `tests/test_spoke.py` (new tests reusing the existing fixtures `_make_spoke` / `_SOURCE_MD` / `_CANDIDATE`)

Verifies the gate end-to-end: a faithful report with prose numbers PASSES; an invented-number report and a judge-flagged report each hard-block at 锚点门.

- [ ] **Step 1: Write the integration tests** — add to `tests/test_spoke.py` (mirror `test_spoke_g2_block_aborts_before_any_vault:529`'s shape; inject a `faithfulness_judge` fake via `make_spoke`):

```python
def test_spoke_branch1_passes_faithful_prose_numbers(tmp_path, fake_http, fake_cli):
    # A report carrying grounded prose numbers must NOT be quarantined (ADR-0012).
    _tier2_http(fake_http, dict(_CANDIDATE))
    spoke = _make_spoke(tmp_path, fake_http, fake_cli, analysis_md=_SOURCE_MD)
    result = spoke(dict(_CANDIDATE))
    assert result.status == "done"


def test_spoke_branch1_blocks_on_judge_drift(tmp_path, fake_http, fake_cli):
    # The (c) judge flagging material misleading → 锚点门 hard-block, no vaults.
    _tier2_http(fake_http, dict(_CANDIDATE))
    def _drift_judge(report_text, ara_dir):
        return {"faithful": False, "findings": [{"claim": "x", "issue": "misattributed"}]}
    spoke = _make_spoke(tmp_path, fake_http, fake_cli, analysis_md=_SOURCE_MD,
                        faithfulness_judge=_drift_judge)
    result = spoke(dict(_CANDIDATE))
    assert result.status == "failed"
    assert result.failure_class == FAILURE_AUDIT_BLOCK
```
> Add a `faithfulness_judge=None` kwarg to the `_make_spoke` helper (`tests/test_spoke.py:418`) and forward it into `make_spoke` (default None → existing tests unaffected). Confirm `make_spoke` accepts/forwards it (threaded in Tasks 5-6).

- [ ] **Step 2: Run them**

Run: `uv run pytest tests/test_spoke.py -k "branch1" -q`
Expected: PASS.

- [ ] **Step 3: Full green + commit**

```bash
uv run pytest -q
uv run ruff check .claude/skills/paper-landscape/scripts/ tests/
git add tests/test_spoke.py
git commit -m "test(spoke): branch1 忠实门 end-to-end — faithful prose passes, judge-drift blocks (ADR-0012)"
```

---

## After the plan lands

- **Revive the false-quarantined papers.** DiffusionForcing / Genie / the batch's branch1 failures were quarantined by the OLD prose-anchor gate. Run `scripts.revival` over the `_failed/` scenes — most should now pass under 忠实门.
- **Flip ADR-0012 + the CONTEXT.md 锚点门 entry from "implementation pending" to shipped** (drop the "(Per ADR-0012; implementation pending...)" parenthetical).
- **Sync the codemap** `docs/guides/codemaps/audit-gates.md` 锚点门 section (it still describes the `<!--ref-->`-per-line gate).
- **Watch for judge rubber-stamping.** If the qwen3.7-plus judge passes obviously-drifted reports, escalate the `faithfulness` route to a cross-family provider (local agent / different vendor) — config-only, no code change (the isolation is a routing discipline).

## Out of scope (YAGNI)

- Separate looser tolerance knobs for the report vs the ARA — this plan reuses 数字门's tolerant values; add report-specific knobs only if the shared values prove wrong in practice.
- A trained empirical-claim classifier (ROADMAP C4) — `unanchored_empirical_lines` stays defined but unused for a future plug-in.
