# Problem Specification

## Observations

### O1: 闭环自动驾驶评测需要环境对 policy action 产生即时反馈，否则无法测
- **Statement**: 闭环自动驾驶评测需要环境对 policy action 产生即时反馈，否则无法测试动作如何改变后续场景演化。
- **Evidence**: Introduction 与 Figure 1 描述 policy、AlpaSim 和 OmniDreams 之间的闭环交互。
- **Implication**: 世界模型必须同时具备动作条件控制、低延迟生成和长时一致性。

### O2: reconstruction-based neural simulators 在
- **Statement**: reconstruction-based neural simulators 在真实记录附近很强，但受限于最初采集的数据。
- **Evidence**: Introduction 明确指出这类工作 anchored to captured data，难以扩展到 captured corridor 之外、新内容或新条件。
- **Implication**: 长尾天气、未观察动态物体和偏离原轨迹视角需要生成式模型补足。

### O3: 通用视频生成模型不能直接满足闭环 AV simulator 的交互需求。
- **Statement**: 通用视频生成模型不能直接满足闭环 AV simulator 的交互需求。
- **Evidence**: Model Architecture 将 OmniDreams 与 offline video generation methods 区分，强调 causal diffusion、streaming KV cache 和当前 conditioning。
- **Implication**: 需要把视频扩散骨干改造成按块、自回归、可服务化的世界模型。

## Gaps

### G1: 离线视频模型可生成长片段，但不天然支持策略动作逐步改变未来观测。
- **Statement**: 离线视频模型可生成长片段，但不天然支持策略动作逐步改变未来观测。
- **Caused by**: 推理形式与 closed-loop simulator 的时序接口不匹配。
- **Existing attempts**: ['causal masking', 'Diffusion Forcing', 'streaming KV cache']
- **Why they fail**: 双向或离线采样依赖完整片段上下文，无法自然对应闭环中逐步到来的 action。

### G2: 重建式仿真在偏离采集轨迹或引入未见内容时质量下降。
- **Statement**: 重建式仿真在偏离采集轨迹或引入未见内容时质量下降。
- **Caused by**: 场景表示被原始采集数据约束。
- **Existing attempts**: ['world-scenario map conditioning', 'text prompt control', 'generative video prior']
- **Why they fail**: 它主要重放或外推已捕获射线与场景结构，缺少可生成新动态和新外观的视觉先验。

### G3: 自回归视频扩散容易在长 rollout 中累积错误。
- **Statement**: 自回归视频扩散容易在长 rollout 中累积错误。
- **Caused by**: teacher forcing 与自回归推理分布不一致。
- **Existing attempts**: ['Self Forcing', 'DMD', 'progressive long-context teacher']
- **Why they fail**: 训练时依赖 clean context，推理时依赖自己生成的 imperfect outputs，形成 exposure bias。

## Key Insight
- **Insight**: 把 Cosmos 的视觉先验、world-scenario map 控制、因果 KV-cache 自回归和 Self Forcing distillation 组合起来，可以把生成式视频模型变成实时闭环 sensor simulator。
- **Derived from**: 论文从 reconstruction-based simulators 的外推限制、offline video models 的交互缺口以及 autoregressive rollout 的误差累积三类问题推导出该设计。
- **Enables**: 支持动作条件、多视角一致、长时 rollout 和 AlpaSim 中的闭环策略评测。

## Assumptions
- first-frame RGB seed 与 abstract world-scenario map 足以约束闭环仿真的关键驾驶线索。
- Cosmos-Predict 2.5 的视觉先验经过 AV 数据 mid-training 和 post-training 后可迁移到自动驾驶传感器生成。
- 以 chunk 为单位的延迟和状态缓存语义可以被 AlpaSim 的 microservice 架构接受。
- NuRec 在接近记录轨迹时可作为 reconstruction-based reference 来比较闭环评测一致性。
