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

## Code-window reference / 代码窗口参考
Reviewed [Prism's official documentation](https://prismjs.com/) for semantic `pre > code.language-*`, token classes, toolbar/copy and line-highlighting conventions. The bundled window uses those general presentation conventions with a small original offline Python/JSON lexer and source-only copy logic, rather than a CDN or vendored Prism implementation. Unknown languages remain escaped plain code. Highlighting is presentation, not a syntax validator.
检查 Prism 官方文档的语义 pre/code、语言标识、token 高亮、工具栏/复制及行高亮约定。内置窗口借鉴通用呈现方式，采用自行编写的离线 Python/JSON 词法着色与纯源码复制，不引入 CDN 或复制 Prism 实现。未知语言保留转义纯文本；高亮不等于语法校验。
