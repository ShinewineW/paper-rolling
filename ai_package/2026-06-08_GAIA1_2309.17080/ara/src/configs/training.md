## 图像tokenizer初始学习率
- **Value**: 1×10^{-4}
- **Rationale**: AdamW优化器初始学习率，配合线性预热与余弦衰减调度
- **Search range**: [1×10^{-5}, 1×10^{-3}]
- **Sensitivity**: high
- **Source**: Sec 4.1

## 图像tokenizer最终学习率（余弦衰减后）
- **Value**: 1×10^{-5}
- **Rationale**: 10k步余弦衰减后的最终学习率
- **Search range**: [1×10^{-6}, 1×10^{-4}]
- **Sensitivity**: medium
- **Source**: Sec 4.1

## 图像tokenizer线性预热步数
- **Value**: 5k
- **Rationale**: 线性学习率预热步数
- **Search range**: [1k, 10k]
- **Sensitivity**: low
- **Source**: Sec 4.1

## 图像tokenizer训练总步数
- **Value**: 200k
- **Rationale**: 总训练步数，约4天完成
- **Search range**: [100k, 500k]
- **Sensitivity**: medium
- **Source**: Sec 4.1

## 图像tokenizer批大小
- **Value**: 160
- **Rationale**: 分布于32块A100 80GB GPU上训练
- **Search range**: [64, 512]
- **Sensitivity**: medium
- **Source**: Sec 4.1

## 图像tokenizer AdamW权重衰减
- **Value**: 0.01
- **Rationale**: AdamW正则化权重衰减系数
- **Search range**: [0.001, 0.1]
- **Sensitivity**: low
- **Source**: Sec 4.1

## 图像tokenizer AdamW beta系数
- **Value**: (0.5, 0.9)
- **Rationale**: GAN训练惯用较低beta1以减少参数更新震荡
- **Search range**: beta1 [0.0, 0.9], beta2 [0.8, 0.999]
- **Sensitivity**: medium
- **Source**: Sec 4.1

## 图像tokenizer损失权重 λ_{L1}
- **Value**: 0.2
- **Rationale**: 图像重建损失中L1分量权重
- **Search range**: [0.05, 1.0]
- **Sensitivity**: medium
- **Source**: Sec 4.1

## 图像tokenizer损失权重 λ_{L2}
- **Value**: 2.0
- **Rationale**: 图像重建损失中L2分量权重
- **Search range**: [0.5, 5.0]
- **Sensitivity**: medium
- **Source**: Sec 4.1

## 图像tokenizer损失权重 λ_{perceptual}
- **Value**: 0.1
- **Rationale**: 感知损失权重
- **Search range**: [0.05, 0.5]
- **Sensitivity**: medium
- **Source**: Sec 4.1

## 图像tokenizer损失权重 λ_{GAN}
- **Value**: 1.0
- **Rationale**: GAN对抗损失权重
- **Search range**: [0.1, 2.0]
- **Sensitivity**: high
- **Source**: Sec 4.1

## 图像tokenizer损失权重 λ_{codebook}
- **Value**: 1.0
- **Rationale**: VQ-VAE codebook量化损失（嵌入损失+承诺损失）权重
- **Search range**: [0.1, 2.0]
- **Sensitivity**: medium
- **Source**: Sec 4.1

## 图像tokenizer损失权重 λ_{DINO}
- **Value**: 0.1
- **Rationale**: DINO余弦相似度蒸馏损失权重，引导token学习语义表示
- **Search range**: [0.01, 0.5]
- **Sensitivity**: medium
- **Source**: Sec 4.1

## 世界模型初始学习率
- **Value**: 1×10^{-4}
- **Rationale**: 大型autoregressive transformer的标准初始学习率
- **Search range**: [1×10^{-5}, 1×10^{-3}]
- **Sensitivity**: high
- **Source**: Sec 4.2

## 世界模型训练总步数
- **Value**: 100k
- **Rationale**: 总训练步数，约15天完成
- **Search range**: [50k, 200k]
- **Sensitivity**: medium
- **Source**: Sec 4.2

## 世界模型线性预热步数
- **Value**: 2.5k
- **Rationale**: 线性学习率预热步数
- **Search range**: [1k, 10k]
- **Sensitivity**: low
- **Source**: Sec 4.2

## 世界模型余弦衰减步数
- **Value**: 97.5k
- **Rationale**: 余弦衰减步数，学习率共降低10倍
- **Search range**: [50k, 150k]
- **Sensitivity**: medium
- **Source**: Sec 4.2

