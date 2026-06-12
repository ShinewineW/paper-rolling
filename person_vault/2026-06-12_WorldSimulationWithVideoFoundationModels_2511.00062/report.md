# WorldSimulationWithVideoFoundationModels — 深度解读

> 面向人类读者的深度解读(中文)。事实源与配对的 AI 知识包 `ai_package/2026-06-12_WorldSimulationWithVideoFoundationModels_2511.00062/ara/` 同源,均已通过数据保真审计。

## 核心结论

> 每条结论后的隐形锚点把数字回链到论文原文(忠实性保证)。

1. Cosmos-Predict2.5 采用 flow matching 架构，并将 Text2World、Image2World 与 Video2World 统一到单一模型中，用 Cosmos-Reason1 提供更丰富的文本表征与更细粒度控制。<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-nvidia-sup-1-sup--><!--anchor:quote:NVIDIA%3Csup%3E1%3C%2Fsup%3E-->
2. 在 VideoAlign 奖励模型下进行强化学习后，Cosmos-Predict2.5-2B 在 Text2World 与 Image2World 设置中的文本对齐、运动质量、视觉质量综合奖励整体提高，论文还报告 RL 生成结果在人工投票中平均更受偏好。<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C-->
3. rCM 时间步蒸馏后的 Cosmos-Predict2.5-2B 在 PAI-Bench Text2World 与 Image2World 上取得与 teacher 相近的定量结果，论文称其可用更少步骤生成高保真样本。<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C-->
4. 在 PAI-Bench-Predict 的 Text2World 和 Image2World 基准中，Cosmos-Predict2.5 post-trained 模型相对自身 pre-trained 版本提升，并在 Image2World 中达到论文所称最佳表现。<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C-->
5. Cosmos-Transfer2.5-2B 在 PAIBench-Transfer 的多种控制配置中，相比 Cosmos-Transfer1-7B 展示更好的整体质量，并在单模态与均匀权重多模态设置中改善多项控制对齐指标。<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-nvidia-sup-1-sup--><!--anchor:quote:NVIDIA%3Csup%3E1%3C%2Fsup%3E--><!--ref:r-2-2-2-autonomous-drivi--><!--anchor:quote:2.2.2%20Autonomous%20Driving%207-->
6. 用 Cosmos-Transfer2.5-2B 生成的视觉增强数据训练策略后，真实机器人在多种未见物体与环境变化场景中的成功率高于仅用原始演示或标准图像增强的策略。<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C-->
7. Cosmos-Predict2.5 和 Cosmos-Transfer2.5 的多视角驾驶版本在 RDS-HQ-HL 生成视频评测中，相比上一代模型改善 FVD、FID 等视觉指标，并在车道与三维框检测指标上提升控制遵循。<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C-->
8. Cosmos-Predict2.5-2B/robot/action-cond 在 Bridge 数据集上优于 Cosmos-Predict1 动作条件基线；消融显示通过 TimeEmbedding 注入动作优于 CrossAtten 与 ChannelConcat。<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-nvidia-sup-1-sup--><!--anchor:quote:NVIDIA%3Csup%3E1%3C%2Fsup%3E-->

ç¨æ·å¸ææä½ä¸ºä¸ä½èµæ·±çä¸­æï¼æ°åä¸ç¯è®ºææ·±åº¦è§£è¯»æ¥åä¸­çä¸èï¼âä¸å¥è¯æ»ç»ä¸å¯¼è¯»æ¯ä¸ï¼éè¦æç»é¢æã
1. ä¸å¥è¯å¨åä»ä¹ã
2. è§£å³äºä»ä¹çå®çç¹ï¼ã
3. ææ ¸å¿çä¸ä¸ª idea æ¯ä»ä¹ã
4. å¼å¤´ç»ä¸å¥è¯ TL;DRï¼å ç²ï¼ã

ç¡¬çº¦æï¼
1. ä¸­æï¼ä¼ç§çææ¯åå®¢/æ·±åº¦ç§æ®ï¼å¯ç¨æ°å½æ¯å»ï¼æ æ³¨âç´è§ï¼éä¸¥æ ¼å¯¹åºâï¼ãè®²éâä¸ºä»ä¹ãçç¹ãæºå¶âï¼æç»ç©ºè¯ã
2. å¿ å®ï¼åªç¨æä¾çäºå®æºï¼ARAç¼é ãä¸æåè¯ï¼Cosmos-Predict2.5, Physical AI, Text2World, Image2World, Video2World, Cosmos-Reason1, flow matching, shifted logit-normal distribution, VideoAlign, rCM, PAI-Bench, Cosmos-Transfer2.5 ç­ï¼åï¼ä¸ç¿»è¯ã
3. æ¥å°ä¸­**ç»å¯¹ä¸è½**åºç°ç²¾ç¡®æ§è½æ°å­ï¼å¦å¾åãæåç¾åæ¯ç­ï¼ãæ§è½æ¯è¾ç¨å®æ§è¯­è¨ãéæ§è½æ°å­ï¼å¦2Båæ°ãåè¾¨çç­ï¼å¦æäºå®æºæçè¯ï¼äºå®æºæå°äºCosmos-Predict2.5-2Bï¼å¯ä»¥å2Båæ°ï¼å¯ä»¥åã
4.50-800ä¸­æå­ã
5. åªè¾åºæ¬èæ­£æï¼ä»¥ `## ä¸å¥è¯æ»ç»ä¸å¯¼è¯»` å¼å¤´ï¼å¸¦emojiï¼æ ¹æ®è§èâH2 å¥é¦å¯å¸¦ä¸ä¸ª emojiâï¼ãä¸è¦èï¼ä¸è¦åæ´ç¯æ é¢ï¼ä¸è¦ä»£ç å´æ å¤çè§£éã

åæäºå®æºï¼
- è®ºæï¼WorldSimulationWithVideoFoundationModels (Cosmos-Predict2.5)
- çç¹ (Observations & Gaps)ï¼Physical AI å¨çå®ä¸çè®­ç»ææ¬é«ï¼éè¦ä¸çæ¨¡æå¨ãä½éç¨è§é¢æ¨¡ååæ©æä¸çæ¨¡åå¨ç»ç²åº¦æ§å¶ãç©çä¸è´æ§ä¸ä¸è¶³ï¼åæ£ççææ¨¡å¼ï¼Text/Image/Video2Worldï¼ä¸å©äºç»ä¸æ¥å£ï¼é«åè¾¨çè§é¢è®­ç»æåºç°æ¶é´è¿æ¸¡ä¼ªå½±ã
- æ ¸å¿ Idea (Key Insight)ï¼æä¸çæ¨¡æè§ä¸ºå¸¦å¤æ¨¡ææ¡ä»¶çéåº¦åºå­¦ä¹ ï¼flow matchingï¼ï¼ç»ä¸ Text2WorldãImage2World å Video2Worldï¼åç¨é¢åæ°æ®ãå¥å±æ¨¡åï¼VideoAlign RLï¼åæ§å¶åæ¯ï¼Cosmos-Transfer2.5ï¼éæ­¥ä¸é¨åã
- æ¨¡åï¼Cosmos-Predict2.5 (2Båæ°), Cosmos-Reason1 (text encoder), Cosmos-Transfer2.5.

èµ·èç»æï¼
## ð¯ ä¸å¥è¯æ»ç»ä¸å¯¼è¯»
**TL;DRï¼Cosmos-Predict2.5 å°è§é¢çæåç»´ä¸ºç©çä¸ççâæ²çæ¨æ¼âï¼éè¿ç»ä¸ç flow matching æ¶æä¸å¤æ¨¡ææ¡ä»¶æ§å¶ï¼ä¸º Physical AI æé äºä¸ä¸ªé«ä¿çãå¯äº¤äºä¸

ï¼æ®µè½1ï¼å¨åä»ä¹ & çç¹ï¼
è®­ç» Physical AIï¼å¦æºå¨äººæèªå¨é©¾é©¶ï¼å¦æç´æ¥å¨çå®ä¸çæ¸ç¬æ»æï¼è¿å°±å¥½æ¯è®©ä¸ä¸ªæ°æå¸æºç´æ¥å¨æ©é«å³°çé¹å¸åºç»è½¦ï¼ç´è§ï¼éä¸¥æ ¼å¯¹åºï¼ãå æ­¤ï¼æä»¬éè¦ä¸ä¸ªè½çæé«è´¨éãç¬¦åç©çè§å¾çâèææ²çâââä¸çæ¨¡æå¨ãç¶èï¼ç°æçéç¨è§é¢çææ¨¡åå¾å¾åªâç»é¢å¥½çâï¼å¨ç©ä½å¨æãç©çä¸è´æ§åç»ç²åº¦æ§å¶ä¸é¢é¢ç¿»è½¦ï¼ä¸ææ¬ãå¾åãè§é¢ç­çæä»»å¡åèªä¸ºæï¼é¾ä»¥å½¢æç»ä¸çæ§å¶æ¥å£ã

ï¼æ®µè½2ï¼æ ¸å¿ Idea & æºå¶ï¼
ä¸ºäºå¡«è¡¥è¿ä¸é¸¿æ²ï¼Cosmos-Predict2.5 æåºäºæ ¸å¿ ideaï¼å°ä¸çæ¨¡æè§ä¸º**å¸¦å¤æ¨¡ææ¡ä»¶çéåº¦åºå­¦ä¹ **ãå®éç¨ flow matching æ¶æï¼å·§å¦å°å° Text2WorldãImage2World ä¸ Video2World ç»ä¸å°ä¸ä¸ª 2B åæ°çåä¸æ¨¡åä¸­ãéè¿1 æä¾æ´æ·±å±çææ¬è¯­ä¹è¡¨å¾ï¼å¹¶ç»å frame-replacement ç­ç¥å¤çè§è§æ¡ä»¶ç»âåºè§é¢ï¼æ´è½âçè§£âç©çäº¤äºãå¨æ­¤åºç¡ä¸æ°æ®è¿æ»¤ãVideoAlign å¼ºåå­¦ä¹ åè®­ç»ä»¥å Cosmos-Transfer2.5 çæ§å¶åæ¯ï¼å®æåå°éç¨çè§é¢çæè½åè½¬åä¸ºé¢åæºå¨äººåèªå¨é©¾é©¶çç²¾åä»¿çè½åï¼è®©æ°å­å­ªçä¸çä¸­é«æè¯éä¸è¿åã

æ£æ¥çº¦æï¼
1. ä¸­æï¼ï¼ææ¯å»ï¼æ°æå¸æºé¹å¸åºç»è½¦ï¼æ æ³¨äºç´è§éä¸¥æ ¼å¯¹åºï¼ã
2. å¿ å®ï¼ä½¿ç¨äº Physical AI, flow matching, Text2World, Image2World, Video2World, Cosmos-Reason1, frame-replacement, VideoAlign, Cosmos-Transfer2.5, 2Bãæ²¡æç¼é ã
3.æ²¡æç²¾ç¡®æ§è½æ°å­ãæå°äº 2B åæ°ï¼éæ§è½æ°å­ï¼å±äºæ¨¡åè§æ¨¡ï¼ã
4.å¤§çº¦ 400-500 å­ï¼ç¬¦å 350-800 å­çè¦æ±ã
5. æ ¼å¼ï¼`## ð¯ ä¸å¥è¯æ»ç»ä¸å¯¼è¯»` å¼å¤´ãæ²¡æå¤ä½è¯­è¨æ·±åº¦ç§æ®âçè´¨æï¼
"è®­ç» Physical AIï¼å¦æºå¨äººæèªå¨é©¾é©¶ï¼å¦æç´æ¥å¨çå®ç©çä¸çæ¸ç¬æ»é«æãè¿­ä»£å¥½æ¯è®©ä¸ä¸ªæ°æå¸æºç´æ¥å¨æ©é«å³°çé¹å¸åºç»è½¦ï¼ç´è§ï¼éä¸¥æ ¼å¯¹åºï¼ãå æ­¤ï¼ä¸çæ¥éä¸ä¸ªè½çæé«è´¨éãç¬¦åç©çè§å¾çâèææ²çâââä¸çæ¨¡æå¨ãç¶èï¼ç°æçéç¨è§é¢çææ¨¡åç»é¢å¥½çâï¼å¨ç©ä½å¨æãç©çä¸è´æ§åç»ç²åº¦æ§å¶ä¸é¢é¢ç¿»è½¦ï¼ä¸ææ¬ãå¾åãè§é¢ç­çæä»»å¡åèªä¸ºæï¼é¾ä»¥å½¢æç»ä¸çäº¤äºæ¥å£ã" -> è¿æ®µå¾å¥½ã

"ä¸ºäºå¡«è¡¥è¿ä¸é¸¿æ²ï¼Cosmos-Predict2.5 æåºäºä¸ä¸ª ideaï¼å°ä¸çæ¨¡æè§ä¸º**å¸¦å¤æ¨¡ææ¡ä»¶çéåº¦åºå­¦ä¹ **ãå®éç¨ flow matching æ¶æï¼å·§å¦å°å° Text2WorldãImage2World ä¸ Video2World ç»ä¸å°ä¸ä¸ª 2B åæ°çåä¸æ¨¡åä¸­-Reason1 æä¾æ´æ·±å±çææ¬è¯­ä¹è¡¨å¾ï¼å¹¶ç»å frame-replacement ç­ç¥å¤çè§è§æ¡ä»¶ç»âåºè§é¢ï¼æ´è½âçè§£âç©çäº¤äºãé¢åæ°æ®è¿æ»¤ãVideoAlign å¼ºåå­¦ä¹ åè®­ç»ä»¥å Cosmos-Transfer2.5 çæ§å¶åæ¯ï¼å®æåå°éç¨çè§é¢çæè½åè½¬åä¸ºé¢åæºå¨äººåèªå¨é©¾é©¶çç²¾åä»¿çè½åï¼è®©æ°å­å­ªçä¸çä¸­é«æè¯éä¸è¿åã" -> è¿æ®µä¹å¾å¥½ã

å­æ°ç»è®¡ï¼å¤§æ¦ 480 å­ãæ»¡è¶³ 350-800 çè¦æ±ã
æ£æ¥ H2 æ é¢ï¼`## ð¯ ä¸å¥è¯æ»ç»ä¸å¯¼è¯»`ãç¬¦åâH2 å¥é¦å¯å¸¦ä¸ä¸ª emojiâã
æ£æ¥ææ²¡æä¸å°å¿ååºæ§è½æ°å­ï¼æ²¡æã
æ£æ¥ä¸æåè¯ï¼Physical AI, Cosmos-Predict2.5, flow matching, Text2World, Image2World, Video2World, Cosmos-Reason1, frame-replacement, VideoAlign, Cosmos-Transfer2.5ãåä¿çåæ ·ã

ç¡®è®¤æ è¯¯ï¼è¾åºã## ð¯ ä¸å¥è¯æ»ç»ä¸å¯¼è¯»

**TL;DRï¼Cosmos-Predict2.5 å°è§é¢çæåç»´ä¸ºç©çä¸ççâæ²çæ¨æ¼âï¼éè¿ç»ä¸ç flow matching æ¶æä¸å¤æ¨¡ææ¡ä»¶æ§å¶ï¼ä¸º Physical AI æé äºä¸ä¸ªé«ä¿çãå¯äº¤äºã**

è®­ç» Physical AIï¼å¦æºå¨äººæèªå¨é©¾é©¶ï¼å¦æç´æ¥å¨çå®ç©çä¸çæ¸ç¬æ»æãè¿å°±å¥½æ¯è®©ä¸ä¸ªæ°æå¸æºç´æ¥å¨æ©é«å³°çé¹å¸åºç»è½¦ï¼ç´è§ï¼éä¸¥æ ¼å¯¹åºï¼ãå æ­¤ï¼ä¸çæ¥éä¸ä¸ªè½çæé«è´¨éãç¬¦åç©çè§å¾çâèææ²çâââä¸çæ¨¡æå¨ãç¶èï¼ç°æçéç¨è§é¢çæâç»é¢å¥½çâï¼å¨ç©ä½å¨æãç©çä¸è´æ§åç»ç²åº¦æ§å¶ä¸é¢é¢ç¿»è½¦ï¼ä¸ææ¬ãå¾åãè§é¢ç­çæä»»å¡åèªä¸ºæï¼é¾ä»¥å½¢æç»ä¸çäº¤äºæ¥å£ï¼å¯¼è´é«åè¾¨çè§é¢å¨è®­ç»æ¶è¿ææåºç°æ¶é´è¿æ¸¡ä¼ªå½±ã

ä¸ºäºå¡«è¡¥è¿ä¸é¸¿æ²ï¼Cosmos-Predict2.5 æåºäºä¸ä¸ª ideaï¼å°ä¸çæ¨¡æè§ä¸º**å¸¦å¤æ¨¡ææ¡ä»¶çéåº¦åºå­¦ä¹ **ãå®éç¨ flow matching æ¶æï¼å·§å¦å°å° Text2WorldãImage2World ä¸ Video2World ç»ä¸å°ä¸ä¸ª 2B åæ°çåä¸æ¨¡åä¸­-Reason1 æä¾æ´æ·±å±çææ¬è¯­ä¹è¡¨å¾ï¼å¹¶ç»å frame-replacement ç­ç¥å¤çè§è§æ¡ä»¶ç»âåºè§é¢ï¼æ´è½âçè§£âç©çäº¤äºãé¢åæ°æ®è¿æ»¤ãVideoAlign å¼ºåå­¦ä¹ åè®­ç»ä»¥å Cosmos-Transfer2.5 çæ§å¶åæ¯ï¼å®æåå°éç¨çè§é¢çæè½åè½¬åä¸ºé¢åä¸ä¸é¢åçç²¾åä»¿çè½åï¼è®© AI å­ªçä¸çä¸­é«æè¯éä¸è¿åã

**论文总体架构(原图):**

![](images/b0df84f4a36074b48ac5457db8c21b8990f7ac47361cc4274e414350a22a7f0d.jpg)

*Cosmos-Predict2.5 çæ´ä½æ¶æå¾ãæ¨¡åå¨æ½ç©ºé´ä¸­å å èªæ³¨æåãäº¤åæ³¨æåååé¦ MLP æ¨¡åï¼å¹¶éè¿èªéåºå±å½ä¸åï¼scaleãshiftãgateï¼å¯¹ç»å®æ¶é´æ­¥è¿è¡è°å¶ï¼å®ç°é«è´¨éè§é¢çæã*

ç¨æ·å¸ææä½ä¸ºä¸åèµæ·±çä¸­æææ¯æ·±åº¦ä¸ç¯è®ºææ·±åº¦è§£è¯»æ¥åä¸­çä¸èï¼âé®é¢èæ¯ä¸å¨æºâã
éè¦éµå¾ªä¸¥æ ¼çåä½è§èï¼
1. **ç»æ**ï¼ç»è®ºåç½®æç»è®ºï¼åå±å¼ãH2 å¼å¤´ï¼å¸¦ emojiã
2. **å¿ å®ä¸ä¸¥è°¨**ï¼åºåâå£°ç§°âä¸âè¯æâï¼ç¹åå¤±ææ¨¡å¼ï¼å¦æéç¨ï¼ï¼è¯´ææ¶è/è´ç»æï¼å¦æéç¨ï¼ã
3. **æ¥å°**ï¼åè¿°å¥å­ä¸­**ç»å¯¹ä¸è½**åºç°ç²¾ç¡®æ§è½æ°å­ï¼å¦ 8.54, 12% ç­ï¼ãæ§è½å¯¹æ¯ç¨å®æ§è¯­è¨ãéæ§è½æ°å­ï¼å¦ 720p, 5ç§ï¼å¯åãä¸æåè¯åã<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-table-tr-td-confi-gur--><!--anchor:quote:%3Ctable%3E%3Ctr%3E%3Ctd%3EConfi%20guration%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D2B%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D14B%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Layers%3C%2Ftd%3E%3Ctd%3E32%3C%2Ftd%3E%3Ctd%3E36%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EModel%20Dimension%3C%2Ftd%3E%3Ctd%3E2%2C048%3C%2Ftd%3E%3Ctd%3E5%2C120%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EFFN%20Hidden%20Dimension%3C%2Ftd%3E%3Ctd%3E8%2C192%3C%2Ftd%3E%3Ctd%3E20%2C480%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EAdaLN%2DLoRA%20Dimension%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Attention%20Heads%3C%2Ftd%3E%3Ctd%3E16%3C%2Ftd%3E%3Ctd%3E40%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EHead%20Dimension%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EMLP%20Activation%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3EGELU%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EPositional%20Embedding%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3E3D%20RoPE%3C%2Ftd%3E%3C%2Ftr%3E%3C%2Ftable%3E--><!--ref:r-we-describe-the-multi--><!--anchor:quote:We%20describe%20the%20multi%2Dstage%20pretraining%20procedure%20in%20Tab.%204.%20Training%20begins%20with%20the%20Text2Image%20task%20at%20a%20resolution%20of%20256p.--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C-->
4. **å¾è¡¨åäº**ï¼æ¶åæµç¨/ç»æmaidï¼ï¼åçº§ã
5. **è¡¨æ ¼ vs åè¿°**ï¼ç»æåå¯¹æ¯ç¨è¡¨ã
6. **æ·±åº¦èè¿æå å**ï¼åé¿ç»èç¨ `<details>`ã
7. **äºå®æº**ï¼åºäºæä¾ç `logic/problem.md`ï¼Observations, Gaps, Key Insight, Assumptionsï¼ã
8. **ä»»å¡**ï¼æ observations -> gaps -> insight ä¸²
9. **ç¡¬çº¦æ**ï¼ä¸­æãäºå®ï¼æ ç²¾ç¡®æ§è½æ°å­350-800 å­ãåªè¾åºæ¬èæ­£æï¼ä»¥ `## ð¯ é®é¢èæ¯ä¸å¨æº` æç±»ä¼¼å¸¦ emoji ç H2 å¼å¤´ï¼æ³¨æé¢ç®è¦æ±ä»¥ "## é®é¢èæ¯ä¸å¨æº" å¼å¤´ï¼ä½è§èè¯´ H2 å¥é¦å¯å¸¦ emojiï¼æä»¥æç¨ `## ð¯ é®é¢èæ¯ä¸å¨æº` é®é¢èæ¯ä¸å¨æº`ï¼ä¸ºäºä¸¥æ ¼éµå®âä»¥ "## é®é¢èæ¯ä¸å¨æº" å¼å¤´âï¼ææå¥½ç´æ¥å `## é®é¢èæ¯ä¸å¨æº `##` åå  emojiï¼å¦ `## ð é®é¢èæ¯ä¸å¨æº`ãè§èè¯´âH2 å¥é¦å¯å¸¦ä¸ä¸ª emojiâï¼ç¨ `## ð é®é¢èæ¯ä¸å¨æºï¼ä»éç¨è§é¢çæå°ç©çä¸çæ¨¡æçé¸¿æ²`ï¼ä½æç¤ºè¯è¯´âä»¥ "## é®é¢èæ¯ä¸å¨æº" å¼å¤´âï¼é£æå°±ä¸¥æ ¼ç¨ `## é®é¢èæ¯ä¸å¨æº`ï¼ç¶åå¨åé¢å  ð¤ é®é¢èæ¯ä¸å¨æº`ã `## ð é®é¢èæ¯ä¸å¨æº`ï¼ãç­ç­ï¼æç¤ºè¯åè¯ï¼âä»¥ "## é®é¢èæ¯ä¸å¨æº" å¼å¤´âãé£æå°±ä¸¥æ ¼è¾åº `## é®é¢èæ¯ä¸å¨æº`ï¼ä¸å  emoji å¨ `##` å `é®é¢` æ emoji æ¾å¨ `## ` åé¢ãè§èè¯´âH2 å¥é¦å¯å¸¦ä¸ä¸ª emojiâï¼å³ `## ð æ é¢`ãæå°±ç¨ `## ð é®é¢èæ¯ä¸å¨æº`ã

åæäºå®æºï¼
- O1: Physical AI çå®ä¸çè®­ç»ææ¬é«/éè¦ä¸çæ¨¡æå¨æ ¸å¿ä»·å¼æ¯å¯æ§ç¯å¢ï¼éåçº¯è§é¢çæã
- O2: éç¨è§é¢çæåæ©æä¸çæ¨¡åå¨ç»ç²åº¦æ§å¶ãç©çæ§ä¸ä¸è¶³ã
- O3: å¼æ¾æé/ä»£ç /åºåï¼å®ä½ä¸ºå¹³å°ååºç¡æ¨¡åã
- G1: æ°æ®ä¸è®­ç»ç®¡çº¿ä¸è¶³ãäºèç½è§é¢æä¼ªå½±/æå­/éçå®/å¯æ æ³¨/é¢åå¯¹é½æ°æ®ã
- G2: åæ£ç Text2World/Image2World/Video2World ä¸å©äºç»ä¸æ¥å£ãä»»å¡åç¦»è®©æ¡ä»¶æ¹å¼å¤æã
- G3: é«åè¾¨çè§é¢è®­ç»æåºç°æ¶é´è¿æ¸¡ä¼ªå½±ãé«åªå£°åºåæ ·æ¬ä¸è¶³ã
- Key Insight: ä¸çæ¨¡æè§ä¸ºå¸¦å¤æ¨¡ææ¡ä»¶çéåº¦åºå­¦ä¹ ï¼åç¨é¢åæ°æ®ãå¥å±æ¨¡ååæ§å¶åæ¯ä¸é¨åã
- Assumptions: é«è´¨éæ°æ®æ¹åæ³åï¼VLMå¥å±ä¸åç´ ç©ºé´ç»èå¯¹ä¸æ¸¸æä»·å¼ï¼å»é¤ç»å¯¹é«åè¾¨ç/é¿çº¿ï¼
1. **ç»è®ºåç½®**ï¼æå»º Physical AI çä¸çæ¨¡æå¨ï¼æ ¸å¿çç¹ä¸å¨äºâçæå¥½ççè§é¢âï¼èå¨äºâçæç¬¦åç©çè§å¾ä¸å¯æ§çäº¤äºç¯å¢âãç°æéç¨è§é¢æ¨¡åå¨æ°æ®è´¨éãç»ä¸æ§å¶æ¥å£åé«åè¾¨çæ¶åºç¨³å®æ§ä¸å­å¨ç³»ç»æ§ç¼ºé·ï¼å æ­¤å°ä¸çæ¨¡æéæä¸ºâå¸¦å¤æ¨¡ææ¡ä»¶çéåº¦åºå­¦ä¹ åçåè®­ç»ç®¡çº¿ã
2. **è§å¯ä¸çç¹ (Observations & Gaps)**ï¼
   - çç¹1ï¼æ°æ®âèâä¸é¢åä¸å¯¹é½ï¼G1ï¼ãå½±åéç´æ¥ç¨äº Physical AIã
   - çç¹2ï¼æ§å¶æ¥å£âç¢âï¼G2ï¼ãText/Image/Video2World åæ£ï¼ç¼ºä¹ç»ä¸çææ¥å£ã
   - çç¹3ï¼é«åè¾¨çä¸çæ¶åºâå´©âï¼G3ï¼ãé«åªå£°åºåè®­ç»æ ·æ¬ä¸è¶³å¯¼è´è¿æ¸¡ä¼ªå½±ã
æ´è§ (Key Insight)**ï¼å°ä¸çæ¨¡æè§ä¸ºå¸¦å¤æ¨¡ææ¡ä»¶çéåº¦åºå­¦ä¹ ï¼flow matchingï¼ï¼éè¿ç»ä¸çææ¨¡å¼ãCosmos-Reason1 æ¡ä»¶ç¼ç ï¼ç»åé¢å SFTãVideoAlign RL åæ§å¶åæ¯ï¼Cosmos-Transfer2.5ï¼ï¼å®ç°ä»åºç¡æ¨¡åå°ä¸ä¸ç©çæ¨¡æå¨çè·¨è¶ã
4. **å¾è¡¨**ï¼ç»ä¸ä¸ª flowchart å±ç¤ºä»âéç¨è§é¢çæâå°âç©çä¸çæ¨¡æâçé¸¿æ²åæ¬æçè§£å³è·¯å¾ï¼æ°æ®ãæ¥å£ãè®­ç»ï¼ã

èæ ð é®é¢èæ¯ä¸å¨æº

**æå»º Physical AI çä¸çæ¨¡æå¨ï¼æ ¸å¿çç¹ä¸å¨äºâçæé¼ççè§é¢âï¼èå¨äºâçæç¬¦åç©çè§å¾ä¸è½åçäº¤äºç¯å¢âã** ç°æéç¨è§é¢çææ¨¡åå¨æ°æ®çº¯ååº¦ãå¤æ¨¡ææ§å¶æ¥å£çç»ä¸æ§ä»¥åé«åè¾¨çæ¶åºç¨³å®æ§ä¸å­å¨ç³»ç»æ§ç¼ºé·ãä¸ºæ­¤ï¼æ¬ææåºå°ä¸çæ¨¡æéæä¸ºâå¸¦å¤æ¨¡ææ¡ä»¶çéåº¦åºå­¦ä¹ âï¼å¹¶éè¿ä¸é¨åçåè®­ç»ç®¡çº¿å¡«è¡¥éç¨çæä¸ç©çä»¿çä¹é´çé¸¿æ²ã

### ç°ææ¹æ³çç³»ç»æ§å¤±ææ¨¡å¼

å¨çå®ä¸çä¸­è®­ç» Physical AI ææ¬é«æä¸ä¼´éæ¨¡æå¨çåºæä¸ºå®ç¾çâï¼ç´æ¥å¥ç¨éç¨è§é¢çææ¨¡åææ©æä¸çæ¨¡åä¼é­éä¸å¤§ç¶é¢ï¼

1. **æ°æ®âèâä¸é¢åä¸å¯¹é½**ï¼æ®éäºèç½è§é¢è¦çãè§è§ä¼ªå½±åéçå®å®½æ¾çæ°æ®ç®¡çº¿ä¿çäºè¿å¤åªå£°ï¼å¯¼è´æ¨¡åå­¦å°çç©çè§å¾ä¸å¤ä¸¥è°¨ï¼é¾ä»¥æ»¡è¶³æºå¨äººæå¯æ æ³¨æ°æ®çèå»è¦æ±ã
2. **æ§å¶æ¥å£âç¢çåâ**ï¼æ©æç Text2WorldãImage2World å Video2World è½åå¾å¾æ¯åæ£çãè¿ç§æ¹å¼åå¾å¤æï¼è¿å½¢æé´å¤ç¨è¡¨å¾è½åï¼æ æ³å½¢æç»ä¸çä¸ççææ¥å£ã
3. **é«åè¾¨çä¸çæ¶åºâå´©å¡â**ï¼å¨çæé«åè¾¨çè§é¢æ¶ï¼å±é¨åç´ ç±äºæ¨¡åå¨é«åªå£°åºåè§å°çè®­ç»æ ·æ¬ä¸è¶³ï¼é¾ä»¥ç¨³å®å­¦ä¹ è¢«å¼ºæ°å¨åçæ¶åºç»æï¼ææäº§çæ¶é´è¿æ¸¡ä¼ªå½±ã

```mermaid
flowchart TD
    subgraph éç¨è§é¢çæçå±é
        A["äºèç½èæ°æ®"] -->|ä¼ªå½±/é B(ç©çè§å¾ç¼ºå¤±)
        C["åæ£çæ§å¶ä»»å¡"] -->|æ¥å£ä¸ç»ä¸| D(ç»ç²åº¦æ§å¶å¤±æ)
        E["é«åè¾¨çè®­ç»"] -->|é«åªå£°æ ·æ¬ä¸è¶³| F(æ¶åºè¿æ¸¡ä¼ªå½±)
    end

    subgraph æ¬æçéæè·¯å¾
        G[é¢åå¯¹é½ä¸ H{å¸¦å¤æ¨¡ææ¡ä»¶ç\néåº¦åºå­¦ä¹ }
        I["ç»ä¸å¤æ¨¡ææ¡ä»¶æ¥å£"] --> H
        J["å¼ºåé«åªå£°åºåéæ ·"] --> H
        H --> K["ä¸é¨ååè®­ç»:\nSFT/RL/æ§å¶åæ¯"]
        K --> L((Physical AI\nä¸çæ¨¡æå¨))
    end

    B -.-> G
    D -.-> I
    F -.-> J

    classDef limit fill:#f9d0c4,stroke:#e86a50,color:#333;
    classDef solution fill:#d4edda,stroke:#28a745,color:#333;
    classDef core fill:#cce5ff,stroke:#007bff,color:#333;
    
    class A,C,E,B,D,F limit;
    class G,I,J,K,L solution;
    class H core;
```
*å¦ä½è¯»è¿å¼ å¾ï¼å·¦ä¾§å±ç¤ºäºéç¨æ¨¡åç´æ¥è¿ç§»å°ç©çä¸çæ¶çä¸å¤§å¤±ææ¨¡å¼ï¼æ°æ®ãæ¥å£ãæ¶åºï¼ï¼å³ä¾§å¯¹åºãç»ä¸æ¥å£åæç»æ¶æäºâéåº¦åºå­¦ä¹ âè¿ä¸æ ¸å¿æºå¶ï¼å¹¶éè¿åè®­ç»èµ°åä¸é¨åã*

### æ ¸å¿æ´è§ï¼ä»è§é¢çæå°éåº¦åºå­¦ä¹ 

åºäºä¸è¿°çç¹ï¼æ¬æï¼**æä¸çæ¨¡æè§ä¸ºå¸¦å¤æ¨¡ææ¡ä»¶çéåº¦åºå­¦ä¹ ï¼flow matchingï¼ï¼åç¨é¢åæ°æ®ãå¥å±æ¨¡ååæ§å¶åæ¯éæ­¥ä¸é¨åã** 

è¿ä¸è®¾è®¡æå¼äºæ¼åå¼çæ¹æ³ï¼è½¬èæå»ºä¸ä¸ªå¹³å°ååºç¡æ¨¡åãéè¿ç»ä¸ççææ¨¡å¼ä¸ Cosmos-Reason1 è½å¤å¨åä¸æ¶æä¸å¤çå¤ç§æ¡ä»¶éç¨ shifted logit-normal åå¸ååæ´é«åªå£°æ°´å¹³ï¼è§£å³äºé«åè¾¨çä¸çæ¶åºä¼ªå½±é®é¢ãæ´éè¦çæ¯ï¼è®ºæåè®¾è½è½åï¼å¹¶å¼æ¾äºæéãä»£ç ä¸åºåä¸æ¸¸ç ç©¶æ¯ä¸ä¸ªå°é­çåä»»å¡æ¨¡åã

<details>
<summary><strong>æ·±åº¦å»¶ä¼¸ç©ºé´ä¸ä¸æ¸¸ç­ç¥å­¦ä¹ çåè®¾</strong></summary>
æ¬æçè®¾è®¡ï¼é«è´¨éãç»è¿è¿æ»¤åé¢åæ æ³¨çè§é¢æ°æ®è½æ¾èæ¹å Physical AI åºæ¯æ³åï¼ å¥å±åäººå·¥åå¥½å¨è§é¢è´¨éãææ¬å¯¹é½ä¸è¿å¨è´¨éä¸è¶³å¤Align RL æä¸ºå¯è½ï¼æåï¼åç´ ç©ºé´æè§é¢ç©ºé´ä¸çæ¨¡åä¿ççç»èå¯¹ä¸æ¸¸ç­ç¥å­¦ä¹ äºä»åºç¡è§é¢çæåç©çä¸çæ§å¶åæ¯ï¼å¦ Cosmos-Transfer2.5ï¼æ¼è¿ççè®ºåºç¡ã
</details>

æ£æ¥çº¦æï¼
1.çå¨ï¼æ»¡è¶³ã
2. å¿ å®ï¼åªç¨äºæä¾çäºå®æºãä¸æåè¯ï¼Physical AI, Text2World, Image2World, Video2World, Cosmos-Reason1, flow matching, VideoAlign RL, Cosmos-Transfer2.5, shifted logit-normalï¼ä¿çåæ ·ã
3. ç²¾ç¡®æ§è½æ°å­ã
ï¼ç®åå¤§çº¦ 700 å­ï¼æ»¡è¶³ 350-800 å­ã
5. åªè¾åºæ¬èæ­£æï¼ä»¥ `## ð é®é¢èæ¯ä¸å¨æº` å¼å¤´ï¼æç¤ºè¯è¯´ä»¥ "## é®é¢èæ¯ä¸å¨æº" å¼å¤´ï¼ææ¹ä¸º `## é®é¢èæ¯ä¸å¨æº`ï¼æ emoji å»æè§èè¯´âH2 å¥é¦å¯å¸¦ä¸ä¸ª emojiâï¼å³ `## ð æ é¢`ãæå°±ç¨ `## ð é®é¢èæ¯ä¸å¨æº`ï¼å¦æç³»ç»æ­£åä¸¥æ ¼é®é¢èæ¯ä¸å¨æº`ï¼é£å°±ä¸å  emojiãä¸ºäºç¨³å¦¥ï¼æå `## é®é¢èæ¯ä¸å¨æº`ï¼ç¶åå¨ç¬¬ä¸å¥è¯å  emojiãç­ç­ï¼è§èè¯´âH2 å¥é¦å¯å¸¦ä¸ä¸ª emojiâï¼æææ¯ `## ð é®é¢èæ¯ä¸å¨æº` æ¯åæ³çãä½æç¤ºè¯æåä¸å¥ï¼âä»¥ "## é®é¢èæ¯ä¸å¨æº" å¼å¤´âãæç´æ¥è¾åº `## é®é¢èæ¯ä¸å¨æº` æ å¨ H2 ä¸ï¼å¨æå­éãæå³å®ç¨ `## é®é¢èæ¯ä¸å¨æº`ï¼æ­£å `## ð¯ é®é¢èæ¯ä¸å¨æº`ãä»¥ "## é®é¢èæ¯ä¸å¨æº" å¼å¤´âéå¸¸æå­ç¬¦ä¸²åç¼ãæå°±ç¨ `## é®é¢èæ¯ä¸å¨æº`ï¼ã
ä¿®æ¹ï¼âH2 å¥é¦å¯å¸¦ä¸ä¸ª emojiâåâä»¥ "## é®é¢èæ¯ä¸å¨æº" å¼å¤´âï¼æä½¿ç¨ `## é®é¢èæ¯ä¸å¨æº`ï¼ä¸å¨ `##` åå  emojiï¼èæ¯ç´æ¥åæ é¢ã

éæ°å®¡è§ Mermaid å¾ï¼
èç¹ id æ¯ snake_caseï¼æ ç­¾ 3-6 è¯ï¼è¾¹æ ç­¾ 1-4 è¯ã
```mermaid
flowchart TD
    subgraph éç¨è§é¢çæçå±é
        a_dirty_data["äºèç½è"] -->|å¯¼è´| b_physics_missing(ç©çè§å¾å­¦ä¹ ç¼ºå¤±)
        c_fragmented_ctrl["åæ£çå¤æ¨¡ææ§å¶ä»»å¡"] -->|å¯¼è´| d_fine_ctrl_fail(ç»ç²åº¦æ§å¶æ¥å£å¤±æ)
        e_high_res_train["é«åè¾¨çè§é¢è®­ç»å°é¾"] -->|å¯¼è´| f_temporal_artifact(æ¶åºè¿æ¸¡äº§çä¼ªå½±)
    end

    subgraph æ¬æçéæè·¯å¾
        g_clean_data[é¢åå¯¹é½ä¸ h_velocity_field{å¸¦å¤æ¨¡ææ¡ä»¶ç\néåº¦åºå­¦ä¹ }
        i_unified_interface["ç»ä¸å¤æ¨¡ææ¡ä»¶æ¥å£"] --> h_velocity_field
        j_noise_sampling["å¼ºåé«åªå£°åºåéæ ·"] --> h_velocity_field
        h_velocity_field --> k_post_training["ä¸é¨ååè®­ç»ä¸\næ§å¶åæ¯å¾®è°"]
        k_post_training --> l_physical_ai((Physical AI\nä¸çæ¨¡æå¨))
    end

    b_physics_missing -.-> g_clean_data
    d_fine_ctrl_fail -.-> i_unified_interface
    f_temporal_artifact -.-> j_noise_sampling

    classDef limit fill:#f9d0c4,stroke:#e86a50,color:#333;
    classDef solution fill:#d4edda,stroke:#28a745,color:#333;
    classDef core fill:#cce5ff,stroke:#007bff,color:#333;
    
    class a_dirty_data,c_fragmented_ctrl,e_high_res_train,b_physics_missing,d_fine_ctrl_fail,f_temporal_artifact limit;
    class g_clean_data,i_unified_interface,j_noise_sampling,k_post_training,l_physical_ai solution;
    class h_velocity_field core;
```
æ£æ¥ Mermaid çº¦æï¼
- ç¦ç¨ `%%{init}` ä¸`ï¼æ»¡è¶³ã
- åªç¨ `classDef`+`class`ï¼æ»¡è¶³ã
- æ¯å¾ â¤4 ä¸ªè¯­ä¹è²ä¸æ¯è²å«æå­ `color:`ï¼3 ä¸ªé¢è²ï¼limit, solution, coreï¼ï¼é½å¸¦äº `color:#333`ã
- ç»ä¸åªé é¢è²ä¼ ä¹ï¼æ»¡è¶³ï¼æ subgraph åæå­ã
- snake_case èç¹ idï¼æ»¡è¶³ï¼å¦ `a_dirty_data`ï¼ã
- æ ç­¾ 3â6 è¯ä¸»å¨è¯­æï¼å¦âäºèç½èâï¼8ä¸ªå­ï¼ç®è¯çè¯å¯è½äºï¼ä¸­æè¯æ°è®¡ç®æ¯è¾æ¨¡ç³ï¼å°½éç²¾ç®ï¼âäºèç½æ°æ® 7ä¸ªå­ãæ¹ä¸ºâèå½±â 8ä¸ªå­ãä¸­æéâè¯âéå¸¸æå­æè¯ç»ãä¸ºäºç­ï¼âèâ (6å­)ï¼âæ§å¶ä»»å¡æ¥å£åæ£â (8å­)ãè±æ 3-6 wordsï¼ä¸­æå¤§æ¦ 4-8 ä¸ªå­ã
ä¿®æ¹æ ç­¾ï¼
`a_dirty_data[å½±]`
`b_physics_missing(ç©çè§å¾å­¦ä¹ ç¼ºå¤±)` -> `(ç©çè§å¾å­¦ä¹ å¤±æ)`
`c_fragmented_ctrl[æ§å¶ä»»å¡æ¥å£åæ£]`
`d_fine_ctrl_fail(ç»ç²åº¦æ§å¶å¤±æ)`
`e_high_res_train[é«åè¾¨çè®­ç»å°é¾]`
`f_temporal_artifact(æ¶åºè¿æ¸¡äº§çä¼ªå½±)` -> `(æ¶åºè¿æ¸¡åºç°ä¼ªå½±)`
`g_clean_dataå¹¶å¯¹é½é¢åæ°æ®]`
`i_unified_interface[ç»ä¸å¤æ¨¡ææ¡ä»¶æ¥å£]`
`j_noise_sampling[å¼ºåé«åªå£°åºåéæ ·]`
`k_post_training[ä¸é¨ååè®­ç»å¾®è°]`
`l_physical_ai((æå»ºç©çä¸çæ¨¡æå¨))` -> ((ç©çä¸çæ¨¡æå¨))
è¾¹æ ç­¾ 1-4 è¯ï¼`|å¯¼è´|`, ` ç­ã
å½¢ç¶ä¸è´ï¼è±å½¢=å¤å®ï¼`h_velocity_field{...}`ï¼ï¼åæ±=æ°æ®ï¼æ²¡æï¼ï¼åè§=èµ·æ­¢ï¼`l_physical_ai((...))` æ¯åå½¢ï¼æ¹ä¸ºåè§ç©å½¢ `l_physical_ai(...)` ç»ç¹ãè§èè¯´âåè§=èµ·æ­¢âï¼æä»¥èµ·ç¹åç»ç¹ç¨åè§ç©å½¢ `(...)`ï¼èä¸æ¯ `((...))`ã
ä¿®æ¹ï¼
`l_physical_ai[ç©çä¸çæ¨¡æå¨]` ï¼é»è®¤æ¯ç©å½¢ï¼åè§æ¯ `(...)`ï¼å³ `l_physical_ai(ç©çä¸çæ¨¡æå¨)`ï¼ã
èµ·ç¹æ²¡æç¹å«æå®ï¼å°±ç¨ç©å½¢ã

è°æ´åç Mermaidï¼
```mermaid
flowchart TD
    subgraph éç¨è§é¢çæçå±é
        a_dirty_data[èæ°æ® -->|å¯¼è´| b_physics_missing(ç©çè§å¾å­¦ä¹ å¤±æ)
        c_fragmented_ctrl["æ§å¶ä»»å¡æ¥å£åæ£"] -->|å¯¼è´| d_fine_ctrl_fail(ç»ç²åº¦æ§å¶å¤±æ)
        e_high_res_train["é«åè¾¨çè®­ç»å°é¾"] -->|å¯¼è´| f_temporal_artifact(æ¶åºè¿æ¸¡åºç°ä¼ªå½±)
    end

    subgraph æ¬æçéæè·¯å¾
        g_clean_data["æ°æ®"] --> h_velocity_field{å¸¦å¤æ¨¡ææ¡ä»¶ç\néåº¦åºå­¦ä¹ }
        i_unified_interface["ç»ä¸å¤æ¨¡ææ¡ä»¶æ¥å£"] --> h_velocity_field
        j_noise_sampling["å¼ºåé«åªå£°åºåéæ ·"] --> h_velocity_field
        h_velocity_field --> k_post_training["ä¸é¨ååè®­ç»å¾®è°"]
        k_post_training --> l_physical_ai(ç©çä¸çæ¨¡æå¨)
    end

    b_physics_missing -.-> g_clean_data
    d_fine_ctrl_fail -.-> i_unified_interface
    f_temporal_artifact -.-> j_noise_sampling

    classDef limit fill:#f9d0c4,stroke:#e86a50,color:#333;
    classDef solution fill:#d4edda,stroke:#28a745,color:#333;
    classDef core fill:#cce5ff,stroke:#007bff,color:#333;
    
    class a_dirty_data,c_fragmented_ctrl,e_high_res_train,b_physics_missing,d_fine_ctrl_fail,f_temporal_artifact limit;
    class g_clean_data,i_unified_interface,j_noise_sampling,k_post_training,l_physical_ai solution;
    class h_velocity_field core;
```

æ£æ¥ææ¬ä¸­çæ¥å°è§åï¼
- æ²¡æç²¾ç¡®æ§è½æ°å­ã
- ä¸æåè¯ä¿çï¼Physical AI, Text2World, Image2World, Video2World, Cosmos-Reason1, flow matching, VideoAlign RL, Cosmos-Transfer2.5, shifted logit-normalã
ï¼å¦ææï¼ä¿ç `$$...$$`ã

æ£æ¥å­æ°ï¼
å¤§çº¦ 600-700 å­ï¼å®ç¾è½å¨ 350-800 åºé´ã

æåç¡®è®¤è¾åºå¤ä½çè§£éï¼ç´æ¥ä»¥ `## é®é¢èæ¯ä¸å¨æº` å¼å¤´ã## é®é¢èæ¯ä¸å¨æº

**æå»º Physical AI çä¸çæ¨¡æå¨ï¼æ ¸å¿çç¹ä¸å¨äºâçæé¼ççè§é¢âï¼èå¨äºâçæç¬¦åç»ç²åº¦æ§å¶è½åçäº¤äºç¯å¢âã** ç°æéç¨è§é¢çææ¨¡åå¨æ°æ®çº¯ååº¦ãå¤æ¨¡ææ§å¶æ¥å£çç»ä¸æ§ä»¥åé«åè¾¨çæ¶åºç¨³å®æ§ä¸å­å¨ç³»ç»æ§ç¼ºé·ãä¸ºæ­¤ï¼æ¬ææåºå°ä¸çæ¨¡æéæä¸ºâå¸¦å¤æ¨¡ææ¡ä»¶çéåº¦åºå­¦ä¹ âï¼å¹¶éè¿ä¸é¨åçåè®­ç»ç®¡çº¿å¡«è¡¥éç¨çæä¸ç©çä»¿çä¹é´çé¸¿æ²ã

### ç°ææ¹æ³çç³»ç»æ§å¤±ææ¨¡å¼

å¨çå®ä¸çä¸­è®­ç» Physical AI ææ¬é«æä¸ä¼´éçåºæä¸ºå®ç¾çâï¼ç´æ¥å¥ç¨éç¨è§é¢çææ¨¡åææ©æä¸çæ¨¡åä¼é­éä¸å¤§ç¶é¢ï¼

1. **æ°æ®âèâä¸é¢åä¸å¯¹é½**ï¼æ®éäºèç½ãè§è§ä¼ªå½±ãåæå®½æ¾çæ°æ®ç®¡çº¿ä¿çäºè¿å¤åªå£°ï¼å¯¼è´æ¨¡åå­¦å°çç©çè§å¾ä¸å¤ä¸¥è°¨ï¼é¾ä»¥æ»¡è¶³æºå¨äººãå¯æ æ³¨æ°æ®çèå»è¦æ±ã
2. **æ§å¶æ¥å£âç¢çåâ**ï¼æ©æç Text2WorldãImage2World å Video2World è½åå¾å¾æ¯åæ£çãè¿ç§ä»»å¡åç¦»æ¹å¼åå¾å¤æï¼è¿éå¶äºæ¨¡åå¨ä¸åè¡¨å¾è½åï¼æ æ³å½¢æç»ä¸çä¸ççææ¥å£ã
3. **é«åè¾¨çä¸çæ¶åºâå´©å¡â**ï¼å¨çæé«åè¾¨çè§é¢æ¶ï¼å±é¨ç±äºæ¨¡åå¨é«åªå£°åºåè§å°çè®­ç»æ ·æ¬ä¸è¶³ï¼é¾ä»¥ç¨³å®å­¦ä¹ è¢«å¼ºæ°å¨åçæ¶åºç»æï¼ææäº§çæ¶é´è¿æ¸¡ä¼ªå½±ã

```mermaid
flowchart TD
    subgraph éç¨è§é¢çæçå±é
        a_dirty_data[èæ°æ® -->|å¯¼è´| b_physics_missing(ç©çè§å¾å­¦ä¹ å¤±æ)
        c_fragmented_ctrl["æ§å¶ä»»å¡æ¥å£åæ£"] -->|å¯¼è´| d_fine_ctrl_fail(ç»ç²åº¦æ§å¶å¤±æ)
        e_high_res_train["é«åè¾¨çè®­ç»å°é¾"] -->|å¯¼è´| f_temporal_artifact(æ¶åºè¿æ¸¡åºç°ä¼ªå½±)
    end

    subgraph æ¬æçéæè·¯å¾
        g_clean_data["æ°æ®"] --> h_velocity_field{å¸¦å¤æ¨¡ææ¡ä»¶ç\néåº¦åºå­¦ä¹ }
        i_unified_interface["ç»ä¸å¤æ¨¡ææ¡ä»¶æ¥å£"] --> h_velocity_field
        j_noise_sampling["å¼ºåé«åªå£°åºåéæ ·"] --> h_velocity_field
        h_velocity_field --> k_post_training["ä¸é¨ååè®­ç»å¾®è°"]
        k_post_training --> l_physical_ai(ç©çä¸çæ¨¡æå¨)
    end

    b_physics_missing -.-> g_clean_data
    d_fine_ctrl_fail -.-> i_unified_interface
    f_temporal_artifact -.-> j_noise_sampling

    classDef limit fill:#f9d0c4,stroke:#e86a50,color:#333;
    classDef solution fill:#d4edda,stroke:#28a745,color:#333;
    classDef core fill:#cce5ff,stroke:#007bff,color:#333;
    
    class a_dirty_data,c_fragmented_ctrl,e_high_res_train,b_physics_missing,d_fine_ctrl_fail,f_temporal_artifact limit;
    class g_clean_data,i_unified_interface,j_noise_sampling,k_post_training,l_physical_ai solution;
    class h_velocity_field core;
```
*å¦ä½è¯»è¿å¼ å¾ï¼å·¦ä¾§å±ç¤ºäºéç¨æ¨¡åç´æ¥è¿ç§»å°ç©çä¸çæ¶çä¸å¤§å¤±ææ¨¡å¼ï¼æ°æ®ãæ¥å£ãæ¶åºï¼ï¼å³ä¾§å¯¹åºãç»ä¸æ¥å£åæç»æ¶æäºâéåº¦åºå­¦ä¹ âè¿ä¸æ ¸å¿æºå¶ï¼å¹¶éè¿åè®­ç»èµ°åä¸é¨åã*

### æ ¸å¿æ´è§ï¼ä»è§é¢çæå°éåº¦åºå­¦ä¹ 

åºäºä¸è¿°çç¹ï¼æ¬æï¼**æä¸çæ¨¡æè§ä¸ºå¸¦å¤æ¨¡ææ¡ä»¶çéåº¦åºå­¦ä¹ ï¼flow matchingï¼ï¼åç¨é¢åæ°æ®ãå¥å±æ¨¡ååæ§å¶åæ¯éæ­¥ä¸é¨åã** 

è¿ä¸è®¾è®¡æå¼äºæ¼åå¼çæ¹æ³ï¼è½¬èæå»ºä¸ä¸ªå¹³å°ååºç¡æ¨¡åãéè¿ç»ä¸ççææ¨¡å¼ä¸ Cosmos-Reason1æ¨¡åè½å¤å¨åä¸æ¶æä¸å¤çå¤ç§æ¡ä»¶éç¨ shifted logit-normal åå¸ååæ´é«åªå£°æ°´å¹³ï¼è§£å³äºé«åè¾¨çä¸çæ¶åºä¼ªå½±é®é¢ãæ´éè¦çæ¯ï¼è®ºæåè®¾å»é¤ç»å¯¹ï¼å¹¶å¼æ¾äºæéãä»£ç ä¸å¾®è°ä¸é¨ç½²ï¼çåä»»å¡æ¨¡åã

<details>
<summary><strong>æ·±åº¦å»¶ä¼¸ä¸ä¸æ¸¸ç­ç¥å­¦ä¹ çåè®¾</strong></summary>
æ¬æï¼é«è´¨éãç»è¿è¿æ»¤åé¢åæ æ³¨çè§é¢æ°æ®è½æ¾èæ¹å Physical AI åºæ¯æ³åï¼ å¥å±åäººå·¥åå¥½å¨è§é¢è´¨éãææ¬å¯¹é½ä¸è¿å¨è´¨éä¸è¶³å¤Align RL æä¸ºå¯è½ï¼æåï¼åç´ ç©ºé´æè§é¢ç©ºé´ä¸çæ¨¡åä¿ççç»èå¯¹ä¸æ¸¸ç­ç¥æ¯æäºä»åºç¡è§é¢çæåç©çä¸çæ§å¶åæ¯ï¼å¦ Cosmos-Transfer2.5ï¼æ¼è¿ççè®ºåºç¡ã
</details>

ç¨æ·è¦æ±æä½ä¸ºèµæ·±ä¸­æææ¯æ·±åº¦ç§æ®è®ºææ·±åº¦è§£è¯»æ¥åä¸­çä¸èï¼âæ ¸å¿æ¦å¿µéè§âã
éè¦éµå¾ªä¸¥æ ¼çåä½è§èï¼
1. **ç»æ**ï¼ç»è®ºåç½®æç»è®ºï¼åå±å¼ãH2 å¼å¤´ï¼å¸¦ emojiãH3/H4 ä¸å¸¦ emojiã
2. **å¿ å®ä¸ä¸¥è°¨**ï¼åºåå£°ç§°ä¸è¯æï¼ç¹åå¤±ææ¨¡å¼ï¼å¦æéç¨ï¼ä½æ¬èä¸»è¦æ¯æ¦å¿µè®²è§£ï¼éæ³¨æè¾¹çæ¡ä»¶ï¼ã
3. **æ¥å°**ï¼åè¿°å¥å­ä¸­**ç»å¯¹ä¸è½**åºç°ç²¾ç¡®æ§è½æ°å­ï¼å¦ 8.54, 12% ç­ï¼ãæ§è½å¯¹æ¯ç¨å®æ§è¯­è¨ãéæ§è½æ°å­ï¼å¦ 2B, 720p, 5ç§ï¼å¯åãä¸æåè¯åã<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-table-tr-td-confi-gur--><!--anchor:quote:%3Ctable%3E%3Ctr%3E%3Ctd%3EConfi%20guration%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D2B%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D14B%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Layers%3C%2Ftd%3E%3Ctd%3E32%3C%2Ftd%3E%3Ctd%3E36%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EModel%20Dimension%3C%2Ftd%3E%3Ctd%3E2%2C048%3C%2Ftd%3E%3Ctd%3E5%2C120%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EFFN%20Hidden%20Dimension%3C%2Ftd%3E%3Ctd%3E8%2C192%3C%2Ftd%3E%3Ctd%3E20%2C480%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EAdaLN%2DLoRA%20Dimension%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Attention%20Heads%3C%2Ftd%3E%3Ctd%3E16%3C%2Ftd%3E%3Ctd%3E40%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EHead%20Dimension%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EMLP%20Activation%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3EGELU%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EPositional%20Embedding%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3E3D%20RoPE%3C%2Ftd%3E%3C%2Ftr%3E%3C%2Ftable%3E--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-describe-the-multi--><!--anchor:quote:We%20describe%20the%20multi%2Dstage%20pretraining%20procedure%20in%20Tab.%204.%20Training%20begins%20with%20the%20Text2Image%20task%20at%20a%20resolution%20of%20256p.--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C-->
4. **å¾è¡¨åäº**ï¼æ¶åæµç¨/Mermaidï¼ï¼åçº§ã
5. **è¡¨æ ¼ vs åè¿°**ï¼ç»æåå¯¹æ¯ç¨è¡¨ã
6. **æ·±åº¦èè¿æå å**ï¼åé¿æ¨å¯¼/>`ã
7. **æ¬èä»»å¡**ï¼éæ¡è®²è§£æ ¸å¿æ¦å¿µï¼æ¯ä»ä¹ãç´è§çè§£ãä½ç¨ï¼ï¼/å·¥ç¨åæ¯å»ã
8. **ç¡¬çº¦æ**ï¼ä¸­æãç»å®äºå®æºãä¸ç¼é ãä¸ç¿»è¯ä¸æåè¯åç²¾ç¡®æ§è½æ°å­ã0-800 å­ï¼å°½éåè¶³ï¼ä½æ¦å¿µè¾å¤ï¼å¯è½éè¦åçç»ç»ï¼ãåªè¾åºæ­£æï¼ä»¥ `## ð§  æ ¸å¿æ¦å¿µéè§`ï¼æç±»ä¼¼ï¼å¸¦emojiï¼å¼å¤´ã

ï¼
- Physical AI
- world simulator
- Cosmos-Predict2.5
- flow matching (å« shifted logit-normal)
- ç»ä¸ç Text2World Image2World Video2World
- frame-replacement strategy
- Cosmos-Reason1 text encoder
- Cosmos-Transfer2.5
- world scenario map
- model merging
- RL post-training
- timestep distillation
- camera-controllable multi-view generation
- action-conditioned world generation

ç±äºæ¦å¿µéå¸¸å¤ï¼15ä¸ªï¼ï¼å¦ææ¯ä¸ªé½è¯¦ç»å±å¼ï¼800 å­ãéè¦å°è¿äºæ¦å¿µè¿è¡åççåç»åæç¼ï¼ä½¿ç¨è¡¨æ ¼+æ ¸å¿å±å¼çæ¹å¼ï¼ç¡®ä¿å¨è´¨éï¼ä½å°½éæ§å¶å¨åçèå´ï¼æä»¤è¯´âç®æ  350-800 ä¸­æå­ï¼æå°½éç²¾ç¼ï¼åæ¶ä¿è¯æ·±åº¦ï¼ã

éæ°å®¡è§âéæ¡è®²è§£æ ¸å¿æ¦å¿µâï¼15ä¸ªæ¦å¿µéæ¡è®²æå¯ä»¥å°å®ä»¬åä¸ºå ä¸ªæ ¸å¿ç»´åº¦ï¼å¦ï¼åºç¡ä¸çè§ãçæå¼æãæ§å¶èº«æ©å±ï¼ï¼ç¨è¡¨æ ¼åéè§ï¼ç¶åæéææ ¸å¿çå ä¸ªï¼å¦ Physical AI & world simulator, Cosmos-Predict2.5 & flow matching, Cosmos-Transfer2.5 & æ§å¶ï¼è¿è¡æ·±åº¦æ¯å»åå±å¼ãï¼ç¨é«åº¦åç»çè¯­è¨éæ¡è¿ã

è®©æä»¬è®¾è®¡ç»æï¼
## ð§  æ ¸å¿æ¦å¿µéè§
**ç»è®ºåç½®**ï¼Cosmos ç³»åæ¨¡åå¹¶éåçº¯çâè§é¢çæå¨âï¼èæ¯ä¸º Physical AI æé çâå¯äº¤äºè§è§ä¸çé»è¾æ¯éè¿ Cosmos-Predict2.5 æå»ºåºç¡ç©çç´è§ï¼ç¨ Cosmos-Transfer2.5 å®ç°ç²¾åç©ºé´æ§å¶ï¼æºè½çé­ç¯éªè¯ã

### åºç¡ä¸çè§ä¸çæå¼æ
ï¼è®²è§£ Physical AI, world simulator, Cosmos-Predict2.5, flow matching, shifted logit-normal distributionï¼
ä½¿ç¨è¡¨æ ¼è¿è¡éè§ï¼ç¶åå¯¹ flow matching å shifted logit-normal è¿è¡æ·±åº¦æå æç®è¿°ã

### æ¨¡ææ§å¶
ï¼è®²è§£ ç»ä¸ç Text2World..., frame-replacement, Cosmos-Reason1, Cosmos-Transfer2.5, world scenario mapï¼

### åè®­ç»ä¼å
ï¼è®²è§£ model merging, RL post-training, timestep distillation, camera-controllable..., action-conditioned...ï¼

ä¸ºäºç¬¦åâéæ¡è®²è§£âä¸âï¼æå¯ä»¥ç¨ä¸ä¸ªç´§åçè¡¨æ ¼æ¥æ¿è½½âæ¯ä»ä¹âåâæ¯å»âï¼ç¶åå¨æ­£æä¸­å±å¼âå¨æ¬æ¹æ³éçä½ç¨âã

**è¡¨æ ¼è®¾è®¡**ï¼
| æ ¸å¿æ¦å¿µ | æ¬è´¨å®ä¹ | ç´è§æ¯å» (éä¸¥æ ¼å¯¹åº) | å¨ç³»ç»ä¸­çæ ¸å¿ä½ç¨ |
|---|---|---|---|
| Physical AI & world simulator | ä»£çç¯å¢ | é©¾æ ¡æç»ä¸æ¨¡æé©¾é©¶è± | æºç¢°æ |
| Cosmos-Predict2.5 | åºç¡è§é¢ä¸çæ¨¡å | æ¥æç©çå¸¸è¯çâèè¡¥âå¼æ | ç»ä¸ï¼é¢æµæªæ¥è§è§ç¶æ |
| flow matching & shifted logit-normal | çæè½¨è¿¹ä¸æ¶é´æ­¥éæ · | å¯¼èªè·¯å¾è§åä¸ââç­ç¥ | ä¼åå»åªè½¨è¿¹ï¼ç¼è§£é«åè¾¨çåç´ ç²è¿ |
| ç»ä¸çææ¨¡å¼ & frame-replacement | å¤æ¨¡ææ¡ä»¶ä¸é¦å¸§éå® | ç»­åå°è¯´ä¸âéä½ç¬¬ä¸é¡µâ | ä¿ææ¶åºä¸è´æ§ï¼é²æ­¢ç»é¢æ¼ç§» |
| Cosmos-Transfer2.5 & world scenario map | ç©ºé´æ§å¶æ¡æ¶ä¸åºæ¯å°å¾ | å¸¦æçº¿ç¨¿çå¡«è²æ¸¸æä¸æ½å·¥èå¾ | å®ç° Sim2Real è½¬æ¢ï¼ç²¾åæ§å¶ç©ºé´ç»æ |
| åè®­ç» (merging/RL/distillation) | æ¨¡åèåãå¼ºåå­¦ä¹ ä¸è¸é¦ | åç§çäºè¡¥ãåå¸å¾®è°ä¸èåçªå» | æåç»è´¨ãå¯¹é½äººç±»åå¥½ãå éæ¨ç |
æ©å± (å¤è§è§/å¨ä½æ¡ä»¶) | ç¸æºæ§å¶ä¸å¨ä½é©±å¨çæ | å¤æºä½å¯¼æ­ä¸âæçº¿æ¨å¶â | æ¯ææºå¨äººç­ç¥è¯ä¼°ä¸é­ç¯ä»¿ç |

è¿æ ·è¡¨æ ¼å°±æ¶µçäºæææ¦å¿µãç¶åå¨æ­£æä¸­ï¼æéå ä¸ªå¦ flow matching çæ°å­¦ç´è§ãframe-replacement çå¤±æï¼å¹¶ä½¿ç¨ Mermaid å¾è¡¨å±ç¤ºçææµç¨ã

**Mermaid å¾è¡¨è®¾è®¡**ï¼
å±ç¤º Cosmos-Predict2.5 å° Cosmos-Transfer2.5 åå° Physical AI çé­ç¯æµç¨ã
```mermaid
flowchart TD
    subgraph åºç¡ä¸çé¢æµ
        A[å¤æ¨¡ææ¡ä»¶(Cosmos-Predict2.5)
        B --> C["åºç¡è§è§æªæ¥é¢æµ"]
    end
    subgraph ç²¾åç©ºé´æ§å¶
        C --> D{éè¦ä¸¥æ ¼ç©ºé´çº¦æ?}
        D -- æ¯ --> E(Cosmos-Transfer2.5)
        E --> F["åæ§ä¸çç¿»è¯"]
        D -- å¦ --> G["èªç±çæè§é¢"]
    end
   èº«é­ç¯éªè¯
        F --> H["Physical AI ç­ç¥è¯ä¼°"]
        G --> H
        H --> I["æ§è¡å¨å¨ä½åé¦"]
        I --> A
    end
    classDef core fill:#e1f5fe,stroke:#01579b,color:#01579b;
    classDef cond fill:#fff3e0,stroke:#e65100,color:#e65100;
    classDef act fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20;
    class B,E core;
    class A,D cond;
    class H,I act;
```
ï¼æ£æ¥ Mermaid è§èï¼æ  `%%{init}` `style`ï¼åªç¨ `classDef`+`class`ï¼â¤4ä¸ªè¯­ä¹è²ä¸å«æå­ `color:`ï¼snake_case èç¹ idï¼æ ç­¾ 3-6 è¯ï¼è¾¹æ ç­¾ 1-4 è¯ï¼å½¢ç¶ä¸è´ãä¿®æ¹èç¹ id ä¸º snake_caseï¼è°æ´æ ç­¾å­æ°ãï¼

ä¿®æ¹ Mermaid:
```mermaid
flowchart TD
    subgraph åºç¡ä¸çé¢æµé¶æ®µ
        multi_modal_input["å¤"] --> predict_model(Cosmos-Predict2.5)
        predict_model --> base_video["åºç¡è§è§æªæ¥é¢æµ"]
    end
    subgraph ç²¾åç©ºé´æ§å¶é¶æ®µ
        base_video --> check_spatial{éè¦ä¸¥æ ¼ç©ºé´çº¦æ}
        check_spatial -- æ¯ --> transfer_model(Cosmos-Transfer2.5)
        transfer_model --> controlled_video["åæ§ä¸çç¿»è¯è§é¢"]
        check_spatial -- å¦ --> free_video["èªç±çæè§é¢"]
    end
    subé­ç¯éªè¯é¶æ®µ
        controlled_video --> policy_eval["Physical AI ç­ç¥è¯ä¼°"]
        free_video --> policy_eval
        policy_eval --> action_feedback["æ§è¡å¨å¨ä½åé¦"]
        action_feedback --> multi_modal_input
    end
    classDef core fill:#e1f5fe,stroke:#01579b,color:#01579b;
    classDef cond fill:#fff3e0,stroke:#e65100,color:#e65100;
    classDef act fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20;
    class predict_model,transfer_model core;
    class multi_modal_input,check_spatial cond;
    class policy_eval,action_feedback act;
```
è¾¹æ ç­¾ï¼æ¯/å¦ ï¼1è¯ï¼ãèç¹æ ç­¾ï¼å¤(6è¯? ä¸ï¼ä¸­æå­æ°ãå¤ 6ä¸ªå­ãCosmos-Predict2.5 ç®ä¸ä¸ªè¯ãåºç¡è§è§æªæ¥é¢æµ 8ä¸ªå­ãéè¦ä¸¥æ ¼ç©ºé´çº¦æ 8ä¸ªå­ãåæ§ä¸çç¿»è¯è§é¢ 8ä¸ªå­ãPhysical AI ç­ç¥è¯ä¼° 10ä¸ªå­ç¬¦ãæ§è¡å¨å¨ä½åé¦ 7ä¸ªå­ãå°½éç²¾ç®å° 3-6 ä¸ªè¯/å­)ã
è°æ´èç¹æ ç­¾ï¼
multi_modal_input[å¤æ¨¡ææ¡ä»¶6å­) -> æ¹ä¸ºææ¡ä»¶] (6å­)
predict_model(Cosmos-Predict2.5) -> (é¢æµåºç¡ä¸ç) (6å­) å ä¸ºä¸æåè¯ä¸ç¿»è¯ãè§èè¯´âæ ç­¾ 3-6 è¯âï¼ä¸­æå¤§æ¦ 3-6 ä¸ªå­/è¯ã
å°±ç¨ï¼
[å¤æ¨¡ææ¡ä»¶] (5å­)
(Cosmos-Predict2.5) (ä¸æåè¯)
[åºç¡è§è§é¢æµ] (6å­)
{éè¦ç©ºé´çº¦æ} (6å­)
(Cosmos-Transfer2.5)
[åæ§ä¸çç¿»è¯] (6å­)
[èªç±çæè§é¢] (6å­)ç­ç¥è¯ä¼°] (6å­)
[å¨ä½æ§è¡åé¦] (6å­)

**æ­£ææ°å**ï¼
ç»è®ºåç½®ï¼Cosmos å¹¶éåçº¯çâè§é¢çæå¨âï¼èæ¯ä¸º Physical AI æé çâå¯äº¤äºè§è§ä¸çæ¨¡æå¨æ¯éè¿ Cosmos-Predict2.5 æå»ºåºç¡ç©çç´è§ï¼ç¨ Cosmos-Transfer2.5 å®ç°ç²¾åç©ºé´æ§å¶ï¼æç»æå¡äºé­ç¯éªè¯ã

ç¶åå±å¼æ ¸å¿æ¦å¿µçæ·±åº¦è§£è¯»ã
**1. åºç¡ä¸çè§ä¸çæå¼æ**
- **Physical AI & worldèº«ç³»ç»ä¸ä»£çç¯å¢ãç´è§æ¯å»ï¼é©¾æ ¡æç»ä¸æ¨¡æé©¾é©¶è±ãä½ç¨ï¼æä¾ã
- **Cosmos-Predict2.5 & flow flow matching æ¿ä»£ EDMãï¼$$\mathbf { x } _ { t } = ( 1 - t ) \mathbf { x } + t { \boldsymbol { \epsilon } } .\tag{1}$$
  ç´è§ï¼ä»åªå£°å°æ°æ®çâç´çº¿å¯¼èªâã
- **shifted logit-normal distribution**ï¼
   _ { s } = \frac { \beta t } { 1 + ( \beta - 1 ) t }\tag{4}$$
  ç´è§ï¼ââçéæ ·ç­ç¥ï¼ååé«åªå£°åºåï¼è§£å³é«åè¾¨çä¸å¼ºå¯¼è´çå­¦ä¹ å°é¾ã

**2. æ¨¡ææ§å¶**
- **ç»ä¸çææ¨¡å¼ & frame-replacement strategy**ï¼Text2World / Image2World / Video2Worldãframe-replacement å°±åâéä½ç¬¬ä¸é¡µâç»­åå°è¯´ï¼é²æ­¢ç»é¢æ¼ç§»ãå¤±ææ¨¡å¼æéï¼å®çº¦æå¼å¤´ï¼é¿åºåä»å¯è½åæ£ã
- **Cosmos-Transfer2.5 & world scenario map**ï¼control-net style æ¡æ¶ãæ¯å»ï¼å¸¦æçº¿ç¨¿çå¡«è²æ¸¸æãworld scenario map å° HD maps å 3D bounding boxes æå½±ï¼å®ç°èªå¨é©¾é©¶å¤è§è§æ§å¶ã<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C-->

**3. åè®­ç»æ©å±**
- **åè®­ç»ä¸åå®¢ (model merging / RL post-training / timestep distillation)**ï¼
  model merging (å¦ DARE-TIES) åâåç§çäºè¡¥âï¼RL post-training (VideoAlign) åâåå¸å¾®è°âï¼timestep distillation (rCM) åâèåçªå»âå éæ¨çã
- **camera-controllable & action-conditioned)** PlÃ¼cker raymaps åå¨ä½åºåï¼æ¯ææºå¨äººé­ç¯ã

**æ£æ¥æ¥å°è§å**ï¼
- æ ç²¾ç¡®æ§è½æ°å­ï¼æ¯ã
- ä¿çï¼æ¯ã
- ç»æï¼H2 å¸¦ emojiï¼H3 ä¸å¸¦ãç»è®ºåç½®ã
- å¾è¡¨ï¼Mermaid ç¬¦åè§èã
- æå åï¼æ flow matching å shifted logit-normal çæ°å­¦æ¨å¯¼ç»èæ¾è¿ `<details>`ã

**å­æ°æ§å¶**ï¼
å­æ°ç®æ  350-800ãç±äºæ¦å¿µå¤ã
ä½¿ç¨è¡¨æ ¼æ¥åç¼©âæ¯ä»ä¹âåâæ¯å»âï¼æ­£æåªè®²âä½ç¨âåâæºå¶/å¤±ææ¨¡å¼âã

**èç¨¿ç¼æ**ï¼
## ð§  æ ¸å¿æ¦å¿µéè§

**ç»è®ºåç½®**ï¼Cosmos ç³»åå¹¶éåçº¯çâè§é¢çæå¨âï¼èæ¯ä¸º Physical AI æé çâå¯äº¤äºè§è§ä¸çæ¨¡æå¨æ¯éè¿ Cosmos-Predict2.5 æå»ºåºç¡ç©çç´è§ï¼ç¨ Cosmos-Transfer2.5 å®ç°ç²¾åç©ºé´æ§å¶ï¼æç»æå¡äºé­ç¯éªè¯ãè¯»å®æ¬èï¼ä½ å°ææ¡è¿å¥ç³»ç»å¦ä½ä»âèè¡¥æªæ¥âèµ°åâç²¾åæ§ç©âã

### æ å°

| æ ¸å¿æ¦å¿µç° | æ¬è´¨å®ä¹ | ç´è§æ¯å» (éä¸¥æ ¼å¯¹åº) | å¨ç³»ç»ä¸­çæ ¸å¿ä½ç¨ |
|---|---|---|---|
| **Physical AI & world simulator** |ä»£çç¯å¢ | é©¾æ ¡æç»ä¸æ¨¡æé©¾é©¶è± | æºç¢°æ |
| **Cosmos-Predict2.5 & flow matching** | åºç¡ä¸çæ¨¡åä¸çæè½¨è¿¹ | æ¥æç©çå¸¸è¯çâèè¡¥âå¼æ | ç»ä¸å¤æ¨¡æªæ¥è§è§ç¶æ |
| **ç»ä¸çæ & frame-replacement** | å¤æ¨¡ææ¡ä»¶ä¸é¦å¸§éå® | ç»­åå°è¯´ä¸âéä½ç¬¬ä¸é¡µâ | ä¿ææ¶åºä¸è´æ§ï¼é²æ­¢ç»é¢æ¼ç§» |
| **Cosmos-Transfer2.5 & scenario map** | ç©ºé´æ§å¶æ¡æ¶ä¸åºæ¯å°å¾ | å¸¦çº¿ç¨¿å¡«è²ä¸æ½å·¥èå¾ | å®ç° Sim2Realï¼ç²¾åæ§å¶ç©ºé´ç»æ |
| **åè®­ç» (merging/RL/distillation)** | æ¨¡åèåãå¼ºåå­¦ä¹ ä¸è¸é¦ | åç§çäºè¡¥ãåå¸å¾®è°ä¸èåçªå» | æåç»è´¨ãå¯¹é½åå¥½ãå éæ¨ç |èº«æ©å± (å¤è§è§/å¨ä½æ¡ä»¶)** | ç¸æºæ§å¶ä¸å¨ä½é©±å¨çæ | å¤æºä½å¯¼æ­ä¸âæçº¿æ¨å¶â | æ¯ææºå¨äººç­ç¥è¯ä¼°ä¸é­ç¯ä»¿ç |

### çæå¼æä¸æ§å¶æºå¶æ·±åº¦è§£æ

**åºç¡é¢æµä¸éæ ·åç§»**
Cosmos-Predict2.5 æå¼äºåä»£ç EDMï¼è½¬å flow matchingãç´è§ä¸ï¼è¿æ¯ä»âæ²ææ¢è·¯âåä¸ºâç´çº¿å¯¼èªâãä¸ºäºç¼è§£é«åè¾¨çè¿å¼ºå¸¦æ¥çå­¦ä¹ å°é¾ï¼è®ºæ-normal distributionï¼å°éæ ·ååé«åªå£°åºåï¼å³å¤§æ¾å°âï¼ã
<details><summary><strong>æ°å­¦ç»èï¼flow matching ä¸ timestep åç§»</strong></summary>
flow matching è®©å»åªç½ç»é¢æµ velocity èéç´æ¥é¢æµæ°æ®ï¼
$$\mathbf { x } _ { t } = ( 1 - t ) \mathbf { x } + t { \boldsymbol { \epsilon } } .\tag{1}$$
$$\mathbf { v } _ { t } = \epsilon - \mathbf { x } .\tag{2}$$
$$\begin{array} { r } { \mathcal { L } ( \boldsymbol { \theta } ) = \mathbb { E } _ { \mathbf { x } , \boldsymbol { \epsilon } , \mathbf { c } , t } \left\| \mathbf { u } ( \mathbf { x } _ { t } , t , \mathbf { c } ; \boldsymbol { \theta } ) - \mathbf { v } _ { t } \right\| ^ { 2 } , } \end{array}\tag{3}$$
shifted logit-normal éè¿åè°åæ¢è°æ´ timestepï¼
$$t _ { s } = \frac { \beta t } { 1 + ( \beta - 1 ) t }\tag{4}$$
æ³¨æï¼è¿åªæ¯è®­ç»éæ ·ç­ç¥ï¼ä¸æ¹åç½ç»å±ç»æã
</details>

**æ¡ä»¶æ§å¶**
å¨ Image2World å Video2World ä¸­ï¼frame-replacement strategy éè¿ç¨³å®æ¿æ¢åå§å¸§æ¥éå®è§è§çº¿ç´¢ã**å¤±ææ¨¡å¼æé**çº¦æåºåå¼å¤´ï¼é¿åºåçæä»å¯è½å è¯¯å·®ç´¯ç§¯èåæ£ï¼è½å®ç¾è§£å³é¿ç¨ç©çä¸è´æ§ã
å¯¹äºä¸¥æ ¼çç©ºé´çº¦æï¼Cosmos-Transfer2.5 éç¨ control-net style æ¶æãå¨èªå¨é©¾é©¶åºæ¯ä¸­ï¼world scenario map å° HD maps åå¨æ 3D bounding boxes æå½±å°å¤ç¸æºè§å¾ï¼å®ç°ç²¾åç Sim2Real ç¿»è¯ã<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C-->

```mermaid
flowchart TD
    subgraph åºç¡ä¸çé¢æµé¶æ®µ
        multi_modal_cond["å¤æ¨¡ææ¡ä»¶"] --> predict_model(Cosmos-Predict2.5)
        predict_model --> base_video["åºç¡è§è§é¢æµ"]
    end
    subgraph ç²¾åç©ºé´æ§å¶é¶æ®µ
        base_video --> check_spatial{éè¦ç©ºé´çº¦æ}
        check_spatial -- æ¯ --> transfer_model(Cosmos-Transfer2.5)
        transfer_model --> controlled_video["åæ§ä¸çç¿»è¯"]
        check_spatial -- å¦ --> free_video["èªç±çæè§é¢"]
    end
   èº«é­ç¯éªè¯é¶æ®µ
        controlled_video --> policy_eval[]
        free_video --> policy_eval
        policy_eval --> action_feedback["å¨ä½æ§è¡åé¦"]
        action_feedback --> multi_modal_cond
    end
    classDef core fill:#e1f5fe,stroke:#01579b,color:#01579b;
    classDef cond fill:#fff3e0,stroke:#e65100,color:#e65100;
    classDef act fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20;
    class predict_model,transfer_model core;
    class multi_modal_cond,check_spatial cond;
    class policy_eval,action_feedback act;
```
*å¦ä½è¯»è¿å¼ å¾ï¼ä¸»æµç¨ä»å·¦ä¸å°å³ä¸ï¼å±ç¤ºäºä»èªç±é¢æµå°åæ§ç¿»è¯ï¼æç»é­ç¯å° Physical AI å¨ä½åé¦çå®æ´æ°æ®æµãè±å½¢å¤å®é¨å³å®äºæ§å¶åæ¯ã*

**åæ©å±**
åè®­ç»é¶æ®µï¼model merging (å¦ DARE-TIES) åå¹¶ domain-specific SFTæ¯ä¾å¤±è¡¡ï¼RL post-training å©ç¨ VideoAlign å¥å±æ¨¡åä¼å denoising trajectoriesï¼timestep distillation (rCM) æ­¥æ°ãæ¹é¢Ã¼cker raymaps å®ç° camera-controllable multi-view generationï¼å¹¶ç»å action embedder MLP å®æ action-conditioned world generationï¼å½»åºæéäºä»âçâå°âå¨âçé­ç¯ã

**æ£æ¥ææçº¦æ**ï¼
- ä¸­æï¼ï¼æ¯ã
- å¿ å®ï¼åªç¨ç»å®äºå®ï¼æ ç¼é ãä¸æåè¯åæ ·ä¿çã
- ç²¾ç¡®æ§è½æ°å­ãå®æ§æè¿°ï¼å¦ãâæåç»è´¨âï¼ã
çèµ·æ¥å¨ 800 å­å·¦å³ã
- ç»æï¼H2 å¸¦ emojiï¼H3 ä¸å¸¦ãç»è®ºåç½®ã
- å¾è¡¨ï¼Mermaid ç¬¦åè§èï¼æâå¦ä½è¯»è¿å¼ å¾âã
- è¡¨æ ¼ï¼æç²¾ç¼ã
- æå åï¼æ°å­¦ç»èã

å­æ°ç»è®¡ï¼å¤§æ¦ 700 å­ï¼å®ç¾ç¬¦å 350-800 çè¦æ±ã
æ£æ¥ Mermaid èç¹æ ç­¾å­æ°ï¼
multi_modal_cond[å¤æ¨¡ææ¡ä»¶] (5å­)
predict_model(Cosmos-Predict2.5) (ä¸æåè¯)
base_video[åºç¡è§è§é¢æµ] (6å­)
check_spatial{éè¦ç©ºé´çº¦æ} (6å­)
transfer_model(Cosmos-Transfer2.5)
controlled_video[åæ§ä¸çç¿»è¯] (6å­)
free_video[èªç±çæè§é¢] (6å­)
èº«ç­ç¥è¯ä¼°] (6å­)
action_feedback[å¨ä½æ§è¡åé¦] (7å­) -> æ¹ä¸º [å¨ä½æ§è¡åé¦] (6å­) æ [æ§è¡å¨ä½åé¦] (6å­)ãç¨ [å¨ä½æ§è¡åé¦] æ²¡é®é¢ï¼ä¸­æç® 6 ä¸ªå­ç¬¦ãè§èè¯´ 3-6 è¯ï¼ä¸­æéå¸¸æ 3-6 ä¸ªå­/è¯ã
è¾¹æ ç­¾ï¼æ¯/å¦ (1è¯)ã

å®ç¾ãç´æ¥è¾åºã## ð§  æ ¸å¿æ¦å¿µéè§

**ç»è®ºåç½®**ï¼Cosmos ç³»åå¹¶éåçº¯çâè§é¢çæå¨âï¼èæ¯ä¸º Physical AI æé çâå¯äº¤äºè§è§ä¸çæ¨¡æå¨âã Cosmos-Predict2.5 æå»ºåºç¡ç©çç´è§ï¼ç¨ Cosmos-Transfer2.5 å®ç°ç²¾åç©ºé´æ§å¶èº«æºè½çé­ç¯éªè¯ãè¯»å®æ¬èï¼ä½ å°ææ¡è¿å¥ç³»ç»å¦ä½ä»âèè¡¥æªæ¥âèµ°åâç²¾åæ§ç©âã

###ç´è§æ å°

| æ ¸å¿æ¦å¿µç° | æ¬è´¨å®ä¹ | ç´è§æ¯å» (éä¸¥æ ¼å¯¹åº) | å¨ç³»ç»ä¸­çæ ¸å¿ä½ç¨ |
|---|---|---|---|
| **Physical AI & world simulator** |ä»£çç¯å¢ | é©¾æ ¡æç»ä¸æ¨¡æé©¾é©¶è± | æºç¢°æ |
| **Cosmos-Predict2.5 & flow matching** | åºç¡ä¸çæ¨¡åä¸çæè½¨è¿¹ | æ¥æç©çå¸¸è¯çâèè¡¥âå¼æ | ç»ä¸å¤é¢æµæªæ¥è§è§ç¶æ |
| **ç»ä¸çæ & frame-replacement** | å¤æ¨¡ææ¡ä»¶ä¸é¦å¸§éå® | ç»­åå°è¯´ä¸âéä½ç¬¬ä¸é¡µâ | ä¿ææ¶åºä¸è´æ§ï¼é²æ­¢ç»é¢æ¼ç§» |
| **Cosmos-Transfer2.5 & scenario map** | ç©ºé´æ§å¶æ¡æ¶ä¸åºæ¯å°å¾ | å¸¦çº¿ç¨¿å¡«è²ä¸æ½å·¥èå¾ | å®ç° Sim2Realï¼ç²¾åæ§å¶ç©ºé´ç»æ |
| **åè®­ç» (merging/RL/distillation)** | æ¨¡åèåãå¼ºåå­¦ä¹ ä¸è¸é¦ | åç§çäºè¡¥ãåå¸å¾®è°ä¸èåçªå» | æåç»è´¨ãå¯¹é½åå¥½ãå éæ¨ç |èº«æ©å± (å¤è§è§/å¨ä½æ¡ä»¶)** | ç¸æºæ§å¶ä¸å¨ä½é©±å¨çæ | å¤æºä½å¯¼æ­ä¸âæçº¿æ¨å¶â | æ¯ææºå¨äººç­ç¥è¯ä¼°ä¸é­ç¯ä»¿ç |

### çæå¼æä¸æ§å¶æºå¶æ·±åº¦è§£æ

**åºç¡é¢æµä¸éæ ·åç§»**
Cosmos-Predict2.5 æå¼äºåä»£ç EDMï¼è½¬å flow matchingãç´è§ä¸ï¼è¿æ¯ä»âæ²ææ¢è·¯âåä¸ºâç´çº¿å¯¼èªâãä¸ºäºç¼è§£é«åè¾¨çè¿å¼ºå¸¦æ¥çå­¦ä¹  shifted logit-normal distributionï¼å°éæ ·ååé«åªå£°åºåæå¤§æ¾å°âï¼ã

<details><summary><strong>æ°å­¦ç»èï¼flow matching ä¸ timestep åç§»</strong></summary>
flow matching è®©å»åªç½ç»é¢æµ velocity èéç´æ¥é¢æµæ°æ®ï¼
$$\mathbf { x } _ { t } = ( 1 - t ) \mathbf { x } + t { \boldsymbol { \epsilon } } .\tag{1}$$
$$\mathbf { v } _ { t } = \epsilon - \mathbf { x } .\tag{2}$$
$$\begin{array} { r } { \mathcal { L } ( \boldsymbol { \theta } ) = \mathbb { E } _ { \mathbf { x } , \boldsymbol { \epsilon } , \mathbf { c } , t } \left\| \mathbf { u } ( \mathbf { x } _ { t } , t , \mathbf { c } ; \boldsymbol { \theta } ) - \mathbf { v } _ { t } \right\| ^ { 2 } , } \end{array}\tag{3}$$
shifted logit-normal éè¿åè°åæ¢è°æ´ timestepï¼
$$t _ { s } = \frac { \beta t } { 1 + ( \beta - 1 ) t }\tag{4}$$
æ³¨æï¼è¿åªæ¯è®­ç»éæ ·ç­ç¥ï¼ä¸æ¹åç½ç»å±ç»æï¼ä¹ä¸æ¶åæ¨çæ¶çæ§å¶åæ¯æéã
</details>

**æ§å¶**
å¨ Image2World å Video2World ä¸­ï¼frame-replacement strategy éè¿ç¨³å®æ¿æ¢åå§å¸§æ¥éå®è§è§çº¿ç´¢ã**å¤±ææ¨¡å¼æé**ï¼åºåå¼å¤´ï¼é¿åºåçæä»å¯è½å è¯¯å·®ç´¯ç§¯èåæ£ï¼è®ºæå¹¶æªè§£å³é¿ç¨ç©çä¸è´æ§ãå¯¹äºä¸¥æ ¼çç©ºé´çº¦æï¼Cosmos-Transfer2.5 éç¨ control-net style æ¶æãå¨èªå¨é©¾é©¶åºæ¯ä¸­ï¼world scenario map å° HD maps åå¨æ 3D bounding boxes æå½±å°å¤ç¸æºè§å¾ï¼å®ç°ç²¾åç Sim2Real ç¿»è¯ã<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C-->

```mermaid
flowchart TD
    subgraph åºç¡ä¸çé¢æµé¶æ®µ
        multi_modal_cond["å¤æ¨¡ææ¡ä»¶"] --> predict_model(Cosmos-Predict2.5)
        predict_model --> base_video["åºç¡è§è§é¢æµ"]
    end
    subgraph ç²¾åç©ºé´æ§å¶é¶æ®µ
        base_video --> check_spatial{éè¦ç©ºé´çº¦æ}
        check_spatial -- æ¯ --> transfer_model(Cosmos-Transfer2.5)
        transfer_model --> controlled_video["åæ§ä¸çç¿»è¯"]
        check_spatial -- å¦ --> free_video["èªç±çæè§é¢"]
    end
   èº«é­ç¯éªè¯é¶æ®µ
        controlled_video --> policy_eval[]
        free_video --> policy_eval
        policy_eval --> action_feedback["å¨ä½æ§è¡åé¦"]
        action_feedback --> multi_modal_cond
    end
    classDef core fill:#e1f5fe,stroke:#01579b,color:#01579b;
    classDef cond fill:#fff3e0,stroke:#e65100,color:#e65100;
    classDef act fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20;
    class predict_model,transfer_model core;
    class multi_modal_cond,check_spatial cond;
    class policy_eval,action_feedback act;
```
*å¦ä½è¯»è¿å¼ å¾ï¼ä¸»æµç¨ä»å·¦ä¸å°å³ä¸ï¼å±ç¤ºäºä»èªç±é¢æµå°åæ§ç¿»è¯ï¼æç»é­ç¯å° Physical AI å¨ä½åé¦çå®æ´æ°æ®æµãè±å½¢å¤å®é¨å³å®äºæ¯å¦éè¦åæ¯ã*

**åè®­ç»ä¸
åè®­ç»é¶æ®µï¼model merging (å¦ DARE-TIES) åå¹¶ domain-specific SFTæ¯ä¾å¤±è¡¡ï¼RL post-training å©ç¨ VideoAlign å¥å±æ¨¡åä¼å denoising trajectoriesï¼timestep distillation (rCM) æ­¥æ°ãå¨Ã¼cker raymaps å®ç° camera-controllable multi-view generationï¼å¹¶ç»å action embedder MLP å®æ action-conditioned world generationï¼å½»åºæéäºä»âçâå°âå¨âçé­ç¯éªè¯ã

ç¨æ·è¦æ±æ°åä¸ç¯æ·±åº¦ç§æ®è§£è¯»æ¥åä¸­çä¸èï¼ä¸»é¢æ¯âæ¹æ³ä¸æ´ä½æ¶æâã
éè¦éµå¾ªä¸¥æ ¼çåä½è§èï¼
1. **ç»æ**ï¼ç»è®ºåç½®ï¼åå±å¼ãå°èä»¥ `## æ é¢` å¼å¤´ï¼H2 å¥é¦å¯å¸¦ emojiã
2. **å¿ å®ä¸ä¸¥è°¨**ï¼åºåâå£°ç§°âä¸âè¯æâï¼ç¹åå¤±ææ¨¡å¼ï¼å¦è¿åº¦å®£ç§°ç­ï¼ï¼è¯´ææ¯å¦æ¥åæ¶è/è´ç»æã
3. **æ¥å°**ï¼åè¿°å¥å­ä¸­**ç»å¯¹ä¸è½**åºç°ç²¾ç¡®æ§è½æ°å­ï¼å¦ 8.54, 12% ç­ï¼ï¼åªè½ç¨å®æ§è¯­è¨ãç²¾ç¡®æ°å¼åªè½åºç°å¨è¯æ®è¡¨ææ ¸å¿ç»è®ºåï¼ç³»ç»èªå¨å¤çï¼æä¸éè¦åï¼ãéæ§è½æ°å­ï¼å¦ 2B, 7B, 720p ç­ï¼å¯ä»¥åãä¸æåè¯ååæ ·ã<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-table-tr-td-confi-gur--><!--anchor:quote:%3Ctable%3E%3Ctr%3E%3Ctd%3EConfi%20guration%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D2B%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D14B%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Layers%3C%2Ftd%3E%3Ctd%3E32%3C%2Ftd%3E%3Ctd%3E36%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EModel%20Dimension%3C%2Ftd%3E%3Ctd%3E2%2C048%3C%2Ftd%3E%3Ctd%3E5%2C120%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EFFN%20Hidden%20Dimension%3C%2Ftd%3E%3Ctd%3E8%2C192%3C%2Ftd%3E%3Ctd%3E20%2C480%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EAdaLN%2DLoRA%20Dimension%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Attention%20Heads%3C%2Ftd%3E%3Ctd%3E16%3C%2Ftd%3E%3Ctd%3E40%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EHead%20Dimension%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EMLP%20Activation%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3EGELU%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EPositional%20Embedding%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3E3D%20RoPE%3C%2Ftd%3E%3C%2Ftr%3E%3C%2Ftable%3E--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-2-2-2-autonomous-drivi--><!--anchor:quote:2.2.2%20Autonomous%20Driving%207--><!--ref:r-we-describe-the-multi--><!--anchor:quote:We%20describe%20the%20multi%2Dstage%20pretraining%20procedure%20in%20Tab.%204.%20Training%20begins%20with%20the%20Text2Image%20task%20at%20a%20resolution%20of%20256p.-->
4. **å¾è¡¨ä¸ä¸ª Mermaid flowchart (TB)ï¼åæ çå® pipelineï¼èç¹ç¨çå®ç»ä»¶åãå¾åè¡¥ä¸å¥âå¦ä½è¯»è¿å¼ å¾âãMerï¼ç¦ç¨ `%%{init}` style`ï¼åªç¨ `classDef`+`class`ï¼â¤4ä¸ªè¯­ä¹è²ï¼snake_case èç¹ idï¼æ ç­¾ 3-6 è¯ï¼è¾¹æ ç­¾ 1-4 è¯ãé¦èç¹ `class required`ï¼æ«èç¹ `class output`ã
5. **è¡¨æ ¼ vs åè¿°**ï¼ç»æåå¯¹æ¯ç¨è¡¨ï¼è¿éå¯è½ç¨è¡¨å±ç¤ºæ¨¡åã
6. **æ·±åº¦èè¿æå å**ï¼åé¿æ¨å¯¼ãdetails>` æå ã
7. **ç¡¬çº¦æ**ï¼ï¼æ°å½æ¯å»ãåªç¨æä¾çäºå®æºãä¸ç¼é ãä¸åç²¾ç¡®æ§è½350-800 å­ãåªè¾åºæ¬èæ­£æï¼ä»¥ `## æ¹æ³ä¸æ´ä½æ¶æ` å¼å¤´ï¼å¯ä»¥å  emojiï¼å¦ `## ðï¸ æ¹æ³ä¸æ´ä½æ¶æ`ï¼ä½é¢ç®è¦æ±ä»¥ "## æ¹æ³ä¸æ´ä½æ¶æ" å¼å¤´ï¼ä¸ºäº## æ¹æ³ä¸æ´ä½æ¶æ` ðï¸ æ¹æ³ä¸æ´ä½æ¶æ`ï¼è§èè¯´âH2 å¥é¦å¯å¸¦ä¸ä¸ª emojiâï¼é£æå°±ç¨ `## ðï¸ æ¹æ³ä¸æ´ä½æ¶æ`ï¼ `## æ¹æ³ä¸æ´ä½æ¶æ`ãä¸ºäºç¨³å¦¥ï¼éµå¾ªâä»¥ "## æ¹æ³ä¸æ´ä½æ¶æ" å¼å¤´âï¼æç´æ¥å `## æ¹æ³ä¸æ´ä½æ¶æ`ï¼ä¸å  emoji æ¾å¨åé¢ãè§èè¯´âä»¥ "## æ¹æ³ä¸æ´ä½æ¶æ" å¼å¤´âï¼é£æå°±ä¸¥æ ¼ç¨è¿ä¸ªå­ç¬¦ä¸²ï¼ã

åæäºå®æºï¼
- **æ°æ®ä¾§**ï¼shot-aware video splitting -> GPU-based transcoding -> video cropping -> å¤é¶æ®µ filtering -> captioning -> semantic deduplication -> shardingã
- **æ¨¡åä¾§**ï¼å¾å/è§é¢ç» WAN2.1 VAE ç¼ç å° latentï¼patchificationï¼ææ¬ç± Cosmos-Reason1 ç¼ç ï¼è·¨ blocks æ¼æ¥ token æ¿æ´»æå½±ä¸º text embeddingï¼DiT velocity prediction network å¨ latent ç©ºé´äº¤æ¿ä½¿ç¨ self-attention, cross-attention, feed-forward MLPï¼ç± timestep ç adaptive layer normalization è°å¶ã
- **ä»»å¡æ¯æ**ï¼Cosmos-Predict2.5 æ¯æ Text2World, Image2World, Video2Worldãåplacement ä¿ææ¡ä»¶å¸§ã
- **è®­ç»æµç¨**ï¼progressive pre-training -> domain-specific SFT -> cooldown -> model merging -> RL post-training -> timestep distillationã
- **åºç¨æ©å±**ï¼Cosmos-Transfer2.5 control-net style åæ¯ãå¤è§è§ world scenario mapãcamera trajectoryãaction embedder MLPã
- **ç®æ³Flow matching velocity prediction2,3)ï¼shifted logit-normal)ï¼5)ã


1. **ç»è®ºåç½®**ï¼Cosmos çæ´ä½æ¶ææ¯ä¸ä¸ªä»å¤é¶æ®µæ¸è¿è®­ç»ãåå°å¤ç»´åº¦æ¡ä»¶æ§å¶çç»ä¸æµï¼Flow Matchingï¼çæç®¡çº¿å¨äºéè¿ç»ä¸ç DiT éª¨å¹²å frame-replacement æºå¶ãå¾åãè§é¢ä¹è³æºå¨äººå¨ä½ç­å¤æ¨¡æä¼ ç»å¤ä»»å¡æ¨¡åå¨ä¸çå²è£çç¹ã
2. **æ°æ®ä¸ç¹å¾ç¼ç **ï¼ç®è¿°æ°æ® pipeline å VAE/Text ç¼ç ã
3. **æ ¸å¿çæç½ç» (DiT)**ï¼è®²è§£ DiT velocity prediction networkï¼ä»¥å flow matching ç®æ 
4ä¸å¤ä»»å¡ç»ä¸**ï¼è®²è§£ frame-replacementï¼ä»¥å Cosmos-Transfer2.5 å action embedderã
5. **è®­ç» Pipeline**ï¼æ¸è¿å¼é¢è®­ç»å° RL åè®­ç»ã
6. **Mermaid æµç¨å¾**ï¼ç»åºæ´ä¸ª pipelineã
7. **æå å ç»èã

æ£æ¥çº¦æï¼
- æ²¡æç²¾ç¡®æ§è½æ°å­ã
- ä¸æåè¯ä¸ç¿»è¯ï¼WAN2.1 VAE, Cosmos-Reason1, DiT, Text2World, Image2World, Video2World, frame-replacement, Cosmos-Predict2.5, Cosmos-Transfer2.5, VideoAlign, GRPO, model soup, TIES, DARE-Linear, DARE-TIES, RNDS, DOVERã
-æ ·ï¼$$...$$ã
- Mermaid è§èï¼flowchart TBï¼èç¹ snake_caseï¼æ ç­¾ 3-6 è¯ï¼è¾¹ 1-4 è¯ãé¦å°¾èç¹ classã

èæ Mermaid å¾ï¼
```mermaid
flowchart TB
    data_pipeline["å¤é¶æ®µè§é¢ç"] --> vae_encode["WAN2.1 VAE æ½å¨ç©ºé´ç¼ç "]
    text_encode["Cosmos-Reason1 ææ¬ç¹å¾æå"] --> dit_core
    vae_encode --> dit_core["DiT éåº¦é¢æµæ ¸å¿ç½ç»"]
    cond_frames[æ¡ä»¶å¸§æ¿æ¢ä¸å¤æ¨¡æ --> dit_core
    dit_core --> pretrain["æ¸è¿å¼å¤ä»»å¡é¢è®­ç»"]
    pretrain --> sft_merge["ä¸åå¾®è°ä¸æ¨¡ååå¹¶"]
    sft_merge --> rl_post["VideoAlign å¼ºåå­¦ä¹ åè®­ç»"]
    rl_post --> final_output["ç»ä¸ä¸çæ¨¡åçæè¾åº"]

    class data_pipeline required
    class final_output output
```
è°æ´èç¹æ ç­¾å­æ°ï¼3-6è¯ï¼ï¼
`data_pipeline` -> "å¤é¶æ®µè§é¢æ°æ®ç" (10 chars, maybe count as words? "å¤é¶æ®µ è§é¢ æ°æ® " 5 words). Let's use simpler: "è§é¢æ°æ®ç" (4 words).
`vae_encode` -> "æ½å¨ç©ºé´ç¹å¾ç¼ç " (4 words).
`text_encode` -> "ææ¬è¯­ä¹ç¹å¾æå" (4 words).
`dit_core` -> "éåº¦é¢æµæ ¸å¿ç½ç»" (4 words).
`cond_frames` -> "æ¡ä»¶" (4 words).
`pretrain` -> "æ¸è¿å¼å¤ä»»å¡é¢è®­ç»" (5 words).
`sft_merge` -> "ä¸åå¾®è°ä¸æ¨¡ååå¹¶" (5 words).
`rl_post` -> "å¼ºåå­¦ä¹ å¯¹é½åè®­ç»" (5 words).
`final_output` -> "ç»ä¸ä¸çæ¨¡åçæ" (4 words).

è¾¹æ ç­¾ï¼1-4è¯ï¼ï¼
data_pipeline -->| vae_encode
text_encode -->|è·¨åæ¼æ¥| dit_core
vae_encode -->|ååæ å°| dit_core
cond_frames -->|å¸§çº§æ¿æ¢| dit_core
dit_core --> pretrain
pretrain -->|æ¶æåæ¢| sft_merge
sft_merge -->|ä¼å¿èå| rl_post
rl_post -->|è½¨è¿¹ä¼å| final_output

æ£æ¥ Mermaid è¯­æ³å classDefï¼
```mermaid
flowchart TB
    data_pipeline["åç"] -->| vae_encode["æ½å¨ç©ºé´ç¹å¾ç¼ç "]
    text_encode["ææ¬è¯­ä¹ç¹å¾æå"] -->|è·¨åæ¼æ¥| dit_core["éåº¦é¢æµæ ¸å¿ç½ç»"]
    vae_encode -->|ååæ å°| dit_core
    cond_frames[æ¡ä»¶å¸§ -->|å¸§çº§æ¿æ¢| dit_core
    dit_core| pretrain["æ¸è¿å¼å¤ä»»å¡é¢è®­ç»"]
    pretrain -->|æ¶æåæ¢| sft_merge["ä¸åå¾®è°ä¸æ¨¡ååå¹¶"]
    sft_merge -->|ä¼å¿èå| rl_post["å¼ºåå­¦ä¹ å¯¹é½åè®­ç»"]
    rl_post -->|è½¨è¿¹ä¼å| final_output["ç»ä¸ä¸çæ¨¡åçæ"]

    classDef required fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#1e3a5f
    classDef output fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d
    classDef optional fill:#fef9c3,stroke:#ca8a04,stroke-width:2px,color:#713f12
    
    class data_pipeline required
    class final_output output
```

æ°åæ­£æï¼
ç»è®ºåç½®ï¼Cosmos çæ´ä½æ¶ææ¯ä¸ä¸ªå°å¤é¶æ®µæ¸è¿è®­ç»ãåå°å¤ç»´åº¦æ¡ä»¶æ§å¶çç»ä¸æµï¼çæç®¡çº¿ãæ¯ï¼éè¿ç»ä¸ç DiT éª¨å¹²å frame-replacement æºå¶ï¼æ¨¡åè½2WorldãImage2World å Video2World ç­å¤æ¨¡æä»»å¡ï¼ææè§£å³äºä¼ ç»å¤ä»»å¡åæ¶é´ä¸è´æ§ä¸çå²è£çç¹ã

æ°æ®ä¸ç¹å¾ç¼ç ï¼
æ°æ®ä¾§ç»è¿ shot-aware video splittingãGPU-based transcodingãå¤é¶æ®µ filtering å semantic deduplication ç­ä¸¥å¯å·¥åºï¼å½¢æé«è´¨éè§é¢åçãæ¨¡åä¾§ï¼è§è§æ°æ®ç» WAN2.1 VAE ç¼ç è³ latent ç©ºé´å¹¶è¿è¡ patchificationï¼ææ¬æ¡ä»¶åç± Cosmos-Reason1 ç¼ç ï¼è·¨å¤ä¸ª blocks æ¼æ¥ token æ¿æ´»å¹¶æå½±ä¸º text embeddingã

æ ¸å¿ï¼
æ ¸å¿çæä¾èµ DiT velocity prediction networkï¼å¨ latent ç©ºé´äº¤æ¿ä½¿ç¨ self-attentionãcross-attention å feed-forward MLPï¼å¹¶ç± timestep ç adaptive layer normalization è°å¶ãå¯¹äº Image2World å Video2Worldï¼è®ºæéç¨ frame-replacement ç­ç¥ï¼å°çæåºååå§ frames æç»­æ¿æ¢ä¸ºæ¡ä»¶ framesãè¿ç§ç´è§ä¸ç±»ä¼¼âéå®èµ·ç¹âçåæ³ï¼æ¢å¸§æ°éï¼åç¡®ä¿äºæ©æå¸§å¢å¼ºäºæ¶é´ä¸è´æ§ï¼è®ºææªæ¥åæ¡ä»¶å¸§æ°éçéç¨æä¼ç¹ï¼éæä»»å¡è°æ´ï¼ãæ­¤å¤ï¼Cosmos-Transfer2.5 å° control blocks æ´ååå° action-conditioned çæ¬åå° action embedder MLP è¾åºå å° DiT timestamp embeddingsï¼æ¶èå®éªè¯æè¿ä¼äº cross-attention æ channel concatenationã

è®­ç»ä¸å¯¹é½æµç¨ï¼
è®­ç»éµå¾ªä¸¥æ ¼çæ¸è¿è·¯çº¿Image æåºç¡ï¼åèåå¾åä¸è§é¢ä»»å¡ï¼æåãéåè¿è¡ domain-specific SFTï¼å¹¶éè¿ model mergingï¼æç»éæ© model soupï¼ç»ä¸ä¸åä¼å¿ãæåï¼RL post-training å°æ¡ä»¶è§ä½ statesãdenoising trajectories è§ä½ actionsï¼å©ç¨ VideoAlign è®¡ç® reward å¹¶å¨ç» diffusion loss regularization ç¼è§£ reward hackingã

å¦ä½è¯»è¿å¼ å¾ï¼åºåï¼è§è§ä¸ææ¬ç¹å¾å¨ DiT æ ¸å¿ç½ç»ä¸­äº¤æ±ï¼æ¡ä»¶å¸§æ¿æ¢æºå¶ç¡®ä¿äºå¤æ¨¡ä¾æ¬¡ç»åé¢è®­ç»ãå¾®è°åå¹¶ä¸å¼ºåå­¦ä¹ åè®­ç»ï¼æç»è¾åºæ§çä¸çæ¨¡åçæç»æã

æå åï¼
<details>
<summary><strong>ä¸å¼ºåå­¦ä¹ ç»è</strong></summary>
è®­ç»æçæ¾å¼ç®æ æ¯ flow matching velocity predictionï¼å¦ä¸ï¼
$$
\mathbf { x } _ { t } = ( 1 - t ) \mathbf { x } + t { \boldsymbol { \epsilon } } .\tag{1}
$$
$$
\mathbf { v } _ { t } = \epsilon - \mathbf { x } .\tag{2}
$$
$$
\begin{array} { r } { \mathcal { L } ( \boldsymbol { \theta } ) = \mathbb { E } _ { \mathbf { x } , \boldsymbol { \epsilon } , \mathbf { c } , t } \left\| \mathbf { u } ( \mathbf { x } _ { t } , t , \mathbf { c } ; \boldsymbol { \theta } ) - \mathbf { v } _ { t } \right\| ^ { 2 } , } \end{array}\tag{3}
$$
ä¸ºè¦çé«åªå£°åºåï¼éç¨ shifted logit-normal timestep åæ¢ï¼
$$
t _ { s } = \frac { \beta t } { 1 + ( \beta - 1 ) t }\tag{4}
$$
RL é¶æ®µç±äº GPU memory constraintï¼å° trajectory probability åè§£ä¸ºæ¯æ­¥ conditional probabilities å¹¶åæ®µç´¯ç§¯æ¢¯åº¦ãæ¨çæçé¿è§é¢è¯ä¼°ææ  RNDS å®ä¹ä¸ºï¼
$$
\mathsf { R N D S } [ i ] = \left( \frac { \mathrm { D O V E R } [ i ] } { \mathrm { D O V E R } _ { \mathrm { G T } } [ i ] } \right) / \left( \frac { \mathrm { D O V E R } [ 1 ] } { \mathrm { D O V E R } _ { \mathrm { G T } } [ 1 ] } \right) ,\tag{5}
$$
</details>

æ£æ¥å­æ°ï¼çº¦ 700 å­ï¼ç¬¦å 350-800 å­è¦æ±ã
æ£æ¥æ¥å°ï¼æ²¡æç²¾ç¡®æ§è½æ°å­ã
æ£æ¥ä¸æåè¯ï¼æ£æ¥ Mermaidï¼ç¬¦åææè§èã
æ£æ¥ç»æï¼ç»è®ºåç½®ï¼H2 å¼å¤´ã

å¾®è°è¯­è¨ï¼
âè¿ç§ç´è§ä¸ç±»ä¼¼âéå®èµ·ç¹âçåæ³â -> âè¿ç§ç´è§ä¸ç±»ä¼¼âéå®èµ·ç¹âçåæ³ï¼ç´è§ï¼éä¸¥æ ¼å¯¹åºï¼â
ç¡®ä¿æ²¡æéæ¼ä»»å¡è¦æ±ã
âä»¥ "## æ¹æ³ä¸æ´ä½æ¶æ" å¼å¤´â -> ä¸¥æ ¼éµå®ã

æç»æ£æ¥ Mermaid èç¹åè¾¹ï¼
èç¹ id é½æ¯ snake_caseã
æ ç­¾å­æ°ï¼
è§é¢ç (8 chars, ~4 words)
æ½å¨ç©ºé´ç¹å¾ç¼ç  (8 chars, ~4 words)
ææ¬è¯­ä¹ç¹å¾æå (8 chars, ~4 words)
éåº¦é¢æµæ ¸å¿ç½ç» (8 chars, ~4 words)
æ¡ä»¶ (8 chars, ~4 words)
æ¸è¿å¼å¤ä»»å¡é¢è®­ç» (9 chars, ~5 words)
ä¸åå¾®è°ä¸æ¨¡ååå¹¶ (9 chars, ~5 words)
å¼ºåå­¦ä¹ å¯¹é½åè®­ç» (9 chars, ~5 words)
ç»ä¸ä¸çæ¨¡åçæ (8 chars, ~4 words)
è¾¹æ ç­¾é (4 chars)
è·¨åæ¼æ¥ (4 chars)
ååæ å° (4 chars)
å¸§çº§æ¿æ¢ (4 chars)
æµ chars)
æ¶æåæ¢ (4 chars)
ä¼å¿èå (4 chars)
è½¨è¿¹ä¼å (4 chars)
å®ç¾ã

æ£æ¥ï¼\tag{1} ç­ä¿çåæ ·ã
æ£æ¥ `<details>` æ ç­¾ï¼æ­£ç¡®ã

åå¤è¾åºã## æ¹æ³ä¸æ´ä½æ¶æ

Cosmos çæ´ä½æ¶ææ¯ä¸ä¸ªä»é«è´¨éæ°æ®æ¸è¿è®­ç»ãåå°å¤ç»´åº¦æ¡ä»¶æ§å¶çç»ä¸ Matchingï¼çæç®¡çº¿æ¯ï¼éè¿ç»ä¸ç DiT éª¨å¹²å frame-replacement æºå¶ï¼æ¨¡å2WorldãImage2World å Video2World ç­å¤æ¨¡æä»»å¡ï¼ææè§£å³äºä¼ ç»å¤ä»»å¡æ¨¡åå¨ä¸çå²è£çç¹ã

**æ°æ®ä¸ç¹å¾ç¼ç **
æ°æ®ä¾§ç»è¿ shot-aware video splittingãGPU-based transcodingãå¤é¶æ®µ filtering å semantic deduplication ç­ä¸¥å¯å·¥åºï¼å½¢æé«è´¨éè§é¢åçãæ¨¡åä¾§ï¼è§è§æ°æ®ç» WAN2.1 VAE ç¼ç è³ latent ç©ºé´å¹¶è¿è¡ patchificationï¼ææ¬æ¡ä»¶åç± Cosmos-Reason1 ç¼ç ï¼è·¨å¤ä¸ª blocks æ¼æ¥ token æ¿æ´»å¹¶æå½±ä¸º text embeddingã

**æ ¸å¿**
æ ¸å¿çæä¾èµ DiT velocity prediction networkï¼å¨ latent ç©ºé´äº¤æ¿ä½¿ç¨ self-attentionãcross-attention å feed-forward MLPï¼å¹¶ç± timestep ç adaptive layer normalization è°å¶ãå¯¹äº Image2World å Video2Worldï¼è®ºæéç¨ frame-replacement ç­ç¥ï¼å°çæåºååå§ frames æç»­æ¿æ¢ä¸ºæ¡ä»¶ framesãè¿ç§ç´è§ä¸ç±»ä¼¼âéå®èµ·ç¹âçåæ³ï¼ç´è§ï¼éä¸¥æ ¼å¯¹åºï¼ï¼æ¢å¸§æ°éï¼åç¡®ä¿äºæ©æå¸§å¿ å®å¢å¼ºäºæ¶é´ä¸è´æ§ï¼è®ºææªæ¥åæ¡ä»¶å¸§æ°éçéç¨æä¼ç¹ï¼éæä»»å¡è°æ´ï¼ãæ­¤å¤ï¼Cosmos-Transfer2.5 å° control blocks æ´ååå° action-conditioned çæ¬åå° action embedder MLP è¾åºå å° DiT timestamp embeddingsï¼æ¶èå®éªè¯æè¿ä¼äº cross-attention æ channel concatenationã

**è®­ç»ä¸å¯¹é½æµç¨**
è®­ç»éµå¾ªä¸¥æ ¼çæ¸è¿2Image æåºç¡ï¼åèåå¾åä¸è§é¢ä»»å¡2Worldãéåè¿è¡ domain-specific SFTï¼å¹¶éè¿ model mergingï¼æç»éæ© model soupï¼ç»ä¸ä¸åä¼å¿ãæåï¼RL post-training å°æ¡ä»¶è§ä½ statesãdenoising trajectories è§ä½ actionsï¼å©ç¨ VideoAlign è®¡ç® reward å¹¶å¨ç» loss regularization ç¼è§£ reward hackingã

```mermaid
flowchart TB
    data_pipeline["åç"] -->| vae_encode["æ½å¨ç©ºé´ç¹å¾ç¼ç "]
    text_encode["ææ¬è¯­ä¹ç¹å¾æå"] -->|è·¨åæ¼æ¥| dit_core["éåº¦é¢æµæ ¸å¿ç½ç»"]
    vae_encode -->|ååæ å°| dit_core
    cond_frames[æ¡ä»¶å¸§æ¿æ¢ä¸å¸§çº§æ¿æ¢| dit_core
    dit_core -->|train["æ¸è¿å¼å¤ä»»å¡é¢è®­ç»"]
    pretrain -->|æ¶æåæ¢| sft_merge["ä¸åå¾®è°ä¸æ¨¡ååå¹¶"]
    sft_merge -->|ä¼å¿èå| rl_post["å¼ºåå­¦ä¹ å¯¹é½åè®­ç»"]
    rl_post -->|è½¨è¿¹ä¼å| final_output["ç»ä¸ä¸çæ¨¡åçæ"]

    classDef required fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#1e3a5f
    classDef output fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d
    classDef optional fill:#fef9c3,stroke:#ca8a04,stroke-width:2px,color:#713f12
    
    class data_pipeline required
    class final_output output
```
*å¦ä½è¯»è¿å¼ å¾ï¼ä»ï¼è§è§ä¸ææ¬ç¹å¾å¨ DiT æ ¸å¿ç½ç»ä¸­äº¤æ±ï¼æ¡ä»¶å¸§æ¿æ¢æºå¶ç¡®ä¿äºå¤ä¾æ¬¡ç»åé¢è®­ç»ãå¾®è°åå¹¶ä¸å¼ºåå­¦ä¹ åè®­ç»é«åº¦ç©çä¸è´æ§çä¸çæ¨¡åçæç»æã*

<details>
<summary><strong>å¼ºåå­¦ä¹ ç»è</strong></summary>
è®­ç»æçæ¾å¼ç®æ æ¯ flow matchingå¦ä¸ï¼
$$
\mathbf { x } _ { t } = ( 1 - t ) \mathbf { x } + t { \boldsymbol { \epsilon } } .\tag{1}
$$
$$
\mathbf { v } _ { t } = \epsilon - \mathbf { x } .\tag{2}
$$
$$
\begin{array} { r } { \mathcal { L } ( \boldsymbol { \theta } ) = \mathbb { E } _ { \mathbf { x } , \boldsymbol { \epsilon } , \mathbf { c } , t } \left\| \mathbf { u } ( \mathbf { x } _ { t } , t , \mathbf { c } ; \boldsymbol { \theta } ) - \mathbf { v } _ { t } \right\| ^ { 2 } , } \end{array}\tag{3}
$$
ä¸ºè¦çé«åªå£°åºåï¼éç¨ shifted logit-normal timestep åæ¢ï¼
$$
t _ { s } = \frac { \beta t } { 1 + ( \beta - 1 ) t }\tag{4}
$$
RL é¶æ®µç±äº GPU memory constraintï¼å° trajectory probability åè§£ä¸ºæ¯æ­¥ conditional probabilities å¹¶åæ®µç´¯ç§¯æ¢¯åº¦ãæ¨çæçé¿è§é¢è¯ä¼°ææ  RNDS å®ä¹ä¸ºï¼
$$
\mathsf { R N D S } [ i ] = \left( \frac { \mathrm { D O V E R } [ i ] } { \mathrm { D O V E R } _ { \mathrm { G T } } [ i ] } \right) / \left( \frac { \mathrm { D O V E R } [ 1 ] } { \mathrm { D O V E R } _ { \mathrm { G T } } [ 1 ] } \right) ,\tag{5}
$$
</details>

ç¨æ·è¦æ±æä½ä¸ºèµæ·±ä¸­æææ¯æ·±åº¦ç§æ®è®ºææ·±åº¦è§£è¯»æ¥åä¸­çä¸èï¼æ é¢ä¸ºâ## ç®æ³ç®æ ä¸æ¨å¯¼âã
éè¦éµå®çè§èï¼
1. **ç»æ**ï¼ç»è®ºæç»è®ºï¼åå±å¼ãH2å¼å¤´ï¼å¸¦emojiã
2. **å¿ å®ä¸ä¸¥è°¨**ï¼åºåå£°ç§°ä¸è¯æï¼ç¹åå¤±ææ¨¡å¼ï¼å¦æéç¨ï¼ä½æ¬èä¸»è¦æ¯ç®æ³æ¨å¯¼ï¼å¯è½ä¸éè¦å¤ªå¤å®éªå±éï¼ä½è¦ä¸¥è°¨ï¼ã
3. **æ¥å°**ï¼åè¿°ä¸­**ç»å¯¹ä¸è½**åºç°ç²¾ç¡®æ§è½æ°å­ï¼å¦8.54, 12%ç­ï¼ãæ§è½å¯¹æ¯ç¨å®æ§è¯­è¨ãéæ§è½æ°å­ï¼å¦å±æ°ãåè¾¨çç­ï¼å¯åãä¸æåè¯åã<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-table-tr-td-confi-gur--><!--anchor:quote:%3Ctable%3E%3Ctr%3E%3Ctd%3EConfi%20guration%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D2B%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D14B%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Layers%3C%2Ftd%3E%3Ctd%3E32%3C%2Ftd%3E%3Ctd%3E36%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EModel%20Dimension%3C%2Ftd%3E%3Ctd%3E2%2C048%3C%2Ftd%3E%3Ctd%3E5%2C120%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EFFN%20Hidden%20Dimension%3C%2Ftd%3E%3Ctd%3E8%2C192%3C%2Ftd%3E%3Ctd%3E20%2C480%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EAdaLN%2DLoRA%20Dimension%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Attention%20Heads%3C%2Ftd%3E%3Ctd%3E16%3C%2Ftd%3E%3Ctd%3E40%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EHead%20Dimension%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EMLP%20Activation%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3EGELU%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EPositional%20Embedding%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3E3D%20RoPE%3C%2Ftd%3E%3C%2Ftr%3E%3C%2Ftable%3E-->
4. **å¾è¡¨åäº**ï¼æ¶åæµç¨/Mermaidï¼ï¼`%%{init}`ï¼ä¸ç¨`ï¼ç¨`classDef`+`class`ï¼â¤4ä¸ªè¯­ä¹è²ï¼èç¹id snake_caseï¼æ ç­¾3-6è¯ï¼è¾¹æ ç­¾1-4è¯ã
5. **è¡¨æ ¼ vs åè¿°**ï¼ç»æåå¯¹æ¯ç¨è¡¨ã
6. **æ·±åº¦èè¿æå å**ï¼åé¿æ¨å¯¼ã<details>`æå ã
7. **äºå®æº**ï¼
   - è®­ç»ææ¾å¼ç®æ ï¼flow matching velocity predictionã
   - ï¼$\mathbf { x } _ { t } = ( 1 - t ) \mathbf { x } + t { \boldsymbol { \epsilon } }$
  ï¼$\mathbf { v } _ { t } = \epsilon - \mathbf { x }$
  ï¼$\mathcal { L } ( \boldsymbol { \theta } ) = \mathbb { E } _ { \mathbf { x } , \boldsymbol { \epsilon } , \mathbf { c } , t } \left\| \mathbf { u } ( \mathbf { x } _ { t } , t , \mathbf { c } ; \boldsymbol { \theta } ) - \mathbf { v } _ { t } \right\| ^ { 2 }$
   -shifted logit-normal timestep åæ¢ï¼$t _ { s } = \frac { \beta t } { 1 + ( \beta - 1 ) t }$
   - c æ¯ææ¬ embeddingãreference inputsã
   - è®­ç»æ denoising loss åªæ½å å°æå®éè¦çæç framesã
   - RL post-trainingï¼ä½¿ç¨ VideoAlign rewardãå advantageãè½¨è¿¹æ¡ä»¶æ¦çåè§£å diffusion loss regularizationï¼æ æ¾å¼ RL
   - æ¨çæé¿è§é¢è¯ä¼°ææ  RNDSï¼éè®­ç»ç®æ ï¼ï¼$\mathsf { R N D S } [ i ] = \left( \frac { \mathrm { D O V E R } [ i ] } { \mathrm { D O V E R } _ { \mathrm { G T } } [ i ] } \right) / \left( \frac { \mathrm { D O V E R } [ 1 ] } { \mathrm { D O V E R } _ { \mathrm { G T } } [ 1 ] } \right)$
8. **æ¬èä»»å¡**ï¼
åæ ·ç»åºæº - éå¯¹æ¬ççå®éæ­¥æ¨å¯¼è®²è§£æ¯ä¸é¡¹å«ä¹ä¸è®¾è®¡çç±ï¼ä¸åå¥è¯ï¼ã
   - ç»ä¸ä¸ªç´è§æ¯å»ä¾å­ã
   - æ ç²¾ç¡®æ§è½æ°å­ã
   - æ é¢ï¼â## ç®æ³ç®æ ä¸æ¨å¯¼â (H2å¥é¦å¯å¸¦emojiï¼å¦ "## ð¯ ç®æ³ç®æ ä¸æ¨å¯¼")ã

æèç»æï¼
- **æ é¢**ï¼## ð¯ ç®æ³ç®æ ä¸æ¨å¯¼
- **ç»è®ºåç½®**ï¼æ¬æ¨¡åçæ ¸å¿è®­ç»ç®æ å¹¶éä¼ ç»çåªå£°é¢æµï¼èæ¯åºäº Flow Matching çéåº¦åºé¢æµï¼velocity predictionï¼ï¼éè¿ç´æ¥å­¦ä¹ ä»åªå£°å°çå®æ°æ®çç´çº¿è½¨è¿¹éåº¦ï¼ç»å shifted logit-normal æ¶é´æ­¥éæ ·ä¸å±é¨å»åªæå¤±ï¼å®ç°äºæ´é«æçè§é¢çæå¯¹é½ï¼èå¨åè®­ç»é¶æ®µå VideoAlign çå¼ºåå­¦ä¹ æ¥ä¼åäººç±»åå¥½ï¼æ¨çæéç¨ RNDS è¯ä¼°é¿è§é¢ä¸è´æ§ã
- **æº5ã
- **éæ­¥æ¨å¯¼ä¸è®¾è®¡çç±**ï¼
  - Flow Matching åºç¡ï¼3ï¼ï¼è§£é $x_t$ ççº¿æ§æå¼ï¼$v_t$ çæå®éåº¦ï¼ä»¥åæå¤±å½æ° $\mathcal{L}$ å¦ä½è®©æ¨¡å $\mathbf{u}$ é¼è¿è¿ä¸ªéåº¦ãè®¾è®¡çç±ï¼ç¸æ¯ DDPM çå¤æåªå£°è°åº¦ï¼ç´çº¿è½¨è¿¹æ´ç­ãæ¨çæ´å¿«ã
  - æ¶é´æ­¥åæ¢ï¼è§£é shifted logit-normal çä½ç¨ï¼è®©æ¨¡åå¨ä¸­é´è¿æ¸¡é¶æ®µï¼èéçº¯åªå£°æçº¯æ°æ®ç«¯ï¼èµæºã
  - å±é¨å»åªä¸æ¡ä»¶ $c$ï¼è¯´æ loss åªæ½å å¨éè¦çæç framesï¼ç»åææ¬ååèå¸§ï¼è§£å³é¿è§é¢çæçæ¾å­åä¸è´æ§çç¹ã
  - RL åè®­ç»ä¸ RNDS è¯ä¼°ï¼å®æ§è¯´æ RL çç»ä»¶ï¼ä»¥å RNDS å¦ä½è¡¡éé¿åºåçè¡°åã
- **å¾è¡¨**ï¼ç»ä¸ä¸ª Flow Matching ä¸ RL åè®­ç»çæµç¨å¾ (Mermaid)ã
- **ç´è§æ¯å»ä¸å°
  - æ¯å»ï¼å¯¼èªç³»ç»ï¼Flow Matchingï¼ä¸é©¾æ ¡æç»ï¼RLï¼ã
  -ä¸ç»´ç©ºé´ä¸­å°çä» A å° B çç§»å¨ã
- **æå å**ï¼RL åè®­ç» RNDS çæ°å­¦æè§£ã

æ£æ¥çº¦æï¼
- æ ç²¾ç¡®æ§è½æ°å­ï¼æ¯ã
- ä¸æåè¯ä¸ç¿»è¯ï¼Flow Matching, VideoAlign, RNDS, DOVER, shifted logit-normal timestep, reference frames, conditional inputs, advantage, diffusion loss regularizationã
- Mermaid è§èï¼æ  `%%{init}`ï¼æ style`ï¼ç¨ `classDef`ï¼â¤4è²ï¼snake_case idï¼æ ç­¾å­æ°éå¶ã
- 0-800å­ï¼å°½éåè¶³ï¼å±å¼è¯¦ç»ç¹ï¼å¤§æ¦600-800å­ï¼ã

èæ Mermaid å¾ï¼
```mermaid
flowchart TD
    classDef data fill:#e1f5fe,stroke:#01579b,color:#01579b;
    classDef process fill:#fff3e0,stroke:#e65100,color:#e65100;
    classDef decision fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20;
    classDef output fill:#fce4ec,stroke:#880e4f,color:#880e4f;

    raw_data["çå®è§é¢ä¸åªå£°"]:::data
    linear_interp["çº¿æ§æå¼æå»ºè½¨è¿¹"]:::process
    velocity_target["è®¡ç®æå®éåº¦åº"]:::process
    model_pred["æ¨¡åé¢æµéåº¦åé"]:::process
    calc_loss["è®¡ç®åæ¹è¯¯å·®æå¤±"]:::process
    update_weights["æ´æ°æ¨¡ååæ°"]:::process
    
    raw_data --> linear_interp
    linear_interp --> velocity_target
    velocity_target --> calc_loss
    model_pred --> calc_loss
    calc_loss --> update_weights
```
ä¿®æ¹èç¹æ ç­¾ä»¥ç¬¦å3-6è¯ï¼è¾¹æ ç­¾1-4è¯ã
```mermaid
flowchart TD
    classDef data fill:#e1f5fe,stroke:#01579b,color:#01579b;
    classDef process fill:#fff3e0,stroke:#e65100,color:#e65100;
    classDef reward fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20;
    classDef output fill:#fce4ec,stroke:#880e4f,color:#880e4f;

    raw_video["çå®è§é¢ä¸é«æ¯åªå£°"]:::data
    linear_path["æå»ºçº¿æ§æå¼è½¨è¿¹"]:::process
    target_vel["è®¡ç®ç®æ æå®éåº¦"]:::process
    model_pred["ç¥ç»ç½ç»é¢æµéåº¦åº"]:::process
    mse_loss["è®¡ç®éåº¦åæ¹è¯¯å·®"]:::process
    rl_align["Alignå¥å±å¯¹é½"]:::reward
    final_model["è¾åºé¿è§é¢çææ¨¡å"]:::output

    raw_video -->|æ··åæ°æ®| linear_path
    linear_path -->|æ±å¯¼| target_vel
    target_vel -->|çç£| mse_loss
    model_pred -->|é¢æµ| mse_loss
    mse_loss -->|ååä¼ æ­| model_pred
    model_pred -->|åè®­ç»| rl_align
    rl_align -->|åå¥½ä¼å| final_model
```
æ£æ¥ Mermaid çº¦æï¼
- ç¦ç¨ `%%{init}` ä¸`ï¼æ»¡è¶³ã
- åªç¨ `classDef`+`class`ï¼æ»¡è¶³ã
- æ¯å¾ â¤4 ä¸ªè¯­ä¹è²ä¸æ¯è²å«æå­ `color:`ï¼4ä¸ªé¢è²ï¼é½å¸¦äº `color:`ã
- snake_case èç¹ idï¼æ»¡è¶³ã
- æ ç­¾ 3-6 è¯ä¸»å¨è¯­æï¼
  - çå®è§é¢ä¸é«æ¯åªå£° (7ä¸ªå­ï¼ç®è¯åï¼ä¸­ææå­æè¯ç®ï¼å°½éç­ç¹ï¼çå®è§é¢ä¸åªå£° 6å­) -> çå®è§é¢ä¸çº¯åªå£° (7å­) -> è§é¢æ°æ®ä¸çº¯åªå£° (7å­)ãä¸­æâè¯âçæ¦å¿µæ¯è¾æ¨¡ç³ï¼éå¸¸æ3-6ä¸ªæ±å­æè¯è¯­ãæ¹ä¸ºï¼è§é¢ä¸çº¯åªå£° (6å­)ã
  - æå»ºçº¿æ§æå¼è½¨è¿¹ (8å­) -> æå»ºçº¿æ§æå¼è·¯å¾ (8å­) -> æå»ºçº¿æ§è½¨è¿¹ (6å­)ã
  - è®¡ç®ç®æ æå®éåº¦ (8å­) -> è®¡ç®æå®ç®æ éåº¦ (8å­) -> è®¡ç®ç®æ éåº¦ (6å­)ã
  - ç¥ç»ç½ç»é¢æµéåº¦åº (9å­) -> æ¨¡åé¢æµéåº¦åº (7å­) -> é¢æµéåº¦åé (6å­)ã
  - è®¡ç®éåº¦åæ¹è¯¯å·® (8å­) -> è®¡ç®åæ¹è¯¯å·® (6å­)ã
  -å¥å±å¯¹é½ (12å­ç¬¦) -> å¼ºåå­¦ä¹ åå¥½å¯¹é½ (8å­) -> å¥å±å¯¹é½åå¥½ (6å­)ã
  - è¾åºé¿è§é¢çææ¨¡å (9å­) -> è¾åºè§é¢çææ¨¡å (8å­) -> è¾åºæç»æ¨¡å (6å­)ã
  è¾¹æ ç­¾ï¼
  - æ··åæ°æ® (4å­)
  - æ±å¯¼è®¡ç® (4å­)
  - çç£è®­ç» (4å­)
  - è¾åºé¢æµ (4å­)
  - ååä¼ æ­ (4å­)
  - åè®­ç» (3å­)
  - åå¥½ä¼å (4å­)
  è¿æ ·æ¯è¾ç¨³å¦¥ã

éæ°è°æ´ Mermaid:
```mermaid
flowchart TD
    classDef data fill:#e1f5fe,stroke:#01579b,color:#01579b;
    classDef process fill:#fff3e0,stroke:#e65100,color:#e65100;
    classDef reward fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20;
    classDef output fill:#fce4ec,stroke:#880e4f,color:#880e4f;

    video_noise["è§é¢ä¸çº¯åªå£°"]:::data
    build_path["æå»ºçº¿æ§è½¨è¿¹"]:::process
    calc_vel["è®¡ç®ç®æ éåº¦"]:::process
    pred_vel["é¢æµéåº¦åé"]:::process
    calc_mse["è®¡ç®åæ¹è¯¯å·®"]:::process
    rl_align["å¥å±å¯¹é½åå¥½"]:::reward
    out_model["è¾åºæç»æ¨¡å"]:::output

    video_noise -->|æ··åæ°æ®| build_path
    build_path -->|æ±å¯¼è®¡ç®| calc_vel
    calc_vel -->|çç£è®­ç»| calc_mse
    pred_vel -->|è¾åºé¢æµ| calc_mse
    calc_mse -->|ååä¼ æ­| pred_vel
    pred_vel -->|åè®­ç»| rl_align
    rl_align -->|åå¥½ä¼å| out_model
```

æ­£ææ°åï¼
ç»è®ºåç½®ï¼æ¬æ¨¡åçæ ¸å¿è®­ç»ç®æ å¹¶éä¼ ç»çåªå£°é¢æµï¼èæ¯åºäº Flow Matching çéåº¦åºé¢æµï¼velocity predictionï¼ï¼éè¿ç´æ¥å­¦ä¹ ä»åªå£°å°çå®æ°æ®çç´çº¿è½¨è¿¹éåº¦ï¼ç»å shifted logit-normal æ¶é´æ­¥éæ ·ä¸å±é¨å»åªæå¤±ï¼å®ç°äºæ´é«æçè§é¢çæå¯¹é½ï¼èå¨ååºäº VideoAlign çå¼ºåå­¦ä¹ æ¥ä¼åäººç±»åå¥½ï¼æ¨çæéç¨ RNDS è¯ä¼°é¿è§é¢ä¸è´æ§ã

$$
\mathbf { x } _ { t } = ( 1 - t ) \mathbf { x } + t { \boldsymbol { \epsilon } } .\tag{1}
$$
$$
\mathbf { v } _ { t } = \epsilon - \mathbf { x } .\tag{2}
$$
$$
\begin{array} { r } { \mathcal { L } ( \boldsymbol { \theta } ) = \mathbb { E } _ { \mathbf { x } , \boldsymbol { \epsilon } , \mathbf { c } , t } \left\| \mathbf { u } ( \mathbf { x } _ { t } , t , \mathbf { c } ; \boldsymbol { \theta } ) - \mathbf { v } _ { t } \right\| ^ { 2 } , } \end{array}\tag{3}
$$
$$
t _ { s } = \frac { \beta t } { 1 + ( \beta - 1 ) t }\tag{4}
$$
$$
\mathsf { R N D S } [ i ] = \left( \frac { \mathrm { D O V E R } [ i ] } { \mathrm { D O V E R } _ { \mathrm { G T } } [ i ] } \right) / \left( \frac { \mathrm { D O V E R } [ 1 ] } { \mathrm { D O V E R } _ { \mathrm { G T } } [ 1 ] } \right) ,\tag{5}
$$

æ¨å¯¼ä¸è®¾è®¡çç±ï¼
 å (2) å®ä¹äº Flow Matching çæ ¸å¿ï¼å¨çå®æ°æ® $\mathbf{x}$ åçº¯åªå£° $\boldsymbol{\epsilon}$ ä¹é´æå»ºä¸æ¡æç®åççº¿æ§æå¼è·¯å¾ $\mathbf{x}_t$ãè¿æ¡è·¯å¾çå¯¼æ°å³ä¸ºæå®éåº¦åº $\mathbf{v}_t$ãè®¾è®¡çç±å¨äºï¼ç¸æ¯äº DDPM ä¸­å¤æçéçº¿æ§åªå£°è°åº¦ï¼ç´çº¿è½¨è¿¹å¨æ°å­¦ä¸æ´ç­ãæ´å¹³æ»ï¼ä½¿å¾æ¨¡åå¨æ¨çæ¶å¯ä»¥ç¨æ´å°çæ­¥æ°å°è¾¾ç»ç¹ã
3) æ¯è®­ç»æçæ¾å¼ç®æ ï¼è¦æ±ç¥ç»ç½ç» $\mathbf{u}$ å¨ç»å®æ¡ä»¶ $\mathbf{c}$ãreference inputsï¼ä¸ï¼é¢æµçéåº¦å°½å¯è½é¼è¿çå®éåº¦ $\mathbf{v}_t$ãå¼å¾æ³¨æçæ¯ï¼denoising loss éè¦çæç framesï¼è¿ç§å±é¨çç£æºå¶éä½äºé¿è§é¢è®­ç»çæ¾å­å¼éï¼åæ¶å©ç¨ reference frames éå®äºæ¶åºä¸è´æ§ã (4) ç shifted logit-normal timestep åæ¢è§£å³äºéæ ·æçé®é¢ãéè¿å°æ¶é´æ­¥ $t$ æ å°ä¸º $t_s$ï¼æ¨¡åè½å¨è½¨è¿¹çä¸­é´è¿æ¸¡é¶æ®µï¼å³ç»ææåå¨çº¯åªå£°æçº¯æ°æ®ç«¯æµªè´¹ç®åã

ç´è§æ¯å»ä¸å°**ç´è§æ¯å»**ï¼ç´è§ï¼éä¸¥æ ¼å¯¹åºï¼ï¼ä¼ ç»çæ©æ£æ¨¡ååæ¯å¨æµé¾ä¸­æ ¹æ®âé£åâï¼åªå£°é¢æµï¼æ¸ç´¢åå®¶ï¼è Flow Matching åæ¯ç´æ¥ç»ä½ ä¸å¼ å¯¼èªå°å¾ï¼åè¯ä½ ä»å½åä½ç½®å°å®¶çâç´çº¿æå®è½¦éâï¼éåº¦åºé¢æµï¼ãRL åè®­ç»ååæ¯é©¾æ ¡æç»ï¼è¦æ±ä½ å¼å°ç»ç¹ï¼è¿è¦æ±ä½ å¼å¾âå¹³ç¨³ãç¬¦åäººç±»å®¡ç¾âï¼VideoAlign rewardï¼ã
**å°åè®¾å¨ä¸ç»´æ°è½´ä¸ï¼å°çè¦ä»åæ  $x=0$ï¼åªå£°ï¼ç§»å¨å° $x=10$ï¼çå®è§é¢å¸§ï¼ãFlow Matching ç´æ¥è®¾å®éåº¦ $v = 10 - 0 = 10$ãå¨ $t=0.5$ æ¶ï¼å°çä½äº $x_{0.5} = 5$ãæ¨¡ååªéé¢æµåºéåº¦ $10$ï¼æ¨çæ¶ææ­¤éåº¦ç§¯åå³å¯ç²¾åå°è¾¾ $10$ï¼æ éå¤æçæ¹å·®ç¼©æ¾ã

RL åè®­ç»ä¸é¿è§é¢è¯ä¼°ï¼
å¨é¢è®­ç»å¯¹é½ç©çè§å¾ RL post-trainingãè®ºæå®æ§è¯´æä½¿ç¨äº VideoAlign rewardãå advantageãè½¨è¿¹æ¡ä»¶æ¦çåè§£å diffusion loss regularizationï¼ä»¥æ­¤å°çæè´¨éä¸äººç±»åå¥½å¯¹é½ãä¸ºäºè¡¡éé¿è§é¢å¨æ¶é´è½´ä¸çè´¨éè¡°åï¼æ¨ç 5ï¼ï¼éè¿è®¡ç®ç¬¬ $i$ å¸§ä¸ç¬¬ $1$ å¸§ç DOVER è´¨éæ¯å¼ï¼éåé¿åºåçæ¶åºä¸è´æ§ã

æå åï¼
<details>
<summary><strong>RL åè®­ç»ç»ä»¶ä¸ RNDS ææ æ·±åº¦æè§£</strong></summary>
RL é¶æ®µå¹¶æªç»åºæ¾å¼æå¤±æºå¶ä¾èµäºåä¸ªç»ä»¶çååï¼VideoAlign reward æä¾æ éåé¦ä¸å advantage éä½æ¹å·®ï¼è½¨è¿¹æ¡ä»¶æ¦çåè§£å¤çé¿åºåçä¿¡ç¨ loss regularization åé²æ­¢æ¨¡åå¨ä¼ååå¥½æ¶åç¦»é¢è®­ç»çæ°æ®æµå½¢ï¼å³é²æ­¢ reward hackingï¼ã
RNDS ææ çè®¾è®¡å·§å¦ä¹å¤å¨äºâç¸å¯¹è¡°åâèéâç»å¯¹è´¨éâãåå­è¡¡éçæè§é¢ç¬¬ $i$ å¸§ç¸å¯¹äºç¬¬ $1$ å¸§çè´¨éä¿æçï¼åæ¯åç¨ Ground Truth (GT) çåç­è¡°åçè¿è¡æ ¡åãè¿ç§è®¾è®¡å¥ç¦»äºè§é¢æ¬èº«åºæçé¾åº¦å·®å¼ï¼çº¯ç²¹è¯ä¼°æ¨¡åå¨é¿ç¨çæä¸­çè¯¯å·®ç´¯ç§¯æåºã
</details>

æ£æ¥å­æ°ï¼çº¦ 700 å­ï¼ç¬¦å 350-800 çè¦æ±ã
æ£æ¥æ¥å°ï¼æ²¡æç²¾ç¡®æ§è½æ°å­ã
æ£æ¥ä¸æåè¯ï¼Flow Matching, velocity prediction, DDPM, shifted logit-normal timestep, reference frames, conditional inputs, VideoAlign, advantage, diffusion loss regularization, RNDS, DOVER, reward hackingãåä¿çåæ ·ãåæ ·ä¿çï¼æ²¡æä¿®æ¹ã
æ£æ¥å¾è¡¨ï¼Mermaid ç¬¦åææè§èã

æ´åä¼ç§çä¸­æææ¯åå®¢ã
âç»è®ºåç½®âé¨åå¯ä»¥æ´ç²¾ç¼æåã
âæ¨å¯¼ä¸è®¾è®¡çç±âé¨åç¡®ä¿é»è¾ä¸¥å¯ã
ç¡®ä¿æ²¡æä½¿ç¨âç±æ²¿ä¼åæ¹åè¿­ä»£âè¿ç§å¥è¯ã

ä¿®æ¹åçç»è®ºåç½®ï¼
æ¬æ¨¡åçæ ¸å¿è®­ç»ç®æ å¹¶éä¼ ç»çåªå£°é¢æµï¼èæ¯åºäº Flow Matching çéåº¦åºé¢æµï¼velocity predictionï¼ãéè¿ç´æ¥å­¦ä¹ ä»åªå£°å°çå®æ°æ®çç´çº¿è½¨è¿¹éåº¦ï¼ç»å shifted logit-normal æ¶é´æ­¥éæ ·ä¸å±é¨å»åªæå¤±ï¼æ¨¡åå®ç°äºæ´é«æçè§é¢çæå¯¹é½ï¼ååºäº VideoAlign çå¼ºåå­¦ä¹ ä¼åäººç±»åå¥½ï¼å¹¶å¨æ¨çæéç¨ RNDS è¯ä¼°é¿è§é¢æ¶åºä¸è´æ§ã

æ£æ¥ Mermaid å¾çèç¹åè¾¹ï¼
video_noise[è§é¢ä¸çº¯åªå£°]
build_path[æå»ºçº¿æ§è½¨è¿¹]
calc_vel[è®¡ç®ç®æ éåº¦]
pred_vel[é¢æµéåº¦åé]
calc_mse[è®¡ç®åæ¹è¯¯å·®]
rl_align[å¥å±å¯¹é½åå¥½]
out_model[è¾åºæç»æ¨¡å]
è¾¹ï¼æ··åæ°æ®ï¼æ±å¯¼è®¡ç®ï¼çç£è®­ç»ï¼è¾åºé¢æµï¼ååä¼ æ­ï¼åè®­ç»ï¼åå¥½ä¼åã
3-6 è¯ï¼æ±å­ï¼ï¼1-4 è¯ï¼æ±å­ï¼çè¦æ±ã

æç»ç¡®è®¤æ éæ¼ï¼çæè¾åºã## ð¯ ç®æ³ç®æ ä¸æ¨å¯¼

æ¬æ¨¡åçæ ¸å¿è®­ç»ç®æ å¹¶éä¼ ç»çåªå£°é¢æµï¼èæ¯åºäº Flow Matching çéåº¦åºé¢æµï¼velocity predictionï¼ãéè¿ç´æ¥å­¦ä¹ ä»åªå£°å°çå®æ°æ®çç´çº¿è½¨è¿¹éåº¦ï¼ç»å shifted logit-normal æ¶é´æ­¥éæ ·ä¸å±é¨å»åªæå¤±ï¼æ¨¡åå®ç°äºæ´é«æçè§é¢çæå¯¹é½ï¼åè®­ç»é¶æ®µå çå¼ºåå­¦ä¹ ä¼åäººç±»åå¥½ï¼å¹¶å¨æ¨çæéç¨ RNDS è¯ä¼°é¿è§é¢æ¶åºä¸è´æ§ã

### æºå¶

è®ºæéå­ç»åºçè®­ç»æä¸æ¨çææ ¸å¿$$
\mathbf { x } _ { t } = ( 1 - t ) \mathbf { x } + t { \boldsymbol { \epsilon } } .\tag{1}
$$
$$
\mathbf { v } _ { t } = \epsilon - \mathbf { x } .\tag{2}
$$
$$
\begin{array} { r } { \mathcal { L } ( \boldsymbol { \theta } ) = \mathbb { E } _ { \mathbf { x } , \boldsymbol { \epsilon } , \mathbf { c } , t } \left\| \mathbf { u } ( \mathbf { x } _ { t } , t , \mathbf { c } ; \boldsymbol { \theta } ) - \mathbf { v } _ { t } \right\| ^ { 2 } , } \end{array}\tag{3}
$$
$$
t _ { s } = \frac { \beta t } { 1 + ( \beta - 1 ) t }\tag{4}
$$
$$
\mathsf { R N D S } [ i ] = \left( \frac { \mathrm { D O V E R } [ i ] } { \mathrm { D O V E R } _ { \mathrm { G T } } [ i ] } \right) / \left( \frac { \mathrm { D O V E R } [ 1 ] } { \mathrm { D O V E R } _ { \mathrm { G T } } [ 1 ] } \right) ,\tag{5}
$$

### éæ­¥æ¨å¯¼ (1) å (2) å®ä¹äº Flow Matching çå ä½åºç¡ï¼å¨çå®æ°æ® $\mathbf{x}$ åçº¯åªå£° $\boldsymbol{\epsilon}$ ä¹é´æå»ºä¸æ¡æç®åççº¿æ§æå¼è·¯å¾ $\mathbf{x}_t$ãè¿æ¡è·¯å¾çå¯¼æ°å³ä¸ºæå®éåº¦åº $\mathbf{v}_t$ãè®¾è®¡çç±å¨äºï¼ç¸æ¯äº DDPM ä¸­å¤æçéçº¿æ§åªå£°è°åº¦ï¼ç´çº¿è½¨è¿¹å¨æ°å­¦ä¸æ´ç­ãæ´å¹³æ»ï¼ä½¿å¾æ¨¡åå¨æ¨çæ¶å¯ä»¥ç¨æ´å°çæ­¥æ°å°è¾¾ç»ç¹3) æ¯è®­ç»æçæ¾å¼ç®æ ï¼è¦æ±ç¥ç»ç½ç» $\mathbf{u}$ å¨ç»å®æ¡ä»¶ $\mathbf{c}$ãreference frames ä¸ï¼é¢æµçéåº¦å°½å¯è½é¼è¿çå®éåº¦ $\mathbf{v}_t$ãå¼å¾æ³¨æçæ¯ï¼denoising loss éè¦çæç framesï¼è¿ç§å±é¨çç£æºå¶è®­ç»çæ¾å­å¼éï¼åæ¶å©ç¨ reference frames éå®äºæ¶åºä¸è´æ§ã

 ç shifted logit-normal timestep åæ¢è§£å³äºéæ ·æçé®é¢ãéè¿å°æ¶é´æ­¥ $t$ æ å°ä¸º $t_s$ï¼æ¨¡åè½å¨è½¨è¿¹çä¸­é´è¿æ¸¡é¶æ®µï¼å³è§é¢ç»ææåçº¯åªå£°æçº¯æ°æ®ç«¯æµªè´¹ç®åã

```mermaid
flowchart TD
    classDef data fill:#e1f5fe,stroke:#01579b,color:#01579b;
    classDef process fill:#fff3e0,stroke:#e65100,color:#e65100;
    classDef reward fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20;
    classDef output fill:#fce4ec,stroke:#880e4f,color:#880e4f;

    video_noise["è§é¢ä¸çº¯åªå£°"]:::data
    build_path["æå»ºçº¿æ§è½¨è¿¹"]:::process
    calc_vel["è®¡ç®ç®æ éåº¦"]:::process
    pred_vel["é¢æµéåº¦åé"]:::process
    calc_mse["è®¡ç®åæ¹è¯¯å·®"]:::process
    rl_align["å¥å±å¯¹é½åå¥½"]:::reward
    out_model["è¾åºæç»æ¨¡å"]:::output

    video_noise -->|æ··åæ°æ®| build_path
    build_path -->|æ±å¯¼è®¡ç®| calc_vel
    calc_vel -->|çç£è®­ç»| calc_mse
    pred_vel -->|è¾åºé¢æµ| calc_mse
    calc_mse -->|ååä¼ æ­| pred_vel
    pred_vel -->|åè®­ç»| rl_align
    rl_align -->|åå¥½ä¼å| out_model
```
*å¦ä½è¯»è¿å¼ å¾ï¼ä¸åé¨åå±ç¤ºäº Flow Matching é¢è®­ç»çååä¼ æ­ä¸ååæ´æ°é­ç¯ï¼ä¸åé¨åæ­ç¤ºäº RL åè®­ç»å¦ä½æ¥ç®¡é¢è®­ç»æ¨¡åè¿è¡åå¥½å¯¹é½ã*

### ç´è§

**ç´è§æ¯å»**ï¼ç´è§ï¼éä¸¥æ ¼å¯¹åºï¼ï¼ä¼ ç»çæ©æ£æ¨¡ååæ¯å¨æµé¾ä¸­æ ¹æ®âé£åâï¼åªå£°é¢æµï¼æ¸ç´¢åå®¶ï¼è Flow Matching åæ¯ç´æ¥ç»ä½ ä¸å¼ å¯¼èªå°å¾ï¼åè¯ä½ ä»å½åä½ç½®å°å®¶çâç´çº¿æå®è½¦éâï¼éåº¦åºé¢æµï¼ãRL åè®­ç»ååæ¯é©¾æ ¡ä½ å¼å°ç»ç¹ï¼è¿è¦æ±ä½ å¼å¾âå¹³ç¨³ãç¬¦åäººç±»å®¡ç¾âï¼VideoAlign rewardï¼ãä¾å­**ï¼åè®¾å¨ä¸ç»´æ°è½´ä¸ï¼å°çè¦ä»åæ  $x=0$ï¼åªå£°ï¼ç§»å¨å° $x=10$ï¼çå®è§é¢å¸§ï¼ãFlow Matching ç´æ¥è®¾å®éåº¦ $v = 10 - 0 = 10$ãå¨ $t=0.5$ æ¶ï¼å°çä½äº $x_{0.5} = 5$ãæ¨¡ååªéé¢æµåºéåº¦ $10$ï¼æ¨çæ¶ææ­¤éåº¦ç§¯åå³å¯ç²¾åå°è¾¾ $10$ï¼æ éå¤æçæ¹å·®ç¼©æ¾ã

### RL åè®­ç»ä¸é¿è§é¢è¯ä¼°

å¨é¢è®­ç»å¯¹é½ç©çè§å¾åï¼æ¨¡åãè®ºæå®æ§è¯´æä½¿ç¨äº VideoAlign rewardä¸å advantageãè½¨è¿¹æ¡ä»¶æ¦çåè§£å diffusion loss regularizationï¼ä»¥æ­¤å°çæè´¨éä¸äººç±»åå¥½å¯¹é½ãä¸ºäºè¡¡éé¿è§é¢å¨æ¶é´è½´ä¸çè´¨éè¡°å RNDS ææ ï¼ï¼éè¿è®¡ç®ç¬¬ $i$ å¸§ä¸ç¬¬ $1$ å¸§ç DOVER è´¨éæ¯å¼ï¼éåé¿åºåçæ¶åºä¸è´æ§ï¼å®éªä¸å¯¹æ¯âä¸èçè¡¨æ ¼ï¼ã

<details>
<summary><strong>RL åè®­ç»ç»ä»¶ä¸ RNDS ææ æ·±åº¦æè§£</strong></summary>
RL é¶æ®µå¹¶æªç»åºæ¾å¼æå¤±æºå¶ä¾èµäºåä¸ªç»ä»¶çååï¼VideoAlign reward æä¾æ éåé¦ï¼å advantage éä½æ¹å·®ï¼è½¨è¿¹æ¡ä»¶æ¦çåè§£å¤çé¿ï¼è diffusion loss regularization åé²æ­¢æ¨¡åå¨ä¼ååå¥½æ¶åç¦»é¢è®­ç»çæ°æ®æµå½¢ï¼å³é²æ­¢ reward hackingï¼ã

RNDS ææ çè®¾è®¡å·§å¦ä¹å¤å¨äºâç¸å¯¹è¡°åâèéâç»å¯¹è´¨éâãåå­è¡¡éçæè§é¢ç¬¬ $i$ å¸§ç¸å¯¹äºç¬¬ $1$ å¸§çè´¨éä¿æçï¼åæ¯åç¨ Ground Truth (GT) çåç­è¡°åçè¿è¡æ ¡åãè¿ç§è®¾è®¡å¥ç¦»äºè§é¢æ¬èº«åºæçé¾åº¦å·®å¼ï¼çº¯ç²¹è¯ä¼°æ¨¡åå¨é¿ç¨çæä¸­çè¯¯å·®ç´¯ç§¯æåºã
</details>

ç¨æ·è¦æ±æ°åä¸ç¯æ·±åº¦ç§æ®è®ºæè§£è¯»æ¥åä¸­çä¸èï¼æ é¢ä¸ºâ## å®éªè®¾è®¡ä¸ç»æè§£è¯»âã
éè¦éµå¾ªä¸¥æ ¼çåä½è§èï¼
1. **ç»æ**ï¼ç»è®ºåç½®æç»è®ºï¼åå±å¼ãH2å¼å¤´ï¼å¸¦emojiãH3/H4ä¸å¸¦emojiã
2. **å¿ å®ä¸ä¸¥è°¨**ï¼åºåâå£°ç§°âä¸âè¯æâï¼ç¹åå¤±ææ¨¡å¼ï¼å¦ç­ï¼ï¼è¯´ææ¯å¦æ¥åæ¶è/è´ç»æã
3. **æ¥å°**ï¼**ç»å¯¹ä¸è¦å¨åè¿°å¥å­éåç²¾ç¡®æ§è½æ°å­**ï¼å¦è¾¾å°8.54ï¼æå12%ç­ï¼ãæ§è½å¯¹æ¯ç¨å®æ§è¯­è¨ï¼éè¦æ¶éâ(å®éªä¸å¯¹æ¯âçè¡¨æ ¼)âãéæ§è½æ°å­ï¼å¦2B, 14B, 720p, 93å¸§, 4096 GPUsï¼å¯æ­£å¸¸åãä¿çåæ ·ã<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-table-tr-td-confi-gur--><!--anchor:quote:%3Ctable%3E%3Ctr%3E%3Ctd%3EConfi%20guration%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D2B%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D14B%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Layers%3C%2Ftd%3E%3Ctd%3E32%3C%2Ftd%3E%3Ctd%3E36%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EModel%20Dimension%3C%2Ftd%3E%3Ctd%3E2%2C048%3C%2Ftd%3E%3Ctd%3E5%2C120%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EFFN%20Hidden%20Dimension%3C%2Ftd%3E%3Ctd%3E8%2C192%3C%2Ftd%3E%3Ctd%3E20%2C480%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EAdaLN%2DLoRA%20Dimension%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Attention%20Heads%3C%2Ftd%3E%3Ctd%3E16%3C%2Ftd%3E%3Ctd%3E40%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EHead%20Dimension%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EMLP%20Activation%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3EGELU%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EPositional%20Embedding%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3E3D%20RoPE%3C%2Ftd%3E%3C%2Ftr%3E%3C%2Ftable%3E--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-describe-the-multi--><!--anchor:quote:We%20describe%20the%20multi%2Dstage%20pretraining%20procedure%20in%20Tab.%204.%20Training%20begins%20with%20the%20Text2Image%20task%20at%20a%20resolution%20of%20256p.--><!--ref:r-we-adopt-a-different-s--><!--anchor:quote:We%20adopt%20a%20different%20set%20of%20auxiliary%20models%20in%20%5BCosmos%2DPredict2.5%5D%20compared%20to%20%5BCosmos%2DPredict1%5D%2C%20with%20improvements%20in%20both%20visual%20and%20textual--><!--ref:r-table-9-training-effic--><!--anchor:quote:Table%209%3A%20Training%20efficiency%20with%204096%20NVIDIA%20H100%20GPUs%20where%20the%20video%20resolution%20is%20720p%20and%20number%20of%20frames%20is-->
4. **å¾è¡¨åäº**ï¼æ¶åæµç¨/ç»æ/Mermaidï¼ï¼`%%{init`style`ï¼åªç¨`classDef`+`class`ï¼â¤4ä¸ªè¯­ä¹è²ï¼snake_caseèç¹idï¼æ ç­¾3-6è¯ï¼è¾¹æ ç­¾1-4è¯ãå¤æå¾åè¡¥ä¸å¥âå¦ä½è¯»è¿å¼ å¾âã
5. **è¡¨æ ¼ vs åè¿°**ï¼ç»æåå¯¹æ¯ç¨è¡¨ï¼åè¿°ä¸å¡è¿è¡¨ã
6. **æ·±åº¦èè¿æå å**ï¼åé¿ç»èç¨`<details>`æå ã
7. **ç¡¬çº¦æ**çå¨ï¼æ¯å»æ°å½ãåªç¨æä¾çäºå®æºãä¸ç¼é ãä¸åç²¾ç¡®æ§è½50-800å­ï¼å°½éåè¶³ï¼å¯è½éè¦æ´é¿ä»¥è¦çææå®éªï¼ä½æä¼æ§å¶å¨åçè¾åºæ¬èæ­£æï¼ä»¥â## å®éªè®¾è®¡ä¸ç»æè§£è¯»âå¼å¤´ã

åææä¾çäºå®æºï¼
- E1: Cosmos-Predict2.5 è®­ç»2B, 14B, 4096 H100, 720p, 93å¸§) -> éªè¯ç»ä¸æ¨¡åè¦çå¤- E2: VideoAlign å¼ºåå­¦ä¹ åè®­ç»è¯ä¼° (RLååå¯¹æ¯, PAI-Bench, äººå·¥æç¥¨) -> RLæåå¥å±åäººå·¥åå¥½ã
- E3: rCM æ¶é´æ­¥è¸é¦è¯ä¼° (teacher vs distilled, Text2World/Image2World) -> è¸é¦æ¨¡åæ¥è¿teacherã
- E4: PAI-Bench Predict èªå¨åºåè¯ä¼° (pre-train vs post-train vs Wanç³»å) -> post-trainä¼äºpre-trainï¼Image
- E5: PAIBench-Transfer å¤æ§å¶æ¨¡æè¯ä¼° (åæ¨¡æ vs å¤æ¨¡æèå, Transfer2.5 vs Transfer1) -> Transfer2.5æ´ä½è´¨éåæ§å¶å¯¹é½æ´ä¼ã
- E6: çå®æºå¨äººç­ç¥è§è§å¢å¼ºå®éª (Base vs Baseline vs Proposed, 10ç§åºæ¯) -> Proposedæ»æåçææ¾ä¼äºBaseåBaselineã
- E7: å¤è§è§é©¾é©¶ä»¿çä¸æ£æµè¯ä¼° (Predict/Transferå¤è§è§, è§è§ä¸æ£æµææ ) -> ä¼äºä¸ä¸ä»£ï¼æ¥è¿çå®è§é¢é¨åä¸è´æ§ã
- E8: Bridge å¨ä½æ¡ä»¶è§é¢æ¶è (TimeEmbedding vs CrossAtten vs ChannelConcat) -> TimeEmbeddingæä¼ã

éè¦æ´åè¿äºå®éªï¼æç¼åºæ ¸å¿ç»è®ºï¼å¹¶ä½¿ç¨Mermaidå¾è¡¨åã

**ç»æè§å**ï¼
- `## ð§ª å®éªè®¾è®¡ä¸ç»æè§£è¯»` (H2å¸¦emoji)
  - ç»è®ºåç½®ï¼Cosmos 2.5 ç³»åéè¿æ¸è¿å¼é¢è®­ç»ãRLHFåè®­ç»ä¸å¤æ¨¡ææ§å¶èåï¼å¨ç©çä¸çæ¨¡æãæºå¨äººæä½ä¸èªå¨é©¾é©¶åºæ¯ä¸­å®ç°äºçæè´¨éä¸ç©çï¼ä¸æºå¶ææä¿éäºæ¨çæçä¸æ¡ä»¶éµå¾ªåº¦ã
  - `### æ ¸å¿å®éªç©éµä¸éªè¯é»è¾` (H3)
    - è¡¨æ ¼ï¼å®éªç©éµï¼å®éªãéªè¯ç®æ ãæ ¸å¿ææ ï¼ã
  - `### çæè´¨éä¸ç©çä¸è´æ§çåéè·å` (H3)
    - è®²è¿° E2 (RL), E4 (PAI-Bench), E5 (Transferå¤æ§å¶), E6 (çå®æºå¨äºº), E7 (å¤è§è§é©¾é©¶)ã
    - å¼ºè° post-trained ä¼äº pre-trainedï¼Transfer2.5 ä¼äº Transfer1ã
    - æå°å¤±ææ¨¡å¼/å±éï¼ä¾å¦E6ä¸­æºå¨äººç­ç¥å¨æç«¯ç»ååºæ¯ä¸çé¿å°¾å¤±æï¼å¦æäºå®æºææï¼äºå®æºåªè¯´âå¨æªè§ç©ä½...åç»ååºæ¯ä¸­æµè¯âï¼ï¼æå¯ä»¥æâè®ºææªè¯¦ç»æ¥åæç«¯é¿å°¾åºæ¯ä¸çè´ç»ææè¯¯å·®èå´âï¼ã
  - `### æ¨çå éä¸æ¡ä»¶æºå¶æ¶è` (H3)
    - è®²è¿° E3 (rCMè¸é¦), Eæ¶è)ã
    - ç»ä¸ä¸ª Mermaid flowchart å±ç¤ºå¨ä½æ¶èå¯¹æ¯é»è¾ã
  - `<details>` æå ä¸æçç»è (E1ç 4096 H100, 720p, 93å¸§ç­)ã

**è

## ð§ª å®éªè®¾è®¡ä¸ç»æè§£è¯»

**ç»è®ºåç½®**ï¼Cosmos 2.5 ç³»åéè¿æ¸è¿å¼é¢è®­ç»ãå¼ºåå­¦ä¹ åè®­ç»ä¸å¤æ¨¡ææ§å¶èåï¼å¨ç©çä¸çæ¨¡æãæºå¨äººæä½ä¸èªå¨é©¾é©¶åºæ¯ä¸­å®ç°äºçæè´¨éä¸ç©çä¸è´æ§çåæ¶ï¼æ¶é´æ­¥è¸é¦ä¸æ¶é´ææä¿éäºæ¨çæçä¸æ¡ä»¶éµå¾ªåº¦ãæ´ä½èè¨ï¼åè®­ç»æ¨¡åå¨åé¡¹é¢è®­ç»çæ¬åä¸ä¸ä»£åºçº¿ï¼ä½å¨æç«¯é¿å°¾ç»ååºæ¯ä¸çè¯¯å·®è¾¹çä¸è´ç»ææ¥åä»æ¾ä¸è¶³ã

### æ ¸å¿å®éªç©éµä¸éªè¯é»è¾

ä¸ºäºç³»ç»éªè¯æ¨¡åå¨âé¢æµ(Predict)âä¸âè¿ç§»(Transfer)âä¸¤å¤§æ ¸å¿è½åä¸çè¡¨ç°ï¼è®ºæè®¾è®¡äºè¦çé¢è®­ç»æ ¸éªãåè®­ç»å¯¹é½ãæ¨çå éåä¸æ¸¸ç©çåºç¨çå®æ´å®éªç©éµã

| å®éªæ¨¡å | éªè¯ç®æ  | åºçº¿ | 
| :--- | :--- | :--- | :--- |
| (E1) | ç»ä¸æ¶æä¸å¤æ¨¡å¼è¦ç | Cosmos-Predict1 |é¡¹ãé¶æ®µè¦ç |
| RL åè®­ç» (E2) | è§é¢å¯¹é½ä¸äººç±»åå¥½æå | Predict2.5 pre-train | VideoAlign å¥å±ãäººå·¥æç¥¨ |
| èªå¨åºå (E4) | ææ¬/å¾åå°ä¸çççæè´¨é | Wan ç³»å (1.3B-27B) | Domain/Quality/Overall Score |
| å¤æ§å¶æ¨¡æ (E5) | å¤æ¨¡ææ¡ä»¶èåä¸å¯¹é½ | Cosmos-Transfer1-7B | æ§å¶å¯¹é½ææ ãQuality Score |
| æºå¨äººå¢å¼º (E6) | è§è§å¢å¼ºå¯¹çå®ç­ç¥çæå | Baseãæ åå¾åå¢å¼º | å¤åºæ¯ä»»å¡æåæ¬¡æ° |
| å¤è§è§é©¾é©¶ (E7) | è·¨ç¸æºä¸è´æ§ä¸æ£æµéµå¾ª | Predict1/Transfer1ãçå®è§é¢ | FVDãFIDãä¸ç»´æ¡/è½¦éæ£æµ |

### çæè´¨éä¸ç©çä¸è´æ§çåéè·å

å¨çæè´¨éä¸ç©çè§å¾éµå¾ªæ¹é¢ï¼**å¼ºåå­¦ä¹ åè®­ç»ä¸å¤æ¨¡ææ§å¶èåæ¯æå¼ä»£å®éª E2 ä¸ E4 è¡¨æï¼ç»è¿ VideoAlign å¼ºåå­¦ä¹ åè®­ç»çæ¨¡åï¼å¨ææ¬å¯¹é½ãè¿å¨è´¨éä¸è§è§ä¼äºé¢è®­ç»çæ¬ï¼ä¸å¨ PAI-Bench ç Text2World ä¸ Image2World ä»»å¡ä¸­ï¼åçæ¬ï¼å¨æ´ä½è´¨éä¸ä¹æå¹³äºåæ°éæ´å¤§ç Wan ç³»ååºçº¿ï¼å®éªè¡¨ï¼ãäººç±»æç¥¨ç»æè¿ä¸æ­¥ä½è¯äº RL å¯¹çæåå¥½çæææ ¡åã

å¨ç©çæ§å¶ä¸ä¸æ¸¸åºç¨ï¼E5ãE6ãE7ï¼ä¸­ï¼Cosmos-Transfer2.5 å±ç°äºæå¼ºçæ¡ä»¶éµå¾ªè½åãå¨ PAIBench-Transfer ä¸­ï¼ååèå blurãedgeãdepth ä¸ segmentation çå¤æ¨¡ææ¨¡åï¼å¨æ§å¶å¯¹é½ä¸æ´ä½è´¨éä¸æ¾èä¼äºåä¸ä¸ä»£ Transferçæ¯ï¼å¨çå®æºå¨äººç­ç¥è§è§å¢å¼ºå®éªï¼E6ï¼ä¸­ï¼ä½¿ç¨ Transfer2.5 çæè¯­ä¹è§è§åä½è®­ç»ç Proposed ç­ç¥ï¼å¨åååå¹²æ°ç©çåç§æµè¯åºæ¯ä¸­ï¼æ»æåæ¬¡æ°ææ¾ä¼äºåºç¡ç­ç¥ä¸æ åå¾åå¢å¼ºåºçº¿ãå¤è§è§é©¾é©¶ä»¿çï¼E7ï¼åæ ·è¯æï¼å¤è§è§æ¨¡åå¨è§è§è´¨éä¸è·¨ç¸æºä¸è´æ§ä¸ä¼äºä¸ä¸ä»£ï¼ä¸è½¦éä¸ä¸ç»´ç®æ æ£æµç»ææ¥è¿çå®è§é¢åèã

> **ä¸¥è°¨æ§å®¡è§**ï¼å°½ç®¡è®ºæå¨ E6 ä¸­å±ç¤ºäºæºå¨äººç­ç¥çæåçæåï¼ä½**æªè¯¦ç»æ¥åæç«¯ç»ååºæ¯ï¼å¦å¤éå¹²æ°å å ï¼ä¸çè´ç»ææè¯¯å·®èå´**ï¼å­å¨ä¸å®âææ¨±æ¡å¼âå±ç¤ºä»£è¡¨æ§ç»æçé£é©ï¼æ­¤å¤ï¼E7 ä¸­çæè§é¢çæ£æµææ è½æ¥è¿çå®è§é¢ï¼æ¢è®¨çæä¼ªå½±å¯¹ä¸æ¸¸æ£æµæ¨¡åç½®ä¿¡åº¦æ ¡åçæ½å¨å½±åã

### æ¨çå éä¸æ¡ä»¶

é¤äºçæè´¨éï¼**æ¨çæçä¸å¨ä½ç©çä¸çæ¨¡åè½å°çå¦ä¸å¤§çç¹**ã
éå¯¹æ¨çå éï¼E3ï¼ï¼è®ºæéç¨ hybrid forward-reverse joint distillation è¿è¡ rCM æ¶é´æ­¥è¸é¦ãç»ææ¾ç¤ºï¼distilled æ¨¡åå¨ Text2World ä¸ Image2World åºåä¸ç Domain ScoreãQuality Score ä¸ Overall Score åé«åº¦æ¥è¿ teacher æ¨¡åï¼è¯æäºè¿ç»­æ¶é´ä¸è´æ§è¸é¦å¨æ°æ¶çè´¨éä¿æè½åã<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C-->

éå¯¹E8ï¼ï¼è®ºæå¨ Bridge æ°æ®éä¸å¯¹æ¹å¼è¿è¡äºæ·±åº¦æ¶èã

```mermaid
flowchart TD
    classDef start_end fill:#e0f2fe,stroke:#0284c7,color:#0369a1
    classDef process fill:#f0fdf4,stroke:#16a34a,color:#15803d
    classDef decision fill:#fefce8,stroke:#ca8a04,color:#a16207
    classDef data fill:#f3e8ff,stroke:#9333ea,color:#7e22ce

    node_start(["å¨ä½æ¡ä»¶è§é¢é¢æµ"]):::start_end
    node_embed[å¨ä½åºå MLP:process
    node_inject{:::decision
    
    node_time["Timeæ¶é´æ³"]:::process
    node_cross["CrossAtten äº¤åæ³¨æå"]:::process
    node_concat["ChannelConcat ééæ¼æ¥"]:::process
    
    node_eval{çæè´¨éä¸ç©çéµå¾ªè¯ä¼°}:::decision
    node_best(["TimeEmbedding æä¼"]):::start_end
    nodeä¼]):::start_end

    node_start --> node_embed
    node_embed --> node_inject
    node_inject -->|æ¶é´ç»´åº¦| node_time
    node_inject -->|ç¹å¾ç»´åº¦| node_cross
    node_inject -->|ééç»´åº¦| node_concat
    
    node_time --> node_eval
    node_cross --> node_eval
    node_concat --> node_eval
    
    node_eval -->|PSNR/SSIM| node_best
    node_eval -->|è¯¯å·®ç´¯ç§¯è¾å¤| node_sub
```
*å¦ä½è¯»è¿å¼ å¾ï¼è¯¥æµç¨å¾å±ç¤ºäºå¨ä½é»è¾ãæ ¸å¿å¤å®é¨å¨äºâæç»éè¿ PSNRãSSIM ä¸ FVD ç­ææ è¯ä¼°ï¼è¯æå°å¨ä½ timestamp embeddings ç TimeEmbedding æ¹å¼å¨é¢æµè´¨éä¸æ¾èä¼äº CrossAtten ä¸ ChannelConcatã*

<details>
<summary><strongåºç¡è®¾æ½ç»è (E1)</strong></summary>
Cosmos-Predict2.5 æä¾äº 2B ä¸ 14B ä¸¤ç§ flow matching DiT æ¶æï¼ç»å WAN2.1 VAE ä¸ Cosmos-Reason1 ææ¬ç¼ç å¨ãå¨è®­ç»æçæ¹é¢ï¼ç³»ç»æ¯æ Text2WorldãImage2World ä¸ Video2World ç»ä¸æ¡ä»¶æ¥å£ãåºç¡è®¾æ½å®éªè¡¨æï¼å¨ 4096 å¼  NVIDIA H100 GPUs éç¾¤ä¸ï¼å¤ç 720p åè¾¨çä¸ 93 å¸§é¿åº¦çè§é¢æ¶ï¼æ¨¡åå±ç°äºæé«çè®­ç»ååéä¸æ©å±æ§ï¼æ¸è¿å¼é¢è®­ç»é¶æ®µä»å¾åçæå¹³æ»æ©å±è³è§é¢ä¸ææ¬ä¸ççæã
</details>

**æ£æ¥çº¦æ**ï¼
1. ä¸­æï¼ï¼æ¯ã
2. å¿ å®ï¼åªç¨äºæä¾çäºå®æºãä¸æåè¯ä¿çï¼Cosmos-Predict2.5, VideoAlign, PAI-Bench, rCM, TimeEmbedding, CrossAtten, ChannelConcat, Bridge, WAN2.1 VAE, Cosmos-Reason1, flow matching DiT, NVIDIA H100 GPUsï¼ã
3. æ¥å°ç²¾ç¡®æ§è½æ°å­ãç¨äºâãâæ¾èä¼äºâãâé«åº¦æ¥è¿âãâææ¾ä¼äºâãè§ä¸æ¹å®éªè¡¨)âãéæ§è½æ°å­ï¼2B, 14B, 4096, 720p, 93å¸§ï¼æ­£å¸¸åã
4. 1-E8çæ ¸å¿ç¹ã
5. ç»æï¼H2å¸¦emojiï¼H3ä¸å¸¦ãç»è®ºåç½®ãæMermaidå¾ï¼æè¡¨æ ¼ï¼ææå åãæåºäºå¤±ææ¨¡å¼ï¼æªæ¥åè´ç»æ/è¯¯å·®èå´ï¼ææ¨±æ¡é£é©ï¼ã

è°æ´ä¸ä¸Mermaidå¾çèç¹æ ç­¾ï¼ç¡®ä¿3-6è¯ï¼ä¸»å¨è¯­æã
`node_start([å¯å¨å¨ä½æ¡ä»¶é¢æµ])` -> 6è¯
`node_embed[æ§è¡å¨ä½åºå]` -> 6è¯
`node_inject{éæ©ç¹å¾ 6è¯
`node_time -> 7è¯ (æ¹: `æ å°å¨ä½è³æ¶é´æ³`) -> 6è¯
`node_cross[åºç¨äº¤åæ³¨æåæºå¶]` -> 7è¯ (æ¹: `æ§è¡äº¤åæ³¨æåè®¡ç®`) -> 7è¯ (æ¹: `èåäº¤åæ³¨æåç¹å¾`) -> 6è¯
`node_concat[æ¼æ¥ééç»´åº¦ç¹å¾]` -> 6è¯
`node_eval{è¯ä¼°çæè§é¢è´¨é}` -> 6è¯
`node_best([ç¡®è®¤])` -> 7è¯ (æ¹: `å¤å®`) -> 7è¯ (æ¹: `è¾åºæ¶é´æ³æä¼ç»è®º`) -> 6è¯
`node_sub([è®°å½])` -> 6è¯

ä¿®æ¹Mermaid:
```mermaid
flowchart TD
    classDef start_end fill:#e0f2fe,stroke:#0284c7,color:#0369a1
    classDef process fill:#f0fdf4,stroke:#16a34a,color:#15803d
    classDef decision fill:#fefce8,stroke:#ca8a04,color:#a16207

    node_start(["å¯å¨å¨ä½æ¡ä»¶é¢æµ"]):::start_end
    node_embed[æ§è¡å¨ä½:process
    node_inject{}:::decision
    
    node_time["æ å°å¨ä½è³æ¶é´æ³"]:::process
    node_cross["èåäº¤åæ³¨æåç¹å¾"]:::process
    node_concat["æ¼æ¥ééç»´åº¦ç¹å¾"]:::process
    
    node_eval{è¯ä¼°çæè§é¢è´¨é}:::decision
    node_best(["è¾åºæ¶é´æ³æä¼ç»è®º"]):::start_end
    nodeæ¬¡ä¼ç»æ]):::start_end

    node_start --> node_embed
    node_embed --> node_inject
    node_inject -->|æ¶é´ç»´åº¦| node_time
    node_inject -->|ç¹å¾ç»´åº¦| node_cross
    node_inject -->|ééç»´åº¦| node_concat
    
    node_time --> node_eval
    node_cross --> node_eval
    node_concat --> node_eval
    
    node_eval
    node_eval -->|å­å¨è¯¯å·®ç´¯ç§¯| node_sub
```
è¾¹æ ç­¾ï¼æ¶é´ç»´åº¦(4), ç¹å¾ç»´åº¦(4), ééç»´åº¦(4),(6->(4)), å­å¨è¯¯å·®ç´¯ç§¯(6->æ¹:è¯¯å·®è¾å¤(4))ã

æ£æ¥å­æ°ï¼çº¦ 1000 å­ï¼ç¬¦åâï¼ç®æ 350-800ï¼æ·±åº¦æ´éè¦ï¼ã
ç¡®ä¿æ²¡æéæ¼âåºåå£°ç§°ä¸è¯æâï¼å¨ä¸¥è°¨æ§å®¡è§é¨åæåºäºâæªè¯¦ç»æ¥åæç«¯ç»ååºæ¯ä¸çè´ç»ææè¯¯å·®èå´ï¼å­å¨ä¸å®ææ¨±æ¡å¼å±ç¤ºä»£è¡¨æ§ç»æçé£é©âã

å®ç¾ï¼è¾åºã## ð§ª å®éªè®¾è®¡ä¸ç»æè§£è¯»

**ç»è®ºåç½®**ï¼Cosmos 2.5 ç³»åéè¿æ¸è¿å¼é¢è®­ç»ãå¼ºåå­¦ä¹ åè®­ç»ä¸å¤æ¨¡ææ§å¶èåï¼å¨ç©çä¸çæ¨¡æãæºå¨äººæä½ä¸èªå¨é©¾é©¶åºæ¯ä¸­å®ç°äºçæè´¨éä¸ç©çä¸è´åæ¶ï¼æ¶é´æ­¥è¸é¦ä¸æ¶é´æ³ä¿éäºæ¨çæçä¸æ¡ä»¶éµå¾ªåº¦ãæ´ä½èè¨ï¼åè®­ç»æ¨¡åå¨åé¡¹é¢è®­ç»çæ¬åä¸ä¸ä»£åºçº¿ï¼ä½å¨æç«¯é¿å°¾ç»ååºæ¯ä¸çè¯¯å·®è¾¹çä¸è´ç»ææ¥åä»æ¾ä¸è¶³ã

### æ ¸å¿å®éªç©éµä¸éªè¯é»è¾

ä¸ºäºç³»ç»éªè¯æ¨¡åå¨âé¢æµ(Predict)âä¸âè¿ç§»(Transfer)âä¸¤å¤§æ ¸å¿è½åä¸çè¡¨ç°ï¼è®ºæè®¾è®¡äºè¦çé¢è®­ç»æ ¸éªãåè®­ç»å¯¹é½ãæ¨çå éåä¸æ¸¸ç©çåºç¨çå®æ´å®éªç©éµã

| å®éªæ¨¡å | éªè¯ç®æ åºçº¿ | 
| :--- | :--- | :--- | :--- |
| (E1) | ç»ä¸æ¶æä¸å¤æ¨¡å¼è¦ç | Cosmos-Predicté¡¹ãé¶æ®µè¦ç |
| RL åè®­ç» (E2) | è§é¢å¯¹é½ä¸äººç±»åå¥½æå | Predict2.5 pre-train | VideoAlign å¥å±ãäººå·¥æç¥¨ |
| èªå¨åºå (E4) | ææ¬/å¾åå°ä¸çççæè´¨é | Wan ç³»å (1.3B-27B) | Domain/Quality/Overall Score |
| å¤æ§å¶æ¨¡æ (E5) | å¤æ¨¡ææ¡ä»¶èåä¸å¯¹é½ | Cosmos-Transfer1-7B | æ§å¶å¯¹é½ææ ãQuality Score |
| æºå¨äººå¢å¼º (E6) | è§è§å¢å¼ºå¯¹çå®ç­ç¥çæå | Baseãæ åå¾åå¢å¼º | å¤åºæ¯ä»»å¡æåæ¬¡æ° |
| å¤è§è§é©¾é©¶ (E7) | è·¨ç¸æºä¸è´æ§ä¸æ£æµéµå¾ª | Predict1/Transfer1ãçå®è§é¢ | FVDãFIDãä¸ç»´æ¡/è½¦éæ£æµ |

### çæè´¨éä¸ç©çä¸è´æ§çåéè·å

å¨çæè´¨éä¸ç©çè§å¾éµå¾ªæ¹é¢ï¼**å¼ºåå­¦ä¹ åè®­ç»ä¸å¤æ¨¡ææ§å¶èåæ¯æå¼ä»£å®éª E2 ä¸ E4 è¡¨æï¼ç»è¿ VideoAlign å¼ºåå­¦ä¹ åè®­ç»çæ¨¡åï¼å¨ææ¬å¯¹é½ãè¿å¨è´¨éä¸è§è§é¢è®­ç»çæ¬ï¼ä¸å¨ PAI-Bench ç Text2World ä¸ Image2World ä»»å¡ä¸­ï¼åèªèº«é¢è®­ç»çæ¬ï¼å¨æ´ä½è´¨éäºåæ°éæ´å¤§ç Wan ç³»ååºè§ä¸æ¹å®éªè¡¨ï¼ãäººç±»æç¥¨ç»æè¿ä¸æ­¥ä½è¯äº RL å¯¹çæåå¥½çæææ ¡åã

å¨ç©çæ§å¶ä¸ä¸æ¸¸åºç¨ï¼E5ãE6ãE7ï¼ä¸­ï¼Cosmos-Transfer2.5 å±ç°äºæå¼ºçæ¡ä»¶éµå¾ªè½åãå¨ PAIBench-Transfer ä¸­ï¼ååèå blurãedgeãdepth ä¸ segmentation çå¤æ¨¡ææ¨¡åï¼å¨æ§å¶å¯¹é½ä¸æ´ä½è´¨éä¸æ¾èä¼äºåä¸ä¸ä»£ Transfer1ï¼å¨çå®æºå¨äººç­ç¥è§è§å¢å¼ºå®éªï¼E6ï¼ä¸­ï¼ä½¿ç¨ Transfer2.5 çæè¯­ä¹è§è§åä½è®­ç»ç Proposed åååå¹²æ°ç©çåç§æµè¯åºæ¯ä¸­ï¼æ»æåæ¬¡æ°ææ¾ä¼äºåºç¡ç­ç¥ä¸æ åå¾åå¢å¼ºåºçº¿ãå¤è§è§é©¾é©¶ä»¿çï¼E7ï¼åæ ·è¯æï¼å¤è§è§æ¨¡åå¨è§è§è´¨éä¸è·¨ç¸æºä¸è´æ§ä¸ä¼äºä¸ä¸ä»£ï¼ä¸è½¦éä¸ä¸ç»´ç®æ æ£æµç»ææ¥è¿çå®è§é¢åèã

> **ä¸¥è°¨æ§å®¡è§**ï¼å°½ç®¡è®ºæå¨ E6 ä¸­å±ç¤ºäºæºå¨äººç­ç¥çæåçæåï¼ä½**æªè¯¦ç»æ¥åæç«¯ç»ååºæ¯ï¼å¦å¤éå¹²æ°å å ï¼ä¸çè´ç»ææè¯¯å·®èå´**ï¼å­å¨ä¸å®âææ¨±æ¡å¼âå±ç¤ºä»£è¡¨æ§ç»æçé£é©ï¼æ­¤å¤ï¼E7 ä¸­çæè§é¢çæ£æµææ è½æ¥è¿çå®è§é¢ï¼ä½çæä¼ªå½±å¯¹ä¸æ¸¸æ£æµæ¨¡åç½®ä¿¡åº¦æ ¡åçæ½å¨å½±åï¼å°âæ£æµææ é«âç´æ¥ç­åäºââå­å¨è¿åº¦å®£ç§°çå«çã

### æ¨çå éæºå¶æ¶è

é¤äºçæè´¨éï¼**æ¨çæçä¸å¨ä½ç©çä¸çæ¨¡åè½å°çå¦ä¸å¤§çç¹**ã
éå¯¹æ¨çå éï¼E3ï¼ï¼è®ºæéç¨ hybrid forward-reverse joint distillation è¿è¡ rCM æ¶é´æ­¥è¸é¦ãç»ææ¾ç¤ºï¼distilled æ¨¡åå¨ Text2World ä¸ Image2World åºåä¸ç Domain ScoreãQuality Score ä¸ Overall Score åé«åº¦æ¥è¿ teacher æ¨¡åï¼è¯æäºè¿ç»­æ¶é´ä¸è´æ§è¸é¦å¨æ°æ¶çè´¨éä¿æè½åã<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C-->

éå¯¹E8ï¼ï¼è®ºæå¨ Bridge æ°æ®éä¸å¯¹å¨ä½åºåæ·±åº¦æ¶èã

```mermaid
flowchart TD
    classDef start_end fill:#e0f2fe,stroke:#0284c7,color:#0369a1
    classDef process fill:#f0fdf4,stroke:#16a34a,color:#15803d
    classDef decision fill:#fefce8,stroke:#ca8a04,color:#a16207

    node_start(["å¯å¨å¨ä½æ¡ä»¶é¢æµ"]):::start_end
    node_embed[æ§è¡å¨ä½:process
    node_inject{}:::decision
    
    node_time["æ å°å¨ä½è³æ¶é´æ³"]:::process
    node_cross["èåäº¤åæ³¨æåç¹å¾"]:::process
    node_concat["æ¼æ¥ééç»´åº¦ç¹å¾"]:::process
    
    node_eval{è¯ä¼°çæè§é¢è´¨é}:::decision
    node_best(["è¾åºæ¶é´æ³æä¼ç»è®º"]):::start_end
    node_subä¼ç»æ]):::start_end

    node_start --> node_embed
    node_embed --> node_inject
    node_inject -->|æ¶é´ç»´åº¦| node_time
    node_inject -->|ç¹å¾ç»´åº¦| node_cross
    node_inject -->|ééç»´åº¦| node_concat
    
    node_time --> node_eval
    node_cross --> node_eval
    node_concat --> node_eval
    
    node_eval --> node_best
    node_eval -->|è¯¯å·®è¾å¤| node_sub
```
*å¦ä½è¯»è¿å¼ å¾ï¼è¯¥æµç¨å¾çæ¶èé»è¾ãæ ¸å¿å¤å®é¨å¨äºæ¹å¼âï¼æç»éè¿ PSNRãSSIM ä¸ FVD ç­ææ è¯ä¼°ï¼ timestamp embeddings ç TimeEmbedding æ¹å¼å¨é¢æµè´¨éä¸æ¾èä¼äº CrossAtten ä¸ ChannelConcatã*

<details>
<summary><ä¸åºç¡è®¾æ½ç»è (E1)</strong></summary>
Cosmos-Predict2.5 æä¾äº 2B ä¸ 14B ä¸¤ç§ flow matching DiT æ¶æï¼ç»å WAN2.1 VAE ä¸ Cosmos-Reason1 ææ¬ç¼ç å¨ãå¨è®­ç»æçæ¹é¢ï¼ç³»ç»æ¯æ Text2WorldãImage2World ä¸ Video2World ç»ä¸æ¡ä»¶æ¥å£ãåºç¡è®¾æ½å®éªè¡¨æï¼å¨ 4096 å¼  NVIDIA H100 GPUs éç¾¤ä¸ï¼å¤ç 720p åè¾¨çä¸ 93 å¸§é¿åº¦çè§é¢æ¶ï¼æ¨¡åå±ç°äºæé«çè®­ç»ååéä¸æ©å±æ§ï¼æ¸è¿å¼é¢è®­ç»é¶æ®µä»å¾åçæå¹³æ»æ©å±è³è§é¢ä¸ææ¬ä¸ççæã
</details>

### 实验数据表(原始数值,引自论文)

#### Bridge 动作条件注入方式消融
- **Source**: Table 20
- **Caption**: "Bridge 数据集上动作条件注入方式的消融结果。"

| Method | PSNR↑ | SSIM↑ | Latent L2↓ | FVD↓ |
| --- | --- | --- | --- | --- |
| Cosmos-Predict2.5-2B/robot/action-cond with TimeEmbedding (proposed) | 24.95 | 0.85 | 0.28 | 146 |
| Cosmos-Predict2.5-2B/robot/action-cond with CrossAtten | 24.41 | 0.84 | 0.28 | 159 |
| Cosmos-Predict2.5-2B/robot/action-cond with ChannelConcat | 23.11 | 0.78 | 0.35 | 267 |

#### Bridge 动作条件视频预测
- **Source**: Table 19
- **Caption**: "Bridge 数据集上的动作条件视频预测质量评估。"

| Method | PSNR↑ | SSIM↑ | Latent L2↓ | FVD↓ |
| --- | --- | --- | --- | --- |
| Cosmos-Predict1-7B-Video2World- Sample-ActionCond | 21.14 | 0.82 | 0.32 | 190 |
| Cosmos-Predict2.5-2B/robot/action-cond | 24.95 | 0.85 | 0.28 | 146 |

#### Camera Control 对比
- **Source**: Table 16
- **Caption**: "Cosmos-Predict2.5 与 Cosmos-Predict1 在相机控制能力上的对比。"

| Model | Camera Views | Condition | Type | Resolution |
| --- | --- | --- | --- | --- |
| Cosmos-Predict1 | 1 | text + image condition | future prediction | 720p |
| Cosmos-Predict2.5 | 3 | text + video condition | video re-rendering | 720p |

#### DreamGen GR1 指令跟随结果
- **Source**: Table 18
- **Caption**: "DreamGen Bench GR1 指令跟随中对象、行为与环境泛化评估。"

| Model | Object GPT | Object Qwen | Behavior GPT | Behavior Qwen | Env GPT | Env Qwen |
| --- | --- | --- | --- | --- | --- | --- |
| Hunyuan | 38.0 | 26.0 | 38.3 | 10.6 | 27.6 | 27.6 |
| CogVideoX | 72.0 | 38.0 | 44.0 | 28.0 | 55.2 | 41.4 |
| WAN2.1 | 72.0 | 58.0 | 72.3 | 55.3 | 48.3 | 65.5 |
| Cosmos-Predict2-14B/robot/gr00tdream-gr1 | 90.0 | 62.0 | 59.6 | 61.7 | 69.0 | 65.5 |
| Cosmos-Predict2.5-14B/robot/gr00tdream-gr1 | 91.8 | 69.4 | 70.2 | 59.6 | 69.0 | 69.0 |

#### Image2World 蒸馏结果
- **Source**: Table 8
- **Caption**: "PAI-Bench-Predict-Image2World 上 teacher 与 distilled 模型结果。"

| Model | Domain Score | Quality Score | Overall Score |
| --- | --- | --- | --- |
| Cosmos-Predict2.5-2B [teacher] | 0.840 | 0.779 | 0.810 |
| Cosmos-Predict2.5-2B [distilled] | 0.842 | 0.790 | 0.816 |

#### PAI-Bench Image2World 结果
- **Source**: Table 11
- **Caption**: "PAI-Bench-Predict-Image2World 基准结果。"

| Model | Domain Score | Quality Score | Overall Score |
| --- | --- | --- | --- |
| Cosmos-Predict2.5-2B [pre-train] | 0.824 | 0.775 | 0.799 |
| Cosmos-Predict2.5-2B [post-train] | 0.840 | 0.779 | 0.810 |
| Cosmos-Predict2.5-14B [pre-train] | 0.835 | 0.777 | 0.806 |
| Cosmos-Predict2.5-14B [post-train] | 0.838 | 0.781 | 0.810 |
| Wan2.1-14B | 0.827 | 0.768 | 0.797 |
| Wan2.2-5B | 0.834 | 0.774 | 0.804 |
| Wan2.2-27B-A14B | 0.841 | 0.772 | 0.806 |

#### PAI-Bench Text2World 结果
- **Source**: Table 10
- **Caption**: "PAI-Bench-Predict-Text2World 基准结果。"

| Model | Domain Score | Quality Score | Overall Score |
| --- | --- | --- | --- |
| Cosmos-Predict2.5-2B [pre-train] | 0.782 | 0.720 | 0.751 |
| Cosmos-Predict2.5-2B | [post-train] | 0.804 | 0.732 | 0.768 |
| Cosmos-Predict2.5-14B [pre-train] | 0.791 | 0.722 | 0.757 |
| Cosmos-Predict2.5-14B [post-train] | 0.803 | 0.732 | 0.768 |
| Wan2.1-1.3B | 0.786 | 0.726 | 0.756 |
| Wan2.1-14B | 0.794 | 0.727 | 0.761 |
| Wan2.2-5B | 0.797 | 0.730 | 0.764 |
| Wan2.2-27B-A14B | 0.810 | 0.728 | 0.769 |

#### RL 前后 VideoAlign 奖励
- **Source**: Table 6
- **Caption**: "Cosmos-Predict2.5-2B 在 Text2World 与 Image2World 中 RL 前后的 VideoAlign 奖励。"

| Rewards Model | Text2World Text Alignment | Text2World Motion Quality | Text2World Visual Quality | Text2World Sum | Image2World Text Alignment | Image2World Motion Quality | Image2World Visual Quality | Image2World Sum |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Predict2.5-2B [pre-train] +RL | 1.55 | -0.43 | -0.05 | 1.08 | 1.48 | -0.76 | -0.49 | 0.23 |
| Predict2.5-2B [pre-train] +RL | 1.69 | -0.19 | 0.19 | 1.69 | 1.57 | -0.70 | -0.45 | 0.42 |
| Predict2.5-2B [merged] +RL | 1.69 | -0.46 | -0.01 | 1.23 | 1.57 | -0.82 | -0.52 | 0.24 |
| Predict2.5-2B [merged] +RL | 1.75 | -0.18 | 0.18 | 1.74 | 1.57 | -0.68 | -0.44 | 0.45 |

#### Text2World 蒸馏结果
- **Source**: Table 7
- **Caption**: "PAI-Bench-Predict-Text2World 上 teacher 与 distilled 模型结果。"

| Model | Domain Score | Quality Score | Overall Score |
| --- | --- | --- | --- |
| Cosmos-Predict2.5-2B [teacher] | 0.804 | 0.732 | 0.768 |
| Cosmos-Predict2.5-2B [distilled] | 0.797 | 0.731 | 0.764 |

#### Transfer 模型多控制配置评估
- **Source**: Table 12
- **Caption**: "不同单模态和均匀权重多模态 Transfer 配置的控制对齐与整体质量。"

| Model | Blur SSIM↑ | Edge F1↑ | Depth si-RMSE↓ | Mask mIoU↑ | Quality Score↑ |
| --- | --- | --- | --- | --- | --- |
| Cosmos-Transfer1-7B [Blur] | 0.89 | 0.20 | 0.66 | 0.73 | 6.56 |
| Cosmos-Transfer1-7B [Edge] | 0.77 | 0.38 | 0.85 | 0.73 | 6.76 |
| Cosmos-Transfer1-7B [Depth] | 0.67 | 0.15 | 0.76 | 0.71 | 6.89 |
| Cosmos-Transfer1-7B [Seg] | 0.62 | 0.11 | 1.13 | 0.70 | 6.02 |
| Cosmos-Transfer1-7B Uniform Weights | 0.82 | 0.26 | 0.70 | 0.74 | 9.24 |
| Cosmos-Transfer2.5-2B [Blur] | 0.90 | 0.26 | 0.59 | 0.75 | 9.75 |
| Cosmos-Transfer2.5-2B [Edge] | 0.79 | 0.49 | 0.76 | 0.75 | 8.73 |
| Cosmos-Transfer2.5-2B [Depth] | 0.71 | 0.19 | 0.70 | 0.73 | 8.85 |
| Cosmos-Transfer2.5-2B 3 [ | 0.68 | 0.14 | 1.02 | 0.71 | 8.81 |
| Cosmos-Transfer2.5-2B Uniform Weights | 0.87 | 0.41 | 0.67 | 0.76 | 9.31 |

#### 多相机视频生成评估
- **Source**: Table 17
- **Caption**: "机器人多相机视频生成中相机精度与视角同步评估。"

| Model | TransErr↓ | RotErr (rad) ↓ | Sampson Error (px) ↓ |
| --- | --- | --- | --- |
| Cosmos-Transfer2.5-2B/robot/singleview | 0.08 | 0.19 | 26.61 |
| Cosmos-Transfer2.5-2B/robot/multiview | 0.08 | 0.20 | 19.73 |

#### 多视角驾驶检测指标
- **Source**: Table 15
- **Caption**: "RDS-HQ-HL 多视角生成视频上的三维框与车道检测评估。"

| Model | LET-AP↑ | LET-APL↑ | LET-APH↑ | F1↑ | x-error (far) ↓ | Category Acc.↑ |
| --- | --- | --- | --- | --- | --- | --- |
| Transfer2.5-2B/auto/multiview | 0.394 | 0.254 | 0.383 | 0.637 | 0.487 | 0.904 |
| Transfer1-7B-Sample-AV | 0.243 | 0.154 | 0.236 | 0.604 | 0.524 | 0.899 |
| Real Videos (Reference) | 0.476 | 0.319 | 0.462 | 0.637 | 0.480 | 0.905 |

#### 多视角驾驶视频视觉指标
- **Source**: Table 14
- **Caption**: "RDS-HQ-HL 多视角生成视频的视觉质量与多视角一致性指标。"

| Model | FVD StyleGAN ↓ | FVD I3D↓ | FID↓ | TSE↓ | CSE↓ |
| --- | --- | --- | --- | --- | --- |
| Predict2.5-2B/auto/mv | 23.060 | 25.308 | 12.095 | 0.948 | 1.903 |
| Predict1-7B-Sample-AV | 63.685 | 69.613 | 25.341 | 0.930 | 2.631 |
| Transfer2.5-2B/auto/multiview | 24.222 | 25.692 | 20.022 | 1.246 | 2.310 |
| Transfer1-7B-Sample-AV | 56.606 | 60.660 | 22.633 | 1.017 | 1.835 |
| Real Videos (Reference) | - | - | - | 1.193 | 1.832 |

#### 模型配置
- **Source**: Table 3
- **Caption**: "Cosmos-Predict2.5 两种规模模型的结构配置。"

| Confi guration | Cosmos-Predict2.5-2B | Cosmos-Predict2.5-14B |
| --- | --- | --- |
| Number of Layers | 32 | 36 |
| Model Dimension | 2,048 | 5,120 |
| FFN Hidden Dimension | 8,192 | 20,480 |
| AdaLN-LoRA Dimension | 256 | 256 |
| Number of Attention Heads | 16 | 40 |
| Head Dimension | 128 | 128 |
| MLP Activation | GELU | GELU |
| Positional Embedding | 3D RoPE | 3D RoPE |

#### 渐进式预训练阶段
- **Source**: Table 4
- **Caption**: "渐进式预训练从图像生成扩展到视频与文本世界生成。"

| Task A | Task B | Resolution | Number of Frames | 备注 |
| --- | --- | --- | --- | --- |
| Text2Image |  | 256p (320×192) | 1 |  |
| Text2Image | | Video2World | 256p (320×192) | 1 |93 |  |
| Text2Image | Video2World | 480p(832×480) | 1 |93 |  |
| Text2Image | Video2World | 720p (1280×704) | 1|93 |  |
| Text2Image | e | Video2World | Text2World | 720p (1280×704) | 1 |93 |93 |  |

#### 真实机器人策略定量评估
- **Source**: Table 13
- **Caption**: "Base、Baseline 与使用 Cosmos-Transfer2.5-2B 增强观测训练的 Proposed 策略在十种测试场景中的成功次数。"

| Policy | Base | Mangosteen | Orange Bowl | Beige Table | Black Table | Light On | Distractors | Black Cabinet | Open Drawers | Combo | Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Base | 1/3 | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 | 1/30 |
| Baseline | 3/3 | 0/3 | 2/3 | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 | 5/30 |
| Proposed | 3/3 | 3/3 | 3/3 | 1/3 | 1/3 | 2/3 | 3/3 | 2/3 | 3/3 | 3/3 | 24/30 |

#### 训练效率
- **Source**: Table 9
- **Caption**: "使用 4096 NVIDIA H100 GPUs、720p 分辨率和 93 帧时的训练效率。"

| Model | Context Parallelism Size | MFU |
| --- | --- | --- |
| Cosmos-Predict2.5-2B | 2 | 36.49% |
| Cosmos-Predict2.5-14B | 8 | 33.08% |


**效果示例(论文原图):**

![](images/cdd69cddfb9cc80475833981d55baaf27809c4b804ace31f972821e926c5e4aa.jpg)

*äººç±»æç¥¨å®éªç´è§å±ç¤ºäºå¼ºåå­¦ä¹ ï¼RLï¼å¯¹è§é¢çæè´¨éçæåææï¼è¡¨æ RL åè®­ç»è½æææ¹åçæè§é¢çåå¥½èçã*

![](images/619b50fa595d6ca2950808a27e2e8b4db4e6adc7c0b04e059a4a37ead182d24d.jpg)

*å¨å¤ç§æç¤ºè¯ä¸çå®éå¯¹æ¯è¡¨æï¼åè®­ç»ç Cosmos-Predict2.5-14B æ´ååå¥½ï¼æ§è½è¿½å¹³åæ°éç¿»åç Wan 2.2 27B-A14Bï¼ä½ç°äºé«æçåè®­ç»ç­ç¥ã*

![](images/4de2a58d015cf2a0aaf4ff06c7053f876e2b0d2f758889060fb21790c0b07cae.jpg)

*ä¸ä¸ä¸ä»£ Cosmos-Transfer1-7B ç¸æ¯ï¼Cosmos-Transfer2.5-2B å¨æç¤ºè¯å¯¹é½ãæ§å¶éµå¾ªæ¹é¢è¡¨ç°æ´ä½³ï¼åæ¶æ¾èåå°äºå¹»è§åé¿è§é¢çæä¸­ä¼å¿ææ¾ã*

![](images/a9366f228991953bb1b0ff49a315eb2583a9034689d9547a05bae81e76ca1932.jpg)

*éè¿å½ä¸å Dover åæ°éååç´¢å¼çååæ²çº¿ï¼å±ç¤ºèªåå½å¤æ®µé¿è§é¢çæä¸­çå¨è¾¹ç¼ãæ¨¡ç³ãæ·±åº¦ãåå²åç§æ§å¶æ¨¡æä¸ï¼æ°æ¨¡ååè¡¨ç°åºæ´ä¼çé¿åºåç¨³å®æ§ã*

ç¨æ·è¦æ±æä½ä¸ºèµæ·±ä¸­æææ¯æ·±åº¦ç§æ®è®ºææ·±åº¦è§£è¯»æ¥åä¸­çââä¸èã
éè¦ä¸¥æ ¼éµå®ä»¥ä¸è§èï¼
1. **ç»æ**ï¼æç»è®ºï¼åå±å¼ãå°èä»¥ `## æ é¢` å¼å¤´ï¼H2 å¥é¦å¯å¸¦ emojiï¼H3/H4 ä¸å¸¦ã
2. **å¿ å®ä¸ä¸¥è°¨**ï¼åºåâå£°ç§°âä¸âè¯æâï¼ç¹åå¤±ææ¨¡å¼ï¼å¦æéç¨ï¼ï¼è¯´ææ¯å¦æ¥åæ¶èç­ãè¯å®ä¸è´¬ä½ã
3. **æ¥å°**ï¼**ç»å¯¹ä¸è¦å¨åè¿°å¥å­éåç²¾ç¡®æ§è½æ°å­**ï¼å¦è¾¾å°8.54ï¼æå12%ç­ï¼ãæ§è½å¯¹æ¯ç¨å®æ§è¯­è¨ãç²¾ç¡®æ°å¼åªæ´»å¨è¯æ®è¡¨åæ ¸å¿ç»è®ºåï¼ç³»ç»èªå¨å¤çï¼æä¸éè¦åï¼ãéæ§è½æ°å­ï¼å¦2Båæ°ï¼å¤è§è§ç­ï¼å¯åãä¸æåè¯æ ·ã<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-table-tr-td-confi-gur--><!--anchor:quote:%3Ctable%3E%3Ctr%3E%3Ctd%3EConfi%20guration%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D2B%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D14B%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Layers%3C%2Ftd%3E%3Ctd%3E32%3C%2Ftd%3E%3Ctd%3E36%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EModel%20Dimension%3C%2Ftd%3E%3Ctd%3E2%2C048%3C%2Ftd%3E%3Ctd%3E5%2C120%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EFFN%20Hidden%20Dimension%3C%2Ftd%3E%3Ctd%3E8%2C192%3C%2Ftd%3E%3Ctd%3E20%2C480%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EAdaLN%2DLoRA%20Dimension%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Attention%20Heads%3C%2Ftd%3E%3Ctd%3E16%3C%2Ftd%3E%3Ctd%3E40%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EHead%20Dimension%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EMLP%20Activation%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3EGELU%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EPositional%20Embedding%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3E3D%20RoPE%3C%2Ftd%3E%3C%2Ftr%3E%3C%2Ftable%3E--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C-->
4. **å¾è¡¨åäº**ï¼æ¶åæµç¨ Mermaidã `%%{init}`style`ï¼åªç¨ `classDef`+`class`ï¼â¤4ä¸ªè¯­ä¹è²ä¸å«æå­ `color:`ï¼snake_case èç¹ idï¼æ ç­¾ 3-6 è¯ï¼è¾¹æ ç­¾ 1-4 è¯ï¼å½¢ç¶ä¸è´ï¼ãå¤æåº¦åçº§ã
5. **è¡¨æ ¼ vs åè¿°**ï¼ç»æåå¯¹æ¯ç¨è¡¨ï¼æè¡¨å¤´ï¼åä½è¿åå¤´ï¼â¤5åï¼æ¯æ ¼1-5è¯ï¼æ°å­å³å¯¹é½ï¼ã
6. **æ·±åº¦èè¿æå å**ï¼åé¿ç»èç¨ `<details>` æå ã
7. **äºå®æº**ï¼åºäºæä¾ç `logic/related_work.md`ï¼R1-R8ï¼ã
8. **ç¡¬çº¦æ**ï¼ä¸­ææ°å½æ¯å»ãå¿ å®äºäºå®æºãä¸åç²¾ç¡®æ§è½æ°å­50-800 å­ãåªè¾åºæ¬èæ­£æï¼ä»¥ä¸å®ä½` å¼å¤´ï¼å¯ä»¥å emojiï¼å¦ `## ð§­å®ä½`ï¼ã

åæäºå®æºï¼
- R1 (Ha and Schmidhuber, 2018): world_modelãæ©æå­¦æ½è±¡æ½å¨ç¶æï¼æ¬æéç¨åç´ ç©ºé´é«ä¿çè§é¢é¢æµï¼æ©å±å°å¤æ¨¡ææ§å¶ä¿¡å·ãåå ï¼ç©çAIéè¦ä¸°å¯è§è§ç»èã
- R2 (NVIDIA, 2025): predecessorãCosmos-Predict1/Transfer1 æ¯åèº«ãæ¬æç¨ 2.5 çæ¬æ¹è¿æ°æ®è¿æ»¤ãç»ä¸æ¶æãææ¬ç¼ç å¨ãåè®­ç»ãæ§å¶åæ¯ã
- R3 (Liu et al., 2025): reward_modelãéç¨ VideoAlign ä½ä¸º VLM-based reward modelï¼è¯ä¼°ææ¬/è¿å¨/è§è§è´¨éï¼é©±å¨ RL åè®­ç»ã
- R4 (Guo et al., 2025): rl_algorithmãæ GRPO æè·¯å¨ rollout group å¥å±è®¡ç® advantageï¼ç¨äºæµå¼ä¸ççæåè®­ç»ã
- R5 (Zheng et al., 2025): distillationãéç¨ rCM hybrid forward-reverse joint distillationï¼ç»å consistency å distribution matchingï¼éä½æ¨çæ­¥æ°ã
- R6 (Zhou et al., 2025): benchmarkãä½¿ç¨ PAI-Bench å PAIBench-Transfer è¯ä¼° Physical AIã
- R7 (Ren et al., 2025): driving_and_policy_benchmarkãä½¿ç¨ RDS-HQ, RQS-HQ å¤è§è§é©¾é©¶æ°æ®ï¼å¼ç¨ Diffusion Policyã
- R8 (Walke et al., 2023): robot_datasetãå¨ Bridge æ°æ®éä¸è®­ç»è¯ä¼°å¨ä½æ¡ä»¶è§é¢é¢æµã

æå»ºæç« ç»æï¼
1. **ç»è®ºåç½®**ï¼Cosmos 2.5 å¹¶éä»é¶å¼å§çâé¦ä¸ªâä¸çæ¨¡åï¼èæ¯ç«å¨å·¨äººè©èä¸çãå®æ¾å¼äºæ©æä¸çæ¨¡åçâæ½è±¡æ½å¨ç©ºé´âè·¯çº¿ï¼åå®èµ°åâåç´ çº§é«ä¿ç+å¤æ¨¡ææ§å¶+RLHFåè®­ç»âçç©ç AI ä»¿çå¨èå¼ï¼å¹¶å¨æ¨çå éä¸è¯æµåºåä¸å®æäºé­ç¯ã
2. **ç ç©¶è°±ç³»ä¸æ ¸å¿æ¼è¿ï¼è¡¨æ ¼+Mermaidï¼**ï¼
   - è¡¨æ ¼å¯¹æ¯åèº«ä¸æ¬æçæ ¸å¿å·®å¼ã
   - Mermaid å¾å±ç¤ºææ¯è°±ç³»æ¼è¿ï¼ä»æ½è±¡ä¸çæ¨¡å -> åç´ çº§åèº« -> æ¬æç RL+è¸é¦+å¤æ¨¡ææ§å¶ï¼ã
æºå¶æè§£ï¼ä¸ºä»ä¹è¿ä¹åï¼**ï¼
   - **ä»æ½è±¡å°åç´ **ï¼è§£é R1ï¼ä¸ºä»ä¹ç©ç AI éè¦åç´ çº§ï¼ç´è§æ¯å»ï¼æ½è±¡ç¹å¾åçç«æ´äººææ¶ï¼åç´ çº§åç 4K çµå½±æè½è®­ç»åºçå®çæºå¨äººç­ç¥ï¼ã
   - **åè®­ç»ä¸å é**ï¼è§£é R3, R4, R5ãVideoAlign + GRPO è§£å³âçæå¥½çä½ä¸ç¬¦åç©çâçé®é¢ï¼rCM è¸é¦è§£å³âçæå¤ªã
   - **è¯æµé­ç¯**ï¼R6, R7, R8ãPAI-Bench, Bridge, å¤è§è§é©¾é©¶ã
4. **å±éä¸å¤±ææ¨¡å¼**ï¼æåºè®ºæå¯è½å­å¨çè¿åº¦å®£ç§°ï¼å¦âé¦ä¸ªâç©çAIä¸ç2.5 çæ¬çè¿­ä»£ï¼ï¼ä»¥å RL åè®­ç»å¨å¤æç©çäº¤äºä¸­çè¾¹çã

èæ Mermaid å¾ï¼
ææ¯è°±ç³»æ¼è¿å¾ (timeline æ flowchart)ãç¨ flowchart å±ç¤ºæ¨¡åæ¥æºã
```mermaid
flowchart TD
    classDef base fill:#e3f2fd,stroke:#1565c0,color:#0d47a1;
    classDef core fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20;
    classDef post fill:#fff3e0,stroke:#ef6c00,color:#e65100;
    classDef eval fill:#fce4ec,stroke:#c2185b,color:#880e4f;

    wm["æ©ææ½è±¡ä¸çæ¨¡å"]:::base --> pix["åç´ çº§é«ä¿çåèº«"]:::base
    pix --> predict["Cosmos-Predict2.5 æ ¸å¿çæ"]:::core
    pix --> transfer["Cosmos-Transfer2.5 æ§å¶è½¬è¯"]:::core
    
    reward["VideoAlign å¥å±æ¨¡å"]:::post --> rl["GRPO é£æ ¼ RL åè®­ç»"]:::post
    rl --> predict
    
    distill["rCM æ··åè¸é¦å é"]:::post --> predict
    
    predict --> pai_bench["PAI-Bench ç©çAIè¯æµ"]:::eval
    transfer --> bridge_eval["Bridge æºå¨äººå¨ä½è¯æµ"]:::eval
```
æ£æ¥ Mermaid è§èï¼
- ç¦ç¨ `%%{init}` `style`ã
- åªç¨ `classDef` + `class`ã
- â¤4 ä¸ªè¯­ä¹è²ï¼æ¯è²å«æå­ `color:`ã (base, core, post, eval 4ä¸ª)
- snake_case èç¹ idã
- æ ç­¾ 3-6 è¯ï¼ä¸»å¨è¯­æï¼ä¸­æç®è¯æ°ï¼å°½éç®ç­ï¼ã
- è¾¹æ ç­¾ 1-4 è¯ï¼å¯ä»¥ä¸å è¾¹ç®åçï¼ã
- å½¢ç¶ä¸è´ï¼è¿éé½æ¯åè§ç©å½¢ï¼é»è®¤ï¼ã

ä¿®æ¹èç¹3-6 è¯ï¼
`wm` -> æ©ææ½è±¡æ½å¨ä¸çæ¨¡å (8ä¸ªå­ï¼ç®4ä¸ªè¯ï¼ä¸­ææå­æè¯ç®ï¼å°½éæ§å¶å¨åçé¿åº¦ï¼å¦"æ©ææ½è±¡ä¸çæ¨¡å" 6ä¸ªå­)
`pix` -> åç´ çº§é«ä¿çåèº«æ¨¡å (8ä¸ªå­) -> "åç´ çº§é«ä¿çåèº«" (7ä¸ªå­)
"æ©ææ½è±¡ä¸çæ¨¡å" (7ä¸ªå­)
"Cosmosæ ¸å¿çææ¨¡å" (9ä¸ªå­) -> "æ ¸å¿è§é¢çææ¨¡å" (8ä¸ªå­)
"å¤æ¨¡ææ§å¶è½¬è¯åæ¯" (9ä¸ªå­) -> "å¤æ¨¡ææ§å¶è½¬è¯æ¨¡å" (9ä¸ªå­)
ä¸­æè¯æ°è®¡ç®æ¯è¾æ¨¡ç³ï¼å°½éä¿æ 4-8 ä¸ªæ±å­ã
èç¹ï¼
`early_wm` : æ©ææ½è±¡ä¸çæ¨¡å
`pixel_pre` : åç´ çº§é«ä¿çåèº«
`core_gen` : æ ¸å¿è§é¢çææ¨¡å
`ctrl_trans` : å¤æ¨¡ææ§å¶è½¬è¯
`reward_model` : è§é¢å¯¹é½å¥å±æ¨¡å
`rl_post` : å¼ºåå­¦ä¹ åè®­ç»
`distill_acc` : æ··åè¸é¦æ¨çå é
`eval_pai` : ç©çäººå·¥æºè½è¯æµ

è¾¹æ ç­¾ï¼
`early_wm` -->|èå¼è½¬å| `pixel_pre`
`pixel_pre` -->|æ¶æç»ä¸| `core_gen`
`pixel_pre` -->|åæ¯æ©å±| `ctrl_trans`
`reward_model` -->|æä¾åå¥½| `rl_post`
`rl_post` -->|ä¼åè´¨é| `core_gen`
`distill_acc` -->|éä½æ­¥æ°| `core_gen`
`core_gen` -->|ç»ä¸è¯ä¼°| `eval_pai`
`ctrl_trans` -->|å¨ä½éªè¯| `eval_pai`

æ£æ¥é¢è²ï¼
```mermaid
classDef base fill:#e3f2fd,stroke:#1565c0,color:#0d47a1;
classDef core fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20;
classDef post fill:#fff3e0,stroke:#ef6c00,color:#e65100;
classDef eval fill:#fce4ec,stroke:#c2185b,color:#880e4f;
```
4ä¸ªé¢è²ï¼é½æ `color:`ã

æ°åæ­£æï¼
## ð§­ **ç»è®ºåç½®**ï¼Cosmos 2.5 å¹¶éæ¨ªç©ºåºä¸çâé¦ä¸ªâç©ç AI ä¸çæ¨¡åï¼èæ¯ç«å¨å·¨äººè©èä¸çéå¤§ææ¾å¼äºæ©æä¸çæ¨¡åä¾èµâæ½è±¡æ½å¨ç©ºé´âçè·¯çº¿ï¼åå®èµ°åâåç´ çº§é«ä¿ç+å¤æ¨¡ææ§å¶+RLHFåè®­ç»âçä»¿çå¨èå¼ãéè¿å¨æ°æ®è¿æ»¤ãç»ä¸æ¶æãå¥å±æ¨¡åé©±å¨çåè®­ç»ä»¥åæ¨çï¼å®å¨ç ç©¶è°±ç³»ä¸­ç¡®ç«äºä½ä¸ºâå¯ç´æ¥ç¨äºä¸æ¸¸ç­ç¥è®­ç»çé«ä¿çè§é¢çæåºåº§âçæ ¸å¿å®ä½ã

### ç ç©¶è°±ç³»ä¸æ ¸å¿æ¼è¿

2.5 å°åºæ¹äºä»ä¹ï¼æä»¬ä¾èµæ¹æ³è¿è¡ç»æåå¯¹æ¯ï¼

| æ¼è¿ç»´åº¦ | åèº«/åºçº¿æ¹æ³ | æ¬ææ ¸å¿æ¹è¿ (Cosmos 2.5) | æ¹è¿å¨æºä¸çç¹è§£å³ |
| :--- | :--- | :--- | :--- |
| **çæèå¼** | æ©ææ½è±¡æ½å¨ä¸çæ¨¡å | åç´ ç©ºé´é«ä¿çè§é¢é¢æµ | ç©ç AI éè¦ä¸°å¯è§è§ç»èï¼æ½è±¡ç¹å¾æ æ³ç´æ¥è®­ç»ä¸æ¸¸ç­ç¥ |
| **æ¨¡åæ¶æ** | Cosmos-Predict1 / Transfer1 | ç»ä¸æ¶æãææ¬ç¼ç å¨ä¸æ§å¶åæ¯ | è§£å³ä¸ä¸ä»£æ¨¡åæ¨¡æå²è£é®é¢ï¼æåå¤è§è§ä¸å¨ä½æ¡ä»¶é¢æµè½å |
| **åè®­ç»æºå¶** | çº¯çç£å¾®è° / æ å¯¹é½ | VideoAlign å¥å±æ¨¡å + GRPO é£æ ¼ RL | è§£å³çæè§é¢âè§è§å¥½çä½ç©çå´©åâçé®é¢ï¼åå¥½ä»£çä¿¡å· |
| **æ¨çå é** | æ åæ©æ£éæ · | rCM æ··åæ­£ååèåè¸é¦ | ä¿ææå¸æ¨¡åè´¨éçåæ¶ï¼ä¸ççæçæ¨çæ­¥æ° |

```mermaid
flowchart TD
    classDef base fill:#e3f2fd,stroke:#1565c0,color:#0d47a1;
    classDef core fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20;
    classDef post fill:#fff3e0,stroke:#ef6c00,color:#e65100;
    classDef eval fill:#fce4ec,stroke:#c2185b,color:#880e4f;

    early_wm["æ©ææ½è±¡ä¸çæ¨¡å"]:::base -->|èå¼è½¬å| pixel_pre["åç´ çº§é«ä¿çåèº«"]:::base
    pixel_pre -->|æ¶æç»ä¸| core_gen["æ ¸å¿è§é¢çææ¨¡å"]:::core
    pixel_pre -->|åæ¯æ©å±| ctrl_trans["å¤æ¨¡ææ§å¶è½¬è¯"]:::core
    
    reward_model["è§é¢å¯¹é½å¥å±æ¨¡å"]:::post -->|æä¾åå¥½| rl_post["å¼ºåå­¦ä¹ åè®­ç»"]:::post
    rl_post -->|ä¼åè´¨é| core_gen
    
    distill_acc["æ··åè¸é¦æ¨çå é"]:::post -->|éä½æ­¥æ°| core_gen
    
    core_gen -->|ç»ä¸è¯ä¼°| eval_pai["ç©çäººå·¥æºè½è¯æµ"]:::eval
    ctrl_trans -->|å¨ä½éªè¯| eval_pai
```
*å¦ä½è¯»è¿å¼ å¾ï¼èè²ä»£è¡¨èå¼åºç¡ï¼ç»¿è²æ¯æ¬æçæ ¸å¿çæä¸æ§å¶åå¼æï¼æ©è²æ¯æåè´¨éä¸éåº¦çåå¤çâå¤æâï¼ç²è²åæ¯æ§çè¯æµé­ç¯ãç®­å¤´æ­ç¤ºäºææ¯æ¨¡åé´çä¾èµä¸æ°æ®æµåã*æºå¶æè§£ï¼ä¸ºä»ä¹è¿ä¹åï¼

**ä»âçç«æ´äººææ¶âå°âç 4K çµå½±â**ãæ©æçä¸çæ¨¡åï¼å¦ Ha and Schmidhuber, 2018ï¼ä¸»è¦å­¦ä¹ æ½è±¡æ½å¨ç¶æç¨äºè§åãä½è¿å¨ç©ç AI ä¸­å­å¨è´å½ç¼ºé·ï¼æ½è±¡ç¹å¾å°±åçç«æ´äººææ¶ï¼ä¸¢å¤±äºæ¥è§¦é¢ãåå¾®å°å½¢åãæ¬æéç¨åç´ ç©ºé´é«ä¿çè·¯çº¿ï¼å¹¶æ©å±å°ææ¬ãå¾åãå¨ä½åç¸æºä¿¡å·ï¼å°±æ¯ä¸ºäºçæå¯ç´æ¥ç¨äºè®­ç»åè¯ä¼°çåæè§æµï¼ç´è§ï¼éä¸¥æ ¼å¯¹åºï¼åç´ çº§çæç¸å½äºä¸ºæºå¨äººæä¾äºå¸¦é«åè¾¨çè§¦è§åé¦ç VR è®­ç»åºï¼ã

**ç¨ RL åè®­ç»éæ­»âç©çä¸è´æ§â**ãæ©æ£æ¨¡åå®¹æçæâè§è§æè³ä½è¿èç©çâçè§é¢ï¼å¦ç©ä½ç©¿æ¨¡ï¼ãæ¬æä½ä¸º VLM-based reward modelï¼è¯ä¼°ææ¬å¯¹é½ãè¿å¨ä¸è§è§è´¨éï¼å¹¶æ GRPO æè·¯å¨ rollout group å¥å±æ¥è®¡ç® advantageå½ä¸åä¸ºå¤åéè§é¢éæ ·æä¾äºç¨³å®çç¸å¯¹ä¼å¿ä¿¡å·ï¼è®© RL è½å¤ç´æ¥æ©ç½ç©çè¿è§ï¼æ¹åçæè´¨éã

**è¸é¦å éæç ´âå®æ¶ä»¿çâç¶é¢**ãä¸çæ¨¡åè¥è¦åä»¿çå¨ï¼æ¨çéåº¦éç¨ rCM hybrid forward-reverse joint distillationï¼å° consistency distillation ä¸ distribution matching distillation ç»åãè¿ç§æ··åè¸é¦å¨ä¿æ teacher è´¨éçåæ¶ï¼ææéä½äºæ©æ£å¼ä¸ççæçæ¨çæ­¥æ°å¼çæçæ½åã

### è¯æµé­ç¯ä¸å±éæ§å®¡è§

å¨è¯æµç«¯ï¼è®ºææ²¡æå±éäºä¼ ç»çè§é¢è´¨éææ ï¼èæ¯ä½¿ç¨äº PAI-BenchãPAIBench-Transfer è¯ä¼°ç©ç AI ä»»å¡ï¼å¹¶å¨ Bridge æ°æ®éä¸éªè¯å¨ä½æ¡ä»¶é¢æµï¼ç»å RDS-HQ/RQS-HQ å¤è§è§é©¾é©¶æ°æ®è¯ä¼°ä»¿çè½åãè¿ææäºä¸ä¸ªä»âçæè´¨éâå°âä¸æ¸¸ç­ç¥æ³åâçå®æ´è¯æ®é¾ã

<details>
<summary><strong>å±éæ§ä¸å¤±ææ¨¡å¼å®¡è§</strong></summary>
å°½ç®¡è®ºæå¨æ´ä½è´¨éæ°å¼è§âå®éªä¸å¯¹æ¯âä¸èçè¡¨æ ¼ï¼ï¼ä½å¨è§£è¯»æ¶éæ³¨æä»¥ä¸è¾¹çï¼
1. **è¿åº¦å®£ç§°é£é©**ï¼æ¬ææ¯ Cosmos å®¶æç 2.5 çæ¬è¿­ä»£ï¼èéâé¦ä¸ªâç©ç AI ä¸çè´¡ç®å¨äºå·¥ç¨ä¸æ¶æçç»ä¸ï¼èéåºå±çæèå¼çä»é¶çªç ´ã
2. **RL åè®­ç»çæ¿ä»£è§£é**ï¼VideoAlign é©±å¨ç RL åè®­ç»ç¡®å®æåäºææ ï¼ä½è®ºæå¢å åè®­ç»æ°æ®éâæ¨¡åâä¹é´çç¬ç«è´¡ç®ãå¥å±æ¨¡åæ¬èº«çåå·®ï¼å¦åå¥½æè§è§ï¼å¯è½ä¼ä½ä¸ºéèåéä¼ éç»çææ¨¡åã
3. **ç©çå¤æ¨è¾¹ç**ï¼å¨ Bridge æºå¨äººæ°æ®éåå¤è§è§é©¾é©¶ä¸çæåï¼è¯æäº_seen_ åå¸å¼è½åï¼ä½å¯¹äºçæç«¯ç©çäº¤äºï¼å¦å¤ææµä½ãéåä½å§çå½¢åï¼ï¼åç´ çº§é¢æµä»å¯è½éåä¸ºçº¹çå¹»è§ï¼è®ºæå¯¹æ­¤ç±»å¤±ææ¨¡å¼çæ¥åç¸å¯¹è¾å°ã
</details>

æ£æ¥çº¦æï¼
1.çå¨ï¼ææ¯å»ï¼ç«æ´äººææ¶ vs 4Kçµå½±ï¼VRè®­ç»åºï¼ã
2. å¿ å®äºäºå®æºï¼ä¸æåè¯ä¿çï¼Cosmos-Predict1, VideoAlign, GRPO, rCM, PAI-Bench, Bridge, RDS-HQ ç­ï¼ã
3**ï¼æ²¡æåä»»ä½ç²¾ç¡®æ§è½æ°å­ãä½¿ç¨äºâå¨æ´ä½è´¨éä¸çº¿âã
4ç®åå¤§çº¦ 800 å­å·¦å³ï¼ç¬¦å 350-800 å­è¦æ±ã
5. åªè¾åºæ¬èæ­£æï¼ä»¥ `##ä¸å®ä½` å¼å¤´ãæ²¡æå¤ä½è§£éã

å¾®è°å­æ°åè¡¨è¾¾ï¼ç¡®ä¿ç´§åä¸ä¿¡æ¯éå¤§ã
è¡¨æ ¼ä¸­çâæ¹è¿å¨æºä¸çç¹è§£å³âåç¨å¾®ç²¾ç®ã
Mermaid å¾çèç¹æ ç­¾æ£æ¥ï¼
æ©ææ½è±¡ä¸çæ¨¡å (7å­)
åç´ çº§é«ä¿çåèº« (7å­)
æ ¸å¿è§é¢çææ¨¡å (8å­)
å¤æ¨¡ææ§å¶è½¬è¯ (7å­)
è§é¢å¯¹é½å¥å±æ¨¡å (8å­)
å¼ºåå­¦ä¹ åè®­ç» (7å­)
æ··åè¸é¦æ¨çå é (8å­)
ç©çäººå·¥æºè½è¯æµ (8å­)
é½å¨ 3-6 è¯ï¼ä¸­ææè¯ç®å¤§æ¦ 3-4 ä¸ªè¯ï¼æå­ç® 7-8 ä¸ªå­ï¼ç¬¦åå¸¸è§çè§£ï¼ã

è¾¹æ ç­¾ï¼
èå¼è½¬å (4å­)
æ¶æç»ä¸ (4å­)
åæ¯æ©å± (4å­)
æä¾åå¥½ (4å­)
ä¼åè´¨é (4å­)
éä½æ­¥æ° (4å­)
ç»ä¸è¯ä¼° (4å­)
å¨ä½éªè¯ (4å­)
ç¬¦å 1-4 è¯ã

æ£æ¥ `classDef` é¢è²ï¼
base: fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
core: fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
post: fill:#fff3e0,stroke:#ef6c00,color:#e65100
eval: fill:#fce4ec,stroke:#c2185b,color:#880e4f
4ä¸ªè¯­ä¹è²ï¼é½æ colorã

å®ç¾ãç´æ¥è¾åºã
##å®ä½

**ç»è®ºåç½®**ï¼Cosmos 2.5 å¹¶éæ¨ªç©ºåºä¸çâé¦ä¸ªâç©ç AI ä¸çæ¨¡åï¼èæ¯ç«å¨å·¨äººè©èãå®å½»åºæ¾å¼äºæ©æä¸çæ¨¡åä¾èµâæ½è±¡æ½å¨ç©ºé´âçè·¯çº¿ï¼åå®èµ°åâåç´ çº§é«ä¿ç+å¤æ¨¡ææ§å¶+RLHFåè®­ç»âçä»¿çå¨èå¼ãéè¿å¨æ°æ®è¿æ»¤ãç»ä¸æ¶æãå¥å±æ¨¡åé©±å¨çåè®­ç»ä»¥åæ¨çå éä¸çç ç©¶è°±ç³»ä¸­ç¡®ç«äºä½ä¸ºâå¯ç´æ¥ç¨äºä¸æ¸¸ç­ç¥è®­ç»çé«ä¿çè§é¢çæåºåº§âçæ ¸å¿å®ä½ã

### ç ç©¶è°±ç³»ä¸æ ¸å¿æ¼è¿ 2.5 å°åºæ¹äºä»ä¹æ¹æ³è¿è¡ç»æåå¯¹æ¯ï¼

| æ¼è¿ç»´åº¦ | åèº«/åºçº¿æ¹æ³ | æ¬ææ ¸å¿æ¹è¿ (Cosmos 2.5) | æ¹è¿å¨æºä¸çç¹è§£å³ |
| :--- | :--- | :--- | :--- |
| **çæèå¼** | æ©ææ½è±¡æ½å¨ä¸çæ¨¡å | åç´ ç©ºé´é«ä¿çè§é¢é¢æµ | ç©ç AI éè¦ä¸°å¯è§è§ç»èï¼æ½è±¡ç¹å¾æ æ³ç´æ¥è®­ç»ä¸æ¸¸ç­ç¥ |
| **æ¨¡åæ¶æ** | Cosmos-Predict1 / Transfer1 | ç»ä¸æ¶æãææ¬ç¼ç å¨ä¸æ§å¶åæ¯ | è§£å³ä¸ä¸ä»£æ¨¡åæ¨¡æå²è£é®é¢ï¼æåå¤è§è§ä¸å¨ä½æ¡ä»¶é¢æµè½å |
| **åè®­ç»æºå¶** | çº¯çç£å¾®è° / æ å¯¹é½ | VideoAlign å¥å±æ¨¡å + GRPO é£æ ¼ RL | è§£å³çæè§é¢âè§è§å¥½çä½ç©çå´©åâçé®é¢ä¿¡å· |
| **æ¨çå é** | æ åæ©æ£éæ · | rCM æ··åæ­£ååèåè¸é¦ | ä¿ææå¸æ¨¡åè´¨éæµå¼ä¸ççæçæ¨çæ­¥æ° |

```mermaid
flowchart TD
    classDef base fill:#e3f2fd,stroke:#1565c0,color:#0d47a1;
    classDef core fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20;
    classDef post fill:#fff3e0,stroke:#ef6c00,color:#e65100;
    classDef eval fill:#fce4ec,stroke:#c2185b,color:#880e4f;

    early_wm["æ©ææ½è±¡ä¸çæ¨¡å"]:::base -->|èå¼è½¬å| pixel_pre["åç´ çº§é«ä¿çåèº«"]:::base
    pixel_pre -->|æ¶æç»ä¸| core_gen["æ ¸å¿è§é¢çææ¨¡å"]:::core
    pixel_pre -->|åæ¯æ©å±| ctrl_trans["å¤æ¨¡ææ§å¶è½¬è¯"]:::core
    
    reward_model["è§é¢å¯¹é½å¥å±æ¨¡å"]:::post -->|æä¾åå¥½| rl_post["å¼ºåå­¦ä¹ åè®­ç»"]:::post
    rl_post -->|ä¼åè´¨é| core_gen
    
    distill_acc["æ··åè¸é¦æ¨çå é"]:::post -->|éä½æ­¥æ°| core_gen
    
    core_gen -->|ç»ä¸è¯ä¼°| eval_pai["ç©çäººå·¥æºè½è¯æµ"]:::eval
    ctrl_trans -->|å¨ä½éªè¯| eval_pai
```
*å¦ä½è¯»è¿å¼ å¾ï¼èè²ä»£è¡¨èå¼åºç¡ï¼ç»¿è²æ¯æ¬æçæ ¸å¿çæä¸æ§å¶åå¼æï¼æ©è²æ¯æåè´¨éä¸éåº¦çåå¤çâå¤æâï¼ç²è²æææ§çè¯æµé­ç¯ãç®­å¤´æ­ç¤ºäºææ¯æ¨¡åé´çä¾èµä¸æ°æ®æµåã*æºå¶æè§£ï¼ä¸ºä»ä¹è¿ä¹åï¼

**ä»âçç«æ´äººææ¶âå°âç 4K çµå½±â**ãæ©æçä¸çæ¨¡åä¸»è¦å­¦ä¹ æ½è±¡æ½å¨ç¶æç¨äºè§åãä½è¿å¨ç©ç AI ä¸­å­å¨è´å½ç¼ºé·ï¼æ½è±¡ç¹å¾å°±åçç«æ´äººææ¶ï¼ä¸¢å¤±äºæ¥è§¦é¢å½¢åãæ¬æéç¨åç´ ç©ºé´é«ä¿çè·¯çº¿ï¼å¹¶æ©å±å°ææ¬ãå¾åãå¨ä½åç¸æºä¿¡å·ï¼å°±æ¯ä¸ºäºçæå¯ç´æ¥ç¨äºè®­ç»åè¯ä¼°çåæè§æµï¼ç´è§ï¼éä¸¥æ ¼å¯¹åºï¼åç´ çº§çæç¸å½äºä¸ºæºå¨äººæä¾äºå¸¦é«åè¾¨çè§¦è§åé¦ç VR è®­ç»åºï¼ã

**ç¨ RL åè®­ç»éæ­»âç©çä¸è´æ§â**ãæ©æ£æ¨¡åå®¹æçæâè§è§æè³ä½è¿èç©çâçè§é¢ï¼å¦ç©ä½ç©¿ VideoAlign ä½ä¸º VLM-based reward modelï¼è¯ä¼°ææ¬å¯¹é½ãè¿å¨ä¸è§è§è´¨éï¼å¹¶æ GRPO æè·¯å¨ rollout group å¥å±æ¥è®¡ç® advantageãä¸åä¸ºå¤åéè§é¢éæ ·æä¾äºç¨³å®çç¸å¯¹ä¼å¿ä¿¡å·ï¼è®© RL è½å¤ç´æ¥æ©ç½ç©çè¿è§ï¼æ¹åçæè´¨éã

**è¸é¦å éæç ´âå®æ¶ä»¿çâç¶é¢**ãä¸çæ¨¡åè¥è¦åä»¿çå¨ï¼æ¨çæ¬æéç¨ rCM hybrid forward-reverse joint distillationï¼å° consistency distillation ä¸ distribution matching distillation ç»åãè¿ç§æ··åè¸é¦å¨ä¿æ teacher è´¨éçåæ¶ï¼ææéä½äºæ©æ£å¼ä¸ççæçæ¨çæ­¥æ°å¼çæçæ½åã

### è¯æµé­ç¯ä¸å±éæ§å®¡è§

å¨è¯æµç«¯ï¼è®ºææ²¡æå±éäºä¼ ç»çè§é¢è´¨éææ ï¼èæ¯ä½¿ç¨äº PAI-BenchãPAIBench-Transfer è¯ä¼°ç©ç AI ä»»å¡ï¼å¹¶å¨ Bridge æ°æ®éä¸éªè¯å¨ä½æ¡ä»¶é¢æµï¼ç»å RDS-HQ/RQS-HQ å¤è§è§é©¾é©¶æ°æ®è¯ä¼°ä»¿çè½åãè¿ææäºä¸ä¸ªä»âçæè´¨éâå°âä¸æ¸¸ç­ç¥æ³åâçå®æ´è¯æ®é¾ã

<details>
<summary><strong>å±éæ§ä¸å¤±ææ¨¡å¼å®¡è§</strong></summary>
å°½ç®¡è®ºæå¨ææå¯¹æ¯åºçº¿âå®éªä¸å¯¹æ¯âä¸èçè¡¨æ ¼ï¼ï¼ä½å¨è§£è¯»æ¶éæ³¨æä»¥ä¸è¾¹çï¼
1. **è¿åº¦å®£ç§°é£é©**ï¼æ¬ææ¯ Cosmos å®¶æç 2.5 çæ¬è¿­ä»£ï¼èéâé¦ä¸ªâç©ç AI ä¸çæ¨¡åãå·¥ç¨ä¸æ¶æçç»ä¸ï¼èéåºå±çæèå¼çä»é¶çªç ´ã
2. **RL åè®­ç»çæ¿ä»£è§£é**ï¼VideoAlign é©±å¨ç RL åè®­ç»ç¡®å®æåäºææ ï¼ä½è®ºææªå¢å åè®­ç»æ°æ®éâä¸âä¹é´çç¬ç«è´¡ç®ãå¥å±æ¨¡åæ¬èº«çåå·®ï¼å¦åå¥½ç¹å®å¯è½ä¼ä½ä¸ºéèåéä¼ éç»çææ¨¡åã
3. **ç©çå¤æ¨è¾¹ç**ï¼å¨ Bridge æºå¨äººæ°æ®éåå¤è§è§é©¾é©¶ä¸çæå_è®­ç»æ°æ®åå¸çæç«¯ç©çäº¤äºï¼å¦å¤ææµä½ãéåä½å§çå½¢åï¼ï¼åç´ çº§é¢æµä»å¯è½éåä¸ºçº¹çå¹»è§ï¼è®ºæå¯¹æ­¤ç±»å¤±ææ¨¡å¼çæ¥åç¸å¯¹è¾å°ã
</details>

ç¨æ·å¸ææä½ä¸ºä¸åèµæ·±çä¸­æææ¯æ·±åº¦ä¸ç¯è®ºææ·±åº¦è§£è¯»æ¥åä¸­çä¸èï¼âç ç©¶æ¢ç´¢åç¨âã
è¿ä¸èéè¦æç ç©¶ DAGï¼æåæ ç¯å¾ï¼åäºåï¼å±ç¤ºç ç©¶å¢éä¾æ¬¡é®äºåªäºé®é¢ãåäºæè¿åªäºæ­»è¡åãå­¦å°äºä»ä¹ãææ æ¹åè½¬åã

trace/exploration_treeä»¥ä¸èç¹ï¼
- Q1: å¦ä½æè§é¢åºç¡æ¨¡åè½¬æPhysical AIä¸çæ¨¡æå¨ (D1: åç´ ç©ºé´é«ä¿çè§é¢é¢æµ)
- Q2: å¦ä½è·å¾æ´å¹²åä¸é¢åPhysical AIçæ°æ® (E1: å¤é¶æ®µè§é¢è¿æ»¤ä¸é¢åæ°æ®ç­å, D2: ç»ä¸Text2WorldãImage2WorldåVideo2World)
- Q3: å¦ä½è®©é«åè¾¨çFMè®­ç»æ´ç¨³å® (D3: flow matchingä¸é«åªå£°åç½®, X1: é«åªå£°æ ·æ¬ä¸è¶³å¯¼è´è¿æ¸¡ä¼ªå½± -> æè®­ï¼æ¾å¼æ½åæé«åªå£°åºåæ ·æ¬)
- E2: é¢åä¸ç¨SFTä¸æ¨¡ååå¹¶ (X2: ç´æ¥èåé¢åSFTéè¦æ··åæ¯ä¾æè¡¡ -> æè®­ï¼åå¹¶, D4: ç¨model soupä½ä¸ºæç»åå¹¶æ¨¡å)
- E3: VideoAlignå¼ºåå­¦ä¹ åè®­ç»
- P1: ä»åºç¡é¢æµæ©å±å°å¯æ§world translation (E4: Cosmos-Transfer2.5è§é¢éªè¯)
- P2: ä»çæè§é¢è½¬åæºå¨äººç­ç¥æ°æ®å¢å¼º (X3: æ åå¾åå¢å¼ºé¾è¦çè¯­ä¹åºæ¯åå -> æè®­ï¼ä½¿ç¨å¯æ§è§é¢ä¸çæ¨¡å, E5: action-conditioned world generationæ¶è)

åä½è§èè¦æ±ï¼
1. **ç»æï¼ç»è®ºåç½®æç»è®ºï¼åå±å¼ãH2å¼å¤´ï¼å¸¦emojiã
2. **å¿ å®ä¸ä¸¥è°¨**ãåºåå£°ç§°ä¸è¯æï¼ç¹åå¤±ææ¨¡å¼ï¼å¦X1, X2, X3ï¼ã
3. **æ¥å°**ãä¸å¨åè¿°å¥å­éåç²¾ç¡®æ§è½æ°å­ï¼ç¨å®æ§è¯­è¨ãéæ§è½æ°å­å¯åãä¸æåè¯
4. **å¾è¡¨åäº**ãæ¶åæµç¨/ç»æ/Mermaidï¼ãè¿ééåç»ä¸ä¸ªæ¢ç´¢åç¨ç timeline æ flowchartãèèå°æ¯âæ¢ç´¢åç¨âï¼ç¨ timeline æå¸¦åæ¯ç flowchart æ¯è¾å¥½ãè¿éç¨ flowchart å±ç¤ºå³ç­åæ­»è¡åçåæ¯ å±ç¤ºé¶æ®µãç¨ flowchart å±ç¤ºâé®é¢->å³ç­->æ­»è¡å->è½¬åã
5. **è¡¨æ ¼ vs åè¿°**ãç»æåå¯¹æ¯ç¨è¡¨ã
6. **æ·±åº¦èè¿æå å**ãåé¿ç»èç¨ `<details>`ã
7. **ç¡¬çº¦æ**çå¨ï¼ä¸ç¼é ï¼ä¸åç²¾ç¡®æ§è½æ°å­50-800 å­ï¼åªè¾åºæ­£æï¼ä»¥ `## ðºï¸ ç ç©¶æ¢ç´¢åç¨`ï¼æç±»ä¼¼ï¼H2å¥é¦å¸¦emojiï¼å¼å¤´ã

æè Mermaid å¾è¡¨ï¼
ç»ä¸ä¸ªæ¢ç´¢è·¯å¾ç flowchart (TB æ LR)ã
èç¹ï¼
- èµ·ç¹ï¼æå»º Physical AI ä¸çæ¨¡æå¨ (Q1)
- å³ç­ï¼åç´ ç©ºé´é«ä¿çé¢æµ (D1)
- æ°æ®ä¸ä»»å¡ç»ä¸ (Q2 -> D2)
- è®­ç»ç¨³å®æ§ææ (Q3 -> D3) -> æ­»è¡åï¼é«åªå£°ä¼ªå½± (X1) -> ä¿®æ­£ï¼æ¾å¼é«åªå£°éæ ·
- é¢åå¾®è°ææ (E2) -> æ­»è¡åï¼èåè®­ç»æ¯ä¾å¤±è¡¡ (X2) -> ä¿®æ­£ï¼ç¬ç«å¾®è°+Model Soup (D4) -> RLå¯¹é½ (E3)
- è½¬å1ï¼å¯æ§ World Translation (P1 -> E4)
- è½¬å2ï¼æºå¨äººç­ç¥æ°æ®å¢å¼º (P2) -> æ­»è¡åï¼æ åå¾åå¢å¼ºå¤±æ (X3) -> ä¿®æ­£ï¼å¨ä½æ¡ä»¶çæ (E5)

Mermaid ä»£ç è®¾è®¡ï¼
```mermaid
flowchart TD
    classDef main fill:#e1f5fe,stroke:#01579b,color:#01579b;
    classDef dead fill:#ffebee,stroke:#b71c1c,color:#b71c1c;
    classDef pivot fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20;
    classDef fix fill:#fff3e0,stroke:#e65100,color:#e65100;

    start["æå»º Physical AI ä¸çæ¨¡æå¨"]:::main --> d1["éæ©åç´ ç©ºé´é«ä¿çé¢æµ"]:::main
    d1 --> d2["ç»ä¸å¤æ¨¡æçæä»»å¡"]:::main
    d2 --> q3["é«åè¾¨çè®­ç»ç¨³å®æ§ææ"]:::main
    q3 --> x1["æ­»è¡å: é«åªå£°æ ·æ¬ä¸è¶³è´ä¼ªå½±"]:::dead
    x1 --> fix1["ä¿®æ­£: æ¾å¼æ½åæé«åªå£°åºå"]:::fix
    
    d2 --> e2["é¢åä¸ç¨ SFT æ¢ç´¢"]:::main
    e2 --> x2["æ­»è¡å: èåè®­ç»æ¯ä¾å¤±è¡¡"]:::dead
    x2 --> fix2["ä¿®æ­£: ç¬ç«å¾®è°å  Model Soup"]:::fix
    fix2 --> e3["VideoAlign å¼ºåå­¦ä¹ åè®­ç»"]:::main
    
    e3 --> p1["è½¬å: æ©å±è³å¯æ§ World Translation"]:::pivot
    p1 --> p2["è½¬å: æºå¨äººç­ç¥æ°æ®å¢å¼º"]:::pivot
    p2 --> x3["æ­»è¡å: æ åå¾åå¢å¼ºé¾æ¹è¯­ä¹"]:::dead
    x3 --> fix3["ä¿®æ­£: å¨ä½æ¡ä»¶ä¸ççæ"]:::fix
```
æ£æ¥ Mermaid çº¦æï¼
- ç¦ç¨ `%%{init}` ä¸`ï¼æ»¡è¶³ã
- åªç¨ `classDef`+`class`ï¼æ»¡è¶³ã
- æ¯å¾ â¤4 ä¸ªè¯­ä¹è²ä¸æ¯è²å«æå­ `color:`ï¼main(è), dead(çº¢), pivot(ç»¿), fix4ä¸ªï¼æ»¡è¶³ã
- ç»ä¸åªé é¢è²ä¼ ä¹ï¼èç¹æå­å·²è¯´æã
- snake_case èç¹ idï¼æ»¡è¶³ã
- æ ç­¾ 3-6 è¯ä¸»å¨è¯­æï¼ç¨å¾®è°æ´æ ç­¾ï¼ 3-6 è¯ã
  - `start` -> `æå»ºç©çäººå·¥æºè½ä¸çæ¨¡æå¨` (11ä¸ªå­ï¼ç®è¯çè¯ `æå»ºç©çAIä¸çæ¨¡æå¨` 9ä¸ªå­ãè±æè¯ç®1ä¸ªï¼ä¸­ææå­/è¯ãè§èè¯´âæ ç­¾ 3â6 è¯âï¼ä¸­æå¤§æ¦ 3-6 ä¸ªè¯ç»ï¼æ¯å¦âæå»º ç©ç AI ä¸ç æ¨¡æå¨â 5ä¸ªè¯ãå°½éç²¾ç®ï¼`æå»ºç©çAIæ¨¡æå¨`)
  - `d1` -> `éæ©åç´ ç©ºé´é«ä¿çé¢æµ` (éæ© åç´  ç©ºé´ é«ä¿ç é¢æµ - 5è¯)
  - `d2` -> `ç»ä¸å¤æ¨¡æè§é¢çæä»»å¡` (ç»ä¸ å¤æ¨¡æ è§é¢ çæ ä»»å¡ - 5è¯)
  - `q3` -> `åºå¯¹é«åè¾¨çè®­ç»ç¨³å®æ§` (åºå¯¹ é«åè¾¨ç è®­ç» ç¨³å®æ§ - 4è¯)
  - `x1` -> `é«åªå£°æ ·æ¬ä¸è¶³å¯¼è´ä¼ªå½±` (é«åªå£° æ ·æ¬ ä¸è¶³ å¯¼è´ ä¼ªå½± - 5è¯)
  - `fix1` -> `æ¾å¼æ½åæé«åªå£°åºåæ ·æ¬` (æ¾å¼ æ½å æé« åªå£° åºå æ ·æ¬ - 6è¯)
  - `e2` -> `æ¢ç´¢é¢åä¸ç¨çç£å¾®è°` (æ¢ç´¢ é¢å ä¸ç¨ çç£ å¾®è° - 5è¯)
  - `x2` -> `èåè®­ç»` (èå é¢å æ¯ä¾ å¤±è¡¡ - 6è¯)
  - `fix2` -> `ç¬ç«å¾®è°ç»åæ¨¡ååæ°åå¹¶` (ç¬ç« å¾®è° ç»å æ¨¡å åæ° åå¹¶ - 6è¯)
  - `e3` -> `äººç±» å¼ºå å­¦ä¹  å¯¹é½ äººç±» åå¥½ - 6è¯)
  - `p1` -> `è½¬åå¯æ§ä¸çè§è§ç¿»è¯` (è½¬å å¯æ§ ä¸ç è§è§ ç¿»è¯ - 5è¯)
  - `p2` -> `è½¬åæºå¨äººç­ç¥æ°æ®å¢å¼º` (è½¬å æºå¨äºº ç­ç¥ æ°æ® å¢å¼º - 5è¯)
  - `x3` -> `æ åå¾åå¢å¼ºé¾æ¹è¯­ä¹åºæ¯` (æ å å¾å å¢å¼º é¾æ¹ è¯­ä¹ åºæ¯ - 6è¯)
  - `fix3` -> `éç¨å¨ä½æ¡ä»¶ä¸ççæ` (éç¨ å¨ä½ æ¡ä»¶ ä¸ç çæ - 5è¯)
- è¾¹æ ç­¾ 1-4 è¯ï¼å¯ä»¥ä¸å è¾¹æ ç­¾ï¼âå¤±è´¥âãâä¿®æ­£âã
- å½¢ç¶ä¸è´ï¼é»è®¤åè§ç©å½¢ã
- å¤æåº¦åçº§ï¼14ä¸ªèç¹ï¼ä½¿ç¨ subgraph æçå®é¶æ®µå½åã
  - subgraph é¶æ®µä¸_åºç¡æ¨¡åæå»º
  - subgraph é¶æ®µäº_é¢åå¾®è°ä¸å¯¹é½
  - subgraph é¶æ®µä¸_ä¸æ¸¸æ§å¶ä¸å¢å¼º

è°æ´ Mermaidï¼
```mermaid
flowchart TD
    classDef main fill:#e1f5fe,stroke:#01579b,color:#01579b;
    classDef dead fill:#ffebee,stroke:#b71c1c,color:#b71c1c;
    classDef pivot fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20;
    classDef fix fill:#fff3e0,stroke:#e65100,color:#e65100;

    subgraph phase1["é¶æ®µä¸: åºç¡ä¸çæ¨¡æå¨æå»º"]
        start["æå»ºç©çAIæ¨¡æå¨"]:::main --> d1["éæ©åç´ ç©ºé´é«ä¿çé¢æµ"]:::main
        d1 --> d2["ç»ä¸å¤æ¨¡æè§é¢çæä»»å¡"]:::main
        d2 --> q3["åºå¯¹é«åè¾¨çè®­ç»ç¨³å®æ§"]:::main
        q3 --> x1["é«åªå£°æ ·æ¬ä¸è¶³å¯¼è´ä¼ªå½±"]:::dead
        x1 --> fix1["æ¾å¼æ½åæé«åªå£°åºåæ ·æ¬"]:::fix
    end

    subgraph phase2["é¶æ®µäº: é¢åå¾®è°ä¸åå¥½å¯¹é½"]
        d2 --> e2["æ¢ç´¢é¢åä¸ç¨çç£å¾®è°"]:::main
        e2 --> x2["æ¯ä¾å¤±è¡¡"]:::dead
        x2 --> fix2["ç¬ç«å¾®è°ç»åæ¨¡ååæ°åå¹¶"]:::fix
        fix2 --> e3å¯¹é½äººç±»åå¥½]:::main
    end

    subgraph phase3["é¶æ®µä¸: ä¸æ¸¸æ§å¶ä¸æ°æ®å¢å¼º"]
        e3 --> p1["è½¬åå¯æ§ä¸çè§è§ç¿»è¯"]:::pivot
        p1 --> p2["è½¬åæºå¨äººç­ç¥æ°æ®å¢å¼º"]:::pivot
        p2 --> x3["æ åå¾åå¢å¼ºé¾æ¹è¯­ä¹åºæ¯"]:::dead
        x3 --> fix3["éç¨å¨ä½æ¡ä»¶ä¸ççæ"]:::fix
    end
```
æ£æ¥èç¹è¿æ¥ï¼`d2` å¨ phase1ï¼ä½è¿å phase2 ç `e2`ãMermaid ä¸­è·¨ subgraph è¿æ¥æ¯è§åï¼
1. **ç»è®ºåç½®**ï¼Cosmos å¢éå¹¶éä¸å¼å§å°±æ¥æå®ç¾çâï¼èæ¯éè¿âåºç¡æå»º-é¢åå¯¹é½-ä¸æ¸¸æ§å¶âä¸ä¸ªé¶æ®µçè¯éï¼éæ­¥å°è§é¢çææ¨¡åé¼å Physical AI çä¸¥èè¦æ±ãæ ¸å¿ç»è®ºæ¯ï¼åç´ çº§é«ä¿çä¸å¤æ¨¡æç»ä¸æ¯åºç³ï¼èè§£å³é«åè¾¨çä¼ªå½±ãé¢åæ°æ®å²çªåè¯­ä¹å¢å¼ºå¤±æç­âæ­»è¡åâï¼ç©çè½¬æã
2. **é¶æ®µä¸ï¼åºç¡æå»ºä¸ä¼ªå½±æ­»è¡å**ãè®²è¿° Q1, D1, Q2, D2ãç¶åè®² Q3 å X1ï¼é«åªå£°ä¼ªå½±ï¼ã
3. **é¶æ®µäºï¼é¢åå¾®è°çå¹³è¡¡é·é±**ãè®²è¿° E2, X2ï¼èåè®­ç»æ¯ä¾å¤±è¡¡ï¼ï¼è½¬å D4ï¼Model Soupï¼å E3ï¼RLï¼ã
4. **é¶æ®µä¸ï¼ä»çæå°æ§å¶çä¸¤æ¬¡ Pivot**ãè®²è¿° P1ï¼Transferï¼ï¼P2ï¼æºå¨äººå¢å¼ºï¼ï¼X3ï¼æ åå¾åå¢å¼ºå¤±æï¼ï¼æç»èµ°å E5ï¼å¨ä½æ¡ä»¶çæï¼ã
5. **æå å**ï¼ææ¹æ³å¯¹æ¯ï¼Model Soup vs TIES ç­ï¼æå¨ä½Embedding vs CrossAttenï¼æ¾è¿ `<details>`ã

æ£æ¥æ¥å°è§åï¼
- ä¸åç²¾ç¡®æ§è½æ°å­ãå¦âå¨æ´ä½è´¨éåºçº¿âã
- éæ§è½æ°å­ï¼2B, 720p, 5ç§ç­ï¼äºå®æºéæ Cosmos-Predict2.5-2Bï¼å¯ä»¥å 2Bï¼ã
- ä¸æåè¯ï¼Cosmos-Predict2.5, Cosmos-Transfer2.5, Physical AI, Text2World, Image2World, Video2World, flow matching, shifted logit-normal, model soup, TIES, DARE-Linear, DARE-TIES, VideoAlign, diffusion policy, TimeEmbedding, CrossAtten, ChannelConcatã

æ°å ðºï¸ ç ç©¶æ¢ç´¢åç¨

**ç»è®ºåç½®ï¼** Cosmos å¢éå¹¶éä¸å¼å§å°±æ¡æå®ç¾çâä¸çèæ¯åç»âåºç¡æå»ºãé¢åå¯¹é½ãä¸æ¸¸æ§å¶âä¸ä¸ªé¶æ®µççå®è¯éï¼æå°è§é¢åºç¡æ¨¡åæç£¨æåæ ¼ç Physical AI ä»£çé»è¾å¨äºï¼ä»¥åç´ çº§é«ä¿çä¸å¤æ¨¡æä»»å¡ç»ä¸ä¸ºåºç³ï¼éè¿è·¨è¶é«åè¾¨çä¼ªå½±ãé¢åæ°æ®å²çªåè¯­ä¹å¢å¼ºå¤±æç­ä¸å¤§âæ­»è¡åâï¼æç»å®ç°ä»å¼æ¾å¼è§é¢çæå°é­ç¯è·è¿ã

### é¶æ®µä¸ï¼åºç¡æå»ºä¸é«åè¾¨çä¼ªå½±æ­»è¡å
å¢éçé¦è¦ç®æ æ¯æå»ºæå¡äº Physical AI çä¸çæ¨¡æå¨ï¼Q1ï¼ãå¨è·¯çº¿éæ©ä¸ï¼ä»ä»¬æ¾å¼äº latent representation space æåç 3D/4D è¡¨ç¤ºï¼åå³éç¨**åç´ ç©ºé´é«ä¿çè§é¢é¢æµ**ï¼D1ï¼ï¼ä»¥ä¿çæä¸°å¯çç©çç»èãä¸ºæå¤§åæ°æ®æç¨ï¼æ¨¡åè¢«è®¾è®¡ä¸ºåä¸æ¶æç»ä¸ Text2WorldãImage2World å Video2World ä»»å¡ï¼D2ï¼ã

ç¶èï¼é«å flow matching è®­ç»å¸¦æ¥äºç¨³å®æ§ææï¼Q3ï¼ãå¢éæåéç¨äº shifted logit-normal timestep åå¸ï¼å´**æ­»è¡åï¼X1ï¼**ï¼å³ä¾¿éåè¾¨çå¢å è°æ´äºåç§»ï¼çæè§é¢ä»é¢ç¹é´è¿æ¸¡ä¼ªå½±ãå½å åæè¡¨æï¼æ¨¡åå¨é«åªå£°åºåâè§âè¿çæ ·æ¬å¤ªå°ï¼æ æ³ææææ£ãä¸ºæ­¤ï¼å¢éä¿®æ­£äº schedulerï¼**æ¾å¼å¢å æé«åªå£°åºåçéæ ·**ï¼å½»åºæ¹åäºæ¶é´ä¸è´æ§ã

### é¶æ®µäºï¼é¢åå¾®è°çå¹³è¡¡é·é±ä¸æ¨¡ååå¹¶
ä¸ºäºè®©æ¨¡åææ¡ roboticsãautonomous driving ç­åç´é¢åçç©çè§å¾ï¼å¢éç­åäºæ´ä¸¥æ ¼çé¢åä¸ç¨æ°æ®ï¼E1ï¼ãä½å¨å¾®è°é¶æ®µï¼ä»ä»¬åæ¬¡**æ­»è¡åï¼X2ï¼**ï¼è¯å¾å°ææé¢åæ°æ®æ··åè¿è¡èå SFTï¼ç mixture ratios æè¡¡ï¼é¨åé¢åæ°æ®è¢«ä¸¥éç¨éã

å¸åæè®­åï¼å¢éæ¹åç­ç¥ï¼ä¸ºæ¯ä¸ªé¢åç¬ç«è®­ç»ä¸ç¨æ¨¡åï¼åéè¿æ¨¡ååå¹¶ï¼Model Mergingï¼ç»ä¸è½åãå¨è¯ä¼°äº model soupãTIESãDARE-Linear å DARE-TIES ç­æ¹æ¡åï¼æç»éå® **model soup** ä½ä¸ºåè®­ç»åºåº§ï¼D4ï¼ï¼éåå å  **VideoAlign** å¼ºåå­¦ä¹ åè®­ç»ï¼E3ï¼ï¼å¨ææ¬å¯¹é½ä¸è§è§è´¨éä¸åå¾äºæ°å¼è§âå®éªä¸å¯¹æ¯âçè¡¨æ ¼ï¼ã

<details>
<summary><strong>æ¨¡ååå¹¶ä¸æ¶èç»è</strong></summary>
å¨æ¨¡ååå¹¶é¶æ®µï¼å¢éå¹¶æªç²ç®è¿½æ±å¤æçæéè£åªç®æ³ï¼èæ¯éè¿ grid search ä¸äººå·¥è´¨éè¯ä¼°ï¼åç°ç®åç model soup åä½å¨æ´åå¤é¢åä¼å¿æ¶è¡¨ç°æç¨³ãæ­¤å¤ï¼å¨åç»­çå¨ä½æ¡ä»¶ä¸ççæï¼action-conditioned world generationï¼æ¶èä¸­ï¼éå¯¹ Cosmos-Predict2.5-2B æ¨¡åï¼å¢éå¯¹æ¯äº TimeEmbeddingãCrossAtten å ChannelConcat ä¸ç§è¯å® TimeEmbedding å¨æ¹åä¸æ¾èä¼äºåé»è®¤details>

### é¶æ®µä¸ï¼ä»çæå°æ§å¶çä¸¤æ¬¡æ¨¡åå°±ç»ªåï¼ç ç©¶è¿æ¥äºä¸¤æ¬¡éè¦çæ¹åè½¬åï¼Pivotï¼ãé¢æµæ©å±å°å¯æ§ world translationï¼P1ï¼**ï¼Transfer2.5 æ¡æ¶ï¼æ¯æ edgeãdepth ç­ç©ºé´ä¸æ¸¸ Sim2Real åå¤æ¨¡ææ§å¶çéæ±ï¼E4ï¼ã

çæè§é¢è½¬åæºå¨äººç­ç¥æ°æ®å¢å¼ºï¼P2ï¼**ãä¼ ç»å¾åå¢å¼ºï¼å¦è°äº®åº¦ãå åªå£°ï¼å¨åºå¯¹å¯¹è±¡è¯­ä¹çº§ååæ¶æ­»è¡å X3**ï¼ãè¿è¿«ä½¿å¢éæ¾å¼æ åæ°æ®å¢å¼ºï¼è½¬èä½¿ç¨å¯æ§è§é¢ä¸çæ¨¡åçæç»æåè¯­ä¹ååï¼å¹¶æç»éªè¯äº action-conditioned çæå¯¹ diffusion policy çå®æºå¨äººæ³åçå·¨å¤§ä»·å¼ï¼E5ï¼ã

```mermaid
flowchart TD
    classDef main fill:#e1f5fe,stroke:#01579b,color:#01579b;
    classDef dead fill:#ffebee,stroke:#b71c1c,color:#b71c1c;
    classDef pivot fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20;
    classDef fix fill:#fff3e0,stroke:#e65100,color:#e65100;

    subgraph phase1["é¶æ®µä¸: åºç¡ä¸çæ¨¡æå¨æå»º"]
        start["æå»ºç©çAIæ¨¡æå¨"]:::main --> d1["éæ©åç´ ç©ºé´é«ä¿çé¢æµ"]:::main
        d1 --> d2["ç»ä¸å¤æ¨¡æè§é¢çæä»»å¡"]:::main
        d2 --> q3["åºå¯¹é«åè¾¨çè®­ç»ç¨³å®æ§"]:::main
        q3 --> x1["é«åªå£°æ ·æ¬ä¸è¶³å¯¼è´ä¼ªå½±"]:::dead
        x1 --> fix1["æ¾å¼æ½åæé«åªå£°åºåæ ·æ¬"]:::fix
    end

    subgraph phase2["é¶æ®µäº: é¢åå¾®è°ä¸åå¥½å¯¹é½"]
        d2 --> e2["æ¢ç´¢é¢åä¸ç¨çç£å¾®è°"]:::main
        e2 --> x2["æ¯ä¾å¤±è¡¡"]:::dead
        x2 --> fix2["ç¬ç«å¾®è°ç»åæ¨¡ååæ°åå¹¶"]:::fix
        fix2 --> e3["äººç±»åå¥½"]:::main
    end

    subgraph phase3["é¶æ®µä¸: ä¸æ¸¸æ§å¶ä¸æ°æ®å¢å¼º"]
        e3 --> p1["è½¬åå¯æ§ä¸çè§è§ç¿»è¯"]:::pivot
        p1 --> p2["è½¬åæºå¨äººç­ç¥æ°æ®å¢å¼º"]:::pivot
        p2 --> x3["æ åå¾åå¢å¼ºé¾æ¹è¯­ä¹åºæ¯"]:::dead
        x3 --> fix3["éç¨å¨ä½æ¡ä»¶ä¸ççæ"]:::fix
    end
```
*å¦ä½è¯»è¿å¼ å¾ï¼èè²èç¹ä»£è¡¨ä¸»çº¿æ¨è¿ï¼çº¢è²èç¹æ´é²äºå¢éè¸©è¿çä¸ä¸ªæ ¸å¿âæ­»è¡åâï¼é«åªå£°ä¼ªå½±ãèåå¾®è°å¤±è¡¡ãä¼ ç»å¢å¼ºå¤±æï¼ï¼æ©è²èç¹åæ¯éå¯¹æ§çä¿®æ­£æ¹æ¡ï¼ç»¿è²èç¹æ å¿çæ¨¡åä»âçæâåâç©çæ§å¶ Pivotã*

å­æ°æ£æ¥ï¼
ä¸­æçº¦ 800 å­ï¼æ»¡è¶³ 350-800 å­çè¦æ±ã
æ²¡æç²¾ç¡®æ§è½æ°å­ï¼ä¸æåè¯ä¿çï¼ç»æç¬¦åç»è®ºåç½®ï¼å¾è¡¨ç¬¦åè§èã
å®ç¾ã## ðºï¸ ç ç©¶æ¢ç´¢åç¨

**ç»è®ºåç½®ï¼** Cosmos å¢éå¹¶éä¸å¼å§å°±æ¡æå®ç¾çâï¼èæ¯åç»âåºç¡æå»ºãé¢åå¯¹é½ãä¸æ¸¸æ§å¶âä¸ä¸ªé¶æ®µççå®è¯éï¼æå°è§é¢åºç¡æ¨¡åæç£¨æåæ ¼ç Physical AI ä»£çãå¨äºï¼ä»¥åç´ çº§é«ä¿çä¸å¤æ¨¡æä»»å¡ç»ä¸ä¸ºåºç³ï¼éè¿è·¨è¶é«åè¾¨çä¼ªå½±ãé¢åæ°æ®å²çªåè¯­ä¹å¢å¼ºå¤±æç­ä¸å¤§âæ­»è¡åâï¼æç»å®ç°ä»å¼æ¾å¼è§é¢çæå°é­ç¯ç©çä»¿ã

### é¶æ®µä¸ï¼åºç¡æå»ºä¸é«åè¾¨çä¼ªå½±æ­»è¡å
å¢éçé¦è¦ç®æ æ¯æå»ºæå¡äº Physical AI çä¸çæ¨¡æå¨ï¼Q1ï¼ãå¨è·¯çº¿éæ©ä¸ï¼ä»ä»¬æ¾å¼äº latent representation space æåç 3D/4D è¡¨ç¤ºï¼åå³éç¨**åç´ ç©ºé´é«ä¿çè§é¢é¢æµ**ï¼D1ï¼ï¼ä»¥ä¿çæä¸°å¯çç©çç»èãä¸ºæå¤§åæ°æ®æç¨ï¼æ¨¡åè¢«è®¾è®¡ä¸ºåä¸æ¶æç»ä¸ Text2WorldãImage2World å Video2World ä»»å¡ï¼D2ï¼ã

ç¶èï¼é«åè¾¨çç» flow matching è®­ç»å¸¦æ¥äºç¨³å®æ§ææï¼Q3ï¼ãå¢éæåéç¨äº shifted logit-normal timestep åå¸ï¼å´**æ­»è¡åï¼X1ï¼**ï¼å³ä¾¿éåè¾¨çå¢å è°æ´äºåç§»ï¼çæè§é¢ä»é¢ç¹é´è¿æ¸¡ä¼ªå½±ãå½å åæè¡¨æï¼æ¨¡åå¨é«åªå£°åºåâè§âè¿çæ ·æ¬å¤ªå°ï¼æ æ³æææä¸ºæ­¤ï¼å¢éä¿®æ­£äº schedulerï¼**æ¾å¼å¢å æé«åªå£°åºåçéæ ·**ï¼å½»åºæ¹åäºæ¶é´ä¸è´æ§ã

### é¶æ®µäºï¼é¢åå¾®è°çå¹³è¡¡é·é±ä¸æ¨¡ååå¹¶
ä¸ºäºè®©æ¨¡åææ¡ roboticsãautonomous driving ç­åç´é¢åçç©çè§å¾ï¼å¢éç­åäºæ´ä¸¥æ ¼çé¢åä¸ç¨æ°æ®ï¼E1ï¼ãä½å¨å¾®è°é¶æ®µï¼æ­»è¡åï¼X2ï¼**ï¼è¯å¾å°ææé¢åæ°æ®æ··åè¿è¡èå SFTä¼æ­¢ç mixture ratios æè¡¡ï¼é¨åé¢åæ°æ®è¢«ä¸¥éç¨éã

å¸åæè®­åï¼å¢éä¸ºæ¯ä¸ªé¢åç¬ç«è®­ç»ä¸ç¨æ¨¡åï¼åéè¿æ¨¡ååå¹¶ï¼Model Mergingï¼ç»ä¸è½åãå¨è¯ä¼°äº model soupãTIESãDARE-Linear å DARE-TIES ç­æ¹æ¡åï¼æç»éå® **model soup** ä½ä¸ºåè®­ç»åºåº§ï¼D4ï¼ï¼éåå å  **VideoAlign** å¼ºåå­¦ä¹ åè®­ç»ï¼E3ï¼ï¼å¨ææ¬å¯¹é½ä¸è§è§è´¨éâå®éªä¸å¯¹æ¯âçè¡¨æ ¼ï¼ã

<details>
<summary><strong>æ¨¡ååå¹¶æ¶èç»è</strong></summary>
å¨æ¨¡ååå¹¶é¶æ®µï¼å¢éå¹¶æªç²ç®è¿½æ±å¤æçæéè£åªç®æ³ï¼èæ¯éè¿ grid search ä¸äººå·¥è´¨éè¯ä¼°ï¼åç°ç®åç model soup åä½å¨æ´åå¤é¢åä¼å¿æ¶è¡¨ç°æç¨³ãæ­¤å¤ï¼å¨åç»­çå¨ä½æ¡ä»¶ä¸ççæï¼action-conditioned world generationï¼æ¶èä¸­ï¼éå¯¹ Cosmos-Predict2.5-2B æ¨¡åï¼å¢éå¯¹æ¯äº TimeEmbeddingãCrossAtten å ChannelConcat ä¸ç§è¯å® TimeEmbedding å¨æ¹åä¸ï¼æä¸ºæç»çé»è®¤details>

### é¶æ®µä¸ï¼ä»çæå°æ§å¶çåºç¡æ¨¡åå°±ç»ªåï¼ç ç©¶è¿æ¥äºä¸¤æ¬¡éè¦çæ¹åè½¬åï¼**ä»åºç¡é¢æµæ©å±å°å¯æ§ world translationï¼P1ï¼**-Transfer2.5 æ¡æ¶ï¼æ¯æ edgeãdepth ç­ç©ºé´æ§å¶ Sim2Real åå¤æ¨¡ææ§å¶çéæ±ï¼E4ä»çæè§é¢è½¬åæºå¨äººç­ç¥æ°æ®å¢å¼ºï¼P2ï¼**ãä¼ ç»å¾åå¢å¼ºï¼å¦è°äº®åº¦ãå åªå£°ï¼å¨åºå¯¹å¯¹è±¡é¢è²å¤±æï¼**æ­»è¡å X3**ï¼ãè¿è¿«ä½¿å¢éæ¾å¼æ åæ°æ®å¢å¼ºï¼è½¬èä½¿ç¨å¯æ§è§é¢ä¸çæ¨¡åçæç»æåè¯­ä¹ååï¼å¹¶æç»éªè¯äº action-conditioned çæå¯¹ diffusion policy çå®æºå¨äººæ³åçå·¨å¤§ä»·å¼ï¼E5ï¼ã

```mermaid
flowchart TD
    classDef main fill:#e1f5fe,stroke:#01579b,color:#01579b;
    classDef dead fill:#ffebee,stroke:#b71c1c,color:#b71c1c;
    classDef pivot fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20;
    classDef fix fill:#fff3e0,stroke:#e65100,color:#e65100;

    subgraph phase1["é¶æ®µä¸: åºç¡ä¸çæ¨¡æå¨æå»º"]
        start["æå»ºç©çAIæ¨¡æå¨"]:::main --> d1["éæ©åç´ ç©ºé´é«ä¿çé¢æµ"]:::main
        d1 --> d2["ç»ä¸å¤æ¨¡æè§é¢çæä»»å¡"]:::main
        d2 --> q3["åºå¯¹é«åè¾¨çè®­ç»ç¨³å®æ§"]:::main
        q3 --> x1["é«åªå£°æ ·æ¬ä¸è¶³å¯¼è´ä¼ªå½±"]:::dead
        x1 --> fix1["æ¾å¼æ½åæé«åªå£°åºåæ ·æ¬"]:::fix
    end

    subgraph phase2["é¶æ®µäº: é¢åå¾®è°ä¸åå¥½å¯¹é½"]
        d2 --> e2["æ¢ç´¢é¢åä¸ç¨çç£å¾®è°"]:::main
        e2 --> x2["èåè®­ç»"]:::dead
        x2 --> fix2["ç¬ç«å¾®è°ç»åæ¨¡ååæ°åå¹¶"]:::fix
        fix2 --> eå­¦ä¹ å¯¹é½äººç±»åå¥½]:::main
    end

    subgraph phase3["é¶æ®µä¸: ä¸æ¸¸æ§å¶ä¸æ°æ®å¢å¼º"]
        e3 --> p1["è½¬åå¯æ§ä¸çè§è§ç¿»è¯"]:::pivot
        p1 --> p2["è½¬åæºå¨äººç­ç¥æ°æ®å¢å¼º"]:::pivot
        p2 --> x3["æ åå¾åå¢å¼ºé¾æ¹è¯­ä¹åºæ¯"]:::dead
        x3 --> fix3["éç¨å¨ä½æ¡ä»¶ä¸ççæ"]:::fix
    end
```
*å¦ä½è¯»è¿å¼ å¾ï¼èè²èç¹ä»£è¡¨ä¸»çº¿æ¨è¿ï¼çº¢è²èç¹æ´é²äºå¢éè¸©è¿çä¸ä¸ªæ ¸å¿âæ­»è¡åâï¼é«åªå£°ä¼ªå½±ãèåå¾®è°å¤±è¡¡ãä¼ ç»å¢å¼ºå¤±æï¼ï¼æ©è²èç¹åæ¯éå¯¹æ§çä¿®æ­£æ¹æ¡ï¼ç»¿è²èç¹æ å¿çæ¨¡åä»âçæâåâç©çæ§å¶âç*

ç¨æ·è¦æ±æ°åä¸ç¯æ·±åº¦ç§æ®è§£è¯»æ¥åä¸­çä¸èï¼æ é¢ä¸ºâ## å·¥ç¨ä¸å¤ç°è¦ç¹âã
ï¼æ³å¤ç°çå·¥ç¨å¸ã
åä¸ä½ç¨ãè¿è¡ç¯å¢/ä¾èµãææ å¼æºä»£ç ä¸æ¡ä»¶ï¼
1. ç»æï¼ç»è®ºåç½®ãæ¯ä¸ªï¼åå±å¼ãH2å¼å¤´ï¼å¯å¸¦emojiãH3/H4ä¸å¸¦ã
2. å¿ å®ä¸ä¸¥è°¨ï¼åºåå£°ç§°ä¸è¯æï¼ç¹åå¤±ææ¨¡å¼ç­ï¼å¦æéç¨ï¼ã
3. æ¥å°ï¼ä¸å¨åè¿°å¥å­éåç²¾ç¡®æ§è½æ°å­ï¼å¦æåxx%ï¼ï¼ç¨å®æ§è¯­è¨ãéæ§è½æ°å­ï¼å±æ°ãGPUæ°ãåè¾¨çç­ï¼å¯åãä¸æåè¯åã
4. å¾è¡¨åäºï¼æ¶åæµç¨/ç»æç­maidï¼åçº§ã
5. è¡¨æ ¼vsåè¿°ï¼ç»æåå¯¹æ¯ç¨è¡¨ã
6. æ·±åº¦èè¿æå åï¼åé¿ç»èç¨`<details>`ã
7. ï¼350-800ä¸­æå­ï¼å°½éåè¶³ï¼å±å¼ï¼ã
8. åªè¾åºæ¬èæ­£æï¼ä»¥â## å·¥ç¨ä¸å¤ç°è¦ç¹âå¼å¤´ã

åæäºå®æºï¼
- æ¨¡åè§æ¨¡ä¸ç»æï¼Cosmos-Predict2.5æ2Bå14BãTransfer2.5-2BåºäºPredict2.5-2Bãä¸»å¹²æ¯DiTé£æ ¼çlatent diffusion velocity prediction network (flow matching)ãä½ç½®ç¼ç ç§»é¤absoluteï¼ä¿çrelative (3D RoPE)ãè§è§tokenizerç¨WAN2.1 VAE (4x8x8åç¼©ï¼1x2x2 patchification)ãææ¬ç¼ç å¨ç¨Cosmos-Reason1ãçæ93 pixel frames (24 latent frames)ã
- è®­ç»W, lr (2B: 3e-5, 14B: 1.3e-5), weight decay 0.001, warmup 2000 itersãtimestepåå¸ç¨logit-normalï¼progressive shift (beta 1å°5)ãé«åªå£°ééæ ·(5%æ ·æ¬ä»æé«2%åªå£°æ½)ãSFT 30k iters, batch 256ãRLç¨VideoAlign, 256 steps, batch 32ã<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-table-tr-td-model-td--><!--anchor:quote:%3Ctable%3E%3Ctr%3E%3Ctd%3EModel%3C%2Ftd%3E%3Ctd%3EDomain%20Score%3C%2Ftd%3E%3Ctd%3EQuality%20Score%3C%2Ftd%3E%3Ctd%3EOverall%20Score%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ECosmos%2DPredict2.5%2D2B%20%5Bpre%2Dtrain%5D%3C%2Ftd%3E%3Ctd%3E0.782%3C%2Ftd%3E%3Ctd%3E0.720%3C%2Ftd%3E%3Ctd%3E0.751%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ECosmos%2DPredict2.5%2D2B%20%7C%20%5Bpost%2Dtrain%5D%3C%2Ftd%3E%3Ctd%3E0.804%3C%2Ftd%3E%3Ctd%3E0.732%3C%2Ftd%3E%3Ctd%3E0.768%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ECosmos%2DPredict2.5%2D14B%20%5Bpre%2Dtrain%5D%3C%2Ftd%3E%3Ctd%3E0.791%3C%2Ftd%3E%3Ctd%3E0.722%3C%2Ftd%3E%3Ctd%3E0.757%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ECosmos%2DPredict2.5%2D14B%20%5Bpost%2Dtrain%5D%3C%2Ftd%3E%3Ctd%3E0.803%3C%2Ftd%3E%3Ctd%3E0.732%3C%2Ftd%3E%3Ctd%3E0.768%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EWan2.1%2D1.3B%3C%2Ftd%3E%3Ctd%3E0.786%3C%2Ftd%3E%3Ctd%3E0.726%3C%2Ftd%3E%3Ctd%3E0.756%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EWan2.1%2D14B%3C%2Ftd%3E%3Ctd%3E0.794%3C%2Ftd%3E%3Ctd%3E0.727%3C%2Ftd%3E%3Ctd%3E0.761%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EWan2.2%2D5B%3C%2Ftd%3E%3Ctd%3E0.797%3C%2Ftd%3E%3Ctd%3E0.730%3C%2Ftd%3E%3Ctd%3E0.764%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EWan2.2%2D27B%2DA14B%3C%2Ftd%3E%3Ctd%3E0.810%3C%2Ftd%3E%3Ctd%3E0.728%3C%2Ftd%3E%3Ctd%3E0.769%3C%2Ftd%3E%3C%2Ftr%3E%3C%2Ftable%3E--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-train-using-the-ada--><!--anchor:quote:We%20train%20using%20the%20AdamW%20optimizer%20with%20%24%5Cbeta%20_%20%7B%201%20%7D%20%3D%200%20.%209%24%20and%20%24%5Cbeta%20_%20%7B--><!--ref:r-we-train-using-the-ada--><!--anchor:quote:We%20train%20using%20the%20AdamW%20optimizer%20with%20%24%5Cbeta%20_%20%7B%201%20%7D%20%3D%200%20.%209%24%20and%20%24%5Cbeta%20_%20%7B--><!--ref:r-nvidia-sup-1-sup--><!--anchor:quote:NVIDIA%3Csup%3E1%3C%2Fsup%3E--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-in-contrast-to-the-pip--><!--anchor:quote:In%20contrast%20to%20the%20pipeline%20in%20%5BCosmos%2DPredict1%5D%2C%20the%20%5BCosmos%2DPredict2.5%5D%20pipeline%20scales%20to%20a%20much%20larger%20volume%2C%20processing%2035%20million%20hours--><!--ref:r-table-tr-td-confi-gur--><!--anchor:quote:%3Ctable%3E%3Ctr%3E%3Ctd%3EConfi%20guration%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D2B%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D14B%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Layers%3C%2Ftd%3E%3Ctd%3E32%3C%2Ftd%3E%3Ctd%3E36%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EModel%20Dimension%3C%2Ftd%3E%3Ctd%3E2%2C048%3C%2Ftd%3E%3Ctd%3E5%2C120%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EFFN%20Hidden%20Dimension%3C%2Ftd%3E%3Ctd%3E8%2C192%3C%2Ftd%3E%3Ctd%3E20%2C480%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EAdaLN%2DLoRA%20Dimension%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Attention%20Heads%3C%2Ftd%3E%3Ctd%3E16%3C%2Ftd%3E%3Ctd%3E40%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EHead%20Dimension%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EMLP%20Activation%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3EGELU%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EPositional%20Embedding%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3E3D%20RoPE%3C%2Ftd%3E%3C%2Ftr%3E%3C%2Ftable%3E--><!--ref:r-table-tr-td-confi-gur--><!--anchor:quote:%3Ctable%3E%3Ctr%3E%3Ctd%3EConfi%20guration%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D2B%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D14B%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Layers%3C%2Ftd%3E%3Ctd%3E32%3C%2Ftd%3E%3Ctd%3E36%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EModel%20Dimension%3C%2Ftd%3E%3Ctd%3E2%2C048%3C%2Ftd%3E%3Ctd%3E5%2C120%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EFFN%20Hidden%20Dimension%3C%2Ftd%3E%3Ctd%3E8%2C192%3C%2Ftd%3E%3Ctd%3E20%2C480%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EAdaLN%2DLoRA%20Dimension%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Attention%20Heads%3C%2Ftd%3E%3Ctd%3E16%3C%2Ftd%3E%3Ctd%3E40%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EHead%20Dimension%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EMLP%20Activation%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3EGELU%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EPositional%20Embedding%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3E3D%20RoPE%3C%2Ftd%3E%3C%2Ftr%3E%3C%2Ftable%3E--><!--ref:r-6-5-synthetic-data-gen--><!--anchor:quote:6.5%20Synthetic%20Data%20Generation%20for%20VLA%20training%20.%2032-->
- è¿è¡ç¯å¢/ä¾èµï¼FSDP2, TorchTitan, Ulysses-style context parallelism, 4096 NVIDIA H100 GPUsãä¾èµWAN2.1 VAE, Cosmos-Reason1ç­ã
- å¼æºä»£ç ï¼https://github.com/nvidia-cosmos/cosmos-predict2.5ï¼pinned commit `a2c298b0a3df3778b973fe65e9e58877b292d8a7`ã

æå»ºç»æï¼
## ð ï¸ å·¥ç¨ä¸å¤ç°è¦ç¹
ç»è®ºåç½®ï¼Cosmos-Predict2.5 çå·¥ç¨å®ç°é«åº¦ä¾èµå¤§è§æ¨¡åå¸å¼è®­ç»æ¡æ¶ä¸ç¹å®çç¡¬ä»¶å¼æºä»£ç æä¾äºæ ¸å¿æ¨çä¸å¾®è°é¢è®­ç»å¤ç°ä»éæé«çç®åé¨æ§ä¸éæ§å·¥ç¨è°ä¼ã

### æ¨¡åè§æ¨¡ä¸æ ¸å¿æ¶æ
ä»ç»2Bå14Bçåºå«ï¼DiTä¸»å¹²ï¼Flow matchingï¼3D RoPEï¼WAN2.1 VAEã
ç¨è¡¨æ ¼å¯¹æ¯2Bå14Bçç»æã

### è®­ç»åè°åº¦ä¸å¤±ææ¨¡å¼è§é¿
ä»ç»timestep shiftï¼é«åªå£°ééæ ·ï¼å­¦ä¹ çç­ã
è¯´æä¸ºä»ä¹è¿ä¹åï¼è§£å³é«åªå£°åºåè®­ç»ä¸è¶³å¯¼è´çå¸§é´ è¿è¡ç¯å¢ãåå¸å¼ç­ç¥ä¸ä»ç»4096 H100ï¼FSDP2ï¼Context Parallelismã
ç»åºä»£ç ä»åºåcommitã

ç»å¾ï¼
è®­ç»é¶æ®µä¸å¹¶è¡ç­ç¥çæµç¨å¾ææ¶æä¾èµç»ä¸ä¸ªæ¨¡åç»ä»¶ä¸æ°æ®æµçå¾ã
è¿éç»ä¸ä¸ªâå¤é¶æ®µæµç¨è®­ç»æ¶æä¾èµâã
éæ©âåå¸å¼è®­ç»ä¸æ¨¡åç»ä»¶ä¾èµâï¼
```mermaid
flowchart TD
    subgraph æ ¸å¿ç»ä»¶
        A[ææ¬(Cosmos-Reason1)
        C["è§é¢å¸§"] --> D(WAN2.1 VAE)
    end
    subgraph DiT ä¸»å¹²ç½ç»
        B --> E{Cross-Attention}
        D --> E
        E --> F["3D RoPE ç¸å¯¹ä½ç½®ç¼ç "]
        F --> G["Flow Matching éåº¦é¢æµ"]
    end
    subgraph åå¸å¼è®­ç»ç¯å¢
        G --> H["FSDP2 åæ°åç"]
        H --> I["Ulysses ä¸ä¸æå¹¶è¡"]
        I --> J((4096 H100 éç¾¤))
    end
```
æ£æ¥Mermaidè§èï¼
- ç¦ç¨ `%%{init}` ä¸`
- åªç¨ `classDef`+`class`
- æ¯å¾ â¤4 ä¸ªè¯­ä¹è²ä¸æ¯è²å«æå­ `color:`
- snake_case èç¹ idï¼æ ç­¾ 3-6 è¯ä¸»å¨è¯­æï¼è¾¹æ ç­¾ 1-4 è¯ï¼å½¢ç¶ä¸è´ã

ä¿®æ¹Mermaidï¼
```mermaid
flowchart TD
    subgraph
        text_input[ææ¬æç¤º_enc(Cosmos-Reason1 ç¼ç )
        video_input["åå§è§é¢å¸§"] --> vae_enc(WAN2.1 VAE åç¼©)
    end
    subgraph DiTä¸»å¹²ç½ç»
        text_enc --> cross_attn{Cross-Attention èå}
        vae_enc --> cross_attn
        cross_attn --> rope_layer["3D RoPE ä½ç½®ç¼ç "]
        rope_layer --> flow_pred["Flow Matching éåº¦é¢æµ"]
    end
    subgraph åå¸å¼è®­ç»ç¯å¢
        flow_pred --> fsdp_shard["FSDP2 åæ°åç"]
        fsdp_shard --> context_par["Ulysses ä¸ä¸æå¹¶è¡"]
        context_par --> h100_cluster((4096 H100 éç¾¤))
    end
    
    classDef input_comp fill:#e1f5fe,stroke:#01579b,color:#01579b;
    classDef dit_net fill:#fff3e0,stroke:#e65100,color:#e65100;
    classDef dist_env fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20;
    
    class text_input,video_input input_comp;
    class text_enc,vae_enc,cross_attn,rope_layer,flow_pred dit_net;
    class fsdp_shard,context_par,h100_cluster dist_env;
```
èç¹idï¼snake_caseãæ ç­¾3-6è¯ãè¾¹æ ç­¾1-4è¯ï¼è¿éæ²¡å è¾¹æ ç­¾ï¼å¯ä»¥å ä¸ç¹ï¼ã
ä¿®æ¹è¾¹æ ç­¾ï¼
```mermaid
flowchart TD
    subgraph æ ¸å¿ text_input[ææ¬|æåè¯­ä¹| text_enc(Cosmos-Reason1 ç¼ç )
        video_input["åå§è§é¢å¸§"] -->|æ¶ç©ºåç¼©| vae_enc(WAN2.1 VAE åç¼©)
    end
    subgraph DiTä¸»å¹²ç½ç»
        text_enc -->æ¡ä»¶| cross_attn{Cross-Attention èå}
        vae_encç¹å¾| cross_attn
        cross_attn -->|æ·»å ä½ç½®| rope_layer["3D RoPE ä½ç½®ç¼ç "]
        rope_layer -->|é¢æµè½¨è¿¹| flow_pred["Flow Matching éåº¦é¢æµ"]
    end
    subgraph åå¸å¼è®­ç»ç¯å¢
        flow_pred -->|æ¢¯åº¦åæ­¥| fsdp_shard["FSDP2 åæ°åç"]
        fsdp_shard -->|åºååå| context_par["Ulysses ä¸ä¸æå¹¶è¡"]
        context_par -->|ç®åæ¯æ| h100_cluster((4096 H100 éç¾¤))
    end
    
    classDef input_comp fill:#e1f5fe,stroke:#01579b,color:#01579b;
    classDef dit_net fill:#fff3e0,stroke:#e65100,color:#e65100;
    classDef dist_env fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20;
    
    class text_input,video_input input_comp;
    class text_enc,vae_enc,cross_attn,rope_layer,flow_pred dit_net;
    class fsdp_shard,context_par,h100_cluster dist_env;
```
å¦ä½è¯»è¿å¼ å¾ï¼ä»é¡¶é¨çå¤æ¨¡ï¼ç»è¿ç¼ç ä¸åç¼© ä¸»å¹²è¿è¡ç¹å¾èåä¸éåº¦é¢æµï¼åºå±å±ç¤ºäºæ¯æè¯¥åºå¤§è®¡ç®éçåå¸å¼è®­ç»ç¯å¢ååç­ç¥ã

è¡¨æ ¼ï¼2Bä¸14Bæ¨¡åç»æå¯¹æ¯
 | Cosmos-Predict2.5-2B | Cosmos-Predict2.5-14B |
|---|---|---|
| å±æ° (Layers) | 32 | 36 |
| æ¨¡åç»´åº¦ (Model Dim) | 2,048 | 5,120 |
| FFN éèç»´åº¦ | 8,192 | 20,480 |
| æ³¨æåå¤´æ° | 16 | 40 |


å­¦ä¹ çï¼2Bç¨ 3e-5ï¼14Bç¨ 1.3e-5ã
é«åªå£°ééæ ·ï¼5%æ ·æ¬ä»æé«2%åªå£°æ½åãè§£å³<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C-->

ä»åºï¼https://github.com/nvidia-cosmos/cosmos-predict2.5
Commit: `a2c298b0a3df3778b973fe65e9e58877b292d8a7`

æ£æ¥çº¦æï¼
1. ç»è®ºåç½®ï¼é¦æ®µç»åºç»è®ºã
2. å¿ å®ä¸ä¸¥è°¨ï¼ä¸ç¼é ã
3. æ¥å°ç²¾ç¡®æ§è½æ°å­ã
4.50-800å­ã
5. åªè¾åºæ­£æï¼ä»¥â## å·¥ç¨ä¸å¤ç°è¦ç¹âå¼å¤´ã

æ°å ð ï¸ å·¥ç¨ä¸å¤ç°è¦ç¹

**ç»è®ºåç½®**ï¼Cosmos-Predict2.5 çå·¥ç¨å®ç°é«åº¦ä¾èµå¤§è§æ¨¡åå¸å¼è®­ç»æ¡æ¶ä¸ç¹å®çç¡¬ä»¶å¼æºä»£ç æä¾äºæ ¸å¿æ¨çä¸å¾®è°é¢è®­ç»å¤ç°ä»éæé«çç®åé¨æ§ä¸éæ§çå·¥ç¨è°ä¼ï¼å¦é«åªå£°ééæ ·ä¸æ¸è¿å¼åè¾¨çè°åº¦ï¼ã

### æ¨¡åè§æ¨¡ä¸Cosmos-Predict2.5 åå¸äº 2B å 14B ä¸¤ç§åæ°è§æ¨¡ï¼åå¤ç¨ DiT é£æ ¼ç latent diffusion velocity prediction networkï¼å¹¶åºäº flow matching é¢æµéåº¦ãä¸ºäºè®©æ¨¡åçµæ´»å¤çé«åè¾¨çä¸é¿åºåï¼æ¶æç§»é¤äº absoluteè½¬å 3D RoPE ç¸å¯¹ä½ç½®ç¼ç ãè§è§ç«¯éç¨ WAN2.1 VAE è¿è¡ $4 \times 8 \times 8$ çæ¶ç©ºåç¼©ï¼ææ¬ç«¯åç¨ Cosmos-Reason1 æ¿æ¢äºä¼ ç»ç T5 encoderã

| -Predict2.5-2B | Cosmos-Predict2.5-14B |
|---|---|---|
| ç½ç»å±æ° | 32 | 36 |
| æ¨¡åç»´åº¦ | 2,048 | 5,120 |
| FFN éèç»´åº¦ | 8,192 | 20,480 |
| æ³¨æåå¤´æ° | 16 | 40 |

###è°åº¦ä¸å¤±ææ¨¡å¼è§é¿
å¨è®­ç»è°åº¦ä¸ï¼è®ºæéå¯¹è§é¢çæä¸­å¸¸è§çâå¸§é´è¿æ¸¡âè¿ä¸å¤±æä¿®æ­£ãåªå£°åºåè®­ç»æ ·æ¬è¿å°ï¼åªå£°ééæ ·ç­ç¥ï¼æ¾å¼å°é¨åè®­ç»æ ·æ¬ä»åªå£°åå¸çæé«åºé´æ½åãæ­¤å¤ï¼timestep åå¸éç¨ logit-normalï¼å¹¶éåè¾¨çæååºç¨ progressive timestep shiftï¼ä» 256p ç $\beta=1$ å¢è³ 720p ç $\beta=5$ï¼ï¼è¿«ä½¿æ¨¡åå¨å¼ºå­¦ä¹ éå»ºç»æãä¼åå¨ç»ä¸ä½¿ç¨ AdamWï¼2B ä¸ 14B æ¨¡ååå«éç¨ä¸åçå­¦ä¹ çä»¥ã

<details>
<summary><strong>é¢å SFT ä¸æ¨¡ååå¹¶ç»è</strong></summary>
å¨ SFT é¶æ®µï¼æ¨¡åéå¯¹ object permanenceãhigh motion ç­ç¹å®é¢ååç¬å¾®è°ãä¸ºäºèåè¿äºä¸åè½åå¹¶ç¼è§£éç¨åéåï¼å¢éå¯¹æ¯äº model soupãTIESãDARE-Linear ç­æ¹æ³ãæç»éè¿ç®åç grid search éæ©äº model soup åä½ï¼ç0 ä¸ªåå¹¶åéæ¨¡åï¼è¯æäºç®åå¹³ååºäºåä¸æ¨¡åèççå¯åå¼éæ©ã
</details>

### è¿è¡ç¯å¢ãåå¸å¼
æ¯æè¯¥æ¨¡åè®­ç»çæ¯ç± 4096 å¼  NVIDIA H100 GPUs ç»æçéç¾¤ãå·¥ç¨ä¸æ·±åº¦ä¾èµ FSDP2 ä½ä¸ºåå¸å¼è®­ç»æ¡æ¶ï¼å¹¶ç»å TorchTitan ä¼åä¸ Ulysses-style context parallelismãå¨ 720pã93 frames çè®­ç»B æ¨¡åä½¿ç¨ context parallelism size 2ï¼è 14B æ¨¡ååæ©å±è³ size 8 ä»¥ååé¿ã

```mermaid
flowchart TD
    subç»ä»¶
        text_input[ææ¬æç¤ºæåè¯­ä¹| text_enc(Cosmos-Reason1 ç¼ç )
        video_input["åå§è§é¢å¸§"] -->|æ¶ç©ºåç¼©| vae_enc(WAN2.1 VAE åç¼©)
    end
    subgraph DiTä¸»å¹²ç½ç»
        text_enc| cross_attn{Cross-Attention èå}
        vae_enc| cross_attn
        cross_attn -->|æ·»å ä½ç½®| rope_layer["3D RoPE ä½ç½®ç¼ç "]
        rope_layer -->|é¢æµè½¨è¿¹| flow_pred["Flow Matching éåº¦é¢æµ"]
    end
    subgraph åå¸å¼è®­ç»ç¯å¢
        flow_pred -->|æ¢¯åº¦åæ­¥| fsdp_shard["FSDP2 åæ°åç"]
        fsdp_shard -->|åºååå| context_par["Ulysses ä¸ä¸æå¹¶è¡"]
        context_par -->|ç®åæ¯æ| h100_cluster((4096 H100 éç¾¤))
    end
    
    classDef input_comp fill:#e1f5fe,stroke:#01579b,color:#01579b;
    classDef dit_net fill:#fff3e0,stroke:#e65100,color:#e65100;
    classDef dist_env fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20;
    
    class text_input,video_input input_comp;
    class text_enc,vae_enc,cross_attn,rope_layer,flow_pred dit_net;
    class fsdp_shard,context_par,h100_cluster dist_env;
```
*å¦ä½è¯»è¿å¼ å¾ï¼ä»é¡¶é¨çå¼å§ï¼ç»è¿ç¼ç  DiT ä¸»å¹²è¿è¡ç¹å¾èåä¸éåº¦é¢æµï¼åºå±å±ç¤ºäºæ¯æè¯¥åºå¤§è®¡ç®éçåå¸å¼è®­ç»ç¯å¢ååç­ç¥ã*

å¯¹äºå¸æå¤ç°æå¾®è°çå·¥ç¨å¸ï¼å®æ¹å¼æºäºæ ¸å¿ä»£ç ä»åºï¼`https://github.com/nvidia-cosmos/cosmos-predict2.5`ï¼ï¼å»ºè®®éå®å¨éªè¯è¿ç commit `a2c298b0a3df3778b973fe65e9e58877b292d8a7`ãéè¦æ³¨æçæ¯ï¼å¼æºä»åºä¸»è¦æä¾æ¨çä¸ä¸æ¸¸ä»»å¡ï¼å¦ Transfer2.5 æ§å¶åæ¯ï¼çï¼å®æ´çé¢è®­ç»æ°æ®è¿æ»¤ç®¡çº¿ä¸ RL post-training ç VideoAlign å¥å±æ¨¡åä»éä¾èµå¤é¨ç»ä»¶æèªè¡æ­å»ºã

å­æ°æ£æ¥ï¼
ä¸æ®µä¸æ®µç®ï¼
ç»è®ºï¼70å­
æ¨¡åè§æ¨¡ï¼160å­
è¡¨æ ¼ï¼50å­
è®­ç»80å­
æå åï¼120å­
è¿è¡ç¯å¢ï¼130å­
Mermaidåè¯´æï¼100ï¼120å­
æ»è®¡å¤§çº¦ 800-900å­ï¼ç¨å¾®ç²¾ç®ä¸ç¹ï¼æ§å¶å¨8ã

ç²¾ç®ï¼
âå¨è®­ç»è°åº¦ä¸ï¼è®ºæéå¯¹è§é¢çæä¸­å¸¸è§çâå¸§èªç¶è¿æ¸¡âè¿ä¸å¤±ææ¨¡å¼ï¼ååºäº âéå¯¹è§é¢çæä¸­å¸¸è§çæ¨¡å¼è°åº¦ä¿®æ­£ãâ
âåªå£°åºåè®­ç»æ ·æ¬è¿å°ï¼å æ­¤éæ ·ç­ç¥ï¼æ¾å¼å°é¨åè®­ç»æ ·æ¬ä»åªå£°åå¸çæé«åºé´æ½åãâ -> âéè¿é«åªå£°ééæ ·ç­ç¥ï¼æ¾å¼å°é¨åæ ·æ¬ä»åªå£°åå¸æé«åºé´æ½åï¼å¼¥è¡¥é«åªåºåè®­ç»ä¸è¶³ãâ
âæ­¤å¤ï¼timestep åå¸éç¨ logit-normalï¼å¹¶éåè¾¨çæååºç¨ progressive timestep shiftï¼ä» 256p ç $\beta=1$ å¢è³ 720p ç $\beta=5$ï¼ï¼è¿«ä½¿è¢«ç ´åæ¶å­¦ä¹ éå»ºç»æãâ -> âåæ¶ï¼timestep éç¨ logit-normal åå¸ï¼å¹¶éåè¾¨çåºç¨ progressive timestep shiftï¼$\beta$ ä» 1 å¢è³ 5ï¼ï¼è¿«ä½¿æ¨¡åå¨å¼ºå­¦ä¹ éå»ºç»æãâ

ç²¾ç®åå­æ°å¤§æ¦å¨ 750 å­å·¦å³ï¼ç¬¦å 350-800 çè¦æ±ã

æ£æ¥æ¥å°è§åï¼
- æ²¡æç²¾ç¡®æ§è½æ°å­ï¼å¦åç¡®çãæåç¾åæ¯ï¼ã
- éæ§è½æ°å­ï¼2B, 14B, 32å±, 4096 H100, 256p, 720p, 93 frames, 4x8x8ï¼æ­£å¸¸ä¿çã
- ä¸æåè¯ï¼Cosmos-Predict2.5, DiT, flow matching, 3D RoPE, WAN2.1 VAE, Cosmos-Reason1, T5, AdamW, logit-normal, progressive timestep shift, FSDP2, TorchTitan, Ulysses-style context parallelism, VideoAlign, Transfer2.5ï¼ä¿çåæ ·ã
-beta=1$, $4 \times 8 \times 8$ ä¿çã

æ£æ¥Mermaidè§èï¼
- æ  `%%{init}`ï¼style`ã
- åªæ `classDef` å `class`ã
- 3ä¸ªè¯­ä¹è²ï¼æ¯ä¸ªå¸¦ `color:`ã
- èç¹ id æ¯ snake_caseã
- æ ç­¾ 3-6 è¯ï¼å¦âææ¬æç¤ºâãâCosmos-Reason1 ç¼ç âãâCross-Attention èåâç­ï¼ä¸­æç®è¯çè¯å¯è½ç¨å¾®å®½æ¾ï¼ä½å°½éä¿æç®ç­ï¼ã
- è¾¹æ ç­¾ 1-4 è¯ï¼âæåè¯­ä¹âãâï¼ã
- å½¢ç¶ä¸è´ï¼é¤äºå¤å®è±å½¢ååæ±ï¼è¿éç¨äºåè§åè±å½¢ï¼ç¬¦åè§èï¼ã

æ£æ¥æå åï¼
ä½¿ç¨äº `<details><summary><strong>...</strong></summary> ... </details>`ï¼æ²¡æè£¸æ§è½æ°å­ã

æ£æ¥è¡¨æ ¼ï¼
æè¡¨å¤´ï¼æ åä½ï¼å ä¸ºæ¯çº¯æ°å­ï¼ï¼<=5åï¼æ¯æ ¼1-5è¯ã

æç»ç¡®è®¤æ è¯¯ã
## ð ï¸ å·¥ç¨ä¸å¤ç°è¦ç¹

**ç»è®ºåç½®**ï¼Cosmos-Predict2.5 çå·¥ç¨å®ç°é«åº¦ä¾èµå¤§è§æ¨¡åå¸å¼è®­ç»æ¡æ¶ä¸ç¹å®çç¡¬ä»¶å¹¶è¡ç­ç¥æä¾äºæ ¸å¿æ¨çä¸å®æ´é¢è®­ç»å¤ç°ä»éæé«çç®åé¨æ§ä¸éæ§çå·¥ç¨è°ä¼ï¼å¦é«åªå£°ééæ ·ä¸æ¸è¿å¼åè¾¨çè°åº¦ï¼ã

### æ¨¡åè§æ¨¡
Cosmos-Predict2.5 åå¸äº 2B å 14B ä¸¤ç§åæ°è§æ¨¡ï¼åå¤ç¨ DiT é£æ ¼ç latent diffusion velocity prediction networkï¼å¹¶åºäº flow matching é¢æµéåº¦ãä¸ºçµæ´»å¤çé«åè¾¨çä¸é¿åºåï¼æ¶æç§»é¤äº absolute positional embeddingsï¼D RoPE ç¸å¯¹ä½ç½®ç¼ç ãè§è§ç«¯éç¨ WAN2.1 VAE è¿è¡ $4 \times 8 \times 8$ çæ¶ç©ºåç¼©ï¼ææ¬ç«¯åç¨ Cosmos-Reason1 æ¿æ¢äºä¼ ç»ç T5 encoderã

 | Cosmos-Predict2.5-2B | Cosmos-Predict2.5-14B |
|---|---|---|
| ç½ç»å±æ° | 32 | 36 |
| æ¨¡åç»´åº¦ | 2,048 | 5,120 |
| FFN éèç»´åº¦ | 8,192 | 20,480 |
| æ³¨æåå¤´æ° | 16 | 40 |

åè°åº¦ä¸å¤±ææ¨¡å¼è§é¿
éå¯¹è§é¢çæä¸­å¸¸è§çæ¨¡å¼ï¼è®ºæååºäºéè¿é«åªå£°ééæ ·ç­ç¥ï¼æ¾å¼å°é¨åæ ·æ¬ä»åªå£°åå¸æé«åºé´æ½åï¼å¼¥è¡¥é«åªåºåè®­ç»ä¸è¶³ãåæ¶ï¼timestep éç¨ logit-normal åå¸ï¼å¹¶éåè¾¨çåºç¨ progressive timestep shiftï¼$\beta$ ä» 1 å¢è³ 5ï¼ï¼è¿«ä½¿æ¨¡åç ´åæ¶å­¦ä¹ éå»ºç»æãä¼åå¨ç»ä¸ä½¿ç¨ AdamWï¼2B ä¸ 14B æ¨¡ååå«éç¨ä¸åçå­¦ä¹ çç¨³å®æ§ã

<details>
<summary><strong>é¢å SFT ä¸æ¨¡ååå¹¶ç»è</strong></summary>
å¨ SFT é¶æ®µï¼æ¨¡åéå¯¹ object permanenceãhigh motion ç­ç¹å®é¢ååç¬å¾®è°ãä¸ºäºèåä¸åè½åå¹¶ç¼è§£éç¨åéåï¼å¢éå¯¹æ¯äº model soupãTIESãDARE-Linear ç­æ¹æ³ãæç»éè¿ç®åç grid search éæ©äº model soup åä½ 20 ä¸ªåå¹¶åéæ¨¡åï¼è¯æäºç®åå¹³ååºäºåä¸æ¨¡åèççå¯åå¼éæ©ã
</details>

### è¿è¡ç¯å¢ãåå¸å¼
æ¯æè¯¥æ¨¡åè®­ç»çæ¯ç± 4096 å¼  NVIDIA H100 GPUs ç»æçéç¾¤ãå·¥ç¨ä¸æ·±åº¦ä¾èµ FSDP2 ä½ä¸ºåå¸å¼è®­ç»æ¡æ¶ï¼å¹¶ç»å TorchTitan ä¼åä¸ Ulysses-style context parallelismãå¨ 720pã93 frames 2B æ¨¡åä½¿ç¨ context parallelism size 2ï¼è 14B æ¨¡ååæ©å±è³ size 8 ä»¥åã

```mermaid
flowchart TD
    subç»ä»¶
        text_input[ææ¬æç¤ºæåè¯­ä¹| text_enc(Cosmos-Reason1 ç¼ç )
        video_input["åå§è§é¢å¸§"] -->|æ¶ç©ºåç¼©| vae_enc(WAN2.1 VAE åç¼©)
    end
    subgraph DiTä¸»å¹²ç½ç»
        text_enc| cross_attn{Cross-Attention èå}
        vae_enc --> cross_attn
        cross_attn -->|æ·»å ä½ç½®| rope_layer["3D RoPE ä½ç½®ç¼ç "]
        rope_layer -->|é¢æµè½¨è¿¹| flow_pred["Flow Matching éåº¦é¢æµ"]
    end
    subgraph åå¸å¼è®­ç»ç¯å¢
        flow_pred -->|æ¢¯åº¦åæ­¥| fsdp_shard["FSDP2 åæ°åç"]
        fsdp_shard -->|åºååå| context_par["Ulysses ä¸ä¸æå¹¶è¡"]
        context_par -->|ç®åæ¯æ| h100_cluster((4096 H100 éç¾¤))
    end
    
    classDef input_comp fill:#e1f5fe,stroke:#01579b,color:#01579b;
    classDef dit_net fill:#fff3e0,stroke:#e65100,color:#e65100;
    classDef dist_env fill:#e8f5e9,stroke:#1b5e20,color:#1b5e20;
    
    class text_input,video_input input_comp;
    class text_enc,vae_enc,cross_attn,rope_layer,flow_pred dit_net;
    class fsdp_shard,context_par,h100_cluster dist_env;
```
*å¦ä½è¯»è¿å¼ å¾ï¼ä»é¡¶é¨çå¤ï¼ç»è¿ç¼ç ä¸T ä¸»å¹²è¿è¡ç¹å¾èåä¸éåº¦é¢æµï¼åºå±å±ç¤ºäºæ¯æè¯¥åºå¤§è®¡ç®éçåå¸å¼è®­ç»ç¯å¢ååç­ç¥ã*

å¯¹äºå¸æå¤ç°çå·¥ç¨å¸ï¼å®æ¹å¼æºäºæ ¸å¿ä»£ç ä»åºï¼`https://github.com/nvidia-cosmos/cosmos-predict2.5`ï¼ï¼å»ºè®®éå®å¨éªè¯è¿ç commit `a2c298b0a3df3778b973fe65e9e58877b292d8a7`ãéæ³¨æï¼å¼æºä»åºä¸»è¦æä¾æ¨çä¸ä¸æ¸¸ä»»å¡ï¼å¦ Cosmos-Transfer2.5 æ§å¶åæ¯å®æ´çé¢è®­ç»æ°æ®è¿æ»¤ç®¡çº¿ä¸ RL post-training ç VideoAlign å¥å±æ¨¡åä»éä¾èµå¤é¨ç»ä»¶æèªè¡æ­å»ºã

ç¨æ·è¦æ±æä½ä¸ºèµæ·±ä¸­æææ¯æ·±åº¦ç§æ®è®ºææ·±åº¦è§£è¯»æ¥åä¸­çä¸èï¼âå±éä¸éç¨è¾¹çâã
éè¦ä¸¥æ ¼éµå®ä»¥ä¸è§èï¼
1. **ç»æ**ï¼ç»è®ºåç½®ï¼åå±å¼ãä»¥ `## å±éä¸éç¨è¾¹ç` å¼å¤´ï¼H2ï¼ï¼H2å¥é¦å¯å¸¦emojiï¼H3/H4ä¸å¸¦ã
2. **å¿ å®ä¸ä¸¥è°¨**ï¼æç¡®åºåâå£°ç§°âä¸âè¯æâï¼ä¸»å¨ç¹åå¤±ææ¨¡å¼ï¼è¿åº¦å®£ç§°ãå¿½ç¥æ¿ä»£è§£éç­ï¼ï¼è¯´ææ¯å¦æ¥åæ¶è/è´ç»æãè¯å®ä¸è´¬ä½ã
3. **æ¥å°**ï¼**ç»å¯¹ä¸è¦å¨åè¿°å¥å­éåç²¾ç¡®æ§è½æ°å­**ãæ§è½å¯¹æ¯ç¨å®æ§è¯­è¨ãç²¾ç¡®æ°å¼åªæ´»å¨è¯æ®è¡¨åæ ¸å¿ç»è®ºåï¼ç³»ç»èªå¨å¤çï¼æä¸åï¼ãéæ§è½æ°å­ï¼å±æ°ãGPUæ°ç­ï¼å¯åãä¸æåæ ·ã
4. **å¾è¡¨åäº**ï¼æ¶åæµç¨/ç»æ/Mermaidï¼ãè¿éè®²å±éåè¾¹çï¼å¯ä»¥ç»ä¸ä¸ªâéç¨è¾¹çä¸å¤±ææ¨¡å¼å³ç­å¾âæâé·è¾¾å¾/æµç¨å¾âãMermaidè§èï¼ç¦ç¨ `%%{init}` `style`ï¼åªç¨ `classDef`+`class`ï¼â¤4ä¸ªè¯­ä¹è²ä¸å¸¦æå­ `color:`ï¼snake_caseèç¹idï¼æ ç­¾3-6è¯ï¼è¾¹æ ç­¾1-4è¯ï¼å½¢ç¶ä¸è´ãå¤æåº¦â¤10èç¹å¹³éºæsubgraphã
5. **è¡¨æ ¼ vs åè¿°**ï¼ç»æåå¯¹æ¯ç¨è¡¨ã
6. **æ·±åº¦èè¿æå å**ï¼åé¿ç»èç¨ `<details>` æå ã
7. **äºå®æº**ï¼
   - æ²¡ç» RL post-training å®æ´æ¾å¼æå¤± VideoAlign rewardãtrajectory probability decomposition å diffusion loss regularizationã
   - Cosmos-Transfer2.5 ç control branch ç»èä¾èµ Cosmos-Transfer1ï¼æ¬æåªè¯´æ control blocks ã
   - å¤å¤åºç¨å®éªæ¯ç¹å® roboticsãdriving æ camera-control è®¾ç½® embodimentãä¼ æå¨å¸å±ååºæ¯ç±»åéè¦åéªè¯ã
   - action-conditioned æ¨¡ååªæ¯è¾ TimeEmbeddingãCrossAtten å ChannelConcat ä¸ç§å¨ä½ç©·å°½ææå¨ä½æ¡ä»¶åè®¾è®¡ã
   - é¿è§é¢çæä»éç¨ chunked autoregressive æ¹å¼ï¼éç¹è¯ä¼°è¯¯å·®ç´¯ç§¯ä½æªå£°ç§°å½»åºæ¶é¤ç´¯ç§¯ã
   - æ°æ®å¤çãreward serviceãè®­ç»åºç¡è®¾æ½ä¾èµå¤§è§æ¨¡ GPUãå¤é¨ reward models åä¸ææ°æ®ç®¡çº¿ï¼å¤ç°ææ¬é«ã
   - Cosmos-Reason1 ç vision encoder å¯æ¯æé¢å¤è§è§ controlï¼ä½è®ºä½ future explorationã

æèç»æï¼
- **ç»è®ºåç½®**ï¼Cosmos ç³»åå¨ç¹å®åºæ¯ä¸å±ç°äºå¼ºå¤§çç©çä¸çæ¨¡æåæ§ãé¿æ¶åºä¸è´æ§ä»¥åå¤ç°é¨æ§ææäºææ¾çéç¨è¾¹çãå®å¹¶éä¸ä¸ªâå¼ç®±å³ç¨âçéç¨ä¸çæ¨¡åï¼èæ¯ä¸ä¸ªé«åº¦ä¾èµç¹å®æ°æ®ç®¡çº¿åç®ååºç¡è®¾æ½çâéåæ­¦å¨âã
- **Mermaid å¾**ï¼éç¨è¾¹çä¸å¤±ææ¨¡å¼å¤å®æµç¨ï¼flowchartï¼ã
- **åç¹å±å¼**ï¼
  1. **åºæ¯æ³èº«ç»å®**ï¼å®éªå±éäºç¹å® roboticsãdriving æ camera-controlã ééªè¯ã
  2. **é¿è§é¢çæçè¯¯å·®ç´¯ç§¯**ï¼chunked autoregressive æ¹å¼ï¼æªå½»åºæ¶é¤ç´¯ç§¯ã
  3. **å¨ä½æ¡ä»¶åä¸ç½ç»è®¾è®¡çæªç«ä¹ä¸**ï¼åªæ¹å¼ï¼Control branch ä¾èµåä»£ï¼RL Style control çä½æªæ¥ã
  4. **å¤ç°å£åä¸åºç¡è®¾æ½ä¾èµ**ï¼å¤§è§æ¨¡ GPUãå¤é¨ reward modelsãä¸ææ°æ®ç®¡çº¿ã
- **æå å** RL post-training æå¤±-conditioned è®¾è®¡æªç©·å°½çè¯¦ç»ææ¯æ¢è®¨ã

èæ Mermaid å¾ï¼
éç¨è¾¹çå¤å®æµç¨ã
```mermaid
flowchart TD
    start_node((è¯ä¼°åºæ¯)) --> check_embodiment{æ¯å¦å±äºç¹å®<br/>æºå¨äººæé©¾é©¶?}
    check_embodiment -- æ¯ --> check<br/>è¿ç»­çæ?}
    check_embodiment -- å¦ --> fail_generalize["æ³åé£é©é«<br/>ééæ°éªè¯"]
    check_length -- æ¯ --> warn_drift["è­¦æè¯¯å·®ç´¯ç§¯<br/>èªåå½æ¼ç§»"]
    check_length -- å¦ --> check_compute/>GPUä¸ä¸æç®¡çº¿?}
    check_compute -- æ¯ --> success_deploy["å¯å°è¯å¤ç°<br/>ä¸å¾®è°é¨ç½²"]
    check_compute -- å¦ --> fail_reproduce["å¤ç°å£åé«<br/>å»ºè®®å¼æº"]
    
    classDef start_class fill:#E3F2FD,stroke:#1565C0,color:#0D47A1;
    classDef decision_class fill:#FFF3E0,stroke:#E65100,color:#BF360C;
    classDef success_class fill:#E8F5E9,stroke:#2E7D32,color:#1B5E20;
    classDef fail_class fill:#FFEBEE,stroke:#C62828,color:#B71C1C;
    
    class start_node start_class;
    class check_embodiment,check_length,check_compute decision_class;
    class success_deploy success_class;
    class fail_generalize,warn_drift,fail_reproduce fail_class;
```
æ£æ¥ Mermaid è§èï¼
- ç¦ç¨ `%%{init}` åè¡ï¼æ»¡è¶³ã
- åªç¨ `classDef`+`class`ï¼æ»¡è¶³ã
- â¤4 ä¸ªè¯­ä¹è²ä¸å«æå­ `color:`ï¼4ä¸ªé¢è²ï¼start, decision, success, failï¼ï¼é½å¸¦äº `color:`ã
- snake_case èç¹ idï¼æ»¡è¶³ã
- æ ç­¾ 3-6 è¯ä¸»å¨è¯­æ/åè¯ï¼è¯ä¼°åºæ¯(4), æ¯å¦å±äºç¹å®æºå¨äººæé©¾é©¶(10 - ç¨å¾®é¿äºç¹ï¼æ¹æ"å±äºç¹å®æºå¨äººæé©¾é©¶åºæ¯è¿ç»­çæ(8 - æ¹æ"éè¦ æ³åé£é©é«ééæ°éªè¯(10 - æ¹æ"æ³åé£é©é«ééæ°éªè¯"), è­¦æè¯¯å·®ç´¯ç§¯èªåå½æ¼ç§»(10 - æ¹æ"è­¦æèªåå½è¯¯å·®ç´¯ç§¯"),ä¸ä¸æç®¡çº¿(11 - ç®åä¸ç®¡çº¿"), å¯å°è¯å¤ç°ä¸å¾®è°é¨ç½²(10 - æ¹æ"å¯å°è¯å¤ç°ä¸é¨ç½²"), å¤ç°å£åé«å»ºè®®1 - æ¹æ"å¤ç°å£åé«å»ºè®®è§æ")ã
ä¿®æ¹æ ç­¾ä»¥ç¬¦å 3-6 è¯ï¼ä¸­æå­ç®è¯è¿æ¯å­ï¼éå¸¸ä¸­æ3-6ä¸ªå­/è¯ãå°½éç²¾ç®ï¼ã
- è¯ä¼°åºæ¯ (4å­) -> è¯ä¼°ç®æ åºæ¯ (6å­)
- å±äºç¹å®æºå¨äººæé©¾é©¶åºæ¯ (12å­) -> å±äºæºå¨äººæé©¾é©¶åºæ¯ (10å­) -> éå®æºå¨äººæé©¾é©¶ (7å­) -> ç¹å®æºå¨æé©¾é©¶ (7å­) -> åºæ¯ (8å­)ãç®è¯çè¯ï¼âå±äº/èº«/åºæ¯â 4ä¸ªè¯ã
-çæ (8å­) -> éè¦é¿è§é¢è¿ç»­çæ (9å­) -> çæé¿è§é¢åºå (7å­)è§é¢ (6å­)ã
- æ³åé£é©é«ééæ°éªè¯ (10å­) -> æ³åé£é©ééæ°éªè¯ (9å­) -> å­å¨æ³åå¤±æé£é© (8å­) -> æ³åå­å¨å¤±æé£é© (8å­)ã
- è­¦æèªåå½è¯¯å·®ç´¯ç§¯ (9å­) -> è­¦æèªåå½è¯¯å·® (7å­) -> å­å¨è¯¯å·®ç´¯ç§¯é£é© (8å­)ã
- ç®¡çº¿ (10å­) -> 7å­) -> æ¥æå¤§è§æ¨¡ç®å (7å­)ã
- å¯å°è¯å¤ç°ä¸é¨ç½² (8å­) -> å¯å°è¯å¤ç°é¨ç½² (7å­) -> éåå¤ç°ä¸é¨ç½² (7å­)ã
- å¤ç°å£åé«å»ºè®®è§æ (9å­) -> å¤ç°å£åè¾é« (6å­)ã

è°æ´ Mermaid:
```mermaid
flowchart TD
    start_node((è¯ä¼°ç®æ åºæ¯)) --> check_embodiment{å±äº?}
    check_embodiment -- æ¯ --> check_length{çæ
    check_embodiment -- å¦ --> fail_generalize["å­å¨æ³åå¤±æé£é©"]
    check_length -- æ¯ --> warn_drift["å­å¨è¯¯å·®ç´¯ç§¯é£é©"]
    check_length -- å¦ --> check_compute{æ¥æå¤§è§æ¨¡ç®å?}
    check_compute -- æ¯ --> success_deploy["éåå¤ç°ä¸é¨ç½²"]
    check_compute -- å¦ --> fail_reproduce["å¤ç°å£åè¾é«"]
    
    classDef start_class fill:#E3F2FD,stroke:#1565C0,color:#0D47A1;
    classDef decision_class fill:#FFF3E0,stroke:#E65100,color:#BF360C;
    classDef success_class fill:#E8F5E9,stroke:#2E7D32,color:#1B5E20;
    classDef fail_class fill:#FFEBEE,stroke:#C62828,color:#B71C1C;
    
    class start_node start_class;
    class check_embodiment,check_length,check_compute decision_class;
    class success_deploy success_class;
    class fail_generalize,warn_drift,fail_reproduce fail_class;
```
è¾¹æ ç­¾ï¼1-4è¯ã
"æ¯" (1), "å¦" (1)ãç¬¦åã
å½¢ç¶ä¸è´ï¼è±å½¢=å¤å®ï¼åæ±=æ°æ®ï¼åè§=èµ·æ­¢ã
start_node æ¯åè§ï¼(( ))ï¼ï¼check æ¯è±å½¢ï¼{ }ï¼ï¼fail/success æ¯æ¹æ¬å·ï¼[ ]ï¼è¿éæ²¡ç¨åè§ï¼æ¹æåè§ ([æ¹æ¬å·ï¼è§èè¯´âåè§=èµ·æ­¢âï¼ä¸­é´èç¹ç¨ç©å½¢æåè§ç©å½¢é½å¯ä»¥ï¼è¿éç¨ç©å½¢ [ ] æåè§ç©å½¢ ([ ])ãä¸ºäºç»ä¸ï¼ä¸­é´ç»æç¨ ([ ]) åè§ç©å½¢ã
ä¿®æ¹ï¼
`fail_generalize([å­å¨æ³åå¤±æé£é©])`
`warn_drift([å­å¨è¯¯å·®ç´¯ç§¯é£é©])`
`success_deploy([éåå¤ç°ä¸é¨ç½²])`
`fail_reproduce([å¤ç°å£åè¾é«])`

æ­£ææ°åï¼
**ç»è®ºåç½®**ï¼
Cosmos èº«åé©¾é©¶åºæ¯ä¸å±ç°äºå¼ºå¤§çç©çä¸çæ¨¡æè½åï¼ãé¿æ¶åºä¸è´æ§ä»¥åå¤ç°é¨æ§ææäºææ¾çéç¨è¾¹çãå®å¹¶éä¸ä¸ªâå¼ç®±å³ç¨âçéç¨ä¸çæ¨¡åï¼èæ¯ä¸ä¸ªé«åº¦ä¾èµç¹å®æ°æ®ç®¡çº¿åç®ååºç¡è®¾æ½çâéåæ­¦å¨âãå¨æ åä¼ æå¨ æ¶ï¼çåå¤ã

**å¾è¡¨**maidã
å¦ä½è¯»è¿å¼ å¾ï¼åºæ¯åºåï¼æ²¿çå³ç­æ åä¸èµ°ãå¦æåºæ¯åç¦»äºè®ºæéªè¯çç¹å® robotics æ driving æ¯æçç®åï¼å°±éè¦è­¦ææ½å¨çå¤±ææ¨¡å¼ã

**åç¹å±å¼**ï¼
1. **åºæ¯æ³åä¸
è®ºæçå¤å¤åºç¨å®éªæ·±åº¦ç»å®äºç¹å®ç roboticsãdriving æ camera-control è®¾ç½®ãè½ç¶æ¨¡åå¨ç©çè§å¾éµå¾ªä¸è¡¨ç°åºè²ï¼ä½è¿ç§è¡¨ç°å¾å¤§ç¨åº¦ä¸å¾çäºç¹å®åºæ¯çé«è´¨éæ°æ®åå¸ã embodimentãæªç¶ä¸åçä¼ æå¨å¸å±æåºæ¯ç±»åæ¶ï¼æ¨¡åå¯è½ä¼é­éåå¸å¤ï¼OODï¼å¤±æãå½¢æçæ³åè½åï¼è¿æå³çå¨æ°ç¡¬ä»¶ä¸é¨ç½²åéªè¯ã

2. **é¿è§é¢çæçè¯¯å·®ç´¯ç§¯**
å¨é¿è§é¢çææ¹é¢ï¼ç³»ç»ä»éç¨ chunked autoregressive æ¹å¼ãè½ç¶è®ºæéç¹è¯ä¼°äºè¯¯å·®ç´¯ç§¯ç°è±¡ï¼æ¶é´ä½å¹¶æªå£°ç§°å½»åºæ¶é¤äºèªåå½çæåºæçæ¼ç§»é®é¢ãéççæåºåçå»¶é¿ï¼å¾®å°çç©çè¿åææåç´ çº§åå·®ä¼éæ¸æ¾å¤§ï¼ç´è§ï¼éä¸¥æ ¼å¯¹åºï¼å°±åå¤å°æºè¿ç»­å¤å°ï¼ä»£æ°è¶å¤ç»èä¸¢å¤±è¶ä¸¥éï¼ãå¯¹äºéè¦æé«é¿æ¶åºä¸è´æ§çä»»å¡ï¼è¿ç§ç´¯ç§¯è¯¯å·®ä»æ¯ä¸å¯å¿½è§çå±éã

3. **å¨ä½æ¡ä»¶åä¸ç½ç»è®¾è®¡çæªç«ä¹ä¸**
å¨ action-conditioned æ¨¡åçè®¾è®¡æ¯è¾äº TimeEmbeddingãCrossAtten å ChannelConcat ä¸ç§å¨ä½ç©·å°½ææå¯è½çå¨ä½æ¡ä»¶åè®¾è®¡ãæ­¤å¤ï¼Cosmos-Transfer2.5 ç control branch ç»èé«åº¦ä¾èµåä»£ Cosmos-Transfer1ç¼ºä¹å¯¹éæãåæ¶ï¼Cosmos-Reason1 ç vision encoder è½æ¯æé¢å¤è§è§æ¡ä»¶ style control çæ½åï¼ä½è®ºä½ future explorationï¼å¼ç®±å³ç¨çé£æ ¼æ§å¶è½åã

4. **å¤ç°å£åä¸åºç¡è®¾æ½ä¾èµ**
è¿æ¯é»ç¢ç¤¾åºå¹¿æ³éªè¯çæå¤§é¨æ§ãæä¸­çæ°æ®å¤çãreward service ä»¥åè®­ç»åºç¡è®¾æ½ï¼æ·±åº¦ä¾èµå¤§è§æ¨¡ GPU éç¾¤ãå¤é¨ reward models åä¸æçæ°æ®ç®¡çº¿ãè®ºææ²¡æç»åº RL post-training çå®æ´æ¾ advantageãtrajectory probability decomposition å diffusion loss regularization ç­æ ¸å¿ç»ä»¶ãè¿ç§âéèµäº§âå±æ§ä½¿å¾ç¬ç«æé¾ä»å¤´å¤ç°è®­ç»æµç¨ã

**æå å**ï¼
<details>
<summary><strong>æ·±åº¦æ¢è®¨ï¼RL </strong></summary>
å¨å¼ºåå­¦ä¹ åè®­ç»ï¼RL post-trainingï¼é¶æ®µï¼è®ºææªæä¾å®æ´çæ¾å¼è¿å¨ä¸å®ç¨åº¦ä¸éä½äºæ¹æ³çå¯å¤ç°æ§ VideoAlign rewardãè®¡ç®ãtrajectory probability decomposition ä»¥å diffusion loss regularization ç­æå­æè¿°æ¥æ¨æµè¿ç§ä¿¡æ¯ç¼ºå¤±å¯è½å¯¼è´å¨å¤ç°æ¶ï¼å¥å±ä¿¡å·çç¼©æ¾æ¯ä¾ææ­£ååæéçå¾®è°
æ­¤å¤ï¼å¨å¨ä½æ¡ä»¶åï¼action-conditionedï¼ TimeEmbeddingãCrossAtten å ChannelConcat ä¸ç§æ¹å¼ï¼å¿½ç¥äºè¯¸å¦ FiLMï¼Feature-wise Linear Modulationï¼æåºäºæ³¨æåæºå¶çæ´ç»ç­æ¿ä»£æ¹æ¡ãæªæ¥åè¿äºæ¿ä»£æ¹æ¡çæ¶èå®éªæè´ç»æï¼ä½¿å¾æä»¬æ æ³å¤æ­å½åéæ©è¿æ¯ä¸çå±é¨æä¼ã
</details>

æ£æ¥çº¦æï¼
1.çå¨ï¼æ¯å»ï¼å¤å°æºè¿ç»­å¤å°ï¼å·²æ æ³¨ç´è§ï¼ãæ ç©ºè¯ã
2. å¿ å®ï¼åªç¨ç»å®äºå®ãä¸æåè¯ï¼Cosmos-Transfer2.5, Cosmos-Transfer1, Cosmos-Reason1, TimeEmbedding, CrossAtten, ChannelConcat, VideoAlign reward, RL post-training, embodiment, camera-control, robotics, driving, chunked autoregressive, style control, future exploration, control branch, control blocks, vision encoderï¼ä¿çåæ ·ãæ ç¼é ã
3ï¼æ²¡æç²¾ç¡®æ§è½æ°å­ãå®æ§æè¿°ï¼âè¡¨ç°åºè²âãâä¸å®âï¼ãéæ§è½æ°å­ï¼ä¸ç§æ­£å¸¸åã
ï¼350-800å­ãå½åå­æ°å¤§çº¦ 800 å­å·¦å³ï¼éå¸¸åéã
5. åªè¾åºæ¬èæ­£æï¼ä»¥ `## å±éä¸éç¨è¾¹ç` å¼å¤´ãæ å¤ä½è§£éã

å¾®è°å­æ°åè¡¨è¾¾ï¼ç¡®ä¿ç´§åä¸ç¬¦åææè§èã
- "Cosmos ç³»åå¨é©¾é©¶åºæ¯ä¸å±ç°äºå¼ºå¤§çç©çä¸çæ¨¡æè½å..." -> ã
- Mermaid å¾æ£æ¥ï¼èç¹ id snake_caseï¼æ ç­¾ 3-6 è¯ï¼è¾¹æ ç­¾ 1-4 è¯ã
  - `start_node` (è¯ä¼°ç®æ åºæ¯ - 4è¯)
  - `check_embodiment` (å±äº - 5è¯)
  - `check_lengthè§é¢ - 4è¯)
  - `fail_generalize` (å­å¨æ³åå¤±æé£é© - 5è¯)
  - `warn_drift` (å­å¨è¯¯å·®ç´¯ç§¯é£é© - 5è¯)
  - `check_compute` (æ¥æå¤§è§æ¨¡ç®å - 4è¯)
  - `success_deploy` (éåå¤ç°ä¸é¨ç½² - 5è¯)
  - `fail_reproduce` (å¤ç°å£åè¾é« - 4è¯)
  å®ç¾ã
- è¡¨æ ¼ vs åè¿°ï¼è¿éæ²¡æææ¾çç»æåå¯¹æ¯éè¦è¡¨æ ¼ï¼åè¿°æ§æ¨çä¸å¡è¿è¡¨ã
- æ·±åº¦èè¿æå åï¼å·²ä½¿ç¨ `<details>`ã

æç»æ£æ¥ï¼
- H2 å¥é¦å¸¦ emojiï¼`## ð å±éä¸éç¨è¾¹ç` ï¼ï¼è§èè¯´âå¯å¸¦âï¼å ä¸ä¸ªæ¯è¾éç®ï¼æ¯å¦ `## ð§ å±éä¸éç¨è¾¹ç`ï¼ã
- H3/H4 ä¸å¸¦ emojiï¼æ¬ææ²¡æç¨ H3/H4ï¼ç´æ¥å ç²å°æ é¢ã
- æ²¡æä½¿ç¨ `[^N]` èæ³¨ã
- æ²¡æç²¾ç¡®æ§è½æ°å­ã

ç¡®è®¤æ è¯¯ï¼è¾åºã
## ð§ å±éä¸éç¨è¾¹ç

Cosmos ç³»åå¨é©¾é©¶åºæ¯ä¸å±ç°äºå¼ºå¤§çç©çä¸çæ¨¡æåæ§ãé¿æ¶åºä¸è´æ§ä»¥åå¤ç°é¨æ§ææäºææ¾çéç¨è¾¹çãå®å¹¶éä¸ä¸ªâå¼ç®±å³ç¨âçéç¨ä¸çæ¨¡åï¼èæ¯ä¸ä¸ªé«åº¦ä¾èµç¹å®æ°æ®ç®¡çº¿åç®ååºç¡è®¾æ½çâéåæ­¦å¨å°éæ åä¼ æå¨åå¥½éæ°éªè¯çåå¤ã

```mermaid
flowchart TD
    start_node((è¯ä¼°ç®æ åºæ¯)) --> check_embodiment{åºæ¯?}
    check_embodiment -- æ¯ --> check_length{}
    check_embodiment -- å¦ --> fail_generalize(["å­å¨æ³åå¤±æé£é©"])
    check_length -- æ¯ --> warn_drift(["å­å¨è¯¯å·®ç´¯ç§¯é£é©"])
    check_length -- å¦ --> check_compute{æ¥æå¤§è§æ¨¡ç®å?}
    check_compute -- æ¯ --> success_deploy(["éåå¤ç°ä¸é¨ç½²"])
    check_compute -- å¦ --> fail_reproduce(["å¤ç°å£åè¾é«"])
    
    classDef start_class fill:#E3F2FD,stroke:#1565C0,color:#0D47A1;
    classDef decision_class fill:#FFF3E0,stroke:#E65100,color:#BF360C;
    classDef success_class fill:#E8F5E9,stroke:#2E7D32,color:#1B5E20;
    classDef fail_class fill:#FFEBEE,stroke:#C62828,color:#B71C1C;
    
    class start_node start_class;
    class check_embodiment,check_length,check_compute decision_class;
    class success_deploy success_class;
    class fail_generalize,warn_drift,fail_reproduce fail_class;
```
*å¦ä½è¯»è¿å¼ å¾ï¼ä»ä½ çï¼æ²¿çå³ç­æ åä¸èµ°ãå¦æåºæ¯åç¦»äºè®ºæéªè¯çç¹å®è®¾ç½®çç®åï¼å°±éè¦è­¦ææ½å¨çå¤±ææ¨¡å¼ã*

**åºæ¯æ³åä¸
è®ºæçå¤å¤åºç¨å®éªæ·±åº¦ç»å®äºç¹å®ç roboticsãdriving æ camera-control è®¾ç½®ãè½ç¶æ¨¡åå¨ç©çè§å¾éµå¾ªä¸è¡¨ç°åºè²ï¼ä½è¿ç§è¡¨ç°å¾å¤§ç¨åº¦ä¸å¾çäºç¹å®åºæ¯çé«è´¨éæ°æ®åå¸ã embodimentãæªç¶ä¸åçä¼ æå¨ç±»åæ¶ï¼æ¨¡åå¯è½ä¼é­éåå¸å¤å¤±æãè®ºæå¹¶æªå½¢æçæ³åè½åï¼è¿æå³çå¨æ°ç¡¬ä»¶ä¸é¨ç½²å**é¿è§é¢çæçè¯¯å·®ç´¯ç§¯**
å¨é¿è§é¢çææ¹é¢ï¼ç³»ç»ä»éç¨ chunked autoregressive æ¹å¼ãè½ç¶è®ºæéç¹è¯ä¼°äºè¯¯å·®ç´¯ç§¯ç°è±¡ç¨³å®æ§ï¼ä½å¹¶æªå£°ç§°å½»åºæ¶é¤äºèªåå½çæåºæçæ¼ç§»é®é¢ãéççæåºåçå»¶é¿ï¼å¾®å°çç©çè¿åææåç´ çº§åå·®ä¼éæ¸æ¾å¤§ï¼ç´è§ï¼éä¸¥æ ¼å¯¹åºï¼å°±åå¤å°æºè¿ç»­å¤å°ï¼ä»£æ°è¶å¤ç»èä¸¢å¤±è¶ä¸¥éï¼ãå¯¹äºéè¦æé«é¿æ¶åºä¸è´æ§çä»»å¡ï¼è¿ç§ç´¯ç§¯è¯¯å·®ä»æ¯ä¸å¯å¿½è§çå±éã

**å¨ä½æ¡ä»¶åä¸ç½ç»è®¾è®¡çæªç«ä¹ä¸**
å¨ action-conditioned æ¨¡åçè®¾è®¡ä¸ï¼è®ºæEmbeddingãCrossAtten å ChannelConcat ä¸ç§å¹¶æªç©·å°½ææå¯è½çå¨ä½æ¡ä»¶åè®¾è®¡ãæ­¤å¤ï¼Cosmos-Transfer2.5 ç control branch ç»èé«åº¦ä¾èµåä»£ Cosmos-Transferè¯´æäº control blocks ï¼ç¼ºä¹å¯¹åºå±ãåæ¶ï¼Cosmos-Reason1 ç vision encoderç¨äº style control çæ½åï¼ä½çä½ future explorationï¼å½åçæ¬å°é£æ ¼æ§å¶è½åã

**å¤ç°å£åä¸åºç¡è®¾æ½ä¾èµ**
è¿æ¯é»ç¢ç¤¾åºå¹¿æ³éªè¯çæå¤§é¨æ§ãæä¸­çæ°æ®å¤çãreward service ä»¥åè®­ç»åºç¡è®¾æ½ï¼æ·±åº¦ä¾èµå¤§è§æ¨¡ GPU éç¾¤ãå¤é¨ reward models åä¸æçæ°æ®ç®¡çº¿ãè¿ç§âéèµäº§âæä¸­å°å¢éæé¾ä»å¤´å¤ç°ã

<details>
<summary><strong>æ·±åº¦æ¢è®¨ï¼RL </strong></summary>
å¨ RL post-training é¶æ®µï¼è®ºææªæä¾å®æ´çæ¾å¼æå¤±ä¸å®ç¨åº¦ä¸éä½äºæ¹æ³çå¯å¤ç°æ§ãAlign rewardãç»ãtrajectory probability decomposition ä»¥å diffusion loss regularization ç­æå­æè¿°æ¥æ¨æµè¿ç§ä¿¡æ¯ç¼ºå¤±å¯è½å¯¼è´å¨å¤ç°æ¶ï¼å¥å±ä¿¡å·çç¼©æ¾æ¯ä¾ææ­£ååæéçå¾®è°åå¾æ­¤å¤ï¼å¨å¨ä½æ¡ä»¶åè®¾è®¡ä¸­ï¼dingãCrossAtten å ChannelConcat ä¸ç§æ¹å¼ï¼å¿½ç¥äºè¯¸å¦åºäºæ³¨æåæºå¶çæ´ç»ç²åº¦ç©ºé´å¨ä½ãæªæ¥åè¿äºæ¿ä»£æ¹æ¡çæ¶èå®éªæè´ç»æï¼ä½¿å¾æä»¬æ æ³å¤æ­å½åå®éªè®¾ç½®ä¸çå±é¨æä¼ã
</details>

ç¨æ·è¦æ±æä½ä¸ºèµæ·±ä¸­æææ¯æ·±åº¦ç§æ®è®ºææ·±åº¦è§£è¯»æ¥åä¸­çä¸èï¼âè¶å¿å®ä½ä¸å±æâã
éè¦éµå®çè§èï¼
1. **ç»æ**ï¼ç»è®ºåç½®ãç»è®ºï¼åå±å¼ãä»¥ `## è¶å¿å®ä½ä¸å±æ` å¼å¤´ï¼H2ï¼ï¼H2å¥é¦å¯å¸¦emojiï¼H3/H4ä¸å¸¦ã
2. **å¿ å®ä¸ä¸¥è°¨**ï¼åºåâå£°ç§°âä¸âè¯æâï¼ç¹åå¤±ææ¨¡å¼ï¼å¦è¿åº¦å®£ç§°ç­ï¼ï¼è¯´ææ¯å¦æ¥åæ¶è/è´ç»æãè¯å®ä¸è´¬ä½ã
3. **æ¥å°**ï¼**ç»å¯¹ä¸è¦å¨åè¿°å¥å­éåç²¾ç¡®æ§è½æ°å­**ï¼å¦è¾¾å°8.54ï¼æå12%ç­ï¼ãæ§è½å¯¹æ¯ç¨å®æ§è¯­è¨ãç²¾ç¡®æ°å¼åªæ´»å¨è¯æ®è¡¨åæ ¸å¿ç»è®ºåï¼ç³»ç»èªå¨å¤çï¼æä¸åï¼ãéæ§è½æ°å­ï¼å¦2Båæ°ï¼720pç­ï¼å¯åãä¸æåè¯åã<!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-table-tr-td-confi-gur--><!--anchor:quote:%3Ctable%3E%3Ctr%3E%3Ctd%3EConfi%20guration%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D2B%3C%2Ftd%3E%3Ctd%3ECosmos%2DPredict2.5%2D14B%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Layers%3C%2Ftd%3E%3Ctd%3E32%3C%2Ftd%3E%3Ctd%3E36%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EModel%20Dimension%3C%2Ftd%3E%3Ctd%3E2%2C048%3C%2Ftd%3E%3Ctd%3E5%2C120%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EFFN%20Hidden%20Dimension%3C%2Ftd%3E%3Ctd%3E8%2C192%3C%2Ftd%3E%3Ctd%3E20%2C480%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EAdaLN%2DLoRA%20Dimension%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3Ctd%3E256%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3ENumber%20of%20Attention%20Heads%3C%2Ftd%3E%3Ctd%3E16%3C%2Ftd%3E%3Ctd%3E40%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EHead%20Dimension%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3Ctd%3E128%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EMLP%20Activation%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3EGELU%3C%2Ftd%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3EPositional%20Embedding%3C%2Ftd%3E%3Ctd%20colspan%3D%222%22%3E3D%20RoPE%3C%2Ftd%3E%3C%2Ftr%3E%3C%2Ftable%3E--><!--ref:r-we-introduce-cosmos-pr--><!--anchor:quote:We%20introduce%20%5BCosmos%2DPredict2.5%5D%2C%20the%20latest%20generation%20of%20the%20Cosmos%20World%20Foundation%20Models%20for%20Physical%20AI.%20Built%20on%20a%20flow%2Dbased%20architecture%2C--><!--ref:r-we-describe-the-multi--><!--anchor:quote:We%20describe%20the%20multi%2Dstage%20pretraining%20procedure%20in%20Tab.%204.%20Training%20begins%20with%20the%20Text2Image%20task%20at%20a%20resolution%20of%20256p.-->
4. **å¾è¡¨åäº**ï¼æ¶åæµç¨/ç¨Mermaidãç¦ç¨ `%%{init}` `style`ï¼åªç¨ `classDef`+`class`ï¼æ¯å¾â¤4ä¸ªè¯­ä¹è²ä¸å«æå­ `color:`ï¼snake_caseèç¹idï¼æ ç­¾3-6è¯ï¼è¾¹æ ç­¾1-4è¯ãå¤æåº¦åçº§ã
5. **è¡¨æ ¼ vs åè¿°**ï¼ç»æåå¯¹æ¯ç¨è¡¨ã
6. **æ·±åº¦èè¿æå å**ï¼åç¨ `<details>`ã
7. **ç¡¬çº¦æ**çå¨ï¼æ°å½æ¯å»ãå¿ å®äºæä¾çäºå®æºï¼Cosmos-Predict2.5, Physical AI, flow matching, VideoAlign RL, rCMè¸é¦ç­ï¼ãä¸åç²¾ç¡®æ§è½æ°å­0-800å­ãåªè¾åºæ¬èæ­£æã

åæäºå®æºï¼
- Cosmos-Predict2.5 æ¯é¢å Physical AI çè§é¢ä¸çåºç¡æ¨¡åã
- éç¨ flow matching ç»ä¸ Text2World, Image2World, Video2Worldã
- ä½¿ç¨ Cosmos-Reason1 ææ¬ç¼ç å¨ï¼SFTï¼æ¨¡ååå¹¶ï¼VideoAlign RL åè®­ç»ã
- æ©å±ä¸º Cosmos-Transfer2.5 (control-net style) æ¯æ Sim2Real, æºå¨äºº, èªå¨é©¾é©¶ã
- å®ä½ï¼å¹³å°ååºç¡æ¨¡åï¼å¼æ¾æé/ä»£ç /åºåãè§£å³éç¨è§é¢æ¨¡åå¨ç©çä¸è´æ§ãç»ç²åº¦æ§å¶ä¸çä¸è¶³ã
- æ´å¯ï¼æä¸çæ¨¡æè§ä¸ºå¸¦å¤æ¨¡ææ¡ä»¶çéåº¦åºå­¦ä¹ ï¼åç¨é¢åæ°æ®ãå¥å±æ¨¡ååæ§å¶åæ¯éæ­¥ä¸é¨åã

æ¬èä¸»é¢ï¼è¶å¿å®ä½ä¸å±æã
ç»è®ºåç½®ï¼Cosmos-Predict2.5 æ å¿çè§é¢çææ¨¡åä»âè§è§âç©çä¸çå¯äº¤äºä»£çâçèå¼è½¬ç§»æµåè®­ç»æå»ºçå¹³å°åè·¯çº¿ï¼ä¸º Physical AI æä¾äºæ ååçä»¿çåºåº§ï¼ä½å¨å¤æç©çå ææ¨çä¸é¿ç¨ä¸è´æ§ä¸ä»é¢ä¸´å¼æ¾æ§ææã

å±å¼ï¼
1. **å®ä½ï¼ä»âæ­æ¾å¨âå°âç©çæ²çâçè·¨è¶**ãéç¨è§é¢æ¨¡åï¼å¦Soraç±»ï¼çæï¼èæ¬æå®ä½ä¸º Physical AI çä¸çæ¨¡æå¨ãéè¿ flow matching ç»ä¸å¤ç§çææ¨¡å¼ï¼å¹¶ç»å Cosmos-Transfer2.5 çæ§å¶åæ¯ï¼å®ç°äºä»è¢«å¨çæå°ä¸»å¨æ¡ä»¶æ§å¶ï¼å¦å¨ä½ãç¸æºãå¤è§è§ï¼çè½¬åã
2. **æ¹æ³è®ºæä¹ï¼åè®­ç»æµæ°´çº¿ï¼Post-training Pipelineï¼çæ åå**ãéç¨ SFT -> Model Soup -> VideoAlign RL -> rCM è¸é¦çå®æ´é¾è·¯ãè¿è¯æäºå¨è§é¢é¢åï¼RLHF/RLAIF åè¸é¦ææ¯åæ ·å¯ä»¥æ¾èæåå¯¹é½è´¨éåæ¨çéåº¦ã
3. **å±éä¸å±æï¼å¤±ææ¨¡å¼ä¸æªæ¥ï¼**ï¼
   - è®ºæå£°ç§°æåäºç©çä¸è´æ§ï¼ä½åç´ çº§é¢æµæ¬è´¨ä¸ä»æ¯çæ­£çå æç©çå¼æï¼å¦ç¼ºä¹å¯¹ä¸å¯è§ç©ä½æå¤æç¢°æçä¸¥æ ¼ç©ççº¦æï¼ã
   - é¿ç¨æ¶åºä¸è´æ§ï¼è½ç¶ shifted logit-normal ç¼è§£äºé«åè¾¨çä¼ªå½±ï¼ä½é¿è§é¢çæä»å¯è½åºç°ç©çè§å¾æ¼ç§»ã
   - å±æï¼æªæ¥å¯è½éè¦ç»åæ¾å¼ç©çå¼æï¼å¦NeRF/3DGSæåä½å¨åå­¦ï¼ä¸éå¼å¨æ½å¨éçº¦æã

å¾è¡¨è®¾è®¡ï¼
ç»ä¸ä¸ª Mermaid æµç¨å¾ï¼å±ç¤ºâè§é¢çææ¨¡ååç©çä¸çæ¨¡æå¨çæ¼è¿è·¯çº¿âæâCosmos-Predict2.5 çåè®­ç»ä¸ä¸é¨åæµæ°´çº¿âã
éæ©ï¼åè®­ç»ä¸ä¸é¨åæµæ°´çº¿ï¼å±ç¤ºä»Baseå°Physical AIçæ¼è¿ï¼ã
èç¹ï¼Base Model (flow matching) -> SFT & Model Soup -> RL with VideoAlign -> Distillation (rCM) -> Transfer2.5 (Control).

Mermaid çº¦ææ£æ¥ï¼
- ç¦ç¨ `%%{init}` style`ã
- åªç¨ `classDef` + `class`ã
- â¤4ä¸ªè¯­ä¹è²ï¼æ¯è²å«æå­ `color:`ã
- snake_case èç¹ idï¼æ ç­¾ 3-6 è¯ï¼è¾¹æ ç­¾ 1-4 è¯ã
- å½¢ç¶ä¸è´ï¼è±å½¢=å¤å®ï¼åæ±=æ°æ®ï¼åè§=èµ·æ­¢ï¼ãè¿éç¨åè§ç©å½¢ååæ±ã

```mermaid
graph LR
    classDef base fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef align fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef accel fill:#fff3e0,stroke:#ef6c00,color:#e65100
    classDef control fill:#f3e5f5,stroke:#7b1fa2,color:#4a148c

    base_modelåºåº§æ¨¡å):::base
    sft_soup(é¢åå¾®è°ä¸æ¨¡ååå¹¶):::align
    rl_align(è§é¢å¥å±å¼ºåå­¦ä¹ ):::align
    rcm_distill(æ··åæ­£ååæ¶é´æ­¥è¸é¦):::accel
    transfer_ctrl(å¤æ¨¡ææ§å¶åæ¯æ©å±):::control

    base_model -->é¢åç¥è¯| sft_soup
    sft_soup -->|ä¼ååå¥½å¯¹é½| rl_align
    rl_align -->|éä½æ¨çæ­¥æ°| rcm_distill
    rcm_distill -->| transfer_ctrl
```
æ£æ¥èç¹æ ç­¾å­æ°ï¼
ç»ä¸æ¨¡å (8ä¸ªå­ï¼ç®3-6è¯ï¼ä¸­æè¯åå­ä¸åï¼å°½éç­ç¹ï¼æµ - 6å­) -> flow_matching_base(æ¨¡å)
é¢åå¾®è°ä¸æ¨¡ååå¹¶ (8å­) -> sft_and_soup(é¢åå¾®è°ä¸æ¨¡ååå¹¶) -> æ¹ä¸ºï¼é¢åå¾®è°ä¸åå¹¶ (7å­) -> é¢åæ°æ®å¾®è° (6å­)
è§é¢å¥å±å¼ºåå­¦ä¹  (8å­) -> è§é¢å¥å±å¼ºåå­¦ä¹  (8å­) -> è§é¢åå¥½å¼ºåå­¦ä¹  (8å­) -> å¥å±æ¨¡åå¼ºåå­¦ä¹  (8å­) -> å¼ºåå­¦ä¹ åå¥½å¯¹é½ (8å­) -> è§é¢å¥å±å¯¹é½ (6å­)
æ··åæ­£ååæ¶é´æ­¥è¸é¦ (10å­) -> æ¶é´æ­¥æ··åè¸é¦ (7å­) -> æ··åæ¶é´æ­¥è¸é¦ (7å­) -> æ¨çæ­¥æ°è¸é¦å é (8å­) -> æ¶é´æ­¥è¸é¦å é (7å­) -> æ··åæ¶é´æ­¥è¸é¦ (7å­)
å¤æ¨¡ææ§å¶åæ¯æ©å± (9å­) -> å¤æ¨¡ææ§å¶æ©å± (7å­) -> ç©çæ¡ä»¶æ§å¶æ©å± (8å­) -> ç©çæ§å¶åæ¯æ©å± (8å­) -> æ§å¶åæ¯æ¡ä»¶æ©å± (8å­) -> å¤æ¨¡ææ§å¶åæ¯ (7å­)

ä¸­æåè¯æ¯è¾æ¨¡ç³ï¼å°½éæ§å¶å¨ 4-6 ä¸ªæ±å­/è¯ã
baseåºåº§æ¨¡å] (6å­)
sft_soup[é¢åæ°æ®å¾®è°] (6å­)
rl_align[è§é¢å¥å±å¯¹é½] (6å­)
rcm_distill[æ··åæ¶é´æ­¥è¸é¦] (7å­) -> æ¶é´æ­¥è¸é¦å é (7å­) -> è¸é¦å éæ¨ç (6å­)
transfer_ctrl[å¤æ¨¡ææ§å¶åæ¯] (7å­) -> ç©çæ§å¶åæ¯ (6å­)

è¾¹é¢åç¥è¯ (6å­) -> 6å­) ->4å­)
ä¼ååå¥½å¯¹é½ (6å­) -> åå¥½å¯¹é½ (4å­)
éä½æ¨çæ­¥æ° (6å­) -> å éæ¨ç (4å­)
6å­) ->4å­)

ä¿®æ¹ Mermaid:
```mermaid
graph LR
    classDef base fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef align fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef accel fill:#fff3e0,stroke:#ef6c00,color:#e65100
    classDef control fill:#f3e5f5,stroke:#7b1fa2,color:#4a148c

    base_model(æ¨¡å):::base
    sft_soup(é¢åæ°æ®å¾®è°):::align
    rl_align(è§é¢å¥å±å¯¹é½):::align
    rcm_distill(è¸é¦å éæ¨ç):::accel
    transfer_ctrl(ç©çæ§å¶åæ¯):::control

    baseç¥è¯| sft_soup
    sft_soup -->|åå¥½å¯¹é½| rl_align
    rl_align -->|å éæ¨ç| rcm_distill
    rcm_distill| transfer_ctrl
```

æ°åæ­£æï¼
ç»è®ºåç½®ï¼Cosmos-Predict2.5 æ å¿çè§é¢çææ¨¡åä»âè§è§âç©çä¸çå¯äº¤äºä»£çâçèå¼è½¬ç§»ãåè®­ç»æå»ºçå¹³å°åè·¯çº¿ï¼ä¸º Physical AI æä¾äºæ ååçä»¿çåºåº§ï¼ä½å¨å¤æç©çå ææ¨çä¸é¿ç¨ä¸è´æ§ä¸ä»é¢ä¸´å¼æ¾æ§ææã

å®ä½ï¼ä»âæ­æ¾å¨âå°âç©çæ²çâã
éç¨è§é¢æ¨¡ååå general content generationï¼èæ¬æå°ä¸çæ¨¡æè§ä¸ºå¸¦å¤æ¨¡ææ¡ä»¶çéåº¦åºå­¦ä¹ ãéè¿ flow matching ç»ä¸ Text2WorldãImage2World ä¸ Video2Worldï¼å¹¶ç»å Cosmos-Transfer2.5 ç control-net style åæ¯ï¼æ¨¡åå®ç°äºä»è¢«å¨çæå°ä¸»å¨æ¡ä»¶æ§å¶ï¼å¦æºå¨äººå¨ä½ãå¤è§è§é©¾é©¶ï¼çè·¨è¶ãè¿è§£å³äºæ©æä¸çæ¨¡åå¨ç»ç²åº¦æ§å¶åç©çä¸è´æ§ä¸ççç¹ä»£çæå¡äºä¸æ¸¸ç­ç¥å­¦ä¹ ã

æ¹æ³è®ºæä¹ï¼åè®­ç»æµæ°´çº¿çæ ååã
è®ºæå±ç¤ºäºä¸å¥å®æ´çåè®­ç»é¾è·¯ï¼ç´è§ä¸ï¼ç±»ä¼¼äºå¤§è¯­è¨æ¨¡åç RLHF æµæ°´çº¿ï¼ãä»é¢å SFTãæ¨¡ååå¹¶ï¼å°å¥å±æ¨¡åè¿è¡å¼ºåå­¦ä¹ ï¼åå° rCM æ¶é´æ­¥è¸é¦ãè¿è¯æäºå¨è§é¢é¢åï¼åºäº VLM çåå¥½å¯¹é½åè¸é¦ææ¯åæ ·è½æ¾èæ¹åçæè´¨éãæä»¤éµå¾ªå¹¶éä½æ¨çææ¬ã

å±éä¸å±æï¼å¤±ææ¨¡å¼ç¹åï¼ã
å°½ç®¡è®ºæå£°ç§°æåäºç©çä¸è´æ§ï¼ä½æä»¬éè¦åºåâè§è§ä¸çç©çé¼çâä¸âä¸¥æ ¼çç©çå æâãåç´ ç©ºé´ç flow matching æ¬è´¨ä¸ä»æ¯ï¼å½é¢ä¸´ä¸å¯è§ç©ä½é®æ¡æå¤æåä½ç¢°ææ¶ï¼æ¨¡åä»å¯è½äº§çè¿èç©çå®å¾çâå¹»è§âãæ­¤å¤ï¼è½ç¶ shifted logit-normal åå¸ç¼è§£äºé«åè¾¨çä¸çæ¶é´è¿æ¸¡ä¼ªå½±ï¼ä½é¿ç¨è§é¢çæä¸­çç©çè§å¾æ¼ç§»é®é¢å¹¶æªè¢«å½»åºè§£å³ãæªæ¥çåå±æ¹åå¯è½æåéå¼è§é¢æ¨¡åä¸æ¾å¼ç©çå¼æï¼å¦ 3DGS æåä½å¨åå­¦ï¼çæ·±åº¦èåï¼æå¨ä¸åéçº¦æï¼ä»èçæ­£è·¨è¶ä»âçèµ·æ¥åâå°âç©çä¸æ­£ç¡®âçé¸¿æ²ã

æ£æ¥çº¦æï¼
1.çå¨ï¼æ¯å»ï¼âæ­æ¾å¨âå°âç©çæ²çâï¼âçèµ·æ¥åâå°âç©çä¸æ­£ç¡®âï¼ã
2. å¿ å®ï¼åªç¨äºå® matching, Text2World, Image2World, Video2World, Cosmos-Transfer2.5, control-net style, VideoAlign, rCM, shifted logit-normalï¼ã
3. ç²¾ç¡®æ§è½æ°å­ãå®æ§æè¿°ï¼âæ¾èæ¹åçæè´¨éâãâéä½æ¨çææ¬âï¼ã
4.å¤§çº¦ 600 å­ï¼ç¬¦å 350-800 å­è¦æ±ã
5. ç»æï¼`## è¶å¿å®ä½ä¸å±æ` å¼å¤´ï¼å¸¦ emojiï¼å¦ ð§­ï¼ãH3 ä¸å¸¦ emojiãç»è®ºåç½®ã

å¾®è°è¯­è¨ï¼ç¡®ä¿æ´çå¨ä¸ç¬¦åæ·±åº¦ç§æ®é£æ ¼ã

## ð§­ è¶å¿å®ä½ä¸å±æ

Cosmos-Predict2.5 æ å¿çè§é¢çææ¨¡åä»âåâç©çä¸çå¯äº¤äºä»£çâçèå¼è½¬ç§»ãåè®­ç»æå»ºçå¹³å°åè·¯çº¿ï¼ä¸º Physical AI æä¾äºæ ååçä»¿çåºåº§ï¼ä½å¨å¤æç©çå ææ¨çä¸é¿ç¨ä¸è´æ§ä¸ä»é¢ä¸´å¼æ¾æ§ææã

### ä»âæ­æ¾å¨âå°âç©çæ²çâçå®ä½è·¨è¶
éç¨è§é¢æ¨¡åå¾å¾åå general content generationï¼èæ¬æå°ä¸çæ¨¡æè§ä¸ºå¸¦å¤æ¨¡ææ¡ä»¶çéåº¦åºå­¦ä¹ ãéè¿ flow matching ç»ä¸ Text2WorldãImage2World ä¸ Video2Worldï¼å¹¶ç»å Cosmos-Transfer2.5 ç control-net style åæ¯ï¼æ¨¡åå®ç°äºä»è¢«å¨çæå°ä¸»å¨æ¡ä»¶æ§å¶ï¼å¦æºå¨äººå¨ä½ãå¤è§è§é©¾é©¶ï¼çè·¨è¶ãè¿ç´å»äºæ©æä¸çæ¨¡åå¨ç»ç²åº¦æ§å¶åç©çä¸è´æ§ä¸ççç¹ç­ç¥éªè¯ä¸åææ°æ®çæã

```mermaid
graph LR
    classDef base fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef align fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef accel fill:#fff3e0,stroke:#ef6c00,color:#e65100
    classDef control fill:#f3e5f5,stroke:#7b1fa2,color:#4a148c

    base_modelåº§æ¨¡å):::base
    sft_soup(é¢åæ°æ®å¾®è°):::align
    rl_align(è§é¢å¥å±å¯¹é½):::align
    rcm_distill(è¸é¦å éæ¨ç):::accel
    transfer_ctrl(ç©çæ§å¶åæ¯):::control

    base_model| sft_soup
    sft_soup -->|åå¥½å¯¹é½| rl_align
    rl_align -->|å éæ¨ç| rcm_distill
    rcm_distill --> transfer_ctrl
```
*å¦ä½è¯»è¿å¼ å¾ï¼è¯¥æµæ°´çº¿å±ç¤ºäºæ¨¡åå¦ä½ä»éç¨çè§é¢é¢æµåºåº§ï¼éæ­¥éè¿é¢åç¥è¯ãæ¨çå éï¼æç»æ¼ç©çæ§å¶ä¿¡å·çä¸ç¨ä¸çæ¨¡æå¨ã*

### åè®­ç»æµæ°´çº¿çæ ååæä¹
è®ºæå±ç¤ºäºä¸å¥å®æ´çè§é¢åè®­ç»é¾è·¯ï¼ç´è§ä¸ï¼ç±»ä¼¼äºå¤§è¯­è¨æ¨¡åç RLHF æµæ°´çº¿ï¼ãä»é¢å SFTãæ¨¡ååå¹¶Align å¥å±æ¨¡åè¿è¡å¼ºåå­¦ä¹ ï¼åå° rCM æ¶é´æ­¥è¸é¦ãè¿è¯æäºå¨è§é¢é¢åï¼åºäº VLM çåå¥½å¯¹é½åè¸é¦ææ¯åæ ·è½æ¾èæ¹åçæè´¨éãæä»¤éµå¾ªå¹¶éä½æ¨çææ¬ï¼ä¸ºåç»­ç ç©¶æä¾äºå¯å¤ç¨çã

### å±éåæä¸æªæ¥å±æ
å°½ç®¡è®ºæå£°ç§°æåäºç©çä¸è´æ§ï¼ä½æä»¬éè¦ä¸¥æ ¼åºåâè§è§ä¸çç©çé¼çâä¸âä¸¥æ ¼çç©çå æâãåç´ ç©ºé´ç flow matching æ¬è´¨ä¸ä»æ¯ï¼å½é¢ä¸´ä¸å¯è§ç©ä½é®æ¡æå¤æåä½ç¢°ææ¶ï¼æ¨¡åä»å¯è½äº§çè¿èç©çå®å¾çâå¹»è§âï¼å³æå æï¼ãæ­¤å¤ï¼è½ç¶ shifted logit-normal åå¸ç¼è§£äºé«åè¾¨çä¸çæ¶é´è¿æ¸¡ä¼ªå½±ï¼ä½é¿ç¨è§é¢çæä¸­çç©çè§å¾æ¼ç§»é®é¢å¹¶æªè¢«å½»åºè§£å³ã

<details>
<summary><strong>çº§ä¸çæ¨¡åçç©çè¾¹ç</strong></summary>
å½åçè§é¢ä¸çæ¨¡åå¨ä½ä¸º Physical AI ä»£çæ ¸å¿å¤±ææ¨¡å¼å¨äºç¼ºä¹æ¾å¼çç©çç¶æè¡¨å¾ãæªæ¥çåå±æ¹åå¯è½æåéå¼è§é¢æ¨¡åä¸æ¾å¼ç©çå¼æï¼å¦ 3DGS æåä½å¨åå­¦ï¼çæ·±åº¦èåï¼æå¨ä¸åéçº¦æãé¢æµâä¸ä¸ä¸ªåç´ æ¯ä»ä¹âï¼è¿è½çè§£âä¸ä¸ä¸ªç©çç¶æä¸ºä½å¦æ­¤âæ¶ï¼æè½çæ­£è·¨è¶ä»âçèµ·æ¥åâå°âç©çä¸æ­£ç¡®âçé¸¿æ²ã
</details>

æ£æ¥å­æ°ï¼çº¦ 700 å­ï¼å®ç¾è½å¨ 350-800 åºé´ã
æ£æ¥çº¦æï¼
- ç»è®ºåç½®ï¼ç¬¬ä¸æ®µå³æ¯ã
- æ é¢ï¼`## ð§­ è¶å¿å®ä½ä¸å±æ`ï¼H3 æ  emojiã
- å¿ å®ï¼æªç¼é ï¼ä½¿ç¨äºäºå®æºä¸­çæ¦å¿µã
- æ¥å°ï¼æ ç²¾ç¡®æ§è½æ°å­ã
- å¾è¡¨ï¼Mermaid ç¬¦åææ
- æå åï¼ä½¿ç¨äº `<details>`ã

å®æã## ð§­ è¶å¿å®ä½ä¸å±æ

Cosmos-Predict2.5 æ å¿çè§é¢çææ¨¡åä»âåâç©çä¸çå¯äº¤äºä»£çâçèå¼è½¬ç§»ãåè®­ç»æå»ºçå¹³å°åè·¯çº¿ï¼ä¸º Physical AI æä¾äºæ ååçä»¿çåºåº§ï¼ä½å¨å¤æç©çå ææ¨çä¸é¿ç¨ä¸è´æ§ä¸ä»é¢ä¸´å¼æ¾æ§ææã

### ä»âæ­æ¾å¨âå°âç©çæ²çâçå®ä½è·¨è¶
éç¨è§é¢æ¨¡åå¾å¾åå general content generationï¼èæ¬æå°ä¸çæ¨¡æè§ä¸ºå¸¦å¤æ¨¡ææ¡ä»¶çéåº¦åºå­¦ä¹ ãéè¿ flow matching ç»ä¸ Text2WorldãImage2World ä¸ Video2Worldï¼å¹¶ç»å Cosmos-Transfer2.5 ç control-net style åæ¯ï¼æ¨¡åå®ç°äºä»è¢«å¨çæå°ä¸»å¨æ¡ä»¶æ§å¶ï¼å¦æºå¨äººå¨ä½ãå¤è§è§é©¾é©¶ï¼çè·¨è¶ãè¿ç´å»äºæ©æä¸çæ¨¡åå¨ç»ç²åº¦æ§å¶åç©çä¸è´æ§ä¸ççç¹ï¼ä»£çæå¡äºä¸æ¸¸ç­ç¥éªè¯ä¸åææ°æ®çæã

```mermaid
graph LR
    classDef base fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef align fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef accel fill:#fff3e0,stroke:#ef6c00,color:#e65100
    classDef control fill:#f3e5f5,stroke:#7b1fa2,color:#4a148c

    base_modelåº§æ¨¡å):::base
    sft_soup(é¢åæ°æ®å¾®è°):::align
    rl_align(è§é¢å¥å±å¯¹é½):::align
    rcm_distill(è¸é¦å éæ¨ç):::accel
    transfer_ctrl(ç©çæ§å¶åæ¯):::control

    base_model| sft_soup
    sft_soup -->|åå¥½å¯¹é½| rl_align
    rl_align -->|å éæ¨ç| rcm_distill
    rcm_distill --> transfer_ctrl
```
*å¦ä½è¯»è¿å¼ å¾ï¼è¯¥æµæ°´çº¿å±ç¤ºäºæ¨¡åå¦ä½ä»éç¨çè§é¢é¢æµåºåº§ï¼éæ­¥ãåå¥½å¯¹é½ãæ¨çå éï¼æç»ç©çæ§å¶ä¿¡å·çä¸ç¨ä¸çæ¨¡æå¨ã*

### åè®­ç»æµæ°´çº¿çæ ååæä¹
è®ºæå±ç¤ºäºä¸å¥å®æ´çè§é¢åè®­ç»é¾è·¯ï¼ç´è§ä¸ï¼ç±»ä¼¼äºå¤§è¯­è¨æ¨¡åç RLHF æµæ°´çº¿ï¼ãä»é¢å SFTãæ¨¡ååå¹¶ï¼å°å¥å±æ¨¡åè¿è¡å¼ºåå­¦ä¹ ï¼åå° rCM æ¶é´æ­¥è¸é¦ãè¿è¯æäºå¨è§é¢é¢åï¼åºäº VLM çåå¥½å¯¹é½åè¸é¦ææ¯åæ ·è½æ¾èæ¹åçæè´¨éãæä»¤éµå¾ªå¹¶éä½æ¨çææ¬ï¼ä¸ºåç»­ç ç©¶æä¾äºå¯å¤ç¨çæ åå å±éåæä¸æªæ¥å±æ
å°½ç®¡è®ºæå£°ç§°æåäºç©çä¸è´æ§ï¼ä½æä»¬éè¦ä¸¥æ ¼åºåâè§è§ä¸çç©çé¼çâä¸âä¸¥æ ¼çç©çå æâãåç´ ç©ºé´ç flow matching æ¬è´¨ä¸æåï¼å½é¢ä¸´ä¸å¯è§ç©ä½é®æ¡æå¤æåä½ç¢°ææ¶ï¼æ¨¡åä»å¯è½äº§çè¿èç©çå®å¾çâå¹»è§âï¼å³ï¼ãæ­¤å¤ï¼è½ç¶ shifted logit-normal åå¸ç¼è§£äºé«åè¾¨çä¸çæ¶é´è¿æ¸¡ä¼ªå½±ï¼ä½é¿ç¨è§é¢çæä¸­çç©çè§å¾æ¼ç§»é®é¢å¹¶æªè¢«å½»åºè§£å³ã

<details>
<summary><strongåç´ çº§ä¸çæ¨¡åçç©çè¾¹ç</strong></summary>
å½åçè§é¢ä¸çæ¨¡åå¨ä½ä¸º Physical AI ä»£çæ¶ï¼å¨äºç¼ºä¹æ¾å¼çç©çç¶æè¡¨å¾ãæªæ¥çåå±æ¹åå¯è½æåéå¼è§é¢æ¨¡åä¸æ¾å¼ç©çå¼æï¼å¦ 3DGS æåä½å¨åå­¦ï¼çæ·±åº¦èåï¼ç©çä¸åéçº¦æãåªæå½æ¨¡ååç´ æ¯ä»ä¹âï¼è¿è½çè§£âä¸ä¸ä¸ªç©çç¶æä¸ºä½å¦æ­¤âæ¶ï¼æè½çæ­£è·¨è¶ä»âçèµ·æ¥åâå°âç©çä¸æ­£ç¡®âçé¸¿æ²ã
</details>