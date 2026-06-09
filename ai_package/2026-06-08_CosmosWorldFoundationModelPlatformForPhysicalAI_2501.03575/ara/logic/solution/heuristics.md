# Heuristics

## H1: DOVER感知质量评分去除底部15%视频片段
- **Rationale**: 保守阈值在保留足够训练数据的同时剔除感知质量最低片段
- **Sensitivity**: 中等; 阈值变化直接影响训练数据量和质量分布
- **Bounds**: 删除比例=15%
- **Code ref**: [visual_quality_filter]
- **Source**: 第3.3.2节: 「we use the scores to remove clips that are in the bottom 15%」

## H2: 图像美学分数阈值设为3.5
- **Rationale**: 美学对Physical AI训练重要性低于物理真实性, 采用保守偏低阈值避免过度过滤数据
- **Sensitivity**: 低; 论文明确指出美学对Physical AI不关键
- **Bounds**: 阈值=3.5
- **Code ref**: [aesthetic_filter]
- **Source**: 第3.3.2节: 「We set a conservative threshold, i.e., 3.5, since aesthetics are less important for Physical AI」

## H3: TransNetV2镜头检测置信度阈值0.4
- **Rationale**: 在ShotBench多数据集验证0.4在精确率与召回率间取得良好平衡, 优于启发式方法
- **Sensitivity**: 中等; 阈值过低误检增加, 过高遗漏真实镜头边界
- **Bounds**: 置信度∈[0,1], 设置0.4
- **Code ref**: [shot_detection_threshold]
- **Source**: 第3.2.1节: 「We set the confidence threshold to 0.4 for both TransNetV2 and AutoShot」

## H4: 语义去重k-means聚类数k=10,000, 最终去除约30%数据
- **Rationale**: 足够多的簇保证语义粒度和多样性; GPU加速k-means使其在数亿clips规模下计算可行
- **Sensitivity**: 中等; k过小去重粒度粗, k过大计算开销高
- **Bounds**: k=10,000; 去除约30%训练数据
- **Code ref**: [semantic_dedup_kmeans]
- **Source**: 第3.5节: 「k-means...with k=10,000...We remove about 30% of training data during deduplication」

## H5: 视频批次噪声级别相对图像批次按帧数平方根缩放
- **Rationale**: 视频帧间时序冗余导致视频批次梯度量级小于图像批次; 帧数开方缩放对齐两者信噪比改善收敛一致性
- **Sensitivity**: 高; 不加缩放时视频损失收敛明显慢于图像损失
- **Bounds**: 缩放因子=sqrt(视频帧数/参考帧数)
- **Code ref**: [video_noise_scaling]
- **Source**: 第5.1.3节: 「scaling the video batch noise levels by the square root of the frame count relative to image batch noise levels」

## H6: 自回归WFM z-loss系数λ=3×10^{-4}
- **Rationale**: 过大系数影响生成质量, 过小无法防止logit爆炸; 3×10^{-4}为实验确定最优平衡点
- **Sensitivity**: 高; 论文称z-loss对大规模GPU节点训练稳定性至关重要
- **Bounds**: λ=3×10^{-4}
- **Code ref**: [z_loss_lambda]
- **Source**: 第5.2.1节: 「z-loss coefficient λ=3×10^{-4} strikes an optimal balance, effectively stabilizing training without adversely affecting model performance」

## H7: Medusa投机解码头数最优为9
- **Rationale**: 9头在token吞吐量与前向传播次数之间取得最优权衡; 更多头减少前向传播但降低整体吞吐
- **Sensitivity**: 中等; 9头时4B模型获约2.0×吞吐提升和约4.6×前向传播减少
- **Bounds**: 测试范围0至12头, 最优9头
- **Code ref**: [medusa_head_count]
- **Source**: 第5.2.4节: 「We find that 9 Medusa heads yield the best trade-off between computational efficiency and model performance」

## H8: FSQ量化级别(8,8,8,5,5,5)对应词表大小64,000
- **Rationale**: 在离散latent重建质量与词表规模间平衡; 64,000词表与LLM tokenizer规模相近利于集成
- **Sensitivity**: 高; 量化级别直接决定离散tokenizer重建质量和自回归WFM token空间
- **Bounds**: 词表大小=8×8×8×5×5×5=64,000
- **Code ref**: [FSQQuantizer]
- **Source**: 第4.1节: 「FSQ levels, which are (8,8,8,5,5,5). This configuration corresponds to a vocabulary size of 64,000」
