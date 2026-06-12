# Heuristics

## H1: 优先沿着从 Mask-based Models 到 Unified Models、Interactive Generative Models、Memory and Consistency、True World Models 的窄路组织系统，而不是罗列所有相关 world model 分支。
- **Rationale**: 论文明确说 bypass loosely related branches，聚焦 generative heart、interactive loop 和 memory system，并把 Stage V 定义为前序阶段的 synthesis。
- **Sensitivity**: 如果研究目标只是特定任务优化或静态基准，这条路线会显得过窄；若目标是 true world models，论文认为该窄路更贴近核心。
- **Bounds**: 适用于论文定义的 true world model 路线图；不覆盖所有 reinforcement learning、agent planning 或社会模拟文献。
- **Code ref**: [无；综述论文未提供代码。]
- **Source**: Abstract；Section 1；Section 7

## H2: 构建统一模型时，排除不同模态拼接不同范式的 glue models，保留 shared backbone 与 same paradigm。
- **Rationale**: 论文将 unified model 定义为用 shared backbone 和 same paradigm 处理并生成不同模态，并明确排除 text 用 autoregression、image 用 diffusion 的简单拼接。
- **Sensitivity**: 边界对 industrial-scale systems 敏感，因为 Gemini 和 GPT-4o 被归为 single system 但 not in a single paradigm。
- **Bounds**: 只适用于 Stage II 的统一建模筛选；不能把所有多模态系统都视为论文意义上的 unified model。
- **Code ref**: [无；综述论文未提供代码。]
- **Source**: Section 4；Section 4.1

## H3: 交互生成系统必须把输出条件化在 streamed inputs 或 user actions 上，并维护 internal state。
- **Rationale**: 论文定义 Interactive Generative Models 为由流式输入或用户动作条件化、由内部状态支撑的系统，目标是闭合 action-perception loop。
- **Sensitivity**: 如果缺少 low-latency response 或 action-conditioned evolution，系统会退化为静态预测器或 one-shot generator。
- **Bounds**: 论文说明 mask-based interactive modeling 仍 underexplored，因此该启发式是 architecture-agnostic。
- **Code ref**: [无；综述论文未提供代码。]
- **Source**: Section 5

## H4: 长程一致性不能只靠更长 context；需要显式决定 what to write、what to retrieve、how to update、when to forget。
- **Rationale**: 论文指出 longer context alone is insufficient，consistency emerges from explicit policies over memory。
- **Sensitivity**: 对世界表示很敏感：implicit 2D video frames 容易 forgetting 和 drifting，explicit 3D scenes 空间一致性更强但动态状态更难。
- **Bounds**: 适用于 Stage IV 的 memory regulation；论文也提出记忆系统可能是硬件和数据约束下的 workaround。
- **Code ref**: [无；综述论文未提供代码。]
- **Source**: Section 6.3；Section 6.4

## H5: True World Models 的最终判据不是再加一个模块，而是让 Generative Heart、Interactive Loop 与 Memory System 长时间协同，产生 Persistence、Agency 与 Emergence。
- **Rationale**: 论文明确说 Stage V is not the addition of another component，而是 synthesis into a cohesive, autonomous whole。
- **Sensitivity**: 如果只有生成能力但没有共享历史、目标导向 agents 或涌现动态，就仍是 simulator 或 precursor。
- **Bounds**: 这是论文的概念性系统判据，不是可直接训练的工程指标。
- **Code ref**: [无；综述论文未提供代码。]
- **Source**: Section 7；Section 7.1
