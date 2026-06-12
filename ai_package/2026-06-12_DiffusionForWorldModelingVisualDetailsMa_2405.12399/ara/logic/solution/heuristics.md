# Heuristics

## H1: 采用 EDM 而不是 DDPM 作为 diffusion paradigm。
- **Rationale**: 论文说明 DDPM 在少量 denoising steps 下会出现严重 compounding error，而 EDM 的自适应 signal/noise 目标在长时 rollout 中更稳定。
- **Sensitivity**: 对 denoising steps 很敏感；当 NFE 必须保持较低时，DDPM 更容易漂移出分布，EDM 可在更少步数下保持视觉质量。
- **Bounds**: 论文主文讨论 at most tens of denoising steps 且 preferably fewer；主实验使用 Number of steps 3。
- **Code ref**: [Section 3.1, Section 5.1, Appendix C, Table 3]
- **Source**: EDM formulation、Equation 7、Figure 3 与 Appendix C。

## H2: 训练时从 log-normal distribution 采样噪声水平 sigma。
- **Rationale**: 论文称 Equation 7 在噪声调度两端方差较高，因此按 Karras et al. 的经验分布把训练集中到 medium-noise regions。
- **Sensitivity**: 若采样过多落在极低或极高噪声区域，训练目标方差会变高；若只覆盖中间区域，可能影响极端去噪阶段的泛化。
- **Bounds**: Appendix C 给出 P_mean = -0.4, P_std = 1.2, sigma_data = 0.5。
- **Code ref**: [Appendix C, Algorithm 1 update_diffusion_model]
- **Source**: Equation 13 与 Appendix C。

## H3: 观测条件化使用 frame stacking，动作和 diffusion time 使用 Adaptive Group Normalization。
- **Rationale**: 论文主模型选择标准 U-Net 2D，用最近 L 个过去观测和动作条件化；Appendix M 还指出 frame-stack 在额外视觉质量实验中优于 cross-attention。
- **Sensitivity**: 对历史长度和部分可观测性敏感；历史太短会限制隐状态恢复，cross-attention 并未在文中额外实验中带来优势。
- **Bounds**: 主实验 L 为 4；额外视觉质量实验评估中模型条件化 L = 6 previous real frames。
- **Code ref**: [Section 3.1, Appendix D, Appendix M.2]
- **Source**: Model architectures 与 Table 2。

## H4: 采样器采用 Euler 方法，避免高阶采样器的额外 NFE 和 stochastic sampling 的复杂度。
- **Rationale**: 论文称 Euler’s method 有效，并避免 higher order samplers 的额外 Number of Function Evaluations，也避免 stochastic sampling 的不必要复杂度。
- **Sensitivity**: Euler 步数过少可能造成多模态场景模糊；步数更多改善视觉质量但增加推理成本。
- **Bounds**: 主实验 diffusion sampling method 为 Euler，Number of steps 为 3；CS:GO upsampler 使用 10 denoising steps 而 dynamics model 仍使用 3。
- **Code ref**: [Section 3.1, Table 3, Section 6]
- **Source**: Sampling paragraph、Table 3 与 Section 6。

## H5: 在 imagination 中单独训练 reward/termination model，而不把奖励和终止并入扩散图像模型。
- **Rationale**: 论文把奖励和终止视为 scalar prediction problems，使用 CNN 与 LSTM 处理 partial observability，补全图像世界模型训练 RL 所需的环境接口。
- **Sensitivity**: 奖励和终止错误会直接影响 λ-return 与策略梯度；burn-in 不足时 LSTM 状态可能无法表达部分可观测信息。
- **Bounds**: R_psi burn-in length 实践中设为 L，training sequence length 为 burn-in 加 imagination horizon。
- **Code ref**: [Section 3.2, Appendix D, Algorithm 1 update_reward_end_model]
- **Source**: Reinforcement learning in imagination 与 Algorithm 1。
