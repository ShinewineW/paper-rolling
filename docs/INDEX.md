# paper-rolling 文档地图

> 本页是导航索引兼**治理总纲**(meta-doc)。`docs/` 下的一切目录、归属与习惯都在此统筹。
> 代码总览见仓库根 `README.md`;引擎契约见 `.claude/skills/paper-landscape/SKILL.md`。
> 类目语义、文件名规则、文件头字段的完整定义见全局规范 `~/.claude/rules/common/docs-metadata-standard.md`。

---

## 治理规则(改动 `docs/` 前必读)

1. **先注册,再建目录** —— 不允许"遇到什么事就随手建文件夹"。任何**新增目录**都必须**先**在下方《目录结构》表登记(类目 / 收什么 / 文件头规范),再落盘。
2. **不建 `plan/` 目录** —— 所有计划类文档,无论 design 还是 impl,一律写入 `spec/`;过时后移入 `spec/archive/`。
3. **`adr/` 自管理豁免** —— `adr/` 由 `mp-grill-me` 技能维护(产品定义与关键命名),自我管理,豁免四分类与文件头约束;此处仅登记其存在与归属。
4. **`reference/` 不入库** —— 参考来源(GitHub 仓库、博客等克隆体)本地保留、**不被 git 追踪**,仅其 `INDEX.md` 清单入库(`.gitignore` 第 44–45 行)。
5. **改动既有文档**时同步刷新其文件头的"更新日期"。

---

## 目录结构

| 目录 | 类目 | 收什么 | 文件头规范 |
|------|------|--------|-----------|
| `guides/` | 操作指南 | 常青 how-to / 工作流 / 路线图——"怎么做、往哪走" | H1 + `创建日期 / 更新日期 / 适用环境` |
| `guides/codemaps/` | 代码地图(代码感知) | 本仓库架构概览:绑定代码模块的常青地图(子系统拓扑、数据流、关键决策),供快速建立代码感知 | H1 + `范围`(子索引见 `guides/codemaps/INDEX.md`) |
| `spec/` | 设计文档 | 带生命周期的设计方案与实施计划(design + impl,`YYYY-MM-DD-<topic>.md`) | H1 + `日期 / 状态 / 作者 / 基准版本 / 目的` |
| `spec/archive/` | 设计文档(归档) | 已过时或已落地的设计——从 `spec/` 移入,文件名不变 | 同上(状态改为"已归档") |
| `reports/` | 报告 | 时间点产物:对本代码仓库的观测、审计、排查结论(正文中文) | H1 + `日期 / 作者 / 基准版本 / 影响范围` |
| `reference/` | 参考来源 | 所有参考的 GitHub 仓库 / 博客等克隆体(本地、不入库);仅 `INDEX.md` 清单入库 | H1 + `范围` |
| `adr/` | 架构决策记录 | 不可变架构决策(编号 `NNNN-<slug>.md`)——**由 `mp-grill-me` 自管理,豁免** | H1 + `Status: <状态> — <日期>` |
| `handoff/` | 上下文接手 | 临时切换上下文时的接手 / 进度交接文档(工作态草稿区,随任务来去) | 自由(工作态,不强制规范) |

---

## 现有文档

### guides/ — 操作指南
- [`guides/EXTENDING.md`](guides/EXTENDING.md) — 如何在 paper 垂域内扩展引擎(新增 source / tier / gate / branch / 跨论文步骤)。
- [`guides/ROADMAP.md`](guides/ROADMAP.md) — 能力 / 可信度路线图(planned·in-progress·done 状态,持续更新)。
- [`guides/mineru-setup.md`](guides/mineru-setup.md) — Tier-2 mineru 环境修复(socksio + ModelScope 直连下模型);"装了≠能跑"的排查与 preflight deep-smoke 验证。

