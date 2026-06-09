## α（世界模型损失权重）
- **Value**: 0.04
- **Rationale**: 图像 token 数量（256×256 时 256 个，512×512 时 1024 个）远多于动作 token（7 个），需用 α 平衡两路损失贡献，防止图像生成损失淹没动作损失
- **Search range**: 论文未报告超参搜索范围
- **Sensitivity**: high
- **Source**: Sec 3.3, Eq. 4

## M（历史图像帧数，默认值）
- **Value**: 2
- **Rationale**: 单帧输入效果不足；消融实验表明双帧时成功率趋于饱和（尤其启用动作分块时），是成功率与计算开销的最优折衷
- **Search range**: 论文测试了 1、2、4 帧（见 Table 5）
- **Sensitivity**: high
- **Source**: Sec 4.1, Table 5

## K（动作块大小，LIBERO-Long 任务）
- **Value**: 10
- **Rationale**: LIBERO-Long 为长视野任务，需要生成更长的动作序列
- **Search range**: Fig. 6 展示了多种 K 值的消融结果
- **Sensitivity**: high
- **Source**: Sec 4.1

## K（动作块大小，其余三个 LIBERO 任务）
- **Value**: 5
- **Rationale**: 短视野任务的默认配置
- **Search range**: Fig. 6 展示了多种 K 值的消融结果
- **Sensitivity**: medium
- **Source**: Sec 4.1

## N（世界模型单样本循环次数）
- **Value**: 1
- **Rationale**: 为降低计算开销，世界模型每条训练样本仅进行一轮下一帧预测
- **Search range**: 论文未报告其他取值
- **Sensitivity**: medium
- **Source**: Sec 4.1

## 训练集/验证集划分比例
- **Value**: 90% / 10%
- **Rationale**: 世界模型评估需要真值配对的视频与动作数据，因此保留 10% 轨迹作为验证集；Table 2 主实验使用全量数据以保证公平比较
- **Search range**: 固定值
- **Sensitivity**: low
- **Source**: Sec 4.1

## 动作模型每任务评估 rollout 次数
- **Value**: 50
- **Rationale**: 在不同初始状态下运行 50 次以统计任务成功率（SR），保证评估统计稳健性
- **Search range**: 固定值
- **Sensitivity**: low
- **Source**: Sec 4.1
