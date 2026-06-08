# Environment
- **Python**: 未报告
- **Framework**: SFT 采用支持 5D 并行（DP/PP/CP/FSDP/TP）的 Megatron-LM 风格训练基础设施；RL 采用自研全异步异构训练框架，包含 Dispatcher、Actor Rollout 和 Policy Training 三个模块，actor rollout 节点支持 DP/PP/TP，使用定制 NCCL 通信器在 dispatcher 与 rollout/policy 节点间通信；优化器为 fused Adam
- **Hardware**: 未报告具体 GPU 型号或集群规模
- **Key dependencies**: Qwen2.5-VL（Cosmos-Reason1-7B 预训练基础模型）, Nemotron-H（Cosmos-Reason1-56B LLM 骨干）, InternViT-300M-V2.5（Cosmos-Reason1-56B 视觉编码器）, DeepSeek-R1（SFT 数据中推理迹蒸馏来源）, Libero（物体永久性仿真数据生成平台，含 130 个机械臂操作任务）, GRPO 算法（来源：DeepSeekMath，Shao et al. 2024）, PixelShuffle（视觉 token 空间→通道降采样，Shi et al. 2016）, ECoT（BridgeData V2 数据标注时提供物体与动作序列信息）
- **Random seeds**: 评估时使用 5 个不同随机种子，各次推理温度 0.6，top-p 0.95，取平均精度
