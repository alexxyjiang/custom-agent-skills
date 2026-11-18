# Worked Examples, Teaching Functions, and Handoff / 具体示例、教学函数与交接

## Scope and evidence / 范围与证据

Activate only when the user requests examples, code/functions, or an orchestrator explicitly requests a structured handoff. A normal analysis keeps its existing behavior. Preserve all reading, scoring, optional-section dependencies, companion checks, and application-verdict rules in SKILL.md and skill-collaboration.md. Examples illustrate mechanisms; they do not establish impact, adoption, or a PoC verdict.

仅在用户请求示例、代码/函数，或编排器明确要求结构化交接时启用。普通分析维持原有行为。保留 SKILL.md 与 skill-collaboration.md 的全文阅读、评分、可选节依赖、协作检查及应用判断规则。示例解释机制，不能证明影响、采用或 PoC 结论。

The orchestrator owns the approved named paper set and source/read/compute budget. Reuse its IDs, versions, evidence and output paths; approval for that set needs no repeated question. Neither a handoff nor an example expands that set, follows citations automatically, or authorizes extra full texts, cloning, installs, paid LLM calls or experiment runs. Return gaps to the orchestrator; name any proposed additional source for approval before access.

编排器控制已批准的具名论文集合及来源/阅读/计算预算。复用其编号、版本、证据与输出路径；集合已获批无需重复询问。交接或示例均不能扩大集合、自动追踪引用，或授权额外全文、克隆、安装、付费 LLM 调用及实验运行。缺口返回编排器；新增来源先点名获批再访问。

Full-PDF reading remains the requirement. If the PDF is unavailable, identify the exact available HTML/version and disclose that fallback and every read gap; do not silently substitute abstract/metadata for full reading. Unread figures, tables, equations, or appendices keep coverage `partial` even if all HTML text was read. Metadata-only access is `metadata-only`, never grounds for a 1–4 score or a full-read claim. For collection publication a numeric 1–4 score and evidence-backed rationale are mandatory: complete substantive Method, Results and Related Work appraisal, then state any limits on that paper-based judgment separately. Remaining visual gaps do not become a deferred/placeholder score or a false full-read claim.

完整阅读 PDF 的要求不变。PDF 不可用时，明确可用 HTML 及版本，披露替代方式和所有未读部分；不能用摘要/元数据悄然替代全文。即使读完 HTML 文字，若图、表、公式或附录未读，覆盖仍为 `partial`。仅元数据标为 `metadata-only`，不能据此给 1–4 分或宣称读完。集合发布必须有 1–4 数值评分和证据理由：先完成方法、结果及相关工作的实质审查，论文内判断的局限另列。剩余视觉缺口不能替代为暂缓/占位评分，也不能伪装成完整阅读。

## Build the explanation / 构建讲解

For each selected mechanism, follow this chain in the report language (bilingual only when requested):

每个选定机制按以下链条展开，使用报告语言（仅用户要求时双语）：

1. **Mechanism → source:** explain the actual operation and assumptions, with a verified page/section/equation/algorithm locator and versioned source URL.
   **机制 → 来源：**解释实际操作及假设，给出核实的页/节/公式/算法定位和带版本来源 URL。
2. **Concrete worked example:** choose tiny explicit inputs and calculate intermediate states before showing code. Explain why this input exposes the mechanism rather than a generic surrounding API.
   **具体算例：**选取极小、明确的输入，先算中间状态再展示代码；说明它如何揭示机制，而非只演示外围 API。
3. **Teaching function:** provide a complete minimal runnable function, sample call, input/output types, dependencies with versions where needed, and exact run command. Prefer standard-library code when it faithfully teaches the operation; label omitted model/data/training components.
   **教学函数：**提供完整最小可运行函数、样例调用、输入输出类型、依赖（必要时版本）及精确运行命令。能忠实解释操作时优先标准库；标明省略的模型/数据/训练组件。
