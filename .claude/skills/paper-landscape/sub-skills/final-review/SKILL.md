---
name: final-review
description: 终审修订层(ADR-0013)——可选、操作者触发的收尾验收。一轮 /loop 跑完后,主会话派每篇一个 Opus 子 agent,对已发布产物对照源 MD 做「修订或回炉」:小瑕疵直接外科修(REVISE),无可信基底的(读错论文/整体胡说/重写级)降级走 branch2 复活赛(FAIL)。默认关、不接进 /loop。
---

# 终审修订(final-review / ADR-0013)

把"机器门(双门 + 封印)过了"提升到"最强模型确认/修订过了"的**可选验收层**。它**不是门**——
可选、操作者触发、**不接进 /loop**、默认关。引擎只提供确定性纯函数(`output/final_review.py` 终审
标记、`demote.py` 降级、`revival.revive_all(only_keys=...)` 限定复活);非确定的修订判断全在主会话
派出的 Opus 子 agent 里(各自独立上下文)。账本 / 失败现场 / 复活赛只由主会话**串行**写(单写者
LS-1 不变量)。

## 终审修订(可选,操作者一轮跑完后触发;默认关)

前置:不接进 /loop;需要主会话有强模型(Opus + 高 effort)。没有就跳过。

1. 定批次:默认(**单行 `-c`**,勿换行——`from X import` 断行会 SyntaxError):
   `PYTHONPATH=.claude/skills/paper-landscape uv run python -c "from pathlib import Path; from scripts.output.final_review import unreviewed_compliant_keys; print(unreviewed_compliant_keys(Path('.')))"`
   (合规 + 未终审的 idbase 列表);也可由操作者显式给一个 idbase 子集。空 → 直接结束。

   FAIL 路径前置:demote → 复活赛重分析依赖 corpus 的 `images/`(gitignored)在场。
   `revival._revive_one` 先跑 `corpus_readiness_problems`,images 缺/不全时判 `manual`(需
   re-ingest)、不重分析。跨机 / 纯 checkout 上先确认 corpus 完整(`scripts.status` /
   `scripts.preflight`),不全就先 re-ingest 再跑 FAIL 收尾。

2. 跑 Workflow(pipeline over 批次,每篇一个 agent):
   - 每个 `agent(...)` 用下面的 prompt + schema;**pin model=opus + 足够 effort**;
     不同篇只碰各自文件 → 并行安全(无需 worktree)。
   - prompt 的 `{today}` 由主会话注入当天日期;若用 Workflow 脚本,经 `args` 传入(脚本不可用 Date.now)。
   - agent 自己改 + 自跑机械回归 + 写 final_review.json(CLEAN/REVISED)或返回 FAILED。
   - 主会话只收每篇的结构化 JSON,**不载入论文全文**。

3. 主会话串行收尾(单写者 LS-1)。**显式持一把锁、复用同一个 Ledger 实例**,整段包住 demote +
   revive_all(demote 的 `record` 与 `revive_all` 都不自锁、靠调用方持锁;两个 Ledger 实例会让第二
   次 `acquire()` 抛 LedgerLockError)。镜像 `revival.py` 的 `__main__` 装配:

       from pathlib import Path
       from scripts.ledger.store import Ledger
       from scripts.llm.seams import build_seams
       from scripts.output.repo_resolve import make_repo_resolver   # R10:复活也要码链解析
       from scripts.status import collect
       from scripts.demote import demote_to_scene
       from scripts.revival import revive_all

       ws = Path(".")
       led = Ledger(ws)
       seams = build_seams()
       resolver = make_repo_resolver(web_search=seams.get("web_search"))
       # failed = [(idbase, fail_category, fail_reason), ...] —— 取自各篇 verdict=="failed"
       with led.acquire():                      # LS-1:整段一把锁
           # 持锁后重核(MED-2):failed 源自锁外无锁快照(status.collect),窗口内 /loop /
           # revival 可能改了状态;剔除已不再合规/已不存在的篇。注意**不**按 ledger_diverged
           # 过滤(DOI-only 会被误判 diverged → 漏掉,与 _compliant_idbases 一致;且 rescinded-
           # compliant 篇的 FAIL→revive 本就让账本收敛,demote 它无害)。
           live = {r["idbase"] for r in collect(ws) if r["state"] == "compliant"}
           failed = [(ib, c, w) for ib, c, w in failed if ib in live]
           scenes = [
               demote_to_scene(ws, idbase, ledger=led, category=cat, reason=why)
               for idbase, cat, why in failed
           ]
           res = revive_all(                    # 只复活本批降级的现场(branch2 根)→ 重封印 → 重发布
               workspace=ws, ledger=led, seams=seams,
               repo_resolver=resolver, human_directive=None,
               only_keys={s.name for s in scenes},  # 关键:不碰 _failed/ 既有无关积压
           )

   - 复活后的新产物**不带** final_review.json → 下一轮终审会再覆盖它。
   - `res` 里 `status=="manual"` 的篇(corpus images 缺)= 没重分析成功、ledger 仍 deferred,
     需 re-ingest 后再来;**单独汇报,别计入"已重发布"**。
   - REVISED/CLEAN 的篇:agent 已写好 marker,无需主会话动账本。

