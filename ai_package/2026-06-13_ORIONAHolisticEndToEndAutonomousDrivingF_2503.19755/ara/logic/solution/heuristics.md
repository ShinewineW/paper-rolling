# Heuristics

## H1: 用 QT-Former 的 history queries 先从 memory bank 检索历史信息，再与当前 scene queries 交互，最后按 FIFO 将更新后的 history queries 写回 memory bank。
- **Rationale**: 论文明确指出历史信息会影响当前场景中的 trajectory planning；history queries 不只存储压缩历史，还用于提取与历史最相关的当前场景特征，从而增强 long-term memory ability。
- **Sensitivity**: history queries 过少会削弱历史上下文建模；过多会妨碍 VLM 捕获当前帧特征，论文将这种退化解释为当前帧特征在 driving scene 中更关键。
- **Bounds**: 只把该机制视为论文中的 temporal context 聚合策略；不要把 memory bank 写成外部检索数据库或在线地图。
- **Code ref**: [QT-Former memory bank FIFO update]
- **Source**: Sec. 3.1: history queries 与 long-term memory bank；Sec. 4.5: Influence of the number of history queries

## H2: 用 perception queries 的 auxiliary heads 对 object detection、traffic state 与 motion prediction 进行监督，再把 scene tokens 与 history tokens 输入 LLM。
- **Rationale**: 论文把 perception queries 用于 traffic elements 感知，并在消融中说明 explicit traffic state supervision 能帮助 ORION 更好理解 traffic signals，从而减少闭环 infractions。
- **Sensitivity**: 仅加入交通状态监督不能保证所有方法都理解因果关系；论文强调 ORION 通过 reasoning space 与 action space 对齐后更能利用 VLM 的 reasoning ability。
- **Bounds**: 不要把 auxiliary heads 解释为独立的传统感知栈；它们服务于 QT-Former 表征和统一训练。
- **Code ref**: [QT-Former perception heads]
- **Source**: Sec. 3.1: multiple auxiliary heads；Sec. 4.5: Effectiveness of QT-Former designs

## H3: LLM 通过 planning QA template 生成特殊 planning token s，将 scene understanding 与 action reasoning 的上下文累积到该 token。
- **Rationale**: 论文明确说 planning token s 的 embedding 作为条件控制 trajectory generation，使语言推理信息进入 generative planner。
- **Sensitivity**: 如果只让 VLM 直接输出 text-based planning results，论文认为其数学计算与数值推理能力不足，且 autoregressive 机制只推断单一结果，不符合 human planning 的不确定性。
- **Bounds**: 不要把 planning token 当成离散 meta-action；论文将它作为 generative planner 的条件 token。
- **Code ref**: [planning QA template with special planning token s]
- **Source**: Sec. 3.2: Large Language Model；Introduction: text-based planning results 的局限

## H4: generative planner 采用 VAE 将 planning token 与 ground-truth trajectory 投影到 Gaussian latent space，并用 KL divergence 对齐后由 GRU decoder 解码轨迹。
- **Rationale**: 论文主张通过 generative model 建立 unified latent representation，以桥接 VLM reasoning space 与 trajectory action space。
- **Sensitivity**: 论文也尝试 diffusion model，但分析认为 VAE latent space 更直接有效地对齐 reasoning information 到 multi-modal action space，且训练更稳定。
- **Bounds**: 不要把 VAE 与 GenAD 的 VAE 作用混同；本文只用 ego vehicle 视角的 single token encoded in reasoning space 作为输入。
- **Code ref**: [VAE generative planner with GRU decoder]
- **Source**: Sec. 3.3: Generative Planner；Sec. 4.5: Analysis on different generative planners

## H5: 训练采用 progressive space alignment：先做 3D Vision-Language Alignment，再做 Language-Action Alignment，最后 End-to-End Fine-tuning 联合 VQA 与 planning。
- **Rationale**: 论文附录说明逐阶段继承上一阶段权重，以加速 vision-reasoning-action space alignment，并逐步增强 reasoning 与 planning capabilities。
- **Sensitivity**: 单任务训练无法同时获得 reasoning 与 planning capabilities；联合训练在论文中被描述为同时改善 planning 与 language metrics。
- **Bounds**: 不要把三阶段策略写成推理流程；它是训练期策略。
- **Code ref**: [three-stage training strategy]
- **Source**: Appendix B: Training Details；Sec. 4.5: Influence between VQA task training and planning task training
