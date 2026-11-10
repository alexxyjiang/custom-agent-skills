# DOCUMENT-TEMPLATES / 统一详略模板 / Unified Depth Templates

## 使用原则 / Usage

Documenter 负责文档风格，Skill Author 负责 skill 格式；术语、本地化标题、源码引用与 Mermaid 一致。详略表示深度而非模式：Quick 默认精简，要求深度／契约时可详细；真正有歧义才问，Deep 完整覆盖不变。
Documenter owns documentation style, Skill Author skill formatting; align terms, localized headings, source references and Mermaid. Profiles control depth, not modes: Quick defaults concise but can be detailed for requested depth/contracts; ask only for genuine ambiguity. Deep coverage remains complete.

[QUICK-MODE.md](./QUICK-MODE.md) 原产物模板及流水线规范决定具体要求；共享命名、语言、保留与验证规则见 [SKILL.md](./SKILL.md#通用规则--shared-rules)。
QUICK-MODE.md original artifact templates and pipeline profile control specific requirements; see SKILL.md Shared Rules for shared naming, language, preservation and verification policy.

## 精简版模板 / Concise Template

```markdown
# [Project or Component] — [Document Purpose]

## 概述 / Overview
[Purpose, scope, key boundary; quickly scannable.]
[目的、范围、关键边界；便于快速浏览。]

## 结构与职责 / Structure and Responsibilities
[Key paths/modules and collaboration.]
[关键路径/模块及其协作。]

## 核心流程 / Core Flow
[Main stages; source-backed Mermaid when useful.]
[主要阶段；有帮助时使用有源码依据的 Mermaid 图。]

## 关键约束 / Key Constraints
[Essential applicable invariants; omit only when none exist.]
[适用的关键不变条件；仅在不存在任何此类条件时省略。]

## 源码引用 / Source References
[Exact inspected files/functions and source identity.]
[实际检查的具体文件/函数及源码身份。]

## 设计依据 / Design Rationale [Optional]
## 输入与输出契约 / Input and Output Contracts [Optional]
## 数据结构 / Data Structures [Optional]
## 修改场景 / Modification Scenarios [Optional]
## 构建、运行与测试 / Build, Run and Test [Optional]
## 入门指南 / Getting Started [Optional]
## 恢复与完成 / Recovery and Completion [Optional]
## 验证与待解问题 / Verification and Open Questions [Optional]
```

## 详细版模板 / Detailed Template

详细版是精简版的超集：五个必选章节同序，保留全部可选章节并扩展深度。标题可按场景改写，但语义对应的章节视为同一章节，不因改名而遗漏或合并掉覆盖。
The detailed template is a superset of the concise template: keep the five required sections in order, retain all optional sections, and expand depth. Scenario-specific titles are equivalent when their section meaning is unchanged; renaming must not lose coverage.

```markdown
# [Project or Component] — [Document Purpose]

## 概述 / Overview
[Purpose, scope, key boundaries and system context; keep the opening quickly scannable.]
[目的、范围、关键边界及系统背景；开篇仍便于快速浏览。]

## 结构与模块职责 / Structure and Module Responsibilities
[Key paths/modules, ownership, dependencies and collaboration; cite concrete implementations.]
[关键路径/模块、职责归属、依赖与协作；引用具体实现。]

## 核心流程与阶段细节 / Core Flow and Stage Details
[Entry-to-output stages, meaningful branches and implementation pointers; use source-backed Mermaid when useful.]
[入口到输出的阶段、重要分支与实现位置；有帮助时使用有源码依据的 Mermaid 图。]

## 关键约束 / Key Constraints
[Essential applicable invariants, boundary conditions and failure limits; omit only when none exist.]
[适用的关键不变条件、边界条件及失败限制；仅在不存在任何此类条件时省略。]

## 源码引用 / Source References
[Exact inspected files/functions, source identity and evidence links for the documented behavior.]
[实际检查的具体文件/函数、源码身份及文档行为对应的证据链接。]

## 设计依据与权衡 / Design Rationale and Trade-offs [Optional]
## 入口与输入输出契约 / Entry Points and Input and Output Contracts [Optional]
## 核心数据结构 / Core Data Structures [Optional]
## 修改场景 / Modification Scenarios [Optional]
## 构建、运行环境与测试 / Build, Runtime Environment and Test [Optional]
## 入门指南 / Getting Started [Optional]
## 恢复与完成 / Recovery and Completion [Optional]
## 验证与待解问题 / Verification and Open Questions [Optional]
## 辅助作业与部署 / Auxiliary Jobs and Deployment [Optional]
```

### 章节对应检查 / Section Correspondence

| 精简版 / Concise | 详细版 / Detailed | 属性 / Status |
| --- | --- | --- |
| 概述 / Overview | 概述 / Overview | 必选 / Required |
| 结构与职责 / Structure and Responsibilities | 结构与模块职责 / Structure and Module Responsibilities | 必选、场景化同义 / Required, scenario-equivalent |
| 核心流程 / Core Flow | 核心流程与阶段细节 / Core Flow and Stage Details | 必选、展开细节 / Required, expanded |
| 关键约束 / Key Constraints | 关键约束 / Key Constraints | 必选 / Required |
| 源码引用 / Source References | 源码引用 / Source References | 必选 / Required |
| 设计依据 / Design Rationale | 设计依据与权衡 / Design Rationale and Trade-offs | 可选 / Optional |
| 输入与输出契约 / Input and Output Contracts | 入口与输入输出契约 / Entry Points and Input and Output Contracts | 可选、扩展入口 / Optional, adds entry points |
| 数据结构 / Data Structures | 核心数据结构 / Core Data Structures | 可选 / Optional |
| 修改场景 / Modification Scenarios | 修改场景 / Modification Scenarios | 可选 / Optional |
| 构建、运行与测试 / Build, Run and Test | 构建、运行环境与测试 / Build, Runtime Environment and Test | 可选、包含运行与环境 / Optional, includes runtime and environment |
| 入门指南 / Getting Started | 入门指南 / Getting Started | 可选 / Optional |
| 恢复与完成 / Recovery and Completion | 恢复与完成 / Recovery and Completion | 可选 / Optional |
| 验证与待解问题 / Verification and Open Questions | 验证与待解问题 / Verification and Open Questions | 可选 / Optional |
| — | 辅助作业与部署 / Auxiliary Jobs and Deployment | 详细版附加 / Detailed-only addition |

## 可选与产物要求 / Applicability and Artifact Requirements

[Optional]／[可选] 只表示适用性；交付时去掉标记，省略不适用章节，不填空洞内容。模板不替代产物专用要求。
[Optional]/[可选] means applicability only; remove markers in delivery and omit inapplicable sections without empty filler. Templates do not replace artifact-specific requirements.

| 产物／内容 / Artifact/content | 必须保留 / Must retain |
| --- | --- |
| 流水线 / Pipeline | 已实现且相关的契约、恢复／完成；遵守 QUICK-MODE.md 精确规范，不推断不存在的恢复 / implemented, relevant contracts and recovery/completion; exact QUICK-MODE.md profile, no invented recovery |
| 构建／测试 / Build/test | 原产物模板要求的章节；未知命令用本地化未知标记，不编造示例 / sections required by the original artifact template; localized unknown markers for unknown commands, no fabricated examples |
| Deep 模块 / Deep modules | 用途／能力、设计逻辑、核心结构、状态流、至少三个带源码位置的修改场景；Config/Doc 按实际契约适配 / purpose/capabilities, design logic, core structures, state flow, at least three source-pointed changes; adapt Config/Doc to actual contracts |
| Deep 索引 / Deep index | 来源／验证元数据、实际模块位置、依赖、跨模块指南；区分抽样验证模块覆盖与未验证综合场景；完整清单见 AGENT-SKILL-AUTHOR.md / source/verification metadata, actual module locations, dependencies, cross-module guides; separate sampled verified coverage from unverified synthesis; full inventory in AGENT-SKILL-AUTHOR.md |
| CLAUDE.md | 简短、命令优先，保留必要加载上下文；不换成通用结构模板 / terse, command-first, essential loading context; no generic structure-template replacement |
| CONTRIBUTING.md | 保留原贡献模板，不换成通用结构模板 / retain original contribution template, no generic structure-template replacement |
| 文件保留 / File preservation | 保留无关内容，确认完整基础文档迁移；大写 basename、保留语言后缀（`STRUCTURE.zh-CN.md`），不重命名源码路径 / preserve unrelated content, confirm full base-document migration; uppercase basenames, retain language suffixes, never rename source paths |

语言布局按 SKILL.md：仅非 skill 文档使用基础导航＋完整英文／中文语言文件；skill、支持文件和索引双语在文件内，不创建语言拆分 skill；显式语言优先。
Use SKILL.md language layout: only non-skill documents split into base navigation plus full English/Chinese files; skills, supports and indexes are bilingual in-file with no language-split skills; explicit language wins.

## Markdown 渲染兼容 / Markdown Rendering Compatibility

- 加粗、斜体和行内代码采用同一边界保护：与相邻正文或其他行内格式之间保留一个普通 ASCII 空格，如 加载 **重点** 内容、使用 *术语* 说明、调用 `Loader` 方法、**加载：** `Loader`。空格在完整标记外，不插入标记内部或代码内容；行首／行尾不额外加空格。
  Apply the same boundary protection to bold, italic and inline code: one ASCII space between a complete span and adjacent prose/other inline spans. Keep spacing outside delimiters, preserve code bytes and avoid extra leading/trailing spaces.
- 强调使用成对 ASCII 标记（加粗为两个星号、斜体为一个星号），内部首尾不留空白；行内代码使用成对、等长反引号，内容含反引号时选更长分隔符。检查渲染结构，不用全局替换误改代码围栏、列表星号、链接目标、路径或转义字符。
  Use paired ASCII emphasis markers with whitespace-free inner edges and matching-length backtick delimiters; use longer delimiters for embedded backticks. Check parsed structure rather than blindly rewriting fences, list markers, link targets, paths or escapes.
- 有序／无序列表每项独占一行，编号后留空格；不把下一项接到前一段末尾。嵌套项及续段正确缩进，列表、标题、表格、引用与代码块之间留空行；需要硬换行时明确使用 Markdown 换行语法。
  Put each list item on its own line with a space after its marker; indent nested/continued content, separate blocks with blank lines and use explicit syntax for intended hard breaks.
- 表格有表头分隔行，列数一致；单元格中的 `|` 转义为 `\|`，包含管道的命令优先放表格外的代码块。代码围栏独占行、成对且缩进一致，内容包含围栏时使用更长围栏；正文行内代码的反引号也须配对。
  Use valid table separators/column counts and escape literal pipes; place pipe-heavy commands outside tables. Pair standalone consistent fences, use longer fences around embedded fences, and pair inline backticks.
- 链接目标含空格或括号时使用兼容的 URL 编码或尖括号目标，正文不依赖自定义 HTML/CSS 或特定扩展排版；Mermaid 标签的格式化按下方共享规则与实际查看器能力处理。Mermaid 是否显示取决于查看器支持。
  Encode or angle-wrap link targets with spaces/parentheses; avoid renderer-specific HTML/CSS in prose; Mermaid label formatting follows the shared rules below and actual viewer capabilities. Mermaid requires viewer support.
- 写入后检查这些格式；已有 Markdown 解析器／目标浏览器查看器时做实际渲染核对，记录实际检查级别。Chrome 本身不解析 Markdown，语法检查不能宣称所有 Chrome 查看器渲染通过。
  Check formatting after writing and use an available parser/target browser viewer for rendering; report actual validation. Chrome does not natively parse Markdown, so syntax checks alone do not establish compatibility with every viewer.


## Mermaid 生成风格 / Mermaid Authoring Style

适用于 Quick / Deep / Mix 中的所有 Mermaid 图，覆盖上方模板的简略示例；显式用户要求优先。只统一表达方式，不引入特定仓库的业务流程、问题分类或本机部署配置。
Apply to every Mermaid diagram in Quick / Deep / Mix, including the abbreviated examples above; explicit user instructions win. Standardize presentation without importing repository-specific workflows, question categories or machine-local deployment configuration.

### 字体、连线与布局 / Fonts, Edges and Layout

- 默认字体栈为 `Iosevka Aile, Noto Sans CJK SC, sans-serif`，根配置和主题配置保持一致。英文/Latin 优先 Iosevka Aile；中文等缺失字形回退 Noto Sans CJK SC，其他不支持的字形继续回退系统字体；这是逐字形覆盖回退，不是语言识别。
  Use `Iosevka Aile, Noto Sans CJK SC, sans-serif` in both root and theme configuration. Latin prefers Iosevka Aile; missing glyphs such as CJK fall back to Noto Sans CJK SC, then system fonts for unsupported glyphs. This is glyph fallback, not language detection.
- 流程连线默认采用直线段与圆角转弯（`curve: "rounded"`），避免大幅连续弧线。先核对目标 Mermaid 版本是否支持；不支持时说明并采用可验证的兼容配置，不把某个远端服务当前版本硬编码为长期要求。
  Prefer straight edge sections with rounded bends (`curve: "rounded"`) over broad continuous curves. Check target-version support; disclose unsupported settings and use a verified compatible configuration instead of hard-coding a remote service's current version as a permanent requirement.
- 不设置固定节点宽高、任意 `wrappingWidth`、全局 `nowrap` 或用于掩盖裁切的 overflow/padding 补丁。使用 Mermaid 默认尺寸计算；包名、类名、方法名分行，多方法逐行，较长节点说明和连线标签用 `<br/>` 在语义边界折行。默认保留查看器的响应式行为，只有明确的预览/导出需求才调整容器策略。
  Keep Mermaid's default sizing; do not impose fixed node dimensions, arbitrary `wrappingWidth`, global `nowrap`, or overflow/padding patches to hide clipping. Put package, class and methods on separate lines, list multiple methods on separate lines, and break long node/edge labels at semantic boundaries with `<br/>`. Preserve viewer responsiveness unless an explicit preview/export requirement justifies a container override.

在支持圆角连线和 HTML 标签的目标渲染器中使用以下基线；`htmlLabels` 用于保留下划线等标签样式，不代表所有查看器均支持。
Use this baseline when the target renderer supports rounded edges and HTML labels; `htmlLabels` preserves label styling such as underlines, without implying universal viewer support.

```json
{
  "fontFamily": "Iosevka Aile, Noto Sans CJK SC, sans-serif",
  "themeVariables": {
    "fontFamily": "Iosevka Aile, Noto Sans CJK SC, sans-serif"
  },
  "flowchart": {
    "htmlLabels": true,
    "curve": "rounded"
  }
}
```

将基线放入 Mermaid 支持的 init directive 或渲染端配置；不得把配置文本误作图节点。
Apply through a supported Mermaid init directive or renderer configuration, never as graph nodes.

### 类级节点与标注 / Class-Level Nodes and Annotations

- 类级调用图标题统一为 `(完整包名) 类名 :: 方法名`，显示时允许换行；多个方法以换行加 `/` 分隔。类名、接口名、方法名用 `<u>…</u>` 下划线；数据/类型节点无具体方法时省略 `::`，不补造方法。函数式/脚本项目使用真实模块与函数，不虚构 class。
  Use `(full.package) ClassName :: methodName` for class-level call diagrams, allowing line breaks and separating multiple methods with a line break and `/`. Underline type/interface/method names with `<u>…</u>`; omit `::` for type/data nodes without a specific method. Use actual modules/functions for functional or script projects instead of inventing classes.
- 从锁定源码的定义、import 或已核实依赖定义确认包名/类型/方法。区分本仓库实现、外部接口、宿主代码与教学示例；不要把示例类当作已接入实现。回调属性、字段和方法分别如实标注。同一类可按方法职责拆成多个节点，但需说明这不代表新增组件或执行阶段。
  Verify packages/types/methods against pinned definitions, imports or inspected dependency definitions. Distinguish repository implementations, external interfaces, host code and examples; do not promote example classes to wired implementations. Identify callback properties, fields and methods accurately. A class may appear as multiple responsibility slices, with an explicit note that these are not additional components or execution stages.
- 概览/流水线图可保留真实阶段、数据集、服务名；仅类级调用图要求上述标签格式。所有图使用稳定 ASCII ID 和加引号的标签。用户要求标出问题/修改范围时，用图例定义专属、共享及其他边界，按方法/字段职责着色，不照搬其他项目的分类；短标注用 `<b><i>…</i></b>` 加粗斜体，长连线标签加引号并折行。
  Overview/pipeline diagrams may retain actual stages, datasets and service names; class headers apply only to class-level call diagrams. Use stable ASCII IDs and quoted labels throughout. For requested question/change overlays, define exclusive/shared/other boundaries in a legend, color by method/field responsibility, and derive categories from the current task. Format short annotations with `<b><i>…</i></b>`; quote and break long edge labels.

### 字体测量与导出验证 / Font Measurement and Export Checks

- 用户报告裁切时，先确认真实渲染链路：网页客户端渲染、编辑器导出、服务端生成 SVG，还是 `<img>` 加载已有 SVG；Chrome 本身不内建 Mermaid 渲染器。比较渲染器版本、字体和实际 SVG/图片请求，不连续盲调 box 宽度。
  Diagnose the actual pipeline before fixing clipping: browser-side rendering, editor export, server-generated SVG, or an existing SVG loaded via `<img>`. Chrome does not itself supply Mermaid rendering. Inspect renderer versions, fonts and actual SVG/image responses instead of repeatedly guessing box widths.
- 能控制渲染端时，先定义/加载所需字体及粗体/斜体，再等待 `document.fonts.load(...)` 与 `document.fonts.ready`，最后运行 Mermaid。服务器生成后在另一环境显示时，两端字体度量须一致；按需要嵌入获准字体或输出自包含 SVG。等待消费页面字体不能修复已用错误度量生成的 SVG。
  When controlling rendering, define/load the required font faces and weights/styles, await `document.fonts.load(...)` and `document.fonts.ready`, then run Mermaid. Server-generated SVG displayed elsewhere needs consistent font metrics; embed permitted fonts or produce self-contained SVG when appropriate. Waiting on the consuming page cannot repair SVG already laid out with wrong metrics.
- SVG 通过 `<img>` 展示时检查 decode、固有尺寸和 viewBox；导出器可从实际布局 viewBox 写入固有宽高，这不等于给 Markdown 设置固定节点尺寸。缓存键应包含渲染器版本、配置和字体身份，避免旧 SVG 或失败请求被复用。验证实际节点/连线标签边界、字体和图像加载；区分结构/语法、浏览器几何检查与人工视觉验证，不宣称未执行的检查。
  For SVG embedded through `<img>`, check decoding, intrinsic dimensions and viewBox; exporters may derive intrinsic width/height from the actual layout without fixing Markdown node dimensions. Cache identity should include renderer version, configuration and fonts to avoid stale SVGs or failed-request reuse. Check node/edge bounds, fonts and image loading; distinguish structure/syntax, browser geometry checks and human visual review, reporting only checks actually performed.
