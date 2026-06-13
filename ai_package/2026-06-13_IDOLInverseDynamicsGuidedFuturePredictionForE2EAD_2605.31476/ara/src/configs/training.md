## 训练数据划分
- **Value**: NAVSIM training split
- **Rationale**: 论文说明所有模型都在 NAVSIM training split 上训练，并在 NAVSIM benchmark 上评估。
- **Search range**: 论文未报告可选范围。
- **Sensitivity**: 训练划分是评估可比性的基础，论文未做不同训练划分敏感性实验。
- **Source**: Appendix B

## 训练轮数
- **Value**: 30
- **Rationale**: Table 6 将 Epochs 列为 30。
- **Search range**: 论文未报告可选范围。
- **Sensitivity**: 论文未报告训练轮数消融。
- **Source**: Table 6

## 优化器
- **Value**: AdamW
- **Rationale**: 实现细节说明训练使用 AdamW。
- **Search range**: 论文未报告其他优化器。
- **Sensitivity**: 论文未报告优化器敏感性实验。
- **Source**: Sec 4.2

## 初始学习率
- **Value**: 2 × 10^-4
- **Rationale**: Table 6 给出 Learning rate 为 2 × 10^-4。
- **Search range**: 论文未报告学习率搜索范围。
- **Sensitivity**: 论文未报告学习率敏感性实验。
- **Source**: Table 6

## 权重衰减
- **Value**: 1 × 10^-4
- **Rationale**: Table 6 给出 Weight decay 为 1 × 10^-4。
- **Search range**: 论文未报告权重衰减搜索范围。
- **Sensitivity**: 论文未报告权重衰减敏感性实验。
- **Source**: Table 6

## 批大小
- **Value**: 4 per GPU
- **Rationale**: 实现细节说明训练在 4 NVIDIA GeForce RTX 3090 GPUs 上进行，每个 GPU 的 batch size 为 4。
- **Search range**: 论文未报告其他 batch size。
- **Sensitivity**: 论文未报告 batch size 敏感性实验。
- **Source**: Sec 4.2

## 训练时长
- **Value**: approximately 24 hours
- **Rationale**: 实现细节说明训练约 24 hours。
- **Search range**: 论文未报告训练时长范围。
- **Sensitivity**: 训练时长与硬件和批大小相关，论文未做敏感性分析。
- **Source**: Sec 4.2

## 训练损失组成
- **Value**: trajectory offset regression、imitation reward supervision、simulator-metric reward supervision、BEV semantic supervision
- **Rationale**: 论文训练目标混合轨迹 offset 回归、reward 监督和 BEV 语义监督，用于稳定场景编码、latent future prediction 和 trajectory ranking。
- **Search range**: 论文未报告损失权重数值范围。
- **Sensitivity**: Table 7 仅列出损失项角色，论文未报告去除各训练损失项的独立消融。
- **Source**: Sec 3.5; Table 7
