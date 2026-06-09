# Related Work

## R1: Chitta et al. [7] Transfuser
- **DOI**: TPAMI 2022
- **Type**: baseline
- **Delta**:
  - What changed: DiffusionDrive以Transfuser为基础,将其确定性MLP规划头替换为截断扩散解码器,保持相同感知模块和主干网络
  - Why: Transfuser是代表性单模式回归端到端规划方法,作为公平对比的基准
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['ResNet-34主干网络', '感知模块架构', 'BEV特征表示', '训练和推理方案']

## R2: Chen et al. [3] VADv2
- **DOI**: arXiv:2402.13243
- **Type**: comparison
- **Delta**:
  - What changed: DiffusionDrive用仅20个锚点的扩散生成范式替代VADv2的8192锚点大固定词汇表采样范式
  - Why: 大固定词汇表范式受限于词汇表大小和质量,在词汇表外场景失效且计算开销大
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: []

## R3: Li et al. [25] Hydra-MDP
- **DOI**: arXiv:2406.06978
- **Type**: comparison
- **Delta**:
  - What changed: DiffusionDrive不依赖额外规则评分器监督和置信度后处理,依然在PDMS上超越Hydra-MDP-V8192-W-EP
  - Why: Hydra-MDP改进了VADv2的评分机制并代表NAVSIM挑战赛最优方案,是最强竞争基准
- **Claims affected**: ['C2']
- **Adopted elements**: []

## R4: Chi et al. [6] Diffusion Policy
- **DOI**: RSS 2023
- **Type**: method_foundation
- **Delta**:
  - What changed: DiffusionDrive在原始扩散策略基础上引入截断机制和锚定高斯分布,解决直接适配驾驶场景时的模态崩溃和推理效率问题
  - Why: 原始扩散策略在机器人策略学习中表现出色但直接应用于自动驾驶面临20步去噪效率瓶颈和模态崩溃挑战
- **Claims affected**: ['C1']
- **Adopted elements**: ['条件扩散模型基本框架', 'DDIM去噪采样机制']

## R5: Sun et al. [39] SparseDrive
- **DOI**: arXiv:2405.19620
- **Type**: baseline
- **Delta**:
  - What changed: DiffusionDrive在SparseDrive基础上替换规划模块为截断扩散机制用于nuScenes评估
  - Why: SparseDrive提供了高质量稀疏场景表示和感知基础,便于公平比较规划模块的改进效果
- **Claims affected**: ['C4']
- **Adopted elements**: ['两阶段训练协议', '稀疏场景表示', '阶段1感知预训练权重', 'PV特征和地图查询']

## R6: Song et al. [35] DDIM
- **DOI**: ICLR 2021
- **Type**: method_component
- **Delta**:
  - What changed: DiffusionDrive继承DDIM的高效非马尔可夫去噪采样规则,并在截断扩散框架下将推理步数进一步压缩至2步
  - Why: DDIM通过非马尔可夫扩散过程实现比DDPM更少步数的高效采样,是截断框架的基础组件
- **Claims affected**: ['C1']
- **Adopted elements**: ['DDIM更新规则(推理阶段使用)']

## R7: Hu et al. [16] UniAD
- **DOI**: CVPR 2023
- **Type**: comparison
- **Delta**:
  - What changed: DiffusionDrive以生成式扩散模型取代UniAD的单模式确定性规划范式,在相同主干下实现更高PDMS
  - Why: UniAD是端到端自动驾驶领域的开创性工作,通过集成多感知任务提升规划性能,是重要对比基准
- **Claims affected**: ['C2', 'C4']
- **Adopted elements**: []

## R8: Zheng et al. [57] TDPM
- **DOI**: ICLR 2023
- **Type**: related_concept
- **Delta**:
  - What changed: DiffusionDrive引入显式驾驶先验的截断扩散策略,而TDPM从隐式中间分布启动生成用于图像加速;两者均采用截断思想但出发点和目标域不同
  - Why: TDPM提出截断去噪以加速图像生成,与本文截断扩散用于驾驶轨迹的思路有关联但针对不同问题
- **Claims affected**: ['C1']
- **Adopted elements**: []
