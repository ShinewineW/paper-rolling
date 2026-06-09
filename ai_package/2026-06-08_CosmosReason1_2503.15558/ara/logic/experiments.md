# Experiments

## E1: Physical AI SFT 在物理常识基准上的评估
- **Verifies**: C1, C6
- **Setup**:
  - Model: Cosmos-Reason1-7B（以 Qwen2.5-VL 为预训练起点）和 Cosmos-Reason1-56B（以 InternViT-300M-V2.5 + Nemotron-H 混合骨干为起点）；对比基线：Gemini 2.0 Flash、GPT-4o、OpenAI o1、Qwen2.5-VL-7B、Nemotron-H-56B
  - Hardware: 论文未明确指定评估阶段所用硬件
  - Dataset: 自建物理常识基准：共 604 题，来自 426 段视频，涵盖 Space（80 题，13.25%）、Time（298 题，49.33%）、Fundamental Physics（226 题，37.4%）三类，包含 336 道二选一题和 268 道多选题
  - System: Cosmos-Reason1 系列报告 5 次推理（temperature 0.6，top-p 0.95，不同随机种子）的平均准确率；外部基线使用零样本链式思维（Zero-shot CoT）提示，闭源模型通过 API 调用，Qwen2.5-VL 使用开源权重
- **Procedure**:
  1. 以自建物理常识基准中的视频和问题作为输入
  2. 对 Cosmos-Reason1 系列使用 5 个不同随机种子分别推理并取平均准确率
  3. 对 GPT-4o、OpenAI o1、Gemini 2.0 Flash 调用 API 进行零样本 CoT 评测
  4. 对 Qwen2.5-VL-7B 和 Nemotron-H-56B 使用开源权重进行零样本 CoT 评测
  5. 按 Space、Time、Fundamental Physics 三个子类分别统计准确率，并计算平均
- **Metrics**: ['Space 准确率（%）', 'Time 准确率（%）', 'Other Physics 准确率（%）', '平均准确率（%）']
- **Expected outcome**: Physical AI SFT 后的 Cosmos-Reason1 系列应显著优于各自的骨干 VLM，56B 变体应达到或超过顶尖闭源推理模型水平
- **Baselines**: ['Gemini 2.0 Flash', 'GPT-4o', 'OpenAI o1', 'Qwen2.5-VL-7B', 'Nemotron-H-56B']
- **Dependencies**: ['Physical AI SFT 训练完成', '物理常识基准构建完成']

## E2: Physical AI SFT 在具身推理基准上的评估
- **Verifies**: C1
- **Setup**:
  - Model: Cosmos-Reason1-7B 和 Cosmos-Reason1-56B；对比基线同 E1
  - Hardware: 论文未明确指定评估阶段所用硬件
  - Dataset: 自建具身推理基准：共 610 题，来自 600 段视频，覆盖 BridgeData V2（100 题）、RoboVQA（110 题）、RoboFail（100 题）、AgiBot（100 题）、HoloAssist（100 题）、AV（100 题）六个子集；测试集与训练集无重叠
  - System: 多选题（MCQ）格式评测；零样本 CoT 提示；Cosmos-Reason1 系列报告 5 次推理平均准确率
- **Procedure**:
  1. 以自建具身推理基准中的视频和多选题问题作为输入
  2. 对 Cosmos-Reason1 系列使用 5 个不同随机种子推理并取平均
  3. 对其他基线模型使用零样本 CoT 评测
  4. 按六个子数据集分别统计准确率，并计算综合平均
- **Metrics**: ['BridgeData V2 准确率（%）', 'RoboVQA 准确率（%）', 'AgiBot 准确率（%）', 'HoloAssist 准确率（%）', 'AV 准确率（%）', 'RoboFail 准确率（%）', '平均准确率（%）']
- **Expected outcome**: Physical AI SFT 后的 Cosmos-Reason1 系列应在具身推理各子任务上均显著优于各自骨干 VLM
- **Baselines**: ['Gemini 2.0 Flash', 'GPT-4o', 'OpenAI o1', 'Qwen2.5-VL-7B', 'Nemotron-H-56B']
- **Dependencies**: ['Physical AI SFT 训练完成', '具身推理基准构建完成（含人工精炼 MCQ 选项）']

## E3: 直觉物理 SFT 在三项直觉物理任务上与基线对比评估
- **Verifies**: C3, C4
- **Setup**:
  - Model: Cosmos-Reason1-7B（含 Physical AI SFT，其中包括直觉物理专项训练）；对比基线：Random Guess、Gemini 2.0 Flash、GPT-4o、OpenAI o1、Qwen2.5-VL-7B
  - Hardware: 论文未明确指定评估阶段所用硬件
  - Dataset: 自建直觉物理基准：时间箭头（Arrow of Time）100 题、空间拼图（Spatial Puzzle）100 题、物体永恒（Object Permanence）100 题；执行数据去污以确保与训练集无重叠
  - System: 零样本 CoT 提示；Cosmos-Reason1-7B 报告 5 次推理平均准确率；随机猜测基线按答案选项数推算
