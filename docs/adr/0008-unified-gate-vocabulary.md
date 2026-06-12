# 0008 — Unified gate vocabulary (communication-only, code identifiers untouched)

> **Status**: accepted

The per-paper pipeline has four gate checkpoints whose names were scattered
across the codebase and docs (`Seal-1`, `G2`, `三层锚点`, `G3`, `Seal Level 2`,
plus internal D-codes `吸收-D1`, `audit-D1`…), making them costly to talk about.
We adopt **one canonical Chinese name per checkpoint for all human
communication** and **deliberately do NOT rename the code identifiers**.

## The four gates (canonical order)

| Canonical | Stage | Code identifier(s) | Mechanical / LLM | Guards |
|---|---|---|---|---|
| **结构门** | after branch2 | `Seal-1` / `validate_ara_tree` / 吸收-D8 | mechanical | SSOT exploration-tree is structurally valid (node types, required fields, `also_depends_on` points to a real node) |
| **数字门** | branch2 → branch1 | `G2` / data-fidelity / audit-D1 | LLM (skeptic, N votes) | every evidence number appears in the source MD |
| **锚点门** | inside branch1 | 忠实门 / 吸收-D1 + ADR-0012 / `AnchorGateError` | mechanical + LLM judge | ADR-0012 (name kept): prose numbers GROUNDED in the source MD ((b)) + report not materially misleading vs the ARA ((c)); engine 核心结论 block still carries `<!--ref-->` anchors |
| **最终门** | after both chains | `G3` / seal / Seal Level 2 | mixed | composite of 4 sub-checks (below) |

**最终门 (G3) sub-checks**: (a) anchor resolution — claims resolve to source MD;
(b) entailment — each claim's experiment design matches its claim type (LLM);
(c) 6-dim rigor score (LLM); (d) equation fidelity — count/hash vs
content_list (mechanical).

## Why communication-only (rejected: rename the code)

`G2` / `G3` / `Seal-1` are entrenched across source, tests, ADRs, and docs.
Renaming identifiers is a large, regression-prone refactor whose only payoff is
cosmetic — the cognitive load was in *conversation*, not in the code. A glossary
fixes the conversation cost at zero risk. Future readers: the code names and the
canonical names refer to the same gates on purpose; do NOT "tidy up" by renaming
identifiers to match the Chinese names.
