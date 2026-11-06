# 部署 / Deployment

适用于新 repo-specific skill；工具自身保持已有位置。遵循 [SKILL.md](./SKILL.md) 命名与语言规则。
Applies to generated repo-specific skills, not relocation of this tool; follow shared naming/language rules.

## 路径选择 / Paths

先检查项目约定，一次确认实际目录；推荐 `<repo>/.agent/skills/`，未确认不写入。明确自定义路径优先，并确认发现映射；只有显式选择才启用方式 2。
Inspect conventions and confirm actual paths before writing. Custom paths require discovery mapping; option 2 requires explicit selection.

| 方式 / Option | 模块 skill / Modules | DR 索引 / Index |
| --- | --- | --- |
| 1（默认 / default） | `<repo>/.agent/skills/<project>-dr-<module>/` | `<repo>/.agent/skills/<project>-dr/` |
| 2（仅索引全局 / index-global） | 同项目路径 / same project storage | `~/.agent/skills/<project>-dr/` |

全局索引仍专属该 repo，记录路径／URL、来源身份和实际模块路径；不授予外部目录权限。移动／失效路径应报告。
Global indexes remain repo-specific and carry actual locations/source identity; they grant no filesystem access. Report stale paths.

## 兼容发现 / Discovery

`.agent/skills/` 只是存储，通过逐 skill 相对目录软链暴露：
Storage alone is not discovery; expose per-skill relative directory links:

```text
<repo>/.claude/skills/<name> -> ../../.agent/skills/<name>
~/.claude/skills/<name>      -> ../../.agent/skills/<name>
```

- 两个 host 均发现 `.claude/skills/`；Claude Code 支持 skill 软链，OpenCode 在已装版本实际核对。若不支持，先确认再按当前 schema 配置 `skills.paths`；不将文件存在等同加载成功。
  Check host discovery, not just paths. If OpenCode link discovery fails, confirm schema-valid `skills.paths` configuration before editing it.
- 创建前检查父目录、路径、软链、归属和同名冲突；保留已有 native 入口，不覆盖未知内容。name 与目录一致。
  Inspect parents, targets, ownership and collisions; preserve existing entries and never overwrite unknown contents.

## 发布与检查 / Publication

候选在发现目录外生成和验证，已有版本保持可用；通过后 Coordinator 按冻结清单和哈希发布，处理已拥有的过时支持文件，再更新软链。核对解析目标、支持／模块引用及实际 host 列表；host 不可用则注明未做加载验证。
Verify private candidates before replacing deployed content; publish exact inventories/hashes and reconcile obsolete owned supports, then links. Check targets/references and available host listings; report unavailable checks.

OpenCode 需重启加载；Claude Code 可刷新，新顶层目录可用 `/reload-skills`。含生成 skill／文档的 checkout 是部署位置，须保留；另行确认迁移并修复引用后才考虑删除。原始快照、题库、答案和成绩不发布。
Restart OpenCode; Claude Code can reload. Retain checkouts containing deployed outputs unless separately confirmed relocation repairs references. Keep source snapshots/exam records private.
