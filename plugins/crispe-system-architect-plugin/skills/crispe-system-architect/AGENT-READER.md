# agent-reader / 源码分析者

遵循 SKILL.md「分析排除项」：来源枚举、未提交清单及证据阅读先过滤 VCS／托管配置路径；不将其视为模块或来源证据。
Apply SKILL.md Analysis Exclusions before source/dirty-path enumeration and evidence reads; excluded VCS/hosting paths are neither modules nor evidence.

职责是分析与证据交接，不写发布文档或 skill。遵循 [SKILL.md](./SKILL.md) 和 [SOURCE-VERSION.md](./SOURCE-VERSION.md)。
Analyze source and hand off evidence; do not author published documents/skills.

## 输入与交接 / Inputs and Handoff

| 输入 / Input | 内容 / Content |
| --- | --- |
| `{source-dir}`, `{module-dir}` | repo／模块；Quick 为仓库范围 / repo/module; Quick repository scope |
| `{project-name}`, `{ref}`, `{source-sha}` | 项目、确认版本和完整 commit / project, confirmed ref and commit |
| `{source-identity}`, `{source-manifest}`, `{snapshot-dir}` | Git + 获准快照，使用前核对哈希 / approved source resolver; validate hashes |
| `{mode}`, `{quick-handoff}` | Quick 或 Deep；Mix 的 Quick 交接路径，其他场景空 / reading depth and Mix handoff or empty |
| `{handoff-dir}/ANALYSIS.md` | 私有结构化分析与证据 / private structured analysis/evidence |

## 阅读范围 / Reading Scope

- Quick／选择前发现：依据 QUICK-MODE.md 抽样建图，不宣称全读。Deep：确认范围后彻底阅读选中模块全部文件，必要时检查协作者作为有限上下文。
  Sample for Quick/bounded discovery; fully read every selected module file in Deep, with narrowly relevant collaborator context.
- 以源码／build／package 边界列主要模块，独立 Config／Doc 目录单列；默认全选须确认，Mix 在 Quick 后选择。排除 build／依赖／生成噪声，未选模块不称为 Deep 覆盖。
  Discover actual modules plus independent Config/Doc; confirmed default all, selection after Mix Quick. Exclude noise and do not claim unselected coverage.
- Mix 复用 Quick 图与证据，对同一来源核实后补深读，不重复同一扫描。纠正时提供事实和证据，不把推断设计意图当已知。
  Verify/reuse Quick knowledge, deepen gaps, and supply evidence-backed corrections without inventing intent.

## Deep 五维交接 / Five Knowledge Dimensions

| 维度 / Dimension | 必须覆盖 / Coverage |
| --- | --- |
| 能力 / Capabilities | 定位、外部能力、API／签名与输入输出 / purpose, external APIs/signatures and I/O |
| 设计 / Design | 已记录的依据、思维模型、权衡；区分推断 / documented rationale, mental model, trade-offs vs inference |
| 结构 / Structures | 类型、字段、关系与定义路径 / types, fields, relationships and paths |
| 状态流 / State flow | 入口、处理、结果、错误、副作用／修改 / entry, processing, results, errors and mutations |
| 修改 / Modifications | 至少 3 个具体场景及真实文件／函数 / at least 3 concrete changes with paths/functions |

Config 模块对应键／默认值、加载／覆盖、依赖和错误；Doc 对应指南、导航、契约及源码一致性。明确不适用的可执行维度，不虚构 API／状态机。
Adapt Config/Doc coverage to actual contracts and maintenance; mark inapplicable executable dimensions.

Pipeline 模块同时使用已提供的 QUICK-MODE.md profile：输入契约、真实转换顺序、算法默认值／分支、输出与恢复完成语义，使用有帮助的 Mermaid。每项引用准确路径／函数／行号。
Use supplied pipeline rules for contracts/order/defaults/outputs/recovery and useful Mermaid, citing concrete evidence.

ANALYSIS.md 记录来源／范围、模块依赖、知识、证据、已知／推断／未知和修改场景。私有修复 keys／grades 不混入文档复用交接；缺证据就报告待调查。
Record source/scope/map/knowledge/evidence/uncertainties; keep repair keys/grades out of reusable analysis and report gaps honestly.
