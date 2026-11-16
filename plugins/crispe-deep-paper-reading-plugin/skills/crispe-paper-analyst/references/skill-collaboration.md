# Companion Skills: Discovery, Installation, and Bounded Handoffs / 协作技能：发现、安装与有界交接

## Discovery and availability / 发现与可用状态

The four companions are optional integrations, not unconditional prerequisites. At the first
paper-analysis invocation in a session, check each name with the host skill registry and check
`~/.agents/skills/<name>/SKILL.md` (expand `~`). If not found there, check the host's configured
project/user skill paths, including `~/.claude/skills/<name>/SKILL.md`; resolve symlinks so one
installation is not counted twice. Read the actual definition before using a selected companion.
An absent entry in the loader alone does not mean an existing readable skill is uninstalled.
Do not scan unrelated home directories or load credentials just to inventory skills.

四个协作技能为可选集成，不是无条件前置依赖。会话首次分析时检查宿主注册表及 `~/.agents/skills/<name>/SKILL.md`，不存在再查宿主配置路径（包括 `~/.claude/skills/<name>/SKILL.md`）；解析符号链接去重。使用前读取实际定义；加载器未列出不等于本地未安装。不要为清点技能扫描无关目录或读取凭据。

Distinguish these states:
- **Available:** the host can load it, or its local SKILL.md and required references are readable.
- **Missing:** neither registry nor configured skill paths provide a readable definition.
- **Installed but unusable for this subtask:** a required script, package, tool, network or service
  access fails. Report that specific limitation; reinstalling the skill is not a dependency fix.

区分三种状态：可用（宿主可加载或定义及所需参考可读）；缺失（注册表与配置路径都没有可读定义）；已安装但本子任务不可用（脚本、包、工具、网络或服务失败）。说明具体限制，重装技能不能修复运行依赖。

Check runtime requirements only for the selected subtask. Use existing tools or environments when
suitable, but do not assume globally available Python includes packages from an isolated uv tool.
Do not silently install packages, provision interpreters, configure services or perform paid calls.

只检查选定子任务的运行要求；适当复用现有环境，但默认 Python 不一定包含隔离 uv 工具环境的包。不要静默安装包、配置解释器/服务或调用收费接口。

## Original sources and installation commands / 原始来源与安装命令

Before invoking selected companions, check their installation state. If one is missing, proactively
show its exact command below in a short setup notice before collaborative analysis begins. These are user-level
installs for Claude Code, GitHub Copilot and OpenCode. `github-copilot` is the CLI agent identifier.
Installing skill files does not install dependencies or configure credentials. Execute only if the
user explicitly asks for installation; if they do, recheck discovery before invoking it.

调用选定协作技能前检查安装状态；缺失时在协作分析开始前主动提示下列精确命令。命令为 Claude Code、GitHub Copilot、OpenCode 的用户级安装，Copilot 标识为 github-copilot。技能文件安装不会补运行依赖或凭据。用户明确要求后才安装，安装后重查再调用。

| Skill / 技能 | Expected user-level definition / 用户级路径 | Original GitHub repository / 原始仓库 |
|---|---|---|
| github-deep-research | `~/.agents/skills/github-deep-research/SKILL.md` | `bytedance/deer-flow` |
| literature-review | `~/.agents/skills/literature-review/SKILL.md` | `K-Dense-AI/scientific-agent-skills` |
| paper-lookup | `~/.agents/skills/paper-lookup/SKILL.md` | `K-Dense-AI/scientific-agent-skills` |
| scientific-critical-thinking | `~/.agents/skills/scientific-critical-thinking/SKILL.md` | `K-Dense-AI/scientific-agent-skills` |

```bash
npx skills add bytedance/deer-flow --skill github-deep-research -g -a claude-code -a github-copilot -a opencode
npx skills add K-Dense-AI/scientific-agent-skills --skill literature-review -g -a claude-code -a github-copilot -a opencode
npx skills add K-Dense-AI/scientific-agent-skills --skill paper-lookup -g -a claude-code -a github-copilot -a opencode
npx skills add K-Dense-AI/scientific-agent-skills --skill scientific-critical-thinking -g -a claude-code -a github-copilot -a opencode
```

For a normal paper-analysis request, show commands for selected missing companions in a table:
`skill-name | status | install-code`, then continue the available analysis without waiting for
installation. Explain which checks remain unavailable. For an explicit request to set up the full
collaboration suite, show all four commands and distinguish missing from already installed; do not
instruct the user to reinstall available skills. For example, when GitHub research and paper lookup
are selected but only paper-lookup is missing, show only the K-Dense paper-lookup command before
starting that collaboration. Never silently substitute an install attempt for this notice.
Source packages from these original repositories, not aggregator copies. Current local installation
state is not a fact to hard-code into this portable skill.

