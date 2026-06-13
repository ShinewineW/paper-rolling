# Related Work

## R1: Ha and Schmidhuber, 2018; Oh et al., 2015; Hafner et al., 2020, 2021; Micheli et al., 2023; Robine et al., 2023
- **DOI**: 
- **Type**: World Models
- **Delta**:
  - What changed: 已有 World Models 通常做 action-conditioned next-frame prediction，并可用于 agent training；Genie 改为从 videos alone 无监督学习可控 world model。
  - Why: 这一区别支撑 C1：Genie 的关键新意不是简单预测视频，而是在没有 action-conditioned data 的训练条件下形成 frame-level controllability。
- **Claims affected**: ['C1']
- **Adopted elements**: ['next-frame prediction', 'action-conditioned world model framing', 'agent training motivation']

## R2: Villegas et al., 2023; Yan et al., 2023; Gupta et al., 2023; Chang et al., 2022; Xu et al., 2020
- **DOI**: 
- **Type**: Video Models
- **Delta**:
  - What changed: Genie 继承 transformer-based video generation 中的 tokenized images、MaskGIT 与 ST-Transformer 思路，但显式学习 latent action space，使用户或 agents 能 play the model。
  - Why: 这解释了 C3 和 C5 的技术来源：ST-ViViT 与 MaskGIT dynamics model 是扩展 video model 到 interactive environment 的关键组件。
- **Claims affected**: ['C3', 'C5']
- **Adopted elements**: ['MaskGIT', 'ST-Transformer', 'tokenized video generation']

## R3: Menapace et al., 2021, 2022
- **DOI**: 
- **Type**: Playable Video Generation
- **Delta**:
  - What changed: PVG 使用 latent actions 控制从视频学习的 world models；Genie 将目标扩展到通过 prompting 生成 entirely new environments，并减少 domain-specific static examples 的限制。
  - Why: 这直接关联 C1 与 C7：Genie 将 playable video generation 的控制思想推广到更通用的视频-only 生成式交互环境。
- **Claims affected**: ['C1', 'C7']
- **Adopted elements**: ['latent actions for controllable video', 'playable generation framing']

## R4: Baker et al., 2022; Torabi et al., 2018; Edwards et al., 2019; Ye et al., 2022
- **DOI**: 
- **Type**: Training agents with latent actions
- **Delta**:
  - What changed: VPT 等方法用 ground-truth action labeled data 或 observation-only imitation 训练策略；Genie 使用完全离线从 Internet videos 学到的 latent actions 来为 unseen videos 推断策略。
  - Why: 这支撑 C6：论文强调 latent-to-real mapping 不包含当前 observation 信息，因此迁移依赖 latent actions 的一致性。
- **Claims affected**: ['C6']
- **Adopted elements**: ['imitation from observation', 'inverse dynamics style labeling', 'latent action policy training']

## R5: Brohan et al., 2023; Yang et al., 2023; Kalashnikov et al., 2018
- **DOI**: 
- **Type**: Robotics world models
- **Delta**:
  - What changed: RT1、UniSim 与 QT-Opt 相关数据和方法提供 robotic manipulation 场景背景；Genie 在 Robotics videos 中不使用 actions，仅把数据当作视频学习可控 dynamics。
  - Why: 这支持 C7 的跨域论证：同一 video-only latent action 方法可用于 robotics，而不是只适用于 Platformers。
- **Claims affected**: ['C7']
- **Adopted elements**: ['Robotics dataset setting', 'robot manipulation evaluation context']
