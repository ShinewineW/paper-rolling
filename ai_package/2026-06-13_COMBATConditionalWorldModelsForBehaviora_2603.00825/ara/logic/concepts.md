# Concepts

## COMBAT
- **Notation**: $P _ { \theta } ( s _ { t + 1 } \mid s _ { t - k : t } , a _ { t - k : t } ^ { ( 1 ) } )$
- **Definition**: COMBAT 是面向 Tekken 3 的条件世界模型，用视频观测学习多智能体环境中的运动动态与对手行为，并在只以 Player 1 输入作为条件时生成后续画面。
- **Boundary conditions**: 它不是显式策略学习器，也不是依赖奖励信号的 RL 方法；论文强调的是通过条件世界建模隐式获得行为。
- **Related concepts**: ['条件视频生成', '部分观测多智能体轨迹', 'Player 1 动作条件', 'Player 2 涌现策略', 'Diffusion Transformer']

## 部分观测多智能体轨迹
- **Notation**: $D = \{ ( s _ { t } , a _ { t } ^ { ( 1 ) } , s _ { t + 1 } ) \} _ { t = 1 } ^ { T }$
- **Definition**: 训练数据被表述为包含当前帧、Player 1 观测动作与下一帧的轨迹，而 Player 2 的动作保持未观测。
- **Boundary conditions**: 它不等同于完整状态动作轨迹；论文明确指出 Player 2 的动作标签不作为训练条件。
- **Related concepts**: ['COMBAT', 'Player 1 动作条件', 'Player 2 涌现策略', '隐式行为学习']

## Player 1 动作条件
- **Notation**: $a _ { t } ^ { ( 1 ) } \in \{ 0 , 1 \} ^ { 8 }$
- **Definition**: Player 1 的输入以 multi-hot 按键向量表示，并与扩散时间嵌入结合，作为 DiT 主干的条件信息。
- **Boundary conditions**: 该条件只覆盖 Player 1；不能把它理解为同时提供了 Player 2 的动作监督。
- **Related concepts**: ['COMBAT', '动作嵌入', '条件向量', 'AdaLNZero', 'Player 2 涌现策略']

## Player 2 涌现策略
- **Notation**: $\pi ^ { ( 2 ) } ( a _ { t } ^ { ( 2 ) } \mid s _ { t } , a _ { t } ^ { ( 1 ) } )$
- **Definition**: Player 2 涌现策略指模型在没有 Player 2 动作标签监督时，通过生成时间一致且可信的多智能体交互，隐式推断出的反应性与战术性行为。
- **Boundary conditions**: 这是论文根据生成行为与评估提出的隐式策略概念，不是一个被单独标注或直接优化的 Player 2 策略网络。
- **Related concepts**: ['部分观测多智能体轨迹', 'COMBAT', '反应式对手行为', '时间一致性', 'TAA', 'ARC']

## Deep Compression AutoEncoder latent
- **Notation**: DCAE latent
- **Definition**: Deep Compression AutoEncoder 用于把 RGB 或 RGB-pose 输入压缩到紧凑潜空间，供后续世界模型在潜空间中生成和去噪。
- **Boundary conditions**: 它负责状态压缩与重建，不直接提供 Player 2 的动作标签或奖励信号。
- **Related concepts**: ['joint RGB-pose representation', 'Diffusion Transformer', 'decoder distillation', 'VAE']

## joint RGB-pose representation
- **Notation**: RGB-pose latent
- **Definition**: joint RGB-pose representation 将视觉帧与姿态关键点放入共享表示空间，用于加强角色运动的结构一致性。
- **Boundary conditions**: 它不是额外的对手策略监督；姿态是状态表示的一部分，而不是 Player 2 决策标签。
- **Related concepts**: ['Deep Compression AutoEncoder latent', 'COMBAT: Pose', '结构一致性', '角色运动']

## autoregressive Diffusion Transformer
- **Notation**: DiT
- **Definition**: autoregressive Diffusion Transformer 是 COMBAT 的生成主干，在潜空间中根据历史状态和 Player 1 条件去噪并预测未来潜帧。
- **Boundary conditions**: 论文未把它描述为传统游戏引擎或显式动力学方程；它通过学习数据分布来生成后续画面。
- **Related concepts**: ['COMBAT', 'AdaLNZero', 'hybrid local-global attention', 'RoPE', 'FlexAttention']

## AdaLNZero conditioning
- **Notation**: AdaLNZero
- **Definition**: AdaLNZero conditioning 是将动作嵌入与扩散时间嵌入形成的条件向量注入 DiT block 的机制。
- **Boundary conditions**: 它是条件注入层，不是独立的评估指标或行为标签来源。
- **Related concepts**: ['Player 1 动作条件', 'Diffusion Transformer', '动作嵌入', '扩散时间嵌入']

## hybrid local-global attention
- **Notation**: local attention + global attention
- **Definition**: hybrid local-global attention 结合 frame-causal local sliding window 与周期性 global attention，用于在长序列中兼顾局部动作连续性和较长程上下文。
- **Boundary conditions**: 它是时空建模策略，不直接定义 Player 2 的战术目标。
- **Related concepts**: ['Diffusion Transformer', 'RoPE', 'FlexAttention', '长程依赖', '时间一致性']

## CausVid DMD step distillation
- **Notation**: DMD, CausVid
- **Definition**: CausVid DMD step distillation 将训练好的 DiT 蒸馏为少步采样器，以减少扩散推理步骤并支持实时交互。
- **Boundary conditions**: 它作用在推理效率上；论文也指出 step distillation 可能损害智能体响应性和攻击频率。
- **Related concepts**: ['real-time inference', 'decoder distillation', 'static key-value caching', 'COMBAT']

## Behavioral Consistency Metrics
- **Notation**: Damage Distribution Analysis, Health Trajectory Analysis
- **Definition**: Behavioral Consistency Metrics 使用游戏内生命值相关信号评估生成序列是否学到规则后果和比赛节奏。
- **Boundary conditions**: 它们评估的是生成 gameplay 的规则与节奏一致性，不直接读取隐藏的真实策略或未观测动作。
- **Related concepts**: ['Damage Distribution Analysis', 'Health Trajectory Analysis', 'Wasserstein distance', 'MSE', 'Player 1', 'Player 2']

## Total Action Adherence
- **Notation**: $$\mathrm { T A A } = \frac { G _ { \mathrm { k i c k s } } + G _ { \mathrm { p u n c h } } } { O _ { \mathrm { k i c k s } } + O _ { \mathrm { p u n c h } } }$$
- **Definition**: Total Action Adherence 衡量生成智能体的进攻动作总量是否接近原始 gameplay 中的人类动作总量。
- **Boundary conditions**: 它只覆盖进攻动作总量，不刻画动作类型比例之外的空间策略、时机质量或胜负目标。
- **Related concepts**: ['ARC', 'human evaluation', 'Player 2 涌现策略', 'offensive actions']

## Action Ratio Consistency
- **Notation**: $$\mathsf { A R C } = \frac { \frac { G _ { \mathrm { p u n c h } } } { G _ { \mathrm { k i c k s } } } } { \frac { O _ { \mathrm { p u n c h } } } { O _ { \mathrm { k i c k s } } } }$$
- **Definition**: Action Ratio Consistency 衡量生成 gameplay 中 punches 与 kicks 的相对比例是否贴近原始 gameplay。
- **Boundary conditions**: 它不衡量视觉质量，也不直接证明策略最优；论文还把它作为未来保持行为保真的潜在优化指标。
- **Related concepts**: ['TAA', 'human evaluation', 'offensive actions', 'Player 2 涌现策略']
