## 预训练数据规模与过滤策略
- **Value**: 从超过6 billion curated clips中过滤保留约200 million trainable clips；仅约4%初始 clips 通过全部过滤
- **Rationale**: 更严格的多阶段过滤用于去除运动伪影、失真、视觉噪声、overlay text、语义伪影和不适合训练的内容，从而提升预训练数据质量。
- **Search range**: clips 长度为5 to 60 seconds；低于5 seconds的片段被丢弃；保留率从30%收紧到4%
- **Sensitivity**: 高；数据质量、语义多样性与物理世界分布对后续 Text2World、Image2World、Video2World 质量都有直接影响。
- **Source**: Sec 2.1

## 渐进式预训练阶段
- **Value**: 从Text2Image 256p开始，随后加入Image2World和Video2World，并逐步提升到480p与720p，最后加入Text2World
- **Rationale**: 先学习单帧质量，再逐步增加运动、时间一致性、分辨率和任务多样性，以平衡效率与模型质量。
- **Search range**: Table 4列出256p 320×192、480p 832×480、720p 1280×704；帧数为1或93
- **Sensitivity**: 高；论文说明在模型收敛且视觉质量进入平台期后才进入下一阶段，说明阶段推进影响稳定性与质量。
- **Source**: Sec 4.1; Tab. 4

## 条件帧采样
- **Value**: Image2World和Video2World阶段随机采样1或5个条件帧；最终阶段采样0、1或2个条件帧，概率为0.5、0.25、0.25
- **Rationale**: 统一支持Text2World、Image2World和Video2World，并通过mask标记条件输入，只在指定帧上施加去噪损失。
- **Search range**: 条件帧数量为0、1、2、5；生成总长为93 pixel frames，对应24 latent video frames
- **Sensitivity**: 中高；条件帧数量会改变任务形式和梯度作用位置，影响输入忠实度和自由生成能力。
- **Source**: Sec 4.1

## timestep分布与shift
- **Value**: 训练timesteps来自logit-normal distribution，并随分辨率使用progressive timestep shift，从β = 1 at 256p逐渐增加到β = 5 at 720p
- **Rationale**: 高分辨率内容存在强相关性，向更高噪声偏置可帮助模型在相关性被破坏时学习重建结构。
- **Search range**: β = 1时无shift；论文给出最高到β = 5 at 720p
- **Sensitivity**: 高；论文明确指出噪声区域覆盖不足会导致帧间突兀和不自然过渡。
- **Source**: Sec 3.1; Sec 4.1

## 高噪声重采样
- **Value**: 5%训练样本显式从噪声分布最高2%抽取
- **Rationale**: 作者观察到生成视频存在突兀、不自然的帧间过渡，并假设模型在高噪声区域训练样本过少；该策略显著减少过渡伪影并改善时间一致性。
- **Search range**: 论文只给出5%与最高2%，未说明其他比例扫描范围
- **Sensitivity**: 高；这是针对已观察失败模式的关键调度修正。
- **Source**: Sec 4.1

## 优化器
- **Value**: AdamW，β1 = 0.9，β2 = 0.999
- **Rationale**: 用于主模型训练；论文没有报告替代优化器比较。
- **Search range**: 论文未说明可调范围
- **Sensitivity**: 中；作为基础训练超参数，可能影响稳定性，但论文未提供敏感性实验。
- **Source**: Sec 4.1

## 学习率
- **Value**: Cosmos-Predict2.5-2B使用3 × 10^{-5}；Cosmos-Predict2.5-14B使用1.3 × 10^{-5}
- **Rationale**: 不同规模模型使用不同学习率以适配训练稳定性和模型容量。
- **Search range**: 论文仅给出这两个模型规模的学习率
- **Sensitivity**: 中高；论文把学习率列为训练recipe核心配置，但未给出扫参曲线。
- **Source**: Sec 4.1

## weight decay与warmup
- **Value**: weight decay为0.001；线性衰减学习率调度器包含2000 iterations初始warmup
- **Rationale**: 用于稳定优化，并在训练过程中逐步降低学习率。
- **Search range**: 论文未说明其他weight decay或warmup设置
- **Sensitivity**: 中；论文明确用于稳定优化，但未报告单独消融。
- **Source**: Sec 4.1

## SFT训练设置
- **Value**: 每个领域单独fine-tune 30k iterations，batch size为256，使用预训练最终阶段相同超参数
- **Rationale**: 领域专用SFT可充分利用各领域数据，无需联合数据混合比例；小幅通用域退化可通过模型合并缓解。
- **Search range**: 领域包括object permanence、high motion、complex scenes、driving、robotic manipulation
- **Sensitivity**: 高；论文报告每个SFT模型在目标领域相对pretrained baseline有更高human preference win rate。
- **Source**: Sec 4.2.1; Tab. 5; Fig. 3

## 模型合并选择
- **Value**: 比较model soup、TIES、DARE-Linear、DARE-TIES；每种方法做hyperparameter sweeps并生成超过20个merged models；最终选择model soup variant
- **Rationale**: 用于合并领域SFT模型和cooldown模型的优点，同时保持通用域表现。
- **Search range**: 四类合并方法；候选超过20个merged models
- **Sensitivity**: 高；作者指出simple grid search优于基于单个fine-tuned模型win rate的启发式选择，且DARE-Linear是例外表现较弱。
- **Source**: Sec 4.2.1; Fig. 4

## RL post-training
- **Value**: 使用VideoAlign reward model；每个条件生成8个outputs、20 diffusion steps；训练256 steps，batch size为32，并用diffusion loss正则化
- **Rationale**: 通过奖励模型对text alignment、motion quality和visual quality进行后训练，并用GRPO式组内归一化优势；diffusion loss用于缓解reward hacking。
- **Search range**: 论文仅给出Cosmos-Predict2.5-2B的RL设置
- **Sensitivity**: 高；Tab. 6和human voting显示RL后reward与偏好均提升。
- **Source**: Sec 4.2.2; Tab. 6; Fig. 5

## Cosmos-Transfer2.5控制分支训练
- **Value**: 每个control branch独立训练100,000 iterations，effective batch size为64，其余超参数沿用Cosmos-Predict2.5-2B
- **Rationale**: 让每个模态分支先专门学习从edge、blur、segmentation、depth等控制输入提取有用表示。
- **Search range**: 控制条件包括edge、blur、segmentation、depth
- **Sensitivity**: 中高；控制分支质量直接影响PAIBench-Transfer中的control alignment和overall quality。
- **Source**: Sec 6.1
