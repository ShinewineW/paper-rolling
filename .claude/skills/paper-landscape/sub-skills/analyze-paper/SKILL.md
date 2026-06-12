---
name: analyze-paper
description: The paper-landscape analyzer sub-agent — turns a frozen paper MD into the ARA analysis bundle that backs the resolve_analysis seam.
---

# analyze-paper (resolve_analysis seam role)

This sub-skill is the **independent sub-agent** that backs the
`resolve_analysis` seam — the first of the five LLM seams in
[`../../SKILL.md`](../../SKILL.md) (§ *Wiring the model seams*). Per the engine
contract, every `resolve_analysis` call **MUST** be a fresh Agent-tool
invocation (its own sub-agent), so the downstream audit votes (G2 skeptic, G3
rigor/entailment) stay uncorrelated with the analyzer that produced the numbers.

## Role

Read a single frozen paper and emit its analysis bundle — nothing else. You are
called once per paper, inside the per-paper spoke, **before** any output is
written: `produce_outputs` (`../../scripts/output/produce.py`) calls
`resolve_analysis(md_path, candidate)` and feeds the result into `write_branch2`
→ `write_branch1`. You never write to a vault, the ledger, or the corpus; you
only return the dict.

## Contract

```
resolve_analysis(md_path: Path, candidate: dict) -> dict
```

- **`md_path`** — the frozen `corpus/{ID}/{ID}.md`: the MD-only truth base and
  the anchor target. This is your **only** source of paper content. Read it in
  full.
- **`candidate`** — the discovery record (identity + metadata: `title`,
  `arxiv_id`, `doi`, …). Use for identity/context, **not** as a content source.
- **returns** — the ARA analysis bundle (a `dict`) consumed by `branch2_ara`,
  `branch1`, and the `landscapes` cross-paper comparator.

### Required headline keys [MUST]

The returned dict **MUST** include the three headline-metric keys the landscape
table reads off `ai_package/*/ara/PAPER.md` frontmatter:

- `headline_metric: str` — e.g. `"NDS"`
- `headline_value: float`
- `params_million: float`

A paper missing headline frontmatter is **dropped** from the cross-paper table
(`../../scripts/landscapes.py`). Do not omit these.

### Full bundle shape

The headline keys are the hard contract; the rest of the bundle (`overview`,
`problem`, `claims`, `concepts`, `experiments`, `related_work`, `architecture`,
`algorithm`, `heuristics`, `configs_training`, `configs_model`, `environment`,
`execution_stub`, `innovations`, `exploration_tree`, `evidence_tables`,
`loss_highlight`, `math_intuition`, `trend`, …) follows the ARA schema. **Do not
restate it here** — see [`../../references/ara-schema.md`](../../references/ara-schema.md)
for the authoritative shape, and [`../../examples/sample-ara-bundle.json`](../../examples/sample-ara-bundle.json)
for a complete, copy-pasteable instance.

## Discipline

- **Faithful to source.** Every claim traces to the frozen MD. Do not import
  outside knowledge about the paper or its results.
- **Exact numbers ONLY under `evidence`.** Headline values and any quantitative
  claim must be grounded in the MD text. Fabricated or paraphrased-into-existence
  numbers are caught downstream: G2 (`../../scripts/audit/g2_data_fidelity.py`)
  runs ground-truth-isolated skeptic votes over your numbers and **hard-blocks**
  fabrication before branch1 promotion. A report number that isn't grounded in the
  MD — or that misattributes a result — later raises `AnchorGateError` in branch1's
  忠实门 (ADR-0012: (b) grounding + (c) judge; 吸收-D1).
- **Independent invocation [MUST].** A single, isolated Agent-tool call per
  paper. No shared analyzer state across concurrent spokes — `resolve_analysis`
  is injected as a keyword arg precisely so concurrent spokes never share or
  mutate one analyzer (`produce_outputs` docstring).

## See also

- [`../../SKILL.md`](../../SKILL.md) — engine overview, pipeline order, all five seams.
- [`../../references/ara-schema.md`](../../references/ara-schema.md) — full ARA bundle shape.
- [`../../examples/worked-example.md`](../../examples/worked-example.md) — your output
  in the full pipeline; [`../../examples/sample-ara-bundle.json`](../../examples/sample-ara-bundle.json)
  is the literal target dict.
- Sibling audit seams back the gates that check this analyzer's output: G2
  skeptic, G3 rigor reviewer, G3 entailment judge.