### guides/codemaps/ — 代码地图(系统架构 / 代码感知)
- [`guides/codemaps/INDEX.md`](guides/codemaps/INDEX.md) — 代码地图总索引(2026-06-08 LLM 管线集成)。
- [`guides/codemaps/llm-pipeline.md`](guides/codemaps/llm-pipeline.md) — 可插拔 LLM 提供商层 + 人链 LLM 写入器。
- [`guides/codemaps/engine-core.md`](guides/codemaps/engine-core.md) — 核心管道:发现 → 摄入 → 双链 → 两道门 → 景观。
- [`guides/codemaps/audit-gates.md`](guides/codemaps/audit-gates.md) — G2 数据保真 + G3 6 维严谨性密封。
- [`guides/codemaps/discovery-sources.md`](guides/codemaps/discovery-sources.md) — 多源排序 (ADR-0001)、LLM 查询扩展。
- [`guides/codemaps/output-branches.md`](guides/codemaps/output-branches.md) — 双链原子产出、LLM 人链、图形策展。

### spec/ — 设计文档
- [`spec/2026-06-09-code-ref-repo-resolution-impl.md`](spec/2026-06-09-code-ref-repo-resolution-impl.md) — code_ref 官方仓定位级联(T1 grep+T2a PwC离线+T2b HF-live+T4 websearch)+ clone 验证闸门 + 三态语义实施计划(P0)。
- [`spec/2026-06-11-paper-list-input-mode-impl.md`](spec/2026-06-11-paper-list-input-mode-impl.md) — 指定列表输入模式(关闭自发查找、只跑操作者给的论文集),与自发查找二元切换实施计划(依据 ADR-0010)。
- [`spec/2026-06-12-ara-delete-safety-impl.md`](spec/2026-06-12-ara-delete-safety-impl.md) — ARA 删除安全:失败/abort 一律移入 `_failed/`、绝不反射式 rm token-expensive 的 ARA,空壳/person/可再生临时物照删(依据 ADR-0011;已落地)。

### spec/archive/ — 设计文档(归档)
- [`spec/archive/2026-06-09-失败现场与复活赛-impl.md`](spec/archive/2026-06-09-失败现场与复活赛-impl.md) — 失败现场保全 + branch 级重试 + 批次复活赛实施计划(依据 ADR-0006~0009;已落地归档)。
- [`spec/archive/2026-06-07-人链重做-双链对等.md`](spec/archive/2026-06-07-人链重做-双链对等.md) — 人链重做:双链对等设计(已落地归档)。

### reports/ — 报告
- [`reports/2026-06-09-24篇批量跑根因诊断.md`](reports/2026-06-09-24篇批量跑根因诊断.md) — 24 篇批量跑失败原因诊断与修复记录。

### reference/ — 参考来源 provenance
- [`reference/INDEX.md`](reference/INDEX.md) — 上游仓库清单:3 个 provenance 研究仓库 + 6 个 ≥20k★ 领域基准仓库(MinerU/docling/marker/markitdown/storm/gpt-researcher)。克隆体本地忽略,仅 `INDEX.md` 入库。

### adr/ — 架构决策记录(mp-grill-me 自管理)
- [`adr/0001-multi-signal-authority-no-citation-gate.md`](adr/0001-multi-signal-authority-no-citation-gate.md) — 多信号 OR 权威排序、不设引用硬门禁。
- [`adr/0002-extend-on-rule-of-three.md`](adr/0002-extend-on-rule-of-three.md) — rule-of-three 扩展策略;抽象发现源 seam、推迟 tier/branch 框架。
- [`adr/0003-skill-knowledge-layer-and-shipped-adapters.md`](adr/0003-skill-knowledge-layer-and-shipped-adapters.md) — 技能逻辑分层为知识层 + 出厂确定性 infra 适配器;LLM seam 由 agent 注入。
- [`adr/0004-llm-seam-transport-claude-p-default.md`](adr/0004-llm-seam-transport-claude-p-default.md) — LLM seam = 同步注入 callable;默认传输锁死 `claude -p`,另留直连 API 适配器。
- [`adr/0005-public-cc-by-nc-keep-original-figures.md`](adr/0005-public-cc-by-nc-keep-original-figures.md) — 保持公开 + CC-BY-NC;原图原样嵌入(不改 Apache、不只重绘);版权立场与权衡。

### handoff/ — 上下文接手(工作态)
- [`handoff/debug-drivers/`](handoff/debug-drivers/) — 批量跑根因诊断期间的接手文档 + 复现驱动脚本(`loop_progress.md` 进度交接 + `run24.py` 等驱动,被 `reports/2026-06-09-…` 引用为复现配套)。