- **Procedure**:
  1. 以自建直觉物理基准作为评测输入
  2. 对所有模型进行零样本 CoT 评测
  3. 分别记录时间箭头、空间拼图、物体永恒三项子任务的准确率
  4. 与随机猜测基线对比，验证各模型是否具备超越随机猜测的物理世界感知能力
- **Metrics**: ['Arrow of Time 准确率（%）', 'Spatial Puzzle 准确率（%）', 'Object Permanence 准确率（%）', '平均准确率（%）']
- **Expected outcome**: 不含直觉物理专项训练的主流 VLM 应接近随机猜测水平；Cosmos-Reason1-7B 经专项 SFT 后应在三项任务上均显著优于基线
- **Baselines**: ['Random Guess', 'Gemini 2.0 Flash', 'GPT-4o', 'OpenAI o1', 'Qwen2.5-VL-7B']
- **Dependencies**: ['直觉物理 SFT 数据集构建完成（空间拼图 11K、时间箭头 30K、物体永恒 10K）', '数据去污处理完成']

## E4: Physical AI RL 后训练在物理常识与具身推理基准上的评估
- **Verifies**: C2, C5
- **Setup**:
  - Model: Cosmos-Reason1-7B（在 Physical AI SFT 权重基础上进行 RL 后训练）
  - Hardware: 全异步异构 RL 训练框架：策略训练节点（5D 并行：DP+PP+CP+FSDP+TP）与 actor rollout 节点（DP+PP+TP）异构部署，Cosmos-Reason1-7B 训练使用 TP=4
  - Dataset: RL 数据集（共 30,304 条 MCQ 样本）：物理常识 5,133 条、BridgeData V2 240 条、RoboVQA 252 条、AgiBot 200 条、HoloAssist 200 条、AV 200 条、空间拼图 3,998 条、时间箭头 9,994 条、物体永恒 10,087 条
  - System: GRPO 算法；全局 batch size 128 题，每题采样 9 个输出，最大长度 6144 tokens；学习率 4×10⁻⁶，KL 惩罚系数 0.005，训练 500 步；RL 训练期间动态打乱 MCQ 选项顺序
- **Procedure**:
  1. 加载 Physical AI SFT 后的 Cosmos-Reason1-7B 权重
  2. 在 RL 数据集上按 GRPO 进行后训练，各数据来源以等概率采样
  3. RL 训练完成后，在 SFT 评测所用同款物理常识和具身推理基准上进行评测
  4. 对比 SFT 版本与 SFT+RL 版本在各子任务和整体平均准确率上的差异
- **Metrics**: ['物理常识平均准确率（%）', 'BridgeData V2 准确率（%）', 'RoboVQA 准确率（%）', 'AgiBot 准确率（%）', 'HoloAssist 准确率（%）', 'AV 准确率（%）', 'RoboFail 准确率（%）', '综合平均准确率（%）']
- **Expected outcome**: Physical AI RL 后训练应在大多数基准子任务上进一步提升 SFT 模型的准确率，综合平均准确率相比 SFT 基线有所提升
- **Baselines**: ['Cosmos-Reason1-7B（仅 Physical AI SFT，不含 RL）']
- **Dependencies**: ['Physical AI SFT 完成', 'RL 数据集构建完成', '全异步 RL 训练框架就绪']

## E5: Physical AI RL 后训练在直觉物理基准上的评估
- **Verifies**: C2, C3
- **Setup**:
  - Model: Cosmos-Reason1-7B SFT 版本 与 Cosmos-Reason1-7B SFT+RL 版本
  - Hardware: 论文未明确指定评估阶段所用硬件
  - Dataset: 自建直觉物理基准（同 E3）；RL 训练使用 24,079 条高质量样本（含空间连续性、时间箭头、物体永恒），严格确保与 SFT 训练所用片段无重叠
  - System: 同 E4 的 GRPO RL 设置；直觉物理 RL 数据集天然为 MCQ 格式（自监督构建），无需人工标注，易于规模化
- **Procedure**:
  1. 在直觉物理基准上分别评测 SFT 版和 SFT+RL 版 Cosmos-Reason1-7B
  2. 按时间箭头、空间拼图、物体永恒三项子任务分别记录准确率
  3. 与 E3 中的 SFT 结果对比，量化 RL 额外带来的提升
- **Metrics**: ['Arrow of Time 准确率（%）', 'Spatial Puzzle 准确率（%）', 'Object Permanence 准确率（%）', '平均准确率（%）']
- **Expected outcome**: RL 后训练应进一步提升空间拼图和物体永恒任务的准确率；时间箭头任务仍相对困难，提升幅度相对较小
- **Baselines**: ['Cosmos-Reason1-7B（仅 Physical AI SFT，不含 RL）']
- **Dependencies**: ['直觉物理 SFT 完成', '直觉物理 RL 数据集构建完成（与 SFT 片段无重叠）']
