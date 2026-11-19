# Portable project bundle contract v1 / 可移植项目包约定 v1

Read before creating or modifying `project.<locale>.json`. This file is self-contained; no installed companion or external schema is needed to interpret it. The same contract is used by reading orchestration, cross-linking and the slides-writer handoff.
创建或修改 `project.<locale>.json` 前阅读本文。本约定自包含，无需安装其他技能或访问外部模式；阅读编排、关系构建及幻灯片写作交接使用同一约定。

## Ownership and portability / 职责与可移植性

Agents generate and review the research bundle: sources, reading reports, claims, examples, relations and slide content. A builder is a deterministic presentation step, not a researcher: it must not search, fetch full texts, invent evidence, infer missing relations, upgrade coverage or turn not-run code into passed code. A successful build establishes presentation validity only.
智能体生成并审查研究包：来源、阅读报告、主张、示例、关系与幻灯片内容。构建器仅确定性呈现，不做研究；不得检索、获取全文、补造证据、推断缺失关系、升级阅读覆盖或将未运行代码改为通过。构建成功仅说明呈现有效。

Use a bundle root containing `project.<locale>.json` (`project.zh-CN.json` / `project.en-US.json`), optional `reports/`, and optional `assets/`. Relative files resolve from that root, not the current working directory. Ship referenced files together. No absolute filesystem paths, `file:` URLs, `..` traversal, machine-specific home paths or escaping symlinks. `figure.src` is a relative asset path, never a remote URL. Public evidence URLs are HTTP(S), not local paths. Preserve existing valid content when updating a bundle.
项目根目录包含 `project.<locale>.json`（`project.zh-CN.json` / `project.en-US.json`）、可选 `reports/` 和 `assets/`；相对路径从项目根解析，随包交付引用文件。禁止绝对文件路径、`file:` URL、`..` 越界、本机主目录及逃逸符号链接。`figure.src` 必须为相对资源路径而非远程 URL；公开证据地址使用 HTTP(S)。更新时保留已有有效内容。

## Exact shape / 精确结构

All fields below are required except those explicitly marked optional. Arrays may be empty; required strings remain present, with unknown/not-applicable facts explicitly explained rather than fabricated. Use JSON integers for schema_version, score.value, budgets and line indices; paper.version stays a string and booleans are JSON booleans. Do not rename keys, change enums, add private schema fields or substitute per-paper bundles. Research logs and reports can hold additional narrative without extending this shape.
除明确标注可选外，下列字段均必需。数组可为空；必需字符串仍需保留，未知或不适用须说明而非编造。schema_version、score.value、预算及行号使用JSON整数；paper.version保持字符串，布尔值使用JSON布尔。禁止改键、改枚举、添加私有模式字段或拆成逐篇项目包；补充叙述放日志和报告。

