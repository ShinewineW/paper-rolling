# Related Work

## R1: Baker et al. 2022, Video pretraining (vpt): Learning to act by watching unlabeled online videos
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: VPT 使用 contractor gameplay 训练 action labeler，并用合成 mouse 和 keyboard actions 标注网页视频；本文改为只使用 VPT contractor dataset 进行离线训练，并在同类低层键鼠动作设置下评估 Dreamer 4。
  - Why: 该对比界定了 Dreamer 4 的离线数据效率和相对 VPT offline agent 的改进。
- **Claims affected**: ['C1', 'C5']
- **Adopted elements**: ['VPT evaluation protocol', 'VPT contractor dataset', 'mouse and keyboard action processing']

## R2: Hafner et al. 2025, Mastering diverse control tasks through world models
- **DOI**: 
- **Type**: prior_method
- **Delta**:
  - What changed: Dreamer 3 从在线交互中学习 Minecraft 钻石任务，并使用 RSSM 世界模型；Dreamer 4 转向可扩展 transformer 世界模型、shortcut forcing objective 和离线想象训练。
  - Why: 该对比说明本文将 Dreamer 系列从在线交互控制扩展到复杂离线 Minecraft 设置。
- **Claims affected**: ['C1', 'C5']
- **Adopted elements**: ['world model agent paradigm', 'value learning from imagined trajectories']

## R3: Chen et al. 2024, Diffusion forcing: Next-token prediction meets full-sequence diffusion
- **DOI**: 
- **Type**: method_foundation
- **Delta**:
  - What changed: 本文基于 diffusion forcing 的序列建模思想，但加入 shortcut forcing、x-space prediction 和 ramp loss weight，以支持少量 forward passes 的交互式长 rollout。
  - Why: 该变化直接服务于世界模型的快速推理和减少长期生成误差。
- **Claims affected**: ['C4']
- **Adopted elements**: ['diffusion forcing for sequential data']

## R4: Frans et al. 2025, One step diffusion via shortcut models
- **DOI**: 
- **Type**: method_foundation
- **Delta**:
  - What changed: Shortcut models 通过同时条件化 signal level 和 step size 支持快速采样；本文将该思想用于动作条件化世界模型，并结合 x-space 目标和 transformer 架构。
  - Why: 该方法基础解释了为什么 Dreamer 4 可以用较少采样步进行交互式生成。
- **Claims affected**: ['C2', 'C4']
- **Adopted elements**: ['shortcut conditioning on signal level and step size']

## R5: Seid and Hojel 2024, Lucid v1: Real-tiem latent world models
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: Lucid-v1 是 Minecraft 交互式世界模型基线；本文用人工交互任务展示 Dreamer 4 在复杂物体交互和游戏机制上的优势。
  - Why: 该比较支撑 Dreamer 4 相对先前 Minecraft 世界模型的改进主张。
- **Claims affected**: ['C2']
- **Adopted elements**: []

## R6: Guo et al. 2025, Mineworld: a real-time and open-source interactive world model on minecraft
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: MineWorld 学习 Minecraft simulator，但论文指出其交互推理限制使其不适合本文需要大量连续动作的人工任务评估。
  - Why: 该工作提供了 Minecraft 世界模型的相关基线，并凸显交互式推理速度对评估和想象训练的重要性。
- **Claims affected**: ['C2']
- **Adopted elements**: []
