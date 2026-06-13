# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

from typing import Iterable, Any

class Tokenizer:
    def encode(self, frames):
        return ['z0'] if not frames else [f'z{i}' for i, _ in enumerate(frames)]
    def decode(self, tokens):
        return {'frame_from_tokens': list(tokens)}

class ActionCodebook:
    def lookup(self, action_id: int):
        return {'latent_action': int(action_id)}

class DynamicsModel:
    def sample_next_tokens(self, token_history, latent_action):
        return token_history + [f'z{len(token_history)}_a{latent_action[\'latent_action\']}']

def rollout(prompt_frame: Any, user_actions: Iterable[int]):
    tokenizer = Tokenizer()
    codebook = ActionCodebook()
    dynamics = DynamicsModel()
    token_history = tokenizer.encode([prompt_frame])
    frames = [prompt_frame]
    for action_id in user_actions:
        latent_action = codebook.lookup(action_id)
        token_history = dynamics.sample_next_tokens(token_history, latent_action)
        frames.append(tokenizer.decode(token_history[-1:]))
    return frames

if __name__ == '__main__':
    print(rollout({'prompt': 'image'}, [0, 1, 1, 0]))
