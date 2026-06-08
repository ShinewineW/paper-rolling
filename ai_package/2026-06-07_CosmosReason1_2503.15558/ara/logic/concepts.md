# Concepts

## 物理常识 (Physical Common Sense)
- **Notation**: 三大类别：Space / Time / Fundamental Physics；16 个子类别如 Relationship、Plausibility、Affordance、Environment、Actions、Order、Causality、Camera、Planning、Attributes、States、Object Permanence、Mechanics、Electromagnetism、Thermodynamics、Anti-Physics
- **Definition**: 具身无关的物理世界通用理解能力，涵盖对空间关系、时间顺序、物理规律等的知识，用于判断真实世界中何种情况合理或不可能发生。由三大类别——Space（空间）、Time（时间）、Fundamental Physics（基础物理）——及 16 个细粒度子类别共同构成层级本体论。
- **Boundary conditions**: 仅涵盖通用的、与机体无关的世界知识，不包括特定机器人或载具的运动学/动力学参数；Anti-Physics 子类别专门处理违反物理定律的反例场景（如反重力、时间逆转），属于常识边界检测而非物理规律本身。
- **Related concepts**: ['物理AI本体论', '直觉物理', 'Physical AI SFT']

## 具身推理 (Embodied Reasoning)
- **Notation**: 二维本体论：能力维度 × 主体类型；三项核心具身任务：任务完成验证 (task-completion verification)、动作可供性评估 (action affordance)、下一步合理动作预测 (next plausible action prediction)
- **Definition**: AI 系统在物理环境中感知复杂感觉输入、预测行动效果、遵从物理约束并从交互中学习的能力集合，以二维本体论组织：四类推理能力（处理复杂感官输入、预测行动效果、遵从物理约束、从交互中学习）× 五类具身主体（人类/动物等自然主体、机械臂、人形机器人、自动驾驶车辆等机器人系统）。
- **Boundary conditions**: 本文实现中仅覆盖前三种能力，「从交互中学习」不在当前训练范围内；具身推理基于短时程 (short-horizon) 动作/子任务粒度，非全局长程规划；动作粒度层级分三级：atomic actions（动作）→ subtasks（子任务）→ goals（目标）。
- **Related concepts**: ['物理常识', '物理AI本体论', 'Physical AI SFT', '长链推理']

## 物理AI本体论 (Physical AI Ontology)
- **Notation**: 物理常识本体论：三大类 / 16 子类（见 Table 1）；具身推理本体论：4 × N 二维矩阵（见 Table 2）
- **Definition**: 为统一定义和度量 Physical AI 推理能力而设计的结构化知识框架，包括两套本体论：其一是层级式物理常识本体论（Space / Time / Fundamental Physics 三类、16 个细粒度子类别），其二是二维具身推理本体论（4 类能力 × 5 类主体）。
- **Boundary conditions**: 本体论仅刻画「能力」而非「实现路径」；当前版本不覆盖听觉、触觉等非视觉感知模态；具身主体分类涵盖人类/动物与机械臂/人形机器人/自动驾驶车辆，不含微型机器人或分布式多机器人系统。
- **Related concepts**: ['物理常识', '具身推理', 'Physical AI SFT']

## 混合 Mamba-MLP-Transformer 架构 (Hybrid Mamba-MLP-Transformer)
- **Notation**: Cosmos-Reason1-56B 采用此架构，共 118 层，模型维度 8192，FFN 隐藏维度 32768，注意力头数 64；训练并行配置 TP=8, PP=2
- **Definition**: 将线性时间复杂度的 Mamba 选择性状态空间模型 (SSM) 与 MLP 层及少量 Transformer 层混合组合的 LLM 骨干架构，以线性时间复杂度处理长序列，同时借助 Transformer 层弥补 Mamba 在长上下文细节捕捉上的不足。
- **Boundary conditions**: 混合架构仅应用于 Cosmos-Reason1-56B，7B 版本使用纯 Transformer；Mamba SSM 在极长序列上仍可能遗漏某些细节，Transformer 层的补充仅解决部分问题；架构预训练权重来自 Nemotron-H（NVIDIA, 2025），非从零训练。
- **Related concepts**: ['Cosmos-Reason1-56B', '长链推理', 'PixelShuffle 下采样']

## GRPO (Group Relative Policy Optimization)
- **Notation**: $$A _ { i } = \frac { R ( o _ { i } ) - \mathsf { m e a n } ( \mathcal { G } ) } { \mathsf { s t d } ( \mathcal { G } ) }$$，其中 $\mathcal{G} = \{o_1, o_2, \dots, o_G\}$ 为同一提示词的一组响应，$R(o_i)$ 为响应 $o_i$ 的奖励。
- **Definition**: 一种用于 RL 后训练的策略优化算法，通过对同一提示词的一组采样响应归一化奖励来计算优势函数，无需单独训练和维护批评者 (critic) 模型，从而降低计算成本。优势 $A_i$ 定义为组内奖励去均值后除以标准差。
- **Boundary conditions**: GRPO 的优势计算假设同组响应在分布上可比；其适用前提是奖励可规则化验证（如 MCQ 字符串匹配），对需要人工评估的开放域生成任务不直接适用；KL 惩罚系数 0.005 和学习率 $4 \times 10^{-6}$ 为本文具体超参数，不具备普适性。
- **Related concepts**: ['Physical AI RL', '规则化可验证奖励', '长链推理']

