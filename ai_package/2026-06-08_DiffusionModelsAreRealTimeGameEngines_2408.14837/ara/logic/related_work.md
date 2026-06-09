# Related Work

## R1: Ha & Schmidhuber (2018)
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: GameNGen 采用潜变量扩散模型替代 VAE+RNN 结构，将视觉质量提升至与原始游戏相当的水平，而非低分辨率抽象表示
  - Why: World Models 是最早用神经网络仿真 DOOM 的工作之一，也是论文可视化对比的直接前驱，但受限于视觉质量和复杂度
- **Claims affected**: ['C1']
- **Adopted elements**: []

## R2: Kim et al. (2020)
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: GameNGen 用扩散模型替代 LSTM+卷积解码器+对抗训练目标，实现更高视觉保真度和实时交互速度
  - Why: GameGAN 是神经网络仿真 DOOM 的直接先驱，论文与之进行了可视化质量对比（图 2）
- **Claims affected**: ['C1']
- **Adopted elements**: []

## R3: Rombach et al. (2022)
- **DOI**: 
- **Type**: foundation
- **Delta**:
  - What changed: GameNGen 在 Stable Diffusion v1.4 基础上改造：去除文本条件，添加动作嵌入交叉注意力和历史帧潜变量拼接条件，并微调解码器，实现游戏仿真
  - Why: Stable Diffusion v1.4 是 GameNGen 的预训练基础模型，其潜变量扩散架构（U-Net + 自编码器）是整个系统的核心
- **Claims affected**: ['C1', 'C3', 'C4']
- **Adopted elements**: ['潜变量自编码器（8x8 像素块压缩为 4 个潜变量通道）', 'U-Net 去噪骨干', '线性噪声调度 $\\bar{\\alpha}_t$']

## R4: Ho et al. (2021)
- **DOI**: 
- **Type**: technique
- **Delta**:
  - What changed: GameNGen 将噪声增强思想适配至历史上下文帧上，以解决自回归游戏仿真中的分布偏移漂移问题
  - Why: 噪声增强的核心思路（对条件帧加噪并提供噪声级别作为输入）来源于 Ho et al. 的级联扩散模型工作
- **Claims affected**: ['C2']
- **Adopted elements**: ['上下文帧高斯噪声增强（可变噪声量，噪声级别作为模型输入）']

## R5: Song et al. (2020)
- **DOI**: 
- **Type**: technique
- **Delta**:
  - What changed: GameNGen 发现 DDIM 在游戏仿真场景中仅需 4 步即可达到高质量，远少于图像/视频生成任务所需步数
  - Why: DDIM 是 GameNGen 推理阶段采用的采样方法，其高效性对实现 20 FPS 实时推理至关重要
- **Claims affected**: ['C3']
- **Adopted elements**: ['DDIM 采样（4 步）']

## R6: Salimans & Ho (2022)
- **DOI**: 
- **Type**: technique
- **Delta**:
  - What changed: GameNGen 采用 velocity 参数化作为训练目标，并参考渐进蒸馏思路实验了单步蒸馏模型（可达 50 FPS）
  - Why: velocity 参数化用于 GameNGen 的训练损失；蒸馏技术参考了该工作的框架
- **Claims affected**: ['C3']
- **Adopted elements**: ["velocity 参数化损失 $$\\mathcal{L} = \\mathbb{E}_{t,\\epsilon,T}\\left[||v(\\epsilon,x_0,t)-v_{\\theta'}(x_t,t,\\{\\phi(o_{i<n})\\},\\{A_{emb}(a_{i<n})\\})||_2^2\\right]$$"]

## R7: Ho & Salimans (2022)
- **DOI**: 
- **Type**: technique
- **Delta**:
  - What changed: GameNGen 仅对历史观测条件使用 CFG（权重 1.5），未对动作条件使用 CFG
  - Why: 无分类器引导（CFG）用于 GameNGen 推理阶段以提升历史帧条件生成质量
- **Claims affected**: ['C1']
- **Adopted elements**: ['CFG（仅用于历史观测条件，权重 1.5）']

## R8: Alonso et al. (2024)
- **DOI**: 
- **Type**: concurrent
- **Delta**:
  - What changed: GameNGen 专注于基于预训练 text-to-image 扩散模型的单一复杂游戏高质量实时仿真，而 Alonso et al. 侧重于在 Atari 游戏上迭代训练世界模型与 RL 模型的协同框架
  - Why: 与 GameNGen 同期进行的工作，同样使用扩散世界模型进行游戏仿真，方法互补
- **Claims affected**: ['C1']
- **Adopted elements**: []

## R9: Bruce et al. (2024)
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: GameNGen 采用受监督的显式动作条件化而非无监督动作发现，实现了更高视觉质量的 DOOM 实时仿真
  - Why: Genie 是同类交互式神经仿真相关工作，强调从视频中无监督学习可控动作
- **Claims affected**: ['C1']
- **Adopted elements**: []

## R10: Schulman et al. (2017)
- **DOI**: 
- **Type**: technique
- **Delta**:
  - What changed: GameNGen 使用 PPO 仅用于数据采集阶段（训练 RL 智能体生成多样化轨迹），而非训练最终游戏策略
  - Why: PPO 是训练数据采集智能体的算法基础，是两阶段训练流程的第一阶段核心
- **Claims affected**: ['C5']
- **Adopted elements**: ['PPO 训练框架', 'Stable Baselines 3 基础设施', '8 路并行游戏环境']
