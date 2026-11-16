---
name: crispe-slides-writer
description: >-
  Generate reading-first, evidence-linked HTML paper slides and collection websites from analyzed papers,
  including worked examples and step-by-step code. Use for paper slides, paper-reading websites,
  turn this analysis into slides, or match a supplied reading template. 生成论文精读幻灯片、论文阅读网页、
  把分析做成 slides、按模板生成论文网页；支持中文与英文。 Consumes analysis; does not replace full-paper reading.
  消费已完成的分析，不代替全文阅读；普通 UI 开发、单纯论文总结或 PPT 转换不触发。
version: 1.3.1
argument-hint: "[project.json路径 / project-json-path] (可选/optional) -- 指定论文分析项目；可附模板路径、输出目录及中英文要求 / specify an analyzed-paper project, optional template path, output directory and Chinese/English preference"
---

# CRISPE Slides Writer / CRISPE 精读网页写作

## Context and role / 背景与角色
Build a reusable reading experience: topic collection → paper narrative → worked example → mechanism/code → evidence appendix. Treat claims, code and original figures as traceable content, not decoration.
构建可复用的阅读体验：主题集合 → 单篇叙事 → 具体实例 → 机制/代码 → 证据附录。主张、代码和原图应可追溯，不是装饰。

## Language / 语言
Follow an explicit output-language request, otherwise mirror the user (bare identifiers inherit conversation language; Chinese only if no signal). Keep identifiers, symbols and paper titles stable. This bilingual skill does not force duplicate bilingual slides. For English output translate narrative, examples, evidence limitations and logs as well as interface labels. Deliver a fully English example bundle, not Chinese prose under English headings. Use separate zh-CN/en-US bundles and optional reciprocal language links.
指定语言优先，否则跟随用户（纯编号沿用会话语言，无线索才回退中文）。标识符、符号与论文标题保持稳定。双语技能不强制每页重复两种语言；英文输出须翻译叙事、实例、证据局限和日志，而非只有标题英文；使用独立 zh-CN/en-US 项目包及可选双向语言切换。

## Instructions / 执行步骤
1. Read [references/design.md](references/design.md) and [references/contracts.md](references/contracts.md). Locate analyzed reports, claim locators, code execution records and figure assets. Missing analysis goes back to `crispe-paper-analyst`; an absent source stays a visible gap. Never silently fetch more full texts.
   阅读设计规则和契约，定位分析报告、主张定位、代码执行记录和图片。缺分析交给 analyst，缺证据明确标注，不静默获取更多全文。
2. If a local template is supplied, inspect its index and at least two representative paper pages, including code, evidence and navigation behavior. Record design tokens and source commit. If unavailable, use bundled assets; no hardcoded home-directory dependency. See [references/reuse.md](references/reuse.md) for evaluated online/local alternatives.
   有本地模板时检查索引和至少两篇代表页面，覆盖代码、证据及导航，记录设计变量与来源版本。不可用则用内置资源，不依赖固定个人路径。复用评估见参考。
3. Plan one claim or question per slide. Start with a concrete case, advance its state through mechanism and code, then test against original results and limitations. Every index.html paper card must show its evidence-based numeric 1–4 analyst score; missing/null/deferred scores fail publication. Keep the existing calibration and disclose reading gaps separately. Preserve complete report separately; optional background/formula sections follow analyst rules.
   每页一个主张或问题；从具体案例出发，经机制和代码推进状态，再核对原始结果与局限。index.html 每张论文卡片必须展示有依据的 1–4 数值评分，不接受缺失/空值/暂缓；保留原量表，阅读缺口另列。保留阅读顺序，完整报告单独保留；概念/公式依 analyst 规则选择。
4. Author `slides` in `project.json`, referencing existing claims/examples. Code steps use exact 1-based line numbers and explain input → operation → state/output. Display teaching/original/reproduction and execution status. Wrap code, JSON and execution logs in labelled semantic pre/code windows with syntax highlighting, source-only copy buttons and bounded scrolling. Figures retain source URL, page/section/figure locator, alt and caption; use relative assets. Add an appendix for original evidence, and typed cross-paper links from `crispe-paper-cross-link`.
   在 project.json 编写 slides，引用已有主张/实例。代码步骤按真实一基行号映射输入、操作与状态；显示教学/原始/复现性质及执行状态；代码、JSON 和运行日志统一用带语言标签、语法高亮、纯源码复制按钮及有限滚动的 pre/code 窗口。原图保留来源、定位、替代文字和图注，用相对资源。加入证据附录及 cross-link 的类型化跨论文连接。
