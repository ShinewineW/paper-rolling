训练期目标为视觉 token 生成与轨迹回归的联合监督，论文显式给出的训练损失如下：
$$
\omega ( d _ { t + k } ^ { i } , d _ { t + k - 1 } ^ { i } ) = \alpha \mathbb { I } ( d _ { t + k } ^ { i } \neq d _ { t + k - 1 } ^ { i } ) + \beta \mathbb { I } ( d _ { t + k } ^ { i } = d _ { t + k - 1 } ^ { i } ) , \quad \alpha > \beta\tag{5}
$$
$$
\mathcal { L } _ { \mathrm { d y n } } = - \frac { 1 } { N } \sum _ { k = 1 } ^ { N } \sum _ { i = 1 } ^ { L } \omega ( d _ { t + k } ^ { i } , d _ { t + k - 1 } ^ { i } ) \log p _ { \theta } ( d _ { t + k } ^ { i } \mid \hat { d } _ { < t + k } ^ { i } , \hat { a } _ { < t + k } ^ { i } ) ,\tag{6}
$$
$$
\mathcal { L } _ { \mathrm { t r a j } } = \frac { 1 } { N } \sum _ { k = 1 } ^ { N } \left. \hat { a } _ { t + k } - a _ { t + k } \right. _ { 1 } .\tag{7}
$$
$$
\begin{array} { r } { \mathcal { L } = \lambda _ { 1 } \mathcal { L } _ { \mathrm { d y n } } + \lambda _ { 2 } \mathcal { L } _ { \mathrm { t r a j } } , } \end{array}\tag{8}
$$
推理期不是额外训练目标，而是逐步自回归交替生成未来视觉 token 与动作 token，并复用 KV-cache；论文显式给出的生成关系如下：
$$
\hat { d } _ { t + k } \sim p _ { \theta } ( d _ { t + k } \mid \hat { d } _ { \leq t + k - 1 } , \hat { a } _ { \leq t + k - 1 } ) ,\tag{2}
$$
$$
\hat { a } _ { t + k } \sim p _ { \theta } ( a _ { t + k } \mid \hat { d } _ { \leq t + k } , \hat { a } _ { \leq t + k - 1 } ) ,\tag{3}
$$
