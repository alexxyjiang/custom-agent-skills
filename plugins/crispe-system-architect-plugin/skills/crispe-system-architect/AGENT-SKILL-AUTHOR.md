# AGENT-SKILL-AUTHOR / 模块与索引技能编写者 / Module and Index Skill Author

## 范围与输入 / Scope and Inputs

仅本角色生成／修订模块、组件、支持文件和 DR 索引；Coordinator 负责评分、发布和发现链接。优先使用可用的宿主原生技能编写指南。
Only this role generates/revises module, component, support and DR index skills; Coordinator owns scoring, publication and discovery links. Use available host-native skill authoring guidance.

| 输入 / Input | 要求 / Requirement |
| --- | --- |
| 标识与路径 / Identity and paths | `{project-name}`、`{module-name}`、已确认部署目录 `{output-dir}`、私有 `{candidate-output-dir}` 或 `{index-output-dir}` / confirmed deployed directory and private candidate/index directory |
| 分析 / Analysis | 源码身份/ref、Reader 核查的分析／证据、模块范围、语言及适用流水线规范 / source identity/ref, Reader's checked analysis/evidence, scope, language and applicable pipeline profile |
| 修复 / Repair | 私有且经 Coordinator 批准的纠正交接 / private Coordinator-approved correction handoff |
| 索引 / Index | 所有已选模块 skill 与已验证记录，以及下方索引清单 / all selected module skills, verified records and the index inventory below |

