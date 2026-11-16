# Discovery and original-source reuse / 技能发现与原始来源复用

## Discovery / 发现

Check the host registry/skill loader first and host-configured project/user skill roots next. Resolve symlinks and use the actual readable `SKILL.md` plus only references required by the subtask; loader absence alone is not proof of missing installation. Common roots such as `~/.agents/skills` or `~/.claude/skills` are optional fallbacks, not prerequisites. Do not hardcode a particular user's absolute path or scan unrelated directories. Resolve scripts relative to the loaded skill, not this skill.
先查宿主注册表/加载器，再查宿主配置的项目/用户技能根目录；解析符号链接，读取实际定义及本子任务必需参考。加载器未列出不等于缺安装。常见目录只是可选回退，不是前提，不写死某用户绝对路径、不扫无关目录；脚本相对所加载技能解析。

For scientific companions, optionally check a user-configured scientific-skills checkout, or `~/OpenProjects/scientific-agent-skills/skills/<name>/SKILL.md` if present (also allow `<checkout>/<name>/SKILL.md` when that is the checkout layout). This is a local read-only reuse source, not a required clone, installation destination or proof of runtime capability. On this task, literature-review and citation-management are partially reusable for synthesis and bibliographic identity; neither supplies this contract's typed claim graph plus HTML navigation.
科学协作技能可选查用户配置检出目录，或存在时查 `~/OpenProjects/scientific-agent-skills/skills/<name>/SKILL.md`（若布局如此也支持根下 `<name>/SKILL.md`）。该路径仅为本地只读复用来源，不是必需克隆、安装目标或运行能力证明。本任务中综述及引用管理可部分复用综合与书目信息，但都不提供本约定的有类型主张图及 HTML 导航。

Record `available`, `missing`, or `installed-but-unusable` with a concrete reason. File presence does not imply scripts, packages, credentials or network work. Load selected definitions before invoking them. Do not recursively route skills back into the orchestrator; use same-agent role execution unless authorized delegation is available.
记录可用、缺失、已安装但不可用及具体原因。文件存在不代表脚本/包/凭据/网络可用；调用前读选中定义，避免递归回调编排器。没有获准且可用的委派则同一智能体顺序执行。

## Original repositories / 原始仓库

| Skill / 技能 | Role / 职责 | Original source / 原始来源 |
|---|---|---|
| crispe-paper-analyst | Full-paper reading/report / 全文阅读及报告 | alexxyjiang/custom-agent-skills |
| crispe-paper-cross-link | Typed evidence graph/navigation / 类型证据图与导航 | alexxyjiang/custom-agent-skills |
| crispe-slides-writer | Presentation authoring/integration / 呈现写作集成 | alexxyjiang/custom-agent-skills |
| literature-review | Bounded synthesis / 有界综合 | K-Dense-AI/scientific-agent-skills |
| citation-management | Metadata identity, deduplication and citations / 元数据身份、去重与引用 | K-Dense-AI/scientific-agent-skills |
| paper-lookup | Scoped scholarly lookup/provenance / 限定学术检索及来源 | K-Dense-AI/scientific-agent-skills |
| scientific-critical-thinking | Claim validity, comparability and independence / 有效性、可比性及独立性 | K-Dense-AI/scientific-agent-skills |

For selected missing skills, show a short `skill | status | original-repository install command` notice before collaborative work. Construct the exact command by replacing `<name>` with the table's skill name; do not show unresolved placeholders to the user. For example:
选中的协作技能缺失时，协作前简短提示技能、状态和原始仓库安装命令。将下列 `<name>` 替换为表中名称，向用户展示时不能留占位符。例如：

```bash
npx skills add alexxyjiang/custom-agent-skills --skill crispe-paper-analyst -g -a claude-code -a github-copilot -a opencode
npx skills add alexxyjiang/custom-agent-skills --skill <name> -g -a claude-code -a github-copilot -a opencode
npx skills add K-Dense-AI/scientific-agent-skills --skill citation-management -g -a claude-code -a github-copilot -a opencode
npx skills add K-Dense-AI/scientific-agent-skills --skill <name> -g -a claude-code -a github-copilot -a opencode
```

Only show the command matching the actual selected missing skill and original repository. Do not install, update installed copies, change configuration or provision dependencies without an explicit user request. Available skills need no reinstall; unusable ones need a precise runtime limitation rather than a misleading reinstall notice. Continue feasible work with transparent gaps; never claim an unavailable companion ran.
只展示实际选中且缺失技能的对应原始仓库命令；未经用户明确要求不安装、不更新已安装副本、不改配置或配依赖。可用无需重装；不可运行须说明具体依赖限制而非误导重装。可做工作继续并披露缺口，不能声称运行了不可用技能。

Every handoff carries the question, exact named/versioned approved set, remaining metadata/full-text budgets, stop criteria, exclusions, existing artifacts and expected evidence/locators. Companion defaults cannot override these constraints. Check for automatic full-text retrieval, citation expansion, code execution or paid generation and keep those outside the subtask unless already authorized.
每次交接传问题、精确具名版本授权集、剩余预算、停止条件、排除项、已有产物和所需证据/定位；协作默认不能覆盖范围。检查自动取全文、扩引用、执行代码或付费生成行为，未经授权不纳入子任务。

## Already assessed alternatives / 已评估替代项

`rigorpilot`'s `ai-research-explore` is experimental candidate discovery, not a reading orchestrator. `frontend-slides` is generic presentation, not an analyst→cross-link→writer reading chain. They are not required dependencies or substitutes for evidence/approval checkpoints. Do not repeat this research unless the user requests updated discovery.
`rigorpilot` 的 `ai-research-explore` 是实验性候选发现而非阅读编排；`frontend-slides` 是通用呈现而非分析师→互链→写作链。二者不是必需依赖，也不替代证据/授权检查点；除非用户要求更新发现，否则不重复调研。
