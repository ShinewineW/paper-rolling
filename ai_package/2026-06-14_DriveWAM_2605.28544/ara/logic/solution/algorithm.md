训练期目标是 joint flow-matching objective，视频分支保持 future-visual-prediction prior，action 分支学习把 predicted future world evolution 解码为 executable ego motion。论文显式给出的训练损失公式为：
$$
\begin{array} { r } { \mathcal { L } = \mathbb { E } _ { k , \tau } \left[ \left. \hat { v } _ { k + 1 , \tau } ^ { z } - v _ { k + 1 , \tau } ^ { z } \right. _ { 2 } ^ { 2 } + \beta _ { a } \left. \hat { v } _ { k + 1 , \tau } ^ { a } - v _ { k + 1 , \tau } ^ { a } \right. _ { 2 } ^ { 2 } \right] , } \end{array}\tag{4}
$$
其中视频 velocity prediction 与 action velocity prediction 在论文中分别写为：
$$
\hat { v } _ { k + 1 , \tau } ^ { z } = T _ { \omega } ( z _ { k + 1 , \tau } ; H _ { k } , e _ { k } , g _ { k } , \tau ) .\tag{2}
$$
$$
\hat { v } _ { k + 1 , \tau } ^ { a } = D _ { a } ( T _ { \omega } ( u _ { k + 1 , \tau } ; \tilde { z } _ { k + 1 } , H _ { k } , e _ { k } , g _ { k } , \tau ) ) ,\tag{3}
$$
训练期 \tilde { z } _ { k + 1 } 使用 clean future video latent，推理期使用 generated latent；selective KV memory 是 inference-time、training-free，不改变训练目标或模型参数。推理期缓存选择显式公式为：
$$
\rho _ { j } ^ { m } = \frac { 1 } { \left| Q _ { k } ^ { m } \right| } \sum _ { \mathbf { q } \in Q _ { k } ^ { m } } \left[ \mathrm { s o f t m a x } _ { \ell \in H _ { k } ^ { m } } \left( \frac { \mathbf { q } ^ { \top } \mathbf { k } _ { \ell } ^ { m } } { \sqrt { d } } \right) \right] _ { j } , \qquad \eta _ { j } ^ { m } = \mathrm { m e a n } _ { \ell \neq j } \cos ( \mathbf { k } _ { j } ^ { m } , \mathbf { k } _ { \ell } ^ { m } ) ,\tag{6}
$$
$$
s _ { j } ^ { m } = \lambda \rho _ { j } ^ { m } - ( 1 - \lambda ) \eta _ { j } ^ { m } ,\tag{7}
$$
$$
\begin{array} { r } { H _ { k + 1 } ^ { m }  \mathrm { T o p } _ { B ^ { m } - | \Delta H _ { k + 1 } ^ { m } | } ( H _ { k } ^ { m } ) \cup \Delta H _ { k + 1 } ^ { m } , \qquad m \in \{ v , a \} . } \end{array}\tag{8}
$$
