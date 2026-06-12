# Concepts

## OmniDreams
- **Notation**: 无单独符号；系统包含 OmniDreams-SV 与 OmniDreams-MV 两种变体。
- **Definition**: 面向自动驾驶闭环仿真的 action-conditioned generative world model，从 Cosmos-Predict 2.5 中训练而来，用自回归方式生成由动作、仿真状态和历史画面条件化的相机观测。
- **Boundary conditions**: 论文将其定位为生成式传感器模拟器与可迁移的策略骨干；它不是传统 reconstruction-based neural simulator，也不保证替代物理、交通和控制服务。
- **Related concepts**: ['Cosmos-Predict 2.5', 'AlpaSim', 'Alpamayo 1', 'World-scenario map', 'Streaming KV cache']

## 闭环仿真
- **Notation**: 无固定公式；流程为 policy action 到 simulator state update 到 sensor observations 到下一次 policy action。
- **Definition**: 策略模型在仿真中主动输出动作，仿真器更新世界状态，再把新的传感器观测返回给策略，形成连续交互循环。
- **Boundary conditions**: 闭环仿真依赖外部策略、交通、物理和编排系统；OmniDreams只承担相机观测合成和相关状态维护。
- **Related concepts**: ['AlpaSim', 'OmniDreams', 'Alpamayo 1', 'Pre-fetch generation', 'Session-based state']

## World-scenario map
- **Notation**: 在附录中归入条件 c：辅助条件包括 text caption、first-frame image、HD map control、ego trajectory。
- **Definition**: 由 HD map、车道线、道路边界、交通设施、动态主体 3D bounding boxes 与策略或驾驶动作共同形成的抽象世界状态，用作视频生成的结构化条件。
- **Boundary conditions**: 它不是最终 RGB 图像，也不能单独决定外观；天气、光照和时间等外观属性主要由 text prompt 与视觉历史补充。
- **Related concepts**: ['HD map', 'Abstract world scenario', 'Lightweight control branch', 'Controllable Scenario Editing', 'Out-of-distribution object modeling']

## Autoregressive diffusion video generation
- **Notation**: $p ( \mathbf { x } ^ { 1 : T } ) = \Pi _ { i = 1 } ^ { T } p ( \mathbf { x } ^ { i } | \mathbf { x } ^ { < i } )$；条件因子由 $ { \mathbf { u } } \theta (  { \mathbf { x } } _ { t } ^ { i } |  { \mathbf { x } } ^ { < i } )$ 参数化。
- **Definition**: OmniDreams逐步生成未来短视频块，每一步只依赖过去观测和当前条件，使用 causal diffusion formulation 支持闭环交互。
- **Boundary conditions**: 它不同于一次性生成长片段的 bidirectional video generation；未来帧不能访问未来观测，只能通过当前条件和历史上下文推断。
- **Related concepts**: ['Causal masking', 'Diffusion Forcing', 'Streaming KV cache', 'Chunk-based generation', 'Self Forcing']

## Streaming KV cache
- **Notation**: 论文附录称 KV cache 为 key-value cache；Streaming KV cache 是带固定形状、滚动窗口淘汰并支持 CUDA Graph capture 的有界缓存。
- **Definition**: 自回归 Transformer 中保存过去生成 tokens 的 keys 与 values 的缓存，用于在新帧生成时提供时间上下文并避免重复计算完整历史。
- **Boundary conditions**: 缓存是有界的，论文还需要 local-window attention、attention-sink tokens 与 progressive long-context teacher 来缓解长序列漂移；它本身不等于无限记忆。
- **Related concepts**: ['Local-window attention', 'Attention-sink tokens', 'CUDA Graphs', 'Session-based state', 'Long Rollouts']

## Lightweight control branch
- **Notation**: 无独立公式；属于条件 c 中的 control signals 注入机制。
- **Definition**: 用于把结构化 world-scenario conditioning 注入生成模型的小型控制分支，把控制输入经 MLP 编码为紧凑 control tokens，再与视觉 tokens 对齐并拼接后送入 Transformer。
- **Boundary conditions**: 它不是 ControlNet；论文强调其轻量、与视觉 tokens 分离，但没有把它描述为完整独立生成网络。
- **Related concepts**: ['World-scenario map', 'MLP', 'ControlNet', 'Causal transformer backbone', 'OmniDreams-MV']

## Cross-view attention
- **Notation**: 原文将朴素全注意力复杂度写为 $\mathcal { O } ( N ^ { 2 } T ^ { 2 } )$，并将注意力分解为每视角时间注意力与逐时间步 cross-view attention。
- **Definition**: 多视角生成中在同一时间步跨相机视角应用的注意力，使不同视角 tokens 互相参照以保持共享几何、物体位置和运动一致。
- **Boundary conditions**: 它只在多视角建模中发挥作用；单视角 OmniDreams-SV 不需要跨相机一致性机制。
- **Related concepts**: ['OmniDreams-MV', 'View embedding', 'Temporal attention', 'Multi-View Cross Block', 'Context parallelism']

