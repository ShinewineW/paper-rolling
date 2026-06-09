# Related Work

## R1: Schulman et al. 2017 (PPO)
- **DOI**: arXiv:1707.06347
- **Type**: baseline
- **Delta**:
  - What changed: DreamerV3将PPO作为通用基线在所有领域统一比较；PPO本身也使用固定超参数，选用Acme框架实现，在ProcGen上验证与高度调优版本性能相当
  - Why: PPO是强化学习领域最广泛使用的标准算法，代表通用基线的性能上界
- **Claims affected**: ['C1']
- **Adopted elements**: []

## R2: Schrittwieser et al. 2019 (MuZero)
- **DOI**: arXiv:1911.08265
- **Type**: baseline
- **Delta**:
  - What changed: 在Atari（200M步）上与MuZero对比；DreamerV3在使用远少于MuZero计算资源的情况下取得更高性能
  - Why: MuZero是基于规划的世界模型方法，在棋盘游戏和Atari上均有出色表现，代表了专门设计的强基线
- **Claims affected**: ['C1']
- **Adopted elements**: []

## R3: Baker et al. 2022 (VPT)
- **DOI**: arXiv:2206.11795
- **Type**: baseline
- **Delta**:
  - What changed: VPT使用承包商收集的大量人类键鼠数据进行行为克隆预训练，再用强化学习微调以获取钻石，使用720个GPU训练9天；DreamerV3无需任何人类数据，仅用1个GPU训练9天即可从稀疏奖励出发采集到钻石
  - Why: VPT是在Minecraft中获取钻石的主要先前工作，体现了「有人类数据」与「无人类数据」路线的关键对比
- **Claims affected**: ['C2']
- **Adopted elements**: []

## R4: Hafner et al. 2019 (DreamerV1)
- **DOI**: arXiv:1912.01603
- **Type**: predecessor
- **Delta**:
  - What changed: DreamerV1仅限于连续控制任务；DreamerV3通过鲁棒性技术和架构更新将适用范围扩展到包括离散动作、稀疏奖励、视觉输入等多样领域，无需跨领域调整超参数
  - Why: DreamerV1是本工作的直接前身，奠定了「通过潜在表征想象未来来学习行为」的世界模型框架
- **Claims affected**: ['C1', 'C3']
- **Adopted elements**: ['基于潜在想象学习actor-critic行为的框架']

## R5: Hafner et al. 2020 (DreamerV2)
- **DOI**: arXiv:2010.02193
- **Type**: predecessor
- **Delta**:
  - What changed: DreamerV2在Atari上超越人类水平，但在视觉复杂度不同的环境中需要调整表征损失权重；DreamerV3通过将free bits与小表征损失权重结合，消除了这一跨领域超参数依赖
  - Why: DreamerV2是本工作的直接前身，引入了离散世界模型，但尚不支持固定超参数跨领域训练
- **Claims affected**: ['C1', 'C3']
- **Adopted elements**: ['RSSM世界模型结构', '直通梯度的离散类别表征']

## R6: Hafner et al. 2018 (RSSM / PlaNet)
- **DOI**: arXiv:1811.04551
- **Type**: builds_on
- **Delta**:
  - What changed: DreamerV3继续使用Recurrent State-Space Model (RSSM)作为世界模型核心架构，并在其基础上增加鲁棒性技术（归一化、变换等）
  - Why: RSSM提供了世界模型的基础结构（序列模型+编码器+动态预测器+奖励预测器+解码器），是DreamerV3的底层模型框架
- **Claims affected**: ['C3']
- **Adopted elements**: ['RSSM架构（公式1）']

## R7: Ye et al. 2021 (EfficientZero)
- **DOI**: NeurIPS 2021
- **Type**: baseline
- **Delta**:
  - What changed: EfficientZero在Atari100K上通过在线树搜索、优先回放和超参数调度取得最高分，但修改了标准环境配置，使比较困难；DreamerV3在不改变环境配置的情况下超越了其余所有方法
  - Why: EfficientZero是Atari100K上的当时最优方法，是数据效率基准上的重要参考点
- **Claims affected**: ['C1']
- **Adopted elements**: []

## R8: Micheli et al. 2022 (IRIS)
- **DOI**: arXiv:2209.00588
- **Type**: baseline
- **Delta**:
  - What changed: IRIS是基于Transformer的离散世界模型，在Atari100K上gamer均值达到105%；DreamerV3在gamer均值上达到125%，且使用更少计算资源（0.1 GPU天 vs. IRIS的3.5 GPU天）
  - Why: IRIS是Atari100K基准上使用世界模型的强竞争方法
- **Claims affected**: ['C1']
- **Adopted elements**: []

## R9: Cobbe et al. 2021 (PPG)
- **DOI**: ICML 2021
- **Type**: baseline
- **Delta**:
  - What changed: PPG是针对ProcGen调优的专家算法，归一化均值为64.89；DreamerV3以固定超参数在ProcGen归一化均值上达到66.01，与PPG持平
  - Why: PPG是ProcGen基准上公认的调优专家算法，代表该领域专门方法的上界
- **Claims affected**: ['C1']
- **Adopted elements**: []

## R10: Yarats et al. 2021 (DrQ-v2)
- **DOI**: arXiv:2107.09645
- **Type**: baseline
- **Delta**:
  - What changed: DrQ-v2是专为视觉连续控制设计、利用数据增强的无模型算法；DreamerV3在视觉控制套件上以任务均值861超越DrQ-v2的770
  - Why: DrQ-v2是视觉连续控制领域的最强基线之一，代表专门方法的水平
- **Claims affected**: ['C1']
- **Adopted elements**: []

## R11: Reed et al. 2022 (Gato)
- **DOI**: arXiv:2205.06175
- **Type**: competing
- **Delta**:
  - What changed: Gato是大型通用模型，通过拟合多任务专家示范数据实现跨任务学习，但仅在专家数据可得时适用；DreamerV3不需要专家数据，从零开始通过强化学习掌握多样领域
  - Why: Gato代表了「模仿学习」通用智能体范式，论文将DreamerV3与其进行概念对比，强调无需专家数据的优势
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: []
