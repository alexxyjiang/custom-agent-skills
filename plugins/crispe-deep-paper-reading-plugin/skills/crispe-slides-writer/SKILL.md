---
name: crispe-slides-writer
description: >-
  Generate reading-first, evidence-linked HTML paper slides and collection websites from analyzed papers,
  including worked examples and step-by-step code. Use for paper slides, paper-reading websites,
  turn this analysis into slides, or match a supplied reading template. 生成论文精读幻灯片、论文阅读网页、
  把分析做成 slides、按模板生成论文网页；支持中文与英文。 Consumes analysis; does not replace full-paper reading.
  消费已完成的分析，不代替全文阅读；普通 UI 开发、单纯论文总结或 PPT 转换不触发。
version: 1.4.1
argument-hint: "[project.<locale>.json路径 / project.<locale>.json-path] (可选/optional) -- 指定论文分析项目；可附模板路径、输出目录及中英文要求 / specify an analyzed-paper project, optional template path, output directory and Chinese/English preference"
---

# CRISPE Slides Writer / CRISPE 精读网页写作

## [Context] / 背景
Turn completed paper analysis into a reading-first website: topic collection → paper narrative → worked example → mechanism/code → evidence appendix. Readers need a coherent explanation with original-result boundaries, not a document pasted onto slides.
把已完成分析转成阅读优先网页：主题集合→单篇叙事→实例→机制/代码→证据附录；读者需要连贯讲解及原始结果边界，而非把文档直接贴到幻灯片。

### READ, THINK, PRESENTATION / 先阅读，再思考，后呈现
Use the exact site slogan `READ, THINK, PRESENTATION`. Read the approved source material first; think through mechanisms, evidence, comparisons and limitations next; only then organize the verified understanding into self-contained slides. Presentation is the result of reading and reasoning, never a substitute for them or a template-first summary of an abstract.
站点slogan固定为上述文字。先阅读获批原始材料，再思考机制、证据、比较与局限，最后将核实后的理解组织为可独立阅读的slides。呈现是阅读与思考的产物，不能以模板填充或摘要改写代替理解。

## [Role] / 角色
Act as a technical presentation author and interaction designer. Own narrative, template adaptation, accessible navigation and deterministic site generation; the analyst supplies claims/scores and cross-link supplies typed relationships. Never invent missing research to fill a layout.
担任技术演示作者与交互设计者，负责叙事、模板适配、可访问导航和确定性生成；分析师提供主张/评分，互链技能提供类型关系。不得为填版面补造研究。

## [Instruction] / 执行步骤
1. Read [references/design.md](references/design.md) and [references/contracts.md](references/contracts.md). Locate analyzed reports, claim locators, code execution records and figure assets. Missing analysis goes back to `crispe-paper-analyst`; an absent source stays a visible gap. Never silently fetch more full texts.
   阅读设计规则和契约，定位分析报告、主张定位、代码执行记录和图片。缺分析交给 analyst，缺证据明确标注，不静默获取更多全文。
2. If a local template is supplied, inspect its index and at least two representative paper pages, including code, evidence and navigation behavior. Record design tokens and source commit. If unavailable, use bundled assets; no hardcoded home-directory dependency. See [references/reuse.md](references/reuse.md) for evaluated online/local alternatives.
   有本地模板时检查索引和至少两篇代表页面，覆盖代码、证据及导航，记录设计变量与来源版本。不可用则用内置资源，不依赖固定个人路径。复用评估见参考。
3. Plan one claim or question per slide. Start with a concrete case, advance its state through mechanism and code, then test against original results and limitations. Every index.html paper card must show its evidence-based numeric 1–4 analyst score; missing/null/deferred scores fail publication. Keep the existing calibration and disclose reading gaps separately. Preserve complete report separately; optional background/formula sections follow analyst rules.
   每页一个主张或问题；从具体案例出发，经机制和代码推进状态，再核对原始结果与局限。index.html 每张论文卡片必须展示有依据的 1–4 数值评分，不接受缺失/空值/暂缓；保留原量表，阅读缺口另列。保留阅读顺序，完整报告单独保留；概念/公式依 analyst 规则选择。
