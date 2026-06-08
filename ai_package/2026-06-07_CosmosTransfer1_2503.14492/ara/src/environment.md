# Environment
- **Python**: 论文未明确指定 Python 版本
- **Framework**: PyTorch（提示上采样器使用 FSDP2 进行分布式训练）
- **Hardware**: {'training': '每模态控制分支：1024 × NVIDIA H100 GPU', 'inference_demo': 'NVIDIA GB200 NVL72 机架（36 Grace CPU + 72 B200 GPU，any-to-any NVLink 互联；每块 B200 搭载最高 192 GB HBM）'}
- **Key dependencies**: Cosmos-Predict1-7B-Video2World（基础扩散世界模型，含 Video2World 与 Sample-AV 变体）, DepthAnything2（视频逐帧深度估计，归一化至 [0, 1]）, GroundingDINO（开放集目标检测，用于分割标注与提示上采样器训练）, SAM2（视频实例分割掩码提取）, Pixtral-12B（提示上采样器基座，多模态 VLM）, Gemma-2-9B-it（提示上采样器训练数据中短提示生成）, Real-ESRGAN（4KUpscaler 训练时高分辨率视频退化增强）, StreamPetr + Hydra-MDP（AV 评估用 3D 目标检测方法）, DOVER（视频感知质量评估指标）, LPIPS（生成多样性评估指标）, bilateral blur / Canny edge detector（训练期间随机参数数据增强）
- **Random seeds**: 论文未明确报告随机种子设置
