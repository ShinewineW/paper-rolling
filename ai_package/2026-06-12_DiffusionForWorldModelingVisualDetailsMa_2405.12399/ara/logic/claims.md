# Claims

## C1: DIAMOND 在世界模型代理中取得更强 Atari 表现
- **Statement**: 在 Atari 100k benchmark 上，DIAMOND 相比同类完全在 world model 内训练的代理取得更高的平均表现，并在若干需要小视觉细节的游戏上表现突出。
- **Status**: 支持
- **Falsification criteria**: 若在相同 Atari 100k benchmark、相同经验预算和相同聚合指标下，STORM、DreamerV3、IRIS、TWM 或 SimPLe 的平均表现不低于 DIAMOND，则该结论会被削弱。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: Table 1 直接比较了 DIAMOND 与多个 world model baseline；作者将较高表现与更忠实的视觉细节建模联系起来。
- **Tags**: ['improvement', 'generalization']

## C2: EDM 选择提升低步数自回归稳定性
- **Statement**: 相对 DDPM，基于 EDM 的 diffusion world model 在少量 denoising steps 下更能维持长时序 imagined trajectories 的稳定性。
- **Status**: 支持
- **Falsification criteria**: 若在共享架构和共享静态数据上，DDPM 在相同或更低推理成本下不出现更强 compounding error，或 EDM 不再更稳定，则该机制性解释会被削弱。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 论文将差异归因于 EDM 的 adaptive mixing 训练目标；这是论文明确给出的机制解释，而非外部推断。
- **Tags**: ['causal', 'improvement']

## C3: 多步去噪改善部分可观测场景中的采样质量与代理表现
- **Statement**: 单步 denoising 在多模态后验或部分可观测情形下容易生成模糊或折中结果，而多步采样更能趋向具体模式，并在定量消融中总体更优。
- **Status**: 支持
- **Falsification criteria**: 若减少 denoising steps 后在同一游戏集合上的聚合表现不下降，且视觉样例不再出现模糊或模式折中，则该结论会被削弱。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: Table 7 给出减少 denoising steps 的消融；Figure 4 给出 Boxing 中单步与多步采样的质性差异。
- **Tags**: ['causal', 'improvement']

## C4: 视觉细节一致性与强化学习表现相关
- **Statement**: DIAMOND 比 IRIS 更少出现跨帧视觉不一致；这些细节差异在 Asterix、Breakout 和 Road Runner 等游戏中与更好的代理表现相对应。
- **Status**: 支持
- **Falsification criteria**: 若在相同 expert-policy 静态数据比较中，IRIS 不再出现细节不一致，或这些游戏上的代理表现差异不随视觉一致性变化，则该解释会被削弱。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 论文明确说这些改进一般反映在 Table 1 的 agent performance 上，并指出由于 agent 组件相似，改进很可能来自 world model。
- **Tags**: ['causal', 'descriptive']

## C5: DIAMOND 的性能提升不只是更大计算量导致
- **Statement**: 与 IRIS 和 DreamerV3 的附加比较显示，DIAMOND 在参数量与训练时间维度并非简单依靠更大模型或更多训练计算取得表现。
- **Status**: 支持
- **Falsification criteria**: 若 DIAMOND 的参数量和训练时间实际上高于主要 baseline，或控制计算后优势消失，则该限定结论会被削弱。
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: Table 4 比较参数量、训练时间和 Mean HNS；Table 5 展示 DIAMOND 训练时间构成，用于界定计算成本。
- **Tags**: ['scoping', 'descriptive']

## C6: DIAMOND 可扩展到静态数据上的复杂 3D 视觉世界模型
- **Statement**: 在 CS:GO 与 motorway driving 的静态数据实验中，DIAMOND 的 frame-stack 版本在视觉质量指标上优于报告的 baseline，并可产生可交互或可视上合理的轨迹。
- **Status**: 支持
- **Falsification criteria**: 若在相同静态数据、相同条件输入和相同视觉指标下，DreamerV3 或 IRIS 的生成质量优于 DIAMOND，或 DIAMOND 不能响应动作条件，则该泛化结论会被削弱。
- **Proof**: [E6]
- **Evidence basis**: ['E6']
- **Interpretation**: Table 8 量化比较 3D environments 的 FID、FVD、LPIPS、sample rate 和参数；正文与 Figure 10 到 Figure 12 描述了轨迹合理性和动作响应局限。
- **Tags**: ['generalization', 'improvement']
