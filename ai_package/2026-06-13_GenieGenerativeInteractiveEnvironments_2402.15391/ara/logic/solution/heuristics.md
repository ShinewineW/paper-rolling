# Heuristics

## H1: 在所有组件中使用 ST-transformer，把空间注意力与时间注意力交替组织，并在时间层使用 causal mask。
- **Rationale**: 原文强调视频 token 数量很大，ST-transformer 让主导计算项随帧数线性增长，同时保持跨帧动态建模能力。
- **Sensitivity**: 若改为全时空注意力，内存压力会上升；若退化为空间-only tokenizer，原文消融显示视频保真与可控性方向上变差。
- **Bounds**: 适用于需要长序列视频生成但又受内存约束的设置；不保证解决长时域一致性，原文仍指出记忆长度受限。
- **Code ref**: [ST-transformer]
- **Source**: Methodology 与 Tokenizer architecture ablations

## H2: LAM 从原始像素而不是 tokenizer token 中学习 latent action。
- **Rationale**: 原文认为 tokenization 可能丢失运动和动态信息，像素输入在两个环境中带来更好的可控性方向。
- **Sensitivity**: 若改为 token-input，可能获得局部视频保真收益，但可控性更弱，且在 Robotics 上不保持优势。
- **Bounds**: 适用于动作标签缺失但可访问相邻原始帧的视频；推理期不会保留完整 LAM，只保留 codebook。
- **Code ref**: [Pixel-input]
- **Source**: Design choices for latent action model

## H3: 将 latent action 作为加性嵌入并入 LAM 与 dynamics model，而不是拼接到对应帧。
- **Rationale**: 原文明确说这种处理帮助提升生成的可控性。
- **Sensitivity**: 若改为常见的帧级拼接，可能弱化动作对预测 token 的控制效果。
- **Bounds**: 这是论文经验性设计选择；原文未给出单独公式化目标或独立消融表。
- **Code ref**: [additive embeddings]
- **Source**: Dynamics Model

## H4: 将 latent action codebook 维持为小型离散集合，以便人类可玩并加强可控性。
- **Rationale**: 原文说明小 vocabulary 能限制可选动作数量，使玩家或智能体更容易操控，同时迫使动作编码捕获过去到未来的关键变化。
- **Sensitivity**: 增加 code 数量可能提升表达能力，但原文指出会牺牲人类和 AI agent 的 playability。
- **Bounds**: 适用于低层动作语义较少、需要离散控制接口的环境；复杂连续控制可能需要重新权衡。
- **Code ref**: [num_codes]
- **Source**: Latent Action Model 与 Appendix C.1

## H5: 训练 dynamics model 时随机 mask 中间输入 token，并用 MaskGIT 预测未来帧 token。
- **Rationale**: 该策略让模型在不完整上下文下学习补全未来 token，符合 decoder-only MaskGIT 的生成流程。
- **Sensitivity**: mask 分布过弱会降低补全鲁棒性，过强会增加预测难度；原文仅给出采用的采样区间，未系统展开敏感性曲线。
- **Bounds**: 适用于离散 token 视频建模；不能直接替代像素空间连续扩散式生成。
- **Code ref**: [MaskGIT]
- **Source**: Dynamics Model
