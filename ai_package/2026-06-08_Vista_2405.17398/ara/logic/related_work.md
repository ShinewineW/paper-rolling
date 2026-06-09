# Related Work

## R1: Blattmann et al., 2023 [5]
- **DOI**: arXiv:2311.15127
- **Type**: pretrained_base
- **Delta**:
  - What changed: Vista 以 SVD（Stable Video Diffusion）为基础架构，将第一帧预测强制锁定为条件图像、禁用噪声增强、引入动态先验潜在替换、添加动态增强损失与结构保留损失，并新增行动控制投影层与 LoRA 适配器
  - Why: SVD 具备高质量图像到视频生成能力及大规模预训练权重，但缺乏预测对齐、行动可控性和驾驶场景动态建模能力
- **Claims affected**: ['C1', 'C2', 'C3', 'C4', 'C5']
- **Adopted elements**: ['UNet 去噪架构', 'EDM 扩散框架', '连续时间步公式', '潜在视频扩散训练目标']

## R2: Hu et al., 2023 [54]
- **DOI**: arXiv:2309.17080
- **Type**: competitor
- **Delta**:
  - What changed: GAIA-1 使用自回归 Transformer 建模驾驶视频；Vista 改用扩散框架，支持多模态行动控制，并以更高时空分辨率（576×1024，10 Hz）运行
  - Why: GAIA-1 是代表性大规模驾驶世界模型，但仅支持命令输入，不支持轨迹、目标点或角度/速度等细粒度控制
- **Claims affected**: ['C6']
- **Adopted elements**: []

## R3: Wang et al., 2024 [127]
- **DOI**: CVPR 2024
- **Type**: competitor
- **Delta**:
  - What changed: Drive-WM 使用外部感知检测器（BEVFormer、MapTR）构建奖励函数；Vista 直接利用自身预测不确定性作为奖励源，无需外部模型，泛化能力更强
  - Why: Drive-WM 是使用奖励模块评估驾驶动作的代表性工作，但其奖励依赖特定数据集训练的检测器，限制了跨场景泛化
- **Claims affected**: ['C7']
- **Adopted elements**: []

## R4: Yang et al., 2024 [136]
- **DOI**: CVPR 2024
- **Type**: baseline_and_dataset
- **Delta**:
  - What changed: Vista 以 GenAD 提出的 OpenDV-YouTube 数据集为训练数据基础，但引入动态增强损失、结构保留损失及多模态行动控制，并以更高帧率（10 Hz）和分辨率（576×1024）运行
  - Why: OpenDV-YouTube 是最大规模的公开驾驶视频数据集，有助于提升跨域泛化能力；GenAD 也是 nuScenes 上的最优竞争基线
- **Claims affected**: ['C1', 'C6']
- **Adopted elements**: ['OpenDV-YouTube 数据集', '逆动力学模型（IDM）用于行动控制评估']

## R5: Hu et al., 2022 [55]
- **DOI**: ICLR 2022
- **Type**: method_component
- **Delta**:
  - What changed: Vista 在行动控制学习阶段对 UNet 所有注意力块引入 LoRA 低秩适配器（秩设置为 16），避免在低分辨率微调时破坏预训练高保真预测能力
  - Why: 完全冻结 UNet 权重仅训练新增投影层会导致质量下降；完全解冻则破坏预训练能力；LoRA 提供了在固定预训练权重基础上高效适应的折中方案
- **Claims affected**: ['C5', 'C6']
- **Adopted elements**: ['LoRA 低秩适配，秩设置为 16，部署在所有注意力块']
