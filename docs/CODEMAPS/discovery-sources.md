# Discovery & Multi-Source Ranking 代码地图

> **范围**: `scripts/discovery/` — discover.py, query_expand.py, openalex.py, s2.py, arxiv_src.py, hf_papers.py, dblp.py, authority.py, dedup.py, http_client.py
> **最后更新**: 2026-06-08
> **关键特性**: Multi-signal OR authority ranking (ADR-0001)、LLM 查询扩展 (config 路由)、多源去重

<!-- Generated: 2026-06-08 | Files scanned: 12 | Token estimate: ~3500 -->

## 高层流程

```
run_campaign_tick()
    ↓
discover(topic, llm=seams["expand_llm"], force_include, ...)
    ├─ 1. LLM query expansion (LLM 路由 → config/llm.yaml)
    │      topic: "autonomous vehicle trajectory prediction"
    │      → [query1, query2, query3, ...]
    │
    ├─ 2. Multi-source parallel fetch
    │      ├─ OpenAlex (polite pool + venue signal)
    │      ├─ Semantic Scholar (venue, year, author)
    │      ├─ arXiv (category-restricted)
    │      ├─ HF Papers (hardcoded read-only token)
    │      └─ force_include papers (prepended, authority-bypassed)
    │
    ├─ 3. Cross-source dedup + field merge
    │      (DOI + arxiv_id + title matching)
    │
    ├─ 4. DBLP venue enrichment
    │      (S2 venue signal + authority whitelists)
    │
    ├─ 5. Multi-signal OR authority ranking (ADR-0001)
    │      ├─ S1: citation count (OpenAlex)
    │      ├─ S2: venue (DBLP authority list)
    │      ├─ S3: institution (affiliation)
    │      └─ S4: recency heat (2026 release)
    │
    └─ 6. Authority filter + rank
           → sorted candidates (2-3×N pool)
           ↓
          return [paper, paper, paper, ...]
```

---

## 模块拓扑

### `scripts/discovery/discover.py` — Orchestrator

**核心函数**：

```python
def discover(
    topic: str,
    *,
    llm: Callable[[str], list[str]] | None = None,
    force_include: list[dict] | None = None,
    is_ad_domain: bool = False,
    http: Callable | None = None,
    run_cli: Callable | None = None,
    over_pull_factor: float = 2.5,  # Fetch 2.5×N to allow backfill
) → list[dict]:
    """Discover papers matching topic via multi-source ranking.
    
    Returns a sorted list of candidate dicts:
      [{
        arxiv_id: "2401.12345",
        doi: "10.1234/...",
        title: "...",
        abstract: "...",
        year: 2024,
        authors: ["A", "B"],
        source: "arxiv",
        venue: "CVPR 2024",
        authority_score: 8.5,
        _discovery_rank: 1,
      }, ...]
    """
    
    # 1. Expand topic via LLM (seam, routed via config/llm.yaml)
    queries = expand_queries(topic, llm=llm)
    # queries = ["autonomous vehicle trajectory", "motion prediction", ...]
    
    # 2. Fetch from all sources in parallel
    all_candidates = []
    
    for query in queries:
        # Fetch from all sources (max workers = N)
        fetch_results = asyncio.run(_fetch_all_sources(
            query=query,
            force_include=force_include,
            http=http,
            over_pull_factor=over_pull_factor,
        ))
        all_candidates.extend(fetch_results)
    
    # 3. Dedup + field merge
    deduped = dedup_candidates(all_candidates)
    # Merges arxiv_id + doi + title matches into single entries
    
    # 4. DBLP venue enrichment (S2 signal)
    enriched = _enrich_with_dblp(deduped, run_cli=run_cli)
    
    # 5. Authority ranking (multi-signal OR)
    scored = score_authority(
        enriched,
        is_ad_domain=is_ad_domain,
        config={"require_venue": False, ...}
    )
    
    # 6. Sort and return top 2-3×N
    ranked = sorted(scored, key=lambda x: x.get("authority_score", 0), reverse=True)
    return ranked

async def _fetch_all_sources(
    query: str,
    force_include: list[dict],
    http: Callable,
    over_pull_factor: float,
) → list[dict]:
    """Fetch from all sources in parallel."""
    results = []
    
    # Prepend force_include (authority-bypassed)
    for paper in force_include:
        results.append({**paper, "_force_included": True})
    
    # Parallel fetch from sources
    tasks = [
        openalex_fetch(query, http, n=int(N * over_pull_factor)),
        s2_fetch(query, http, n=...),
        arxiv_fetch(query, http, n=...),
        hf_papers_fetch(query, http, n=...),
    ]
    
    source_results = await asyncio.gather(*tasks, return_exceptions=True)
    for sr in source_results:
        if isinstance(sr, Exception):
            log.warning(f"Source fetch failed: {sr}")
        else:
            results.extend(sr)
    
    return results
```

