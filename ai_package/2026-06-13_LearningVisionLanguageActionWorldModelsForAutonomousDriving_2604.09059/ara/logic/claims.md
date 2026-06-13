# Claims

## C1: VLA-World提升端到端轨迹规划
- **Statement**: VLA-World在nuScenes端到端轨迹规划评测中，相比多类非自回归与自回归基线取得更低的L2误差与碰撞率，并且论文将收益归因于动作条件未来帧生成与反思式轨迹修正。
- **Status**: supported
- **Falsification criteria**: 如果在相同nuScenes协议下，VLA-World未能优于表中主要自回归基线，或碰撞率与L2误差不再占优，则该主张被削弱。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 该结果支持论文核心论点：把预测性想象和反思式推理合并到同一VLA世界模型中，可以改善规划安全性与轨迹精度。
- **Tags**: ['improvement']

## C2: 未来帧生成质量优于生成基线
- **Statement**: VLA-World在nuScenes未来帧生成评测中取得最低FID，论文认为即便未来帧只是中间推理步骤，也能有效释放多模态大模型的视觉生成能力。
- **Status**: supported
- **Falsification criteria**: 如果在相同FID评测设置下，VLA-World不能优于Doe-1、FSDrive或专门的扩散式生成基线，则该主张不成立。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 该证据表明，动作与轨迹条件化的短期未来生成不仅服务于规划，也能形成可量化的视觉质量优势。
- **Tags**: ['improvement']

## C3: 动作预测能力增强
- **Statement**: VLA-World在nuScenes动作预测任务中，相比基础Qwen2-VL-2B及其nuScenes微调版本，在横向与纵向动作类别上表现更好。
- **Status**: supported
- **Falsification criteria**: 如果同一动作F1评测中，VLA-World不能在各动作类型上保持优势，则论文关于目标条件控制学习能力增强的解释会被削弱。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 动作预测结果补充说明模型不只是拟合轨迹点，还学习了更明确的驾驶意图与控制类别。
- **Tags**: ['improvement']

## C4: 训练阶段、数据管线和奖励项均有贡献
- **Statement**: 消融结果显示，去掉预训练、SFT、RL、感知、生成、推理或不同奖励项都会带来轨迹规划退化，其中论文特别强调SFT对冷启动和因果链理解的重要性。
- **Status**: supported
- **Falsification criteria**: 如果删除这些阶段或组件后性能不变或更优，则三阶段训练与管线组件共同贡献的因果解释不成立。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 这些消融把主模型收益分解到训练策略、数据管线与奖励设计，支持完整VLA-World训练方案的必要性。
- **Tags**: ['causal']

## C5: 输入分辨率、模型规模和混合任务训练影响规划表现
- **Statement**: 补充消融显示，更高输入分辨率、更大Qwen-VL系列骨干以及混合任务训练与更好的轨迹规划表现相关。
- **Status**: supported
- **Falsification criteria**: 如果改变输入分辨率、模型规模或移除混合数据后不会影响规划L2误差，则该扩展性与训练数据作用主张被削弱。
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: 该结果说明VLA-World的效果不仅来自单一主干配置，还受视觉保真度、模型容量与多任务监督共同影响。
- **Tags**: ['generalization']
