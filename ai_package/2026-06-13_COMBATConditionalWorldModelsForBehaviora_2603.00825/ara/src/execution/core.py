# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import numpy as np

class Encoder:
    def __call__(self, frames, poses=None):
        return np.zeros((len(frames), 128, 23, 11), dtype=np.float32)

class DiTWorldModel:
    def denoise_next_latent(self, context_latents, p1_actions, diffusion_step, kv_cache=None):
        cond = {'p1_actions': p1_actions, 'diffusion_step': diffusion_step}
        next_latent = context_latents[-1].copy()
        return next_latent, kv_cache, cond

class Decoder:
    def __call__(self, latent):
        return np.zeros((448, 736, 3), dtype=np.uint8)

def rollout(seed_frames, seed_poses, p1_action_stream, steps=32, distilled_steps=4):
    encoder, world, decoder = Encoder(), DiTWorldModel(), Decoder()
    latents = list(encoder(seed_frames, seed_poses))
    frames = []
    kv_cache = None
    for t in range(steps):
        action_history = p1_action_stream[max(0, t - 127):t + 1]
        latent = latents[-1]
        for diffusion_step in range(distilled_steps):
            latent, kv_cache, _ = world.denoise_next_latent(latents[-128:], action_history, diffusion_step, kv_cache)
        latents.append(latent)
        frames.append(decoder(latent))
    return frames