普通分析只列本次所需且缺失的技能，以 skill-name / status / install-code 表格提示后继续可做的分析，并说明缺失核查。完整配置请求展示全部四条命令，区分已安装与缺失，不要求重装可用技能。例如仅 paper-lookup 缺失就只显示它的 K-Dense 命令。不能用静默安装代替提示；来源用原始仓库而非聚合副本，不把当前本机状态写死到可移植技能。

## Subtask contract and synthesis / 子任务约定与综合

For each selected companion, supply the target paper ID/version, the specific question, available
paper locators or verified repo URL, allowed source/read scope, date cutoff, and requested evidence
fields. Bring back only claims supported by exact sources, the actual access/read date and scope,
and limitations. Keep one shared evidence table so metadata lookup and synthesis do not repeat
searches or mistake a preprint and its publication for independent studies.

每个协作子任务提供目标论文编号/版本、具体问题、论文定位或已核实仓库地址、允许的来源/阅读范围、日期截止及所需证据字段。只带回有精确来源支持的主张、实际访问/阅读日期和范围及限制。共用证据表，避免重复检索或把预印本及正式版当作独立研究。

Metadata/abstract lookup is allowed for scoped external positioning unless the user restricts it.
Before downloading or reading additional paper full text, name the papers and obtain confirmation;
this includes cited works, follow-ups and papers found by literature-review. Approval for a named
set is sufficient; do not ask again for that set. A supplied/explicitly requested comparison set is
already in scope. Never pass a blanket full-text retrieval instruction to a companion that bypasses
this boundary. Abstract-only evidence cannot establish method-level reproduction or validity.

除非用户限制，可为有限外部定位检索元数据/摘要。下载或阅读额外论文全文前，点名并确认，包括参考文献、后续研究及综述发现的论文；具名集合获批无需重复询问，用户已提供或明确要求的比较集已在范围内。不能向协作技能下达绕过边界的全量全文获取指令；摘要不能证明方法级复现或有效性。

For GitHub checks, use public API/docs without cloning or executing code by default. Label missing
artifacts as not located in the checked sources, not proof they do not exist. Separate numerical
execution, independent reproduction, maintenance activity and real-world adoption. An official
README or author-linked demo does not establish independent adoption.

GitHub 核查默认使用公开 API/文档，不克隆或执行代码。缺失材料表述为在已查来源中未找到，不证明不存在。区分数值执行、独立复现、维护活跃与实际采用；官方 README 或作者演示不证明独立采用。

Retain the analyst report's required first two sections and optional-section dependency rules.
Integrate bounded findings into section 2; only produce a separate full review/repository report
when explicitly requested. Do not let a companion route back to crispe-paper-analyst or recursively
launch the other companions. Use only host-authorized tools and delegation. In offline/paper-only
mode, perform local appraisal, mark external impact unverified and omit irrelevant setup prompts.

保留前两节必需输出与可选节依赖；有限核查合并到第二节，仅明确要求才另产完整综述/仓库报告。避免协作技能回调本技能或递归启动其他技能，只用宿主授权工具及委派。离线/仅论文模式做本地评估，外部影响标未核实，省略无关安装提示。

## Scenario checks when editing these rules / 修改规则时的场景检查

- Local PDF, offline: read the paper and appraise locally; no lookup or GitHub calls, no fabricated
  external adoption, and no installation detour for irrelevant missing companions.
- Current-impact/application request plus verified repo: use lookup for follow-ups, critical thinking
  for the central claim, and GitHub research for maturity; synthesize a sourced PoC/watch/defer verdict.
- Several-paper comparison: reuse lookup records in literature-review; request permission before
  fetching any additional full texts outside the supplied/requested set.
- Missing paper-lookup in a collaboration request: proactively show its K-Dense install command
  before collaborative work, continue paper-based analysis and label current-impact claims unverified;
  do not install, wait for a failure, hide the command in the final report or claim the skill ran.
- Full collaboration setup request: show all four original-repository commands with current
  installation states; already installed companions are marked no reinstall needed.
- Installed literature-review but missing requests: report script dependency failure, use available
  bounded tools/guidance when possible, and do not misclassify it as an uninstalled skill.


场景检查：离线本地 PDF 只做本地阅读与审查，不查外网、不捏造采用、不为无关技能打断安装；影响/落地请求结合检索、证据审查和已核实仓库调查，产出有来源的 PoC/观察/暂缓判断；多论文比较复用检索记录，额外全文先确认；协作缺失 paper-lookup 时先显示原始 K-Dense 命令，再做可用分析，不静默安装、等待失败或声称已运行；完整配置列四条命令与状态；已安装 literature-review 但缺 requests 时说明运行依赖，不误判未安装。