4. Author `slides` in `project.<locale>.json`, referencing existing claims/examples. Code steps use exact 1-based line numbers and explain input → operation → state/output. Display teaching/original/reproduction and execution status. Wrap code, JSON and execution logs in labelled semantic pre/code windows with syntax highlighting, source-only copy buttons and bounded scrolling. Figures retain source URL, page/section/figure locator, alt and caption; use relative assets. Add an appendix for original evidence, and typed cross-paper links from `crispe-paper-cross-link`.
   在 project.<locale>.json 编写 slides，引用已有主张/实例。代码步骤按真实一基行号映射输入、操作与状态；显示教学/原始/复现性质及执行状态；代码、JSON 和运行日志统一用带语言标签、语法高亮、纯源码复制按钮及有限滚动的 pre/code 窗口。原图保留来源、定位、替代文字和图注，用相对资源。加入证据附录及 cross-link 的类型化跨论文连接。
5. Run the deterministic builder below from the resolved installed skill path. It validates links/claim IDs/line mappings, escapes text, embeds local images, and produces portable HTML; it neither reads papers nor executes supplied code. On validation failure fix input, not the research evidence to fit a layout.
   从实际安装目录运行下列确定性生成器；它校验链接、主张和行号、转义文本、嵌入图片并生成可移植 HTML，不负责读论文或执行代码。校验失败修正输入，不为排版改研究证据。

```bash
python3 <skill-dir>/scripts/build_site.py project.zh-CN.json --translation project.en-US.json --output ./site
# Validate without writing / 仅校验
python3 <skill-dir>/scripts/build_site.py project.zh-CN.json --check
python3 -m http.server 8000 --directory ./site
```

6. Review every slide at 1600×900 and 1280×720 plus a phone viewport. Verify opt-in autoplay with 5s/15s/30s/1min per page, speed changes, pause/resume, dialog/hidden-tab holds and last-page stopping. Check card/code overflow, image loading, TOC keyboard focus/Escape, arrows/Home/End, hash links, step highlights, collection return and cross-paper target anchors. Split overloaded slides instead of shrinking text. Optional browser tooling is not a mandatory runtime dependency; report unperformed visual checks honestly.
   在桌面及手机视口检查每页，核对主动开启的自动播放、每页5s/15s/30s/1min、变速、暂停/恢复、对话框/隐藏页签阻止推进及末页停止；检查溢出、图片、目录键盘焦点/Escape、翻页/Home/End、深链接、代码高亮、返回索引及跨论文定位。过密就拆页，不缩字。浏览器测试工具是可选验证依赖，未执行视觉检查如实说明。

## [Specification] / 输出规范
Deliver locale-qualified bundles (`project.zh-CN.json`, `project.en-US.json`), source reports/examples, `site/index.html` language entry, `site/<locale>/index.html`, one `site/<locale>/<paper-id>.html` per paper, and a validation summary with actual command results. The site works via `file://` and local HTTP, without remote font/CDN requests, API keys or JavaScript build tools. Do not copy the template's paper content into reusable assets or generatively redraw quantitative results.
交付契约文件、报告/实例、根语言入口、对应语言目录中的集合索引及每篇 HTML 和真实验证摘要。网页支持本地直接打开或 HTTP，无需远程字体/CDN请求、API Key或JavaScript构建工具。不要把模板论文内容写死到资源，也不要用生成图片重画定量结果。

### Language and directories / 语言与目录
Follow an explicit output-language request, otherwise mirror the user (bare identifiers inherit conversation language; Chinese only if no signal). Keep identifiers, symbols and paper titles stable. This bilingual skill does not force duplicate bilingual slides. For English output translate narrative, examples, evidence limitations and logs as well as interface labels. Deliver a fully English example bundle, not Chinese prose under English headings. Use separate zh-CN/en-US bundles and optional reciprocal language links.
指定语言优先，否则跟随用户（纯编号沿用会话语言，无线索才回退中文）。标识符、符号与论文标题保持稳定。双语技能不强制每页重复两种语言；英文输出须翻译叙事、实例、证据局限和日志，而非只有标题英文；使用独立 zh-CN/en-US 项目包及可选双向语言切换。

