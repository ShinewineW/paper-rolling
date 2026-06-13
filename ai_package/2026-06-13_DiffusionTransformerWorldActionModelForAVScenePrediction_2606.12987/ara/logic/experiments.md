# Experiments

## E1: 冻结编码器动作预测基准
- **Verifies**: C1
- **Setup**:
  - Model: shared MLP probe over frozen encoder embeddings
  - Hardware: 论文未说明
  - Dataset: nuScenes v1.0-trainval按scene划分后的held-out test split
  - System: 六种冻结视觉编码器，统一投影到pooled latent后预测steering和acceleration
- **Procedure**:
  1. 为每个keyframe或clip抽取冻结视觉表征。
  2. 用相同MLP probe从表征预测steering和acceleration。
  3. 按scene聚合，在held-out test scenes上计算RMSE并用bootstrap给出置信区间。
  4. 比较V-JEPA2 rep64与V-JEPA2 rep1以及其他单帧编码器。
- **Metrics**: ['Steer RMSE', 'Accel RMSE']
- **Expected outcome**: V-JEPA2 rep64应在steering上优于单帧编码器，acceleration差距更小。
- **Baselines**: ['V-JEPA2 rep1', 'DINOv2-S/14', 'CLIP ViT-B/32', 'ViT-S/16', 'VQ-VAE Tracker']
- **Dependencies**: ['nuScenes CAN-bus actions', 'frozen visual encoders', 'scene-level evaluation harness']

## E2: SD-VAE管线的perception-distortion frontier评估
- **Verifies**: C2
- **Setup**:
  - Model: AnchoredVAEDiT diffusion与direct regression baseline
  - Hardware: 论文未说明
  - Dataset: nuScenes held-out test frames decoded through frozen Stable-Diffusion VAE
  - System: 当前front-camera latent和ego-actions输入，预测future scene latents并由frozen decoder渲染
- **Procedure**:
  1. 用direct regression和diffusion模型分别预测future VAE latents。
  2. 对diffusion输出应用仅由training split估计的per-channel calibration。
  3. 将预测latents解码为frames。
  4. 同时计算distribution metrics和distortion metrics，比较direct、raw diffusion、latent interpolation与calibrated diffusion。
- **Metrics**: ['KID', 'FID', 'CosSim']
- **Expected outcome**: direct regression应在distortion方向更优，calibrated diffusion应在distribution quality方向更优。
- **Baselines**: ['Direct regression', 'Diffusion raw', 'latent interpolation', 'VAE-GT ceiling']
- **Dependencies**: ['frozen Stable-Diffusion VAE', 'torchmetrics FID/KID', 'train-derived calibration']

## E3: motion fidelity诊断与chain-anchor jump model
- **Verifies**: C3
- **Setup**:
  - Model: compact Jump DiT与single-pass world model
  - Hardware: 论文未说明
  - Dataset: held-out nuScenes scenes
  - System: single Δt jump transition经open-loop chain逐步re-anchoring到更远horizon
- **Procedure**:
  1. 解码连续预测帧并分解相邻帧差异。
  2. 用Gaussian blur得到low-frequency coherent scene motion，用残差得到high-frequency texture variation。
  3. 计算image-plane displacement的magnitude ratio和direction correlation。
  4. 比较single-pass模型与chain-anchor jump model在open-loop own anchors设置下的运动表现。
- **Metrics**: ['low-frequency consecutive L2', 'high-frequency consecutive L2', 'image-plane displacement magnitude ratio', 'direction correlation']
- **Expected outcome**: jump model应比shared-present single-pass模型更能恢复coherent motion和motion direction。
- **Baselines**: ['single-pass diffusion model', 'single-pass direct model']
- **Dependencies**: ['motion decomposition pipeline', 'frozen VAE decoder', 'open-loop chain inference']

## E4: steering sweep动作可控性实验
- **Verifies**: C4
- **Setup**:
  - Model: diffusion world model与direct regression baseline
  - Hardware: 论文未说明
  - Dataset: held-out nuScenes windows
  - System: 固定diffusion noise，扫描steering输入并测量预测场景水平位移
- **Procedure**:
  1. 保持输入scene和diffusion noise固定。
  2. 在training distribution范围内扫描steering值。
  3. 在远期预测帧上测量horizontal scene displacement。
  4. 用rank correlation和sign correctness判断steering与shift是否单调一致。
- **Metrics**: ['Spearman correlation', 'sign correctness', 'inverse-control chance error ratio']
- **Expected outcome**: diffusion模型应呈现单调steering controllability，direct regression应缺少稳定相关性。
- **Baselines**: ['Direct regression']
- **Dependencies**: ['steering perturbation pipeline', 'scene displacement estimator', 'fixed-noise diffusion sampling']

## E5: compact latent DiT诊断链
- **Verifies**: C5
- **Setup**:
  - Model: DiT direct、DiT diffusion与matched MLP residual baseline
  - Hardware: 论文未说明
  - Dataset: nuScenes compact pooled latent与spatial-token latent设置
  - System: 围绕capacity、objective、horizon和action-seq conditioning的controlled diagnostic chain
- **Procedure**:
  1. 先在compact pooled latents中比较DiT和MLP residual baseline。
  2. 切换epsilon prediction与x0 prediction objective，观察collapse与gap recovery。
  3. 改变horizon以检验更长预测是否天然有利于DiT。
  4. 加入per-token action-sequence conditioning并恢复spatial tokens与residual anchoring。
- **Metrics**: ['CosSim', 'DeltaCosSim', 'gap recovery direction', 'matched-parameter comparison']
- **Expected outcome**: x0 objective、spatial tokens、residual anchoring和匹配采样应共同改善DiT表现；capacity或horizon本身不应充分解释收益。
- **Baselines**: ['MLP residual baseline', 'DiT direct', 'epsilon-prediction diffusion']
- **Dependencies**: ['controlled ablation setup', 'matched parameter baselines', 'action-sequence conditioning']