4. **Trace:** map 1-based code line numbers to intermediate state and explain why each change follows from the mechanism. Line numbers refer to the exact `code` string or displayed code block, excluding Markdown fences; keep numbering synchronized after edits.
   **追踪：**将从 1 开始的代码行号对应到中间状态，解释变化为何符合机制。行号以实际 `code` 字符串或代码块为准，不含 Markdown 围栏；修改后同步。
5. **Result and limits:** separate expected output from captured actual output, execution status and limitations. State what the example proves and what it cannot test; connect back to the paper without extrapolating toy behavior to measured gains.
   **结果与局限：**分开列预期输出、实际捕获输出、执行状态和限制。说明示例证明了什么、不能验证什么；回扣论文，但不能把玩具行为外推成实测收益。

Label every example `original` (verified author-provided code, with provenance/license and any edits), `teaching` (analyst-authored simplification), or `reproduction` (attempt to implement and evaluate the paper under stated conditions). Reproduction is a scope label, not a success claim; only actual comparable runs support reproduced results. Do not blindly translate a paper's buggy pseudocode: check invariants and edge cases, document the original issue, the exact correction and its effect, and distinguish a correction from an unverified interpretation. Keep source text/code and analyst changes distinguishable.

每个示例标为 `original`（核实的作者代码，附来源/许可及修改）、`teaching`（分析者编写的简化实现）或 `reproduction`（在声明条件下尝试实现并评测论文）。复现标签表示范围，不表示成功；只有真实且可比的运行才能支持复现结果。不能盲译论文中有错误的伪代码：检查不变量和边界情况，记录原问题、精确修正及影响，区分修正与未经验证的解释，并分清来源代码和分析者修改。

## Execution and semantic checks / 执行与语义检查

Use `execution: not-run` and `actual_output: "not observed; not run"` if execution was not performed; record why (missing dependencies/data/tools, permission or budget). Expected output is a prediction, not a measurement. `passed` requires captured output matching the expectation and meaningful semantic checks; `failed` records the real error or mismatch in `actual_output`, with the failing input and limitations. Never replace a failed run with the expected output. Do not invent LLM responses, accuracy, latency, token costs, benchmark scores or reproduction metrics; a stub/mock must be labeled and cannot validate the real model.

未执行时使用 `execution: not-run`、`actual_output: "not observed; not run"`，说明依赖/数据/工具、权限或预算原因。预期输出是预测，不是测量。`passed` 需捕获输出匹配预期且通过有意义的语义检查；`failed` 在 `actual_output` 保留真实错误或差异，并记录失败输入与局限。不能用预期输出替换失败结果。禁止编造 LLM 响应、准确率、延迟、token 成本、基准分或复现指标；桩/mock 必须标记且不能验证真实模型。

Check behavior, not just syntax or self-confirming assertions: manually derive one nontrivial result; exercise an empty/no-match case, a boundary/tie, an invalid input, and exhaustion of the mechanism's budget. Check relevant invariants (e.g. selection stays within the visited prefix and top-k, scores use the stated rule, ties are deterministic). For stochastic/model code, report seed, model/data/version, tolerance and uncertainty where actually available. A teaching smoke check is not independent reproduction.

检查行为而非只查语法或自证断言：手算一个非平凡结果，覆盖空/无匹配、边界/并列、非法输入及机制预算耗尽。检查相关不变量（如选择不超已访问前缀和 top-k、评分符合声明规则、并列确定性）。随机/模型代码仅报告实际已知的种子、模型/数据/版本、容差及不确定性。教学冒烟检查不等于独立复现。

Handle missing inputs, dependency/runtime errors, timeouts and budget exhaustion explicitly. Bound retries, input size, retrieval steps and output size as appropriate; return the partial state and stop reason rather than silently increasing budgets. If safe authorized execution is unavailable, provide runnable instructions with `not-run` instead of installing or provisioning implicitly.

明确处理输入缺失、依赖/运行错误、超时及预算耗尽。按需限制重试、输入规模、检索步数和输出规模；返回部分状态与停止原因，不悄然提高预算。无法在授权范围运行时提供可运行说明并标记 `not-run`，不隐式安装或配置环境。

