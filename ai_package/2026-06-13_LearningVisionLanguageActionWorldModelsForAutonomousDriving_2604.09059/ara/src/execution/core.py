# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

def vla_world_step(obs, ego_status, goal, model, tokenizer):
    scene = model.perceive(obs, ego_status)
    short_pred = model.predict_short_term(scene, ego_status, goal)
    visual_tokens = model.generate_visual_tokens(scene, short_pred, goal)
    future_frame = tokenizer.decode(visual_tokens)
    reasoning = model.think(scene, short_pred, future_frame, goal)
    action = model.predict_action(scene, reasoning, goal)
    trajectory = model.plan_trajectory(scene, reasoning, action)
    return {'perception': scene, 'prediction': short_pred, 'visual': visual_tokens, 'think': reasoning, 'action': action, 'answer': trajectory}

def grpo_train_step(prompt, policy, verifier, optimizer):
    rollouts = [policy.sample(prompt) for _ in range(policy.group_size)]
    rewards = [verifier.score(r) for r in rollouts]
    mean = sum(rewards) / len(rewards)
    var = sum((r - mean) ** 2 for r in rewards) / max(len(rewards), 1)
    std = var ** 0.5 or 1.0
    advantages = [(r - mean) / std for r in rewards]
    loss = policy.grpo_surrogate_loss(prompt, rollouts, advantages)
    optimizer.zero_grad(); loss.backward(); optimizer.step()
    return float(loss)
