# Problem Specification

## Observations

### O1: 交互式world model过去主要关注空间和时间一致的环境模拟，但动态、会反应
- **Statement**: 交互式world model过去主要关注空间和时间一致的环境模拟，但动态、会反应的agent仍是关键短板。
- **Evidence**: 摘要和引言明确说现有world models的显著限制是建模dynamic, reactive agents，它们会智能地影响并交互于世界。
- **Implication**: 如果只学静态场景或被控主体，模型难以覆盖真实多agent环境中最不可预测的部分。

### O2: Tekken 3提供了适合检验隐式行为学习的受控环境。
- **Statement**: Tekken 3提供了适合检验隐式行为学习的受控环境。
- **Evidence**: 论文将其描述为具有清晰视觉反馈、确定性game mechanics、多样movesets和frame-precise timing requirements的环境。
- **Implication**: 在这个环境里，生成错误更容易暴露为动作后果、节奏或对手反应的不一致。

### O3: COMBAT只把Player 1输入作为条件，却观察到Player 2出现blo
- **Statement**: COMBAT只把Player 1输入作为条件，却观察到Player 2出现block、counterattack和combo execution等行为。
- **Evidence**: 引言和结论都强调Player 2行为是在没有direct supervision of the opponent’s policy的情况下出现的。
- **Implication**: 论文把对手策略视为world modeling过程中的涌现属性，而不是显式监督训练出的独立policy。

## Gaps

### G1: 传统imitation learning需要完整的agent动作监督。
- **Statement**: 传统imitation learning需要完整的agent动作监督。
- **Caused by**: Player 2动作标签缺失，且行为只通过视频后果间接体现。
- **Existing attempts**: ['用world model学习条件视频生成，而不是显式拟合所有agent动作。', '让模型通过生成temporally consistent and plausible multi-agent interactions来隐式推断Player 2 policy。']
- **Why they fail**: 在部分可观测multi-agent轨迹中，对手的动作、观察和决策过程可能不可见。

### G2: 传统视频指标不能充分衡量未显式监督的战术能力。
- **Statement**: 传统视频指标不能充分衡量未显式监督的战术能力。
- **Caused by**: COMBAT的行为模式是通过world modeling隐式学习的。
- **Existing attempts**: ['提出基于health data的behavioral consistency metrics。', '提出Total Action Adherence和Action Ratio Consistency来用人类可解释的动作模式评估emergent behavior。']
- **Why they fail**: 视觉保真指标主要测perceptual quality，RL指标又假设可访问ground-truth actions或rewards。

### G3: 扩散采样天然较慢，直接用于游戏交互会受限。
- **Statement**: 扩散采样天然较慢，直接用于游戏交互会受限。
- **Caused by**: diffusion model推理需要多步去噪并持续生成后续帧。
- **Existing attempts**: ['采用CausVid DMD进行step distillation。', '使用static key-value caching复用attention states。', '对decoder进行student-teacher distillation以减少渲染开销。']
- **Why they fail**: 迭代采样计算密集，难以满足实时互动需求。

## Key Insight
- **Insight**: 如果生成模型必须在只看到Player 1条件的情况下持续产出合理的双人对战轨迹，它就被迫在潜空间中吸收Player 2的反应规律。
- **Derived from**: 论文的问题形式化、Key Innovation段落以及结论中关于temporal consistency导致intricate behaviors隐式出现的表述。
- **Enables**: 把部分可观测multi-agent录像转化为可训练的behavioral world model，并为不依赖完整动作标签的agent行为学习提供路径。

## Assumptions
- 近期画面历史足以近似决定下一步game state。
- Player 1输入和视觉状态中包含足够信息，可让模型推断Player 2的合理反应。
- Tekken 3的确定性机制和清晰视觉反馈能让视频生成目标承载行为学习信号。
- pose-augmented latent representation有助于保持角色运动结构一致性。