## Diffusion Forcing
- **Notation**: $\begin{array} { r } { { \bf L } _ { D F } = \mathbb { E } _ { { \bf x } ^ { 1 : T } , \epsilon } \left[ \| { \bf u } \theta ( \mathrm { x } _ { \mathrm { t } } ^ { 1 : T } , \mathrm { t } ) - \mathrm { v } _ { \mathrm { t } } \| ^ { 2 } \right] . } \end{array}\tag{1}$
- **Definition**: 一种训练范式，为序列中的每个 token 分配独立随机噪声水平，使同一模型既能做 next-token predictor，也能做 full-sequence denoiser；本文用它把双向模型转成自回归因果模型。
- **Boundary conditions**: 它不是最终的少步实时推理方案；论文后续还用 Self Forcing 与 DMD 做蒸馏以减少长 rollout 误差和推理步数。
- **Related concepts**: ['Causal masking', 'Autoregressive diffusion video generation', 'Rectified flow', 'RDS', 'RDS-HQ-1M']

## Self Forcing
- **Notation**: 论文描述 self-rollout 使用 ??-step diffusion process，并在实现中给出 ??=2 与 timestep schedule [1000, 450]；反向传播限制在随机采样的 denoising step $s \sim \mathrm { \sigma }$。
- **Definition**: 通过训练时自 rollout，让模型用自己先前生成的帧作为上下文，从而缩小 teacher forcing 与推理时自回归生成之间的分布差异。
- **Boundary conditions**: Self Forcing本身仍可能出现 shifting artifacts；论文进一步用 progressive teacher strategy 缓解长缓存超出短教师上下文后的不稳定。
- **Related concepts**: ['DMD', 'Exposure bias', 'Rolling KV cache', 'Progressive long-context teacher', 'Distillation']

## DMD
- **Notation**: $\begin{array} { r } { \mathcal { L } _ { \mathrm { D M D } } ( \theta ) = \mathbb { E } \left[ \frac { 1 } { 2 } \left| \left| \hat { x } - \mathrm { s g } \left[ \hat { x } - \left( \mathbf { f } _ { \psi } ( \hat { x } _ { t } , t ) - \mathbf { f } _ { \phi } ( \hat { x } _ { t } , t ) \right) \right] \right| \right| ^ { 2 } \right] , } \end{array}\tag{2}$
- **Definition**: Distribution Matching Distillation，是 Self Forcing 蒸馏阶段使用的整体视频级分布匹配目标，通过真实分布得分网络与生成分布得分网络的差异引导生成器。
- **Boundary conditions**: 该目标依赖 frozen real score network 与 learned fake score network；论文没有把它描述为需要成对像素监督的损失。
- **Related concepts**: ['Self Forcing', 'KL', 'Score networks', 'Distillation', 'Real data manifold']

## World-Action Model
- **Notation**: 未来轨迹 latent 写作 $\tau \in \mathbb { R } ^ { 6 4 \times 3 }$；history-token 位置的 DiT 输出 ℎ 被送入 U-Net-shaped MLP 来参数化轨迹 latent 的 flow matching velocity field $ \mathbf { u }$。
- **Definition**: WAM 是一种 video-conditioned policy，将视频输入映射到动作，不显式使用语言模态；本文将 OmniDreams-SV checkpoint 微调为端到端轨迹预测器。
- **Boundary conditions**: WAM 在本文是后训练得到的策略模型，不是 OmniDreams 作为传感器模拟器时的默认闭环渲染组件；其任务不需要 world-scenario map conditioning control。
- **Related concepts**: ['OmniDreams-SV', 'Alpamayo 1.5', 'History token', 'DINOv2', 'Trajectory prediction']

## Diffusion Fixer
- **Notation**: 论文未给出 Diffusion Fixer 的显式损失公式；只说明 denoising process 从 degraded rendering 本身开始，而不是从 random Gaussian noise 开始。
- **Definition**: 把蒸馏后的自回归 OmniDreams checkpoint 后训练为重建伪影校正模块，将 reconstruction-based simulator 的退化渲染映射到干净图像流形，同时保留场景布局、相机视角和驾驶相关结构。
- **Boundary conditions**: 它不是独立构建场景几何的重建方法；输入仍来自已有 reconstruction-based simulator，作用是自回归视觉校正。
- **Related concepts**: ['NuRec', '3D Gaussian Splatting', 'Reconstruction artifact correction', 'Causal history', 'KV-cache conditioning']
