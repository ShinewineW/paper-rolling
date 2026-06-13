# Experiments

## E1: Bench2Drive base set主闭环与开环对比
- **Verifies**: C1
- **Setup**:
  - Model: ORION
  - Hardware: 论文所述多卡NVIDIA A800训练环境
  - Dataset: Bench2Drive base set与官方闭环评测集
  - System: CARLA V2闭环仿真协议
- **Procedure**:
  1. 使用官方Bench2Drive训练与评测协议训练ORION。
  2. 在相同base set条件下与TCP、ThinkTwice、DriveAdapter、UniAD、VAD、GenAD、MomAD和DriveTransformer-Large等方法比较。
  3. 同时报告闭环Driving Score、Success Rate、Efficiency、Comfortness与开环Avg. L2。
- **Metrics**: ['DS', 'SR(%)', 'Efficiency', 'Comfortness', 'Avg. L2']
- **Expected outcome**: ORION应在主要闭环指标上高于强基线，开环误差保持可比。
- **Baselines**: ['TCP', 'TCP-ctrl', 'TCP-traj', 'ThinkTwice', 'DriveAdapter', 'AD-MLP', 'UniAD-Tiny', 'UniAD-Base', 'VAD', 'GenAD', 'MomAD', 'DriveTransformer-Large']
- **Dependencies**: ['Bench2Drive', 'CARLA V2', 'EVA-02-L', 'Vicuna v1.5', 'LoRA']

## E2: Bench2Drive Multi-Ability能力分解
- **Verifies**: C2
- **Setup**:
  - Model: ORION
  - Hardware: 论文所述训练环境
  - Dataset: Bench2Drive base set
  - System: Bench2Drive Multi-Ability评测
- **Procedure**:
  1. 在Bench2Drive多能力协议下分别统计合流、超车、紧急制动、让行和交通标志相关能力。
  2. 与同表E2E-AD方法逐项比较。
  3. 观察ORION强项与短板对应的交互场景类别。
- **Metrics**: ['Merging', 'Overtaking', 'Emergency Brake', 'Give Way', 'Traff c Sign', 'Mean']
- **Expected outcome**: ORION应在能力均值与若干交互能力上优于主要基线，同时保留论文报告的变道相关短板。
- **Baselines**: ['TCP', 'TCP-ctrl', 'TCP-traj', 'ThinkTwice', 'DriveAdapter', 'AD-MLP', 'UniAD-Tiny', 'UniAD-Base', 'VAD', 'DriveTransformer-Large']
- **Dependencies**: ['Bench2Drive Multi-Ability', 'ORION闭环评测输出']

## E3: 不同生成式规划器消融
- **Verifies**: C3
- **Setup**:
  - Model: ORION with Diffusion或VAE planner
  - Hardware: 论文所述训练环境
  - Dataset: Bench2Drive
  - System: 相同ORION框架下仅替换生成式规划器
- **Procedure**:
  1. 保持传感器输入、VLM与QT-Former等设置一致。
  2. 将VAE生成规划器替换为Diffusion生成规划器进行训练和评测。
  3. 比较闭环、开环和能力均值指标。
- **Metrics**: ['DS', 'SR(%)', 'Avg. L2', 'Avg. col', 'Ability Avg.']
- **Expected outcome**: VAE式规划器应整体优于Diffusion式规划器。
- **Baselines**: ['Diffusion']
- **Dependencies**: ['VAE', 'Diffusion', 'K-means trajectory anchors', 'GRU decoder']

## E4: QT-Former模块与输出类型消融
- **Verifies**: C4
- **Setup**:
  - Model: ORION及Plain Text变体
  - Hardware: 论文所述训练环境
  - Dataset: Bench2Drive
  - System: QT-Former不同设计组合与不同输出类型
- **Procedure**:
  1. 构造包含或不包含交通状态监督、运动预测、Memory Bank的QT-Former变体。
  2. 分别评估Instructed Generator与Plain Text输出类型。
  3. 比较各ID变体的闭环Driving Score与Success Rate。
