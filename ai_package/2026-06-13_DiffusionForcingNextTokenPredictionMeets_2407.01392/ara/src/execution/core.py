# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import numpy as np

class CDFModel:
    def init_latent(self):
        return np.zeros((1,))
    def update_latent(self, z_prev, x_noisy, k):
        return z_prev + 0.0 * np.mean(x_noisy) + 0.0 * k
    def predict_eps(self, z_prev, x_noisy, k):
        return np.zeros_like(x_noisy)

def forward_diffuse(x, k, alpha_bar):
    eps = np.random.randn(*x.shape)
    return np.sqrt(alpha_bar[k]) * x + np.sqrt(1.0 - alpha_bar[k]) * eps, eps

def train_step(model, x_seq, K, alpha_bar):
    z_prev = model.init_latent()
    losses = []
    for x_t in x_seq:
        k_t = np.random.randint(0, K + 1)
        x_noisy, eps = forward_diffuse(x_t, k_t, alpha_bar)
        eps_hat = model.predict_eps(z_prev, x_noisy, k_t)
        losses.append(np.mean((eps - eps_hat) ** 2))
        z_prev = model.update_latent(z_prev, x_noisy, k_t)
    return float(np.mean(losses))

def sample(model, shape, schedule, alpha, alpha_bar, sigma, guidance=None):
    x = np.random.randn(schedule.shape[1], *shape) * sigma[-1]
    z = [model.init_latent() for _ in range(schedule.shape[1] + 1)]
    for m in range(schedule.shape[0] - 2, -1, -1):
        for t in range(schedule.shape[1]):
            k = int(schedule[m, t])
            z[t + 1] = model.update_latent(z[t], x[t], int(schedule[m + 1, t]))
            eps = model.predict_eps(z[t + 1], x[t], k)
            w = np.random.randn(*shape)
            x[t] = (x[t] - (1.0 - alpha[k]) / np.sqrt(1.0 - alpha_bar[k]) * eps) / np.sqrt(alpha[k]) + sigma[k] * w
        if guidance is not None:
            x = guidance(x)
    return x
