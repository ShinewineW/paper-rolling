# 核心 GRPO Physical AI RL 训练循环草图
G = 9          # 每 prompt 采样回复数
kl_coeff = 0.005
lr = 4e-6
max_len = 6144

for step, batch in enumerate(rl_dataloader):   # 全局 batch=128 questions
    prompts = shuffle_choices_on_the_fly(batch['prompt'])  # 随机打乱 MCQ 选项
    answers = batch['answer']

    # Actor rollout: 每 prompt 生成 G 条回复
    groups = []
    for p in prompts:
        responses = actor.generate(p, num_return=G, max_new_tokens=max_len)
        groups.append(responses)   # shape per prompt: [G, seq_len]

    # 计算规则奖励: 准确率 + 格式
    rewards = compute_rewards(groups, answers)  # shape: [B, G]
    acc_r  = accuracy_reward(groups, answers)   # 字符串匹配 <answer> 标签
    fmt_r  = format_reward(groups)              # 正则匹配 <think>/<answer>
    rewards = acc_r + fmt_r

    # GRPO 优势归一化 (论文公式)
    mean_r = rewards.mean(dim=-1, keepdim=True)
    std_r  = rewards.std(dim=-1, keepdim=True)
    adv = (rewards - mean_r) / (std_r + 1e-8)

    # 策略梯度 + KL 惩罚更新
    loss = grpo_policy_loss(actor, ref_model, groups, adv, kl_coeff)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if step >= 500:
        break
