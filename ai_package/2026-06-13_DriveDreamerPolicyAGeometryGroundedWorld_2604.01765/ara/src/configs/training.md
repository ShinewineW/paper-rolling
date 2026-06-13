## 训练数据
- **Value**: Navsim training data；不使用额外数据集，除初始化骨干外不做额外预训练
- **Rationale**: 保持训练来源与论文实验设置一致，避免额外数据带来的比较偏差。
- **Search range**: 论文未报告可选范围。
- **Sensitivity**: 高；额外数据或额外预训练会改变公平性与泛化来源。
- **Source**: Sec 4.1 Implementation Details

## 训练阶段
- **Value**: single stage
- **Rationale**: 所有组件以联合多任务方式训练，避免分阶段接口漂移。
- **Search range**: 论文未报告分阶段替代设置。
- **Sensitivity**: 中；分阶段训练可能改变深度、视频、动作分支之间的协同。
- **Source**: Sec 3.3；Sec 4.1 Implementation Details

## 训练步数
- **Value**: 100k steps
- **Rationale**: 论文实现细节给出的默认训练预算。
- **Search range**: 论文未报告其他步数范围。
- **Sensitivity**: 中；训练不足可能影响生成和规划，过长训练的收益未在论文中报告。
- **Source**: Sec 4.1 Implementation Details

## 批大小
- **Value**: 32
- **Rationale**: 论文实现细节给出的默认 batch size。
- **Search range**: 论文未报告其他 batch size。
- **Sensitivity**: 中；会影响优化稳定性和显存需求。
- **Source**: Sec 4.1 Implementation Details

## 优化器
- **Value**: AdamW
- **Rationale**: 用于联合训练 DriveDreamer-Policy。
- **Search range**: 论文未报告其他优化器。
- **Sensitivity**: 中；优化器改变可能影响联合多任务收敛。
- **Source**: Sec 4.1 Implementation Details

## 学习率
- **Value**: $1 \times 1 0 ^ { - 5 }$
- **Rationale**: 论文实现细节给出的默认 learning rate。
- **Search range**: 论文未报告学习率扫描。
- **Sensitivity**: 高；联合训练包含 LLM 接口和扩散专家，学习率过大或过小都可能影响稳定性。
- **Source**: Sec 4.1 Implementation Details

## 联合多任务损失
- **Value**: $\mathcal { L } = \lambda _ { d } \mathcal { L } _ { d } + \lambda _ { v } \mathcal { L } _ { v } + \lambda _ { a } \mathcal { L } _ { a } ,\tag{3}$；$\lambda _ { d } = 0 .$ 1，其余超参数默认 1.0
- **Rationale**: 将 depth prediction、video prediction 和 trajectory prediction 联合优化。
- **Search range**: 论文未报告其他权重范围。
- **Sensitivity**: 高；深度权重会改变几何监督相对动作和视频任务的影响。
- **Source**: Sec 3.3 Training Objective and Optimization

## 深度标签来源
- **Value**: Depth Anything 3 (DA3)
- **Rationale**: 训练中的 depth label 来自 off-the-shelf depth foundation model。
- **Search range**: 论文未报告其他深度标签源。
- **Sensitivity**: 高；深度伪标签质量直接影响几何脚手架。
- **Source**: Sec 3.3 Training Objective and Optimization

## 深度归一化
- **Value**: 先对 depth map 做 log transform，再按每图 percentiles 归一化到 [-0.5, 0.5]；推理时反变换恢复 metric 或 relative depth
- **Rationale**: 将深度值缩放到稳定训练范围。
- **Search range**: 论文未报告 percentile 具体取值或替代范围。
- **Sensitivity**: 中；归一化会影响 pixel-space depth generator 的数值稳定性。
- **Source**: Sec 3.3 Depth Normalization

## 视频训练 horizon
- **Value**: 9 frames
- **Rationale**: 用于 future video generation 的训练目标长度。
- **Search range**: 论文未报告其他 horizon。
- **Sensitivity**: 中；horizon 改变会影响未来场景建模难度和规划可用上下文。
- **Source**: Sec 3.3 Model Initialization and Adaptation

## 空间分辨率
- **Value**: 144 × 256
- **Rationale**: depth 和 video generation 在该分辨率 fine-tune，以降低计算和显存成本。
- **Search range**: 论文未报告其他分辨率。
- **Sensitivity**: 高；分辨率影响几何边界、视频质量与计算成本。
- **Source**: Sec 3.3 Model Initialization and Adaptation

## 评估协议
- **Value**: navtrain 训练，navtest 评估；Navsim v1 使用 PDMS，Navsim v2 使用 EPDMS
- **Rationale**: 遵循标准 Navsim protocol 与近期方法的公平比较设置。
- **Search range**: 论文未报告其他 split。
- **Sensitivity**: 高；split 或指标改变会影响结果可比性。
- **Source**: Sec 4.1 Datasets and Planning Metrics
