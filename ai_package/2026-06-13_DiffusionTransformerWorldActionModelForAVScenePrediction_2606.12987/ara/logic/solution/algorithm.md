训练期：论文显式给出 diffusion 的 x0-prediction objective，且说明 epsilon-prediction 在 compact latent spaces 中会 collapse；classifier-free guidance 通过 action dropout 在训练时随机置零 action embedding。损失公式逐字转录如下：
$$
\mathcal { L } _ { \mathrm { d i f f } } = \mathbb { E } _ { \tau , \epsilon } \left. \hat { z } _ { 0 } ( \tilde { z } _ { \tau } , c , \tau ) - z _ { 0 } \right. _ { 2 } ^ { 2 } ,\tag{4}
$$
推理期：DDIM deterministic sampling 从 pure Gaussian noise 迭代细化预测；train-derived calibration 是测试时应用的 per-channel mean and scale shift，不属于训练目标；latent interpolation、distribution metric 选择与 jump open-loop chaining 也不应写入 diffusion training loss。
