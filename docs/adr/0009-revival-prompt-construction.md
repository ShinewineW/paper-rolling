# 0009 — Revival prompt construction: branch-level re-gen with whole-report feedback

> **Status**: accepted
> **修订**: 2026-06-09 — 多 agent 审计推翻了初稿的 "section 级外科手术"。`Finding.target`
> 从不携带 writer 章节标识(给的是文件路径 / ARA 节点 id / `level2_report.json`),
> 且 `write_branch1_llm` 用 `sorted(sections)` 全量拼装、无章节 merge-back 机制 —— "只重跑
> 受影响节" 需新建一整套定位层 + merge-back + 全链路透传,对尚不成熟的引擎是过早优化。
> 改为 **branch 级**。

一次 re-emit / 复活赛重放 **复用已通过的上游阶段产物,整段重跑失败的那一条链(branch)**,
把 verdict 评语作为**整篇反馈块**注入,而非定位到某一节。

## 失败归属分派(按 `Finding.target` 的文件级归属,不是章节级)

`run_g3` 的 hard_findings 的 target 是**文件/节点级**(g3_seal.py / anchor_resolution.py /
entailment.py 实测):

| finding 根在 | target 形态 | 重跑哪条链 |
|---|---|---|
| branch1(人类报告) | `report.md`(锚点解析) | 重跑 **branch1**(整篇,带反馈)— 复用 branch2 SSOT |
| branch2(ARA 包) | `claims.md:<id>`(entailment)/ `level2_report.json`(rigor) | 重跑 **branch2**(重调 analyzer,带反馈)+ 下游 branch1 |
| ingest/MD | `<id>.md`(公式保真) | 不可自动修 → 现场,人工回 ingest |

一个 verdict 可能跨多类;取"最上游"的根重跑(有 branch2 根 → 从 branch2 起;否则只 branch1)。

## 反馈注入(整篇,非按节)

- **branch1 反馈**:把 hard_findings 的 `observation` 汇成一个整体 `prior_failure` 块,
  注入 `write_human_sections` 的每节 prompt 前言(writer.py `_section_prompt`)。整篇重写,
  writer 本就并发写全部 ~11 节,重跑一遍是一次 writer pass。
- **branch2 反馈**(rigor/entailment 根):把 observation 注入 analyzer 的 `_chunk_prompt`,
  重调 `resolve_analysis`(fresh sub-agent,新采样)。
- **G2(数字门)永不吃反馈**(ADR-0006):盲重试 = 重调 `resolve_analysis`(新采样,**不是**只
  重跑确定性的 `write_branch2` 渲染)再核对,不泄露近似正确值。

## 护栏(不变)

- 门控对**整篇产物**独立重审,非只查旧条目。
- 只回传 `Finding.observation`,绝不回传私有 rigor 评分细则(ADR-0006)。
- 建设性反馈("锚定/定性化"),不许靠删内容过关。
- 有界:重放再失败仍留现场(ledger `deferred`),等下次引擎修复,不无人值守空转。

## 可选 per-batch 人工指令

批次复活驱动接受一句可选人工指令,注入每篇重放的 `prior_failure`,用于 reviewer 看出整批
共性时(比逐篇 finding 更准)。

## 注入点(接地,审计修正)

`prior_failure` 必须**全链路透传**(初稿只改了最底层 `write_human_sections`,中间两层断流):
`stage_branch1 → write_branch1_llm(branch1_llm.py:212)→ write_report seam(seams.py:333)
→ write_human_sections → _section_prompt`,每层加 `prior_failure: str | None = None`(默认 None
保持原行为)。analyzer 侧:`analyzer._chunk_prompt` 同加。`write_report` 是注入 seam,改签名
等于动 6-seam 装配契约(ADR-0012 后为 7,新增 faithfulness),以 keyword + 默认 None 保持向后兼容。

## 收敛模型与目的风险(spec-review / sim-review 修订)

**为什么不另加 writer 硬规则。** (本节为 ADR-0009 当时的论证;**ADR-0012 已推翻其前提** ——
当时 `writer._CONSTRAINTS` 第 3 条禁止散文写精确数字、要求"数值见表格",而这 7 篇最终门正是
带着那条形式规则被误杀的;ADR-0012 正是为此把门从"形式锚点"改为"忠实落源 (b)+判官 (c)",
正文从此允许有据数字。下文按当时语境保留。)当时:`writer._CONSTRAINTS` 第 3 条**已经**禁止
散文写精确数字、要求"数值见表格"。7 篇最终门正是带着这条规则失败的 —— deepseek 在密集论文上
系统性无视它。故"再加一条规则"无效。**反馈重试是更尖锐的执行**:基线规则是泛泛的"别写数字",
反馈是定点的"你在此处写了 PSNR(21.14),移走"(ADR-0012 后改为"该数字未落源→落源或删")
—— 给了实打实的第二次机会。

**收敛靠人在环,不靠无限自动重试(once-per-scene)。** 复活每篇**只试 1 次**;再失败 → 留现场
(ledger 仍 `deferred`)→ **人次日确认处理**(迭代 prompt / 必要时启用下方备选)。批次无 spend
cap(人工触发 + 人工复核的离线批处理,非无人值守 cron),但**累计花费打日志**给可见性。

**已知备选杠杆(暂不建):** 若反馈始终修不好密集论文,把 writer seam 对密集论文路由到
`claude`(更强、更守规则)。暂不建 —— 它会抢 `claude -p` 的 5 槽并发(与 rigor 同理的代价)。
留作人工在收敛停滞时手动启用的杠杆。
