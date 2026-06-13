# Related Work

## R1: LAW [18]
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: LAW 通过 latent world model 进行自监督表征学习并减少对感知标注的依赖；World4Drive 在此基础上引入意图感知世界模型、空间语义先验和 world model selector。
  - Why: 论文指出 LAW 的单模态 latent feature 难以捕获 spatial-semantic scene information 和 multi-modal driving intentions，导致收敛慢和性能不足。
- **Claims affected**: ['C1', 'C3', 'C4']
- **Adopted elements**: ['latent world model', 'self-supervised learning', 'perception annotation-free planning']

## R2: VADv2 [3]
- **DOI**: 
- **Type**: related_method
- **Delta**:
  - What changed: VADv2 将 driving intentions 纳入 probabilistic planning；World4Drive 使用 trajectory vocabulary 提取多模态 driving intention 并与 latent world model 耦合。
  - Why: 论文将 driving intention uncertainty 作为规划问题中的关键因素，并在自身方法中用 intention encoder 和 world model selector 处理多模态意图。
- **Claims affected**: ['C3']
- **Adopted elements**: ['trajectory vocabulary', 'driving intentions']

## R3: Metric3D v2 [11]
- **DOI**: 
- **Type**: dependency
- **Delta**:
  - What changed: World4Drive 使用 Metric3D v2 的 giant model 进行 depth estimation，为 Physical World Latent Encoding 提供 3D spatial encoding。
  - Why: 论文认为 scale-aware depth 能为每个像素提供物理世界中的位置信息，从而增强空间理解。
- **Claims affected**: ['C3', 'C5']
- **Adopted elements**: ['metric depth estimation', '3D spatial encoding']

## R4: Grounded-SAM [31]
- **DOI**: 
- **Type**: dependency
- **Delta**:
  - What changed: World4Drive 使用 Grounded-SAM 生成 pseudo semantic labels，并用 cross-entropy loss 增强 latent representations 的语义理解。
  - Why: 论文将 open-vocabulary semantic supervision 作为 physical world latent representation 的语义先验来源。
- **Claims affected**: ['C3']
- **Adopted elements**: ['pseudo semantic labels', 'semantic segmentation']

## R5: DiffusionDrive [23]
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: DiffusionDrive 是 NavSim 表中包含 camera 和 lidar 输入的强基线；World4Drive 在 camera 输入下与其比较闭环指标。
  - Why: 论文说明 World4Drive 的闭环指标超过其他需要感知标注的方法，但 DiffusionDrive 是例外。
- **Claims affected**: ['C2']
- **Adopted elements**: []
