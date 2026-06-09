import torch

# 核心训练循环草图
def train_step(model, action_batch, world_batch, alpha=0.04):
    # --- 动作模型分支 ---
    # 输入: [BOS]{text}[BOI]{img}x M[EOI][BOA]
    # 使用修改注意力掩码:动作token只能看到文本和图像token,不能看到先前动作token
    act_input, act_target = action_batch  # act_target 仅含动作token位置
    act_logits = model(act_input, attn_mask='action_mask')  # 屏蔽先前动作
    L_action = cross_entropy(act_logits, act_target, ignore_non_action=True)

    # --- 世界模型分支 ---
    # 输入: [BOS]{text}[BOI]{img}[EOI][BOA]{action}[EOA][EOS][BOI]
    # 使用标准因果注意力掩码
    world_input, world_target = world_batch  # world_target 仅含图像token位置
    world_logits = model(world_input, attn_mask='causal')
    L_world = cross_entropy(world_logits, world_target, ignore_non_image=True)

    loss = L_action + alpha * L_world
    loss.backward()
    return loss

# 推理(策略分支)
def infer_actions(model, obs_history, text, K=5):
    # obs_history: M帧图像(默认M=2)
    tokens = build_action_seq(text, obs_history)  # [BOS]{text}{img}x M[BOA]
    # 并行生成K步动作(注意力掩码使每步独立于先前动作)
    action_tokens = model.generate(tokens, max_new_tokens=7*K, attn_mask='action_mask')
    return decode_actions(action_tokens)  # shape: [K, 7]
