# Problem Specification

## Observations

### O1: 复杂具身任务需要智能体理解行动会如何改变未来状态，而 world model 可
- **Statement**: 复杂具身任务需要智能体理解行动会如何改变未来状态，而 world model 可以把这种理解转化为规划或想象训练。
- **Evidence**: 引言说明 world models 通过从智能体视角预测潜在行动的未来结果，让智能体在想象中选择动作。
- **Implication**: 如果世界模型足够准确，离线数据也能支持长程控制策略学习。

### O2: 既有 world model agent 在窄环境里快且准，但架构难以拟合复杂真
- **Statement**: 既有 world model agent 在窄环境里快且准，但架构难以拟合复杂真实分布。
- **Evidence**: 论文指出 Dreamer 3 等模型在游戏和机器人中表现强，但其架构缺乏拟合复杂真实世界分布的能力。
- **Implication**: 单纯沿用轻量级循环或窄域模型难以支撑 Minecraft 这类细节密集环境。

### O3: 可控视频模型能生成多样场景和简单交互，但对精确物体交互和游戏机制仍不可靠。
- **Statement**: 可控视频模型能生成多样场景和简单交互，但对精确物体交互和游戏机制仍不可靠。
- **Evidence**: 论文明确说 Genie 3 等可控视频模型仍难以学习 precise physics of object interactions and game mechanics，并且常需要多 GPU 才能实时模拟单场景。
- **Implication**: 仅有可扩展视频生成能力还不足以作为训练成功 agent 的环境。

## Gaps

### G1: 离线 Minecraft diamond challenge 同时要求长程动作序
- **Statement**: 离线 Minecraft diamond challenge 同时要求长程动作序列、原始像素理解和低层鼠标键盘控制。
- **Caused by**: 稀疏奖励、长程依赖、复杂 UI 操作和低层动作空间共同放大了离线学习难度。
- **Existing attempts**: ['VPT (finetuned) 使用大规模带动作标注的视频数据。', 'BC 与 VLA (Gemma 3) 尝试从 contractor actions 或视觉语言模型表征中学习策略。', 'WM+BC 使用 world model 表征做行为克隆，但尚未经过想象训练。']
- **Why they fail**: 行为克隆容易停留在数据中展示过的策略，越到后期里程碑越难推进。

### G2: 交互式 world model 需要在保持高容量的同时避免长 rollout 中
- **Statement**: 交互式 world model 需要在保持高容量的同时避免长 rollout 中误差积累。
- **Caused by**: 高频输出目标、长上下文 KV cache 成本和密集视频 token 注意力共同限制了质量与速度。
- **Existing attempts**: ['diffusion forcing 支持序列上不同信号等级的去噪。', 'shortcut models 用步长条件减少采样前向次数。', '高效 transformer 通过空间/时间分解注意力、较少时间层、GQA 和 register tokens 降低交互推理成本。']
- **Why they fail**: 传统 v-prediction 在逐帧生成长视频时会产生细微误差并随时间累积。

## Key Insight
- **Insight**: 把 world model 预训练、任务条件行为克隆、奖励建模与想象中的 policy optimization 串成同一套可扩展 transformer 流程，能把离线视频知识转化为可执行的长程控制策略。
- **Derived from**: 论文把 tokenizer、dynamics、agent tokens、reward/value/policy heads 和 PMPO imagination training 组织成 Dreamer 4，并在 Minecraft 离线 diamond 任务与 human interaction 评估中验证。
- **Enables**: 允许 agent 在没有在线环境交互的情况下，通过模型生成的轨迹改进策略，并用同一世界模型支持人类实时检查交互预测。

## Assumptions
- 冻结的 world model 在想象训练期间足够可靠，策略不会主要利用模型误差。
- VPT contractor dataset 中的事件标注足以构造任务奖励与 prompt sequence。
- Minecraft 的低层动作条件可以从少量配对动作视频泛化到更广的视频分布。
- 人类在 world model 中完成任务可作为复杂交互预测质量的有效检验。
