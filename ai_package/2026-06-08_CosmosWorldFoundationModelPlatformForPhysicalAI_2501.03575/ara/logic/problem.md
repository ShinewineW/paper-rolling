# Problem Specification

## Observations

### O1: Physical AI 训练数据扩展极为困难：所需数据必须包含交织的观测与动作序
- **Statement**: Physical AI 训练数据扩展极为困难：所需数据必须包含交织的观测与动作序列，且动作会扰动物理世界、造成系统损坏，探索性动作尤其危险
- **Evidence**: 论文第 1 节指出「scaling training data for Physical AI is much more challenging」
- **Implication**: Physical AI 进展缓慢，亟需数字孪生的世界模型来替代实体数据采集

### O2: 视频 Tokenizer 的压缩率与重建质量存在显著权衡，过高压缩会导致关键视觉
- **Statement**: 视频 Tokenizer 的压缩率与重建质量存在显著权衡，过高压缩会导致关键视觉细节丢失，在离散 Tokenizer 场景下尤为明显
- **Evidence**: Table 5、Table 6 对比不同压缩率下的 PSNR/rFVD，自回归 WFM 离散 Token 输出存在明显模糊伪影（Sec. 5.2.5）
- **Implication**: 需要专门的视频 Tokenizer 设计才能兼顾压缩效率与重建质量，进而支撑高质量 WFM 训练

### O3: 现有视频生成模型（如 VideoLDM）在 3D 一致性与摄像机可控性方面严重不
- **Statement**: 现有视频生成模型（如 VideoLDM）在 3D 一致性与摄像机可控性方面严重不足，相机姿态估计成功率仅 4.4%
- **Evidence**: Table 19 VideoLDM 相机姿态估计成功率 4.4%，Sampson error 0.841
- **Implication**: 用作 Physical AI 世界模拟器的视频生成模型必须具备几何合理的三维结构，现有方案差距巨大

## Gaps

### G1: 缺乏可供 Physical AI 开发者定制的通用世界基础模型平台：现有工作要么
- **Statement**: 缺乏可供 Physical AI 开发者定制的通用世界基础模型平台：现有工作要么专注特定任务，要么未提供可微调的开放预训练基础
- **Caused by**: C1
- **Existing attempts**: []
- **Why they fail**: 已有视频生成模型以生成质量为目标，未专门设计为可微调的世界基础模型，也未开放完整训练权重

### G2: 千万小时量级视频数据处理缺乏高效自动化流水线，不同 codec、分辨率、时长的异
- **Statement**: 千万小时量级视频数据处理缺乏高效自动化流水线，不同 codec、分辨率、时长的异构视频难以统一高质量处理
- **Caused by**: C1
- **Existing attempts**: ['使用 TransNetV2 神经网络镜头检测替代基于颜色直方图的启发式算法（PySceneDetect）', '用 PyNvideoCodec 替换 ffmpeg 以充分利用 NVDEC/NVENC 硬件加速器，提升转码吞吐约 6.5 倍', '采用 Ray 分布式编排框架解耦数据传输与计算，支持地理分布式集群流式处理']
- **Why they fail**: 各处理步骤（解码、过滤、标注）吞吐量差异巨大，简单串行流水线资源利用率极低

## Key Insight
- **Insight**: 将世界模型分解为「通用预训练 WFM」与「专用后训练 WFM」两阶段：先用大规模多样化视频训练通用物理先验，再用少量特定领域数据微调，以较低成本得到针对具体 Physical AI 环境的专用世界模拟器
- **Derived from**: C1, C4
- **Enables**: Physical AI 开发者无需从头训练大规模模型，只需在开放预训练 WFM 上进行领域微调，即可构建摄像机控制、机器人操控、自动驾驶等专用物理世界模拟器

## Assumptions
- 大规模真实视频数据包含足够的物理规律隐含信息，使得数据驱动预训练可以涌现物理理解能力
- 连续 Token（扩散 WFM）和离散 Token（自回归 WFM）是互补的世界表示方式，各有视觉质量与 LLM 技术复用的优劣权衡（论文明确讨论，未给出统一优胜结论）
- 预训练 WFM 提供的先验足够强，使得后训练所需的领域特定数据量远小于从头训练所需规模
