# Concepts

## True World Model
- **Notation**: G, (F, C), M；z_t 表示潜在信念状态，h_t 表示确定性记忆状态，a_t 表示动作，o_t 表示观测。
- **Definition**: 论文将 True World Model 定义为由 Generative Heart、Interactive Loop 和 Memory System 三个核心子系统综合而成的系统；它不是单一模型块，而是能够生成世界状态、实时闭合动作感知循环，并在长时程中维持一致性的整体。
- **Boundary conditions**: Unified Model 只拥有强生成能力时仍只是前驱；缺少专门的交互循环和显式记忆系统，就不能支撑持久的、由智能体栖居的世界。
- **Related concepts**: ['Generative Heart', 'Interactive Loop', 'Memory System', 'Persistence', 'Agency', 'Emergence']

## Generative Heart
- **Notation**: G = (p_θ(z_{t+1}|z_t,a_t), p_θ(o_t|z_t), p_θ(r_t|z_t,a_t), p_θ(γ_t|z_t,a_t))
- **Definition**: Generative Heart 是世界模型的基础子系统，用学习到的生成过程刻画世界的动态与外观，并预测未来状态、观测以及任务相关结果。
- **Boundary conditions**: 它本身不足以构成 True World Model；如果没有 Interactive Loop 与 Memory System，系统仍可能只是被动生成器或短程预测器。
- **Related concepts**: ['True World Model', 'Dynamics Model', 'Observation Model', 'Outcome Model', 'Generation']

## Interactive Loop
- **Notation**: F: q_φ(z_t|h_{t-1},o_t); C = (π_η(a_t|z_t,h_t), v_ω(z_t,h_t))
- **Definition**: Interactive Loop 是让模型不止成为被动影片生成器的闭环机制；在部分可观测世界中，它需要推断滤波器解释实时观测，并需要策略和值函数基于理解采取行动和评估轨迹。
- **Boundary conditions**: 仅有闭环反应仍不足以维持持久世界；论文指出没有专门记忆和状态管理时，交互系统会难以支撑长期一致性。
- **Related concepts**: ['True World Model', 'Inference Model', 'Control Model', 'Interactive Generative Models', 'Agency']

## Memory System
- **Notation**: M: h_t = f_ψ(h_{t-1}, z_t, a_{t-1})
- **Definition**: Memory System 是保证长时程一致性的子系统，它让过去事件影响未来，并通过循环状态 h_t 表征历史。
- **Boundary conditions**: 长上下文本身不等同于可靠记忆；论文强调一致性来自关于写入、检索、更新和遗忘的显式策略。
- **Related concepts**: ['True World Model', 'Persistence', 'Memory and Consistency', 'Externalized Memory', 'Architectural Persistence']

## Mask-based Models
- **Notation**: MLM, MIM, [MASK]
- **Definition**: Mask-based Models 是通向世界模型的第一阶段，系统通过重建输入中缺失或损坏的部分学习，论文将其概括为 mask、infill 和 generalize。
- **Boundary conditions**: 这一阶段统一的是预训练范式，而不是模型本身；不同模态中的模型仍是专门架构，无法形成整体世界观。
- **Related concepts**: ['Unified Models', 'Masked Language Modeling', 'Masked Image Modeling', 'Discrete Diffusion']

## Unified Models
- **Notation**: shared backbone + same paradigm
- **Definition**: Unified Models 是处理并生成多种模态的系统，具有共享 backbone 和相同范式；论文把它作为从分散专门模型走向 True World Model 的关键阶段。
- **Boundary conditions**: 论文排除简单拼接不同范式的 glue models；即使统一架构取得进展，许多视觉优先模型仍受限于 single-shot synthesis 或 stepwise editing，缺少连续实时闭环交互能力。
- **Related concepts**: ['Mask-based Models', 'Language-Prior Modeling', 'Visual-Prior Modeling', 'True World Model']

