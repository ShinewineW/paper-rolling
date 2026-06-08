# Cosmos-Transfer1 推理核心草图
# 假设 control_branches、base_dit 已加载

def control_branch_forward(branch, c_i):
    """控制分支：3 个 transformer 块 + 零初始化线性层"""
    activations = []
    for block, linear in zip(branch.blocks, branch.zero_linears):
        h = block(c_i)
        activations.append(linear(h))  # h_i^j
    return activations

def cosmos_transfer1_step(x_sigma, sigma, modality_inputs, control_weights, text_tokens):
    """
    x_sigma: 带噪视频 token
    modality_inputs: {modality_name: c_i}
    control_weights: tensor [N, X, Y, T]
    """
    branch_acts = {}  # {modality: [h_i^0, h_i^1, h_i^2]}
    for i, (mod, c_i) in enumerate(modality_inputs.items()):
        h_list = control_branch_forward(control_branches[mod], c_i)
        w_i = control_weights[i]  # [X, Y, T]
        # 权重归一化（若各模态权重之和 > 1）
        w_sum = sum(control_weights).clamp(min=1.0)
        w_i_norm = w_i / w_sum
        # 元素积加权: w_i · h_i^j
        branch_acts[mod] = [w_i_norm.unsqueeze(-1) * h for h in h_list]
    # 主干 DiT 去噪预测
    noise_pred = base_dit(x_sigma, sigma, branch_acts, text_tokens)
    return noise_pred

# 扩散采样主循环
for sigma in noise_schedule:  # 多步去噪
    noise_pred = cosmos_transfer1_step(
        x_t, sigma, modality_inputs, weights, text_tokens
    )
    x_t = sampler.step(x_t, noise_pred, sigma)
# x_t 即最终生成的视频 token（56K tokens → 5 秒 1280×704p@24fps）
