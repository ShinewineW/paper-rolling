## 学习率
- **Value**: 4×10^-5
- **Rationale**: 跨所有领域统一使用同一学习率,配合AGC梯度裁剪实现稳定训练
- **Search range**: 论文未提供搜索范围
- **Sensitivity**: 论文未单独消融,属于固定超参数之一
- **Source**: Table 4

## 批次大小(B)
- **Value**: 16
- **Rationale**: 并行序列轨迹数,平衡训练效率与内存占用
- **Search range**: 论文未提供搜索范围
- **Sensitivity**: 论文未单独消融
- **Source**: Table 4

## 批次长度(T)
- **Value**: 64
- **Rationale**: 每条训练序列包含的时间步数,控制BPTT截断长度
- **Search range**: 论文未提供搜索范围
- **Sensitivity**: 论文未单独消融
- **Source**: Table 4

## 重放缓冲区容量
- **Value**: 5×10^6
- **Rationale**: 均匀重放缓冲区存储经验轨迹及对应潜态,支持离线回放训练
- **Search range**: 论文未提供搜索范围
- **Sensitivity**: 论文未单独消融
- **Source**: Table 4

## 优化器
- **Value**: LaProp(ε=10^-20, β1=0.9, β2=0.99)
- **Rationale**: 先用RMSProp归一化梯度再用动量平滑,避免Adam在某些情况下的偶发不稳定性;极小ε避免数值截断
- **Search range**: 论文未提供搜索范围
- **Sensitivity**: 论文提到Adam在某些情况有不稳定性,故改用LaProp
- **Source**: Methods节 Optimizer部分

## 自适应梯度裁剪(AGC)
- **Value**: 阈值0.3, ε=10^-3
- **Rationale**: 当每张量梯度超过对应权重矩阵L2范数30%时裁剪;将裁剪阈值与损失量级解耦,允许修改损失函数或损失权重而无需重新调整裁剪阈值
- **Search range**: 论文未提供搜索范围
- **Sensitivity**: 论文强调AGC与损失量级解耦是跨域固定超参数的关键支撑
- **Source**: Methods节 Optimizer部分

## 世界模型损失权重(β_pred, β_dyn, β_rep)
- **Value**: β_pred=1, β_dyn=1, β_rep=0.1
- **Rationale**: 小权重β_rep=0.1配合free bits替代依赖视觉复杂度的旧调参方案,使KL正则化强度可跨域固定
- **Search range**: 论文未提供搜索范围
- **Sensitivity**: 消融实验表明KL目标(含β_dyn和β_rep)对整体性能贡献最显著
- **Source**: Section World model learning, Table 4

## 自由位(free nats)
- **Value**: 1 nat(≈1.44 bits)
- **Rationale**: 对动态和表示KL损失设置下限,防止序列模型退化为平凡预测;当KL已满足时停止该梯度以专注重建损失
- **Search range**: 论文未提供搜索范围
- **Sensitivity**: 消融实验表明KL目标相关技术(含free bits)对性能贡献最显著
- **Source**: Section World model learning

## 想象时域(H)
- **Value**: 15
- **Rationale**: 行为者-评论家在世界模型想象轨迹上的展开步数
- **Search range**: 论文未提供搜索范围
- **Sensitivity**: 论文未单独消融
- **Source**: Table 4

## 折扣时域(1/(1-γ))
- **Value**: 333(对应γ≈0.997)
- **Rationale**: 高折扣因子使智能体重视长期回报;跨所有领域统一使用,与PPO基线保持一致以便对比
- **Search range**: 论文未提供搜索范围
- **Sensitivity**: 论文未单独消融
- **Source**: Table 4

## λ-回报系数(λ)
- **Value**: 0.95
- **Rationale**: λ-回报中平衡多步回报与自举估计偏差的折中系数
- **Search range**: 论文未提供搜索范围
- **Sensitivity**: 论文未单独消融
- **Source**: Table 4

## 评论家损失权重(β_val, β_repval)
- **Value**: β_val=1, β_repval=0.3
- **Rationale**: 在想象轨迹和重放轨迹上均训练评论家,改善奖励难以预测环境中的值估计质量
- **Search range**: 论文未提供搜索范围
- **Sensitivity**: 论文未单独消融
- **Source**: Section Critic learning, Table 4

## 评论家EMA衰减
- **Value**: 0.98
- **Rationale**: 将评论家向其参数的指数移动平均靠拢以稳定学习,类似目标网络但允许用当前网络计算回报
- **Search range**: 论文未提供搜索范围
- **Sensitivity**: 论文未单独消融
- **Source**: Section Critic learning, Table 4

## 行为者熵正则化系数(η)
- **Value**: 3×10^-4
- **Rationale**: 固定熵系数鼓励探索;需配合返回值归一化才能跨域稳定(不受奖励任意缩放影响)
- **Search range**: 论文未提供搜索范围
- **Sensitivity**: 论文强调若无返回值归一化则无法为此参数找到跨域稳定值
- **Source**: Section Actor learning, Table 4

## 返回值归一化(RetNorm)
- **Value**: S=EMA(Per(R,95)-Per(R,5), 0.99), 分母下限L=1
- **Rationale**: 用5th~95th百分位区间对离群值鲁棒;EMA衰减0.99平滑估计;分母下限L=1防止稀疏奖励时噪声被过度放大
- **Search range**: 论文未提供搜索范围
- **Sensitivity**: 消融实验表明返回值归一化对性能有显著贡献,尤其在稀疏奖励任务上
- **Source**: Section Actor learning, Table 4, 式(7)

## 训练策略限定
- **Value**: 无学习率退火,无优先重放,无权重衰减,无dropout
- **Rationale**: 简化超参数空间,实现跨域固定配置目标
- **Search range**: N/A
- **Sensitivity**: 论文将这些简化设计视为Dreamer鲁棒性的组成部分
- **Source**: Table 4 注脚
