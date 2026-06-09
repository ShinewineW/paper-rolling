训练期三个显式目标如下。

【世界模型(训练期), 公式 (2)(3)】
$$\mathcal{L}(\phi)\doteq\mathrm{E}_{q_\phi}\!\left[\sum_{t=1}^{T}\bigl(\beta_{\mathrm{pred}}\mathcal{L}_{\mathrm{pred}}(\phi)+\beta_{\mathrm{dyn}}\mathcal{L}_{\mathrm{dyn}}(\phi)+\beta_{\mathrm{rep}}\mathcal{L}_{\mathrm{rep}}(\phi)\bigr)\right]$$
$$\mathcal{L}_{\mathrm{pred}}(\phi)\doteq-\ln p_\phi(x_t|z_t,h_t)-\ln p_\phi(r_t|z_t,h_t)-\ln p_\phi(c_t|z_t,h_t)$$
$$\mathcal{L}_{\mathrm{dyn}}(\phi)\doteq\max\!\bigl(1,\mathrm{KL}[\mathrm{sg}(q_\phi(z_t|h_t,x_t))\|p_\phi(z_t|h_t)]\bigr)$$
$$\mathcal{L}_{\mathrm{rep}}(\phi)\doteq\max\!\bigl(1,\mathrm{KL}[q_\phi(z_t|h_t,x_t)\|\mathrm{sg}(p_\phi(z_t|h_t))]\bigr)$$
权重 β_pred=1, β_dyn=1, β_rep=0.1。解码器和奖励预测器对确定性目标使用 symlog 均方损失(公式 (8)):
$$\mathcal{L}(\theta)\doteq\tfrac{1}{2}\bigl(f(x,\theta)-\mathrm{symlog}(y)\bigr)^{2}$$
奖励预测器和 Critic 对随机目标使用 symexp twohot 交叉熵损失(公式 (11)):
$$\mathcal{L}(\theta)\doteq-\mathrm{twohot}(y)^{T}\log\mathrm{softmax}(f(x,\theta))$$

【Critic(训练期), 公式 (5)】
$$\mathcal{L}(\psi)\doteq-\sum_{t=1}^{T}\ln p_\psi(R_t^\lambda|s_t),\quad R_t^\lambda\doteq r_t+\gamma c_t\bigl((1-\lambda)v_t+\lambda R_{t+1}^\lambda\bigr),\quad R_T^\lambda\doteq v_T$$
γ=0.997, λ=0.95。Critic 损失同时应用于想象轨迹(损失权重 β_val=1)和回放缓冲区轨迹(β_repval=0.3)。

【Actor(训练期), 公式 (6)(7)】
$$\mathcal{L}(\theta)\doteq-\sum_{t=1}^{T}\mathrm{sg}\!\left(\frac{R_t^\lambda-v_\psi(s_t)}{\max(1,S)}\right)\log\pi_\theta(a_t|s_t)+\eta\,\mathrm{H}[\pi_\theta(a_t|s_t)]$$
$$S\doteq\mathrm{EMA}\bigl(\mathrm{Per}(R_t^\lambda,95)-\mathrm{Per}(R_t^\lambda,5),\,0.99\bigr)$$
η=3×10^−4, 分母下限 L=1。推理期仅执行 $a_t\sim\pi_\theta(a_t|s_t)$，上述损失项均不参与。
