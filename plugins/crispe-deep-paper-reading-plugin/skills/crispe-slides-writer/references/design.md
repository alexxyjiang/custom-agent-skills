# Template-derived design / 模板提炼设计

## Provenance / 来源
Inspected local `~/paper-reading-slides`: `index.html`, `react.html`, `reflexion.html`, `hipporag.html`; the path is a session input, not an installed dependency. The bundled renderer is a new implementation of the observed design grammar, not a copy of paper-specific HTML or image payloads.
已检查上述本地索引、ReAct、Reflexion、HippoRAG 页面；该路径是本次输入，不是安装依赖。内置生成器重新实现所观察到的设计规则，不复制论文正文或图片负载。

## Tokens and layouts / 变量与版式
- Stage 1600×900; Ivory #fffff0 outer webpage background, GhostWhite #f8f8ff slide, MidnightBlue/Navy text, LightSteelBlue #b0c4de borders, RoyalBlue #4169e1 accent.
  1600×900固定画布，在Ivory #fffff0网页外背景中等比例缩放；slide为GhostWhite #f8f8ff，正文、边框及强调色如上。
- RoyalBlue `#4169e1`: primary accent. Semantic cards use AliceBlue `#f0f8ff`, Honeydew `#f0fff0`, Ivory `#fffff0`, and MistyRose `#ffe4e1`; retain 16px corners, generous gutters and role-specific local fonts.
  皇家蓝作为主强调色；机制、证据、提醒和反例分别采用上述标准浅蓝、浅绿、浅黄、浅红卡片，保留16px圆角和充分间距。
- Chapter pill → informative question/title → lead → two/three panels → takeaway → source strip. Code left, explanation/state right. Collection page uses responsive topic groups and linked cards, not the fixed slide stage.
  章节标签→问题标题→导语→双/三栏→要点→来源条。代码左侧、解释和状态右侧；集合页响应式主题卡片，不受固定画布限制。

## Narrative and interactions / 叙事与交互
Use the same concrete problem across consecutive pages: failure → mechanism → state trace → function → result → counterexample. Keep original results and teaching simulations distinctly labeled. Main pages link to evidence appendix; appendix links return to narrative. Do not inherit claims such as zero hallucination or direct historical causation merely because a template says so.
连续页面沿用同一具体问题：失败→机制→状态轨迹→函数→结果→反例。原始结果和教学模拟明确区分；正文跳证据附录，附录可返回正文。不能因模板如此书写就继承“零幻觉”或直接历史因果等主张。

Required interactions: previous/next, TOC, page/progress, stable `#slide-<id>` anchors, Home/End and arrow keys, focus restoration, code line-step highlighting, original figure enlargement, cross-paper links, collection return, reduced motion and printable linear reading.
必需交互：翻页、目录、页码/进度、稳定锚点、Home/End/方向键、焦点恢复、代码行步骤高亮、原图放大、跨论文链接、回索引、减少动画及线性打印。

## Content density / 信息密度
Target titles ≤70 characters, leads ≤240, two/three cards with short paragraphs, and ≤22 displayed code lines. These are authoring heuristics, not scientific limits. A full function can live in an example file; split its explanation into pages. Check rendered sizes, not character count alone. Original image zoom never replaces legible captions.
建议标题≤70 字符、导语≤240、双/三卡短段落及每页≤22 行代码，作为编写提示而非科学限制。完整函数可单独保存，讲解拆页。最终看实际渲染，不仅看字数；图片放大不能代替可读图注。

## Typography and rendering / 字体与渲染
- Titles, navigation, buttons and UI: `"Iosevka Aile", "Noto Sans CJK SC", sans-serif`.
  标题、导航、按钮及界面按上述顺序回退。
- Prose and explanatory text: `"Iosevka Etoile", "Noto Serif CJK SC", serif`.
  正文及解释文字按上述顺序回退。
