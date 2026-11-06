# DEEP-MODE / 深度知识验证

系统性深读，生成模块能力、设计逻辑、数据结构、状态流和修改指南 skill；证据核查题库、累积闭卷回归和独立终考只验证记录版本的抽样知识。
Systematically read modules and generate capability, design, data/state and modification skills; evidence-checked cumulative regression and independent holdout verify sampled knowledge for the recorded source version.

## 用法与职责 / Usage and Roles

```text
/crispe-system-architect Deep <source>
```

`<source>` 为本地路径或 GitHub URL；`{output-dir}` 必须确认，遵循 [部署规则 / Deployment](./DEPLOYMENT.md)。
`<source>` is a local path or GitHub URL; confirm `{output-dir}` under Deployment rules, never silently choose it.

按以下七阶段执行，逐模块分别跟踪阅读、编写、验证进度。Reader 分析；Author 独占模块／支持／索引 skill 编写与修复；Coordinator 核查证据、维护题库、评分和发布。
Follow the seven phases in order, tracking reading, authoring and verification separately per module. Reader analyzes; Author alone writes/repairs module, support and index skills; Coordinator checks evidence, maintains banks, grades and publishes.

使用宿主原生技能编写指南；不可用时使用本流程模板：有效 YAML `name` / `description`、聚焦正文和相对支持链接。默认 CRISPE，模块与索引均适用。
Use native skill-authoring guidance when available; otherwise use the workflow templates: valid YAML `name` / `description`, focused body and relative support links. Default to CRISPE for modules and index alike.

## 阶段 1：准备 / Phase 1: Prepare

遵循 [来源版本 / Source Version](./SOURCE-VERSION.md)、Deployment 和 [主文件通用规则 / Shared Rules](./SKILL.md)：检查仓库，规范项目名，推荐并单独确认 ref，记录完整 commit、采集时间、来源身份与输出位置。
Follow Source Version, Deployment and Shared Rules: inspect the repository, normalize project name, recommend/independently confirm ref, and record full commit, capture timestamp, source identity and output locations.

URL 克隆位置先确认，不放入生成 skill 目录，不盲目复用未知 checkout；本地工作树只读。未提交 Code / Doc / Config / Other 逐类独立确认，以 SHA-256 清单冻结批准覆盖和删除。
Confirm URL checkout location before cloning, outside generated skill directories; inspect unknown checkouts before reuse. Keep local worktrees read-only; independently confirm dirty Code / Doc / Config / Other and freeze approved overlays/deletions with SHA-256 manifests.

每次确认实际项目 skill 目录，推荐 `.agent/skills/`；默认部署 1 全部项目级，显式部署 2 仅 DR 索引置于 `~/.agent/skills/`。确认前不写入。
Confirm actual project skill storage each run; recommend `.agent/skills/`. Default deployment 1 is all-project; explicit deployment 2 globalizes only the DR index in `~/.agent/skills/`. Wait before writing.

Mix 复用 Quick 前锁定的来源，来源／范围／目标不变则不重问；若 Deep 目标尚未确认，在开始 Deep 前确认。
Mix reuses the identity locked before Quick; re-ask only on source/scope/destination changes. Confirm any unresolved Deep destination before starting Deep.

## 阶段 2：扫描与选择 / Phase 2: Scan and Select

复用主文件共享扫描与 [Reader 模块规则 / Reader Scope](./AGENT-READER.md)；Mix 先完成 Quick，再复用映射／证据并补齐边界。按构建、包、导入与实际职责识别源码模块，跳过依赖／构建／生成噪声。
Reuse main-file shared scanning and Reader scope rules; finish Quick first in Mix, then reuse maps/evidence and supplement boundaries. Identify code modules by build/package/import/responsibility boundaries, skipping dependency/build/generated noise.

独立 Config / Doc 目录单列 `config` / `doc`，不因支持代码而合并。展示稳定 ID／名称、种类（`code` / `config` / `doc`）、实际路径、用途和依赖。
List independent Config/Doc directories separately as `config`/`doc`, even when supporting code. Show stable ID/name, kind (`code`/`config`/`doc`), actual path, purpose and dependencies.

