# Concepts

## Vision-Language-Action foundation model
- **Notation**: 
- **Definition**: 一种面向机器人操作的基础模型范式，用视觉、语言和动作信号共同支持自然语言指令驱动的多任务执行；本文把它作为研究对象，关注其在真实机器人数据规模扩大时的泛化、适配和训练效率。<!--ref: Vision-Language-Action (VLA) foundation models [5, 6, 27] have emerged as a promising method for enabling robots to perform diverse manipulation tasks guided by natural language instructions. -->
- **Boundary conditions**: 本文讨论范围限定在机器人操作中的 VLA 基础模型，重点是双臂真实世界操作、后训练适配和评测；不把仿真结果直接等同于真实物理世界表现。<!--ref: Although simulation environments typically employ idealized physical models, their results often do not fully represent the complexity of the real physical world. -->
- **Related concepts**: ['LingBot-VLA', 'pre-trained VLM', 'action expert', 'Flow Matching']

## LingBot-VLA
- **Notation**: 
- **Definition**: 本文提出的实用型 VLA foundation model，结合真实世界机器人操作数据、跨平台评测和优化训练代码库，目标是在性能、泛化与训练效率之间取得可部署的平衡。<!--ref: In this paper, we present LingBot-VLA, a pragmatic VLA foundation model trained on about 20,000 hours of real-world manipulation data from 9 robotic platforms. -->
- **Boundary conditions**: 它的预训练与评测主要围绕真实世界双臂机器人操作；论文结论不声称已经覆盖单臂、移动机器人或开放无限制环境，后者被列为未来方向。<!--ref: Future research will focus on scaling the model versatility by integrating single-arm and mobile robotic data, paving the way for more diverse and mobile manipulation capabilities in unconstrained environments. -->
- **Related concepts**: ['Vision-Language-Action foundation model', 'MoT', 'action expert', 'vision distillation', 'GM-100']

## pre-trained VLM
- **Notation**: $\mathbf { I } _ { t }$ 表示操作图像 token，$\mathbf { T } _ { t }$ 表示任务指令，二者进入观测条件 $\mathbf { O } _ { t }$。
- **Definition**: LingBot-VLA 中承担语义和多模态条件编码的视觉语言骨干，用于编码多视角操作图像与任务指令，并为后续动作生成提供条件信息。<!--ref: Multi-view operational images and the related task instruction are uniformly encoded through a VLM to establish multimodal conditioning for subsequent action generation. -->
- **Boundary conditions**: 论文点名使用 Qwen2.5-VL [2] 作为 VLM，但 concept 本身指的是该类视觉语言骨干；不要把没有在论文中出现的其他具体 VLM 产品替换进来。<!--ref: LingBot-VLA integrates the pre-trained VLM (i.e., Qwen2.5- VL [2]) -->
- **Related concepts**: ['LingBot-VLA', 'MoT', 'observation condition', 'action expert']

## action expert
- **Notation**: $v _ { \theta } ( \mathbf { A } _ { t , s } , \mathbf { O } _ { t } , s )$
- **Definition**: LingBot-VLA 中初始化的动作生成模块，接收机器人本体状态与动作片段，并在观测条件下预测动作生成所需的连续向量场。<!--ref: initialized action generation module called ‘action expert’ -->
- **Boundary conditions**: 它不是独立于观测条件运行的控制器，也不是论文中未给出的传统规划器；其训练目标由 Flow Matching objective 描述。<!--ref: The action expert v _ { \theta } is trained to predict the conditional vector field by minimizing the Flow Matching objective -->
- **Related concepts**: ['Flow Matching', 'action chunk', 'MoT', 'blockwise causal attention']

## Mixture-of-Transformers
- **Notation**: 联合序列由 $[ \mathbf { O } _ { t } , \mathbf { A } _ { t } ]$ 表示。
- **Definition**: LingBot-VLA 用来组织 VLM 与 action expert 的架构形式，视觉语言模态和动作模态走不同 transformer pathway，并通过共享 self-attention 进行逐层统一序列建模。<!--ref: organized via a Mixture-of-Transformers (MoT) architecture like BAGEL [10] -->
- **Boundary conditions**: 不要把 MoT 解读为任意专家路由或稀疏专家模型；本文描述的是视觉语言与动作路径的分离处理和共享注意力耦合。<!--ref: distinct transformer pathways, coupled by a shared self-attention mechanism -->
- **Related concepts**: ['pre-trained VLM', 'action expert', 'blockwise causal attention', 'observation condition']

## observation condition
- **Notation**: $$\begin{array} { r } { \mathbf { O } _ { t } = [ \mathbf { I } _ { t } ^ { 1 } , \mathbf { I } _ { t } ^ { 2 } , \mathbf { I } _ { t } ^ { 3 } , \mathbf { T } _ { t } , \mathbf { s } _ { t } ] , } \end{array}\tag{1}$$
- **Definition**: 时间步 $t$ 的观测条件，组合操作图像 token、任务指令和机器人状态，用作动作片段条件生成的上下文。<!--ref: the observation context is defined as -->
- **Boundary conditions**: 它不是只包含图像或语言的上下文；论文明确把机器人状态也纳入 $\mathbf { O } _ { t }$。<!--ref: the task instruction \mathbf { T } _ { t } , and the robot state \mathbf { s } _ { t } -->
- **Related concepts**: ['action chunk', 'pre-trained VLM', 'blockwise causal attention', 'Flow Matching']