4. 收尾报告:CLEAN / REVISED / FAILED(→ 复活 done / manual 各几篇)+ `status --card`。

## 逐篇 agent 输出 schema

每个子 agent 只返回这个 JSON(主会话只收 JSON,不载入论文全文):

```json
{
  "idbase": "string",
  "verdict": "clean | revised | failed",
  "edits": ["string, 每条=改了哪个文件/要点(verdict=revised 时非空)"],
  "fail_category": "读错论文 | 整体胡说 | 重写级 | null(仅 verdict=failed 时填)",
  "fail_reason": "string | null(一句话,仅 failed)"
}
```

## 逐篇 agent prompt 模板

每个 agent 用;注入变量:`{idbase}`、`{md_path}`、`{report_md}`、`{report_html}`、`{ara_dir}`、
`{today}` —— `{today}` 由主会话/编排注入当天日期(如 `2026-06-14`),引擎脚本与 Workflow 脚本都
**不可**用 `Date.now`/`new Date()`。

```
你是对单篇已发布论文产物做「终审修订」的资深审稿人,用最强能力 + 怀疑精神。读盘,不信任何分数。
目的是【改,不是判】:小瑕疵你直接外科修;只有无可信基底时才判失败。定位是【修订,不是重写】。

论文: {idbase}
文件(绝对路径,全部可读可改):
- 源 MD(基底/ground truth,只读基准): {md_path}
- 人链报告: {report_md}   (+ 改完用引擎 _html 重生 {report_html})
- AI 知识库 ARA 目录: {ara_dir}  真实布局(已核对):
    · PAPER.md（元数据 frontmatter）
    · logic/  → claims.md(论断)、concepts.md、experiments.md、problem.md、related_work.md、solution/
    · evidence/tables/  → 数字证据表(.md)
    · src/code_ref.md  → 码链三态指针
    · trace/、AUDIT_FLAGS.md、level2_report.json（封印报告，含 passes_seal2）
  （没有顶层 claims/ 目录——claims.md 在 logic/ 下;动手前先 `ls {ara_dir}` 核对）

步骤:
1. 读源 MD + 人链报告 + ARA,逐项对照。
2. 判 verdict:
   - REVISE(默认,存疑偏这个): 论文身份对、整体方法叙事对,只是局部有错(数字、码链 prose、
     表格错位、漏旗标/漏图、内部矛盾、思维链残留、个别 claim 偏差)——【全文件可改,含 ARA 封印内容】,
     直接下笔外科修。改完 report.md 必须用引擎 _html 重生 report.html(img_dir = report.md
     所在目录 = person_vault/<key>/,图片在其 images/ 下)。用 `uv run python`(裸 `python` 不在
     PATH);标题取首个 `# ` H1,取不到则退回目录名(别让 .group 在无 H1 时崩)。**必须单行
     `-c`**(多行缩进体会触发 IndentationError):
       PYTHONPATH=.claude/skills/paper-landscape uv run python -c "import re; from pathlib import Path; from scripts.output.branch1_llm import _html; d=Path('{report_md}').parent; md=(d/'report.md').read_text('utf-8'); m=re.search(r'^#\\s+(.+)$', md, re.M); t=(m.group(1).strip() if m else d.name); (d/'report.html').write_text(_html(t, md, d), encoding='utf-8')"
   - FAIL(只三类,确信才判): ① 读错论文(讲的是另一篇) ② 整体胡说(核心方法/claims 是编的、不在源文)
     ③ 重写级(现有产物是瓦砾不是基底,修=重写整段叙事)。FAIL 时【不改任何文件】,只返回判决。
   判据 = 「基底 vs 瓦砾」:能在站得住的基底上打补丁→REVISE;没有基底→FAIL。
