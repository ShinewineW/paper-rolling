# Concepts

## Physical AI
- **Notation**: Physical AI
- **Definition**: 本文中的 Physical AI 指带有传感器和执行器、能够在物理环境中根据感知输入采取动作的具身系统。
- **Boundary conditions**: 该概念不等同于纯文本或纯图像生成任务；本文强调的是能支持感知、控制、策略验证和合成数据生成的物理世界交互系统。
- **Related concepts**: ['world simulator', 'Cosmos-Predict2.5', 'Cosmos-Transfer2.5', 'VLA']

## world simulator
- **Notation**: world simulator
- **Definition**: world simulator 是一种能根据 Physical AI agent 的动作或条件生成高质量、多样化视觉环境的代理环境，用来在真实部署前安全地训练或验证系统。
- **Boundary conditions**: 它不是完整的物理引擎定义；本文主要讨论视觉世界模拟，且许多控制、动作和多视角能力通过视频生成模型扩展得到。
- **Related concepts**: ['Physical AI', 'world model', 'closed-loop simulation', 'policy evaluation']

## Cosmos-Predict2.5
- **Notation**: Cosmos-Predict2.5
- **Definition**: Cosmos-Predict2.5 是本文提出的 Cosmos World Foundation Models 新一代视频世界基础模型，基于 flow-based architecture，统一 Text2World、Image2World 和 Video2World 生成，并使用 Cosmos-Reason1 提供文本条件。
- **Boundary conditions**: 它不同于 Cosmos-Transfer2.5；前者是基础世界预测模型，后者是在其上扩展的 control-net style world translation 框架。
- **Related concepts**: ['flow matching', 'Text2World', 'Image2World', 'Video2World', 'Cosmos-Reason1']

## flow matching
- **Notation**: $$\mathbf { x } _ { t } = ( 1 - t ) \mathbf { x } + t { \boldsymbol { \epsilon } } .\tag{1}$$
$$\mathbf { v } _ { t } = \epsilon - \mathbf { x } .\tag{2}$$
$$\begin{array} { r } { \mathcal { L } ( \boldsymbol { \theta } ) = \mathbb { E } _ { \mathbf { x } , \boldsymbol { \epsilon } , \mathbf { c } , t } \left\| \mathbf { u } ( \mathbf { x } _ { t } , t , \mathbf { c } ; \boldsymbol { \theta } ) - \mathbf { v } _ { t } \right\| ^ { 2 } , } \end{array}\tag{3}$$
- **Definition**: flow matching 是本文用于训练 Cosmos-Predict2.5 的生成建模方式，让去噪网络预测 diffusion trajectory 的 velocity，而不是沿用 Cosmos-Predict1 中 EDM 的网络参数化方式。
- **Boundary conditions**: 该概念只覆盖论文显式给出的训练公式；推理阶段的控制输入融合、RNDS 指标或控制分支权重不属于该训练损失公式。
- **Related concepts**: ['Cosmos-Predict2.5', 'velocity prediction', 'shifted logit-normal distribution', 'denoising network']

## shifted logit-normal distribution
- **Notation**: $$t _ { s } = \frac { \beta t } { 1 + ( \beta - 1 ) t }\tag{4}$$
- **Definition**: shifted logit-normal distribution 是本文对训练 timestep 分布的调整，用单调变换把采样偏向更高噪声区域，以缓解高分辨率内容中相邻像素相关性过强带来的学习困难。
- **Boundary conditions**: 它是训练采样策略，不是新的网络层，也不是评价指标；当 beta 未移位时论文说明不会改变 timestep。
- **Related concepts**: ['flow matching', 'training timestep', 'temporal consistency', 'high-resolution generation']

## 统一的 Text2World Image2World Video2World
- **Notation**: Text2World / Image2World / Video2World
- **Definition**: Cosmos-Predict2.5 被设计为在 Text2World、Image2World 和 Video2World 三种模式下运行：仅文本、文本加参考图像、文本加视频序列分别作为生成条件。
- **Boundary conditions**: 三种模式的条件来源不同；Image2World 和 Video2World 使用 frame-replacement strategy，Text2World 则不依赖输入图像或视频帧。
- **Related concepts**: ['Cosmos-Predict2.5', 'frame-replacement strategy', 'conditioning information', 'Cosmos-Reason1']

## frame-replacement strategy
- **Notation**: conditioned frames
- **Definition**: frame-replacement strategy 是 Image2World 和 Video2World 中使用的条件注入方式：生成序列的初始帧被条件帧稳定替换，以保持输入视觉线索。
- **Boundary conditions**: 它不是 Text2World 的必要机制，也不是动作条件生成中的 action embedder；它只描述参考帧如何约束生成序列开头。
- **Related concepts**: ['Image2World', 'Video2World', 'temporal consistency', 'conditional inputs']

