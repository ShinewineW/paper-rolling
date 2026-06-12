# Heuristics

## H1: text prompts 使用 short、medium、long 三档 caption，并在训练中按 0.1/0.2/0.7 采样。
- **Rationale**: 让模型对 prompt length 更鲁棒，同时保留环境、天气、驾驶行为和交通描述。
- **Sensitivity**: 若长 caption 权重过低，可能削弱复杂场景属性控制；若短 caption 权重过低，可能降低对简短控制输入的适应。
- **Bounds**: 仅用于训练 caption 采样；caption 来自 10s-long temporal windows，并对 7 cameras 独立生成。
- **Code ref**: [Sec. 2.2 Text prompts]
- **Source**: 论文明确说明三档长度与采样概率。

## H2: world-scenario control 先在 93-frame clips 上训练到收敛，再扩展到 189-frame clips。
- **Rationale**: 先降低训练难度获得结构控制能力，再学习更长时间一致性。
- **Sensitivity**: 较短 clip 更易收敛但长程一致性不足；扩展过早可能增加训练成本和不稳定性。
- **Bounds**: 用于 world-scenario map control 训练阶段；论文没有给出更长或更短 clip 的系统扫描。
- **Code ref**: [Sec. 4.1 World-scenario map control]
- **Source**: 论文明确描述 93-frame 到 189-frame 的训练顺序。

## H3: view embeddings 与 Cross-View Attention 的 output projection weights 采用 zero-initialized。
- **Rationale**: 在从 Cosmos-Predict 2.5 迁移到多视角结构时稳定收敛，避免新分支一开始破坏已有生成能力。
- **Sensitivity**: 若不做 zero initialization，新增视角条件和 cross-view 子层可能在训练早期扰动 backbone。
- **Bounds**: 适用于 OmniDreams-MV 的 multi-view adaptation；不代表所有 control 分支都必须如此。
- **Code ref**: [Sec. 4.1 Multi-view adaptation]
- **Source**: 论文明确说明 view embeddings 和 cross-view attention 输出投影权重均 zero-initialized。

## H4: Self Forcing self-rollout 使用 2-step diffusion process，timestep schedule 为 [1000, 450]，且每次只对随机采样 denoising step 反传。
- **Rationale**: 用训练时自生成上下文匹配推理时条件分布，同时控制训练成本。
- **Sensitivity**: 步数或 schedule 改动会改变少步生成质量和速度；只对单步反传会依赖跨迭代覆盖。
- **Bounds**: 这是作者 implementation 中的设置；论文未报告替代 schedule 的消融。
- **Code ref**: [Sec. 4.3 Self Forcing Training via Self-Rollout]
- **Source**: 论文明确给出 2-step 与 [1000, 450]。

## H5: 长 rollout 中使用 rolling KV cache，并从 short-context teacher 继续到 progressive long-context bidirectional teacher。
- **Rationale**: rolling cache 控制复杂度，long-context teacher 用于缓解超过训练上下文后的 shifting artifacts。
- **Sensitivity**: teacher context 太短时会累积 temporal inconsistencies；cache window 太小可能损害 appearance 与 identity 保持。
- **Bounds**: 用于 Self Forcing distillation 后的长视频稳定性改进；具体 cache frame 数在 MD 中以乱码占位出现，不能精确复述。
- **Code ref**: [Sec. 4.3 Progressive Training with a Longer Teacher; Sec. 9.2 Long Rollouts]
- **Source**: 论文明确描述 shifting artifacts 与 progressive teacher 策略。

## H6: 推理期 temporal attention 限定为 local window：OmniDreams-SV 为 6 latent frames，OmniDreams-MV 为 8 latent frames。
- **Rationale**: 在 cache size、memory、speed 与长程上下文之间折中，使 per-chunk attention 成本可控。
- **Sensitivity**: window 变小可能损害长期一致性，变大则增加显存和延迟。
- **Bounds**: 这是 training-free inference optimization，不属于训练损失；SV/MV 设置不同。
- **Code ref**: [Sec. 5.1 Local temporal attention]
- **Source**: 论文明确给出 SV 和 MV 的 local-window 设置。

## H7: AlpaSim 选择 pre-fetch generation：在 chunk 边界先让 policy 和 traffic models 产出多步 trajectory，再请求 video model。
- **Rationale**: 保持事件顺序，避免 post-fetch 把逻辑上更早的 video frames 注入已经推进的 simulation timeline。
- **Sensitivity**: chunk 越长，policy 在 chunk 内越需要提前承诺轨迹；未来若 frame-at-a-time generation 可行，这个约束会减弱。
- **Bounds**: 这是 AlpaSim prototype 的集成选择；论文同时讨论 post-fetch，但实现选择 pre-fetch。
- **Code ref**: [Sec. 6.4.2 Pre-fetch generation]
- **Source**: 论文明确说明选择 pre-fetch 主要是 preserve ordering of events。

## H8: OOD object modeling 通过 randomized dynamic-cuboid dropout post-training，让动态 cuboids 随机从 abstract world-scenario map 中移除，静态 cuboids 保留。
- **Rationale**: 避免模型完全依赖 dynamic cuboids，从 visual history、first-frame seed 和上下文推断插入物体的持续性与运动。
- **Sensitivity**: dropout 过弱会继续依赖 cuboid，过强可能削弱结构条件对真实动态 actor 的约束。
- **Bounds**: 用于没有显式 cuboid trajectory 的 first-frame edit 传播；论文未给出 dropout 概率。
- **Code ref**: [Sec. 9.3.2 Out-of-Distribution Object Modeling]
- **Source**: 论文明确描述 randomized dynamic-cuboid dropout 的目的和静态 cuboid 保留。