## Interactive Generative Models
- **Notation**: action-conditioned evolution, internal state, closed action-perception loop
- **Definition**: Interactive Generative Models 是输出受流式输入或用户动作条件化、并由内部状态支持的生成系统；它们不再只是静态预测器或一次性生成器。
- **Boundary conditions**: 论文指出 mask-based interactive modeling 仍然探索不足，因此该阶段采用架构无关视角；同时，实时交互并未解决长时程一致性。
- **Related concepts**: ['Interactive Loop', 'Language-based Worlds', 'Video-based Worlds', 'Scene-based Worlds', 'Memory and Consistency']

## Memory and Consistency
- **Notation**: externalized memory, recurrent state, context compression, consistency policies
- **Definition**: Memory and Consistency 是世界模型演化的第四阶段，目标是让模型在长时程中维持连贯状态、保存身份并抵抗漂移。
- **Boundary conditions**: 论文明确说 mask-based persistent memory 仍探索不足且差异很大，因此该阶段聚焦记忆与一致性，而不是限定在某种 mask-specific 机制。
- **Related concepts**: ['Memory System', 'Externalized Memory', 'Architectural Persistence', 'Drift', 'Forgetting']

## Persistence
- **Notation**: 由 Memory System (M) 支撑
- **Definition**: Persistence 是 True World Model 的定义性属性之一，指世界状态和历史独立于单一用户会话而存在，并随时间积累后果。
- **Boundary conditions**: 短期上下文、临时 KV cache 或短程对象保持不能自动构成 Persistence；论文关注的是跨长时程维持世界历史和后果。
- **Related concepts**: ['True World Model', 'Memory System', 'Emergence', 'Agency']

## Agency
- **Notation**: 由 Interactive Loop (F, C) 支撑
- **Definition**: Agency 指世界中存在多个有目标导向的智能体，包括人类或 AI，它们在共享语境中交互。
- **Boundary conditions**: 单一环境或单用户控制的交互体验不必然具备论文所说的 Agency；关键在于多个目标导向智能体在共享世界中行动。
- **Related concepts**: ['True World Model', 'Interactive Loop', 'Persistence', 'Emergence']

## Emergence
- **Notation**: G + (F, C) + M over time
- **Definition**: Emergence 指世界的宏观动态来自智能体与底层规则的微观互动，而不是显式脚本化。
- **Boundary conditions**: 论文把 Emergence 视为三大子系统综合后的临界属性；单独的生成能力、交互能力或记忆能力都不足以保证它出现。
- **Related concepts**: ['True World Model', 'Generative Heart', 'Interactive Loop', 'Memory System', 'Agency']

## Coherence Problem
- **Notation**: evaluation of internal logical, causal, and narrative coherence
- **Definition**: Coherence Problem 是 True World Model 前沿挑战中的评估问题：当世界模型书写自身历史时，需要形式化并测量其内部逻辑、因果和叙事一致性。
- **Boundary conditions**: 传统模型与外部真值比对的 fidelity 不能直接覆盖该问题，因为 True World Model 的历史由模型自身生成。
- **Related concepts**: ['True World Model', 'Memory and Consistency', 'Alignment Problem', 'Compression Problem']

## Compression Problem
- **Notation**: causally sufficient state abstractions
- **Definition**: Compression Problem 是 True World Model 前沿挑战中的扩展问题：持续增长的历史会带来计算崩溃风险，因此需要学习因果充分的状态抽象，保留后果并丢弃噪声。
- **Boundary conditions**: 简单扩大上下文窗口不一定解决该问题；论文将世界模型也视为需要科学观察的对象，而不仅是工程系统。
- **Related concepts**: ['Persistence', 'Memory System', 'Coherence Problem', 'True World Model']

## Alignment Problem
- **Notation**: substrate alignment + emergent dynamics alignment
- **Definition**: Alignment Problem 是 True World Model 前沿挑战中的安全问题，涉及生成过程与人类价值对齐，以及作为多智能体社会基底时涌现动态的对齐。
- **Boundary conditions**: 它不同于普通单环境模拟器的对齐；难点来自持久、自主世界成为多智能体社会的基底。
- **Related concepts**: ['True World Model', 'Agency', 'Emergence', 'Coherence Problem']
