## 图像扩散模型训练迭代数
- **Value**: 60000
- **Rationale**: 在Stable Diffusion预训练权重基础上充分训练条件图像扩散模型
- **Search range**: 论文未给出范围
- **Sensitivity**: 中
- **Source**: Sec B.1

## 图像模型总批次大小
- **Value**: 768
- **Rationale**: 大批次训练有助于扩散模型稳定收敛
- **Search range**: 论文未给出范围
- **Sensitivity**: 中
- **Source**: Sec B.1

## 图像模型学习率
- **Value**: 1e-4
- **Rationale**: AdamW优化器配合的标准图像扩散模型学习率
- **Search range**: 论文未给出范围
- **Sensitivity**: 高
- **Source**: Sec B.1

## 视频模型微调迭代数
- **Value**: 40000
- **Rationale**: 在图像模型基础上微调时序和多视角参数，所需步数少于图像模型训练
- **Search range**: 论文未给出范围
- **Sensitivity**: 中
- **Source**: Sec B.1

## 视频模型批次大小
- **Value**: 32
- **Rationale**: 视频序列显存占用大，批次大小受GPU显存约束
- **Search range**: 论文未给出范围
- **Sensitivity**: 中
- **Source**: Sec B.1

## 视频训练帧长度T
- **Value**: 8
- **Rationale**: 每个训练样本包含T=8帧多视角视频，平衡时序建模效果与显存开销
- **Search range**: 论文未给出范围
- **Sensitivity**: 中
- **Source**: Sec B.1

## 视频模型学习率
- **Value**: 5e-5
- **Rationale**: 微调阶段使用更小学习率，保护已冻结的空间参数
- **Search range**: 论文未给出范围
- **Sensitivity**: 高
- **Source**: Sec B.1

## 条件随机丢弃概率(CFG训练)
- **Value**: 0.20
- **Rationale**: 训练时以20%概率随机丢弃每个条件，使模型支持无条件生成，以便推理时使用分类器自由引导(CFG)
- **Search range**: 论文未给出范围
- **Sensitivity**: 中
- **Source**: Sec B.1

## DDIM推理采样步数
- **Value**: 50
- **Rationale**: 推理阶段采用50步DDIM采样，兼顾生成质量与推理速度
- **Search range**: 论文未给出范围
- **Sensitivity**: 中
- **Source**: Sec B.1

## DDIM随机性参数η
- **Value**: 1.0
- **Rationale**: η=1.0对应DDPM随机采样，保留生成多样性
- **Search range**: [0, 1]
- **Sensitivity**: 中
- **Source**: Sec B.1

## 分类器自由引导强度CFG
- **Value**: 5.0
- **Rationale**: CFG=5.0增强条件对生成内容的控制效果
- **Search range**: 论文未给出范围
- **Sensitivity**: 高
- **Source**: Sec B.1

## 动作数据均衡采样每格数量N
- **Value**: 36
- **Rationale**: 对(转向角×速度)分布的每个分箱采样N=36个片段，缓解nuScenes动作分布不均衡问题
- **Search range**: 论文未给出范围
- **Sensitivity**: 中
- **Source**: Sec C.2
