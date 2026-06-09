# code_ref 官方仓定位级联 — 实施计划（P0）

> **日期**: 2026-06-09
> **状态**: 草稿
> **作者**: ShinewineW（含 Claude Opus 协作）
> **基准版本**: `paper-rolling@2e47446`
> **目的**: 把 code_ref 从"discovery 没带 `github_repo` 就一律标 closed-source"改造为"多源级联定位官方实现 + clone 验证闸门 + 三态语义",修复 12/13 论文被误标无仓的 P0 缺陷。
> 范围: `.claude/skills/paper-landscape/scripts/output/`（`code_ref.py` / `branch2_ara.py` / 新增 `repo_resolve.py`）+ `scripts/discovery/adapters`（复用 http）+ 新增 `data/` 离线表 + `scripts/tools/` 构建脚本

---

## 1. 背景与依据

当前 `code_ref.build_code_ref` 只接收 `branch2_ara.py:317` 传入的 `candidate.get("github_repo")`;而 discovery 四源里 OpenAlex/S2/arXiv 硬编码 `github_repo=None`,仅 HF Papers 源带仓,且其 token 曾过期 → 12/13 论文 `None` → `code_ref.py:59-60` 渲染成 **"No public repository — closed-source"**(把"没找到"误说成"已确认闭源")。

调研实测(`attn_sink/paper2code-research/findings.md`)结论:
- **无单一源可靠**:HF-live 会把官方链成重实现(Diffusion Forcing→`leffff`、Genie→`1xgpt`);websearch 会漏低星时效官方仓。
- **最强离线源 = PwC dump `is_official`**:18 万唯一 `arxiv_id→官方仓`,压成 ~5.7MB,确定性、零网络;修对了 HF-live/websearch 的错。短板是冻结 ~2025-09,新论文需 HF-live/websearch 补。

## 2. 锁定的架构

**级联(按权威性,命中即停;候选统一过验证闸门)**:

| 层 | 源 | 性质 | 依赖 |
|---|---|---|---|
| **T1** | grep 论文全文 MD 的 `github.com` 链接(作者自报) | 纯确定性 | `md_path` |
| **T2a** | PwC 离线 `is_official` 查找表 | 纯确定性、零网络 | 随包 `data/` 表 |
| **T2b** | HF live `api/papers/{arxiv_id}` → `githubRepo` | 网络 | 注入 `http` 适配器 |
| **T4** | websearch 兜底 | 网络/LLM | 注入 `web_search` seam(可选) |
| **闸门** | `clone --depth1` + `_locate` 验证候选 | I/O | 复用 `code_ref.py` |
| **输出** | 三态 code_ref.md | — | — |

**验证闸门接受规则**:
- T2a `is_official=true` → **高信任**,clone 成功即接受(clone 失败仍记录链接 + "unavailable" 注记,沿用现有 `clone_error` 分支)。
- T1 / T2b / T4 候选 → clone 后须满足其一:repo 内出现该 **arxiv_id 或论文标题**,或 `_locate` 命中 **≥1 个 innovation symbol**;否则丢弃,试下一候选。

**三态语义**(替换 `code_ref.py:59-60` 的 `None→closed-source`):
- `found` — 渲染 repo + SHA + innovation→file:line,并标 **来源**(paper-text / pwc-official / hf-live / websearch)+ 置信。
- `searched, not found` — 所有层跑过、无候选通过验证;如实写"已检索未找到",**不等于闭源**。
- `author-declared closed-source` — 仅当 **T1 在论文正文检出闭源声明**(如 "code will not be released")才下此结论。

> 反例红线:`github_repo is None` 永不再渲染成 "closed-source";未通过验证的候选永不写入。

## 3. 离线表:位置、格式、刷新

- **位置(tracked)**: `.claude/skills/paper-landscape/data/pwc_official_arxiv2repo.tsv.gz`(引擎+config 属 tracked 范畴)。
- **格式**: gzipped TSV,每行 `arxiv_id<TAB>repo_url`,仅 `is_official=true` 子集(~18 万行,gz ~3–4MB)。
- **运行时读取**: 纯 stdlib `gzip`,首次用时 **lazy 载入 dict**(180k 条内存可忽略),**无 duckdb/pyarrow 运行时依赖**。
- **构建脚本**: `scripts/tools/build_pwc_table.py`(PEP723 内联 `duckdb` 依赖或 `uv run --with duckdb`)——下载 `pwc-archive/links-between-paper-and-code` parquet → filter `is_official` → 导出 gz TSV。**仅离线构建用,非运行时**。
- **刷新策略**: PwC 已停服,dump 实质静态 → **无需自动刷新**;若 HF 快照更新,手动重跑构建脚本。新论文(冻结后)由 T2b/T4 覆盖,不依赖此表刷新。

