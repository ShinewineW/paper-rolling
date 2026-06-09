# LLM Pipeline & Provider Layer 代码地图

> **范围**: `scripts/llm/` + `config/llm.yaml` + `config/audit.yaml`
> **最后更新**: 2026-06-09
> **关键特性**: Vendor-neutral 提供商路由、**无兜底**(provider 失败 → `EngineAbort` loudly,绝不静默回落主订阅)、Per-seam 独立调用、每 seam 必须显式路由

<!-- Generated: 2026-06-08 | Files scanned: 9 | Token estimate: ~3500 -->

## 架构概览

```
Execution Flow:

  run_campaign() [entry point]
       │
       ├─ load_campaign(config/campaign.yaml)
       │
       └─ build_seams()  ← 加载 config/llm.yaml + config/audit.yaml
            │
            ├─ resolve_analysis(md, candidate) → ARA bundle
            │   Provider: claude-code (grounded)
            │   Tool: Read MD chunked-parallel
            │
            ├─ skeptic_votes(numbers, md, claim) → SkepticVote[]
            │   Provider: routed (default opencode)
            │   Role: G2 cross-model 审计（不见证据、不见答案）
            │
            ├─ rigor_scores(ara) → 6-dim rubric score
            │   Provider: routed (default opencode)
            │   Role: G3 严谨性评分（rubric 私有）
            │
            ├─ entailment_judge(claim, experiment) → (bool, reason)
            │   Provider: routed (default opencode)
            │   Role: G3 蕴含检查
            │
            ├─ expand_llm(topic) → [query, ...]
            │   Provider: routed (default opencode)
            │   Role: discovery query 扩展（小、便宜）
            │
            └─ write_report(ara, figures_list) → rich HTML report
                Provider: routed (default opencode)
                Role: 人链 LLM（生成 vivid 中文 + 图形注释）

  Each seam = independent provider call
           ↓
  [ Provider routing via config/llm.yaml ]
           ↓
  Strong model (sonnet/deepseek) OR fast model (haiku/flash)
           ↓
  Transport: claude -p subprocess OR OpenAI HTTP API
           ↓
  [ JSON parsing + nudge retry ]
           ↓
  Result OR StrictProvider 捕获 ProviderError → EngineAbort（无兜底）
           ↓
  Success OR EngineAbort (tick 中止，loudly 报错，绝不退化到主订阅)
```

---

## 模块拓扑

### `scripts/llm/__init__.py` — Package marker

| 功能 | 文件 | 导出 |
|-----|------|------|
| 包标记 | `__init__.py` | 无 |

### `scripts/llm/providers.py` — Transport layer (LLM-agnostic)

**核心类**：

| 类 | 协议/基类 | 职责 |
|---|---------|------|
| `LLMProvider` | Protocol | 运输接口：`complete(prompt, *, tier, effort, tools) → str` |
| `ClaudeCodeProvider` | frozen dataclass | Headless `claude -p` subprocess；指数退避重试；支持 grounded `--allowedTools`；**model 必填,无默认** |
| `OpenAICompatibleProvider` | frozen dataclass | 任何 OpenAI chat-completions API；从 `.env` 读 token（不硬编码） |
| `StrictProvider` | frozen dataclass | 包裹路由到的 provider；`ProviderError` → `EngineAbort`（**无兜底**,绝不静默切换后端/主订阅） |
| `ProviderError` | RuntimeError | Provider 调用失败（经过重试预算用尽） |

**关键函数**：

```python
def _backoff_sleep(attempt: int) -> None
    # 指数退避：5s × 2^(attempt-1)，max 60s

class ClaudeCodeProvider:
    def complete(prompt, *, tier="strong", effort="high", timeout=900, tools=None) → str
        # 运行 `claude -p --effort {effort} --model {model}`
        # 如果 tools = ("Read", "Grep")，传 --allowedTools（grounded 模式）
        # 重试：max 4 次（timeout 或 non-zero exit 或 JSON 无效）
        # 返回 JSON envelope 中的 result 字符串

class OpenAICompatibleProvider:
    def complete(prompt, *, tier="strong", effort="high", timeout=900, tools=None) → str
        # 发送 POST 到 base_url/v1/chat/completions
        # 从 api_key_env 读 token
        # 支持可选的 reasoning_effort（pass-through 到支持的后端）
        # 重试：max 3 次（transient 错误）
        # 返回 choice[0].message.content

class StrictProvider:
    provider: LLMProvider                # 唯一字段:被路由到的 provider
    def complete(prompt, *, tier="strong", effort="high", timeout=900, tools=None) → str
        # 调用 self.provider.complete(...)
        # ProviderError（重试已用尽）→ raise EngineAbort（从 scripts.paths 导入）
        # 无 fallback —— 失败 loudly 上抛,绝不静默切到别的后端
```

