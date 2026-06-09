# Concepts

## 生成式世界模型（Generative World Model）
- **Notation**: 输入序列为 $$( \mathbf{c}_1, \mathbf{z}_1, \mathbf{a}_1, \ldots, \mathbf{c}_T, \mathbf{z}_T, \mathbf{a}_T )$$，其中 $\mathbf{c}_t$ 为文本令牌、$\mathbf{z}_t$ 为图像令牌、$\mathbf{a}_t$ 为动作令牌
- **Definition**: 一种能够学习环境结构化表示、预测未来可能状态的生成模型。它将世界建模问题转化为无监督序列建模问题，通过预测离散令牌序列中的下一个令牌来隐式掌握世界的运行规律，同时具备生成高保真视频样本的能力。
- **Boundary conditions**: 论文将世界模型定位为自驾驾驶场景下的应用，训练数据为英国伦敦城市驾驶场景。自回归生成过程尚不能实时运行，但论文指出该过程天然适合并行化以并发生成多个样本。
- **Related concepts**: ['自回归下一令牌预测', '向量量化图像标记化', '视频扩散解码器', '世界模型缩放定律']

## 向量量化图像标记化（VQ Image Tokenization）
- **Notation**: 每张图像 $\mathbf{x}_t$ 经编码器 $E_\theta$ 量化为 $\mathbf{z}_t = E_\theta(\mathbf{x}_t)$，包含 $$n = \frac{H}{D} \times \frac{W}{D}$$ 个离散令牌，词汇表大小为 $K$；在 $H \times W = 288 \times 512$、$D = 16$ 时，$n = 18 \times 32 = 576$，$K = 8192$
- **Definition**: 使用离散自编码器将连续图像帧压缩为有限词汇表中的离散令牌序列的技术。编码器将图像在空间上下采样后，通过最近邻查找从可学习嵌入表中选取离散索引，从而把每帧图像表示为一组整数令牌。
- **Boundary conditions**: 由于解码器在单张图像上训练，直接对视频解码时缺乏时序一致性；论文为此另行训练了视频扩散解码器。量化本身带来信息损失，代码本（codebook）的词汇表大小 $K$ 决定了表示精度与序列长度的权衡。
- **Related concepts**: ['DINO语义蒸馏归纳偏置', '自回归下一令牌预测', '视频扩散解码器']

## DINO语义蒸馏归纳偏置（DINO Semantic Distillation Inductive Bias）
- **Notation**: 归纳偏置损失：量化后的图像特征与预训练 DINO 模型图像特征之间的余弦相似度损失，权重为 $\lambda_{L_{\mathrm{DINO}}} = 0.1$
- **Definition**: 在训练图像标记化器时，通过余弦相似度损失将预训练DINO自监督视觉模型的语义特征蒸馏到量化图像令牌中的技术，引导压缩方向从高频像素信号偏向语义表示。
- **Boundary conditions**: DINO模型以固定权重作为教师，仅蒸馏单帧图像级语义，不建模时序语义信息。蒸馏损失权重 $\lambda_{L_{\mathrm{DINO}}} = 0.1$ 相对较小，以避免过度压制重建质量损失。
- **Related concepts**: ['向量量化图像标记化', '自回归下一令牌预测']

## 自回归下一令牌预测（Autoregressive Next-Token Prediction）
- **Notation**: $$L_{\mathrm{worldmodel}} = -\sum_{t=1}^{T}\sum_{i=1}^{n}\log p(z_{t,i} \mid \mathbf{z}_{<t},\, z_{t,j<i},\, \mathbf{c}_{\leq t},\, \mathbf{a}_{<t})$$
- **Definition**: 将视频未来预测问题转化为「给定历史所有令牌、预测序列中下一个图像令牌」的条件分类问题，采用带因果掩码的自回归变换器实现。这是大语言模型范式在世界建模领域的直接迁移。
- **Boundary conditions**: 仅预测图像令牌（不预测文本或动作令牌），因果掩码确保不存在信息泄漏。对于超出上下文长度的长视频生成，采用滑动窗口策略。
- **Related concepts**: ['生成式世界模型', '向量量化图像标记化', '无分类器引导', 'Top-k采样策略', '世界模型缩放定律']

