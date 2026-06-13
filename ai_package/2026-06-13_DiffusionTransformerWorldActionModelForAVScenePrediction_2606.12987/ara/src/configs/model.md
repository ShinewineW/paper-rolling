## 主模型输入输出
- **Value**: current front-camera frame 的 Stable-Diffusion-VAE latent 加 logged ego-actions，输出 up to 16 horizon steps future scene latents，decoder 渲染 256×256 frames
- **Rationale**: 任务被定义为 action-conditioned latent world model，而不是 pixel-space 直接预测。
- **Search range**: up to 16 horizon steps；8 s at 2 Hz
- **Sensitivity**: 高；latent 空间与 horizon 定义决定建模难度。
- **Source**: Sec 1 Input and output

## VAE latent grid
- **Value**: CAM FRONT frames at 256×256 resolution 编码为 32×32×4 latent grids；scaling factor 0.18215
- **Rationale**: Stable-Diffusion VAE 提供 encode-predict-decode pipeline 的紧凑表示。
- **Search range**: 256×256 frames 到 32×32×4 latents
- **Sensitivity**: 高；latent 分辨率与 scaling 影响重建 ceiling 与预测空间。
- **Source**: Sec 3 Image features and latent encoding

## patchification
- **Value**: patch size 4；产生 8×8=64 spatial tokens；每个 token dimension 64
- **Rationale**: 恢复 spatial tokens 后 DiT 才能在 compact setting 中超越 matched-parameter MLP。
- **Search range**: 64 spatial tokens
- **Sensitivity**: 高；spatial tokens 是论文列出的必要因素之一。
- **Source**: Sec 3；Sec 5.2

## AnchoredVAEDiT 主干
- **Value**: 4 transformer blocks，4 attention heads，model dimension 256，约 5.4 M parameters
- **Rationale**: 这是 single-pass architecture 的核心容量设定。
- **Search range**: world model 1.6–5.4 M；主报告模型约 5.4 M
- **Sensitivity**: 中；capacity probe 显示更大模型在 diffusion points 上更好，但只有 2 points 与 1 seed。
- **Source**: Sec 4.2 Architecture；Sec 5.3；Sec 5.6

## conditioning 机制
- **Value**: adaLN-Zero conditioning；conditioning vector 汇总 sinusoidal timestep embedding、pooled present latent、per-token Fourier action embedding
- **Rationale**: 将时间步、当前场景和逐 horizon 动作共同注入 transformer block。
- **Search range**: 每个 block 使用 adaLN-Zero，gate 初始化为 zero
- **Sensitivity**: 中；论文采用 DiT formulation，但未单独 ablate adaLN-Zero。
- **Source**: Sec 4.2 Architecture

## Fourier action embedding
- **Value**: learned Fourier features；64 frequencies per dimension；per-token embeddings 随 horizon 变化
- **Rationale**: 让每个预测步的 action conditioning 不同，使 self-attention 可利用 perstep temporal structure。
- **Search range**: N_f = 64
- **Sensitivity**: 中高；action-seq conditioning 对 DiT 的收益被部分确认。
- **Source**: Sec 4.2 Fourier action embedding；Sec 5.2

## residual anchoring
- **Value**: 预测 residual，并从 present z_t broadcast 到所有 horizon positions
- **Rationale**: 稳定 early training，并让失败模式退化为 copy present 而不是 random noise。
- **Search range**: single-pass 模型共享 present anchor；jump model 改为 per-step reanchoring
- **Sensitivity**: 高；它既是必要因素，也是 single-pass motion limitation 的根因。
- **Source**: Sec 4.2 Residual anchoring；Sec 5.4 Diagnosis

## prediction horizons
- **Value**: H ∈ {4, 8, 16}，对应 2, 4, 8 s at 2 Hz
- **Rationale**: 多 horizon targets 覆盖短到 8 秒未来，并用于测试长 horizon 是否有利于 DiT。
- **Search range**: 4, 8, 16 steps
- **Sensitivity**: 中；H3 显示 longer horizons do not favor DiT。
- **Source**: Sec 3 Multi-horizon targets；Sec 5.2

## direct regression baseline
- **Value**: same architecture at tau=0，无 noise，single forward pass；present embedding replicated
- **Rationale**: 作为强 deterministic baseline，用来区分生成式 sampling 与架构本身贡献。
- **Search range**: Direct regression；matched MLP baseline 384→512→384 with GELU residual output
- **Sensitivity**: 高；distortion metrics 偏好该 baseline，distribution metrics 偏好 diffusion。
- **Source**: Sec 4.2 Direct regression baseline；Sec 5.3

## jump world model
- **Value**: 1.7 M-parameter，n_blocks=2，dim 192；预测单个 Δ=4 transition，并在推理时 4-step open-loop re-anchoring
- **Rationale**: 针对 shared-present anchor 导致的 motion limitation，把预测改写成链式 re-anchoring。
- **Search range**: Δ=4；四次 sequential transitions 到 z_{t+16}
- **Sensitivity**: 高；该 reparameterization 恢复 coarse motion direction。
- **Source**: Sec 4.4 Chain-anchor jump model；Sec 5.4
