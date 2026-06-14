# Related Work

## R1: DriveVLA-W0 [3]
- **DOI**: 未提供
- **Type**: VLA-based driving policy with world-model component
- **Delta**:
  - What changed: DriveVLA-W0 将 generative world-model components 加入 VLM-based policy，但论文指出其 policy core 仍是 VLM-centric；DriveWAM 改为继承 pretrained video generative model 作为 policy core。
  - Why: 这一差异支撑 DriveWAM 将视频生成先验放在策略骨干中的设计动机。
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['对比 VLA-based policies', '保留高层语义 reasoning 的互补作用']

## R2: DriveDreamer-Policy [14]
- **DOI**: 未提供
- **Type**: VLA pipeline with visual world modeling
- **Delta**:
  - What changed: DriveDreamer-Policy 使用 world-model components 辅助 VLM-based policy；DriveWAM 将未来世界演化与 ego actions 作为统一视频动作生成问题建模。
  - Why: 该对比说明 DriveWAM 不是把视觉生成作为辅助分支，而是把视频生成骨干作为端到端策略核心。
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['世界模型辅助规划的任务动机', '与 VLA-based methods 的 benchmark 对比']

## R3: WorldDrive [22]
- **DOI**: 未提供
- **Type**: driving-oriented world-action baseline
- **Delta**:
  - What changed: WorldDrive 将 driving world model 学到的表示转移到下游 planner，仍保留 separate planner；DriveWAM 直接把 pretrained video diffusion transformer 改造成统一 video-action policy backbone。
  - Why: 该差异支撑 DriveWAM 对端到端 WA policy 的贡献表述。
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['WA-based benchmark baseline', 'scene generation 与 planning 结合的问题设定']

## R4: VaViM/VaVAM [23]
- **DOI**: 未提供
- **Type**: autoregressive video modeling for autonomous driving
- **Delta**:
  - What changed: VaViM/VaVAM 使用 discrete VQ-VAE tokens 和 GPT-style transformer，并扩展 action expert；DriveWAM 直接构建在 pretrained video diffusion transformer 上，并用 unified flow-matching objective 适配视频与动作流。
  - Why: 该对比说明 DriveWAM 避免依赖离散视频 tokenizer 和定制生成架构，从而更直接继承视频生成先验。
- **Claims affected**: ['C2', 'C5']
- **Adopted elements**: ['PhysicalAI-Autonomous-Vehicles baseline', 'autoregressive video-action framing']

## R5: Epona [24]
- **DOI**: 未提供
- **Type**: autoregressive diffusion world model for autonomous driving
- **Delta**:
  - What changed: Epona 使用 spatiotemporal transformer 与 twin diffusion transformers 分别处理 next-frame generation 和 ego-trajectory prediction；DriveWAM 使用共享 transformer 进行 future video latents 与 action chunk 建模。
  - Why: 该对比突出 DriveWAM 的统一视频动作骨干和联合监督设计。
- **Claims affected**: ['C1', 'C5']
- **Adopted elements**: ['WA-based NAVSIM baseline', '自回归世界模型任务设定']

## R6: FlowCache [26]
- **DOI**: 未提供
- **Type**: efficient autoregressive video generation caching
- **Delta**:
  - What changed: FlowCache 提供 relevance-redundancy cache selection 思路；DriveWAM 将该准则适配为 modality-aware 的 video 与 action KV memory pools，用于 driving long-horizon rollout。
  - Why: 该继承关系解释 selective KV memory 的算法来源，也支撑其与 FIFO、Full cache 的消融设计。
- **Claims affected**: ['C6']
- **Adopted elements**: ['relevance-redundancy criterion', 'bounded inference-time cache selection']

## R7: Qwen3-VL-8B [9]
- **DOI**: 未提供
- **Type**: frozen VLM guidance source
- **Delta**:
  - What changed: DriveWAM 使用 frozen Qwen3-VL-8B 生成 chunk-specific semantic intent，而不是把 VLM 作为主 policy backbone。
  - Why: 该设计把高层场景理解与视频生成先验分工，支撑 scene-evolving guidance 的消融。
- **Claims affected**: ['C3', 'C7']
- **Adopted elements**: ['chunk-specific guidance generation', 'dataset curation tagging']

## R8: Causal World Modeling for Robot Control [19]
- **DOI**: 未提供
- **Type**: world-action modeling code and checkpoint basis
- **Delta**:
  - What changed: DriveWAM 基于 [19] 的代码框架，并从其 released base checkpoint 初始化，同时将方法转向 autonomous driving 的 video-action policy。
  - Why: 该依赖为 DriveWAM 的实现基础、noisy-history augmentation 和 inference solver 设置提供来源。
- **Claims affected**: ['C5', 'C7']
- **Adopted elements**: ['code framework', 'base checkpoint', 'noisy-history augmentation', 'Euler ODE solver setting']
