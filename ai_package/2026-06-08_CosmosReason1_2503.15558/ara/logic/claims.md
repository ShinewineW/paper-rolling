# Claims

## C1: Physical AI SFT 显著提升物理常识与具身推理基准性能
- **Statement**: 经过专门的 Physical AI SFT 训练（约 400 万条视频-文本标注），Cosmos-Reason1-7B 和 Cosmos-Reason1-56B 在物理常识和具身推理基准上，相比各自骨干 VLM 均实现超过 10% 的平均准确率提升。
- **Status**: 已验证
- **Falsification criteria**: 若 SFT 后模型在物理常识或具身推理任一基准的平均准确率相比骨干 VLM 提升幅度低于 10%，则本 claim 被证伪。
- **Proof**: [E1, E2]
- **Evidence basis**: ['E1', 'E2']
- **Interpretation**: 专门构建的物理 AI SFT 数据集（涵盖物理常识 VQA、具身推理、直觉物理三类）对于弥合通用预训练 VLM 在物理世界理解方面的能力差距起决定性作用。56B 变体在物理常识基准上略超 OpenAI o1，7B 变体在具身推理基准上平均提升达 11.0 个百分点。
- **Tags**: ['improvement', 'causal']

## C2: Physical AI RL 在 SFT 基础上进一步提升推理性能
- **Statement**: 基于规则可验证奖励（准确率奖励 + 格式奖励）的 GRPO RL 后训练，能在 Physical AI SFT 模型基础上进一步提升物理常识和具身推理的整体平均准确率。
- **Status**: 已验证
- **Falsification criteria**: 若 RL 后训练后，Cosmos-Reason1-7B 在综合基准上的平均准确率相比 SFT 版本未见提升，则本 claim 被证伪。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: RL 所用奖励均为规则可验证型（MCQ 字符串匹配准确率 + 推理格式正则匹配），无需额外奖励模型。RL 在大多数基准子任务上带来进一步提升，但在 RoboFail 这一高难度具身推理基准上提升有限，论文将其归因于训练数据中缺乏足够的代表性样本。
- **Tags**: ['improvement', 'causal']

## C3: 直觉物理专项 SFT 使 Cosmos-Reason1-7B 在三项直觉物理任务上大幅超越基线
- **Statement**: 经过专门的直觉物理 SFT（空间拼图 11K、时间箭头 30K、物体永恒 10K 样本），Cosmos-Reason1-7B 在三项直觉物理任务上均显著优于同规模骨干 VLM，整体平均提升幅度远超随机猜测水平。
- **Status**: 已验证
- **Falsification criteria**: 若 Cosmos-Reason1-7B 在时间箭头、空间拼图、物体永恒三项任务的平均准确率与 Qwen2.5-VL-7B 基线相近或更低，则本 claim 被证伪。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 直觉物理任务具有自监督特性（视频逆播、图像拼图重排、仿真环境物体消失检测），数据构建成本远低于人工标注的物理常识或具身推理任务，具备规模化潜力。
- **Tags**: ['improvement', 'causal']

## C4: 当前主流 VLM 在基础直觉物理任务上接近随机猜测水平
- **Statement**: 在时间箭头和物体永恒任务上，包括 Gemini 2.0 Flash、Qwen2.5-VL-7B 在内的当前主流 VLM 表现不高于随机猜测基线，表明标准多模态基准无法充分反映模型对物理世界的真实理解。
- **Status**: 已验证
- **Falsification criteria**: 若主流 VLM 在时间箭头或物体永恒任务上显著超过随机猜测基线（时间箭头随机基线为 50%，物体永恒随机基线为 50%），则本 claim 被证伪。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 该发现揭示了通用多模态基准（如 MMMU）与直觉物理理解能力评估之间存在明显差距，即便在通用基准上达到优秀表现的模型，在基础物理世界感知任务上仍可能表现接近随机。
- **Tags**: ['descriptive']

## C5: 全异步 RL 训练框架相比共址框架训练效率提升约 160%
- **Statement**: 论文所提出的全异步异构 RL 训练框架（策略训练节点与 actor rollout 节点分离部署，通过统一调度器实现端到端异步）相比主流共址框架的训练效率提升约 160%。
- **Status**: 已验证（论文作者报告，无独立消融对比表）
- **Falsification criteria**: 若在相同任务和硬件条件下，异步框架与共址框架的训练吞吐量无显著差异，则本 claim 被证伪。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 提升来源于消除了策略训练与 actor rollout 之间的同步等待，实现全流水线端到端异步；框架还支持节点失效时快速自重构和动态规模伸缩，无需代价高昂的重启操作。
- **Tags**: ['improvement', 'causal']

## C6: Cosmos-Reason1-56B 在物理常识基准上略优于 OpenAI o1
- **Statement**: Physical AI SFT 后，Cosmos-Reason1-56B 在物理常识基准平均准确率上略超 OpenAI o1，是所有参与对比的模型中最高的。
- **Status**: 已验证
- **Falsification criteria**: 若 Cosmos-Reason1-56B 物理常识基准平均准确率不高于 OpenAI o1，则本 claim 被证伪。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: Cosmos-Reason1-56B 采用混合 Mamba-MLP-Transformer 架构（以 Nemotron-H 为 LLM 骨干），该结果体现了专门构建的物理 AI SFT 数据集对大规模模型物理常识理解的显著增益。
- **Tags**: ['improvement', 'descriptive']