| Object / 对象 | Fields and types / 字段与类型 |
|---|---|
| root | `schema_version`: integer exactly `1`; `title`: string; `language`: `zh-CN` or `en-US`; `scope`: object below; `papers`: paper array; `relations`: relation array |
| scope | `question`: string; `approved_full_text`: string array of paper ids mapped to exact versions; `max_metadata_records`: nonnegative integer; `max_full_text`: nonnegative integer; `stop_conditions`: string array; `search_log`: string array; `exclusions`: string array |
| paper | `id`: safe slug; `title`: string; `source_url`: versioned HTTP(S) URL; `version`: string; `publication_source`: optional verified conference/journal label string (e.g. ICLR 2026); `archive_source`: optional verified preprint/archive label including identifier/version; `topic`: string; `summary`: string; `score`: score object below; `read_coverage`: object below; `report_path`: optional relative path string; `claims`: claim array; `examples`: example array; `slides`: slide array |
| score | `value`: integer 1–4 (required, never null/deferred); `rationale`: nonempty string; `claim_ids`: nonempty array referencing this paper's evidence claims |
| read_coverage | `status`: `full-text`, `partial`, or `metadata-only`; `read`: string array of inspected page/section/figure/table/equation locators; `unread`: string array of outstanding locators and reasons |
| claim | `id`: string unique within its paper; `text`: string; `locator`: string; `url`: HTTP(S) string; `kind`: `paper-claim`, `external-evidence`, or `analyst-inference`; `limits`: string |
| example | `id`: string unique within its paper; `kind`: `teaching`, `original`, or `reproduction`; `source_locator`: string; `code`: string; `language`: string; `run_command`: string; `expected_output`: string; `actual_output`: string; `execution`: `passed`, `not-run`, or `failed`; `limitations`: string; `steps`: step array |
| step | `lines`: array of 1-based integers into the example's `code`; `explanation`: string; `state`: string |
| slide | `id`: safe slug unique within its paper; `title`: string; `chapter`: string; `lead`: string; `cards`: card array; `claim_ids`: string array referring to this paper's claims; `example_id`: optional reference to this paper's example; `appendix`: boolean; `takeaway`: optional string; `links`: link array; `figure`: optional figure object; `figure_role`: optional `key`/`reference`; `figure_notes`: optional card array; `figure_layout`: optional `auto`/`left`/`right`/`top`/`bottom`/`full` |
| card | `title`: string; `text`: string; `tone`: `indigo`, `emerald`, `amber`, or `rose` |
| link | `paper_id`: existing paper id; `slide_id`: existing slide id in that paper; `label`: string |
| figure | `src`: relative asset path string; `alt`: string; `caption`: string; `source_url`: HTTP(S) string; `locator`: string; `original_caption`: optional complete verbatim caption provenance (not rendered separately) string |
| relation | `id`: string unique across relations; `from`: source paper id; `to`: target paper id; `type`: `cites`, `extends`, `supports`, `contradicts`, `similar`, or `replicates`; `statement`: string; `status`: `verified`, `provisional`, or `unresolved`; `evidence`: evidence array; `comparability`: object below; `navigation`: object below |
| evidence | `paper_id`: existing paper id; `claim_id`: existing claim id within that paper |
| comparability | `status`: `comparable`, `not-comparable`, or `not-assessed`; `reason`: string |
| navigation | `from_slide`: existing slide id in the relation's `from` paper; `to_slide`: existing slide id in the relation's `to` paper |

A safe slug matches `^[a-z0-9]+(?:-[a-z0-9]+)*$`. Paper ids are globally unique. Claim/example ids are scoped to their paper: resolve evidence as `(paper_id, claim_id)`, never claim id alone. `state` is an explanatory string (e.g. variable state or "not observed; not run"), not an additional execution enum. `limits` and `limitations` are strings, not arrays. `language` on an example is a programming language; root `language` is the primary presentation locale. Bilingual prose may appear inside string values; do not invent a `bilingual` locale.
安全 slug 使用上述正则。论文 id 全局唯一；主张与示例 id 属于论文命名空间，证据按二元组解析。`state` 是解释性字符串（如变量状态或“未观察；未运行”），不是新增执行枚举。`limits`、`limitations` 是字符串而非数组。示例 `language` 表示编程语言，根级表示主要呈现语言；值内可双语，但不能新增 `bilingual` 枚举。

## Scope and versions / 范围与版本

`approved_full_text` contains paper ids such as `paper-a`; each id maps to its exact `paper.version` and versioned `source_url`, also recorded in `search_log`. Supplied or explicitly requested named targets count as approved. A topic or "find related work" is not blanket full-text approval. Approval does not remove `max_full_text`; count distinct approved paper/version full texts accessed for this task, including supplied files. Metadata budget counts records returned/examined before deduplication (including repeats across queries); cap each request by the remaining budget and stop pagination at the cap.
`approved_full_text` 使用精确论文 id，并通过 paper.version 与 source_url 固定版本，并在 `search_log` 保持一一映射。用户提供或明确要求的具名目标视为获批；主题或“找相关工作”不是无限全文授权。获批仍受全文上限约束；本任务访问的不同论文/版本全文（含用户提供文件）均计数。元数据预算按去重前返回/检查记录计数（含跨查询重复项）；每次请求限于剩余额度，到上限停止翻页。

Resolve arXiv links to explicit `vN` versions. For publications use a specific version-of-record DOI HTTP(S) URL or immutable publisher version URL and state that version. A mutable landing page without a pinned version is insufficient. For local-only or unavailable provenance, preserve a useful partial draft and log the unresolved URL/version in a report; do not invent an HTTP source or claim the bundle is ready for final handoff. Updating a version requires checking approval, coverage and all dependent evidence again.
arXiv 链接须明确 `vN`；正式出版用特定正式版本 DOI 的 HTTP(S) 地址或不可变出版社版本链接，并填写版本。未固定版本的可变落地页不够。仅本地文件或来源不明时保留有用的部分草稿，在报告记录待解决地址/版本；不得捏造 HTTP 来源或声称可最终交接。换版本须重新核查授权、覆盖和所有依赖证据。

