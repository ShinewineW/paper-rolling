# Environment
- **Python**: 论文未说明
- **Framework**: 论文未说明具体软件框架；训练使用 FSDP sharding
- **Hardware**: 训练使用 256 to 1024 TPU-v5p；world model 推理速度在 single H100 GPU 上测量
- **Key dependencies**: FSDP sharding, LPIPS, RMSNorm, RoPE, SwiGLU, QKNorm, GQA, PMPO, FSDP, DeepSpeed 引用为系统文献
- **Random seeds**: 论文未说明
