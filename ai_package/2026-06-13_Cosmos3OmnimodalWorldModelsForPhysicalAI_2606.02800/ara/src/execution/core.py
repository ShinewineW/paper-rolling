# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

from dataclasses import dataclass
import random

@dataclass
class Segment:
    modality: str
    clean: bool
    tokens: list


def encode(segment):
    return [f'{segment.modality}:{i}' for i, _ in enumerate(segment.tokens)]


def pack_sample(language_tokens, ar_media, dm_segments):
    ar = list(language_tokens)
    for seg in ar_media:
        ar.extend(encode(seg))
    ar += ['<EOS>', '<BOG>']
    clean_dm, noisy_dm = [], []
    order = {'vision': 0, 'audio': 1, 'action': 2}
    for seg in sorted(dm_segments, key=lambda s: (not s.clean, order[s.modality])):
        if seg.clean:
            clean_dm.extend(encode(seg))
        else:
            noisy_dm.extend(encode(seg))
    return ar, clean_dm + noisy_dm


def reasoner_next_token_loss(ar_tokens):
    return max(0, len(ar_tokens) - 1)


def generator_velocity_mse(dm_tokens, conditioning_mask):
    loss = 0.0
    for tok, is_conditioning in zip(dm_tokens, conditioning_mask):
        if is_conditioning:
            continue
        eps = random.gauss(0.0, 1.0)
        x0 = random.random()
        sigma = random.random()
        x_sigma = sigma * eps + (1.0 - sigma) * x0
        target_velocity = eps - x0
        pred_velocity = 0.0 * x_sigma
        loss += (pred_velocity - target_velocity) ** 2
    return loss


def train_step(sample, stage='generator'):
    ar, dm = pack_sample(sample['text'], sample.get('ar_media', []), sample['dm_segments'])
    if stage == 'reasoner':
        return reasoner_next_token_loss(ar)
    conditioning_mask = [tok.startswith('vision') and 'clean' in tok for tok in dm]
    return generator_velocity_mse(dm, conditioning_mask)

sample = {
    'text': ['prompt'],
    'dm_segments': [Segment('vision', True, [0]), Segment('vision', False, [1, 2]), Segment('action', False, [3])],
}
print(train_step(sample))
