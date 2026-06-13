# Related Work

## R1: Qwen3-VL
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: 论文把 Qwen3-VL 作为理解与初始化相关基线，并与 Cosmos 3 Reasoner 或 Cosmos 3 变体进行对照。
  - Why: 该对比用于说明 Cosmos 3 Reasoner 初始化和全模型在 Physical AI 相关 domain score 上的作用。
- **Claims affected**: ['C1', 'C4']
- **Adopted elements**: ['作为比较基线', '作为 understanding tower ablation 的替代初始化']

## R2: Wan2.2-A14B
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: 论文将 Wan2.2-A14B 纳入视频生成、HUE、PAIBench-G 和 Physics-IQ 等生成评测。
  - Why: 该基线帮助定位 Cosmos 3 Generator 相对强开放视频模型的表现。
- **Claims affected**: ['C2']
- **Adopted elements**: ['作为开放生成基线']

## R3: Cosmos-Predict2.5
- **DOI**: 
- **Type**: prior_system
- **Delta**:
  - What changed: 论文把 Cosmos-Predict2.5 系列作为视频生成和 HUE 对比对象，展示 Cosmos 3 相对前序 Cosmos 系统的变化。
  - Why: 该比较用于说明 Cosmos 3 在统一 omnimodal 框架下相对既有 world simulation 模型的增量。
- **Claims affected**: ['C2']
- **Adopted elements**: ['作为 Cosmos 系列前序基线']

## R4: Cosmos-Transfer2.5
- **DOI**: 
- **Type**: prior_system
- **Delta**:
  - What changed: 论文在条件生成控制评测中使用 Cosmos-Transfer2.5 作为对比。
  - Why: 该对比用于检验 Cosmos 3 在 transfer generation 和控制一致性上的表现。
- **Claims affected**: ['C2']
- **Adopted elements**: ['作为控制生成基线']

## R5: π0.5
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: 论文在机器人 policy 结果总览和 RoboLab 相关对比中纳入 π0.5。
  - Why: 该基线用于评估 Cosmos3-Nano-Policy-DROID 在机器人策略任务上的相对表现。
- **Claims affected**: ['C3']
- **Adopted elements**: ['作为机器人 policy 基线']
