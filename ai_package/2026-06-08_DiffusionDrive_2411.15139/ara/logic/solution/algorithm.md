训练目标(论文公式6):
$$\mathcal{L} = \sum_{k=1}^{N_{\mathrm{anchor}}} [y_k \mathcal{L}_{\mathrm{rec}}(\hat{\tau}_k, \tau_{\mathrm{gt}}) + \lambda \mathrm{BCE}(\hat{s}_k, y_k)]$$
其中 $y_k\in\{0,1\}$ 为正负样本标签(距真值最近的锚点为正，其余为负)，$\mathcal{L}_{\mathrm{rec}}$ 为L1轨迹重建损失，$\mathrm{BCE}$ 为二值交叉熵分类损失，$\lambda$ 为平衡权重(论文未给出具体数值)。

训练期截断前向扩散过程(论文公式4)：
$$\tau_k^i = \sqrt{\bar{\alpha}^i} \mathbf{a}_k + \sqrt{1-\bar{\alpha}^i}\epsilon,\quad \epsilon\sim\mathcal{N}(0,\mathbf{I})$$
其中 $i\in[1,T_{\mathrm{trunc}}]$，$T_{\mathrm{trunc}}\ll T$，$\mathbf{a}_k$ 为第k个K-Means锚点轨迹。

推理期使用DDIM更新规则执行2步去噪，从锚定高斯分布出发逐步还原轨迹，此过程不属于训练目标。
