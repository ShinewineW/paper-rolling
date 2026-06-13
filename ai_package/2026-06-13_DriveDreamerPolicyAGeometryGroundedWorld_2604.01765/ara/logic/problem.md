# Problem Specification

## Observations

### O1: 现有 VLA 规划器多直接优化动作输出，缺少对未来世界演化的显式建模。
- **Statement**: 现有 VLA 规划器多直接优化动作输出，缺少对未来世界演化的显式建模。
- **Evidence**: 原文指出 most VLA planners primarily optimize action outputs and do not explicitly model how the future world may evolve under alternative actions。
- **Implication**: 这会削弱遮挡、隐藏风险等需要前瞻推理场景下的可解释性与可靠性。

### O2: 现有 world-action models 虽然统一生成与规划，但很多仍停留在
- **Statement**: 现有 world-action models 虽然统一生成与规划，但很多仍停留在图像、视频或潜变量层面。
- **Evidence**: 原文指出 world component is still implemented as image/video prediction or latent rollouts without explicit geometric grounding。
- **Implication**: 生成结果可能视觉上合理，却不一定给规划提供几何布局、自由空间和安全边界等结构化信息。

### O3: 自动驾驶被论文视为几何随时间演化的物理过程，深度适合作为紧凑的显式几何支架。
- **Statement**: 自动驾驶被论文视为几何随时间演化的物理过程，深度适合作为紧凑的显式几何支架。
- **Evidence**: 原文强调 autonomous driving is fundamentally a 4D physical process，并称 depth is compact, directly tied to geometry。
- **Implication**: 若把深度作为上游世界表示，视频想象和动作规划都能获得更直接的物理约束。

## Gaps

### G1: 只做动作预测的 VLA 方法缺少显式未来世界状态。
- **Statement**: 只做动作预测的 VLA 方法缺少显式未来世界状态。
- **Caused by**: 规划目标集中在轨迹或动作输出。
- **Existing attempts**: ['引入 driving world models 预测未来观测', '用 world-action models 统一未来生成与规划']
- **Why they fail**: 它们没有把候选动作下的未来观测变化作为模型内部目标来学习。

### G2: 只用图像、视频或潜变量的世界模型缺少几何落点。
- **Statement**: 只用图像、视频或潜变量的世界模型缺少几何落点。
- **Caused by**: 世界分支没有显式 depth 生成或几何约束。
- **Existing attempts**: ['用视频生成支撑可控仿真', '把视频生成潜变量接入规划器', '使用固定查询把生成专家接入 LLM']
- **Why they fail**: 外观可拟合并不等价于距离、遮挡、自由空间等规划关键信息被稳定表达。

### G3: 强耦合或表示不匹配会限制想象结果对动作预测的帮助。
- **Statement**: 强耦合或表示不匹配会限制想象结果对动作预测的帮助。
- **Caused by**: 模块设计耦合紧、世界表征与动作表征之间缺少结构化接口。
- **Existing attempts**: ['使用模块化生成专家', '用固定大小查询作为瓶颈接口', '采用 depth→video→action 的因果查询顺序']
- **Why they fail**: 生成分支和规划分支若没有清晰的信息流，规划器难以稳定消费世界表征。

## Key Insight
- **Insight**: 把深度作为显式几何支架放在视频和动作之前，可以让世界想象先获得空间结构，再把这些线索传给规划。
- **Derived from**: 论文对现有 WAM 缺少 geometric grounding 的诊断，以及 depth is compact, directly tied to geometry 的观察。
- **Enables**: 统一深度生成、未来视频生成和动作规划，并在同一次前向信息流中让后续分支消费上游几何与未来世界上下文。

## Assumptions
- 深度标签可由 Depth Anything 3 提供，论文将其作为训练用的现成深度来源。
- LLM 查询嵌入能作为紧凑接口承载语言意图、多视角感知、动作上下文和世界信息。
- 单目深度虽有歧义，但生成式目标比确定性回归更适合保留边界和不确定性。
- depth→video→action 的顺序足以表达论文所需的单向信息依赖，而无需迭代同步。
