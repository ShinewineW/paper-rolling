<!--
TEMPLATE — landscapes/{topic-slug}/  (written by scripts/output/../landscapes.py after each batch)
Two files. Both are built ONLY from each ai_package/*/ara/PAPER.md headline frontmatter
(key + headline_metric + headline_value + params_million). A paper missing that frontmatter is
dropped. Column order below matches _render_index / _render_report exactly. See ../references/landscapes.md.
-->

<!-- ========== landscapes/{topic-slug}/INDEX.md  (per-paper nav, newest-first) ========== -->
# {topic} — 论文索引

> 生成日期: {generated_on} | 共 {N} 篇论文
>
> [完整全景报告](report.md)

## 快速导航（按年份倒序）

| # | 论文 | 年份 | 主指标 |
|---|------|------|--------|
| 1 | {title} | {year} | {headline_metric}={headline_value} |


<!-- ========== landscapes/{topic-slug}/report.md  (unified comparison) ========== -->
# {topic} — 全景对比报告

> 共 {N} 篇论文 | 生成日期 {generated_on}

## 一、统一指标对比表

| 论文 | 年份 | 主指标 | 数值 | 参数量(M) | 效率(指标/M) |
|------|------|--------|------|-----------|--------------|
| {title} | {year} | {headline_metric} | {headline_value} | {params_million} | {efficiency} |

<!-- efficiency = round(headline_value / params_million, 4); 0 when params_million <= 0.
     Subsequent sections (efficiency ranking, trends) extend from the same PaperSummary set. -->