遵循 [SKILL.md 通用规则 / Shared Rules](./SKILL.md#通用规则--shared-rules)，尤其是单文件双语、确认、命名和私有候选发布规则；详略呈现见 [DOCUMENT-TEMPLATES.md](./DOCUMENT-TEMPLATES.md)。
Follow SKILL.md Shared Rules, especially bilingual in-file delivery, confirmation, naming and private-candidate publication; use DOCUMENT-TEMPLATES.md for presentation depth.

## 模块范围与证据 / Module Scope and Evidence

只编写明确确认的已选模块；默认全选仍须 Coordinator 确认清单。按源码边界划分，独立 Config/Doc 目录可单列；索引列出已选／排除范围，不暗示排除项已验证。
Author only explicitly confirmed selected modules; default-all still needs Coordinator inventory confirmation. Use source boundaries, with independent Config/Doc directories eligible as modules; index selected/excluded scope without implying excluded verification.

Config/Doc 按实际配置／文档契约调整用途、设计、结构、流转和修改场景；标注不适用的执行细节，不虚构，证据与验证标准相同。
Adapt Config/Doc purpose, design, structures, flow and changes to actual configuration/documentation contracts; mark executable details inapplicable rather than inventing them, with the same evidence and verification standards.

模块候选写入 `{candidate-output-dir}/{project-name}-dr-{module-name}/`，位于发现根目录外；不修改已发布目录。Coordinator 核对哈希后发布准确的已验证清单。
Write module candidates outside discovery roots at `{candidate-output-dir}/{project-name}-dr-{module-name}/`; do not modify published directories. Coordinator publishes the exact verified inventory after hash checks.

## 五维完整知识 / Five-Dimension Complete Knowledge

每个 skill 必须自足，覆盖下表；行为论断均可追溯到核查过的源码。
Each skill must be self-sufficient, cover this table and trace every behavioral claim to checked source evidence.

| 维度 / Dimension | 必需内容 / Required content |
| --- | --- |
| 用途／能力 / Purpose/capabilities | 对外行为、签名、输入／输出说明 / public behavior, signatures, input/output descriptions |
| 设计逻辑 / Design logic | 已记载的依据、心智模型、权衡；明确标注推断与未知意图 / documented rationale, mental model, trade-offs; label inference and unknown intent |
| 核心结构 / Core structures | 类型、字段、关系、确切源码位置 / types, fields, relationships, exact source locations |
| 状态流转 / State flow | 入口 → 处理 → 输出、错误路径、副作用、变更 / entry → processing → output, error paths, side effects, mutations |
| 修改指南 / Modification guides | 至少三个具体场景，含实际文件／函数 / at least three concrete scenarios with actual files/functions |

作业另须遵循所提供 [QUICK-MODE.md](./QUICK-MODE.md) 流水线规范：契约、转换顺序、生效默认值／分支、输出、恢复／完成及 Mermaid 规则。
Jobs additionally follow the supplied QUICK-MODE.md pipeline profile: contracts, transformation order, effective defaults/branches, outputs, recovery/completion and Mermaid rules.

可整合 Quick 发现，但 Quick 文档本身不是证据；Verifier 不应依赖外部 Quick 文档或私有 Reader 交接。
Integrate useful Quick findings, but Quick documents alone are not proof; Verifier must not need external Quick documents or private Reader handoffs.

## 默认 CRISPE 与格式 / Default CRISPE and Format

新模块／组件和 DR 索引默认在标准 YAML 后使用 CRISPE；用户明确格式优先，但保留有效 SKILL.md 元数据、完整知识和验证要求。不得为标题削弱内容或虚构示例。
New module/component and DR index skills default to CRISPE after standard YAML. Explicit user format overrides retain valid SKILL.md metadata, complete knowledge and verification; do not weaken content for headings or invent examples.

| 章节 / Section | 内容 / Content |
| --- | --- |
| Context | 仓库／模块背景 / repository/module grounding |
| Role | 知识使用者 / knowledge consumer |
| Instruction | 如何使用知识 / how to use the knowledge |
| Specification | 经验证的五维知识／修改指南，或索引版本／模块／验证记录 / verified five-dimensional knowledge/change guides, or index version/module/verification records |
| Performance | 约束、覆盖限制 / constraints, coverage limits |
| Example | 源码支撑的使用／修改示例或跨模块指南 / source-backed usage/change examples or cross-module guides |

```yaml
---
name: {project-name}-dr-{module-name}
description: Use when working with the {module-name} module of {project-name} — [purpose and useful contexts]
---
```

名称／目录为单连字符分隔的小写字母数字，1–64 字符；验证并确认歧义规范化和冲突。description 非空且 ≤1024 字符。
Names/directories are lowercase alphanumerics separated by single hyphens, 1–64 characters; validate/confirm ambiguous normalization and collisions. Description is nonempty and ≤1024 characters.

文件 basename 大写（SKILL.md、REFERENCE.md、DATA-STRUCTURES.md）；支持文件用相对链接并说明加载时机。SKILL.md 聚焦，大型参考内容可拆分但不得丢失覆盖。
Use uppercase basenames (SKILL.md, REFERENCE.md, DATA-STRUCTURES.md), relative support links and load guidance. Keep SKILL.md focused; split large references without losing coverage.

不发布原始考试答案键、必需事实题库、评分明细或修复答案；纠正须转为通用模块知识，而非背诵答案。冻结候选的编辑经 Coordinator，受影响考试结果失效。
Do not publish raw exam keys, required-fact banks, grading material or repair answers; turn checked corrections into general module knowledge, not memorized answers. Frozen edits go through Coordinator and invalidate affected exams.

## DR 索引 / DR Index

Coordinator 确认全部已选模块已验证后，读取全部已选 skill，生成 `{index-output-dir}/{project-name}-dr/SKILL.md`，name 为 `{project-name}-dr`。
After Coordinator confirms every selected module verified, read all selected skills and generate `{index-output-dir}/{project-name}-dr/SKILL.md` with name `{project-name}-dr`.

| 必需记录 / Required record | 内容 / Content |
| --- | --- |
| 来源版本 / Source version | 仓库身份／位置、ref/commit、捕获／生成时间、批准的源码覆盖身份、跟踪分支值或显式 N/A / repo identity/location, ref/commit, capture/generation timestamps, approved source overlay identity, tracked branch or explicit N/A |
| 范围与图谱 / Scope and maps | 显式已选／排除模块及类型清单、带版本的模块／依赖图 / explicit selected/excluded inventory and kinds, versioned module/dependency map |
| 同轮模块 / Same-run modules | 准确已验证路径／记录、用途、源码／候选哈希、隔离等级、回归／终考分数、测试主题、依赖 / exact verified paths/records, purpose, source/candidate hashes, isolation level, regression/final scores, tested topics, dependencies |
| 场景入口 / Scenario entry guides | 跨模块指南；综合场景注明未经模块考试验证 / cross-module guides; label synthesized scenarios unverified by module exams |

不得从缺失 skill 推测排除范围，或混入其他运行的同名旧模块。仅发布所需验证摘要，原始考试／评分材料保持私有。
Do not infer exclusions from missing skills or include stale same-name modules from other runs. Publish required verification summaries only; keep raw exam/grading material private.

按 [DEPLOYMENT.md](./DEPLOYMENT.md) 部署；仅明确选择方式 2 才全局存放索引。全局路径不授权外部项目访问，也不使知识脱离仓库。
Deploy through DEPLOYMENT.md; only explicit option 2 places the index globally. Global paths grant neither external project access nor repo-independent knowledge.

## 交付检查 / Delivery Checks

验证 YAML、全部支持／模块链接；逐文件核对双语模块选择、来源、契约／默认值、示例和验证状态一致。完整双语文件计算候选哈希；不创建语言后缀 skill 文件。
Validate YAML and all support/module links; compare paired languages for identical selections, source identity, contracts/defaults, examples and verification status. Hash each complete bilingual candidate file; create no language-suffixed skill files.

向 Coordinator 返回实际路径、候选文件清单、未解决缺口；编写完成不等于已验证。
Return actual paths, candidate inventory and unresolved gaps to Coordinator; authoring completion is not verified status.