## 4. 代码改动与集成点

### 4.1 新增 `scripts/output/repo_resolve.py`(纯核心 + 可选注入)
```
@dataclass(frozen=True)
class RepoCandidate: url:str; source:str; trust:str  # trust: "official"|"declared"|"search"

def resolve_repo_candidates(
    arxiv_id: str|None, md_path: Path|None, candidate: dict, *,
    pwc_lookup: Callable[[str], str|None],          # T2a,注入(默认读随包表)
    http=None,                                       # T2b,注入 http 适配器,缺省跳过
    web_search=None,                                 # T4,注入 seam,缺省跳过
) -> list[RepoCandidate]:  # 已按 T1→T2a→T2b→T4 排序、去重
```
- T1: 正则 grep `md_path` 文本里的 `github.com/{owner}/{repo}`(复用 `figures.py` 同款正则风格)。
- T2a: `pwc_lookup(arxiv_id)`。
- T2b: `http.get_json("https://huggingface.co/api/papers/{id}", headers=_hf_headers())["githubRepo"]`(复用 `hf_papers._hf_headers`)。
- T4: `web_search(query)` → 解析候选 github URL。

### 4.2 改 `code_ref.build_code_ref`(`code_ref.py:86`)
- 入参由 `github_repo: str|None` 改为 `candidates: list[RepoCandidate]`(+ `arxiv_id`/`title` 供验证闸门匹配)。
- 逻辑:按序 clone 每个候选 → 验证规则(§2)→ 首个通过即 `found` 渲染;全失败 → `searched-not-found`;`candidates` 为空且检出闭源声明 → `author-declared-closed`。
- `_render` 增三态分支 + 来源/置信行。

### 4.3 改 `branch2_ara.write_branch2`(`branch2_ara.py:316`)
- 调 `resolve_repo_candidates(...)` 取候选 → 传给 `build_code_ref`。
- `write_branch2` 增可选注入参数 `http=None, web_search=None`(沿用 P1-a 的可选参数兼容手法;14+ 调用方零改动)。
- `produce.produce_outputs` 在调用点把驱动注入的 `http`/`web_search` 透传下来。

### 4.4 seam 接线
- T2b 用既有基础设施适配器 `http`(`run_campaign` 已注入)。
- **T4 `web_search` 为新增可选 seam**:驱动(Claude Code agent)用 WebSearch 工具实现并注入;缺省不注入 → T4 自动跳过(图省事/离线场景仍可跑 T1+T2a+T2b)。

## 5. 分阶段实施(每步先 RED 再 GREEN)

### Phase 1 — 确定性地基(无新 seam,无网络)
- [ ] T1 grep MD 链接提取 + 单测(含 Tier-1 无图/无链接退化)
- [ ] `build_pwc_table.py` 构建脚本 + 产出 `data/pwc_official_arxiv2repo.tsv.gz`(tracked)
- [ ] T2a lazy dict 加载 + `pwc_lookup` + 单测
- [ ] 验证闸门规则(clone+match)落到 `build_code_ref` + 单测(重实现被拒、官方被接受)
- [ ] 三态渲染替换 `None→closed-source` + 单测(三态各一)
- [ ] `resolve_repo_candidates` 串 T1+T2a + `branch2`/`produce` 接线 + 集成测试
- [ ] 全量 `corpus/` 回扫脚本:对 26 篇打印解析结果(人工抽检准确率)

### Phase 2 — 时效补充(注入式)
- [ ] T2b HF-live(注入 http)+ 单测(mock http)
- [ ] T4 `web_search` 可选 seam + 单测(mock seam;缺省跳过)
- [ ] 端到端:对 PwC 冻结后论文(ORION/Dreamer4/2026 系列)验证 T2b/T4 兜底

## 6. 验收标准

- `uv run pytest` 全绿;`ruff check` 引擎源干净。
- 回扫 26 篇:之前误标 closed-source 的 ≥10 篇被正确解析为 `found`(官方仓),真闭源(GAIA-1/Genie/GameNGen)正确落 `author-declared-closed` 或 `searched-not-found`,**无一例误链重实现**。
- `code_ref.py` 不再存在 `github_repo is None → "closed-source"` 路径。

## 7. 风险与缓解

- **离线表体积**:3–4MB gz 入 git 一次性,可接受;若超预期改 sqlite(stdlib)。
- **验证闸门误杀**:官方仓 README 偶尔不含 arxiv_id/标题且 innovation symbol grep 不到 → 对 `is_official` 高信任候选放宽(clone 成功即收);对其他候选记录"未通过验证"而非静默丢弃(log)。
- **clone 成本**:仅对通过前序筛选的少量候选 clone,且 `--depth1`;沿用现有超时。