## 世界模型批大小
- **Value**: 128
- **Rationale**: 分布于64块A100 80GB GPU上训练
- **Search range**: [64, 256]
- **Sensitivity**: medium
- **Source**: Sec 4.2

## 世界模型AdamW权重衰减
- **Value**: 0.1
- **Rationale**: 较强权重正则化，防止大规模参数过拟合
- **Search range**: [0.01, 0.3]
- **Sensitivity**: medium
- **Source**: Sec 4.2

## 世界模型AdamW beta系数
- **Value**: (0.9, 0.95)
- **Rationale**: LLM训练惯用配置，beta2较低以更快适应梯度变化
- **Search range**: beta1 [0.8, 0.95], beta2 [0.9, 0.999]
- **Sensitivity**: low
- **Source**: Sec 4.2

## 世界模型梯度范数裁剪
- **Value**: 1.0
- **Rationale**: 防止梯度爆炸的标准范数裁剪阈值
- **Search range**: [0.5, 5.0]
- **Sensitivity**: medium
- **Source**: Sec 4.2

## 世界模型条件模式训练比例（无条件/动作/文本）
- **Value**: 20% / 40% / 40%
- **Rationale**: 三种条件模式的采样比例，支持无条件生成、动作条件生成和文本条件生成
- **Search range**: 各模式 [10%, 60%]，总和100%
- **Sensitivity**: high
- **Source**: Sec 4.2

## 视频解码器初始学习率
- **Value**: 5×10^{-5}
- **Rationale**: 扩散模型训练的初始学习率
- **Search range**: [1×10^{-5}, 1×10^{-4}]
- **Sensitivity**: high
- **Source**: Sec 4.3

## 视频解码器最终学习率（余弦衰减后）
- **Value**: 1×10^{-6}
- **Rationale**: 5k步余弦衰减后的最终学习率
- **Search range**: [1×10^{-7}, 1×10^{-5}]
- **Sensitivity**: medium
- **Source**: Sec 4.3

## 视频解码器训练总步数
- **Value**: 300k
- **Rationale**: 总训练步数，约15天完成
- **Search range**: [100k, 500k]
- **Sensitivity**: medium
- **Source**: Sec 4.3

## 视频解码器线性预热步数
- **Value**: 2.5k
- **Rationale**: 线性学习率预热步数
- **Search range**: [1k, 10k]
- **Sensitivity**: low
- **Source**: Sec 4.3

## 视频解码器批大小
- **Value**: 64
- **Rationale**: 分布于32块A100 80GB GPU上训练
- **Search range**: [32, 128]
- **Sensitivity**: medium
- **Source**: Sec 4.3

## 视频解码器AdamW权重衰减
- **Value**: 0.01
- **Rationale**: 扩散模型轻量正则化系数
- **Search range**: [0.001, 0.1]
- **Sensitivity**: low
- **Source**: Sec 4.3

## 视频解码器AdamW beta系数
- **Value**: (0.9, 0.99)
- **Rationale**: 扩散模型训练常用配置
- **Search range**: beta1 [0.8, 0.95], beta2 [0.95, 0.999]
- **Sensitivity**: low
- **Source**: Sec 4.3

## 视频解码器梯度范数裁剪
- **Value**: 1.0
- **Rationale**: 防止扩散模型训练中梯度爆炸
- **Search range**: [0.5, 5.0]
- **Sensitivity**: medium
- **Source**: Sec 4.3

## 视频解码器EMA参数衰减率
- **Value**: 0.999
- **Rationale**: 指数移动平均，稳定扩散模型训练
- **Search range**: [0.99, 0.9999]
- **Sensitivity**: medium
- **Source**: Sec 4.3

## 视频解码器损失权重 λ_{L1}
- **Value**: 0.1
- **Rationale**: 视频扩散去噪目标中L1分量权重
- **Search range**: [0.05, 0.5]
- **Sensitivity**: medium
- **Source**: Sec 4.3

## 视频解码器损失权重 λ_{L2}
- **Value**: 1.0
- **Rationale**: 视频扩散去噪目标中L2分量权重
- **Search range**: [0.5, 2.0]
- **Sensitivity**: medium
- **Source**: Sec 4.3

## 视频解码器条件token dropout概率
- **Value**: 0.15
- **Rationale**: 随机遮蔽条件图像token，提升模型泛化能力和时序一致性
- **Search range**: [0.05, 0.3]
- **Sensitivity**: medium
- **Source**: Sec 2.4

## 数据均衡采样指数
- **Value**: 0.5
- **Rationale**: 采样权重指数，0对应经验分布，1对应均匀分布，0.5为折中权衡
- **Search range**: [0, 1]
- **Sensitivity**: medium
- **Source**: Sec 3
