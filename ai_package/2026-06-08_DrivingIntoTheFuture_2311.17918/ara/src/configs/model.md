## 训练输入图像分辨率
- **Value**: 384×192
- **Rationale**: 从nuScenes原始1600×900裁剪顶部至1600×800后缩放，降低计算量
- **Search range**: 论文未给出范围
- **Sensitivity**: 高
- **Source**: Sec 5.1, Sec B.1

## 基础模型初始化权重
- **Value**: Stable Diffusion 预训练检查点
- **Rationale**: 利用图像生成先验，无需从零训练，仅对时序和多视角参数进行微调
- **Search range**: N/A
- **Sensitivity**: 高
- **Source**: Sec B.1

## 图像条件编码器
- **Value**: ConvNeXt
- **Rationale**: 将图像条件(初始帧、参考视角)编码为d维嵌入序列，与其他条件统一处理
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec 3.3

## 文本条件编码器
- **Value**: 预训练CLIP
- **Rationale**: 延续扩散模型惯例使用CLIP文本编码器，提取视角、天气、光线等语义描述特征
- **Search range**: N/A
- **Sensitivity**: 低
- **Source**: Sec 3.3

## 动作条件编码器
- **Value**: MLP
- **Rationale**: 将二维自车位移(Δx, Δy)映射为d维嵌入向量，接入统一条件接口
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec 3.3

## 条件注入机制
- **Value**: 跨注意力(cross attention)，逐帧注入3D UNet
- **Rationale**: 统一条件嵌入ct在每帧与去噪潜变量zt通过跨注意力交互，实现灵活多条件控制
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec 3.3

## 时序编码层结构
- **Value**: 3D卷积(空间时序维度THW) + 多头时序自注意力
- **Rationale**: 3D卷积捕获时空局部特征，时序自注意力建模帧间全局依赖，共同提升视频时序一致性
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec 3.1

## 多视角编码层结构
- **Value**: 视角维度自注意力(view-dimension self-attention)
- **Rationale**: 在视角维度上应用自注意力，使所有视角共享风格和整体结构
- **Search range**: N/A
- **Sensitivity**: 高
- **Source**: Sec 3.1

## nuScenes参考视角配置
- **Value**: 前视(F)、左后视(BL)、右后视(BR)
- **Rationale**: 参考视角间互不重叠，先联合生成参考视角视频，再以此为条件生成三个缝合视角
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec B.2

## Waymo推理图像分辨率
- **Value**: 768×512
- **Rationale**: Waymo数据集前置摄像头采用高分辨率推理，验证Drive-WM在不同数据集和分辨率下的泛化能力
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec A.6