## Report placement / 报告位置

Preserve the existing sections 1–5, their selection rules and fixed relative order. Only when examples/functions are requested, append an examples section after all included existing sections, using the next sequential number without gaps (6 if all five are present; 3 if only the required two are present). An orchestrator handoff alone does not force a human-facing examples section. Put the machine artifact in a sidecar at the agreed path and link it; do not insert its schema into or reorder the report. The later writer owns slide authoring; the analyst supplies evidence and traces, not slides.

保留现有 1–5 节及选用规则和固定相对顺序。仅请求示例/函数时，在实际保留的原有章节之后追加示例节，使用连续的下一个编号、不留空号（五节齐全为 6，仅必需两节为 3）。单纯编排器交接不强制添加面向读者的示例节。机器产物按约定路径另存 sidecar 并链接，不把 schema 塞进报告或调整其顺序。后续 writer 负责幻灯片创作；分析者提供证据与追踪，不代写 slides。

## Sidecar contract / Sidecar 契约

Emit JSON with exactly the following contract, using `schema_version: 1` and a `papers` array in approved-set order. Include all listed fields; use empty arrays for absent claims/examples, and explicit unknown/not-observed strings for unavailable scalar evidence rather than invented values. A paper's `id` must be a unique safe slug matching `[a-z0-9]+(?:-[a-z0-9]+)*`, never a title-derived path with slashes. Preserve the authoritative identifier in `version`/source metadata as appropriate; confirm collisions with the orchestrator. Never add unapproved papers merely to fill the array.

输出 JSON，使用以下确切契约、`schema_version: 1` 和按批准集合顺序排列的 `papers` 数组。所有列出的字段均保留；无主张/示例用空数组，确实不可得的标量证据用明确的未知/未观察字符串，不编造。论文 `id` 为唯一安全 slug，匹配 `[a-z0-9]+(?:-[a-z0-9]+)*`，不能把带斜线的标题当路径。按实际情况在 `version`/来源元数据中保留权威标识；冲突与编排器确认。不能为填满数组加入未批准论文。

| Object / 对象 | Fields and types / 字段与类型 |
|---|---|
| root / 根 | `schema_version`: integer `1`; `papers`: array of paper objects / 论文对象数组 |
| paper / 论文 | `id`: safe slug string / 安全标识字符串; `title`: string / 字符串; `source_url`: versioned URL string / 带版本 URL; `version`: string / 版本字符串; `topic`: string / 主题; `summary`: string / 摘要; `score`: {`value`: integer 1–4, `rationale`: string, `claim_ids`: nonempty evidence-id array} / 必需数值评分及证据; `read_coverage`: coverage object / 覆盖对象; `report_path`: string / 报告路径; `claims`: claim array / 主张数组; `examples`: example array / 示例数组 |
| read_coverage / 阅读覆盖 | `status`: `full-text` / `partial` / `metadata-only`; `read`: string array of actually read locators / 已读定位字符串数组; `unread`: string array of gaps / 未读缺口字符串数组 |
| claim / 主张 | `id`: unique string within paper / 论文内唯一字符串; `text`: string / 文本; `locator`: string / 定位; `url`: exact source URL string / 精确来源 URL; `kind`: `paper-claim` / `external-evidence` / `analyst-inference`; `limits`: string / 局限 |
| example / 示例 | `id`: unique string within paper / 论文内唯一字符串; `kind`: `teaching` / `original` / `reproduction`; `source_locator`: string / 来源定位; `code`: complete code string / 完整代码字符串; `language`: string / 编程语言; `run_command`: string / 运行命令; `expected_output`: string / 预期输出; `actual_output`: captured string or explicit not-observed string / 实际捕获或明确未观察字符串; `execution`: `passed` / `not-run` / `failed`; `limitations`: string / 局限; `steps`: step array / 步骤数组 |
| step / 步骤 | `lines`: array of 1-based integer line numbers within `code` / `code` 内从 1 开始的整数行号数组; `explanation`: string / 解释; `state`: explanatory string of intermediate values / 中间值解释字符串 |

