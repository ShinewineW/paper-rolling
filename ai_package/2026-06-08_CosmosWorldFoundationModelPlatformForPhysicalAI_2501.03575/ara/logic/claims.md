# Claims

## C1: 预训练→后训练范式高效支持多下游物理AI任务
- **Statement**: Cosmos WFM平台采用「预训练→后训练」两阶段范式，通过大规模多样视频数据预训练获得通才WFM，再通过少量领域数据微调即可适配相机控制、机器人操控和自动驾驶等多个物理AI下游任务，后训练模型在各任务上均显著优于从头训练的专用基线
- **Status**: supported
- **Falsification criteria**: 若后训练模型在下游任务中不比从头训练的专用模型更有效，或需要与预训练等量的领域数据才能达到同等性能，则该范式的效率主张不成立
- **Proof**: [E4, E5, E6]
- **Evidence basis**: ['E4', 'E5', 'E6']
- **Interpretation**: 预训练WFM提供的强大视觉物理先验大幅降低了针对具体物理AI应用所需的领域数据量；三类后训练实验（相机控制、机器人操控、自动驾驶）共同验证了此范式的普适性
- **Tags**: ['improvement', 'generalization']

## C2: Cosmos Tokenizer在重建质量和推理速度上均优于现有同类方法
- **Statement**: Cosmos Tokenizer在DAVIS和TokenBench多个基准上的PSNR、SSIM、rFVD等重建指标均超越现有连续和离散视频tokenizer，在A100 GPU上推理速度显著快于同类方法，且参数量更小；在更高压缩率下仍保持优于对比方法低压缩率时的重建质量
- **Status**: supported
- **Falsification criteria**: 若Cosmos Tokenizer在相同压缩率下的PSNR低于对比方法，或在更高压缩率下有明显质量劣势，则此声明不成立
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: Cosmos Tokenizer采用小波变换前处理消除像素冗余、因果时序卷积和注意力设计保证时序因果性、FSQ离散量化避免VQ代码本坍塌，实现了压缩率与重建质量的优越权衡
- **Tags**: ['improvement', 'descriptive']

## C3: 扩散型WFM在3D一致性和视觉质量上普遍优于自回归型WFM
- **Statement**: 在3D一致性评估中，扩散型WFM的Sampson几何误差更低、相机位姿估计成功率更高；在物理对齐评估中，扩散型WFM在多帧条件设置下的像素级预测指标优于自回归型；扩散型WFM的总体感知视觉质量更高
- **Status**: supported
- **Falsification criteria**: 若自回归型WFM在3D一致性指标或物理对齐指标上与扩散型相当或更优，则此声明不成立
- **Proof**: [E2, E3]
- **Evidence basis**: ['E2', 'E3']
- **Interpretation**: 扩散型WFM视觉质量更优，但自回归型WFM具有利用LLM社区推理优化技术（KV缓存、推测解码）的潜力；论文指出二者各有优劣，混合架构是有前景的方向（分析推断，论文明确陈述了前景但未给出混合架构结果）
- **Tags**: ['descriptive', 'causal']

## C4: 后训练相机控制模型在轨迹对齐和视频生成质量上显著优于CamCo
- **Statement**: Cosmos-Predict1-7B-Video2World-Sample-CameraCond在RealEstate10K测试集上的相机位姿估计成功率远高于CamCo，旋转误差和平移误差更小，FID和FVD显著更低，并能克服DL3DV-10K到RealEstate10K的数据分布偏移
- **Status**: supported
- **Falsification criteria**: 若Cosmos相机控制模型的FID/FVD或轨迹对齐误差与CamCo相当，则优越性主张不成立
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 基于强大预训练WFM进行微调的相机控制模型具有更好的3D世界感知和泛化能力，在跨数据集分布偏移下仍能生成高质量3D一致视频
- **Tags**: ['improvement', 'causal']

## C5: 后训练机器人操控模型在指令跟随和动作预测上优于专有基线
- **Statement**: 在指令跟随任务上，Cosmos后训练模型在人类评估的整体偏好率上显著高于VideoLDM-Instruction；在动作条件化次帧预测任务上，Cosmos后训练模型在PSNR、SSIM和FVD上均优于IRASim-Action基线
- **Status**: supported
- **Falsification criteria**: 若Cosmos后训练模型在人类评估偏好率或PSNR/FVD指标上与基线相当或更差，则此声明不成立
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: 预训练WFM提供的强大视觉先验使后训练模型在理解空间关系和物体动态方面具有优势，从而更好地理解操控指令并预测物理合理的机器人动作视频
- **Tags**: ['improvement']

## C6: 后训练多视角自动驾驶世界模型在生成质量和几何一致性上优于VideoLDM基线
- **Statement**: Cosmos多视角驾驶世界模型在FID、FVD、时间Sampson误差（TSE）和跨视角Sampson误差（CSE）上均显著优于VideoLDM-MultiView，附加轨迹控制条件进一步改善多视角几何一致性，且轨迹跟随误差接近真实视频水平
- **Status**: supported
- **Falsification criteria**: 若多视角一致性指标（TSE/CSE）上Cosmos模型与VideoLDM-MultiView相比无显著改善，则此声明不成立
- **Proof**: [E6]
- **Evidence basis**: ['E6']
- **Interpretation**: 借助预训练WFM的视觉物理先验，后训练多视角模型能生成跨相机视角几何上一致、多样且逼真的驾驶场景；轨迹条件输入进一步约束3D空间一致性；该评估使用RDS内部数据集，为相对基线的比较结论
- **Tags**: ['improvement']

## C7: 大规模视频数据管道高效从海量原始视频提取高质量训练片段
- **Statement**: 从约2000万小时原始视频出发，通过分镜检测、多维过滤、VLM标注、语义去重和分片共五步流水线处理，最终提取约1亿个视频片段用于预训练；语义去重阶段删除大量冗余数据；使用TransNetV2端到端分镜检测模型和PyNvideoCodec实现显著高于传统方案的处理吞吐量
- **Status**: supported
- **Falsification criteria**: 若流程提取数据的多样性或质量不足以支撑高质量WFM预训练，则规模数字仍成立而质量声明不成立
- **Proof**: [E8]
- **Evidence basis**: ['E8']
- **Interpretation**: 流水线关键设计：TransNetV2在复杂镜头切换场景下F1高于PySceneDetect；PyNvideoCodec替代ffmpeg视频流处理实现约6.5倍转码吞吐提升；InternVideo2嵌入支持K-means语义去重和视觉搜索引擎
- **Tags**: ['descriptive', 'scoping']

## C8: Medusa多头投机解码显著加速自回归WFM推理且不损失生成质量
- **Statement**: 在自回归WFM中引入Medusa多头解码，4B和5B模型token吞吐量均得到显著提升，前向传播次数大幅减少；结合低分辨率适配后，模型可在8×H100 GPU上实现10 FPS实时视频生成；仅解冻最后两个transformer层和最终unembedding层的微调策略可避免生成质量下降
- **Status**: supported
- **Falsification criteria**: 若Medusa加速导致明显的生成质量下降，或低分辨率适配无法达到实时帧率，则此声明不成立
- **Proof**: [E7]
- **Evidence basis**: ['E7']
- **Interpretation**: 9个Medusa头为吞吐量与性能的最优折中；合并多个Medusa头的权重矩阵为针对视频自回归加速的特定优化，不同于CamCo等原始Medusa实现
- **Tags**: ['improvement']
