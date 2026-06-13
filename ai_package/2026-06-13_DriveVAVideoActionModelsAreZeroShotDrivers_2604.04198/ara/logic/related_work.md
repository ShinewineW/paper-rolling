# Related Work

## R1: Wan, T., Wang, A., Ai, B., Wen, B., Mao, C., Xie, C.W., Chen, D., et al.: Wan: Open and advanced large-scale video generative models. arXiv preprint arXiv:2503.20314 (2025)
- **DOI**: 
- **Type**: video generation backbone
- **Delta**:
  - What changed: DriveVA 采用 Wan2.2-TI2V-5B 的 text encoder 与 3D-causal VAE，并将其作为预训练 video generation backbone 进行 driving-domain 适配。
  - Why: 论文认为大规模视频生成模型包含时空动态与物理合理性先验，可为零样本驾驶规划提供更强迁移基础。
- **Claims affected**: ['C5']
- **Adopted elements**: ['Wan2.2-TI2V-5B', 'text encoder', '3D-causal VAE', 'video priors']

## R2: Peebles, W., Xie, S.: Scalable diffusion models with transformers. In: Proceedings of the IEEE/CVF international conference on computer vision. pp. 4195–4205 (2023)
- **DOI**: 
- **Type**: architecture
- **Delta**:
  - What changed: DriveVA 使用 DiT-based decoder 同时预测 future video latents 与 future action tokens。
  - Why: 该结构让 video 与 action tokens 在 shared latent generative process 中交互，从而支撑统一解码和一致性建模。
- **Claims affected**: ['C3', 'C4']
- **Adopted elements**: ['DiT', 'shared latent space', 'bidirectional interaction']

## R3: Teed, Z., Lipson, L., Deng, J.: Deep patch visual odometry. Advances in Neural Information Processing Systems 36, 39033–39051 (2023)
- **DOI**: 
- **Type**: verification tool
- **Delta**:
  - What changed: 论文使用 DPVO 对 ground-truth future videos 与 generated future videos 进行 camera trajectory reconstruction。
  - Why: DPVO 提供外部视觉里程计检验，用来判断生成视频隐含运动是否与参考轨迹或预测轨迹一致。
- **Claims affected**: ['C3']
- **Adopted elements**: ['DPVO', '2D similarity alignment', 'Avg.L2']

## R4: Zhao, Z., Fu, T., Wang, Y., Wang, L., Lu, H.: From forecasting to planning: Policy world model for collaborative state-action prediction. arXiv preprint arXiv:2510.19654 (2025)
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: DriveVA 与 PWM 在 NAVSIM、zero-shot nuScenes 和 Bench2Drive 上对比，并指出 PWM 在零样本可视化中存在 video-trajectory mismatch。
  - Why: PWM 是论文重点比较的 state-of-the-art world-model-based planner，用于证明 DriveVA 的零样本泛化和一致性优势。
- **Claims affected**: ['C1', 'C2', 'C3']
- **Adopted elements**: ['WorldModel Methods baseline', 'zero-shot comparison']

## R5: Li, Y., Shang, S., Liu, W., Zhan, B., Wang, H., Wang, Y., Chen, Y., Wang, X., An, Y., Tang, C., et al.: Drivevla-w0: World models amplify data scaling law in autonomous driving. arXiv preprint arXiv:2510.12796 (2025)
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: DriveVA 与 DriveVLA-W0 比较，论文强调 DriveVA 不把视觉预测仅作为辅助信号，而是联合生成视频与动作。
  - Why: 该对比用于界定 DriveVA 相对已有 VLA-world-model 方法在闭环表现和零样本迁移上的差异。
- **Claims affected**: ['C1', 'C2', 'C4']
- **Adopted elements**: ['VLA-World Model baseline']

## R6: Ye, S., Ge, Y., Zheng, K., Gao, S., Yu, S., Kurian, G., Indupuru, S., Tan, Y.L., Zhu, C., Xiang, J., et al.: World action models are zero-shot policies. arXiv preprint arXiv:2602.15922 (2026)
- **DOI**: 
- **Type**: conceptual prior
- **Delta**:
  - What changed: 论文借鉴 VAM-style approaches 的方向，将视频扩散 backbone 的时空先验用于动作生成与规划。
  - Why: 相关工作支持作者关于 video-action model 可以把视觉未来与动作决策耦合起来的研究动机。
- **Claims affected**: ['C3', 'C5']
- **Adopted elements**: ['VAM-style approaches', 'zero-shot policy framing']

## R7: Xia, T., Li, Y., Zhou, L., Yao, J., Xiong, K., Sun, H., Wang, B., Ma, K., Chen, G., Ye, H., et al.: Drivelaw: Unifying planning and video generation in a latent driving world. arXiv preprint arXiv:2512.23421 (2025)
- **DOI**: 
- **Type**: related method
- **Delta**:
  - What changed: DriveVA 与 DriveLaW 等 visually predictive approaches 的区别在于不依赖松耦合或多阶段优化，而是在单一 generative process 内联合解码。
  - Why: 该对比用于说明本文针对 video-action mismatch 的结构性改动。
- **Claims affected**: ['C3', 'C4']
- **Adopted elements**: ['planning and video generation framing']

## R8: Zhang, K., Tang, Z., Hu, X., Pan, X., Guo, X., Liu, Y., Huang, J., Yuan, L., Zhang, Q., Long, X.X., et al.: Epona: Autoregressive diffusion world model for autonomous driving. arXiv preprint arXiv:2506.24113 (2025)
- **DOI**: 
- **Type**: baseline
- **Delta**:
  - What changed: DriveVA 在 NAVSIM 与 nuScenes 规划表中同 Epona 对比，突出无需 nuScenes finetune 的表现。
  - Why: Epona 代表 visually predictive world model baseline，有助于界定 DriveVA 的闭环与零样本优势。
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['world model baseline']
