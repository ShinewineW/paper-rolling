## 轨迹词表规模 N
- **Value**: 8192
- **Rationale**: Intention Encoder 使用 trajectory vocabulary，并在默认设置中给出 N。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 论文未报告 N 的敏感性。
- **Source**: Sec 3.2.1 Intention Encoder

## 每个命令的意图数 K
- **Value**: 6
- **Rationale**: Intention Encoder 默认设置 K，nuScenes 实现也说明每个命令预测 6 条规划轨迹。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 论文消融表明意图建模方向上有收益，但未单独扫描 K。
- **Source**: Sec 3.2.1 Intention Encoder; Sec 4.2 Implementation Details

## nuScenes 图像骨干
- **Value**: ResNet-50
- **Rationale**: 论文遵循 VAD-Tiny 配置，在 nuScenes 上采用 ResNet-50。
- **Search range**: ResNet-34, ResNet-50, ResNet-101
- **Sensitivity**: 可扩展性消融显示扩大 image backbone 会影响规划表现。
- **Source**: Sec 4.2 Implementation Details; Tab. 6

## NavSim 图像骨干
- **Value**: ResNet-34
- **Rationale**: 论文在 NavSim 实现细节中说明采用 ResNet-34 提取图像特征。
- **Search range**: 论文未给出 NavSim 骨干搜索范围。
- **Sensitivity**: 论文未报告 NavSim 骨干敏感性。
- **Source**: Sec 4.2 Implementation Details

## nuScenes 输入视角与分辨率
- **Value**: 6 surround-view images, 360 × 640
- **Rationale**: 论文在 nuScenes 实现细节中说明输入多视角图像数量与分辨率。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 论文未报告输入分辨率敏感性。
- **Source**: Sec 4.2 Implementation Details

## NavSim 输入视图与分辨率
- **Value**: front, front-left, front-right stitched image, 256×1024
- **Rationale**: 论文说明闭环模型将三个前向相机视图拼接后 resize。
- **Search range**: 论文未给出搜索范围。
- **Sensitivity**: 论文未报告输入视图或分辨率敏感性。
- **Source**: Sec 4.2 Implementation Details

## 深度先验模型
- **Value**: giant model from Metric3D v2
- **Rationale**: 论文在视觉基础模型设置中说明用于 depth estimation 的模型。
- **Search range**: 论文未给出替代模型范围。
- **Sensitivity**: 组件消融显示 depth 先验对轨迹拟合方向有帮助，但未比较不同深度模型。
- **Source**: Sec 4.2 Implementation Details; Sec 4.4.1

## 语义先验模型
- **Value**: Grounded-SAM
- **Rationale**: 论文说明使用 Grounded-SAM 进行 semantic segmentation，并用伪语义标签增强 latent 表征。
- **Search range**: 论文未给出替代模型范围。
- **Sensitivity**: 组件消融显示 semantic 先验对碰撞方向有帮助，但未比较不同语义模型。
- **Source**: Sec 3.2.2 Physical World Latent Encoding; Sec 4.2 Implementation Details; Sec 4.4.1

## 隐藏维度 D
- **Value**: 256
- **Rationale**: Tab. 6 将 ResNet-50 与 Dimension 256 作为完整设置之一，并比较 128、256、384。
- **Search range**: 128, 256, 384
- **Sensitivity**: 可扩展性消融显示扩大 hidden dimension 会影响规划表现。
- **Source**: Tab. 6

## 推理期轨迹选择
- **Value**: 选择 world model 最高 score 对应的 trajectory
- **Rationale**: 论文明确区分推理期直接选择最高 score 的轨迹。
- **Search range**: 论文未给出替代推理策略范围。
- **Sensitivity**: 论文未报告推理选择规则敏感性。
- **Source**: Sec 3.3.2 World Model Selector
