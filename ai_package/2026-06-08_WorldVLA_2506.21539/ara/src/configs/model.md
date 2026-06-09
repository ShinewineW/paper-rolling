## 骨干网络
- **Value**: Chameleon (Team, 2024)
- **Rationale**: Chameleon 是面向混合模态的早融合基础模型，其图像 tokenizer 和 LLM 组件均在 512×512 分辨率下优化，适合作为 WorldVLA 初始化权重
- **Search range**: 固定选型
- **Sensitivity**: high
- **Source**: Sec 3.2

## 图像 tokenizer 类型
- **Value**: VQ-GAN（含针对人脸和显著区域的额外感知损失）
- **Rationale**: VQ-GAN 将图像离散化为 codebook token，可与文本 token 共享词表，支持单一 LLM 自回归统一建模；附加感知损失提升关键区域重建质量
- **Search range**: 固定选型
- **Sensitivity**: high
- **Source**: Sec 3.2

## 图像 tokenizer 压缩比
- **Value**: 16
- **Rationale**: 控制图像空间下采样倍率，决定每张图像所需的 token 数量
- **Search range**: 固定值
- **Sensitivity**: medium
- **Source**: Sec 3.2

## 图像 codebook 大小
- **Value**: 8192
- **Rationale**: VQ-GAN codebook 容量，决定图像离散化的表达精度
- **Search range**: 固定值
- **Sensitivity**: medium
- **Source**: Sec 3.2

## 256×256 图像对应 token 数
- **Value**: 256
- **Rationale**: 压缩比 16 下 256×256 图像映射为 256 个离散 token
- **Search range**: 固定值，由压缩比决定
- **Sensitivity**: medium
- **Source**: Sec 3.2

## 512×512 图像对应 token 数
- **Value**: 1024
- **Rationale**: 压缩比 16 下 512×512 图像映射为 1024 个离散 token；更高分辨率提供更多细节，有利于精细抓取任务，且与 Chameleon 预训练分辨率一致
- **Search range**: 固定值，由压缩比决定
- **Sensitivity**: high
- **Source**: Sec 3.2, Sec 4.2

## 动作 tokenizer 离散化 bin 数（每维）
- **Value**: 256
- **Rationale**: 将连续机器人动作每个维度均匀离散为 256 个区间，bin 宽由训练数据值域决定；与 OpenVLA 一致
- **Search range**: 固定值，参考 OpenVLA / RT-2 设计
- **Sensitivity**: medium
- **Source**: Sec 3.2

## 每步动作 token 数
- **Value**: 7
- **Rationale**: 机器人动作表示为 7 维：3 个相对位置、3 个相对角度、1 个绝对夹爪状态，每维对应 1 个 token
- **Search range**: 由机器人硬件约束决定
- **Sensitivity**: medium
- **Source**: Sec 3.2

## BPE 词表大小
- **Value**: 65536
- **Rationale**: 统一词表包含文本 token、8192 个图像 token 和 256 个动作 token，支持三模态自回归联合训练
- **Search range**: 固定值
- **Sensitivity**: low
- **Source**: Sec 3.2
