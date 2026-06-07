# paper-rolling 文档地图

> 本页是导航索引（meta-doc），按文档四分类规范组织 `docs/`。新增文档时**先判定类目、放进对应目录、并在下表登记**；改动既有文档时同步刷新其文件头的"更新日期"。代码总览见仓库根 `README.md`；引擎契约见 `.claude/skills/paper-landscape/SKILL.md`。

---

## 目录结构

| 目录 | 类目 | 收什么 | 文件头规范 |
|------|------|--------|-----------|
| `guides/` | 操作指南 | 常青 how-to / 工作流 / 路线图——"怎么做、往哪走" | H1 + `创建日期 / 更新日期 / 适用环境` |
| `spec/` | 设计文档 | 带生命周期的设计方案、实施计划（`YYYY-MM-DD-<topic>.md`） | H1 + `日期 / 状态 / 作者 / 基准版本 / 目的` |
| `spec/archive/` | 设计文档（归档） | 已过时或已落地完成的设计——从 `spec/` 移入，文件名不变 | 同上（状态改为"已归档"） |
| `reports/` | 报告 | 时间点产物：审计报告、排查报告、对仓库的观察结论（正文中文） | H1 + `日期 / 作者 / 基准版本 / 影响范围` |
| `reference/` | 参考文档 | 参考来源 provenance（克隆的上游仓库，本地忽略）+ 清单 `index.md` | H1 + `范围` |
| `adr/` | 架构决策记录 | 不可变的架构决策（编号 `NNNN-<slug>.md`），记录"为什么这样设计" | H1 + `Status: <状态> — <日期>` |

> 类目语义、文件名规则、文件头字段的完整定义见全局规范 `~/.claude/rules/common/docs-metadata-standard.md`。

## 现有文档

### guides/ — 操作指南
- [`guides/EXTENDING.md`](guides/EXTENDING.md) — 如何在 paper 垂域内扩展引擎（新增 source / tier / gate / branch / 跨论文步骤）。
- [`guides/ROADMAP.md`](guides/ROADMAP.md) — 能力 / 可信度路线图（planned·in-progress·done 状态，持续更新）。

### CODEMAPS/ — 代码地图（系统架构概览）
- [`CODEMAPS/INDEX.md`](CODEMAPS/INDEX.md) — 代码地图总索引（2026-06-08 LLM 管线集成）。
- [`CODEMAPS/llm-pipeline.md`](CODEMAPS/llm-pipeline.md) — 新增可插拔 LLM 提供商层 + 人链 LLM 写入器。
- [`CODEMAPS/engine-core.md`](CODEMAPS/engine-core.md) — 核心管道：发现 → 摄入 → 双链 → 两道门 → 景观。
- [`CODEMAPS/audit-gates.md`](CODEMAPS/audit-gates.md) — G2 数据保真 + G3 6 维严谨性密封。
- [`CODEMAPS/discovery-sources.md`](CODEMAPS/discovery-sources.md) — 多源排序 (ADR-0001)、LLM 查询扩展。
- [`CODEMAPS/output-branches.md`](CODEMAPS/output-branches.md) — 双链原子产出、LLM 人链、图形策展。

### adr/ — 架构决策记录
- [`adr/0001-multi-signal-authority-no-citation-gate.md`](adr/0001-multi-signal-authority-no-citation-gate.md) — 多信号 OR 权威排序、不设引用硬门禁。
- [`adr/0002-extend-on-rule-of-three.md`](adr/0002-extend-on-rule-of-three.md) — rule-of-three 扩展策略；抽象发现源 seam、推迟 tier/branch 框架。
- [`adr/0003-skill-knowledge-layer-and-shipped-adapters.md`](adr/0003-skill-knowledge-layer-and-shipped-adapters.md) — 技能逻辑分层为知识层（`references/` + `sub-skills/`）+ 出厂确定性 infra 适配器；LLM seam 仍由 agent 注入（含 W1 终判）。
- [`adr/0004-llm-seam-transport-claude-p-default.md`](adr/0004-llm-seam-transport-claude-p-default.md) — LLM seam = 同步注入 callable；默认传输为锁死的 `claude -p`（订阅鉴权），另留直连 API 适配器；纯会话内 Agent-tool 仅用于交互式 survey，不进强制管线（修订 ADR-0003 决策 #3）。

### reference/ — 参考来源 provenance
- [`reference/index.md`](reference/index.md) — 上游仓库清单：3 个 provenance 研究仓库（被借鉴/vendored 的来源）+ 6 个 ≥20k★ 领域基准仓库（自动化读论文/科研，如 MinerU/docling/marker/markitdown/storm/gpt-researcher）。克隆体本地忽略，仅 `index.md` 入库。

### spec/ — 设计文档
- *（暂空）* 新的实施计划 / 设计方案放这里；过时后移入 `spec/archive/`。

### reports/ — 报告
- *（暂空）* 审计 / 排查 / 观察类报告放这里。