---

### `scripts/discovery/query_expand.py` — LLM query expansion

**核心函数**：

```python
def expand_queries(
    topic: str,
    llm: Callable[[str], list[str]] | None = None,
) → list[str]:
    """Expand a topic into multiple search queries using LLM.
    
    Example:
      Input: "autonomous vehicle trajectory prediction"
      Output: [
        "motion planning prediction autonomous driving",
        "vehicle trajectory forecasting",
        "path prediction self-driving cars",
        "trajectory modeling robotics",
        ...
      ]
    
    LLM is routed via config/llm.yaml seams["expand"].
    Cheap seam (fast model, small prompt).
    """
    
    if llm is None:
        # Fallback: naive regex expansion
        return [topic] + topic.split()
    
    # Call LLM expand seam (independent provider call)
    prompt = f"""
    Given a research topic, generate 5-7 alternative search queries
    that would find papers on the same topic using different keywords.
    
    Topic: {topic}
    
    Return a JSON list of query strings.
    """
    
    response = llm(prompt)
    # response = '["query1", "query2", ...]'
    queries = json.loads(response)
    
    return queries
```

**关键特性**：
- **LLM-powered**: Expands topic into semantically similar queries
- **Seam routing**: Uses config/llm.yaml seams["expand"] (cheap, fast)
- **Fallback**: If LLM unavailable, use regex split

---

### `scripts/discovery/openalex.py` — OpenAlex source

**核心函数**：

```python
def openalex_fetch(
    query: str,
    http: Callable,
    n: int = 50,
    polite_email: str = "research@example.org",
) → list[dict]:
    """Fetch papers from OpenAlex (large academic corpus).
    
    OpenAlex query API (free, polite-pool support).
    """
    
    # Polite pool: email lifts rate limit
    params = {
        "search": query,
        "filter": "is_open_access:true",  # optional
        "per_page": min(n, 100),
        "mailto": polite_email,
    }
    
    response = http.get("https://api.openalex.org/works", params=params)
    data = response.json()
    
    candidates = []
    for work in data.get("results", [])[:n]:
        # Extract canonical fields
        cand = {
            "title": work.get("title", ""),
            "abstract": work.get("abstract", ""),
            "doi": work.get("doi", "").replace("https://doi.org/", ""),
            "year": work.get("publication_year"),
            "authors": [a["display_name"] for a in work.get("authorships", [])],
            "source": "openalex",
            "cited_by_count": work.get("cited_by_count", 0),  # S1 signal
            "_openalex_id": work.get("id"),
        }
        candidates.append(cand)
    
    return candidates
```

---

### `scripts/discovery/s2.py` — Semantic Scholar source

**核心函数**：

```python
def s2_fetch(
    query: str,
    http: Callable,
    n: int = 50,
) → list[dict]:
    """Fetch from Semantic Scholar (venue authority signal S2)."""
    
    params = {
        "query": query,
        "limit": min(n, 100),
        "fields": "paperId,title,abstract,venue,year,authors,publicationTypes",
    }
    
    response = http.get("https://api.semanticscholar.org/graph/v1/paper/search", params=params)
    data = response.json()
    
    candidates = []
    for paper in data.get("data", [])[:n]:
        cand = {
            "title": paper.get("title", ""),
            "abstract": paper.get("abstract", ""),
            "year": paper.get("year"),
            "authors": [a["name"] for a in paper.get("authors", [])],
            "source": "semantic_scholar",
            "venue": paper.get("venue", ""),  # S2 signal
            "publication_types": paper.get("publicationTypes", []),
            "_s2_id": paper.get("paperId"),
        }
        candidates.append(cand)
    
    return candidates
```

