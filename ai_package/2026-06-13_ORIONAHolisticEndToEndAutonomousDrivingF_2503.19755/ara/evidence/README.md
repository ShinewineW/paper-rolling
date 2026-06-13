# Evidence Index

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/Bench2Drive闭环与开环主结果.md](tables/Bench2Drive闭环与开环主结果.md) | Table 1 | ['C1'] | Bench2Drive base set上E2E-AD方法的闭环与开环结果；C/L表示camera/LiDAR，NC表示navigation command，TP表示target point。 |
| [tables/Bench2Drive多能力结果.md](tables/Bench2Drive多能力结果.md) | Table 2 | ['C2'] | Bench2Drive base set上E2E-AD方法的Multi-Ability结果。 |
| [tables/生成式规划器消融.md](tables/生成式规划器消融.md) | Table 3 | ['C3'] | 不同生成式规划器的消融结果，指标包含闭环、开环和能力均值。 |
| [tables/QT-Former设计消融.md](tables/QT-Former设计消融.md) | Table 4 | ['C4'] | 不同框架下QT-Former设计的消融结果；T表示Plain Text，G表示Instructed Generator。 |
| [tables/历史查询数量消融.md](tables/历史查询数量消融.md) | Table 5 | ['C5'] | 历史查询数量对闭环与开环指标的影响。 |
| [tables/辅助VQA任务训练有效性.md](tables/辅助VQA任务训练有效性.md) | Table 6 | ['C6'] | 辅助VQA任务训练的有效性，C/B/R表示CIDEr、BLEU与ROUGE-L，FT表示Fine Tuning。 |
| [tables/nuScenes开环规划对比.md](tables/nuScenes开环规划对比.md) | Table A1 | ['C7'] | nuScenes开环规划对比；†表示ego status与planning trajectory均由LLM以文本模态处理，‡表示训练和测试阶段不使用high-level command。 |
| [tables/训练策略消融.md](tables/训练策略消融.md) | Table A2 | ['C8'] | 训练策略消融；V/L/A表示vision、language与action空间。 |

## Figures
| Source ref | Role | Caption |
|------------|------|---------|
| `images/c2fe40bc773ae001faae61f942bebc18ff3a34e1132a19077fa56b29df135d94.jpg` | architecture | Figure 1. The comparison of different E2E paradigms. Our ORION framework establishes the differentiable connection between reasoning and action space via the generative planner. |
| `images/5efd5c7d9e2a5908b40773b5fb10286633744da89bd94356ace412bce2410763.jpg` | architecture | Figure 2. The pipeline of our ORION, a holistic E2E framework aligning vision-reasoning-action space. It consists of three key components: a QT-Former to extract long-term context and link the vision space of the vision encoder and the reasoning space of LLM; the LLM for performing reasoning tasks a |
| `images/102d6578f04f8a2a4718876d7f0223b30d2591f55417ff8d4499f7a132bc0cd9.jpg` | architecture | Figure 3. The detailed architecture of QT-Former. It accepts diverse queries and image features as inputs to detect traffic elements, predict motion, and aggregate long-term vision context. |
| `images/3e19c4b9c2d73904b4cf130b61951206efb478ebfc53d9a0543153520abf369a.jpg` | result | Figure 4. Qualitative results of ORION on the Bench2Drive closed-loop evaluation set. The brown, red, and green refer to the action decision, the objects that influence driving decisions, and the prediction trajectory, respectively. |
| `images/6212b5a3979244c702959dfb5db36ddef63f445c88b66273e777075a1f8c9024.jpg` | result | Figure 5. Advantages of the vision-language instructed action generation. DS and SR denote Driving Score and Success Rate separately. VAD [25] is a classic E2E model. |
| `images/e74e7863385913b747aa1bb174b47a41e211c2ce50a7551abb41364b32d7cfdd.jpg` | architecture | Figure A1. The automated annotation pipeline for the Chat-B2D dataset. |
| `images/ff2ca0938c2394e981093b82225a42caafc83201584ba8d6f2b5ee1891f28102.jpg` | result | Figure A2. Qualitative results of historical information memory and retrieval on Bench2Drive open-loop validation set. |
| `images/061cc40c6efc7c1d7fb2041687774f89e96ec1e5ca54069cba23b16b53e9f214.jpg` | result | (b) |
