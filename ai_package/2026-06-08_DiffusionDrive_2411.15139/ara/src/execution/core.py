# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import torch, math

def truncated_diffusion_inference(
    anchors,     # (N_anchor, T_f, 2) K-Means锚点轨迹
    model,       # f_theta: 级联扩散解码器
    scene_ctx,   # BEV特征 + agent/map查询
    alpha_bar,   # 噪声调度累积乘积
    T_trunc=50,
    N_infer=20,
    steps=2
):
    # 从锚定高斯分布采样含噪轨迹(公式4)
    ab = alpha_bar[T_trunc]
    noisy = (math.sqrt(ab) * anchors[:N_infer]
             + math.sqrt(1 - ab) * torch.randn_like(anchors[:N_infer]))

    # DDIM 2步去噪(推理期)
    timesteps = torch.linspace(T_trunc, 1, steps, dtype=torch.long)
    for t in timesteps:
        scores, pred_traj = model(noisy, scene_ctx, t)  # 公式5
        noisy = ddim_update(pred_traj, noisy, alpha_bar, t)

    return pred_traj[scores.argmax()]  # 取置信分数最高轨迹
