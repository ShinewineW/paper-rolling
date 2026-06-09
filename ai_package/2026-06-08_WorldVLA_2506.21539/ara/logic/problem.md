# Problem Specification

## Observations

### O1: 现有 VLA 模型将动作仅作为输出而非输入，缺乏对动作的深度理解
- **Statement**: 现有 VLA 模型将动作仅作为输出而非输入，缺乏对动作的深度理解
- **Evidence**: 论文第 1 节：「these models often lack a comprehensive understanding of actions, as actions are treated solely as outputs but not being integrated as inputs for deeper analysis」
- **Implication**: VLA 模型无法利用动作语义反馈来辅助视觉理解与环境规划

### O2: 世界模型能预测未来视觉状态，但无法直接输出动作
- **Statement**: 世界模型能预测未来视觉状态，但无法直接输出动作
- **Evidence**: 论文第 1 节：「world models are constrained by their inability to directly generate action outputs, resulting in a functional gap」
- **Implication**: 世界模型在需要显式动作规划的机器人场景中存在功能缺口

### O3: 自回归方式顺序生成多个动作时，模型性能出现明显下降
- **Statement**: 自回归方式顺序生成多个动作时，模型性能出现明显下降
- **Evidence**: Table 3 第 3 行（启用 action chunking 但无掩码）Average SR 仅 54.0%，低于单步基线第 1 行的 62.8%
- **Implication**: 预训练 MLLM 在动作域泛化能力有限，早期动作误差会随自回归步骤不断传播

## Gaps

### G1: 缺乏能同时执行动作预测与世界状态预测、并让两者互相增强的统一框架
- **Statement**: 缺乏能同时执行动作预测与世界状态预测、并让两者互相增强的统一框架
- **Caused by**: C1, C2
- **Existing attempts**: []
- **Why they fail**: VLA 与世界模型各自只完成一项任务，无法从对方的监督信号中获益

### G2: 自回归动作块生成中的误差传播问题缺乏有效的结构性解决方案
- **Statement**: 自回归动作块生成中的误差传播问题缺乏有效的结构性解决方案
- **Caused by**: C3
- **Existing attempts**: []
- **Why they fail**: 默认因果注意力掩码使后续动作 token 依赖先前动作 token，而非视觉输入，导致误差随序列长度累积

## Key Insight
- **Insight**: 将图像、文本、动作三种模态的 token 纳入统一离散词表，用单一自回归 LLM 混合训练动作模型数据与世界模型数据；同时引入专用注意力掩码，令动作 token 的生成仅依赖视觉/文本输入而屏蔽先前动作，从而同时解决双任务互促与误差传播两个问题
- **Derived from**: G1, G2
- **Enables**: 无需额外预训练即可在动作成功率和视频生成质量两个维度同步超越单独的动作模型与世界模型

## Assumptions
- Chameleon 骨干的共享词表可统一表达图像、文本、动作三种模态，无需为不同模态设计独立编解码器（分析推断，论文未显式声明）
- 将连续动作每维离散化为 256 个 bin 足以覆盖机器人操控任务所需精度
- 混合训练时世界模型数据对动作模型的干扰可通过超参数 α 充分控制（分析推断，论文未显式声明）
