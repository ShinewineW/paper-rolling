# Environment
- **Python**: 论文未说明
- **Framework**: PyTorch；pretraining 和 supervised fine-tuning 使用 LLaMA Factory；reinforcement learning 使用 Easy-R1
- **Hardware**: 训练阶段使用 8 A100 GPUs；推理阶段使用 4 A100 GPUs；主文另写作 $8 \times 8 0$ GB GPUs
- **Key dependencies**: Qwen-VL family, Qwen2-VL-2B, VQGAN, LLaMA Factory, Easy-R1, AdamW, GRPO, nuScenes, Fréchet Inception Distance
- **Random seeds**: 论文未说明
