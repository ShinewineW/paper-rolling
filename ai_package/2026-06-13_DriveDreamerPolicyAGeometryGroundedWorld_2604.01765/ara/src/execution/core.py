# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import numpy as np

class Expert:
    def __init__(self, name):
        self.name = name
    def sample(self, noise, condition):
        return noise * 0.0 + condition.mean(axis=0, keepdims=True)

def causal_query_mask(n_depth, n_video, n_action):
    groups = np.array([0] * n_depth + [1] * n_video + [2] * n_action)
    return groups[:, None] >= groups[None, :]

def run_step(text_tokens, image_tokens, action_tokens, mode='imagination'):
    n_depth, n_video, n_action = 64, 64, 8
    queries = np.random.randn(n_depth + n_video + n_action, 16)
    mask = causal_query_mask(n_depth, n_video, n_action)
    tokens = np.concatenate([text_tokens, image_tokens, action_tokens, queries], axis=0)
    hidden = tokens[-len(queries):] + mask.mean(axis=1, keepdims=True)
    depth_emb = hidden[:n_depth]
    video_emb = hidden[n_depth:n_depth + n_video]
    action_emb = hidden[n_depth + n_video:]
    outputs = {}
    if mode in {'imagination', 'full'}:
        outputs['depth'] = Expert('depth').sample(np.random.randn(1, 16), depth_emb)
        clip_condition = image_tokens.mean(axis=0, keepdims=True)
        outputs['video'] = Expert('video').sample(np.random.randn(1, 16), np.concatenate([video_emb, clip_condition], axis=0))
    outputs['actions'] = Expert('action').sample(np.random.randn(1, 16), action_emb)
    return outputs

if __name__ == '__main__':
    text = np.random.randn(4, 16)
    images = np.random.randn(32, 16)
    action = np.random.randn(2, 16)
    print(run_step(text, images, action, mode='imagination').keys())
