# Concepts

## 世界基础模型 (World Foundation Model, WFM)
- **Notation**: $$\hat{x}_{t+1} = \mathcal{M}(x_{0:t}, c_t)$$
- **Definition**: 物理世界的数字孪生体，根据过去视觉观测序列 $x_{0:t}$ 和当前扰动 $c_t$（如动作、文本指令、随机干预等）预测未来世界状态 $\hat{x}_{t+1}$。作为通用预训练模型，可通过后训练精调为针对特定 Physical AI 场景的专用世界模型。
- **Boundary conditions**: 当前论文中观测空间为 RGB 视频；物理一致性仍有缺陷，模型未能完全遵循牛顿力学（如重力违反、物体凭空出现等），需要更好的数据筛选和模型设计。论文未展示 WFM 用于强化学习训练或模型预测控制的实证结果，仅列为未来方向。
- **Related concepts**: ['预训练后训练范式', 'Physical AI', '视频分词器', '扩散 WFM', '自回归 WFM']

## 视频分词器 (Video Tokenizer)
- **Notation**: $$\hat{x}_{0:T} = \mathcal{D}\bigl(\mathcal{E}(x_{0:T})\bigr)$$
空间压缩比 $s_{HW} = H/H' = W/W'$，时间压缩比 $s_T = T/T'$
- **Definition**: 将原始视频压缩为紧凑 token 序列的编解码架构，分为两类：连续分词器（Continuous Tokenizer，输出连续向量，供扩散模型使用）和离散分词器（Discrete Tokenizer，通过有限标量量化输出整数索引，供自回归模型使用）。Cosmos Tokenizer 采用因果时序卷积与注意力机制，并在小波域进行操作以消除像素冗余。
- **Boundary conditions**: 离散分词器词汇表大小固定为 64,000（FSQ 量化配置 8×8×8×5×5×5）；论文在 DAVIS 和 TokenBench 基准上评测；分词器具有时序长度无关的推理能力，可处理比训练时更长的视频。
- **Related concepts**: ['世界基础模型', '有限标量量化 (FSQ)', '时序因果设计', '扩散 WFM', '自回归 WFM']

## 预训练后训练范式 (Pre-training and Post-training Paradigm)
- **Notation**: 论文未给出显式公式描述整体范式；扩散 WFM 训练目标见公式 (5)–(8)，自回归 WFM 训练目标见公式 (9)。
- **Definition**: 两阶段训练策略：第一阶段用约 $10^8$ 个多样化视频片段进行大规模通用预训练，使 WFM 成为覆盖多种物理现象的通才；第二阶段用特定 Physical AI 场景的「提示-视频」配对数据对预训练 WFM 进行精调，生成面向具体应用（相机控制、机器人操作、自动驾驶等）的专用世界模型。
- **Boundary conditions**: 文中展示了相机控制、机器人操作、自动驾驶三类后训练示例，并明确标注为示范性应用（「-Sample」后缀），非面向生产的完整系统；开发者须在自有数据集上精调才能用于实际 Physical AI 场景。
- **Related concepts**: ['世界基础模型', '视频数据管道', '扩散 WFM 训练目标', '自回归 WFM']

## 时序因果分词 (Temporal Causal Tokenization)
- **Notation**: $$\{g_0, g_{0:1}, g_{0:2}, \ldots\} \to \{\xi_0, \xi_1, \xi_2, \ldots\}$$
最终输出 token $z_{0:T'} \in \mathbb{R}^{(1+T') \times H' \times W' \times C}$，第一帧 token 代表输入第一帧，使 $T=0$（图像）与 $T>0$（视频）共享同一潜空间。
- **Definition**: 分词器在时序维度采用因果设计，即处理当前帧时不依赖未来帧，通过因果时序卷积（左填充 $k-1$）和因果时序注意力（掩码）实现。在小波域中输入先以分组方式降采样 $\{x_0, x_{1:4}, x_{5:8}, \ldots\} \to \{g_0, g_1, g_2, \ldots\}$，后续各编码阶段以因果方式递进处理。
- **Boundary conditions**: 因果约束仅施加于时间维度；空间维度无因果限制。2 级 Haar 小波变换在空间和时间方向各下采样 4×，是减少后续层计算量的预处理步骤。
- **Related concepts**: ['视频分词器', '世界基础模型', 'Physical AI']

