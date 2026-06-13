# Heuristics

## H1: 采用严格 F→A 的 interleaved frame-action generation，而不是先完整预测世界再规划。
- **Rationale**: 论文指出这种 step-wise interaction 让 action query 在每个未来帧之后反馈给 LLM，使后续生成持续受已预测状态约束，缓解固定初始意图导致的 open-loop imagination 漂移。
- **Sensitivity**: 对时间对齐敏感；Table 4 显示 Scheme E 与 NAVSIM 的 2 Hz planning/evaluation protocol 对齐时最好，而高频或滑窗 action 监督会带来协议错配或冲突监督。
- **Bounds**: 默认生成 N = 8 个未来帧，每帧间隔 0.5 seconds，对应 4.0-second prediction horizon。
- **Code ref**: [interleaved_frame_action_loop]
- **Source**: Sec. 3 Interleaved frame-action generation；Sec. 4.3 Table 4

## H2: 对视觉 token 使用 Dynamic Focal Loss 的动态区域加权。
- **Rationale**: 论文引用 [62] 指出单纯 cross-entropy 会让大量相邻帧 token 保持不变，因此用 \omega 对变化 token 赋予更高权重，以强调 temporally varying image regions。
- **Sensitivity**: 依赖 \alpha 与 \beta 的相对大小；论文只声明 \alpha > \beta，未给出具体取值。
- **Bounds**: 作用在每个未来帧的 L 个 predicted visual tokens 上，并只属于训练期 visual prediction 监督。
- **Code ref**: [dynamic_weighted_cross_entropy]
- **Source**: Sec. 3 Training objectives

## H3: 历史视觉输入拆成 contextual tokens 与 dynamic tokens。
- **Rationale**: contextual tokens 提供高分辨率场景语义与结构信息，dynamic tokens 以 10 Hz 低分辨率采样捕捉细粒度运动线索；Table 5 说明二者结合提供更好的整体平衡。
- **Sensitivity**: 仅用 dynamic tokens 明显削弱规划与生成质量；仅用 contextual tokens 仍保留较强空间结构，但运动线索不足。
- **Bounds**: 实现中高分辨率分支处理 256 × 448 并产生 448 contextual tokens，低分辨率分支处理 128 × 224 并产生 28 dynamic tokens。
- **Code ref**: [context_dynamic_tokenizer]
- **Source**: Sec. 3 Inputs and tokenization；Sec. 4.1 Implementation details；Sec. 4.3 Table 5

## H4: 用 Depth Anything 3 的单目深度，经 CDE / DDE 与视觉 token embedding 做 cross-attention 融合。
- **Rationale**: 论文称深度提供 complementary geometric information，用于增强 future frame prediction；Fig. 5 描述 depth fusion 在更长时间与转弯场景中保持更清晰空间布局。
- **Sensitivity**: 深度融合质量依赖深度估计与跨模块融合稳定性；论文因此采用 two-stage progressive paradigm。
- **Bounds**: 深度 map 被 resize 到 256×448 与 128×224 两种分辨率，分别送入 CDE 与 DDE。
- **Code ref**: [depth_cross_attention_fusion]
- **Source**: Sec. 3 Depth integration；Sec. 4.1 Stage 1 / Stage 2

## H5: 推理时复用 KV-cache，只计算新增 token 的 attention。
- **Rationale**: 论文说明 KV-cache 存储并复用 previous steps 的 key/value representations，避免每一步重新处理完整序列，提高自回归 interleaved inference 效率。
- **Sensitivity**: 必须保持 attention masking scheme 与训练一致，否则历史 token、当前帧内 token 与因果时间关系可能不一致。
- **Bounds**: 仅用于推理期效率优化，不是训练目标项。
- **Code ref**: [kv_cache_autoregressive_inference]
- **Source**: Sec. 3 Inference