- Code, JSON and execution records: `"IosevkaAlexJiang", "Noto Sans Mono CJK SC", monospace`.
  代码、JSON和运行记录按上述顺序回退。

Use bundled KaTeX for inline `\(x\)` and display `\[x\]` / `$$x$$`; keep its own math font families. Never scan pre/code or single-dollar prices. Use bundled PrismJS with its official default prism.css theme, without application token/background recoloring. Keep KaTeX default colors unchanged. Tokenize an entire block so multiline strings stay correct; preserve exact 1-based line wrappers for walkthroughs and copy only original source. Both libraries and WOFF2 math fonts are embedded in generated HTML; inspect `assets/vendor/manifest.json` and packaged MIT licenses for provenance.
采用内置KaTeX处理行内与独立公式并保留数学字体；不扫描pre/code或单美元价格。代码用PrismJS官方默认prism.css，不覆盖语法或背景颜色；KaTeX默认色表不变。整块分词保证多行字符串，保留一基行包装与纯源码复制。两库与数学WOFF2字体内嵌HTML；来源及MIT许可见vendor清单和许可文件。

## Playback observability and recovery / 播放可观察性与恢复
A pressed button is not proof of autoplay. Show seconds until the next slide and localized waiting reasons. Observe all details toggle events with capture, including dynamically added nodes; use one cancellable deadline/timer with a recovery fallback. Reconcile modal/tab changes without resetting a live deadline. Real-time regression must run against the user's generated file and the generator output, including the non-code details close/resume path.
按钮按下不代表播放正常；显示下一页倒计时及等待原因。捕获所有details事件含动态节点，单可取消计时器/截止时间并有恢复兜底；弹窗/页签变化协调状态但不重置有效截止时间。真实计时回归同时覆盖用户文件及生成输出，包含非代码区详情收起恢复。

