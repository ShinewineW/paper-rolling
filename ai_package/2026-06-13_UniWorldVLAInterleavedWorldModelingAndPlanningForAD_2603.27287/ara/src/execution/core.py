# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

from dataclasses import dataclass

@dataclass
class DummyLLM:
    def generate_frame_tokens(self, context, kv_cache=None):
        return ['d_hat'], {'cache': True}
    def generate_action(self, context, frame_tokens, kv_cache=None):
        return (0.0, 0.0), kv_cache

class DummyTokenizer:
    def encode(self, image):
        return ['c'], ['d']
    def decode(self, d_hat, c_guidance):
        return {'rgb_frame': d_hat, 'context': c_guidance}

def plan_uniworld_vla(history_images, ego_tokens, steps=8):
    tokenizer = DummyTokenizer()
    llm = DummyLLM()
    context = []
    contextual = []
    for image in history_images:
        c, d = tokenizer.encode(image)
        contextual.append(c)
        context.extend(d + c)
    context.extend(ego_tokens)
    frames, actions, kv_cache = [], [], None
    for k in range(1, steps + 1):
        d_hat, kv_cache = llm.generate_frame_tokens(context, kv_cache)
        c_guidance = contextual[min(len(contextual) - 1, (k - 1) // 2)]
        frame = tokenizer.decode(d_hat, c_guidance)
        action, kv_cache = llm.generate_action(context, d_hat, kv_cache)
        frames.append(frame)
        actions.append(action)
        context.extend(d_hat + ['<|act|>', action, '<|act|>'])
    return frames, actions

if __name__ == '__main__':
    print(plan_uniworld_vla(['I_t_minus_1', 'I_t'], ['velocity', 'acceleration', 'command']))
