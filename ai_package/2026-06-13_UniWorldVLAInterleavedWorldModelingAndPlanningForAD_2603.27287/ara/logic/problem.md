# Problem Specification

## Observations

### O1: 自动驾驶需要同时推理环境如何演化并据此规划动作，但既有 VLA 和 world 
- **Statement**: 自动驾驶需要同时推理环境如何演化并据此规划动作，但既有 VLA 和 world model 往往分别处理轨迹预测与环境建模。
- **Evidence**: Introduction 指出这些方法通常单独开发，分别处理 trajectory prediction 和 environment modeling，难以共享互补知识。
- **Implication**: 如果世界预测和控制输出之间缺少紧耦合，规划器难以利用模型学到的动态演化知识。

### O2: 并行的 predict-and-plan 虽然联合训练，但功能上仍解耦。
- **Statement**: 并行的 predict-and-plan 虽然联合训练，但功能上仍解耦。
- **Evidence**: Introduction 描述该范式中 world modeling 关注 next-frame prediction，trajectory planning 将视觉观测映射到控制输出，未显式利用 learned dynamics。
- **Implication**: 联合架构本身不保证规划会真正吸收未来动态信息。

### O3: 顺序的 predict-then-plan 先预测未来场景再规划，隐含环境静止或
- **Statement**: 顺序的 predict-then-plan 先预测未来场景再规划，隐含环境静止或响应固定计划的假设。
- **Evidence**: Introduction 指出该范式的关键限制是 implicit assumption that the environment remains stationary，而真实交通是 non-stationary。
- **Implication**: 复杂城市交互中，后段视觉证据可能已经与前段自车微调后的真实决策过程脱节。

### O4: 仅依赖 RGB 的既有 world model 会限制几何推理。
- **Statement**: 仅依赖 RGB 的既有 world model 会限制几何推理。
- **Evidence**: Related Work 指出多数先前方法 rely solely on RGB inputs，并说明本文引入 depth-informed conditioning。
- **Implication**: 缺少深度线索会削弱远期场景结构和运动关系的建模。

## Gaps

### G1: 开环未来滚动会产生与实际决策过程漂移的未来想象。
- **Statement**: 开环未来滚动会产生与实际决策过程漂移的未来想象。
- **Caused by**: predict-then-plan 将世界预测和规划按阶段分开。
- **Existing attempts**: ['ImagiDrive 等先预测 future scenes 再基于它们生成 ego trajectory', 'Epona 等 autoregressive world model 强调未来场景生成']
- **Why they fail**: 完整生成未来后再规划时，未来场景没有持续吸收前面时间步的动作调整。

### G2: 并行联合建模未必让规划显式利用世界动态。
- **Statement**: 并行联合建模未必让规划显式利用世界动态。
- **Caused by**: predict-and-plan 中规划路径仍主要从视觉观测到控制输出。
- **Existing attempts**: ['DrivingGPT 和 PWM 等将状态与动作放入统一 autoregressive 框架']
- **Why they fail**: world modeling 与 trajectory planning 虽在单个架构中训练，但任务目标仍各做各的。

### G3: RGB-only 历史提示对远期结构保持不足。
- **Statement**: RGB-only 历史提示对远期结构保持不足。
- **Caused by**: 历史视觉条件主要来自 RGB token。
- **Existing attempts**: ['先前 driving world model 多依赖 RGB inputs', '部分方法使用多传感器输入，但本文强调 single-view camera-only 设计']
- **Why they fail**: 缺少单目深度提供的空间几何约束，快速行驶和转弯场景中更容易出现结构模糊。

## Key Insight
- **Insight**: 将未来帧预测和同时间步动作查询交替排列，让预测出的世界状态立即进入下一步规划与下一步世界生成，形成闭环式视觉-动作反馈。
- **Derived from**: 由 Introduction 中对 frozen hallucination 的批评、Fig. 1(c) 的 interleaved world modeling and planning，以及 Methods 中 frame-action generation 的流程共同推出。
- **Enables**: 规划决策可以随着生成的未来观测逐步更新，同时深度融合为未来帧提供更稳定的几何上下文。

## Assumptions
- 历史视觉 token 足以承载用于规划的场景语义和短期动态。
- Depth Anything 3 估计的单目深度可作为可靠的几何辅助信号。
- NAVSIM 的 closed-loop planning 指标能反映本文交替生成范式的主要收益。
- 论文未显式给出总参数量；params_million 使用 -1.0 表示未披露。