默认全选，问：“默认已选中所有模块。请确认全部，或指定纳入／排除模块。”等待明确确认；记录精确选中／排除表，为每个选中模块创建 Deep 任务。
Default to all; ask: “All modules are selected by default. Confirm all, or specify modules to include/exclude.” Wait for confirmation; silence is not permission. Record exact selection/exclusions and create one Deep task per selected module.

未选模块不完整阅读／编写／考试，只可读取确立选中事实所需的有限跨边界上下文，并标注非 Deep 覆盖。Mix Quick 可覆盖全仓，DR 索引须注明排除范围。
Excluded modules skip full reading/authoring/exams; narrowly read collaborators only as necessary context for selected facts, not Deep coverage. Mix Quick may cover the whole repo; disclose exclusions in the DR index.

Config 覆盖键／默认值、加载／覆盖优先级、依赖、验证／错误与具体修改；Doc 覆盖范围、导航、契约、源码／指南一致性与维护修改。不适用代码维度显式标注，不虚构 API／状态机；所有选中种类执行同样的源码闭卷验证。
Config covers keys/defaults, load/override precedence, dependencies, validation/errors and changes; Doc covers scope, navigation, contracts, source/guide consistency and maintenance. Mark inapplicable code dimensions; invent no APIs/state machines. Apply identical source-backed exams to every selected kind.

## 阶段 3：阅读与私有候选 / Phase 3: Read and Author Private Candidates

按来源规则读取 `{source-sha}` Git 对象及批准的不可变快照／清单，绝不混用版本；调度 Reader 按其完整 Deep 规则读取所选模块全部文件并提供精确证据，核查 Mix 复用论断。
Read Git objects at `{source-sha}` plus approved immutable snapshots/manifests under source rules; never mix versions. Dispatch Reader to read every selected-module file under its full Deep rules, supply exact evidence and check reused Mix claims.

流水线／作业模块须传入 [Quick 流水线规范 / Pipeline Profile](./QUICK-MODE.md) 的实际内容，而非未解析的相对路径。
For pipeline/job modules, supply the actual Quick pipeline profile content, not an unresolved relative path.

Author 写入前打印并确认实际模块／索引文件清单（路径、文件内双语、角色、必选／可选、部署目标）。调度 [Author](./AGENT-SKILL-AUTHOR.md)，提供 Reader 交接、来源身份和私有候选目录。
Before Author writes, print/confirm actual module/index inventory (paths, in-file languages, roles, required/optional files, deployment). Dispatch Author with Reader handoff, source identity and private candidate directory.

显式传递全部变量 / Pass all variables explicitly:
`{source-dir}`, `{module-dir}`, `{module-name}`, `{project-name}`, `{ref}`, `{source-sha}`, `{source-identity}`, `{source-manifest}`, `{snapshot-dir}`, `{handoff-dir}`, `{output-dir}`, `{candidate-output-dir}`.

Reader `{mode}` = `Deep`；`{quick-handoff}` 为具体 Mix 交接路径，非 Mix 显式为空。`{candidate-output-dir}` 是所有发现根目录外的私有运行目录。
Reader `{mode}` = `Deep`; `{quick-handoff}` is the concrete Mix handoff path, explicitly empty otherwise. Resolve `{candidate-output-dir}` to a private run directory outside all discovery roots.

检查 `{candidate-output-dir}/{project-name}-dr-{module-name}/SKILL.md`、元数据与链接；候选验证前不发布，不编辑现有部署版。原始阅读交接留在发布目录外。
Check `{candidate-output-dir}/{project-name}-dr-{module-name}/SKILL.md`, metadata and links; keep candidates private until verified and do not edit deployed versions. Keep raw reading handoffs outside published directories.

## 阶段 4：有界闭卷验证 / Phase 4: Bounded Closed-Book Verification

每模块最多 **3 轮**（包括初始候选）；每轮先跑完整累积回归，通过后对同一冻结候选跑全新独立终考。
Allow at most **3 rounds per module**, including the initial candidate; each round runs full cumulative regression, then a fresh independent holdout on the same frozen candidate only after regression passes.

