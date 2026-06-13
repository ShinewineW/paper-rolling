# Claims

## C1: 真实机器人基准优势
- **Statement**: LingBot-VLA 在 GM-100 真实世界评估中相对 WALL-OSS、GR00T N1.6 与 π0.5 表现更强，优势同时体现在任务完成与分步进展两个指标上。
- **Status**: supported
- **Falsification criteria**: 若在相同训练、相同硬件任务配对和相同评估协议下，基线方法在 GM-100 聚合结果或明细任务上稳定达到或超过 LingBot-VLA，则该主张被削弱。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 该结论来自论文对多种真实机器人平台的统一后训练和顺序测试；它说明模型在跨 embodiment 的真实操作环境中具备更强的整体表现。
- **Tags**: ['improvement', 'generalization']

## C2: 深度信息带来空间感知收益
- **Statement**: 加入基于 LingBot-Depth 的深度蒸馏后，LingBot-VLA w/ depth 在聚合真实世界结果中优于 π0.5，并在若干平台和任务上改善 SR 或 PS。
- **Status**: supported
- **Falsification criteria**: 若移除深度蒸馏或替换为空间无关信号后仍得到同等趋势，或在复现实验中 w/ depth 不能稳定优于对应设置，则该因果解释不成立。
- **Proof**: [E1, E2]
- **Evidence basis**: ['E1', 'E2']
- **Interpretation**: 论文把深度收益解释为 learnable query 与 LingBot-Depth token 对齐带来的空间先验；因果性来自 w/o depth 与 w/ depth 的对照设置。
- **Tags**: ['improvement', 'causal']

## C3: 仿真多任务泛化提升
- **Statement**: 在 RoboTwin 2.0 仿真评估中，LingBot-VLA 两个变体相对 π0.5 在 clean 和 randomized 场景的平均成功率上表现更好。
- **Status**: supported
- **Falsification criteria**: 若在相同 RoboTwin 2.0 训练数据、随机化设置和评估任务下，π0.5 的平均成功率达到或超过 LingBot-VLA，则该主张被推翻。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 该结果表明模型收益不只出现在真实机器人测试，也延伸到带随机化的仿真多任务设置。
- **Tags**: ['improvement', 'generalization']

## C4: 预训练数据规模仍呈上升趋势
- **Statement**: 在论文的 scaling experiments 中，随着真实世界预训练数据时长增加，Progress Rate 与 Success Rate 呈持续上升趋势，论文称未观察到饱和。
- **Status**: supported
- **Falsification criteria**: 若进一步扩大或复现数据规模时指标停滞、下降，或不同 embodiment 的趋势不再一致，则该扩展规律需要修正。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 这是图示和正文趋势主张，不在本块 evidence_tables 中给出精确图上读数；因此这里只保留方向性结论。
- **Tags**: ['improvement', 'descriptive']

## C5: 训练吞吐优化提升效率
- **Statement**: 论文称其训练代码库在不同 VLM 底座复现的 π-like 模型上，相比 StarVLA、Dexbotic 与 OpenPI 具备更快训练速度，并保持较好的扩展效率。
- **Status**: supported
- **Falsification criteria**: 若在相同 Libero 数据、相同 π-like 架构和相同 batch 设置下，开源基线吞吐超过该代码库或扩展效率不再接近理论趋势，则该主张被削弱。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 该主张依赖 Figure 4 的吞吐曲线和正文描述；由于论文未以表格给出图中精确读数，本块不转录图上数值。
- **Tags**: ['improvement', 'descriptive']
