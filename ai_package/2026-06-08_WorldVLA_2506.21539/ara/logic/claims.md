# Claims

## C1: WorldVLA 统一框架实现动作与视觉理解生成的互促增益
- **Statement**: WorldVLA 将 VLA 动作模型与世界模型统一在单一离散自回归框架中，两者相互增益：世界模型提升动作生成性能，动作模型提升视频生成质量，联合框架整体优于各自独立模型。
- **Status**: supported
- **Falsification criteria**: 若在 LIBERO 基准上 WorldVLA 的动作成功率不高于单独动作模型，且视频生成质量不优于单独世界模型，则该声明被否定。
- **Proof**: [E1, E2, E3]
- **Evidence basis**: ['E1', 'E2', 'E3']
- **Interpretation**: 共享表征联合训练使世界模型迫使模型学习物理动态，间接增强动作生成；动作模型增强视觉理解，进而改善视频预测。两者形成正向循环。
- **Tags**: ['improvement', 'causal']

## C2: 世界模型集成显著提升动作模型性能
- **Statement**: 在 LIBERO 基准上，加入世界模型数据联合训练后，WorldVLA 平均抓取成功率相较单独动作模型提升约 4%；在 LIBERO-Long 任务上提升尤为显著。
- **Status**: supported
- **Falsification criteria**: 若 Table 3 消融中加入世界模型（行 2）的平均 SR 不高于不加世界模型（行 1），则该声明被否定。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 世界模型通过预测下一状态，迫使模型理解环境物理动态和动作语义，同时赋予系统前瞻仿真能力，有助于动作决策规避不良状态。
- **Tags**: ['improvement', 'causal']

## C3: 动作模型集成提升世界模型长序列视频生成质量
- **Statement**: 与单独世界模型相比，WorldVLA 动作世界模型在长序列（50 帧）视频生成上具有更低的 FVD，表明动作模型对视觉理解的增强有助于生成更物理合理的视频序列。
- **Status**: supported
- **Falsification criteria**: 若 Table 4 中 50 帧条件下动作世界模型的 FVD 不低于纯世界模型，则该声明被否定。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 动作模型训练增强了对图像语义及行为模式的理解，有助于世界模型更准确预测未来状态。短序列（10 帧）FVD 略高于纯世界模型，说明增益主要体现在长序列上。
- **Tags**: ['improvement', 'causal']

## C4: 自回归动作块生成存在错误传播导致性能退化
- **Statement**: 在自回归框架中，采用默认因果注意力遮蔽连续生成多个动作时，后续动作过度依赖前序动作而非视觉输入，导致错误累积，抓取成功率下降 10% 至 50%。
- **Status**: supported
- **Falsification criteria**: 若 Table 3 中使用默认注意力遮蔽的动作块生成（行 3）成功率不低于单步动作生成（行 1），则该声明被否定。
- **Proof**: [E2, E4]
- **Evidence basis**: ['E2', 'E4']
- **Interpretation**: MLLM 预训练阶段主要接触图像和文本，动作域泛化能力有限。默认因果遮蔽使后续动作条件化于前序动作，而动作 token 与图像/文本 token 共享同一空间，导致误差随序列增长而累积。
- **Tags**: ['causal', 'descriptive']

## C5: 提出的动作注意力遮蔽策略有效缓解动作块生成退化
- **Statement**: WorldVLA 提出的注意力遮蔽策略在生成当前动作时屏蔽所有前序动作 token，使每个动作独立依赖视觉和文本输入，在动作块生成任务中可提升抓取成功率 4% 至 23%。
- **Status**: supported
- **Falsification criteria**: 若 Table 3 中使用新注意力遮蔽（行 4）的平均 SR 不高于使用默认遮蔽的动作块生成（行 3），则该声明被否定。
- **Proof**: [E2, E4]
- **Evidence basis**: ['E2', 'E4']
- **Interpretation**: 该遮蔽机制令自回归框架在动作维度实现并行解码，本质上与 π0、OpenVLA-OFT 等连续动作模型的并行动作输出目标一致，但在离散自回归架构下实现。
- **Tags**: ['improvement', 'causal']

## C6: 以世界模型权重预训练动作模型可进一步提升性能
- **Statement**: 以世界模型权重作为动作模型预训练起点，相较直接训练动作模型，可进一步提升 LIBERO 基准各子任务的抓取成功率。
- **Status**: supported
- **Falsification criteria**: 若 Table 6 中使用世界模型预训练的动作模型平均 SR 不高于不使用预训练的版本，则该声明被否定。
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: 世界模型预训练使模型预先掌握视觉输入、动作输入以及状态转换的物理动态，为下游动作微调提供更有信息量的初始化权重。
- **Tags**: ['improvement', 'causal']

## C7: 有动作条件的世界模型优于无动作条件的视频预测模型
- **Statement**: 以动作为条件的世界模型对动作模型的提升效果在所有评测任务上均为正向，而无动作条件的视频预测模型对部分任务有益但对另一些任务产生负面影响。
- **Status**: supported
- **Falsification criteria**: 若视频预测模型对动作模型各任务的平均提升不低于世界模型，或世界模型对某任务出现负向影响，则该声明被否定。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 视频预测模型缺乏动作条件约束，同一起始帧可对应多个合理未来帧，训练时引入歧义噪声；世界模型通过动作输入唯一化预测目标，同时迫使模型深度理解动作语义。
- **Tags**: ['improvement', 'causal', 'descriptive']