### 4A：来源、记录与隔离 / Source, Records and Isolation

记录 Reader / Author / Questioner 一致的来源身份及批准覆盖；验证期间身份改变即停止，基于一致新版本重新生成，旧评分不可复用。
Record the same source identity and approved overlays for Reader/Author/Questioner; stop on identity changes, regenerate consistently and do not reuse old grades.

记录位于确认的私有 `{verification-dir}/{project-name}/{run-id}/{module-name}/`，在所有生成／发布 skill 根目录外，`{run-id}` 唯一；保存题 ID、核查键／证据、拒题原因、Verifier 答案、评分理由、轮次和全部候选哈希。答案键不发布。
Use confirmed private `{verification-dir}/{project-name}/{run-id}/{module-name}/` outside all generated/published skill roots, with unique `{run-id}`; retain IDs, validated keys/evidence, rejected questions/reasons, Verifier answers, grading decisions, rounds and all candidate hashes. Never publish keys.

Questioner / Verifier 使用无继承对话、源码摘录、答案键或旧答案的新上下文。Questioner 只获允许的源码与题目避重输入；Verifier 仅获候选文件和 question-only 输入。
Start Questioner/Verifier in fresh contexts without inherited conversation, source excerpts, keys or earlier answers. Questioner receives allowed source/question-deduplication inputs; Verifier receives only candidate files and question-only input.

隔离记录为 `enforced`（限定读取）、`observed`（完整工具／读取日志核查）或 `prompt_only`（仅提示，无独立访问核查）。任何观察到的越界读取均为污染。
Record isolation as `enforced` (scoped reads), `observed` (complete tool/read logs checked) or `prompt_only` (instructions without independently checkable access). Any observed out-of-scope read is contamination.

两智能体均可返回阻塞格式 / Either agent may return this blocker instead of normal output:
`{"status":"blocked","reason":"context_contamination|source_unavailable","detail":"..."}`.

污染允许在新上下文重试 **1 次**，再发生即 `blocked`；源码不可用直接停止模块验证。阻塞响应不评分，也不计格式错误答案。
Retry contamination **once** in a fresh context, then stop `blocked` on recurrence. Source-unavailable blockers stop module verification immediately. Never grade blockers or treat them as malformed answers.

每轮冻结每个 skill／支持文件 SHA-256，两次考试后均核查；任何编辑使本轮结果失效，按 4E 在下一轮测试修改版。
Freeze SHA-256 hashes of every skill/support file each round and check after both exams; any edit invalidates that round and follows 4E for testing the changed candidate next round.

### 4B：累积题库与证据核查 / Cumulative Bank and Evidence Validation

调度 [Questioner](./AGENT-QUESTIONER.md)，模型须能准确追踪模块源码，按已展示准确度选择成本。
Dispatch Questioner with a model capable of accurate module tracing; choose cost based on demonstrated accuracy.

显式输入 / Explicit inputs: `{source-dir}`, `{module-dir}`, `{module-name}`, `{source-sha}`, `{source-identity}`, `{source-manifest}`, `{snapshot-dir}`; `{mode}` = `regression`.
`{previous_questions}` 为所有先前问题仅含 `id` / `question` 的 JSON 对象；首轮 `[]` / JSON objects containing only `id`/`question` for all prior questions; `[]` initially.

Questioner 返回 `verification` / `recommended` 数组；Coordinator 分配稳定新 ID，保留推荐题供验收。首轮 **5–8** 题，后续每轮新增 **3–5** 题。
Questioner returns `verification`/`recommended` arrays; Coordinator assigns stable new IDs and retains recommendations for acceptance. Generate **5–8 initial questions**, then **3–5 additions** per later round.

保留所有先前有效题，包括通过／失败的终考题；新增只扩充，绝不替换题库。不得为通过而删除旧失败题。
Retain every previously validated question, including passing/failed holdout questions; new output extends, never replaces the bank. Never remove an earlier failed question to obtain a pass.

