# 人链报告写作规范（distilled from the reference repos）

> **范围**: `scripts/llm/writer.py` 的写手 seam — 给人读的中文精读报告(`person_vault/{key}/report.md`)的写作规范。蒸馏自 `docs/reference/` 三个上游仓库,并与本引擎的接地系统(锚点 + 证据表)对齐。

本文档有两部分:**(A) 注入块** —— `writer.py` 读取下方 (A) 小节里 `INJECT` 起止标记之间的内容,原样拼进每个写手 prompt;**(B) 来源与完整最佳实践** —— 供维护者参考。要调写手风格,直接编辑 (A)。

## 致谢与来源(provenance)

蒸馏自 `docs/reference/` 下三个仓库,均按其许可署名:

- **scientific-agent-skills**(K-Dense Inc.,MIT;内含 vendored `markdown-mermaid-writing`,Apache-2.0 / Clayton Young, Superior Byte Works)——`markdown_style_guide.md`(结论前置、可扫读、引用纪律)、`mermaid_style_guide.md`(主题安全 classDef 调色板、复杂度分级)、`peer-review/common_issues.md`(22 类方法/统计/解读缺陷清单)、`clinical-reports/data_presentation.md`(表格/数字诚实)、`scientific-visualization/publication_guidelines.md`(图表规范)、`templates/research_paper.md`("show your work")。
- **AI-Research-SKILLs**(Orchestra-Research,MIT)——`ml-paper-writing` / `academic-plotting`(Illustrated Technical style、图生成)、`22-agent-native-research-artifact`(ARA)、`dev_data/deep_research_report_1.md`(成稿范例)。
- **academic-research-skills**(Cheng-I Wu,CC-BY-NC 4.0)——deep-research agents(`synthesis` / `report_compiler` / `editor_in_chief`)、`argumentation_reasoning_framework`、`apa7_style_guide`、`benchmark_report_pattern.md`。

---

## (A) 注入块 — 写手必须遵守(已与本引擎接地系统对齐)

<!-- INJECT:START -->
### 写作规范(精读报告 / 必须遵守)

**结构:结论前置。** 每个小节先抛**结论**,再展开方法/推导/数据来佐证;读者读完该节不应残留"那……到底怎样?"。小节以 `## 标题` 开头(整篇唯一 H1 由系统添加),标题具体("自适应多模态控制"而非"方法细节"),一个标题只讲一件事;H2 句首可带一个 emoji,H3/H4 不带。

**忠实与严谨(写"实验/对比"与"局限"时逐条过审)。** 明确区分论文"声称"与"证明"了什么;主动点名失效模式:相关性当因果、过度宣称("首个""超出数据外推")、挑樱桃式"代表性"结果、忽略替代解释、方法与结果不一致;并说明论文是否报告了消融/负结果/误差范围。诚实但不贬低。

**接地(关键,与本引擎对齐):不要在叙述句子里写精确性能数字**(如"达到 8.54""比基线高 0.71""提升 12%")。性能对比一律用定性语言("在整体质量上领先所有单模态配置"),需要时附"(具体数值见'实验与对比'的表格)"。精确数值只活在两处:系统自动内联的**证据表**、以及系统自动锚定的**核心结论**块——你无需手写脚注或编号引用(本引擎用隐形锚点接地,不用 `[^N]`)。非性能数字(层数、GPU 数、720p、5 秒、4k)可正常写。专有名词(模型/指标/数据集/硬件名)与公式 `$$...$$` 一律保留原样,不翻译。

**图表叙事(而非装饰)。** 凡涉及流程/结构/关系/时序/比较就配图,且选**最具体**的类型(流程决策→flowchart,交互→sequence,生命周期→state,历程→timeline,数值趋势→xychart,多维方法对比→radar);"若你正用一段文字描述一个可视概念,停下来画图"。图就近内嵌,不单设"配图"章节。图要带"为什么":flowchart 画出关键判定门与通过/失败分支,timeline 分段标"时代+驱动压力"而非裸年份,对比图/表暴露论文做出的权衡;复杂图后补一句"如何读这张图"。
- Mermaid 主题安全:禁用 `%%{init}` 与行内 `style`,只用 `classDef`+`class`;每图 ≤4 个语义色且每色含文字 `color:`,绝不只靠颜色传义;snake_case 节点 id,标签 3–6 词主动语态,边标签 1–4 词,形状一致(菱形=判定,圆柱=数据,圆角=起止)。
- 复杂度分级:≤10 节点平铺;10–30 节点用 2–6 个按真实阶段命名的 `subgraph`;主方向单一(层级/流程 TB,流水线 LR)。

**表格 vs 叙述。** 结构化对比(方法/基线、相关工作映射、关键超参)用表:有表头、单位写进列头、≤5 列、每格 1–5 词、数字列右对齐;叙述性推理不塞进表,也不要把对比塞进长段落。(注:论文的原始性能数值表由系统自动附在"实验与对比"末尾,你不必重画。)

**深度藏进折叠块(信息要慷慨,别删内容)。** 冗长的推导细节、复现的精确配置/命令、边界 caveat 可用 `<details><summary><strong>标签</strong></summary>` 折叠,主线保持可略读,认真的读者可展开;`<details>` 内同样不得出现裸性能数字(遵守上面的接地规则)。
<!-- INJECT:END -->

---

## (B) 完整最佳实践(参考,未全部注入)

以下来自上游仓库,部分与本引擎机制不冲突但偏外部场景(如学术论文写作、临床报告),作为维护者扩展写手时的参考:

- **引用纪律(原始版,本引擎已用锚点替代)**:上游要求"每个外部统计/benchmark/他人观点配脚注 `[^N]` + 可解析 URL/DOI,统一汇总到末尾"。本引擎改用隐形三层锚点(数字回链源 MD)+ 指向配对 `ai_package/` 证据,故注入块不要求写手手写脚注。
- **数字诚实(来自 clinical-reports/data_presentation)**:百分比给分子/分母(78/150, 52%);误差棒注明含义(SD/SEM/95% CI);p 值给 2–3 位精确值(别写 p=0.000→p<0.001);同表小数位一致;优先效应量+置信区间。——本引擎的精确数值在证据表里,此规则供"核心结论/对比解读"措辞参考。
- **同行评审失效清单(peer-review/common_issues.md,22 类)**:p 值滥用、过度宣称、挑樱桃、忽略替代解释、方法-结果不一致等——是"局限/对比"节做忠实复核的完整 checklist。
- **图表发表规范(scientific-visualization)**:色盲安全调色板(viridis / Okabe-Ito,避免红绿),灰度可辨(靠线型/marker),避免 chart junk / 截断坐标轴 / 3D。
- **成稿范例**:`AI-Research-SKILLs/dev_data/deep_research_report_1.md`(分层结构、决策指南、版本追踪);`scientific-agent-skills/.../assets/examples/example-research-report.md`(核心发现前置 + 内嵌流程图 + 结果表 + `<details>` 技术深度 + radar 对比 + 脚注)。
