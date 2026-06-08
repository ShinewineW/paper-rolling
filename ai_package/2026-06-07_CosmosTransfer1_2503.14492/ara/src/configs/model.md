## 基础世界模型
- **Value**: Cosmos-Predict1-7B-Video2World（7B 参数，DiT 架构）
- **Rationale**: 在预训练世界模型基础上进行 post-training，复用其强大的视频生成先验；AV 版本则从 Cosmos-Predict1-7B-Video2World-Sample-AV 出发
- **Search range**: N/A
- **Sensitivity**: high
- **Source**: Sec 4

## 每个控制分支中的条件 Transformer 块数量
- **Value**: 3
- **Rationale**: 经实验验证在控制效果与推理效率之间取得良好平衡（论文原文：empirically offers a good balance）
- **Search range**: 论文未明确给出其他配置的对比
- **Sensitivity**: medium
- **Source**: Sec 2

## 控制分支与主干分支的连接方式
- **Value**: 控制分支输出经零初始化线性层后逐元素加至主干分支对应 Transformer 块的激活
- **Rationale**: 零初始化确保训练初始时控制分支对主干无干扰；线性层提供灵活的输出缩放
- **Search range**: N/A
- **Sensitivity**: high
- **Source**: Sec 2

## 单次推理输出规格
- **Value**: 5 秒，1280×704p，24 fps，56K tokens
- **Rationale**: 继承 Cosmos-Predict1-7B-Video2World 的生成规格，面向 Physical AI 应用场景
- **Search range**: N/A
- **Sensitivity**: medium
- **Source**: Sec 4

## 注意力头数量
- **Value**: 32
- **Rationale**: 模型架构参数，决定推理并行时头并行的最大 GPU 分配粒度（正负条件各占一半，最多可分配至 64 GPU）
- **Search range**: N/A
- **Sensitivity**: medium
- **Source**: Sec 6

## 时空控制图（spatiotemporal control map）形状
- **Value**: $$\mathbf{w} \in \mathbb{R}^{N \times X \times Y \times T}$$，N 为模态数，X/Y/T 为视频宽高帧数
- **Rationale**: 对每个模态、每个空间位置、每个时间帧独立指定权重，实现精细自适应控制；多模态权重之和超过 1 时自动归一化
- **Search range**: [0, 1]（归一化后）
- **Sensitivity**: high
- **Source**: Sec 3

## 4KUpscaler 推理分块策略
- **Value**: 将 4K 输出划分为 3×3 网格，相邻网格设有重叠区域，去噪步骤中各网格输出在重叠区域取平均
- **Rationale**: 保证输出视频在网格边界处的无缝连续性，避免拼接伪影
- **Search range**: N/A
- **Sensitivity**: medium
- **Source**: Sec 4

## 均匀多模态融合基线每模态权重
- **Value**: 0.25（4 个模态等权）
- **Rationale**: 作为多模态融合实验的基线配置，与单模态（权重 1.0）及自适应时空权重方案进行对比
- **Search range**: 0–1
- **Sensitivity**: high
- **Source**: Sec 5.1
