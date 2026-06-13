# Heuristics

## H1: 训练时为每个 token 独立采样噪声等级,而不是让整段序列共享同一噪声等级。
- **Rationale**: 论文将 independent noise levels 作为 Diffusion Forcing 的关键条件,用于支持 stabilization of autoregressive rollout、modeling causal uncertainty 和 corrupted observations 条件化等采样期能力。
- **Sensitivity**: 若噪声等级不独立,采样期可调 schedule 会退化为必须匹配训练噪声模式,论文指出 AR-Diffusion 与 Rolling Diffusion 因此受限。
- **Bounds**: 噪声等级按论文描述从 $[ K ] ^ { T }$ 均匀采样；Appendix B.2 还描述为 per-token noise level following i.i.d uniform distribution。
- **Code ref**: [sample_noise_levels_iid_uniform]
- **Source**: Sec. 3.2, Appendix B.2

## H2: 长序列自回归 rollout 时,用带少量噪声的 latent 继续下一步,而不是只用完全干净的前一帧 latent。
- **Rationale**: 论文解释为 conditioning on $\mathbf { x } _ { t } ^ { k _ { \mathrm { s m a l l } } }$ 的实现,使测试时的 noisy past observation 与训练目标覆盖的输入分布一致。
- **Sensitivity**: 噪声过小会更接近普通自回归并增加累积误差风险；噪声过大则会削弱已生成上下文的信息量。
- **Bounds**: 论文给出约束 $0 < k _ { \mathrm { s m a l l } } \ll K$。
- **Code ref**: [stabilize_autoregressive_rollout]
- **Source**: Sec. 3.3, Appendix B.4

## H3: 规划或长 horizon guidance 时,让近未来 token 比远未来 token 更快去噪,保留远未来的不确定性。
- **Rationale**: 论文把噪声等级解释为 uncertainty,并说明 future tokens 高噪声可让 MCG 对未来 outcome 分布求期望而不是对单条未来样本求梯度。
- **Sensitivity**: 若远未来过早变干净,会削弱 causal uncertainty；若近未来长期高噪声,会影响当前可执行 action 的确定性。
- **Bounds**: 论文示例使用 zig-zag schedule 与 Appendix D.7 的 $K ^ { \mathrm { p y r a m i d } }$。
- **Code ref**: [pyramid_schedule]
- **Source**: Sec. 3.3, Sec. 3.4, Appendix D.7

## H4: Monte Carlo Guidance 用多个未来 rollout 的 guidance gradient 平均来引导当前 token。
- **Rationale**: 论文称其估计 cost-to-go guidance 时提供 variance reduction,并依赖从当前 token rollout 未来 token 的能力。
- **Sensitivity**: 样本数越少越接近单条未来样本 guidance；样本数增加会提高计算成本。
- **Bounds**: 论文未给出固定样本数边界,只说明可 draw multiple samples of the future and average their guidance gradients。
- **Code ref**: [monte_carlo_guidance]
- **Source**: Sec. 3.4, Appendix B.5

## H5: 采样时若 token 需要停留在同一噪声等级,MCG 场景优先使用 resampling,即先反向扩散再前向扩散回原噪声等级。
- **Rationale**: 论文在 corner case 中比较 copying 与 resampling,并说明使用 resampling 生成 Monte Carlo Guidance 的多个样本。
- **Sensitivity**: copying 更省算力但减少重采样随机性；resampling 保留随机性但增加采样计算。
- **Bounds**: 论文说明除 Monte Carlo Guidance 外,该 corner case 在实验中只发生于 $k _ { t } = 0$ 或 $k _ { t } = K$。
- **Code ref**: [resample_same_noise_level]
- **Source**: Appendix D.5

## H6: 实验实现中视频用 U-net 输出接 GRU 更新 latent,非视频输入用 resMLP 接 GRU,再用 observation model 输出预测。
- **Rationale**: 论文把 transition model 与 observation model 合为 RNN layer,并说明 RNN 对 online decision-making 更高效。
- **Sensitivity**: 换成 transformer 可能提升效果,但论文主实现集中在 RNN；无 causal mask transformer 的因果性属于 Appendix B.1 的扩展直觉。
- **Bounds**: 论文未把 backbone 选择写成理论约束；Discussion 明确当前 causal implementation is based on an RNN。
- **Code ref**: [rnn_diffusion_unit]
- **Source**: Appendix D.2, Appendix B.1, Discussion
