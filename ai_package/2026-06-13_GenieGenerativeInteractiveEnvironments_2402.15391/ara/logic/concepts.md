# Concepts

## Generative Interactive Environment
- **Notation**: Genie
- **Definition**: 一种从 video-only data 训练出的生成式交互环境范式，模型可由单个图像或文本相关提示启动，并在后续步骤中根据用户选择的 latent action 逐帧生成可交互轨迹。
- **Boundary conditions**: 它不是传统需要 Video + Actions 的 world model，也不是只在视频级别可控的 Video Models；其边界是当前主要展示为由像素视频学习出的可玩环境，且论文承认长时一致性与交互帧率仍有限。
- **Related concepts**: ['Latent Action Model', 'Video Tokenizer', 'Dynamics Model', 'Action-Controllable Video Generation']

## Latent Action Model
- **Notation**: LAM, $\tilde { \pmb { a } } _ { 1 : t }$, $a _ { t }$
- **Definition**: 用于从相邻视频帧之间推断 latent action 的模型；编码器接收历史帧和下一帧，输出连续 latent actions，训练时再通过 VQ-VAE 类目标压缩到小型离散代码集合。
- **Boundary conditions**: LAM 的解码器只提供训练信号；推理时除 VQ codebook 外，整个 LAM 被丢弃，并由用户输入的离散动作替代。
- **Related concepts**: ['Latent Action Space', 'Dynamics Model', 'Action-Controllable Video Generation', 'Behavioral Cloning with Latent Actions']

## Latent Action Space
- **Notation**: $| { \cal A } |$, $[ 0 , | { \cal A } | )$, $\tilde { a } _ { t }$
- **Definition**: 由 VQ codebook 形成的离散动作空间，用于限制模型可选择的 latent actions，并使人类或智能体可以在推理时以离散索引方式控制生成过程。
- **Boundary conditions**: latent actions 不等同于环境的 ground-truth actions；在需要落地到真实环境动作时，仍要通过少量 action-labeled expert sequences 建立 latent-to-real action 映射。
- **Related concepts**: ['Latent Action Model', 'Action-Controllable Video Generation', 'Controllability', 'Behavioral Cloning with Latent Actions']

## Video Tokenizer
- **Notation**: $\pmb { x } _ { 1 : T } \in \mathbb { R } ^ { T \times H \times W \times C }$, $\mathfrak { z } _ { 1 : T } \in \mathbb { I } ^ { T \times D }$
- **Definition**: 将原始视频帧压缩为离散 video tokens 的 VQ-VAE 模块，用于降低维度并为高质量视频生成提供离散表示。
- **Boundary conditions**: 不同于只关注 spatial-only compression 的 tokenizer；论文把它作为 dynamics model 的前置训练模块，先训练 tokenizer，再与 LAM 和 dynamics model 的后续训练流程衔接。
- **Related concepts**: ['ST-Transformer', 'Dynamics Model', 'Action-Controllable Video Generation']

## ST-Transformer
- **Notation**: ST-transformer, ST block, $1 \times H \times W$, $T \times 1 \times 1$
- **Definition**: 一种用于视频的 spatiotemporal transformer 结构，由交错的空间注意力层、时间注意力层和 feed-forward layer 组成，用于在多个 Genie 组件中处理视频 token。
- **Boundary conditions**: 它不是普通全注意力 transformer；论文还说明 ST block 中省略 post-spatial FFW，只在空间和时间组件之后保留一个 FFW，以便把计算用于扩大模型其他部分。
- **Related concepts**: ['Video Tokenizer', 'Latent Action Model', 'Dynamics Model']

## Dynamics Model
- **Notation**: $\mathfrak { z } _ { 1 : t - 1 }$, $\tilde { \mathbf { a } } _ { 1 : t - 1 }$, $\hat { \boldsymbol { z } } _ { t }$
- **Definition**: decoder-only MaskGIT transformer，接收过去的 video tokens 与 stopgrad latent actions，预测下一帧的离散 tokens，并以自回归方式生成后续帧。
- **Boundary conditions**: 动作不是按常见做法简单拼接到对应帧，而是作为 additive embeddings 注入；论文称这种处理改善了生成的 controllability。
- **Related concepts**: ['Video Tokenizer', 'Latent Action Model', 'Action-Controllable Video Generation', 'ST-Transformer']

## Action-Controllable Video Generation
- **Notation**: $x _ { 1 }$, ${ \mathfrak { z } } _ { 1 }$, $a _ { 1 }$, $\hat { \pmb { z } } _ { 2 : T }$, $\hat { x } _ { 2 : T }$
- **Definition**: Genie 推理阶段的逐帧交互生成流程：给定初始 prompt frame，用户选择离散 latent action，模型预测下一帧 tokens，再由 tokenizer decoder 解码成图像，并反复生成轨迹。
- **Boundary conditions**: 该过程使用用户动作替代训练期 LAM 的推断输出；因此推理控制来自离散 latent action 索引，而不是外部真实动作标签。
- **Related concepts**: ['Generative Interactive Environment', 'Latent Action Space', 'Dynamics Model', 'Video Tokenizer']

## Controllability
- **Notation**: $$\Delta _ { t } \mathrm { P S N R } = \mathrm { P S N R } ( x _ { t } , \hat { x } _ { t } ) - \mathrm { P S N R } ( x _ { t } , \hat { x } _ { t } ^ { \prime } ) ,$$
- **Definition**: 衡量 latent actions 对生成结果影响程度的概念；论文用基于 PSNR 的 $\Delta _ { t } \mathrm { P S N R }$ 比较真实推断动作与随机动作条件下生成帧相对 ground-truth 的差异。
- **Boundary conditions**: 这是本文提出的评估指标之一，只反映 latent action 对生成差异的影响；视频视觉质量则另用 FVD 衡量。
- **Related concepts**: ['Latent Action Space', 'Action-Controllable Video Generation', 'Dynamics Model']

## Behavioral Cloning with Latent Actions
- **Notation**: $a _ { t } \gets L A M ( x _ { t } , x _ { t + 1 } )$, $\pi ( \boldsymbol { a } _ { t } | \boldsymbol { x } _ { t } )$, $u _ { t } \sim D [ a _ { t } ]$
- **Definition**: 用冻结的 Genie LAM 从 unseen videos 中提取 latent action labels，再训练策略根据观察预测专家 latent action；执行时通过少量带真实动作标签的 expert sequences 建立 latent actions 到 real actions 的映射。
- **Boundary conditions**: 策略最终进入真实环境时仍需要 latent-to-real action 映射；论文明确用 expert data 做映射以便评估 learned policy 的质量，而不是声称完全不需要任何真实动作标签。
- **Related concepts**: ['Latent Action Model', 'Latent Action Space', 'Generative Interactive Environment']