Coordinator 接纳前读取同一 Git／快照的引用范围、相关条件／调用点，核查每个 `required_facts` 和 `answer_key` 与 `{source-identity}`；评分前解决语义歧义并核实推断设计意图。
Before admission, Coordinator reads cited ranges and relevant conditions/call sites from the same Git/snapshot, checks every `required_facts` and `answer_key` against `{source-identity}`, and resolves ambiguity/inferred intent before grading.

错误键仅凭源码纠正并留记录；无效题记录原因，请求替代以满足本轮题数，最多 **1 次替代请求**，仍无效即 `blocked`。无效题不是技能失败；替代题用新 ID，保留拒题 ID／原因。
Correct wrong keys only from source evidence and record it; reject invalid questions with reasons and request replacements to meet round counts, at most **one replacement request**, then `blocked` if still invalid. Invalid questions are not skill failures; replacements get new IDs while rejected IDs/reasons remain.

任何题目／键纠正都使其旧评分失效；决定考试结果前让 Verifier 重新回答改动题。
Any question/key correction invalidates its prior grade; have Verifier answer changed questions afresh before deciding the exam result.

### 4C：完整回答与评分 / Complete Answers and Grading

新上下文调度 [Verifier](./AGENT-VERIFIER.md)：`{skill-dir}` = `{candidate-output-dir}/{project-name}-dr-{module-name}/`，提供 `{module-name}` 和 `{questions}`。
Dispatch a fresh Verifier with `{skill-dir}` = `{candidate-output-dir}/{project-name}-dr-{module-name}/`, `{module-name}` and `{questions}`.

`{questions}` 为整个有效回归题库投影，每项恰好只有 `id` / `question`。`answer_key`、`required_facts`、源码证据、评分说明和旧答案由 Coordinator 私藏。
Project the entire validated regression bank into `{questions}`, each item containing exactly `id`/`question`. Keep `answer_key`, `required_facts`, source evidence, grading notes and prior answers private to Coordinator.

每个输入 ID 恰好一个答案；缺失／重复／未知 ID 为无效响应，允许新上下文 **1 次格式重试**，仍错误即 `blocked`，不可算通过。
Require exactly one answer per supplied ID; missing/duplicate/unknown IDs invalidate the response. Allow **one format retry** in a fresh context, then `blocked` if still malformed; never count it as a pass.

Coordinator 对照核查事实并验证技能引用，记录覆盖／缺失／矛盾及理由；语义评分必须有依据，关键词命中不够。
Coordinator compares checked facts and verifies skill citations, recording coverage, omissions, contradictions and reasons; semantic grading needs reasoned support, not keywords alone.

- **PASS：**全部必需事实有候选支持，答案无实质错误／矛盾。 / All required facts are candidate-supported, with no materially incorrect/contradictory answer claims.
- **FAIL：**缺事实、违背源码、实质虚假论断、无技能证据或 `CANNOT_ANSWER`。 / Missing required facts, source contradictions, materially false claims, missing skill evidence or `CANNOT_ANSWER`.
- **DISPUTED：**题／键歧义或源码支持不足；先按 4B 有界纠正／替代，未解决则阻塞。 / Ambiguous question/key or inadequate source support; resolve through bounded 4B correction/replacement before scoring, otherwise block.

回归／终考分别报告 `passed / all valid questions`；空考试不通过；无效、替代、争议题均在记录中可见。
Report `passed / all valid questions` separately for regression/holdout; empty exams cannot pass. Keep invalid, replaced and disputed questions visible in records.

### 4D：独立终考 / Independent Holdout

仅完整回归通过后，冻结同一候选，调度 **新 Questioner**，`{mode}` = `holdout`；提供 4B 源码范围／身份变量和仅为避重的 `{previous_questions}` ID／文本。
Only after full regression passes, retain the same frozen candidate and dispatch a **new Questioner**, `{mode}` = `holdout`, with 4B source scope/identity variables and `{previous_questions}` IDs/text solely to avoid overlap.

Questioner 不接触候选、Quick 文档、旧键／答案／分数／修复反馈；生成 **5–8** 个实用新题：机制、限制、失败条件、模式／API 适用时机。改写旧题或同一事实换措辞不算新案例。
Keep candidate skills, Quick docs, earlier keys/answers/scores/repair feedback out of Questioner's context; generate **5–8** useful new questions on mechanisms, limits, failure conditions and pattern/API applicability. Rewording a question or the same required fact is not a new case.

