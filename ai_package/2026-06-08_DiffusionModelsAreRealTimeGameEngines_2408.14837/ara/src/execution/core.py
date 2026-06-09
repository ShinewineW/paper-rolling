# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import torch

def gamengen_loop(unet, encoder, decoder, action_emb, init_frames, init_actions,
                  num_ddim_steps=4, cfg_w=1.5, max_ctx=64):
    ctx_frames = list(init_frames[-max_ctx:])
    ctx_actions = list(init_actions[-max_ctx:])
    while True:
        action = get_user_input()
        # 编码上下文帧为潜变量,推理时 noise_level=0
        ctx_latents = torch.stack([encoder(f) for f in ctx_frames], dim=1)
        act_tokens = torch.stack([action_emb(a) for a in ctx_actions], dim=1)
        # 4 步 DDIM 去噪,对历史帧条件施加 CFG(w=1.5)
        x = torch.randn(1, 4, 32, 40)  # 随机初始噪声潜变量
        for t in reversed(range(num_ddim_steps)):
            v_cond = unet(x, t, ctx_latents, act_tokens)
            v_uncond = unet(x, t, torch.zeros_like(ctx_latents), act_tokens)
            v = v_uncond + cfg_w * (v_cond - v_uncond)
            x = ddim_step(x, v, t)
        frame = decoder(x)
        display(frame)
        ctx_frames = (ctx_frames + [frame])[-max_ctx:]
        ctx_actions = (ctx_actions + [action])[-max_ctx:]
