## world model diffusion paradigm
- **Value**: EDM formulation
- **Rationale**: 作者明确选择 Karras et al. (2022) 的 EDM 而非历史上自然的 DDPM 候选,以适应低 NFE 的 world modeling。
- **Search range**: 比较对象包括 DDPM 与 EDM。
- **Sensitivity**: Section 5.1 显示 DDPM 在低 denoising steps 下更容易累积误差,EDM 更稳定。
- **Source**: Sec 3.1; Sec 5.1

## perturbation kernel
- **Value**: Gaussian kernel with f=0 and g(τ)=sqrt(2 dot_sigma(τ) sigma(τ))
- **Rationale**: EDM 设定将 drift 设为零并以 σ(τ) 控制加性高斯扰动。
- **Search range**: 论文用 DDPM appendix 作为替代范式说明。
- **Sensitivity**: 决定训练噪声分布与反向采样动态；与 EDM preconditioning 联动。
- **Source**: Sec 3.1

## network preconditioning
- **Value**: c_in, c_out, c_noise, c_skip from EDM
- **Rationale**: D_theta 被参数化为 noised observation 与 F_theta 预测的加权和,用于保持输入输出方差并调节训练目标。
- **Search range**: 论文给出 Eq 9-Eq 12,未报告替代 preconditioner 搜索。
- **Sensitivity**: Section 5.1 将 EDM 的稳定低步数生成归因于该自适应信号噪声混合目标。
- **Source**: Sec 3.1; Appendix C

## σ_data
- **Value**: 0.5
- **Rationale**: Appendix C 给出 EDM preconditioners 中使用的数据标准差。
- **Search range**: 论文仅给默认值,未报告搜索范围。
- **Sensitivity**: 进入 c_in、c_out 与 c_skip,影响不同噪声水平下的目标缩放。
- **Source**: Appendix C

## noise sampling distribution
- **Value**: log(σ(τ)) ~ N(P_mean, P_std^2), P_mean=-0.4, P_std=1.2
- **Rationale**: 训练时从经验 log-normal 分布采样噪声水平,集中在中等噪声区域。
- **Search range**: 论文引用 Karras et al. (2022),未报告本文内搜索范围。
- **Sensitivity**: 作者指出极端噪声区域目标方差高,该采样分布用于改善训练有效性。
- **Source**: Sec 3.1; Appendix C; Algorithm 1

## diffusion model backbone
- **Value**: standard U-Net 2D
- **Rationale**: F_theta 使用 standard U-Net 2D；主实验 frame-stacking 与 U-Net 2D 兼容。
- **Search range**: Appendix M 对比 frame-stacking 与 cross-attention,并展示 U-Net 3D 作为视频扩散参照。
- **Sensitivity**: Appendix M 中 frame-stacking 在视觉质量上优于 cross-attention,作者认为逐帧直接输入的 inductive bias 适合 autoregressive generation。
- **Source**: Sec 3.1; Appendix D; Appendix M

## observation conditioning
- **Value**: Frame stacking with L=4 for Atari main experiments
- **Rationale**: diffusion model 条件化在过去观测和动作上,主实验使用最后 4 帧与动作。
- **Search range**: Appendix M 的静态 3D 评估使用 L=6 previous real frames。
- **Sensitivity**: 关系到部分可观测环境中的短期记忆；作者在 Limitations 中指出 frame stacking 是最小记忆机制。
- **Source**: Appendix D; Appendix E; Appendix M; Sec 8

## action conditioning
- **Value**: Adaptive Group Normalization
- **Rationale**: 动作通过 U-Net residual blocks 中的 Adaptive Group Normalization 输入。
- **Search range**: 论文未报告其他 action conditioning 搜索。
- **Sensitivity**: 影响 world model 对 agent actions 的遵循程度；论文未单独消融。
- **Source**: Sec 3.1; Appendix D; Table 2

## diffusion time conditioning
- **Value**: Adaptive Group Normalization
- **Rationale**: diffusion time τ 也通过 Adaptive Group Normalization 条件化。
- **Search range**: 论文未报告替代机制。
- **Sensitivity**: 影响不同噪声水平下的去噪行为；论文未单独消融。
- **Source**: Appendix D; Table 2

## diffusion residual blocks layers
- **Value**: [2, 2, 2, 2]
- **Rationale**: Table 2 给出 diffusion model residual blocks 层数配置。
- **Search range**: 论文仅给默认结构。
- **Sensitivity**: 影响 capacity 与计算成本；论文未报告结构消融。
- **Source**: Appendix D Table 2

## diffusion residual blocks channels
- **Value**: [64, 64, 64, 64]
- **Rationale**: Table 2 给出 Atari diffusion model 通道配置。
- **Search range**: CS:GO 扩展实验将 U-Net channels 放大,使参数从 4M 增至 381M,含 upsampler。
- **Sensitivity**: 控制模型容量与速度；CS:GO 部分显示更复杂环境需要放大模型。
- **Source**: Appendix D Table 2; Sec 6