Write this skill and its explanatory references in paired Chinese and English. Currently support only zh-CN and en-US output; do not add another documentation or output language. Generated websites use root index.html as the language entry: single-locale builds redirect to that locale with a visible fallback, while bilingual builds show both language choices. Chinese collection/deck pages live under zh-CN/ and English pages under en-US/. Any future approved locale must follow the same locale-directory convention.
本技能及说明性参考文档保持中文、英文对照。目前仅支持 zh-CN 和 en-US，不新增其他文档或输出语言。根 index.html 为语言入口：单语言跳转至对应语言并保留备用链接，双语显示两种选择；中文集合/论文页放 zh-CN/，英文放 en-US/；未来获准增加语言时也按地区语言目录组织。

### Generation credit / 生成署名
Every generated index.html (root entry and locale collections) must visibly credit crispe-deep-paper-reading and link to https://github.com/alexxyjiang/custom-agent-skills/tree/master/plugins/crispe-deep-paper-reading-plugin using only “Generated with [crispe-deep-paper-reading]” (or its Chinese equivalent). Match the generated page language; an English-only build has English-only credit, a Chinese-only build Chinese-only, and a bilingual entry credits both. Keep skill documentation Chinese/English paired.
所有生成的 index.html（根入口及语言集合）必须可见地注明由 crispe-deep-paper-reading 生成，仅用“由 [crispe-deep-paper-reading] 生成”并链接到 https://github.com/alexxyjiang/custom-agent-skills/tree/master/plugins/crispe-deep-paper-reading-plugin。署名跟随生成语言；仅英文则只用英文，仅中文则只用中文，双语入口两种都展示。技能文档仍保持中英文对照。

### Typography, mathematics and code / 字体、公式与代码
Use UI/title/control fonts in order: Iosevka Aile → Noto Sans CJK SC → sans-serif; prose: Iosevka Etoile → Noto Serif CJK SC → serif; code: IosevkaAlexJiang → Noto Sans Mono CJK SC → monospace. These are local fallback stacks, not remotely downloaded fonts. Keep KaTeX's bundled math fonts for mathematical glyph metrics.
标题/界面/控件字体依次使用Iosevka Aile、Noto Sans CJK SC、sans-serif；正文依次Iosevka Etoile、Noto Serif CJK SC、serif；代码依次IosevkaAlexJiang、Noto Sans Mono CJK SC、monospace。均为本地回退，不远程下载字体；数学字形保留KaTeX配套字体以保证度量。

Render authored prose formulas with bundled KaTeX using `\(…\)` inline and `\[…\]` or `$$…$$` display delimiters. Do not treat single-dollar prices as math or render code/JSON as formulas. Use actual bundled PrismJS for full-block tokenization before rebuilding exact line-step wrappers; unsupported languages stay escaped plain code. Preserve source text and exact copying across multiline tokens. Include dependency versions, licenses and font assets; generated pages remain offline and CDN-free.
公式使用内置KaTeX渲染：上述行内/独立公式定界符；单美元价格不作公式，代码/JSON不参与数学渲染。代码采用真实内置PrismJS，先整块分词再生成精确行步骤；不支持的语言保留转义纯文本。多行token仍须保留原始源码和准确复制；附依赖版本/许可/数学字体资源，生成网页保持离线无CDN。

### Original figures / 原始图表
Slides must be independently readable: whenever the explanation refers to a paper figure/table or relies on it to support a claim, include the relevant original figure/table or a faithful crop on that slide; split into adjacent explanation slides if necessary. Explain the visible panels, axes, numbers or evidence path beside the image. Source links are provenance, never a required detour to understand the slide; a figure number, “see paper” link or distant appendix alone is insufficient. Follow [references/paper-figures.md](references/paper-figures.md) for extraction, provenance and layout; use scripts/extract_paper_figure.py when suitable. Preserve labels/panels, localize caption/alt, retain page/figure/source locators and full-resolution zoom; split crowded slides, record unavailable assets and never generatively redraw quantitative results.
Slides须可独立阅读：讲解提及或依赖原文图表支撑主张时，将相关原图表或忠实裁图直接置于当前页；放不下就拆成相邻讲解页。在图旁解释面板、坐标、数字或证据路径。来源链接仅供溯源，不是理解内容的必经跳转；只写图号、见原文或把必要图表远置附录均不够。按原图参考执行提取/溯源/排版，可用辅助脚本；保留标签面板、本地化图注/替代文字、页图来源和全分辨率放大。过密拆页，资源不可得留缺口，不生成式重画数据。

