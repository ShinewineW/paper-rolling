# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import torch
import torch.nn.functional as F

# === 扩散WFM核心训练循环 ===
def diffusion_train_step(model, tokenizer, text_enc, batch, P_mean, P_std, sigma_data):
    z0 = tokenizer.encode(batch['video'])        # CV8x8x8连续latent [B,T',H',W',C]
    cond = text_enc(batch['text'])               # T5-XXL文本嵌入
    log_sigma = torch.randn(z0.shape[0]) * P_std + P_mean
    sigma = log_sigma.exp().view(-1, 1, 1, 1, 1)
    n = torch.randn_like(z0) * sigma
    pred = model(z0 + n, sigma.flatten(), cond)  # DiT + AdaLN-LoRA + FPS-aware 3D RoPE
    l_sigma = ((pred - z0) ** 2).mean()
    lam = (sigma**2 + sigma_data**2) / (sigma * sigma_data)**2
    u = model.uncertainty_mlp(sigma)             # 可学习不确定性MLP
    loss = (lam / u.exp() * l_sigma + u).mean()  # EDM不确定性加权损失
    return loss

# === 自回归WFM核心训练循环 ===
def ar_train_step(model, disc_tokenizer, text_enc, batch, vocab_size=64000, z_lam=3e-4):
    v = disc_tokenizer.encode(batch['video'])    # DV8x16x16离散token [B,T',H',W']
    v_seq = v.reshape(v.shape[0], -1)            # 展平序列 [B, seq_len]
    cond = text_enc(batch['text'])               # T5-XXL嵌入(cross-attn)
    logits = model(v_seq[:, :-1], cond)          # Transformer Decoder [B, seq_len-1, V]
    nll = F.cross_entropy(
        logits.reshape(-1, vocab_size),
        v_seq[:, 1:].reshape(-1)
    )
    z_loss = z_lam * logits.pow(2).sum(-1).mean()  # z-loss稳定训练
    return nll + z_loss
