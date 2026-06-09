## 生成模型批次大小
- **Value**: 128
- **Rationale**: 平衡训练吞吐量与显存占用
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 中
- **Source**: Sec 4.2

## 生成模型学习率
- **Value**: 2e-5
- **Rationale**: 与 Adafactor 优化器配合，使用恒定学习率
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 中
- **Source**: Sec 4.2

## 优化器
- **Value**: Adafactor（无权重衰减）
- **Rationale**: 自适应学习率，内存开销低于 Adam
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec 4.2

## 梯度裁剪阈值
- **Value**: 1.0
- **Rationale**: 防止梯度爆炸，稳定训练
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 低
- **Source**: Sec 4.2

## 训练步数
- **Value**: 700,000
- **Rationale**: 默认评估检查点；论文指出 70M 数据集下性能在 700k 步后仍继续改善
- **Search range**: 消融实验使用 200k 步；主实验使用 700k 步
- **Sensitivity**: 高
- **Source**: Sec 4.2

## 训练数据规模
- **Value**: 70M 条轨迹样本
- **Rationale**: 来自 RL 智能体训练与评估阶段记录轨迹的随机子集
- **Search range**: 消融测试了 1M、5M、10M、70M
- **Sensitivity**: 高
- **Source**: Sec 4.2, Appendix A.3

## 历史帧条件丢弃概率（CFG 训练）
- **Value**: 0.1
- **Rationale**: 以 10% 概率丢弃历史帧条件，支持推理时使用 Classifier-Free Guidance
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 中
- **Source**: Sec 4.2

## 训练硬件
- **Value**: 128 TPU-v5e（数据并行）
- **Rationale**: 支持大规模数据并行训练
- **Search range**: N/A
- **Sensitivity**: N/A
- **Source**: Sec 4.2

## 噪声增强最大噪声水平
- **Value**: 0.7
- **Rationale**: 控制上下文帧被添加高斯噪声的最大幅度，用于缓解自回归漂移
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 高
- **Source**: Sec 4.2

## 噪声水平嵌入桶数
- **Value**: 10
- **Rationale**: 将连续噪声水平离散化为 10 个桶，每个桶学习独立嵌入
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 低
- **Source**: Sec 4.2

## 解码器微调批次大小
- **Value**: 2,048
- **Rationale**: latent 解码器单独微调时使用更大批次，其余参数与去噪器相同
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 低
- **Source**: Sec 4.2

## 训练图像分辨率
- **Value**: 320x240（padding 至 320x256）
- **Rationale**: 接近 DOOM 原生分辨率，并 padding 以适配 Stable Diffusion v1.4 的 8x 下采样 latent 空间
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec 4.2

## 训练损失
- **Value**: v-prediction 扩散损失（velocity parameterization），见 Eq. 1
- **Rationale**: velocity parameterization 以速度预测为目标，比噪声预测更稳定；Eq. 1 为论文显式给出的唯一训练目标公式
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec 3.2, Eq. 1

## RL 智能体训练算法
- **Value**: PPO
- **Rationale**: 近端策略优化，适合稳定的游戏数据采集
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec 4.1

## RL 智能体每次迭代批次大小
- **Value**: 64
- **Rationale**: 每轮更新使用的小批量大小
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 低
- **Source**: Sec 4.1

## RL 智能体每次迭代训练轮数
- **Value**: 10
- **Rationale**: 每次数据收集后对网络进行 10 轮梯度更新
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 低
- **Source**: Sec 4.1

## RL 智能体学习率
- **Value**: 1e-4
- **Rationale**: 标准 PPO 学习率设置
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 中
- **Source**: Sec 4.1

## RL 智能体总环境步数
- **Value**: 50M
- **Rationale**: 保证智能体能够学习有效策略并覆盖足够多的游戏场景
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 高
- **Source**: Sec 4.1

## RL 智能体折扣因子
- **Value**: 0.99
- **Rationale**: 标准长期奖励折扣系数（γ = 0.99）
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 低
- **Source**: Sec 4.1

## RL 智能体熵系数
- **Value**: 0.1
- **Rationale**: 鼓励策略探索多样化动作，防止过早收敛
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 低
- **Source**: Sec 4.1

## RL 智能体并行游戏实例数
- **Value**: 8
- **Rationale**: 同时运行 8 个游戏实例以提高数据采集效率
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 低
- **Source**: Sec 4.1

## RL 智能体回放缓冲大小
- **Value**: 512
- **Rationale**: 每个游戏实例的回放缓冲区大小
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 低
- **Source**: Sec 4.1
