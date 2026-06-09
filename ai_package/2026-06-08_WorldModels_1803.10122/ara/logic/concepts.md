# Concepts

## 世界模型 (World Model)
- **Notation**: Agent = V ⊕ M ⊕ C；整体系统通过 rollout 产生累积奖励
- **Definition**: 智能体对环境的生成式神经网络内部模型，以无监督方式快速训练，同时学习环境的压缩空间表示与时间表示。世界模型由视觉组件 V、记忆组件 M、控制器组件 C 三部分组成，共同构成可完整替代真实环境的虚拟仿真器。
- **Boundary conditions**: 本文仅展示单次迭代即可解决较简单任务的情形；对于更复杂任务，论文指出需要迭代训练流程，但相应实验留待未来工作。
- **Related concepts**: ['VAE (V模型)', 'MDN-RNN (M模型)', '控制器 (C模型)', '梦境训练', '温度参数τ']

## VAE V模型 (Variational Autoencoder V Model)
- **Notation**: $z_t \sim N(\mu, \sigma I)$，CarRacing 中 $z \in \mathcal{R}^{32}$，VizDoom 中 $z \in \mathcal{R}^{64}$
- **Definition**: 智能体的视觉感知组件，使用卷积变分自编码器将每帧高维像素图像压缩为低维潜在向量 $z$。编码器将 64×64×3 输入映射到均值 $\mu$ 和标准差 $\sigma$，潜在向量 $z$ 从高斯先验 $N(\mu, \sigma I)$ 中采样；解码器利用反卷积层重建原始图像。训练目标为最小化重建损失（$L^2$ 距离）与 KL 散度之和。
- **Boundary conditions**: V 模型单独训练，不与 M 共同端到端优化（论文提及可以联合训练，但实践中分开训练更高效）；编码对象为单帧静态图像，时序信息依赖 M 模型承载。
- **Related concepts**: ['世界模型 (World Model)', 'MDN-RNN (M模型)', '潜在空间', '梦境训练']

## MDN-RNN M模型 (Mixture Density Network RNN M Model)
- **Notation**: $P(z_{t+1} \mid a_t, z_t, h_t)$，建模为混合高斯；VizDoom 扩展为 $P(z_{t+1}, d_{t+1} \mid a_t, z_t, h_t)$；两任务均使用 5 个高斯混合分量
- **Definition**: 智能体的记忆与预测组件，将 LSTM 与混合密度网络输出层结合，对下一时刻潜在向量 $z_{t+1}$ 的概率分布建模为混合高斯分布，而非确定性预测。输入为当前动作 $a_t$、当前潜在向量 $z_t$ 及 RNN 隐藏状态 $h_t$。在 VizDoom 实验中，M 模型还额外预测智能体是否在下一帧死亡（二值事件 $d_t$）。
- **Boundary conditions**: M 模型不对 $z$ 各维度间的相关参数 $\rho$ 建模，输出对角协方差矩阵的因式化混合高斯分布。LSTM 的有限容量可能导致灾难性遗忘问题，论文提出可用高容量模型或外部记忆模块替换。
- **Related concepts**: ['世界模型 (World Model)', 'VAE (V模型)', '温度参数τ', '对抗性策略问题', '梦境训练']

## 控制器 C模型 (Controller C Model)
- **Notation**: $$a_t = W_c \left[z_t\ h_t\right] + b_c$$
- **Definition**: 智能体的决策组件，设计为极度简洁的单层线性模型，将 V 模型输出的 $z_t$ 与 M 模型隐藏状态 $h_t$ 的拼接向量直接映射到动作 $a_t$。参数量极少（CarRacing 为 867，VizDoom 为 1,088），与 V 和 M 分开独立训练，使用协方差矩阵自适应进化策略 CMA-ES 优化。
- **Boundary conditions**: C 是纯线性模型，不包含隐藏层（论文在消融实验中测试了增加隐藏层的变体）；C 与 V、M 完全分开训练，不进行联合反向传播优化。
- **Related concepts**: ['世界模型 (World Model)', 'VAE (V模型)', 'MDN-RNN (M模型)', 'CMA-ES进化策略']

