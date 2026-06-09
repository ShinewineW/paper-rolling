# Heuristics

## H1: Free bits: 将动力学损失 L_dyn 和表示损失 L_rep 在 1 nat 处截断，当 KL 已充分最小化时停止进一步优化
- **Rationale**: 防止序列模型退化为平凡解(KL=0 但表示不含信息)；同时消除深度 VAE 常见的 KL 训练尖刺
- **Sensitivity**: 关键；消融实验中去掉 KL 目标(含 free bits)是对 Dreamer 整体性能影响最大的单项
- **Bounds**: 截断阈值固定为 1 nat
- **Code ref**: [loss_dyn, loss_rep]
- **Source**: 公式 (3); Table 4 free_nats=1; 正文第 88 行

## H2: 表示损失权重 β_rep=0.1，重建损失和动力学损失权重各为 1
- **Rationale**: 较小 β_rep 使模型在 3D 复杂场景保留细粒度感知细节，同时为简单场景提供适度正则化，实现跨域固定超参数
- **Sensitivity**: 较高；过大导致 3D 环境细节丢失，过小使动力学难以预测
- **Bounds**: β_pred=1, β_dyn=1, β_rep=0.1
- **Code ref**: [world_model_loss]
- **Source**: 公式 (2); 正文第 82-94 行

## H3: 百分位回报归一化: 用 EMA(Per(R^λ,95)-Per(R^λ,5)) 作为 Actor 梯度归一化尺度，分母下限 L=1，EMA 衰减系数 0.99
- **Rationale**: 稀疏奖励下标准差趋近零会放大噪声；百分位方法对离群值鲁棒；L=1 防止小回报被过度放大导致探索停滞
- **Sensitivity**: 关键；去除后在稀疏奖励域探索停滞
- **Bounds**: 百分位区间 [5, 95]; EMA decay=0.99; 下限 L=1; 熵系数 η=3×10^-4
- **Code ref**: [RetNorm, return_normalization]
- **Source**: 公式 (6)(7); 正文第 120-132 行

## H4: Unimix: 所有 categorical 分布(编码器、动力学预测器、Actor)为 99% 网络 softmax 输出与 1% 均匀分布的混合
- **Rationale**: 防止分布变为确定性使 KL 散度无界，保证对数概率有界，消除训练中偶发的 KL 尖刺
- **Sensitivity**: 低；主要防止极端退化情况
- **Bounds**: 混合比例: 1% 均匀 + 99% 网络输出，全部 categorical 分布统一适用
- **Code ref**: [unimix]
- **Source**: Table 4 latent_unimix=1%; 正文第 96-97 行

## H5: Symlog 变换族: 向量观测以 symlog 变换后输入/重建; 奖励预测器和 Critic 使用 symexp 指数间隔 bin 配合 twohot 损失
- **Rationale**: 不同域奖励和观测量级差异达多个数量级; symlog 压缩大值但不截断且保留符号; twohot 使梯度尺度与预测目标量级完全解耦
- **Sensitivity**: 关键；去掉后大量级目标(如部分 Atari 分数)导致损失发散
- **Bounds**: symlog(x)=sign(x)ln(|x|+1); bins B=symexp([-20,...,+20]), 共 41 个指数间隔 bin
- **Code ref**: [symlog, symexp, twohot]
- **Source**: 公式 (8)(9)(10)(11)

## H6: 奖励预测器和 Critic 的输出权重矩阵初始化为零
- **Rationale**: 随机初始化时两者在训练初期产生大量级虚假奖励/价值预测，延迟有效学习的启动
- **Sensitivity**: 中等；主要影响早期学习速度
- **Bounds**: 仅适用于奖励预测器和 Critic 输出层线性权重矩阵
- **Code ref**: [reward_predictor, critic]
- **Source**: 正文第 114 行

## H7: Critic EMA 正则化: 以 Critic 自身参数的指数移动平均为软目标进行正则化，EMA decay=0.98
- **Rationale**: Critic 自举训练中目标依赖自身预测; EMA 正则类似软目标网络起稳定作用，同时允许使用当前网络直接计算回报估计
- **Sensitivity**: 中等
- **Bounds**: EMA decay=0.98
- **Code ref**: [critic_ema]
- **Source**: Table 4 Critic EMA decay 0.98; 正文第 114 行