## diffusion residual conditioning dimension
- **Value**: 256
- **Rationale**: Table 2 给出 diffusion residual blocks conditioning dimension。
- **Search range**: 论文仅给默认值。
- **Sensitivity**: 影响 action 与 diffusion time conditioning 的容量；论文未报告消融。
- **Source**: Appendix D Table 2

## sampling method
- **Value**: Euler
- **Rationale**: 作者发现 Euler’s method 有效,避免高阶 sampler 的额外 NFE 与 stochastic sampling 的复杂度。
- **Search range**: 代码支持多种 sampling schemes；Appendix A 提到 Euler、Euler-Maruyama 与 Heun’s method。
- **Sensitivity**: 采样器决定每帧推理成本与截断误差；高阶方法可能降低误差但增加 NFE。
- **Source**: Sec 3.1; Appendix A; Appendix E Table 3

## denoising steps for Atari
- **Value**: 3
- **Rationale**: 作者指出单步在多模态不确定场景中会产生模糊,因此所有主实验使用 n=3。
- **Search range**: Section 5.1 展示 n≤10 的低步数比较；Appendix L 对 n=3 与 n=1 做消融。
- **Sensitivity**: 高度敏感；减少到 1 step 通常降低高表现游戏的整体方向性表现,尤其在 Boxing 这类多模态场景。
- **Source**: Sec 5.2; Appendix E Table 3; Appendix L

## reward/termination model
- **Value**: CNN residual blocks plus LSTM with shared layers and separate heads
- **Rationale**: reward 与 termination 是标量预测问题,作者使用独立模型 R_ψ 并通过 LSTM 处理部分可观测性。
- **Search range**: 论文未报告与 diffusion model 合并的实现,并在 Limitations 中留作未来工作。
- **Sensitivity**: 影响 imagination 中 reward 与 termination 的正确性；合并进 diffusion model 被认为会增加复杂度。
- **Source**: Sec 3.2; Appendix D; Sec 8

## reward/termination residual layers and channels
- **Value**: layers [2, 2, 2, 2], channels [32, 32, 32, 32]
- **Rationale**: Table 2 给出 reward/termination model 的 residual 配置。
- **Search range**: 论文仅给默认结构。
- **Sensitivity**: 影响标量预测容量与计算成本；论文未报告结构消融。
- **Source**: Appendix D Table 2

## reward/termination LSTM dimension
- **Value**: 128
- **Rationale**: Table 2 给出 R_ψ 的 LSTM dimension。
- **Search range**: 论文仅给默认值。
- **Sensitivity**: 关系到 partial observability 下的短期状态建模；论文未报告消融。
- **Source**: Appendix D Table 2

## actor-critic architecture
- **Value**: shared CNN-LSTM with policy and value heads
- **Rationale**: policy π_φ 与 value network V_φ 共享除最后层外的权重,输入帧后经过 convolutional trunk 与 LSTM。
- **Search range**: 论文未报告替代 actor-critic 架构。
- **Sensitivity**: 影响想象训练中的 policy/value 表达；论文主要归因改进来自 world model 而非 agent 组件。
- **Source**: Sec 3.2; Appendix D

## actor-critic residual layers and channels
- **Value**: layers [1, 1, 1, 1], channels [32, 32, 64, 64], LSTM dimension 512
- **Rationale**: Table 2 给出 actor-critic trunk 与 LSTM 配置。
- **Search range**: 论文仅给默认结构。
- **Sensitivity**: 影响 policy/value 容量与训练成本；论文未报告结构消融。
- **Source**: Appendix D Table 2

## Atari observation and action environment
- **Value**: 64×64×3 images, Discrete action space up to 18 actions, frameskip 4, max noop 30, termination on life loss True
- **Rationale**: 表3给出 Atari 环境预处理与动作空间设置。
- **Search range**: 论文主实验使用 Atari 100k benchmark 的 26 games。
- **Sensitivity**: 决定 world model 输入输出维度与 RL 协议；论文未报告这些环境配置的消融。
- **Source**: Appendix E Table 3; Sec 4

## CS:GO scaling model
- **Value**: 56×30 dynamics model plus original-resolution upsampler, 381M parameters including 51M upsampler
- **Rationale**: 为降低成本先降分辨率建模,再用第二个较小 diffusion model 上采样以改善原始分辨率图像。
- **Search range**: Atari model 为 4M parameters；CS:GO 扩展到 381M parameters。
- **Sensitivity**: 更高容量与 upsampler 支持复杂 3D 环境视觉质量,但仍受记忆与数据覆盖限制。
- **Source**: Sec 6

## CS:GO sampling
- **Value**: dynamics model 3 denoising steps, upsampler 10 denoising steps with stochastic sampling
- **Rationale**: 作者增加 upsampler denoising steps 并引入 stochastic sampling,同时保持 dynamics model 不变以平衡视觉质量与推理成本。
- **Search range**: dynamics model 保持 3 steps；upsampler 增至 10 steps。
- **Sensitivity**: 改善生成视觉质量但增加推理成本；最终可在 RTX 3090 上运行 at 10Hz。
- **Source**: Sec 6
