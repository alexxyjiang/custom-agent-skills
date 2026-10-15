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
