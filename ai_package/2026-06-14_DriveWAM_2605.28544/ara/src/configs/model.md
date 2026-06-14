## 视频骨干
- **Value**: Wan2.2-TI2V-5B
- **Rationale**: 作为pretrained video diffusion transformer和policy core。
- **Search range**: 论文消融比较pretrained init.与从头训练，但未报告其他骨干。
- **Sensitivity**: Table 4显示去掉pretrained initialization或joint video supervision都会变差。
- **Source**: Sec 4.2 Implementation Details; Sec 4.4 Video Foundation Model Adaptation

## 初始化
- **Value**: initialized from the base checkpoint released by [19]
- **Rationale**: 继承video generative priors并用于policy adaptation。
- **Search range**: Table 4包含从头训练和无video supervision设置。
- **Sensitivity**: 论文指出从头训练移除large-scale spatio-temporal priors并导致表现下降。
- **Source**: Sec 4.2; Sec 4.4 Video Foundation Model Adaptation

## 可训练范围
- **Value**: fine-tune the full video diffusion transformer together with action and ego-state modules
- **Rationale**: 同时适配视频骨干和新增动作、ego-state模块。
- **Search range**: Unless otherwise specified；论文未报告冻结骨干消融。
- **Sensitivity**: 分析推断,论文未显式声明：全量微调更能适配驾驶任务，但显存和数据需求更高。
- **Source**: Sec 4.2 Implementation Details

## action encoder / decoder
- **Value**: MLPs with hidden dimension 3072
- **Rationale**: 将normalized ego-frame translation and yaw increments嵌入到动作token，并从共享Transformer输出解码动作速度。
- **Search range**: 论文未报告其他hidden dimension。
- **Sensitivity**: 分析推断,论文未显式声明：隐藏维度影响动作表征容量和新增参数量。
- **Source**: Sec 3.1 Tokenization; Sec 4.2 Implementation Details

## ego-state编码
- **Value**: separate MLP plus separate ego-state cross-attention branch
- **Rationale**: 将velocity、acceleration、curvature等ego state作为当前驾驶上下文注入。
- **Search range**: 论文未报告其他ego-state注入方式。
- **Sensitivity**: 分析推断,论文未显式声明：该分支影响动作预测对车辆状态的条件化能力。
- **Source**: Sec 3.1 World-action flow; Sec 4.2 Implementation Details

## VAE tokenization
- **Value**: pretrained VAE encodes each observed video chunk into z_k
- **Rationale**: 复用视频生成模型的latent空间，并通过latent input embedding映射到transformer hidden dimension。
- **Search range**: 论文未报告替代tokenizer。
- **Sensitivity**: 分析推断,论文未显式声明：VAE latent质量会影响未来视频latent和后续动作生成。
- **Source**: Sec 3.1 Tokenization

## 统一token序列
- **Value**: video and action chunks organized into a unified temporal token sequence
- **Rationale**: 保持时间顺序，使同一Transformer联合建模视频和动作。
- **Search range**: 论文未报告分离序列替代方案。
- **Sensitivity**: 显式设计目标是jointly model video-action generation；具体消融未报告。
- **Source**: Sec 3.1 Tokenization

## 训练目标
- **Value**: joint flow-matching objective
- **Rationale**: 视频分支学习future world modeling，动作分支学习inverse-dynamics action generation。
- **Search range**: Table 4消融joint video supervision；论文未报告其他损失族。
- **Sensitivity**: 论文显示action-only adaptation无法保持生成式video priors。
- **Source**: Sec 3.1 Training objective; Sec 4.4 Video Foundation Model Adaptation

## scene-evolving guidance模型
- **Value**: frozen Qwen3-VL-8B
- **Rationale**: 每个decision step从causally available context生成chunk-specific semantic intent。
- **Search range**: 论文未报告其他VLM。
- **Sensitivity**: Table 3显示替换global prompt为scene-evolving guidance会改善轨迹预测趋势。
- **Source**: Sec 3.2; Sec 4.2; Sec 4.4 Scene-evolving Driving Guidance

## guidance注入
- **Value**: temporally localized cross-attention with block-diagonal text mask
- **Rationale**: 让目标chunk只访问对应g_k，避免跨chunk和未来guidance泄漏。
- **Search range**: 论文未报告其他mask形式。
- **Sensitivity**: 显式说明无约束会破坏causal consistency；定量mask消融未报告。
- **Source**: Sec 3.2 Temporally localized guidance injection

## selective KV memory
- **Value**: bounded modality-aware video and action memory pools with relevance-redundancy retention
- **Rationale**: 长horizon rollout中保留prediction-relevant且非冗余的历史。
- **Search range**: 对比Full、FIFO、Selective；Selective使用固定cache budget。
- **Sensitivity**: Table 5显示Selective在显著降低开销时接近Full，FIFO明显变差。
- **Source**: Sec 3.3; Sec 4.4 Selective KV Memory

## selective KV参数
- **Value**: λ = 0 . 0 7；video cache capacity 448 tokens；action cache capacity 160 tokens
- **Rationale**: 按FlowCache设置relevance与redundancy权衡，并分别限制video/action缓存容量。
- **Search range**: λ ∈ [ 0 , 1 ]；论文未报告λ或capacity搜索。
- **Sensitivity**: 论文说明λ平衡relevance和redundancy；具体敏感性未报告。
- **Source**: Sec 3.3; Sec 4.2 Implementation Details

## 推理ODE solver
- **Value**: Euler ODE solver with 3 steps for video tokens and 10 steps for action tokens
- **Rationale**: 视频先生成未来latent，动作再在生成未来条件下denoise。
- **Search range**: Appendix C报告action steps从10降到5的变体；视频steps其他范围未报告。
- **Sensitivity**: Appendix C说明降低action denoising steps可减少延迟且轨迹指标变化很小。
- **Source**: Sec 4.2 Implementation Details; Appendix C Efficiency Analysis

## flow积分区间
- **Value**: video: τ = 1 to τ = 0 . 6；action: τ = 1 to τ = 0
- **Rationale**: 视频token只积分到中间噪声水平，动作token积分到clean endpoint。
- **Search range**: 论文未报告其他积分区间。
- **Sensitivity**: 分析推断,论文未显式声明：积分区间影响生成质量、速度和动作精度。
- **Source**: Sec 4.2 Implementation Details