**关键不变式**：
- 所有 Provider 实现都是 `@dataclass(frozen=True)` — immutable, stateless
- Timeout 默认 900 秒（15 分钟，大型论文分析）
- Token 从 env 读取（`.env` 中定义，gitignored）；never hardcoded
- Grounded mode 仅 claude-code 支持（API 后端没有文件访问）

### `scripts/llm/config.py` — Configuration management

**核心类**：

```python
class LLMConfig:
    providers: dict[str, LLMProvider]  # name → provider instance
    routing: dict[str, str]            # seam → provider name（每 seam 必有,load 时强校验）
    modes: dict[str, str]              # seam → inline | grounded | agent_team

    def resolve(seam: str) → StrictProvider
        # 查表 routing[seam]，返回 StrictProvider(provider)（无 fallback）

def load_llm_config(workspace_root: Path) → LLMConfig
    # 读 config/llm.yaml（必需；不存在 → ValueError 硬报错,无默认）
    # 解析 providers 块 + seams 块；每个 seam 必须显式路由,否则 ValueError
    # 实例化所有 provider（从 .env 读 token）
    # 返回 LLMConfig
```

**Config 格式** （`config/llm.yaml`）：

```yaml
providers:
  claude-code:                         # 仅被显式路由到此的 seam 使用（如 grounded analyzer）
    type: claude_code
    strong_model: claude-sonnet-4-6    # 必填,无默认
    fast_model: claude-haiku-4-5-20251001
  
  opencode:                            # 示例：任何 OpenAI 兼容端点
    type: openai_compatible
    base_url: https://opencode.ai/zen/go/v1
    api_key_env: OPENCODE_API_KEY
    strong_model: deepseek-v4-pro
    fast_model: deepseek-v4-flash
    send_reasoning_effort: false       # 可选，默认 false

seams:
  analyzer: { provider: claude-code, mode: grounded }
  skeptic: opencode
  rigor: opencode
  entailment: opencode
  expand: opencode
  writer: opencode
```

**特性**：
- `config/llm.yaml` 必需；缺文件 / 任一 seam 未路由 / provider 未定义 → `ValueError` 硬报错（无默认回落）
- `grounded` 模式仍要求 claude_code provider（本地 Read/Grep 能力校验,与额度无关）
- Per-seam override via `_SEAM_OVERRIDE` dict（测试用）
- Future: seam 值可能变成 provider 列表（多模型 A/B，暂未活跃）

### `scripts/llm/seams.py` — Seam factory & routing

**核心函数**：

```python
def build_seams() → dict[str, Callable]
    # 单次调用，返回所有 6 个 seam（已路由 + StrictProvider 包裹,无回退）
    # 返回 {
    #   "resolve_analysis": seam_fn,
    #   "skeptic_votes": seam_fn,
    #   "rigor_scores": seam_fn,
    #   "entailment_judge": seam_fn,
    #   "expand_llm": seam_fn,
    #   "write_report": seam_fn,
    # }

def _provider_for(seam: str) → StrictProvider
    # 从 config/llm.yaml 查表 → provider name
    # 返回 StrictProvider(provider)（无 fallback；失败 → EngineAbort）
    # 支持 _SEAM_OVERRIDE 测试覆盖

def _ask_json(prompt, *, seam, tier="strong", retries=2, ...) → dict | list
    # 通用 JSON 提取器，支持重试 + 递进式 nudge
    # 尝试 1: 原始 prompt
    # 尝试 2: prompt + nudge（"必须是 JSON，无散文"）
    # 失败 → raise ProviderError 或 JSONDecodeError
```

**每个 Seam 的 signature**：

