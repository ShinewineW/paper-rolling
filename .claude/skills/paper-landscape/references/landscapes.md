# Cross-paper landscape generation

`scripts/landscapes.py` is the **corpus-batch-comparator**: a pure read-side
aggregator that, after each tick's batch, regenerates the topic landscape from
every paper's branch2 ARA frontmatter. It **never writes the ledger or vaults**
(module docstring) — the hub regenerates landscapes *after* the spoke batch
finishes, not per-paper.

## What it reads

For each entry under `{workspace}/ai_package/`, it reads
`{entry}/ara/PAPER.md` and parses YAML frontmatter (`_read_frontmatter` splits
on `---`, requires a leading `---`). The `_HEADLINE_KEYS` it needs:

```python
_HEADLINE_KEYS = ("key", "headline_metric", "headline_value", "params_million")
```

`load_paper_summary(workspace, entry_name)` coerces frontmatter into a frozen
`PaperSummary(key, title, year, headline_metric, headline_value, params_million)`.
`headline_metric`/`headline_value`/`params_million` are the same fields the
analyzer (`resolve_analysis`) MUST put in the ARA bundle — see
[ara-schema.md](./ara-schema.md) for the schema origin.

## Drop rule (no crash on missing metrics)

`_collect(workspace)` iterates `sorted(ai_root.iterdir())`; for each entry it
skips when `paper_md` is absent **or** `_has_headline_frontmatter(paper_md)` is
False. `_has_headline_frontmatter` returns `all(k in fm for k in _HEADLINE_KEYS)`.
A branch2 `PAPER.md` lacking headline metrics (no leaderboard number to
aggregate) is **dropped from the cross-paper table** rather than crashing the
aggregator — per the docstring, "the entry still lives in the vault; it just has
no metric row in the landscape." Returns `[]` if `ai_package/` does not exist.

## Outputs

`generate_landscapes(workspace, *, topic, generated_on=None) -> LandscapeResult`:

- `slug = slugify(topic)` — kebab-case, ascii + CJK safe
  (`re.sub(r"[^\w一-鿿]+", "-", ...)`, falls back to `"topic"`).
- Writes into `{workspace}/landscapes/{slug}/`:
  - `INDEX.md` (`_render_index`) — per-paper navigation, **newest-first**
    (`sorted(papers, key=lambda p: (-p.year, p.title))`); columns `# | 论文 | 年份 | 主指标`.
  - `report.md` (`_render_report`) — three sections:
    1. **统一指标对比表** — `论文 | 年份 | 主指标 | 数值 | 参数量(M) | 效率(指标/M)`.
    2. **效率分析** — `_efficiency(s) = round(headline_value / params_million, 4)`
       (`0.0` when `params_million <= 0`); names `max(ordered, key=_efficiency)`.
    3. **趋势** — chronological (`sorted(..., key=lambda p: p.year)`) first→last
       `headline_value` delta, formatted `{delta:+}`.
- `generated_on` defaults to `datetime.date.today().isoformat()` so a daily
  `/loop` tick stamps the current date; callers may inject a fixed value for
  deterministic output (Codex R17).

Returns `LandscapeResult(paper_count, index_path, report_path)`.

## Why it runs last, and why it never writes the ledger

In pipeline order (`discover → ingest → ledger → branch2 → G2 → branch1 → G3 →
landscapes`), the landscape is the final read pass over the whole corpus, so it
only sees entries already promoted to `ai_package/`. The promotion is atomic
(`scripts/output/produce.py` `produce_outputs`): branch2 is staged, gated by G2,
then both branches are `shutil.move`d into `person_vault/{key}` and
`ai_package/{key}` together (OT-5: both or neither). The aggregator scans those
promoted vault dirs — `produce.py` notes "landscapes scan vault dirs, not
code-ref notes" — so a paper a stalled spoke abandoned mid-commit is pruned by
`store.consistency_check` before it can pollute a metric row.

`PaperSummary` is `frozen=True`; `landscapes.py` imports only `datetime`, `re`,
`dataclass`, `Path`, and `yaml` — no ledger, vault, or LLM seam dependency,
keeping the comparator a side-effect-free read layer. It emits only markdown
tables (`INDEX.md` + `report.md`); it generates no Mermaid diagrams — the
cherry-picked Mermaid `classDef` palette lives in `scripts/output/branch1_report.py`
(branch1 model-structure re-draws), not here.

---
See also: [ara-schema.md](./ara-schema.md) (headline frontmatter origin),
[../scripts/output/produce.py](../scripts/output/produce.py) (atomic promotion that
populates `ai_package/`).
