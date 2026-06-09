## 推理去噪步数
- **Value**: 2
- **Rationale**: 截断扩散策略从锚定高斯分布出发，2步即可达到良好规划质量，满足实时约束
- **Search range**: ablation探索了1/2/3步（Tab. 4）
- **Sensitivity**: 中
- **Source**: Sec 4.2，Tab. 4

## 级联扩散解码器层数
- **Value**: 2
- **Rationale**: 2层级联在规划质量与参数量/推理时间之间取得平衡；4层虽可略微提升但代价更高
- **Search range**: ablation探索了1/2/4层（Tab. 5）
- **Sensitivity**: 低
- **Source**: Sec 4.2，Tab. 5

## 图像骨干网络
- **Value**: ResNet-34（NAVSIM）/ ResNet-50（nuScenes）
- **Rationale**: 与基线Transfuser/SparseDrive对齐，保证公平比较；ImageNet预训练初始化
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec 4.2，Sec 4.7，补充材料 Sec A

## 模型总参数量（NAVSIM ResNet-34配置）
- **Value**: 60M
- **Rationale**: Transformer扩散解码器替代UNet，相比TransfuserTD（102M）减少参数约39%，同时提升规划质量
- **Search range**: Tab. 3中不同消融配置从57M到102M
- **Sensitivity**: 低
- **Source**: Tab. 2，Tab. 3

## 推理采样轨迹数量N_infer
- **Value**: 20
- **Rationale**: 推理阶段可灵活调整，训练时N_anchor=20，推理时N_infer可不同；默认20条覆盖潜在动作空间
- **Search range**: ablation探索了10/20/40（Tab. 6）
- **Sensitivity**: 中
- **Source**: Tab. 6，Sec 3.3

## 规划输出路径点数及时域范围
- **Value**: 8个路径点，覆盖4秒
- **Rationale**: 与NAVSIM评估协议对齐
- **Search range**: N/A
- **Sensitivity**: 低
- **Source**: Sec 4.2

## 空间交叉注意力特征来源
- **Value**: BEV特征（NAVSIM）/ PV特征（nuScenes）
- **Rationale**: 根据上游感知模块特性选择：Transfuser产出BEV特征，SparseDrive产出PV特征
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec 4.2，补充材料 Sec A

## 推理速度（NAVSIM ResNet-34）
- **Value**: 45 FPS（NVIDIA 4090）
- **Rationale**: 截断扩散2步+高效Transformer解码器（每步3.8ms，总规划耗时7.6ms）实现实时驾驶帧率
- **Search range**: N/A
- **Sensitivity**: N/A
- **Source**: Abstract，Tab. 2
