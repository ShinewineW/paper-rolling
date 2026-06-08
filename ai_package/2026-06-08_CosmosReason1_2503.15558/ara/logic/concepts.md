# Concepts

## 物理常识本体（Physical Common Sense Ontology）
- **Notation**: 三大类：Space、Time、Fundamental Physics；16 个子类包括 Relationship、Plausibility、Affordance、Environment、Actions、Order、Causality、Camera、Planning、Attributes、States、Object Permanence、Mechanics、Electromagnetism、Thermodynamics、Anti-Physics。
- **Definition**: 一套层级化分类体系，将物理 AI 系统所需的物理常识归纳为三大类（空间 Space、时间 Time、基础物理 Fundamental Physics）及 16 个细粒度子类，用于衡量模型对现实世界规律的理解能力。
- **Boundary conditions**: 仅覆盖能力定义层面，不涉及具体实现机制；不对人形运动方式（如双腿行走）做规定；与具身推理本体共同构成 Physical AI 推理的完整框架，二者分别处理通用物理知识和针对具体实体的决策推理。
- **Related concepts**: ['具身推理本体', 'Physical AI SFT', '物理常识基准测试']

## 具身推理本体（Embodied Reasoning Ontology）
- **Notation**: 四大能力维度：Process Complex Sensory Inputs、Predict Action Effects、Respect Physical Constraints、Learn from Interactions；五类实体：humans、animals、robot arms、humanoid robots、autonomous vehicles。
- **Definition**: 一个二维分类框架，将具身推理能力（处理复杂感知输入、预测动作效果、尊重物理约束、从交互中学习）与实体类型（自然智体如人类动物，机器人系统如机械臂、人形机器人、自动驾驶汽车）做交叉映射，形成能力×实体的矩阵式本体。
- **Boundary conditions**: 论文明确仅实现前三项能力（感知输入、预测动作效果、尊重物理约束），第四项能力在本工作中未实现。本体定义适用于视频作为感知输入的场景，不涵盖触觉、力反馈等其他感知模态。
- **Related concepts**: ['物理常识本体', '具身推理 SFT', '具身推理基准测试']

## GRPO（Group Relative Policy Optimization）
- **Notation**: 优势函数：$$A _ { i } = \frac { R ( o _ { i } ) - \mathsf { m e a n } ( \mathcal { G } ) } { \mathsf { s t d } ( \mathcal { G } ) }$$，其中 $R(o_i)$ 为响应 $o_i$ 的奖励，$\mathcal{G} = \{o_1, o_2, \dots, o_G\}$ 为同一提示的响应组。
- **Definition**: 一种强化学习策略优化算法，通过在同一提示下生成一组响应、以组内奖励均值和标准差归一化计算优势函数，从而避免训练独立的 Critic 模型，简化训练流程并降低计算开销。
- **Boundary conditions**: 论文中 GRPO 仅用于多选题（MCQ）奖励场景，奖励信号为规则化字符串匹配（准确率奖励）和格式匹配（格式奖励）；不适用于开放式自由文本回答的奖励评估，后者因难以定义可验证奖励而被排除在 RL 训练之外。
- **Related concepts**: ['Physical AI RL 训练框架', '规则化可验证奖励', 'KL 惩罚项']

## 直觉物理推理（Intuitive Physics Reasoning）
- **Notation**: 三类子任务：Spatial Puzzle（2×2 图块乱序复原）、Arrow of Time（AoT，判断视频正向/逆向播放）、Object Permanence（判断物体是否违反持续存在规律而消失）。
- **Definition**: 模型对无需显式物理方程即可理解的基本物理现象的推理能力，涵盖空间连续性（通过空间拼图任务衡量）、时间箭头（通过视频正反播放判断任务衡量）以及物体永久性（通过仿真场景中物体消失判断任务衡量）三个子能力。
- **Boundary conditions**: 论文仅覆盖以上三个子任务，并非完整的直觉物理分类体系（完整分类见 Tab. 1）。「时间箭头」任务在 RL 阶段改善幅度有限，表明该能力仍是难点；「空间拼图」和「物体永久性」在 RL 后有明显提升。
- **Related concepts**: ['物理常识本体', '自监督数据生成', 'Physical AI SFT', 'Physical AI RL']

## 异步 RL 训练框架（Asynchronous RL Training Framework）
- **Notation**: 三大组件：Dispatcher（调度与分发）、Actor Rollout（生成响应并计算奖励与优势）、Policy Training（执行 RL 算法更新策略）。策略训练节点支持 5D 并行：DP、PP、CP、FSDP、TP；演员推理节点支持 DP、PP、TP。
- **Definition**: 论文提出的一种全异步、高容错的强化学习训练架构，将策略训练节点与演员推理（Actor Rollout）节点异构部署，通过统一调度器（Dispatcher）实现端到端异步并行，避免主流同置框架因同步开销导致的资源利用率低下问题。
- **Boundary conditions**: 效率提升数字（160%）为与同置框架对比的相对值，具体实现细节（如 NCCL 通信机制）属于基础设施层面。该框架专为 Physical AI RL 场景设计，其通用性适用范围论文未做额外声明。
- **Related concepts**: ['GRPO', 'Tensor Parallelism', 'Pipeline Parallelism', 'Physical AI RL']

## 混合 Mamba-MLP-Transformer 骨干（Hybrid Mamba-MLP-Transformer Backbone）
- **Notation**: Cosmos-Reason1-56B 中采用此架构（Nemotron-H），共 118 层，模型维度 8192，注意力头数 64，FFN 隐藏维度 32768；训练并行配置：TP=8，PP=2。
- **Definition**: 一种将线性时间复杂度的 Mamba 选择性状态空间模型（SSM）、MLP 层与少量 Transformer 自注意力层相结合的混合语言模型架构，旨在兼顾长序列建模效率与对长上下文细节的捕获能力。
- **Boundary conditions**: 该架构仅用于 Cosmos-Reason1-56B；Cosmos-Reason1-7B 采用标准 Transformer 骨干（Qwen2.5-VL）。论文未对混合比例（Mamba 层与 Transformer 层的数量比）做详细消融分析。
- **Related concepts**: ['Mamba 架构', 'Transformer 架构', 'Cosmos-Reason1-56B', 'PixelShuffle 下采样']

## 规则化可验证奖励（Rule-based Verifiable Rewards）
- **Notation**: 准确率奖励：<answer></answer> 标签内容字符串匹配；格式奖励：正则表达式匹配 <think></think> 与 <answer></answer> 标签结构。
- **Definition**: 在强化学习训练中使用无需神经网络判断、可通过确定性规则自动核验的奖励信号。论文中具体实现为：（1）准确率奖励——通过字符串匹配判断模型输出的 <answer> 标签内容是否与多选题标准答案一致；（2）格式奖励——通过正则表达式匹配验证模型是否将思考过程封装在 <think> 标签内、答案封装在 <answer> 标签内。
- **Boundary conditions**: 可验证奖励的前提是答案存在唯一正确选项，因此论文排除了自由文本答案的数据；该方案对具身推理数据的规模扩展存在一定限制，因为将非二元题目转化为高质量 MCQ 需要人工介入确保选项质量。
- **Related concepts**: ['GRPO', 'Physical AI RL', '多选题（MCQ）', '异步 RL 训练框架']