Coordinator 核查键与重叠，再让新 Verifier 按 4B–4C 回答／评分（同样替代／格式／污染上限）。终考题／键在评分完成前不交给 Author。
Coordinator validates keys and overlap, then a fresh Verifier answers/is graded under 4B–4C with the same replacement/format/contamination bounds. Hide holdout questions/keys from Author until grading completes.

### 4E：结果与修复边界 / Results and Repair Bounds

- 全回归／终考通过且哈希不变：`enforced` / `observed` 标 `verified`；`prompt_only` 标 `partial_validated`，说明闭卷隔离无法独立核查。记录来源、候选、两项分数和主题，非穷尽覆盖证明。
  All regression/holdout pass with unchanged hashes: `verified` for `enforced`/`observed`; `partial_validated` for `prompt_only`, explicitly reporting unchecked isolation. Record source/candidate identities, both scores and topics; this is sampled verification, not exhaustive proof.
- 任一有效题失败：候选未验证；尝试过终考则将**整个有效终考**追加回归。轮次 < 3 时，Reader 收失败题、核查证据／键和 Verifier 答案来核实补充；Author 仅据核查修复交接修订。
  Any valid failure leaves the candidate unverified; append the **entire validated holdout** if attempted. Below round 3, Reader checks/supplements failed questions, checked evidence/keys and Verifier answers; Author revises from the checked repair handoff.
- 下一轮重跑**完整题库**，通过后用**新终考**；第 3 轮失败直接 `needs_review`，不再调度修复。
  Next round reruns the **complete bank**, then a **new holdout** after passing; round-3 failures go directly to `needs_review`, without another repair dispatch.
- 第 3 轮前候选编辑：丢弃本轮评分，保留被丢弃考试全部有效题为回归材料，下一轮测试改动候选。
  Candidate edits before round 3 discard that round's grades, retain every validated question from discarded exams as regression material and test the changed candidate next round.
- 第 3 轮失败／编辑：`needs_review`，展示缺口与分数并停止。已向 Author 暴露的终考不再作为独立验收证据；**绝不自动重启三轮循环**。
  Round-3 failures/edits: `needs_review`, report gaps/scores and stop. Never reuse Author-exposed holdout as independent acceptance evidence or **automatically reset the three-round cycle**.

## 阶段 5：精确发布与索引 / Phase 5: Exact Publication and Index

仅全部选中模块 `verified` 后，Coordinator 发布精确冻结清单。先核实冲突／归属，不覆盖无关内容；逐文件比对清单／哈希，包括移除过时自有支持文件；任何不匹配阻塞交付。重跑替代验证前保留旧部署版。
Only after all selected modules are `verified`, Coordinator publishes exact frozen inventories. Inspect conflicts/ownership, preserve unrelated content, compare every file/inventory/hash including obsolete owned support removals; any mismatch blocks delivery. Preserve deployed versions until replacements verify.

验证及交付核查后才按 Deployment 更新兼容发现链接并检查真实加载。遇 `blocked` / `needs_review` / `partial_validated` 展示状态证据，停止，不宣称完成。
Update compatible discovery links/check actual loading under Deployment only after verification/delivery checks. Report evidence for `blocked`/`needs_review`/`partial_validated` and stop before claiming completion.

全部选中验证后，调度 Author 生成 `{index-output-dir}/{project-name}-dr/SKILL.md`；`{index-output-dir}` 按 Deployment 解析，传入确认选中／排除表与种类、版本化 Phase 2 依赖图、**同一运行实际验证模块清单**、跟踪分支值。
After all selected modules verify, dispatch Author to generate `{index-output-dir}/{project-name}-dr/SKILL.md`; resolve `{index-output-dir}` via Deployment and pass confirmed selections/exclusions/kinds, versioned Phase 2 dependency map, **exact same-run verified module inventory** and tracked branch.

