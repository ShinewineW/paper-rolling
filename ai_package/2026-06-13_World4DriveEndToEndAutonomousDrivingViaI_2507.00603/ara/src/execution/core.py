# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import numpy as np

def mse(a, b):
    return ((a - b) ** 2).mean(axis=tuple(range(1, a.ndim)))

def train_step(batch, model, weights):
    images_t, images_future, traj_vocab, expert_traj = batch
    q_plan = model.intention_encoder(traj_vocab)
    latent_t = model.physical_latent_encoder(images_t)
    latent_future_actual = model.physical_latent_encoder(images_future)
    trajectories = model.action_decoder(q_plan, latent_t)
    action_tokens = model.action_encoder(trajectories)
    latent_future_pred = model.world_model(action_tokens, latent_t)
    distances = mse(latent_future_pred, latent_future_actual[:, None])
    j = distances.argmin(axis=1)
    selected_traj = trajectories[np.arange(len(j)), j]
    scores = model.score_net(latent_future_pred)
    losses = {
        'sem': model.semantic_loss(),
        'recon': distances[np.arange(len(j)), j].mean(),
        'score': model.focal_loss(scores, j),
        'traj': np.abs(selected_traj - expert_traj).mean(),
    }
    return sum(weights[k] * losses[k] for k in losses), selected_traj

def infer(images_t, traj_vocab, model):
    q_plan = model.intention_encoder(traj_vocab)
    latent_t = model.physical_latent_encoder(images_t)
    trajectories = model.action_decoder(q_plan, latent_t)
    action_tokens = model.action_encoder(trajectories)
    latent_future_pred = model.world_model(action_tokens, latent_t)
    scores = model.score_net(latent_future_pred)
    return trajectories[np.arange(scores.shape[0]), scores.argmax(axis=1)]
