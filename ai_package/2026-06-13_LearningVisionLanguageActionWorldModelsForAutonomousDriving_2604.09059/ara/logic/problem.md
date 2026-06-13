# Problem Specification

## Observations

### O1: 现有VLA模型擅长把感知、语言推理和动作生成统一起来，但对场景随时间演化的显式建
- **Statement**: 现有VLA模型擅长把感知、语言推理和动作生成统一起来，但对场景随时间演化的显式建模不足。
- **Evidence**: 引言和预备部分说明VLA通常从历史观测与目标直接映射到轨迹，缺少explicit modeling of temporal dynamics and world consistency。
- **Implication**: 模型容易关注自车动作，难以可靠推断其他交通参与者的运动，从而限制前瞻性和安全性。

### O2: 现有world model能够生成未来场景，但通常缺少对生成未来的反思性评估。
- **Statement**: 现有world model能够生成未来场景，但通常缺少对生成未来的反思性评估。
- **Evidence**: 相关工作和预备部分说明world model能simulate plausible futures，但不能评估这些未来是否安全、可行或值得执行。
- **Implication**: 只追求未来帧逼真度会让想象与驾驶决策收益脱节，生成结果未必能提升规划。

### O3: 短时轨迹条件下生成的未来帧可以作为反思推理的显式证据。
- **Statement**: 短时轨迹条件下生成的未来帧可以作为反思推理的显式证据。
- **Evidence**: 方法部分把预测轨迹、未来帧生成和reflective reasoning串联，并说明generated future image用于识别重要目标和潜在风险。
- **Implication**: 规划器获得了一个可检查的未来假设，可在输出最终轨迹前修正不安全或不一致的决定。

## Gaps

### G1: VLA路线缺少显式世界演化环节。
- **Statement**: VLA路线缺少显式世界演化环节。
- **Caused by**: 训练目标主要围绕轨迹或动作生成，世界一致性和时序动态没有成为中间约束。
- **Existing attempts**: ['语言推理增强动作解释', 'GRPO强化自反思', '端到端轨迹模仿']
- **Why they fail**: 直接从观测到动作的映射没有要求模型预测周围动态体随自车行为如何变化。

### G2: world model路线缺少面向驾驶后果的决策闭环。
- **Statement**: world model路线缺少面向驾驶后果的决策闭环。
- **Caused by**: 规划奖励没有直接回传到生成与推理链路，未来想象容易停留在模拟层面。
- **Existing attempts**: ['未来视频生成', '占用预测', '生成未来帧作为中间推理步骤']
- **Why they fail**: 生成模型通常学习视觉或潜变量转移，像素保真和交通安全收益之间可能不一致。

## Key Insight
- **Insight**: 本文的核心洞见是把短时动作条件下的未来帧当作模型自己的草稿纸，先想象再反思，从而把世界动态建模和驾驶决策收益接起来。
- **Derived from**: 来自VLA缺少时序世界一致性、world model缺少反思评估这两个缺口，以及方法部分的imagination到reflective reasoning闭环。
- **Enables**: 使同一模型能同时生成未来证据、检查风险并细化轨迹，形成更安全且更可解释的端到端规划。

## Assumptions
- 短时预测的未来帧足以携带对规划有用的时空线索。
- 生成未来的质量和反思推理之间存在可训练的耦合关系。
- 规则奖励能够为GRPO提供足够稳定的安全、格式、动作和轨迹反馈。
- 多任务混合数据能把感知、生成、推理和规划放入同一输出结构中学习。
