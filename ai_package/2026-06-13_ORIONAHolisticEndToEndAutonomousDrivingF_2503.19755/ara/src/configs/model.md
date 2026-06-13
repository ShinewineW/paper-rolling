## 整体框架
- **Value**: ORION由QT-Former、LLM和generative planner组成
- **Rationale**: 论文将ORION描述为对齐vision-reasoning-action space的整体E2E框架。
- **Search range**: QT-Former提取长期上下文；LLM进行驾驶场景推理并产生planning token；generative planner生成multi-modal trajectory
- **Sensitivity**: 消融显示仅文本输出、dual-system和MLP decoder均不如vision-language instructed action generation方向性有效。
- **Source**: ['Fig. 2', 'Sec 3', 'Sec 4.5']

## 地图与条件输入
- **Value**: fully HD map-free；仅使用Navigation Command作为轨迹预测输入条件，不使用target point
- **Rationale**: Model Setting明确说明ORION遵循Bench2Drive经典E2E基线设置，仅用NC而非TP。
- **Search range**: Condition为NC；Modality为camera
- **Sensitivity**: 该设置用于与NC基线公平比较，论文未对TP条件做ORION消融。
- **Source**: ['Sec 4.2', 'Table 1']

## 轨迹输出模式
- **Value**: anchor-free；输出6 mode trajectory predictions，对应Bench2Drive定义的6 NC
- **Rationale**: Model Setting显式说明ORION为anchor-free方法并输出6 mode trajectories。
- **Search range**: 6 mode trajectory predictions
- **Sensitivity**: 论文未给出6 mode数量敏感性；diffusion替代实验使用20 mode trajectory predictions作为对照生成器设置。
- **Source**: ['Sec 4.2', 'Sec 4.5']

## vision encoder
- **Value**: EVA-02-L
- **Rationale**: Training Process说明遵循Omnidrive采用EVA-02-L作为vision encoder。
- **Search range**: 论文未报告其他vision encoder主模型设置
- **Sensitivity**: 范式消融中保持同一vision encoder以保证公平，说明该组件被固定用于比较输出范式。
- **Source**: ['Sec 4.2', 'Sec 4.5']

## LLM
- **Value**: Vicuna v1.5
- **Rationale**: Training Process说明ORION采用Vicuna v1.5并用LoRA微调。
- **Search range**: 论文未报告其他LLM主模型设置
- **Sensitivity**: 论文未单独消融LLM型号；限制部分指出scalable VLM计算复杂度限制实时驾驶。
- **Source**: ['Sec 4.2', 'Sec 5']

## LoRA设置
- **Value**: rank dimension和alpha均为16
- **Rationale**: Training Process显式说明LoRA的rank dimension和alpha设置。
- **Search range**: rank dimension=16；alpha=16
- **Sensitivity**: 论文未报告LoRA rank或alpha敏感性。
- **Source**: ['Sec 4.2']

## QT-Former scene queries
- **Value**: 512
- **Rationale**: Training Process给出默认scene queries数量。
- **Search range**: 默认值512
- **Sensitivity**: 论文未单独消融scene queries数量。
- **Source**: ['Sec 4.2']

## QT-Former perception queries
- **Value**: 600
- **Rationale**: Training Process给出默认perception queries数量。
- **Search range**: 默认值600
- **Sensitivity**: 论文未单独消融perception queries数量。
- **Source**: ['Sec 4.2']

## QT-Former history queries
- **Value**: 16
- **Rationale**: Training Process给出默认historical queries数量，Table 5进一步消融history queries数量。
- **Search range**: 消融包含0、8、16、32
- **Sensitivity**: history queries数量存在甜点；过多history queries会阻碍VLM捕获当前帧特征。
- **Source**: ['Sec 4.2', 'Sec 4.5 Tab. 5']

## Memory Bank stored frame number
- **Value**: n=16
- **Rationale**: Training Process显式说明Memory Bank存储帧数n设为16。
- **Search range**: 默认n=16
- **Sensitivity**: Memory Bank结合历史QA监督带来方向性提升；论文未单独消融n。
- **Source**: ['Sec 4.2', 'Sec 4.5 Tab. 4']

## generative planner主模型
- **Value**: VAE加GRU decoder
- **Rationale**: Sec 3.3说明使用VAE将reasoning space和action space对齐到Gaussian distribution，并使用GenAD中的GRU decoder从latent space解码轨迹。
- **Search range**: 主模型为VAE；替代生成器为diffusion model
- **Sensitivity**: VAE-based trajectory generator相对diffusion-based在闭环与开放环方向性更优，论文归因于latent space更直接对齐且训练更稳定。
- **Source**: ['Sec 3.3', 'Sec 4.5 Tab. 3']

## QT-Former任务头
- **Value**: object detection、traffic state、motion prediction
- **Rationale**: QT-Former的perception queries输入多个辅助头，用于检测关键对象和车道、traffic state以及动态agent motion prediction。
- **Search range**: 检测、traffic state、motion prediction三类辅助任务
- **Sensitivity**: traffic state、motion prediction和memory bank的组合消融显示QT-Former设计会影响闭环表现。
- **Source**: ['Sec 3.1', 'Sec 4.5 Tab. 4']
