# Problem Specification

## Observations

### O1: 现有世界模型常把环境动态建模为离散 latent 序列，这有助于缓解长时域误差累
- **Statement**: 现有世界模型常把环境动态建模为离散 latent 序列，这有助于缓解长时域误差累积，但会牺牲重建质量和泛化性。
- **Evidence**: 引言说明 recent world modeling methods often model environment dynamics as a sequence of discrete latent variables，并指出这种 encoding may lose information。
- **Implication**: 如果决策依赖小的视觉差异，压缩后的表示可能让智能体学到错误策略。

### O2: 在一些任务中，少量像素级视觉差异也可能改变最优行为。
- **Statement**: 在一些任务中，少量像素级视觉差异也可能改变最优行为。
- **Evidence**: 引言以交通灯、远处行人为例说明 small details in the visual input may change the policy of an agent；视觉比较还指出奖励和敌人被混淆会影响学习。
- **Implication**: 世界模型的视觉保真度不只是生成质量问题，而是会进入强化学习信用分配和策略学习。

### O3: diffusion 模型提供了避免离散化的一条路径，并且天然适合按历史观测与动作
- **Statement**: diffusion 模型提供了避免离散化的一条路径，并且天然适合按历史观测与动作进行条件化。
- **Evidence**: 论文说 diffusion challenges methods modeling discrete tokens，并在 Section 2.3 将无条件 diffusion 改成条件环境动态模型。
- **Implication**: 方法可以在图像空间直接生成下一观测，使世界模型更像可替换的环境接口。

## Gaps

### G1: 直接采用传统 DDPM 风格 diffusion 难以满足世界模型的低延迟长 r
- **Statement**: 直接采用传统 DDPM 风格 diffusion 难以满足世界模型的低延迟长 rollout 需求。
- **Caused by**: DDPM 的噪声预测目标在高噪声区域给出较差 score 估计，采样开头质量下降。
- **Existing attempts**: ['采用 EDM 公式而非 DDPM 作为主 diffusion 框架', '使用 Euler’s method 控制 NFE 成本', '通过网络预条件让训练目标随噪声水平自适应混合信号与噪声']
- **Why they fail**: 论文分析指出在少量去噪步下 DDPM-based generation suffers from compounding error，容易漂出分布。

### G2: 单步采样虽然便宜，但在部分可观测和多模态场景中会产生模糊平均。
- **Statement**: 单步采样虽然便宜，但在部分可观测和多模态场景中会产生模糊平均。
- **Caused by**: 不可预测对象的未来位置存在多种可能，单次去噪会在模式之间插值。
- **Existing attempts**: ['采用迭代 solver 将生成推向某个模式', '在主实验中使用固定的多步 EDM 采样', '用 Boxing 的视觉分析说明多步采样能得到更清晰图像']
- **Why they fail**: Section 5.2 说明单步预测等价于给定 noisy input 的可能重建期望，多模态时可能落在分布外。

## Key Insight
- **Insight**: 核心洞察是：世界模型不应只追求紧凑 latent 的可预测性，还要保留会改变策略的视觉细节；EDM-style diffusion 通过图像空间条件生成和自适应训练目标，把视觉保真与长 rollout 稳定性同时纳入设计。
- **Derived from**: ['离散 latent 压缩会损失重要视觉信息', 'diffusion 已成为高质量图像生成范式', 'EDM 在少量去噪步下比 DDPM 更稳定', 'DIAMOND 与 IRIS 的视觉对比显示细节一致性差异会对应到策略表现']
- **Enables**: 让智能体可以完全在 diffusion world model 的 imagination 中训练，同时让该世界模型也可作为交互式 neural game engine 使用。

## Assumptions
- 过去观测和动作包含足够信息来近似 POMDP 中不可见状态。
- 图像空间生成带来的视觉细节收益足以抵消 diffusion 采样成本。
- 奖励和终止可以由单独的 CNN-LSTM 模型补足，而不需要由 diffusion 模型直接生成。
- EDM 预条件带来的低步数稳定性可迁移到 Atari 多游戏设置。
