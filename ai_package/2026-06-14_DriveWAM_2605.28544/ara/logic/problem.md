# Problem Specification

## Observations

### O1: VLM-centric driving policy 擅长语义理解，但其预训练主
- **Statement**: VLM-centric driving policy 擅长语义理解，但其预训练主要来自静态 image-text pair，时间密集的视觉动态先验需要更多下游驾驶数据学习。
- **Evidence**: 引言指出 VLM backbones are pretrained primarily on image-text data rather than video dynamics，并强调驾驶需要 spatial layout、motion continuity 和 future scene evolution。
- **Implication**: 仅靠 VLM 作为策略核心时，低层时空动态建模不是天然强项。

### O2: 视频生成模型天然包含物体持续性、运动模式和场景演化先验，适合动态决策。
- **Statement**: 视频生成模型天然包含物体持续性、运动模式和场景演化先验，适合动态决策。
- **Evidence**: 引言称 video generative models are pretrained on large-scale videos to model object persistence, motion patterns, and scene evolution。
- **Implication**: 把视频生成先验直接转成 world-action policy，有机会提升端到端驾驶的时空预测与动作生成。

### O3: 长时域 autoregressive rollout 需要历史上下文，但 ful
- **Statement**: 长时域 autoregressive rollout 需要历史上下文，但 full KV cache 成本随时域增长，FIFO 又可能丢掉旧但仍关键的证据。
- **Evidence**: 方法部分说明 full-window cache grows linearly with rollout length，sliding-window cache evicts oldest tokens，且 older tokens may remain decision-relevant。
- **Implication**: 需要一种有界但不只按时间淘汰的记忆机制。

## Gaps

### G1: 把 video foundation model 变成 ego-action c
- **Statement**: 把 video foundation model 变成 ego-action control policy 并不直接。
- **Caused by**: 预训练目标与 action control 目标不一致。
- **Existing attempts**: ['将 driving 分解为 future world modeling 和 inverse-dynamics action generation。', '把 video token 与 action token 组织进统一时序序列。', '用 joint flow-matching objective 同时训练 video branch 与 action branch。']
- **Why they fail**: 原始视频模型面向视觉生成，不直接输出连续驾驶动作。

### G2: 视频生成先验缺少高层语义规划，单一 clip-level text condit
- **Statement**: 视频生成先验缺少高层语义规划，单一 clip-level text condition 难以适配每个未来片段。
- **Caused by**: world-action methods 通常只用简单导航命令或固定文本条件。
- **Existing attempts**: ['引入 frozen Qwen3-VL-8B 作为 scene-evolving semantic guide。', '每个决策步只用因果可得的最新 observation、recent ego trajectory 和 route command 生成 guidance。', '通过 temporally localized cross-attention 注入 chunk-specific intent。']
- **Why they fail**: 同一段文本无法表达随路线、交通参与者和场景变化而改变的决策意图。

### G3: 长时域 rollout 中，完整历史太贵，固定窗口又可能丢失仍有预测价值的信息。
- **Statement**: 长时域 rollout 中，完整历史太贵，固定窗口又可能丢失仍有预测价值的信息。
- **Caused by**: 视频和动作 token 密度、功能不同，单一全局缓存会被视觉 token 主导。
- **Existing attempts**: ['维护分离的 video 与 action memory pools。', '用 relevance-redundancy retention 选择历史 token。', '只在 inference time 应用，不改变训练目标。']
- **Why they fail**: full cache 无界增长，FIFO 只看年龄不看任务相关性。

## Key Insight
- **Insight**: 核心洞见是让视频生成模型负责想象可行的未来世界，再让动作生成作为 inverse-dynamics readout 从这个未来中读出 ego motion，同时用 VLM 只补语义意图而不取代视频骨干。
- **Derived from**: ['C1', 'C2', 'C4', 'C5']
- **Enables**: 形成一个统一的 semantically guided world-action policy，在保留 video generative priors 的同时生成可执行驾驶动作。

## Assumptions
- pretrained video diffusion transformer 的时空生成先验能迁移到驾驶动作生成。
- 因果可得的 VLM guidance 足以提供 route intent 与 decision-level semantics。
- attention relevance 与 key redundancy 能作为保留长期历史 token 的有效代理信号。
