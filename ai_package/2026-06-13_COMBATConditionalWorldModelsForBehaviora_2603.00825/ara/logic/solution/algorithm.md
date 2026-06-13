训练期目标是条件视频生成和 latent denoising，论文只给出问题建模公式，没有给出显式训练损失公式；DCAE 训练目标仅定性写为 L2 reconstruction loss、perceptual similarity loss、KL divergence term 的组合，world model 训练为在 Player 1 actions 条件下预测 next latent frame，distillation 定性写为 DMD loss 与 critic loss 的组合。论文显式公式如下：
$$
P ( s _ { t + 1 } \mid s _ { \leq t } ) \approx P ( s _ { t + 1 } \mid s _ { t - k : t } ) ,
$$
$$
D = \{ ( s _ { t } , a _ { t } ^ { ( 1 ) } , s _ { t + 1 } ) \} _ { t = 1 } ^ { T } ,
$$
$$
P _ { \theta } ( s _ { t + 1 } \mid s _ { t - k : t } , a _ { t - k : t } ^ { ( 1 ) } )
$$
$$
\pi ^ { ( 2 ) } ( a _ { t } ^ { ( 2 ) } \mid s _ { t } , a _ { t } ^ { ( 1 ) } ) ,
$$
$$
\begin{array} { r } { \mathrm { A d a L N }  \mathrm { A t t e n t i o n }  \mathrm { G a t e d R e s i d u a l }  } \\ { \mathrm { A d a L N }  \mathrm { M L P }  \mathrm { G a t e d R e s i d u a l } } \end{array}
$$
推理期单独使用 CausVid DMD few-step sampling、static key-value caching 与 distilled decoder；这些加速项不应写入原始 world model 训练目标。