---

### `scripts/discovery/arxiv_src.py` — arXiv source

**核心函数**：

```python
def arxiv_fetch(
    query: str,
    http: Callable,
    n: int = 50,
    categories: list[str] | None = None,
) → list[dict]:
    """Fetch from arXiv (category-restricted for quality).
    
    Default categories: cs.CV, cs.AI, cs.RO, stat.ML, (auto-driving domain adds cs.CY, ...)
    """
    
    if categories is None:
        categories = ["cs.CV", "cs.AI", "cs.RO", "stat.ML"]
    
    # arXiv API (free, no auth)
    cat_filter = " OR ".join([f"cat:{c}" for c in categories])
    arxiv_query = f"({cat_filter}) AND ({query})"
    
    params = {
        "search_query": arxiv_query,
        "max_results": min(n, 100),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    
    feed = http.get("http://export.arxiv.org/api/query", params=params).text
    # Parse Atom feed
    
    candidates = []
    for entry in feed:
        arxiv_id = entry.id.split("/abs/")[-1]
        cand = {
            "title": entry.title,
            "abstract": entry.summary,
            "arxiv_id": arxiv_id,
            "year": int(arxiv_id[:4]),  # First 4 digits of arxiv_id
            "authors": [a.name for a in entry.authors],
            "source": "arxiv",
            "published": entry.published,
        }
        candidates.append(cand)
    
    return candidates
```

---

### `scripts/discovery/hf_papers.py` — Hugging Face Papers source

**核心函数**：

```python
def hf_papers_fetch(
    query: str,
    http: Callable,
    n: int = 50,
) → list[dict]:
    """Fetch from Hugging Face Papers (model/dataset research).
    
    Uses a HARDCODED READ-ONLY HF token (owner exemption, D-发现-4).
    This is an exceptional case where a secret is hardcoded due to
    self-contained distribution; the token is read-only + scoped to
    public metadata queries only.
    """
    
    HF_READONLY_TOKEN = "hf_readonly_XXXXXX..."  # hardcoded, read-only scope
    
    headers = {"Authorization": f"Bearer {HF_READONLY_TOKEN}"}
    
    # Check env override (optional)
    if os.getenv("HF_TOKEN"):
        headers["Authorization"] = f"Bearer {os.getenv('HF_TOKEN')}"
    
    params = {
        "query": query,
        "sort": "likes",
        "direction": -1,
        "limit": min(n, 100),
    }
    
    response = http.get(
        "https://huggingface.co/api/papers/search",
        params=params,
        headers=headers,
    )
    data = response.json()
    
    candidates = []
    for paper in data.get("papers", [])[:n]:
        cand = {
            "title": paper.get("title", ""),
            "abstract": paper.get("summary", ""),
            "arxiv_id": paper.get("arxiv_id"),
            "hf_url": paper.get("url"),
            "source": "hf_papers",
            "year": int(paper.get("arxiv_id", "")[:4]) if paper.get("arxiv_id") else None,
        }
        candidates.append(cand)
    
    return candidates
```

**关键特性**：
- **Hardcoded read-only token**: 例外情况（owner exemption）
- **Env override**: `HF_TOKEN` env 可覆盖（无需编辑源）
- **Scope**: 仅公开元数据（无私有 repo 访问）

---

### `scripts/discovery/dblp.py` — DBLP venue enrichment

**核心函数**：

