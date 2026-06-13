训练期:论文显式给出标准 flow matching 训练损失为 $$
\mathcal { L } _ { \mathrm { F M } } = \mathbb { E } _ { s , \epsilon , x _ { \mathrm { d a t a } } } \left[ \left\| v _ { \boldsymbol { \theta } } \left( \boldsymbol { x } ^ { ( s ) } , { s } \right) - \dot { \boldsymbol { x } } ^ { ( s ) } \right\| _ { 2 } ^ { 2 } \right] .\tag{2}
$$。在 DriveVA 方法段中,论文把 clean target tokens 记为 $\mathbf { Y } _ { 0 } ^ { ( l ) }$,采样 $s \sim \mathcal { U } ( 0 , 1 )$ 与 $\mathbf { \epsilon } \gets \mathcal { N } ( \mathbf { 0 } , \mathbf { I } )$,用线性插值构造 noisy target,目标速度为 $\dot { \mathbf { Y } } ^ { ( l , s ) } = \mathbf { Y } _ { 0 } ^ { ( l ) } - \epsilon$,并逐字给出训练公式 $$
\mathcal { L } \mathbb { F }\tag{9}
$$。该 markdown 未给出更完整的显式联合损失公式；正文仅定性说明 training objective combines a flow-matching loss for future-frame generation with a trajectory prediction loss。推理期:从噪声目标块开始,在固定历史条件、ego state 与文本 token 条件下用 DiT 做 flow-based sampling,论文说明 inference 使用 2 sampling steps；video continuation 是推理/滚动时维持长时域一致性的策略,不得写入训练损失。
