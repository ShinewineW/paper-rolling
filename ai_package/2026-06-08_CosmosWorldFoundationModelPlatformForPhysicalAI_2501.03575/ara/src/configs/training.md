## 扩散 WFM 7B 基础学习率
- **Value**: 2^-15
- **Rationale**: 适配 7B 扩散模型规模，配合 AdamW 与低 β2/ε 值稳定训练
- **Search range**: 2^-16 ~ 2^-14
- **Sensitivity**: 高：7B 与 14B 分别设置不同档学习率，反映规模差异
- **Source**: ['Tab. 11']

## 扩散 WFM 14B 基础学习率
- **Value**: 2^-16
- **Rationale**: 更大模型需更小学习率以避免训练不稳定
- **Search range**: 2^-17 ~ 2^-15
- **Sensitivity**: 高：相较 7B 降低一档
- **Source**: ['Tab. 11']

## 扩散 WFM 7B 权重衰减
- **Value**: 0.1
- **Rationale**: 适度正则化防止过拟合
- **Search range**: 0.05 ~ 0.2
- **Sensitivity**: 中
- **Source**: ['Tab. 11']

## 扩散 WFM 14B 权重衰减
- **Value**: 0.2
- **Rationale**: 更大模型需更强正则化
- **Search range**: 0.1 ~ 0.3
- **Sensitivity**: 中
- **Source**: ['Tab. 11']

## AdamW 动量参数 β1, β2
- **Value**: β1=0.9, β2=0.99
- **Rationale**: 论文发现更低的 β2（0.99 而非常用的 0.999）显著减少 loss 尖峰
- **Search range**: β1: 0.9; β2: 0.95~0.999
- **Sensitivity**: 高：β2 与 ε 共同影响训练稳定性
- **Source**: ['Tab. 11', 'Sec. 5.1.3']

## AdamW ε
- **Value**: 10^-10
- **Rationale**: 更小 ε 配合低 β2 减少 loss 尖峰，论文明确指出此组合显著稳定 14B 训练
- **Search range**: 10^-10 ~ 10^-8
- **Sensitivity**: 高：论文明确指出低 ε 值可稳定训练
- **Source**: ['Tab. 11', 'Sec. 5.1.3']

## 扩散 WFM 学习率预热迭代次数
- **Value**: 2,500
- **Rationale**: 线性预热避免训练初期梯度爆炸
- **Search range**: 1000 ~ 5000
- **Sensitivity**: 低至中
- **Source**: ['Tab. 11']

## 去噪得分匹配损失缩放因子
- **Value**: 10
- **Rationale**: 对 Eq.(5) 损失乘以 10 进一步稳定扩散训练
- **Search range**: 5 ~ 20
- **Sensitivity**: 中
- **Source**: ['Sec. 5.1.3']

## Video2World 条件帧增强噪声 P_mean / P_std
- **Value**: P_mean=-3.0, P_std=2.0
- **Rationale**: 训练时对条件帧注入增强噪声以增强推理时的鲁棒性
- **Search range**: P_mean: -5.0 ~ -1.0; P_std: 1.0 ~ 3.0
- **Sensitivity**: 中
- **Source**: ['Sec. 5.1.3']

## 自回归 WFM 4B/12B 基础学习率
- **Value**: 1×10^-3
- **Rationale**: 自回归 WFM 基于 NLL 损失，基础学习率高于扩散模型
- **Search range**: 1×10^-4 ~ 1×10^-2
- **Sensitivity**: 高
- **Source**: ['Tab. 14']

## 自回归 WFM 5B-Video2World 基础学习率
- **Value**: 3×10^-4
- **Rationale**: 从 4B 预训练权重继续训练，使用较小学习率进行微调
- **Search range**: 1×10^-4 ~ 1×10^-3
- **Sensitivity**: 高
- **Source**: ['Tab. 14']

## 自回归 WFM 13B-Video2World 基础学习率
- **Value**: 5×10^-4
- **Rationale**: 从 12B 预训练权重继续训练
- **Search range**: 1×10^-4 ~ 1×10^-3
- **Sensitivity**: 高
- **Source**: ['Tab. 14']

## 自回归 WFM 权重衰减
- **Value**: 0.01
- **Rationale**: 自回归 WFM 正则化强度低于扩散模型
- **Search range**: 0.001 ~ 0.1
- **Sensitivity**: 中
- **Source**: ['Tab. 14']

## 自回归 WFM 学习率预热迭代次数
- **Value**: 5,000
- **Rationale**: 线性预热稳定自回归模型训练初期
- **Search range**: 2000 ~ 10000
- **Sensitivity**: 低至中
- **Source**: ['Tab. 14']

## z-loss 系数 λ
- **Value**: 3×10^-4
- **Rationale**: 惩罚过大 logit 值以防梯度爆炸，在大规模 GPU 节点训练时至关重要，论文通过消融确认此值为最优平衡点
- **Search range**: 1×10^-4 ~ 1×10^-3
- **Sensitivity**: 高：论文明确称此系数「strikes an optimal balance」
- **Source**: ['Sec. 5.2.1']

## 自回归冷却阶段迭代次数
- **Value**: 30,000
- **Rationale**: 学习率线性衰减至 0 的高质量数据微调阶段，类似 LLM 训练惯例
- **Search range**: 10000 ~ 50000
- **Sensitivity**: 中
- **Source**: ['Sec. 5.2.3']

## 渐进式训练低分辨率阶段规格
- **Value**: 512p (640×512)，57 帧，上下文长度 10,240，FSDP=64，CP=2
- **Rationale**: 先在低分辨率建立基础能力以降低训练计算量
- **Search range**: 固定配置
- **Sensitivity**: 高：阶段顺序与帧数影响最终模型质量
- **Source**: ['Tab. 12']

## 渐进式训练高分辨率阶段规格
- **Value**: 720p (1280×704)，121 帧，上下文长度 56,320，FSDP=64，CP=8
- **Rationale**: 在目标分辨率和帧率下完成预训练，CP=8 扩展到更长上下文
- **Search range**: 固定配置
- **Sensitivity**: 高
- **Source**: ['Tab. 12']

## 数据去重 k-means 聚类数 k
- **Value**: 10,000
- **Rationale**: 语义去重将视频嵌入聚类为 10,000 类以识别近重复样本
- **Search range**: 5000 ~ 50000
- **Sensitivity**: 中
- **Source**: ['Sec. 3.5']

## 视觉质量过滤底部阈值
- **Value**: 15%
- **Rationale**: 去除感知质量最低的视频片段，保留质量较高训练数据
- **Search range**: 10% ~ 25%
- **Sensitivity**: 中
- **Source**: ['Sec. 3.3.2']
