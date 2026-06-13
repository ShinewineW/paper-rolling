# Related Work

## R1: Jonathan Ho and Stefano Ermon. Generative adversarial imitation learning. In Advances in Neural Information Processing Systems. Curran Associates, Inc., 2016.
- **DOI**: None
- **Type**: imitation learning
- **Delta**:
  - What changed: COMBAT 不要求为所有 agents 提供 explicit state-action supervision，而是在只给出 Player 1 actions 的部分观测设置中学习 Player 2 行为。
  - Why: 论文用 GAIL 代表需要完整动作监督的 imitation learning 路线，并以此突出 COMBAT 的 partially observed data 设置。
- **Claims affected**: ['C2']
- **Adopted elements**: []

## R2: Junyu Chen, Han Cai, Junsong Chen, Enze Xie, Shang Yang, Haotian Tang, Muyang Li, Yao Lu, and Song Han. Deep compression autoencoder for efficient high-resolution diffusion models, 2025.
- **DOI**: None
- **Type**: autoencoder compression
- **Delta**:
  - What changed: COMBAT 采用 DCAE 思路压缩 Tekken 3 frames，并进一步使用 visual–pose latent representation 支持世界模型训练。
  - Why: 高压缩 latent representation 让 Diffusion Transformer 能在潜空间中建模长序列 gameplay。
- **Claims affected**: ['C1']
- **Adopted elements**: ['DCAE', 'joint RGB–pose variational autoencoder']

## R3: William Peebles and Saining Xie. Scalable diffusion models with transformers. arXiv preprint arXiv:2212.09748, 2022.
- **DOI**: None
- **Type**: diffusion transformer
- **Delta**:
  - What changed: COMBAT 将 DiT backbone 用于 action-conditioned interactive environment，而不是一般图像生成。
  - Why: 论文认为 Transformer-based diffusion models 更适合复杂时空关系，并据此构建 autoregressive world model。
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['Diffusion Transformer', 'AdaLNZero']

## R4: Tianwei Yin, Qiang Zhang, Richard Zhang, William T Freeman, Fredo Durand, Eli Shechtman, and Xun Huang. From slow bidirectional to fast autoregressive video diffusion models. 2025.
- **DOI**: None
- **Type**: distillation
- **Delta**:
  - What changed: COMBAT 将 CausVid DMD 用于将 fully-trained DiT 蒸馏为 few-step interactive sampler。
  - Why: 实时交互要求降低 diffusion sampling 成本，同时尽量保持视觉质量和行为质量。
- **Claims affected**: ['C4']
- **Adopted elements**: ['CausVid DMD', 'Distribution Matching Distillation']

## R5: Dani Valevski, Yaniv Leviathan, Moab Arar, and Shlomi Fruchter. Diffusion models are real-time game engines. In International Conference on Representation Learning, pages 73754–73776, 2025.
- **DOI**: None
- **Type**: neural game engine
- **Delta**:
  - What changed: COMBAT 延续 action-conditioned neural game simulation 的方向，但将重点转向没有显式监督的 reactive opponent behavior。
  - Why: 论文把实时 neural game engine 作为背景，说明现有工作已能从 frames 和 actions 学习可交互仿真，而 COMBAT 进一步关注多智能体行为涌现。
- **Claims affected**: ['C2', 'C4']
- **Adopted elements**: ['action-conditioned world modeling', 'real-time neural simulation framing']
