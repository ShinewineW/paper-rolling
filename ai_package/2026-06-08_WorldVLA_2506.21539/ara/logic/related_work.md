# Related Work

## R1: Kim et al., 2024 (OpenVLA)
- **DOI**: arXiv:2406.09246
- **Type**: baseline
- **Delta**:
  - What changed: WorldVLA 在 OpenVLA 的离散动作 token 化基础上，增加了世界模型联合训练分支，并引入新注意力遮蔽策略以实现动作块生成
  - Why: OpenVLA 是最直接的离散动作模型基线，WorldVLA 在相同离散框架下对比，以凸显世界模型集成的贡献
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['动作 token 化策略（每维 256 个 bin，共 7 个 token）', 'VLA 训练范式与数据预处理']

## R2: Team, 2024 (Chameleon)
- **DOI**: arXiv:2405.09818
- **Type**: backbone
- **Delta**:
  - What changed: WorldVLA 以 Chameleon 为基础，扩展了动作 token 词表（256 个动作 token），并增加了动作模型与世界模型的联合训练目标 $\mathcal{L} = \mathcal{L}_{action} + \alpha \mathcal{L}_{world}$
  - Why: Chameleon 提供了统一图像理解与生成的离散自回归框架，天然支持多模态 token 共享词表，是实现 WorldVLA 统一框架的合适基础
- **Claims affected**: ['C1']
- **Adopted elements**: ['VQ-GAN 图像分词器（压缩比 16，码本大小 8192）', 'BPE 文本分词器（词表 65536）', '因果注意力自回归架构']

## R3: Kim et al., 2025 (OpenVLA-OFT)
- **DOI**: arXiv:2502.19645
- **Type**: comparison
- **Delta**:
  - What changed: WorldVLA 采用离散自回归配合注意力遮蔽实现动作块生成，而 OpenVLA-OFT 使用连续动作头直接并行输出多步动作；WorldVLA 无需大规模预训练即在多项子任务上与 OpenVLA-OFT 形成竞争
  - Why: OpenVLA-OFT 是 LIBERO 上性能最强的连续动作模型基线之一，用于展示 WorldVLA 与当前最优方法的性能对比
- **Claims affected**: ['C1']
- **Adopted elements**: ['动作块并行生成的设计思路']

## R4: Li et al., 2025 (UVA)
- **DOI**: arxiv
- **Type**: comparison
- **Delta**:
  - What changed: WorldVLA 采用统一的离散自回归框架同时生成图像和动作，而 UVA 使用不同的扩散头分别生成图像和动作；WorldVLA 是 Action World Model 分类中的离散路线代表
  - Why: UVA 是另一种统一视频-动作模型，与 WorldVLA 同属 Action World Model 类别（Table 1），对比有助于分析离散自回归 vs 扩散头两种统一架构路线
- **Claims affected**: ['C1']
- **Adopted elements**: []

## R5: Wu et al., 2025 (iVideoGPT)
- **DOI**: NeurIPS 2025
- **Type**: comparison
- **Delta**:
  - What changed: WorldVLA 在世界模型视频生成能力之外增加了显式动作生成能力，而 iVideoGPT 仅输出视频而不输出动作
  - Why: iVideoGPT 是代表性离散世界模型，对比凸显 WorldVLA 在统一动作与视频生成方面的核心创新点
- **Claims affected**: ['C1']
- **Adopted elements**: []

## R6: Wu et al., 2023 (GR-1)
- **DOI**: arXiv:2312.13139
- **Type**: comparison
- **Delta**:
  - What changed: WorldVLA 采用以动作为条件的世界模型（需要理解动作输入），而 GR-1 使用无动作条件的视频预测模型作为辅助信号；实验显示有动作条件的世界模型在所有任务上均有正向效果
  - Why: GR-1 是将视频预测用于动作模型预训练的代表性方法，论文通过与其对比论证了有动作条件的世界模型优于无条件视频预测
- **Claims affected**: ['C7']
- **Adopted elements**: []

## R7: Black et al., 2024 (π0)
- **DOI**: arXiv:2410.24164
- **Type**: comparison
- **Delta**:
  - What changed: WorldVLA 采用离散自回归架构配合注意力遮蔽实现动作块生成，而 π0 采用流式扩散策略头实现连续多步动作并行生成
  - Why: π0 是连续动作模型中的代表，对比有助于定位 WorldVLA 在动作并行生成方法上的异同，说明注意力遮蔽策略的必要性
- **Claims affected**: ['C5']
- **Adopted elements**: ['动作块并行生成的设计目标']

## R8: Ha and Schmidhuber, 2018
- **DOI**: arXiv:1803.10122
- **Type**: foundational
- **Delta**:
  - What changed: WorldVLA 将世界模型与显式动作生成统一在同一自回归框架中，而 Ha & Schmidhuber 的经典世界模型框架中世界模型与控制器是分离的组件
  - Why: 该工作是世界模型领域的奠基性参考，WorldVLA 引用以说明世界模型预测未来视觉状态从而理解环境物理动态的基本能力
- **Claims affected**: ['C1']
- **Adopted elements**: []

## R9: Esser et al., 2021 (VQ-GAN)
- **DOI**: CVPR 2021
- **Type**: component
- **Delta**:
  - What changed: WorldVLA 在 VQ-GAN 基础上添加了针对特定图像区域（面部、显著对象）的感知损失，用于图像分词；压缩比固定为 16，码本大小 8192
  - Why: VQ-GAN 提供了将连续图像离散化为 token 的基础能力，是 WorldVLA 实现统一多模态 token 框架的关键组件
- **Claims affected**: ['C1']
- **Adopted elements**: ['离散图像分词器（256×256 图像生成 256 个 token，512×512 图像生成 1024 个 token）']