- **Metrics**: ['DS', 'SR(%)']
- **Expected outcome**: 加入QT-Former关键设计后闭环表现应提升，Instructed Generator应明显优于Plain Text。
- **Baselines**: ['无交通状态监督变体', '无Memory Bank变体', 'Plain Text输出变体']
- **Dependencies**: ['QT-Former', 'Traffic State supervision', 'Motion Pred.', 'Memory Bank', 'Instructed Generator']

## E5: 历史查询数量消融
- **Verifies**: C5
- **Setup**:
  - Model: ORION历史查询变体
  - Hardware: 论文所述训练环境
  - Dataset: Bench2Drive
  - System: 仅使用规划轨迹与历史QA对以加速训练的消融设置
- **Procedure**:
  1. 改变历史查询数量并保持其余训练配置一致。
  2. 分别评估闭环与开环指标。
  3. 比较随历史查询数量变化的趋势。
- **Metrics**: ['DS', 'SR(%)', 'Avg. L2', 'Avg. col']
- **Expected outcome**: 适量历史查询应优于无历史查询，过多历史查询会降低闭环表现。
- **Baselines**: ['无历史查询变体', '较少历史查询变体', '较多历史查询变体']
- **Dependencies**: ['History queries', 'Memory Bank', 'history QA pairs']

## E6: 辅助VQA任务训练有效性
- **Verifies**: C6
- **Setup**:
  - Model: ORION训练任务变体
  - Hardware: 论文所述训练环境
  - Dataset: Bench2Drive与Chat-B2D
  - System: VQA微调、规划微调与联合训练对比
- **Procedure**:
  1. 分别进行仅VQA微调、仅规划微调和VQA加规划联合微调。
  2. 评估闭环规划指标、语言指标与开环规划误差。
  3. 比较单任务与联合任务训练是否能同时保持两类能力。
- **Metrics**: ['DS', 'SR(%)', 'CIDEr', 'BLEU', 'ROUGE-L', 'Avg. L2']
- **Expected outcome**: 联合训练应同时获得规划与语言侧能力，优于单任务训练的能力覆盖。
- **Baselines**: ['仅FT', '仅VQA Planning FT']
- **Dependencies**: ['Chat-B2D', 'VQA Planning FT', 'Fine Tuning']

## E7: nuScenes开环规划对比
- **Verifies**: C7
- **Setup**:
  - Model: 修改后的ORION
  - Hardware: 论文所述训练环境
  - Dataset: nuScenes
  - System: 替换为OmniDrive Q-Former且不使用显式ego status的开环规划设置
- **Procedure**:
  1. 在nuScenes开环规划协议下评估ORION。
  2. 与经典E2E方法和VLM-Based方法比较L2误差与碰撞率。
  3. 结合论文对数据分布差异的解释界定ORION的泛化边界。
- **Metrics**: ['L2', 'Collision']
- **Expected outcome**: ORION应与部分经典非VLM方法可比，但不应被解读为在nuScenes上全面领先VLM-Based方法。
- **Baselines**: ['ST-P3', 'UniAD', 'VAD-Base', 'Ego-MLP', 'BEV-Planner', 'DriveVLM', 'OmniDrive', 'Senna', 'EMMA']
- **Dependencies**: ['nuScenes', 'Q-Former from OmniDrive']

## E8: 训练策略消融
- **Verifies**: C8
- **Setup**:
  - Model: ORION训练阶段变体
  - Hardware: 论文所述训练环境
  - Dataset: Bench2Drive与Chat-B2D
  - System: vision-language-action渐进式空间对齐训练
- **Procedure**:
  1. 比较直接语言到动作训练、加入视觉语言对齐、以及完整vision-to-language-to-action训练。
  2. 保持论文指定的简化QT-Former设置。
  3. 评估不同训练阶段组合的闭环结果。
- **Metrics**: ['DS', 'SR(%)']
- **Expected outcome**: 完整渐进式训练应优于缺少早期空间对齐的训练流程。
- **Baselines**: ['仅L→A训练', 'V L加L→A训练']
- **Dependencies**: ['3D Vision-Language Alignment', 'Language-Action Alignment', 'End-to-End Fine-tuning']