3. 若 REVISE: 改完跑【纯机械回归】(决策 #5,不是 LLM 验收)——**两道都要过**:
   (a) ARA bundle 结构:
       `PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.output.check_ara_bundle {ara_dir}`
   (b) status 合规(权威判定——覆盖 报告合规 + ARA 封印 `passes_seal2` + 非 corrupt;`check_ara_bundle`
       不查这些。单行 `-c`,assert 失败即回归失败):
       PYTHONPATH=.claude/skills/paper-landscape uv run python -c "from pathlib import Path; from scripts.status import collect; r=[x for x in collect(Path('.')) if x['idbase']=='{idbase}']; assert r and r[0]['state']=='compliant', 'NOT compliant: '+str(r)"
   编辑时务必保住这些不变量(否则 (b) 会挂):report.md 仍以 `# <标题> — 深度解读` 这一行 H1
   开篇(别删/移 H1,否则 report.html 重生取不到标题),导读 blockquote 之后保留 `## 评价` 段;无
   `<!--ref:-->`/`<!--anchor:-->`;无 ARA-未读入标记(「未能读取已验证知识包(ARA)」「(未解析到
   结论)」、回退标题 `# ai_package`);`level2_report.json` 仍是合法 JSON 且 `passes_seal2` 不变
   (改了封印内容不重跑 G3,靠 final_review.json 盖来源章——决策 #2)。
   - 两道都过 → 写终审标记(date 用注入的 {today};edits 列你改了哪些文件/要点;**单行 `-c`**):
       PYTHONPATH=.claude/skills/paper-landscape uv run python -c "from pathlib import Path; from scripts.output.final_review import write_marker; write_marker(Path('{ara_dir}'), verdict='revised', edits=['report.md: …'], date='{today}')"
     返回 {idbase:"{idbase}", verdict:"revised", edits:[...]}。
   - 任一道挂了 → 改崩了(结构破损,非内容)→ 重试修一次;再挂 → 返回 {idbase:"{idbase}",
     verdict:"failed", fail_category:"重写级", fail_reason:"机械回归无法通过"}(不写 marker)。
4. 若 CLEAN(无需改): 同款**单行** incantation 写标记,但 verdict='clean'、edits=[]:
       PYTHONPATH=.claude/skills/paper-landscape uv run python -c "from pathlib import Path; from scripts.output.final_review import write_marker; write_marker(Path('{ara_dir}'), verdict='clean', edits=[], date='{today}')"
   返回 {idbase:"{idbase}", verdict:"clean"}。
5. 若 FAIL: 不改任何文件、不写 marker,返回 {idbase:"{idbase}", verdict:"failed", fail_category, fail_reason}。

每个返回 JSON 都必须带 `idbase:"{idbase}"`(即上面注入的论文 id)+ 对应 verdict 的字段,
与 schema 一致。只返回该 JSON。你的编辑发生在你自己的上下文里;主会话只收这个 JSON。
```

> provenance(ADR-0013 #2):改了封印内容**不重跑 G3**;`final_review.json`(verdict=revised)即来源章,
> `passes_seal2` 布尔保持原值。这条已写进 prompt 的 "REVISE" 说明里。

## 串行收尾固化(可选)

可在 `attn_sink/` 放一个一次性 driver(scratch),或直接由主会话按上面步骤手动编排。**不**新增引擎
CLI(保持引擎纯函数 + 主会话编排的分工)。