Use the exact read version in `source_url` (e.g. an arXiv URL ending in the verified `vN`) and `version`; do not guess a version suffix. If no versioned URL is available, do not emit a final bundle; keep the unresolved URL in an interim report, disclose the available unversioned/local source in `read_coverage.read` and the gap in `unread`, and return the unresolved version to the orchestrator. Unknown identity/version is not permission to fabricate one. Claim URLs point to their own evidence, not automatically to the target paper. Keep provenance and read gaps consistent with the report. For a generic teaching illustration, use `source_locator: "generic illustration; no paper source"` and explicitly state that it is not derived from this paper; never invent a section number.

`source_url` 和 `version` 必须对应实际阅读版本（如以核实的 `vN` 结尾的 arXiv URL），不能猜版本。没有带版本 URL 时不交最终项目包，在阶段报告记录未解决 URL，在 `read_coverage.read` 说明可用的无版本/本地来源，在 `unread` 记录缺口，并向编排器返回未解决版本。身份/版本未知不能成为编造理由。主张 URL 指向各自证据，不能一律指向目标论文。来源与阅读缺口应和报告一致。通用教学示例使用 `source_locator: "generic illustration; no paper source"`，明确不源自该论文，不能编造节号。

## Generic bounded retrieval illustration / 通用有界检索示例

This standalone `teaching` illustration has no paper source (`source_locator: "generic illustration; no paper source"`); it is not an implementation of any claimed paper algorithm. It demonstrates a visit budget, lexical overlap, deterministic ranking and top-k truncation, not embeddings or LLM generation. Input types: `query: str`, `docs: list[str]`, `k: int`, `budget: int`; output: `list[tuple[int, int]]` of zero-based document index and overlap score. Dependencies: Python 3 standard library only. Save the exact block as `bounded_retrieve.py`; run `python3 bounded_retrieve.py`.

此独立 `teaching` 示例无论文来源（`source_locator: "generic illustration; no paper source"`），不是任何论文算法的实现。演示访问预算、词项重合、确定性排序和 top-k 截断，不含嵌入或 LLM 生成。输入类型为 `query: str`、`docs: list[str]`、`k: int`、`budget: int`；输出为零基文档下标与重合分数的 `list[tuple[int, int]]`。仅依赖 Python 3 标准库。将代码块原样保存为 `bounded_retrieve.py`，运行 `python3 bounded_retrieve.py`。

```python
def bounded_retrieve(query, docs, k, budget):
    if type(k) is not int or type(budget) is not int or min(k, budget) < 0:
        raise ValueError("k and budget must be nonnegative integers")
    terms = set(query.lower().split())
    ranked = []
    for index, text in enumerate(docs[:budget]):
        score = len(terms & set(text.lower().split()))
        if score:
            ranked.append((index, score))
    ranked.sort(key=lambda item: (-item[1], item[0]))
    return ranked[:k]


docs = ["red blue", "red", "red blue green"]
print(bounded_retrieve("red blue green", docs, k=1, budget=2))
```

Worked calculation: query terms are `{red, blue, green}`. Budget 2 admits only documents 0 and 1, with scores 2 and 1. Document 2 would score 3 but is never visited. Sorting gives `[(0, 2), (1, 1)]`; top-1 returns `[(0, 2)]`. The budget constrains visited documents, not total input bytes or ranking complexity; this is a teaching simplification, not a production resource guarantee.

手算：查询词集合为 `{red, blue, green}`。预算 2 仅允许访问文档 0、1，得分分别为 2、1。文档 2 虽可得 3 分但未访问。排序得到 `[(0, 2), (1, 1)]`，top-1 返回 `[(0, 2)]`。预算限制访问文档数，不限制总输入字节或排序复杂度；这是教学简化，不是生产资源保证。

