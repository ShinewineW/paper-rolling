# Claims

## C1: 神经网络可在单张 TPU 上实时模拟复杂游戏 DOOM
- **Statement**: GameNGen 是首个完全由神经模型驱动的游戏引擎，能够在单张 TPU-v5 上以 20 FPS 对复杂游戏 DOOM 进行实时交互式仿真，并在长时轨迹上保持与原始游戏相当的视觉质量
- **Status**: supported
- **Falsification criteria**: 若系统无法维持 20 FPS 或在多分钟游戏后视觉质量显著退化，则此主张不成立
- **Proof**: [E1, E2, E3, E4]
- **Evidence basis**: ['E1', 'E2', 'E3', 'E4']
- **Interpretation**: 通过两阶段训练——RL 智能体采集多样化轨迹数据，再用扩散模型学习次帧预测——在 Stable Diffusion v1.4 基础上实现了对复杂游戏环境的神经实时仿真，4 步 DDIM 采样使总推理延迟降至 50ms（20 FPS）
- **Tags**: ['improvement', 'descriptive']

## C2: 噪声增强是维持自回归长轨迹稳定性的关键技术
- **Statement**: 在训练时对历史上下文帧添加可变量高斯噪声（噪声增强），能有效阻止自回归生成中因教师强制与推理分布偏移导致的质量退化，是长轨迹稳定仿真的必要条件
- **Status**: supported
- **Falsification criteria**: 若去除噪声增强后自回归生成在 64 帧内质量不下降，则此主张不成立
- **Proof**: [E6]
- **Evidence basis**: ['E6']
- **Interpretation**: 噪声增强令模型习得纠正前帧噪声的能力，弥合训练期教师强制与推理期自回归之间的域偏移；即使推理时不添加噪声，相较于完全无噪声增强的基线质量也显著更高
- **Tags**: ['causal']

## C3: 4 步 DDIM 采样即可达到与多步相当的仿真质量
- **Statement**: GameNGen 仅需 4 个 DDIM 采样步骤即可达到与 20 步或更多步骤相当的仿真质量，从而在单张 TPU-v5 上实现 20 FPS 实时推理；单步蒸馏模型可进一步提升至 50 FPS，但带来轻微质量损耗
- **Status**: supported
- **Falsification criteria**: 若 4 步采样与 20 步以上采样之间存在显著质量差距，则此主张不成立
- **Proof**: [E4]
- **Evidence basis**: ['E4']
- **Interpretation**: 作者推测质量对步数不敏感源于：受约束的游戏图像空间以及来自历史帧的强条件信号；蒸馏模型（标记为 D）可在单步下大幅提升质量但仍有轻微代价
- **Tags**: ['descriptive', 'causal']

## C4: 微调潜变量解码器改善视觉细节保真度
- **Statement**: 对 Stable Diffusion v1.4 预训练潜变量自编码器的解码器进行微调（MSE 损失，目标帧像素），可显著改善游戏帧中小字体、HUD 等细节区域的渲染质量，且不影响自回归潜变量条件路径
- **Status**: supported
- **Falsification criteria**: 若解码器微调前后帧质量无可见差异，则此主张不成立
- **Proof**: [E1]
- **Evidence basis**: ['E1']
- **Interpretation**: 解码器微调与 U-Net 微调完全解耦；论文在 Appendix A.2（图 12）提供定性对比，量化评估结果（PSNR/LPIPS）来自包含解码器微调的完整模型
- **Tags**: ['improvement', 'causal']

## C5: RL 智能体数据在中等难度区域显著优于随机策略数据
- **Statement**: 使用 RL 智能体生成的训练数据整体优于随机策略数据，尤其在需要探索的中等难度区域差异最大；简单和困难区域差异相对较小，随机策略数据整体表现出乎意料地好
- **Status**: supported
- **Falsification criteria**: 若随机策略数据训练的模型在各难度级别均与智能体数据持平，则此主张不成立
- **Proof**: [E7]
- **Evidence basis**: ['E7']
- **Interpretation**: 随机策略因探索能力受限，对中等难度区域覆盖不足；智能体训练数据多样性更高，在未充分覆盖区域的泛化能力更强，反映了数据分布质量对仿真能力的影响
- **Tags**: ['causal', 'descriptive']

## C6: 人类评估者难以区分仿真与真实游戏短片
- **Statement**: 人类评估者区分 GameNGen 仿真短片与真实游戏短片的准确率仅略高于随机水平；在经过 5-10 分钟自回归生成后的长片段对比中，评估者准确率接近随机水平
- **Status**: supported
- **Falsification criteria**: 若人类评估者能以远高于随机的准确率稳定区分仿真与真实游戏，则此主张不成立
- **Proof**: [E3]
- **Evidence basis**: ['E3']
- **Interpretation**: 这表明模型在感知质量上与真实游戏高度接近；但论文作者（熟悉仿真具体局限性）在短时间内即可识别差异，说明感知相似性不等同于逻辑一致性
- **Tags**: ['descriptive']
