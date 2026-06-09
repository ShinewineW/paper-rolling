# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import torch
import torch.nn.functional as F
from sklearn.cluster import KMeans

# 预计算K-Means锚点
anchors = KMeans(n_clusters=N_ANCHOR).fit(train_trajs).cluster_centers_
anchors = torch.tensor(anchors)  # [N_ANCHOR, T_f, 2]

# 训练循环
for sensors, gt_traj in dataloader:
    z = perception_backbone(sensors)  # BEV特征 + 智能体查询
    # 截断扩散前向过程(公式4)
    i = torch.randint(1, T_TRUNC + 1, (1,)).item()
    alpha_bar = noise_schedule[i]
    eps = torch.randn_like(anchors)
    tau_noisy = (alpha_bar ** 0.5) * anchors + ((1 - alpha_bar) ** 0.5) * eps
    # 级联扩散解码器预测(公式5)
    scores, tau_pred = cascade_decoder(tau_noisy, z, timestep=i)
    # 正样本: 距离真值最近的锚点
    dists = ((anchors - gt_traj) ** 2).sum(-1).sum(-1)
    y = torch.zeros(N_ANCHOR)
    y[dists.argmin()] = 1.0
    # 训练损失(公式6)
    rec = F.l1_loss(tau_pred, gt_traj.expand_as(tau_pred), reduction='none').mean([-2, -1])
    loss = (y * rec).sum() + lam * F.binary_cross_entropy(scores, y)
    loss.backward()
    optimizer.step()

# 推理: 从锚定高斯分布出发,DDIM 2步去噪
z = perception_backbone(sensors)
tau = sample_anchored_gaussian(anchors, N_INFER, noise_schedule, T_TRUNC)
for step in range(N_STEPS):  # 默认2步
    scores, tau_pred = cascade_decoder(tau, z, timestep=T_TRUNC - step)
    tau = ddim_update(tau, tau_pred, step, noise_schedule)
best_traj = tau_pred[scores.argmax()]
