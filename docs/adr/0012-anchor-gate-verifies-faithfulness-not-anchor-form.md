# 0012 — 锚点门 verifies report FAITHFULNESS, not anchor-form (amends ADR-0006)

> **Status**: accepted + IMPLEMENTED (`feat/branch1-faithfulness-gate`, 2026-06-12; cross-reviewed by Codex, 4 rounds). Amends ADR-0006's "a number in prose instead of a table is a failure" premise.

The 锚点门 (inside branch1) was hard-blocking **content-perfect** papers: a 理解阅读
whose ARA had already passed 结构门 + 数字门 (e.g. DiffusionForcing — ARA 70/70 numbers
grounded, structure valid) was quarantined only because its **prose** carried numbers /
percentages without a `<!--ref-->` marker (e.g. "视频实验只用约 10% 的总数据"). This is the
same form-over-substance trap we removed from 数字门: a **mechanical discipline (self-attach
an anchor to every empirical line)** was offloaded onto the LLM writer, which (a) fails it
unreliably and (b) does not even prove the number is real — a bogus `<!--ref-->` passes the
lint. The writer prompt's companion rule "don't put precise numbers in prose" also made
reports stilted and was regularly **leaked verbatim into the report body**.

## Decision

The 理解阅读 (human report) **MAY contain numbers in prose**. The 锚点门 stops gating on
"did the LLM attach `<!--ref-->` to every empirical prose line" and instead verifies the
report is **faithful**, in two layers (mirroring the 数字门 redesign):

- **(b) mechanical number-grounding** — every number in the report prose must appear in the
  source MD (reuse 数字门's value-match machinery). Runs in **tolerant** mode: a stray miss is
  flagged, only systematic ungrounded numbers hard-block.
- **(c) semantic faithfulness judge** — a **new LLM seam, routed through `config/llm.yaml`**
  like every seam (NOT hardcoded), comparing report ↔ ARA for misattribution / overclaim.
  Bar = "would a reader be **materially misled**", not prose-precision nitpicks.

Both are **content gates**: on failure they feed the finding back to the branch1 writer
(ADR-0006's content-gate-adapts path), bounded rounds, then `_failed/<key>/`. No laundering
risk — unlike 数字门, the writer's truth source (the verified ARA) is in hand, so "correct the
report to match the ARA" is the goal, not a fabrication launder; (c) backstops any number
swapped in merely to pass (b).

## Guiding principle — why the human chain can be loose

Rigor concentrates in the **ARA (AI知识库)** — the AI-consumed SSOT, strictly held by
结构门 + 数字门 + 最终门. The 理解阅读 is its **readable human derivative**, so it gets only a
LIGHT faithfulness backstop, lenient **above a "do not seriously mislead" floor**. The floor
is non-negotiable (理解阅读 is a published Release product), but precision/style above it is
not gated.

## Scope — surgical (ADR-0006's expression guard kept where it is mechanical)

- Prose is freed: no `<!--ref-->` self-anchoring required; faithfulness via (b)+(c).
- The engine-generated, **mechanically-anchored 核心结论 block KEEPS its anchors** (no LLM
  burden); 最终门's anchor-resolution sub-check narrows to resolving THAT block.
- **Name unchanged: still 锚点门** (ADR-0008 — canonical names are communication-only; code
  identifiers `AnchorGateError` / 三层锚点 stay). The name is now a mild misnomer kept for
  continuity; the gate's job is faithfulness.

## Consequences

- A faithful report with natural prose numbers passes — the DiffusionForcing / Genie class of
  false-quarantine ends. Papers failed under the OLD 锚点门 are revivable once this lands.
- 数字门 stays **blind / no-feedback** (ADR-0006 unchanged for it); only the branch1 gate's
  premise changes here.
- New seam to route in `config/llm.yaml`, default to a non-writer model (writer = qwen3.7-max
  → judge = qwen3.7-plus today). **judge ⊥ writer** isolation is a routing discipline, not a
  hardcode — escalatable to a cross-family provider if the judge starts rubber-stamping.
