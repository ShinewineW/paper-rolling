# branch1 report — quality bar & anchor discipline

What makes a *good* `person_vault/{key}/report.md` (the illustrated Chinese
report), and the rules that keep it past the **branch1 忠实门**
(`scripts/output/branch1_gate.py`, ADR-0012; kept anchor-form lint in
`scripts/output/anchor_lint.py`, 吸收-D1). The producer is
`scripts/output/branch1_report.py`; the structure template is
`../templates/branch1-report.md`; a full instance is `../examples/worked-example.md`.

This is the headline anti-hallucination surface for the human report: a number
the reader sees must be traceable to the frozen `{ID}.md`, or it must not read as
a performance claim at all.

## The 忠实门 contract (hard-gate — violations raise `AnchorGateError`)

The branch1 gate is `scripts/output/branch1_gate.py` `check_report_faithfulness`
(ADR-0012). It keeps the anchor-form lint for the engine `## 核心结论` block AND
adds two faithfulness layers for free prose:

1. **Anchor grammar (engine 核心结论 block).** Every `<!--ref:slug-->` is immediately
   followed by a well-formed `<!--anchor:<kind>:<value>-->`,
   `kind ∈ {quote, page, section, paragraph, none}`. A `quote` value is URL-encoded,
   **≤ 25 words**, and contains no raw `--`. Non-`none` kinds need a non-empty value.
2. **No orphans.** An `<!--anchor:…-->` with no preceding well-formed `<!--ref-->` fails.
3. **Faithful prose numbers (ADR-0012 — replaces the old unanchored-claim block).**
   Prose MAY carry performance numbers in natural language WITHOUT a `<!--ref-->`
   marker. Instead: (b) every prose number must be mechanically grounded in
   `{ID}.md` (its value must appear in the source), and (c) an LLM judge confirms the
   report does not materially mislead vs the verified ARA (misattribution / overclaim).
   An ungrounded number or a misleading claim hard-blocks; 最终门 still resolves the
   核心结论 block's anchors.

## How to satisfy it (what the producer does — match it)

- **Ground every prose number.** Each number the report states in prose must have
  its value present in `{ID}.md` — the (b) layer matches by VALUE (`28.40` == `28.4`,
  `1.0` == `1`), so cosmetic forms are fine; a value absent from the source hard-blocks.
  The producer additionally anchors the engine `## 核心结论` block's numbers
  (`\d+(?:\.\d+)?`, integers AND decimals) so 最终门 can resolve them.
- **Keep illustration number-free.** `### 数学方法` and `### Loss 亮点解释` are
  deliberately **number-free and metric-cue-free** (use `math_intuition` /
  `math_toy_example` / `loss_highlight` analogies, not figures). That is *why* they
  pass the gate without anchors: they make no performance claim.
- **Quote anchors stay short.** ≤ 25 words, URL-encoded, no `--`.

## Faithfulness rules (quality, not just gate-passing)

- **Original figure is ground truth.** The Mermaid re-draw is explicitly labelled
  "简化示意,以原图为准". Never present the re-draw as authoritative; it is a unified-
  style illustration. classDef palette (Apache-2.0): `required` (blue input) /
  `output` (green terminal) / `optional` (yellow); first node → `required`, last → `output`.
- **No fixed-domain narrative on off-domain papers.** The math/loss/trend prose is
  sourced from the analyzer's per-paper fields; when a field is absent the producer
  falls back to a **neutral, number-free** line — it must not stamp an AD/diffusion
  (or any domain) story onto a paper that is not about it.
- **Exact figures live in the paired AI pack.** The report cross-links to
  `../../ai_package/{key}/ara/evidence/`; deep numeric detail belongs there, not in
  the prose.

## Anti-patterns (reject these)

- A prose number whose value is **not present** in `{ID}.md` → hard-block (忠实门
  (b) grounding). Numbers in natural prose are fine *if grounded* — ADR-0012 dropped
  the per-line `<!--ref-->` requirement.
- A number attributed to the **wrong system** / an overclaim vs the ARA → hard-block
  (忠实门 (c) judge).
- A **fabricated** number not in `{ID}.md` → **G2's skeptic catches it first** (runs
  before branch1) and the (b) layer would also reject it here; never invent figures.
- Anchoring with `kind: quote` but quoting > 25 words, or leaving a raw `--` inside.
- Asserting a domain-specific mechanism the source does not state (use the neutral
  number-free fallback instead).
- Treating the Mermaid re-draw as the real architecture (it is illustrative).
