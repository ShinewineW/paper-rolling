训练期目标显式包括 Diffusion Forcing 与 Self Forcing DMD；推理期的 local-window attention、streaming KV cache、CUDA Graphs、LightTAE、pixel shuffle、multi-GPU context parallelism 和 pre-fetch chunk 语义是 serving/集成优化，不写入训练目标。论文还在 causal masking 中给出自回归分解与 block-autoregressive 分解，但它们不是 $$...$$ 形式的损失公式。显式损失公式如下：
$$
\begin{array} { r } { { \bf L } _ { D F } = \mathbb { E } _ { { \bf x } ^ { 1 : T } , \epsilon } \left[ \| { \bf u } \theta ( \mathrm { x } _ { \mathrm { t } } ^ { 1 : T } , \mathrm { t } ) - \mathrm { v } _ { \mathrm { t } } \| ^ { 2 } \right] . } \end{array}\tag{1}
$$
$$
\begin{array} { r } { \mathcal { L } _ { \mathrm { D M D } } ( \theta ) = \mathbb { E } \left[ \frac { 1 } { 2 } \left| \left| \hat { x } - \mathrm { s g } \left[ \hat { x } - \left( \mathbf { f } _ { \psi } ( \hat { x } _ { t } , t ) - \mathbf { f } _ { \phi } ( \hat { x } _ { t } , t ) \right) \right] \right| \right| ^ { 2 } \right] , } \end{array}\tag{2}
$$
定性地说，Diffusion Forcing 用 causal masking 让每个 latent token 在独立噪声时间下学习基于过去帧的 velocity prediction；Self Forcing 在训练中用模型自己的 self-rollout 替代干净上下文，并通过 DMD 的 full-sequence distribution matching 缓解 exposure bias 与长 rollout 累积误差。
