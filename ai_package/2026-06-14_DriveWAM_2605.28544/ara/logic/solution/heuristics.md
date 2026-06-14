# Heuristics

## H1: Scene-evolving guidance：每个 decision step 让 frozen Qwen3-VL-8B 只读取 causally available 的 latest observation、recent ego trajectory 与 route command，生成当前 chunk 的 guidance。
- **Rationale**: 视频 foundation model 提供 dense dynamic priors，但论文指出它缺少 semantic planning ability；chunk-specific guidance 让 upcoming horizon 获得随 scene context 和 route intent 演化的语义意图。
- **Sensitivity**: 对 prompt、route command 与可见上下文敏感；若 guidance 使用 target chunk observation 会造成 future information leakage。
- **Bounds**: 训练期 guidance texts 预计算并缓存；推理期每个 decision step 查询一次并在所有 denoising steps 复用。
- **Code ref**: [Phi_VLM_g_k]
- **Source**: Sec. 3.2, Appendix B

## H2: Temporally localized guidance injection：为每个 chunk 的 guidance 使用 block-diagonal text mask，使目标 chunk 的 video-action tokens 只 attend 到对应 guidance tokens。
- **Rationale**: 避免 tokens attend 到其他 chunks 的 guidance，尤其是 later decision steps 的 future guidance，从而保持 causal consistency。
- **Sensitivity**: 对 chunk 对齐与 mask 构造敏感；mask 错位会导致 cross-chunk leakage 或语义条件缺失。
- **Bounds**: 仅限制 text guidance attention；论文将其作为 causal teacher-forcing 训练结构的一部分。
- **Code ref**: [block_diagonal_text_mask]
- **Source**: Sec. 3.2, Figure 2

## H3: Noisy-history augmentation：训练中 action 分支使用 clean future video latent，而推理中使用 generated latent，论文采用 noisy-history augmentation 缓解 train-test mismatch。
- **Rationale**: action decoder 被设计为 predicted future 的 inverse-dynamics readout；如果训练只见 clean latent，推理时 generated latent 的误差会传递到 action sampling。
- **Sensitivity**: 对历史噪声分布与生成 latent 误差分布是否匹配敏感；论文未给出更细的噪声日程。
- **Bounds**: 论文只说明使用 noisy-history augmentation，没有给出独立公式。
- **Code ref**: [noisy_history_augmentation]
- **Source**: Sec. 3.1

## H4: Modality-aware memory pools：推理期把 history 拆成 video KV pool 与 action KV pool，而不是单一全局 cache。
- **Rationale**: video tokens 数量更多且编码 scene context，action tokens 更紧凑且编码 ego-motion history；单一全局 cache 可能被 visual tokens 支配并低估 motion context。
- **Sensitivity**: 对 video/action cache budgets 敏感；budget 太小会丢失 prediction-relevant history，太大则长时 rollout 成本上升。
- **Bounds**: 两个 pool 都 bounded，分别满足论文中的 memory budget 约束。
- **Code ref**: [H_k_v_H_k_a]
- **Source**: Sec. 3.3

## H5: Relevance-redundancy retention：当 modality pool 超出预算时，用 attention mass 衡量当前 relevance，用 cached keys 间相似度衡量 redundancy，低 score historical tokens 被驱逐。
- **Rationale**: Driving 中较旧 token 可能仍包含 nearby vehicle motion trend 或 occluded pedestrian evidence，而较新 token 可能只是 repeated static background；按 relevance 与 complementarity 选择比 FIFO 更适合长时 rollout。
- **Sensitivity**: 对 lambda、attention 分布、key similarity 度量和当前 query tokens 敏感；lambda 偏向 relevance 或 redundancy 会改变保留模式。
- **Bounds**: 只在 inference time 应用，training-free，不改变 training objective 或 model parameters。
- **Code ref**: [retention_score_s_j_m]
- **Source**: Sec. 3.3, Eq. 6, Eq. 7, Eq. 8

## H6: Route command construction：Appendix B 在缺少 explicit route annotations 时，从 chunk 内 ego yaw change 构造 straight、left、right coarse command。
- **Rationale**: VLM guidance 需要 high-level route intent，但 command 只提供 directional intent，不包含 future positions、velocities、distances 或 trajectory coordinates。
- **Sensitivity**: 对 yaw-change threshold 与 ego pose 标注质量敏感；边界附近的转向可能被粗分类。
- **Bounds**: 仅用于 labeling purposes 生成 coarse command；论文强调不含低层轨迹值。
- **Code ref**: [route_command_from_yaw_change]
- **Source**: Appendix B