独立 commit／tag 未建立跟踪分支时显式传入 `N/A`（不适用／未建立），不得虚构。
For detached commits/tags without an established tracked branch, explicitly pass `N/A` (not applicable/not established); never invent one.

```yaml
---
name: {project-name}-dr
description: 在处理 {project-name} 代码库时使用 / Use when working with {project-name} — module knowledge, design logic and modification guides (generated from {ref})
---
```

索引必含 / Index must include:
- 仓库 URL／本地路径；tag／commit、来源身份、批准覆盖清单与采集时间；跟踪分支和生成时间。 / Repo URL/local path; tag/commit, source identity, approved overlay manifest/capture timestamp; tracked branch and generation timestamp.
- 各模块验证来源、候选哈希、隔离等级、回归／终考分数、测试主题；一行用途与实际部署路径。 / Per-module verified source, candidate hashes, isolation, regression/holdout scores, topics, one-line purpose and actual deployed path.
- 选中／排除范围与种类（排除未经验证）、模块依赖、跨模块常用操作入口及执行顺序；综合场景标注未受模块考试验证。 / Selections/exclusions/kinds (excluded are unverified), dependencies and cross-module operation entry/order; label synthesized scenarios unverified by module exams.

Author 读取全部模块 skill 综合工作流，不复制私有键／原始交接。全局索引引用真实项目路径，说明文件访问要求，不授予额外权限。
Author reads ALL module skills to synthesize workflows, never copying private keys/raw handoffs. Global indexes use actual project paths and explain filesystem access requirements without granting permissions.

## 阶段 6：仅 skill 用户验收 / Phase 6: Skill-Only User Acceptance

展示 Phase 4 推荐题：“技能已生成并验证；欢迎测试以下问题或任意 {project-name} 问题，我仅使用生成 skill 回答。”
Present Phase 4 recommendations: “Skills generated and verified. Try these questions or any question about {project-name}; I will answer using ONLY the generated skills.”

仅可读取 `{output-dir}/{project-name}-dr*/` 模块 skill 和 `{index-output-dir}/{project-name}-dr/` 索引；不读源码或无关项目。技能不足则如实指出缺口，直到用户满意或结束。
Read ONLY generated module skills in `{output-dir}/{project-name}-dr*/` and index in `{index-output-dir}/{project-name}-dr/`; no source or unrelated projects. Admit skill-only gaps honestly; continue until user satisfaction or session end.

## 阶段 7：清理 / Phase 7: Cleanup

本地仓库跳过。仅本轮 URL 新建 checkout 且不含生成输出／保留证据时，询问删除该确切目录或保留，明确确认后才删。
Skip for local repos. Only for a URL checkout created this run with no generated outputs/retained evidence, ask whether to delete that exact checkout or retain it; delete only after explicit confirmation.

含项目 skill／文档／证据的克隆必须保留，说明路径依赖；删除前需另行确认保留输出的迁移并修复索引／发现引用。不得清理既有 checkout、生成 skill 或证据记录。
Retain clones containing project skills/docs/evidence and explain path dependencies; deletion requires separately confirmed output-preserving relocation and repaired index/discovery references. Never remove pre-existing checkouts, generated skills or evidence records as cleanup.

## 格式与交付核查 / Formatting and Delivery Checks

源码始终只读；技能须自足并报告测试范围／缺口。名称／目录小写 kebab-case 且匹配 YAML；Markdown basename 大写（含 `REFERENCE.md`），验证前检查 frontmatter／相对链接。
Keep source read-only; skills must be self-sufficient and report tested coverage/gaps. Names/directories use lowercase kebab-case matching YAML; uppercase Markdown basenames (including `REFERENCE.md`); check frontmatter/relative links before exams.

默认中文／英文在同一 skill／支持文件内按章节配对，显式语言优先，不生成语言后缀 skill 文件。核对两语选中范围、来源、契约／默认值、示例与状态一致，检查支持链接，对**完整双语文件**计算候选哈希。
Default to section-paired Chinese/English in the same skill/support files; explicit language wins, with no language-suffixed skill files. Reconcile selections, source identity, contracts/defaults, examples and statuses, check support links and hash each **complete bilingual file** as a candidate.