| Seam | Input | Output | Mode | Cost |
|------|-------|--------|------|------|
| `resolve_analysis` | (md_path, candidate) | ARA dict | grounded | 高（全文） |
| `skeptic_votes` | (numbers, source_md, claim) | SkepticVote[] | inline | 低 × N_votes |
| `rigor_scores` | (ara_bundle) | 6-dim rubric dict | inline | 中 |
| `entailment_judge` | (claim, experiment) | (bool, reason) | inline | 低 |
| `expand_llm` | (topic) | [query, ...] | inline | 低 |
| `write_report` | (ara_bundle, figures) | rich HTML str | inline | 中 |

**Global state**:

```python
_LLM_CONFIG: LLMConfig | None = None  # Lazy-loaded once per process
_SEAM_OVERRIDE: dict[str, str] = {}   # Test override (seam name → provider name)
_MD_CHAR_CAP = 200_000                # Skeptic/rigor input cap (avoid OOM on huge papers)
```

---

### `scripts/llm/analyzer.py` — Chunked-parallel grounded analyzer

**核心函数**：

```python
def analyze_chunked(md_path: Path, candidate: dict, provider: LLMProvider) → dict
    # ARA bundle 的源头（被 resolve_analysis seam 调用）
    # 读 corpus/{ID}/{ID}.md（frozen source of truth）
    # 分块（~200k tokens/chunk，避免 OOM）
    # 并行发送 chunks 到 analyzer（不同 seam 独立调用）
    # 合并 chunks 的结果 → 完整 ARA

    REQUIRED_ARA_KEYS = [
        "overview", "problem", "claims", "concepts", "experiments",
        "related_work", "architecture", "algorithm", "heuristics",
        "configs_training", "configs_model", "environment",
        "execution_stub", "innovations", "exploration_tree",
        "evidence_tables", "headline_metric", "headline_value",
        "params_million", "lls", ...
    ]  # 丢失的 → 填默认值或 null

    # Formula-fidelity discipline (2026-06-08):
    # 分析器必须检查 LaTeX 等式块
    # 报告 eq_count_source（MD 中实际方程数）
    # vs eq_count_claimed（分析器声称找到的）
    # 不匹配 → ARA.AUDIT_FLAGS 标记
```

**关键特性**：
- **Grounded**: Analyzer 在 claude -p grounded 模式下运行，自己读 MD（不嵌入）
- **Chunked**: 大论文分割成多个 chunks，并行处理，然后合并
- **Formula fidelity**: 记录等式块数（不做验证，仅计数；G2 稍后检查）
- **缓冲语义**: 分析没有缓存；每次调用新鲜分析

---

### `scripts/llm/writer.py` — Human chain LLM writer

**核心函数**：

```python
def write_human_sections(ara: dict, provider: LLMProvider) → dict
    # LLM 从 ARA bundle 生成 VIVID 中文段落
    # 返回 {section_key: rich_markdown_str, ...}
    # 例如：
    #   "introduction": "系统提出了一种新的...",
    #   "methods": "我们的方法基于...",
    #   "results": "实验在三个数据集上...", ...

def curate_figures(ara: dict, figures: list[Figure]) → list[Figure]
    # 从 corpus/{ID}/images/ 提取所有图形
    # 按 anchor 标签按类别分类（architecture, results, ablation, ...）
    # 选中强制架构图 + 最多 N 个其他高信息量图
    # 返回 [(fig, science_pop_caption_zh), ...]

class Figure:
    ref: str              # 图像文件引用（e.g., "../images/fig_1.png"）
    caption: str          # 原始论文 caption（英文）
    category: str         # "architecture" | "results" | "ablation" | ...
    confidence: float     # 策展置信度 (0-1)

    # science_pop 描述（中文）由 LLM writer 为每个选中图形生成
```

**关键特性**：
- **Vivid prose**: LLM 生成活泼的中文，不是僵硬的数据翻译
- **Selective**: 架构图强制，仅额外 N~3 个高优先级结果图
- **science-pop**: 每个图添加中文解释（科普级，非 caption 直译）
- **Base64 inlining**: 图自包含在 HTML 报告中（不外链）

---

### `scripts/llm/jsonparse.py` — Tolerant JSON extraction

**核心函数**：

