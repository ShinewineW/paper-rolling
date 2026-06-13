# Claims

## C1: 规划中的因果不确定性与MCG提升奖励
- **Statement**: 在D4RL迷宫规划中，Diffusion Forcing通过不同时间步的噪声日程和MCG，将未来不确定性纳入引导采样；论文报告其平均奖励优于主要离线强化学习与Diffuser基线，去掉MCG后性能下降。
- **Status**: 支持
- **Falsification criteria**: 若在相同D4RL迷宫设置、相同奖励度量和相同执行协议下，Diffusion Forcing不再优于Diffuser或去掉MCG不导致下降，则该主张被削弱。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 该结论来自Table 1及正文对MCG、因果一致性和Diffuser执行动作失败的说明；奖励指标本身在附录中被作者提醒可能不完全反映到达目标的速度。
- **Tags**: ['improvement', 'causal']

## C2: 视频长滚动稳定性
- **Statement**: 在Minecraft和DMLab视频预测中，Causal Diffusion Forcing被用于自回归滚动，论文称其能在训练视野之外保持稳定，而teacher forcing和causal full-sequence diffusion基线较快发散。
- **Status**: 支持
- **Falsification criteria**: 若在相同Minecraft与DMLab数据、相同RNN架构和相同采样稳定化设置下，基线在训练视野外同样稳定或CDF出现同等发散，则该主张不成立。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 这是定性视觉实验与附录非挑选可视化支持的主张；论文没有给出对应定量表，因此本块不把视频长度数值写入claim。
- **Tags**: ['improvement', 'generalization']

## C3: 机器人长程模仿学习依赖记忆且对扰动更稳健
- **Statement**: 在水果换位机器人任务中，Diffusion Forcing利用潜状态记忆处理非马尔可夫观察，并在视觉干扰或遮挡时通过噪声观测机制依赖先验，从而优于无记忆的diffusion policy和next-frame diffusion基线。
- **Status**: 支持
- **Falsification criteria**: 若在相同Franka机器人任务、相同演示数据和相同扰动测试下，无记忆策略或next-frame diffusion达到相当表现，则该主张被削弱。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 该证据来自Section 4.4的成功率叙述和Figure 4任务说明；精确成功率只在本块的证据表中列出。
- **Tags**: ['improvement', 'descriptive']

## C4: 通用时间序列预测能力没有明显退化
- **Statement**: 在GluonTS多变量概率时间序列预测中，Diffusion Forcing使用相同架构和超参数进行多个数据集评测，论文称其整体上与强扩散和transformer基线竞争，目的在于说明新训练目标作为通用序列模型没有明显性能折衷。
- **Status**: 支持
- **Falsification criteria**: 若在相同GluonTS数据、相同CRPS_sum评估、相同协变量和早停协议下，Diffusion Forcing相对TimeGrad、Transformer-MAF和ScoreGrad系统性落后，则该主张不成立。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: Table 2显示不同数据集上优劣不一致，作者也明确说time series不是核心应用，因此该主张应解读为适用性和竞争性，而非全数据集绝对最优。
- **Tags**: ['generalization', 'scoping']
