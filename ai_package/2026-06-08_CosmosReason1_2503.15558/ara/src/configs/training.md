## SFT 学习率调度（Cosmos-Reason1-7B）
- **Value**: 余弦退火，初始值 1×10^-5 衰减至终值 1×10^-6
- **Rationale**: 余弦退火使学习率平滑下降，有助于大规模多模态 SFT 阶段收敛稳定
- **Search range**: 1×10^-6 ~ 1×10^-5
- **Sensitivity**: high
- **Source**: Sec 7.1

## SFT 训练迭代数（Cosmos-Reason1-7B）
- **Value**: 约 12.5K 次（原 MD 文件该处存在编码特殊字符，数值以论文原文为准）
- **Rationale**: 论文报告值
- **Search range**: 论文未给出范围
- **Sensitivity**: medium
- **Source**: Sec 7.1

## SFT 学习率策略（Cosmos-Reason1-56B）
- **Value**: 第一阶段约 30K 次迭代使用 1×10^-5，第二阶段约 20K 次迭代衰减至 1×10^-6
- **Rationale**: 两阶段学习率策略适配大规模混合架构模型，先快速学习后精细收敛
- **Search range**: 1×10^-6 ~ 1×10^-5
- **Sensitivity**: high
- **Source**: Sec 7.1

## SFT 全局批量大小（Cosmos-Reason1-7B）
- **Value**: 256
- **Rationale**: 7B 密集 Transformer 模型 SFT 阶段使用的全局批量大小
- **Search range**: 论文未给出范围
- **Sensitivity**: medium
- **Source**: Sec 7.1

## SFT 全局批量大小（Cosmos-Reason1-56B）
- **Value**: 32
- **Rationale**: 56B 混合架构模型受显存限制使用较小批量
- **Search range**: 论文未给出范围
- **Sensitivity**: medium
- **Source**: Sec 7.1

## SFT 优化器
- **Value**: Fused Adam，β1=0.9，β2=0.95，权重衰减 0.1
- **Rationale**: Fused Adam 在大规模训练中计算效率更高；适中的权重衰减防止过拟合
- **Search range**: 论文未给出范围
- **Sensitivity**: medium
- **Source**: Sec 7.1

## SFT 数据均衡采样策略
- **Value**: 均衡采样（balanced data sampling）
- **Rationale**: 防止特定领域数据在 SFT 训练中过度表示，保证多领域能力均衡发展
- **Search range**: N/A
- **Sensitivity**: medium
- **Source**: Sec 7.1

## RL 算法
- **Value**: GRPO（Group Relative Policy Optimization），优势函数 $$A_i = \frac{R(o_i) - \mathsf{mean}(\mathcal{G})}{\mathsf{std}(\mathcal{G})}$$
- **Rationale**: GRPO 无需单独训练价值网络（critic），计算效率高；通过组内奖励归一化计算优势，消除量纲差异
- **Search range**: N/A
- **Sensitivity**: high
- **Source**: Sec 4.1

## RL 学习率
- **Value**: 4×10^-6
- **Rationale**: RL 后训练使用比 SFT 更小的学习率，防止策略更新过大破坏已有能力
- **Search range**: 论文未给出范围
- **Sensitivity**: high
- **Source**: Sec 7.2.1

## RL KL 惩罚系数
- **Value**: 0.005
- **Rationale**: 控制策略偏离参考模型的程度，防止奖励黑客行为与分布崩塌
- **Search range**: 论文未给出范围
- **Sensitivity**: high
- **Source**: Sec 7.2.1

## RL 训练迭代数
- **Value**: 500
- **Rationale**: 论文报告的 RL 后训练总迭代次数
- **Search range**: 论文未给出范围
- **Sensitivity**: medium
- **Source**: Sec 7.2.1

## RL 全局批量大小
- **Value**: 128 个问题
- **Rationale**: 每个 RL 训练步使用 128 道 MCQ 题目
- **Search range**: 论文未给出范围
- **Sensitivity**: medium
- **Source**: Sec 7.2.1

## 每题 RL 采样输出数
- **Value**: 9
- **Rationale**: GRPO 对每道题采样一组响应以计算组内归一化优势；9 个输出覆盖足够多样性
- **Search range**: 论文未给出范围
- **Sensitivity**: medium
- **Source**: Sec 7.2.1

## RL 输出最大 token 数
- **Value**: 6144
- **Rationale**: 限制长链式推理输出长度，平衡推理质量与训练效率
- **Search range**: 论文未给出范围
- **Sensitivity**: medium
- **Source**: Sec 7.2.1

## RL 训练时 MCQ 选项动态打乱
- **Value**: 开启，on-the-fly 随机打乱
- **Rationale**: 鼓励模型泛化，防止记忆选项顺序导致奖励黑客行为
- **Search range**: N/A
- **Sensitivity**: medium
- **Source**: Sec 7.2.1

## RL 奖励类型
- **Value**: 准确率奖励（字符串匹配 answer 标签内容）+ 格式奖励（正则匹配 think/answer 标签）
- **Rationale**: 规则可验证的双奖励设计：准确率奖励确保答案正确，格式奖励促进结构化推理链生成
- **Search range**: N/A
- **Sensitivity**: high
- **Source**: Sec 7.2.1

## 推理评估温度
- **Value**: 0.6
- **Rationale**: 适中温度平衡多样性与确定性，用于评估时多次推理取均值
- **Search range**: 论文未给出范围
- **Sensitivity**: low
- **Source**: Sec 7.1

## 推理评估 top-p
- **Value**: 0.95
- **Rationale**: 核采样参数，配合温度 0.6 使用
- **Search range**: 论文未给出范围
- **Sensitivity**: low
- **Source**: Sec 7.1

## 推理平均次数
- **Value**: 5 次（不同随机种子）
- **Rationale**: 对 5 次不同随机种子的推理结果取平均准确率，减少随机性影响
- **Search range**: N/A
- **Sensitivity**: low
- **Source**: Sec 7.1

## SFT 张量并行度（Cosmos-Reason1-7B）
- **Value**: TP=4
- **Rationale**: 7B 密集 Transformer 模型的张量并行配置
- **Search range**: N/A
- **Sensitivity**: low
- **Source**: Sec 3.2

## SFT 张量并行度与流水线并行度（Cosmos-Reason1-56B）
- **Value**: TP=8，PP=2
- **Rationale**: 56B 混合架构模型需要更大并行度以适应显存容量
- **Search range**: N/A
- **Sensitivity**: low
- **Source**: Sec 3.2
