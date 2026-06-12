# Related Work

## R1: Ha & Schmidhuber
- **DOI**: None
- **Type**: 早期控制导向世界模型
- **Delta**:
  - What changed: 论文将该类工作定位为学习潜在动力学模拟器用于 agent planning 的源头，而不是完整真世界模型。
  - Why: 它提供了生成式动态建模的早期视角，但论文认为真世界模型还必须整合交互闭环和持久记忆。
- **Claims affected**: ['C1']
- **Adopted elements**: ['潜在动力学模拟', 'agent planning 视角']

## R2: MaskGIT
- **DOI**: None
- **Type**: 掩码生成模型
- **Delta**:
  - What changed: 论文把 MaskGIT 作为视觉生成中并行掩码补全路线的代表，并将其放入通向统一和交互世界模型的早期基础。
  - Why: 掩码、补全与泛化为跨模态预训练和生成提供了统一原则，是后续统一模型的前置能力。
- **Claims affected**: ['C2']
- **Adopted elements**: ['掩码补全范式', '非自回归并行生成思想']

## R3: Genie series
- **DOI**: None
- **Type**: 交互生成环境
- **Delta**:
  - What changed: 论文用 Genie 系列说明从可控环境到实时 text-to-world 体验的进展，同时指出长期一致性仍远未达到持久世界。
  - Why: 这些工作体现了交互闭环的重要性，也暴露了缺少专门记忆和状态管理时的遗忘与漂移问题。
- **Claims affected**: ['C2', 'C3']
- **Adopted elements**: ['action-conditioned generation', '实时交互世界体验']

## R4: RETRO
- **DOI**: None
- **Type**: 外部化记忆
- **Delta**:
  - What changed: 论文将 RETRO 放在外部检索记忆路线中，强调通过检索大规模语料片段扩展有效上下文并保持证据可追踪。
  - Why: 外部化记忆展示了知识可编辑、可更新和可追踪的方向，是持久世界记忆系统的一种候选机制。
- **Claims affected**: ['C3']
- **Adopted elements**: ['检索增强记忆', '可追踪证据']

## R5: FramePack
- **DOI**: None
- **Type**: 视频一致性调控
- **Delta**:
  - What changed: 论文将 FramePack 描述为通过关键帧锚定和上下文压缩降低长视频 rollout 漂移的方法。
  - Why: 它直接对应论文关于持久性需要记忆策略和一致性规训的论点。
- **Claims affected**: ['C3']
- **Adopted elements**: ['关键帧锚定', '上下文压缩']
