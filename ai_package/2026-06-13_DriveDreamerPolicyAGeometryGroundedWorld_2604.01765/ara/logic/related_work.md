# Related Work

## R1: Epona (Zhang et al., 2025)
- **DOI**: 
- **Type**: driving world-action model
- **Delta**:
  - What changed: Epona 使用 autoregressive diffusion world model，将 causal temporal latents 与 per-step diffusion generation 解耦以支持 long-horizon video rollout 和 trajectory planning；DriveDreamer-Policy 在同一世界动作方向上加入 explicit depth generation 与 depth→video→action 条件路径。
  - Why: 论文认为现有 world-action models 往往集中于 image/video prediction 或 latent rollouts，缺少 explicit geometric grounding。
- **Claims affected**: ['C1', 'C3']
- **Adopted elements**: ['world-action model', 'future world generation', 'trajectory planning']

## R2: PWM (Zhao et al., 2025)
- **DOI**: 
- **Type**: policy world model
- **Delta**:
  - What changed: PWM 将 unified autoregressive transformer 作为 Policy World Model，执行 action-free future forecasting 与 collaborative state-action prediction；DriveDreamer-Policy 保留规划与生成统一目标，但改为通过 LLM query embeddings 条件化 depth、video 与 action experts。
  - Why: PWM 是论文在 planning 和 video generation 中直接比较的重要 world-model-based baseline，用于显示 DriveDreamer-Policy 的规划与生成改进。
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['future forecasting', 'state-action prediction', 'world-model-based planning baseline']

## R3: DriveVLA-W0 (Li et al., 2025)
- **DOI**: 
- **Type**: driving VLA model
- **Delta**:
  - What changed: DriveVLA-W0 通过 future-image world modeling 增强 VLA 学习，并使用 lightweight MoE action expert；DriveDreamer-Policy 将 image-token world prediction 替换为 diffusion video generation head，并进一步加入 depth-based 3D representation。
  - Why: 论文将自身定位为对 end-to-end VLA 方向的扩展，用 explicit geometry grounding 解决 missing-geometry grounding。
- **Claims affected**: ['C1', 'C3']
- **Adopted elements**: ['LLM/VLA planning', 'world modeling supervision', 'lightweight action expert idea']

## R4: PPD (Xu et al., 2025)
- **DOI**: 
- **Type**: depth foundation model
- **Delta**:
  - What changed: PPD 是 Pixel-perfect depth with semantics-prompted diffusion transformers；DriveDreamer-Policy 的 depth generator 初始化自 PPD，并通过 LLM world depth embeddings 条件化以提升 Navsim 深度预测。
  - Why: 论文选择 PPD 作为 depth generator 初始化来源和深度预测对比对象，以检验 DriveDreamer-Policy 的 depth learning 是否超越 PPD 变体。
- **Claims affected**: ['C2', 'C4']
- **Adopted elements**: ['depth generator initialization', 'diffusion transformer depth prediction', 'depth baseline']

## R5: UniPGT (Lu et al., 2025)
- **DOI**: 
- **Type**: unified understanding generation planning model
- **Delta**:
  - What changed: UniPGT 通过 hybrid experts 将 pretrained VLM 与 video generator 集成，统一 understanding、video generation 和 trajectory planning；DriveDreamer-Policy 进一步让 fixed-size latent queries 作为 cross-attention keys，使 generative experts 首次联合预测 depth、video 和 action。
  - Why: 该工作说明统一理解、生成和规划是相关趋势，而本文的变化重点在 depth modality 与 causal 3D→2D→1D conditioning。
- **Claims affected**: ['C1', 'C2']
- **Adopted elements**: ['pretrained VLM integration', 'video generation', 'trajectory planning']
