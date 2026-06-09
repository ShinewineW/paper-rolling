# Environment
- **Python**: 论文未给出 Python 版本信息
- **Framework**: 自定义全异步 RL 训练框架（含 Dispatcher、Actor Rollout、Policy Training 三部分）；Megatron-LM 式 5D 并行（DP、PP、CP、FSDP、TP）；NCCL 定制通信器；fused Adam 优化器；PixelShuffle 空间下采样（Shi et al., 2016）
- **Hardware**: Cosmos-Reason1-7B 训练使用 TP=4；Cosmos-Reason1-56B 训练使用 TP=8、PP=2；具体 GPU 型号论文未明确给出
- **Key dependencies**: GRPO（Shao et al., 2024）, InternViT-300M-V2.5（Chen et al., 2024）作为 56B 视觉编码器, Nemotron-H（NVIDIA, 2025）作为 56B LLM 主干, Qwen2.5-VL（Bai et al., 2025）作为 7B 预训练基础模型, DeepSeek-R1（DeepSeek-AI, 2025）用于 SFT 数据推理链蒸馏, PixelShuffle（Shi et al., 2016）用于视觉 token 空间下采样, NCCL 定制通信器用于分布式训练节点间通信, Libero（Liu et al., 2023）用于物体恒存性仿真数据合成
- **Random seeds**: 推理评估时使用 5 个不同随机种子，对准确率取平均
