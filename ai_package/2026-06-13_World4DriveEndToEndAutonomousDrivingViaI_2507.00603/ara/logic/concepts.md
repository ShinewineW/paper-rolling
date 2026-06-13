# Concepts

## World4Drive
- **Notation**: 输入包括 multi-view images 与 trajectory vocabulary；核心输出包括 T 与最终选择的 T^j。
- **Definition**: World4Drive 是一个端到端自动驾驶框架，用 vision foundation models 构建 latent world models，用于生成、评估并选择 multi-modal planning trajectories。<!--ref:World4Drive, an endto-end autonomous driving framework-->
- **Boundary conditions**: 本文描述的 World4Drive 不输出显式 perception results；可视化中感知结果来自 ground truth annotations，而不是模型预测。<!--ref:World4Drive does not predict explicit perception results-->
- **Related concepts**: ['Driving World Encoding', 'Intention-aware World Model', 'World Model Selector', 'Physical World Latent Encoding']

## Driving World Encoding
- **Notation**: 模块包含 intention encoder 与 physical latent encoder；输出包括 Q_plan 与 L_t。
- **Definition**: Driving World Encoding 是 World4Drive 的前端编码模块，从 RGB images 和 trajectory vocabulary 中抽取 driving intention 与 physical world latent representations。<!--ref:Driving World Encoding-->
- **Boundary conditions**: 它本身不是最终规划选择器；最终选择由 Intention-aware World Model 与 World Model Selector 完成。<!--ref:scores multi-modal planning trajectories via the world model selector-->
- **Related concepts**: ['Intention Encoder', 'Physical World Latent Encoding', 'World4Drive']

## Intention Encoder
- **Notation**: Q_plan = SelfAttention((Q_ego + Q_I))；trajectory vocabulary 记为 ν̇，intention point 记为 P_I，planning query 记为 Q_plan。
- **Definition**: Intention Encoder 接收 trajectory vocabulary，利用 k-means clustering 在轨迹端点上得到 intention point，并通过 sinusoidal position encoding 与 self-attention 形成 intention-aware multimodal planning query。<!--ref:Intention Encoder-->
- **Boundary conditions**: 它负责表达候选驾驶意图，不直接评估哪条候选轨迹最合理；评分与选择发生在 World Model Selector。<!--ref:evaluate trajectories under K different intentions-->
- **Related concepts**: ['Driving World Encoding', 'trajectory vocabulary', 'Q_plan', 'multi-modal driving intentions']

## Physical World Latent Encoding
- **Notation**: 输入为 I_t 与图像特征 F_t；输出为 L_t。
- **Definition**: Physical World Latent Encoding 用 context encoder 与 temporal aggregation module 提取包含 spatial、semantic 和 temporal 信息的 world latent representations。<!--ref:Physical World Latent Encoding-->
- **Boundary conditions**: 该模块引入 vision-language model 与 metric depth estimation model 的先验，但论文没有把它描述为人工 perception annotation 监督。<!--ref:without perception annotations-->
- **Related concepts**: ['Context Encoder', 'Semantic Understanding', '3D Spatial Encoding', 'Temporal Aggregation']

## Semantic Understanding
- **Notation**: S_t = GroundedSAM(F_t)；语义损失记为 L_sem。
- **Definition**: Semantic Understanding 使用 Grounded-SAM 产生 pseudo semantic labels，并保留 high confidence labels，再用 cross-entropy loss L_sem 增强 latent representations 的语义理解。<!--ref:Semantic Understanding-->
- **Boundary conditions**: 这些标签是 pseudo semantic labels，且论文只说明保留高置信标签以减少错误标注，没有声称其等同于人工真值标注。<!--ref:we only keep labels with high confidence to reduce incorrect labeling-->
- **Related concepts**: ['Physical World Latent Encoding', 'Context Encoder', 'Grounded-SAM', 'L_sem']

## 3D Spatial Encoding
- **Notation**: D_t 表示 depth maps，p = {x, y, z} 表示 ego coordinate system 中的位置，P_t 表示 3D position maps，E_t = MLP(SPE(P_t))。
- **Definition**: 3D Spatial Encoding 使用 metric depth model 估计 multi-view depth maps，再通过相机内参和 forward projection 得到 ego coordinate system 中每个像素的 3D position maps。<!--ref:3D Spatial Encoding-->
- **Boundary conditions**: 它采用 forward projection，不是 PETR 中的 postprojection meshgrid 路径；论文只描述用 metric depth model 估计深度，未把深度估计器训练过程展开。<!--ref:In contrast to PETR, we adopt a forward projection approach-->
- **Related concepts**: ['Physical World Latent Encoding', 'Metric3D v2', 'E_t', 'P_t']

## Temporal Aggregation
- **Notation**: L_t = CrossAttention(F̂_t, F̂_{t-1})。
- **Definition**: Temporal Aggregation 保存上一时刻的 visual feature，并通过 cross-attention 将历史信息聚合到当前 visual features，得到 world latent representations。<!--ref:Temporal Aggregation-->
- **Boundary conditions**: 论文将该模块与 LAW 使用 randomly initialized queries 的做法区分开来；它不负责生成未来 latent，那属于 Intention-aware World Model Prediction。<!--ref:Different from previous work [18] that uses randomly initialized queries-->
- **Related concepts**: ['Physical World Latent Encoding', 'L_t', 'F̂_t']

## Intention-aware World Model
- **Notation**: T = MLP(CrossAttention(Q_plan, L_t))；L_{t+n} = CrossAttention(Q_future, Concat(A, L))。
- **Definition**: Intention-aware World Model 根据 multi-modal driving intentions 预测 future world latents，并通过 selector 对 multi-modal planning trajectories 评分。<!--ref:Intention-aware World Model-->
- **Boundary conditions**: 它预测的是 latent representation of the future world，而不是直接生成未来图像或显式 3D 场景。<!--ref:future world latents-->
- **Related concepts**: ['Action Encoding', 'World Model Selector', 'Q_future', 'A', 'L_{t+n}']

## World Model Selector
- **Notation**: S = Softmax(C(L_{t+n}))；selected modality index 记为 j；最终轨迹记为 T^j。
- **Definition**: World Model Selector 比较每个 predicted intention-aware future latent 与 actual future latent 的 feature distance，选择距离最小的 modality 及其对应轨迹，并训练 ScoreNet 预测各 modality 的分数。<!--ref:World Model Selector-->
- **Boundary conditions**: 训练期的最小 latent distance 选择与推理期的最高 score 选择不同；不能把推理期最高分选择写成训练目标中的距离最小操作。<!--ref:The modality with the minimum distance is selected as the final selected modality-->
- **Related concepts**: ['Intention-aware World Model', 'ScoreNet', 'L_recon', 'L_score', 'T^j']

## Training Loss
- **Notation**: L = α L_sem + β L_recon + γ L_score + η L_traj。
- **Definition**: Training Loss 将 semantic understanding、reconstruction、score prediction 与 trajectory imitation 相关损失组合为端到端训练目标。<!--ref:Training Loss-->
- **Boundary conditions**: 论文显式给出了总损失公式，但没有给出 focal loss 和 MSE distance 的完整展开公式；因此不应自行补写未出现的具体损失表达式。<!--ref:We utilize a focal loss between scores and the selected modality index j-->
- **Related concepts**: ['L_sem', 'L_recon', 'L_score', 'L_traj', 'World Model Selector']
