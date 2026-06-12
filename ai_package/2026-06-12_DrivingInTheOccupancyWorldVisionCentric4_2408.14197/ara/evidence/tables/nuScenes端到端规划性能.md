# nuScenes端到端规划性能
- **Source**: Table 5
- **Caption**: "End-to-end Planning Performance on nuScenes. † indicates the NoAvg evaluation protocol, while ‡ denotes the TemAvg protocol. ∗ signifies the use of ego status in the planning module and the calculations of collision rates following BEV-Planner (Li et al. 2024b)."

| Method | MD抽取的L2字段 | MD抽取的Collision字段 |
| --- | --- | --- |
| NMP (Zeng et al. 2019) SA-NMP (Zeng et al. 2019) | - 2.31 2.05 | 1.92 - |
| FF (Hu et al. 2021) EO (Khurana et al. 2022) | 0.551.202.54 0.671.36 2.78 1.43 1.60 | 0.060.17 0.040.09 1.59 1.07 0.88 0.43 0.33 |
| ST-P3 † (Hu et al. 2022) UniAD† (Hu et al. 2023b) VAD-Base† (Jiang et al. 2023) OccNet t (Tong et al. 2023) | 1.29 0.541.15 2.13 |1.72 3.26 4.86 0.480.96 1.65 51.98 2.99 3.28 1.03 1.22 2.14 | 0.21 0.44 0.050.17 0.10 1.08 0.24 0.59 3.01 0.71 0.96 1.37 1.51 0.31 0.43 0.72 |
| Drive-OccWorldP † (Ours) ST-P3 (Hu et al. 2022) UniAD† (Hu et al. 2023b) | 0.41 0.32 0.75  1.49 0.85 1.332.11 0.440.67 2.90 0.96 2.11 0.69 | 0.23 0.040.08 0.62 1.27 0.23 0.05 0.17 0.64 0.29 0.71 0.12 |
| VAD-Base+ (Jiang et al. 2023) Drive-WM+ (Wang et al. 2024b) | 0.70 0.43 0.77 )1.05 1.20 0.72 0.80 | 0.02 0.250.84 0.070.17 0.10 0.41 0.22 |
| Drive-OccWorldP † (Ours) UniAD * (Hu et al. 2023b) VAD-Base* (Jiang et al. 2023) BEV-Planner+* (Li et al. 2024b) Drive-OccWorldP * (Ours) 0.17 | 0.17 0.340.60 0.16  0.32 0.57 |0.200.42 0.75 0.25  0.44 0.72 0.47 0.46 | 0.21 0.03  0.08  0.22 0.48 0.26 0.11 |
