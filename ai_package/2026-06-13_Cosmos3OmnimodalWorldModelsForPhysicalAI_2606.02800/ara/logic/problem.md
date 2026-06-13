# Problem Specification

## Observations

### O1: Physical AI 需要同时理解当前世界、预测未来演化并选择动作，论文把理解
- **Statement**: Physical AI 需要同时理解当前世界、预测未来演化并选择动作，论文把理解和生成视为相互耦合的能力。
- **Evidence**: 引言说明 understanding 负责从部分观察中推断语义和动力学，generation 负责预测和模拟未来，并判断世界如何演化以及 agent 如何响应。
- **Implication**: 单纯的感知模型或单纯的视频生成模型都不足以承担完整的 embodied agent backbone。

### O2: 既有范式把感知推理、视频生成、世界模拟和动作预测拆成多个模型。
- **Statement**: 既有范式把感知推理、视频生成、世界模拟和动作预测拆成多个模型。
- **Evidence**: 论文列举 VLMs、Video Generation Models、Forward Dynamics Models、VLAs、WAMs 分别服务不同环节，并称这种 paradigm separation 有限制。
- **Implication**: 系统需要模型间转换、任务适配和外部流水线，容易带来计算浪费和表示断裂。

### O3: 动作被作为核心模态引入，而不是外部控制标签。
- **Statement**: 动作被作为核心模态引入，而不是外部控制标签。
- **Evidence**: 架构部分说明 Cosmos 3 treats action as a core modality，并引入 dedicated class of action tokens，将 physical world 与语言推理、视频世界建模连接起来。
- **Implication**: 同一模型可以表达 forward dynamics、inverse dynamics 和 policy mode，而不是只生成被动视频。

## Gaps

### G1: 分离式 Physical AI 流水线难以把任务理解、未来模拟和动作执行放在同一
- **Statement**: 分离式 Physical AI 流水线难以把任务理解、未来模拟和动作执行放在同一个可训练接口里。
- **Caused by**: 理解和生成在既有工作中通常被分别建模，动作空间还随 embodiment 改变。
- **Existing attempts**: ['使用 VLM 做场景理解和规划', '使用 Forward Dynamics Models 或 Video Generation Models 做未来模拟', '使用 VLAs 或 WAMs 生成动作']
- **Why they fail**: VLM 输出文本，生成模型输出媒体，动作模型输出控制，彼此没有天然共享的状态和因果接口。

### G2: 普通多模态生成进展仍偏向感知质量和媒体生成，对物理动态、动作条件和 embodi
- **Statement**: 普通多模态生成进展仍偏向感知质量和媒体生成，对物理动态、动作条件和 embodied control 覆盖不足。
- **Caused by**: 媒体生成目标与 Physical AI 的可控世界模拟目标不完全一致。
- **Existing attempts**: ['text-to-video 模型提升视觉真实感', 'control-conditioned video generation 提升结构控制', 'omnimodels 尝试统一理解和生成']
- **Why they fail**: 只优化文本到图像或视频的表面一致性，不能保证干预、接触、声音和动作后果在同一世界状态中一致。

## Key Insight
- **Insight**: 把任务统一成一段 interleaved multimodal sequence，并在 MoT 中让 AR subsequence 与 diffusion subsequence 分塔处理、共享注意力交互，可以把理解、生成和动作建模归入同一条件化序列问题。
- **Derived from**: 由论文的 token arrangement、Mixture-of-Transformers、dual-stream joint attention 和 action tokenization 共同推出。
- **Enables**: 同一 Cosmos 3 backbone 可在不改架构的情况下切换 VLM、T2I、T2V、I2V、audio-video generation、forward dynamics、inverse dynamics 和 policy mode。

## Assumptions
- 不同模态可以先经 modality-specific encoders 投到统一表示空间，再由同一 backbone 建模。
- AR reasoner 的因果完整性需要保留，生成端则需要对条件和待生成 token 做双向交互。
- 不同 embodiment 的动作可以通过共享几何结构和 domain-aware projections 对齐到可学习的 action token 空间。
