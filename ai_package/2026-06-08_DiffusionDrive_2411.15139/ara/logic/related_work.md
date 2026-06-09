# Related Work

## R1: Chi et al., 2023 - Diffusion Policy [6]
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: 原始论文将扩散模型用于机器人视觉运动策略学习，捕获多模式动作分布；本文将其迁移至端到端自动驾驶，并针对驾驶场景的模式崩塌和实时性问题提出截断扩散策略
  - Why: Diffusion Policy是本文最直接的技术起点，证明了扩散模型捕获多模式动作分布的能力；Transfuser_DP即将其UNet条件扩散头嫁接至Transfuser，构成路线图实验的基准变体
- **Claims affected**: ['C1', 'C3']
- **Adopted elements**: ['条件扩散模型框架（前向扩散过程、反向去噪训练）', 'UNet扩散解码器结构（Transfuser_DP中使用）', 'DDIM推理采样器']

## R2: Song et al., 2021 - DDIM [35]
- **DOI**: 
- **Type**: component
- **Delta**:
  - What changed: DDIM通过非马尔可夫扩散过程实现少步高效图像生成；本文在此基础上进一步截断扩散时间表至仅需2步，并从锚定高斯分布而非纯高斯噪声出发，实现更激进的加速
  - Why: DDIM是实验中原始扩散策略采用的20步采样器，也是截断推理阶段步间更新规则的直接来源
- **Claims affected**: ['C1']
- **Adopted elements**: ['DDIM步间更新规则（推理阶段）', '非马尔可夫扩散采样思路']

## R3: Chen et al., 2024 - VADv2 [3]
- **DOI**: 
- **Type**: comparison
- **Delta**:
  - What changed: VADv2使用8192个固定锚点词汇表离散化动作空间并评分采样；本文仅使用20个K-Means锚点结合扩散生成，将锚点数量减少400倍，并通过扩散模型的分布表达能力覆盖词外场景
  - Why: VADv2是多模态规划的代表性先验工作，也是NAVSIM挑战赛强基线；与其对比直接量化了本文方法在锚点效率与规划质量上的双重优势
- **Claims affected**: ['C2']
- **Adopted elements**: []

## R4: Chitta et al., 2022 - Transfuser [7]
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: Transfuser是单模式确定性端到端规划器（MLP回归头）；本文以其为骨干感知模块，逐步替换规划头为扩散模型，最终形成完整DiffusionDrive系统
  - Why: Transfuser是NAVSIM官方基线，以其作为骨干确保感知模块的公平对齐；路线图实验（Table 2）追踪了从Transfuser到DiffusionDrive每一步改进，清晰量化了各组件的贡献
- **Claims affected**: ['C1', 'C2', 'C3', 'C4']
- **Adopted elements**: ['ResNet-34骨干与感知模块（3D目标检测、BEV语义分割）', 'BEV LiDAR特征表示', '训练/推理流程配置（裁剪下采样前向相机图像+BEV LiDAR）']

## R5: Zheng et al., 2023 - TDPM（截断扩散概率模型）[57]
- **DOI**: 
- **Type**: inspiration
- **Delta**:
  - What changed: TDPM提出从隐式中间分布出发加速图像生成采样；本文针对驾驶场景引入「显式多模式先验」（K-Means锚点构建的锚定高斯分布），将中间起始分布从隐式提升为可解释的多模式驾驶行为先验
  - Why: TDPM是截断扩散思想在图像生成领域的先行工作；本文明确区分了两者——TDPM无显式驾驶先验，本文的截断专为捕获多模式驾驶行为而设计
- **Claims affected**: ['C1']
- **Adopted elements**: ['截断扩散时间表的基本思路']

## R6: Sun et al., 2024 - SparseDrive [39]
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: SparseDrive提出无BEV的稀疏场景表示端到端驾驶框架；本文将其作为nuScenes实验的感知骨干，替换规划模块为截断扩散解码器
  - Why: SparseDrive在nuScenes上是强基线，基于它构建DiffusionDrive验证了截断扩散策略在稀疏PV特征等不同感知架构下的通用性
- **Claims affected**: ['C5']
- **Adopted elements**: ['两阶段训练流程（感知预训练→规划微调）', '阶段1预训练权重（官方开源实现）', 'nuScenes评测配置']

## R7: Li et al., 2024 - Hydra-MDP [25]
- **DOI**: 
- **Type**: comparison
- **Delta**:
  - What changed: Hydra-MDP在VADv2词汇表采样范式上引入多目标蒸馏改进评分机制；其最强变体Hydra-MDP-V8192-W-EP进一步添加规则评分器额外监督和加权置信度后处理；DiffusionDrive无需后处理仍超越该变体1.6 PDMS
  - Why: Hydra-MDP-V8192-W-EP是NAVSIM挑战赛冠军方案，与其对比验证了DiffusionDrive在竞赛级设置下不借助工程后处理的竞争力
- **Claims affected**: ['C2']
- **Adopted elements**: []

## R8: Jiang et al., 2023 - MotionDiffuser [21]
- **DOI**: 
- **Type**: prior_work
- **Delta**:
  - What changed: MotionDiffuser将扩散模型用于多智能体运动预测（依赖感知真值），仅限于交通仿真；本文将扩散模型扩展至端到端自动驾驶，从原始传感器输入直接生成自车规划轨迹，无需感知真值输入
  - Why: MotionDiffuser是扩散模型在交通场景的代表性先行工作，本文明确指出了将其局限于感知真值输入的约束，以此定位本文贡献的新颖性
- **Claims affected**: ['C1']
- **Adopted elements**: []
