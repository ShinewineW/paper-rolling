## 体素化空间范围
- **Value**: [[±51.2m],[±51.2m],[-5m,3m]]
- **Rationale**: 定义 3D environment voxelization 的空间边界。
- **Search range**: 论文未给出其他空间范围。
- **Sensitivity**: 空间范围决定 occupancy 与 flow prediction 的三维覆盖区域；论文未做范围消融。
- **Source**: Appendix C.3

## 体素分辨率
- **Value**: 0.2m
- **Rationale**: 用于把 3D environment voxelized 成固定体素网格。
- **Search range**: 论文未给出其他体素分辨率。
- **Sensitivity**: 分辨率影响三维结构细粒度与计算规模；论文未做分辨率消融。
- **Source**: Appendix C.3

## 体素体积大小
- **Value**: 512 × 512 × 40
- **Rationale**: 由空间范围与体素分辨率得到的 3D volume size。
- **Search range**: 论文未给出其他 volume size。
- **Sensitivity**: volume size 决定 occupancy target 的空间容量；论文未做直接消融。
- **Source**: Appendix C.3

## history encoder
- **Value**: BEVFormerbased encoder with image backbone, FPN neck, and six additional transformer encoder layers
- **Rationale**: 从历史相机图像提取多视角几何特征并转换为 BEV embeddings。
- **Search range**: 论文说明该 encoder derived from BEVFormerbased encoder；未给出替代 encoder。
- **Sensitivity**: Table 9 与 Sec D.1 指出主要延迟来自 historical encoder。
- **Source**: Sec 3.2；Appendix C.3；Sec D.1

## BEV query 空间分辨率
- **Value**: h,w = 200
- **Rationale**: 作为 BEV queries 的空间分辨率。
- **Search range**: 论文未给出其他 BEV query 分辨率。
- **Sensitivity**: 该设置影响 BEV 表示密度；论文未报告分辨率敏感性。
- **Source**: Appendix C.3

## world decoder 层数
- **Value**: three layers
- **Rationale**: world decoder 通过 temporal modeling 与 action condition 预测未来 BEV embeddings。
- **Search range**: 论文未给出其他层数。
- **Sensitivity**: 论文未报告 decoder depth 消融。
- **Source**: Sec 3.2；Appendix C.3

## world decoder 通道数
- **Value**: 256 channels
- **Rationale**: 每个 world decoder layer 使用该通道规模。
- **Search range**: 论文未给出其他通道数。
- **Sensitivity**: 论文未报告 channel size 消融。
- **Source**: Appendix C.3

## prediction heads 输出通道
- **Value**: 16
- **Rationale**: prediction heads 通过 channel-to-height operation 将 BEV embeddings 转为 3D semantic occupancy 与 flow predictions。
- **Search range**: 论文未给出其他输出通道。
- **Sensitivity**: 该通道数对应输出体积的高度维表示；论文未做消融。
- **Source**: Sec 3.2；Appendix C.3

## world decoder 注意力结构
- **Value**: deformable self-attention、temporal cross-attention、conditional cross-attention、feedforward network
- **Rationale**: 先建模 BEV query 上下文，再从历史 embeddings 提取时序信息，并注入 action conditions。
- **Search range**: Table 7 对 addition 与 cross-attention 的条件接口做消融。
- **Sensitivity**: cross-attention 比 addition 更有效，Fourier embedding 进一步改善条件注入。
- **Source**: Sec 3.2；Appendix A；Table 7

## 动作条件集合
- **Value**: velocity、steering angle、trajectory、commands
- **Rationale**: 不同粒度的 ego motion 与意图被编码后注入 world decoder，实现 action-controllable generation。
- **Search range**: 低层条件包括 velocity、steering angle、trajectory；高层条件包括 go forward、turn left、turn right。
- **Sensitivity**: 任意动作条件均优于 baseline；trajectory 与 velocity 对未来预测提升更明显，commands 对当前时刻更有帮助但对未来预测影响有限。
- **Source**: Sec 3.3；Table 3

## 条件编码接口
- **Value**: Fourier embeddings, concatenated and fused via learned projections, aligned with conditional cross-attention layers
- **Rationale**: 将异构动作条件统一成可供 world decoder cross-attention 使用的 embedding。
- **Search range**: 论文比较 addition、cross-attention 与 Fourier Embed。
- **Sensitivity**: cross-attention 更适合整合先验条件，Fourier embedding 可编码高频条件信息并带来额外提升。
- **Source**: Sec 3.3；Table 7

## occupancy-based planner 成本项
- **Value**: Agent-Safety Cost、Road-Safety Cost、Learned-Volume Cost
- **Rationale**: 用未来 occupancy 与 BEV latent features 评价候选轨迹并选择最优轨迹。
- **Search range**: Table 8 消融了 agent、road、volume 与 BEV refinement。
- **Sensitivity**: 每个 cost factor 都有助于安全规划，缺少 agent constraints 会导致更高 collision rate，BEV refinement 对提供综合 3D 信息很重要。
- **Source**: Sec 3.4；Table 8
