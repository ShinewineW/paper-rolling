# 0008 — Unified gate vocabulary (communication-only, code identifiers untouched)

> **Status**: accepted

The per-paper pipeline has four gate checkpoints whose names were scattered
across the codebase and docs (`Seal-1`, `G2`, `三层锚点`, `G3`, `Seal Level 2`,
plus internal D-codes `吸收-D1`, `audit-D1`…), making them costly to talk about.
We adopt **one canonical Chinese name per checkpoint for all human
communication** and **deliberately do NOT rename the code identifiers**.

## The gates (canonical order — three after ADR-0012)

| Canonical | Stage | Code identifier(s) | Mechanical / LLM | Guards |
|---|---|---|---|---|
| **结构门** | after branch2 | `Seal-1` / `validate_ara_tree` / 吸收-D8 | mechanical | SSOT exploration-tree is structurally valid (node types, required fields, `also_depends_on` points to a real node) |
| **数字门** | branch2 → branch1 | `G2` / data-fidelity / audit-D1 | LLM (skeptic, N votes) | every evidence number appears in the source MD |
| **最终门** | after both chains | `G3` / seal / Seal Level 2 | mixed | composite sub-checks (below) |

> **ADR-0012 修订(2026-06-13,已落地)**:**锚点门不再是一道门**。branch1 人链报告改为不设
> 任何硬门——原 (b) 数字落源 + (c) 判官不再硬拦,转为生成报告**开篇的「评价」**(对照 ARA 的忠实性
> 自述,judge 写、永不拦)。**「评价」是 branch1 的内容产物,不是 checkpoint。** 因此**规范门只剩
> 三道,全在 ARA 上:结构门 → 数字门 → 最终门**;最终门的"锚点解析"子检查也随之移除。下表保留旧的
> 锚点门行仅作历史对照。

| ~~**锚点门**(已退役为「评价」,ADR-0012)~~ | ~~inside branch1~~ | ~~忠实门 / `AnchorGateError`~~ | ~~mechanical + LLM judge~~ | ~~(历史)prose 落源 + 判官;现改为开篇「评价」,不拦~~ |

**最终门 (G3) sub-checks** (ADR-0012 removed the branch1 anchor-resolution sub-check):
(a) entailment — each claim's experiment design matches its claim type (LLM);
(b) 6-dim rigor score (LLM); (c) equation fidelity — count/hash vs
content_list (mechanical).

## Why communication-only (rejected: rename the code)

`G2` / `G3` / `Seal-1` are entrenched across source, tests, ADRs, and docs.
Renaming identifiers is a large, regression-prone refactor whose only payoff is
cosmetic — the cognitive load was in *conversation*, not in the code. A glossary
fixes the conversation cost at zero risk. Future readers: the code names and the
canonical names refer to the same gates on purpose; do NOT "tidy up" by renaming
identifiers to match the Chinese names.
