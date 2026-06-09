# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

# env, rnn, vae 为全局变量（来自论文 Section 2.4 伪代码原文）
def rollout(controller):
    obs = env.reset()
    h = rnn.initial_state()
    done = False
    cumulative_reward = 0
    while not done:
        z = vae.encode(obs)              # V: 帧 -> 潜变量 z_t
        a = controller.action([z, h])    # C: [z_t, h_t] -> 动作 a_t
        obs, reward, done = env.step(a)
        cumulative_reward += reward
        h = rnn.forward([a, z, h])       # M: 更新隐藏状态 h_{t+1}
    return cumulative_reward
