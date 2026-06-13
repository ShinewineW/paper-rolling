# Concepts

## IDOL
- **Notation**: IDOL；论文中也写作 $\mathrm { I D O L }$
- **Definition**: 一种面向端到端自动驾驶的 inverse-dynamics-guided future prediction 框架，在 latent BEV space 中把 BEV world model 的未来预测、IDM 的转移解码、轨迹锚点优化和闭环细化连接起来。
- **Boundary conditions**: IDOL 不是单纯预测未来 BEV 状态的方法，也不是只对候选轨迹打分的规划器；其关键边界在于必须利用相邻 latent futures 的转移信息来产生 motion-aware feedback。
- **Related concepts**: ['latent BEV world model', 'IDM', 'closed-loop query refinement', 'trajectory anchors', 'reward model']

## inverse dynamics model
- **Notation**: $$d _ { t } = f _ { \mathrm { i d m } } ( \xi _ { t } , \xi _ { t + 1 } )$$
- **Definition**: 用于从两个相邻状态之间推断能够解释该转移的 latent action 或 motion representation 的模型；在本文中，它作用于相邻 imagined BEV latent states，并输出与规划相关的转移描述。
- **Boundary conditions**: 论文把 inverse dynamics 用作规划细化中的转移到动作语义映射，不把它描述为低层控制器，也不声称直接输出车辆控制指令。
- **Related concepts**: ['IDM', 'spatial dynamics map', 'global dynamics feature', 'latent BEV transition', 'trajectory refinement']

## latent BEV world model
- **Notation**: $$X _ { k } ^ { ( u ) } = [ e _ { k } ^ { ( u ) } , \tilde { B } _ { k } ^ { ( u ) } ]$$；$$\hat { X } _ { k } ^ { ( u + 1 ) } = \mathrm { B E V W o r l d M o d e l } \left( X _ { k } ^ { ( u ) } \right)$$
- **Definition**: 基于 transformer 的 latent world model，接收由 ego query 与 candidate-conditioned BEV features 组成的序列，并滚动预测下一步 ego query 与 imagined latent BEV state。
- **Boundary conditions**: 该概念限定在 latent BEV space 的未来想象，不等同于像素级视频生成，也不单独完成最终轨迹选择。
- **Related concepts**: ['candidate-conditioned BEV features', 'anchor-conditioned ego query', 'imagined latent BEV state', 'IDM']

## trajectory anchors
- **Notation**: $$\mathcal { A } \overset { \cdot } { = } \{ \tau _ { k } \} _ { k = 1 } ^ { K }$$；$$e _ { k } ^ { ( 0 ) } = \phi ( [ z , a _ { k } ] )$$
- **Definition**: 离线维护的候选未来运动词表，每个 anchor 表示一个候选未来 motion，并被编码为 anchor feature 后与 ego-state feature 组合成 candidate-specific planning query。
- **Boundary conditions**: 它不是最终输出轨迹本身；最终轨迹是在 anchor 基础上预测 offset、再经过候选评分排序后确定。
- **Related concepts**: ['anchor-conditioned ego query', 'planning network', 'candidate trajectories', 'reward model']

## anchor-conditioned ego query
- **Notation**: $$e _ { k } ^ { ( 0 ) } = \phi ( [ z , a _ { k } ] ) , \qquad k = 1 , \ldots , K$$
- **Definition**: 由 ego-state feature 与 anchor feature 拼接后映射得到的候选特定规划查询，用作未来想象、闭环细化和后续轨迹预测的中心表示。
- **Boundary conditions**: 该 query 是候选级表示，不是全局唯一的场景表示；不同 anchor 对应不同的候选规划查询。
- **Related concepts**: ['trajectory anchors', 'latent BEV world model', 'closed-loop query refinement', 'planning network']

## candidate-conditioned BEV features
- **Notation**: $\tilde { B } _ { k } ^ { ( u ) }$；$$\{ ( e _ { k } ^ { ( u ) } , \tilde { B } _ { k } ^ { ( u ) } ) \} _ { u = 0 } ^ { U }$$
- **Definition**: 在 rollout step 中把 ego query 注入 latent BEV feature map 后得到的候选条件化 BEV 特征，用于构造 scene feature sequence 并生成候选特定的 latent future trajectory。
- **Boundary conditions**: 它不是原始传感器 BEV 图，也不是语义输出图；它是为候选 rollout 服务的 latent feature representation。
- **Related concepts**: ['latent BEV world model', 'anchor-conditioned ego query', 'imagined latent BEV state', 'IDM']

