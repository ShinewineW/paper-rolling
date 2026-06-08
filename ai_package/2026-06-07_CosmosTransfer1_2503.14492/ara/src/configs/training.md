## 控制分支训练 GPU 数量
- **Value**: 每模态 1024 块 NVIDIA H100 GPU
- **Rationale**: 大规模视频世界模型训练对算力的刚性需求，确保模型在合理时间内收敛
- **Search range**: 论文未给出替代配置
- **Sensitivity**: high
- **Source**: Sec 4

## 每模态控制分支训练时长
- **Value**: 2 至 4 周（依模态复杂度而定）
- **Rationale**: 不同模态（Blur/Edge/Depth/Seg/LiDAR/HDMap）的学习难度和收敛速度存在差异
- **Search range**: 2–4 weeks
- **Sensitivity**: medium
- **Source**: Sec 4

## 控制分支训练策略
- **Value**: 各控制分支独立分别训练，仅在推理时融合
- **Rationale**: 内存高效（每次仅需将一个控制分支载入内存）；允许不同模态使用异构数据集；可在推理时灵活增减模态
- **Search range**: 联合训练所有分支（论文以内存效率为由否定）
- **Sensitivity**: high
- **Source**: Sec 3

## 基模型权重冻结策略
- **Value**: 训练控制分支期间 Cosmos-Predict1-7B 基模型权重完全冻结
- **Rationale**: 保留预训练世界模型的生成能力，避免破坏其已学习的视频生成先验
- **Search range**: N/A
- **Sensitivity**: high
- **Source**: Sec 2

## 提示上采样器训练基座模型
- **Value**: Pixtral-12B（在目标数据上微调）
- **Rationale**: 多模态视觉-语言模型，能同时理解条件视频帧（分割图/深度图等）与短文本提示，将其扩展为结构化长描述
- **Search range**: 论文未给出替代模型
- **Sensitivity**: medium
- **Source**: Appendix A

## 提示上采样器训练数据规模与训练轮次
- **Value**: 每模态 100 万条视频，多模态联合训练 1 个 epoch，使用 FSDP2
- **Rationale**: 覆盖各模态分布差异，使上采样器具备跨模态理解与提示生成能力
- **Search range**: 论文未给出替代值
- **Sensitivity**: medium
- **Source**: Appendix A

## 自动驾驶专项数据集（RDS-HQ）规模
- **Value**: 65K 条 20 秒环视视频（约 360 小时），10 Hz LiDAR 扫描，NVIDIA 驾驶平台采集
- **Rationale**: 自动驾驶场景需专域高质量数据，RDS-HQ 附带 HD 地图和 3D 包围框标注，用于训练 Cosmos-Transfer1-7B-Sample-AV 的 HDMap 与 LiDAR 控制分支
- **Search range**: N/A
- **Sensitivity**: high
- **Source**: Sec 4

## 提示上采样器训练数据生成辅助模型
- **Value**: Gemma-2-9B-it（生成多样化短提示作为训练对的输入侧）
- **Rationale**: 利用已有训练长提示，通过 Gemma-2-9B-it 反向生成多样化短提示，构建配对训练数据
- **Search range**: 论文未给出替代模型
- **Sensitivity**: low
- **Source**: Appendix A
