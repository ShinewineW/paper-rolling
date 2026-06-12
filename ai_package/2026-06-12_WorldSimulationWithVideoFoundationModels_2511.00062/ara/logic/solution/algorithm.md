训练期的显式目标是 flow matching velocity prediction，论文逐字给出的公式为：
$$
\mathbf { x } _ { t } = ( 1 - t ) \mathbf { x } + t { \boldsymbol { \epsilon } } .\tag{1}
$$
$$
\mathbf { v } _ { t } = \epsilon - \mathbf { x } .\tag{2}
$$
$$
\begin{array} { r } { \mathcal { L } ( \boldsymbol { \theta } ) = \mathbb { E } _ { \mathbf { x } , \boldsymbol { \epsilon } , \mathbf { c } , t } \left\| \mathbf { u } ( \mathbf { x } _ { t } , t , \mathbf { c } ; \boldsymbol { \theta } ) - \mathbf { v } _ { t } \right\| ^ { 2 } , } \end{array}\tag{3}
$$
论文还给出 shifted logit-normal timestep 变换：
$$
t _ { s } = \frac { \beta t } { 1 + ( \beta - 1 ) t }\tag{4}
$$
其中 c 是文本 embedding、reference frames 和其他 conditional inputs 等条件信息；训练期 denoising loss 只施加到指定需要生成的 frames。RL post-training 中论文定性说明使用 VideoAlign reward、组内归一化 advantage、轨迹条件概率分解和 diffusion loss regularization，但未给出显式 RL 损失公式。推理期的长视频评估指标不是训练目标，论文逐字给出的 RNDS 公式为：
$$
\mathsf { R N D S } [ i ] = \left( \frac { \mathrm { D O V E R } [ i ] } { \mathrm { D O V E R } _ { \mathrm { G T } } [ i ] } \right) / \left( \frac { \mathrm { D O V E R } [ 1 ] } { \mathrm { D O V E R } _ { \mathrm { G T } } [ 1 ] } \right) ,\tag{5}
$$
