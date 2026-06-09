# Concepts

## Physical AI
- **Notation**: 
- **Definition**: 设计用于与物理世界交互的人工智能系统，需要感知、理解并对物理世界进行推理，以遵循指令并采取适当行动实现目标。其核心能力分为物理常识推理与具身推理两类。
- **Boundary conditions**: 本文聚焦于视频作为感官输入的代表性场景，「从交互中学习」被明确列为未来工作，不在当前系统范围内。
- **Related concepts**: ['物理常识', '具身推理', '多模态大语言模型']

## 物理常识层级本体
- **Notation**: 
- **Definition**: 将物理常识组织为三大类别（空间 Space、时间 Time、基础物理 Fundamental Physics）并进一步细分为 16 个细粒度子类别的层级分类体系。该本体以能力为导向，而非以机制或具身形态为导向。
- **Boundary conditions**: 本体以能力为粒度，不规定实现机制（如不要求类人行走），子类别定义见论文 Tab. 1，不覆盖超出上述 16 个子类别的物理知识领域。
- **Related concepts**: ['Physical AI', '具身推理二维本体', '直觉物理']

## 具身推理二维本体
- **Notation**: 
- **Definition**: 以「能力维度」×「具身类型维度」构成的二维分类框架：能力维度包含处理复杂感官输入、预测动作效果、遵守物理约束、从交互中学习四项；具身类型维度包含自然主体（人类、动物）与机器人系统（机械臂、类人机器人、自动驾驶车辆）两大类。
- **Boundary conditions**: 「从交互中学习」在本文被留作未来工作；当前评估仅覆盖 humans、robot arms、humanoid robots、autonomous vehicles 四类具身形态。
- **Related concepts**: ['Physical AI', '物理常识层级本体', '任务完成验证', '下一步动作预测', '动作 Affordance']

## GRPO（组内相对策略优化）
- **Notation**: $$A _ { i } = \frac { R ( o _ { i } ) - \mathsf { m e a n } ( \mathcal { G } ) } { \mathsf { s t d } ( \mathcal { G } ) }$$
- **Definition**: 一种强化学习策略优化算法，通过在同一提示对应的一组响应内部对奖励进行归一化来计算优势函数，从而避免训练并维护单独的 Critic 模型。
- **Boundary conditions**: GRPO 的适用前提是奖励可被规则化、可验证地计算；本文借助多选题（MCQ）格式将物理常识与具身推理问题转化为可验证答案，从而满足该前提。
- **Related concepts**: ['Physical AI RL 后训练', '基于规则的可验证奖励', '准确率奖励', '格式奖励']

## 基于规则的可验证奖励
- **Notation**: 
- **Definition**: 不依赖额外奖励模型、仅通过确定性规则（字符串匹配、正则表达式等）验证模型输出正确性的奖励机制。本文使用两类奖励：准确率奖励（答案是否与标准答案匹配）和格式奖励（输出是否符合 `<think>` / `<answer>` 标签规范）。
- **Boundary conditions**: 仅适用于可被转化为 MCQ 格式的任务；对于需要自由回答的开放式评估场景，该奖励机制不直接适用。格式奖励仅约束输出结构，不评估思维链的质量。
- **Related concepts**: ['GRPO', 'Physical AI RL 后训练', '多选题']

## 混合 Mamba-MLP-Transformer 架构
- **Notation**: 
- **Definition**: 将线性时间复杂度的选择性状态空间模型（Mamba）与 MLP 层交替排列，并引入少量 Transformer 自注意力层以弥补 Mamba 在长序列细节建模上的不足，形成兼顾效率与建模能力的混合主干架构。
- **Boundary conditions**: Cosmos-Reason1-7B 使用纯 Transformer 主干，不采用该混合架构；混合比例（Mamba 层 vs Transformer 层的具体数量）见预训练基础模型的原始论文，本文未详细列出。
- **Related concepts**: ['Cosmos-Reason1-56B', 'PixelShuffle', '视觉编码器', 'Tensor Parallelism']

## 直觉物理（Intuitive Physics）
- **Notation**: 
- **Definition**: 指模型无需显式物理方程即可对空间连续性、时间方向性（时间箭头）和对象恒存性等基础物理属性进行推理的能力。本文通过三类自监督任务来强化和评估该能力：空间拼图（Spatial Puzzles）、时间箭头（Arrow of Time, AoT）、对象恒存性（Object Permanence）。
- **Boundary conditions**: 当前评估以 100 个视频/问题为单位；论文指出现有主流 VLM 在时间箭头和对象恒存性任务上仅接近随机猜测水平，表明现有通用基准未能充分考察这类基础物理推理能力。
- **Related concepts**: ['物理常识层级本体', 'Physical AI SFT', 'Physical AI RL 后训练']

## 异步 RL 训练框架
- **Notation**: 
- **Definition**: 将策略训练节点（Policy Training）与 Actor 采样节点（Actor Rollout）解耦部署，通过统一调度器（Dispatcher）异步分发训练提示，使整个训练流水线端到端异步化，同时支持节点故障后快速自愈和动态扩缩容的分布式强化学习基础设施。
- **Boundary conditions**: 论文声称约 160% 的训练效率提升是相对于协同部署框架而言（分析推断，论文未显式声明与特定基线的精确对比配置）；节点故障自愈仅在训练步内有效，不涵盖跨步级别的断点续训。
- **Related concepts**: ['GRPO', '5D 并行', 'Tensor Parallelism']
