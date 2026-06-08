# Experiments

## E1: Physical AI SFT模型在物理常识基准上的评估
- **Verifies**: C1, C5
- **Setup**:
  - Model: Cosmos-Reason1-7B（基于Qwen2.5-VL骨干）、Cosmos-Reason1-56B（基于Nemotron-H骨干）；基线：Gemini 2.0 Flash、GPT-4o、OpenAI o1、Qwen2.5-VL-7B、Nemotron-H-56B
  - Hardware: 论文未详细说明评估阶段硬件；训练阶段7B用TP=4，56B用TP=8、PP=2
  - Dataset: 物理常识基准：手动策划604道题，来自426段视频，涵盖Space（80题，13.25%）、Time（298题，49.33%）、Fundamental Physics（226题，37.4%）三类
  - System: Cosmos-Reason1经Physical AI SFT后推理；商业模型通过API零样本CoT提示，开源模型加载权重推理
- **Procedure**:
  1. 按物理常识本体定义从互联网视频手动策划604道题（包含二选一及多选题）
  2. 对Cosmos-Reason1取温度0.6、top-p 0.95下5次推理的平均准确率
  3. 对Gemini 2.0 Flash、GPT-4o、OpenAI o1调用API并使用零样本CoT提示（Kojima et al., 2022）
  4. 对Qwen2.5-VL-7B加载开源权重后推理
  5. 按Space、Time、Other Physics维度及整体平均准确率汇报结果
- **Metrics**: ['Space准确率', 'Time准确率', 'Other Physics准确率', '平均准确率（Avg.）']
- **Expected outcome**: SFT后的Cosmos-Reason1在各维度准确率高于对应骨干模型，56B变体接近或超过OpenAI o1
- **Baselines**: ['Gemini 2.0 Flash', 'GPT-4o', 'OpenAI o1', 'Qwen2.5-VL-7B', 'Nemotron-H-56B']
- **Dependencies**: ['物理常识SFT数据策划流程（Sec. 5.1.1）；约1.81M条理解样本+约1.93M条推理样本（Tab. 4）']

## E2: Physical AI SFT模型在具身推理基准上的评估
- **Verifies**: C1
- **Setup**:
  - Model: Cosmos-Reason1-7B、Cosmos-Reason1-56B；基线：Gemini 2.0 Flash、GPT-4o、OpenAI o1、Qwen2.5-VL-7B、Nemotron-H-56B
  - Hardware: 论文未详细说明评估阶段硬件
  - Dataset: 具身推理基准：六个子集共610道MCQ题，来自600段视频（BridgeData V2 100题、RoboVQA 110题、RoboFail 100题、Agibot 100题、HoloAssist 100题、AV 100题）
  - System: Cosmos-Reason1经Physical AI SFT后推理；基线模型零样本CoT推理
- **Procedure**:
  1. 按任务完成验证、动作可行性、下一合理动作预测三类属性构建MCQ格式基准
  2. 采用统一问题模板与动作粒度层级（actions/subtasks/goals），手动精炼选项避免歧义
  3. 对Cosmos-Reason1取5次推理平均准确率，对基线模型零样本CoT推理
  4. 按BridgeData V2、RoboVQA、Agibot、HoloAssist、AV、RoboFail及平均准确率报告结果
- **Metrics**: ['BridgeData V2准确率', 'RoboVQA准确率', 'Agibot准确率', 'HoloAssist准确率', 'AV准确率', 'RoboFail准确率', '平均准确率（Avg.）']
- **Expected outcome**: Cosmos-Reason1在具身推理基准平均准确率比骨干模型提升超过10个百分点
- **Baselines**: ['Gemini 2.0 Flash', 'GPT-4o', 'OpenAI o1', 'Qwen2.5-VL-7B', 'Nemotron-H-56B']
- **Dependencies**: ['具身推理SFT数据策划流程（Sec. 5.1.2）；涵盖BridgeData V2、RoboVQA、AgiBot、HoloAssist、AV数据集']

