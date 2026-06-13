# Related Work

## R1: DriveTransformer
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: ORION在Bench2Drive闭环主结果中以VLM推理指导生成式轨迹规划，而DriveTransformer作为主要SOTA闭环基线被用于对比。
  - Why: 该对比用于证明ORION在复杂闭环交互场景中的优势。
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['Bench2Drive闭环评测', 'NC条件', '相机模态对比']

## R2: DriveAdapter
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: DriveAdapter使用专家特征蒸馏并结合camera与LiDAR输入；ORION仅用相机与NC条件进行对比，并在部分能力上仍存在短板。
  - Why: 该对比用于同时展示ORION的整体优势和变道相关局限。
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['闭环基线比较', 'Multi-Ability分项分析']

## R3: VAD
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: VAD作为经典E2E模型和dual-system范式中的代表，用于说明仅用经典E2E轨迹模块承接VLM接口可能受限。
  - Why: 论文借此支撑需要直接对齐推理空间与动作空间的设计动机。
- **Claims affected**: ['C4']
- **Adopted elements**: ['dual-system范式参照', 'NC条件闭环对比']

## R4: OmniDrive
- **DOI**: 
- **Type**: method
- **Delta**:
  - What changed: ORION借鉴Q-Former风格的视觉特征压缩思路，并扩展为QT-Former以处理长期历史上下文。
  - Why: 该关系用于说明QT-Former不是简单多帧拼接，而是通过查询与Memory Bank进行时间信息聚合。
- **Claims affected**: ['C4', 'C5', 'C7']
- **Adopted elements**: ['Q-Former风格结构', 'nuScenes替换设置参照']

## R5: GenAD
- **DOI**: 
- **Type**: method
- **Delta**:
  - What changed: ORION使用GenAD中的GRU decoder解码轨迹，但VAE在本文中用于连接单个推理空间planning token与动作空间。
  - Why: 该差异用于界定ORION生成式规划器的功能重点是reasoning-action alignment。
- **Claims affected**: ['C3']
- **Adopted elements**: ['GRU decoder', '多模态轨迹生成参照']

## R6: Qwen2VL
- **DOI**: 
- **Type**: tooling
- **Delta**:
  - What changed: 论文使用Qwen2VL自动生成Chat-B2D的VQA标注，再将其用于ORION的VQA与规划联合训练。
  - Why: 该流程为辅助VQA训练和联合训练有效性提供数据来源。
- **Claims affected**: ['C6']
- **Adopted elements**: ['自动VQA标注', 'Chat-B2D生成流程']
