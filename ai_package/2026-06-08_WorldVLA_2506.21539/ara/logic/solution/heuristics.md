# Heuristics

## H1: 损失平衡系数 α = 0.04
- **Rationale**: 图像token数量(256×256图像256个token,512×512图像1024个token)远多于动作token(7个),需将世界模型损失权重缩小,防止图像重建梯度主导训练,影响动作预测性能
- **Sensitivity**: 高:直接决定两个任务目标之间的梯度比例分配
- **Bounds**: 论文固定为0.04,未报告其他取值消融
- **Code ref**: [alpha=0.04 in L=L_action+alpha*L_world]
- **Source**: Section 4.1 Training Setting

## H2: 历史图像帧数默认 M = 2
- **Rationale**: 单帧输入性能次优;2帧在成功率与推理速度(FPS)之间取得最佳折中;消融表明4帧时性能饱和但FPS进一步下降
- **Sensitivity**: 中:帧数增加带来性能边际收益递减
- **Bounds**: 消融了1/2/4帧;默认选2帧(Table 5)
- **Code ref**: [M=2 in action model token sequence]
- **Source**: Section 4.1 Training Setting, Table 5

## H3: 动作块大小 K:LIBERO Long任务为10,其余三个LIBERO任务为5
- **Rationale**: 长程任务需要更长规划窗口;块过长导致机器人无法及时重新规划策略,性能下降(Fig.6)
- **Sensitivity**: 高:块越长在无注意力掩码时误差累积越严重;加掩码后仍有最优块长度
- **Bounds**: 消融了多个K值(Fig.6);过长导致性能衰减
- **Code ref**: [K=10/5 in action_chunk_size]
- **Source**: Section 4.1 Training Setting, Section 4.2 Fig.6

## H4: 世界模型每次训练仅预测 N = 1 帧
- **Rationale**: 为降低计算开销,每个训练样本仅展开一步预测
- **Sensitivity**: 低(计算效率权衡):增大N会提升世界模型训练信号但成倍增加计算量
- **Bounds**: 论文固定为1,未消融其他值
- **Code ref**: [N=1 in world_model_data_repeat]
- **Source**: Section 4.1 Training Setting

## H5: 动作分词器每维度256个等宽bin,7维动作用7个token表示
- **Rationale**: 将连续动作离散化以对齐LLM的下一token预测范式;7维覆盖3个相对位置、3个相对角度和1个绝对夹爪状态;bin宽度由训练数据范围确定
- **Sensitivity**: 中:bin数量影响动作精度,过少导致信息损失,影响操作任务精度
- **Bounds**: 256 bins,沿用 OpenVLA 等先前工作设定
- **Code ref**: [action_tokenizer bins=256 tokens=7]
- **Source**: Section 3.2 Architecture

## H6: VQ-GAN图像分词器压缩比16,码本大小8192;256×256图像产生256 token,512×512图像产生1024 token
- **Rationale**: 压缩比和码本大小决定图像重建保真度与序列长度;512×512分辨率性能更优,因Chameleon骨干在该分辨率下预训练
- **Sensitivity**: 高:分辨率越高token序列越长,计算量与性能同步提升
- **Bounds**: 固定自Chameleon预训练配置
- **Code ref**: [VQGAN codebook_size=8192 compression_ratio=16]
- **Source**: Section 3.2 Architecture, Section 4.2 Benchmark Results
