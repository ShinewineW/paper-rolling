# branch1 report — quality bar & faithfulness assessment

<!-- Generated: 2026-06-13 | Scope: branch1 opening assessment design (ADR-0012 rev) -->

> **更新日期**: 2026-06-13
> **ADR**: ADR-0012 rev (2026-06-12 landed)

What makes a *good* `person_vault/{key}/report.md` (the illustrated Chinese
report). The producer is `scripts/output/branch1_report.py`; the structure
template is `../templates/branch1-report.md`; a full instance is
`../examples/worked-example.md`. Faithfulness is surfaced in the opening
**`## 评价`** section (non-blocking assessment), not via a hard gate.

This is the headline anti-hallucination surface for the human report: a number
the reader sees must be traceable to the frozen `{ID}.md`, or it must not read as
a performance claim at all.

## The 评价 (opening assessment — fail-soft, never blocks)

The opening `## 评价` block (`scripts/output/branch1_gate.py` `build_assessment`,
ADR-0012 rev) surfaces three pieces of information to the reader:

1. **(b) Ungrounded numbers.** A mechanical list of numbers in the prose that do
   NOT appear in the verified ARA (`corpus/{ID}/{ID}.md`). If the ARA is
   unreadable, the list says "未能读取 ARA，本次未核对" (never a false
   all-clear). This is a FACT for the reader, not a gate — it surfaces drift but
   never blocks publication.
2. **(c) Judge's note.** An LLM judge compares the human report against the
   verified ARA and writes a Chinese prose advisory note (e.g., flagging
   misattribution, overclaim, or certifying "与 ARA 核对无问题"). The note is
   fail-soft: if the judge fails or is absent, the note is simply omitted.
3. **AUDIT_FLAGS context.** The ARA's own `AUDIT_FLAGS.md` body (if present) is
   quoted inline so the reader sees any caveats the analyzer flagged.

**Critically: the `## 评价` never fails the report.** It is an advisory opening,
fail-soft at every layer (unreadable ARA → omit facts; judge fails → omit note;
missing ARA → omit all). Reports with ungrounded numbers or unfavourable judge
notes still publish — faithfulness is transparent to the reader, not a gate.

## Writing quality bar (what the producer does — match it)

- **Ground every prose number in the ARA.** Each number the report states in
  prose must have its value present in `{ID}.md`. The opening `## 评价` will
  surface any ungrounded numbers as a fact for the reader. Grounding by VALUE:
  `28.40` == `28.4`, `1.0` == `1` (cosmetic forms fine).
- **Keep illustration number-free.** `### 数学方法` and `### Loss 亮点解释` are
  deliberately **number-free and metric-cue-free** (use `math_intuition` /
  `math_toy_example` / `loss_highlight` analogies, not figures). They make no
  performance claim and have nothing to ground.
- **`## 核心结论` is plain prose.** No anchors, no `<!--ref-->` machinery
  (RETIRED, ADR-0012 rev). Write it as a clear, vivid summary of the paper's
  contributions and key findings — faithful, not anchored.

## Writing discipline (quality, not gate-passing)

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

## Anti-patterns (avoid these)

- A prose number whose value is **not present** in `{ID}.md`. The opening
  `## 评价` will flag it as ungrounded. While the report still publishes, unfaithful
  numbers erode credibility.
- A number attributed to the **wrong system** / an overclaim vs the ARA. The judge
  note will flag this. Again, still publishes, but surfaced to the reader.
- A **fabricated** number not in the ARA. **G2's skeptic catches it first** (runs
  before branch1) and hard-blocks it; never invent figures.
- Asserting a domain-specific mechanism the source does not state (use the neutral
  number-free fallback instead).
- Treating the Mermaid re-draw as the real architecture (it is illustrative).
