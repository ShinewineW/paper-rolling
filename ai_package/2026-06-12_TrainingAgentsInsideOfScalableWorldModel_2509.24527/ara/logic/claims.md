# Claims

## C1: 离线 Minecraft 钻石挑战
- **Statement**: Dreamer 4 通过在世界模型中进行想象训练，可以在不进行在线环境交互的离线设置中完成 Minecraft 钻石挑战，并且相对行为克隆类基线表现更强。
- **Status**: supported
- **Falsification criteria**: 若在相同 VPT contractor dataset、相同评估协议和相同提示序列下，Dreamer 4 不能超过行为克隆类基线，或不能取得 Diamond 成功，则该主张被削弱。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: Table 7 和 Table 8 支持该结论：Dreamer 4 在多项里程碑成功率上领先，并且成功到达时通常更快；Diamond 项显示其具备离线取得钻石的能力。
- **Tags**: ['improvement', 'causal']

## C2: 交互式世界模型能力
- **Statement**: Dreamer 4 的世界模型在 Minecraft 中比 Oasis、Lucid-v1 和 MineWorld 更能支持复杂物体交互与游戏机制的实时交互式模拟。
- **Status**: supported
- **Falsification criteria**: 若同一人工交互任务集合中，其他世界模型在成功任务数、上下文长度或实时交互速度上达到或超过 Dreamer 4，则该主张不成立。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: Table 1 显示 Dreamer 4 同时具备较长上下文、接近游戏帧率的交互速度和更高任务成功数，论文文字还指出 MineWorld 因缺少交互式推理未被完整任务评估。
- **Tags**: ['improvement', 'descriptive']

## C3: 少量动作数据的动作条件化
- **Statement**: Dreamer 4 可以从大量无动作标签视频中吸收主要世界知识，只用少量配对动作视频学习动作条件化，并能泛化到只在无标签视频中出现的 Minecraft 维度。
- **Status**: supported
- **Falsification criteria**: 若减少配对动作数据后，动作条件化生成质量不能相对无动作模型明显提升，或在 Nether 和 End 持出维度上无法维持动作条件化效果，则该主张被削弱。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: Figure 7 与正文报告了动作数据量实验和跨维度动作外推实验，说明模型可在少量动作标签下获得动作条件化，并将动作 grounding 泛化到仅通过无标签视频见过的场景。
- **Tags**: ['generalization', 'descriptive']

## C4: 目标和架构消融
- **Statement**: Shortcut forcing、x-space 预测与损失、ramp weight、交替 batch 长度、稀疏时间注意力、GQA 和更多空间 token 的级联设计共同提升了 Dreamer 4 的生成质量与推理效率。
- **Status**: supported
- **Falsification criteria**: 若在同样训练预算和生成评估协议下，移除这些设计后 FVD 与 FPS 不劣化，或完整模型不能优于朴素 diffusion forcing transformer，则该主张被削弱。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: Table 2 的消融级联显示，从朴素基线到完整设计，质量指标和推理速度随设计选择变化；论文也将这些变化解释为高容量和高效率的来源。
- **Tags**: ['causal', 'improvement']

## C5: 实验设置边界
- **Statement**: Dreamer 4 与既有 Minecraft 钻石智能体的关键差异在于只使用离线 contractor 数据、采用高分辨率图像输入和低层键鼠动作，而不依赖在线交互或大规模合成标注网页视频。
- **Status**: supported
- **Falsification criteria**: 若实验设置显示 Dreamer 4 使用了在线交互数据或大规模网页视频动作标注数据，则该范围主张不成立。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: Table 3 将 Dreamer 4 与 Dreamer 3、VPT (RL)、VPT (BC) 的输入、动作和数据来源并列，限定了论文声称的离线训练边界。
- **Tags**: ['scoping', 'descriptive']
