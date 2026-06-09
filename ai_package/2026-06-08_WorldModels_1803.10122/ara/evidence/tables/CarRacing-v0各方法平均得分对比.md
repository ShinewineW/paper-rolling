# CarRacing-v0各方法平均得分对比
- **Source**: Table 1
- **Caption**: "CarRacing-v0各方法在100次随机轨迹上的平均累积得分对比，解任务阈值为平均分900。完整世界模型（V与M联合）达到906 ± 21，超越所有基线并首次解决该任务。"

| METHOD | AVG. SCORE |
| --- | --- |
| DQN (PRIEUR,2017) | 343 ± 18 |
| A3C (CONTINUOUS) (JANG ET AL., 2017) | 591 ± 45 |
| A3C (DISCRETE) (KHAN & ELIBOL,2016) | 652 ± 10 |
| CEOBILLIONAIRE (GYM LEADERBOARD) | 838 ± 11 |
| V MODEL | 632 ± 251 |
| V MODEL WITH HIDDEN LAYER | 788 ± 141 |
| FULL WORLD MODEL | 906 ± 21 |
