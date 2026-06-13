# Claims

## C1: 统一模型覆盖多种 Physical AI 能力
- **Statement**: Cosmos 3 在推理、图像生成、视频生成、音频生成、迁移生成和动作生成上都给出了同一模型族或后训练变体的结果，论文据此主张它可以作为 Physical AI 的通用 backbone。
- **Status**: supported
- **Falsification criteria**: 如果同一模型族在这些能力上不能复现实验表中的相对表现，或需要任务特定架构改动才能完成这些模式，该主张会被削弱。
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 证据来自结果总览与各任务评测表；这是覆盖范围和性能并列的经验性主张。
- **Tags**: ['descriptive', 'generalization']

## C2: Cosmos 3 Generator 在图像和视频生成中具有强开放模型竞争力
- **Statement**: 在 Text-to-Image、PAIBench-G、RBench、Cosmos HUE 与 Human World Bench 中，Cosmos 3 的生成器变体整体上优于或接近主要开放模型，并在若干开放模型比较中领先。
- **Status**: supported
- **Falsification criteria**: 如果使用相同提示、采样配置和评测协议时，开放基线稳定超过 Cosmos 3 对应变体，该改进主张不成立。
- **Proof**: [E2]
- **Evidence basis**: ['E2']
- **Interpretation**: 论文把图像、视频和人工评测结果放在多个基准下交叉呈现，支撑生成质量的改进结论。
- **Tags**: ['improvement']

## C3: 动作生成和后训练提升机器人与世界动作任务
- **Statement**: 在 forward dynamics、inverse dynamics、RoboLab、LIBERO-10 和 PushT 动作模式实验中，mid-training 或 joint action 训练通常带来更好的动作相关表现。
- **Status**: supported
- **Falsification criteria**: 如果控制初始化、训练步数和数据后，MT-init 或 joint action 训练不能带来相同方向的改善，该因果解释会被削弱。
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 该结论包含论文实验设计中的对照因素，因此比单纯排行榜更接近训练策略的因果证据。
- **Tags**: ['improvement', 'causal']

## C4: 合成数据、理解塔、FPS 控制与音频数据的消融显示若干设计选择有效
- **Statement**: 论文的消融实验显示，SDG 数据、Cosmos 3 Reasoner 初始化、Text Control 与 MRoPE FPS Modulation 组合、以及音频数据引入都对部分生成指标有正向作用。
- **Status**: supported
- **Falsification criteria**: 如果在相同训练预算、数据和评测协议下替换这些组件后指标不再按论文方向变化，则相关设计选择的有效性需要重新评估。
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 不同消融覆盖数据、初始化、时间控制和模态输入，说明论文把模型能力拆成了可检验设计因素。
- **Tags**: ['causal', 'improvement']

## C5: 训练与推理基础设施优化带来效率收益
- **Statement**: 异步 checkpoint、吞吐测量和推理 batching 实验表明，论文不仅报告模型质量，也量化了大规模训练与服务效率。
- **Status**: supported
- **Falsification criteria**: 如果相同硬件和任务设置下无法观察到相同方向的效率变化，则基础设施收益主张不成立。
- **Proof**: [E5]
- **Evidence basis**: ['E5']
- **Interpretation**: 这些表不是模型能力主结果，但支撑 Cosmos 3 作为可训练、可服务系统的工程可行性。
- **Tags**: ['descriptive', 'improvement']
