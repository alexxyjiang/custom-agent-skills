---
name: crispe-system-architect
description: >-
  Use when asked to analyze a repo, generate STRUCTURE.md / ARCHITECTURE.md /
  OVERVIEW.md / CLAUDE.md / CONTRIBUTING.md, map architecture or explain job
  inputs, outputs and data flows with Mermaid diagrams. Also use for deep code
  reading, module design and modification guides, verified reusable skills or
  selected-component skill extraction from a local repo or GitHub URL.
  Defaults to Quick documentation; supports Deep verified skills and Mix (Quick first,
  then Deep reusing Quick outputs). 支持分析仓库、架构文档、作业流程图、深度理解代码库、
  生成可复用 skill、抽取组件；支持中文、English 和中英双语。
  Offers documentation before code changes when architecture/context docs are absent.
version: 2.0.1
argument-hint: "[Quick|Deep|Mix] [source] — Quick artifact 1|2|3; confirm source, scope and deployment interactively"
metadata:
  version: "2.0.1"
compatibility: "Claude Code and OpenCode; Git and SHA-256 hashing; fresh-context subagents for Deep verification."
---

# CRISPE System Architect / 仓库架构与知识生成

## 模式 / Modes

**默认 Quick / Default: Quick.** 明确要求深读或生成 skill 时选择 Deep，同时需要文档和 skill 时选择 Mix；有冲突才询问模式。
Use Deep for explicit deep reading/skill generation, Mix for both documents and skills; ask about mode only when instructions conflict.

| 模式 / Mode | 顺序 / Sequence | 产物与检查 / Outputs and checks |
| --- | --- | --- |
| Quick（默认 / default） | Reader → Documenter | 仓库文档与源码核对；不跑闭卷考试 / repository docs and source checks; no closed-book exams |
| Deep | Reader → Author → Questioner / Verifier → Coordinator | 所选模块 skill 与 DR 索引；回归题库和独立终考 / selected module skills and DR index; regression and fresh holdout |
| Mix | 先完整 Quick，再复用成果执行 Deep / finish Quick before Deep reuse | 两类产物分别报告状态 / report both output statuses separately |

代码改动前发现仓库根目录无架构／上下文文档（含语言版本），按 Quick 提供三种文档选择或跳过；不自动进入 Deep/Mix。
Before code changes without root architecture/context docs, offer Quick's three choices or skip; never auto-expand to Deep/Mix.

## 通用规则 / Shared Rules

1. **证据与确认 / Evidence and confirmation：** 先检查，后写入；不猜命令、默认值或设计意图。有歧义一次问一个问题并等待，已确认事项只在来源／范围／路径变化时重问。
   Inspect before writing; do not invent commands, defaults or intent. Ask one focused question and wait; revisit confirmed decisions only when inputs/scope/paths change.
2. **来源 / Source：** 已提交内容从确认 commit 的 Git 对象读取；timestamp 记录时间。未提交 Code / Doc / Config / Other 逐类确认，纳入内容以不可变快照和 SHA-256 锁定。Mix 在 Quick 前锁定同一来源。保持源码工作区只读，生成输出不作为本轮输入。
   Pin committed content to Git; record timestamps. Confirm dirty categories independently and hash accepted immutable snapshots. Lock one source before Mix Quick; keep source unchanged and exclude generated outputs from input monitoring.
3. **模块 / Modules：** 按源码边界列主要模块，独立 Config/Doc 目录单列。默认全选但须确认；Mix 在 Quick 后选择。确认前只做有限扫描，未选模块跳过 Deep 阅读／生成／考试，索引注明范围。模块选择与未提交内容纳入是独立决策。
   List code-boundary modules plus independent Config/Doc directories. Default all, wait for confirmation; select after Quick in Mix. Use bounded discovery before selection; exclude unselected modules from full Deep work and report scope separately from dirty-file decisions.
4. **生成风格 / Authoring：** 新 skill 默认 CRISPE（Context / Role / Instruction / Specification / Performance / Example）。文件 basename 大写，skill 名称／目录小写 kebab-case，与 YAML name 一致。详略模板中的 Optional 按适用性，不降低 Deep 覆盖或验证要求。
   Default new skills to CRISPE; uppercase file basenames and lowercase kebab-case skill names matching YAML. Optional means applicability, not reduced Deep coverage.
