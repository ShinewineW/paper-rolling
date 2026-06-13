# ⚠️ RECONSTRUCTED STUB — NOT the official implementation.
# A minimal runnable reconstruction inferred from the paper text, for ARA
# tracing only. For the authoritative code (repo + pinned SHA + file:line),
# see ../code_ref.md. Do not cite this as the paper's real implementation.

import torch

class ToyVLA(torch.nn.Module):
    def __init__(self, obs_dim=16, action_dim=8):
        super().__init__()
        self.net = torch.nn.Sequential(torch.nn.Linear(obs_dim + action_dim + 1, 64), torch.nn.SiLU(), torch.nn.Linear(64, action_dim))
        self.proj = torch.nn.Linear(obs_dim, obs_dim)

    def forward(self, a_ts, obs, s):
        return self.net(torch.cat([a_ts, obs, s], dim=-1))

model = ToyVLA()
opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
for step in range(3):
    obs = torch.randn(4, 16)
    action = torch.randn(4, 8)
    eps = torch.randn_like(action)
    s = torch.rand(4, 1)
    a_ts = s * action + (1 - s) * eps
    velocity = model(a_ts, obs, s)
    loss_fm = ((velocity - (action - eps)) ** 2).mean()
    q = torch.randn(4, 16)
    d = torch.randn(4, 16)
    loss_distill = (model.proj(q) - d).abs().mean()
    loss = loss_fm + loss_distill
    opt.zero_grad()
    loss.backward()
    opt.step()
print(round(float(loss.detach()), 6))