## E3: 直觉物理SFT及RL模型在直觉物理基准上的评估
- **Verifies**: C4, C6
- **Setup**:
  - Model: Cosmos-Reason1-7B（SFT版及SFT+RL版）；基线：随机猜测、Gemini 2.0 Flash、GPT-4o、OpenAI o1、Qwen2.5-VL-7B
  - Hardware: 论文未详细说明评估阶段硬件
  - Dataset: 直觉物理基准：时间箭头100题（二分类）、空间谜题100题（四选一）、物体恒常性100题（二分类），共300题；进行数据去污染确保与训练集无重叠
  - System: 经Sec. 5.1.3专项直觉物理SFT数据训练的Cosmos-Reason1-7B；RL版本在其基础上进一步RL后训练
- **Procedure**:
  1. 从对应数据源提取100段视频构建各任务评估集，进行数据去污染
  2. 时间箭头任务：判断视频正放还是反放（二分类）
  3. 空间谜题任务：提供32帧（8张图各分成2×2拼块打乱），识别指定位置的正确拼块（四选一）
  4. 物体恒常性任务：判断是否有物体违反物体恒常性（二分类）
  5. 汇报各任务准确率及平均准确率，与基线对比
- **Metrics**: ['时间箭头准确率（Arrow of Time）', '空间谜题准确率（Spatial Puzzle）', '物体恒常性准确率（Object Permanence）', '平均准确率（Avg.）']
- **Expected outcome**: Cosmos-Reason1-7B在三项任务上均显著高于基线模型，RL版本进一步提升空间谜题和物体恒常性；时间箭头任务提升相对有限
- **Baselines**: ['随机猜测', 'Gemini 2.0 Flash', 'GPT-4o', 'OpenAI o1', 'Qwen2.5-VL-7B']
- **Dependencies**: ['直觉物理SFT数据集（Sec. 5.1.3）：空间谜题11k、时间箭头30k、物体恒常性10k']

## E4: Physical AI RL后训练的综合评估
- **Verifies**: C2, C3
- **Setup**:
  - Model: Cosmos-Reason1-7B（在Physical AI SFT检查点基础上进行RL后训练）
  - Hardware: 策略训练节点支持5D并行（DP、PP、CP、FSDP、TP），Actor展开节点支持DP、PP、TP；使用定制化NCCL通信器的全异步分布式RL框架
  - Dataset: RL后训练数据集：共30,304条MCQ样本（物理常识5,133条、BridgeData V2 240条、RoboVQA 252条、Agibot 200条、HoloAssist 200条、AV 200条、空间谜题3,998条、时间箭头9,994条、物体恒常性10,087条）
  - System: GRPO算法；准确率奖励（字符串匹配answer标签内容）+ 格式奖励（正则匹配think/answer标签）
- **Procedure**:
  1. 将所有训练样本转换为单一正确答案的MCQ格式，对不可直接MCQ化的样本进行人工质量验证
  2. 动态随机化MCQ选项顺序以促进泛化，防止奖励黑客攻击
  3. 全局批量大小128题，每题采样9个输出，最大长度6144 token
  4. 训练500次迭代，学习率4×10⁻⁶，KL惩罚系数0.005
  5. 在物理常识和具身推理综合基准（Tab. 9）及直觉物理基准（Tab. 10）上对比SFT阶段
- **Metrics**: ['物理常识平均准确率', '具身推理各子集及平均准确率', '直觉物理各子任务及平均准确率', '综合整体平均准确率']
- **Expected outcome**: RL后训练在物理常识、具身推理大多数子集及直觉物理任务上进一步高于SFT基线
- **Baselines**: ['Cosmos-Reason1-7B（Physical AI SFT阶段）']
- **Dependencies**: ['E1', 'E2', 'E3', 'Physical AI RL数据集（Sec. 5.2，Tab. 5）', 'GRPO算法（Shao et al., 2024）']
