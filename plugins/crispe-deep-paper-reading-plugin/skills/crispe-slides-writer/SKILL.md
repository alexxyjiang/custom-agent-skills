---
name: crispe-slides-writer
description: >-
  Generate reading-first, evidence-linked HTML paper slides and collection websites from analyzed papers,
  including worked examples and step-by-step code. Use for paper slides, paper-reading websites,
  turn this analysis into slides, or match a supplied reading template. 生成论文精读幻灯片、论文阅读网页、
  把分析做成 slides、按模板生成论文网页；支持中文与英文。 Consumes analysis; does not replace full-paper reading.
  消费已完成的分析，不代替全文阅读；普通 UI 开发、单纯论文总结或 PPT 转换不触发。
version: 1.4.0
argument-hint: "[project.zh-CN.json路径 / project-json-path] (可选/optional) -- 指定论文分析项目；可附模板路径、输出目录及中英文要求 / specify an analyzed-paper project, optional template path, output directory and Chinese/English preference"
---

# CRISPE Slides Writer / CRISPE 精读网页写作

## [Context] / 背景
Turn completed paper analysis into a reading-first website: topic collection → paper narrative → worked example → mechanism/code → evidence appendix. Readers need a coherent explanation with original-result boundaries, not a document pasted onto slides.
把已完成分析转成阅读优先网页：主题集合→单篇叙事→实例→机制/代码→证据附录；读者需要连贯讲解及原始结果边界，而非把文档直接贴到幻灯片。

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
Deliver locale-qualified bundles (`project.zh-CN.json`, `project.en-US.json`), source reports/examples, `site/index.html` language entry, `site/<locale>/index.html`, one `site/<locale>/<paper-id>.html` per paper, and a validation summary with actual command results. The site works via `file://` and local HTTP, without fonts/CDNs/API keys/build tools. Do not copy the template's paper content into reusable assets or generatively redraw quantitative results.
交付契约文件、报告/实例、根语言入口、对应语言目录中的集合索引及每篇 HTML 和真实验证摘要。网页支持本地直接打开或 HTTP，无字体/CDN/API Key/构建工具依赖。不要把模板论文内容写死到资源，也不要用生成图片重画定量结果。

### Language and directories / 语言与目录
Follow an explicit output-language request, otherwise mirror the user (bare identifiers inherit conversation language; Chinese only if no signal). Keep identifiers, symbols and paper titles stable. This bilingual skill does not force duplicate bilingual slides. For English output translate narrative, examples, evidence limitations and logs as well as interface labels. Deliver a fully English example bundle, not Chinese prose under English headings. Use separate zh-CN/en-US bundles and optional reciprocal language links.
指定语言优先，否则跟随用户（纯编号沿用会话语言，无线索才回退中文）。标识符、符号与论文标题保持稳定。双语技能不强制每页重复两种语言；英文输出须翻译叙事、实例、证据局限和日志，而非只有标题英文；使用独立 zh-CN/en-US 项目包及可选双向语言切换。

Write this skill and its explanatory references in paired Chinese and English. Currently support only zh-CN and en-US output; do not add another documentation or output language. Generated websites use a bilingual root index.html entry, with all Chinese collection/deck pages under zh-CN/ and all English pages under en-US/. Any future approved locale must follow the same locale-directory convention.
本技能及说明性参考文档保持中文、英文对照。目前仅支持 zh-CN 和 en-US，不新增其他文档或输出语言。生成网站使用双语根 index.html 入口，中文集合/论文页面全部放 zh-CN/，英文全部放 en-US/；未来获准增加语言时也按地区语言目录组织。

### Generation credit / 生成署名
Every generated index.html (root entry and locale collections) must visibly credit crispe-deep-paper-reading and link to https://github.com/alexxyjiang/custom-agent-skills/tree/master/plugins/crispe-deep-paper-reading-plugin using only “Generated with [crispe-deep-paper-reading]” (or its Chinese equivalent). Match the generated page language; an English-only build has English-only credit, a Chinese-only build Chinese-only, and a bilingual entry credits both. Keep skill documentation Chinese/English paired.
所有生成的 index.html（根入口及语言集合）必须可见地注明由 crispe-deep-paper-reading 生成，仅用“由 [crispe-deep-paper-reading] 生成”并链接到 https://github.com/alexxyjiang/custom-agent-skills/tree/master/plugins/crispe-deep-paper-reading-plugin。署名跟随生成语言；仅英文则只用英文，仅中文则只用中文，双语入口两种都展示。技能文档仍保持中英文对照。

