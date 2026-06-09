## 编码器结构
- **Value**: 双流CNN编码器(静态相机 + 夹爪相机)
- **Rationale**: 分别处理两路RGB图像并融合本体感知状态,为RSSM提供多视角输入
- **Search range**: 论文未讨论替代方案
- **Sensitivity**: 未讨论
- **Source**: Sec III.A

## 编码器嵌入维度
- **Value**: e_t ∈ R^{1554}
- **Rationale**: 双流图像特征与本体感知状态融合后的总嵌入维度,作为逆向动力学头的输入
- **Search range**: 论文未讨论
- **Sensitivity**: 未讨论
- **Source**: Sec III.A

## RSSM随机潜变量规格
- **Value**: 离散分类变量 32×32
- **Rationale**: 沿用DreamerV2的离散分类潜变量设计,相比高斯潜变量训练更稳定
- **Search range**: 论文未讨论替代方案
- **Sensitivity**: 未讨论
- **Source**: Sec III.A

## 联合潜特征维度
- **Value**: f_t = [h_t; z_t] ∈ R^{2048}
- **Rationale**: 确定性隐状态与随机潜变量拼接,提供下游扩散策略所需的完整上下文
- **Search range**: 论文未讨论
- **Sensitivity**: 未讨论
- **Source**: Sec III.A

## 逆向动力学头结构
- **Value**: 三层MLP ψ,输入为 [e_t; e_{t+1}] 的拼接
- **Rationale**: 轻量MLP足以从相邻编码器嵌入预测动作;作用于e_t而非f_t以避免动作预测平凡化
- **Search range**: 论文未讨论替代结构
- **Sensitivity**: 未讨论
- **Source**: Sec III.A, Eq. 6

## 动作预测损失类型
- **Value**: L1回归损失
- **Rationale**: L1损失对动作空间中的离群值更鲁棒
- **Search range**: 论文未讨论替代方案
- **Sensitivity**: 未讨论
- **Source**: Sec IV.A

## 下游策略架构
- **Value**: DiffusionMLP
- **Rationale**: 与DiWA基线保持相同策略架构,排除架构差异对实验结论的干扰
- **Search range**: 论文未讨论替代方案
- **Sensitivity**: 低(与基线共享,差异仅来自特征质量)
- **Source**: Sec III.B, Table II

## 奖励分类器数量与指标
- **Value**: 8个二值分类器;所有分类器精度 ≥0.97,召回率 1.00
- **Rationale**: 为每个操作任务单独训练奖励分类器,在WAM潜空间中提供可靠的任务完成信号
- **Search range**: 论文未讨论
- **Sensitivity**: 高;分类器精度直接影响PPO优化的奖励信号质量
- **Source**: Sec III.B, Sec IV.B

## 每任务专家演示数量
- **Value**: 50 episodes/task
- **Rationale**: 有限专家数据场景,模拟真实低数据量情况
- **Search range**: 论文未讨论
- **Sensitivity**: 未讨论
- **Source**: Sec III.B
