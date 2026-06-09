# Problem Specification

## Observations

### O1: 现有WAM普遍采用「想象→执行」范式:在测试时通过迭代视频去噪生成未来帧,再以生
- **Statement**: 现有WAM普遍采用「想象→执行」范式:在测试时通过迭代视频去噪生成未来帧,再以生成的未来帧指导动作预测,造成实质性的推理延迟
- **Evidence**: Abstract与Introduction明确指出该范式「incurring substantial test-time latency from iterative video denoising」
- **Implication**: 测试时生成未来视频的计算代价或许并非必要

### O2: WAM的效果可能来自两个相互独立的因素:训练期间的视频预测目标,以及推理时的显式
- **Statement**: WAM的效果可能来自两个相互独立的因素:训练期间的视频预测目标,以及推理时的显式未来生成;但现有系统将二者耦合于同一前向过程,无法单独评估各自贡献
- **Evidence**: Introduction明确区分「(1) the video prediction objective during training...and (2) explicit future generation during inference」并指出现有系统将二者耦合
- **Implication**: 需要设计受控变体以独立量化两个因素的贡献

### O3: 标准VLA预训练主要依赖静态图文数据,未显式建模物理世界在动作下的演化方式
- **Statement**: 标准VLA预训练主要依赖静态图文数据,未显式建模物理世界在动作下的演化方式
- **Evidence**: Related Work节引述近期WAM文献的观察:「standard VLA pretraining is largely based on static image-text data and does not explicitly model how the physical world evolves under action」
- **Implication**: 视频建模训练目标本身可为策略提供VLA所缺失的物理先验

## Gaps

### G1: 尚不清楚WAM在测试时是否真的需要显式未来想象才能获得强行动性能
- **Statement**: 尚不清楚WAM在测试时是否真的需要显式未来想象才能获得强行动性能
- **Caused by**: 「想象→执行」设计将训练信号与推理机制绑定在同一架构中
- **Existing attempts**: []
- **Why they fail**: 现有WAM将训练期视频目标与推理期视频生成耦合,无法独立评估各自贡献

### G2: 「想象→执行」WAM的测试时推理延迟过高,难以实时部署
- **Statement**: 「想象→执行」WAM的测试时推理延迟过高,难以实时部署
- **Caused by**: 生成式视频扩散模型在测试时的迭代采样机制
- **Existing attempts**: ['VPP 从视频扩散模型提取预测视觉表示来条件化策略,减少但未消除对视频模型特征的依赖', 'UVA 联合建模视频和动作并在测试时跳过视频解码以加速推理,但研究侧重点不同,未对两因素做受控解耦']
- **Why they fail**: 迭代视频去噪需要多步扩散采样,推理代价随视频帧数显著增加

## Key Insight
- **Insight**: WAM的主要价值在于训练时视频预测目标所塑造的潜在世界表示,而非测试时的显式未来视觉生成;通过设计解耦的架构,可在保留训练收益的同时消除推理时的视频生成代价
- **Derived from**: C1、C2对现有WAM范式的分析,以及G1关于两因素耦合导致可归因困难的识别
- **Enables**: Fast-WAM架构:保留训练期视频联合目标,推理时仅执行单次前向传播,直接从潜在世界表示生成动作

## Assumptions
- 视频联合训练目标与测试时显式未来生成可以通过结构化注意力掩码在设计上完全解耦(分析推断,论文未显式声明该假设成立的充分条件)
- 预训练视频DiT在单次前向传播中足以提取捕获物理动态和交互结构的潜在表示
- 阻断动作令牌访问未来视频令牌的注意力掩码不会实质性损害动作预测质量
