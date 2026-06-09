# Environment
- **Python**: 论文未明确说明Python版本
- **Framework**: Stable Video Diffusion (SVD) [5] 作为基础框架; EDM扩散框架 [66]; AdamW优化器 [87]; DDIM采样器 [109]; LoRA [55]; Fourier特征嵌入 [114,116]
- **Hardware**: 阶段一: 128 A100 GPUs (约8天); 阶段二动作控制学习: 8 A100 GPUs (约10天，其中低分辨率约8天，高分辨率约2天); 消融实验: 8 A100 GPUs
- **Key dependencies**: SVD预训练权重 (stable video diffusion non-commercial community license), OpenDV-YouTube [136] (经手工过滤后约1735小时无标注驾驶视频), nuScenes [10] (训练集，用于动作控制学习阶段), DDIM采样器 [109], LoRA低秩适配器 [55], Fourier特征嵌入 [114, 116], EDM扩散框架 [66], AdamW优化器 [87]
- **Random seeds**: 论文未明确说明随机种子设置
