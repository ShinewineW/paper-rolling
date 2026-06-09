# Heuristics

## H1: 逆动力学动作损失权重 λ_act = 1000.0,远大于 λ_KL = 3.0 与 λ_img = 1.0
- **Rationale**: 动作预测的绝对误差量级远小于像素重建损失,需高权重才能让动作梯度有效正则化编码器表示
- **Sensitivity**: high
- **Bounds**: 论文使用 λ_act = 1000.0;论文指出需「carefully tune」以平衡重建质量与动作预测
- **Code ref**: [N/A(论文未提供实现代码)]
- **Source**: §III.A.2 Training Objective; §IV.A.2 Training Settings

## H2: KL 均衡系数 α = 0.8
- **Rationale**: 控制先验与后验在 KL 损失中各自的梯度权重比例,使先验在想象展开时输出更稳定的潜在状态
- **Sensitivity**: medium
- **Bounds**: α = 0.8(来自 DreamerV2 设置,论文未做消融)
- **Code ref**: [N/A(论文未提供实现代码)]
- **Source**: §IV.A.2 Training Settings

## H3: 逆动力学头 ψ 作用于编码器嵌入 e_t,而非 RSSM 组合特征 f_t
- **Rationale**: f_t 通过 GRU 已接收上一步动作 a_{t-1} 作为输入,若在 f_t 上预测 a_t 则问题平凡可解,无法产生真正的编码器正则化,级联效果将失效
- **Sensitivity**: high
- **Bounds**: 必须使用 e_t;改用 f_t 会使动作预测退化为直接查表
- **Code ref**: [N/A(论文未提供实现代码)]
- **Source**: §III.A.2 Action-Regularized World Model

## H4: WAM 训练约 230K 梯度步,基线 DreamingV2 需 2M 步,约为 8.7× 更少
- **Rationale**: 逆动力学正则化加速表示收敛,无需完整训练步数即可达到更优的下游策略性能
- **Sensitivity**: medium
- **Bounds**: ∼230K 步;论文未报告更多步数对下游性能的边际收益
- **Code ref**: [N/A(论文未提供实现代码)]
- **Source**: §IV.A.2 Training Settings

## H5: PPO 微调期间扩散策略去噪步数降至 K=10(BC 预训练期为 K=20),并加入 BC 正则化系数 α_BC = 0.025
- **Rationale**: 减少去噪步数以降低想象展开的计算开销;BC 正则化系数锚定原始行为分布,防止在潜在空间 RL 微调中发生灾难性遗忘
- **Sensitivity**: medium
- **Bounds**: K=10(PPO 期)、K=20(BC 期);α_BC = 0.025
- **Code ref**: [N/A(论文未提供实现代码)]
- **Source**: §III.B Offline Policy Fine-tuning; §IV.B.3 Online Policy Fine-tuning Settings

## H6: 每次 PPO 迭代生成 50 条并行想象展开,PPO 每轮执行 10 个更新 epoch
- **Rationale**: 50 条展开提供足够的策略梯度估计以稳定 PPO 更新,同时维持合理计算开销
- **Sensitivity**: low
- **Bounds**: 50 条展开/迭代;共 800 次迭代,每 25 次评估一次
- **Code ref**: [N/A(论文未提供实现代码)]
- **Source**: §III.B Offline Policy Fine-tuning; §IV.B.3 Online Policy Fine-tuning Settings
