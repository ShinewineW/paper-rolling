# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import numpy as np

class DummyVelocityNet:
    def __call__(self, x_t, t, cond):
        return np.zeros_like(x_t)

def shifted_timestep(t, beta):
    return beta * t / (1 + (beta - 1) * t)

def fm_train_step(model, x, cond, beta=1.0, lr=1e-4):
    eps = np.random.randn(*x.shape)
    t = np.random.rand()
    t = shifted_timestep(t, beta)
    x_t = (1 - t) * x + t * eps
    v_t = eps - x
    pred = model(x_t, t, cond)
    loss = np.mean((pred - v_t) ** 2)
    return loss

def sample_loop(model, shape, cond, steps=20, conditioned_frames=None):
    x = np.random.randn(*shape)
    for s in range(steps, 0, -1):
        t = s / steps
        v = model(x, t, cond)
        x = x - v / steps
        if conditioned_frames is not None:
            n = conditioned_frames.shape[0]
            x[:n] = conditioned_frames
    return x

x = np.random.randn(24, 32, 32, 4)
cond = {'text_embedding': np.random.randn(77, 1024)}
model = DummyVelocityNet()
print(float(fm_train_step(model, x, cond)))
y = sample_loop(model, x.shape, cond, conditioned_frames=x[:1])
print(y.shape)
