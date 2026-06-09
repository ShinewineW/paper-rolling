# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import torch

def autoregressive_rollout(model, cond_frame, action, total_steps=15):
    # cond_frame: [C, H, W] tensor; action: single modality (one of traj/cmd/angle_speed/goal_pt)
    K = 25
    priors = [cond_frame]
    all_clips = []

    for _ in range(total_steps):
        n_prior = min(len(priors), 3)

        # build frame mask m for latent replacement
        m = torch.zeros(K)
        m[:n_prior] = 1.0

        # encode history frames to clean latents
        z_list = [model.encode(f) for f in priors[-n_prior:]]

        # sample Gaussian noise
        n_noisy = torch.randn(K, *z_list[0].shape) * model.sigma_max

        # latent replacement: n_hat = m * z + (1 - m) * n
        n_hat = n_noisy.clone()
        for i, z in enumerate(z_list):
            n_hat[i] = z

        # denoise with triangular CFG and single-mode action conditioning
        clip = model.ddim_sample(
            n_hat, m=m, action=action,
            s_min=1.0, s_max=2.5, steps=50
        )  # -> [K, C, H, W]

        all_clips.append(clip)
        # use last 3 frames as dynamic priors for next rollout step
        priors = [clip[K - 3], clip[K - 2], clip[K - 1]]

    return torch.cat(all_clips, dim=0)
