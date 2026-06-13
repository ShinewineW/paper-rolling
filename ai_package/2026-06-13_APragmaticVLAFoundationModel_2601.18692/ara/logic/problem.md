# Problem Specification

## Observations

### O1: VLA foundation model 已能通过大规模预训练获得可迁移操作能力
- **Statement**: VLA foundation model 已能通过大规模预训练获得可迁移操作能力，但真实机器人场景下的数据规模化规律仍缺少系统实证。
- **Evidence**: Introduction 明确指出社区仍缺少关于 real-robot performance 如何随 increasingly vast pre-training datasets 扩展的 comprehensive empirical studies。
- **Implication**: 本文把问题中心放在真实机器人数据规模、任务多样性与跨平台评测之间的关系。

### O2: 仿真评测便捷但不能充分代表真实物理世界，真实评测又受硬件并行度限制。
- **Statement**: 仿真评测便捷但不能充分代表真实物理世界，真实评测又受硬件并行度限制。
- **Evidence**: Evaluation on Robot Policy 中说明 simulation environments 的结果 often do not fully represent the complexity of the real physical world，且 real-world evaluations 的效率受 extensive hardware parallelism 限制。
- **Implication**: 需要用真实平台上的标准化任务和一致协议来检验 VLA 的实际可部署性。

### O3: 大规模 VLA 训练不仅是模型问题，也受数据 I/O、通信开销和算子效率制约。
- **Statement**: 大规模 VLA 训练不仅是模型问题，也受数据 I/O、通信开销和算子效率制约。
- **Evidence**: Efficient VLA Training 中指出 multi-node clusters 上训练 large-scale VLA models 仍面临 data I/O bottlenecks and communication overheads。
- **Implication**: 论文将训练基础设施作为方法贡献的一部分，而不只报告模型结构。

## Gaps

### G1: 缺少真实机器人数据规模化的直接证据。
- **Statement**: 缺少真实机器人数据规模化的直接证据。
- **Caused by**: 真实数据采集和大规模真实评测成本高，且平台、任务和协议难以统一。
- **Existing attempts**: ['采用大规模真实遥操作数据进行预训练。', '在 GM-100 上进行跨平台真实评测。', '用 scaling experiments 检查预训练数据增加时的趋势。']
- **Why they fail**: 过去进展展示了多任务和多具身适应能力，但没有充分回答真实数据继续增加时 success rates 是否持续受益。

### G2: 缺少能支撑大规模 VLA 训练的高效代码路径。
- **Statement**: 缺少能支撑大规模 VLA 训练的高效代码路径。
- **Caused by**: 视觉、语言、动作融合带来稀疏注意力和多模块并行训练需求。
- **Existing attempts**: ['使用 FSDP 与 action expert shard groups 降低不必要通信。', '用 FlexAttention 优化稀疏注意力计算。', '用 torch.compile 做算子融合以减少 kernel launch overhead。']
- **Why they fail**: 已有代码库面向不同研究优先级，但多节点训练中的数据加载、分布式通信和算子开销仍会限制吞吐。

## Key Insight
- **Insight**: 本文的核心洞察是，VLA 的真实可用性需要同时扩展真实多具身数据、严格真实评测和训练系统效率，而不是只扩大单一模型组件。
- **Derived from**: ['C1', 'C2', 'C3']
- **Enables**: 使 LingBot-VLA 能以统一框架讨论泛化、空间感知、数据效率和训练吞吐。

## Assumptions
- 真实机器人任务上的 Success Rate 与 Progress Score 能代表部署可行性。
- GM-100 的任务多样性足以暴露跨平台泛化差异。
- 预训练 VLM 的语义表示可以通过 action expert 转化为连续控制能力。
- 深度表示蒸馏能为复杂操作提供有用的空间先验。
