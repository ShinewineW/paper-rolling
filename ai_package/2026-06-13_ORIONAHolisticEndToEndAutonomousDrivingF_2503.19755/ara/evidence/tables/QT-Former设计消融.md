# QT-Former设计消融
- **Source**: Table 4
- **Caption**: "不同框架下QT-Former设计的消融结果；T表示Plain Text，G表示Instructed Generator。"

| ID | Traffic State | Motion Pred. | Memory Bank | T | G | DS↑ | SR(%)↑ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  | √ | 56.33 | 26.05 |
| 2 |  |  |  |  | √ | 74.65 | 49.31 |
| 3 | √√ | √ |  |  | √ | 74.07 | 49.77 |
| 4 | √ | ✓ | √ |  | √ | 77.74 | 54.62 |
| 5 |  |  |  | √ |  | 25.45 | 10.38 |
| 6 | √ | √ | √ | ✓ |  | 42.23 | 13.14 |
