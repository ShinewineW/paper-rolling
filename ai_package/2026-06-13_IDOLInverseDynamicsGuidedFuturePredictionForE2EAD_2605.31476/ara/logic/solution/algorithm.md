训练期目标只使用论文显式给出的 overall objective：$$
\mathcal { L } = \lambda _ { \mathrm { o f f } } \mathcal { L } _ { \mathrm { o f f } } + \lambda _ { \mathrm { o f f - i m } } \mathcal { L } _ { \mathrm { o f f - i m } } + \lambda _ { \mathrm { i m } } \mathcal { L } _ { \mathrm { i m } } + \lambda _ { \mathrm { s i m } } \mathcal { L } _ { \mathrm { s i m } } + \lambda _ { \mathrm { m a p } } \mathcal { L } _ { \mathrm { m a p } } ,\tag{12}
$$ 其中 L_off 是 trajectory offset loss，L_off-im 与 L_im 是 imitation reward supervision，L_sim 是 simulator-metric loss，L_map 是 current 与 imagined future states 的 BEV semantic supervision。推理期不把融合或加权项写入训练目标；推理期流程使用 anchor query、latent rollout、IDM transition decoding、spatial CrossAttn、MLN_idm、MLN_cl、trajectory offset prediction 与 reward model ranking。论文显式给出的相关推理公式包括：$$
e _ { k } ^ { ( 0 ) } = \phi ( [ z , a _ { k } ] ) , \qquad k = 1 , \ldots , K .\tag{2}
$$ $$
X _ { k } ^ { ( u ) } = [ e _ { k } ^ { ( u ) } , \tilde { B } _ { k } ^ { ( u ) } ] ,\tag{3}
$$ $$
\begin{array} { r } { \hat { X } _ { k } ^ { ( u + 1 ) } = \mathrm { B E V W o r l d M o d e l } \left( X _ { k } ^ { ( u ) } \right) . } \end{array}\tag{4}
$$ $$
\{ ( e _ { k } ^ { ( u ) } , \tilde { B } _ { k } ^ { ( u ) } ) \} _ { u = 0 } ^ { U } ,\tag{5}
$$ $$
\left( S _ { k } ^ { ( u ) } , g _ { k } ^ { ( u ) } \right) = \mathrm { I D M } \left( \tilde { B } _ { k } ^ { ( u ) } , \tilde { B } _ { k } ^ { ( u + 1 ) } \right) ,\tag{6}
$$ $$
S _ { k } = \frac { 1 } { U } \sum _ { u = 0 } ^ { U - 1 } S _ { k } ^ { ( u ) } , \qquad g _ { k } = \frac { 1 } { U } \sum _ { u = 0 } ^ { U - 1 } g _ { k } ^ { ( u ) } .\tag{7}
$$ $$
\begin{array} { r } { \tilde { e } _ { k } ^ { ( \ell ) } = \mathrm { L N } \Big ( e _ { k , \mathrm { i n } } ^ { ( \ell ) } + \mathrm { C r o s s A t t n } \big ( e _ { k , \mathrm { i n } } ^ { ( \ell ) } , S _ { k } ^ { ( \ell ) } , S _ { k } ^ { ( \ell ) } \big ) \Big ) , } \end{array}\tag{8}
$$ $$
\begin{array} { r } { \bar { e } _ { k } ^ { ( \ell ) } = \mathrm { M L N _ { i d m } } \left( \tilde { e } _ { k } ^ { ( \ell ) } , g _ { k } ^ { ( \ell ) } \right) . } \end{array}\tag{9}
$$ $$
e _ { k , \mathrm { i n } } ^ { ( \ell ) } = \mathrm { M L N } _ { \mathrm { c l } } \left( e _ { k } ^ { ( 0 ) } , \bar { e } _ { k } ^ { ( \ell - 1 ) } \right) , \qquad \ell \geq 1 ,\tag{10}
$$ $$
e _ { k , \mathrm { i n } } ^ { ( 0 ) } = e _ { k } ^ { ( 0 ) } .\tag{11}
$$
