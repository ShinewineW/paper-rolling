训练期的扩散目标由论文显式给出为：
$$
\begin{array} { r } { \mathcal L ( \boldsymbol { \theta } ) = \mathbb { E } \left[ \| \mathbf { D } _ { \boldsymbol { \theta } } ( \mathbf { x } _ { t + 1 } ^ { \tau } , \tau , \mathbf { x } _ { \leq t } ^ { 0 } , a _ { \leq t } ) - \mathbf { x } _ { t + 1 } ^ { 0 } \| ^ { 2 } \right] . } \end{array}\tag{5}
$$
EDM 预条件化的去噪器参数化为：
$$
\begin{array} { r } { \mathbf { D } _ { \theta } ( \mathbf { x } _ { t + 1 } ^ { \tau } , y _ { t } ^ { \tau } ) = c _ { \mathrm { s k i p } } ^ { \tau } \mathbf { x } _ { t + 1 } ^ { \tau } + c _ { \mathrm { o u t } } ^ { \tau } \mathbf { F } _ { \theta } \big ( c _ { \mathrm { i n } } ^ { \tau } \mathbf { x } _ { t + 1 } ^ { \tau } , y _ { t } ^ { \tau } \big ) , } \end{array}\tag{6}
$$
对应的 F_theta 训练目标为：
$$
\begin{array} { r } { \mathcal L ( \theta ) = \mathbb E \Big [ | | \underbrace { \mathbf F _ { \theta } \big ( c _ { \mathrm { i n } } ^ { \tau } \mathbf x _ { t + 1 } ^ { \tau } , y _ { t } ^ { \tau } \big ) } _ { \mathrm { N e t w o r k ~ p r e d i c t i o n } } - \underbrace { \frac 1 { c _ { \mathrm { o u t } } ^ { \tau } } \big ( \mathbf x _ { t + 1 } ^ { 0 } - c _ { \mathrm { s k i p } } ^ { \tau } \mathbf x _ { t + 1 } ^ { \tau } \big ) } _ { \mathrm { N e t w o r k ~ t r a i n i n g ~ t a r g e t } } | | ^ { 2 } \Big ] . } \end{array}\tag{7}
$$
预条件器与噪声采样为：
$$
c _ { i n } ^ { \tau } = \frac { 1 } { \sqrt { \sigma ( \tau ) ^ { 2 } + \sigma _ { d a t a } ^ { 2 } } }\tag{9}
$$
$$
c _ { o u t } ^ { \tau } = \frac { \sigma ( \tau ) \sigma _ { d a t a } } { \sqrt { \sigma ( \tau ) ^ { 2 } + \sigma _ { d a t a } ^ { 2 } } }\tag{10}
$$
$$
c _ { n o i s e } ^ { \tau } = \frac { 1 } { 4 } \log ( \sigma ( \tau ) )\tag{11}
$$
$$
c _ { s k i p } ^ { \tau } = \frac { \sigma _ { d a t a } ^ { 2 } } { \sigma _ { d a t a } ^ { 2 } + \sigma ^ { 2 } ( \tau ) } ,\tag{12}
$$
$$
\log ( \sigma ( \tau ) ) \sim \mathcal { N } ( P _ { m e a n } , P _ { s t d } ^ { 2 } ) ,\tag{13}
$$
推理期不把这些采样权重写入训练目标，而是对下一观测从 prior noise 出发迭代求解 reverse SDE；论文主实验采用 Euler sampling。策略训练期的显式目标还包括 λ-return、value loss 与 policy loss：
$$
\boldsymbol { \Lambda } _ { t } = \left\{ \begin{array} { l l l } { r _ { t } + \gamma ( 1 - d _ { t } ) \Big [ ( 1 - \lambda ) V _ { \phi } ( \mathbf { x } _ { t + 1 } ) + \lambda \boldsymbol { \Lambda } _ { t + 1 } \Big ] } & { \mathrm { i f } } & { t < H } \\ { V _ { \phi } ( \mathbf { x } _ { H } ) } & { \mathrm { i f } } & { t = H . } \end{array} \right.\tag{14}
$$
$$
\mathcal { L } _ { V } ( \phi ) = \mathbb { E } _ { \pi _ { \phi } } \left[ \sum _ { t = 0 } ^ { H - 1 } \left( V _ { \phi } ( \mathbf { x } _ { t } ) - \mathrm { s g } ( \Lambda _ { t } ) \right) ^ { 2 } \right] ,\tag{15}
$$
$$
\mathcal { L } _ { \pi } ( \phi ) = - \mathbb { E } _ { \pi _ { \phi } } \left[ \sum _ { t = 0 } ^ { H - 1 } \log \left( \pi _ { \phi } \left( a _ { t } \mid \mathbf { x } _ { \le t } \right) \right) \mathrm { s g } \left( \Lambda _ { t } - V _ { \phi } \left( \mathbf { x } _ { t } \right) \right) + \eta \mathcal { H } \left( \pi _ { \phi } \left( a _ { t } \mid \mathbf { x } _ { \le t } \right) \right) \right] .\tag{16}
$$
