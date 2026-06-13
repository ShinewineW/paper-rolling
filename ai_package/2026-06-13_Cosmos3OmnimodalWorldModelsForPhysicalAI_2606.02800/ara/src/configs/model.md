## 统一模态范围
- **Value**: language、image、video、audio、action 在同一 Cosmos 3 omnimodal world model 中共同建模
- **Rationale**: 模型目标是同时覆盖理解、生成、模拟和动作预测，减少 Physical AI 中分离 pipeline 的拼接成本。
- **Search range**: 支持 VLM、Text-to-Image、Text-to-Video、Image-to-Video、Video-to-Video、audio-video、forward dynamics、inverse dynamics、policy。
- **Sensitivity**: 高；统一建模带来共享表征收益，也要求 token arrangement 与 MoT 路由正确隔离不同目标。
- **Source**: Abstract, Sec 1, Sec 2

## 视觉理解编码器
- **Value**: ViT encoder pre-trained with vision-language alignment；16×16 patch size；two-layer MLP merges 2×2 tokens；ViT 与 backbone 联合训练
- **Rationale**: 用于 AR subsequence 的视觉理解，使 Reasoner 继承图文对齐能力并支持多模态输入到文本。
- **Search range**: image 与 video understanding。
- **Sensitivity**: 中高；ViT 是否联合训练会影响视觉理解和语言推理对齐。
- **Source**: Sec 2.1.1

## 视觉生成编码器
- **Value**: video VAE encoder from Wan2.2-TI2V-5B；temporal compression 4×，spatial compression 32×32；linear projection 到 transformer hidden dimension；VAE frozen during training
- **Rationale**: 把图像和视频映射为连续 latent tokens，供 diffusion subsequence 去噪生成。
- **Search range**: image 与 video generation。
- **Sensitivity**: 高；冻结 VAE 与压缩率决定 latent 表示、序列长度和可生成细节。
- **Source**: Sec 2.1.1

## 音频编码器
- **Value**: audio VAE from Lee et al. 2025b；raw stereo audio 48 kHz；hop size 1920 samples；25 tokens per second；audio VAE frozen during training
- **Rationale**: 音频作为同步世界事件证据进入同一生成接口，支持视频和音频联合生成。
- **Search range**: audio generation。
- **Sensitivity**: 中高；token rate 与冻结 VAE 影响音画同步和计算负载。
- **Source**: Sec 2.1.2

## action 表征
- **Value**: action token 表示从 v_t-1 到 v_t 的状态转移；ego poses、effector poses、grasp states 组成统一接口；ego 和 effector 用 relative-pose pseudo-actions，包含 3D translation 与 6D rotation
- **Rationale**: 用共享几何组件统一不同 embodiment 的控制空间，使 action 与视频动态建立因果连接。
- **Search range**: autonomous vehicles、camera motion、robots、egocentric human motion。
- **Sensitivity**: 高；action 表征决定跨 embodiment transfer 和下游 policy 可执行性。
- **Source**: Sec 2.1.3

## domain-aware action projection
- **Value**: 每个 embodiment domain 使用单独 input 与 output projection weight matrices，同时共享 MoT backbone；投影参数从头初始化并与 MoT backbone 联合优化
- **Rationale**: 不同 action-vector 长度和语义通过 domain-aware 投影对齐到共享 latent action space。
- **Search range**: domain identifier k 属于 K 个 embodiment domains。
- **Sensitivity**: 高；投影层初始化和 domain 划分影响跨域共享与域内精度。
- **Source**: Sec 2.1.3

## token arrangement
- **Value**: 序列由 AR subsequence 后接 diffusion subsequence；AR 包含 language 与 ViT image/video tokens；DM 包含 VAE image/video tokens、audio tokens、action tokens；DM 内 clean conditioning tokens 放在 noisy diffusion tokens 前
- **Rationale**: 统一 packing 让同一模型以不同输入输出配置支持理解、生成和动作任务。
- **Search range**: 适用于 T2I、T2V、I2V、V2V、transfer、action modes。
- **Sensitivity**: 高；clean/noisy token 顺序错误会破坏条件生成和动作推理。
- **Source**: Sec 2.2.1