## Cosmos-Reason1 text encoder
- **Notation**: Cosmos-Reason1
- **Definition**: Cosmos-Reason1 在本文中作为 Cosmos-Predict2.5 的文本编码器，替换 Cosmos-Predict1 使用的 T5 encoder，并通过多层激活拼接与投影形成文本 embedding。
- **Boundary conditions**: 本文只把 Cosmos-Reason1 的视觉输入能力作为未来探索方向；不要把它误写成本文已经用于图像或视频条件编码的组件。
- **Related concepts**: ['Cosmos-Predict2.5', 'cross-attention', 'text grounding', 'Physical AI']

## Cosmos-Transfer2.5
- **Notation**: Cosmos-Transfer2.5
- **Definition**: Cosmos-Transfer2.5 是基于 Cosmos-Predict2.5 扩展出的 control-net style 框架，用于 Sim2Real 和 Real2Real world translation，可接受 edge、blur、segmentation、depth 等空间控制输入。
- **Boundary conditions**: 它不是单纯的文本到视频模型；其核心差异是控制分支和空间控制模态，且不同于 Cosmos-Predict2.5 的基础预测模型定位。
- **Related concepts**: ['Cosmos-Predict2.5', 'control branch', 'Sim2Real', 'Real2Real', 'world scenario map']

## world scenario map
- **Notation**: world scenario map
- **Definition**: world scenario map 是 Cosmos-Transfer2.5-2B/auto/multiview 中用于自动驾驶仿真的控制输入，把 HD maps 和动态对象投影到多相机视图中。
- **Boundary conditions**: 它不是真实视频本身，也不是通用控制模态；本文将它限定在自动驾驶多视角控制生成场景中。
- **Related concepts**: ['Cosmos-Transfer2.5-2B/auto/multiview', 'multi-view generation', 'HD maps', 'dynamic 3D bounding boxes']

## model merging
- **Notation**: model soup / TIES / DARE-Linear / DARE-TIES
- **Definition**: model merging 是本文 post-training 阶段用于合并 domain-specific SFT models 与 cooldown model 优势的方法，候选方法包括 model soup、TIES、DARE-Linear 和 DARE-TIES。
- **Boundary conditions**: 它不是从头联合训练所有域；论文明确说明单独 domain-specific SFT 可避免混合比例平衡问题，合并用于缓解一般域退化。
- **Related concepts**: ['SFT', 'cooldown stage', 'post-trained model', 'human preference voting']

## RL post-training
- **Notation**: VideoAlign / GRPO / denoising trajectories
- **Definition**: RL post-training 是本文在合并模型上进一步提升生成质量的强化学习后训练流程，把条件视为 states，把整个 denoising trajectories 视为 actions，并用 VideoAlign 奖励模型评价输出。
- **Boundary conditions**: 论文没有把推理时控制信号写入新的训练目标；RL 描述的是后训练优化机制，不应与 flow matching 的基础 MSE 损失混同。
- **Related concepts**: ['Cosmos-Predict2.5-2B', 'reward model', 'text alignment', 'motion quality', 'visual quality']

## timestep distillation
- **Notation**: rCM
- **Definition**: timestep distillation 是本文用于加速 diffusion-based world generation 推理的蒸馏过程，采用 rCM hybrid forward-reverse joint distillation 框架。
- **Boundary conditions**: 它服务于推理加速，不是数据过滤、SFT 或 RL post-training 的替代方案。
- **Related concepts**: ['Cosmos-Predict2.5-2B', 'inference acceleration', 'continuous-time consistency distillation', 'distribution matching distillation']

## camera-controllable multi-view generation
- **Notation**: Plücker raymaps
- **Definition**: camera-controllable multi-view generation 是本文面向机器人操控的多视角生成能力：给定参考视角视频和目标 camera trajectories，合成多个目标视角视频。
- **Boundary conditions**: 它不是简单的视频超分或单视角续写；关键条件是相机内外参定义的轨迹，并且论文用 raymap token 将相机姿态注入 DiT。
- **Related concepts**: ['Cosmos-Transfer2.5-2B/robot/multiview', 'camera trajectories', 'cross-view consistency', 'Sampson error']

## action-conditioned world generation
- **Notation**: Cosmos-Predict2.5-2B/robot/action-cond
- **Definition**: action-conditioned world generation 是将 Cosmos-Predict2.5 扩展为根据单张条件图像和机器人动作序列生成未来视频块的能力。
- **Boundary conditions**: 它不是纯视频生成，也不是从视频中反推动作；本文明确输入包含条件图像和动作序列，输出是未来视频帧。
- **Related concepts**: ['action embedder MLP', 'autoregressive generation', 'Bridge dataset', 'policy evaluation']
