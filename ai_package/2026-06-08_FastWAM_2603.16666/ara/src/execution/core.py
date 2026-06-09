import torch

def fast_wam_infer(obs_frame, lang_text, model, num_steps=10, H=32):
    # 编码观测与语言指令
    z_obs = model.vae.encode(obs_frame)       # 干净第一帧潜变量 tokens
    lang_emb = model.text_encoder(lang_text)  # T5 语言嵌入

    # 视频 DiT 单次前向，得到潜在世界表征（不生成未来帧）
    world_repr = model.video_dit(
        clean_tokens=z_obs,
        lang_cond=lang_emb,
        future_tokens=None
    )

    # 动作 DiT 流匹配去噪（10步）
    a_t = torch.randn(1, H, model.action_dim)
    dt = 1.0 / num_steps
    for i in range(num_steps, 0, -1):
        t_val = torch.tensor([i * dt])
        vel = model.action_dit(a_t, t_val, world_repr, lang_emb)
        a_t = a_t - vel * dt  # Euler step
    return a_t  # shape: [1, H, action_dim]
