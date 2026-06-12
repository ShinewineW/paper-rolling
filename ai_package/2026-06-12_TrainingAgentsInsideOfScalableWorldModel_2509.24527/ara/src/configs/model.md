## 总参数量
- **Value**: 2B parameters
- **Rationale**: 高容量 world model 用于复杂 Minecraft object interactions 与 game mechanics。
- **Search range**: tokenizer 400M；dynamics model 1.6B。
- **Sensitivity**: 高；模型容量与复杂交互预测质量直接相关。
- **Source**: Sec 4

## tokenizer 参数量
- **Value**: 400M
- **Rationale**: 负责把视频帧压缩为 dynamics model 可消费与生成的连续表示。
- **Search range**: 论文只报告 400M。
- **Sensitivity**: 中；瓶颈表示质量会影响后续 dynamics。
- **Source**: Sec 4

## dynamics model 参数量
- **Value**: 1.6B
- **Rationale**: 负责基于交错动作与 tokenizer 表示预测未来表示。
- **Search range**: 论文只报告 1.6B。
- **Sensitivity**: 高；是交互式 world model 的主要容量来源。
- **Source**: Sec 4

## 共享 transformer 架构
- **Value**: tokenizer 与 dynamics model 都使用 block-causal efficient transformer
- **Rationale**: 同一类架构支持因果时间建模、空间与时间维度建模以及交互式逐帧解码。
- **Search range**: 论文未报告替代共享策略。
- **Sensitivity**: 高；是实现高容量与快速推理的核心结构选择。
- **Source**: Fig 2; Sec 3.4

## 基础 transformer 组件
- **Value**: pre-layer RMSNorm、RoPE、SwiGLU、QKNorm、attention logit soft capping
- **Rationale**: 在标准 transformer 基础上增加稳定性组件，以支持大规模 world model 训练。
- **Search range**: 论文未给出每个组件的超参范围。
- **Sensitivity**: 中；论文将 QKNorm 与 logit soft capping 明确关联到训练稳定性。
- **Source**: Sec 3.4

## attention 分解
- **Value**: space-only 与 time-only attention；temporal attention 每 4 layers 使用一次
- **Rationale**: 降低 dense attention 成本，并保留长上下文交互式生成能力。
- **Search range**: temporal attention 间隔显式为每 4 layers。
- **Sensitivity**: 高；ablation 显示它同时影响速度与生成质量。
- **Source**: Sec 3.4; Sec 4.4

## GQA
- **Value**: dynamics 中所有 attention layers 使用 GQA
- **Rationale**: 多个 query heads 共享 key-value heads，降低 KV cache 大小并提升推理效率。
- **Search range**: 论文未报告 GQA 分组数。
- **Sensitivity**: 中；论文称其进一步加速生成且不降低表现。
- **Source**: Sec 3.4; Sec 4.4

## Minecraft spatial tokens
- **Value**: N_z=256
- **Rationale**: 增加 spatial tokens 改善视觉质量，并在 Minecraft 设置中用于 dynamics model 表示。
- **Search range**: ablation 从 N_z=64 增加到 128，再到 256。
- **Sensitivity**: 高；论文称更多 spatial tokens 改善复杂交互预测。
- **Source**: Sec 4; Table 2; Appendix A

## Minecraft context length
- **Value**: 192 frames
- **Rationale**: 较长时间上下文支持更一致的交互式生成。
- **Search range**: Minecraft 使用 192 frames；real world datasets 使用 96 frames。
- **Sensitivity**: 高；论文指出 Dreamer 4 相比先前模型有更长 context，但仍受短记忆限制。
- **Source**: Sec 4; Appendix A; Sec 5

## Minecraft batch length
- **Value**: 256
- **Rationale**: batch length 需要长于 context length，以避免模型总在 context 开头看到 start frame 并支持长度泛化。
- **Search range**: Minecraft 使用 T1=64 与 T2=256；real world datasets 使用 T1=32 与 T2=128。
- **Sensitivity**: 中；alternating batch lengths 被列为提升训练与中间生成可诊断性的设计。
- **Source**: Sec 3.4; Sec 4; Appendix A

## action encoding
- **Value**: keyboard 为 23 binary distributions；mouse 为 121 classes
- **Rationale**: 保持低层 keyboard 与 mouse action space，使 agent 与 VPT evaluation protocol 对齐。
- **Search range**: mouse 由 11 bins per coordinate 枚举为 121 combinations。
- **Sensitivity**: 高；动作表示直接决定 action conditioning 与 Minecraft 控制粒度。
- **Source**: Sec 4.1; Appendix A

## real world dataset 设置
- **Value**: 512 spatial tokens；96 frames context length；128 batch length
- **Rationale**: SOAR Robotics 与 Epic Kitchens 使用相同的 real world dynamics 配置。
- **Search range**: Minecraft 对应用 256 spatial tokens、192 frames context length、256 batch length。
- **Sensitivity**: 中；体现数据域与输入分辨率下的配置调整。
- **Source**: Sec 4; Appendix A
