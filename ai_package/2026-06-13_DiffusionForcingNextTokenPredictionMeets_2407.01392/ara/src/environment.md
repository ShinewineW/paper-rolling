# Environment
- **Python**: 论文未说明。
- **Framework**: 论文未说明核心深度学习框架；time series 部分明确 follow the implementation of pytorch-ts，并通过 GluonTS 访问数据与计算指标。
- **Hardware**: 所有实验使用 fp16 mixed precision training。time series、maze planning、compositionally、visual imitation experiments 可用单张 2080Ti 11GB 训练；video prediction 对两个视频数据集使用 8 A100 GPUs。
- **Key dependencies**: GluonTS, pytorch-ts, D4RL, DDIM, TECO dataset, Minecraft navigation dataset, DMLab navigation dataset
- **Random seeds**: time series Table 2 对本文方法报告 five runs trained with different seeds；具体 seed 值未说明。
