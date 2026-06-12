# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import numpy as np

class StubWorld:
    def encode_history(self, images):
        return np.asarray(images, dtype=float).mean(axis=0)
    def normalize_memory(self, bev, semantic=None, ego_pose=None, flow=None):
        mean = bev.mean()
        std = bev.std() + 1e-6
        return (bev - mean) / std
    def decode_next(self, memory, action):
        action_bias = np.asarray(action, dtype=float).mean()
        occ = memory + action_bias
        flow = np.zeros(memory.shape + (3,), dtype=float)
        return occ, flow

class StubPlanner:
    def sample(self, command, n=5):
        return [np.array([i, 0.0], dtype=float) for i in range(n)]
    def cost(self, occ, traj):
        return float(np.maximum(occ, 0).mean() + np.linalg.norm(traj))
    def refine(self, traj, bev):
        return traj

world = StubWorld()
planner = StubPlanner()
history_images = np.random.randn(3, 4, 4)
action = np.array([0.0, 0.0])
bev = world.encode_history(history_images)
memory = world.normalize_memory(bev)
rollout = []
for t in range(3):
    occ, flow = world.decode_next(memory, action)
    candidates = planner.sample(command='go forward')
    traj = min(candidates, key=lambda tau: planner.cost(occ, tau))
    traj = planner.refine(traj, occ)
    rollout.append({'occupancy': occ, 'flow': flow, 'trajectory': traj})
    action = traj
    memory = world.normalize_memory(occ)
