训练期：论文明确给出 conditional flow matching 的插值路径与速度回归目标，并给出单阶段 joint multi-task loss。公式逐字转录如下：

$$
x _ { t } = \left( 1 - t \right) x _ { 0 } + t x _ { 1 } , \quad t \sim \mathcal { U } ( 0 , 1 ) ,\tag{1}
$$

$$
\mathcal { L } _ { \mathrm { F M } } = \mathbb { E } _ { x _ { 0 } , x _ { 1 } , t } \left[ \left. v _ { \theta } ( x _ { t } , t \vert c ) - ( x _ { 1 } - x _ { 0 } ) \right. _ { 2 } ^ { 2 } \right] .\tag{2}
$$

$$
\mathcal { L } = \lambda _ { d } \mathcal { L } _ { d } + \lambda _ { v } \mathcal { L } _ { v } + \lambda _ { a } \mathcal { L } _ { a } ,\tag{3}
$$

其中 \mathcal { L } _ { d }、\mathcal { L } _ { v }、\mathcal { L } _ { a } 分别对应深度预测、视频预测和轨迹预测。训练描述中 depth generator 对 ground-truth depth 加噪并预测 denoising update，video generator 在 latent-space 初始化 noisy video latents，action generator 将 noise trajectory 映射为 feasible future action sequence。推理期：从噪声采样并沿 ODE backward integration 得到与条件一致的样本；action generator 可独立激活用于 planning，论文未把任何推理期融合或加权项写入训练目标。
