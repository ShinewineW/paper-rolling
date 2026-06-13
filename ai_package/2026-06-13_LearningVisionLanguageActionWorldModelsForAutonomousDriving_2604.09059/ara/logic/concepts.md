# Concepts

## VLA-World
- **Notation**: p(\tau _ { t : t + H } , x _ { t + 1 } \mid o _ { 1 : t } , g ) = p(\tau _ { t : t + H } \mid o _ { 1 : t } , g) \cdot p(x _ { t + 1 } \mid o _ { 1 : t } , \tau _ { t + 1 })
- **Definition**: 一种面向端到端自动驾驶的统一框架，把VLA的感知、语言推理与动作生成能力和World Model的未来场景生成能力合并到同一流程中，用自生成的未来图像辅助反思式轨迹修正。
- **Boundary conditions**: 适用于论文设定中的自动驾驶多模态观测、目标条件和轨迹规划；不等同于通用视频生成器，也不代表无需结构化奖励或训练阶段即可获得反思能力。
- **Related concepts**: ['VLA Models', 'World Models', 'Predictive Imagination', 'Reflective Reasoning', 'Action and Trajectory Planning']

## VLA Models
- **Notation**: \pi _ { \boldsymbol { \theta } }(\tau _ { t : t + H })
- **Definition**: VLA模型把视觉感知、语言推理和动作生成放在大型语言或多模态语言模型框架中，学习从历史观测和任务目标到未来轨迹的直接映射。
- **Boundary conditions**: 概念边界是从观测到动作或轨迹的策略建模；它本身不显式生成未来环境状态，因此不能单独承担论文所说的未来想象功能。
- **Related concepts**: ['VLA-World', 'Vision-Language Models', 'Action and Trajectory Planning', 'Reflective Reasoning']

## World Models
- **Notation**: p _ { \psi } ( w _ { t + 1 } \mid w _ { t } , a _ { t } )
- **Definition**: World Model用于建模环境在动作影响下如何演化，通常学习潜在状态转移并通过解码器重建或想象未来观测。
- **Boundary conditions**: 它强调动态预测和未来想象，不等同于能直接输出安全驾驶决策；若只优化重建或像素保真，规划效用可能与安全目标脱节。
- **Related concepts**: ['VLA-World', 'Predictive Imagination', 'Condition-guided Generation', 'Latent Dynamics']

## Predictive Imagination
- **Notation**: \hat { x } _ { t + 1 } \sim p _ { \psi } ( x _ { t + 1 } \mid o _ { 1 : t } , \hat { \tau } _ { t : t + 1 } )
- **Definition**: 预测性想象是VLA-World利用短期预测轨迹条件化生成下一步未来图像的能力，用来把计划可能导致的场景变化显式可视化。
- **Boundary conditions**: 论文中它服务于驾驶推理和轨迹规划；不能把它理解为独立追求最真实图像的生成任务，也不能把推理期图像证据混同为人工构造的训练损失。
- **Related concepts**: ['Condition-guided Generation', 'Short-term Prediction', 'Visual Tokens', 'Reflective Reasoning']

## Reflective Reasoning
- **Notation**: \tilde { \tau } _ { t : t + H } = f _ { \mathrm { r e f } }(o _ { 1 : t } , \hat { x } _ { t + 1 } , \hat { \tau } _ { t : t + 1 })
- **Definition**: 反思式推理是在生成未来图像之后，对其中的重要实体、运动线索、潜在交互和风险进行分析，并据此修正初始轨迹。
- **Boundary conditions**: 它依赖模型自生成的未来图像和结构化推理流程；不是任意文本解释，也不是只在输出端附加理由而不改变规划结果。
- **Related concepts**: ['Predictive Imagination', 'Thinking with Visual Tokens', 'Action and Trajectory Planning', 'Self-Verification']

## Short-term Prediction
- **Notation**: \hat { \tau } _ { t : t + 1 }
- **Definition**: 短期预测模块把当前感知结果、历史自车状态和目标信息转换为近未来路点与驾驶方向，作为未来图像生成的条件。
- **Boundary conditions**: 它只描述短期演化基础，不等同于最终长时域轨迹；最终轨迹还要经过生成图像和反思式推理的修正。
- **Related concepts**: ['Perception', 'Condition-guided Generation', 'Physics-grounded Trajectory Predictor', 'Action and Trajectory Planning']

## Condition-guided Generation
- **Notation**: Q _ { t + 1 } ^ { k }, q _ { i } ^ { k }, \hat { I } _ { t + 1 } ^ { k }
- **Definition**: 条件引导生成是将编码后的场景上下文和预测路点转化为近未来视觉token，再解码为下一帧图像的模块。
- **Boundary conditions**: 它关注由预测轨迹和方向约束的近未来帧；不是只依据过去图像自由采样，也不是直接替代动作或轨迹规划模块。
- **Related concepts**: ['Visual Tokens', 'Predictive Imagination', 'VQGAN', 'Short-term Prediction']

## Visual Tokens
- **Notation**: P ( Q _ { t + 1 } ^ { k } ) = \prod _ { i = 1 } ^ { N } P _ { \theta } ( q _ { i } ^ { k } \mid q _ { < i } ^ { k } , h _ { t } , L )
- **Definition**: 视觉token是由VQGAN码本表示的离散图像符号序列，VLA-World在视觉预训练和条件生成中自回归预测这些token以生成未来图像。
- **Boundary conditions**: 视觉token必须对应有效码本条目才能重建有意义图像；它不是自然语言token，也不能单独表达完整驾驶决策。
- **Related concepts**: ['Condition-guided Generation', 'VQGAN', 'Thinking with Visual Tokens', 'Visual Pretraining']

## Thinking with Visual Tokens
- **Notation**: <Think>
- **Definition**: Thinking with Visual Tokens是论文中连接想象和决策修正的认知层，模型在生成未来视觉内容后分析显著实体、运动线索和潜在风险。
- **Boundary conditions**: 它是结构化输出流程中的推理阶段；不能脱离生成的未来视觉证据，也不等同于只输出可读解释而不影响后续动作。
- **Related concepts**: ['Reflective Reasoning', 'Visual Tokens', 'Condition-guided Generation', 'Action and Trajectory Planning']

## GRPO-based Self-Verification
- **Notation**: A _ { i } = \frac { r _ { i } - \mu } { \sigma }
- **Definition**: GRPO-based Self-Verification是强化学习阶段的相对优化机制，通过一组候选输出的规则奖励和组内归一化优势，引导模型保留更安全、更合规的推理与规划路径。
- **Boundary conditions**: 它不依赖神经奖励模型，而依赖轻量规则验证器；它是训练阶段的策略优化方法，不是推理时手工搜索所有候选轨迹。
- **Related concepts**: ['Reflective Reasoning', 'Rule-based Rewards', 'Self-Verification', 'Action and Trajectory Planning']
