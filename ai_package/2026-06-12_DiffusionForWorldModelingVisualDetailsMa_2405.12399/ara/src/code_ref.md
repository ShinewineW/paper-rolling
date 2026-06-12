# Code Reference

- **Repository**: https://github.com/eloialonso/diamond
- **Pinned commit**: `5bcd1599755b4f2fae8e5e079e02f0728e174965`
- **Source**: pwc-official (official-flagged)
- **Reproduce**: re-clone at the pinned commit; this workspace keeps no runnable copy.

## Innovation → code location

| Innovation | Location (`file:line`) |
|---|---|
| DIAMOND：把 diffusion world model 作为训练 RL agent 的 imagination 环境，并在像素空间直接生成下一帧。 | README.md:3 |
| EDM 预条件化目标：用 c_skip、c_out、c_in 自适应混合信号和噪声，改善少步采样稳定性。 | src/models/diffusion/denoiser.py:22 |
| Frame-stacking 条件化：用标准 U-Net 2D 接收过去帧和 noised next frame，而不是离散 latent token 序列。 | _not found_ |
| Adaptive Group Normalization：把动作和 diffusion time 注入 residual blocks。 | _not found_ |
| Euler 低 NFE 采样：在 world model rollout 中用少量 denoising steps 生成下一观测。 | config/trainer.yaml:76 |
| 独立 neural game engine 演示：在 Counter-Strike: Global Offensive 静态 gameplay 上训练可交互世界模型。 | README.md:50 |
