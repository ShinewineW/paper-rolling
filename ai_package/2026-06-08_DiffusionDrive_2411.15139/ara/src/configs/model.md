## 图像主干网络（NAVSIM）
- **Value**: ResNet-34
- **Rationale**: 与Transfuser基线保持一致以进行公平比较
- **Search range**: ResNet-34（NAVSIM），ResNet-50（nuScenes）
- **Sensitivity**: 高
- **Source**: Sec 4.2

## 图像主干网络（nuScenes）
- **Value**: ResNet-50
- **Rationale**: 遵循SparseDrive基线配置
- **Search range**: 论文未进行消融实验
- **Sensitivity**: 高
- **Source**: Sec 4.7

## 图像输入分辨率
- **Value**: 1024×256
- **Rationale**: 三张裁剪并下采样的前向摄像头图像水平拼接而成
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec 4.2

## 级联扩散解码器层数
- **Value**: 2
- **Rationale**: 消融实验（Table 5）表明2层在性能与参数量之间取得最佳平衡，4层时性能趋于饱和且参数增加
- **Search range**: 1-4
- **Sensitivity**: 中
- **Source**: Sec 4.2, Table 5

## 推理去噪步数
- **Value**: 2
- **Rationale**: 截断扩散策略使仅需2步即可获得高质量多模式轨迹，相比标准DDIM的20步减少10倍
- **Search range**: 1-3
- **Sensitivity**: 低（消融实验显示1步已达到接近质量）
- **Source**: Sec 4.2, Table 4

## 规划时域输出格式
- **Value**: 8个路径点，覆盖4秒
- **Rationale**: 与Transfuser基线保持一致的输出格式
- **Search range**: N/A
- **Sensitivity**: 中
- **Source**: Sec 4.2

## 推理采样轨迹数量（N_infer）
- **Value**: 20
- **Rationale**: 消融实验（Table 6）显示20个采样轨迹在规划质量与计算效率之间取得良好平衡
- **Search range**: 10-40
- **Sensitivity**: 中
- **Source**: Table 6

## LiDAR感知范围
- **Value**: 前后左右各32m
- **Rationale**: 遵循Transfuser基线的LiDAR输入范围配置
- **Search range**: N/A
- **Sensitivity**: 低
- **Source**: Appendix A

## 扩散解码器空间注意力类型
- **Value**: 稀疏可变形交叉注意力
- **Rationale**: 基于轨迹坐标与BEV或透视视图特征进行空间交叉注意力，消融实验（ID-3与ID-2对比）验证其对规划质量至关重要
- **Search range**: N/A
- **Sensitivity**: 高
- **Source**: Sec 3.4, Table 3

## 模型总参数量
- **Value**: 60M
- **Rationale**: 采用轻量级Transformer解码器替代UNet，相比TransfuserDP的101M减少约39%参数，同时达到更高规划质量
- **Search range**: N/A
- **Sensitivity**: 低
- **Source**: Table 2, Table 3
