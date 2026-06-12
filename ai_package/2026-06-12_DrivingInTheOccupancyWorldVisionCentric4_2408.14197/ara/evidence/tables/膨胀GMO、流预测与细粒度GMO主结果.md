# 膨胀GMO、流预测与细粒度GMO主结果
- **Source**: Table 1
- **Caption**: "Comparisons of Inflated GMO and Flow Forecasting on the nuScenes and Lyft-Level5 datasets, and Fine-Grained GMO Forecasting on the nuScenes-Occupancy dataset, with the top two results highlighted in bold and underlined text."

| Method | nuScenes mIoUc | nuScenes mIoU f (2 s) | nuScenes mIoU f | nuScenes VPQf | Lyft-Level5 IoUc | Lyft-Level5 mIoUf (0.8 s) | Lyft-Level5 mIoUf | Lyft-Level5 VPQf | nuScenes-Occupancy mIoUc | nuScenes-Occupancy mIoU f (2 s) | nuScenes-Occupancy mIoU f |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SPC | 1.3 | failed | failed | 一 | 1.4 | failed | failed | - | 5.9 | 1.1 | 1.1 |
| OpenOccupancy-C (Wang et al. 2023c) | 12.2 | 11.5 21.3 | 11.7 | - | 14.0 | 13.5 | 13.7 | - | 10.8 | 8.0 | 8.5 |
| PowerBEV-3D (Li et al. 2023a) | 23.1 | 26.8 | 21.9 28.0 | 20.0 | 26.2 | 24.5 | 25.1 | 27.4 | 5.9 | 5.3 | 5.5 |
| Cam4DOcc (Ma et al. 2024b) | 31.3 |  |  | 18.6 | 36.4 | 33.6 | 34.6 | 28.2 | 11.5 | 9.7 | 10.1 |
| Drive-OccWorldA (Ours) | 39.7 | 36.3 | 37.3 | 23.7 | 40.6 | 39.3 | 40.0 | 32.2 | 13.6 | 11.9 | 12.3 |
| Drive-OccWorldP (Ours) | 39.8 | 36.3 | 37.4 | 25.1 | 40.9 | 39.7 | 40.6 | 33.4 | 13.6 | 12.0 | 12.4 |
