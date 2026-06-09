# Problem Specification

## Observations

### O1: 主流端到端规划器（如 Transfuser、UniAD、VAD）从 ego-qu
- **Statement**: 主流端到端规划器（如 Transfuser、UniAD、VAD）从 ego-query 回归单一轨迹，无法建模驾驶行为固有的不确定性和多模态性。
- **Evidence**: 论文第 1 节对 Fig. 1a 的描述：单模态回归范式不考虑驾驶行为的内在不确定性和多模态性。
- **Implication**: 单模态回归在复杂场景下泛化能力不足，无法覆盖潜在的行驶动作空间。

### O2: 基于大型固定词汇表的方法（如 VADv2，含 8192 个锚轨迹）在词汇表之外的
- **Statement**: 基于大型固定词汇表的方法（如 VADv2，含 8192 个锚轨迹）在词汇表之外的场景下表现受限，且大量锚点带来显著计算开销。
- **Evidence**: 论文第 1 节指出此类范式「fundamentally constrained by the number and quality of anchor trajectories, often failing in out-of-vocabulary scenarios」。
- **Implication**: 固定词汇表的表示容量有上限，难以覆盖开放世界交通场景的完整分布。

### O3: 将机器人领域的普通 DDIM 扩散策略直接用于自动驾驶时，出现模式坍塌：不同随机
- **Statement**: 将机器人领域的普通 DDIM 扩散策略直接用于自动驾驶时，出现模式坍塌：不同随机噪声去噪后收敛到相似轨迹，多样性极低。
- **Evidence**: 论文第 3.2 节 Fig. 2 及 Tab. 2 的模式多样性分数 D 结果：Transfuser_DP 仅有 11% 多样性。
- **Implication**: 普通扩散策略在驾驶场景中无法有效建模多模态分布，失去生成模型的核心价值。

### O4: 普通 DDIM 扩散策略需要 20 步去噪，将规划模块运行时间增大 650 倍，
- **Statement**: 普通 DDIM 扩散策略需要 20 步去噪，将规划模块运行时间增大 650 倍，FPS 从 60 降至 7，无法满足自动驾驶实时需求。
- **Evidence**: 论文第 3.2 节：「Tab. 2 shows ... a total 650× increase in runtime overhead」，FPS 数值来自 Tab. 2。
- **Implication**: 推理效率瓶颈使普通扩散策略在在线自动驾驶部署中不可行。

## Gaps

### G1: 从纯随机高斯分布去噪导致模式坍塌，无法生成多样的合理轨迹。
- **Statement**: 从纯随机高斯分布去噪导致模式坍塌，无法生成多样的合理轨迹。
- **Caused by**: O3
- **Existing attempts**: ['VADv2 使用大型固定词汇表离散化动作空间，但受限于词汇表覆盖范围（O2）。']
- **Why they fail**: 随机高斯噪声与驾驶动作分布之间距离过大，扩散模型在复杂开放世界场景中难以有效探索多模态空间。

### G2: 普通扩散策略的多步去噪导致推理速度远低于实时要求。
- **Statement**: 普通扩散策略的多步去噪导致推理速度远低于实时要求。
- **Caused by**: O4
- **Existing attempts**: ['DDIM 已相较 DDPM 大幅减少步数，但在自动驾驶场景中仍需 20 步（O4）。']
- **Why they fail**: 每步去噪均需完整的神经网络前向传播，20 步累积开销不可接受。

## Key Insight
- **Insight**: 人类驾驶遵循有限的固定模式并根据实时交通动态调整；将这些先验驾驶模式作为锚点嵌入扩散过程，把去噪起点从随机高斯噪声改为「锚定高斯分布」，即可同时解决模式坍塌（G1）和推理效率（G2）两个问题。
- **Derived from**: O3 + O4 + 对人类驾驶行为模式的观察
- **Enables**: 截断扩散调度使去噪步骤从 20 步减少到 2 步，同时提升轨迹多样性；配合高效级联解码器，实现实时多模态规划。

## Assumptions
- 驾驶动作分布可以被有限数量（论文中为 20 个）的 K-Means 聚类锚点充分代表，从而覆盖典型驾驶模式。
- 从锚定高斯分布出发的截断去噪过程能够学习到与从纯高斯噪声完整去噪等效的动作分布。（分析推断，论文未显式声明）
- 推理阶段可灵活调整采样数量 $N_{\mathrm{infer}}$ 而不需重新训练，模型泛化能力足以支持训练锚点数之外的采样量。
