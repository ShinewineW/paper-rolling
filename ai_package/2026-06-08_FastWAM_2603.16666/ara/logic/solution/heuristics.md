# Heuristics

## H1: 结构化注意力掩码：训练时动作 tokens 仅在动作分支内双向注意，并可访问干净第一帧 tokens，不得访问未来视频噪声 tokens；干净第一帧 tokens 作为共享视觉锚点，不访问任何其他 tokens；未来视频 tokens 在视频分支内双向注意并可访问第一帧 tokens。推理时完整去除未来视频分支而不改变动作分支的注意力模式。
- **Rationale**: 防止未来信息泄露进动作分支，同时保证训练期与推理期动作分支感受野完全一致，实现视频协同训练与测试时动作生成的结构性解耦。
- **Sensitivity**: 该掩码设计是 Fast-WAM 与 Fast-WAM-Joint 的本质区别；若允许动作 tokens 访问未来视频 tokens，则变为联合生成范式。
- **Bounds**: 布尔性结构设计，无数值超参数。
- **Code ref**: [论文§3.2 图2b（训练掩码与推理掩码示意）]
- **Source**: §3.2 Model Architecture

## H2: 视频帧时序下采样4×，每个动作 chunk 对应9个视频帧。
- **Rationale**: 压缩视频 token 序列长度以降低显存和计算开销，同时覆盖足够时序跨度的动态信息。
- **Sensitivity**: 下采样率影响视频协同训练的时序分辨率；论文未对此值进行消融。
- **Bounds**: 时序下采样率=4；帧数=9帧/chunk。
- **Code ref**: [论文§4.1]
- **Source**: §4.1 Implementation Details

## H3: 动作 horizon 固定为 H=32，每次输出32步动作序列；动作专家 DiT hidden dim 为 d_a=1024（约1B参数），总模型参数约6B。
- **Rationale**: H=32 覆盖足够长的执行窗口，减少策略查询频率；d_a=1024 在容量与计算效率之间平衡，使动作专家体量约为视频 DiT 的1/5。
- **Sensitivity**: H 值影响单次推理覆盖的动作窗口；d_a 影响动作专家表达能力；论文未对两者进行消融。
- **Bounds**: H=32；d_a=1024。
- **Code ref**: [论文§4.1]
- **Source**: §4.1 Implementation Details

## H4: 推理时动作去噪步数=10；分类器自由引导 (CFG) 系数=1.0（不使用额外无条件前向）。
- **Rationale**: 10步流匹配去噪在生成质量与推理速度之间取得平衡；CFG=1.0 避免引入额外前向开销。
- **Sensitivity**: 去噪步数直接影响推理延迟，步数增加则延迟增加；论文未消融步数选择。
- **Bounds**: 去噪步数=10；CFG scale=1.0。
- **Code ref**: [论文§4.1]
- **Source**: §4.1 Implementation Details

## H5: 训练与推理均采用 logit-normal 分布对时间步 t 采样，遵循 Wan2.2-5B [36] 的原始噪声调度配置。
- **Rationale**: Logit-normal 分布将训练信号集中在中间噪声水平，有助于流匹配训练稳定性；沿用骨干配置可充分兼容预训练权重。
- **Sensitivity**: 沿用 Wan2.2-5B 原始配置，论文未独立消融此调度选择。
- **Bounds**: 与文献[36] Wan2.2-5B 配置一致。
- **Code ref**: [论文§4.1]
- **Source**: §4.1 Implementation Details，参照文献[36]

## H6: Fast-WAM-IDM 变体训练时以概率 p=0.5 对 ground-truth 视频 tokens 施加噪声增强。
- **Rationale**: 仿照 LingBot-VA [3] 的配置，缓解训练时使用干净视频与推理时使用生成视频之间的分布偏移问题。
- **Sensitivity**: 仅适用于 Fast-WAM-IDM 变体，不适用于 Fast-WAM；p 过小则分布偏移更严重，p 过大则失去干净视频监督信号。
- **Bounds**: p=0.5（固定值）；仅用于 Fast-WAM-IDM。
- **Code ref**: [论文§4.1]
- **Source**: §4.1 Implementation Details，参照文献[3]
