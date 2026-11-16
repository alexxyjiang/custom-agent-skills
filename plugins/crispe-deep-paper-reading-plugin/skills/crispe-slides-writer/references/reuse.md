# Reuse decisions / 复用决策

Inspected on 2026-11-16; counts are discovery snapshots, not quality guarantees.
检索日期 2026-11-16；安装数仅当时快照，不代表质量保证。

| Candidate / 候选 | Observed capability / 已核查能力 | Decision / 决策 |
|---|---|---|
| [frontend-slides](https://skills.sh/zarazhangrui/frontend-slides/frontend-slides), source `zarazhangrui/frontend-slides` (1.2K installs, directory showed 32.3K stars) | Read actual upstream SKILL.md: standalone HTML, 1920×1080 fixed stage, style previews and browser checks / 已读原定义，独立 HTML、固定画布、预览与浏览器检查 | Optional general presentation companion; its mandatory font/style discovery and 1920 stage differ from this supplied 1600 template; keep custom writer / 可选通用演示协作，字体/选风格/画布规则不直接套用 |
| [frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | Actual source says user-specified design wins / 原定义明确用户设计优先 | Optional visual critique, not paper analysis or evidence navigation / 可辅助视觉评审，不承担论文证据编排 |
| Local `scientific-slides` in scientific-agent-skills | Reviewed actual definition: research talks, PPTX/Beamer/image-PDF, optional OpenRouter / 已核查，主攻演讲/PPTX/Beamer/图片 PDF | Reuse narrative/figure fidelity guidance; not HTML reading renderer / 借鉴叙事及原图保真，不替代 HTML 生成 |
| `ai-research-explore`, `lllllllama/rigorpilot-skills` (359.9K installs, directory showed 486 stars) | Actual published excerpt requires research anchor and candidate authorization, targets experimental research / 定义面向研究候选与实验 | Not a bounded paper-reading orchestrator / 不直接承担阅读范围编排 |

Use original sources for optional installs, only on user request. The working default needs none of these. No upstream code or skill prose was vendored.
可选安装用原始来源，仅应用户请求执行；默认无需以上依赖，未复制第三方代码或技能正文。

```bash
npx skills add zarazhangrui/frontend-slides --skill frontend-slides
npx skills add anthropics/skills --skill frontend-design
```

## Rendering dependencies / 渲染依赖
PrismJS 1.30.0 (official npm prismjs archive) now performs actual full-block tokenization for Python, JSON, JavaScript, Bash and SQL; unknown languages remain escaped plain code. The bundled Tomorrow theme is adapted by component styles; retain exact source and line wrappers. KaTeX 0.16.22 plus its auto-render extension and WOFF2 fonts renders prose formulas. These are vendored MIT-licensed distributions, not CDN requests; package URLs, SHA-256 digests and file lists are recorded in `assets/vendor/manifest.json`. Python build/runtime still uses only the standard library.
PrismJS 1.30.0真实执行整块代码分词，内置上述语言，其他语言转义纯文本；Tomorrow主题按组件调整并保留精确源码和行包装。KaTeX 0.16.22及auto-render/WOFF2字体渲染公式。依赖为随包MIT发行版而非CDN；包地址、哈希和文件见vendor清单；Python构建仍仅需标准库。

Official API references / 官方接口参考：[KaTeX auto-render](https://katex.org/docs/autorender)、[Prism token API](https://prismjs.com/extending.html)。