5. **双语 / Languages：** 默认中英文同步，显式语言优先。工具自身、生成的模块／索引 skill 及支持知识（如 REFERENCE.md）均单文件双语；只有非 skill 文档使用基础导航 + `.en.md` + `.zh-CN.md`。SKILL.md 保留有效 YAML 和完整知识；CLAUDE.md 保留必要加载上下文。两种语言的事实、示例和验证状态一致，标识符／命令／路径不翻译。
   Default synchronized English/Chinese, explicit language wins. This skill and its resources, generated skills/indexes and knowledge supports are bilingual in-file. Only non-skill docs split into base navigation and language bodies. Keep YAML/complete skill knowledge, essential CLAUDE context and identical facts/examples/status; preserve identifiers, commands and paths.
6. **部署 / Deployment：** 默认全部项目级 `<repo>/.agents/skills/`；方式 2 仅 DR 索引存 `~/.agent/skills/`。每次确认项目实际目录，通过同级 `.claude/skills/<name>` 相对软链暴露；既有同名内容先核实。工具自身保持既有安装位置。
   Default all-project; option 2 globalizes only the index. Confirm actual paths and expose per-skill relative links in `.claude/skills/`; inspect collisions. Keep this tool's existing installation.
7. **验证与发布 / Verification and publication：** 候选在私有目录生成／冻结／验证，验证后核对准确文件清单与哈希再发布。原始分析、快照、题库、答案和评分留在发布目录外。不把 Quick 文档或综合索引场景宣称为闭卷验证。
   Generate/freeze/verify private candidates; publish the exact checked inventory/hashes. Keep analysis/snapshots/exams private. Quick docs and synthesized index scenarios are not module-exam verified.

### 分析排除项 / Analysis Exclusions

排除仓库及其子目录中的版本控制元数据与托管平台配置，含同名文件／目录：Git `.git`；SVN `.svn`、`_svn`；Mercurial `.hg`；Bazaar `.bzr`；Darcs `_darcs`；Fossil `.fslckout`、`_FOSSIL_`、`.fossil-settings`；CVS `CVS`；RCS `RCS`；SCCS `SCCS`；其他 VCS 的等价管理路径。托管配置排除 `.github`、`.gitlab`、`.bitbucket`、`.gitea`、`.forgejo`、`.azuredevops`、`.circleci` 及版本管理专用配置（如 `.gitignore`、`.gitattributes`、`.gitmodules`、`.hgignore`、`.gitlab-ci.yml`、`bitbucket-pipelines.yml`、`azure-pipelines.yml`）。
Exclude VCS metadata and hosting configuration at repo or nested levels, including files/directories with the listed names and equivalent management paths for other VCS. Exclude hosting/CI metadata and VCS-specific configuration, not ordinary source directories merely named git/github.

此规则覆盖 Quick／Deep／Mix 的树、模块、阅读、证据及未提交候选清单；不将排除目录单列为 Config/Doc 模块，也不通过软链绕过。保留 Git ref／commit／status 等来源锁定操作，只取所需版本信息，不分析管理目录内部；必要信息不能从允许来源核实时明确标注未知，不回读排除项。
Apply exclusions to trees, module selection, reading, evidence and dirty-file inventories in every mode; never promote excluded paths to Config/Doc modules or follow links around exclusions. Git ref/commit/status operations remain allowed for source identity, not metadata-content analysis. Report unavailable facts rather than reading excluded paths.

## 角色 / Roles

