# Problem Specification

## Observations

### O1: world model 一词覆盖了强化学习环境模拟器、带规划的智能体和可模拟社会
- **Statement**: world model 一词覆盖了强化学习环境模拟器、带规划的智能体和可模拟社会的语言模型，概念边界分散。
- **Evidence**: 引言指出该术语被用于 learned environment simulators、agents that integrate learned models with planning 和 large language models that simulate entire societies，并且没有清晰共识说明如何构建 true world model。
- **Implication**: 论文需要先把问题从泛化术语收束为可操作的构建路线。

### O2: 单独强大的生成器不足以成为 true world model。
- **Statement**: 单独强大的生成器不足以成为 true world model。
- **Evidence**: 论文明确说 Unified Model 可能有 powerful generative heart，但通常缺少 dedicated interactive loop 和 explicit memory system。
- **Implication**: 评估世界模型不能只看生成能力，还要看是否能在行动、感知和历史状态之间闭环。

### O3: 长程一致性是从交互生成走向持久世界的关键瓶颈。
- **Statement**: 长程一致性是从交互生成走向持久世界的关键瓶颈。
- **Evidence**: 挑战部分指出 implicit frame-by-frame generators 灵活但容易 losing context 和 hallucinating objects，reactive action-perception loop 没有 dedicated memory and state management 时不能 sustain persistent worlds。
- **Implication**: 记忆不只是扩展上下文，而是构建持久世界状态的必要机制。

## Gaps

### G1: 领域缺少一条清晰的 true world model 构建路径。
- **Statement**: 领域缺少一条清晰的 true world model 构建路径。
- **Caused by**: world model 概念被多个研究传统共同使用，目标函数和系统边界并不统一。
- **Existing attempts**: ['论文把路线收窄为从 masking 到 unified generation，再到 interaction 与 memory 的演化链条。']
- **Why they fail**: 已有工作多优化狭窄任务，偏离生成、交互和持久性这组核心要求。

### G2: 静态生成模型难以承担可进入、可行动的世界。
- **Statement**: 静态生成模型难以承担可进入、可行动的世界。
- **Caused by**: 模型输出没有持续接收行动并更新状态的控制接口。
- **Existing attempts**: ['Interactive Generative Models 将输出条件化到 streamed inputs 或 user actions，并由 internal state 支持。']
- **Why they fail**: 一次性生成或被动视频缺少实时 action-perception 闭环。

### G3: 交互系统仍难保持长期一致。
- **Statement**: 交互系统仍难保持长期一致。
- **Caused by**: 记忆写入、检索、更新和遗忘缺少明确策略。
- **Existing attempts**: ['FramePack、Context-as-Memory、Mixture of Contexts、World-Mem 和 VMem 等方法分别从上下文压缩、检索和显式空间记忆缓解漂移。']
- **Why they fail**: 隐式视频模型会遗忘早期内容并累积误差，显式空间模型又难处理动态变化。

## Key Insight
- **Insight**: true world model 不是新增单个模块，而是把 generative heart、interactive loop 和 memory system 综合为能产生 persistence、agency 与 emergence 的自治整体。
- **Derived from**: 论文从 Stage I 到 Stage IV 的演化归纳，以及 Stage V 对 True World Models 的定义。
- **Enables**: 把研究问题从单项 benchmark 转为系统级构建：生成世界状态、响应行动、保留历史，并让宏观动态从长期交互中涌现。

## Assumptions
- mask-reconstruct-generalize 可作为跨模态生成与表征学习的共同起点。
- 统一架构是 true world model 的前置条件，但不是充分条件。
- 持久世界需要显式或结构化的记忆与状态管理，而不仅是更长上下文。
- persistence、agency 与 emergence 是区分 true world model 和普通模拟器的关键属性。