## 梦境训练 (Dream Training / Latent Space Training)
- **Notation**: 训练发生于 DoomRNN 虚拟环境（纯潜在空间）；策略迁移至实际 DoomTakeCover-v0 评估
- **Definition**: 将控制器完全在世界模型（M模型）生成的幻觉虚拟环境中训练，而非在真实环境中训练的方法。虚拟环境封装为与 OpenAI Gym 接口兼容的 gym.Env，智能体仅在潜在空间中运行，无需渲染真实像素帧或执行真实游戏引擎，训练完成后将策略迁移回真实环境。
- **Boundary conditions**: 梦境训练依赖世界模型的近似质量，若 M 模型覆盖不足，控制器可能发现「对抗性策略」来欺骗模型（即「作弊世界模型」问题）；对于非常简单任务，单次迭代即可，但复杂任务需要多轮迭代训练。
- **Related concepts**: ['世界模型 (World Model)', 'MDN-RNN (M模型)', '温度参数τ', '对抗性策略问题', '迭代训练流程']

## 温度参数τ (Temperature Parameter τ)
- **Notation**: τ ∈ {0.10, 0.50, 1.00, 1.15, 1.30}（论文实验范围）
- **Definition**: MDN-RNN 采样时控制模型不确定性的超参数，通过调整混合高斯分布的采样温度改变虚拟环境的随机程度。τ 较低时近似确定性 LSTM，虚拟环境可预测性高但易被控制器利用（模式坍塌）；τ 较高时虚拟环境更随机难以预测，可防止对抗性策略，但过高会使虚拟环境对学习过难。
- **Boundary conditions**: τ 是需调优的超参数，不同任务的最优值不同；τ 仅作用于 M 模型的采样过程，属于推理期参数，与训练期损失函数无关。
- **Related concepts**: ['MDN-RNN (M模型)', '梦境训练', '对抗性策略问题']

## 对抗性策略问题 (Adversarial Policy / Cheating the World Model)
- **Notation**: τ 极低时（如 0.1）产生模式坍塌，虚拟得分 ~2086，真实得分 ~193
- **Definition**: 当控制器在世界模型生成的虚拟环境中训练时，若世界模型不够完美，控制器会发现并利用模型的缺陷（如使怪物永远不发射火球、超自然消灭已发射的火球），找到在真实环境中不存在的「作弊」策略，导致虚拟环境中表现良好但迁移到真实环境时彻底失败。
- **Boundary conditions**: 完全消除对抗性策略在近似世界模型框架下极难实现；论文提及贝叶斯模型（如 PILCO）可通过不确定性估计部分缓解，但亦未完全解决。
- **Related concepts**: ['梦境训练', '温度参数τ', 'MDN-RNN (M模型)', '世界模型 (World Model)']

## CMA-ES进化策略 (CMA-ES Evolution Strategy)
- **Notation**: 种群大小 = 64；每个体 rollout 次数 = 16；CarRacing 收敛代数 ~1800
- **Definition**: 协方差矩阵自适应进化策略（Covariance-Matrix Adaptation Evolution Strategy），用于优化控制器 C 参数的黑盒优化算法。在 paper-rolling 实验中，使用种群大小 64，每个智能体执行 16 次不同随机种子的 rollout，适应度值为 16 次随机 rollout 的平均累积奖励。CarRacing 任务在 1800 代后达到平均分 900.46（1024 次 rollout 测试）。
- **Boundary conditions**: CMA-ES 仅适用于参数量极小的控制器（本文最多 1,088 参数）；对于参数量更大的模型，需替换为传统深度强化学习或其他可扩展优化方法。
- **Related concepts**: ['控制器 C模型', '世界模型 (World Model)', '梦境训练']
