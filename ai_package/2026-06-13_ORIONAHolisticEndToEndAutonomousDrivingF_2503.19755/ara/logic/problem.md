# Problem Specification

## Observations

### O1: 经典 E2E 方法在 open-loop 上可以通过模仿专家轨迹取得进展，但缺少
- **Statement**: 经典 E2E 方法在 open-loop 上可以通过模仿专家轨迹取得进展，但缺少复杂因果推理能力，因此在需要交互决策的 closed-loop benchmark 中容易受限。
- **Evidence**: Introduction 明确指出 classic E2E methods lack the common sense to complete complex causal reasoning，并在 comprehensive closed-loop benchmarks 中 struggle。
- **Implication**: 仅靠感知、预测、规划的多任务堆叠不足以处理动态交互场景中的因果决策。

### O2: 直接让 VLM 输出文本式规划结果虽然方便，但 VLM 不擅长数学计算或数值推理
- **Statement**: 直接让 VLM 输出文本式规划结果虽然方便，但 VLM 不擅长数学计算或数值推理，且自回归机制倾向于单一结果。
- **Evidence**: Introduction 中说明 text-based planning results using VLM 受 mathematical calculations or numerical reasoning 限制，并且 autoregressive mechanism only infers single results。
- **Implication**: 把轨迹当作文本生成会削弱对连续数值轨迹和多模态不确定性的建模。

### O3: 用 meta-action 把 VLM 与经典 E2E 模型连接起来会形成手工接
- **Statement**: 用 meta-action 把 VLM 与经典 E2E 模型连接起来会形成手工接口，导致 reasoning space 与 action space 被解耦。
- **Evidence**: Introduction 指出 meta-action paradigm adopts a carefully crafted interface，并且 decouples these two spaces。
- **Implication**: 这种接口难以让轨迹优化与 VLM reasoning process 协同优化。

### O4: 历史信息会影响当前场景中的轨迹规划，但简单拼接多帧图像受到 VLM token 
- **Statement**: 历史信息会影响当前场景中的轨迹规划，但简单拼接多帧图像受到 VLM token length 和计算开销约束。
- **Evidence**: Introduction 中写到 long-term memory is necessary，并指出 concatenate multi-frame images 受 token length 与 computational overhead 约束。
- **Implication**: 需要更紧凑的时间上下文机制来为推理与规划提供历史线索。

## Gaps

### G1: VLM 的 semantic reasoning space 与 purely 
- **Statement**: VLM 的 semantic reasoning space 与 purely numerical trajectory output 所在的 action space 存在跨域鸿沟。
- **Caused by**: reasoning space 与 action space 的表示形式、优化目标和输出结构不一致。
- **Existing attempts**: ['text-based planning results using VLM', 'VLM output meta-action to assist classic E2E methods', 'special token decode outputs by MLP']
- **Why they fail**: 直接文本输出难以处理连续数值轨迹，meta-action 接口又不能端到端地让推理与轨迹生成共同优化。

### G2: 现有 VLM for E2E 方法在复杂 closed-loop evaluat
- **Statement**: 现有 VLM for E2E 方法在复杂 closed-loop evaluation 中仍难以稳定发挥。
- **Caused by**: VLM 推理能力没有被有效传递到多模态轨迹生成过程。
- **Existing attempts**: ['plain text outputs', 'dual-system paradigm', 'MLP decoder paradigm']
- **Why they fail**: 论文认为问题来自语义推理空间到纯数值动作空间的对齐不足，以及历史上下文建模效率不足。

## Key Insight
- **Insight**: 把 planning token 作为语义条件，并用 generative planner 在 latent space 中学习 reasoning-to-action 的分布对齐，可以把 VLM 的因果推理转化为可微的轨迹生成约束。
- **Derived from**: 论文从 conditional generation 与不同模态 latent spaces 存在 semantic correlations 的观察出发，引入 VAE 对齐 reasoning space 与 action space。
- **Enables**: 这使 ORION 可以统一优化 VQA 与 planning，并在 closed-loop planning 中输出带推理解释的多模态轨迹。

## Assumptions
- generative model 能够为语义推理信息与轨迹动作建立共享或可对齐的 latent distribution。
- Bench2Drive 的 closed-loop evaluation 能反映复杂交互场景下的因果决策能力。
- QT-Former 提取的历史 token 足以承载对当前规划有用的长期视觉上下文。
- params_million 采用 MD 中显式出现的 Qwen2VL-72B 作为代表性模型规模；论文未给出 ORION 总参数量或 Vicuna v1.5 具体参数量。
