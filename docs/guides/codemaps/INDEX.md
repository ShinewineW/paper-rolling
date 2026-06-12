# paper-landscape 代码地图

> **范围**: `paper-rolling` 工程 — engine + skill + 集成工作流
> **最后更新**: 2026-06-08

本索引汇总按领域分区的架构地图。每份地图聚焦一个关键子系统，记录其模块拓扑、数据流、关键决策和外部依赖。

---

## 📋 地图清单

| 地图 | 覆盖范围 | 关键变更（2026-06-07） |
|-----|--------|----------------------|
| [`llm-pipeline.md`](llm-pipeline.md) | 新增可插拔 LLM 提供商层 + 人链 LLM 写入器 | `scripts/llm/`（6 个新模块）+ `branch1_llm.py` + 2 个配置文件 |
| [`engine-core.md`](engine-core.md) | 核心管道：发现 → 摄入 → 分支2 → G2 → 分支1 → G3 → 景观 | `scripts/spoke.py` / `scripts/output/produce.py` 中的 `write_report` 注入 |
| [`audit-gates.md`](audit-gates.md) | G2 数据保真 + G3 6 维严谨性密封 | EngineAbort 集成（总线中止；`scripts/paths.py`） |
| [`discovery-sources.md`](discovery-sources.md) | 多源排序：OpenAlex + S2 + arXiv + DBLP + HF Papers | `query_expand` 支持 LLM 路由 |
| [`output-branches.md`](output-branches.md) | 双链原子产出（分支2 ARA + 分支1 人类报告） | 分支1 现已支持 LLM 写入（富文本中文段落 + 图形策展） |

---

## 🔑 2026-06-07 ~ 06-08 重点变更

### 1. **新增 LLM 提供商层** （`scripts/llm/` 新增 6 个模块）

```
scripts/llm/
├── providers.py      # LLMProvider 协议 + ClaudeCodeProvider (claude -p, model 必填)
│                       + OpenAICompatibleProvider（API 令牌）
│                       + StrictProvider（无兜底,失败 → EngineAbort）
├── config.py         # LLMConfig 从 config/llm.yaml 加载
├── seams.py          # build_seams() — 7 个 provider 路由的 seam 实例（含 faithfulness_judge, ADR-0012）
├── analyzer.py       # 分块平行接地分析器（formula-fidelity 纪律）
├── writer.py         # 人链 LLM 写入器（vivid 中文段落 + curate_figures）
└── jsonparse.py      # 宽容 JSON 提取 + LaTeX 转义修复
```

**关键特性**：
- **Vendor-neutral**: `openai_compatible` 适配任何 OpenAI API 兼容端点（OpenCode、DeepSeek、OpenRouter 等）
- **Per-seam routing**: `config/llm.yaml`（必需）独立声明每个 seam 的提供商和模式（inline / grounded / agent_team）；每 seam 必须显式路由,无默认
- **无兜底,失败 loudly**: provider 失败 → `EngineAbort`（中止整个 tick）；不再静默回落 claude-code 主订阅,避免额度被悄悄消耗
- **Grounded mode**: analyzer 在 grounded 模式下让 claude -p 自己读文件，避免超大文本嵌入

### 2. **人链 LLM 写入器** （`scripts/output/branch1_llm.py` + `branch1_report.py` 重组）

```python
write_branch1_llm(stage_person, candidate, stage_ai, md_path, write_report, key=key)
```

**流程**：
1. LLM writer 生成富文本中文段落（来自 `write_report` seam）
2. **力学锚定** `## 核心结论` 块（每个数字三层锚定 = 源文本 → Tier1/2 → 证据表）
3. **忠实门 (ADR-0012)**：正文数字允许自然书写，但其值必须出现在 MD（(b) 机械落源），否则 `AnchorGateError`（促进前失败）
4. **忠实门 (c) 判官**：报告不得相对已验证 ARA 实质误导（与分支1 确定性路径共用同一门）
5. **图形策展**：强制架构图 + 几个结果图（base64 内联到自包含 HTML）
6. **NO emoji 铁律**：确定性剥离表情符号 + mermaid 标签引用
7. **MathJax** 数学 + **parse-safe mermaid 11** 引用

**相比之前的确定性 `write_branch1`**：
- 旧方法：数据 → 固定 markdown 模板
- 新方法：分析 ARA → LLM 生成活泼中文 → 接地 + 门控

### 3. **配置文件**（新增或重新定义）

#### `config/llm.yaml` — Per-seam 路由 + 执行模式

