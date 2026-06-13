# Problem Specification

## Observations

### O1: 传统 world models 通常需要 video + actions 才能学
- **Statement**: 传统 world models 通常需要 video + actions 才能学习 action-conditioned next-frame prediction。
- **Evidence**: Table 1 将 World Models 标为 Training Data=Video + Actions、Controllability=Frame-level，而 Genie 标为 Training Data=Video、Controllability=Frame-level。
- **Implication**: 如果要利用公开 Internet videos，就必须把动作变量从视频本身中学出来。

### O2: 普通 video models 虽能从初始帧或文本生成视频，但控制粒度主要停留在
- **Statement**: 普通 video models 虽能从初始帧或文本生成视频，但控制粒度主要停留在 video-level。
- **Evidence**: Table 1 将 Video Models 标为 Training Data=Video + Text、Controllability=Video-level。
- **Implication**: 仅生成一段看起来合理的视频不足以支持玩家或 agent 持续交互。

### O3: 大规模视频建模会遇到 transformer 对视频 tokens 的计算与记忆
- **Statement**: 大规模视频建模会遇到 transformer 对视频 tokens 的计算与记忆成本问题。
- **Evidence**: 方法部分指出视频可包含 $O ( 1 0 ^ { 4 } )$ tokens，并采用 ST-transformer 平衡模型容量与计算约束。
- **Implication**: 要把可交互视频世界模型做大，需要在时空注意力结构上降低扩展成本。

## Gaps

### G1: Internet gameplay videos 丰富但通常没有动作标注。
- **Statement**: Internet gameplay videos 丰富但通常没有动作标注。
- **Caused by**: action annotation 成本高，且公开视频并不天然携带 ground-truth action labels。
- **Existing attempts**: ['从视频帧对中用 LAM 学 latent actions', '用 VQ-VAE-based objective 将动作限制为小离散 codebook', '推理时丢弃 LAM 主体，仅保留 VQ codebook 并接收用户动作']
- **Why they fail**: 直接训练 action-conditioned world model 缺少监督动作输入。

### G2: 空间-only 或全时空 tokenizer 都不能同时满足视频质量、可控性与可
- **Statement**: 空间-only 或全时空 tokenizer 都不能同时满足视频质量、可控性与可扩展性。
- **Caused by**: 视频压缩需要同时保留空间外观与跨帧动态。
- **Existing attempts**: ['在 tokenizer 编码器和解码器中使用 ST-transformer', '用 causal temporal layer 让每个离散编码包含历史帧信息', '在 ablation 中比较 ViT、C-ViViT 与 ST-ViViT']
- **Why they fail**: 空间-only 会损失时序动态，全时空注意力计算更重且可能过拟合。

## Key Insight
- **Insight**: 把动作看成可从视频变化中无监督抽取的离散 latent interface，而不是外部必须提供的标签。
- **Derived from**: LAM decoder 只能访问历史帧与 latent action，因此 latent action 被迫编码过去到未来的关键变化；dynamics model 再把这些 latent actions 当作条件来预测未来 tokens。
- **Enables**: Genie 能从 text-generated images、sketches、photos 或真实视频起步，让用户或 agent 逐帧选择 latent action 并生成后续轨迹。

## Assumptions
- 视频中的连续帧变化包含足够稳定的行为因素，可被小型离散 latent action codebook 捕获。
- Platformers 等领域的视觉动态与控制语义具有跨场景一致性。
- 用生成式 next-frame prediction 学到的 latent actions 可迁移到 unseen RL environments 的 imitation 场景。
