# Problem Specification

## Observations

### O1: 现有 LLM/VLM 虽通过大规模网络文本学习到物理世界知识,但难以将该知识与真
- **Statement**: 现有 LLM/VLM 虽通过大规模网络文本学习到物理世界知识,但难以将该知识与真实物理交互和动态相联系
- **Evidence**: 论文 Abstract 中明确指出:「they often struggle to establish connections between that knowledge and real-world interactions and dynamics」
- **Implication**: 单纯扩大文本预训练数据不足以赋予模型物理 AI 推理能力,需要针对性的物理世界感知-推理训练

### O2: 当前主流 VLM 在直觉物理推理任务(时间箭头、空间拼图、物体永恒性)上仍接近随
- **Statement**: 当前主流 VLM 在直觉物理推理任务(时间箭头、空间拼图、物体永恒性)上仍接近随机猜测水平
- **Evidence**: Table 10 中 Gemini 2.0 Flash 和 Qwen2.5-VL-7B 在时间箭头任务准确率约 50%,在物体永恒性任务约 48%,与随机猜测基线(50.0)相当
- **Implication**: 通用 VLM 的标准训练范式未能培养对物理世界底层规律(熵、因果、物体持续存在)的真实理解

### O3: 现有推理增强研究(如 OpenAI o1、DeepSeek-R1)主要聚焦于代码
- **Statement**: 现有推理增强研究(如 OpenAI o1、DeepSeek-R1)主要聚焦于代码/数学/STEM 领域,物理 AI 方向尚未系统探索
- **Evidence**: Section 8.3 指出:「existing studies primarily focus on reasoning tasks related to coding, mathematics, and STEM fields」
- **Implication**: 将长链式思维 RL 范式迁移至物理 AI 存在明确技术空白

## Gaps

### G1: 物理常识与具身推理缺乏统一能力框架及对应评测基准
- **Statement**: 物理常识与具身推理缺乏统一能力框架及对应评测基准
- **Caused by**: C1
- **Existing attempts**: []
- **Why they fail**: 物理 AI 推理的能力边界未被明确定义,无法系统衡量模型进展

### G2: 物理 AI 领域缺乏可规模化生成的高质量推理训练数据
- **Statement**: 物理 AI 领域缺乏可规模化生成的高质量推理训练数据
- **Caused by**: C1
- **Existing attempts**: []
- **Why they fail**: 物理常识和具身推理答案通常为自由格式,现有数据集无法直接用于 CoT 推理训练

### G3: 物理 AI RL 训练缺乏规则化可验证奖励机制
- **Statement**: 物理 AI RL 训练缺乏规则化可验证奖励机制
- **Caused by**: C2
- **Existing attempts**: []
- **Why they fail**: 不同于数学/代码问题的确定性答案,物理常识与具身推理问题通常为开放式回答,难以进行自动规则验证

## Key Insight
- **Insight**: 通过构建层级化本体论框架明确定义物理 AI 能力范围,结合 DeepSeek-R1 知识蒸馏生成 CoT 训练数据,并将物理推理问题转换为多选题形式以获得规则可验证奖励,从而将长链式推理 RL 范式系统引入物理 AI 领域
- **Derived from**: G1, G2, G3
- **Enables**: 两阶段(SFT + RL)系统化提升多模态 LLM 在物理常识推理、具身推理和直觉物理理解方面的能力

## Assumptions
- 多选题(MCQ)格式足以捕获物理常识和具身推理能力,可作为 RL 可验证奖励的代理目标
- 视频是物理世界感知输入的代表性形式,以视频为主要模态可有效训练物理 AI 推理
- 从 DeepSeek-R1 蒸馏的推理轨迹(以文字描述为上下文)有效代理了视频-问题对上的物理推理过程
- 物理常识理解与具身推理能力可分别通过独立本体论定义并分阶段提升(分析推断,论文未显式声明两者的相互解耦程度)
