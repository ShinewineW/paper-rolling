# Environment
- **Python**: 论文未说明
- **Framework**: 论文未明确说明（分析推断,论文未显式声明）
- **Hardware**: 训练：8块NVIDIA 4090 GPU；推理FPS测量：单块NVIDIA 4090 GPU
- **Key dependencies**: ResNet主干网络（ImageNet预训练权重初始化，用于NAVSIM实验）, DDIM采样器（用于推理阶段的去噪更新规则）, K-Means聚类算法（用于从训练集构建先验锚点轨迹）, AdamW优化器, 可变形注意力机制（基于Deformable DETR [62]）, NAVSIM数据集（基于OpenScene/nuPlan，用于闭环规划评估）, nuScenes数据集（用于开环指标验证）, SparseDrive感知预训练权重（用于nuScenes第二阶段初始化）
- **Random seeds**: 论文未说明
