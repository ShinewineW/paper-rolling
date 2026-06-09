# Concepts

## 世界行动模型 (World Action Models, WAMs)
- **Notation**: 主流 WAM 的「想象后执行」分解：$$p ( a _ { 1 : H } \mid o , l ) = \int p ( v _ { 1 : T } \mid o , l ) p ( a _ { 1 : H } \mid o , l , v _ { 1 : T } ) d v _ { 1 : T }$$
- **Definition**: 将未来视觉预测与动作建模统一在一个框架内的具身控制模型，通过对视觉观察在行动下的演化进行建模来增强策略能力。与标准视觉-语言-行动 (VLA) 模型相比，WAM 显式对物理世界在交互下如何演变进行建模。
- **Boundary conditions**: 论文特指结合视觉预测与动作建模的统一框架，不包括仅使用静态图文数据预训练、不显式对物理世界建模的标准 VLA 策略。
- **Related concepts**: ['想象后执行范式', '视频协同训练', 'Fast-WAM', 'VLA 策略']

## 想象后执行范式 (imagine-then-execute paradigm)
- **Notation**: $$p ( a _ { 1 : H } \mid o , l ) = \int p ( v _ { 1 : T } \mid o , l ) p ( a _ { 1 : H } \mid o , l , v _ { 1 : T } ) d v _ { 1 : T }$$
- **Definition**: WAM 中的主流推理设计：模型首先通过迭代视频去噪生成未来视觉观测 $v_{1:T}$，再以想象的未来为条件预测动作。现有大多数 WAM 遵循此范式，包括联合去噪型 (Joint) 与串行生成-再预测型 (IDM) 两类变体。
- **Boundary conditions**: 论文聚焦于单动作块生成并省略外部自回归循环；此范式的核心特征是「测试时确实执行未来视频去噪」，与 Fast-WAM「训练保留视频目标、推理跳过未来生成」的设计形成对比。
- **Related concepts**: ['WAMs', 'Fast-WAM-Joint', 'Fast-WAM-IDM', '视频协同训练']

## 视频协同训练 (video co-training)
- **Notation**: $$\mathcal{L} = \mathcal{L} _ { \mathrm { act } } + \lambda \mathcal{L} _ { \mathrm { vid } }$$
其中 $\mathcal{L}_{vid} = \mathcal{L}_{FM}(z_{1:T})$，$\lambda$ 平衡动作学习与视频协同训练。
- **Definition**: 在训练阶段将视频预测目标与动作预测目标联合优化的训练策略。以未来视频帧的潜在 token $z_{1:T}$ 为目标，通过流匹配损失 $\mathcal{L}_{vid}$ 塑造视频骨干编码具有物理意义的运动与交互结构的能力。
- **Boundary conditions**: 仅指训练阶段以未来视频 latent 为目标的辅助损失；推理阶段 Fast-WAM 完全跳过未来视频生成，视频协同训练的收益通过潜在世界表征体现。
- **Related concepts**: ['流匹配目标', 'WAMs', 'Fast-WAM', '潜在世界表征']

## 混合专家 Transformer 架构 (Mixture-of-Transformer, MoT)
- **Notation**: 动作专家隐藏维度 $d _ { a } = 1 0 2 4$；总模型参数约 6B（视频 DiT 约 5B + 动作专家约 1B）
- **Definition**: Fast-WAM 所采用的双分支架构，由一个视频扩散 Transformer (DiT) 分支和一个动作专家 DiT 分支组成，两者通过共享注意力机制连接。视频分支复用 Wan2.2-5B 预训练权重，动作专家使用缩减的隐藏维度 $d_a = 1024$，形成约 1B 参数的动作专家和 6B 参数的总模型。
- **Boundary conditions**: 论文所述 MoT 特指视频与动作双分支 DiT 结构，区别于一般专家混合 (MoE) 架构。动作专家与视频 DiT 架构相同但隐藏维度缩减，两者通过共享注意力而非路由机制协作。
- **Related concepts**: ['视频 DiT', '结构化注意力掩码', 'Fast-WAM', 'Wan2.2-5B']

## 流匹配目标 (Flow Matching Objective)
- **Notation**: 插值样本：$$y _ { t } = ( 1 - t ) y + t \epsilon$$
流匹配损失：$$\mathcal { L } _ { \mathrm { F M } } ( y ) = \mathbb { E } _ { y , \epsilon , t } \left[ \| f _ { \theta } ( y _ { t } , t , o , l ) - ( \epsilon - y ) \| _ { 2 } ^ { 2 } \right]$$
动作损失：$$\mathcal { L } _ { \mathrm { a c t } } = \mathcal { L } _ { \mathrm { F M } } ( a _ { 1 : H } )$$
视频损失：$$\mathcal { L } _ { \mathrm { v i d } } = \mathcal { L } _ { \mathrm { F M } } ( z _ { 1 : T } )$$
- **Definition**: Fast-WAM 同时用于动作生成和视频协同训练的生成建模目标。对目标变量 $y$（动作块或未来视频 latent）在插值轨迹上预测速度场，训练时从 Gaussian 噪声 $\epsilon$ 和时间步 $t$ 构建插值样本 $y_t$，再用 $L_2$ 损失监督模型的速度场预测。
- **Boundary conditions**: 论文采用流匹配而非 DDPM 扩散形式；$\mathcal{L}_{FM}$ 中的速度场目标为 $(\epsilon - y)$，$y_t$ 为线性插值构造，时间步 $t \in (0,1)$。
- **Related concepts**: ['视频协同训练', 'Wan2.2-5B', 'logit-normal 噪声调度', 'MoT架构']

## 结构化注意力掩码 (structured attention mask)
- **Notation**: 无显式公式；参见论文 Figure 2b 所示的训练与推理掩码矩阵。
- **Definition**: Fast-WAM 中控制三类 token（干净第一帧 latent token、未来噪声视频 token、动作 token）之间信息流的掩码方案。核心设计原则是：动作 token 不能注意未来视频 token；干净第一帧 token 不注意任何其他 token；两类生成 token 各自在分支内双向注意，并可访问干净第一帧 token。
- **Boundary conditions**: 此掩码方案仅适用于训练阶段三类 token 间的交互控制；推理时整个未来视频 token 分支被移除，掩码逻辑不再相关。干净第一帧 token 作为视频建模与动作生成的共享视觉锚点，始终保持干净状态。
- **Related concepts**: ['MoT架构', 'Fast-WAM', '视频协同训练', '潜在世界表征']

## 潜在世界表征 (latent world representation)
- **Notation**: $$p _ { \theta } ( a _ { 1 : H } \mid o , l ) = p _ { \theta } ( a _ { 1 : H } \mid z ( o , l ) )$$
- **Definition**: 由视频 DiT 骨干网络对当前观测进行单次前向传播所产生的潜在特征 $z(o,l)$，用于参数化动作分布而无需显式合成未来帧。Fast-WAM 在推理时仅保留干净第一帧 latent token 通过视频主干进行一次前向传播，以所得表征驱动动作去噪。
- **Boundary conditions**: $z(o,l)$ 由单次编码前向传播获得，区别于「想象后执行」范式中通过显式采样或去噪未来观测 $v_{1:T}$ 所得的未来条件表征。潜在表征由 Wan2.2-5B 的预训练视频 VAE 编码视觉输入，再经视频 DiT 处理获得。
- **Related concepts**: ['视频协同训练', 'MoT架构', '流匹配目标', 'Fast-WAM']
