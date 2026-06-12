# Environment
- **Python**: 论文未说明 Python 版本。
- **Framework**: 论文未说明具体深度学习框架。
- **Hardware**: Atari 每个 run 约 12GB VRAM,在 single Nvidia RTX 4090 上约 2.9 days；CS:GO combined model 在 RTX 4090 上训练 12 days,并在 RTX 3090 上以 10Hz 运行；Appendix M 的 3D 视觉质量实验在 up to 4×A6000 GPUs 上训练。
- **Key dependencies**: Atari 100k benchmark, Counter-Strike: Global Offensive dataset from Pearce and Zhu (2022), Motorway driving dataset from Santana and Hotz (2016), U-Net 2D, CNN residual blocks, LSTM, Adaptive Group Normalization, Group Normalization, SiLU, AdamW, Euler sampler, FVD as implemented by Skorokhodov et al. (2022), FID, LPIPS
- **Random seeds**: Atari 主实验为每个游戏 5 random seeds；Appendix L 的 1-step ablation 为 single seed；论文未列出具体 seed 值。
