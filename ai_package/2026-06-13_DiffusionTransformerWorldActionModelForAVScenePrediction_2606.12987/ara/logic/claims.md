# Claims

## C1: V-JEPA2 temporal表征更适合动作预测
- **Statement**: 在冻结视觉编码器基准中，V-JEPA2 rep64利用时间上下文，相比单帧编码器在steering RMSE上表现更好；论文将改进归因于时间视频表征捕获了单帧不可见的帧间ego-motion模式与车道曲率动态。
- **Status**: supported
- **Falsification criteria**: 若在相同split、相同MLP probe和相同scene-level评估下，单帧编码器达到或超过V-JEPA2 rep64的steering RMSE，则该主张被削弱。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 该结果说明，在AV动作预测的上游表征选择中，时间上下文不是附加细节，而是主要信号来源之一。
- **Tags**: ['improvement', 'generalization']

## C2: diffusion在分布指标上优于direct regression
- **Statement**: 在SD-VAE encode-predict-decode管线中，direct regression在CosSim等失真指标上更强，但diffusion经过train-derived calibration后在KID和FID等分布指标上更接近真实帧分布。
- **Status**: supported
- **Falsification criteria**: 若同一held-out test设置下direct regression在KID和FID上不劣于train-calibrated diffusion，或calibration依赖test-time ground truth，则该主张不成立。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 论文把这个现象解释为perception-distortion tradeoff：失真指标会奖励模糊条件均值，而分布指标更能反映生成式世界模型的视觉真实性。
- **Tags**: ['improvement', 'descriptive']

## C3: 共享present anchor限制单次rollout的时间运动
- **Statement**: 论文将single-pass模型的有限coherent motion诊断为shared-present anchoring问题，并用chain-anchor jump model通过逐步re-anchoring恢复更好的前向运动方向与低频运动幅度。
- **Status**: supported
- **Falsification criteria**: 若替换为逐步re-anchoring后motion direction和low-frequency motion不改善，或single-pass模型在相同评估下已能累积足够ego-motion，则该因果诊断被削弱。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 该实验支持结构性解释：问题不只是容量不足，而是训练与推理中的锚点参数化影响了运动累积。
- **Tags**: ['causal', 'improvement']

## C4: diffusion world model具有动作可控性
- **Statement**: steering sweep实验显示，固定diffusion noise时，diffusion模型的steering输入会单调驱动预测场景的水平位移，而direct regression baseline缺少这种相关性。
- **Status**: supported
- **Falsification criteria**: 若在held-out windows上改变steering输入不能产生方向一致的scene displacement，或direct regression呈现同等单调相关性，则该主张不成立。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 这表明模型不只是生成合理外观，还在预测中使用了动作条件；这对planning-relevant world model尤其关键。
- **Tags**: ['causal', 'descriptive']

## C5: compact latent中的DiT需要匹配目标不确定性的设计组合
- **Statement**: 论文的诊断链认为，在compact latent regime中，DiT发挥作用依赖spatial tokens、x0 prediction objective、residual anchoring以及sampling matched to target uncertainty；仅增加capacity或horizon并不能解释收益。
- **Status**: supported
- **Falsification criteria**: 若在缺少这些因素之一时DiT仍稳定超过matched MLP，或epsilon objective在compact latent中不出现collapse，则该设计组合的必要性需要重估。
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: 这是论文对方法边界的主要归纳：DiT优势不是自动来自transformer架构，而来自目标、表征和采样设定的匹配。
- **Tags**: ['scoping', 'causal']
