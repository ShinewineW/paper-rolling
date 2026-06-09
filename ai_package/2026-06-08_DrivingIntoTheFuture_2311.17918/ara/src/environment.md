# Environment
- **Python**: 论文未明确说明
- **Framework**: PyTorch(基于Stable Diffusion及VideoLDM实现，论文未显式声明框架名称)
- **Hardware**: A40 (48GB) GPU
- **Key dependencies**: Stable Diffusion(图像扩散基础模型), VideoLDM(视频扩散建模参考实现), DDIM采样器, CLIP文本编码器, ConvNeXt图像编码器, LoFTR(关键点匹配模型，用于KPM一致性评估), AdamW优化器, BEVFormer(3D目标检测，用于图像奖励评估), MapTR(在线HDMap构建，用于图像奖励评估), CVT(BEV分割，用于可控性评估), nuScenes数据集(700训练场景，150验证场景), Waymo Open Dataset(前置摄像头，768×512)
- **Random seeds**: 论文未明确说明
