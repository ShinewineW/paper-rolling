# Problem Specification

## Observations

### O1: Physical AI 直接在真实世界训练成本高、速度慢且有安全风险，因此需要能
- **Statement**: Physical AI 直接在真实世界训练成本高、速度慢且有安全风险，因此需要能生成高质量、多样视觉环境的世界模拟器。
- **Evidence**: 引言说明真实世界训练在早期尤其慢、昂贵且有风险，世界模拟器可作为安全代理。
- **Implication**: 世界模型的核心价值不是单纯视频生成，而是为感知、控制、策略验证和合成数据提供可控环境。

### O2: 通用视频生成模型和早期 Physical AI 世界模型在专业领域的细粒度控制、
- **Statement**: 通用视频生成模型和早期 Physical AI 世界模型在专业领域的细粒度控制、物理一致性和可适配性上仍不足。
- **Evidence**: 相关工作指出多数模型偏向 general content generation，且 often fall short in domains requiring precise, fine-grained control over object dynamics, interactions, and physical consistency。
- **Implication**: 方法必须同时改进数据、条件表征、训练配方和下游控制接口。

### O3: 论文把开放权重、代码和基准作为方法的一部分，服务于下游研究者的微调、扩展和部署。
- **Statement**: 论文把开放权重、代码和基准作为方法的一部分，服务于下游研究者的微调、扩展和部署。
- **Evidence**: 摘要和引言均说明 release source code, pretrained checkpoints, and curated benchmarks。
- **Implication**: 该工作定位为平台型基础模型，而不是单个封闭任务模型。

## Gaps

### G1: Cosmos-Predict1 的数据与训练管线不足以覆盖更广的 Physica
- **Statement**: Cosmos-Predict1 的数据与训练管线不足以覆盖更广的 Physical AI 场景。
- **Caused by**: 物理世界任务需要清洁、可标注、领域对齐的视频，而普通互联网视频包含伪影、文字覆盖、非真实物理内容和重复片段。
- **Existing attempts**: ['强化多阶段过滤与语义去重', '加入领域特定数据管线', '用更细粒度 caption 和 sharding 支撑训练采样']
- **Why they fail**: 原有管线保留的数据更宽松，语义粒度、领域覆盖和质量控制不足。

### G2: 分散的 Text2World、Image2World、Video2World 能
- **Statement**: 分散的 Text2World、Image2World、Video2World 能力不利于形成统一的世界生成接口。
- **Caused by**: 不同任务对条件帧、文本和视频上下文的使用方式不同。
- **Existing attempts**: ['用单一 Cosmos-Predict2.5 模型覆盖多种生成模式', '用 frame-replacement 策略处理视觉条件', '用 cross-attention 注入 Cosmos-Reason1 文本嵌入']
- **Why they fail**: 任务分离会让条件方式和训练配方更复杂，也限制同一模型在不同输入形态间复用能力。

### G3: 高分辨率视频在训练中容易出现时间过渡伪影。
- **Statement**: 高分辨率视频在训练中容易出现时间过渡伪影。
- **Caused by**: 高分辨率内容局部像素相关性强，噪声不足时难以打散冗余。
- **Existing attempts**: ['采用 shifted logit-normal 分布', '在训练中偏向更高噪声水平', '额外强化高噪声区域采样']
- **Why they fail**: 论文认为模型在高噪声区域见到的训练样本不足，难以稳定学习被强扰动后的时序结构。

## Key Insight
- **Insight**: 把世界模拟视为带多模态条件的速度场学习，再用领域数据、奖励模型和控制分支逐步专门化，是本文的核心洞察。
- **Derived from**: flow matching 训练目标、统一生成模式、Cosmos-Reason1 条件编码、domain-specific SFT、model soup、VideoAlign RL 和 Cosmos-Transfer2.5 控制分支。
- **Enables**: 同一个基础模型可被后训练为机器人动作条件预测、多视角自动驾驶仿真、相机可控机器人视角生成和 VLA 合成数据生成器。

## Assumptions
- 高质量、经过过滤和领域标注的视频数据能显著改善 Physical AI 场景泛化。
- VLM 奖励和人工偏好在视频质量、文本对齐与运动质量上足够相关。
- 像素空间或视频空间世界模型保留的细节对下游策略学习有价值。
- 去除绝对位置嵌入后，模型对更高分辨率和更长序列的适配能力会更好。
