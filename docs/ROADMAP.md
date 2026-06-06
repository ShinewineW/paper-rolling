# paper-rolling — capability roadmap (the "trustworthiness rail")

> Two rails. **Extensibility rail (done):** how easy it is to *add* parts —
> Source registry, `audit/ara_tree.py`, the centralized vault-branch set,
> `docs/EXTENDING.md` (ADR-0002). **Capability / trustworthiness rail (this
> doc):** how *strong and trustworthy* the engine's output is. These are
> field-standard patterns surfaced by benchmarking against the ≥20k★ tools and
> the project's three research references — present in the field, not yet in
> paper-rolling. Each item names the reference it draws from.

Status keys: `planned` · `in-progress` · `done`.

## Phase A — ingest-layer fidelity (self-contained, low-risk)

- **A1. Equation-ratio gate** — `planned`. Today the equation gate only fires on
  the all-or-nothing case (HTML had math but pandoc emitted **0** `$$`). PARTIAL
  loss (50 source equations, 5 survive) passes undetected. Add a ratio/threshold
  of emitted `$$` vs the source MathML count. *Source:* LaTeXML/pandoc
  practitioner consensus (pandoc handles vanilla LaTeX/MathML but drops complex
  cases).
- **A2. Table-fidelity gate** — `planned`. pandoc HTML→GFM table conversion is
  weak and there is **no** gate analogous to the equation gate; a garbled/dropped
  table passes silently. Tables are the landscape's core product, so this is the
  biggest silent ingest-failure risk. Add a table-presence/shape check (source
  `<table>` / MathML-table count vs emitted `|` tables). *Source:* Marker
  (TableConverter), MinerU (table→HTML), Docling (TableFormer) — all treat tables
  as a first-class problem.

## Phase B — discovery / output enrichment

- **B1. Retraction / withdrawal detection** — `planned`. discovery has
  preprint_flag + DOI cross-check but no retraction gate. Add an OpenAlex /
  Crossref `is_retracted` check in discovery so retracted papers are excluded (or
  flagged). *Source:* paper-qa retraction checks; ARS contamination triangulation.
- **B2. Bibliographic export** — `planned`. Outputs are MD vaults + ARA JSON with
  no reference-manager-interoperable export. Emit CSL-JSON / BibTeX for the
  discovered corpus so it is reusable. *Source:* ARS CSL-JSON `literature_corpus`;
  scientific-agent-skills pyzotero integration.

## Phase C — verification depth (the headline anti-hallucination gaps)

- **C1. Eval harness** — `planned`, **do before C2**. A fixture set of
  known-fabricated and known-clean papers to MEASURE G2/G3 precision/recall, so
  "we have gates" becomes "the gates catch fabrication at rate X". *Source:*
  paper-qa (0% hallucinated citations), STORM (FreshWiki), AI-Scientist
  (near-human reviewer correlation).
- **C2. Cross-model verification (the deferred B10)** — `planned`. The single
  biggest benchmark gap: G2/G3 verification is same-family multi-vote, which the
  literature warns suffers conformity / premature convergence. Route the skeptic /
  rigor / entailment seams (a sample or all) through a **heterogeneous** model
  family (the already-wired Codex). *Source:* prover-skeptic + adversarial-debate
  literature; ARS / AI-Research-SKILLs reviewer-diversity. Prove it with C1.
- **C3. Claim-audit defect taxonomy (the deferred B8)** — `planned`. G2 is binary
  block/pass; classify WHAT failed (transcription typo vs fabrication vs
  unverifiable) so findings are actionable. *Source:* ARS claim_audit defect-stage
  taxonomy; AI-Scientist multi-dimension rubric.
- **C4. NLI / guarded entailment (the deferred B9)** — `planned`. anchor /
  entailment use metric-cue heuristics; route claim↔evidence entailment through a
  trained NLI / factual-consistency check that generalizes beyond keyword cues.
  *Source:* ARS uncited-assertion guarded detector; factual-consistency models.

## Carried from the oh-my-codex audit (R21, open)

- **W1. Ship production wiring factories** — `planned` (owner decision pending).
  `run_campaign` requires `discover` / `http` / `run_cli` injected; the
  "only LLM is not in code" claim is not true as delivered. Ship `scripts/wiring.py`
  (`build_http` urllib / `build_run_cli` subprocess / `build_discover` source
  assembly) so only the LLM seams are external — OR formally adopt the
  agent-composes-infra skill model and correct the docs. See the review log
  (`attn_sink/oh-my-codex-review-log.md`, Round 21).

## Recommended execution order

A1 → A2 → B1 → B2 → C1 → C2 → C3 → C4. Rationale: the clean, self-contained
fidelity gates first (momentum, low risk); the eval harness (C1) before
cross-model (C2) so C2's value is measurable; C2 is the headline gap; C3/C4 deepen
the audit semantics. W1 (wiring) is an independent owner decision.
