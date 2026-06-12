论文未给出显式损失公式；训练期只定性描述为从 masking 预训练、统一生成、实时交互到持久记忆的逐步组件掌握，并未给出训练 objective 或 loss。推理期/运行期采用论文显式给出的组件形式：$$
\mathcal { G } = \underbrace { \left( \underbrace { p _ { \theta } ( z _ { t + 1 } \mid z _ { t } , a _ { t } ) } _ { \mathrm { D y n a m i c s } } , \underbrace { p _ { \theta } ( o _ { t } \mid z _ { t } ) } _ { \mathrm { O b s e r v a t i o n } } , \underbrace { p _ { \theta } ( r _ { t } \mid z _ { t } , a _ { t } ) } _ { \mathrm { R e w a r d } } , \underbrace { p _ { \theta } ( \gamma _ { t } \mid z _ { t } , a _ { t } ) } _ { \mathrm { D i s c o u n t / T e r m i n a t i o n } } \right) } _ { \mathrm { D i s c o u n t } }
$$
$$
\begin{array} { r l r l } { \mathcal { F } : } & { \underbrace { q _ { \phi } ( z _ { t } \mid h _ { t - 1 } , o _ { t } ) } _ { \mathrm { S t a t e ~ I n f e r e n c e } } , } & & { \mathcal { C } = \Big ( \underbrace { \pi _ { \eta } ( a _ { t } \mid z _ { t } , h _ { t } ) } _ { \mathrm { P o l i c y } } , \underbrace { v _ { \omega } ( z _ { t } , h _ { t } ) } _ { \mathrm { V a l u e } } \Big ) } \end{array}
$$
$$
\begin{array} { r } { \begin{array} { r l } { \mathcal { M } : } & { { } \underbrace { h _ { t } = f _ { \psi } \left( h _ { t - 1 } , { z _ { t } } , a _ { t - 1 } \right) } _ { \mathrm { M e m o r y } \mathrm { U p d a t e } } } \end{array} } \end{array}
$$
