# MIX-MODE / 顺序组合 / Sequential Mix Mode

SKILL.md 选定 Mix 后加载；顺序为完整 Quick → 复用成果执行 Deep，不是独立第三条分析流水线。共享确认、来源、模块、语言和部署规则见 [SKILL.md](./SKILL.md#通用规则--shared-rules)。
Load after SKILL.md selects Mix: finish Quick, then reuse its results in Deep, not a third independent pipeline. Follow SKILL.md Shared Rules for confirmation, source, modules, language and deployment.

## 1. Quick 前锁定来源 / Lock Source Before Quick

遵循 [SOURCE-VERSION.md](./SOURCE-VERSION.md)：确认 commit，分类待处理变更，一次询问一类纳入并等待；冻结批准内容，记录时间戳／哈希清单。克隆 URL 来源前确认检出位置，保持本地工作树不变。
Follow SOURCE-VERSION.md: confirm commit, classify pending changes, ask/wait on inclusion one category at a time; freeze approved content with timestamp/hash manifest. Confirm checkout location before URL cloning; keep local worktrees unchanged.

两个阶段使用同一不可变来源身份，先锁定后复用。
Both stages consume the same immutable source identity, locked before reuse.

## 2. 完整完成 Quick / Finish Quick Completely

遵循 [QUICK-MODE.md](./QUICK-MODE.md)：Coordinator 解决产物选择与已有文件处理；Reader 分析锁定来源，交图谱／证据给 Documenter；Documenter 按适当详略生成并检查全部所选 Quick 产物。
Follow QUICK-MODE.md: Coordinator resolves artifact choice and existing-file handling; Reader analyzes locked source and hands map/evidence to Documenter, who generates and checks all selected Quick artifacts at the appropriate depth.

Quick 任务必须完全完成，之后才开始 Deep；保存大写 basename 的私有交接：
Complete the entire Quick task before starting Deep; save a private uppercase-basename handoff:

| 交接内容 / Handoff content | 必需记录 / Required record |
| --- | --- |
| 来源与产物 / Source and outputs | 来源身份、范围、源码引用、完成文档路径 / source identity, scope, source citations, completed document paths |
| 图谱 / Map | 目录／模块、依赖、入口、主流程 / directories/modules, dependencies, entry points, main flows |
| 证据状态 / Evidence status | 已核查论断与推断、未知项、教程／源码差异 / checked claims versus inferences, unknowns, tutorial/source discrepancies |
| 检查 / Checks | 实际检查及结果；不宣称未渲染的图或未执行命令 / actual checks/results; no claims of unperformed rendering or command execution |

## 3. 确认范围并深化 / Confirm Scope and Deepen

Quick 完成后列主要源码模块及独立 Config/Doc 目录；默认全选仍须用户确认全选或纳入／排除清单。排除项不做 Deep 阅读／编写／考试，索引记录排除范围。未确认时确认实际项目 skill 目录；部署默认 1，仅明确选择启用 2。
After Quick, list major source-code modules and independent Config/Doc directories; default-all still requires user confirmation or inclusions/exclusions. Excluded modules skip Deep reading/authoring/exams and appear as excluded scope in the index. Confirm actual project skill directory if needed; deployment defaults to 1, with 2 only by explicit choice.

Reader 以 Quick 产物／图谱定位，对同一来源核查每个复用事实并全面阅读已选模块；Quick 文本不是独立源码证据，也不应无必要重复相同扫描。
Reader uses Quick artifacts/map for orientation, verifies every reused fact against the same source and thoroughly reads selected modules; Quick text is not independent evidence, and identical scans should not be repeated needlessly.

Author 将有用知识整合到自足模块 skill；Verifier 不需打开 Quick 文档或私有交接。
Author integrates useful knowledge into self-sufficient module skills; Verifier must not need Quick documents or private handoffs.

## 4. 隔离验证与交付 / Isolated Verification and Delivery

严格遵循 [DEEP-MODE.md](./DEEP-MODE.md) 阶段 4–7，不放宽检查：
Follow DEEP-MODE.md Phases 4–7 without loosening checks:

| 角色 / Role | 输入／职责 / Inputs/responsibility |
| --- | --- |
| Questioner | 仅来源身份／范围及允许的旧问题文本；不读 Quick、候选知识、旧答案或反馈 / only source identity/scope and allowed prior question text; no Quick, candidate knowledge, old answers or feedback |
| Verifier | 仅候选 skill 与 question-only 问题输入 / only candidate skills and question-only input |
| Coordinator | 核验证据、评分 / check evidence and grade |
| Reader → Author | 已验证修复知识 → 修订；全部已选模块验证后 Author 建 DR 索引 / verified repair knowledge → revision; Author builds DR index after every selected module verifies |

分别报告 Quick 检查与 Deep 状态；Deep 阻塞时报告已完成 Quick 路径／检查与 Deep 阻塞状态，不宣称 Mix 完成。
Report Quick checks and Deep statuses separately; if Deep blocks, report completed Quick paths/checks and blocked Deep state, not Mix completion.

## 来源变化 / Source Changes

所选输入在阶段间变化时停止，询问新来源身份；其他身份的 Quick 输出在刷新／重查前不可复用。不静默混用版本，生成输出不纳入输入监控。
If selected inputs change between stages, stop and ask about a new identity; Quick outputs from another identity are stale until refreshed/rechecked. Never silently mix versions; exclude generated outputs from input monitoring.
