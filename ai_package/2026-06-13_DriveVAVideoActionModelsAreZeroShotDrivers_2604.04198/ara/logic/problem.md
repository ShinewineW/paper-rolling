# Problem Specification

## Observations

### O1: 自动驾驶泛化要求模型能处理未见交通模式、道路布局、传感器配置和环境条件。
- **Statement**: 自动驾驶泛化要求模型能处理未见交通模式、道路布局、传感器配置和环境条件。
- **Evidence**: 引言指出 real-world deployment 需要面对 unseen traffic patterns、novel road layouts、diverse sensor configurations 和 long-tail events。
- **Implication**: 只在单一训练分布内拟合轨迹，难以支撑跨数据集和跨域部署。

### O2: 现有 VLA 主要继承静态图文预训练中的语义知识，缺少直接的时空和因果运动先验。
- **Statement**: 现有 VLA 主要继承静态图文预训练中的语义知识，缺少直接的时空和因果运动先验。
- **Evidence**: 论文称 VLA pretraining on static image-text pairs 主要迁移 semantic knowledge，但对 spatiotemporal and causal priors 支持有限。
- **Implication**: 模型可能知道场景里有什么，却不够知道世界会怎样运动。

### O3: 现有 world-model-based planning 常把视频想象和轨迹生
- **Statement**: 现有 world-model-based planning 常把视频想象和轨迹生成分离或松耦合，导致两者不一致。
- **Evidence**: 论文多处指出 video imagination and trajectory generation 通常 separately or loosely coupled，并在 Fig. 3 中展示 PWM 想象左转但轨迹近似直行的 mismatch。
- **Implication**: 闭环 rollout 中，规划动作会偏离模型自己想象的未来场景，误差会累积。

### O4: DriveVA的关键不是把视频预测当作附加辅助项，而是让动作作为同一 rollo
- **Statement**: DriveVA的关键不是把视频预测当作附加辅助项，而是让动作作为同一 rollout 的 action grounding。
- **Evidence**: 论文称 video-level supervision 是 planning gains 的 main driver，并说明 future video latents 与 action tokens 共享生成过程。
- **Implication**: 规划收益来自视觉未来和动作输出被同一生成过程约束，而不是来自级联模块的后处理。

## Gaps

### G1: 跨数据集 zero-shot transfer 仍不足。
- **Statement**: 跨数据集 zero-shot transfer 仍不足。
- **Caused by**: 训练信号偏向语义识别或轨迹拟合，而不是可迁移的视觉动态。
- **Existing attempts**: ['构造 corner-case 数据集', '使用 scene- and skill-specialized experts', '使用 latent-dynamics world model']
- **Why they fail**: 静态图文预训练和轨迹模板难以覆盖新平台、新环境和未见交互。

### G2: 视觉预测和动作预测之间缺少强耦合。
- **Statement**: 视觉预测和动作预测之间缺少强耦合。
- **Caused by**: 把 future visual prediction 当作辅助信号、推理中间过程或松耦合模块。
- **Existing attempts**: ['显式预测 future observations', '用 inverse dynamics model 做动作 grounding', '用 multi-stage optimization 连接视频和规划']
- **Why they fail**: 视频分支和动作分支分开训练或多阶段优化时，只能依赖特征传递维持一致。

### G3: 长时域 rollout 容易失去结构一致性。
- **Statement**: 长时域 rollout 容易失去结构一致性。
- **Caused by**: 只做孤立短片段预测，缺少 progressive video continuation。
- **Existing attempts**: ['固定历史窗口条件输入', '短窗口 future clip 预测', 'rolling-horizon 执行']
- **Why they fail**: 短期视觉想象如果不连续递推，后续片段可能与历史条件和动作轨迹脱节。

## Key Insight
- **Insight**: 把未来视频 latent 和 action tokens 放进同一扩散式生成块中相互作用，使动作不再是视频之后的独立输出，而是同一未来想象的可执行 grounding。
- **Derived from**: 论文对 loosely coupled pipelines 的失败分析、DriveVA 的 joint video-action modeling 设计，以及视频监督和 dual-prediction 消融。
- **Enables**: 更紧的视频-轨迹一致性、更稳定的闭环规划，以及从 NAVSIM 到 nuScenes 和 Bench2Drive 的 zero-shot 泛化。

## Assumptions
- 预训练视频模型中的 motion dynamics 和 physical plausibility 先验可以迁移到驾驶场景。
- 未来视频的视觉演化包含足够的 ego-motion 线索，可用于约束轨迹预测。
- 统一生成过程中的 video tokens 与 action tokens 双向交互有助于规划，而不是只让视频作为动作预测的被动上下文。
- video continuation 能把短窗口预测串接成更一致的长时域 rollout。
