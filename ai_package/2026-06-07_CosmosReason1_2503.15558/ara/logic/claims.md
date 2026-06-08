# Claims

## C1: Physical AI SFT显著提升骨干VLM的物理常识与具身推理能力
- **Statement**: 基于精心整理的约400万条物理常识VQA与具身推理SFT数据对骨干VLM进行有监督微调后,Cosmos-Reason1在具身推理基准上相较各自骨干模型均提升超过10个百分点,在物理常识基准上亦有显著提升。
- **Status**: supported
- **Falsification criteria**: 若Cosmos-Reason1-7B和56B在具身推理基准综合均分上均未超过各自骨干模型10个百分点以上,则该声明不成立。
- **Proof**: [E1, E2]
- **Evidence basis**: ['E1', 'E2']
- **Interpretation**: Cosmos-Reason1-7B在具身推理平均分上较骨干Qwen2.5-VL-7B提升+11.0(50.8→61.8),56B较骨干Nemotron-H-56B提升+10.2(53.5→63.7);物理常识基准7B提升+6.9(47.4→54.3),56B提升+2.0(58.2→60.2)。提升来源于两阶段数据整理:人工标注+DeepSeek-R1蒸馏的长思维链推理迹。
- **Tags**: ['improvement']

## C2: Physical AI RL在SFT基础上进一步提升模型的Physical AI推理能力
- **Statement**: 使用基于规则的可验证奖励(准确率奖励+格式奖励)进行强化学习后训练,可在SFT模型基础上进一步提升物理常识、具身推理与直觉物理任务的综合准确率。
- **Status**: supported
- **Falsification criteria**: 若RL后训练在物理常识和具身推理综合均分上未超过SFT模型,则该声明不成立。
- **Proof**: [E3, E4]
- **Evidence basis**: ['E3', 'E4']
- **Interpretation**: RL后训练使Cosmos-Reason1-7B综合均分从60.7提升至65.7(+5.0);直觉物理综合均分从74.5提升至81.5(+7.0)。RL通过将所有训练样本转换为多选题并使用字符串匹配验证,绕开了Physical AI答案评估中开放式响应难以自动验证的困难。
- **Tags**: ['improvement']

## C3: 现有主流VLM在时间箭头与物体恒常性任务上表现接近随机猜测水平
- **Statement**: 在时间箭头(二分类)和物体恒常性任务上,包括Gemini 2.0 Flash、GPT-4o在内的当前最优VLM准确率接近随机猜测基线,揭示了现有评测体系未能有效衡量模型对物理世界的理解能力。
- **Status**: supported
- **Falsification criteria**: 若现有VLM在时间箭头任务上准确率显著高于50%随机猜测基线,则该声明不成立。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: Gemini 2.0 Flash和Qwen2.5-VL-7B在时间箭头任务上分别为50.0和50.2,与随机猜测(50.0)无差异。空间拼图任务GPT-4o表现明显好于随机(77.0 vs 25.0基线),说明现有VLM对空间关系的理解优于对时间动态的推理。
- **Tags**: ['descriptive']

## C4: Cosmos-Reason1-7B在直觉物理基准上大幅超越现有VLM
- **Statement**: 经Physical AI SFT训练后,Cosmos-Reason1-7B在直觉物理综合基准(时间箭头、空间拼图、物体恒常性)上平均准确率相较骨干Qwen2.5-VL-7B提升超过30个百分点,验证了自监督直觉物理数据整理策略的有效性。
- **Status**: supported
- **Falsification criteria**: 若Cosmos-Reason1-7B在直觉物理综合均分上未显著超越骨干模型Qwen2.5-VL-7B,则该声明不成立。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: Cosmos-Reason1-7B直觉物理综合均分74.5相较Qwen2.5-VL-7B的42.1提升+32.4。RL进一步提升至81.5(+7.0)。其中时间箭头提升幅度(56.0→64.5)远小于空间拼图(85.4→94.0),说明时间动态推理仍是难点。
- **Tags**: ['improvement']

## C5: 全异步异构RL训练框架相比同机位框架训练效率提升约160%
- **Statement**: 通过分离策略训练节点与Actor Rollout节点的异构部署,并使用统一调度器实现端到端异步并行,所提出的RL训练框架相比主流同机位框架训练效率提升约160%,同时支持节点故障自动重配置和动态扩缩容。
- **Status**: stated
- **Falsification criteria**: 若实际测量中该框架相对同机位框架的训练吞吐提升不足约160%,则该声明不成立。
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: 论文仅定性陈述约160%的提升并描述架构设计动机,未提供正式消融实验数据作为量化支撑。该数字系论文作者的工程实测报告而非独立验证结果。
- **Tags**: ['improvement']

## C6: RL训练涌现出在歧义问题中拒绝所有选项的推理行为
- **Statement**: 经Physical AI RL训练后,模型在遇到歧义性多选问题时能主动评估每个选项的合理性,选择拒绝全部给定选项并给出问题之外的保守回答,而非强行从不充分选项中作答。
- **Status**: supported
- **Falsification criteria**: 若RL训练前后模型面对歧义问题的行为模式无显著差异,则该声明不成立。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 该行为在论文图9中通过定性案例展示,是RL训练带来的涌现能力而非SFT阶段已具备。RL模型对每个选项逐一分析可行性,当所有选项均不充分时采取保守行动。
- **Tags**: ['descriptive', 'improvement']
