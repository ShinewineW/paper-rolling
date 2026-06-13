论文未给出显式损失公式。训练期分两阶段：先用标准 VQ-VAE 目标训练视频 tokenizer；再从像素训练 LAM，并将其 VQ codebook 输出作为 stopgrad latent action，与视频 token 一起训练 dynamics model。dynamics model 的训练目标在原文中定性表述为预测 token 与 ground-truth token 之间的 cross-entropy loss，并在训练期随机 mask 输入 token。推理期不使用 LAM encoder/decoder，只保留 VQ codebook，由用户动作索引得到 latent action，随后用 MaskGIT 逐帧采样；这些推理期采样设置不属于训练目标。论文显式给出的公式是可控性度量而非训练损失：$$
\Delta _ { t } \mathrm { P S N R } = \mathrm { P S N R } ( x _ { t } , \hat { x } _ { t } ) - \mathrm { P S N R } ( x _ { t } , \hat { x } _ { t } ^ { \prime } ) ,
$$
