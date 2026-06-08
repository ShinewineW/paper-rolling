# Quarantined: 2026-06-07_CosmosWorldFoundationModelPlatformForPhysicalAI_2501.03575

- **arxiv_id**: 2501.03575
- **title**: Cosmos World Foundation Model Platform for Physical AI
- **source_url**: https://arxiv.org/pdf/2501.03575
- **tier**: 2
- **gate**: G3
- **reason**: hard-block survived the gate round budget

## Hard findings

- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): 'Cosmos Tokenizer 在 DAVIS 和 TokenBench 基准上所有指标上均超越对比的 tokenizer，如在 DAVIS 连续视频重建中实'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '在 ShotBench 四个子数据集上，TransNetV2 等端到端神经网络方法在 F1 指标上明显优于 PySceneDetect 和 Panda70M 等'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '在 RealEstate10K 测试集上，Cosmos-Predict1-7B-Text2World 的 Sampson 误差(0.355)远低于 VideoL'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '将 DiT 自适应层归一化(AdaLN)中的稠密线性投影替换为低秩分解(LoRA)，使 Cosmos-Predict1-7B 的参数量从约 11B 降至 7B('
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '在 RealEstate10K 测试集上，Cosmos-Predict1-7B-Video2World-Sample-CameraCond 的相机姿态估计成功率'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '在 Bridge 数据集测试集上，Cosmos-Predict1-7B-Video2World-Sample-ActionCond 在 PSNR(21.14)、'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '在 RDS 测试集上，Cosmos-Predict1-7B-Text2World-Sample-MultiView 的 FID(32.16 vs 60.84)、'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '系统会剪除视觉质量分数处于末尾区间（约 15%）的低质片段，并以一个宽松的美学阈值（3.5）保留动态信息丰富的画面——因为 Physical AI 任务并不追求'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '随后，通过语义嵌入进行 k‑means 聚类（k=10,000）并实施近重复删除，最终剔除约 30% 的训练数据，显著提升了样本多样性'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '为了评估重建能力，论文在视频基准 DAVIS、TokenBench 以及图像基准 MS-COCO、ImageNet-1K 上，与 CogVideoX、Omni-'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '论文在 ShotBench 的多子数据集上对比了 PySceneDetect、Panda70M、TransNetV2 和 AutoShot 等算法，发现端到端神'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '在 DL3DV-10K 上微调后，Cosmos 在 RealEstate10K 测试集（存在跨数据集分布偏移）上，相机轨迹恢复的旋转/平移误差以及视频质量的 F'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| VideoLDM (Blattmann et al., 2023) | 0.841 | 4.4% | 26.23 | 0.783 | 0.135 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| Cosmos-Predict1-7B-Text2World | 0.355 | 62.6% | 33.02 | 0.939 | 0.070 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| Cosmos-Predict1-7B-Video2World | 0.473 | 68.4% | 30.66 | 0.929 | 0.085 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| Cosmos-Predict1-4B | 0.433 | 35.6% | 32.56 | 0.933 | 0.090 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| Cosmos-Predict1-5B-Video2World | 0.392 | 27.0% | 32.18 | 0.931 | 0.090 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| Real Videos (Reference) | 0.431 | 56.4% | 35.38 | 0.962 | 0.054 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| BBC | Precision ↑ | 0.894 | 0.959 | 0.983 | 0.984 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| BBC | Recall ↑ | 0.884 | 0.653 | 0.951 | 0.922 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| BBC | F1 ↑ | 0.889 | 0.777 | 0.967 | 0.952 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| RAI | Precision ↑ | 0.856 | 0.933 | 0.918 | 0.889 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| RAI | Recall ↑ | 0.807 | 0.746 | 0.921 | 0.923 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| RAI | F1 ↑ | 0.831 | 0.829 | 0.919 | 0.906 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| SHOT | Precision ↑ | 0.769 | 0.949 | 0.883 | 0.866 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| SHOT | Recall ↑ | 0.673 | 0.462 | 0.767 | 0.804 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| SHOT | F1 ↑ | 0.718 | 0.622 | 0.821 | 0.834 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| ClipShots | Precision ↑ | 0.395 | 0.649 | 0.685 | 0.653 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| ClipShots | Recall ↑ | 0.602 | 0.424 | 0.772 | 0.781 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| ClipShots | F1 ↑ | 0.477 | 0.513 | 0.726 | 0.711 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| CamCo (Xu et al., 2024) | 43.0% | 8.277 | 0.185 | 57.49 | 433.24 |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| Cosmos-Predict1-7B-Video2World-Sample-CameraCond | 82.0% | 1.646 | 0.038 | 14.'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '| Method | PSNR ↑ | SSIM ↑ | Latent L2 ↓ | FVD ↓ |'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '在相机可控视频生成上，它以大规模预训练先验克服了跨数据集的分布偏移，在姿态估计成功率、FID 和 FVD 等各项指标上均显著优于此前的 SOTA 方法 CamC'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '在动作条件机器人视频预测中，Cosmos 同样在 Bridge 数据集上全面领先 IRASim-Action（Zhu et al.，2024），包括 PSNR、'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): 'LoRA 秩固定为 256，将原本约 110 亿参数的 AdaLN 层压缩近 36% 而性能不降，相当于用很轻量的外挂模块实现了多条件控制'
- [critical] report.md: empirical sentence carries a number but has no anchor (吸收-D1 hard gate): '- **语义理解与过滤**：InternVideo2 提取视频级语义嵌入用于文本过滤、类型分类和去重；VILA-13B（FP8 量化推理引擎）生成视频描述，为 '
- [major] logic/claims.md:C10: C10 is a descriptive claim but its experiment E14 lacks the required 'representative sampling' design
