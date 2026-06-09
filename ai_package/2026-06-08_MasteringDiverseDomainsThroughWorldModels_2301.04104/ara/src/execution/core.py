# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import torch

# DreamerV3 核心训练循环草图 (B=16, T=64, H=15)
for step in range(total_steps):
    # 1. 环境交互
    if step % collect_every == 0:
        with torch.no_grad():
            s = world_model.observe(obs, prev_act)  # 返回 (h_t, z_t)
            action = actor.sample(s)
        next_obs, rew, done, _ = env.step(action)
        replay.add(obs, action, rew, done, s)
        obs, prev_act = next_obs, action

    # 2. 世界模型训练
    batch = replay.sample(B=16, T=64)
    h, z, z_prior = world_model.encode_seq(batch['obs'], batch['act'])
    L_pred = world_model.pred_loss(h, z, batch)         # symlog MSE + twohot 奖励
    L_dyn  = torch.clamp(kl(z.detach(), z_prior), min=1).mean()   # sg(encoder)
    L_rep  = torch.clamp(kl(z, z_prior.detach()), min=1).mean()   # sg(dynamics)
    opt_wm.zero_grad()
    (L_pred + L_dyn + 0.1 * L_rep).backward()
    opt_wm.step()

    # 3. 想象展开 H=15 步
    traj = world_model.imagine(h.detach(), z.detach(), actor, H=15)
    v = critic.mean(traj.states)

    # 4. λ-returns (γ=0.997, λ=0.95)
    R = compute_lambda_return(traj.rew, traj.cont, v, gamma=0.997, lam=0.95)

    # 5. Critic 训练 (symexp twohot 分类损失)
    opt_critic.zero_grad()
    (-critic.log_prob(R.detach(), traj.states).mean()).backward()
    opt_critic.step()
    ema_critic.update()  # decay=0.98

    # 6. Actor 训练 (REINFORCE + 熵 + 百分位回报归一化)
    S = ema_S.update(torch.quantile(R.detach(), 0.95) - torch.quantile(R.detach(), 0.05))
    adv = (R.detach() - v.detach()) / max(1.0, float(S))
    loss_a = -(adv * actor.log_prob(traj.act, traj.states)).mean()
    loss_a = loss_a - 3e-4 * actor.entropy(traj.states).mean()
    opt_actor.zero_grad()
    loss_a.backward()
    opt_actor.step()
