# Environment
- **Python**: 论文未说明 Python 版本
- **Framework**: DeepMind Jax ecosystem，并提到内部 framework 用于 model training
- **Hardware**: 主 Genie dynamics 使用 256 TPUv5p；Appendix C.3 还使用 TPUv2、TPUv3、TPUv5p；CoinRun 可复现实例可在 single mid range TPU/GPU 或 single TPU with 16G memory 上训练
- **Key dependencies**: Jax ecosystem, internal framework, ST-transformer, VQ-VAE, MaskGIT, AdamW, bfloat16, QK norm, stage-3 ZeRO sharding, tensor parallelism, batch parallelism, Procgen CoinRun, R2D2
- **Random seeds**: Figure 15 的 BC results averaged over 5 seeds；CoinRun data collection sample level seeds between zero and 10,000；论文未说明 Genie 主训练 random seed
