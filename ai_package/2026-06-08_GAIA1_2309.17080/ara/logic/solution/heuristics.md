# Heuristics

## H1: 世界模型 token 采样采用 top-k=50 策略
- **Rationale**: argmax 采样使 perplexity 极低导致预测帧陷入重复循环;全分布采样会从低概率尾部采到离分布 token。top-k=50 产生与真实帧相近的 perplexity 分布,兼顾多样性与真实性
- **Sensitivity**: 高:k 过小则多样性不足,k 过大则采到低质尾部 token
- **Bounds**: k=50(Section 5.1 Figure 6 明确标注)
- **Code ref**: [top-k sampling]
- **Source**: Section 5.1, Figure 6

## H2: 分类器自由引导尺度需在 token 维度和帧维度上分别调度
- **Rationale**: 固定尺度导致连续帧间引导累积失控。在 token 上线性递减保证帧内多样性,在帧上余弦衰减避免跨帧过度引导
- **Sensitivity**: 中:引导尺度和调度是需针对具体应用场景调优的超参
- **Bounds**: token 维度线性递减,帧维度余弦衰减(可含初始平台期)
- **Code ref**: [classifier-free guidance schedule]
- **Source**: Section 5.1

## H3: 世界模型将视频从 25Hz 时间下采样至 6.25Hz
- **Rationale**: 降低序列长度使长序列建模可行;视频解码器再做时序超分辨率恢复全帧率
- **Sensitivity**: 高:采样频率直接决定序列长度与上下文时间覆盖范围
- **Bounds**: 6.25Hz(T=26 帧,约 4 秒片段,总序列长 15860)
- **Code ref**: [temporal subsampling]
- **Source**: Section 2.3, 4.2

## H4: 训练数据按特征经验分布反比加权采样,平衡指数取 0.5
- **Rationale**: 指数 0 等同原始分布(无平衡),指数 1 等同完全均匀分布;0.5 是平衡效果与丢弃样本效率之间的折中
- **Sensitivity**: 中:影响训练数据分布但不改变模型结构
- **Bounds**: 指数=0.5(论文 Section 3 明确说明)
- **Code ref**: [data balancing exponent]
- **Source**: Section 3

## H5: 世界模型训练按 20%/40%/40% 比例混合无条件/动作条件/文本条件三种模式
- **Rationale**: 随机 dropout 条件 token 使模型同时具备无条件、动作条件和文本条件生成能力
- **Sensitivity**: 中:影响各条件模式的生成质量与能力均衡
- **Bounds**: 无条件 20%,动作条件 40%,文本条件 40%
- **Code ref**: [conditioning dropout ratios]
- **Source**: Section 4.2

## H6: 视频解码器训练时对条件图像 token 以 p=0.15 随机 dropout
- **Rationale**: 防止解码器过度依赖 token 信息,提高泛化能力和时序一致性
- **Sensitivity**: 低至中
- **Bounds**: p=0.15
- **Code ref**: [conditioning dropout p=0.15]
- **Source**: Section 2.4

## H7: 视频解码推理时从序列末尾向前倒序自回归解码
- **Rationale**: 实验发现从末帧向前解码能产生更稳定的物体和更少的地平线闪烁
- **Sensitivity**: 中:影响视频时序稳定性
- **Bounds**: 全程倒序(Section 5.2 明确说明)
- **Code ref**: [backward autoregressive decoding]
- **Source**: Section 5.2

## H8: 推理期视频解码以 p=0.25 概率随机切换至图像/视频去噪加权平均(w=0.5)
- **Rationale**: 平衡「体现 token 信息内容」与「时序一致性」两个相互竞争的目标
- **Sensitivity**: 中
- **Bounds**: p=0.25, w=0.5
- **Code ref**: [image-video denoising weighted average]
- **Source**: Section 5.2
