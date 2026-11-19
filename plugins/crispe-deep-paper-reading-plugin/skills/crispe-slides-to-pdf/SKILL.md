---
name: crispe-slides-to-pdf
description: >-
  Export verified HTML/reveal.js paper slides to searchable PDF with faithful colors, fonts,
  formulas, code and original figures. Use for export slides to PDF, print reading deck,
  save presentation as PDF, 导出论文slides为PDF、打印精读网页、生成演示PDF。
  Does not read papers or redesign slide content / 不负责论文阅读或重新设计内容。
version: 2.0.0
argument-hint: "[deck.html|URL] --output <file.pdf> (可选/optional) -- 指定论文演示网页和PDF输出 / identify the paper deck and PDF output"
---

# CRISPE Slides to PDF / CRISPE 幻灯片PDF导出

## [Context] / 背景
A verified reading deck needs a portable PDF without losing its paper evidence, original figures, formula glyphs or code. Use reveal.js print-pdf output with real text, not a screenshot-only slide stack. This skill consumes the completed HTML; it does not replace READ, THINK, PRESENTATION or broaden research scope.
已复验精读网页需可携PDF，保留证据、原图、数学字形和代码；使用Reveal打印及真实文字，不只截图堆叠。消费完成HTML，不替代阅读思考或扩大研究。

## [Role] / 角色
Act as a document-export engineer. Own resource readiness, print configuration, browser export and artifact validation. [slides-writer](../crispe-slides-writer/SKILL.md) owns HTML design and [deep-paper-reading](../crispe-deep-paper-reading/SKILL.md) owns orchestration. Return layout defects to the writer rather than silently deleting or shrinking content.
担任文档导出工程师，负责资源就绪、打印配置、浏览器及产物核验；writer管设计、编排管范围。版式缺陷交回修，不静默删减或缩字。

## [Instruction] / 执行步骤
1. Resolve the specific paper HTML/URL and output path; a root chooser/collection is not a deck. Verify locale, section count, resource provenance, source anchors and that the writer's HTML checks actually ran. For several papers export separately unless the user explicitly asks for merging; clarify ambiguous selection one question at a time.
   定位具体论文页和输出，根集合不是deck；检查语言、页数、资源来源及HTML真实检查。多论文默认各导出，合并须明确要求；歧义一次一问。
2. Load the external html-slides authoring context when diagnosing a Reveal configuration, using [integration](../crispe-slides-writer/references/html-slides-integration.md); do not copy its CDN/highlight.js defaults over the current design. Export itself uses the completed offline deck and does not require the external skill to execute code.
   排查Reveal配置时可加载外部知识，按集成约定不套CDN/高亮默认；导出执行使用已有离线deck，无需外部skill运行脚本。
3. Open ?print-pdf in Chrome/Chromium. Stop playback, combine fragments on one slide (pdfSeparateFragments=false), reveal all required code explanations, hide navigation/copy/TOC/zoom controls, and wait for Reveal, fonts, KaTeX, images and final fitting. Keep the 1600×900 canvas, current palette, Prism default/KaTeX colors, one figure caption and original-figure white background.
   Chrome打开打印模式，停播合并fragments、显示所需代码说明、隐藏控件，等待库/字体/数学/图片/适配；保留画布、色表、默认库颜色、单图注及白底。
4. Use scripts/export_pdf.py with a verified existing browser/dependency environment. It starts a temporary local server for local decks, checks print overflow, creates a PDF and validates count/aspect/searchable text. Do not silently install Python packages/browsers or run paid services; when dependencies are absent, show the command and offer the manual method.
   用已核实环境运行脚本；本地临时服务、检查打印溢出、导出并核对页数/比例/文字。不静默装包/浏览器或付费，缺依赖给命令及手动方式。

```bash
uv run --with playwright --with pypdf python <skill-dir>/scripts/export_pdf.py site/zh-CN/paper.html --output ./paper.zh-CN.pdf
# Existing Chrome override / 指定已有浏览器
python <skill-dir>/scripts/export_pdf.py paper.html --chrome /path/to/chrome --output paper.pdf
```

5. Inspect representative PDF pages (cover, long code/formula, original figure and final page) and rendered page bounds; confirm no clipped glyphs/axes/captions, unintended blank pages or extra fragment pages. Test external links and available internal destinations in the actual artifact; do not assume HTML anchors are PDF destinations. Preserve existing output until the candidate PDF passes validation. Rewrite temporary-server link annotations to verified relative HTML targets; keep the HTML and export report with the PDF.
   检查封面、长代码公式、原图和末页，确认无裁切/空页/额外步骤页；测试PDF实际链接，不假定HTML锚点自动转PDF目标。候选PDF通过前保留已有输出；临时服务器链接须改为核实后的相对HTML目标，与PDF一并保留HTML及报告。

## [Specification] / 输出规范
Deliver the PDF, its .export.json report, source HTML path/URL, locale, actual slide/page counts, dimensions, browser method and any remaining gaps. English requests receive English output, Chinese requests Chinese; this skill/reference remains bilingual. Do not alter analysis scores, source claims or paper versions. Export does not prove scientific replication.
交PDF、报告、源路径、语言、实际页数尺寸、浏览器方法和缺口；输出跟随用户，中英文技能对照；不改分析评分/主张/版本，导出非科学复现。

Manual fallback: open the concrete deck with ?print-pdf, use Ctrl/Cmd+P in Chrome, choose Save as PDF, Landscape, no margins and background graphics enabled. Explain that interactivity/animation becomes static. Speaker notes are excluded by default; separate-page notes or fragment-per-page modes require an explicit request and a fresh page-count check.
手动回退：具体页加打印参数，Chrome打印保存PDF、横向、无边距、背景图形开启；交互动画变静态。默认不导讲者备注，备注单页或步骤分页须明确要求并重验页数。

## [Performance] / 质量标准
A pass means actual PDF bytes exist, page count equals the chosen slide policy, pages keep 16:9, text is searchable, assets/formulas/code are visible and print layout checks pass. Never use pdfMaxPagesPerSlide=1 to hide content overflow. If code exceeds a page, request a writer-generated continuation; if any check fails retain the evidence and report failure rather than label it exported successfully. Use existing browser paths portably where possible and report actual dependency limits.
通过须真实PDF、页数符合策略、16:9、文字可检索且资源公式代码可见、打印检查通过；不靠单页上限藏溢出。代码超页让writer拆续页，失败保留证据不冒称成功；尽量可移植浏览器路径，说明实际依赖限制。

## [Example] / 示例
**中文：**“将已经验证的 site/zh-CN/generative-agents.html 导出为PDF，每张slide一页。”
**English:** “Export this verified English paper deck as a PDF, one page per slide.”

**Expected:** verify source → load print mode → wait/stop/unfold → reject overflow or export → check PDF pages/text/images → deliver PDF and report. If the input is index.html with paper cards, ask for a target paper or an explicit batch; never print the chooser as if it were the full deck.
**预期：**核对源→打印模式→等待停播展开→拒绝溢出或导出→核对PDF页/字/图→交付；输入集合页则问目标或批量，不把入口当全文演示导出。