Each `search_log` string records timestamp, database/tool, exact query/filter/cutoff, requested/returned/examined counts, remaining budgets, paper identities, candidate decision (include/defer/exclude), reason and next action as applicable. Record approval events and the actual stopping reason here. `exclusions` records identities and concrete reasons; deferred candidates stay visible in the log, not silently excluded. No search means record "not searched" with the reason, not fictional queries.
每条 `search_log` 字符串按适用记录时间、数据库/工具、原始查询/过滤/截止日期、请求/返回/检查数、剩余预算、论文身份、候选决策（纳入/暂缓/排除）、原因与下一步；也记录授权事件及实际停止原因。`exclusions` 记录身份与具体理由；暂缓项留在日志，不能默默排除。未检索须如实说明原因。

## Evidence, coverage and execution / 证据、覆盖与执行

`full-text` means every page of the approved version, including figures, tables, equations, Related Work, references and available included appendices/supplements, was inspected. Inventory separate unavailable supplements explicitly; unresolved portions make coverage `partial`. `partial` lists both read and unread ranges/reasons. `metadata-only` lists metadata/abstract access and the unread full text; it cannot ground method verification. Do not promote coverage because an abstract, retrieval tool or builder succeeded.
`full-text` 表示已检查获批版本的全部页面，包含图表、公式、相关工作、参考文献及随文可用附录/补充材料。单独补充材料不可得也须列清；尚有未读部分则为 `partial`。部分阅读列出已读和未读范围及原因；`metadata-only` 列元数据/摘要访问与未读全文，不能支持方法级核实。摘要、获取工具或构建成功均不能升级覆盖。

Claims carry a version-consistent URL and precise locator (page + section/table/figure/equation, or abstract/metadata label). Separate what authors assert, independently sourced evidence, and analyst inference. Inference locators identify the inspected basis and limits, not a fictional quotation. A `verified` relation needs resolvable evidence from both endpoints, sufficient inspected passages for its type, and acknowledged limits; verification is scoped to the relation statement, not universal scientific truth. Metadata can verify bibliographic identity or an explicit citation record, not replication or efficacy. `provisional` means some evidence exists but a stated check remains; `unresolved` means the relation is not established. Neither is verified. Record relation-specific gaps in `statement` and claim `limits` without new fields.
主张须有版本一致的 URL 和精确定位（页加节/图/表/公式或摘要/元数据标记）。区分作者主张、外部证据、分析者推断；推断定位写实际依据及局限，不伪造引文。`verified` 关系须有双端可解析证据、足够的已读段落及局限说明；核实仅针对关系表述，不代表普遍科学真理。元数据可核实身份或明确引用记录，不能证明复现或功效。`provisional` 表示有部分证据但检查未完成；`unresolved` 表示尚未建立，均不得当作已核实。关系缺口放 `statement` 和主张 `limits`，不添加字段。

Teaching code is illustrative, original code is attributed to the paper/source, and reproduction code attempts a stated result; none implies independent scientific replication. `passed` requires observed execution matching the stated check; record actual output. `not-run` keeps `actual_output` explicitly unobserved, distinct from `expected_output`. `failed` records the real error/result. Step line numbers must exist; step states cannot imply execution when none occurred. Never execute code merely to fill the schema.
教学代码用于说明，原始代码须归因论文/来源，复现代码尝试指定结果；三者均不自动等于独立科学重复验证。`passed` 须实际运行并通过所述检查，填写真实输出；`not-run` 的实际输出明确未观察，与预期分开；`failed` 记录真实错误/结果。步骤行号须存在，状态不得虚构执行；不能仅为填模式而运行代码。

## Handoff checks / 交接检查

Validate JSON shape/enums, unique ids, approved-version mapping, honest coverage, evidence endpoints, claim/example references, code line ranges, relative files and all slide links. Every relation's `from_slide` belongs to `from`, and `to_slide` belongs to `to`, including unresolved relations. Create truthful gap/appendix slides when needed, or defer the relation outside the final bundle until anchors exist; never insert dangling or global guessed slide ids. Mirror an approved relation in source `slides[].links` using target paper and slide ids with a status-aware label; an optional reverse link is navigation, not a new reverse scientific claim.
核查 JSON 结构/枚举、唯一 id、获批版本映射、真实覆盖、证据端点、主张/示例引用、代码行号、相对文件和全部幻灯片链接。每条关系的起点页属于 `from`，终点页属于 `to`，未解决关系也一样。必要时建立如实标缺口的附录页，或在存在锚点前暂不入最终包；不得悬空或猜测全局页 id。批准的关系在来源页链接中引用目标论文和页，用标签显示状态；可选反向链接仅为导航，不是反向科学主张。

