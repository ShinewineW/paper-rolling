# Concepts

## 世界-动作模型（WAM）
- **Notation**: $$\mathcal{M}_{\theta}$$，包含世界路径 $$\mathcal{M}_{\theta}^{\mathrm{world}}$$ 与动作路径 $$\mathcal{M}_{\theta}^{\mathrm{action}}$$
- **Definition**: WAM 是一种以逆动力学目标增强的世界模型，在 DreamerV2 的 RSSM 骨干上添加逆动力学头，联合预测未来视觉观测与引发状态转变的动作，使潜在表示同时服务于视觉动态预测和动作感知两个目标。
- **Boundary conditions**: WAM 是对 DreamerV2 训练目标的轻量级扩充，不修改策略网络架构；其动作正则化信号作用于编码器嵌入 $$e_t$$，而非 RSSM 特征 $$f_t$$，以避免因 GRU 直接输入 $$a_{t-1}$$ 而使动作预测退化为平凡解。
- **Related concepts**: ['逆动力学模型', 'RSSM', '动作正则化', '扩散策略']

## 逆动力学目标（Inverse Dynamics Objective）
- **Notation**: $$\hat{a}_t = \psi([e_t; e_{t+1}])$$（公式 6）
- **Definition**: 给定两个连续时刻的编码器嵌入 $$e_t$$ 和 $$e_{t+1}$$，通过三层 MLP $$\psi$$ 预测导致该状态转变的动作 $$a_t$$，训练信号为 L1 损失 $$\mathcal{L}_{\mathrm{action}} = \|\hat{a}_t - a_t\|_1$$。
- **Boundary conditions**: 逆动力学头作用于编码器嵌入 $$e_t \in \mathbb{R}^{1554}$$，而非 RSSM 联合特征 $$f_t \in \mathbb{R}^{2048}$$；这是为了让正则化信号能够真正传入编码器，而非被 GRU 接收到的历史动作所「短路」。
- **Related concepts**: ['WAM', '编码器嵌入', '动作感知级联效应', '自监督表示学习']

## 动作感知级联效应（Action-Aware Cascading Effect）
- **Notation**: $$z_t \sim q_\phi(z_t \mid h_t, e_t)$$，$$\hat{z}_t \sim p_\phi(z_t \mid h_t)$$（公式 2–3）
- **Definition**: 逆动力学头对编码器嵌入 $$e_t$$ 的正则化会沿模型路径逐级传播：动作感知的 $$e_t$$ 影响后验 $$z_t \sim q_\phi(z_t \mid h_t, e_t)$$，KL 损失再将这一结构传播至先验 $$\hat{z}_t \sim p_\phi(z_t \mid h_t)$$，最终使基于先验生成的想象轨迹也携带动作相关信息。
- **Boundary conditions**: 论文将级联效应作为 WAM 设计的「关键机制」显式论述；该效应的前提是先验与后验之间存在 KL 正则化，若去掉 KL 损失则级联链断裂。（论文未显式给出传播量化公式，效应强度为定性描述。）
- **Related concepts**: ['WAM', 'RSSM', 'KL 散度损失', '离线策略微调']

## RSSM（循环状态空间模型）
- **Notation**: $$h_t = f_\phi(h_{t-1}, z_{t-1}, a_{t-1})$$（公式 1），$$z_t \sim q_\phi(z_t \mid h_t, e_t)$$（公式 2），$$\hat{z}_t \sim p_\phi(z_t \mid h_t)$$（公式 3），$$f_t = [h_t; z_t] \in \mathbb{R}^{2048}$$
- **Definition**: DreamerV2 的潜在动力学骨干，将确定性循环状态 $$h_t$$ 与随机范畴变量 $$z_t$$（32×32）结合，通过 GRU 建模时序依赖，并利用后验/先验双流结构在训练与推理阶段分别生成潜在特征。
- **Boundary conditions**: WAM 直接复用 DreamerV2 的 RSSM 结构（Hafner et al., 2022），不对网络拓扑作任何改动；RSSM 设计本身来自 PlaNet（Hafner et al., 2019），WAM 论文对其不作进一步修改。
- **Related concepts**: ['WAM', 'DreamerV2', 'KL 散度损失', '潜在空间 MDP']

