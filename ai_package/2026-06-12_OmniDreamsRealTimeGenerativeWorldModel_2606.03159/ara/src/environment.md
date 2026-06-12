# Environment
- **Python**: 论文未说明具体 Python 版本；AlpaSim 以 Docker containers 部署并允许不同 Python 和 OS environments。
- **Framework**: 论文显式提到 PyTorch 2 相关的 torch.compile、CUDA Graphs、Flex-Attention，以及 in-house ring-attention implementation。
- **Hardware**: NVIDIA GB300 用于主要推理结果；单视角报告 single GB300，多视角报告 16-GPU NVIDIA GB300 cabinet；FlashDreams 额外提到 single GB200 和 4 H100s 验证。
- **Key dependencies**: Cosmos-Predict 2.5, Qwen2.5-VL-7B, SIL-Wheel, Flex-Attention, torch.compile, CUDA Graphs, LightX2V, LightVAE, LightTAE, gRPC, NCCL, Docker containers, AlpaSim, Alpamayo 1, NVIDIA NuRec, DINOv2 dinov2_vitb14
- **Random seeds**: 论文未说明随机种子；Sec. 6.3 中 seed 指 first frame of simulation，而非随机数种子。
