# Problem Specification

## Observations

### O1: 普通扩散策略（vanilla diffusion policy）直接迁移至自动驾
- **Statement**: 普通扩散策略（vanilla diffusion policy）直接迁移至自动驾驶场景会出现模式崩溃：20个不同随机噪声去噪后收敛到几乎相同的轨迹，多样性极低
- **Evidence**: 论文定义模式多样性分数 D（基于 mIoU），Table 2 显示 Transfuser_DP 的 D 仅为11%，而 DiffusionDrive 达到74%
- **Implication**: 无法为复杂驾驶场景（障碍规避、变道）生成多种合理候选轨迹

### O2: 普通 DDIM 扩散策略推理需要20步去噪，将规划模块帧率从60 FPS 压缩至
- **Statement**: 普通 DDIM 扩散策略推理需要20步去噪，将规划模块帧率从60 FPS 压缩至7 FPS，无法满足实时自动驾驶需求
- **Evidence**: Table 2：Transfuser 规划耗时0.2ms/60FPS，Transfuser_DP 总耗时130.0ms/7FPS
- **Implication**: 重计算开销阻断了扩散模型在在线自动驾驶中的实用化

### O3: 大词汇表离散化范式（VADv2使用8192个锚轨迹）在词汇表外场景会失败，且管理
- **Statement**: 大词汇表离散化范式（VADv2使用8192个锚轨迹）在词汇表外场景会失败，且管理大量锚带来显著计算挑战
- **Evidence**: Introduction 明确指出「fundamentally constrained by the number and quality of anchor trajectories, often failing in out-of-vocabulary scenarios」
- **Implication**: 用固定词汇表覆盖开放世界驾驶空间存在原理性局限

## Gaps

### G1: 单模式回归范式（Transfuser、UniAD、VAD）忽视驾驶行为的固有不确
- **Statement**: 单模式回归范式（Transfuser、UniAD、VAD）忽视驾驶行为的固有不确定性和多模性
- **Caused by**: 基于确定性 MLP 回归的规划头天然只能建模单峰分布
- **Existing attempts**: []
- **Why they fail**: 仅输出单一确定性轨迹，无法覆盖变道、绕障等多种合理决策

### G2: 将机器人扩散策略直接迁移到端到端自动驾驶，无法同时解决模式崩溃和实时性两个问题
- **Statement**: 将机器人扩散策略直接迁移到端到端自动驾驶，无法同时解决模式崩溃和实时性两个问题
- **Caused by**: vanilla diffusion policy 的标准高斯起点与驾驶动作的先验分布之间距离太大
- **Existing attempts**: ['论文构建了 Transfuser_DP 作为基准，验证直接迁移的失败：PDMS 仅提升0.6、多样性仅11%、FPS 从60降至7']
- **Why they fail**: 驾驶场景比机器人操控更动态、更开放，从纯随机高斯噪声出发的去噪路径过长且缺乏驾驶先验，导致多个噪声样本收敛到同一区域

## Key Insight
- **Insight**: 人类驾驶遵循少数固定模式（直行、变道、转弯等），并根据实时交通条件动态调整；将这些先验驾驶模式嵌入扩散策略——以锚定高斯分布取代随机高斯起点——可同时消除模式崩溃并大幅截断去噪步骤数
- **Derived from**: C1、C2 关于普通扩散策略两大缺陷的分析，以及人类驾驶行为服从先验模式的观察
- **Enables**: 用仅20个 K-Means 锚轨迹 + 2步去噪替代8192个固定词汇/20步随机去噪，兼顾多模态质量与实时效率

## Assumptions
- K-Means 聚类产生的少量锚轨迹（20个）足以覆盖驾驶动作空间的主要先验模式
- 截断扩散调度（50/1000 步）形成的锚定高斯分布与真实驾驶轨迹分布之间的距离，可在2步以内的去噪中有效消除
- 不同驾驶场景下同一组锚轨迹的泛化性足够强（Tab. 9 跨数据集实验部分支持此假设，但属于分析推断，论文未显式声明其为充分条件）
