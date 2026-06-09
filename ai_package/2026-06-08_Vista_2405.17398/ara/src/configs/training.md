## 训练框架
- **Value**: EDM连续时间步扩散框架 + AdamW优化器
- **Rationale**: 基于SVD预训练权重采用EDM框架进行持续预训练；AdamW提供权重衰减正则化
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 高
- **Source**: Appendix C.3

## 阶段一训练分辨率
- **Value**: 576×1024
- **Rationale**: 阶段一直接在目标分辨率下训练全量UNet参数，确保高保真预测能力
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 高
- **Source**: Appendix C.3

## 阶段一迭代步数
- **Value**: 20K
- **Rationale**: 在128块A100 GPU上训练约8天所对应的迭代步数
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 中
- **Source**: Appendix C.3

## 阶段一GPU配置
- **Value**: 128 A100 GPUs
- **Rationale**: 大规模分布式训练以支持576×1024高分辨率和大有效批量
- **Search range**: N/A
- **Sensitivity**: N/A
- **Source**: Appendix C.3

## 阶段一有效批量大小
- **Value**: 256
- **Rationale**: 梯度累积2步实现；实际有效批量大小为256
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 中
- **Source**: Appendix C.3

## 阶段一学习率
- **Value**: 1×10^-5
- **Rationale**: 全局AdamW学习率；空间层学习率另乘以0.1折扣因子
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 高
- **Source**: Appendix C.3

## 空间层学习率折扣因子
- **Value**: 0.1
- **Rationale**: 空间层使用更低学习率以保留预训练的视觉表示能力
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 中
- **Source**: Appendix C.3

## 动态增强损失权重λ1
- **Value**: 1.0
- **Rationale**: 最终损失L_final中L_dynamics项的权重系数
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 中
- **Source**: Appendix C.3, Eq. 6

## 结构保留损失权重λ2
- **Value**: 0.1
- **Rationale**: 最终损失L_final中L_structure项的权重系数，相对较小以平衡主扩散损失
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 中
- **Source**: Appendix C.3, Eq. 6

## 偏移噪声强度
- **Value**: 0.02
- **Rationale**: 偏移噪声 (offset noise) 有助于改善生成视频的时序平滑性
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 低
- **Source**: Appendix C.3

## 动态先验随机采样概率(0/1/2/3条件帧)
- **Value**: 1/15, 2/15, 4/15, 8/15
- **Rationale**: 概率随条件帧数递增，鼓励模型尽量利用更多阶动态先验；三帧条件概率最高
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 中
- **Source**: Appendix C.3

## 阶段二低分辨率训练分辨率
- **Value**: 320×576
- **Rationale**: 比目标分辨率训练吞吐量提升3.5倍，用于动作控制学习的主体训练阶段
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 中
- **Source**: Sec 3.2, Appendix C.3

## 阶段二低分辨率迭代步数
- **Value**: 120K
- **Rationale**: 动作控制学习的主体迭代步数，在320×576分辨率下进行
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 中
- **Source**: Appendix C.3

## 阶段二高分辨率微调步数
- **Value**: 10K
- **Rationale**: 在目标分辨率576×1024上进行短时微调，使学到的可控性适配高分辨率推理
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 中
- **Source**: Appendix C.3

## 阶段二批量大小
- **Value**: 8
- **Rationale**: 动作控制学习阶段每步批量大小
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 低
- **Source**: Appendix C.3

## 阶段二学习率
- **Value**: 5×10^-5
- **Rationale**: 动作控制阶段AdamW学习率，高于阶段一以加速LoRA收敛
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 高
- **Source**: Appendix C.3

## 动作模式dropout比例
- **Value**: 15%
- **Rationale**: 已激活动作模式的dropout比例，用于无分类器引导 (classifier-free guidance) 训练
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 低
- **Source**: Appendix C.3

## 协同训练采样比例(OpenDV-YouTube:nuScenes)
- **Value**: 1:1
- **Rationale**: 均等采样以平衡大规模无标注驾驶视频与有动作标注的nuScenes数据，维持泛化性的同时学习可控性
- **Search range**: 论文未提供候选范围
- **Sensitivity**: 中
- **Source**: Appendix C.3