```python
def venue_for_title(title: str, run_cli: Callable) -> str | None:
    """Query DBLP to find venue for a paper title (enrichment).
    
    S2 signal: venue is one of the multi-signal authority factors.
    """
    
    # DBLP SPARQL query (free)
    sparql = f"""
    SELECT ?venue WHERE {{
      ?paper rdfs:label "{title}"@en .
      ?paper dblp:publishedIn ?venue .
    }}
    """
    
    # Call DBLP SPARQL endpoint (via run_cli or direct HTTP)
    result = run_cli("curl", ..., input=sparql)
    
    if result.returncode == 0:
        # Parse result, extract venue
        return extracted_venue
    return None

def is_authoritative_venue(venue: str, is_ad_domain: bool = False) -> bool:
    """Check if venue is in the whitelist (S2 authority signal)."""
    
    GENERAL_VENUES = {
        "CVPR", "ICCV", "ECCV",  # Vision
        "NeurIPS", "ICML", "ICLR",  # ML
        "SIGMOD", "VLDB",  # Databases
        ...
    }
    
    AD_ROBOTICS_VENUES = {
        "ICRA", "IROS", "CoRL",  # Robotics
        "IV", "ITSC",  # Autonomous Driving
        ...
    }
    
    whitelisted = GENERAL_VENUES
    if is_ad_domain:
        whitelisted = whitelisted | AD_ROBOTICS_VENUES
    
    return venue in whitelisted
```

---

### `scripts/discovery/authority.py` — Multi-signal OR authority scorer (ADR-0001)

**核心函数**：

```python
def score_authority(
    candidates: list[dict],
    is_ad_domain: bool = False,
    config: dict | None = None,
) → list[dict]:
    """Multi-signal OR authority ranking (ADR-0001).
    
    Four signals (any one can grant authority):
      S1: Citation count (OpenAlex cited_by_count)
      S2: Venue in whitelist (DBLP enriched)
      S3: Institution affiliation (top-N research labs)
      S4: Recency heat (published in last 12 months)
    
    Scoring: max(S1, S2, S3, S4) → one signal suffices.
    """
    
    config = config or {}
    require_venue = config.get("require_venue", False)
    threshold = config.get("authority_threshold", 0)  # min score to include
    
    CITATION_THRESHOLD = 50  # S1: >= 50 citations
    INSTITUTION_LIST = ["Stanford", "MIT", "FAIR", "DeepMind", ...]  # S3
    RECENCY_THRESHOLD_MONTHS = 12  # S4: published in last year
    
    scored = []
    for cand in candidates:
        s1_score = 1.0 if cand.get("cited_by_count", 0) >= CITATION_THRESHOLD else 0.0
        
        venue = cand.get("venue", "")
        s2_score = 1.0 if is_authoritative_venue(venue, is_ad_domain) else 0.0
        
        authors_affiliations = cand.get("affiliations", [])
        s3_score = 1.0 if any(inst in str(authors_affiliations) for inst in INSTITUTION_LIST) else 0.0
        
        years_old = 2026 - cand.get("year", 2000)
        s4_score = 1.0 if years_old <= RECENCY_THRESHOLD_MONTHS / 12 else 0.0
        
        # OR logic: one signal suffices
        is_authoritative = max(s1_score, s2_score, s3_score, s4_score) > 0.5
        
        cand["_s1_score"] = s1_score
        cand["_s2_score"] = s2_score
        cand["_s3_score"] = s3_score
        cand["_s4_score"] = s4_score
        cand["is_authoritative"] = is_authoritative
        cand["authority_score"] = max(s1_score, s2_score, s3_score, s4_score)
        
        if is_authoritative or require_venue == False:
            scored.append(cand)
    
    return scored
```

---

### `scripts/discovery/dedup.py` — Cross-source dedup

**核心函数**：

