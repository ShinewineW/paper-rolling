# Environment
- **Python**: 论文未说明
- **Framework**: 论文未说明主训练框架；FID/KID 明确使用 torchmetrics
- **Hardware**: 论文仅提到 cloud compute infrastructure，未说明具体 hardware
- **Key dependencies**: nuScenes v1.0-trainval, CAN-bus data, Stable-Diffusion VAE, DiT formulation, DDIM, torchmetrics, V-JEPA2, DINOv2-S/14, CLIP ViT-B/32, ViT-S/16, VQ-VAE Tracker
- **Random seeds**: encoder benchmark 使用 3 seeds；Table 1 标注 3 seeds；FID/KID 使用 3 seeds；overfitting 部分称 all results use 3 random seeds；capacity probe 为 1 seed each
