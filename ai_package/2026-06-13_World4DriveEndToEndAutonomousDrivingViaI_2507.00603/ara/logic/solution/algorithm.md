论文显式给出的端到端训练损失为：
$$
\mathcal { L } = \alpha \mathcal { L } _ { s e m } + \beta \mathcal { L } _ { r e c o n } + \gamma \mathcal { L } _ { s c o r e } + \eta \mathcal { L } _ { t r a j } ,
$$
其中论文说明默认设置 α = 0.2, β = 0.2, γ = 0.5, η = 1.0。训练期还显式说明用 cross-entropy loss \mathcal { L } _ { s e m } 强化 semantic understanding，用 predicted latent 与 actual latent 的 feature distance 中最小者作为 \mathcal { L } _ { r e c o n }，用 scores 与 selected modality index j 之间的 focal loss 优化 ScoreNet，并用 L _ { 1 } loss \mathcal { L } _ { t r a j } 用 expert trajectory 指导最终 planning trajectory。推理期不同于训练期：论文说明 during inference 直接选择 world model 最高 score 对应的 trajectory 作为 final trajectory，不把推理期选择规则写入训练目标。<!--ref:80--><!--ref:125--><!--ref:131--><!--ref:133--><!--ref:137--><!--ref:139-->
