# custom-agent-skills

My custom agent skills, published two ways from one source of truth:

- as a **Claude Code plugin marketplace** (`plugins/`), and
- as a plain **[`npx skills`](https://vercel.com/docs/agent-resources/skills)** skill repo (`skills/`).

Each skill is authored once inside its plugin under `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`.
The top-level `skills/` directory is a set of symlinks into those same files, so both
install paths always stay in sync -- there's nothing to keep manually updated.

```
.
├── .claude-plugin/
│   └── marketplace.json          # Claude Code marketplace manifest
├── plugins/
│   └── <plugin-name>/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
│           └── <skill-name>/
│               └── SKILL.md      # source of truth
└── skills/
    └── <skill-name> -> ../plugins/<plugin-name>/skills/<skill-name>  # symlink
```

## Install via Claude Code plugin

```
/plugin marketplace add alexxyjiang/custom-agent-skills
/plugin install <plugin-name>@custom-agent-skills
```

See `.claude-plugin/marketplace.json` for the list of available plugins.

## Install via `npx skills`

```bash
# install a specific skill
npx skills add alexxyjiang/custom-agent-skills --skill <skill-name>

# install all skills
npx skills add alexxyjiang/custom-agent-skills --skill '*'

# target a specific agent (claude-code, cursor, codex, etc.)
npx skills add alexxyjiang/custom-agent-skills --skill <skill-name> -a claude-code
```

See `skills/` for the list of available skill names.

## Deep paper reading / 深度论文阅读

A bilingual workflow for bounded paper discovery, full-paper analysis with teaching functions,
evidence-backed cross-paper links, and offline HTML reading slides.
双语工作流覆盖有界检索、带教学函数的全文分析、跨论文证据连接及离线 HTML 精读页面。

All four skills are bundled under `plugins/crispe-deep-paper-reading-plugin/skills/`:
`crispe-deep-paper-reading`, `crispe-paper-analyst`, `crispe-paper-cross-link`, and `crispe-slides-writer`.
四个技能统一打包在 `crispe-deep-paper-reading-plugin`，顶层 `skills/` 符号链接仍支持单独安装。

```text
/plugin install crispe-deep-paper-reading-plugin@custom-claude-skills
```

- [Workflow and usage / 工作流与使用](docs/paper-reading/README.md)
- [Validation / 验证记录](docs/paper-reading/VALIDATION.md)
- [Language entry / 语言入口](examples/deep-paper-reading/site/index.html)
- [中文示例](examples/deep-paper-reading/site/zh-CN/index.html)
- [English example](examples/deep-paper-reading/site/en-US/index.html)
