# Related Work

## R1: Cam4DOcc (Ma et al. 2024b)
- **DOI**: 
- **Type**: benchmark_and_baseline
- **Delta**:
  - What changed: 论文将Cam4DOcc作为相机4D占用预测基准，并在其膨胀GMO、细粒度GMO和流预测任务上比较Drive-OccWorld。
  - Why: Cam4DOcc提供顺序占用状态和3D backward centripetal flow，是本文主实验最直接的占用预测参照。
- **Claims affected**: ['C1']
- **Adopted elements**: ['4D occupancy forecasting benchmark', '3D backward centripetal flow', 'mIoU与VPQ评估']

## R2: Drive-WM (Wang et al. 2024b)
- **DOI**: 
- **Type**: planning_world_model
- **Delta**:
  - What changed: 论文指出Drive-WM使用生成驾驶视频和image-based reward function规划轨迹，而本文转向利用未来占用预测中的几何3D结构进行规划。
  - Why: 该差异支撑本文将世界模型生成能力和occupancy-based planner结合的动机。
- **Claims affected**: ['C3']
- **Adopted elements**: ['world model for planning的任务设定', '与规划方法的比较']

## R3: ST-P3 (Hu et al. 2022)
- **DOI**: 
- **Type**: planning_cost_and_loss
- **Delta**:
  - What changed: 论文借鉴ST-P3的learned-volume cost和max-margin planning loss，并将其放入基于未来占用的规划框架。
  - Why: ST-P3提供可微占用表示和安全轨迹代价的规划思想，是本文occupancy-based cost function的重要来源。
- **Claims affected**: ['C3']
- **Adopted elements**: ['learned-volume cost', 'max-margin loss', '规划评估协议']

## R4: UniAD (Hu et al. 2023b)
- **DOI**: 
- **Type**: end_to_end_planning_baseline
- **Delta**:
  - What changed: 论文使用UniAD作为规划基线，并按其相关协议报告NoAvg和TemAvg规划结果。
  - Why: UniAD是规划导向端到端模型代表，能检验Drive-OccWorldP在同类开放环规划评估中的相对表现。
- **Claims affected**: ['C3']
- **Adopted elements**: ['end-to-end planning baseline', 'NoAvg与TemAvg协议参照']

## R5: OccWorld (Zheng et al. 2023) and OccSora (Wang et al. 2024a)
- **DOI**: 
- **Type**: 3d_volume_world_model
- **Delta**:
  - What changed: 论文将这类3D volume-based world model作为相关工作背景，本文进一步注入动作条件并面向端到端规划。
  - Why: 这些工作说明未来状态可用occupancy形式生成，但本文强调action-controllable generation和planning integration。
- **Claims affected**: ['C1', 'C2', 'C3']
- **Adopted elements**: ['occupancy形式的未来状态建模']