```python
def extract_json(text: str) → dict | list | str | float | int | bool | None
    # 从 LLM 输出中提取单个 JSON 值（宽容）
    # 处理场景：
    #   1. 纯 JSON（"{"foo":"bar"}" 或 "[1,2,3]"）→ 解析
    #   2. 代码块（"```json\n{...}\n```"）→ 提取 + 解析
    #   3. JSON 前有散文 → 找到最早的 JSON start，从那里解析
    #   4. LaTeX 转义问题（\"在 JSON 内）→ 修复

def _fix_latex_escapes(text: str) → str
    # LaTeX 里 \" 常见但不是有效 JSON
    # 转换为 \\" (escaped quote in json context)
    # 或删除不必要的转义
```

**关键特性**：
- **Tolerant**: LLM 可能生成 ```json fence，可能有前置散文，可能 LaTeX 逃逸错误
- **No re-ask**: extract_json 失败时，由调用方（seam）决定是否重试
- **Preserves structure**: 输入的什么 JSON type（dict/list/scalar），输出就是那个 type

---

## 数据流

### Per-seam routing（无 fallback）

```
call seam("analyzer", prompt)
  ↓
_ask_json(prompt, seam="analyzer")
  ↓
provider = _provider_for("analyzer")
           ↓
           StrictProvider(
             provider=claude-code (显式路由, grounded mode)
           )
  ↓
attempt 1: provider.complete(prompt, tier="strong", tools=("Read", "Grep"))
  ↓ (success)
parse JSON → ARA dict
  ↓ (failure)
attempt 2: provider.complete(prompt + nudge, ...)
  ↓
success → return; else → ProviderError（provider 内部重试已用尽）
  ↓
StrictProvider 捕获 → EngineAbort (loudly, abort tick；无兜底,绝不回落主订阅)
```

### Config flow

```
run_campaign()
  ↓
build_seams()
  ↓
load_llm_config(Path("."))
  ↓
read config/llm.yaml + config/audit.yaml
  ↓
instantiate providers (read .env for tokens)
  ↓
LLMConfig(providers={...}, routing={...}, modes={...})
  ↓
_ask_json for each seam → StrictProvider(provider)（无 fallback）
  ↓
return dict[str, Callable] of all 6 seams
  ↓
run_campaign(..., resolve_analysis=seams["resolve_analysis"], ...)
```

---

## 外部依赖

| 库 | 版本 | 用途 |
|---|------|------|
| `requests` | latest | OpenAI HTTP 调用 |
| `pydantic` | 2.x | config.py 中的数据类验证 |
| stdlib: `subprocess` | — | claude -p subprocess 执行 |
| stdlib: `json` | — | JSON parse + serialize |
| stdlib: `re` | — | LaTeX escape 修复 |

## 相关文档

- `SKILL.md` — Wiring contract（6 个 seam，how to inject）
- `references/wiring-the-seams.md` — Provider-agnostic seam composition
- `references/human-report-writing.md` — Writer seam 的语言风格
- ADR-0004 — LLM seam = callable injection；默认 claude -p

---

## 关键设计决策

1. **Vendor-neutral providers** — OpenAI 兼容 API 不硬编码任何厂商。Config 仅改 URL + 模型名 + token env，无代码改动。

2. **Per-seam independent calls** — 每个 seam 是独立 LLM 调用（不共享上下文）。G2 skeptic ≠ generator，G3 rigor ≠ generator → 无相关性。

3. **无兜底,失败 loudly** — 取消了原 claude-code 强制回退。任一 seam 的 provider 失败(重试用尽)→ `EngineAbort`（中止整个 tick,向上抛）。动机:静默回落到 Claude Code 主订阅会让额度急剧消耗且不可感知,故改为强制暴露给操作者修 key/config。主订阅仅在 seam 被显式路由到 claude-code 时使用。

4. **Grounded analyzer** — Analyzer 在 grounded 模式下让 claude -p 自己读文件，避免嵌入 200k+ 字符文本到 prompt。

5. **Tolerant JSON parsing** — LLM 可能生成带 fence / 散文 / 转义错误的 JSON。Parser 宽容，但严格关键字段。

6. **Config-driven routing** — 路由表在 `config/llm.yaml`，不在代码。Runtime 改变 seam 的后端无需重新编译（但需重启）。

