# Problem Specification

## Observations

### O1: AV 世界模型需要在不真实执行动作的情况下预测未来驾驶场景，因此必须同时利用当前
- **Statement**: AV 世界模型需要在不真实执行动作的情况下预测未来驾驶场景，因此必须同时利用当前视觉状态和 ego-actions。
- **Evidence**: 论文在 Introduction 中说明输入为当前前视相机帧的 Stable-Diffusion-VAE latent 与 logged ego-actions，输出未来场景 latent 并由冻结 VAE decoder 渲染。
- **Implication**: 问题不是单纯图像生成，而是带动作条件的未来场景建模。

### O2: 选择 latent 表示会显著影响动作预测和后续世界模型质量。
- **Statement**: 选择 latent 表示会显著影响动作预测和后续世界模型质量。
- **Evidence**: 论文用六种冻结编码器做系统 benchmark，并指出 V-JEPA2 的 temporal context 明显优于 single-frame alternatives。
- **Implication**: 在建模前先定位可预测的表示空间是必要步骤。

### O3: 仅看 CosSim、SSIM、L2 等失真指标会把模糊回归均值误判为更好。
- **Statement**: 仅看 CosSim、SSIM、L2 等失真指标会把模糊回归均值误判为更好。
- **Evidence**: 论文在 Perception-Distortion Frontier 中说明 direct regressor wins every distortion metric，但 diffusion model wins every distribution metric。
- **Implication**: AV latent prediction 若只用失真指标，会低估生成式世界模型的真实感。

### O4: 单次 rollout 的时间运动不足主要来自 shared-present an
- **Statement**: 单次 rollout 的时间运动不足主要来自 shared-present anchoring，而不是单纯容量不足。
- **Evidence**: 论文在 Motion 部分将 limited coherent scene motion 追踪到每个未来 token 都从同一个 z_t 计算 delta，并用 jump model 的 re-anchoring 验证。
- **Implication**: 改动参数化和推理链式锚定，比单纯加损失更直接地缓解运动累积问题。

## Gaps

### G1: 紧凑 pooled latent 中直接套用 DiT 并不自动优于 MLP。
- **Statement**: 紧凑 pooled latent 中直接套用 DiT 并不自动优于 MLP。
- **Caused by**: 紧凑 latent、目标函数选择和缺失空间结构共同限制了 DiT 的优势。
- **Existing attempts**: ['capacity 假设被拒绝', 'objective 假设被确认', '恢复 spatial tokens', '加入 residual anchoring', '让 sampling 匹配 target uncertainty']
- **Why they fail**: 论文诊断显示 DiT-direct 可匹配 MLP，说明架构本身不是瓶颈；epsilon 预测在该 regime 会 collapse to near-copy。

### G2: 点估计损失下的 deterministic regressor 会产生条件均值式
- **Statement**: 点估计损失下的 deterministic regressor 会产生条件均值式模糊。
- **Caused by**: 失真指标鼓励逐样本接近 ground truth，而不是匹配真实帧分布。
- **Existing attempts**: ['引入 FID 和 KID 作为 distribution metrics', '使用 train-derived calibration', '比较 direct、diffusion 和 latent interpolation 的 frontier']
- **Why they fail**: appearance ambiguity under point losses 使回归模型优化失真指标时牺牲清晰结构。

### G3: 单次 AnchoredVAEDiT rollout 难以累积多步前向运动。
- **Statement**: 单次 AnchoredVAEDiT rollout 难以累积多步前向运动。
- **Caused by**: 训练和推理参数化把未来步统一锚定到同一 z_t。
- **Existing attempts**: ['加入 temporal-difference loss 但未改善', '改为 Δt jump 预测', '推理时 open-loop chain 并在自身输出上 re-anchor']
- **Why they fail**: 每个未来 token 都共享当前 present anchor，模型倾向重新渲染当前布局而不是随 ego-motion 推进。

## Key Insight
- **Insight**: 本文的 framing 是：紧凑 AV 世界模型的成败不只取决于是否使用 DiT，而取决于 latent 表示、预测目标、锚定方式和评价指标是否与生成式未来预测的问题匹配。
- **Derived from**: encoder benchmark、DiT diagnosis、perception-distortion frontier、motion fidelity diagnostic 的联合结果。
- **Enables**: 把 blurry regression mean、diffusion realism、action controllability 和 motion re-anchoring 组织成一个可诊断、可扩展的设计路线。

## Assumptions
- 冻结 SD-VAE latent 能承载足够的前视驾驶场景信息。
- logged ego-actions 对未来场景变化有可学习的条件作用。
- KID 和 FID 比单纯失真指标更适合评价未来帧分布真实感。
- 紧凑规模下得到的设计原则可作为更大模型的诊断线索，但论文也承认 scale 是主要外部有效性限制。
