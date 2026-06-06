# paper-rolling — capability roadmap (the "trustworthiness rail")

> **创建日期**: 2026-06-07
> **更新日期**: 2026-06-07
> **适用环境**: `~/Coding/paper-rolling/` 仓库；配合 `docs/guides/EXTENDING.md` 阅读；状态随能力落地持续更新。

---

> Two rails. **Extensibility rail (done):** how easy it is to *add* parts —
> Source registry, `audit/ara_tree.py`, the centralized vault-branch set,
> `docs/guides/EXTENDING.md` (ADR-0002). **Capability / trustworthiness rail (this
> doc):** how *strong and trustworthy* the engine's output is. These are
> field-standard patterns surfaced by benchmarking against the ≥20k★ tools and
> the project's three research references — present in the field, not yet in
> paper-rolling. Each item names the reference it draws from.

Status keys: `planned` · `in-progress` · `done`.

> **Status (2026-06-07): the capability rail is COMPLETE.** A1, A2, B1, B2, C1,
> C2, C3, C4 are all `done` and committed, each with regression tests. The only
> remaining item is **W1 (production wiring)**, which is an owner decision carried
> over from the oh-my-codex audit (R21), not a capability gap.

## Phase A — ingest-layer fidelity (self-contained, low-risk)

- **A1. Equation-ratio gate** — `done`. Today the equation gate only fires on
  the all-or-nothing case (HTML had math but pandoc emitted **0** `$$`). PARTIAL
  loss (50 source equations, 5 survive) passes undetected. Add a ratio/threshold
  of emitted `$$` vs the source MathML count. *Source:* LaTeXML/pandoc
  practitioner consensus (pandoc handles vanilla LaTeX/MathML but drops complex
  cases).
- **A2. Table-fidelity gate** — `done`. pandoc HTML→GFM table conversion is
  weak and there is **no** gate analogous to the equation gate; a garbled/dropped
  table passes silently. Tables are the landscape's core product, so this is the
  biggest silent ingest-failure risk. Add a table-presence/shape check (source
  `<table>` / MathML-table count vs emitted `|` tables). *Source:* Marker
  (TableConverter), MinerU (table→HTML), Docling (TableFormer) — all treat tables
  as a first-class problem.

## Phase B — discovery / output enrichment

- **B1. Retraction / withdrawal detection** — `done`. discovery has
  preprint_flag + DOI cross-check but no retraction gate. Add an OpenAlex /
  Crossref `is_retracted` check in discovery so retracted papers are excluded (or
  flagged). *Source:* paper-qa retraction checks; ARS contamination triangulation.
- **B2. Bibliographic export** — `done`. Outputs are MD vaults + ARA JSON with
  no reference-manager-interoperable export. Emit CSL-JSON / BibTeX for the
  discovered corpus so it is reusable. *Source:* ARS CSL-JSON `literature_corpus`;
  scientific-agent-skills pyzotero integration.

## Phase C — verification depth (the headline anti-hallucination gaps)

- **C1. Eval harness** — `done` (done before C2, as planned). A fixture set of
  known-fabricated and known-clean papers to MEASURE G2/G3 precision/recall, so
  "we have gates" becomes "the gates catch fabrication at rate X". *Source:*
  paper-qa (0% hallucinated citations), STORM (FreshWiki), AI-Scientist
  (near-human reviewer correlation).
- **C2. Cross-model verification (the deferred B10)** — `done`. The single
  biggest benchmark gap: G2/G3 verification is same-family multi-vote, which the
  literature warns suffers conformity / premature convergence. Route the skeptic /
  rigor / entailment seams (a sample or all) through a **heterogeneous** model
  family (the already-wired Codex). *Source:* prover-skeptic + adversarial-debate
  literature; ARS / AI-Research-SKILLs reviewer-diversity. Prove it with C1.
- **C3. Claim-audit defect taxonomy (the deferred B8)** — `done`. G2 is binary
  block/pass; classify WHAT failed (transcription typo vs fabrication vs
  unverifiable) so findings are actionable. *Source:* ARS claim_audit defect-stage
  taxonomy; AI-Scientist multi-dimension rubric.
- **C4. NLI / guarded entailment (the deferred B9)** — `done`. anchor /
  entailment use metric-cue heuristics; route claim↔evidence entailment through a
  trained NLI / factual-consistency check that generalizes beyond keyword cues.
  *Source:* ARS uncited-assertion guarded detector; factual-consistency models.

## Carried from the oh-my-codex audit (R21) — RESOLVED (owner overrule, evidence-based)

- **W1. Production wiring** — `optional` (BLOCKING severity OVERRULED by the owner,
  2026-06-07, grounded in open-source evidence). Codex's R21 BLOCKING ("not runnable
  without writing adapter code") misjudges the SKILL operating model: `anthropics/skills`
  ship no standalone runner and rely on the host agent harness to orchestrate, so the
  absence of a standalone autonomous `main()` is by design, not a defect — and the
  LLM seams must be the agent (correctly already injected). The remaining ~40 lines of
  deterministic glue (`build_http`/`build_run_cli`/`build_discover`) are an OPTIONAL,
  norm-aligned convenience: every comparable project (gpt-researcher, paper-qa, STORM,
  smolagents) AND Anthropic's own skills (docx/pdf) ship deterministic helper scripts,
  and `ingest(http=…, run_cli=…)` needs Python callables the agent's WebFetch/Bash tools
  cannot directly be — so shipping the factories is the norm, but it is low-priority
  polish, NOT a gate. See `attn_sink/oh-my-codex-review-log.md` (R21) + the 2026-06-07
  evidence pass.

## Recommended execution order

A1 → A2 → B1 → B2 → C1 → C2 → C3 → C4. Rationale: the clean, self-contained
fidelity gates first (momentum, low risk); the eval harness (C1) before
cross-model (C2) so C2's value is measurable; C2 is the headline gap; C3/C4 deepen
the audit semantics. W1 (wiring) is an independent owner decision.