## action chunk
- **Notation**: $$\mathbf { A } _ { t } = [ \mathbf { a } _ { t } , \mathbf { a } _ { t + 1 } , \ldots , \mathbf { a } _ { t + T - 1 } ] ,\tag{2}$$
- **Definition**: 从时间步 $t$ 开始的一段未来动作序列，是 LingBot-VLA 在观测条件下要建模和生成的动作目标。<!--ref: The corresponding action sequence is denoted as -->
- **Boundary conditions**: 不要把动作片段理解为完整任务轨迹；论文将 $T$ 定义为预测轨迹的 temporal horizon，而非整段任务长度。<!--ref: where T represents the action chunk length, i.e., the temporal horizon of the predicted trajectory -->
- **Related concepts**: ['observation condition', 'action expert', 'Flow Matching', 'blockwise causal attention']

## Flow Matching
- **Notation**: $$p ( \mathbf { A } _ { t , s } | \mathbf { A } _ { t } ) = \mathcal { N } ( s \mathbf { A } _ { t } , ( 1 - s ) \mathbf { I } ) .\tag{3}$$ $$\begin{array} { r } { \mathcal { L } _ { \mathrm { F M } } = \mathbb { E } _ { s \sim \mathcal { U } \left[ 0 , 1 \right] , \mathbf { A } _ { t } , \epsilon } \left\| v _ { \theta } ( \mathbf { A } _ { t , s } , \mathbf { O } _ { t } , s ) - ( \mathbf { A } _ { t } - \epsilon ) \right\| ^ { 2 } , } \end{array}\tag{4}$$
- **Definition**: LingBot-VLA 用于连续动作建模的训练方法，通过在高斯噪声与真实动作之间构造线性概率路径，并训练 action expert 预测条件向量场。<!--ref: The action expert v _ { \theta } is trained to predict the conditional vector field by minimizing the Flow Matching objective -->
- **Boundary conditions**: 该损失是论文显式给出的训练目标；不要把只用于其他阶段或未在论文中出现的加权项加入这个公式。<!--ref: minimizing the Flow Matching objective -->
- **Related concepts**: ['action expert', 'action chunk', 'observation condition']

## blockwise causal attention
- **Notation**: $[ \mathbf { I } _ { t } ^ { 1 } , \mathbf { I } _ { t } ^ { 2 } , \mathbf { I } _ { t } ^ { 3 } , \mathbf { T } _ { t } ]$，$[ \mathbf { s } _ { t } ]$，$[ \mathbf { a } _ { t } , \mathbf { a } _ { t + 1 } , \dots , \mathbf { a } _ { t + T - 1 } ]$
- **Definition**: 一种用于联合序列 $[ \mathbf { O } _ { t } , \mathbf { A } _ { t } ]$ 的注意力掩码方案，把图像与指令、状态、动作序列划分为功能块，块间按因果顺序访问，块内双向访问。<!--ref: Following π _ { 0 } [6], we implement blockwise causal attention for modeling the joint sequence -->
- **Boundary conditions**: 它不是普通全序列双向注意力；论文明确区分块间因果掩码和同一块内双向注意力。<!--ref: tokens in each block can only attend to themselves and those in preceding blocks. Conversely, all tokens within the same block employ bidirectional attention -->
- **Related concepts**: ['MoT', 'observation condition', 'action chunk', 'action expert']

## vision distillation
- **Notation**: $$\begin{array} { r } { \mathcal { L } _ { d i s t i l l } = \mathbb { E } _ { \mathbf { Q } _ { t } } \left| \mathrm { P r o j } ( \mathbf { Q } _ { t } ) - \mathbf { D } _ { t } \right| , } \end{array}\tag{5}$$
- **Definition**: LingBot-VLA 为引入空间意识采用的视觉蒸馏方法：使用与多视角操作图像对应的 learnable queries，经 VLM 处理后与 LingBot-Depth 的 depth tokens 对齐。<!--ref: To explicitly capture spatial awareness within manipulation environments and further enhance the robot’s execution robustness, we adopt a vision distillation approach -->
- **Boundary conditions**: 这是对 VLM learnable queries 与 depth tokens 的对齐，不应被写成改变 Flow Matching 训练目标的动作损失项。<!--ref: We align the VLM learnable queries and LingBot-Depth tokens by minimizing the distillation loss -->
- **Related concepts**: ['LingBot-Depth', 'pre-trained VLM', 'spatial awareness', 'Flow Matching']

## training efficiency optimization
- **Notation**: FSDP，HSDP，torch.float32，torch.bfloat16，FlexAttention，torch.compile
- **Definition**: 本文代码库层面的训练效率设计，包括数据加载、分布式训练策略和算子级加速，用于支持大规模 VLA 训练。<!--ref: our codebase implements systemic optimizations in data loading, distributed training strategies, and operator-level acceleration. -->
- **Boundary conditions**: 不要把这里的工程优化误写成模型性能指标本身；论文把它作为训练吞吐和可扩展性的基础设施优化来评估。<!--ref: We adopted sample throughput (samples/s) as the primary evaluation metric. -->
- **Related concepts**: ['LingBot-VLA', 'action expert', 'MoT']
