## 训练循环轮数
- **Value**: 1000 epochs
- **Rationale**: DIAMOND 采用循环式流程,每轮先收集真实环境经验,再更新 diffusion model、reward/termination model 与 actor-critic。
- **Search range**: 论文仅给默认值,未报告搜索范围。
- **Sensitivity**: 影响真实交互数据、模型更新与想象训练总量；论文未做该超参数消融。
- **Source**: Appendix E Table 3; Algorithm 1

## 每轮训练步数
- **Value**: 400 steps per epoch
- **Rationale**: 表3将每个 epoch 的训练步数设为统一默认值,并由 Algorithm 1 分别用于多个模型更新循环。
- **Search range**: 论文仅给默认值,未报告搜索范围。
- **Sensitivity**: 直接影响每轮 world model 与 agent 的优化预算；训练时间剖析也按该值计算。
- **Source**: Appendix E Table 3; Appendix I Table 5

## batch size
- **Value**: 32
- **Rationale**: 表3给出 DIAMOND 主实验训练批大小。
- **Search range**: 论文仅给默认值,未报告搜索范围。
- **Sensitivity**: 影响优化稳定性与显存占用；论文未报告 batch size 消融。
- **Source**: Appendix E Table 3

## 每轮环境步数
- **Value**: 100
- **Rationale**: 每轮 collect_experience 使用固定真实环境交互步数,随后在累计 replay dataset 上更新 world model 与 agent。
- **Search range**: Atari 100k 协议总真实交互受限于 100k actions。
- **Sensitivity**: 控制真实数据进入 replay dataset 的速率,与样本效率直接相关。
- **Source**: Appendix E Table 3; Sec 4

## 采集 epsilon
- **Value**: 0.01
- **Rationale**: 数据采集阶段使用 epsilon-greedy 以保留少量探索。
- **Search range**: 论文仅给默认值,未报告搜索范围。
- **Sensitivity**: 过低可能减少探索,过高可能降低当前策略采集质量；论文未做消融。
- **Source**: Appendix E Table 3

## optimizer
- **Value**: AdamW
- **Rationale**: 所有核心模块的优化器在表3中给出为 AdamW。
- **Search range**: 论文未报告其他优化器对比。
- **Sensitivity**: 影响 diffusion model、reward/termination model 与 actor-critic 的优化行为；论文未报告优化器敏感性。
- **Source**: Appendix E Table 3

## learning rate
- **Value**: 1e-4
- **Rationale**: 表3给出统一学习率。
- **Search range**: 论文仅给默认值,未报告搜索范围。
- **Sensitivity**: 影响三类网络训练稳定性；论文未给学习率消融。
- **Source**: Appendix E Table 3

## AdamW epsilon
- **Value**: 1e-8
- **Rationale**: 表3显式给出优化器 epsilon。
- **Search range**: 论文仅给默认值,未报告搜索范围。
- **Sensitivity**: 数值稳定性相关,论文未报告敏感性。
- **Source**: Appendix E Table 3

## weight decay for diffusion model
- **Value**: 1e-2
- **Rationale**: 表3为 diffusion model 指定权重衰减。
- **Search range**: 论文仅给默认值,未报告搜索范围。
- **Sensitivity**: 可能影响图像生成模型泛化与稳定性；论文未报告消融。
- **Source**: Appendix E Table 3

## weight decay for reward/termination model
- **Value**: 1e-2
- **Rationale**: 表3为 reward/termination model 指定权重衰减。
- **Search range**: 论文仅给默认值,未报告搜索范围。
- **Sensitivity**: 影响标量预测模型的正则化；论文未报告消融。
- **Source**: Appendix E Table 3

## weight decay for actor-critic
- **Value**: 0
- **Rationale**: 表3将 policy 与 value network 的权重衰减设为 0。
- **Search range**: 论文仅给默认值,未报告搜索范围。
- **Sensitivity**: 影响 RL 网络正则化；论文未报告对比。
- **Source**: Appendix E Table 3

## imagination horizon H
- **Value**: 15
- **Rationale**: actor-critic 在 world model 中按固定 horizon 生成想象轨迹并计算 λ-returns 与 policy objective。
- **Search range**: 论文仅给默认值,未报告搜索范围。
- **Sensitivity**: 影响长期 credit assignment 与单次 actor-critic 更新成本；Table 5 的 imagination step 剖析与该值相关。
- **Source**: Appendix E Table 3; Appendix F; Appendix I Table 5

## discount factor γ
- **Value**: 0.985
- **Rationale**: λ-returns 递推和价值目标使用该折扣因子。
- **Search range**: 论文仅给默认值,未报告搜索范围。
- **Sensitivity**: 控制未来回报权重；论文未报告消融。
- **Source**: Appendix E Table 3; Appendix F Eq 14

## entropy weight η
- **Value**: 0.001
- **Rationale**: policy objective 将 REINFORCE 项与加权 entropy maximization 结合。
- **Search range**: 论文仅给默认值,未报告搜索范围。
- **Sensitivity**: 影响想象训练中的探索保持；论文未报告消融。
- **Source**: Appendix E Table 3; Appendix F Eq 16

## λ-returns coefficient λ
- **Value**: 0.95
- **Rationale**: value network 使用 λ-returns 平衡 bias 与 variance。
- **Search range**: 论文仅给默认值,未报告搜索范围。
- **Sensitivity**: 影响价值目标的偏差方差权衡；论文未报告消融。
- **Source**: Appendix E Table 3; Appendix F Eq 14

## reward clipping
- **Value**: {−1, 0, 1}
- **Rationale**: 环境设置中对 reward 进行离散裁剪,并在 reward model 中预测 sign reward。
- **Search range**: 论文仅给默认值,未报告搜索范围。
- **Sensitivity**: 影响 reward/termination model 的分类目标与 RL 信号尺度。
- **Source**: Appendix E Table 3; Algorithm 1

## Atari random seeds
- **Value**: 5 random seeds per game
- **Rationale**: 主 Atari 100k 评估中每个游戏从头训练多个随机种子。
- **Search range**: 论文主实验报告固定为 5 random seeds。
- **Sensitivity**: 影响分数估计方差；Table 7 的 1-step 结果被作者标注为 single seed 因而方差更高。
- **Source**: Sec 4; Appendix L