```yaml
providers:
  claude-code:                       # 默认 + 回退（必须存在）
    type: claude_code
    strong_model: claude-sonnet-4-6
    fast_model: claude-haiku-4-5-20251001

  opencode:                          # OpenCode / DeepSeek（示例 API 令牌提供商）
    type: openai_compatible
    base_url: https://opencode.ai/zen/go/v1
    api_key_env: OPENCODE_API_KEY
    strong_model: deepseek-v4-pro
    fast_model: deepseek-v4-flash

seams:
  analyzer: { provider: claude-code, mode: grounded }   # 最重 + 接地（读 MD）
  skeptic: opencode            # G2 cross-model
  rigor: opencode              # G3 6 维
  entailment: opencode         # G3 蕴含
  expand: opencode             # discovery 查询扩展
  writer: opencode             # human chain（便宜）
  faithfulness: opencode       # branch1 忠实门 (c) judge（ADR-0012；每个 seam 都必须路由）
```

#### `config/audit.yaml` — 审计旋钮（用户可调）

```yaml
skeptic_votes: 1              # 多少次 G2 投票（1 = 单次；3 = 三投多数）
max_gate_rounds: 1            # 门重新执行多少次后隔离
data_fidelity:
  mode: tolerant              # tolerant | strict（宽容模式标记未验证数字）
  max_unconfirmed: 5          # 最多允许多少个未验证数字
  max_unconfirmed_ratio: 0.2  # ...或最多 20% 的已检查数字
```

### 4. **管道改进**

| 模块 | 变更 | 原因 |
|-----|------|------|
| `scripts/paths.py` | 新增 `class EngineAbort` | 两层回退都失败 → LLM 无关核心中止（不导入 LLM 层） |
| `scripts/spoke.py` | `write_report: Callable \| None` 参数 | 分支1 可选 LLM 写入；默认 None = thin 确定性 |
| `scripts/output/produce.py` | `if write_report is not None: write_branch1_llm(...) else: write_branch1(...)` | 条件路由到 LLM 或确定性分支1 |
| `scripts/run_campaign.py` | `write_report=seams["write_report"]` + `faithfulness_judge=seams["faithfulness_judge"]` | 从 `build_seams()` 注入 write_report + faithfulness（7 seam 中的两个；ADR-0012） |
| `scripts/output/figures.py` | SELECTIVE 图形策展（强制 arch + 部分结果） | 替代全嵌入方式 |

---

## 📊 高层架构

```
                ┌─── config/llm.yaml ────┐
                │   provider routing      │
                │   per-seam exec modes   │
                └─────────────┬───────────┘
                              │
                    ┌─────────▼─────────┐
                    │  scripts/llm/     │
                    │  seams.py:        │
                    │  build_seams()    │ ← 7 个 provider 路由 seam
                    └─────────┬─────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
    ┌─────▼──────┐   ┌────────▼────────┐  ┌──────▼─────────┐
    │ resolve_   │   │ skeptic_votes   │  │ write_report   │
    │ analysis   │   │ (G2, cross-MD)  │  │ (人链 LLM)     │
    │ (Analyzer) │   │                 │  │                │
    └─────┬──────┘   └────────┬────────┘  └──────┬─────────┘
          │                   │                   │
      ┌───▼─────────────┬─────┴─────────┬────────▼─────────┐
      │  分支2 ARA      │   G2 门       │  分支1 LLM 人链  │
      │  (数据确定)    │  (数据保真)   │  (生成 + 接地)  │
      └───┬─────────────┴─────┬─────────┴────────┬─────────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   person_vault/   │
                    │   ai_package/     │ ← 原子产出
                    │   (双链 1:1)      │
                    └───────────────────┘
```

---

## 🔗 相关文档

- **SKILL.md** — `/paper-landscape` 技能合约 + 硬门 + 每日 /loop 运行约定
- **ADR-0004** — LLM seam = 同步注入 callable；默认传输锁死 `claude -p`
- **`references/wiring-the-seams.md`** — 引擎组成合约（7 个 LLM seam，含 faithfulness）
- **`references/human-report-writing.md`** — 人链写入器的语言风格 + anchor 规范
- **`references/ara-schema.md`** — 分析束输出格式

---

## ✅ 关键不变式

1. **Single-writer ledger** — 只有 hub 写 `_ledger/processed_ledger.yaml`（LS-1 `.lock`）
2. **Ground-truth isolation** — G2 skeptic + G3 rigor 分别调用独立 seam，与生成器不相关
3. **Mandatory gates** — G2 + G3 每次都运行；无跳过选项
4. **NO silent degradation** — LLM 两层都失败 → `EngineAbort`（中止，不静默退化）
5. **Atomic dual-output** — 分支2 + 分支1 一起成功或一起失败（OT-5）

