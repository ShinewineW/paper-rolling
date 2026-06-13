# Concepts

## Diffusion Forcing
- **Notation**: $( \mathbf { x } _ { t } ^ { k _ { t } } ) _ { 1 \leq t \leq T }$；其中 $k _ { t }$ 表示时间步 $t$ 的噪声水平。
- **Definition**: Diffusion Forcing 是一种训练与采样框架，用于处理任意序列长度的带噪 token；核心约束是每个 token 的噪声水平可以随时间步独立变化。<!--ref:Diffusion Forcing (DF) is a framework for training and sampling arbitrary sequence lengths of noisy tokens-->
- **Boundary conditions**: 本文主要在 time series data 语境下实例化该框架；关于 transformer implementation，论文说明放到 Appendix B.1 讨论，而正文最小实现聚焦 vanilla Recurrent Neural Network。<!--ref:we focus on time series data-->
- **Related concepts**: ['Causal Diffusion Forcing', '逐 token 噪声水平', '噪声作为部分遮蔽', '采样调度矩阵']

## Causal Diffusion Forcing
- **Notation**: $\mathbf { x } _ { t } ^ { k _ { t } }$ depends only on past noisy tokens；潜变量更新写作 $\mathbf { z } _ { t } \sim p _ { \theta } ( \mathbf { z } _ { t } | \mathbf { z } _ { t - 1 } , \mathbf { x } _ { t } ^ { k _ { t } } , k _ { t } )$。
- **Definition**: Causal Diffusion Forcing 是 Diffusion Forcing 在因果架构上的实例化，其中当前 noisy token 只依赖过去 noisy tokens。<!--ref:instantiate Diffusion Forcing with causal architectures-->
- **Boundary conditions**: CDF 的因果性不等于传统 teacher forcing；训练时仍然对序列中所有 token 去噪，只是架构上的依赖方向限定为过去到未来。<!--ref:We train the model to denoise all tokens of a sequence at once-->
- **Related concepts**: ['Diffusion Forcing', 'Bayesian filtering', 'RNN latent state', '长程 guidance']

## 噪声作为部分遮蔽
- **Notation**: $\mathbf { x } _ { t } ^ { 0 }$ 表示未加噪 token；$\mathbf { x } _ { t } ^ { K }$ 表示 white noise $\mathcal { N } ( 0 , \bf { I } )$。
- **Definition**: 论文把扩散加噪解释为一种 partial masking：零噪声对应 token 未被遮蔽，完全噪声对应 token 被完全遮蔽。<!--ref:noising tokens is a form of partial masking-->
- **Boundary conditions**: 该概念是训练范式的解释框架，不应被理解为论文引入了一个额外的离散 mask token；原文用 forward diffusion 的噪声水平表达遮蔽程度。<!--ref:degree of partial masking applied to each token through noising-->
- **Related concepts**: ['masking along the time axis', 'masking along the noise axis', '逐 token 噪声水平', 'subsequence modeling']

## 独立逐 token 噪声水平
- **Notation**: $k _ { 1 : T }$ uniformly from $[ K ] ^ { T }$。
- **Definition**: 训练时每个时间步的噪声水平 $k _ { t }$ 独立采样；这使模型见到同一序列内不同 token 处在不同噪声水平的组合。<!--ref:Sample independent noise level k_t-->
- **Boundary conditions**: 这里的独立性指噪声水平采样方式；它不表示 token 内容在数据分布中相互独立，也不取消 CDF 架构中的因果依赖。<!--ref:future tokens depend on past ones via a causal architecture-->
- **Related concepts**: ['Diffusion Forcing', '训练目标', 'all sequences of noise levels', '任意子序列建模']