## IDM spatial dynamics map
- **Notation**: $$S _ { k } ^ { ( u ) } \in \mathbb { R } ^ { H \times W \times C }$$；$$S _ { k } = \frac { 1 } { U } \sum _ { u = 0 } ^ { U - 1 } S _ { k } ^ { ( u ) }$$
- **Definition**: IDM 对相邻 imagined BEV states 解码得到的空间动力学图，保留 latent BEV feature map 中逐位置的 motion variation。
- **Boundary conditions**: 它不是语义 BEV mask，也不是直接的轨迹；其作用是提供空间选择性的转移证据。
- **Related concepts**: ['IDM', 'global dynamics feature', 'spatial cross-attention', 'closed-loop query refinement']

## IDM global dynamics feature
- **Notation**: $$g _ { k } ^ { ( u ) } \in \mathbb { R } ^ { C }$$；$$g _ { k } = \frac { 1 } { U } \sum _ { u = 0 } ^ { U - 1 } g _ { k } ^ { ( u ) }$$
- **Definition**: IDM 对相邻 imagined BEV states 的整体转移进行池化得到的全局动力学特征，用于概括候选未来转移的整体 motion context。
- **Boundary conditions**: 论文明确指出 purely pooled inverse dynamics feature 对规划可能过粗，因此 global dynamics feature 需要与 spatial dynamics map 共同使用，而不是替代空间分支。
- **Related concepts**: ['IDM spatial dynamics map', 'MLN', 'dual-branch fusion', 'closed-loop query refinement']

## closed-loop query refinement
- **Notation**: $$\tilde { e } _ { k } ^ { ( \ell ) } = \mathrm { L N } \Big ( e _ { k , \mathrm { i n } } ^ { ( \ell ) } + \mathrm { C r o s s A t t n } \big ( e _ { k , \mathrm { i n } } ^ { ( \ell ) } , S _ { k } ^ { ( \ell ) } , S _ { k } ^ { ( \ell ) } \big ) \Big )$$；$$\bar { e } _ { k } ^ { ( \ell ) } = \mathrm { M L N _ { i d m } } \left( \tilde { e } _ { k } ^ { ( \ell ) } , g _ { k } ^ { ( \ell ) } \right)$$
- **Definition**: 一种轻量闭环细化过程，先用 IDM 产生的 spatial 和 global dynamics 更新 ego query，再把更新后的 query 用于另一轮 future-aware reasoning，以改善长时域一致性。
- **Boundary conditions**: 它是轻量的 query-level refinement，不是无限迭代过程；论文还通过 re-anchor 到初始 anchor-conditioned query 来抑制 iterative drift。
- **Related concepts**: ['spatial cross-attention', 'MLN', 'IDM spatial dynamics map', 'IDM global dynamics feature', 'planning network']

## dual-branch fusion
- **Notation**: spatial branch: $\mathrm { C r o s s A t t n }$；global branch: $\mathrm { M L N _ { i d m } }$
- **Definition**: 在 inverse-dynamics-guided refinement network 中同时使用 spatial branch 与 global branch 的融合设计：空间分支通过 cross-attention 提取局部转移证据，全局分支通过 MLN 进行整体校准。
- **Boundary conditions**: dual-branch fusion 不是额外的未来预测模型，而是对 IDM 输出如何注入 ego query 的细化机制。
- **Related concepts**: ['IDM spatial dynamics map', 'IDM global dynamics feature', 'closed-loop query refinement']

## planning network
- **Notation**: refined query + trajectory anchors → transformer decoder → MLP head → anchor offsets → reward model ranking
- **Definition**: 在最终细化后接收 refined query，与 trajectory anchors 融合，经 transformer decoder 和 MLP head 为每个 anchor 预测 offset，并由 reward model 对候选轨迹排序选择最终输出。
- **Boundary conditions**: planning network 不负责生成 latent future states；latent future simulation 由 BEV world model 完成，planning network 负责 trajectory offset prediction 与候选选择。
- **Related concepts**: ['closed-loop query refinement', 'trajectory anchors', 'candidate trajectories', 'reward model']

## training objective
- **Notation**: $$\mathcal { L } = \lambda _ { \mathrm { o f f } } \mathcal { L } _ { \mathrm { o f f } } + \lambda _ { \mathrm { o f f - i m } } \mathcal { L } _ { \mathrm { o f f - i m } } + \lambda _ { \mathrm { i m } } \mathcal { L } _ { \mathrm { i m } } + \lambda _ { \mathrm { s i m } } \mathcal { L } _ { \mathrm { s i m } } + \lambda _ { \mathrm { m a p } } \mathcal { L } _ { \mathrm { m a p } }$$
- **Definition**: IDOL 的训练结合 trajectory offset regression、imitation reward supervision、simulator-metric reward supervision 和 BEV semantic supervision，以同时监督轨迹偏移、轨迹排序、仿真指标奖励和 latent scene features。
- **Boundary conditions**: 论文给出的是总损失组合与各项角色，没有在该公式中把推理期的 closed-loop query refinement 写成额外训练目标。
- **Related concepts**: ['trajectory offset loss', 'imitation reward supervision', 'simulator-metric loss', 'BEV semantic supervision', 'reward model']
