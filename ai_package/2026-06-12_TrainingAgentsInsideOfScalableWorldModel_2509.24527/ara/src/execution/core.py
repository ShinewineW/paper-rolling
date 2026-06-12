# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import numpy as np

class Stub:
    def tokenizer(self, frames):
        return frames.mean(axis=(-2, -1), keepdims=True)
    def dynamics(self, z_tilde, tau, d, actions):
        return z_tilde + (1 - tau) * 0.1
    def policy(self, state, task):
        return np.zeros((state.shape[0], 1))
    def reward(self, state, task):
        return np.zeros((state.shape[0],))
    def value(self, state):
        return np.zeros((state.shape[0],))

def train_step(model, batch):
    frames, actions, task = batch['frames'], batch['actions'], batch['task']
    z1 = model.tokenizer(frames)
    z0 = np.random.normal(size=z1.shape)
    tau = np.random.rand(*z1.shape)
    d = np.ones_like(tau) * 0.25
    z_tilde = (1 - tau) * z0 + tau * z1
    z_hat = model.dynamics(z_tilde, tau, d, actions)
    dynamics_loss = ((z_hat - z1) ** 2 * (0.9 * tau + 0.1)).mean()
    pi = model.policy(z_hat.reshape(z_hat.shape[0], -1), task)
    rewards = model.reward(z_hat.reshape(z_hat.shape[0], -1), task)
    values = model.value(z_hat.reshape(z_hat.shape[0], -1))
    agent_loss = np.abs(pi).mean() + np.abs(rewards).mean() + np.abs(values).mean()
    return dynamics_loss + agent_loss

def imagine(model, context, task, horizon=8):
    z = model.tokenizer(context)
    traj = []
    for _ in range(horizon):
        state = z.reshape(z.shape[0], -1)
        action = model.policy(state, task)
        noise = np.random.normal(size=z.shape)
        z_tilde = noise
        for _ in range(4):
            z = model.dynamics(z_tilde, 0.0, 0.25, action)
            z_tilde = z
        traj.append((z, action, model.reward(state, task), model.value(state)))
    return traj

model = Stub()
batch = {'frames': np.random.rand(2, 4, 8, 8), 'actions': np.zeros((2, 1)), 'task': np.zeros((2, 1))}
print(float(train_step(model, batch)))
print(len(imagine(model, batch['frames'], batch['task'])))
