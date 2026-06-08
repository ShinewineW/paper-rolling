# Problem Specification

## Observations

### O1: 在大量互联网文本上训练的 LLM 虽可能获取物理世界相关知识，但往往难以将该知识
- **Statement**: 在大量互联网文本上训练的 LLM 虽可能获取物理世界相关知识，但往往难以将该知识与真实世界的交互和动态建立联系
- **Evidence**: 论文 Introduction 明确指出：「a key limitation of these models lies in their ability to ground their knowledge in the physical world」
- **Implication**: 仅靠文本预训练无法赋予模型物理 AI 所需的具身推理与物理常识接地能力

### O2: 当前最先进 VLM 在时间箭头、空间拼图、物体恒存等基础直觉物理任务上仍接近随机
- **Statement**: 当前最先进 VLM 在时间箭头、空间拼图、物体恒存等基础直觉物理任务上仍接近随机猜测水平，而这些任务在常规基准（如 MMMU）上难以被发现
- **Evidence**: Table 10 显示 Gemini 2.0 Flash、Qwen2.5-VL-7B 在时间箭头任务上均约为 50.0，与随机猜测（50.0）持平
- **Implication**: 现有多模态评测基准未能充分揭示模型对物理世界的真实理解缺口

### O3: 数学和代码领域依赖精确定义的正确答案来构建可验证奖励，而物理常识和具身推理通常是
- **Statement**: 数学和代码领域依赖精确定义的正确答案来构建可验证奖励，而物理常识和具身推理通常是开放式回答，使得奖励分配复杂化
- **Evidence**: 论文第 5.2 节原文：「physical common sense and embodied reasoning typically involve free-form, open-ended responses that complicate reward assignment」
- **Implication**: 需要专门的转化策略才能将物理 AI 任务适配到规则可验证的 RL 训练范式

## Gaps

### G1: 缺乏系统定义和衡量物理 AI 推理能力的本体论框架与对应评测基准
- **Statement**: 缺乏系统定义和衡量物理 AI 推理能力的本体论框架与对应评测基准
- **Caused by**: C1
- **Existing attempts**: []
- **Why they fail**: 现有通用 VLM 基准未针对空间、时间、基础物理等物理 AI 关键能力进行细粒度划分，无法指导有针对性的数据采集和模型评估

### G2: 缺乏专门面向物理常识和具身推理的大规模视频-长链式推理数据集
- **Statement**: 缺乏专门面向物理常识和具身推理的大规模视频-长链式推理数据集
- **Caused by**: C1
- **Existing attempts**: []
- **Why they fail**: 现有机器人/自动驾驶数据集缺少适合物理 AI SFT 的密集推理追踪标注，直接使用现有数据源无法满足需求

### G3: 在物理 AI 领域难以直接设计规则可验证的 RL 奖励
- **Statement**: 在物理 AI 领域难以直接设计规则可验证的 RL 奖励
- **Caused by**: C3
- **Existing attempts**: ['将物理 AI 推理样本统一转化为单一正确答案的多选题（MCQ）格式，从而支持字符串匹配的规则验证']
- **Why they fail**: 具身推理的开放式答案无法像数学题一样通过字符串匹配自动核验

## Key Insight
- **Insight**: 通过为物理常识和具身推理分别建立结构化本体论，设计自监督直觉物理任务（时间箭头、空间拼图、物体恒存），并将所有物理 AI 任务统一转化为 MCQ 格式，可以在无需独立奖励模型的条件下，将长链式推理 RL 训练范式迁移至物理 AI 领域
- **Derived from**: C6
- **Enables**: 利用 GRPO 算法和规则可验证奖励对多模态 VLM 进行物理 AI 后训练，显著提升物理常识、具身推理和直觉物理能力

## Assumptions
- 物理 AI 推理可分解为物理常识推理（无具身依赖）和具身推理（依赖主体类型）两个正交维度
- 视频输入作为「复杂感知输入」的代表性形式，足以为物理世界接地提供充分信号
- 将具身推理转化为 MCQ 格式不会显著降低任务难度或引入系统性虚假奖励信号（分析推断，论文未显式声明）
- DeepSeek-R1 通过文本化视觉上下文蒸馏生成的推理追踪质量，足以作为 SFT 监督信号
