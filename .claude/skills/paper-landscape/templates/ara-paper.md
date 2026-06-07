<!--
TEMPLATE — ai_package/{key}/ara/PAPER.md  (branch2, written by scripts/output/branch2_ara.py::_paper_md)
This is the cross-paper comparator's entry point; its frontmatter is a HARD contract.
{placeholders} are filled from the resolve_analysis ARA bundle (see ../references/ara-schema.md
+ ../examples/sample-ara-bundle.json). Keep the frontmatter keys EXACT — landscapes.py reads them.
-->
---
key: {candidate.arxiv_id or candidate.doi}    # the shared vault key (arxiv_id, else DOI fallback)
title: {candidate.title}
authors: [{candidate.authors}]
year: {candidate.year}
venue: {candidate.venue}
doi: {candidate.doi or "arXiv:"+arxiv_id}
ara_version: "1.0"
schema_version: "1.0"
domain: {analysis.domain}            # neutral fallback "deep learning" if the analyzer omits it
keywords: [{first 8 analysis.concepts[].name}]
claims_summary:                      # analysis.claims[:3] statements
  - {claim_1.statement}
  - {claim_2.statement}
  - {claim_3.statement}
headline_metric: {analysis.headline_metric}   # str, e.g. "NDS" — REQUIRED
headline_value: {analysis.headline_value}     # float, e.g. 87.3      — REQUIRED
params_million: {analysis.params_million}      # float, e.g. 42.0      — REQUIRED
---

# {candidate.title}

## Overview
{analysis.overview}

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → insight |
| [claims.md](logic/claims.md) | {len(claims)} falsifiable claims |
| [concepts.md](logic/concepts.md) | {len(concepts)} concepts |
| [experiments.md](logic/experiments.md) | {len(experiments)} experiments |

### Physical Layer (`/src`)
| File | Description |
|------|-------------|
| [execution/core.py](src/execution/core.py) | Novel-contribution stub |
| [code_ref.md](src/code_ref.md) | Repo + pinned SHA + file:line map |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research DAG |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Index of tables + figures |

<!--
Exact numbers live ONLY under /evidence (each evidence table carries `name`,
`headers`, `rows`, `caption`, `source`, plus `claims` for the index README).
Numbers anywhere outside /evidence are a G2 fidelity risk — keep claims
qualitative in summaries, exact figures under /evidence.
-->

<!--
Note: write_branch2 also emits logic/related_work.md, logic/solution/{architecture,
algorithm,constraints,heuristics}.md, src/configs/{training,model}.md, and
src/environment.md — these are NOT linked from the PAPER.md Layer Index above
(the writer's _paper_md lists only the four rows shown per section).
-->


<!--
WHY the frontmatter contract is hard: landscapes.py::_has_headline_frontmatter requires
key + headline_metric + headline_value + params_million (the _HEADLINE_KEYS tuple); a
PAPER.md missing ANY of them is SILENTLY SKIPPED (via `continue` in _collect) from the
cross-paper table — the entry still lives in the vault, it just gets no metric row. The
headline_value/params_million also drive the efficiency column
(round(headline_value / params_million, 4); 0.0 when params_million <= 0).
-->
