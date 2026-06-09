# Claims

## C1: DreamerV3以固定超参数在超过150个多样任务上超越调优专家算法
- **Statement**: DreamerV3是一种通用强化学习算法，在固定超参数的条件下，可在超过150个多样化任务中超越针对各领域专门设计并调优的专家算法，并大幅优于通用的PPO算法。
- **Status**: supported
- **Falsification criteria**: 若存在某一领域，使用固定超参数的DreamerV3在该领域系统性地劣于调优专家基线，则此声明可被证伪。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 论文通过在Atari、ProcGen、DMLab、Atari100K、BSuite、本征控制、视觉控制等8个领域的基准测试加以支撑，DreamerV3统一使用Table 4中所列的固定超参数，无针对任何领域的调整。
- **Tags**: ['improvement', 'generalization']

## C2: DreamerV3首次从零开始在Minecraft中采集钻石（无需人类数据或课程学习）
- **Statement**: DreamerV3是首个在不使用人类数据、不使用自适应课程学习的条件下，从稀疏奖励出发、从零开始在Minecraft中采集到钻石的算法；所有DreamerV3运行均在100M环境步内发现钻石，而所有对比基线均未能发现钻石。
- **Status**: supported
- **Falsification criteria**: 若有证据表明此前已有算法在完全相同条件下（无人类数据、无课程、仅稀疏奖励）完成了Minecraft钻石采集，则此声明可被证伪。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 论文对比了VPT（使用大量人类视频数据与720个GPU训练9天）及使用自适应课程的算法，所有对比基线均未能发现钻石，验证了该声明的首次性。
- **Tags**: ['improvement', 'scoping']

## C3: 鲁棒性技术（归一化、平衡、变换）是跨领域固定超参数稳定学习的关键
- **Statement**: DreamerV3中的一系列鲁棒性技术——包括KL平衡与自由位、1%均匀混合分布、百分位数回报归一化（带分母下限）、symexp twohot损失——共同使得算法在多样领域下无需超参数调优即可稳定学习。每种技术对部分任务至关重要，但不一定对所有任务均有显著影响。
- **Status**: supported
- **Falsification criteria**: 若消融任一鲁棒性技术后跨领域平均性能没有显著下降，则该技术对鲁棒性的因果贡献将被削弱。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 论文通过14个多样化任务上的消融实验加以验证，所有鲁棒性技术均对整体平均性能有贡献，其中世界模型KL目标贡献最为突出，其次是回报归一化和symexp twohot回归。
- **Tags**: ['causal', 'improvement']

## C4: DreamerV3的性能和数据效率随模型规模可预测地单调扩展
- **Statement**: 随着模型参数量从12M增加到400M，DreamerV3的任务性能单调提升，同时所需环境交互量减少；增大Replay Ratio同样可进一步提升数据效率。两者共同提供了一种可预测的「计算资源换性能」途径，且固定超参数下的扩展表现鲁棒。
- **Status**: supported
- **Falsification criteria**: 若出现某个模型规模区间，更大的模型不能带来更高性能或更低的交互需求，则单调扩展声明将被证伪。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 论文在Crafter和DMLab任务上对6种模型规模（12M至400M参数）及多种Replay Ratio进行测试，观察到超参数固定情况下的鲁棒扩展性。
- **Tags**: ['descriptive', 'improvement']

## C5: 世界模型的无监督重建目标是DreamerV3性能的主要学习信号
- **Statement**: DreamerV3的性能主要依赖于世界模型的无监督重建目标，而非任务相关的奖励和价值预测梯度；停止重建梯度对性能的损害远大于停止奖励/价值梯度。这与大多数先前仅使用任务特定学习信号的强化学习算法形成鲜明对比。
- **Status**: supported
- **Falsification criteria**: 若消融重建梯度后性能仅有微小下降，而消融奖励/价值梯度导致更大下降，则此声明将被证伪。
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: 论文通过分别停止重建梯度和奖励/价值预测梯度的消融实验加以验证（Figure 6b），结果表明重建损失在DreamerV3中具有主导地位，为未来基于无监督预训练的算法变体提供了理论依据。
- **Tags**: ['causal', 'descriptive']