## WAM 训练目标（$$\mathcal{L}_{\mathrm{WAM}}$$）
- **Notation**: $$\mathcal{L}_{\mathrm{WAM}} = \lambda_{\mathrm{KL}}\mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{img}}\mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{act}}\mathcal{L}_{\mathrm{action}}$$（公式 7），其中 $$\mathcal{L}_{\mathrm{KL}} = \mathrm{KL}[q_\phi(z_t \mid h_t, e_t) \| p_\phi(z_t \mid h_t)]$$，$$\mathcal{L}_{\mathrm{recon}} = \|o_t - \hat{o}_t\|_2^2$$，$$\mathcal{L}_{\mathrm{action}} = \|\hat{a}_t - a_t\|_1$$
- **Definition**: WAM 端到端优化三项加权损失之和：KL 散度损失（后验与先验对齐）、图像重建损失（L2）以及动作预测损失（L1），分别通过损失权重 $$\lambda_{\mathrm{KL}}, \lambda_{\mathrm{img}}, \lambda_{\mathrm{act}}$$ 平衡。
- **Boundary conditions**: 损失系数 $$\lambda_{\mathrm{KL}} = 3.0, \lambda_{\mathrm{img}} = 1.0, \lambda_{\mathrm{act}} = 1000.0$$ 是针对 CALVIN 基准调优所得，论文未声称这些超参数可直接迁移至其他域。
- **Related concepts**: ['逆动力学目标', 'RSSM', '动作感知级联效应']

## 潜在空间 MDP（$$\mathcal{M}_{\mathrm{wm}}$$）
- **Notation**: $$\theta^* = \arg\max_\theta \mathbb{E}_{\tau \sim \pi_\theta, P_\phi}\left[\sum_{t=0}^T \gamma^t R_\psi(z_t, a_t)\right]$$（公式 10）
- **Definition**: 冻结 WAM 后，以 WAM 的潜在空间定义马尔可夫决策过程 $$\mathcal{M}_{\mathrm{wm}} = (\mathcal{Z}, \mathcal{A}, P_\phi, R_\psi, \gamma)$$，其中 $$\mathcal{Z}$$ 为潜在状态空间，$$P_\phi$$ 为学习到的转移动力学，$$R_\psi$$ 为二值奖励分类器，策略在该虚拟环境中通过 DPPO 进行离线微调，无需任何物理交互。
- **Boundary conditions**: 该 MDP 框架直接沿用 DiWA 的管线设计；WAM 在此框架中的改进仅体现在更优质的潜在表示上，MDP 结构本身（包括 DPPO 算法、奖励分类器训练流程）与 DiWA 完全相同。
- **Related concepts**: ['WAM', 'DPPO', '奖励分类器', '扩散策略']

## 扩散策略（DiffusionMLP）
- **Notation**: $$a_t^{k-1} = \mu_\theta(f_t, a_t^k, k) + \sigma_k \epsilon$$（公式 8），$$\mathcal{L}_{\mathrm{BC}} = \mathbb{E}_{k, \epsilon, (f_t, a_t)}[\|\mu_\theta(f_t, a_t^k, k) - a_t^{k-1}\|^2]$$（公式 9）
- **Definition**: 以世界模型潜在特征 $$f_t \in \mathbb{R}^{2048}$$ 为条件、通过迭代去噪生成动作的策略网络，采用 DDPM 去噪过程：从高斯噪声出发，经 K 步去噪产生预测动作，训练时最小化去噪目标 $$\mathcal{L}_{\mathrm{BC}}$$。
- **Boundary conditions**: 行为克隆阶段使用 K=20 去噪步，PPO 微调阶段减少至 10 去噪步以提高推理效率；BC 正则化系数 $$\alpha_{\mathrm{BC}} = 0.025$$ 用于防止 PPO 微调过程中的灾难性遗忘。
- **Related concepts**: ['潜在空间 MDP', 'DPPO', 'WAM', '行为克隆']
