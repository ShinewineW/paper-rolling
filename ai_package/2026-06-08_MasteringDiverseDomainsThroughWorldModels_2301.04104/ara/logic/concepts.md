# Concepts

## 循环状态空间模型(RSSM)
- **Notation**: $h_t = f_\phi(h_{t-1}, z_{t-1}, a_{t-1})$;$z_t \sim q_\phi(z_t \mid h_t, x_t)$;$\hat{z}_t \sim p_\phi(\hat{z}_t \mid h_t)$
- **Definition**: 一种同时包含确定性循环状态和随机隐变量的世界模型架构。序列模型维护循环状态 $h_t$,编码器将感知输入 $x_t$ 映射到随机表征 $z_t$,动态预测器在不访问真实输入的情况下预测下一时刻的表征,从而支持在想象空间中展开轨迹。
- **Boundary conditions**: RSSM 是 DreamerV3 的核心世界模型结构,继承自 DreamerV1/V2;此处特指论文所用变体:使用向量 softmax 离散分布、直通梯度,以及块对角 GRU 序列模型,不泛指所有 RSSM 变体。
- **Related concepts**: ['世界模型损失函数', '离散表征与直通梯度', '想象训练']

## symlog/symexp 变换
- **Notation**: $\operatorname{symlog}(x) \doteq \operatorname{sign}(x) \ln(|x|+1)$;$\operatorname{symexp}(x) \doteq \operatorname{sign}(x)(\exp(|x|)-1)$
- **Definition**: 一对双对称对数变换及其逆变换,用于压缩任意量级的正负数目标。symlog 将输入映射为保号的对数压缩值,symexp 为其逆函数。两者合称为 symlog 变换族,用于编码器输入、解码器目标以及奖励/回报的预测损失。
- **Boundary conditions**: 仅适用于目标压缩场景;与标准对数变换的区别在于支持负数输入;论文中 symlog 用于向量观测的编码器输入与解码器目标,symexp twohot 损失用于奖励预测器和评论家。
- **Related concepts**: ['symexp twohot 损失', '鲁棒预测', '回报归一化']

## symexp twohot 损失
- **Notation**: $\hat{y} \doteq \operatorname{softmax}(f(x))^T B$;$B \doteq \operatorname{symexp}([-20 \ldots +20])$;$\mathcal{L}(\theta) \doteq -\operatorname{twohot}(y)^T \log \operatorname{softmax}(f(x,\theta))$
- **Definition**: 一种针对随机连续目标的分布式回归损失。网络输出指数间隔分仓上的 softmax 分布,预测值为各仓位置的加权均值;训练目标通过 twohot 编码将连续标量映射为相邻两仓上和为 1 的软标签,然后最小化分类交叉熵。
- **Boundary conditions**: 论文仅将该损失用于奖励预测器和评论家网络;分仓范围固定为 symexp([-20, +20]);仅适用于需要预测随机连续目标的场景,不适用于确定性重建损失(后者使用 symlog 平方误差)。
- **Related concepts**: ['symlog/symexp 变换', '评论家学习', '鲁棒预测']

## 回报百分位归一化
- **Notation**: $S \doteq \operatorname{EMA}(\operatorname{Per}(R_t^\lambda, 95) - \operatorname{Per}(R_t^\lambda, 5),\ 0.99)$;演员损失中除以 $\max(1, S)$
- **Definition**: 演员学习中用于稳定熵正则化权重的回报标准化方法。以第 5 至第 95 百分位回报之差作为尺度估计,并通过指数移动平均平滑,再对回报进行归一化后计算策略梯度,同时设置下界 $L=1$ 防止稀疏奖励下放大噪声。
- **Boundary conditions**: 归一化仅作用于演员的策略梯度估计,不改变评论家的训练目标;百分位范围固定为 5%-95%;仅在 DreamerV3 演员学习中使用。
- **Related concepts**: ['演员学习', 'symexp twohot 损失', '回报估计']

## 自由比特(Free Bits)
- **Notation**: $\mathcal{L}_{\mathrm{dyn}}(\phi) \doteq \max(1,\ \mathrm{KL}[\operatorname{sg}(q_\phi(z_t|h_t,x_t)) \| p_\phi(z_t|h_t)])$;$\mathcal{L}_{\mathrm{rep}}(\phi) \doteq \max(1,\ \mathrm{KL}[q_\phi(z_t|h_t,x_t) \| \operatorname{sg}(p_\phi(z_t|h_t))])$
- **Definition**: 对世界模型 KL 损失的下界截断技术。将动态损失和表征损失分别截断到不低于 1 nat(约 1.44 bits),当 KL 已经足够小时停止对该项的优化,从而专注于重建损失以防止退化解。
- **Boundary conditions**: 自由比特阈值固定为 1 nat;分别应用于动态损失和表征损失两项;与 DreamerV1 中动态/表征损失权重需随环境视觉复杂度调整的做法形成对比。
- **Related concepts**: ['世界模型损失函数', 'RSSM', '表征学习']

## 想象训练(Imagination Training)
- **Notation**: 从模型状态 $s_t = \{h_t, z_t\}$ 出发;想象视野 $H=15$;折扣因子 $\gamma=0.997$;$\lambda$-回报 $R_t^\lambda \doteq r_t + \gamma c_t((1-\lambda)v_t + \lambda R_{t+1}^\lambda)$
- **Definition**: 演员-评论家完全在世界模型预测的抽象轨迹中学习行为的训练范式。从重放缓冲区中的真实状态出发,通过世界模型的开环预测展开长度为 $T$ 的想象轨迹,演员和评论家在这些虚拟轨迹上进行梯度更新,不与真实环境交互。
- **Boundary conditions**: 想象视野固定为 $H=15$ 步;演员选择动作时不进行前向搜索(lookahead planning),仅从策略网络直接采样;与 MuZero 等基于树搜索的模型不同。
- **Related concepts**: ['RSSM', '评论家学习', '演员学习']

## 1% Unimix 均匀混合
- **Notation**: 混合分布 = 99% 神经网络 softmax 输出 + 1% 均匀分布
- **Definition**: 对编码器、动态预测器和演员的类别分布进行正则化的技术:将网络输出的 softmax 分布与 1% 的均匀分布进行混合,确保任意类别的概率不为零,防止 KL 散度出现无穷大。
- **Boundary conditions**: 混合比例固定为 1%;仅用于类别分布,不适用于连续分布;编码器、动态预测器、演员三处统一使用此技术。
- **Related concepts**: ['RSSM', '自由比特', '演员学习']
