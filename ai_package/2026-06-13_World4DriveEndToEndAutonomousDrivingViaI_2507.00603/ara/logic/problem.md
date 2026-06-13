# Problem Specification

## Observations

### O1: 端到端自动驾驶需要从原始传感器直接生成规划轨迹，但常见方法依赖成本高的感知监督。
- **Statement**: 端到端自动驾驶需要从原始传感器直接生成规划轨迹，但常见方法依赖成本高的感知监督。
- **Evidence**: Abstract 明确说 end-to-end autonomous driving directly generates planning trajectories from raw sensor data，同时 typically relies on costly perception supervision。
- **Implication**: 若要提升可扩展性，核心问题是减少人工 perception annotations 依赖。

### O2: 单一 latent 世界模型难以同时表达物理世界的空间语义信息与多模态驾驶意图。
- **Statement**: 单一 latent 世界模型难以同时表达物理世界的空间语义信息与多模态驾驶意图。
- **Evidence**: Introduction 与 Related Works 均指出 LAW 的 single-modal latent features from images 难以捕获 spatial-semantic scene information 和 uncertainty of multi-modal driving intentions。
- **Implication**: 只学习图像 latent 的未来变化不足以支撑复杂场景中的合理轨迹选择。

### O3: World4Drive 将意图建模、物理 latent 编码和世界模型选择器绑定
- **Statement**: World4Drive 将意图建模、物理 latent 编码和世界模型选择器绑定在同一规划流程中。
- **Evidence**: Method Overview 说明 Driving World Encoding 提取 driving intention 和 physical world latent representations，Intention-aware World Model 预测未来 latent 并通过 world model selector 评分多模态轨迹。
- **Implication**: 规划不再只是回归一条轨迹，而是先想象不同意图对应的未来世界，再选择更合理的候选轨迹。

## Gaps

### G1: 依赖感知标注的方法在扩展到更多场景时成本受限。
- **Statement**: 依赖感知标注的方法在扩展到更多场景时成本受限。
- **Caused by**: BEV-centric、vector-based、sparse-centric 等表示通常把感知监督作为场景信息抽取的支撑。
- **Existing attempts**: ['UniAD', 'VAD', 'SparseDrive', 'VADv2', 'Hydra-MDP']
- **Why they fail**: 论文指出这些方法 typically require perception annotations such as 3D bounding boxes and HD maps。

### G2: 已有 perception-free latent world model 的表
- **Statement**: 已有 perception-free latent world model 的表达能力不足。
- **Caused by**: 缺少显式的空间语义先验，也没有把多种驾驶意图和世界演化预测紧密耦合。
- **Existing attempts**: ['VaVAM', 'LAW']
- **Why they fail**: 论文指出 LAW 从 raw images 构造 uni-modal latent features，难以捕获 spatial-semantic information 和 multi-modal driving intentions。

## Key Insight
- **Insight**: 把未来世界 latent 当作轨迹候选的评估介质，比直接生成单条轨迹更适合处理驾驶意图不确定性。
- **Derived from**: 由 Introduction 中的 multi-modal driving intentions 问题、Sec. 3.3 的 World Model Selector 机制，以及 ablation 中 intentions 与 world modeling 必须结合的结论共同归纳得到。
- **Enables**: 在不使用人工感知标注的前提下，模型可以生成、评估并排序多模态轨迹。

## Assumptions
- 本文把 perception annotation-free 限定为训练与推理不需要 manual perception annotations，但仍使用 vision foundation models 产生先验或伪标签。
- params_million 在论文 Markdown 中没有显式报告；该字段使用缺失哨兵值，不能解释为模型真实参数量。
