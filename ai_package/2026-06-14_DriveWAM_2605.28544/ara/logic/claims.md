# Claims

## C1: NAVSIM 规划性能
- **Statement**: DriveWAM 在 NAVSIM v1 上以单前视相机输入取得强规划表现，并在论文比较的同类端到端规划方法中整体占优。
- **Status**: 支持
- **Falsification criteria**: 若按相同 NAVSIM v1 协议复现时，DriveWAM 的综合规划指标不能优于表中可比方法，则该主张被削弱。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 该结果支持作者关于视频生成骨干能提供时空先验并改善细粒度动作预测的解释，但因比较集合来自论文表格，跨实现公平性仍依赖原文设定。
- **Tags**: ['improvement', 'descriptive']

## C2: PhysicalAI 轨迹预测性能
- **Statement**: DriveWAM 在 PhysicalAI-Autonomous-Vehicles 的精选测试子集上优于论文比较的 VaVAM 与 Alpamayo-1.5。
- **Status**: 支持
- **Falsification criteria**: 若在同一精选测试子集、同一前视相机输入和单轨迹输出设定下，DriveWAM 的 ADE/FDE 不再优于这些基线，则该主张不成立。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 该实验把 DriveWAM 放到大规模真实驾驶基准中比较，支持其世界动作建模不仅适用于 NAVSIM，也能迁移到 PhysicalAI-Autonomous-Vehicles。
- **Tags**: ['improvement', 'generalization']

## C3: scene-evolving guidance 的贡献
- **Statement**: 将固定全局 prompt 替换为 chunk-specific 的 scene-evolving guidance，可以在不同训练数据规模下改善轨迹预测。
- **Status**: 支持
- **Falsification criteria**: 若移除 scene-evolving guidance 后在同样数据规模和训练设置下指标不变或更好，则该组件贡献不成立。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 消融表明高层场景语义对低层 WA backbone 是互补条件，而不是只在小数据设置下有效。
- **Tags**: ['causal', 'improvement']

## C4: 数据扩展趋势
- **Statement**: 在固定训练流程下，训练数据从小规模扩展到更大规模时，DriveWAM 的轨迹误差总体下降，显示视频动作建模具备扩展潜力。
- **Status**: 支持
- **Falsification criteria**: 若扩大训练数据后 ADE/FDE 不再改善，或趋势只在单一 guidance 设置下出现，则扩展性主张被削弱。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 该趋势支持论文关于当前数据规模尚未饱和的判断，但这仍是表内规模范围内的经验结论。
- **Tags**: ['generalization', 'descriptive']

## C5: 视频预训练与联合视频监督
- **Statement**: 预训练视频骨干初始化与联合视频 flow-matching 监督共同有助于保持生成视频先验并提升 WA policy 学习。
- **Status**: 支持
- **Falsification criteria**: 若从头训练或移除视频监督后性能没有下降，或者优于完整配置，则该机制解释不成立。
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: 消融结果符合作者解释：action-only adaptation 难以保留生成视频先验，完整配置表现最好。
- **Tags**: ['causal', 'improvement']

## C6: selective KV memory 的长时 rollout 折中
- **Statement**: selective KV memory 在固定缓存预算下相对 FIFO 更接近 Full KV 的轨迹精度，同时显著降低长时 rollout 的内存与计算开销。
- **Status**: 支持
- **Falsification criteria**: 若在相同缓存预算和 rollout 设置下 selective KV memory 的精度接近 FIFO 或开销接近 Full KV，则该主张被削弱。
- **Proof**: [E6]
- **Evidence basis**: ['E6']
- **Interpretation**: 该结果支持 relevance-redundancy 选择比单纯年龄淘汰更适合保留驾驶相关历史信息。
- **Tags**: ['improvement', 'descriptive']

## C7: 推理成本可比性
- **Statement**: DriveWAM 的低步数动作去噪变体在保持相近轨迹表现的同时，使 per-chunk 推理成本接近 Alpamayo-1.5，并额外生成未来视频。
- **Status**: 支持
- **Falsification criteria**: 若减少动作去噪步数导致轨迹指标明显变差，或总延迟不能接近 Alpamayo-1.5，则该效率主张不成立。
- **Proof**: [E7]
- **Evidence basis**: ['E7']
- **Interpretation**: 附录效率表说明 DriveWAM 的视频生成分支带来额外阶段，但通过减少动作去噪可获得可接受的 per-chunk 成本。
- **Tags**: ['improvement', 'descriptive']
