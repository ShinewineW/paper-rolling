# Heuristics

## H1: 噪声增强最大噪声水平设为 0.7,分 10 个离散桶各自学习嵌入
- **Rationale**: 缓解自回归漂移:训练时对上下文帧加入随机高斯噪声并将噪声水平作为额外输入,使模型学会纠正前帧误差,防止长序列质量快速退化
- **Sensitivity**: 高 — Section 5.2.2 与图 7 显示无噪声增强时质量在 10-20 帧内快速退化,有噪声增强时保持稳定
- **Bounds**: 最大噪声水平 0.7;推理时可设为 0(无噪声)仍有质量改善
- **Code ref**: [noise_augmentation / noise_level]
- **Source**: Section 3.2.1 及 Section 4.2

## H2: DDIM 推理步数固定为 4 步
- **Rationale**: 在单 TPU-v5 上每步 10ms,4 步 U-Net 共 40ms,加自编码器 10ms,总延迟 50ms,实现 20 FPS;4 步与 8~64 步质量相当
- **Sensitivity**: 中 — 单步质量明显下降(Table 1 中 1 步 PSNR 为 25.47,4 步为 32.58),4 步是质量与速度的甜点
- **Bounds**: 最少 4 步保持质量;单步需配合蒸馏(1000 步训练)才可恢复质量并达 50 FPS
- **Code ref**: [ddim_steps / num_inference_steps]
- **Source**: Section 3.3.2 及 Table 1

## H3: 历史上下文长度固定为 64 帧(约 3.2 秒的历史)
- **Rationale**: 更长上下文改善生成质量,但 Table 2 显示边际收益快速递减,64 帧已接近渐近线
- **Sensitivity**: 中低 — 从 1 帧到 64 帧 PSNR 有明显提升(20.94→22.36),但 32→64 仅微幅改善
- **Bounds**: 最小 1,最大 64;进一步增大在当前架构下收益极小
- **Code ref**: [context_length / N]
- **Source**: Section 4.2 及 Table 2

## H4: 推理时 CFG 权重设为 1.5,仅对历史帧条件(past observations)施加,不对动作条件施加
- **Rationale**: 较大权重在自回归生成中会因误差累积产生伪影,小权重 1.5 在质量与稳定性之间取得平衡
- **Sensitivity**: 高 — 更大权重会产生随自回归步数累积的伪影
- **Bounds**: 论文使用 1.5;未对动作条件施加 CFG(实验显示无明显改善)
- **Code ref**: [cfg_weight / guidance_scale]
- **Source**: Section 3.3.1

## H5: 训练时以概率 0.1 丢弃历史帧条件以支持推理期 CFG
- **Rationale**: Classifier-Free Guidance 要求模型同时被训练为有条件与无条件生成模式
- **Sensitivity**: 低 — 标准 CFG 训练做法
- **Bounds**: 概率 0.1
- **Code ref**: [context_drop_prob]
- **Source**: Section 4.2
