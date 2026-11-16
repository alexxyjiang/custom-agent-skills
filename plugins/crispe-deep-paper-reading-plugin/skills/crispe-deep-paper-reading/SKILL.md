---
name: crispe-deep-paper-reading
description: >-
  Orchestrate a bounded deep-paper-reading project from named papers or a research question:
  budgeted candidate discovery, named full-text approval, full-reading analyst reports,
  typed cross-paper evidence links, and a portable slides-writer handoff. Use for multi-stage
  paper reading-to-slides or research reading plans, not a lone bibliographic lookup.
  深度论文阅读编排：有限检索、具名全文授权、逐篇全文分析、跨论文证据关系及幻灯片交接；
  适用于读论文到演示的完整项目、专题精读，不用于单纯元数据查询。
version: 1.3.1
argument-hint: "[论文ID/链接/PDF路径或研究问题 / paper-ids|URLs|PDF-paths|research-question] (可选/optional) -- 指定精读目标或主题、阅读范围及输出语言 / specify reading targets or topic, scope and output language"
---

# Deep Paper Reading / 深度论文阅读

Own the research plan, shared artifacts and checkpoints; let the analyst own actual full reading, cross-link own evidence relationships, and the slides writer own presentation authoring. Read [contracts](references/contracts.md) before touching the bundle, [workflow](references/workflow.md) for phase execution, and [companions](references/companions.md) before collaboration. See [examples](references/examples.md) for bilingual scenarios.
负责研究计划、共享产物与检查点；分析师负责实际全文阅读，cross-link 负责证据关系，slides writer 负责演示写作。修改项目包前读约定，分阶段执行读工作流，协作前读技能参考；双语场景见示例。

## Operating rules / 执行规则

1. Establish the question, output locale (`zh-CN`/`en-US`), named/versioned target set, exclusions, metadata and full-text budgets, query/time boundaries and stop criteria. Reuse user-provided constraints. Explicitly requested/supplied papers are already approved; a topic authorizes bounded discovery, not unnamed full texts. Propose finite defaults when absent: 20 metadata records, at most 3 full texts, 3 queries and 20 minutes of search. State these as provisional limits; do metadata work within them, but obtain a named target approval before any newly discovered full text. If supplied targets exceed a cap, reconcile before reading instead of silently dropping targets.
   先明确问题、语言、具名版本目标、排除项、元数据/全文预算、查询/时间边界及停止条件。沿用用户约束；已指定/提供论文已获批，主题仅允许有限发现而非未具名全文。缺省提议有限预算：20 条元数据、最多 3 篇全文、3 次查询、20 分钟检索。声明为暂定上限，可在内查元数据；新发现全文仍须具名批准。目标超上限先协调，不静默删减。
2. Log each candidate's identity/version, source, relevance, decision (`include`, `defer`, `exclude`), reason and intended depth. Deduplicate versions without confusing reports with independent studies. Stop at the first budget, elapsed-time, query, sufficient-coverage or no-new-relevant-candidates condition; report what stopped and what remains. No recursive citation crawl, autonomous cap increase or companion-driven scope expansion.
   记录每个候选的身份/版本、来源、相关性、决策、理由和拟读深度；去重版本但不将同一研究的报告当独立研究。任一预算、时间、查询、覆盖充分或无新相关候选条件触发即停，报告原因与剩余事项。禁止递归追引、自动加预算或借协作扩大范围。
3. Approve an exact named set once; reuse that approval across analyst, cross-link and writer. Ask only for additions, version changes or cap changes. Pass the approved set and remaining budgets to every companion; inspect optional full-text retrieval behavior before invocation. Do not let a companion fetch cited/follow-up full texts outside the set.
   精确具名集合只授权一次，在全链复用；新增论文、换版本或改上限才再确认。每次协作传递集合和剩余额度，调用前检查其可选全文获取行为，不得越界下载参考或后续论文。
4. Use metadata/abstract depth for candidate screening. Each approved deep-read target goes to `crispe-paper-analyst` for every page, figures, tables, equations, related work, references and included supplements. Preserve its report structure, locator detail and full-reading standard; do not replace it with a short summary or early score. An access/tool/context failure becomes `partial` with explicit unread ranges, never a successful full read. Pause/resume in chunks when needed. A metadata-only candidate is not a deeply read target. Before publishing a collection, require an evidence-backed integer 1–4 score for each card; complete substantive appraisal first, and disclose remaining gaps separately instead of deferring scores.
   候选筛选可只读元数据/摘要；每个获批精读目标交分析师逐页读图表、公式、相关工作、参考文献及随文补充材料。保留其报告结构、精确定位和全文标准，不用短摘要或提前评分代替。访问/工具/上下文失败记部分覆盖及未读范围，不伪装完成；必要时分块续读。元数据候选不算精读完成。集合发布前每张卡片必须有证据支持的1–4整数评分；先完成实质审查，剩余缺口另列，不能以暂缓替代评分。
5. Sequence `crispe-paper-analyst` → `crispe-paper-cross-link` → `crispe-slides-writer`, using one agent-generated `project.json` and relative reports/assets. Sequential role execution in the same agent is valid; delegate only if authorized and supported. Missing skills do not justify pretending they ran: show original-source guidance, execute the documented role with available tools where possible, and expose any remaining checkpoint failure.
   按分析师→关系构建→幻灯片写作执行，使用同一份智能体生成的 `project.json` 和相对报告/资源。同一智能体顺序扮演角色即可；仅经允许且宿主支持才委派。缺技能须提示原始来源，能用现有工具履行角色则继续，不能声称已调用；暴露未满足的检查点。
6. Stop research at the writer boundary. The builder renders deterministically and cannot supply missing research. Hand over verified content and visibly labeled provisional/unresolved items; never upgrade evidence or coverage to make a polished deck.
   写作边界处停止研究；构建器确定性呈现，不能补研究。交付已核实内容及显式标记的暂定/未解决事项，不为美观升级证据或覆盖。

## Delivery / 交付

Return the bundle location, approved targets and actual depths, candidate decisions and actual budget use, report/evidence/navigation checks, unresolved gaps and the last completed checkpoint. Use the user's language; retain identifiers and locators literally. Documentation is bilingual; a generated project uses one primary locale with optional bilingual strings. Never label partial reading as completed deep reading.
返回项目包位置、获批目标与实际深度、候选决策与真实预算、报告/证据/导航检查、未解决缺口和最后完成的检查点。跟随用户语言，保留原始标识与定位。本定义双语，项目选择一个主语言并可在字符串内双语。部分阅读不能标为完整精读。

## Documentation languages / 技能文档语言
Write this skill and its explanatory references in paired Chinese and English. Currently support only zh-CN and en-US output; do not add another documentation or output language. Generated websites use a bilingual root index.html entry, with all Chinese collection/deck pages under zh-CN/ and all English pages under en-US/. Any future approved locale must follow the same locale-directory convention.
本技能及说明性参考文档保持中文、英文对照。目前仅支持 zh-CN 和 en-US，不新增其他文档或输出语言。生成网站使用双语根 index.html 入口，中文集合/论文页面全部放 zh-CN/，英文全部放 en-US/；未来获准增加语言时也按地区语言目录组织。
