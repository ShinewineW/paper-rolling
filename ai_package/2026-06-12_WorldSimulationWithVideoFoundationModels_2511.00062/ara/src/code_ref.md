# Code Reference

- **Repository**: https://github.com/nvidia-cosmos/cosmos-predict2.5
- **Pinned commit**: `a2c298b0a3df3778b973fe65e9e58877b292d8a7`
- **Source**: paper-text (verified)
- **Reproduce**: re-clone at the pinned commit; this workspace keeps no runnable copy.

## Innovation → code location

| Innovation | Location (`file:line`) |
|---|---|
| 统一 Text2World、Image2World 和 Video2World 的 Cosmos-Predict2.5 flow-based world foundation model | README.md:4 |
| 用 Cosmos-Reason1 替换 T5 text encoder 并通过 cross-attention 引导 denoising | README.md:45 |
| 移除 absolute positional embeddings，仅保留 relative positional embeddings 和 3D RoPE 以支持更高分辨率与更长序列 | _not found_ |
| frame-replacement strategy 用于 Image2World 和 Video2World 条件帧保持 | _not found_ |
| shifted logit-normal distribution 与 progressive timestep shift 改善高噪声训练覆盖 | _not found_ |
| domain-specific SFT 后使用 model soup 等 model merging 统一专域能力 | _not found_ |
| VideoAlign reward 与 GRPO 风格 rollout group advantage 用于 flow-based world generation RL post-training | _not found_ |
| Cosmos-Transfer2.5 control-net style framework 支持 edge、blur、segmentation 和 depth 条件 | README.md:41 |
| world scenario map 将 HD map 与 dynamic objects 投影为多视角 driving control input | _not found_ |
| Plücker raymaps 和 camera projection layer 用于 camera-controllable multi-view generation | _not found_ |
| action embedder MLP 加到 timestamp embeddings 实现 action-conditioned world generation | _not found_ |
| rCM timestep distillation 用于少步数 world generation 加速 | _not found_ |
