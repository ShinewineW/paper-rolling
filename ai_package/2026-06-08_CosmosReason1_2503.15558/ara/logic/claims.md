# Claims

## C1: Physical AI SFT显著提升物理常识与具身推理能力
- **Statement**: 针对物理AI能力的专项监督微调（SFT）使7B模型在物理常识基准平均准确率相对骨干模型提升6.9分、在具身推理基准提升11.0个百分点，使56B模型在物理常识基准提升2.0分、在具身推理基准提升10.2个百分点。
- **Status**: supported
- **Falsification criteria**: 若SFT后的Cosmos-Reason1模型在物理常识或具身推理基准的平均准确率未高于对应骨干模型，则主张不成立。
- **Proof**: [E1, E2]
- **Evidence basis**: ['E1', 'E2']
- **Interpretation**: 通过精心策划的约400万条视频-文本对标注（含长链式推理轨迹）进行的专项SFT是提升的直接原因。SFT对部分困难子集（如RoboFail）效果有限，论文认为主要原因是缺乏足够代表性的训练数据。
- **Tags**: ['improvement']

## C2: Physical AI RL进一步在大多数基准上提升推理性能
- **Statement**: 在Physical AI SFT基础上，利用规则化可验证奖励进行强化学习后训练，Cosmos-Reason1-7B整体综合平均准确率进一步提升5.0分（从60.7提升至65.7），直觉物理平均准确率进一步提升7.0分。
- **Status**: supported
- **Falsification criteria**: 若RL后训练后模型在物理常识和具身推理综合基准平均分未超过SFT模型，则主张不成立。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 基于MCQ格式准确率奖励与格式奖励的简单规则化信号即可驱动跨域推理能力提升。RL还使模型出现「在选项含糊时拒绝所有选项」的保守决策行为，属SFT阶段未出现的涌现能力（分析推断，论文未显式声明为学习目标）。对RoboFail等困难子集的改善有限。
- **Tags**: ['improvement']

## C3: 全异步RL训练框架相比同位框架训练效率提升约160%
- **Statement**: 所提出的全异步RL训练框架通过分离策略训练节点与Actor展开节点并使用统一调度器，与主流同位框架相比实现约160%的训练效率提升，同时支持节点故障热恢复与动态弹性扩缩容。
- **Status**: supported
- **Falsification criteria**: 若该框架与主流同位框架（如OpenRLHF、HybridFlow）相比未呈现显著效率优势，则主张不成立。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 效率提升的核心机制是异步并行消除了策略训练与Rollout之间的同步等待开销。节点故障热恢复和弹性扩缩容是额外的工程贡献。该效率数字由论文直接陈述于Sec. 4.2，未单独列表实验。
- **Tags**: ['improvement', 'causal']

## C4: 现有VLM在直觉物理基础任务（时间箭头、物体恒常性）上接近随机水平
- **Statement**: 在时间箭头二分类任务上，Gemini 2.0 Flash和GPT-4o的准确率均约为50%，与随机猜测相同；在物体恒常性任务上大多数模型（包括Gemini 2.0 Flash、Qwen2.5-VL-7B）也接近随机猜测水平。
- **Status**: supported
- **Falsification criteria**: 若主流VLM在时间箭头或物体恒常性任务上准确率显著超过随机水平（时间箭头>50%、物体恒常性>50%），则主张不成立。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 现有标准基准未能充分评估模型对物理世界的基础理解能力。GPT-4o在空间谜题上远好于随机（77.0 vs 25.0随机），表明模型对空间关系的理解优于时序动态理解。这一对比揭示了VLM能力的不对称性。
- **Tags**: ['descriptive', 'scoping']

## C5: Cosmos-Reason1-56B在物理常识基准上略超OpenAI o1
- **Statement**: Cosmos-Reason1-56B在物理常识基准平均准确率为60.2，略高于OpenAI o1的59.9，是所有参与对比模型中最高的。
- **Status**: supported
- **Falsification criteria**: 若Cosmos-Reason1-56B物理常识基准平均分不高于OpenAI o1的59.9，则主张不成立。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 专项Physical AI SFT训练使Cosmos-Reason1-56B在物理常识方面超越了通用推理模型OpenAI o1，验证了领域专项数据策划与训练方法的有效性。
- **Tags**: ['improvement', 'descriptive']

## C6: 专项直觉物理SFT使Cosmos-Reason1习得直觉物理推理能力，RL进一步增强
- **Statement**: 经过专项直觉物理SFT后，Cosmos-Reason1-7B在直觉物理平均准确率提升至74.5（+32.4），RL后进一步提升至81.5（再+7.0），而骨干模型Qwen2.5-VL-7B在同一基准仅为42.1（接近随机水平41.7）。
- **Status**: supported
- **Falsification criteria**: 若直觉物理专项SFT后的Cosmos-Reason1-7B在三项直觉物理任务上无显著超越骨干模型的提升，则主张不成立。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 空间谜题、时间箭头、物体恒常性三类任务具有自监督特性，数据可规模化生成，是低成本提升直觉物理能力的有效途径。时间箭头任务在SFT和RL后仍有较大提升空间（SFT后56.0，RL后64.5），表明时序动态理解仍是挑战。
- **Tags**: ['improvement']
