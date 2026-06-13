## nuScenes 训练轮数
- **Value**: 12 epochs
- **Rationale**: 论文在 nuScenes 实现细节中说明训练轮数。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 训练收敛速度是论文关注点之一，但未给出该超参数的敏感性实验。
- **Source**: Sec 4.2 Implementation Details

## nuScenes 总 batch size
- **Value**: 8
- **Rationale**: 论文在 nuScenes 实现细节中说明总 batch size。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 论文未报告 batch size 敏感性。
- **Source**: Sec 4.2 Implementation Details

## nuScenes 初始学习率
- **Value**: 5e-5
- **Rationale**: 论文在 nuScenes 实现细节中说明 initial learning rate。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 论文未报告学习率敏感性。
- **Source**: Sec 4.2 Implementation Details

## NavSim 训练轮数
- **Value**: 60 epochs
- **Rationale**: 论文在 NavSim 实现细节中说明训练轮数。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 论文未报告该训练轮数的敏感性实验。
- **Source**: Sec 4.2 Implementation Details

## NavSim 总 batch size
- **Value**: 64
- **Rationale**: 论文在 NavSim 实现细节中说明总 batch size。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 论文未报告 batch size 敏感性。
- **Source**: Sec 4.2 Implementation Details

## 损失权重
- **Value**: α = 0.2, β = 0.2, γ = 0.5, η = 1.0
- **Rationale**: 训练目标将语义、重建、评分和轨迹项加权求和，论文给出默认权重。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 论文未报告这些损失权重的消融。
- **Source**: Sec 3.4 Training Loss

## 训练损失公式
- **Value**: $$\mathcal { L } = \alpha \mathcal { L } _ { s e m } + \beta \mathcal { L } _ { r e c o n } + \gamma \mathcal { L } _ { s c o r e } + \eta \mathcal { L } _ { t r a j } ,$$
- **Rationale**: 论文显式给出端到端训练的最终损失公式。
- **Search range**: 论文未给出其他训练目标公式。
- **Sensitivity**: 论文未报告最终损失结构的完整替代实验。
- **Source**: Sec 3.4 Training Loss

## 未来时间间隔 n
- **Value**: n = 3
- **Rationale**: 论文说明 intention-aware world model 预测未来 latent 时的默认 timestamp interval。
- **Search range**: 论文称补充材料中有 timestamp interval n 的消融，正文未给出范围。
- **Sensitivity**: 正文未给出该参数消融结果。
- **Source**: Sec 3.3.1 Intention-aware World Model Dreamer