### Single captions and reader-facing copy / 单一图注与读者文案
Keep every cited body figure/table complete, but show its caption only once as slide text. Use artwork-only images/crops without the printed caption; keep the complete original caption in provenance metadata, and author one accurate page-language caption in figure.caption. Do not automatically append original_caption as a second caption. Screenshot files are optional; if a PDF crop includes its caption, recrop before publishing instead of duplicating it.
所有引用正文图表保持完整，但图注仅以slides文字显示一次。图片/裁图只含图表本体，不含印刷图注；完整原图注存来源元数据，figure.caption编写一份准确的页面语言图注，不自动追加original_caption。截图可选；已含图注的PDF截图应先重裁再发布，避免重复。

Write for the reader, not the generation process. Keep scientific qualifications, source locators, the requested site credit and necessary controls; remove claims about preserving originals/captions, screenshotting, skill workflows or avoiding paper navigation. Use only a minimal instruction such as “点击图表可查看全分辨率” / “Select the figure to view full resolution” when needed. Use RoyalBlue #4169e1 for the primary theme accent.
面向读者而非生成过程写文案；保留科学限定、来源定位、用户要求的站点署名及必要操作提示，删除保留原图/图注、截图方式、技能流程或无需跳论文等自述。需要时仅提示上述查看全分辨率；主主题色采用皇家蓝#4169e1。

### Figure readability / 图表可读性
Keep figure containers, images and zoom viewers on #ffffff, without theme recoloring. Reconstruct PDF soft masks or render a faithful PDF crop if direct extraction loses axes/text; confirm labels, tick marks, legends and error bars remain readable, not merely that the image loads.
图表容器、图片及放大窗口使用#ffffff白底，不主题重着色。提取丢失坐标/文字时重建PDF软蒙版或忠实裁图；验证标签、刻度、图例和误差线可读，而不仅是图片加载。

### Root entry reliability / 根入口可靠性
For a single generated locale, root index.html redirects to its relative locale/index.html using the current file/HTTP URL, preserving query/hash, with a visible fallback link if navigation is unavailable. For multiple locales keep the chooser. Test opening the actual root file and clicking through the collection to a real paper page over both file:// and HTTP; an existing target file alone is not proof of working navigation.
仅一种语言时根入口按当前file/HTTP地址相对跳转至语言集合，保留查询/锚点并保留可见备用链接；多语言保留选择页。必须从实际根文件测试经集合到论文页，覆盖file及HTTP；目标文件存在不等于导航正常。

### Palette boundaries / 色表边界
Use Ivory #fffff0 for the webpage outside the slide frame, the named blue interface chrome and named white/pastel semantic card palette in references/design.md; retain red/yellow/green/blue distinctions and use lowercase application hex notation. PrismJS must use its official default prism.css without token-color overrides; KaTeX keeps its default colors. Do not recolor original paper figures. Theme rules apply only to application chrome/cards, not either rendering library.
slides外框外网页背景固定Ivory #fffff0，界面蓝色及浅色语义卡片按design色表，保留红黄绿蓝区分且自有色值小写。PrismJS使用官方默认prism.css，不覆盖token颜色；KaTeX默认颜色不变；论文原图不改色。主题规则仅作用于应用框架/卡片，不覆盖渲染库。

