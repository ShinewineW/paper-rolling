# Claims

## C1: Navsim 闭环规划性能领先
- **Statement**: DriveDreamer-Policy 在 Navsim v1 和 Navsim v2 的闭环规划评测中，相比论文列出的现有方法取得更强的总体规划表现。
- **Status**: supported
- **Falsification criteria**: 若在相同 Navsim navtest 协议下，表中基线或复现实验的 PDMS/EPDMS 总体规划指标不低于 DriveDreamer-Policy，则该主张被削弱或推翻。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: Table 1 和 Table 2 给出跨 Vision-Based End-to-End Methods、Vision-Language-Action Methods 与 World-Model-Based Methods 的对比，支持其在规划指标上的优势。
- **Tags**: ['improvement', 'generalization']

## C2: 世界生成质量提升
- **Statement**: DriveDreamer-Policy 在 Navsim 世界生成评测中，同时呈现更好的视频生成质量和深度预测质量。
- **Status**: supported
- **Falsification criteria**: 若在相同 Navsim 视频与深度评测协议下，PWM 或 PPD 相关变体在 LPIPS、PSNR、FVD、AbsRel 或阈值准确率上整体优于 DriveDreamer-Policy，则该主张不成立。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: Table 3(a) 比较视频生成，Table 3(b) 比较深度预测；论文将改进归因于 LLM world embeddings 对生成专家的条件引导。
- **Tags**: ['improvement']

## C3: 世界学习增强规划
- **Statement**: 加入世界学习相较 action-only 训练能够改善规划表现，且 depth 与 video 联合训练带来的规划收益最大。
- **Status**: supported
- **Falsification criteria**: 若在相同训练预算下，Without World Learning 或单一世界模态策略达到或超过 depth+video+action 的规划表现，则该因果解释被削弱。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: Table 4 将 Without World Learning、depth+action、video+action 与完整 depth+video+action 放在同一训练预算下比较，支持深度几何与视频时序演化互补的解释。
- **Tags**: ['improvement', 'causal']

## C4: 深度学习帮助视频生成
- **Statement**: 在同样训练数据和计算预算下，联合深度学习并让 video queries 因果条件化于 depth queries，可以提升未来视频生成质量。
- **Status**: supported
- **Falsification criteria**: 若去掉 depth learning 的 video-only 变体在相同设置下视频指标整体不差于 With Depth Learning，则该主张不成立。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: Table 5 直接比较 Without Depth Learning 与 With Depth Learning，论文据此认为 depth 提供了有效的 3D scaffold。
- **Tags**: ['improvement', 'causal']

## C5: 更大查询预算提高容量
- **Statement**: 增加 depth、video 与 action query tokens 的预算，通常能提升世界生成和规划表现。
- **Status**: supported
- **Falsification criteria**: 若较小查询预算在相同设置下整体世界生成与规划指标优于默认查询预算，则查询容量解释被削弱。
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: Table 6 将较小查询预算与默认查询预算比较，论文解释为更多 query tokens 提供了更高容量的上下文槽位。
- **Tags**: ['improvement', 'descriptive']
