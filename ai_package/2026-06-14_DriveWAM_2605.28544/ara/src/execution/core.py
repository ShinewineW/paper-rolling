# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import numpy as np

class DriveWAMStub:
    def __init__(self, video_budget=448, action_budget=160, lam=0.07):
        self.mem = {'v': [], 'a': []}
        self.budget = {'v': video_budget, 'a': action_budget}
        self.lam = lam

    def vlm_guidance(self, latest_frame, recent_action, route_command):
        return '保持与 route command 一致，并根据当前道路参与者调整谨慎程度'

    def encode_video(self, x):
        return np.asarray(x, dtype=float).reshape(-1, 1)

    def encode_action(self, a):
        return np.asarray(a, dtype=float).reshape(-1, 1)

    def sample_video_latent(self, history, ego_state, guidance):
        z = history[-1][0] if history else np.zeros((4, 1))
        for _ in range(3):
            z = z * 0.9
        return z

    def sample_action(self, z_future, history, ego_state, guidance):
        a = np.zeros((10, 1))
        for _ in range(10):
            a = a + z_future.mean() * 0.01
        return a

    def update_memory(self, modality, new_keys, query):
        pool = self.mem[modality] + [np.asarray(k, dtype=float) for k in new_keys]
        budget = self.budget[modality]
        if len(pool) <= budget:
            self.mem[modality] = pool
            return
        keys = np.stack(pool).reshape(len(pool), -1)
        q = np.asarray(query, dtype=float).reshape(1, -1)
        logits = (q @ keys.T).ravel()
        attn = np.exp(logits - logits.max())
        rho = attn / attn.sum()
        norm = np.linalg.norm(keys, axis=1, keepdims=True) + 1e-8
        sim = (keys / norm) @ (keys / norm).T
        eta = (sim.sum(axis=1) - 1.0) / max(len(pool) - 1, 1)
        score = self.lam * rho - (1 - self.lam) * eta
        keep = np.argsort(score)[-budget:]
        self.mem[modality] = [pool[i] for i in keep]

    def rollout(self, observations, ego_states, route_commands):
        history, actions = [], []
        prev_action = np.zeros((10, 1))
        for x_k, e_k, c_k in zip(observations, ego_states, route_commands):
            g_k = self.vlm_guidance(x_k, prev_action, c_k)
            z_hat = self.sample_video_latent(history, e_k, g_k)
            a_hat = self.sample_action(z_hat, history, e_k, g_k)
            z_obs = self.encode_video(x_k)
            u_hat = self.encode_action(a_hat)
            history.append((z_obs, u_hat))
            self.update_memory('v', z_obs, z_hat)
            self.update_memory('a', u_hat, a_hat)
            actions.append(a_hat)
            prev_action = a_hat
        return actions

if __name__ == '__main__':
    model = DriveWAMStub()
    obs = [np.ones((4, 1)), np.ones((4, 1)) * 2]
    ego = [np.zeros(3), np.zeros(3)]
    route = ['straight', 'left']
    print([a.shape for a in model.rollout(obs, ego, route)])
