# Claims

## C1: 姿态增强提高视觉生成质量
- **Statement**: COMBAT 的 visual–pose 版本在标准感知指标上优于 RGB-only 版本，说明显式姿态信息有助于生成质量。
- **Status**: supported
- **Falsification criteria**: 如果在相同测试协议下 RGB-only 版本在 FD、FVD 和 LPIPS 上整体不高于 visual–pose 版本，则该主张不成立。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 论文将较低的 FD、FVD 和 LPIPS 解释为更好的视觉保真度与时间一致性；Table 1 中 COMBAT: Pose 在这些指标上均优于 COMBAT: Non-Pose。
- **Tags**: ['improvement']

## C2: 未监督的 Player 2 行为呈现阶段性涌现
- **Statement**: 在只以 Player 1 输入作为条件的训练设置下，COMBAT 生成的 Player 2 攻击活动量和拳脚比例随训练 checkpoint 呈现不同阶段，显示出从过度活跃到更接近人类行为模式的变化。
- **Status**: supported
- **Falsification criteria**: 如果人工标注的生成序列没有显示 TAA 与 ARC 随训练 checkpoint 变化，或这些变化与人类 gameplay 没有可比基准，则该主张不成立。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: Table 2 支持论文关于 emergent Player 2 behavior 的描述：早期模型更活跃，后续 checkpoint 的活动水平和动作比例发生变化，但论文也指出后期整体一致性会下降。
- **Tags**: ['descriptive', 'causal']

## C3: 行为一致性评价用于检验规则与节奏学习
- **Statement**: 论文提出基于 health data 的 damage distribution analysis 和 health trajectory analysis，用于检验生成 gameplay 是否学习到游戏内在规则、动作后果和比赛节奏。
- **Status**: supported
- **Falsification criteria**: 如果生成序列的伤害分布与平均血量轨迹无法与 ground-truth 序列比较，或这些指标不能反映动作后果和比赛节奏，则该评价主张不成立。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 该主张主要来自评价方法设计与 Figure 3 的定性说明；论文没有在表格中给出这些指标的数值结果。
- **Tags**: ['descriptive', 'scoping']

## C4: 蒸馏支持交互式推理但可能损害行为保真
- **Statement**: 论文采用 CausVid DMD 和 decoder distillation 加速推理，使 COMBAT 面向实时交互更实用；同时论文在 Future Work 中指出 DMD step distillation 会降低 agent responsiveness 和 attack frequency。
- **Status**: supported
- **Falsification criteria**: 如果蒸馏后的模型不能维持可用视觉质量，或没有观察到响应性和攻击频率受损的趋势，则该主张需要修正。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 论文正文将蒸馏描述为速度优化，并在未来工作中明确把行为保真下降作为待解决问题，因此该主张同时包含实用收益与已陈述限制。
- **Tags**: ['improvement', 'descriptive']
