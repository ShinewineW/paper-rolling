# HANDOFF — paper-rolling 跨机器交接

> **日期**: 2026-06-08
> **基准版本**: `paper-rolling@13b045a`(main,线性)
> **状态**: ⚠️ **不可用 / 任务未完成**——引擎已大幅修复(约 11 个 bug 全部提交、406 测试过),
> 但批量重跑卡在 **G3 锚点封印门**。现场已完整保留,供本机器的 AI 接手。
> **给接手 AI**: 先读完本文件,再读 `docs/handoff/debug-drivers/loop_progress.md`(逐时诊断)。

---

## 0. 一句话现状

第 1 篇论文(Cosmos-Transfer1 / 2503.14492)是**唯一通过、且已人工审过**的干净产物。
其余 4 篇 Cosmos + 5 篇 world-action-model 的批量重跑,在引擎所有基础设施 bug 都修好后,
最终**全部死在 G3 锚点门**(`audit_block`)。这是一个明确的、已诊断清楚的设计问题——
修掉它(见 §3),再重跑即可。**这是接手后的第一要务。**

## 1. 这次会话做了什么(背景脉络)

这是一个自主论文知识引擎(skill 在 `.claude/skills/paper-landscape/`)。本次会话:

1. **搭好了可插拔 LLM provider 层**(`scripts/llm/`):claude `-p` 默认 + 任意 OpenAI 兼容 API
   (当前用 opencode/deepseek 跑审计与人链写手)。带每-seam 路由、保底回落 claude-code、
   `EngineAbort` 失败即停。**厂商中立**(不绑死 opencode)。
2. **重做了"人链"**(给人读的中文深度报告):`scripts/output/branch1_llm.py` —— LLM 写手产
   生动中文 + 锚定核心结论 + 证据表 + **选择性嵌入论文原图**(强制架构图 + 精选效果图)+
   MathJax 数学 + 白底自包含 HTML + **禁 emoji 铁律**。已接进引擎(`write_report` seam,默认开)。
3. **试跑第 1 篇并审计**:dynamic workflow 抓出一个真 blocker(analyzer 伪造训练损失公式),
   已根因修复 + 复审通过。人链报告用户已确认过关。
4. **任务 3 批量重跑**:抓出并修复一连串 bug(见 §6),但最终卡 G3。

## 2. Git 状态 / 已提交什么

`main` 线性,本次会话的提交(`git log --oneline -20`,从 `74e2fe0` 之后全是本次):
- provider 层 / 人链 / figures / 数学 / analyzer 修复 …(约 11 个 commit)。
- `29331da` = **第 1 篇干净产物**(ai_package + person_vault + corpus MD)。
- 现已**原样提交完整调试现场**:`_failed/`(失败诊断报告)、`_ledger/processed_ledger.yaml`
  (含今晚的失败行,**溯源用,不要清**)、`2503.15558` 的 G3 失败 vault 条目、4 篇未成功
  论文的 corpus MD、空的 landscape。

**注意**:`attn_sink/` 是 gitignored 的草稿区,不会随 git 传输——所以调试驱动脚本 +
逐时进度日志已复制到 **`docs/handoff/debug-drivers/`**(git 跟踪)。

## 3. ⭐ 核心待办:修 G3 锚点门(任务 3 的唯一阻塞)

### 诊断(已确认)
**branch1 和 G3 用了两套不一致的锚点检查**,于是同一份报告 branch1 放行、G3 拒绝:
- branch1 写报告时用 `scripts/output/anchor_lint.py::lint_text`(**会跳过 markdown 表格行**、
  经验句判定较宽松)→ **放行**。
- G3 复检时用 `scripts/audit/anchor_resolution.py::check_branch1_md_anchors`(**会标记表格行**、
  更严)→ **拒绝**。

失败实例(逐条 critical)见:
`_failed/2026-06-07_CosmosWorldFoundationModelPlatformForPhysicalAI_2501.03575.md`
失败分两类:(a) 证据**表格行**被误判为"未锚定经验句"(`| VideoLDM | 0.841 | …`);
(b) deepseek 写手把**精确数字写进了正文句子**("Sampson 误差(0.355)""PSNR(21.14)")——
这些数字**在论文 MD 里真实存在、可溯源**,但两套检查都没给它们打锚点。
叠加 `config/audit.yaml` 的 `max_gate_rounds: 1`(无重发)→ 第一次失败即硬阻断。

### 决策(用户已拍板):**锚定、不禁止 + 统一两套检查**
引擎哲学是"每个数字都能溯源到原文 MD"。"禁止正文出现数字"是个会在致密论文上崩的简化。
正确做法是让正文里**凡在 MD 中真实存在的数字都自动打锚点**,使其可溯源即可通过门——
不是降低标准。具体修复(待执行):

1. **让 `anchor_resolution.check_branch1_md_anchors` 跳过 markdown 表格行**,与
   `anchor_lint.lint_text` 一致(清晰的 bug 修复,先做这个)。
2. **统一 branch1 与 G3 的"经验句判定"逻辑**——抽出同一个函数共用,避免"一边放行一边拒绝"。
   (`anchor_lint._is_empirical_assertion` vs `anchor_resolution` 内部的判定。)
3. **强化数字接地**:`scripts/output/branch1_llm.py::_ground_report` / `_ground_line` /
   `branch1_report._find_in_md` —— 让正文里任何"MD 中真实出现"的数字自动加 `<!--anchor:…-->`。
   可能要让 `_find_in_md` 对数字格式(`0.355`、`32.16`、百分比等)的匹配更鲁棒。
