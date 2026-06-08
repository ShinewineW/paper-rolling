# Code Reference

- **Repository**: https://github.com/nvidia-cosmos/cosmos-transfer1
- **Pinned commit**: `5005e823dbd478ad8e51f6bc28a913a13a994b5f`
- **Reproduce**: re-clone at the pinned commit; this workspace keeps no runnable copy.

## Innovation → code location

| Innovation | Location (`file:line`) |
|---|---|
| 多模态自适应 DiT ControlNet（每种模态独立控制分支，推理时加权融合） | _not found_ |
| 时空控制图（spatiotemporal control map $\mathbf{w} \in \mathbb{R}^{N \times X \times Y \times T}$，支持不同模态在不同时空位置分配不同权重） | _not found_ |
| 分别训练、推理时融合策略（各控制分支独立训练后于推理时按需组合，节省显存并支持异构训练数据） | _not found_ |
| SalientObject 自动时空权重生成算法（使用 VLM 将 GroundingDINO+SAM2 分割结果分类为前景/背景并自动生成控制权重图） | _not found_ |
| Cosmos-Transfer1-7B-4KUpscaler（基于 ControlNet 的视频超分辨率模块，使用 Real-ESRGAN 腐蚀增强训练，patch 3×3 分块推理） | README.md:28 |
| Prompt Upsampler（微调 Pixtral-12B，将短文本提示结合多模态条件视频扩展为对齐训练分布的长描述） | .git/index:26 |
| GB200 实时推理并行策略（非注意力层纯数据并行 + 注意力层头并行，all-to-all collective，64 GPU 实现实时生成） | _not found_ |
