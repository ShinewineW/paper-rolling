训练期目标严格来自论文显式公式。视觉预训练采用自回归 next-token 预测：$$
P ( Q _ { t + 1 } ^ { k } ) = \prod _ { i = 1 } ^ { N } P _ { \theta } ( q _ { i } ^ { k } \mid q _ { < i } ^ { k } , h _ { t } , L ) ,\tag{5}
$$。RL 阶段先用规则奖励组合得到总奖励：$$
\begin{array} { r } { R _ { \mathrm { a l l } } = \lambda _ { \mathrm { f m t } } { \cdot } R _ { \mathrm { f m t } } { + } \lambda _ { \mathrm { p r e d } } { \cdot } R _ { \mathrm { p r e d } } { + } \lambda _ { \mathrm { v i s } } { \cdot } R _ { \mathrm { v i s } } { + } \lambda _ { \mathrm { a c t } } { \cdot } R _ { \mathrm { a c t } } { + } \lambda _ { \mathrm { t r a j } } { \cdot } R _ { \mathrm { t r a j } } } \\ { ( 6 ) } \end{array}\tag{6}
$$。GRPO 组内优势为：$$
A _ { i } = \frac { r _ { i } - \mu } { \sigma } , \quad \mu = \frac { 1 } { G } \sum _ { j } r _ { j } , \sigma = \mathrm { s t d } ( r _ { 1 } , \dots , r _ { G } )\tag{7}
$$。策略更新最大化代理目标：$$
\begin{array} { l } { \displaystyle { J ( \theta ) = \mathbb { E } \left[ \frac { 1 } { G } \sum _ { i = 1 } ^ { G } \operatorname* { m i n } \left( \frac { \pi _ { \theta } ( \tau _ { i } \mid o ) } { \pi _ { \theta _ { \mathrm { o l d } } } ( \tau _ { i } \mid o ) } A _ { i } , \mathrm { c l i p } \right) \right] } } \\ { \displaystyle { - \beta D _ { \mathrm { K L } } \big ( \pi _ { \theta } , \pi _ { \mathrm { o l d } } \big ) . } } \end{array}\tag{8}
$$。补充理论把完整 token 序列 u 的 GRPO 训练目标写为：$$
\mathcal { T } _ { \mathrm { G R P O } } ( \omega ) = \mathbb { E } _ { u \sim \pi _ { \omega } } \left[ \log \pi _ { \omega } ( u \mid o , g ) \cdot A ( u ) \right]\tag{19}
$$。推理期的短期预测、未来帧生成与反思修正是执行流程，不应写入视觉预训练损失；论文中的 reward 加权项只属于 RL 阶段，不能作为 SFT 或视觉预训练目标。
