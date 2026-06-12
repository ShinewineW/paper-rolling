# Evidence Index

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/膨胀GMO、流预测与细粒度GMO主结果.md](tables/膨胀GMO、流预测与细粒度GMO主结果.md) | Table 1 | ['C1'] | Comparisons of Inflated GMO and Flow Forecasting on the nuScenes and Lyft-Level5 datasets, and Fine-Grained GMO Forecasting on the nuScenes-Occupancy dataset, with the top two results highlighted in bold and underlined text. |
| [tables/细粒度GMO和GSO预测结果.md](tables/细粒度GMO和GSO预测结果.md) | Table 2 | ['C1'] | Comparisons of Fine-Grained GMO and GSO Forecasting on nuScenes-Occupancy dataset. |
| [tables/多种动作条件下的可控性比较.md](tables/多种动作条件下的可控性比较.md) | Table 3 | ['C2'] | Comparisons of controllability under diverse action conditions, with the top two results highlighted in bold and underlined. checkmark P denotes the predicted trajectory. |
| [tables/使用GT trajectory时的规划上界.md](tables/使用GT trajectory时的规划上界.md) | Table 4 | ['C2', 'C3'] | Planning upper bound when using GT trajectory. |
| [tables/nuScenes端到端规划性能.md](tables/nuScenes端到端规划性能.md) | Table 5 | ['C3'] | End-to-end Planning Performance on nuScenes. † indicates the NoAvg evaluation protocol, while ‡ denotes the TemAvg protocol. ∗ signifies the use of ego status in the planning module and the calculations of collision rates following BEV-Planner (Li et al. 2024b). |
| [tables/条件归一化消融.md](tables/条件归一化消融.md) | Table 6 | ['C4'] | Ablations on the conditional normalization. |
| [tables/动作条件注入接口消融.md](tables/动作条件注入接口消融.md) | Table 7 | ['C2', 'C4'] | Ablations on the action conditioning interface. |
| [tables/占用代价因子的贡献.md](tables/占用代价因子的贡献.md) | Table 8 | ['C3'] | Contributions of occupancy-based cost factors. |
| [tables/输入帧数和记忆队列长度的性能与延迟.md](tables/输入帧数和记忆队列长度的性能与延迟.md) | Table 9 | ['C5'] | Latency and performance based on varying numbers of input frames and memory queue lengths. Latency measurements are conducted on an A6000 GPU. |
| [tables/语义占用损失函数消融.md](tables/语义占用损失函数消融.md) | Table 10 | ['C5'] | Ablation studies on the semantic occupancy loss functions, utilizing one historical and the current inputs to predict future states across two timestamps. |

## Figures
| Source ref | Role | Caption |
|------------|------|---------|
| `images/9f3c9fce6240e61b292d5cf4ce9872f6b6db22cebe90c952517c0374669a3cb2.jpg` | result | Figure 1: 4D Occupancy Forecasting and Planning via World Model. Drive-OccWorld takes observations and trajectories as input, incorporating flexible action conditions for action-controllable generation. By leveraging world knowledge and the generative capacity of the world model, we further integrat |
| `images/fcab184b64e8991b30808c60af0f813a79d8119be86989ea1263df5681ea8645.jpg` | architecture | Figure 2: Overview of Drive-OccWorld. (a) The history encoder extracts multi-view image features and transforms them into BEV embeddings. (b) The memory queue employs semantic- and motion-conditional normalization to aggregate historical information. (c) The world decoder incorporates action conditi |
| `images/0e8053af3f27bc929fac8afba16c0550064e7750a4f6ed29db355c678eb68372.jpg` | architecture | Figure 3: Overview of semantic-conditional normalization. |
| `images/84589ac530e7a254321f278fef1837530631a29d6f1cecaec6b9fa10c97b5a2f.jpg` | result | Figure 4: Qualitative results of 4D occupancy and flow forecasting. The results are presented at various future timestamps. |
| `images/c2072d4eeb1788055fdf799262b8a8636d0d9b495f1d3d275e00271a4351d71f.jpg` | result | Figure 5: Qualitative results of controllable generation, using the high-level command or low-level trajectory conditions. |
| `images/3ed84df6a10b64410fa4c90254e31a6207219dc509e96e6ddb289cefc2082522.jpg` | result | Figure 6: Detailed structure of the world decoder, which predicts the next BEV features based on historical BEV features and expected ego actions in an autoregressive manner. |
| `images/77d701d8d6c78cbdd0ba841b0436c5503d0b9aa8ab3a683d8b7ea9ea1fb684c5.jpg` | result | Figure 7: Visualization of BEV features before and after semantic-conditional normalization highlights the responses of BEV grids, particularly for instance objects. Consequently, it extracts discriminative BEV features for forecasting and planning. |
| `images/7c6cae17a69dda5e00782064d18096d2f55c71e6100c669fa557f6835b8a14b2.jpg` | result | Figure 8: Qualitative results of controllable generation, using the high-level steering angle or low-level velocity conditions. |
| `images/bf86ce7a60717e0cc97573537abd01c9509b9ee5ef714a1b6177f1005d479745.jpg` | result | Figure 9: Qualitative results for vision-centric 4D occupancy forecasting on the nuScenes validation set. Top: historical visual inputs over three timestamps, showing only the front images for simplicity. Bottom: future occupancy predictions for two seconds. Notable movable objects are highlighted i |
| `images/f151c4850a224d965f847c339b6363e22347802f4b50260d1ea2289ec8007420.jpg` | result | Figure 10: Qualitative results for continuous forecasting and planning on the nuScenes validation set. Top: historical visual inputs over three timestamps, showing only the front images for simplicity. Bottom: future occupancy and planning results for five timestamps, with predicted trajectories hig |
