## 模型家族
- **Value**: OmniDreams 是从 Cosmos diffusion model mid- and post-trained 的 action-conditioned generative world model
- **Rationale**: 利用 Cosmos 的视觉先验，同时适配 AV 闭环仿真。
- **Search range**: 包括 OmniDreams-SV 和 OmniDreams-MV。
- **Sensitivity**: 高；基础模型决定生成先验和可迁移能力。
- **Source**: Abstract, Sec. 1, Sec. 3

## 参数规模
- **Value**: 论文描述 2B OmniDreams，并在 WAM 对比中写 ∼2 B vs. ∼10 B
- **Rationale**: 以较小参数规模实现实时世界模型和可迁移策略骨干。
- **Search range**: 未给出层数、宽度等完整结构超参。
- **Sensitivity**: 中；规模影响吞吐和表达能力。
- **Source**: Sec. 1, Sec. 7

## SV 生成块
- **Value**: OmniDreams-SV 生成 single front-facing camera view，每步 8 frames，等价 2 latent frames
- **Rationale**: 单视角设置降低计算量并可在单 GPU 达到实时。
- **Search range**: Sec. 5 中推理配置使用 8 RGB frames per chunk，local-attention window 为 6 latent frames。
- **Sensitivity**: 中；chunk 大小影响延迟和策略交互粒度。
- **Source**: Sec. 3, Sec. 5.1, Sec. 5.3

## MV 生成块
- **Value**: OmniDreams-MV 联合生成 four synchronized views，每步 16 frames，等价 4 latent frames
- **Rationale**: 服务多相机闭环策略，同时保持跨视角一致性。
- **Search range**: 生产多视角配置使用 16 RGB frames per chunk，local-attention window 为 8 latent frames。
- **Sensitivity**: 高；多视角同步与实时吞吐依赖该配置。
- **Source**: Sec. 3, Sec. 5.1, Sec. 5.3

## 条件输入
- **Value**: First-frame RGB、Text prompt、Abstract world scenario、Memory cache
- **Rationale**: 首帧初始化外观，文本控制环境属性，结构图控制地图与动态体，KV cache 提供历史上下文。
- **Search range**: 第一步额外使用 single RGB image；后续请求主要携带新 trajectory 与 prompt。
- **Sensitivity**: 高；缺失任一核心条件都会改变可控性或时序一致性。
- **Source**: Fig. 3, Sec. 3.1, Sec. 6

## 主干结构
- **Value**: causal transformer backbone similar to Cosmos-Predict 2.5 base model
- **Rationale**: 在 Cosmos-Predict 2.5 的视频扩散主干上加入因果自回归能力。
- **Search range**: 论文未列出完整层级超参。
- **Sensitivity**: 高；主干决定生成质量和推理成本。
- **Source**: Sec. 3.1

## world-scenario control branch
- **Value**: structured simulator state 先经 small MLP 编码成 compact control tokens，再与 visual tokens concatenated 输入 transformer
- **Rationale**: 相比独立 ControlNet，轻量分支降低开销并保持结构控制与视觉内容分离。
- **Search range**: control branch initialized to zero。
- **Sensitivity**: 高；控制注入方式直接影响地图、代理和轨迹条件的服从度。
- **Source**: Sec. 3.1, Sec. 4.1

## 多视角一致性机制
- **Value**: 每个 camera view 有 learnable embedding，并在每步执行 cross-view attention；temporal attention 在各 view 内独立执行
- **Rationale**: 通过时间与视角分解降低 full self-attention 的复杂度，同时共享场景几何和运动信息。
- **Search range**: Figure 4 中 Multi-View Cross Block 在 text Cross-Attention 后加入 Cross-View Attention。
- **Sensitivity**: 高；决定 MV 的跨相机一致性和实时可行性。
- **Source**: Sec. 3.2, Fig. 4

## 自回归 KV cache
- **Value**: streaming KV cache 存储之前生成 tokens，新的 frame generation 会 attend 过去 generation 的 keys 和 values
- **Rationale**: 在不重算完整序列的情况下保持长时上下文。
- **Search range**: 训练和推理均对 rolling window 做限制；推理中 cache 预分配为固定形状。
- **Sensitivity**: 高；cache 设计影响长 rollout 稳定性、内存和延迟。
- **Source**: Sec. 1, Sec. 3, Sec. 4.3, Sec. 5.1

## 推理局部注意力窗口
- **Value**: OmniDreams-SV 使用 6 latent frames，即 24 RGB frames；OmniDreams-MV 使用 8 latent frames，即 32 RGB frames
- **Rationale**: 在缓存大小、速度和长期一致性之间折中。
- **Search range**: 论文称 window size is a tradeoff between memory and speed。
- **Sensitivity**: 中到高；窗口太短可能漂移，太长增加延迟和显存。
- **Source**: Sec. 5.1

## 编码器与解码器替换
- **Value**: OmniDreams-SV 使用 LightVAE 编码 conditioning video；OmniDreams-MV 使用 pixel shuffle technique 替代 LightVAE；二者均用 LightTAE 解码 RGB
- **Rationale**: 以更低延迟服务实时闭环推理。
- **Search range**: LightTAE 带来速度收益但有质量 trade-off。
- **Sensitivity**: 中；解码器选择影响质量指标和延迟。
- **Source**: Sec. 5.1, Tab. 4, Tab. 5

## 多 GPU 并行
- **Value**: 16-GPU four-view configuration 为 ??=4、??=4、????=1，并使用 in-house ring-attention implementation
- **Rationale**: 沿 view 和 temporal 轴做 hierarchical context-parallel，以适配 4-camera 低延迟生成。
- **Search range**: 超过 16 GPUs 才会开始考虑 ???? sharding。
- **Sensitivity**: 高；MV 实时性能依赖该并行分解。
- **Source**: Sec. 5.2

## 服务化闭环形态
- **Value**: 视频模型作为 stateful video model server，经 gRPC 与 AlpaSim client 通信；rank 0 接收请求并用 NCCL events 转发到其他 ranks
- **Rationale**: 避免将多 GPU 视频模型依赖和 rank dispatch 逻辑侵入仿真系统。
- **Search range**: 返回 JPEG-encoded frames；未来工作提到 RDMA-based gRPC 或 NCCL bulk transfer。
- **Sensitivity**: 中；系统形态影响端到端闭环延迟和部署复杂度。
- **Source**: Sec. 6, Sec. 6.2
