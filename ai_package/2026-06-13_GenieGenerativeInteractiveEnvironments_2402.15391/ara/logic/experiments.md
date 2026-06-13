# Experiments

## E1: latent action model 输入形式消融
- **Verifies**: C1, C2
- **Setup**:
  - Model: Token-input 与 Pixel-input (Genie) latent action model 变体
  - Hardware: 论文未在该消融段落单独点名硬件
  - Dataset: Platformers 与 Robotics
  - System: 相同任务下比较 LAM 读取 tokenized images 或 original images
- **Procedure**:
  1. 分别训练 token-input 与 Pixel-input 版本。
  2. 在 Platformers 与 Robotics 上评估 video fidelity 与 controllability。
  3. 比较 FVD 与 ΔPSNR 的方向性差异。
- **Metrics**: ['FVD', 'ΔPSNR']
- **Expected outcome**: Pixel-input 在 controllability 上优于 token-input，Robotics 上 fidelity 也更优；Platformers 上 fidelity 存在轻微 trade-off。
- **Baselines**: ['Token-input']
- **Dependencies**: ['video tokenizer', 'latent action model', 'dynamics model']

## E2: tokenizer architecture 消融
- **Verifies**: C3
- **Setup**:
  - Model: ViT、C-ViViT、ST-ViViT tokenizer
  - Hardware: 论文未在该段落单独点名硬件
  - Dataset: Platformers
  - System: 使用相同 dynamics 与 latent action model 比较不同 tokenizer
- **Procedure**:
  1. 训练三个 tokenizer architecture 选择。
  2. 在相同下游 dynamics 与 latent action model 设置中进行视频生成。
  3. 报告 FVD 与 ΔtPSNR 并比较方向。
- **Metrics**: ['FVD', 'ΔtPSNR', 'Memory']
- **Expected outcome**: ST-ViViT 在 fidelity 与 controllability 上整体最好，同时保持合理 memory trade-off。
- **Baselines**: ['ViT', 'C-ViViT']
- **Dependencies**: ['dynamics model', 'latent action model', 'Platformers videos']

## E3: Platformers 数据筛选效果评估
- **Verifies**: C4
- **Setup**:
  - Model: 相同参数规模的模型
  - Hardware: 论文未在该段落单独点名硬件
  - Dataset: Original dataset 与 Curated dataset
  - System: 使用 learned classifier 过滤低质量 gameplay clips 后比较训练结果
- **Procedure**:
  1. 从公开 Internet videos 构建 original Platformers clips。
  2. 人工标注一部分视频质量并训练 ResNet18 classifier。
  3. 用决策规则筛选数据，分别在 original 与 curated 数据上训练模型。
  4. 用 FVD 比较结果方向。
- **Metrics**: ['FVD']
- **Expected outcome**: Curated dataset 训练出的模型 FVD 更低。
- **Baselines**: ['Original dataset']
- **Dependencies**: ['ResNet18 classifier', 'Platformers filtering pipeline']

## E4: video tokenizer batch size scaling
- **Verifies**: C3
- **Setup**:
  - Model: video tokenizer
  - Hardware: TPUv2 与 TPUv3
  - Dataset: Platformers
  - System: 改变 tokenizer 训练 batch size 与 compute budget
- **Procedure**:
  1. 使用较小与较大的 tokenizer batch size 训练。
  2. 记录对应 hardware、FLOPs 与 reconstruction PSNR。
  3. 比较 PSNR 的方向性变化。
- **Metrics**: ['PSNR', 'FLOPs']
- **Expected outcome**: 增加 batch size 带来边际 PSNR 改善。
- **Baselines**: ['较小 batch size 设置']
- **Dependencies**: ['video tokenizer optimizer', 'Platformers videos']

## E5: dynamics model size scaling
- **Verifies**: C5
- **Setup**:
  - Model: 不同规模的 dynamics models
  - Hardware: TPUv2 与 TPUv3
  - Dataset: Platformers
  - System: 固定 video tokenizer 与 action model architecture，扩展 dynamics model size
- **Procedure**:
  1. 用固定 batch size 与训练步数训练多个 dynamics model。
  2. 比较 Figure 9 中最终训练损失趋势。
  3. 用 Table 10 记录各模型架构与 compute usage。
- **Metrics**: ['training loss', 'FLOPs', 'training time']
- **Expected outcome**: 更大的 dynamics model 对应更低最终训练损失。
- **Baselines**: ['较小 dynamics model']
- **Dependencies**: ['fixed video tokenizer', 'fixed action model', 'stage-3 ZeRO sharding', 'batch parallelism', 'tensor parallelism']

## E6: dynamics model batch size scaling 与最终 Genie 训练
- **Verifies**: C5
- **Setup**:
  - Model: Genie dynamics model
  - Hardware: TPUv5p 与 TPUv5
  - Dataset: Platformers
  - System: 扩展 batch size 后训练最终 Genie dynamics model
- **Procedure**:
  1. 在相同架构下改变 batch size 比较训练表现趋势。
  2. 选择更大的 final dynamics model 与更大的 batch size 训练。
  3. 用 Table 12 记录最终 dynamics model 的架构与 compute usage。
- **Metrics**: ['training loss', 'FLOPs']
- **Expected outcome**: 更大的 batch size 带来更有利训练表现，并支撑最终 Genie 模型训练。
- **Baselines**: ['较小 batch size 设置']
- **Dependencies**: ['video tokenizer', 'latent action model', 'MaskGIT dynamics model']

## E7: Robotics-trained Genie 定性与测试集评估
- **Verifies**: C1, C7
- **Setup**:
  - Model: Robotics-trained Genie variant
  - Hardware: 论文未在该段落单独点名硬件
  - Dataset: Robotics
  - System: 将 RT1 相关 robot demonstrations、simulation data 与 real robot data 视为 videos，不使用 actions
- **Procedure**:
  1. 用与 Platformers 上最佳设置相同的 hyperparameters 训练 Robotics model。
  2. 在 test split 上评估 FVD。
  3. 用不同 starting frames 观察相同 latent action 是否保持一致语义。
- **Metrics**: ['FVD', 'qualitative latent action consistency']
- **Expected outcome**: 模型能学习 distinct and consistent actions，并能模拟 robotic arm 与 objects 的交互。
- **Baselines**: ['无 action labels 的视频-only 训练设定']
- **Dependencies**: ['Robotics videos', 'latent action model', 'dynamics model']

## E8: CoinRun imitation from observation 行为克隆评估
- **Verifies**: C6
- **Setup**:
  - Model: frozen Genie LAM 与 LAM-based policy
  - Hardware: 论文未在该段落单独点名硬件
  - Dataset: CoinRun expert videos 与 small action-labeled expert sequences
  - System: Procgen CoinRun held out test set，比较 oracle BC 与 random agent
- **Procedure**:
  1. 用 frozen LAM 为 expert videos 标注 latent action labels。
  2. 训练 policy 根据 observation 预测 latent action likelihood。
  3. 用少量 action-labeled expert sequences 建立 latent-to-real action mapping。
  4. 在 hard 与 easy settings 中与 oracle BC 和 random agent 比较。
- **Metrics**: ['levels solved percentage', 'confidence intervals']
- **Expected outcome**: LAM-based policy 随 expert samples 增加接近 oracle BC，并优于 random agent。
- **Baselines**: ['oracle behavioral cloning', 'random agent']
- **Dependencies**: ['frozen LAM', 'CoinRun expert sequences', 'latent-to-real action dictionary']
