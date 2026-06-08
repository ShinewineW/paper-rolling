## 7B SFT 学习率调度
- **Value**: 余弦退火，从 1×10⁻⁵ 衰减至 1×10⁻⁶
- **Rationale**: 余弦退火在训练后期平滑降低学习率，有助于最终收敛稳定，避免震荡
- **Search range**: 初始 1×10⁻⁵，最终 1×10⁻⁶
- **Sensitivity**: medium
- **Source**: Sec. 7.1

## 56B SFT 学习率（两阶段）
- **Value**: 第一阶段 1×10⁻⁵（约 30K 次迭代），第二阶段衰减至 1×10⁻⁶（约 20K 次迭代）
- **Rationale**: 56B 规模更大，采用分段固定学习率策略以在训练前段保持较大更新步长，后段精细收敛
- **Search range**: 1×10⁻⁶ 至 1×10⁻⁵
- **Sensitivity**: medium
- **Source**: Sec. 7.1

## 7B SFT 全局批次大小
- **Value**: 256
- **Rationale**: 较大批次有助于梯度估计稳定性，与 7B 模型规模匹配
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: medium
- **Source**: Sec. 7.1

## 56B SFT 全局批次大小
- **Value**: 32
- **Rationale**: 56B 模型显存占用大，批次大小相应缩小以适配硬件约束
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: medium
- **Source**: Sec. 7.1

## SFT 优化器
- **Value**: fused Adam，β₁=0.9，β₂=0.95，weight decay=0.1
- **Rationale**: fused Adam 在 GPU 上计算高效；weight decay 起正则化作用防止过拟合
- **Search range**: 论文未给出超参搜索范围
- **Sensitivity**: medium
- **Source**: Sec. 7.1

## SFT 数据采样策略
- **Value**: 均衡采样（balanced data sampling）：各数据域等权重，避免任一域过度占比
- **Rationale**: 物理常识与具身推理各子域数据量差异较大，均衡采样防止主要域主导梯度方向
- **Search range**: 均等概率
- **Sensitivity**: medium
- **Source**: Sec. 7.1

## RL 全局批次大小
- **Value**: 128 个问题
- **Rationale**: 每问题采样 9 条输出，实际生成量为 128×9 条，保证 GRPO 优势估计的组内多样性
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: high
- **Source**: Sec. 7.2.1

## RL 每问题输出数（GRPO 组大小 G）
- **Value**: 9
- **Rationale**: GRPO 通过对同一问题的 G 条响应归一化奖励计算优势，组越大估计越准确但计算量越大
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: high
- **Source**: Sec. 7.2.1

## RL 最大输出长度截断
- **Value**: 6144 tokens
- **Rationale**: 长链式推理（CoT）需要充足 token 预算以完成多步思考，过短截断会破坏推理过程
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: medium
- **Source**: Sec. 7.2.1

## RL 学习率
- **Value**: 4×10⁻⁶
- **Rationale**: RL 阶段使用比 SFT 更小的学习率，防止策略大幅偏离 SFT 后的基础能力
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: high
- **Source**: Sec. 7.2.1

## RL KL 惩罚系数
- **Value**: 0.005
- **Rationale**: KL 惩罚约束策略不过度偏离参考模型，防止奖励 hacking 并维持输出质量
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: high
- **Source**: Sec. 7.2.1

## RL 训练迭代次数
- **Value**: 500
- **Rationale**: 在有限迭代内使物理常识与具身推理能力达到收敛，避免过度优化导致退化
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: medium
- **Source**: Sec. 7.2.1

## RL MCQ 选项动态随机化
- **Value**: 训练时对每个 MCQ 问题的选项顺序进行动态随机打乱（on-the-fly shuffling）
- **Rationale**: 防止模型记忆选项位置偏置，提升对选项顺序变化的泛化能力，降低奖励 hacking 风险
- **Search range**: 默认开启
- **Sensitivity**: medium
- **Source**: Sec. 7.2.1

## RL 数据集采样策略
- **Value**: 各 RL 数据集等概率采样，确保跨域均衡表示
- **Rationale**: 物理常识、具身推理、直觉物理各子集规模不同，等概率采样防止某一子域主导训练信号
- **Search range**: 等概率
- **Sensitivity**: medium
- **Source**: Sec. 7.2.1

## 模型评估采样策略
- **Value**: 5 次推理取平均准确率，temperature=0.6，top-p=0.95，每次使用不同随机种子
- **Rationale**: 多次采样取平均降低推理随机性带来的方差，提高评估结果的稳定性
- **Search range**: 固定
- **Sensitivity**: low
- **Source**: Sec. 7.1