## 无分类器引导（Classifier-Free Guidance）
- **Notation**: $$l_{\mathrm{final}} = (1+t)\,l_{\mathrm{conditioned}} - t\,l_{\mathrm{unconditioned}}$$
- **Definition**: 在推理阶段通过放大有条件logits与无条件logits之间差异来增强生成内容与条件提示对齐程度的技术，同时支持「负提示」以主动远离不期望的特征。
- **Boundary conditions**: 引导缩放因子及调度策略是需针对具体用例调整的超参数。训练时通过随机丢弃条件令牌使模型支持无条件生成，这是无分类器引导成立的前提条件。
- **Related concepts**: ['自回归下一令牌预测', '生成式世界模型']

## 视频扩散解码器（Video Diffusion Decoder）
- **Notation**: $$L_{\mathrm{video}} = \mathbb{E}_{\epsilon,\,t^{\prime}}\left[\left\|\epsilon_\theta(\mathbf{x}^{t^{\prime}},\,t^{\prime},\,\mathbf{z},\,\mathbf{m}) - \epsilon\right\|_2^2\right]$$
- **Definition**: 基于去噪扩散概率模型的多任务视频生成组件，将世界模型自回归生成的离散图像令牌翻译回高分辨率、时序一致的像素空间视频，同时承担时序超分辨率（从6.25Hz恢复至25Hz）任务。
- **Boundary conditions**: 解码器（2.6B参数）与世界模型（6.5B参数）分开训练；推理时使用DDIM采样器共50个扩散步骤，不能实时生成。条件令牌以概率 $p=0.15$ 随机掩码以提升泛化能力。
- **Related concepts**: ['向量量化图像标记化', '生成式世界模型', '自回归下一令牌预测']

## Top-k采样策略（Top-k Sampling Strategy）
- **Notation**: 超参数 $k$ 由图像帧令牌数（$n=576$）及码本词汇量大小（$K=8192$）共同决定；论文实验中使用 $k=50$
- **Definition**: 在自回归生成时，从预测概率分布中仅保留概率最高的前k个令牌，并仅从这k个候选中采样下一令牌，以同时规避「argmax退化循环」和「尾部分布越界」两种极端失效模式。
- **Boundary conditions**: 该策略仅适用于离散令牌空间的自回归采样，是推理期超参数；论文提到 $k$ 值的选择与帧令牌数和码本大小相关，但未给出通用的选择公式。
- **Related concepts**: ['自回归下一令牌预测', '生成式世界模型']

## 世界模型缩放定律（World Model Scaling Laws）
- **Notation**: $$f(x) = c + (x/a)^b$$；计算量估计采用 $C = 6N$（$N$ 为不含嵌入层的参数量，$C$ 为单令牌前向+反向浮点运算次数），总计算量 $= C \times$ 训练令牌数
- **Definition**: 在以序列建模方式训练的驾驶世界模型上发现的、与大语言模型类似的幂律形式的计算量-性能关系：通过小规模模型的训练曲线可准确外推大规模模型的最终交叉熵。
- **Boundary conditions**: 外推前提是问题被表述为无监督序列建模（下一令牌预测），若切换为其他训练目标（如扩散损失）则缩放规律不直接适用。论文指出该计算量估计为近似值。
- **Related concepts**: ['自回归下一令牌预测', '生成式世界模型']

## 因式分解时空位置嵌入（Factorized Spatio-Temporal Positional Embedding）
- **Notation**: 共 $T$ 个时间嵌入（每时间步内的所有令牌共享）；共 $m + n + l = 32 + 576 + 2 = 610$ 个空间嵌入（依次对应文本/图像/动作令牌位置）；嵌入维度 $d = 4096$
- **Definition**: 独立建模「令牌在时间步中的位置（空间嵌入）」和「时间步在序列中的位置（时间嵌入）」的位置编码方案，通过将两类可学习嵌入相加赋予每个令牌完整的时空坐标感知能力。
- **Boundary conditions**: 使用可学习嵌入而非固定正弦嵌入，因此嵌入能力受限于训练时见过的最大序列长度 $T=26$；超长视频生成需借助滑动窗口，而非直接外推位置嵌入。
- **Related concepts**: ['自回归下一令牌预测', '向量量化图像标记化']
