# Heuristics

## H1: 用 Semantic- and Motion-Conditional Normalization 调制历史 BEV embeddings: 先做无仿射 LayerNorm, 再用语义、ego motion 或 agent flow 产生的 scale 与 shift 进行 affine transformation。
- **Rationale**: 原始 BEV embeddings 来自 2D image features, 会出现 ray-shaped patterns, 论文认为这些特征对 semantic occupancy predictions 不够有判别性；语义条件归一化能突出 vehicles、pedestrians、bicycles 等 instance objects, motion 条件归一化补偿 ego vehicle 与 other agents 的运动。
- **Sensitivity**: 对语义标签质量、ego-pose transformation、3D backward centripetal flow 预测质量敏感；消融显示不同条件归一化模式都会带来方向性增益, 其中 ego-motion aware normalization 对未来状态预测尤其重要。
- **Bounds**: 适用于历史 BEV latent space 的归一化与记忆聚合；论文没有给出阈值型超参数边界, 只说明 h、w、c、d 等张量维度含义。
- **Code ref**: [MemoryQueue.semantic_motion_conditional_normalization]
- **Source**: §3.2, §D.2, Table 6

## H2: World Decoder 使用 learnable BEV queries, 依次执行 deformable self-attention、temporal cross-attention、conditional cross-attention 和 feedforward network。
- **Rationale**: deformable self-attention 建立上下文关系；temporal cross-attention 从多帧历史 embeddings 提取对应特征, 并用 ego transformations 计算 reference coordinates 处理时间戳间 misalignment；conditional cross-attention 把动作条件注入 forecasting process。
- **Sensitivity**: 对历史帧数量、memory queue length、action embeddings 和 ego transformation alignment 敏感；输入帧和 memory queue length 增加会带来方向性性能提升, 但历史编码器带来主要 latency。
- **Bounds**: 论文实现中 world decoder consists of three layers, each with 256 channels；空间 BEV queries 设置为 h,w = 200；prediction heads output channels set to 16。
- **Code ref**: [WorldDecoder.forward]
- **Source**: §3.2, §B.1, §C.3, Table 9

## H3: 通过 Unified Conditioning Interface 接收 heterogeneous action conditions, 先用 Fourier embeddings 编码, 再 concatenate 并用 learned projections 对齐到 conditional cross-attention layers。
- **Rationale**: velocity、steering angle、trajectory 和 commands 的格式不同, 统一接口让它们形成 coherent embedding；论文消融认为 cross-attention 比把条件加到 BEV queries 更有效, Fourier embedding 还能提供额外提升。
- **Sensitivity**: 低层动作条件如 trajectory 和 velocity 对 future forecasting 更敏感；高层 commands 更偏向提升当前时刻结果, 对未来预测影响有限。
- **Bounds**: 动作格式限制为论文列出的 velocity、steering angle、trajectory、commands；action-controllable generation 时 P 被丢弃以避免 ego-status leakage。
- **Code ref**: [UnifiedConditioningInterface.encode_actions]
- **Source**: §3.3, §4.2, Table 3, Table 7

## H4: Occupancy-based planner 先采样 guided by high-level commands 的 candidate trajectories, 再用 agent-safety、road-safety 和 learned-volume 三类 cost factor 选择轨迹。
- **Rationale**: agent-safety 避免与 pedestrians 和 vehicles 等 road users 碰撞或过近；road-safety 约束车辆留在 drivable area；learned-volume cost 用 F_{+t}^{bev} 生成 2D cost map, 给复杂环境更完整的评价。
- **Sensitivity**: 对 occupancy predictions 的 agents 与 drivable areas 质量敏感；消融说明每个 cost factor 都有助于 safe planning, 缺少 agent constraints 会导致 collision rate 变差。
- **Bounds**: 候选轨迹为 2D grid map surrounding the ego vehicle 中的 τ_{+t}^*；最终还会经过 BEV Refinement。
- **Code ref**: [OccupancyPlanner.select_lowest_cost_trajectory]
- **Source**: §3.4, Table 8

## H5: 端到端规划训练与测试都使用 predicted trajectories 作为 action conditions, 不使用 GT ego actions 作为 planner 的未来条件输入。
- **Rationale**: 论文明确说这样能防止 GT ego actions leaking into the planner, 同时让模型在训练时学习 predicted trajectories, 以改善测试期表现。
- **Sensitivity**: 对 planner 预测轨迹质量敏感；Table 4 显示使用 GT trajectory 是 planning upper bound, 但 predicted trajectory 可略微改善 occupancy 和 flow forecasting quality。
- **Bounds**: 该规则适用于 end-to-end planning；action-controllable generation 场景单独把 a 作为条件注入 W 并丢弃 P。
- **Code ref**: [DriveOccWorld.rollout_with_predicted_trajectory]
- **Source**: §3.1, §3.4, §4.2, Table 4
