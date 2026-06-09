# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import re
import torch

def accuracy_reward(output, ground_truth):
    m = re.search(r'<answer>(.*?)</answer>', output, re.DOTALL)
    if m and m.group(1).strip() == ground_truth:
        return 1.0
    return 0.0

def format_reward(output):
    has_think = bool(re.search(r'<think>.*?</think>', output, re.DOTALL))
    has_answer = bool(re.search(r'<answer>.*?</answer>', output, re.DOTALL))
    return 1.0 if (has_think and has_answer) else 0.0

def grpo_advantage(rewards):
    mean_r = rewards.mean()
    std_r = rewards.std() + 1e-8
    return (rewards - mean_r) / std_r

def grpo_train_step(policy_model, prompts, ground_truths, G=9, max_new_tokens=6144):
    for prompt, gt in zip(prompts, ground_truths):
        outputs = [policy_model.generate(prompt, max_new_tokens=max_new_tokens, temperature=0.6) for _ in range(G)]
        rewards = torch.tensor([accuracy_reward(o, gt) + format_reward(o) for o in outputs])
        advantages = grpo_advantage(rewards)
        # policy gradient update with KL penalty (coeff=0.005) not shown
    return advantages
