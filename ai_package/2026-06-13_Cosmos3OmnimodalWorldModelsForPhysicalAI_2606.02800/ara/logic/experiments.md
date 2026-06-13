# Experiments

## E1: 全能力结果总览评测
- **Verifies**: C1
- **Setup**:
  - Model: Cosmos3-Super、Cosmos3-Nano 及后训练变体
  - Hardware: 论文结果表未在该实验条目中统一给出
  - Dataset: 论文的 reasoning、generation、FD 与 policy 评测集合
  - System: 统一 omnimodal world model 结果汇总
- **Procedure**:
  1. 按论文的各能力基准分别评估 Cosmos 3 变体和专门基线。
  2. 把推理、生成、forward dynamics 与机器人 policy 的指标汇总到总览表。
  3. 比较 Cosmos 3 与开放或闭源基线在对应能力列中的方向性表现。
- **Metrics**: ['Reasoning 分组分数', 'Text2Image 分数', 'Text2Video 分数', 'Image2Video 分数', 'Audio 分数', 'FD 与 Policy 指标']
- **Expected outcome**: Cosmos 3 在多数能力上应达到或超过专门开放基线，并在不同模态任务中保持可用表现。
- **Baselines**: ['Gemini 3.1 Pro†', 'Qwen3-VL-32B', 'Qwen3-VL-8B', 'Gemma-4-31B', 'Gemma-4-E4B', 'Gemini 3 Pro Image†', 'Qwen-Image-2512', 'Veo-3.1t', 'Wan2.2-A14B', 'Ctrl-World', 'π0.5']
- **Dependencies**: ['Table 1']

## E2: 图像与视频生成基准评测
- **Verifies**: C2
- **Setup**:
  - Model: Cosmos3-Super-Text2Image、Cosmos3-Super、Cosmos3-Nano
  - Hardware: 论文结果表未统一给出
  - Dataset: UniGenBench、CVTG、PAIBench-G、RBench、Cosmos HUE、Human World Bench、Cosmos-SoundBench、PAIBench-C、AVBench-C
  - System: 图像、视频、音频视频与条件生成评测流程
- **Procedure**:
  1. 在图像生成、视频生成、音频视频生成和控制生成基准上运行 Cosmos 3 变体。
  2. 按论文指标与开放或闭源模型对比。
  3. 用自动指标和人类评测共同检验生成结果。
- **Metrics**: ['UniGenBench', 'GNED', 'PNED', 'Aesthetic v2', 'HPSv3', 'PAIBench-G', 'RBench', 'Cosmos HUE', 'Human World Bench', 'AVQ', 'SAV', 'DOVER', '控制一致性指标']
- **Expected outcome**: Cosmos 3 生成器应在开放模型中呈现领先或强竞争表现，并在部分闭源模型对比中接近或超过对手。
- **Baselines**: ['FLUX.2-dev', 'Qwen-Image-2512', 'Hunyuan 3.0', 'Z-Image-Turbo', 'Wan2.2-A14B', 'HunyuanVideo-1.5', 'Cosmos-Predict2.5', 'Veo-3.1', 'Seedance-1.5-Pro', 'Sora 2', 'LTX-2.3', 'Cosmos-Transfer2.5']
- **Dependencies**: ['Table 11', 'Table 12', 'Table 13', 'Table 14', 'Table 15', 'Table 16', 'Table 17', 'Table 32', 'Table 33']

## E3: 世界动作与机器人策略评测
- **Verifies**: C3
- **Setup**:
  - Model: Cosmos3-Super、Cosmos3-Nano、Cosmos3-Nano-Policy-DROID、Cosmos3-Edge
  - Hardware: 论文相关表未统一给出
  - Dataset: Autonomous Vehicle、Camera Motion、Egocentric Motion、Robotics、RoboLab、LIBERO-10、PushT
  - System: forward dynamics、inverse dynamics、policy 与 joint video-action prediction
- **Procedure**:
  1. 比较 MT-init 与 PT-init 在多个 action setting 上的表现。
  2. 在 RoboLab 上比较 Cosmos3-Nano-Policy-DROID 与机器人策略基线。
  3. 在 LIBERO-10 上比较不同初始化的快速适应趋势。
  4. 在 PushT 上比较 single-mode 与 joint FD/ID/policy 训练。
- **Metrics**: ['RRE', 'RTE', 'ATE', 'PSNR', 'task success rate', 'policy coverage', 'ID MSE']
- **Expected outcome**: mid-training 初始化和联合动作模式训练应在多数动作相关指标上更优，机器人策略评测应表现出更强闭环成功趋势。
- **Baselines**: ['Lingbot-World', 'HY-World1.5', 'VGGT', 'DepthAnything3', 'LOME', 'Ctrl-World', 'π0.5', 'DreamZero', 'π-FAST', 'paligemma-binning', 'GR00T N1.6', 'π0']
- **Dependencies**: ['Table 18', 'Table 19', 'Table 20', 'Table 31']

## E4: 模型设计与数据消融
- **Verifies**: C4
- **Setup**:
  - Model: Cosmos3-Nano、Cosmos3-Edge 及相关 ablation 变体
  - Hardware: 论文消融段落给出部分训练资源，表格本身以结果为主
  - Dataset: SDG datasets、PAIBench-G、PAIBench T2V/I2V、FPS bands、video-only 与 video-audio 数据、PushT
  - System: 数据、理解塔、FPS 控制、音频数据与动作模式的对照实验
- **Procedure**:
  1. 从相同或可比的训练起点改变单一设计因素。
  2. 在相同基准上比较替换前后的指标方向。
  3. 用表格结果判断每个设计因素是否带来收益或权衡。
- **Metrics**: ['PAIBench-G', 'domain score', 'quality score', 'Avg. VQ', 'Avg. MF', 'Avg. Composite', 'FD PSNR', 'ID MSE', 'Policy Coverage']
- **Expected outcome**: 被采用的设计组合应在关键指标上优于对应基础设置，或显示出论文所述的稳定收益。
- **Baselines**: ['Baseline pre-train', 'Qwen-3 VL understanding tower', 'Base No Control', 'Without Audio', 'single-mode action checkpoints']
- **Dependencies**: ['Table 26', 'Table 28', 'Table 29', 'Table 30', 'Table 31']

## E5: 训练与推理效率实验
- **Verifies**: C5
- **Setup**:
  - Model: Cosmos3-Nano、Cosmos3-Super
  - Hardware: NVIDIA GB200 GPUs、H10080GB、GB200
  - Dataset: T2V task 与训练吞吐设置
  - System: asynchronous checkpointing、steady-state throughput、batching inference
- **Procedure**:
  1. 比较同步与异步 checkpoint 的训练时间影响。
  2. 测量 dense model configuration 的训练吞吐。
  3. 在 T2V 推理中比较 batching 带来的速度变化。
- **Metrics**: ['checkpoint save time', 'speedup over synchronous', 'TFLOPS', 'MFU', 'tokens per GPU-hour', 'inference speedup']
- **Expected outcome**: 异步 checkpoint 与 batching 应带来效率改善，吞吐表应量化不同模型规模的训练成本。
- **Baselines**: ['synchronous checkpointing', 'non-batched inference']
- **Dependencies**: ['Table 7', 'Table 8', 'Table 9']