4. (可选)`config/audit.yaml`: `max_gate_rounds: 2` 给一次重发机会。

### 验证
修完重跑 task3,确认 `2501.03575` 等能过 G3 并 promote 到
`ai_package/2026-06-08_*` + `person_vault/2026-06-08_*`(注意日期会变成处理当天)。

## 4. 怎么重跑任务 3

调试驱动在 `docs/handoff/debug-drivers/task3_run.py`(原件在 gitignored 的
`attn_sink/cosmos_trial/`)。把它放回 `attn_sink/cosmos_trial/` 或任意位置后:

```bash
PYTHONPATH=.claude/skills/paper-landscape uv run python <path>/task3_run.py
```
- **Tick A**:4 篇 Cosmos(`2501.03575/2503.15558/2511.00062/2606.02800`),**直喂、无发现网络**。
- **Tick B**:5 篇 world-action-model,真发现(8 分钟硬超时,防止挂起)。
- **顺序处理**(`max_concurrent=1`)——4 篇并发 × 5 chunk ≈ 20 个 `claude -p` 会触发限流卡死。
- 已接 `write_report` seam(人链 LLM 写手)。

正规流水线入口见 `.claude/skills/paper-landscape/SKILL.md`(用 `build_seams()` + `run_campaign`)。

## 5. 环境 / 已知坑(接手前必看)

- **`claude -p` API 限流**:今晚重度使用(4 次重跑 × 多 chunk + 2 个审计 workflow + 多次
  reprocess)把额度打满,analyzer 变得很慢(进程 5min/9s CPU = ~95% 阻塞)。**换不限流时段重跑。**
- **`.env`(gitignored)里有 `OPENCODE_API_KEY`** —— 另一台机器需要它才能跑 deepseek seam
  (写手 + 审计)。**不在 git 里,要手动带过去。** arXiv 论文是公开的,送 opencode 无敏感泄露。
- **MinerU 会重新摄取**(即使 corpus 已有 MD)——慢但能用;需要 MinerU 已装 + 网络。
- **git-lfs 未安装**:提交多篇前先 `brew install git-lfs && git lfs install` +
  `git lfs track "person_vault/**/*.jpg" "person_vault/**/report.html"`(report.html 内嵌
  base64 图,约 1.3–2.5M/篇,会撑大历史)。
- **环境前置门**:SKILL.md 有一个 REQUIRED 环境 preflight gate,跑前先过。

## 6. 今晚修复的 bug 清单(全在 main,406 测试过)

| # | bug | 提交 |
|---|---|---|
| 1 | analyzer 伪造训练损失公式(论文没有的公式) | 859a9cf |
| 2 | JSON 转义 repair 把合法 `\\` 过度转义 → 崩溃 | 859a9cf |
| 3 | grounded `claude -p` 在 JSON 前加旁白 → 解析失败 | 42a302f |
| 4 | JSON 串内未转义 ASCII 引号 → 解析失败(改用「」) | c51ff65 |
| 5 | 发现层 429/503 重试死循环 → 挂起 32min | (task3_run 直喂+超时) |
| 6 | 4 篇并发 × 5 chunk ≈ 20 个 claude -p → 限流卡死 | (task3_run max_concurrent=1) |
| 7 | O#/G# vs C# ID 命名空间冲突 | c5c5d2e |
| 8 | code_ref 误匹配 `.git/index` 二进制 | c5c5d2e |
| 9 | write_branch2 对无 github/arxiv 的论文 KeyError | 819cf1e |
| 10 | analyzer 过度具体化(论文没点名却写 GPT-4o 等) | c5c5d2e |
| 11 | figures: 连续图把下一张图引用当成 caption | a6d00de |
| — | **G3 锚点门**(见 §3) | **未修,待办** |

## 7. 关键文件地图

- **引擎核心**:`scripts/run_campaign.py`、`hub.py`、`spoke.py`、`output/produce.py`
- **provider 层**:`scripts/llm/{providers,config,seams,analyzer,writer,jsonparse}.py`
  (`EngineAbort` 在 `scripts/paths.py`)
- **人链(branch1)**:`scripts/output/branch1_llm.py` + `figures.py`
- **AI 包(branch2/ARA)**:`scripts/output/branch2_ara.py` + `ara_schema.py`(Seal-1)
- **门**:`scripts/audit/{g2_data_fidelity,g3_seal,anchor_resolution,rigor_rubric}.py`
  + `scripts/output/anchor_lint.py` ← **§3 要改的就是后两个的一致性**
- **配置**:`config/{campaign,llm,audit}.yaml`
- **调试驱动 + 逐时日志**:`docs/handoff/debug-drivers/`
- **文档/架构图**:`docs/CODEMAPS/`(本次新增)、`SKILL.md`

## 8. 第 1 篇(唯一干净产物,可参考其质量基线)

- 人链:`person_vault/2026-06-07_CosmosTransfer1_2503.14492/report.html`
  (白底 / 原图 / 数学,用户已审过)+ `report.md`
- AI 包:`ai_package/2026-06-07_CosmosTransfer1_2503.14492/ara/`(G2/G3 已封印)
- 它**是怎么过 G3 的**:这篇数字密度较低,写手没把大量数字塞进正文,所以锚点门通过了。
  这恰好印证了 §3 的诊断——致密论文才暴露问题。
