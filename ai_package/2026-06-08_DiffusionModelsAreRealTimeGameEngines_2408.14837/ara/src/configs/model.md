## 基础预训练模型
- **Value**: Stable Diffusion v1.4
- **Rationale**: 开源且开放权重，支持低成本微调，具备良好的图像生成能力，适合在单 TPU 上实时运行
- **Search range**: N/A
- **Sensitivity**: 高
- **Source**: Sec 3.2, Sec 4.2

## 动作条件引入方式
- **Value**: 每个动作嵌入为单个 token，通过交叉注意力替换原文本注意力输入
- **Rationale**: 简单有效；动作条件在推理时不使用 CFG（论文发现动作 CFG 无明显提升）
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec 3.2, Sec 3.3.1

## 历史帧条件引入方式
- **Value**: 编码为 latent 后在通道维度与含噪 latent 拼接
- **Rationale**: 简单直接；论文也测试了交叉注意力方式，但未见明显改善
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec 3.2

## 上下文长度
- **Value**: 64 帧
- **Rationale**: 消融实验表明 64 帧在质量与计算开销间取得最佳平衡；更长上下文边际收益迅速递减
- **Search range**: 消融测试了 {1, 2, 4, 8, 16, 32, 64}
- **Sensitivity**: 中
- **Source**: Sec 4.2, Sec 5.2.1, Table 2

## 推理采样算法
- **Value**: DDIM
- **Rationale**: 支持少步高质量采样，与训练时的 v-prediction 参数化一致
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec 3.3.1

## 推理 DDIM 采样步数
- **Value**: 4
- **Rationale**: 4 步与 20 步以上质量相当（Table 1），总推理耗时 50ms 即 20 FPS；单步无蒸馏质量明显下降
- **Search range**: 测试了 1、2、4、8、16、32、64 步及 1 步蒸馏
- **Sensitivity**: 高
- **Source**: Sec 3.3.2, Table 1

## Classifier-Free Guidance 权重
- **Value**: 1.5
- **Rationale**: 较小权重避免自回归采样中伪影放大；仅对历史帧条件使用 CFG
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 中
- **Source**: Sec 3.3.1

## latent 自编码器压缩规格
- **Value**: 8x8 像素块 → 4 latent 通道
- **Rationale**: Stable Diffusion v1.4 预训练自编码器规格；HUD 等细节因此产生伪影，需额外微调解码器
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec 3.2.2

## 噪声调度类型
- **Value**: 线性（linear）
- **Rationale**: 沿用 Stable Diffusion v1.4 的线性噪声调度（与 Rombach et al. 2022 一致）
- **Search range**: N/A
- **Sensitivity**: 低
- **Source**: Sec 3.2

## RL 智能体观测分辨率
- **Value**: 160x120
- **Rationale**: 下采样版帧图像，适配轻量级 CNN 特征提取网络
- **Search range**: N/A
- **Sensitivity**: 低
- **Source**: Sec 4.1

## RL 智能体图像特征维度
- **Value**: 512
- **Rationale**: CNN 图像特征提取网络输出的表示向量维度，每张图像独立提取
- **Search range**: N/A
- **Sensitivity**: 低
- **Source**: Sec 4.1

## RL 智能体历史动作序列长度
- **Value**: 32
- **Rationale**: 为智能体提供近期动作历史以辅助时序决策
- **Search range**: N/A
- **Sensitivity**: 低
- **Source**: Sec 4.1

## RL 智能体策略与价值网络结构
- **Value**: 2 层 MLP（以图像特征与动作序列拼接为输入）
- **Rationale**: 遵循 Mnih et al. (2015b) 的标准 Atari CNN+MLP 架构设计
- **Search range**: N/A
- **Sensitivity**: 低
- **Source**: Sec 4.1
