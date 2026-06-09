# Environment
- **Python**: 论文未指定
- **Framework**: PyTorch（分析推断，论文未显式声明）
- **Hardware**: 单张 NVIDIA RTX 5090D V2 32GB GPU
- **Key dependencies**: Wan2.2-5B 预训练视频DiT骨干, Wan2.2 内置 T5 文本编码器, Wan2.2 预训练视频 VAE, AdamW 优化器, flow matching 训练框架, LIBERO 基准 [37], RoboTwin 2.0 基准 [38], Galaxea R1 Lite 机器人平台（真实世界评估）
- **Random seeds**: 多个随机种子（论文未给出具体值；LIBERO报告跨不同随机种子的2000次试验）
