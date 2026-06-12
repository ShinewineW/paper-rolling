训练期目标只采用论文显式给出的 tokenizer reconstruction、dynamics shortcut forcing、ramp loss weight、behavior cloning 与 reward model、value TD-learning、PMPO policy loss；推理期的 autoregressive sampling、past context corruption、prompt sequence 不属于训练目标。

$$
\mathcal { L } ( \theta ) = \mathcal { L } _ { \mathrm { M S E } } ( \theta ) + 0 . 2 \mathcal { L } _ { \mathrm { L P I P S } } ( \theta )\tag{5}
$$

$$
\begin{array} { r l } { z _ { 0 } \sim \mathrm { N } ( 0 , 1 ) \qquad z _ { 1 } \sim \mathcal { D } } & { { } \tau , d \sim p ( \tau , d ) \qquad \tau , d \in [ 0 , 1 ] ^ { T } } \\ { \hat { z } _ { 1 } = f _ { \theta } ( \tilde { z } , \tau , d , a ) } & { { } \tilde { z } = \left( 1 - \tau \right) z _ { 0 } + \tau z _ { 1 } } \end{array}\tag{6}
$$

$$
\begin{array} { r l } & { b ^ { \prime } = \big ( f _ { \theta } ( \tilde { z } , \tau , \frac { d } { 2 } , a ) - z _ { \tau } \big ) / ( 1 - \tau ) \qquad z ^ { \prime } = \tilde { z } + b ^ { \prime } \frac { d } { 2 } } \\ & { b ^ { \prime \prime } = \big ( f _ { \theta } ( z ^ { \prime } , \tau + \frac { d } { 2 } , \frac { d } { 2 } , a ) - z ^ { \prime } \big ) / ( 1 - ( \tau + \frac { d } { 2 } ) ) } \\ & { \mathcal { L } ( \theta ) = \left\{ \begin{array} { l l } { \| \hat { z } _ { 1 } - z _ { 1 } \| _ { 2 } ^ { 2 } } & { \mathrm { i f ~ } d = d _ { \operatorname* { m i n } } } \\ { ( 1 - \tau ) ^ { 2 } \| ( \hat { z } _ { 1 } - \tilde { z } ) / ( 1 - \tau ) - s g ( b _ { 1 } + b _ { 2 } ) / 2 \| _ { 2 } ^ { 2 } } & { \mathrm { e l s e } } \end{array} \right. } \end{array}\tag{7}
$$

$$
{ w ( \tau ) = 0 . 9 \tau + 0 . 1 }\tag{8}
$$

$$
\mathcal { L } ( \theta ) = - \sum _ { n = 0 } ^ { L } \ln p _ { \theta } ( a _ { t + n } \mid h _ { t } ) - \sum _ { n = 0 } ^ { L } \ln p _ { \theta } ( r _ { t + n } \mid h _ { t } )\tag{9}
$$

$$
\mathcal { L } ( \theta ) = - \sum _ { t = 1 } ^ { T } \ln p _ { \theta } ( R _ { t } ^ { \lambda } \mid s _ { t } ) \qquad R _ { t } ^ { \lambda } = r _ { t } + \gamma c _ { t } \big ( ( 1 - \lambda ) \upsilon _ { t } + \lambda R _ { t + 1 } ^ { \lambda } \big ) \qquad R _ { T } ^ { \lambda } = \upsilon _ { T } \tag{10}
$$

$$
\mathcal { L } ( \theta ) = \frac { 1 - \alpha } { | \mathcal { D } ^ { - } | } \sum _ { i \in \mathcal { D } ^ { - } } \ln \pi _ { \theta } ( a _ { i } \mid s _ { i } ) - \frac { \alpha } { | \mathcal { D } ^ { + } | } \sum _ { i \in \mathcal { D } ^ { + } } \ln \pi _ { \theta } ( a _ { i } \mid s _ { i } ) + \frac { \beta } { N } \sum _ { i = 1 } ^ { N } \mathrm { K L } [ \pi _ { \theta } ( a _ { i } \mid s _ { i } ) \parallel \pi _ { \mathrm { p r i o r } } ]\tag{11}
$$
