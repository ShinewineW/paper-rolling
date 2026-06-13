# Claims

## C1: 无感知标注的开放环规划性能
- **Statement**: World4Drive 在 nuScenes 开放环基准上，在无需人工感知标注的设定中优于感知标注-free 强基线，并在碰撞率指标上表现突出。
- **Status**: supported
- **Falsification criteria**: 若在相同 nuScenes 评测协议和表中基线设定下，World4Drive 的平均 L2 或平均 Collision Rate 不优于感知标注-free 基线，则该主张不成立。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 该结论来自 Table 1；表中 World4Drive 与 LAW* [18] (Perception-free) 及其他方法在 L2 和 Collision Rate 上直接比较。
- **Tags**: ['improvement']

## C2: 闭环 NavSim 竞争性表现
- **Statement**: World4Drive 在 NavSim 闭环基准上相较 LAW (Perception-free) 提升 PDMS，并在若干空间安全相关指标上更好，但仍低于 DiffusionDrive。
- **Status**: supported
- **Falsification criteria**: 若在 Table 2 的 NavSim 设定下，World4Drive 的 PDMS 未超过 LAW (Perception-free)，或超过 DiffusionDrive，则该主张需修正。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 该结论依据 Table 2 和正文对 TTC、DAC、PDMS 的说明；对 DiffusionDrive 的例外也由正文明确指出。
- **Tags**: ['improvement']

## C3: 组件消融显示意图、空间语义先验与世界模型均有作用
- **Statement**: 组件消融表明，引入车辆意图、深度空间先验、语义先验以及保留世界模型评估机制，会影响规划误差和碰撞表现；仅保留意图而缺少世界模型会导致规划表现退化。
- **Status**: supported
- **Falsification criteria**: 若 Table 3 中移除或加入对应组件后 L2 与 Collision 的方向不符合正文所述比较，则该组件贡献主张不成立。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 该主张来自 Table 3 以及 4.4.1 对行间比较的解释；因属于消融实验，支持的是论文内部设定下的因果证据。
- **Tags**: ['causal']

## C4: 多驾驶条件下的鲁棒性
- **Statement**: 在不同光照、天气和驾驶机动条件下，World4Drive 相比 LAW 展现出更好的整体鲁棒性，尤其在夜间、雨天和多类转向机动中生成更安全的规划轨迹。
- **Status**: supported
- **Falsification criteria**: 若 Table 4 或 Table 5 中 World4Drive 在对应条件下未优于 LAW，或正文未支持跨条件更稳健的描述，则该主张不成立。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 该结论来自 Table 4、Table 5 与 4.4.2 的文字分析；Table 5 在 Markdown 中解析质量较差，因此只按原表文本保留证据。
- **Tags**: ['generalization']

## C5: 模型尺度扩展性
- **Statement**: World4Drive 在改变图像 backbone 和 hidden dimension 时表现出可扩展性，论文认为这与潜在表征被直接用于规划任务有关。
- **Status**: supported
- **Falsification criteria**: 若 Table 6 中扩大 backbone 或 dimension 后规划指标未出现改善方向，或正文未做可扩展性解释，则该主张不成立。
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: 该结论来自 Table 6 与 4.4.3；其中关于原因的部分是论文正文解释。
- **Tags**: ['generalization']
