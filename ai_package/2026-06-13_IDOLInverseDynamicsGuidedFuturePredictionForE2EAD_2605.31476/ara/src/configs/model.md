## 输入模态与主干
- **Value**: ResNet34-based TransFuser backbone with image-LiDAR multi-modal fusion
- **Rationale**: 模型用 multi-modal image-LiDAR backbone following TransFuser，并在实现中采用 ResNet34-based TransFuser。
- **Search range**: Table 1 的公平比较使用 ResNet-34 image-backbone setting。
- **Sensitivity**: 论文主比较固定 ResNet-34 setting，未报告主干尺度敏感性。
- **Source**: Sec 3.2; Sec 4.2; Table 1

## 图像输入尺寸
- **Value**: 256 × 1024
- **Rationale**: 实现细节和 Table 6 均说明 stitched front-view image input resize 到 256 × 1024。
- **Search range**: 论文未报告其他输入尺寸。
- **Sensitivity**: 论文未报告输入分辨率消融。
- **Source**: Sec 4.2; Table 6

## BEV latent resolution
- **Value**: 8 × 8
- **Rationale**: 当前实现将 BEV representation 展平为 64 latent queries，BEV resolution 为 8 × 8。
- **Search range**: 论文未报告其他 BEV resolution。
- **Sensitivity**: 论文未报告 BEV resolution 消融。
- **Source**: Sec 4.2; Table 6

## Number of BEV queries
- **Value**: 64
- **Rationale**: Table 6 给出 Number of BEV queries 为 64。
- **Search range**: 论文未报告 query 数范围。
- **Sensitivity**: 论文未报告 BEV query 数敏感性实验。
- **Source**: Table 6

## Latent feature dimension
- **Value**: 256
- **Rationale**: 实现细节和 Table 6 均设置 latent feature dimension 为 256。
- **Search range**: 论文未报告其他 latent feature dimension。
- **Sensitivity**: 论文未报告 latent dimension 消融。
- **Source**: Sec 4.2; Table 6

## Planning horizon
- **Value**: 4 s
- **Rationale**: 模型使用 4 s planning horizon。
- **Search range**: 论文未报告其他 horizon。
- **Sensitivity**: 论文未报告 horizon 敏感性实验。
- **Source**: Sec 4.2; Table 6

## Waypoint interval
- **Value**: 0.5 s
- **Rationale**: 模型使用 0.5 s sampling interval。
- **Search range**: 论文未报告其他 interval。
- **Sensitivity**: 论文未报告 waypoint interval 消融。
- **Source**: Sec 4.2; Table 6

## Number of future waypoints
- **Value**: 8
- **Rationale**: 4 s horizon 和 0.5 s interval 产生 8 future waypoints，Table 6 也列出该配置。
- **Search range**: 论文未报告其他 waypoint 数。
- **Sensitivity**: 论文未报告 waypoint 数敏感性实验。
- **Source**: Sec 4.2; Table 6

## Trajectory-anchor vocabulary size
- **Value**: 256
- **Rationale**: 轨迹规划在 256 trajectory anchors 上进行，Table 6 也列出该大小。
- **Search range**: 论文未报告其他 vocabulary size。
- **Sensitivity**: 论文未报告 anchor vocabulary size 消融。
- **Source**: Sec 4.2; Table 6

## Closed-loop refinement iterations
- **Value**: 2
- **Rationale**: Table 6 将 closed-loop refinement iterations 设为 2，Table 3 显示两次 refinement 获得最佳方向性结果。
- **Search range**: Table 3 比较无 closed-loop、2 次与 3 次 refinement。
- **Sensitivity**: 加入 closed-loop refinement 优于仅 IDM，3 次 refinement 相比 2 次出现过度修正迹象。
- **Source**: Table 3; Table 6

## Inverse dynamics temporal input
- **Value**: 2 frame adjacent BEV transitions
- **Rationale**: IDM 对 adjacent latent imagined BEV states 解码，Table 4 说明 two-frame variant 更适合作为 planning-oriented motion refinement 的紧凑基础。
- **Search range**: Table 4 比较 2 frame 与 4 frame。
- **Sensitivity**: 更长未来窗口可能稀释局部 transition cues，two-frame setting 更优。
- **Source**: Sec 3.4.1; Table 4

## Inverse dynamics architecture
- **Value**: lightweight MLP-based inverse dynamics model with three-stage MLP transition encoder
- **Rationale**: Appendix A 说明 IDOL 采用 lightweight MLP-based IDM，将两帧 latent BEV query features concat 后经三阶段 MLP transition encoder 得到 spatial dynamics map，并聚合 global dynamics feature。
- **Search range**: 论文未报告更大 IDM 版本。
- **Sensitivity**: Limitations 指出 lightweight IDM 保持效率但可能限制复杂长时交互和细微 motion patterns。
- **Source**: Appendix A; Appendix G

## Dynamics branch design
- **Value**: dual-branch spatial and global dynamics
- **Rationale**: 空间分支提供局部 transition evidence，全局分支提供整体 calibration，二者融合形成 query update。
- **Search range**: Table 5 比较 w/o spatial branch、w/o global branch 与 dual-branch IDM。
- **Sensitivity**: 仅保留单一分支弱于 dual-branch，说明 spatial selectivity 与 global calibration 互补。
- **Source**: Sec 3.4.2; Table 5

## Global dynamics fusion
- **Value**: MLN
- **Rationale**: 论文使用 MLN-based fusion 将 global dynamics feature 融入 refined query。
- **Search range**: Table 11 比较 Additive、Concat-MLP 与 MLN。
- **Sensitivity**: 三种策略均有效，MLN-based fusion 方向性最好，说明 global transition information 的集成方式有影响。
- **Source**: Sec 3.4.2; Table 11

## 模型规模
- **Value**: 69.36M parameters
- **Rationale**: 实现细节报告模型包含 69.36M parameters。
- **Search range**: 论文未报告其他模型规模。
- **Sensitivity**: Limitations 指出 IDM 轻量化可能限制复杂长时交互建模能力。
- **Source**: Sec 4.2; Appendix G

## 推理速度
- **Value**: 17.65 FPS with batch size 1
- **Rationale**: 实现细节报告单 NVIDIA RTX 3090 GPU、batch size 1 下达到 17.65 FPS。
- **Search range**: 论文未报告其他推理 batch 或硬件。
- **Sensitivity**: 论文将该结果作为 practical inference efficiency 的证据，未做速度消融。
- **Source**: Sec 4.2