Do not numerically rank papers or pool effects without demonstrated comparability of task, data/splits, metrics/direction, evaluation protocol, resources and uncertainty. Record comparability per relation with a reason; `not-assessed` is not comparable. Qualitative descriptions remain possible with explicit limits. Reading-priority advice is not a cross-paper performance leaderboard.
未证明任务、数据/划分、指标/方向、评测协议、资源与不确定性可比前，不得跨论文数值排名或合并效应；每条关系记录可比状态及理由，`not-assessed` 不等于可比。可提供带局限的定性描述；阅读优先级不是跨论文性能榜。

## Required scores and presentation / 必需评分与呈现
Every published collection card must show the analyst's numeric 1–4 score and preserve its evidence-backed rationale. No missing, null, deferred or placeholder score is accepted. Finish the substantive method, results and Related Work assessment before publication; do not score from metadata alone. Remaining visual or external-positioning gaps stay explicit under read_coverage/limits and never disappear because a score is required. A limited paper-based score is still numeric, with the scope of its basis stated.
每张已发布集合卡片必须展示分析师的 1–4 数值评分并保留证据理由；不接受缺失、空值、暂缓或占位评分。发布前完成方法、结果与相关工作的实质审查，不能仅按元数据评分。视觉或外部定位缺口保留在覆盖/局限中，不因必须评分而消失；有限的论文内判断也须给数值并注明依据范围。

The writer renders JSON, code and execution records inside labelled semantic pre/code windows with syntax highlighting and copy controls; copied content excludes line numbers/chrome. Autoplay is opt-in with 5s/15s/30s/1min per slide, pauses progression while dialogs/details or a hidden tab are active, and stops at the last slide. English requests require English narrative, examples, records and controls, not just translated headings.
writer 将 JSON、代码及执行记录放入带标签、语法高亮和复制按钮的语义 pre/code 窗口；复制不含行号/工具栏。自动播放须主动开启，每页可选5s/15s/30s/1min；目录/详情/隐藏页签期间暂停推进，末页停止。英文请求要求叙事、实例、记录与控件全英文，不仅翻译标题。

## Website locale layout / 网页语言目录
The language field is exactly zh-CN or en-US. Root index.html redirects single-locale builds with a visible fallback, or shows a bilingual chooser; all collection indexes and paper pages live under their locale directories (zh-CN/index.html, en-US/index.html, and locale/paper-id.html). Cross-paper links stay within the locale; language links target the sibling locale and retain the current slide anchor. Only these two locales are currently supported. Skill definitions and references remain Chinese/English paired documentation.
language 字段仅为 zh-CN 或 en-US。根index.html单语言跳转并保留备用入口，双语显示选择；所有集合与论文页面归入对应语言目录。跨论文导航保留在当前语言内，语言切换跳兄弟语言目录并保留当前页锚点。目前只支持上述两种语言，技能定义及参考文档保持中英文对照。

## Formula strings / 公式字符串
Author TeX in prose string values with `\(…\)`, `\[…\]` or `$$…$$`; escape backslashes normally when serializing JSON. KaTeX renders only prose, never code/records. A display expression must fit its card or be split into a dedicated slide; it is not raw HTML and must retain its source locator. Single-dollar prices remain literal. Actual PrismJS handles code colors without changing source text.
正文字符串使用上述TeX定界符，JSON按标准转义反斜线。KaTeX仅渲染正文，不渲染代码/记录；独立公式应适配卡片或单独成页，不允许原始HTML，并保留来源定位。单美元价格保持原样，真实PrismJS负责代码配色且不改源码。

## Locale-qualified bundle filenames / 按语言命名项目包
Name each generated bundle `project.<locale>.json`: `project.zh-CN.json` for Chinese and `project.en-US.json` for English. The suffix must agree with the bundle's language field. A single-language project still includes its locale in the filename; do not generate unqualified or shortened locale filenames.
每个生成项目包命名为上述完整地区语言格式，中文与英文分别使用对应文件名；后缀须与language字段一致。单语言项目也保留地区语言后缀，不生成无后缀或缩写语言名的项目文件。

