## 数据集与切分
- **Value**: nuScenes v1.0-trainval；630 training / 70 validation / 150 test；scene-level split
- **Rationale**: 按 scene 切分避免同一场景进入多个 split，所有指标在 held-out test scenes 上报告。
- **Search range**: 850 driving scenes，33,552 keyframes，2 Hz，约 20 s each
- **Sensitivity**: 高；切分泄漏会直接污染 held-out 评估。
- **Source**: Sec 3 Dataset and Features

## 动作预处理
- **Value**: steering angle 与 acceleration 组成 2D vector，并只用 training-set statistics 做 z-score normalized
- **Rationale**: 动作条件必须在训练统计量下归一化，避免使用验证或测试信息。
- **Search range**: 2D actions：steer, accel
- **Sensitivity**: 中；动作尺度会影响 Fourier action embedding 与 controllability。
- **Source**: Sec 3 Actions

## encoder probe 训练
- **Value**: 2-layer MLP probe，384→256 with GELU→2；Adam；lr $1 0 ^ { - 3 }$；batch 256；50 epochs；3 seeds
- **Rationale**: 统一 probe 让六种 frozen encoder 的比较集中在表征差异，而不是训练头差异。
- **Search range**: 六种 frozen encoders，150 test scenes，bootstrap 95% confidence intervals
- **Sensitivity**: 中；probe 容量与随机种子会影响 RMSE，但实验报告 3 seeds。
- **Source**: Sec 4.1 Encoder Benchmark

## diffusion 训练目标
- **Value**: x_0-prediction objective；cosine schedule；T = 1000 timesteps
- **Rationale**: 诊断显示 epsilon-prediction 在 compact latent spaces 中 collapse，而 x_0 目标恢复大部分 gap。
- **Search range**: epsilon-prediction 到 x_0-prediction
- **Sensitivity**: 高；目标选择是四个必要因素之一。
- **Source**: Sec 4.2 Diffusion objective and sampling；Sec 5.2

## classifier-free guidance 训练 dropout
- **Value**: action dropout p = 0.1，训练时以该概率 zeroing action embedding
- **Rationale**: 用于 classifier-free guidance，使模型学习带动作与无动作条件的路径。
- **Search range**: 论文只报告 p = 0.1
- **Sensitivity**: 中；论文未给出 dropout sweep。
- **Source**: Sec 4.2 Diffusion objective and sampling

## 推理采样
- **Value**: DDIM sampling with 50 deterministic steps，从 pure Gaussian noise refine predictions
- **Rationale**: 采样需要匹配 target uncertainty；论文把 sampling matched to target uncertainty 作为必要因素之一。
- **Search range**: 论文只报告 50 deterministic steps
- **Sensitivity**: 高；采样策略影响 diffusion 输出质量与稳定性。
- **Source**: Sec 4.2；Sec 5.2

## train-derived calibration
- **Value**: per-channel mean and scale shift 在 training split only 估计，test time 应用
- **Rationale**: 修正 VAE encoder/predictor 引入的 perchannel offset，同时避免 test-time statistics。
- **Search range**: train-derived calibration；post-hoc oracle calibration 仅作对照
- **Sensitivity**: 高；论文称该校准解锁 KID advantage 并使结果可部署。
- **Source**: Sec 4.3；Sec 5.3

## EMA regularization
- **Value**: EMA decay 0.999
- **Rationale**: 论文将 EMA 作为 implicit regularization 来缓解 compact model 的 overfitting 风险。
- **Search range**: 论文只报告 decay 0.999
- **Sensitivity**: 中；论文未给出 EMA ablation。
- **Source**: Sec 5.6 Overfitting

## jump model 训练方式
- **Value**: teacher-forced ground-truth anchors；测试时 open-loop chain with model predictions
- **Rationale**: 训练使用 ground-truth anchors，实际 motion fidelity 由开放环自回馈检验。
- **Search range**: 4-step open-loop chain 到 z_{t+16}
- **Sensitivity**: 高；训练-推理对齐是 motion 诊断核心。
- **Source**: Sec 4.4 Motion Fidelity and the Jump Model

## motion-targeted fine-tune
- **Value**: temporal-difference loss fine-tune for 30 epochs 未改善 motion numbers
- **Rationale**: 该负结果支持问题更偏结构性，而不是简单 loss-surface 问题。
- **Search range**: 30 epochs；temporal-difference loss
- **Sensitivity**: 高；它触发从 single-pass anchor 转向 jump reparameterization。
- **Source**: Sec 5.4 Motion
