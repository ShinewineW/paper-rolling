# 10. 指定列表输入模式(二元 auto_discover),与自发查找并列

- Status: Accepted — 2026-06-11

## Context

输入候选此前只有一条路:按 topic **自发查找**(多源 OR 排序,ADR-0001)。
`force_include` 只是"在自发查找之上**额外必收**少量论文"的辅助,从不关闭发现。

出现一个**复发**需求(非一次性):操作者常有**自己的论文列表**,要"**只跑这些、
关闭自动抓取**"——例如复现某综述的参考集、跑固定 benchmark 论文集、手动投喂的阅读
清单。同时,产物按 topic 组织,要为**未来的知识图谱架构**做结构准备,topic 是结构键。

ADR-0002(rule-of-three)倾向:实例少 + 回填便宜 → **DEFER**。但此处实例**复发**、
且 topic 的 KG 结构角色成立(不是 n=1 抢救);若不做成一等模式,每次列表运行都要靠
`force_include` + `invalidate` 绕路,且模式语义(skip_set/分页/重锁)散落在 hub/gate/
config 多处,集中成一个显式开关比散落更稳。据此**越过 0002 的 DEFER 默认**。

## Decision

引入**二元输入模态**,由单一开关 `auto_discover` 切换;`force_include` 为两模式共用的
列表容器,语义随模式分叉:

- **自发查找(`auto_discover=true`,默认)**:多源发现 + `force_include` 必收(现状不变)。
- **指定列表(`auto_discover=false`)**:关闭发现,`force_include` 即**全部工作集**。

指定列表模式的配套语义(均经拷问确定):

- **尊重 skip_set**(幂等):列表里已 done/deferred 的跳过;强制重跑走既有 `invalidate`
  (划范围 与 幂等覆盖 正交)。
- **按 `n_per_tick` 分页**:n 为每跳成功上限;固定列表靠 skip_set 自然分页、自终止;
  列表模式下**不再**像发现模式那样把 n 抬高到覆盖全部 forced。
- **重锁规则**:翻转 `auto_discover` 重锁 Hard Gate;**固定列表分页不重锁**。**列表身份
  集合变更**亦应重锁(**仅列表模式**,经列表指纹检测,手改 campaign.yaml 也能抓到)——
  此项为本 ADR 之决定,但**实现延后**(见 impl spec「Task 6」);**当前已上线的重锁触发
  仅 topic / n_per_tick / auto_discover 三者变更**。
- **topic 两模式皆必需**(landscape 归组 + 未来 KG 结构键),保持精确校验(不放宽)。
- 不在 corpus 的列表论文**照常 ingest**(Tier-1→Tier-2);大论文 OOM 是 ingest 层的
  独立问题,**单篇 quarantine、不崩整批**,不在本 ADR 解决。

## Consequences

- 输入模式成为一等概念,**显式偏离 ADR-0002 的 DEFER**——依据是复发需求 + KG 结构
  角色,未来维护者见此应先读本 ADR 再"纠正"。
- `force_include` 语义按模式分叉(必收追加 / 全集);CONTEXT.md 已记 自发查找 / 指定列表 /
  topic 三个术语。
- **OOM 仍未解决**:留给 ingest 层(未来 Tier-2 pod-aware,或"先 pod 预摄取再列表重发"
  的前置);输入模式不负责治 OOM。
- 实现面**已落地**:`CampaignConfig`(+`auto_discover`)、`build_discover`(列表模式短路、
  跳过发现)、hub(列表模式分页、不抬 n)、`gate_needed`(翻转 `auto_discover` 重锁);并修
  `ingest`(列表条目按 **arxiv_id** 复用已提交语料,标题无需精确)。**延后**:列表身份
  指纹检测重锁(Task 6)。
