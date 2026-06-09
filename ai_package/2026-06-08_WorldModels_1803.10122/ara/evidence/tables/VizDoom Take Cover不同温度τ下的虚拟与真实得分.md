# VizDoom Take Cover不同温度τ下的虚拟与真实得分
- **Source**: Table 2
- **Caption**: "在不同τ设置的DoomRNN虚拟环境中训练的控制器，在虚拟环境（Virtual Score）和真实VizDoom（Actual Score）中的平均存活时步数。解任务阈值为750时步。τ=1.15时真实环境得分最高（1092 ± 556）；τ极低时虚拟得分极高但真实得分退化至随机策略水平。"

| TEMPERATURE T | VIRTUAL SCORE | ACTUAL SCORE |
| --- | --- | --- |
| 0.10 | 2086 ± 140 | 193 ± 58 |
| 0.50 | 2060 ± 277 | 196 ± 50 |
| 1.00 | 1145 ± 690 | 868 ± 511 |
| 1.15 | 918 ± 546 | 1092 ± 556 |
| 1.30 | 732 ± 269 | 753 ± 139 |
| RANDOM POLICY | N/A | 210 ± 108 |
| GYM LEADER | N/A | 820 ± 58 |
