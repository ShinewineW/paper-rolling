# Heuristics

## H1: 使用 spatial tokens，而不是只在 pooled latent 上训练 DiT。
- **Rationale**: 论文诊断认为 pooled compact latents 中 DiT 初始不优于 MLP；恢复 spatial tokens 后，DiT 才在 matched-parameter 比较中体现优势。
- **Sensitivity**: 对 latent 表示形态敏感；若只保留 pooled 表示，自注意力难以利用空间结构。
- **Bounds**: 适用于本文的 compact AV latent world model 设置；论文未证明该判断在大规模 video prior 系统中同样成立。
- **Code ref**: [AnchoredVAEDiT]
- **Source**: Methods 的 Latent DiT World-Action Model 与 Experiments 的 DiT diagnosis

## H2: diffusion 训练使用 x0-prediction，而不是 epsilon-prediction。
- **Rationale**: 论文明确诊断 epsilon-prediction 在 compact latent spaces 中导致 near-copy collapse，而 x0-prediction 是关键因素。
- **Sensitivity**: 对 latent 空间紧凑程度与目标不确定性敏感；若目标 posterior 更复杂，采样策略也需要匹配。
- **Bounds**: 只可作为本文诊断出的训练目标选择；不得把推理期 calibration、interpolation 或 DDIM 项合成进训练损失。
- **Code ref**: [L_diff]
- **Source**: Methods 的 Diffusion objective and sampling 与 Experiments 的 Diagnosis

## H3: 用 residual anchoring 让模型预测 future latent 相对 present latent 的 residual。
- **Rationale**: 论文称 anchoring 稳定 early training，并让模型退化为 copying present 而不是 random noise。
- **Sensitivity**: 有利于单次预测稳定性，但对长期 coherent motion 有副作用，因为所有 future tokens 共享同一个 present anchor。
- **Bounds**: 适合 single-pass 模型的稳定训练；对多步运动，论文改用 re-anchoring 的 jump model 缓解。
- **Code ref**: [Residual anchoring]
- **Source**: Methods 的 Residual anchoring 与 Motion diagnosis

## H4: action conditioning 采用 learned Fourier features，并让每个 horizon token 接收不同动作调制。
- **Rationale**: 论文说明 Fourier action embedding 随 horizon 变化，使 adaLN modulation 在每个 prediction step 不同，从而保留 per-step temporal structure。
- **Sensitivity**: 对动作序列组织敏感；若动作被过度池化，可能削弱 self-attention 对逐步动作结构的利用。
- **Bounds**: jump model 中四段动作被 Fourier-embedded and mean-pooled，属于另一个 transition 设定，不能与 single-pass per-token conditioning 混同。
- **Code ref**: [FourierEmbed]
- **Source**: Methods 的 Fourier action embedding 与 Motion Fidelity and the Jump Model

## H5: distribution realism 依赖 train-derived calibration，而不是使用 test statistics。
- **Rationale**: 论文把 per-channel mean and scale shift 只从 training split 估计，并在 test time 应用，以避免 test-time artifact。
- **Sensitivity**: 对 VAE encoder/predictor 引入的 per-channel offset 敏感；如果 offset 不存在或数据分布变化，收益可能变化。
- **Bounds**: calibration 是部署时后处理，不是训练损失，也不是 oracle post-hoc test calibration。
- **Code ref**: [train-derived calibration]
- **Source**: Methods 的 Distribution Metrics and Calibration 与 Perception-Distortion Frontier

## H6: 对长期 motion 使用 chain-anchor jump model，在推理期按跳重新 anchor 到自身输出。
- **Rationale**: 论文诊断 single-pass shared-present anchoring 会偏向重渲染当前布局；jump model 用 open-loop chaining 对齐训练-推理中的运动累积形式。
- **Sensitivity**: 对误差累积敏感；论文也指出 decoded predictions 会随 chain 变得更 blurry。
- **Bounds**: 解决的是 coarse motion direction 与 low-frequency motion，不等于已解决高保真长时外观生成。
- **Code ref**: [Jump DiT]
- **Source**: Methods 的 Chain-anchor jump model 与 Motion: Diagnosis and a Compact Fix