| Lines / 行号 | Explanation / 解释 | State / 状态 |
|---|---|---|
| 2–4 | Validate limits and tokenize / 校验上限并分词 | `terms = {red, blue, green}` |
| 6–9 | Visit the first two docs only / 仅访问前两条 | `ranked = [(0, 2), (1, 1)]` |
| 10–11 | Sort, then truncate / 排序后截断 | result / 结果 `[(0, 2)]` |
| 14–15 | Explicit sample input and call / 明确样例输入和调用 | `k = 1`, `budget = 2` |

Expected stdout is exactly `[(0, 2)]` followed by a newline. Before running, record `execution: not-run`, `actual_output: "not observed; not run"`; after actually running, replace these only with captured output and the resulting status. Useful semantic checks: budget 3 selects `(2, 3)`; budget 0 or k 0 returns `[]`; empty/no-match inputs return `[]`; tied scores favor the lower index; duplicate tokens do not inflate set overlap; negative/noninteger limits raise `ValueError`. These checks distinguish this mechanism from unrestricted search, token counting, or unstable tie-breaking. No model quality, latency or paper result follows from this example.

预期 stdout 精确为 `[(0, 2)]` 加换行。运行前记录 `execution: not-run`、`actual_output: "not observed; not run"`；真正运行后才以捕获输出及对应状态替换。有效语义检查：预算 3 选中 `(2, 3)`；预算 0 或 k 为 0 返回 `[]`；空/无匹配输入返回 `[]`；并列取较小下标；重复 token 不增加集合重合分；负数/非整数上限抛 `ValueError`。这些检查可区分此机制与无限检索、词频计数或不稳定并列处理。不能从该例推出模型质量、延迟或论文结果。

The analyst sidecar is a partial handoff, merged into the orchestrator's existing project; it is not itself a complete builder input. The orchestrator adds scope, relations, and writer-authored slides. Contract strings (`actual_output`, `state`, `limits`) remain strings even when unknown. Generic examples must not be presented as evidence for a specific paper.
分析师 sidecar 是合并到编排器项目的部分交接，不是可直接构建的完整项目；编排器添加 scope、relations 和 writer 编写的 slides。actual_output、state、limits 即使未知也保持字符串。通用示例不得作为特定论文的证据。

## Figure handoff / 图表交接
For every figure/table invoked by the analysis or used to explain evidence, include its original-asset entry in the writer handoff so the corresponding slide can show and explain it directly without sending readers back to the paper: pinned version, figure/table number, physical PDF page, caption, relevant claim, extraction/crop coordinates if known, and actual visual-read status. Reuse the target PDF; request no unrelated full text. Preserve original labels and data, distinguish original artwork/crop from teaching redrawing, and direct extraction to the writer's paper-figures reference. A successful image extraction does not establish a completed visual read.
分析中提及或用于说明证据的每个图表，都给writer交接原图信息，使对应slide直接展示并讲解，不让读者返回论文横跳：固定版本、图表号、物理页、图注、关联主张、已知提取/裁图坐标及真实视觉阅读状态。复用目标PDF，不取无关全文；保留原始标签和数据，区分原图/裁图与教学重绘，提取按writer原图参考执行。提取成功不等于视觉阅读完成。

Figure handoffs must include the complete original caption, not only a translated summary or figure number. Inventory every body figure/table referenced by slides. Direct embedding is valid; local screenshots are optional, but artwork, caption lines, panel labels and notes must remain complete.
图表交接包含完整原文图注，不能仅译文摘要或图号；清点slides引用的全部正文图表。允许直接嵌入，截图可选，但图表、图注全部行、面板标签及注释须完整。

For slide publication, deliver artwork-only images with complete labels/panels/notes and preserve the original caption separately as provenance. The writer displays one page-language caption, preserving full original caption text only in provenance rather than a second visible caption. Do not include production-process statements in reader-facing explanations.
发布交接提供图表本体，保留完整标签/面板/表注，原图注另存溯源。writer仅展示页面语言的一份图注，完整原图注存溯源而非第二份可见文字；面向读者的解释不写制作过程自述。
