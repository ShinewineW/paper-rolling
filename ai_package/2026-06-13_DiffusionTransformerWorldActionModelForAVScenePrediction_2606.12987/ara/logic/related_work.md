# Related Work

## R1: [5] Y. Blau and T. Michaeli. The perception-distortion tradeoff. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 6228–6237, 2018.
- **DOI**: 
- **Type**: theory
- **Delta**:
  - What changed: 本文把perception-distortion tradeoff用于AV latent world model评估，解释为什么direct regression在distortion metrics上占优却生成模糊条件均值。
  - Why: 该理论为C2提供评价视角，使FID/KID与CosSim的分歧不被误读为单纯模型失败。
- **Claims affected**: ['C2']
- **Adopted elements**: ['perception-distortion tradeoff', 'distribution metrics与distortion metrics并列评估']

## R2: [16] W. Peebles and S. Xie. Scalable diffusion models with transformers. In International Conference on Computer Vision (ICCV), 2023.
- **DOI**: 
- **Type**: method
- **Delta**:
  - What changed: 本文采用DiT formulation和adaLN-Zero conditioning，但把它放入紧凑AV latent world-action setting中做诊断。
  - Why: 该工作提供transformer diffusion骨架，本文的贡献是分析其在compact latent中何时有效。
- **Claims affected**: ['C5']
- **Adopted elements**: ['DiT', 'adaLN-Zero conditioning']

## R3: [19] R. Rombach, A. Blattmann, D. Lorenz, P. Esser, and B. Ommer. High-resolution image synthesis with latent diffusion models. In IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2022.
- **DOI**: 
- **Type**: method
- **Delta**:
  - What changed: 本文使用frozen SD-VAE构建encode-predict-decode管线，在VAE latent中预测未来场景。
  - Why: SD-VAE提供可解码的紧凑空间，使C2的distribution evaluation和C3的decoded motion diagnosis可执行。
- **Claims affected**: ['C2', 'C3']
- **Adopted elements**: ['frozen SD-VAE', 'latent encode-predict-decode']

## R4: [21] J. Song, C. Meng, and S. Ermon. Denoising diffusion implicit models. In International Conference on Learning Representations (ICLR), 2021.
- **DOI**: 
- **Type**: method
- **Delta**:
  - What changed: 本文在inference中使用DDIM deterministic sampling，从noise逐步refine latent predictions。
  - Why: sampling方式是C5中matching target uncertainty设计组合的一部分。
- **Claims affected**: ['C5']
- **Adopted elements**: ['DDIM sampling']

## R5: [22] M. Tancik et al. Fourier features let networks learn high frequency functions in low dimensional domains. In Advances in Neural Information Processing Systems, 2020.
- **DOI**: 
- **Type**: method
- **Delta**:
  - What changed: 本文用learned Fourier features嵌入连续ego-actions，使每个预测horizon的action conditioning可变化。
  - Why: 该嵌入支撑world-action conditioning，并服务于C4的steering controllability实验。
- **Claims affected**: ['C4', 'C5']
- **Adopted elements**: ['learned Fourier action embedding']

## R6: [3] A. Bardes et al. V-JEPA 2: Self-supervised video models enable understanding, prediction and planning. arXiv preprint arXiv:2506.09985, 2025.
- **DOI**: 
- **Type**: representation
- **Delta**:
  - What changed: 本文将V-JEPA2 rep64与V-JEPA2 rep1及其他冻结编码器放入统一AV action prediction benchmark。
  - Why: 该相关工作提供时间视频表征，C1显示其在steering prediction上优于单帧表征。
- **Claims affected**: ['C1']
- **Adopted elements**: ['V-JEPA2 rep64', 'V-JEPA2 rep1']

## R7: [12] A. Hu et al. GAIA-1: A generative world model with integrated action understanding. arXiv preprint arXiv:2309.17080, 2023.
- **DOI**: 
- **Type**: world_model
- **Delta**:
  - What changed: 本文没有追求GAIA-1式大规模pixel或video generation，而是在compact regime中隔离设计因素与评价指标。
  - Why: 该对比界定了论文范围：C5的结论来自可控小规模诊断，而不是大规模系统展示。
- **Claims affected**: ['C5']
- **Adopted elements**: []

## R8: [20] C. Shi, J. Xu, S. Shi, K. Sheng, B. Zhang, and L. Jiang. DriveWAM: Video generative priors enable scalable worldaction modeling for autonomous driving. arXiv preprint arXiv:2605.28544, 2026.
- **DOI**: 
- **Type**: concurrent_work
- **Delta**:
  - What changed: 本文将DriveWAM作为concurrent work对照，强调自身贡献是compact regime中的controlled analysis。
  - Why: 该对照帮助解释C5的适用边界：本文不是scaled system，而是设计因素诊断。
- **Claims affected**: ['C5']
- **Adopted elements**: []
