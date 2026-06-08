# Heuristics

## H1: 每个控制分支使用 3 个 transformer 块（而非更多）
- **Rationale**: 经验表明 3 块在控制有效性与推理效率之间取得良好平衡
- **Sensitivity**: 块数影响控制表达力与推理开销的权衡
- **Bounds**: 论文选择 3 块，无其他数值的消融实验
- **Code ref**: [Fig. 1(b), Section 2]
- **Source**: Section 2

## H2: 多模态时空权重之和超过 1 时对各模态权重归一化，使其在该时空位置的和为 1
- **Rationale**: 防止多模态控制信号叠加过强而导致生成退化
- **Sensitivity**: 高权重之和场景下影响输出质量
- **Bounds**: 触发条件：sum of w_i > 1
- **Code ref**: [Section 3]
- **Source**: Section 3

## H3: Blur Visual 控制分支训练时对双边滤波（bilateral blur）的各参数进行随机化，作为数据增强策略
- **Rationale**: 提高控制分支对不同模糊程度输入的鲁棒性
- **Sensitivity**: 影响 Vis 控制的泛化能力
- **Bounds**: 随机化范围由超参数决定，论文未给出具体数值
- **Code ref**: [Section 4 (Blur visual)]
- **Source**: Section 4

## H4: Edge 控制分支训练时对 Canny 边缘检测器的各阈值参数进行随机化，作为数据增强策略
- **Rationale**: 提高对不同强度边缘输入的泛化能力
- **Sensitivity**: 影响 Edge F1 对齐性能
- **Bounds**: 随机化范围由超参数决定，论文未给出具体数值
- **Code ref**: [Section 4 (Edge)]
- **Source**: Section 4

## H5: 深度图使用 DepthAnything2 提取后归一化至 [0, 1] 范围
- **Rationale**: 统一深度值范围，便于控制分支学习一致的深度表示
- **Sensitivity**: 归一化范围直接影响深度控制信号的数值分布
- **Bounds**: [0, 1]
- **Code ref**: [Section 4 (Depth)]
- **Source**: Section 4

## H6: 分割图中各对象的颜色进行随机化，颜色不再携带语义含义，仅用于区分不同对象实例
- **Rationale**: 避免模型学习依赖固定颜色与语义的绑定关系，提高泛化能力
- **Sensitivity**: 颜色随机化导致分割控制对几何/语义约束较弱，多样性较高
- **Bounds**: 完全随机，无固定颜色与类别对应
- **Code ref**: [Section 4 (Segmentation)]
- **Source**: Section 4

## H7: SalientObject 算法中，前景区域分配 Vis 权重 0.5 + Edge 权重 0.5，背景区域分配 Depth 权重 0.5 + Seg 权重 0.5
- **Rationale**: 前景需高保真度（Vis/Edge 约束强），背景允许多样化（Depth/Seg 约束弱）
- **Sensitivity**: 前景 Vis 权重从 0 增至 0.5 可将前景 Blur SSIM 从 0.43 提升至 0.81（Pearson 相关 0.93）
- **Bounds**: 前景/背景各模态权重均为 0.5
- **Code ref**: [Section 5.2, Fig. 6]
- **Source**: Section 5.2

## H8: 4KUpscaler 推理时将 4K 帧划分为 3×3 个重叠格，每步去噪对所有格并行推理，重叠区域结果取平均
- **Rationale**: 保证输出视频边界无缝衔接，避免拼接处的明显边界伪影
- **Sensitivity**: 重叠区域大小影响边界平滑程度与计算量
- **Bounds**: 3×3 格
- **Code ref**: [Section 4 (4KUpscaler)]
- **Source**: Section 4

## H9: LiDAR 数据与相机帧同步：每帧选最近 LiDAR 扫描及前后各 2 帧（共 5 帧）提供时序上下文，投影孔洞用 kernel size 4 做核插值填补
- **Rationale**: LiDAR 采样率（10 FPS）低于相机（30 FPS），插值与多帧融合弥补时序间隔导致的稀疏性
- **Sensitivity**: kernel size 与相邻帧数影响 LiDAR 投影密度及动态对象位置精度
- **Bounds**: 相邻帧数 4，kernel size 4
- **Code ref**: [Section 4 (LiDAR)]
- **Source**: Section 4
