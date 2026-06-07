# branch1 report — quality bar & anchor discipline

What makes a *good* `person_vault/{key}/report.md` (the illustrated Chinese
report), and the rules that keep it past the **three-layer anchor hard-gate**
(`scripts/output/anchor_lint.py`, 吸收-D1). The producer is
`scripts/output/branch1_report.py`; the structure template is
`../templates/branch1-report.md`; a full instance is `../examples/worked-example.md`.

This is the headline anti-hallucination surface for the human report: a number
the reader sees must be traceable to the frozen `{ID}.md`, or it must not read as
a performance claim at all.

## The anchor contract (hard-gate — violations raise `AnchorGateError`)

1. **Grammar.** Every `<!--ref:slug-->` is immediately followed by a well-formed
   `<!--anchor:<kind>:<value>-->`, `kind ∈ {quote, page, section, paragraph, none}`.
   A `quote` value is URL-encoded, **≤ 25 words**, and contains no raw `--`
   (it would terminate the HTML comment early). Non-`none` kinds need a non-empty value.
2. **No orphans.** An `<!--anchor:…-->` with no preceding well-formed `<!--ref-->` fails.
3. **No unanchored performance claims (the paper-rolling addition).** A line that
   carries a number next to a metric/comparison cue (`NDS`/`mAP`/`accuracy`/`F1`/
   `提升`/`超过`/`达到`/…), or a `%` / `个百分点`, or an English empirical verb
   (`achieved`/`outperformed`/`improved`/…) **must** carry a `<!--ref-->` marker —
   or it hard-blocks. Definition phrases (`is defined as` / `定义为` / `是指` …) are exempt.

## How to satisfy it (what the producer does — match it)

- **Anchor every grounded number.** In `## 摘要翻译`, for each claim, every number
  matching `\d+(?:\.\d+)?` (**integers AND decimals** — `87` and `12.4` both) that
  is found in `{ID}.md` gets an anchor. Anchoring only decimals once left integer
  claims like "61 NDS" unanchored and the lint hard-blocked them — anchor both.
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

- A number with a metric cue and **no** `<!--ref-->` → hard-block (anchor lint #3).
- A **fabricated** number not in `{ID}.md` → this gate can't see it, but **G2's
  skeptic catches it first** (runs before branch1); never invent figures.
- Anchoring with `kind: quote` but quoting > 25 words, or leaving a raw `--` inside.
- Asserting a domain-specific mechanism the source does not state (use the neutral
  number-free fallback instead).
- Treating the Mermaid re-draw as the real architecture (it is illustrative).
