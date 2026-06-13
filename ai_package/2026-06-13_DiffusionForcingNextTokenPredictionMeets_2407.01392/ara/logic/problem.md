# Problem Specification

## Observations

### O1: next-token prediction 适合可变长度生成和在线反馈，但 te
- **Statement**: next-token prediction 适合可变长度生成和在线反馈，但 teacher forcing 训练下，采样时缺少多步目标引导，连续数据长程自回归容易因误差累积而发散。
- **Evidence**: Current next-token prediction models are trained via teacher forcing；no mechanism by which one can guide；slight errors in frame-to-frame predictions accumulate and the model diverges
- **Implication**: 单步预测范式难以同时满足长程稳定生成和目标导向采样。

### O2: full-sequence diffusion 能建模固定长度联合分布并支持 g
- **Statement**: full-sequence diffusion 能建模固定长度联合分布并支持 guidance，但通常采用非因果、无 mask 架构，限制可变长度生成、因果采样和子序列组合。
- **Evidence**: Full-sequence diffusion；noise level is identical across all tokens；universally parameterized via non-causal, unmasked architectures；restricting sampling to full sequences
- **Implication**: 全序列扩散解决了引导问题，却把序列长度和因果结构固定住。

### O3: 把 next-token prediction 和 full-sequence 
- **Statement**: 把 next-token prediction 和 full-sequence diffusion 直接拼接的朴素方案表现差，因为它没有表达早期 token 的低不确定性会约束后续 token 的高不确定性这一结构。
- **Evidence**: naive attempt at combining the best of both worlds；leads to poor generations；small uncertainty in an early token necessitates high uncertainty in a later one
- **Implication**: 关键不只是把模型做成因果扩散，而是要允许不同时间位置有不同噪声状态。

## Gaps

### G1: 现有 next-token prediction 缺少面向整段未来的采样引导。
- **Statement**: 现有 next-token prediction 缺少面向整段未来的采样引导。
- **Caused by**: teacher forcing 与单步自回归采样把历史视为干净上下文。
- **Existing attempts**: ['next-token diffusion sequence model', 'teacher forcing']
- **Why they fail**: 未来 token 必须等过去 token 完全确定后才能逐步采样，梯度无法自然作用于尚未展开的多步轨迹。

### G2: 现有 full-sequence diffusion 难以自然处理可变 hori
- **Statement**: 现有 full-sequence diffusion 难以自然处理可变 horizon 和因果执行。
- **Caused by**: non-causal, unmasked architectures 与 identical noise level across all tokens。
- **Existing attempts**: ['Diffuser', 'conditioning by replacement']
- **Why they fail**: 它把整段序列作为固定长度对象一起去噪，并让所有 token 共享同一噪声水平。

### G3: 线性依赖位置的噪声方案不能覆盖本文需要的采样自由度。
- **Statement**: 线性依赖位置的噪声方案不能覆盖本文需要的采样自由度。
- **Caused by**: noise level linearly dependent on the position of each word 或 exact same noise level scheme at sampling time。
- **Existing attempts**: ['AR-Diffusion', 'Rolling Diffusion']
- **Why they fail**: 训练噪声水平和采样噪声水平绑定，难以只通过改采样日程实现稳定 rollout、坏观测处理和多种 horizon 策略。

## Key Insight
- **Insight**: 把 noising 解释为 partial masking，并让每个 token 的噪声水平独立随机化，模型就被迫学习任意部分遮蔽序列的去噪条件分布。
- **Derived from**: noising tokens is a form of partial masking；independent per-token noise levels；unmask any collection of variably noised tokens
- **Enables**: 同一个训练好的 CDF 可在采样时切换为自回归、全序列、因果不确定性、稳定 rollout、Monte Carlo Guidance 和损坏观测处理等多种行为。

## Assumptions
- 序列 token 可以用噪声水平表示从干净观测到纯噪声的连续遮蔽程度。
- 因果实现中，过去信息可由 RNN latent 汇总并传递给后续 token。
- 训练时独立采样噪声水平能覆盖采样时需要的噪声日程组合。
- 理论结论依赖论文所述 appropriate conditions 与足够表达能力；这是论文显式带条件的表述。
