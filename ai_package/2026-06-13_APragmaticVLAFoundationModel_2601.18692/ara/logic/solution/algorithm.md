训练期目标显式包含条件 Flow Matching 与深度蒸馏；论文没有把推理期加权或融合项写入训练目标。观测与动作序列定义为：
$$
\begin{array} { r } { \mathbf { O } _ { t } = [ \mathbf { I } _ { t } ^ { 1 } , \mathbf { I } _ { t } ^ { 2 } , \mathbf { I } _ { t } ^ { 3 } , \mathbf { T } _ { t } , \mathbf { s } _ { t } ] , } \end{array}\tag{1}
$$
$$
\mathbf { A } _ { t } = [ \mathbf { a } _ { t } , \mathbf { a } _ { t + 1 } , \ldots , \mathbf { a } _ { t + T - 1 } ] ,\tag{2}
$$
论文说明训练目标是通过 conditional flow matching 表征 $p ( \mathbf { A } _ { t } | \mathbf { O } _ { t } )$，并给出概率路径与损失：
$$
p ( \mathbf { A } _ { t , s } | \mathbf { A } _ { t } ) = \mathcal { N } ( s \mathbf { A } _ { t } , ( 1 - s ) \mathbf { I } ) .\tag{3}
$$
$$
\begin{array} { r } { \mathcal { L } _ { \mathrm { F M } } = \mathbb { E } _ { s \sim \mathcal { U } \left[ 0 , 1 \right] , \mathbf { A } _ { t } , \epsilon } \left\| v _ { \theta } ( \mathbf { A } _ { t , s } , \mathbf { O } _ { t } , s ) - ( \mathbf { A } _ { t } - \epsilon ) \right\| ^ { 2 } , } \end{array}\tag{4}
$$
空间蒸馏目标为：
$$
\begin{array} { r } { \mathcal { L } _ { d i s t i l l } = \mathbb { E } _ { \mathbf { Q } _ { t } } \left| \mathrm { P r o j } ( \mathbf { Q } _ { t } ) - \mathbf { D } _ { t } \right| , } \end{array}\tag{5}
$$
