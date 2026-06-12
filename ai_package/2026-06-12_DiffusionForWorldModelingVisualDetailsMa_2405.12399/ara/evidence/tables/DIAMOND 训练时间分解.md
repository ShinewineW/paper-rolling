# DIAMOND 训练时间分解
- **Source**: Table 5
- **Caption**: "使用 Nvidia RTX 4090 profiling 的 DIAMOND 单次更新、epoch 与 run 训练时间分解。"

| Single update | Time (ms) | Detail (ms) |
| --- | --- | --- |
| Total | 543 | 88 + 115 + 340 |
| Diffusion model update | 88 | - |
| Reward/Termination model update | 115 | - |
| Actor-Critic model update | 340 | 15× 20.4+ 34 |
| Imagination step (x 15) | 20.4 | 12.7 + 7.0 + 0.7 |
| Next observation prediction | 12.7 | 3×4.2 |
| Denoising step (x 3) | 4.2 |  |
| Reward/Termination prediction | 7.0 |  |
| Action prediction | 0.7 |  |
| Loss computation and backward | 34 |  |
| Epoch | Time (s) | Detail (s) |
| Total | 217 | 35 + 46 + 136 |
| Diffusion model | 35 | 400×88×10-3 |
| Reward/Termination model | 46 | 400×115×10-3 |
| Actor-Critic model | 136 | 400×340×10-3 |
| Run | Time (days) | Detail (days) |
| Total | 2.9 | 2.5 + 0.4 |
| Training time | 2.5 | 1000×217/(24×3600) |
| Other (collection, evaluation, checkpointing) | 0.4 | - |