## EDM 扩散训练目标 (EDM Denoising Score Matching Loss)
- **Notation**: 基础去噪损失：
$$\mathcal{L}(D_\theta, \sigma) = \mathbb{E}_{\mathbf{x}_0, \mathbf{n}}\bigl[\|D_\theta(\mathbf{x}_0 + \mathbf{n}; \sigma) - \mathbf{x}_0\|_2^2\bigr]$$
总训练损失：
$$\mathcal{L}(D_\theta) = \mathbb{E}_\sigma\left[\frac{\lambda(\sigma)}{e^{u(\sigma)}}\mathcal{L}(D_\theta, \sigma) + u(\sigma)\right]$$
权重函数：
$$\lambda(\sigma) = \bigl(\sigma^2 + \sigma_{\mathrm{data}}^2\bigr) / (\sigma \cdot \sigma_{\mathrm{data}})^2$$
噪声级别采样：
$$\ln(\sigma) \sim \mathcal{N}(P_{\mathrm{mean}}, P_{\mathrm{std}}^2)$$
- **Definition**: 基于 EDM（Elucidated Diffusion Model）框架的去噪得分匹配训练目标，将多噪声级别的去噪视为多任务学习问题，引入连续不确定性函数 $u(\sigma)$ 对各噪声级别的损失贡献进行自适应加权，以缓解训练过程中各任务难度不均衡导致的梯度失衡。
- **Boundary conditions**: 此目标仅适用于扩散 WFM；自回归 WFM 使用负对数似然（NLL）损失（公式 9），两者相互独立。Video2World 模型在图像和视频条件帧位置不计入损失。
- **Related concepts**: ['扩散 WFM', '视频分词器', '预训练后训练范式']

## 自回归世界基础模型 (Autoregressive WFM)
- **Notation**: $$\mathcal{L}_{\mathrm{NLL}} = \sum_i -\log P(v_i \mid v_1, v_2, \ldots, v_{i-1}; \Theta)$$
z-loss：$\mathcal{L}_{\mathrm{z\text{-}loss}} = \lambda \cdot \sum_i z_i^2$（$\lambda = 3 \times 10^{-4}$）
- **Definition**: 将视频生成建模为下一离散 token 预测任务：先将视频通过离散分词器压缩为整数序列 $\mathcal{V} = \{v_1, v_2, \ldots, v_n\}$，再用 Transformer 解码器以过去 token 为上下文预测下一 token，类比大语言模型对文本的建模方式。架构包含 3D RoPE 位置编码、交叉注意力文本条件化、QK 归一化及 z-loss 训练稳定化。
- **Boundary conditions**: 文中 AR WFM 在固定空间分辨率 640×1024 训练；词汇表大小 64,000。4B/12B 基础模型不含文本理解能力，5B/13B Video2World 变体通过新增交叉注意力层引入文本条件。
- **Related concepts**: ['视频分词器（离散）', '扩散解码器', 'Medusa 推测解码', 'EDM 扩散训练目标']

## 扩散解码器 (Diffusion Decoder)
- **Notation**: 论文未给出扩散解码器独立的显式训练损失公式；训练时将嵌入后的离散 token 视频（每个 token 映射为 16 维向量，再在 $x, y$ 方向 2× 上采样与噪声输入对齐）拼接至去噪器通道维度，以 CV8×8×8 连续 token 为去噪目标，复用扩散 WFM 的去噪目标框架。
- **Definition**: 通过精调扩散 WFM 构建的高质量 token 解码桥梁：以自回归 WFM 输出的粗粒度离散 token 视频（DV8×16×16 压缩）为条件输入，求解逆扩散问题，将其映射到精细的连续 token 空间（CV8×8×8 压缩），再由连续分词器解码为 RGB 视频，从而补偿离散量化导致的细节损失。
- **Boundary conditions**: 扩散解码器通过精调 Cosmos-Predict1-7B-Text2World 获得，第一层通道维度扩展以容纳拼接的条件输入；推理时仅依赖 AR WFM 输出的离散 token，不需要原始视频。此方案引入额外推理延迟（如 Tab. 16 所示）。
- **Related concepts**: ['自回归 WFM', '扩散 WFM', '视频分词器']

## Medusa 推测解码 (Medusa Speculative Decoding)
- **Notation**: 论文未给出 Medusa 机制的显式公式；9 个 Medusa 头在 4B 模型上实现最优吞吐量/质量权衡，在 8×H100 GPU 上 4B 模型最高达 2.0× token 吞吐量与 4.6× 前向传播次数减少，5B 模型达 3.2× token 吞吐量与 6.1× 前向传播次数减少。
- **Definition**: 在自回归 WFM 的 Transformer 主干最后一层隐藏状态之后添加多个并行的单层 FFN 解码头（Medusa heads），每次前向传播并行预测多个后续 token，再通过拒绝采样验证，从而减少顺序解码所需的前向传播总次数，加速推理。训练时仅解冻最后两层 Transformer 层和最终 unembedding 层，以平衡推测精度与灾难性遗忘。
- **Boundary conditions**: 实验在 8×H100 80GB GPU 上基于 50 个未见测试视频（640×1024 分辨率）评测；不使用 Cai et al. 2024 中的树形注意力机制；当前实现不支持 MQA/GQA 等注意力优化变体。
- **Related concepts**: ['自回归 WFM', '低分辨率实时推理']
