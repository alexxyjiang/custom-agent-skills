# Bounded workflow and checkpoints / 有界工作流与检查点

## C0 — Scope and discovery / 范围与发现

Create a scope draft and a candidate ledger in `scope.search_log` (strings, per contracts). Record exact query, source, cutoff, counters and include/defer/exclude decisions. `scope.exclusions` holds explicit exclusions. Use finite per-call result limits; do not fetch broad results and truncate only after examining them. Offline means zero network calls; set metadata budget to zero if none is needed. A scoped search is not an exhaustive/systematic review. Do not request additional full texts to fill a quota.
创建范围草稿及 `scope.search_log` 候选台账（按约定使用字符串），记录查询、来源、截止、计数和纳入/暂缓/排除；明确排除放 `scope.exclusions`。每次请求有限条数，不能先大量获取检查再截断。离线不联网；无需元数据检索时预算设零。有界检索不等于穷尽/系统综述，不能为凑篇数额外取全文。

**Artifact:** draft `project.<locale>.json` with `papers: []`, `relations: []`, scope, title, locale and version 1. Candidates can live entirely in the log until identity/version/source is resolved. **Checkpoint:** state scope, limits and a named/versioned proposed full-text set; block new full texts until approved. User-named targets already satisfy this approval, subject to budget consistency.
**产物：** 草稿项目包含空论文/关系数组、范围、标题、语言及版本 1；候选身份/版本/来源未解时留日志即可。**检查点：** 展示范围、上限和具名版本集合；新全文未授权先暂停。用户已指定目标无需重复授权，但须满足预算。

## C1 — Analyst reading / 分析师阅读

For each target, pass question, pinned identity/URL, local file if any, approval list, budgets, exclusions and locale. Request the analyst's actual full-paper report and page-by-page inventory, evidence locators, limitations, and any pedagogical examples with truthful execution status. Keep the analyst's own reading-priority judgment distinct from unsupported cross-paper numerical ranking. Do not score an unread target from its abstract.
逐篇传递问题、固定身份/URL、本地文件、授权集、预算、排除和语言；要求实际全文报告、逐页清单、证据定位、局限及如实标执行状态的教学示例。分析师阅读价值判断不同于无依据的跨论文数值排名；不能根据摘要给未读目标评分。

**Artifacts:** relative `reports/<paper-id>.md`; `papers[]` with coverage, claims and optional examples. Record total pages, inspected ranges and missing ranges in report and coverage. Read appendices/supplements included with the target; separately discovered full-text supplements or other papers require checking the named scope. Keep unapproved material unread. **Checkpoint:** verify every declared full-text target really has no unread material. If partial, state why, offer resume/available-file recovery and proceed to a limited handoff only with that limitation visible. Do not automatically purchase, install tools or widen scope.
**产物：** 相对报告和带覆盖/主张/可选示例的论文对象；报告及覆盖记录总页数、已读与未读。目标随附附录/补充材料应读；另发现的全文补充材料或论文先核对具名范围，未获批不读。**检查点：** 全文目标确无未读材料；部分覆盖则说明原因、可续读/补文件，并仅以显式限制交接，不自动付费、装工具或扩范围。

## C2 — Cross-link / 关系构建

Pass the same bundle, reports and scope to `crispe-paper-cross-link`. Ask for a typed claim relation table, versioned endpoint evidence, comparability reasons, and navigation anchors, not an entire HTML site. Start stable content slide ids in `papers[].slides`; keep enough content to explain the evidence rather than making empty anchors. Cross-link may author focused relation/gap slides and links, not rewrite analyst reports. If only one paper is in scope, an empty relation array is valid.
把同一项目包、报告和范围交 cross-link，要求有类型主张关系、版本端点证据、可比理由和导航锚点，而非完整 HTML。在论文幻灯片数组建立稳定内容页 id，内容须能解释证据，不能只放空锚点。cross-link 可写聚焦关系/缺口页和链接，不重写分析报告。只有一篇时关系数组可为空。

**Artifacts:** enriched `claims`, `relations`, content slide anchors and `slides[].links`, plus a relation review section in existing reports. **Checkpoint:** review each edge's type/status, both endpoint claims and locators, comparability and direction. No edge is verified merely because it is plausible. Unresolved edges remain visible as unverified, or stay in a report if valid navigation is not yet possible.
**产物：** 增补主张、关系、内容锚点、链接和报告关系复核节。**检查点：** 逐边复核类型/状态、双端主张/定位、可比性及方向；看似合理不等于已核实。未解决边明确未核实，若无法有效导航则暂存报告。

## C3 — Writer and deterministic builder / 写作与确定性构建

Supply the requested `project.<locale>.json` and all relative reports/assets to `crispe-slides-writer`. Request teaching-first lead/cards/takeaways, examples and appendix coverage notes, preservation of stable ids and evidence, and accessible navigation/figures. The writer owns deck structure/style/HTML integration. Reordering slides is fine; changing/removing ids requires updating and revalidating all references. The writer must not silently summarize away unread material, convert inferred claims to author claims or turn unresolved relations into conclusions.
将项目包与所有相对报告/资源交 slides writer；要求教学优先的引导/卡片/收获、示例及覆盖附录，保留稳定 id 与证据，提供可访问导航/图示。writer 负责整套结构/样式/HTML 集成；可重排，改/删 id 须同步更新并核查所有引用。不能隐去未读材料、将推断改成作者主张或把未解决关系写成定论。

**Artifact:** reviewed portable bundle and the writer's requested deterministic presentation outputs. **Checkpoint:** validate all contract fields, ids, links, figures, evidence and honest execution/read coverage before building; inspect rendered navigation after building. If writer/builder is unavailable, deliver the valid bundle as a pending presentation handoff, not a completed HTML deck. A builder failure does not invalidate good research or justify researching new claims.
**产物：** 审核后的可移植包及 writer 所需确定性呈现输出。**检查点：** 构建前核查全部约定字段、id、链接、图、证据及执行/阅读真实性；构建后检查导航。writer/构建器不可用则交待呈现的有效包，不冒称完成 HTML。构建失败不否定已有研究，也不能成为补新主张的借口。

Checkpoints are explicit recorded quality states, not repeated permission prompts. Pause for a user decision at new full-text/scope approvals, ambiguous targets, or a genuine blocker; proceed through satisfied checkpoints using existing authorization.
检查点是显式质量记录，不是重复权限提示；只有新全文/范围授权、目标歧义或真实阻塞才暂停请求用户决定，已满足检查点沿用授权继续。

## Visual and layout checkpoints / 图表与版式检查点
C1 records paper.visuals before writer generation: selected main point → claim → original figure/table locator → target slide → ready/missing. C3 reconciles visual_refs and actual assets, and blocks missing originals for figure-based main arguments. Shared figures require a key main target and explicit dependent links. Review main text fit before building: no non-code scrolling by default, reflow or add consecutive pages instead; hard exceptions require text_scroll_reason.
C1在生成前记录重点→主张→原图表定位→目标页→就绪/缺失；C3核对引用和实际资源，主线依赖缺图阻断。同图须主线关键目标及依赖链接。构建前审文字适配，非代码默认无滚动，优先重排/连续页，困难例外记录原因。