5. Run the deterministic builder below from the resolved installed skill path. It validates links/claim IDs/line mappings, escapes text, embeds local images, and produces portable HTML; it neither reads papers nor executes supplied code. On validation failure fix input, not the research evidence to fit a layout.
   从实际安装目录运行下列确定性生成器；它校验链接、主张和行号、转义文本、嵌入图片并生成可移植 HTML，不负责读论文或执行代码。校验失败修正输入，不为排版改研究证据。

```bash
python3 <skill-dir>/scripts/build_site.py project.json --translation project.en.json --output ./site
# Validate without writing / 仅校验
python3 <skill-dir>/scripts/build_site.py project.json --check
python3 -m http.server 8000 --directory ./site
```

6. Review every slide at 1600×900 and 1280×720 plus a phone viewport. Verify opt-in autoplay with 5s/15s/30s/1min per page, speed changes, pause/resume, dialog/hidden-tab holds and last-page stopping. Check card/code overflow, image loading, TOC keyboard focus/Escape, arrows/Home/End, hash links, step highlights, collection return and cross-paper target anchors. Split overloaded slides instead of shrinking text. Optional browser tooling is not a mandatory runtime dependency; report unperformed visual checks honestly.
   在桌面及手机视口检查每页，核对主动开启的自动播放、每页5s/15s/30s/1min、变速、暂停/恢复、对话框/隐藏页签阻止推进及末页停止；检查溢出、图片、目录键盘焦点/Escape、翻页/Home/End、深链接、代码高亮、返回索引及跨论文定位。过密就拆页，不缩字。浏览器测试工具是可选验证依赖，未执行视觉检查如实说明。

## Specification and performance / 规范与质量
Deliver `project.json`, source reports/examples, `site/index.html` language entry, `site/<locale>/index.html`, one `site/<locale>/<paper-id>.html` per paper, and a validation summary with actual command results. The site works via `file://` and local HTTP, without fonts/CDNs/API keys/build tools. Do not copy the template's paper content into reusable assets or generatively redraw quantitative results.
交付契约文件、报告/实例、根语言入口、对应语言目录中的集合索引及每篇 HTML 和真实验证摘要。网页支持本地直接打开或 HTTP，无字体/CDN/API Key/构建工具依赖。不要把模板论文内容写死到资源，也不要用生成图片重画定量结果。

## Examples / 示例
- “把这两篇分析做成与模板接近的中文精读网页。” → validate claims, plan case/code/evidence pages, build a collection and two decks.
  “Turn these two analyses into English reading slides matching this template.” → 同一流程，英文内容和界面。
- “只修复 slides 的代码高亮。” / “Fix code highlighting only.” → inspect mappings and browser behavior; preserve existing claims and scope / 核对映射与交互，保留主张及范围。
- “只给摘要，生成完整证据页。” / “Make evidence slides from this abstract.” → mark metadata-only and request missing analysis; never invent experiments / 标记仅摘要并补分析，不编实验。

## Documentation languages / 技能文档语言
Write this skill and its explanatory references in paired Chinese and English. Currently support only zh-CN and en-US output; do not add another documentation or output language. Generated websites use a bilingual root index.html entry, with all Chinese collection/deck pages under zh-CN/ and all English pages under en-US/. Any future approved locale must follow the same locale-directory convention.
本技能及说明性参考文档保持中文、英文对照。目前仅支持 zh-CN 和 en-US，不新增其他文档或输出语言。生成网站使用双语根 index.html 入口，中文集合/论文页面全部放 zh-CN/，英文全部放 en-US/；未来获准增加语言时也按地区语言目录组织。

## Generation credit / 生成署名
Every generated index.html (root entry and locale collections) must visibly credit crispe-deep-paper-reading and link to https://github.com/alexxyjiang/custom-agent-skills/tree/master/plugins/crispe-deep-paper-reading-plugin using only “Generated with [crispe-deep-paper-reading]” (or its Chinese equivalent). Match the generated page language; an English-only build has English-only credit, a Chinese-only build Chinese-only, and a bilingual entry credits both. Keep skill documentation Chinese/English paired.
所有生成的 index.html（根入口及语言集合）必须可见地注明由 crispe-deep-paper-reading 生成，仅用“由 [crispe-deep-paper-reading] 生成”并链接到 https://github.com/alexxyjiang/custom-agent-skills/tree/master/plugins/crispe-deep-paper-reading-plugin。署名跟随生成语言；仅英文则只用英文，仅中文则只用中文，双语入口两种都展示。技能文档仍保持中英文对照。