Figure publication uses artwork-only src and one visible page-language caption. Keep original_caption as provenance, not a second visible caption; preserve all graphic labels, legends and table notes. Reader-facing text excludes production-process claims. The primary theme accent is RoyalBlue #4169e1.
图表发布使用仅图本体的src和一份页面语言可见图注；original_caption仅溯源不重复显示，图内标签/图例/表注保留。读者文字不含制作过程自述，主主题色为皇家蓝#4169e1。

## Figure placement and slide headings / 图表位置与页标题
Set figure_role=key to keep an essential figure with the main narrative (appendix=false); reference figures go to the trailing appendix. Keep one complete occurrence and shared references/return links, preserve original narrative ids, and never fabricate caption-only reading-point placeholders. Heading/browser title uses topic・verified publication/archive source; figure integrity, caption-once and white-surface rules remain.
关键图设key随主线（appendix=false），参考图归末尾附录；图唯一完整、引用回链共享、保留正文id，不造图注式占位页。顶部及页签为主题・核实出版/存档来源，完整图、单图注及白底规则保留。

When a verified conference or journal is known, set paper.publication_source to its concise venue/year label, e.g. ICLR 2026. Heading Source prefers this label; otherwise it falls back to the pinned arXiv id/version. Preserve the actual source_url and version for evidence provenance; a venue display label does not change the read version. Never invent acceptance or use preprint year as conference year.
已核实会议或期刊时，publication_source填写简短会议/期刊及年份，如ICLR 2026；标题来源优先用此标签，否则回退固定arXiv编号/版本。实际source_url与version仍保留已读证据版本，不因展示标签而改变；不编录用、不把预印本年当会议年。

Source priority is verified publication_source → verified archive_source → archive host/name plus the recorded identifier/version. Use exact brand casing (arXiv, bioRxiv, medRxiv, ChemRxiv, SSRN, OSF, Zenodo, etc.). archive_source supports any archive, not just arXiv; derive it from checked metadata and retain source_url/version. Do not invent identifiers, dates or versions; use the hostname plus recorded version when metadata is incomplete.
Source优先级为已核实publication_source→已核实archive_source→存档站点名/域名加已记录编号版本。品牌大小写保持准确，如arXiv、bioRxiv、medRxiv、ChemRxiv等。archive_source适用任意存档站点，按核实元数据填写并保留source_url/version；不编编号、日期或版本，信息不全时用域名和已有版本。

Both key narrative figures and reference appendix figures may include figure_notes (title/text/tone cards) and figure_layout (auto default; left/right/top/bottom/full). These fields stay with the selected unique figure target. Auto layout measures image ratio, available space and actual rendered notes/caption; explicit directions are preferences with fit fallback. A no-fit result is an unresolved layout failure to fix, not permission to clip content. Figure uniqueness, one caption and original artwork integrity remain mandatory.
主线重点图和附录参考图均可含figure_notes卡片及figure_layout默认auto/左右上下/全幅；同名字段随所选唯一图页。自动排版实测比例、空间、说明和图注，显式方向可回退；无可行版式是待修失败，不能裁切内容蒙混。图唯一、单图注及原图完整继续强制。

Adaptive left/right regions each require >=30% of total figure-layout width; top/bottom regions each require >=30% of height. A failing candidate must fall back or report no-fit; never shrink text, distort the artwork or hide notes. figure_notes stays with the figure in either narrative or appendix.
左右区域各至少整体布局宽度30%，上下各至少高度30%；不合格候选回退或报无可行版，不缩字/变形/藏说明。figure_notes随主线或附录图页。

## External authoring and PDF / 外部写作与PDF
The writer loads html-slides for reveal.js presentation authoring; the assembler validates/embeds assets and retains this v1 contract. Dependency resolution provenance does not prove execution of authoring instructions. crispe-slides-to-pdf consumes verified deck HTML and does not change research fields. Reveal owns slide navigation/scaling, while Prism and KaTeX retain independent default styles. Printed fragments are combined by default, with one logical slide per PDF page; overflow must be corrected before export.
writer加载外部技能进行Reveal写作，装配校验/内嵌且保留v1；解析来源不代表执行。PDF技能消费已验证HTML，不改研究字段；Reveal管导航缩放，Prism/KaTeX默认风格独立。打印默认合并步骤且一页一slide，导出前修溢出。