## MoT dual-tower
- **Value**: 每个 transformer decoder layer 有 reasoner tower 与 generator tower 两套参数；AR tokens 路由到 reasoner，DM tokens 路由到 generator；两塔初始化自 pre-trained VLM weights
- **Rationale**: 保留自回归理解能力，同时给生成任务独立容量学习扩散去噪。
- **Search range**: 所有 Cosmos 3 variants 共享 dual-tower MoT architecture。
- **Sensitivity**: 高；共享注意力和独立参数的边界决定理解与生成是否相互干扰。
- **Source**: Sec 2.3, Sec 2.3.1

## dual-stream joint attention
- **Value**: AR tokens 只对 AR subsequence 做 causal self-attention；DM tokens 对同一样本的 AR 与 DM key/value 做 full bidirectional attention；AR tokens 不被 DM tokens 更新
- **Rationale**: 扩散生成可读取文本和条件上下文，同时保持 autoregressive conditioning path 的因果完整性。
- **Search range**: 每个 transformer decoder layer。
- **Sensitivity**: 高；mask 设计错误会导致 AR 泄漏或 DM 条件不足。
- **Source**: Sec 2.3.2

## 3D MRoPE 与 temporal gap
- **Value**: 位置编码使用 3D MRoPE 加 absolute temporal indexing；audio 与 action spatial indices 为零；AR 与 diffusion subsequence 之间插入 fixed temporal gap 15000
- **Rationale**: 绝对时间轴对齐不同 FPS、audio hop 和 action sampling rate；temporal gap 缓解首帧过饱和和 checkerboard artifacts。
- **Search range**: 所有模型 temporal gap 设为 15000；base TPS 为 24/4=6。
- **Sensitivity**: 高；时间调制影响音画动作同步，temporal gap 影响初始视觉 artifact。
- **Source**: Sec 2.4.1, Sec 2.4.2

## 模型规模
- **Value**: Cosmos3-Edge 为 4B 参数，基于 dense 2B transformer；Cosmos3-Nano 为 16B 参数，基于 dense 8B transformer；Cosmos3-Super 为 64B 参数，基于 dense 32B transformer
- **Rationale**: 三个规模覆盖 on-device 到 large datacenter inference；论文释放 Nano 与 Super，Edge 后续释放。
- **Search range**: Edge、Nano、Super。
- **Sensitivity**: 中高；规模影响能力、吞吐和硬件需求。
- **Source**: Sec 2.5

## MoT variant hyperparameters
- **Value**: Edge：28 layers，hidden 2048，16 attention heads，8 KV heads，head dim 128，FFN 9216；Nano：36 layers，hidden 4096，32 attention heads，8 KV heads，head dim 128，FFN 12288；Super：64 layers，hidden 5120，64 attention heads，8 KV heads，head dim 128，FFN 25600
- **Rationale**: 这些结构参数定义各模型容量与注意力并行上限。
- **Search range**: Table 2 三个 variants。
- **Sensitivity**: 高；层数、hidden size 和 head 数影响容量、CP degree 上限和训练吞吐。
- **Source**: Sec 2.5, Table 2

## 推理默认采样
- **Value**: base Audio-Visual 使用 steps=50、guidance=6、shift=10；T2I post-trained 使用 steps=50、guidance=4、shift=3；I2V post-trained 使用 steps=50、guidance=6、shift=5；FD/ID 使用 steps=50、guidance=1、shift=5；Policy 使用 steps=4、guidance=3、shift=5；Transfer 使用 steps=50、guidance=3、control guidance=1.5、shift=10
- **Rationale**: 不同任务对质量、条件强度和延迟的要求不同，因此使用不同 sampling hyperparameters。
- **Search range**: Table 21 覆盖 Cosmos3-Nano、Cosmos3-Super、Cosmos3-Super-Text2Image、Cosmos3-Super-Image2Video、Cosmos3-Nano-Policy-DROID。
- **Sensitivity**: 高；steps、guidance 和 shift 直接影响质量、条件一致性和延迟。
- **Source**: Sec 6.3.1, Table 21
