世界模型训练目标(论文公式 1,显式给出):
$$L_{\mathrm{worldmodel}} = -\sum_{t=1}^{T}\sum_{i=1}^{n}\log p(z_{t,i}|\mathbf{z}_{<t}, z_{t,j<i}, \mathbf{c}_{\leq t}, \mathbf{a}_{<t})$$
在给定所有过去帧 token、当前帧前序 token、历史文本以及过去动作的条件下,最大化当前图像 token 的对数似然(标准自回归下一 token 预测)。

视频解码器训练目标(论文公式 2,显式给出,v-参数化去噪):
$$L_{\mathrm{video}} = \mathbb{E}_{\epsilon,t'}\left[\|\epsilon_{\theta}(\mathbf{x}^{t'}, t', \mathbf{z}, \mathbf{m}) - \epsilon\|_2^2\right]$$
其中 ε_θ 为去噪网络,ε 为 v-参数化去噪目标,t'~U(0,1) 为扩散时间步,z 为条件图像 token 序列,m 为任务掩码序列。

图像 tokenizer 训练损失为多项加权组合:图像重建损失(L1+L2+感知损失 L_perceptual+GAN 损失 L_GAN)、量化损失(codebook 嵌入损失+commitment 损失)、DINO 余弦相似度蒸馏损失。论文未给出 tokenizer 的统一显式综合目标公式。

以下两式仅用于推理期,不属于训练目标:
分类器自由引导(论文公式 3):
$$l_{\mathrm{final}} = (1+t)l_{\mathrm{conditioned}} - t l_{\mathrm{unconditioned}}$$
推理期视频解码图像/视频去噪加权平均(论文公式 4):
$$\tilde{\epsilon}_{\theta}(\mathbf{x}^{t'}, t', \mathbf{z}, \mathbf{m}) = w \cdot \epsilon_{\theta}^{\pi}(\mathbf{x}^{t'}, t', \mathbf{z}, \mathbf{m}) + (1-w) \cdot \epsilon_{\theta}(\mathbf{x}^{t'}, t', \mathbf{z}, \mathbf{m})$$
