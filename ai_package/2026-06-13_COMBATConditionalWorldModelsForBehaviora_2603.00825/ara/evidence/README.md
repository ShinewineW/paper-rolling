# Evidence Index

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/标准感知指标结果.md](tables/标准感知指标结果.md) | Table 1 | ['C1'] | 所有指标在 held-out test set 上计算；所有分数越低越好。 |
| [tables/TAA 与 ARC checkpoint 结果.md](tables/TAA 与 ARC checkpoint 结果.md) | Table 2 | ['C2'] | 不同 training checkpoints 的 TAA 与 ARC scores，并与 human gameplay 对比。 |

## Figures
| Source ref | Role | Caption |
|------------|------|---------|
| `images/30f0076cae1933eaafda6439a5714c6614ae719a845639e3392ab494019d7128.jpg` | architecture | Figure 1. An overview of the COMBAT world model. (Top) The model is conditioned on the current state (visual frames and poses) and Player 1’s control inputs to autoregressively predict subsequent frames. (Bottom) Three distinct generated trajectories showcase the model’s ability to produce plausible |
| `images/ed7cb0501503743d4cfd13b3c4b96cb669b9fc5c3b3326b45b18b4cff500b573.jpg` | result | Figure 2. Architectural diagram of the COMBAT model. (a) The end-to-end training process, where a Diffusion Transformer is conditioned on action and timestep embeddings to denoise latent frame representations. (b) The internal structure of the DiT backbone, which employs a hybrid local-global attent |
| `images/85cf207cc7b97e0eb332fe35090018fd1fdf8a194995ac48fc4f113022a278d0.jpg` | result | Figure 2. Architectural diagram of the COMBAT model. (a) The end-to-end training process, where a Diffusion Transformer is conditioned on action and timestep embeddings to denoise latent frame representations. (b) The internal structure of the DiT backbone, which employs a hybrid local-global attent |
| `images/36d72cf17b2e4e72af769a0efcc174157451537e3bc3a62093de78629f7a296e.jpg` | result | (a) Player 1 Damage Distribution |
| `images/6d8aee45f98e83db2580383b7abd68fdafe4e205667a1ca6b3a10bb85e3a72b3.jpg` | result | (b) Player 2 Damage Distribution |
| `images/098c95cb6a19683cb0e790a5c6c320f2075586e165b2f85fb3d14c9a9273bc76.jpg` | architecture | Figure 3. Behavioral Consistency Metrics. A comparison of generated gameplay (COMBAT) against the ground truth. (a, b) The per-frame damage distributions for Player 1 and Player 2, showing that our model learns a realistic mapping of actions to consequences. (c, d) The mean health trajectories over  |
| `images/c10932b1a8f9986c46d3bc63dd39b8b503955c7c9836996aa5b8f113b03a40e9.jpg` | architecture | Figure 3. Behavioral Consistency Metrics. A comparison of generated gameplay (COMBAT) against the ground truth. (a, b) The per-frame damage distributions for Player 1 and Player 2, showing that our model learns a realistic mapping of actions to consequences. (c, d) The mean health trajectories over  |
| `images/723674d7723f9393dabcb1e1f344af03554769ef2ea0b1a69e506dff0f837133.jpg` | result | Figure 4. Total Action Adherence across training checkpoints |
| `images/3531e4c4618e0a87029b59182bcd25536809e49e639914ac590dfa8f2ac2b652.jpg` | result | Figure 5. Action Ratio Consistency across training checkpoints |
