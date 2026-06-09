# Concepts

## 动作世界模型（Action World Model）
- **Notation**: $$M _ { \psi } : \left\{ \begin{array} { l } { { a _ { t } = M _ { \psi } ^ { \mathrm { p o l i c y } } ( a _ { t } | \ o _ { t - h : t } , l ) , } } \\ { { o _ { t } = M _ { \psi } ^ { \mathrm { w o r l d } } ( o _ { t } | \ o _ { t - h : t - 1 } , a _ { t - h : t - 1 } ) , } } \end{array} \right.$$
- **Definition**: 同时具备动作生成（策略模型）和未来视觉状态预测（世界模型）能力的统一自回归模型，以文本、图像、动作作为输入，输出动作序列与未来帧。
- **Boundary conditions**: 与单纯的视频预测模型不同，动作世界模型的视觉生成以动作为条件，而不仅依赖任务描述；与单纯的VLA模型不同，它同时输出视频帧与动作，而非只输出动作。
- **Related concepts**: ['VLA模型', '世界模型', '自回归语言模型']

## 动作注意力掩码策略（Action Attention Masking）
- **Notation**: 论文未给出显式公式，仅通过图3(b)示意：当前动作token对先前动作token的注意力权重被置零，对图像/文本token保持因果可见。
- **Definition**: 一种修改的注意力掩码机制，在生成当前动作时屏蔽所有先前动作的可见性，使每个动作仅依赖文本和视觉输入，而非依赖前序动作。
- **Boundary conditions**: 该掩码仅用于动作模型部分；世界模型部分仍使用标准因果注意力掩码。该策略不修改模型参数，仅改变注意力可见性模式。
- **Related concepts**: ['动作分块生成', '因果注意力掩码', '误差传播']

## 动作分块生成（Action Chunking）
- **Notation**: 动作分块大小K在实验中对LIBERO-Long任务设为10，对其余三个LIBERO任务设为5。
- **Definition**: 在一次前向传播中自回归地生成K个连续动作token的机制，旨在提升机器人操作的效率与连贯性。
- **Boundary conditions**: 分块生成与连续动作模型（使用l1回归损失并行输出多动作）不同；这里的分块生成基于离散自回归方式，通过掩码机制使其逼近并行生成的效果，但底层仍是自回归架构。
- **Related concepts**: ['动作注意力掩码策略', '误差传播', '并行解码']

## 统一多模态词表（Unified Vocabulary）
- **Notation**: 文本BPE词表大小65536，其中包含8192个图像token（VQ-GAN码本）和256个动作token（每维度256个bin）；动作用7个token表示（3个相对位置 + 3个相对角度 + 1个夹爪状态）。
- **Definition**: 将文本token、图像token和动作token映射到同一词汇空间，使单一LLM可在同一序列内理解并生成三种模态的内容。
- **Boundary conditions**: 与基于扩散头的统一模型（如UVA）不同，WorldVLA的统一词表使动作生成完全融入自回归文本/图像生成流程，但代价是离散化带来的精度损失，因此在性能上与连续动作模型存在一定差距。
- **Related concepts**: ['VQ-GAN图像分词器', '动作离散化', 'Chameleon']

## 世界模型与动作模型的互增强（Mutual Enhancement）
- **Notation**: 联合训练损失：$$\mathcal{L} = \mathcal{L}_{action} + \alpha \mathcal{L}_{world}$$，其中 $\mathcal{L}_{action}$ 和 $\mathcal{L}_{world}$ 分别为动作模型数据和世界模型数据的交叉熵损失，$\alpha$ 用于平衡两部分损失贡献（实验中固定为0.04）。
- **Definition**: 世界模型通过学习预测动作条件下的未来帧，帮助动作模型理解环境物理动态；动作模型通过生成动作促进视觉理解，反过来提升世界模型的视频生成质量。两者在联合训练框架中相互促进。
- **Boundary conditions**: 互增强效果在长序列视频生成（50帧）上比短序列（10帧）更显著；视频预测模型（无动作条件）因预测目标不唯一而存在歧义，无法稳定提升动作模型性能，这与有动作条件的世界模型形成对比。
- **Related concepts**: ['动作世界模型', '联合训练', 'FVD', '抓取成功率']

## 误差传播（Error Propagation in Autoregressive Action Generation）
- **Notation**: 论文未给出显式公式；该现象通过消融实验（Table 3 第3行 vs 第4行）和图6的分块长度-成功率曲线定量展示。
- **Definition**: 在自回归动作生成中，先前生成的动作若存在预测误差，会通过注意力机制影响后续动作的生成，导致误差沿序列方向累积放大的现象。
- **Boundary conditions**: 误差传播是自回归离散动作生成特有的挑战；连续动作模型（如扩散策略）通常并行生成多动作，不存在自回归序列内的动作间条件依赖，因此不受此问题影响。世界模型部分使用标准因果掩码但不受此问题困扰，因为图像token的预测泛化能力更强。
- **Related concepts**: ['动作分块生成', '动作注意力掩码策略', '自回归语言模型']