## Named palette / 标准命名配色
Keep blue application chrome (RoyalBlue #4169e1, MidnightBlue #191970, Navy #000080, SteelBlue #4682b4, LightSteelBlue #b0c4de). Preserve semantic pastel cards: mechanism AliceBlue #f0f8ff, evidence Honeydew #f0fff0 or MintCream #f5fffa, caution Ivory #fffff0 or OldLace #fdf5e6, counterexample MistyRose #ffe4e1 or LavenderBlush #fff0f5; neutral WhiteSmoke #f5f5f5, Linen #faf0e6 or White #ffffff. Use basic named colors for semantic borders and neutral values. Write application hex values in lowercase. Prism default theme and KaTeX styles are independent of this palette; do not normalize their vendor colors. Original paper artwork remains unchanged.
页面框架采用上述标准蓝色色表，保留机制蓝/证据绿/提醒黄/反例红等浅色语义卡片及中性背景；语义边框和中性色使用基本命名色。应用十六进制全部小写；Prism默认主题和KaTeX不参与应用色表归一，不修改第三方颜色；论文原图不改色。

## Surface boundaries / 背景区域边界
The webpage area outside the slide frame is always Ivory #fffff0, including letterboxing around the uniformly scaled stage on desktop and phone. Keep this separate from the slide canvas (#f8f8ff), semantic pastel cards, blue navigation chrome, and figure/zoom surfaces (#ffffff). Prism uses its unmodified default theme; KaTeX retains default colors. Do not recolor original figures; reconstruct PDF soft masks or render white-background crops when necessary for readable labels/axes. Use lowercase authored hex values throughout.
桌面及手机等比缩放后，slides外框外的网页区域（含上下/左右留白）统一Ivory #fffff0。与slide画布#f8f8ff、浅色语义卡片、蓝色导航及图表/放大白底#ffffff区分。Prism使用未改动默认主题，KaTeX默认色不变；原图不染色，必要时恢复PDF软蒙版或白底裁图保证标签坐标可读。自有十六进制全部小写。

## Contents introduction / 目录导语
Reuse paper.summary from the collection card as the table-of-contents introduction, following the page language. Do not expose raw read_coverage states or an empty “Unread:” label as reader-facing introductory copy. Retain the actual coverage record in the project/report and any substantive limitations in the relevant evidence slides.
目录导语复用集合卡片的paper.summary并跟随页面语言；不把原始read_coverage状态或空未覆盖标签作为读者导语。真实覆盖记录保留在项目/报告，实质局限放相应证据页。

## References and overlap / 引用与重叠
Current-paper footer/figure locators are static italic underlined #4169e1 text; external paper, third-party and slide navigation links retain href with the same style. URL identity distinguishes references, including arXiv abs/pdf/html forms and versions. Preserve provenance in JSON. Do not tolerate overlapping paint: check card descendants against takeaway/footer after final rendering and split dense figure notes into adjacent pages. Keep all existing anchors valid.
本论文底部/图定位为斜体下划线皇家蓝静态文字；外部论文/第三方/页面导航保留同样样式的href。URL身份区分引用，含arXiv不同形式及版本；JSON保留溯源。检查最终绘制卡片子元素与要点/页脚，不容忍覆盖；图旁长解释拆相邻页并保留锚点。

## Heading and appendix layout / 标题与附录布局
Use `[Title]・[Source]` in the chapter heading and browser tab (Motivation・arXiv 2304.03442 v2). Embed key figures directly in the main narrative with substantive explanation; reference-level figures remain in the final appendix. Keep one complete unique occurrence, shared references/return links, one textual caption and full-resolution zoom. Do not generate caption-only placeholder pages.
章节标题栏及页签使用上述格式；关键图随实质解释直接嵌入主线，参考图留末尾附录；每图完整唯一、共享引用回链、单图注及放大，不生成图注式占位页。

For adaptive image/text pairs, each region must occupy >=30% of total layout width in left/right modes or >=30% of total height in top/bottom modes. Reject insufficient candidates and choose another mode or revise the explanation; keep type size and image ratio unchanged.
自适应图文左右各至少整体宽30%，上下各至少整体高30%；不足的候选拒绝，换版或调整解释，不改字号或图比例。

## Formula fitting and verification / 公式适配与验证
Display math may wrap at KaTeX base-unit boundaries without altering the TeX annotation. If the widest indivisible unit or an inline formula still exceeds the card, retry full-width stacked cards, preserving type size, and recheck all text/card/takeaway/footer bounds. Keep fractions, roots, matrices and aligned environments intact; do not insert arbitrary string breaks into TeX commands. Authored aligned/split expressions can improve line meaning. Mark no-fit results, rather than silently accepting a scrollbar. Refit after fonts ready, slide activation and resize; coordinate figure fitting after math height changes. Verify physical bounds at desktop and phone-scaled stage sizes and confirm the exact original TeX annotation remains unchanged.
独立数学沿KaTeX语义单元折行，TeX注释不变；最宽不可分单元或行内公式仍越界则全宽纵排卡片，保留字号并检查文字/卡片/要点/页脚边界。分式、根式、矩阵和aligned保持整体，不在TeX命令中随意插断点；必要时作者用aligned/split提升语义。无可行版标失败，不能默认滚动条算通过。字体/切页/resize后重测，数学高度变化后协调图布局；桌面及手机缩放均测且核对原TeX注释完全保留。

## Locator consistency / 定位一致性
Captions explain the figure; footer markers carry the verified section/figure/page locator once. Use the same locator for links to that figure inside the deck, e.g. §4.1, Figure 6, p.9-10. Claim-kind/coverage metadata is not visible footer copy. Canonicalization removes PDF prefixes and spacing differences without inventing sections or page ranges. Correct provenance errors only against the pinned source.
图注解释图意，页底统一一次节/图/页定位，站内链接复用同定位；主张类型/覆盖元数据不写可见页底。规范化只去PDF前缀和空格差异，不造节页；来源错误须按固定原文核对。