```python
def dedup_candidates(candidates: list[dict]) -> list[dict]:
    """Merge duplicates across sources (DOI, arxiv_id, title matching).
    
    When the same paper is found in multiple sources, merge fields:
      - DOI: exact match → merge
      - arXiv ID: exact match → merge
      - Title: fuzzy similarity > 0.95 → merge
    
    Merge priority: prefer arxiv (has official HTML tier-1 ingest).
    """
    
    deduped = {}  # key → merged candidate
    
    for cand in candidates:
        # Canonicalize arxiv_id (extract from various formats)
        arxiv_id = _normalize_arxiv_id(cand.get("arxiv_id", ""))
        doi = _normalize_doi(cand.get("doi", ""))
        title = cand.get("title", "").lower().strip()
        
        # Find existing entry
        key = None
        if arxiv_id:
            key = ("arxiv", arxiv_id)
        elif doi:
            key = ("doi", doi)
        elif title:
            # Fuzzy match against existing titles
            for existing_key in deduped:
                if existing_key[0] == "title":
                    existing_title = existing_key[1]
                    if _title_similarity(title, existing_title) > 0.95:
                        key = existing_key
                        break
            if key is None:
                key = ("title", title)
        else:
            # No canonical identifier; treat as unique
            key = ("url", cand.get("_openalex_id") or cand.get("_s2_id"))
        
        # Merge
        if key in deduped:
            deduped[key] = _merge_candidates(deduped[key], cand)
        else:
            deduped[key] = cand
    
    return list(deduped.values())

def _merge_candidates(existing: dict, new: dict) -> dict:
    """Merge two candidates, preferring arXiv + filled fields."""
    merged = {**existing}
    
    # Prefer arxiv_id if available
    if "arxiv_id" not in merged and "arxiv_id" in new:
        merged["arxiv_id"] = new["arxiv_id"]
    
    # Fill empty fields from new
    for key in new:
        if key not in merged or merged[key] is None:
            merged[key] = new[key]
    
    # Track sources
    sources = set(merged.get("_sources", []))
    sources.add(new.get("source", "unknown"))
    merged["_sources"] = list(sources)
    
    return merged
```

---

### `scripts/discovery/http_client.py` — Throttled HTTP client

**核心函数**：

```python
def build_http(
    rate_limit: float = 1.0,  # requests/second per domain
    timeout: float = 30.0,
) -> Callable:
    """Polite-pool HTTP client (shared by all sources)."""
    
    class ThrottledHTTPClient:
        def __init__(self):
            self.session = requests.Session()
            self.rate_limiters = {}  # domain → rate limiter
        
        def get(self, url: str, **kwargs):
            domain = urllib.parse.urlparse(url).netloc
            
            # Acquire rate limit permit
            if domain not in self.rate_limiters:
                self.rate_limiters[domain] = asyncio.Semaphore(rate_limit)
            
            async def _request():
                async with self.rate_limiters[domain]:
                    return self.session.get(url, timeout=timeout, **kwargs)
            
            return asyncio.run(_request())
    
    return ThrottledHTTPClient()
```

---

## 配置与常数

| 常数 | 值 | 含义 |
|-----|---|----|
| `over_pull_factor` | 2.5 | Fetch 2.5×N 候选允许 backfill |
| `CITATION_THRESHOLD` | 50 | 至少 50 次引用 = S1 authority signal |
| `RECENCY_THRESHOLD_MONTHS` | 12 | 最近 12 个月内发表 = S4 signal |
| `_MD_CHAR_CAP` | 200k | query_expand seam 输入 cap |
| `HF_READONLY_TOKEN` | hardcoded | Read-only Hugging Face token（owner exemption） |

---

## 关键设计决策（ADR-0001）

1. **Multi-signal OR logic** — 任何单一信号（Citation / Venue / Institution / Recency）都能授予权威性。不是 AND（排他性太强），而是 OR（包容性）。

2. **Venue whitelist per domain** — 通用 venue（CVPR, NeurIPS）总是有效；AD/robotics venue（ICRA, IV）仅当 `is_ad_domain=true` 时有效。

3. **No citation gate** — 不要求最低引用数；S1 只是一个信号而已。新论文（0 引用）也可能有其他信号。

4. **Force-include bypasses authority** — `force_include` 论文被前置、跳过权威过滤。用户说"必须"→ "必须"。

5. **Dedup by DOI > arxiv_id > title** — 优先规范化标识符以避免虚假重复。

6. **Polite-pool HTTP** — 所有源共享单一 rate-limit 客户端（尊重 API）。

---

## 相关文档

- `engine-core.md` — discover 在 hub/spoke 中的位置
- `adr/0001-multi-signal-authority-no-citation-gate.md` — ADR-0001（设计决策）
- `references/discovery-and-authority.md` — Discovery 详细说明

