# Related Work

## R1: Zhao et al. [62]
- **DOI**: 
- **Type**: world model
- **Delta**:
  - What changed: PWM 共同预测 states 和 actions，并提供 Dynamic Focal Loss 与 bi-directional intra-frame attention 的直接背景；本文进一步把 future frames 与 ego actions 按步骤交错生成，使规划持续依赖新预测的视觉状态。
  - Why: 论文将 PWM 作为初始化来源和关键相关范式，同时将其作为 NAVSIM 世界模型基线比较。
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['PWM', 'Dynamic Focal Loss', 'bi-directional intra-frame attention']

## R2: Lin et al. [34]
- **DOI**: 
- **Type**: depth foundation model
- **Delta**:
  - What changed: Depth Anything 3 被用于从输入图像提取 monocular depth maps；本文将 depth features 通过 CDE、DDE 与 cross-attention 融入历史视觉 token，而不是显式生成未来 depth。
  - Why: 该工作为本文 depth-informed conditioning 提供几何先验来源，支撑 depth fusion 的消融主张。
- **Claims affected**: ['C3']
- **Adopted elements**: ['Depth Anything 3', 'monocular depth maps']

## R3: Chen et al. [7]
- **DOI**: 
- **Type**: driving world model
- **Delta**:
  - What changed: DrivingGPT 统一 driving world modeling and planning；本文在相关基线上进一步强调 interleaved prediction-planning，而不是只进行统一建模或先预测后规划。
  - Why: DrivingGPT 同时出现在规划和视频生成比较中，是评估 Uni-World VLA 联合规划与生成能力的重要参照。
- **Claims affected**: ['C1']
- **Adopted elements**: []

## R4: Li et al. [26]
- **DOI**: 
- **Type**: imagination-and-planning framework
- **Delta**:
  - What changed: ImagiDrive 属于将想象与规划结合的相关方向；本文改为 step-wise interleaving，使动作在每个预测时刻与视觉状态交替产生。
  - Why: 该工作代表 predict-then-plan 相关范式，帮助界定本文针对 open-loop imagination 的改动。
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: []

## R5: Zhang et al. [60]
- **DOI**: 
- **Type**: world model baseline
- **Delta**:
  - What changed: ResWorld 使用 temporal residual world model 并在表中作为强基线；本文以 single-view camera-only 设计达到更高综合规划表现。
  - Why: 该基线在主表中接近本文方法，突出 Uni-World VLA 在输入模态更少时的整体竞争力。
- **Claims affected**: ['C1']
- **Adopted elements**: []
