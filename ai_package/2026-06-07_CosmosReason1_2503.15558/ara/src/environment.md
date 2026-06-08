# Environment
- **Python**: 论文未明确说明 Python 版本
- **Framework**: 自研全异步 RL 训练框架：策略训练节点与 Actor rollout 节点异构分离部署，通过统一 Dispatcher 调度与分发训练提示；策略训练支持 5D 并行（数据并行 DP、流水线并行 PP、上下文并行 CP、全分片数据并行 FSDP、张量并行 TP），rollout 节点支持 DP/PP/TP；使用定制 NCCL 通信器连接 Dispatcher 与 rollout/policy 节点；具备训练网格管理逻辑（节点故障时无需重启即可继续当前训练步）和 Dispatcher 冗余机制；SFT 基础设施参考 NVLM-D 同款方案
- **Hardware**: NVIDIA GPU（具体型号论文未明确标注）
- **Key dependencies**: Qwen2.5-VL（7B 基础预训练模型，含视觉编码器与 LLM 主干）, Nemotron-H（56B LLM 主干预训练模型，混合 Mamba-MLP-Transformer 架构）, InternViT-300M-V2.5（56B 视觉编码器）, DeepSeek-R1（SFT 推理迹蒸馏来源，用于物理常识与具身推理数据标注）, GRPO 算法（Shao et al., 2024，RL 策略优化算法）, PixelShuffle（Shi et al., 2016，视觉 token 空间下采样）, Libero 机器人仿真平台（Liu et al., 2023，物体永久性 SFT 数据生成）, Cosmos-Predict1 训练数据子集（NVIDIA, 2025，箭头时间 SFT 视频来源）, ECoT（Zawalski et al., 2024，BridgeData V2 动作序列辅助标注）
- **Random seeds**: 评估时对每个模型使用 5 个不同随机种子独立采样，取平均准确率作为最终报告值
