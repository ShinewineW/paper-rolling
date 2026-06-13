# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import numpy as np

class MemoryBank:
    def __init__(self, max_frames):
        self.max_frames = max_frames
        self.frames = []
    def push(self, qh_hat):
        self.frames.append(qh_hat)
        self.frames = self.frames[-self.max_frames:]
    def stack(self):
        if not self.frames:
            return None
        return np.concatenate(self.frames, axis=0)

def cross_attention(query, key, value):
    if key is None:
        return query
    score = query @ key.T / max(query.shape[-1], 1) ** 0.5
    weight = np.exp(score - score.max(axis=-1, keepdims=True))
    weight = weight / weight.sum(axis=-1, keepdims=True)
    return weight @ value

def mlp(x, out_dim):
    w = np.ones((x.shape[-1], out_dim), dtype=float) / x.shape[-1]
    return x @ w

def llm_reason(scene_tokens, history_tokens, instruction_tokens):
    context = np.concatenate([scene_tokens.mean(0), history_tokens.mean(0), instruction_tokens.mean(0)])
    return mlp(context[None, :], scene_tokens.shape[-1])

def gaussian_project(x):
    mu = mlp(x, x.shape[-1])
    log_sigma = np.clip(mlp(x, x.shape[-1]), -3, 3)
    return mu, np.exp(log_sigma)

def gru_decoder(z, modes=6, horizon=6):
    base = mlp(z, modes * horizon * 2).reshape(modes, horizon, 2)
    return np.cumsum(base, axis=1)

def orion_step(multiview_features, instruction_tokens, memory, q_scene, q_hist, train=False, gt_traj=None):
    scene_queries = cross_attention(q_scene, multiview_features, multiview_features)
    past = memory.stack()
    q_hist = cross_attention(q_hist, past, past) if past is not None else q_hist
    q_hist_hat = cross_attention(q_hist, scene_queries, scene_queries)
    memory.push(q_hist_hat)
    scene_tokens = mlp(scene_queries, instruction_tokens.shape[-1])
    history_tokens = mlp(q_hist_hat, instruction_tokens.shape[-1])
    planning_token = llm_reason(scene_tokens, history_tokens, instruction_tokens)
    mu_s, sig_s = gaussian_project(planning_token)
    z = mu_s
    traj = gru_decoder(z)
    losses = {}
    if train and gt_traj is not None:
        mu_t, sig_t = gaussian_project(gt_traj.reshape(1, -1))
        losses['L_vae_proxy'] = float(np.mean((mu_s - mu_t[:, :mu_s.shape[-1]]) ** 2))
        losses['L_mse_proxy'] = float(np.mean((traj[0] - gt_traj[:traj.shape[1]]) ** 2))
    return traj, losses

rng = np.random.default_rng(0)
features = rng.normal(size=(32, 64))
instruction = rng.normal(size=(8, 64))
mem = MemoryBank(max_frames=16)
q_s = rng.normal(size=(12, 64))
q_h = rng.normal(size=(4, 64))
trajectory, loss_dict = orion_step(features, instruction, mem, q_s, q_h)
print(trajectory.shape)