### Typography, mathematics and code / 字体、公式与代码
Use UI/title/control fonts in order: Iosevka Aile → Noto Sans CJK SC → sans-serif; prose: Iosevka Etoile → Noto Serif CJK SC → serif; code: IosevkaAlexJiang → Noto Sans Mono CJK SC → monospace. These are local fallback stacks, not remotely downloaded fonts. Keep KaTeX's bundled math fonts for mathematical glyph metrics.
标题/界面/控件字体依次使用Iosevka Aile、Noto Sans CJK SC、sans-serif；正文依次Iosevka Etoile、Noto Serif CJK SC、serif；代码依次IosevkaAlexJiang、Noto Sans Mono CJK SC、monospace。均为本地回退，不远程下载字体；数学字形保留KaTeX配套字体以保证度量。

Render authored prose formulas with bundled KaTeX using `\(…\)` inline and `\[…\]` or `$$…$$` display delimiters. Do not treat single-dollar prices as math or render code/JSON as formulas. Use actual bundled PrismJS for full-block tokenization before rebuilding exact line-step wrappers; unsupported languages stay escaped plain code. Preserve source text and exact copying across multiline tokens. Include dependency versions, licenses and font assets; generated pages remain offline and CDN-free.
公式使用内置KaTeX渲染：上述行内/独立公式定界符；单美元价格不作公式，代码/JSON不参与数学渲染。代码采用真实内置PrismJS，先整块分词再生成精确行步骤；不支持的语言保留转义纯文本。多行token仍须保留原始源码和准确复制；附依赖版本/许可/数学字体资源，生成网页保持离线无CDN。

## [Performance] / 质量标准
Every collection card shows an evidence-backed integer 1–4 score. Code/JSON/execution records use labelled semantic windows with highlighting and source-only copy; line-step mappings are exact. Validate both desktop and phone bounds, locale links, source/appendix links, TOC/focus, hash navigation, 5s/15s/30s/1min autoplay, modal/hidden-tab holds and last-slide stop. Prefer splitting overloaded pages to shrinking text. Record actual verification and unperformed checks separately.
集合每张卡片展示有依据的1–4整数评分；代码/JSON/记录有标签、高亮和纯源码复制，行步骤精确。检查桌面/手机边界、语言/来源/附录链接、目录焦点、锚点、四档播放、弹窗/隐藏页签暂停及末页停止。过密拆页不缩字；实际检查与未执行项分开记录。

### Autoplay regression gate / 自动播放回归门槛
Autoplay must advance the actual active slide and URL hash, not merely toggle a button. Display a countdown while running and a localized hold reason while blocked. Track paused/running/waiting states with one timer; observe every current or dynamically added details/dialog and recover after it closes or the tab returns. Duplicate close/toggle events must not restart an already running countdown. Preserve manual-navigation/speed resets and last-slide stopping.
自动播放必须真实推进当前页与URL锚点，不能只切按钮。运行时显示倒计时，阻塞时显示本地化等待原因。用单计时器管理暂停/运行/等待，覆盖已有及动态新增的详情/弹窗，收起或返回页签后恢复；重复关闭/切换事件不能重置正在运行的倒计时。保留手动翻页/变速重置及末页停止。

Before reporting a fix, run `evals/autoplay_check.py <actual-user-deck.html> --real-time` plus the generated-deck regression. Wait at least one real 5-second interval and verify the slide/hash changes, then reproduce a generic non-code details hold and close/resume. Also cover all four speeds, pause, Escape, hidden-tab resume and end/restart with a controlled clock. Test the supplied artifact, not only a simplified fixture; preserve a backup before repairing its embedded runtime.
宣称修复前，对用户实际页面及新生成页面运行上述测试；至少等待一个真实5秒间隔并核对页/锚点变化，再测试非代码区详情等待和收起恢复。受控时钟补测四档速度、暂停、Escape、隐藏页签恢复及末页重启。必须测试实际产物而非仅简化样本；修嵌入脚本前保存备份。

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
