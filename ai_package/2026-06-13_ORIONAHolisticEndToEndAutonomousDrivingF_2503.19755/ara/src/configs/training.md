## 训练数据集
- **Value**: Bench2Drive base set：1000 clips；划分为950 clips训练和50 clips开放环验证
- **Rationale**: 论文说明为与基线公平比较，训练和评估使用Bench2Drive base set，并给出训练与验证划分。
- **Search range**: 训练集为950 clips；开放环验证为50 clips；闭环评估使用220 short routes、44 interactive scenarios、每场景5 routes
- **Sensitivity**: 数据规模和闭环路线覆盖影响模型对交互场景的泛化，论文将Bench2Drive作为主评估环境。
- **Source**: ['Sec 4.1']

## Chat-B2D VQA数据
- **Value**: 2.11M VQA pairs用于训练，0.12M用于验证
- **Rationale**: 论文为弥补闭环模拟环境中高质量VQA标注缺口，构建Chat-B2D并用于VQA相关训练。
- **Search range**: 覆盖Scene description、Behavior description、Meta-driving decisions and action reasoning、Recall of essential historical information四类任务
- **Sensitivity**: VQA数据用于增强场景理解、历史信息回忆和动作推理；消融表明单任务训练不能同时获得推理与规划能力。
- **Source**: ['Appendix A.2', 'Sec 4.5 Tab. 6']

## 训练策略
- **Value**: three-stage training strategy
- **Rationale**: 论文采用逐阶段空间对齐训练，使模型继承上一阶段权重并继续训练，逐步增强推理和规划能力。
- **Search range**: 3D Vision-Language Alignment；Language-Action Alignment；End-to-End Fine-tuning
- **Sensitivity**: 训练流水线消融显示逐步完成V-L、L→A和V→L→A对齐后闭环表现方向性提升。
- **Source**: ['Appendix B', 'Appendix C.2 Tab. A2']

## 每阶段训练轮数
- **Value**: six epochs per stage
- **Rationale**: Appendix B显式说明每个训练阶段训练six epochs。
- **Search range**: 每个阶段均为six epochs
- **Sensitivity**: 论文未给出轮数敏感性消融，仅将其作为训练细节。
- **Source**: ['Appendix B']

## 总batch size
- **Value**: 32
- **Rationale**: Appendix B显式说明训练使用total batch size of 32。
- **Search range**: 论文未报告其他batch size设置
- **Sensitivity**: 论文未给出batch size敏感性消融。
- **Source**: ['Appendix B']

## 图像增强与输入分辨率
- **Value**: 训练时对输入图像做data augmentations，并先resize到640 × 640
- **Rationale**: 实现细节说明训练中对输入图像进行增强，且先调整到指定分辨率。
- **Search range**: 640 × 640
- **Sensitivity**: 论文未单独消融输入分辨率或增强策略。
- **Source**: ['Sec 4.2']

## 第一阶段训练内容
- **Value**: 主要训练QT-Former和VLM，冻结generative planner，并使用Chat-B2D的VQA pairs对齐vision space与reasoning space
- **Rationale**: 第一阶段目标是3D Vision-Language Alignment。
- **Search range**: 冻结generative planner；训练QT-Former和VLM
- **Sensitivity**: 缺少第一阶段时，后续规划训练的闭环效果方向性下降。
- **Source**: ['Appendix B', 'Appendix C.2 Tab. A2']

## 第二阶段训练内容
- **Value**: 解冻generative planner，训练除LLM外的整个模型；LLM通过LoRA训练；不使用auxiliary VQA pairs预测planning trajectories
- **Rationale**: 第二阶段目标是Language-Action Alignment，将world knowledge从reasoning space传递到action space。
- **Search range**: 不使用auxiliary VQA pairs；LLM使用LoRA
- **Sensitivity**: 第二阶段相对直接规划训练带来方向性提升。
- **Source**: ['Appendix B', 'Appendix C.2 Tab. A2']

## 第三阶段训练内容
- **Value**: 沿用上一阶段设置，并加入VQA和planning tasks联合训练
- **Rationale**: 第三阶段End-to-End Fine-tuning进一步促进vision-reasoning-action space对齐。
- **Search range**: 联合训练VQA与planning tasks
- **Sensitivity**: 联合训练相对单任务训练在规划与语言指标上方向性更优。
- **Source**: ['Appendix B', 'Sec 4.5 Tab. 6']

## 训练目标
- **Value**: QT-Former使用检测、traffic state和motion prediction相关损失；LLM使用auto-regressive crossentropy loss；generative planner使用Kullback-Leibler divergence、collision、boundary和MSE loss
- **Rationale**: Sec 3.4显式给出ORION的训练目标组成。
- **Search range**: 总目标为QT-Former、LLM和generative planner三部分损失之和
- **Sensitivity**: 论文没有单独给出各损失权重敏感性；但QT-Former设计和训练任务消融显示这些监督项影响闭环表现。
- **Source**: ['Sec 3.4', 'Sec 4.5 Tab. 4']
