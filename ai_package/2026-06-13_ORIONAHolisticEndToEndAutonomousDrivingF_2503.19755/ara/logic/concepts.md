# Concepts

## ORION
- **Notation**: ORION = vision encoder + QT-Former + LLM + generative planner
- **Definition**: ORION 是一个由 vision-language instructed action generation 构成的整体式 E2E autonomous driving 框架，核心目标是在同一端到端系统中连接视觉输入、LLM 驾驶场景推理与数值轨迹规划。
- **Boundary conditions**: ORION 不是只输出文本规划的 VLM，也不是用 meta-action 外接传统 E2E planner 的双系统；论文强调它通过 generative planner 在推理空间与动作空间之间建立连接。
- **Related concepts**: ['QT-Former', 'LLM', 'generative planner', 'planning token', 'vision-reasoning-action space']

## vision-reasoning-action space alignment
- **Notation**: vision space -> reasoning space -> action space
- **Definition**: vision-reasoning-action space alignment 指 ORION 试图把视觉特征空间、LLM 推理空间和轨迹动作空间连接起来，使视觉上下文、语言推理和数值轨迹生成在同一框架中相互约束。
- **Boundary conditions**: 它不是单纯的视觉语言对齐；范围必须包含最终 action space 中的 trajectory generation。
- **Related concepts**: ['ORION', 'QT-Former', 'planning token', 'generative planner']

## QT-Former
- **Notation**: $Q _ { s }$, $Q _ { p }$, $Q _ { h }$, $M$, $x _ { s }$, $x _ { h }$
- **Definition**: QT-Former 是 ORION 中的 query-based temporal module，用于压缩和提取 multi-view image features，并通过 scene queries、perception queries、history queries 与 memory bank 聚合长期视觉上下文。
- **Boundary conditions**: QT-Former 不是最终轨迹解码器；它输出的是可供 LLM 使用的 scene tokens 与 history tokens，并通过辅助头处理交通元素、运动预测等视觉任务。
- **Related concepts**: ['scene queries', 'perception queries', 'history queries', 'memory bank', 'LLM']

## memory bank and history queries
- **Notation**: $$Q _ { h } = {\bf C A} ( Q _ { h } , M + P _ { t } , M + P _ { t } )$$; $$\hat { Q } _ { h } = {\bf C A} ( Q _ { h } , Q _ { s } , Q _ { s } )$$; $$M = [ \hat { Q } _ { h } ^ { t - n } , \cdot \cdot \cdot , \hat { Q } _ { h } ^ { t - 1 } , \hat { Q } _ { h } ^ { t } ]$$
- **Definition**: memory bank and history queries 是 QT-Former 中用于长期时序建模的机制，history queries 从 memory bank 中检索历史帧查询，并再与当前 scene features 交互以抽取和当前场景相关的历史信息。
- **Boundary conditions**: 它不等同于简单拼接多帧图像；论文明确将其作为减少 token 长度压力并提升长期记忆能力的查询式设计。
- **Related concepts**: ['QT-Former', 'history tokens', 'scene tokens', 'long-term visual context']

## planning token
- **Notation**: $$s \sim p ( s | x _ { s } , x _ { h } , x _ { q } , x _ { a } )$$
- **Definition**: planning token 是 LLM 在 planning QA template 中生成的特殊 token，用于汇聚当前场景理解、历史信息和动作推理上下文，并作为 generative planner 生成轨迹的条件。
- **Boundary conditions**: planning token 不是自然语言答案本身，也不是最终数值轨迹；它是从 LLM 推理上下文中抽取出的条件表示。
- **Related concepts**: ['LLM', 'scene tokens', 'history tokens', 'generative planner', 'trajectory generation']

## generative planner
- **Notation**: $p ( a | s )$
- **Definition**: generative planner 是 ORION 中连接 LLM reasoning space 与 trajectory action space 的轨迹生成模块，论文将当前 trajectory 表述为以 planning token 为条件的条件概率分布。
- **Boundary conditions**: generative planner 不是 LLM 的自回归文本输出；它负责数值轨迹生成，并可由 VAE 或 diffusion model 等生成式方法实现。
- **Related concepts**: ['planning token', 'VAE', 'trajectory generation', 'reasoning-action alignment']

## VAE latent alignment
- **Notation**: $$p ( z _ { s } | s ) \sim N ( \mu _ { s } , \sigma _ { s } ^ { 2 } ) , p ( z _ { t } | t ) \sim N ( \mu _ { t } , \sigma _ { t } ^ { 2 } )$$; $$\mathcal { L } _ { v a e } = D _ { K L } ( p ( \mathbf { z } | \mathbf { s } ) , p ( \mathbf { z } | \mathbf { t } ) ) .$$
- **Definition**: VAE latent alignment 是 ORION 默认 generative planner 的实现方式：把 planning token 对应的 state 与 ground-truth trajectory 投影到 Gaussian latent space，并用 Kullback-Leibler divergence 对齐二者分布。
- **Boundary conditions**: 论文特别区分该 VAE 与 GenAD 中的 VAE：本文只使用来自 ego vehicle 视角的 reasoning-space 单 token 作为输入来桥接空间，而不是使用所有 agents 的 BEV-space features 来学习结构化轨迹模式。
- **Related concepts**: ['generative planner', 'planning token', 'GRU decoder', 'reasoning-action alignment']

## Chat-B2D
- **Notation**: Chat-B2D = Bench2Drive + automated VQA annotation pipeline
- **Definition**: Chat-B2D 是论文从 Bench2Drive 扩展出的 VQA dataset，用于补足 closed-loop simulation environments 中高质量 VQA 标注不足的问题，覆盖 scene description、history information review、scene analysis 与 action reasoning 等任务。
- **Boundary conditions**: Chat-B2D 是 VQA 标注数据集，不是闭环评测协议本身；闭环评测仍在 Bench2Drive 场景中进行。
- **Related concepts**: ['Bench2Drive', 'VQA', 'LLM', 'Qwen2-VL', 'multi-task training']

## closed-loop evaluation on Bench2Drive
- **Notation**: metrics = DS, SR, Efficiency, Comfortness, Multi-Ability
- **Definition**: closed-loop evaluation on Bench2Drive 是论文主要验证 ORION 驾驶决策能力的评测设置，Bench2Drive 基于 CARLA simulator 构建交互场景，并用 Driving Score、Success Rate、Efficiency、Comfortness 与 Multi-Ability 等指标衡量闭环表现。
- **Boundary conditions**: 它不同于 nuScenes open-loop planning；论文主文强调 Bench2Drive 的 closed-loop setting 才是 ORION 主要展示优势的场景。
- **Related concepts**: ['ORION', 'Bench2Drive', 'CARLA', 'Multi-Ability', 'closed-loop planning']
