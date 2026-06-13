# Heuristics

## H1: 使用固定的离线 trajectory-anchor vocabulary，并在训练与评估期间保持不变。
- **Rationale**: anchor 为候选未来运动提供稳定离散支架，使后续 latent rollout、offset prediction 与 reward ranking 都围绕候选轨迹进行。
- **Sensitivity**: anchor vocabulary 若覆盖不足会限制候选运动空间；论文未给出自适应 anchor 更新策略。
- **Bounds**: Trajectory-anchor vocabulary size 为 256。
- **Code ref**: [trajectory_anchor_vocabulary]
- **Source**: 3.2 Scene representation 与 A Implementation details

## H2: IDM 只解码相邻两帧 imagined BEV states，而不是使用更长窗口。
- **Rationale**: 论文消融称 two-frame design 直接解码 adjacent BEV transitions；four-frame variant 可能稀释 immediate refinement 所需的局部 transition cues。
- **Sensitivity**: 更长 temporal input 可能在长时交互中有信息，但本文结果显示 immediate planning refinement 更偏好相邻 transition。
- **Bounds**: 比较对象为 2 frame 与 4 frame。
- **Code ref**: [IDM_two_frame]
- **Source**: 4.4 Ablation study 与 Table 4

## H3: 对多个 rollout transitions 的 S_k^(u) 与 g_k^(u) 进行平均聚合。
- **Rationale**: 论文将多步 transition cue 汇总成候选级 spatial dynamics map 与 global dynamics feature，供后续 query refinement 使用。
- **Sensitivity**: 平均会压平 transition 间差异；若关键动态只出现在少数 rollout step，可能被弱化。
- **Bounds**: 聚合范围是 u = 0 到 U - 1。
- **Code ref**: [transition_average_pooling]
- **Source**: 3.4.1 Inverse dynamics model

## H4: 同时保留 spatial branch 与 global branch：spatial CrossAttn 抽取局部运动证据，MLN_idm 用 global dynamics 做整体校准。
- **Rationale**: 论文称纯 pooled inverse dynamics feature 对规划过粗，而只保留 spatial branch 又缺少 global calibration；dual-branch 提供 spatially selective and globally calibrated feedback。
- **Sensitivity**: 去掉任一分支都会改变反馈形态；global cue 的融合方式还会影响 query calibration。
- **Bounds**: 消融包含 w/o spatial branch、w/o global branch 与 dual-branch IDM。
- **Code ref**: [dual_branch_IDM]
- **Source**: 3.4.2 Closed-loop query refinement 与 Table 5

## H5: 第二轮及之后 closed-loop refinement 通过 MLN_cl 将当前 query 重新锚定到 initial anchor-conditioned query。
- **Rationale**: 论文明确说明该设计用于 prevent iterative drift；主消融显示最佳为两轮，三轮会 slightly reduce performance，提示可能 overcorrection。
- **Sensitivity**: 固定迭代次数对场景复杂度不自适应；复杂或简单场景可能需要不同 refinement 强度。
- **Bounds**: Closed-loop refinement iterations 为 2；消融包含无 CL、2、3。
- **Code ref**: [MLN_cl_reanchor]
- **Source**: 3.4.2 Closed-loop query refinement、4.4 Ablation study 与 Table 6

## H6: global dynamics feature 使用 MLN-based fusion，而不是 additive 或 concat-MLP。
- **Rationale**: 论文称 MLN-based fusion 是 IDOL 使用的 query-calibration mechanism，能更好整合 global transition information into planning。
- **Sensitivity**: Table 11 显示多种 global fusion 都 strong，但 MLN 是本文最终选择；差异可能依赖同一 spatial branch 设置。
- **Bounds**: 比较对象为 Additive、Concat-MLP、MLN。
- **Code ref**: [MLN_idm]
- **Source**: D Additional ablation studies 与 Table 11
