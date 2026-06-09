# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

# WAM 核心训练与策略学习草图(伪代码)
import torch
import torch.nn.functional as F

# --- 阶段 1: 世界模型训练 (~230K 步, AdamW lr=3e-4) ---
for batch in play_dataloader:  # CALVIN play data ~500K transitions
    obs, actions = batch       # [B, T, C, H, W], [B, T, a_dim]
    h, z = init_rssm_state(B)
    e_seq = []
    for t in range(T):         # T=50
        e = cnn_encoder(obs[:, t])            # e_t in R^1554
        h = rssm_gru(h, z, actions[:, t-1])  # h_t
        z = posterior(h, e)                   # z_t ~ q(z|h,e)
        e_seq.append(e)
    # 逆动力学头作用于 e_t 而非 f_t (避免平凡解)
    e_pairs = torch.cat([e_seq[:-1], e_seq[1:]], dim=-1)
    a_hat = inv_dyn_mlp(e_pairs)              # psi([e_t; e_{t+1}])
    loss_kl   = kl_div(posterior_dist, prior_dist)
    loss_recon = F.mse_loss(decoder(f_seq), obs)
    loss_act  = F.l1_loss(a_hat, actions[:, :-1])
    loss = 3.0*loss_kl + 1.0*loss_recon + 1000.0*loss_act
    loss.backward(); optimizer.step()

# --- 阶段 2: BC 预训练 (冻结 WAM, 5000 epochs) ---
wam.eval()
for epoch in range(5000):
    f_t = wam.encode(expert_demos)          # f_t = [h_t; z_t] in R^2048
    a_pred = denoise_step(policy, f_t, a_k, k)  # mu_theta(f_t, a^k, k)
    loss_bc = F.mse_loss(a_pred, a_target)
    loss_bc.backward(); bc_optimizer.step()

# --- 阶段 3: PPO 微调 (冻结 WAM, 800 次迭代) ---
for iteration in range(800):
    # 想象展开使用先验 z_hat ~ p(z|h), 50条并行
    rollouts = wam.imagine(policy, n_parallel=50, denoise_steps=10)
    rewards  = reward_classifier(rollouts)   # R_psi 二值奖励
    ppo_update(policy, rollouts, rewards,
               alpha_bc=0.025)               # BC 正则化防灾难性遗忘
