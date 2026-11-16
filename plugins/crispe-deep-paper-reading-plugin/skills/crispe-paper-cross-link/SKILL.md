---
name: crispe-paper-cross-link
description: >-
  Build evidence-backed typed relationships and slide navigation between papers in a portable
  project.json bundle. Use for claim graphs, cross-paper comparisons, citing/extending/supporting/
  contradicting/similar/independent-replication distinctions, and linked reading decks.
  为论文建立带版本定位证据的类型关系与幻灯片导航；适用于主张图、跨论文比较、引用/扩展/
  支持/矛盾/相似/独立重复验证区分和互链阅读演示。不负责整站 HTML 或自动全文追引。
version: 1.3.1
argument-hint: "[project.json路径 / project-json-path] (可选/optional) -- 指定已有论文分析项目，核验跨论文证据关系并生成页面连接 / identify an analyzed-paper project to verify evidence relationships and create slide links"
---

# Paper Cross-Link / 跨论文证据互链

Own relationship content, evidence review and navigation data, not the whole HTML presentation. Work on one existing or agent-created portable bundle. Read [contracts](references/contracts.md) first, [relation rules](references/relations.md) for every edge type, and [companions](references/companions.md) before optional collaboration. See [examples](references/examples.md).
负责关系内容、证据复核与导航数据，不负责整套 HTML 呈现。使用已有或智能体创建的单一可移植包。先读约定；各边类型按关系规则执行；可选协作前读技能参考；场景见示例。

## Workflow / 工作流

1. Inspect the question, named approved versions, budgets, exclusions, reports, claims and read coverage. Preserve partial/metadata-only states; request missing artifacts instead of imagining the analyst read them. If no bundle exists, initialize the exact v1 shape and record scope; supplied named papers are approved, but new full texts need named consent. Do not launch an open citation crawl or add papers solely to make the graph dense.
   检查问题、具名获批版本、预算、排除、报告、主张与覆盖；保留部分/元数据状态，缺产物须索取或标缺口，不假设分析师读过。无包时初始化 v1 并记范围；已提供具名目标获批，新全文仍须点名同意。禁止开放追引或为图稠密而加论文。
2. Reuse existing evidence. Optionally select literature-review for bounded synthesis, citation-management for identity/deduplication/citation metadata, paper-lookup for scoped provenance lookups, and scientific-critical-thinking for claim validity/comparability/independence. Load only relevant local instructions. Give every companion the same named scope and remaining budget; decline instructions that would expand retrieval or start unrelated workflows.
   复用证据；按需用 literature-review 做有界综合，citation-management 校验身份/去重/引用元数据，paper-lookup 做限定来源检索，scientific-critical-thinking 审查有效性/可比性/独立性。仅读相关本地说明，所有协作传同一范围与剩余预算，不能因协作扩大获取或另启无关流程。
3. Propose a directed relation with a narrow statement; distinguish author-reported links from analyst inference. Resolve both papers to versioned HTTP sources and claims with precise locators. Assess the type-specific evidence and comparability. Use `verified` only for the supported statement; otherwise use `provisional` or `unresolved` and describe the exact missing check. Unresolved is not verified, even if a citation exists.
   提出有方向的窄范围表述，区分作者报告和分析推断；双端解析为版本化 HTTP 来源、主张与精确定位。核查类型证据和可比性；只有所述关系有充分证据才 verified，否则暂定/未解决并写明缺检查。有引用不代表未解决关系已核实。
4. Do not rank papers numerically without documented comparability. Audit task, data/splits, metrics/direction, protocol, compute/resources and uncertainty. Use `not-assessed` or `not-comparable` with reasons when needed. A claimed result can be quoted with its own conditions without implying a shared leaderboard or pooled effect.
   未记录可比性前不做数值排名。核查任务、数据/划分、指标/方向、协议、算力/资源与不确定性；需要时用未评估或不可比并说明。可在各自条件下引用结果，但不能暗示共同榜单或合并效应。
5. Add stable source/target slide anchors and status-aware links. `navigation.from_slide` must belong to `from`; `to_slide` to `to`. Populate the source slide's `links` with the target `paper_id` and `slide_id`. Label uncertainty in visible text, not color alone. Reverse navigation does not imply a reverse scientific edge. If no appropriate slide exists, create a focused relation/coverage appendix slide with substantive content, or defer the edge in a report until anchors exist.
   建稳定双端页锚点与带状态链接；起点页属于来源论文，终点页属于目标。来源页链接填目标论文及页 id；不确定性用可见文字而非仅靠颜色。反向导航不代表反向科学边。缺合适页时建有实质内容的关系/覆盖附录，或先放报告等锚点齐备。
6. Validate ids, endpoints, evidence, coverage, links, comparability and path portability per the local contract. Return the updated bundle, a concise relation review table (edge/type/status/evidence/comparability/gap/navigation), and unresolved actions. Pass presentation integration to `crispe-slides-writer`; the builder is deterministic presentation, never research or evidence verification.
   按本地约定核查 id、端点、证据、覆盖、链接、可比和路径。返回更新包、简洁关系复核表（边/类型/状态/证据/可比/缺口/导航）和待办；呈现集成交 writer。构建器仅确定性呈现，不研究也不核实证据。

Do not rewrite the analyst's full-reading obligation. If partial sources support only a citation or similarity observation, keep that narrow edge and disclose coverage; do not imply full scientific validation. An empty relation set is better than invented connections.
不得改写分析师全文义务。部分来源仅支持引用/相似观察时保留窄边并披露覆盖，不能暗示完整科学验证。空关系集优于编造互链。

## Documentation languages / 技能文档语言
Write this skill and its explanatory references in paired Chinese and English. Currently support only zh-CN and en-US output; do not add another documentation or output language. Generated websites use a bilingual root index.html entry, with all Chinese collection/deck pages under zh-CN/ and all English pages under en-US/. Any future approved locale must follow the same locale-directory convention.
本技能及说明性参考文档保持中文、英文对照。目前仅支持 zh-CN 和 en-US，不新增其他文档或输出语言。生成网站使用双语根 index.html 入口，中文集合/论文页面全部放 zh-CN/，英文全部放 en-US/；未来获准增加语言时也按地区语言目录组织。