## [Performance] / 质量标准
Every collection card shows an evidence-backed integer 1–4 score. Code/JSON/execution records use labelled semantic windows with highlighting and source-only copy; line-step mappings are exact. Validate both desktop and phone bounds, locale links, source/appendix links, TOC/focus, hash navigation, 5s/15s/30s/1min autoplay, modal/hidden-tab holds and last-slide stop. Prefer splitting overloaded pages to shrinking text. Record actual verification and unperformed checks separately.
集合每张卡片展示有依据的1–4整数评分；代码/JSON/记录有标签、高亮和纯源码复制，行步骤精确。检查桌面/手机边界、语言/来源/附录链接、目录焦点、锚点、四档播放、弹窗/隐藏页签暂停及末页停止。过密拆页不缩字；实际检查与未执行项分开记录。

### Autoplay regression gate / 自动播放回归门槛
Autoplay must advance the actual active slide and URL hash, not merely toggle a button. Display a countdown while running and a localized hold reason while blocked. Track paused/running/waiting states with one timer; observe every current or dynamically added details/dialog and recover after it closes or the tab returns. Duplicate close/toggle events must not restart an already running countdown. Preserve manual-navigation/speed resets and last-slide stopping.
自动播放必须真实推进当前页与URL锚点，不能只切按钮。运行时显示倒计时，阻塞时显示本地化等待原因。用单计时器管理暂停/运行/等待，覆盖已有及动态新增的详情/弹窗，收起或返回页签后恢复；重复关闭/切换事件不能重置正在运行的倒计时。保留手动翻页/变速重置及末页停止。

Before reporting a fix, run `evals/autoplay_check.py <actual-user-deck.html> --real-time` plus the generated-deck regression. Wait at least one real 5-second interval and verify the slide/hash changes, then reproduce a generic non-code details hold and close/resume. Also cover all four speeds, pause, Escape, hidden-tab resume and end/restart with a controlled clock. Test the supplied artifact, not only a simplified fixture; preserve a backup before repairing its embedded runtime.
宣称修复前，对用户实际页面及新生成页面运行上述测试；至少等待一个真实5秒间隔并核对页/锚点变化，再测试非代码区详情等待和收起恢复。受控时钟补测四档速度、暂停、Escape、隐藏页签恢复及末页重启。必须测试实际产物而非仅简化样本；修嵌入脚本前保存备份。

### Surface and rendering checklist / 背景与渲染检查
Verify the scaled slide's surrounding webpage is #fffff0 on desktop and phone; keep figure images and zoom viewers #ffffff, semantic cards in the named pastel palette, and RoyalBlue #4169e1 as the primary accent. Use one localized caption outside artwork-only images; retain original caption provenance without duplicating visible captions. Keep reader-facing text free of production-method claims, except the requested generation credit and necessary controls. Confirm Prism default token/background colors and KaTeX default behavior are unaffected by application styling.
检查桌面/手机缩放后slide四周网页为#fffff0，图表及放大窗口为#ffffff，语义卡片按标准浅色表，主色皇家蓝#4169e1。图本体不含印刷图注，外侧仅一份页面语言图注，原图注存溯源不重复显示。除指定生成署名和必要控件外，读者文案不含制作过程自述。确认应用样式不影响Prism默认语法/背景色及KaTeX默认表现。

## [Example] / 示例
- “把这两篇分析做成与模板接近的中文精读网页。” → validate claims, plan case/code/evidence pages, build a collection and two decks.
  “Turn these two analyses into English reading slides matching this template.” → 同一流程，英文内容和界面。
- “只修复 slides 的代码高亮。” / “Fix code highlighting only.” → inspect mappings and browser behavior; preserve existing claims and scope / 核对映射与交互，保留主张及范围。
- “只给摘要，生成完整证据页。” / “Make evidence slides from this abstract.” → mark metadata-only and request missing analysis; never invent experiments / 标记仅摘要并补分析，不编实验。

**Output layout / 输出目录：**
```text
site/
├── index.html
├── zh-CN/index.html + <paper-id>.html
└── en-US/index.html + <paper-id>.html
```

A Chinese-only build credits “由 [crispe-deep-paper-reading] 生成”; an English-only build credits “Generated with [crispe-deep-paper-reading]”. Both use the master-branch plugin link above. A bilingual entry presents both; language switching keeps the current slide.
仅中文署名用上述中文，仅英文用上述英文；均链接master插件目录。双语入口两者都显示，切换语言保留当前页。
