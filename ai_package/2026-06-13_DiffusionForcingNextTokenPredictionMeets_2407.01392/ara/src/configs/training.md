## per_token_noise_sampling
- **Value**: 每个 token 独立采样噪声级别；训练处写为 independent noise level，正文损失处写为均匀采样 k_1:T
- **Rationale**: 这是 Diffusion Forcing 的核心训练设定，用不同时间步的独立噪声级别迫使模型学习任意部分噪声序列的去噪。
- **Search range**: Algorithm 1 写作 {0,1,...,K}；Appendix B.2 写作 i.i.d uniform from [1,2...K]，两处表述不完全一致。
- **Sensitivity**: 论文明确称独立噪声带来 autoregressive rollout 稳定化、causal uncertainty 建模、避免昂贵 reconstruction guidance，并支持一次训练后改变采样方案。
- **Source**: Sec 3.2; Algorithm 1; Appendix B.2

## training_objective
- **Value**: conventional diffusion training objective，噪声预测形式，并在 Algorithm 1 中使用 MSELoss 比较预测噪声与真实噪声。
- **Rationale**: 模型单元以 z_t-1、x_t 的噪声版本和噪声级别为输入，预测噪声或干净 token，从而可直接采用扩散训练目标。
- **Search range**: 适用于序列中所有 token 的并行去噪训练；论文理论部分说明其作为所有噪声序列似然的有效 surrogate 需要 fully expressive neural network 等条件。
- **Sensitivity**: 若噪声级别不独立或目标不覆盖多种噪声组合，会削弱论文强调的稳定 rollout、可变 horizon 与采样方案调参能力。
- **Source**: Sec 3.2; Theorem 3.1; Appendix A.1

## diffusion_steps_K
- **Value**: K = 1000
- **Rationale**: 论文在性能优化处说明训练扩散步数设置，并用较少 DDIM 步数进行采样加速。
- **Search range**: 训练使用 K = 1000；采样时 video prediction 使用 100 DDIM，non-video domains 使用 50。
- **Sensitivity**: 采样步数降低用于加速；论文没有报告对 K 的系统敏感性曲线。
- **Source**: Appendix D.6

## sampling_steps
- **Value**: video prediction 采样使用 100 DDIM；non-video domains 采样使用 50。
- **Rationale**: DDIM 采样用于降低 Diffusion Forcing 的采样成本。
- **Search range**: 100 DDIM 用于 video prediction；50 用于 non-video domains。
- **Sensitivity**: 论文将其作为性能优化选择；未给出不同 DDIM 步数的消融。
- **Source**: Appendix D.6

## frame_stack
- **Value**: DMLab video prediction 使用 4；Minecraft 使用 8；maze planning 使用 10。
- **Rationale**: frame-stacking 用于降低训练时间和 GPU 内存，并避免对相邻高度相似 token 重复 rollout。
- **Search range**: 论文只列出 DMLab、Minecraft、maze planning 的 frame stack 设置。
- **Sensitivity**: 作者认为相邻帧相似时不堆叠会浪费计算；低维系统也可借助 frame stacking 使用更典型的扩散超参数。
- **Source**: Appendix D.6

## noise_schedule
- **Value**: video prediction 使用 sigmoid；maze planning 使用 linear；其他任务使用 cosine。
- **Rationale**: 不同任务采用不同扩散噪声 schedule。
- **Search range**: sigmoid、linear、cosine 三类 schedule。
- **Sensitivity**: 论文未给出 schedule 消融，但将其列为实现细节。
- **Source**: Appendix D.4

## diffusion_parameterization
- **Value**: video prediction 使用 v parameterization；planning 与 imitation learning 偏好 x_0 parameterization；time-series prediction 观察到 v-parameterization 的收益。
- **Rationale**: 不同预测目标会导致不同噪声级别的 loss reweighting，视频生成更依赖高频细节，planning 与 imitation learning 不偏好人为强调高频。
- **Search range**: x_0、epsilon、v parameterization。
- **Sensitivity**: 论文称 v parameterization 对 video prediction 的收敛速度和质量是 essential，并称 planning 与 imitation learning 更偏好 x_0。
- **Source**: Appendix D.3

## fused_snr_reweighting
- **Value**: video prediction 使用 Fused SNR reweighting；non-image domains 未使用。
- **Rationale**: Fused SNR reweighting 将当前 noisy observation 的 SNR 与历史 latent 中的信息合并，用于加速视频预测收敛。
- **Search range**: 基于 min-SNR reweighting 推导 S，并以 signal decay factor gamma 汇聚历史信息；gamma 的具体数值未说明。
- **Sensitivity**: 论文称它对 video prediction 收敛加速 extremely useful，但 non-image domains 未观察到提升。
- **Source**: Appendix D.1

## time_series_early_stopping
- **Value**: validation crps-sum 连续 6 epochs 未改进时 early stopping；每个 epoch 固定为 100 batches。
- **Rationale**: 时间序列实验跟踪 validation set 上的 CRPS_sum，并在训练结束后报告 test set。
- **Search range**: 6 epochs；100 batches。
- **Sensitivity**: 论文没有仔细搜索最小训练步数；此设置是时间序列实验的停止规则。
- **Source**: Sec E.1; Appendix D.9

## batch_size
- **Value**: maze planning 与 compositional experiments 为 2048；visual imitation learning 为 32；video prediction 为 8 x 16；time series 为 32。
- **Rationale**: 作者按 GPU memory 调整 batch size，并在 time series 中沿用同一架构和 batch size。
- **Search range**: 32 到 2048；video prediction 使用 8 x 16。
- **Sensitivity**: 论文说 batch size 被调到充分使用 GPU memory，未报告 batch size 消融。
- **Source**: Appendix D.9; Appendix D.10

## training_steps
- **Value**: time series 通常 50k 到 100k steps 收敛；video prediction 训练 50K steps，并通常在 40K steps 收敛。
- **Rationale**: 给出主要实验的训练时长和收敛步数背景。
- **Search range**: time series 通常 50k 到 100k；video prediction 50K，收敛常在 40K。
- **Sensitivity**: 作者明确说未仔细搜索最小训练步数，因此这些是报告的运行设置而非最优步数。
- **Source**: Appendix D.10
