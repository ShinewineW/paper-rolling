# Environment
- **Python**: 论文未说明
- **Framework**: FSDP2作为主要distributed training framework；结合TorchTitan相关优化、Ulysses-style context parallelism、torch Selective Activation Checkpointing、fused flash attention with JVP support、FSDP2和context parallelism适配
- **Hardware**: Table 9报告4096 NVIDIA H100 GPUs；720p、93 frames训练时Cosmos-Predict2.5-2B使用context parallelism size 2，Cosmos-Predict2.5-14B使用context parallelism size 8
- **Key dependencies**: WAN2.1 VAE, Cosmos-Reason1, Qwen2.5-VL-7B, InternVideo2, VideoAlign, FSDP2, TorchTitan, DeepSpeed, NATTEN sparse attention, CUDA IPC, Redis, Delta Lake, Milvus, Video Depth Anything, SAMv2, Grounding DINO, cuRobo, ViPE, LATR, BEVFormer
- **Random seeds**: 论文未说明
