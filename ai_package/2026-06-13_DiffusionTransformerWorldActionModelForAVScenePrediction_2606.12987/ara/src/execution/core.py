# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import numpy as np

class Model:
    def __call__(self, tokens, cond, tau):
        return tokens * 0.0

def fourier_actions(actions, freqs):
    x = actions[..., None] * freqs
    return np.concatenate([np.sin(2 * np.pi * x), np.cos(2 * np.pi * x)], axis=-1)

def train_step(model, z_now, z_future, actions, freqs, alpha_bar, drop_prob=0.1):
    tau = np.random.randint(0, len(alpha_bar))
    eps = np.random.randn(*z_future.shape)
    z_noisy = np.sqrt(alpha_bar[tau]) * z_future + np.sqrt(1 - alpha_bar[tau]) * eps
    act = fourier_actions(actions, freqs)
    if np.random.rand() < drop_prob:
        act = np.zeros_like(act)
    cond = {'present': z_now, 'actions': act, 'tau': tau}
    delta = model(z_noisy, cond, tau)
    z_hat = z_now[:, None] + delta
    return ((z_hat - z_future) ** 2).mean()

def ddim_infer(model, z_now, actions, freqs, schedule):
    z = np.random.randn(*z_now[:, None].shape)
    act = fourier_actions(actions, freqs)
    for tau in reversed(schedule):
        cond = {'present': z_now, 'actions': act, 'tau': tau}
        z0 = z_now[:, None] + model(z, cond, tau)
        z = z0
    return z

def jump_rollout(jump_model, z_now, action_chunks, freqs):
    anchors = [z_now]
    z = z_now
    for chunk in action_chunks:
        act = fourier_actions(chunk, freqs).mean(axis=1)
        z = jump_model(z, {'actions': act}, 0)
        anchors.append(z)
    return anchors