## 训练目标
- **Notation**: $$\underset { \substack { k _ { t } , \mathbf { x } _ { t } , \epsilon _ { t } } } { \mathbb { E } } \sum _ { \substack { k _ { t } \sim p _ { \theta } ( \mathbf { z } _ { t } | \mathbf { z } _ { t - 1 } , \mathbf { x } _ { t } ^ { k _ { t } } , k _ { t } ) } } ^ { T } \bigg [ \| \epsilon _ { t } - \epsilon _ { \theta } \big ( \mathbf { z } _ { t - 1 } , \mathbf { x } _ { t } ^ { k _ { t } } , k _ { t } \big ) \| ^ { 2 } \bigg ] ,\tag{3.1}$$
- **Definition**: CDF 将一个 RNN unit 参数化为噪声预测器，使用常规 diffusion training objective 对每个 token 的噪声进行预测。<!--ref:parameterize the aforementioned unit in terms of noise prediction-->
- **Boundary conditions**: 公式仅对应论文显式给出的训练目标；采样期 guidance 或调度策略不应被并入该训练目标。<!--ref:During sampling-->
- **Related concepts**: ['Causal Diffusion Forcing', 'noise prediction', 'ELBO', 'Bayesian filtering']

## all sequences of noise levels
- **Notation**: $k _ { 1 : T } \sim [ K ] ^ { T }$；特殊情形包含 $k _ { t } = 0$ 或 $k _ { t } = K$。
- **Definition**: Theorem 3.1 的非正式表述称，Diffusion Forcing 训练过程在适当条件下同时最大化所有噪声水平序列的 likelihood lower bound。<!--ref:all sequences of noise levels-->
- **Boundary conditions**: 该结论依赖论文所说的 appropriate conditions；在概念抽取中不能把它扩展成对任意未见数据分布的无条件保证。<!--ref:under appropriate conditions-->
- **Related concepts**: ['ELBO', '任意子序列建模', '逐 token 噪声水平', 'partial masking']

## 采样调度矩阵
- **Notation**: $\breve { \kappa } \in [ \breve { K } ] ^ { M \times T }$；$\mathcal { K } _ { m , t }$ 表示 row $m$ 中 time-step $t$ token 的 desired noise level。
- **Definition**: Diffusion Forcing 采样由一个二维调度矩阵规定，每一列对应时间步，每一行给出该轮采样中每个 token 的目标噪声水平。<!--ref:prescribing a noise schedule on a 2D M x T grid-->
- **Boundary conditions**: 调度矩阵是推理期机制；它指定去噪路径，不改变训练数据，也不等同于模型参数的一部分。<!--ref:During sampling-->
- **Related concepts**: ['zig-zag schedule', 'pyramid scheduling', 'future uncertainty', 'long-horizon guidance']

## Monte Carlo Guidance
- **Notation**: 对 $\mathbf { x } _ { t } ^ { k }$ 的 guidance 来自 future $\mathbf x _ { t + 1 : T }$ 的分布。
- **Definition**: Monte Carlo Guidance 指在对某个 token 施加 guidance 时，不只使用单条未来轨迹，而是抽取多个未来样本并平均它们的 guidance gradients。<!--ref:draw multiple samples of the future and average their guidance gradients-->
- **Boundary conditions**: MCG 是采样与规划阶段的 guidance 机制，不是训练损失公式的一部分；它依赖 CDF 能够在当前 token 生成时保留未来不确定性。<!--ref:The effect of MCG is enhanced when combined with sampling schedules that keep the noise level of future tokens high-->
- **Related concepts**: ['Causal Diffusion Forcing', 'future uncertainty', 'long-horizon guidance', 'sequential decision making']

## 长程 guidance
- **Notation**: Algorithm 2 的 Line 10 对 $\mathbf { x } _ { 1 : T }$ 使用 AddGuidance；奖励可写作 $\sum _ { t = 1 } ^ { T } \mathbf { r } _ { t }$ 或 $\sum _ { t ^ { \prime } = t } ^ { t + H } \mathbf { r } _ { t }$。
- **Definition**: 长程 guidance 是指在部分扩散轨迹上加入 guidance，使未来 token 的梯度能沿因果依赖向过去传播，从而影响较早 token 的采样。<!--ref:guidance gradients from future tokens can propagate backwards in time-->
- **Boundary conditions**: 论文将该能力与 per-time step policies 区分开；后者不能利用稀疏的长 horizon guidance。<!--ref:Per-time step policies cannot take advantage of this latter, longer horizon guidance-->
- **Related concepts**: ['采样调度矩阵', 'Monte Carlo Guidance', 'sequential decision making', 'causality']
