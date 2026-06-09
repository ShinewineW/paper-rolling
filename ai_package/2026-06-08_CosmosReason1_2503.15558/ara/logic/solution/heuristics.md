# Heuristics

## H1: SFT阶段7B模型使用余弦退火学习率, 从 $1 \times 10^{-5}$ 衰减至 $1 \times 10^{-6}$
- **Rationale**: 余弦退火在训练末期平稳降低学习率, 有助于稳定收敛并避免过拟合
- **Sensitivity**: 中: 初始学习率边界对最终性能影响较显著
- **Bounds**: 初始 $1 \times 10^{-5}$, 最终 $1 \times 10^{-6}$
- **Code ref**: [N/A]
- **Source**: Sec. 7.1

## H2: SFT阶段56B模型先以学习率 $1 \times 10^{-5}$ 训练, 再以衰减后的 $1 \times 10^{-6}$ 继续训练
- **Rationale**: 两段式学习率调度适合大规模模型, 前段充分学习后段精细收敛
- **Sensitivity**: 中
- **Bounds**: 第一段 $1 \times 10^{-5}$, 第二段 $1 \times 10^{-6}$
- **Code ref**: [N/A]
- **Source**: Sec. 7.1

## H3: SFT阶段使用fused Adam优化器, $\beta_1, \beta_2 = (0.9, 0.95)$, 权重衰减0.1; 7B全局批大小256, 56B全局批大小32
- **Rationale**: 较高的 $\beta_2$ 使梯度平方估计更稳定, 适合大模型; 权重衰减抑制过拟合; 56B批大小受限于显存
- **Sensitivity**: 中
- **Bounds**: $\beta_1=0.9$, $\beta_2=0.95$, weight_decay=0.1
- **Code ref**: [N/A]
- **Source**: Sec. 7.1

## H4: 推理评估时对同一问题采样5次(temperature=0.6, top-p=0.95), 取平均准确率作为最终指标
- **Rationale**: 多次采样平均可降低解码随机性带来的评估方差, 使结果更稳定可靠
- **Sensitivity**: 低: 5次平均已足够稳定
- **Bounds**: temperature=0.6, top-p=0.95, 采样次数=5
- **Code ref**: [N/A]
- **Source**: Sec. 7.1

## H5: RL阶段全局批大小128个问题, 每题采样9个输出, 每输出最大长度6144 tokens, 学习率 $4 \times 10^{-6}$, KL惩罚系数0.005, 训练500迭代步
- **Rationale**: 每题多路输出是GRPO组内归一化优势估计的核心需求; 小学习率与KL约束共同保证RL阶段策略稳定
- **Sensitivity**: 高: 每题输出数量直接影响优势函数质量; KL系数过大限制改进空间
- **Bounds**: batch=128, outputs_per_q=9, max_tokens=6144, lr=$4 \times 10^{-6}$, kl_coeff=0.005, iters=500
- **Code ref**: [N/A]
- **Source**: Sec. 7.2.1

## H6: 56B视频输入每帧统一调整至448×448像素, 每帧产生1024个视觉token后经PixelShuffle 2×2下采样至256 tokens; 每视频最多均匀采样32帧, 最大帧率2帧/秒
- **Rationale**: 限制帧数与分辨率是视频理解质量与计算开销之间的工程权衡
- **Sensitivity**: 中: 帧数减少会丢失时序细节
- **Bounds**: frame_size=448×448, tokens_per_frame=256 (downsampled from 1024), max_frames=32, max_fps=2
- **Code ref**: [N/A]
- **Source**: Sec. 3.1

## H7: RL训练中MCQ选项在每个训练步在线随机打乱, 确保模型泛化到不同选项顺序
- **Rationale**: 防止模型对固定选项位置产生偏差, 避免奖励破解(reward hacking)
- **Sensitivity**: 中: 不打乱会导致位置偏差
- **Bounds**: N/A
- **Code ref**: [N/A]
- **Source**: Sec. 7.2.1