| 角色 / Role | 唯一职责 / Responsibility | 提示 / Prompt |
| --- | --- | --- |
| agent-reader | 源码分析、证据与修复知识 / source analysis, evidence and repair knowledge | [Reader](./AGENT-READER.md) |
| agent-documenter | 统一详略架构／说明文档 / unified architecture/documentation | [Documenter](./AGENT-DOCUMENTER.md) |
| agent-skill-author | 所有模块、支持和索引 skill 的生成／修订 / all skill/support/index authoring and repair | [Author](./AGENT-SKILL-AUTHOR.md) |
| agent-questioner | 独立源码出题，不读候选、Quick 文档、旧答案或反馈 / independent source-backed questions, no candidate/Quick/answer/feedback reads | [Questioner](./AGENT-QUESTIONER.md) |
| agent-verifier | 只读候选 skill 与 question-only 输入，闭卷回答 / candidate-only closed-book answers | [Verifier](./AGENT-VERIFIER.md) |
| Coordinator（主 agent / main agent） | 确认、调度、证据核验、题库、评分、隔离状态与发布 / confirmation, dispatch, evidence, banks, grading, isolation and publication | [Deep](./DEEP-MODE.md) |

角色文件是跨平台调度提示，不是已注册的 host agent。使用实际宿主能力，在新上下文调度 Questioner / Verifier 并记录真实隔离等级。
Role resources are portable dispatch prompts, not registered host agents. Use available host capabilities; dispatch exam agents in fresh contexts and record actual isolation.

## 主要文件确认表 / Main Output Confirmation Table

写入前打印实际路径、语言、角色、必选／可选和部署目标，确认清单；写入后逐项核对。显式语言要求覆盖默认双语布局。
Print and confirm actual paths, languages, authors, required/optional status and deployment before writing; reconcile afterwards. Explicit language overrides the default layout.

| 模式 / Mode | 主要文件 / Main files | 要求 / Requirement |
| --- | --- | --- |
| Quick 1 | STRUCTURE.md + STRUCTURE.en.md + STRUCTURE.zh-CN.md | 结构文档；保留已有 ARCHITECTURE/OVERVIEW basename / structure docs; preserve resolved basename |
| Quick 2 | CLAUDE.md + CLAUDE.en.md + CLAUDE.zh-CN.md | 简短命令优先上下文 / terse command-first context |
| Quick 3 | 结构文档组 + CONTRIBUTING.md + CONTRIBUTING.en.md + CONTRIBUTING.zh-CN.md | 两组 / both groups |
| Deep 每模块 / per module | SKILL.md；可选 REFERENCE.md 等 / optional supports | 单文件双语，全部候选文件冻结 / bilingual in-file; freeze all candidate files |
| Deep DR 索引 / index | 独立 DR 目录中的 SKILL.md / separate DR skill directory | 选中模块均验证后生成，注明排除范围 / generate after selected modules verify; disclose exclusions |
| Mix | 所选 Quick 清单，再完成 Deep 清单 / Quick, then Deep inventories | 按阶段确认 / confirm by stage |

## 按需加载 / Workflow Resources

- [QUICK-MODE.md](./QUICK-MODE.md)：文档选择、原模板、语言与 Pipeline 内容规则、文档检查 / artifact choices, original templates, pipeline content and checks.
- [DEEP-MODE.md](./DEEP-MODE.md)：模块范围、独立出题／闭卷验证、有界修复、索引和验收 / scope, exams, bounded repairs, index and acceptance.
- [MIX-MODE.md](./MIX-MODE.md)：Quick 完成后的版本化交接与 Deep 复用 / versioned sequential handoff.
- [SOURCE-VERSION.md](./SOURCE-VERSION.md)：Git／工作区选择、快照、来源新鲜度和候选冻结 / source resolution, snapshots, freshness and freezing.
- [DEPLOYMENT.md](./DEPLOYMENT.md)：路径、相对软链、发布及 host 发现检查 / paths, symlinks, publication and host discovery.
- [DOCUMENT-TEMPLATES.md](./DOCUMENT-TEMPLATES.md)：详略表达与 Optional 适用规则 / concise/detailed presentation and applicability.

检查 YAML、description 长度（1–1024 字符）、资源链接、实际发现和验证状态；不宣称未执行的检查。新鲜度仅提供来源／候选变更停止机制，不实现完整 diff 增量更新服务。
Validate YAML, description length, links, discovery and actual verification state; report only performed checks. Freshness stops on relevant changes; no comprehensive diff-based incremental service is provided.