## 直觉物理 (Intuitive Physics)
- **Notation**: 三项任务：Spatial Puzzle（空间拼图，4选1或多选）、Arrow of Time / AoT（时间箭头，二分类）、Object Permanence（物体恒常性，二分类）
- **Definition**: 针对基础物理推理能力的自监督训练范式，涵盖三项任务：空间连续性推理（空间拼图，打乱视频帧块后还原空间位置）、时间方向推理（时间箭头，判断视频是否正放或倒放）、物体恒常性推理（物体永久消失违反物体恒常性的检测）。这三类任务均可由数据结构本身自动生成标签，无需大规模人工标注。
- **Boundary conditions**: 当前时间箭头任务重点关注宏观尺度时间不可逆性，不涉及量子尺度或微观物理现象；空间拼图仅使用 2×2 分块，不覆盖更复杂的拼图结构；物体恒常性数据来自机器人仿真平台 Libero，可能与真实世界场景存在域偏移。
- **Related concepts**: ['Physical AI SFT', 'GRPO', 'Physical AI RL']

## 规则化可验证奖励 (Rule-based Verifiable Rewards)
- **Notation**: 准确率奖励：MCQ 字符串匹配；格式奖励：正则表达式匹配 <think>...</think> 与 <answer>...</answer>
- **Definition**: Physical AI RL 后训练中采用的两类奖励机制：(1) 准确率奖励——检查模型响应中 <answer></answer> 标签内的答案是否与标准答案匹配（基于字符串匹配的 MCQ 验证）；(2) 格式奖励——通过正则表达式验证模型是否将推理过程包含在 <think></think> 标签内、最终答案包含在 <answer></answer> 标签内。
- **Boundary conditions**: 奖励设计依赖 MCQ 格式，要求所有训练样本均有明确唯一的标准答案；复杂的物理常识和具身推理任务样本难以大规模转化为 MCQ（需要人工干预），因此 RL 数据集规模（约 30,304 条）远小于 SFT 数据集；RoboFail 基准在 RL 后训练后性能未改善，表明规则化奖励对复杂感知细节场景有局限。
- **Related concepts**: ['GRPO', 'Physical AI RL', '直觉物理']

## Physical AI SFT (物理AI监督微调)
- **Notation**: 数据规模约 4M 条；Cosmos-Reason1-7B 训练配置：余弦退火 lr 从 $1 \times 10^{-5}$ 衰减至 $1 \times 10^{-6}$；Cosmos-Reason1-56B 训练配置：lr $1 \times 10^{-5}$；全局 batch size：7B 为 256，56B 为 32；Adam 优化器 $\beta_1, \beta_2 = (0.9, 0.95)$，weight decay 0.1
- **Definition**: 将预训练多模态大语言模型特化为 Physical AI 推理模型的第一训练阶段，利用约 400 万条视频-文本对标注数据（含物理常识 VQA、具身推理数据集和直觉物理数据），通过监督微调同时增强物理常识理解和具身推理能力。训练数据包括「理解」注释（VQA 问答对）和「推理」注释（长链思维轨迹，由 DeepSeek-R1 蒸馏生成）。
- **Boundary conditions**: SFT 数据中视觉上下文通过 VLM 生成的结构化描述压缩为文本后再交给 R1 推理，因此 R1 的推理质量受限于描述准确性；平衡采样策略防止单一领域过拟合，但可能限制对稀有场景的专项优化；第二阶段的 RL 是对 SFT 的补充而非替代。
- **Related concepts**: ['Physical AI RL', '物理常识', '具身推理', '直觉物理']

## 异步 RL 训练框架 (Asynchronous RL Training Framework)
- **Notation**: 三大组件：Dispatcher（数据调度）、Actor Rollout（响应生成与奖励计算）、Policy Training（策略优化）；策略训练节点支持 5D-parallelism：DP/PP/CP/FSDP/TP；训练效率提升约 160%
- **Definition**: 专为 Physical AI 强化学习设计的全异步、高容错分布式训练架构，将策略训练节点（支持 DP/PP/CP/FSDP/TP 五维并行）与演员推理节点（支持 DP/PP/TP）异构部署，通过统一调度器 (Dispatcher) 实现端到端异步并行，相较于主流协同部署框架 (colocated frameworks) 训练效率提升约 160%。
- **Boundary conditions**: 「160% 效率提升」是相对于协同部署框架的对比数据，具体数值依赖特定硬件和工作负载配置；动态扩缩容能力在理论上可行，但实际效果受网络带宽和检查点管理限制；该框架针对多选题格式的规则化奖励优化，对需要复杂奖励计算的场景可能需要额外适配。
- **Related concepts**: ['GRPO', 'Physical AI RL', '规则化可验证奖励']

## 长链推理 (Long Chain-of-Thought Reasoning)
- **Notation**: 推理格式：<think> 推理轨迹 </think> <answer> 最终答案 </answer>；推理输出最大长度截断为 6144 tokens（RL 训练阶段）
- **Definition**: 在生成最终回答前，通过在 <think>...</think> 标签内产生详细中间推理步骤的测试时扩展 (test-time scaling) 机制。该机制使模型在回答物理常识和具身推理问题时可执行「慢思考 (System 2)」，弥补单步直觉推断（System 1）的局限。
- **Boundary conditions**: 「长链推理的质量」（推理轨迹的正确性）在本文中未被定量评估，仅评估最终答案的准确率；当链推理过长时（如 RoboFail 场景），模型可能出现「过度思考 (overthinking)」导致混淆；6144 tokens 的最大长度截断可能限制极复杂推理任务的表现。
- **Related concepts**: ['Physical AI SFT', '规则化可验证奖励', 'GRPO', '直觉物理']
