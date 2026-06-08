# Experiments

## E1: Physical AI SFT在物理常识基准上的评估
- **Verifies**: C1
- **Setup**:
  - Model: Cosmos-Reason1-7B(基于Qwen2.5-VL预训练)、Cosmos-Reason1-56B(基于Nemotron-H+InternViT-300M-V2.5);对比:Gemini 2.0 Flash、GPT-4o、OpenAI o1、Qwen2.5-VL-7B、Nemotron-H-56B
  - Hardware: Cosmos-Reason1-7B训练:TP=4;Cosmos-Reason1-56B训练:TP=8、PP=2
  - Dataset: 物理常识基准:604道问题(336道二选一+268道多选),来自426段视频,覆盖Space/Time/Fundamental Physics三大类16个子类
  - System: 对自研模型取5次推理均值(temperature=0.6,top-p=0.95);对比模型使用零样本思维链提示(API调用或开源权重)
- **Procedure**:
  1. 以约1.81M条理解标注+1.93M条推理标注对骨干VLM进行Physical AI SFT
  2. 在604道物理常识问题上评测各模型
  3. 分别统计Space、Time、Other Physics三个维度准确率及综合均分
  4. 与各骨干模型及同等规模闭源模型比较
- **Metrics**: ['准确率(Space、Time、Other Physics、Avg.)']
- **Expected outcome**: Cosmos-Reason1模型在各维度准确率均高于其对应骨干VLM
- **Baselines**: ['Gemini 2.0 Flash', 'GPT-4o', 'OpenAI o1', 'Qwen2.5-VL-7B', 'Nemotron-H-56B']
- **Dependencies**: []

## E2: Physical AI SFT在具身推理基准上的评估
- **Verifies**: C1
- **Setup**:
  - Model: Cosmos-Reason1-7B、Cosmos-Reason1-56B;对比模型同E1
  - Hardware: 同E1
  - Dataset: 具身推理基准:6个子集共610道多选题,来自600段视频,覆盖BridgeData V2(100)、RoboVQA(110)、RoboFail(100)、Agibot(100)、HoloAssist(100)、AV(100)
  - System: 统一多选题模板,零样本思维链提示;评测样本与训练集无重叠
- **Procedure**:
  1. 以Physical AI SFT数据微调骨干VLM
  2. 在6个具身推理子基准上分别评测
  3. 统计各子集准确率及综合均分
  4. 与骨干模型及对比模型比较,重点关注与骨干模型的提升幅度
- **Metrics**: ['准确率(BridgeData V2、RoboVQA、Agibot、HoloAssist、AV、RoboFail、Avg.)']
- **Expected outcome**: Cosmos-Reason1模型具身推理综合均分高于各自骨干VLM超过10个百分点
- **Baselines**: ['Gemini 2.0 Flash', 'GPT-4o', 'OpenAI o1', 'Qwen2.5-VL-7B', 'Nemotron-H-56B']
- **Dependencies**: []

## E3: Physical AI RL后训练在物理常识与具身推理综合基准上的评估
- **Verifies**: C2, C6
- **Setup**:
  - Model: Cosmos-Reason1-7B(SFT后)进行RL后训练
  - Hardware: 论文未单独说明
  - Dataset: RL训练集共30,304道多选题:物理常识MCQ(5,133道)、具身推理各来源(各约200-252道)、直觉物理(合计24,079道);评测集同E1和E2
  - System: GRPO算法;全局batch size=128个问题,每题采样9个输出,最大token长度6144;学习率4×10^-6;KL惩罚系数0.005;训练500轮;在线随机打乱多选题选项
- **Procedure**:
  1. 将所有SFT数据来源的推理样本转换为多选题格式
  2. 使用准确率奖励(字符串匹配)和格式奖励对SFT模型进行RL后训练
  3. 在物理常识基准和6个具身推理子基准上评测
  4. 与SFT阶段Cosmos-Reason1-7B结果对比
  5. 定性分析RL训练前后模型面对歧义问题时的推理行为变化
- **Metrics**: ['综合均分(Common Sense + 具身推理6个子集 Avg.)']
- **Expected outcome**: RL后训练综合均分高于SFT阶段模型
- **Baselines**: ['Cosmos-Reason1-7B (SFT)']
- **Dependencies**: ['E1', 'E2']

## E4: 直觉物理基准评测:时间箭头、空间拼图与物体恒常性
- **Verifies**: C3, C4
- **Setup**:
  - Model: Cosmos-Reason1-7B(SFT)、Cosmos-Reason1-7B(+Physical AI RL);对比:Random Guess、Gemini 2.0 Flash、GPT-4o、OpenAI o1、Qwen2.5-VL-7B
  - Hardware: 论文未单独说明
  - Dataset: 直觉物理基准:时间箭头100道(二分类)、空间拼图100道(四选一)、物体恒常性100道(二分类);经数据去污染确认与训练数据无重叠
  - System: 零样本评测
- **Procedure**:
  1. 对各模型在三项直觉物理任务上进行零样本评测
  2. 记录各任务单独准确率及三任务综合均分
  3. 与随机猜测基线及现有VLM对比
  4. 比较SFT模型和+RL模型的提升幅度
- **Metrics**: ['准确率(Arrow of Time、Spatial Puzzle、Object Permanence、Avg.)']
- **Expected outcome**: 现有VLM在时间箭头和物体恒常性上接近随机猜测水平;Cosmos-Reason1-7B显著高于骨干Qwen2.5-VL-7B;RL进一步提升性能
- **Baselines**: ['Random Guess', 'Gemini 2.0 Flash', 'GPT-4o', 'OpenAI o1', 'Qwen2.5-VL-7B']
- **Dependencies**: []

## E5: 全异步RL训练框架相对同机位框架的训练效率比较
- **Verifies**: C5
- **Setup**:
  - Model: Cosmos-Reason1系列模型
  - Hardware: 异构节点:策略训练节点与Actor Rollout节点分离部署;策略训练节点支持5D并行(DP、PP、CP、FSDP、TP),Rollout节点支持DP、PP、TP
  - Dataset: Physical AI RL训练阶段数据
  - System: 自研全异步框架(统一调度器+异构部署) vs 主流同机位RL框架(如OpenRLHF、HybridFlow)
- **Procedure**:
  1. 通过分离策略训练与Actor Rollout节点消除同步开销
  2. 利用统一调度器实现端到端异步并行
  3. 测量相比主流同机位框架的训练吞吐提升比例
  4. 验证节点故障自动重配置功能和动态扩缩容能力
- **Metrics**: ['训练效率提升比例(相对于同机位框架)']
- **Expected outcome**: 异步框架训练效率高于同机位框架约160%
- **Baselines**: ['主流同机位RL框架(colocated frameworks)']
- **Dependencies**: []
