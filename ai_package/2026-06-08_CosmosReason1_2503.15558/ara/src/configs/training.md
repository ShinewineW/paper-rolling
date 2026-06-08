## SFT 学习率（Cosmos-Reason1-7B）
- **Value**: 余弦退火，从 1×10^-5 衰减至 1×10^-6
- **Rationale**: 余弦退火使 7B 模型在收敛后期以更小步长细化参数
- **Search range**: 1×10^-6 — 1×10^-5
- **Sensitivity**: 未报告
- **Source**: Sec 7.1

## SFT 学习率（Cosmos-Reason1-56B）
- **Value**: 第一阶段 1×10^-5，第二阶段衰减至 1×10^-6
- **Rationale**: 分两阶段衰减以适配更大规模混合架构模型的收敛特性
- **Search range**: 1×10^-6 — 1×10^-5
- **Sensitivity**: 未报告
- **Source**: Sec 7.1

## SFT 全局批大小（Cosmos-Reason1-7B）
- **Value**: 256
- **Rationale**: 为 7B 密集 Transformer 训练提供足够的梯度估计稳定性
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 7.1

## SFT 全局批大小（Cosmos-Reason1-56B）
- **Value**: 32
- **Rationale**: 56B 混合模型显存占用更高，批大小相应缩小
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 7.1

## Adam 优化器 β1
- **Value**: 0.9
- **Rationale**: 一阶矩估计的标准设置
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 7.1

## Adam 优化器 β2
- **Value**: 0.95
- **Rationale**: 二阶矩估计；相比默认 0.999 更快响应梯度幅度变化
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 7.1

## 权重衰减
- **Value**: 0.1
- **Rationale**: L2 正则化防止过拟合
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 7.1

## RL 学习率
- **Value**: 4×10^-6
- **Rationale**: RL 后训练使用更小学习率以在 SFT 基础上小步更新，保留已习得能力
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 7.2.1

## RL KL 惩罚系数
- **Value**: 0.005
- **Rationale**: 通过 KL 散度约束控制策略相对参考模型的漂移幅度
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 7.2.1

## RL 训练迭代数
- **Value**: 500
- **Rationale**: 在有限规模 MCQ 数据集上完成 RL 收敛所需的迭代轮数
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 7.2.1

## RL 全局批大小（问题数）
- **Value**: 128
- **Rationale**: 兼顾样本多样性与显存效率的批量设置
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 7.2.1

## RL 每题采样输出数（GRPO 组大小 G）
- **Value**: 9
- **Rationale**: 为 GRPO 组内归一化优势函数估计提供足够的响应分布覆盖
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 7.2.1

## RL 最大生成长度
- **Value**: 6144 tokens
- **Rationale**: 为长链式推理过程（CoT）提供充足的生成空间
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 7.2.1

## 评估推理温度
- **Value**: 0.6
- **Rationale**: 温度设置使多次采样结果有一定随机性，取均值以稳健估计模型性能
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 7.1

## 评估 top-p（nucleus sampling）
- **Value**: 0.95
- **Rationale**: 核采样截断配合温度参数共同控制输出分布
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 7.1

## 评估推理次数（取平均）
- **Value**: 5
- **Rationale**: 对不同随机种子取 5 次推理的平均精度，降低单次估计方差
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 7.1

## 张量并行度（Cosmos-Reason1-7B）
- **Value**: TP=4
- **Rationale**: 7B 模型在 4 路张量并行下平衡通信与计算效率
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 3.2

## 张量并行度与流水线并行度（Cosmos-Reason1-56B）
- **Value**: TP=8, PP=2
- **Rationale**: 56B 混合架构模型需更高并行度以适应参数规模与内存需求
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 3.2

## RL 训练效率提升（相对协同部署框架）
- **Value**: 约 160%（训练效率提升）
- **Rationale**: 全异步异构部署策略消除 policy training 与 actor rollout 的同步等待开销
- **Search range**: 未报告
- **Sensitivity**: 未报告
- **Source**: Sec 4.2
