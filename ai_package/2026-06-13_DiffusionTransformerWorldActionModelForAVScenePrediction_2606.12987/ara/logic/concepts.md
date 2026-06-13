# Concepts

## 动作条件世界模型
- **Notation**: z_t, {a_{t+1}, ..., a_{t+H}} -> {z_{t+1}, ..., z_{t+H}}
- **Definition**: 用于 autonomous driving 的未来场景表示预测模型，以当前 front-camera latent 和一段 ego-actions 为条件，输出未来 scene latents，再由冻结 decoder 渲染为帧。
- **Boundary conditions**: 它不等同于闭环驾驶策略，也不直接在环境中执行动作；本文使用 logged ego-actions 和前视相机输入，未覆盖 multicamera 或 predicted actions 的闭环设置。
- **Related concepts**: ['Stable-Diffusion-VAE encode-predict-decode', 'AnchoredVAEDiT', '动作可控性', '多步预测目标']

## Stable-Diffusion-VAE encode-predict-decode
- **Notation**: frame_t -> z_t -> z_hat_{t+k} -> frame_hat_{t+k}
- **Definition**: 一种潜空间工作流：先用冻结 Stable-Diffusion VAE 把 CAM FRONT 图像编码成 latent grid，再在 latent 空间预测未来，最后用冻结 VAE decoder 还原为图像帧。
- **Boundary conditions**: 该概念只描述 VAE latent 管线；它不保证预测天然具备高保真时间运动，本文还单独诊断了 shared-present anchor 带来的 motion 限制。
- **Related concepts**: ['动作条件世界模型', '空间 tokens', '感知-失真前沿', '可部署 train-derived calibration']

## 空间 tokens
- **Notation**: latent grid -> patch tokens -> transformer sequence
- **Definition**: 由 VAE latent grid patchify 得到的空间结构化 token，用于保留图像中的局部空间布局，而不是把帧压成单一 pooled vector。
- **Boundary conditions**: 空间 tokens 是 latent 表示选择，不是新的视觉 encoder；它仍受冻结 VAE 表达能力与单前视相机输入限制。
- **Related concepts**: ['AnchoredVAEDiT', 'x0 预测目标', '残差锚定', 'DiT 诊断四要素']

## AnchoredVAEDiT
- **Notation**: input tokens + c(timestep, z_t, action tokens) -> z_hat_0
- **Definition**: 本文的 latent Diffusion Transformer 世界-动作模型，采用 adaLN-Zero conditioning，把 timestep、present latent 和 per-token Fourier action embedding 作为条件，并预测未来 clean latents。
- **Boundary conditions**: 它不是大规模 video prior 系统；论文强调这是 compact regime 的受控研究，不能直接外推为 GAIA-1 或 Cosmos 规模结论。
- **Related concepts**: ['Stable-Diffusion-VAE encode-predict-decode', 'Fourier action embedding', '残差锚定', 'x0 预测目标']

## x0 预测目标
- **Notation**: z_tilde_tau, c, tau -> z_hat_0
- **Definition**: 扩散训练中直接预测 clean future latent z_0，而不是预测噪声项；论文诊断认为这是 compact latent spaces 中避免 collapse 的关键因素。
- **Boundary conditions**: 该概念只来自本文的 compact latent 诊断；论文没有证明它在所有扩散世界模型或所有视频先验尺度上总是最优。
- **Related concepts**: ['AnchoredVAEDiT', 'DiT 诊断四要素', 'sampling matched to target uncertainty', '残差锚定']

## 残差锚定
- **Notation**: z_hat_{t+k} = z_t + Delta_k(z_t, actions, tau)
- **Definition**: 模型不直接预测绝对未来 latent，而是以当前 latent z_t 为 anchor，预测未来相对当前场景的 residual。
- **Boundary conditions**: 同一个 present anchor 广播到所有未来步会限制 single-pass temporal motion；论文将这种 shared-present anchor 诊断为运动不足的重要原因。
- **Related concepts**: ['AnchoredVAEDiT', '空间 tokens', 'shared-present anchor', 'chain-anchor jump model']

## Fourier action embedding
- **Notation**: a_k = (steer_k, accel_k) -> FourierEmbed(a_k) -> action token conditioning
- **Definition**: 把连续 ego-action 对映射为 learned Fourier features，形成随 horizon 变化的 per-token action conditioning，使不同预测步获得不同动作调制。
- **Boundary conditions**: 它只编码论文使用的 CAN-bus ego-actions；不包含交通参与者行为、地图、语言命令或其他传感器条件。
- **Related concepts**: ['动作条件世界模型', 'AnchoredVAEDiT', '动作可控性', 'per-token action-sequence conditioning']

## 感知-失真前沿
- **Notation**: distortion metrics: CosSim, SSIM; distribution metrics: FID, KID
- **Definition**: 论文用来解释 direct regression 与 diffusion 的评价张力：distortion metrics 偏好模糊的条件均值，而 distribution metrics 更能反映生成帧是否接近真实帧分布。
- **Boundary conditions**: 该前沿是本文在 held-out nuScenes 前视帧和 VAE latent 管线中的经验结果；它不是一个闭环驾驶性能指标。
- **Related concepts**: ['Stable-Diffusion-VAE encode-predict-decode', '可部署 train-derived calibration', 'direct regression baseline', 'Diffusion']

## 可部署 train-derived calibration
- **Notation**: z_hat -> channel-wise calibrated z_hat
- **Definition**: 只用 training split 估计 predicted latents 的 per-channel mean 和 scale shift，并在 test time 应用，以修正 VAE encoder/predictor 引入的小偏移。
- **Boundary conditions**: 它不是 post-hoc test statistics 调参，也不是改变模型结构；只能修正通道级偏移，不能解决所有 appearance fidelity 或 temporal motion 问题。
- **Related concepts**: ['感知-失真前沿', 'Stable-Diffusion-VAE encode-predict-decode', 'FID', 'KID']

## 动作可控性
- **Notation**: steer sweep -> predicted scene shift
- **Definition**: 世界模型的预测应随输入 action 系统性变化；本文通过 steering sweep 和 induced horizontal scene displacement 检查模型是否真正使用动作。
- **Boundary conditions**: 该可控性实验固定 diffusion noise 并在 held-out windows 上进行；它验证 steering 对图像位移的影响，不等同于完整规划闭环成功率。
- **Related concepts**: ['动作条件世界模型', 'Fourier action embedding', 'Diffusion', 'direct regression baseline']

## chain-anchor jump model
- **Notation**: z_{t+4j} = f_theta(z_{t+4(j-1)}, mean action segment)
- **Definition**: 一种 motion-focused reparameterization：模型预测较粗粒度的 latent jump，并在推理时把自己的输出作为下一段 anchor 进行 open-loop chain。
- **Boundary conditions**: jump model 的预测仍然较粗且存在 regression blur；论文将高保真多秒外观留给更大 scale 和更强 temporal supervision。
- **Related concepts**: ['残差锚定', 'shared-present anchor', 'motion fidelity', 'open-loop chain']
