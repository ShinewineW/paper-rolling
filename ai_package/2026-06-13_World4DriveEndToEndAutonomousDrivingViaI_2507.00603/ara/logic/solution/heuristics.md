# Heuristics

## H1: 用 trajectory vocabulary 的 endpoints 做 k-means，按 left、right、straight 三类命令形成每类 K 个 intention point，再用 sinusoidal position encoding 得到 intention query。
- **Rationale**: 论文将多模态驾驶意图显式绑定到候选轨迹端点，目的是覆盖 possible driving behaviors，并为后续多模态 planning query 提供结构化先验。
- **Sensitivity**: K 过小会压缩候选意图覆盖范围，K 过大可能增加 selector 与 world model 的候选评估负担；论文只给出默认 K 设置，未系统展开主文敏感性。
- **Bounds**: 默认 N is set to 8192, and K is set to 6；命令类型为 left、right、straight。
- **Code ref**: [IntentionEncoder.kmeans_endpoints]
- **Source**: Given a randomly initialized ego query；By default, N is set to 8192, and K is set to 6.<!--ref:57--><!--ref:65-->

## H2: semantic pseudo labels 由 Grouded-SAM 根据 object of interest prompt 生成，并且只保留 high confidence labels。
- **Rationale**: 论文用 open-vocabulary semantic supervision 弥补 raw image latent 缺少 semantic understanding 的问题，同时通过 confidence 过滤减少 incorrect labeling。
- **Sensitivity**: prompt 与置信度筛选会影响 semantic mask 质量；论文未给出阈值，因此实现时应把阈值作为可配置项而不是固定为未声明数值。
- **Bounds**: 仅保留 high confidence labels；未给出具体 confidence threshold。
- **Code ref**: [SemanticUnderstanding.filter_high_confidence]
- **Source**: Given the prompt for the object of interest；we only keep labels with high confidence to reduce incorrect labeling.<!--ref:74--><!--ref:80-->

## H3: depth priors 采用 metric depth model 估计 multi-view depth maps，并以前向投影把每个像素映射到 ego coordinate system 的 p = { x , y , z }。
- **Rationale**: 论文认为 scale-aware depth 能为每个像素提供准确 positional information，从而增强 3D Spatial Encoding 与 end-to-end planning 的空间理解。
- **Sensitivity**: 依赖 depth map 与 camera intrinsic matrix 的一致性；depth 尺度或标定偏差会直接污染 P _ { t } 与 positional embedding。
- **Bounds**: 论文写入的形状包括 D _ { t } \in \mathbb { R } ^ { M \times h \times w } 与 P _ { t } \in \mathbb { R } ^ { M \times h \times w \times 3 }。
- **Code ref**: [SpatialEncoding.forward_project_depth]
- **Source**: we adopt a forward projection approach；through depth maps and the camera intrinsic matrix.<!--ref:82-->

## H4: temporal aggregation 保留 prior timestamp 的 visual feature，并用 CrossAttention 将 historical information 聚合到当前视觉特征中。
- **Rationale**: 论文明确对比 previous work 使用 randomly initialized queries，主张历史特征能让 world latent representations enriched with the temporal context。
- **Sensitivity**: 只显式描述 prior timestamp t - 1；扩展到更长历史窗口属于实现扩展，论文主文未声明。
- **Bounds**: 输入为 \hat { F } _ { t } 与 \hat { F } _ { t - 1 }，输出为 L _ { t }。
- **Code ref**: [TemporalAggregation.cross_attention]
- **Source**: we preserve the visual feature \hat { F } _ { t - 1 }；aggregate historical information into the current visual features.<!--ref:90-->

## H5: 训练期 selector 先计算每个 modality 的 predicted future latent 与 actual future latent 的 feature distance，选择 minimum distance 的 modality j，再用其 latent distance 与 trajectory 做监督。
- **Rationale**: 这种硬选择把 self-supervised future alignment 转成 trajectory selection 信号，并同步提供 ScoreNet 的分类目标。
- **Sensitivity**: 论文说明 employ the MSE loss to compute the latent distance，并提到其他 loss 的 ablation 在 supplementary material；主文未提供其他损失细节。
- **Bounds**: 选择规则是 minimum distance；推理期改为 highest score，不再访问 actual future latent。
- **Code ref**: [WorldModelSelector.argmin_distance]
- **Source**: The modality with the minimum distance is selected；during inference, we directly select the trajectory corresponding to the world model with the highest score.<!--ref:125--><!--ref:133-->
