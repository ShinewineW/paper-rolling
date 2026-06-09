## 训练轮次（NAVSIM）
- **Value**: 100
- **Rationale**: 在navtrain上从头训练，足够轮次使模型充分收敛
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 中
- **Source**: Sec 4.2

## 学习率
- **Value**: 6e-4
- **Rationale**: 沿用Transfuser基线训练配置，保证公平对比
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 高
- **Source**: Sec 4.2

## 优化器
- **Value**: AdamW
- **Rationale**: 标准自适应优化器，与基线保持一致
- **Search range**: N/A
- **Sensitivity**: 低
- **Source**: Sec 4.2

## 总批量大小
- **Value**: 512
- **Rationale**: 在8张GPU上分布式训练的总批量大小
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 中
- **Source**: Sec 4.2

## 扩散噪声截断比例（训练）
- **Value**: 50/1000
- **Rationale**: 截断扩散调度，只对锚点轨迹添加少量高斯噪声，使模型学习从锚定高斯分布去噪至真实轨迹分布
- **Search range**: 论文未系统探索该超参数的消融范围
- **Sensitivity**: 高
- **Source**: Sec 4.2

## 训练锚点数量（K-Means聚类）
- **Value**: 20（NAVSIM）/ 18（nuScenes）
- **Rationale**: K-Means聚类训练集轨迹得到先验锚点，少量锚点即可覆盖主要驾驶模式，远少于VADv2的8192个
- **Search range**: 论文仅报告NAVSIM推理时N_infer = 10/20/40的消融（Tab. 6），训练锚点数量本身未消融
- **Sensitivity**: 中
- **Source**: Sec 4.2，Sec 4.7

## 训练损失函数
- **Value**: L1重建损失与BCE分类损失加权组合（权重λ，具体数值未给出）
- **Rationale**: 正样本（最近锚点）计算L1轨迹重建损失，所有锚点计算BCE分类损失；λ平衡两项
- **Search range**: 论文未给出λ的搜索范围
- **Sensitivity**: 中
- **Source**: Eq. 6，Sec 3.3

## 输入图像尺寸
- **Value**: 1024×256
- **Rationale**: 三张前向相机图像裁剪缩放后拼接成单张图，沿用Transfuser输入设置
- **Search range**: N/A
- **Sensitivity**: 低
- **Source**: Sec 4.2

## nuScenes阶段2训练轮次
- **Value**: 10
- **Rationale**: 在SparseDrive阶段1感知预训练权重基础上，仅微调规划模块，轮次较少
- **Search range**: 论文未给出搜索范围
- **Sensitivity**: 中
- **Source**: 补充材料 Sec A
