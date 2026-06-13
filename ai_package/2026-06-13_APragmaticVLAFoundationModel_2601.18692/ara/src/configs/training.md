## 预训练数据规模
- **Value**: about 20,000 hours of real-world manipulation data，来自9个robotic platforms
- **Rationale**: 论文把大规模真实世界多具身数据作为LingBot-VLA泛化能力的主要训练来源。
- **Search range**: 缩放实验覆盖3,000 hours到20,000 hours；论文未给出更细粒度训练规模网格。
- **Sensitivity**: 数据规模增大时，成功率和进展率呈持续上升趋势；到20,000-hour mark未显示饱和。
- **Source**: <!--ref:Abstract--> <!--ref:Sec 1--> <!--ref:Sec 2.1--> <!--ref:Sec 5.5.1-->

## 预训练动作块长度
- **Value**: T is set to 50 during our pre-training stage
- **Rationale**: 动作序列被表示为从当前时刻开始的action chunk，用于条件Flow Matching建模。
- **Search range**: 论文仅显式给出预训练阶段T=50，未报告其他取值。
- **Sensitivity**: 动作块长度影响预测轨迹的时间范围；具体敏感性论文未做消融。
- **Source**: <!--ref:Sec 4.1 Eq 2-->

## 训练目标
- **Value**: Flow Matching objective，用action expert预测conditional vector field
- **Rationale**: 论文用conditional flow matching表征p(A_t | O_t)，以连续动作建模支持平滑机器人控制。
- **Search range**: 论文给出Flow Matching objective和depth distillation loss；未给出替代训练目标的超参网格。
- **Sensitivity**: 训练目标是核心建模选择；论文没有报告对其他目标函数的直接对比。
- **Source**: <!--ref:Sec 4.1 Eq 3--> <!--ref:Sec 4.1 Eq 4--> <!--ref:Sec 4.1 Eq 5-->

## 深度蒸馏训练信号
- **Value**: learnable queries与LingBot-Depth tokens对齐，并最小化L_distill
- **Rationale**: 通过把VLM learnable queries与depth tokens对齐，引入几何信息以增强空间感知。
- **Search range**: 论文描述三视角operational images对应的learnable queries；未报告蒸馏权重或查询数量消融。
- **Sensitivity**: 加入depth-based spatial information后，论文报告真实世界与仿真设置中表现更优；具体机制敏感性未单独量化。
- **Source**: <!--ref:Sec 4.1 Eq 5--> <!--ref:Sec 5.2--> <!--ref:Sec 5.3-->

## 后训练公平比较超参
- **Value**: batch sizes=256, epochs=20
- **Rationale**: 所有模型使用同一post-training pipeline、同一verified dataset和一致超参，以隔离架构性能差异。
- **Search range**: 论文只报告batch sizes=256与epochs=20；未提供其他后训练超参范围。
- **Sensitivity**: 用于公平比较控制变量；论文未做batch size或epoch敏感性分析。
- **Source**: <!--ref:Sec 5.1.3-->

## 训练吞吐对比本地批量
- **Value**: local batch size was standardized to 32 for all experiments
- **Rationale**: 训练效率比较中用统一local batch size控制不同代码库之间的配置差异。
- **Search range**: 论文只说明local batch size=32；未报告其他local batch设置。
- **Sensitivity**: 作为吞吐实验的标准化配置；论文未单独分析local batch size变化。
- **Source**: <!--ref:Sec 5.4-->

## 分布式训练策略
- **Value**: FSDP，action expert modules专用shard groups，reductions in torch.float32，storage and communication使用torch.bfloat16
- **Rationale**: 通过分片optimizer states、model parameters和gradients降低显存占用，并通过action expert shard groups缓解过度分片通信开销。
- **Search range**: 论文还提到FSDP2用于吞吐比较；未给出不同shard group尺寸或精度策略网格。
- **Sensitivity**: 该策略服务于显存占用与吞吐折中；论文报告整体训练速度最快，但未隔离每个分布式子策略的贡献。
- **Source**: <!--ref:Sec 4.2 Distributed Strategy--> <!--ref:Sec 5.4-->

## 算子级优化
- **Value**: FlexAttention和torch.compile operator fusion
- **Rationale**: 论文将多模态融合视为sparse attention，并用FlexAttention优化计算；用torch.compile减少kernel launch overhead并提升memory bandwidth utilization。
- **Search range**: 论文未报告替代attention实现或fusion开关的消融范围。
- **Sensitivity**: 算子优化被归入高吞吐代码库设计；单独敏感性论文未量化。
- **Source**: <!--ref:Sec 4.2 Operator-Level Optimization-->
