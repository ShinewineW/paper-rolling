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

### adr/ — 架构决策记录
- [`adr/0001-multi-signal-authority-no-citation-gate.md`](adr/0001-multi-signal-authority-no-citation-gate.md) — 多信号 OR 权威排序、不设引用硬门禁。
- [`adr/0002-extend-on-rule-of-three.md`](adr/0002-extend-on-rule-of-three.md) — rule-of-three 扩展策略；抽象发现源 seam、推迟 tier/branch 框架。

### reference/ — 参考来源 provenance
- [`reference/index.md`](reference/index.md) — 三个上游研究仓库的清单（URL / license / 各自被借鉴了什么）。克隆体本地忽略，仅 `index.md` 入库。

### spec/ — 设计文档
- *（暂空）* 新的实施计划 / 设计方案放这里；过时后移入 `spec/archive/`。

### reports/ — 报告
- *（暂空）* 审计 / 排查 / 观察类报告放这里。
