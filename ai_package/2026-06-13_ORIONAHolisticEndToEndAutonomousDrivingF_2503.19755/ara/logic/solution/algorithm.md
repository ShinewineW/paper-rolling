论文显式给出如下 latent distribution 与训练目标公式。QT-Former 历史检索与写入：$$
\begin{array} { l } { { Q _ { h } = { \bf C A } ( Q _ { h } , M + P _ { t } , M + P _ { t } ) , } } \\ { { \hat { Q } _ { h } = { \bf C A } ( Q _ { h } , Q _ { s } , Q _ { s } ) , } } \end{array}\tag{1}
$$ $$
M = [ \hat { Q } _ { h } ^ { t - n } , \cdot \cdot \cdot , \hat { Q } _ { h } ^ { t - 1 } , \hat { Q } _ { h } ^ { t } ] ,\tag{2}
$$ LLM 的 planning token 建模：$$
s \sim p ( s | x _ { s } , x _ { h } , x _ { q } , x _ { a } ) ,\tag{3}
$$ generative planner 将 state s 与 ground-truth trajectory t 投影到 Gaussian latent variables：$$
p ( z _ { s } | s ) \sim N ( \mu _ { s } , \sigma _ { s } ^ { 2 } ) , p ( z _ { t } | t ) \sim N ( \mu _ { t } , \sigma _ { t } ^ { 2 } ) ,\tag{4}
$$ 并用 KL divergence 做分布匹配：$$
\begin{array} { r } { \mathcal { L } _ { v a e } = D _ { K L } ( p ( \mathbf { z } | \mathbf { s } ) , p ( \mathbf { z } | \mathbf { t } ) ) . } \end{array}\tag{5}
$$ QT-Former、generative planner 与 ORION 总损失为：$$
\mathcal { L } _ { q t } = \mathcal { L } _ { d e t } + \mathcal { L } _ { t r a } + \mathcal { L } _ { m } .\tag{6}
$$ $$
\mathcal { L } _ { g p } = \mathcal { L } _ { v a e } + \mathcal { L } _ { m s e } + \mathcal { L } _ { c o l } + \mathcal { L } _ { b d } .\tag{7}
$$ $$
\mathcal { L } = \mathcal { L } _ { q t } + \mathcal { L } _ { c e } + \mathcal { L } _ { g p } .\tag{8}
$$ 其中 \mathcal { L } _ { c e } 是 LLM 的 auto-regressive crossentropy loss；\mathcal { L } _ { v a e } 用于对齐 reasoning space 与 action space；\mathcal { L } _ { m s e }、\mathcal { L } _ { c o l }、\mathcal { L } _ { b d } 用于 planning prediction。
