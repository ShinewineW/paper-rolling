# Related Work

## R1: π0.5
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: 本文沿用 π 系列中 flow action modeling 和 blockwise causal attention 的思路，并在更大规模真实世界多 embodiment 数据与深度蒸馏设置下评估。
  - Why: π0.5 是真实世界与仿真评估中的核心 VLA 基线。
- **Claims affected**: ['C1', 'C2', 'C3']
- **Adopted elements**: ['flow action modeling', 'blockwise causal attention', 'public pretrained checkpoints']

## R2: GR00T N1.6
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: 本文将 GR00T N1.6 纳入相同后训练与真实机器人评估协议，比较其在不同 embodiment 上的适应性。
  - Why: 该方法代表通用 humanoid robot foundation model 基线。
- **Claims affected**: ['C1']
- **Adopted elements**: ['public pretrained checkpoints', 'same post-training pipeline']

## R3: GM-100
- **DOI**: 
- **Type**: benchmark
- **Delta**:
  - What changed: 本文使用 GM-100 作为真实世界任务基准，并扩展为多平台、同协议的系统评估。
  - Why: 该基准提供细粒度任务集合，用于检验真实操作中的任务完成和分步进展。
- **Claims affected**: ['C1', 'C2', 'C4']
- **Adopted elements**: ['GM-100 task specifications', 'SR', 'PS']

## R4: RoboTwin 2.0
- **DOI**: 
- **Type**: benchmark
- **Delta**:
  - What changed: 本文在 RoboTwin 2.0 clean 与 randomized 设置下验证仿真多任务泛化。
  - Why: 该基准提供带强随机化的双臂仿真操作评估。
- **Claims affected**: ['C3']
- **Adopted elements**: ['clean setting', 'randomized setting']

## R5: Flow Matching
- **DOI**: 
- **Type**: method
- **Delta**:
  - What changed: 本文使用 Flow Matching 对连续 action chunk 建模，训练 action expert 预测条件向量场。
  - Why: 该方法支持连续动作生成，契合机器人轨迹控制。
- **Claims affected**: ['C1', 'C3']
- **Adopted elements**: ['Flow Matching objective']

## R6: LingBot-Depth
- **DOI**: 
- **Type**: method
- **Delta**:
  - What changed: 本文用 LingBot-Depth token 对齐 VLM learnable queries，将深度相关空间信息注入 VLA。
  - Why: 深度蒸馏是 w/ depth 变体与 w/o depth 变体的关键差异。
- **Claims affected**: ['C2', 'C3']
- **Adopted elements**: ['depth tokens', 'learnable query alignment']

## R7: StarVLA、Dexbotic、OpenPI
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: 本文把这些 VLA 训练代码库作为吞吐分析基线，并复现标准化 π-like 架构进行对比。
  - Why: 它们代表现有 VLA-oriented codebases，用于定位训练效率改进。
- **Claims affected**: ['C5']
- **Adopted elements**: ['training codebase comparison', 'sample throughput metric']
