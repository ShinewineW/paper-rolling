# Concepts

## Uni-World VLA
- **Notation**: 输入为历史 ego-centric frames、ego status 与文本提示；输出为未来 RGB frames 与 ego positions。
- **Definition**: 一种统一的 Vision-Language-Action 自动驾驶模型，把未来帧预测与轨迹规划放在同一个自回归生成框架中处理。
- **Boundary conditions**: 它面向 autonomous driving 的未来场景与轨迹联合预测；论文没有把它描述为通用机器人 VLA，也没有引入外部传感器融合 beyond 文中列出的输入。
- **Related concepts**: ['Vision-Language-Action', 'world model', 'Show-o', 'MagVIT-v2', 'NAVSIM']

## interleaved frame-action generation
- **Notation**: d̂_{t+k} 由既有动态 token 与既有 action token 条件化生成；â_{t+k} 由截至当前的动态 token 与既有 action token 条件化生成。
- **Definition**: 一种逐步交替生成未来视觉 token 与 action token 的范式；每生成一个未来帧后，同时间戳的 action query 被送回 LLM 来预测 ego position，再用于后续生成。
- **Boundary conditions**: 这不是先生成完整 rollout 再规划的 predict-then-plan，也不是只并行训练但任务功能解耦的 predict-and-plan。
- **Related concepts**: ['action query', 'visual tokens', 'action tokens', 'closed-loop interaction', 'autoregressive generation']

## contextual tokens
- **Notation**: c = Encoder_MagVIT(I) 的一部分，解码未来帧时作为 per-second scale 的视觉引导。
- **Definition**: 由高分辨率历史帧编码得到的离散视觉 token，用于提供详细的场景语义和结构信息。
- **Boundary conditions**: 它们不是 action token，也不直接表示 ego velocity、acceleration 或 high-level driving command。
- **Related concepts**: ['MagVIT-v2', 'dynamic tokens', 'historical visual information', 'context token embeddings']

## dynamic tokens
- **Notation**: d = Encoder_MagVIT(I) 的一部分；未来动态 token 记作 d̂_{t+k}。
- **Definition**: 由较低分辨率、高频采样的历史视觉流编码得到的离散 token，用于捕捉细粒度运动线索和短期时间变化。
- **Boundary conditions**: 它们不等同于 RGB 帧本身，需要通过 MagVIT-v2 decoder 才能重构为未来图像。
- **Related concepts**: ['MagVIT-v2', 'contextual tokens', 'future frame prediction', 'Dynamic Focal Loss']

## action tokens
- **Notation**: â_{t+1}, â_{t+2}, …, â_{t+N} 构成 planned trajectory。
- **Definition**: 对应 ego-vehicle trajectory 的 token 表示；LLM 中与 action token 对应的 hidden states 会送入 MLP head 回归未来 ego positions。
- **Boundary conditions**: 论文附录说明 inference 时 ego status 直接投影到 embedding space，而不是离散化为 token；不要把 ego status 输入与未来 action token 输出混同。
- **Related concepts**: ['action query', 'MLP head', 'ego status', 'trajectory prediction']

## depth fusion
- **Notation**: context token embeddings 和 dynamic token embeddings 分别作为 query，与 CDE 和 DDE 输出的 key、value 做 CA 融合。
- **Definition**: 使用 Depth Anything 3 从输入图像估计 monocular depth maps，并通过 cross-attention 将深度特征与历史视觉 token 融合。
- **Boundary conditions**: 论文说它增强 historical visual prompts 的空间感知，但没有把未来帧生成改成显式深度建模任务。
- **Related concepts**: ['Depth Anything 3', 'CDE', 'DDE', 'cross-attention', 'monocular depth']

## Dynamic Focal Loss
- **Notation**: ω(d_{t+k}^i, d_{t+k-1}^i) 根据相邻 token 是否变化在 α 与 β 之间选择，且 α > β。
- **Definition**: 用于视觉 token 预测的动态加权交叉熵，给相邻帧中发生变化的 token 更高权重，以缓解大量静态 token 主导监督的问题。
- **Boundary conditions**: 它只覆盖视觉 token 生成项；轨迹预测另用 L1 loss，最终目标是视觉生成损失与轨迹损失的加权和。
- **Related concepts**: ['future visual token generation', 'MagVIT-v2 vocabulary', 'dynamic tokens', 'training objectives']

## bi-directional intra-frame attention
- **Notation**: 生成当前 future frame 时，新视觉 token 可关注所有 previous tokens 与 current frame 内全部 token。
- **Definition**: 一种注意力掩码设计，使同一帧内的 token 可以相互关注，同时保留跨时间的 causal masking。
- **Boundary conditions**: 它不是让未来时间步泄漏给过去时间步；跨时间仍然遵守自回归因果结构。
- **Related concepts**: ['attention mask', 'causal masking', 'future frame prediction', 'temporal dependencies']

## KV-cache interleaved inference
- **Notation**: 从当前帧开始生成 t+1 visual tokens，解码后追加 action query，再把生成 token 附加到 context 继续生成后续步。
- **Definition**: 推理时逐步生成未来帧和 action，并缓存 previous steps 的 key 与 value 表示，后续只为新生成 token 计算注意力。
- **Boundary conditions**: KV-cache 是推理效率机制，不是训练目标，也不改变论文定义的 frame-action 生成顺序。
- **Related concepts**: ['autoregressive inference', 'KV-cache', 'interleaved frame-action generation', 'attention mask']
