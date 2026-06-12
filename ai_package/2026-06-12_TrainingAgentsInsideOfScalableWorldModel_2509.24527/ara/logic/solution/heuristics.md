# Heuristics

## H1: tokenizer 采用 masked autoencoding, 对输入 patch 随机 dropout, 并保留推理时不 dropout 的情形。
- **Rationale**: 论文称该训练改善 dynamics model 生成视频的 spatial consistency。
- **Sensitivity**: mask 太弱可能学不到鲁棒表示, mask 太强可能偏离推理输入分布；论文用随机化覆盖弱到强的遮挡。
- **Bounds**: 遵循论文给出的 dropout 概率分布, 不外推到未报告的遮挡制度。
- **Code ref**: [masked_autoencoding_dropout]
- **Source**: Section 3.1 Causal Tokenizer

## H2: dynamics 用 x-prediction 与 x-space loss, 而不是 v-prediction 作为长视频逐帧生成的主参数化。
- **Rationale**: 论文认为 v-prediction 产生高频输出, 在长 rollout 中细微错误会累积；x-prediction 使任意长度 rollout 质量更好。
- **Sensitivity**: 对长 rollout 与逐帧交互推理敏感；对一次性整块生成的收益不应从本文过度推断。
- **Bounds**: 限定在论文的 shortcut forcing dynamics 与 tokenizer representation 空间内。
- **Code ref**: [x_prediction_x_loss]
- **Source**: Section 3.2 Interactive Dynamics

## H3: ramp loss weight 随 signal level 线性增大, 将容量集中到学习信号更强的项。
- **Rationale**: 论文说明低 signal level 的 flow matching 会退化为预测 dataset mean, bootstrap target 又更确定, 因此需要重权 clean 侧信号。
- **Sensitivity**: 权重过低会浪费容量在低信号项, 过高可能削弱带噪状态覆盖；论文只报告其级联消融中的设置。
- **Bounds**: 使用论文公式 (8) 的范围, 不自行改写为别的 schedule。
- **Code ref**: [ramp_loss_weight]
- **Source**: Section 3.2 Interactive Dynamics

## H4: agent tokens 只能读取其他模态, 其他模态不能反向 attend 到 agent tokens。
- **Rationale**: 论文称这对避免 causal confusion 很关键, 因为 world model 的 future predictions 应只被 actions 直接影响, 不能被 current task 直接影响。
- **Sensitivity**: 若放开反向注意力, dynamics 可能利用 task 泄漏生成未来而非学习 action-conditioned mechanics。
- **Bounds**: 适用于 task-conditioned policy 和 reward heads 插入 dynamics transformer 的阶段。
- **Code ref**: [agent_token_attention_mask]
- **Source**: Section 3.3 Imagination Training

## H5: imagination training 中冻结 transformer, 只更新 policy 与 value heads, 并保留 frozen policy head 作为 behavioral prior。
- **Rationale**: 论文目标是在 learned world model 内改进策略, 同时通过 prior KL 将策略约束在合理行为空间。
- **Sensitivity**: 若同时更新 world model, rollout 分布与奖励模型可能漂移；若 prior 太强, 策略改进受限。
- **Bounds**: 限于论文离线设置中的 policy/value 后训练阶段。
- **Code ref**: [frozen_world_model_behavioral_prior]
- **Source**: Section 3.3 Imagination Training

## H6: efficient transformer 用 space-only 与 time-only attention 分解, temporal attention 间隔使用, 并在 dynamics 中使用 GQA。
- **Rationale**: 论文将这些作为同时提高训练和推理效率、降低 KV cache 带宽压力的架构选择。
- **Sensitivity**: temporal attention 太少可能损害时序一致性, dense long context 又会拖慢交互推理。
- **Bounds**: 限定在 block-causal 2D transformer 与 interleaved generation 设置。
- **Code ref**: [space_time_attention_gqa]
- **Source**: Section 3.4 Efficient Transformer

## H7: 训练 batch length 交替使用 short batches 与 occasional long batches, 后续只用 long batches finetune。
- **Rationale**: 论文称这样让中期指标与生成更能预示最终表现, 并避免模型过拟合总是在 context 起点看到 start frame。
- **Sensitivity**: 若 batch length 不超过 context length, length generalization 会受影响。
- **Bounds**: 遵循论文的 sequence length 训练策略, 不把它泛化为所有视频模型的必需项。
- **Code ref**: [alternating_batch_lengths]
- **Source**: Section 3.4 Efficient Transformer

## H8: 多任务 agent 数据混合使用 uniform sequences 与 relevant sequences, BC loss 只施加于 relevant fraction, dynamics loss 只施加于 uniform sequences。
- **Rationale**: 论文称这样放大 behavior cloning、reward modeling、reinforcement learning 的信号, 同时避免 optimistic generations。
- **Sensitivity**: relevant fraction 太低会削弱稀疏任务信号, dynamics 若在筛选成功片段上训练可能偏乐观。
- **Bounds**: 限于 Offline Diamond Challenge 的实现设置。
- **Code ref**: [uniform_relevant_data_mixture]
- **Source**: Section 4.1 Offline Diamond Challenge
