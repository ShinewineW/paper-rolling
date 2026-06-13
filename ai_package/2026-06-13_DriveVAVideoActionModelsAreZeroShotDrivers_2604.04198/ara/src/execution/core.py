# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import numpy as np

class DriveVAStub:
    def __init__(self, steps=2, horizon=8):
        self.steps = steps
        self.horizon = horizon

    def encode_text(self, instruction):
        return {'text': instruction}

    def encode_video_history(self, frames):
        return np.asarray(frames, dtype=float).mean(axis=0, keepdims=True)

    def embed_state(self, ego_state):
        return np.asarray(ego_state, dtype=float)

    def dit_velocity(self, y, cond, s):
        video_bias = cond['history'].reshape(-1).mean()
        state_bias = cond['state'].mean()
        return 0.25 * np.tanh(video_bias + state_bias) - 0.5 * y

    def sample_targets(self, cond):
        y = np.random.randn(self.horizon, 4)
        for step in range(self.steps):
            s = step / max(self.steps - 1, 1)
            y = y + self.dit_velocity(y, cond, s) / self.steps
        future_video_latents = y[:, :1]
        action_tokens = y[:, 1:4]
        return future_video_latents, action_tokens

    def rollout(self, history_frames, ego_state, instruction, rounds=1):
        actions = []
        history = list(history_frames)
        for _ in range(rounds):
            cond = {
                'history': self.encode_video_history(history),
                'state': self.embed_state(ego_state),
                'text': self.encode_text(instruction),
            }
            future_latents, chunk = self.sample_targets(cond)
            actions.extend(chunk.tolist())
            history = history[-3:] + [float(v[0]) for v in future_latents[:1]]
        return actions

model = DriveVAStub()
print(model.rollout([0.0, 0.1, 0.2, 0.3], [1.0, 0.0], 'turn left', rounds=1))
