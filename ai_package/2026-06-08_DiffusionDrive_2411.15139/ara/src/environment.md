# Environment
- **Python**: 未在论文中明确说明
- **Framework**: 未在论文中显式说明（代码仓库 hustvl/DiffusionDrive 公开，框架推断为PyTorch，但论文未显式声明）
- **Hardware**: 训练：8×NVIDIA 4090 GPU；推理基准测试：1×NVIDIA 4090 GPU
- **Key dependencies**: ResNet-34 / ResNet-50 骨干网络（ImageNet预训练权重初始化）, DDIM采样器（用于截断去噪推理，Denoising Diffusion Implicit Models）, 可变形空间交叉注意力（Deformable Spatial Cross-Attention，基于Deformable DETR）, AdamW优化器, NAVSIM数据集（navtrain/navtest split，基于OpenScene/nuPlan）, nuScenes数据集, SparseDrive阶段1感知预训练权重（nuScenes配置下使用）, CARLA模拟器（泛化性验证实验，Longest6 benchmark）
- **Random seeds**: 未在论文中明确说明
