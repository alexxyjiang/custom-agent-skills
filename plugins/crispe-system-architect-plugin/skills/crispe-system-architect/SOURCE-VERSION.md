# 来源版本 / Source Version

遵循 SKILL.md「分析排除项」：来源枚举、未提交清单及证据阅读先过滤 VCS／托管配置路径；不将其视为模块或来源证据。
Apply SKILL.md Analysis Exclusions before source/dirty-path enumeration and evidence reads; excluded VCS/hosting paths are neither modules nor evidence.

遵循 [SKILL.md](./SKILL.md) 通用规则。来源身份由 Git 基线和获准工作区快照构成；时间不替代内容标识。
Follow shared rules. Source identity combines the Git baseline and approved overlays; timestamps are not content identity.

## Git 基线 / Git Baseline

- 检查当前完整 commit ID（`git rev-parse HEAD`）；Deep/Mix 列出合理 tag/branch、推荐 ref 并单独确认，再解析完整 commit。Quick 默认当前 HEAD，来源不明时询问。
  Inspect full HEAD; confirm a recommended ref for Deep/Mix and resolve its commit. Quick uses HEAD unless another version is requested; clarify unknown sources.
- 本地仓库不 checkout、不改工作区；通过 `git ls-tree -r --name-only <commit>` 和 `git show <commit>:<path>` 读取。已提交内容直接依赖 Git，不重复计算逐文件哈希；timestamp 记录带时区采集时间。缺少必要 Git 证据时询问，不虚构版本。
  Read pinned Git objects without checkout; no duplicate hashes for clean committed files. Capture timestamps with timezone; missing required Git evidence is a blocker to clarify.
- URL 克隆前确认位置、检查已有路径；不从未确认的 skills 目录推定克隆位置，不删除已有 checkout。
  Confirm URL checkout location and inspect existing paths before clone; never infer it from an unconfirmed output or destroy an existing checkout.

## 未提交内容 / Uncommitted Inclusion

1. 检查 staged/unstaged、删除、重命名及未跟踪路径，如 `git status --porcelain=v1 -uall` 与相关 diff。按真实职责分 Code（含测试／脚本）、Doc、Config、Other；分类不明先问，ignored 文件仅明确批准后纳入。
   Inspect index/worktree changes, deletions, renames and untracked files. Classify by semantics, not extensions; clarify ambiguity and require approval for ignored files.
2. 展示每类路径与状态，一次确认一类，等待回答，允许逐文件例外；无变更类别不用问。staged 与 worktree 不同则确认采用哪个，不整体默认纳入／排除。
   Ask one changed category at a time with path/status and exceptions; clarify index/worktree differences, never blanket-include or exclude dirty content.
3. 纳入内容复制为不可变快照，删除为 tombstone，重命名记录旧／新路径；未纳入 tracked 变更使用 Git 基线，未纳入 untracked 不存在于本次来源。部分重命名或矛盾选择先确认再建快照。
   Approved content overrides Git through snapshots; record tombstones and both rename paths. Rejected tracked changes use Git, rejected additions are absent; resolve partial/conflicting selections first.

## 私有清单 / Private Manifest

存入已确认的私有运行目录，位于发布 skill 外，优先源码仓外；使用 SOURCE-MANIFEST.json / SOURCE-SNAPSHOT/ 等大写名称，不发布原始快照。
Use confirmed private run storage outside published skills, preferably outside source; do not publish snapshots.

| 字段 / Field | 内容 / Content |
| --- | --- |
| 来源 / Source | repo 路径／URL、ref、完整 commit / repo path/URL, ref, full commit |
| 采集 / Capture | 带时区 captured_at、类别／路径选择 / zoned timestamp and category/path decisions |
| 覆盖 / Overlays | repo 相对路径、状态、index/worktree 选择、快照路径、准确字节 SHA-256；删除无内容 / path, status, selected version, snapshot/hash or tombstone |
| 范围 / Scope | 分析范围、生成输出排除项、manifest identity/hash / scope, output exclusions and manifest identity/hash |

Reader、Documenter、Questioner 与 Coordinator 均使用同一 Git／快照解析器和准确行号。Questioner 仅获来源身份／清单／快照，不获分析、生成文档、答案或评分。
All source evidence uses one resolver and exact ranges. Questioner receives source identity/manifest/snapshot only, not analysis, docs, keys or grades.

## 新鲜度与冻结 / Freshness and Freezing

- 使用前校验快照，在阶段／考试边界检查所选输入；相关内容变化则停止并确认新身份。ref 移动不自动切换 commit；排除内容不自动生效，生成产物／记录不属于本轮输入。
  Validate snapshots and selected inputs at boundaries; relevant changes require stopping and confirming a new identity. Pin refs; excluded changes and outputs do not become inputs.
- 每轮候选全部 skill／支持文件考试前后计算 SHA-256，按 DEEP-MODE.md 处理修改失效与有限修复。来源清单改变须重新一致分析，不复用旧成绩。
  Hash all candidate files before/after exams; apply Deep invalidation bounds. Source-manifest changes require consistent reanalysis, not old grades.
