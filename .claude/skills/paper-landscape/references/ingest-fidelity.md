# 2-tier MD-only ingest & fidelity gates

The ingest layer turns one discovered `candidate: dict` into a single trusted
Markdown file. Everything downstream (analysis, audit, both output branches,
landscapes) reads **only** `{ID}.md` — the MD-only contract. PDFs and source
HTML are converted once and then frozen; no later stage re-parses them.

Source: `scripts/ingest/ingest.py`, `scripts/ingest/tier1_html.py`,
`scripts/ingest/contract.py`.

## Entry point

```python
ingest(candidate, corpus_dir, *, http, run_cli, now=None) -> IngestResult
```

`http(url) -> (status, bytes)` and `run_cli(argv, cwd) -> result` are the two
injected infra adapters (see [wiring-the-seams.md](./wiring-the-seams.md)).
Tier chain: Tier-1 → Tier-2 → raise. Both fail → `raise IngestFailed`; the HUB
catches it and calls `quarantine(...)` to write `_failed/{ID}.json` (中枢-D2).
`IngestResult` fields: `md_path`, `contract`, `tier`, `images_dir`,
`content_list_path: Path | None`.

## Corpus ID (`_paper_id`)

Stable, no-LLM corpus dir name (OT-3):
- arXiv → `{arxiv_id}{arxiv_version}_{ShortName}`
- non-arXiv (DOI only) → `{identity_base(None, doi)}_{ShortName}` via
  `scripts.output.naming.identity_base` — never `None_...` (Codex R21)
- `ShortName` = `short_name(title)`, deterministic CamelCase, max 40 chars.

`short_name` is deliberately distinct from `naming.derive_name` (the vault key):
two separate stable ID spaces, do not consolidate. Naming authority overall →
[naming-and-ledger.md](./naming-and-ledger.md).

## Tier 1 — arXiv HTML → pandoc GFM

`run_tier1(arxiv_id, version, out_dir, *, http, run_cli, pandoc_version)`
(`PANDOC_VERSION = "3.1.2"`). Highest-fidelity path, **no PDF downloaded**:

1. Fetch `https://arxiv.org/html/{id}{version}` (arXiv's LaTeXML render).
2. Quality gate → `raise Tier1Unavailable` when `status != 200`/empty body
   (`html_missing`) or the `_LATEXML_ERROR` marker regex
   (`ltx_ERROR|LaTeXML error|Unable to process`) matches (`latexml_error`).
   `Tier1Unavailable` is a *soft* signal: demote to Tier-2.
3. Download relative `<img src>` figures (skips `http(s)://` / `data:` refs).
4. pandoc `--from html --to gfm` (MathML → LaTeX `$$`). Non-zero rc →
   `pandoc_failed`; missing output → `pandoc_no_output`.

`Tier1Output` carries `html_math_count` (count of `<math display="block">`,
the `_DISPLAY_MATH` regex) and `html_table_count` (count of `<table>`,
`_HTML_TABLE`). Inline math (`$...$`) is **excluded** — it never produces a
`$$` block, so counting it would falsely demote inline-only-math papers.

## Fidelity gates (摄取-D1 / ROADMAP A1+A2)

In `ingest()`, after a successful Tier-1 conversion, the emitted MD is compared
against the source counts before being accepted:

```python
EQUATION_SURVIVAL_RATIO = 0.5
TABLE_SURVIVAL_RATIO    = 0.5
```

- `src_eq > 0 and eq_blocks < src_eq * EQUATION_SURVIVAL_RATIO` → `equation_gate`
  reason → demote to Tier-2.
- `src_tbl > 0 and tbl_blocks < src_tbl * TABLE_SURVIVAL_RATIO` → `table_gate`
  reason → demote to Tier-2.

`eq_blocks = count_equation_blocks(md)` pairs `$$` fences (`_FENCE`, every 2
occurrences = 1 block; dangling unpaired `$$` does not count).
`tbl_blocks = count_table_blocks(md)` counts GFM header-separator rows
(`_TABLE_SEP`, `^\|[\s:|-]+\|$`). These catch **partial** loss (e.g. 50 source
equations, 5 survive; 8 tables, 1 survives), not only the all-or-nothing case.
The `src_* > 0` guard means a legitimately equation-free or table-free paper is
never demoted.

## Tier 2 — PDF → MinerU

When Tier-1 is unavailable or demoted: `run_tier2(pdf_url, paper_dir, *, http,
run_cli, mineru_version)` (`MINERU_VERSION = "2.0.0"`). PDF URL =
`candidate["oa_pdf_url"]` (Round 1 F7 canonical field), falling back to a
derived `https://arxiv.org/pdf/{aid}{ver}` when only an arXiv id is present
(Codex R21). No PDF URL at all → `IngestFailed`. `run_tier2` failure
(`Tier2Failed`) is wrapped into `IngestFailed` carrying both tier reasons.
MinerU images are copied into the canonical `paper_dir/images/`.

## Outputs per paper

`_finalize` writes `corpus/{ID}/{ID}.md` plus `images/` and serializes
`.md_contract.json` via `write_contract`. `MdContract` (frozen dataclass) fields:
`source_pdf_sha256` (`None` for Tier-1 — no PDF), `converter`
(`"pandoc"`|`"mineru"`), `converter_version`, `md_sha256`, `image_count`,
`equation_block_count`.

`content_list.json` — typed blocks for the G3 equation gate:
- Tier-2 (MinerU) **emits** it natively → `content_list_path` set.
- Tier-1 (pandoc) emits none → `content_list_path = None`; the **spoke**
  synthesizes one `{"type":"equation"}` entry per `$$` display block.

## Field context — why MinerU is the Tier-2 engine

Benchmark PDF→MD engines are cloned read-only under `../../../../docs/reference/`
for comparison; MinerU is the chosen Tier-2 because of its native
`content_list.json` (typed formula/table blocks that feed the G3 equation gate
directly). Each alternative tackles the same hard problem — **table fidelity**,
the lossy step pandoc HTML→GFM also suffers (hence `table_gate`):
- `docs/reference/docling` — TableFormer structure-recovery model.
- `docs/reference/marker` — TableConverter pipeline.
- `docs/reference/markitdown` — lightweight Office/HTML→MD (no deep table model).

See also: [wiring-the-seams.md](./wiring-the-seams.md) (the `http`/`run_cli`
adapters), [glossary.md](./glossary.md) (摄取-/中枢- discipline tags).
