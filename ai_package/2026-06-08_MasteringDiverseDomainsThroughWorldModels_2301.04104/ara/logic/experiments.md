# Experiments

## E1: 跨8个领域超过150个任务的多基准评测
- **Verifies**: C1
- **Setup**:
  - Model: DreamerV3（200M参数，固定超参数，见Table 4）
  - Hardware: 单块 Nvidia A100 GPU（每个智能体独立训练）
  - Dataset: Atari（57个游戏，200M步）、ProcGen（16个游戏，50M步）、DMLab（30个任务，100M步）、Atari100K（26个游戏，400K步）、BSuite（23个环境，468个配置）、本征控制（18个任务，500K步）、视觉控制（20个任务，1M步）
  - System: 8个领域共超过150个任务；对照PPO（固定超参数，Acme实现）和各领域调优专家算法
- **Procedure**:
  1. 对每个领域遵循标准评测协议（动作重复、步数预算等，见Table 2）
  2. DreamerV3统一使用Table 4所列超参数，不针对任何领域调整
  3. PPO使用固定超参数（Table 1），在ProcGen上验证与原始高度调优版本持平
  4. 与各领域调优专家基线（MuZero、Rainbow、IQN、PPG、R2D2+、IMPALA、EfficientZero、IRIS、TWM、DrQ-v2、D4PG等）进行比较
  5. 报告各领域分数及归一化均值/中位数
- **Metrics**: ['各领域任务得分或归一化比率（gamer mean %、human mean capped %等）', '与调优专家基线的相对性能']
- **Expected outcome**: DreamerV3在大多数领域高于或持平于调优专家基线，并大幅高于固定超参数的PPO
- **Baselines**: ['PPO（固定超参数，Acme实现）', 'MuZero', 'Rainbow', 'IQN', 'PPG', 'R2D2+', 'IMPALA', 'EfficientZero', 'IRIS', 'TWM', 'DrQ-v2', 'CURL', 'D4PG', 'DMPO', 'Boot DQN']
- **Dependencies**: []

## E2: Minecraft钻石采集实验（无人类数据、无课程、稀疏奖励）
- **Verifies**: C2
- **Setup**:
  - Model: DreamerV3（200M参数，默认超参数，开箱即用）
  - Hardware: 单块 Nvidia A100 GPU，64个并行环境实例（远程CPU workers）
  - Dataset: 基于MineRL v0.4.4构建的Minecraft Diamond环境（64×64×3第一人称图像，稀疏奖励，12个里程碑物品）
  - System: episodes最长36000步（约30分钟），100M环境步数预算，10个随机种子；Minecraft版本1.11.2
- **Procedure**:
  1. 在MineRL基础上构建Minecraft Diamond环境并修正原始环境若干问题（早终止条件、跳跃动作持续时长等）
  2. 以稀疏奖励信号（12个里程碑各+1，无人类数据，无自适应课程）运行DreamerV3
  3. 运行IMPALA和Rainbow作为对照基线（Acme实现，调优学习率和熵正则）
  4. 在100M环境步数处报告episode回报及各物品发现率（Figure 5, Figure 9）
  5. 统计10个种子中发现钻石的智能体比例
- **Metrics**: ['episode回报（100M步处）', '各物品发现率（%）', '发现钻石的运行比例']
- **Expected outcome**: DreamerV3能够发现钻石而所有基线均不能，且所有DreamerV3运行最终均能发现至少一枚钻石
- **Baselines**: ['IMPALA（调优）', 'Rainbow（调优）', 'PPO', 'VPT（参考，使用人类数据）']
- **Dependencies**: []

## E3: 鲁棒性技术消融实验（14个多样任务子集）
- **Verifies**: C3
- **Setup**:
  - Model: DreamerV3完整版及各单一消融变体（逐一去除每项鲁棒性技术）
  - Hardware: Nvidia A100 GPU
  - Dataset: 从多个领域选取的14个任务子集
  - System: 消融对象：KL目标（世界模型）、回报归一化、symexp twohot回归、观测symlog、unimix分布、Critic EMA正则化等
- **Procedure**:
  1. 对14个多样化任务分别运行DreamerV3完整版和每个单一消融变体
  2. 记录各技术被去除后的平均性能变化
  3. 分析每项技术对全部任务的贡献模式（部分技术仅影响特定任务子集）
  4. 汇总平均性能曲线（Figure 6a），补充各任务独立曲线于附录（Figure 17）
- **Metrics**: ['各任务得分及跨14个任务的平均性能']
- **Expected outcome**: 所有鲁棒性技术均对整体平均性能有正向贡献，其中KL目标贡献最为显著，回报归一化和symexp twohot回归次之
- **Baselines**: ['DreamerV3完整版']
- **Dependencies**: []

## E4: 模型规模与Replay Ratio扩展实验
- **Verifies**: C4
- **Setup**:
  - Model: DreamerV3的6种参数规模（12M至400M），多种Replay Ratio
  - Hardware: Nvidia A100 GPU
  - Dataset: Crafter 和 DMLab 任务
  - System: 固定所有超参数，仅改变模型规模（通过模型维度参数化，见Table 3）或Replay Ratio
- **Procedure**:
  1. 训练6种模型规模（12M、25M、50M、100M、200M、400M参数）的DreamerV3
  2. 对不同Replay Ratio（影响每步环境交互对应的梯度更新次数）分别训练
  3. 记录任务性能及达到目标性能所需环境步数随规模的变化
  4. 在Crafter和DMLab任务上绘制学习曲线（Figure 6c/d）
- **Metrics**: ['任务得分（不同模型规模和Replay Ratio下）', '达到目标性能所需环境交互量']
- **Expected outcome**: 更大的模型规模单调提升任务性能并降低数据需求；更高的Replay Ratio进一步减少所需环境交互量；两者均表现出可预测的扩展行为
- **Baselines**: ['各规模之间相互比较']
- **Dependencies**: []

## E5: 学习信号消融实验（重建目标 vs. 奖励/价值梯度）
- **Verifies**: C5
- **Setup**:
  - Model: DreamerV3完整版及两种消融变体
  - Hardware: Nvidia A100 GPU
  - Dataset: 14个多样化任务子集
  - System: 分别停止任务相关的奖励/价值预测梯度或任务无关的重建梯度对世界模型表征的影响
- **Procedure**:
  1. 运行DreamerV3完整版作为对照
  2. 消融变体A：停止奖励和价值预测梯度对世界模型表征的影响
  3. 消融变体B：停止重建梯度对世界模型表征的影响
  4. 比较两种消融对平均性能的影响（Figure 6b）
- **Metrics**: ['跨多任务的平均性能']
- **Expected outcome**: 停止重建梯度对性能的损害明显大于停止奖励/价值梯度，说明无监督重建是DreamerV3的主要学习信号
- **Baselines**: ['DreamerV3完整版']
- **Dependencies**: []
