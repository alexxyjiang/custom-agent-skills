# Template-derived design / 模板提炼设计

## Provenance / 来源
Inspected local `~/paper-reading-slides`: `index.html`, `react.html`, `reflexion.html`, `hipporag.html`; the path is a session input, not an installed dependency. The bundled renderer is a new implementation of the observed design grammar, not a copy of paper-specific HTML or image payloads.
已检查上述本地索引、ReAct、Reflexion、HippoRAG 页面；该路径是本次输入，不是安装依赖。内置生成器重新实现所观察到的设计规则，不复制论文正文或图片负载。

## Tokens and layouts / 变量与版式
- Stage 1600×900, scaled uniformly inside a dark `#0b1120` viewport; slide `#f8fafc`, text `#0f172a`, body `#334155`, muted `#64748b`, border `#e2e8f0`.
  1600×900 固定画布，暗背景中等比例缩放；页面、正文、弱化文字及边框采用上述颜色。
- Indigo `#4f46e5`: mechanism; emerald `#059669`: evidence; amber `#d97706`: assumptions; rose `#e11d48`: failures. White/tinted cards, 16px radius, generous gutters; role-specific local font stacks below.
  靛蓝对应机制，绿色对应证据，琥珀对应假设，玫红对应失败；白色/浅色卡片、16px 圆角、充分间距、下述按角色区分的本地字体栈。
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

Use bundled KaTeX for inline `\(x\)` and display `\[x\]` / `$$x$$`; keep its own math font families. Never scan pre/code or single-dollar prices. Use bundled PrismJS with the Tomorrow palette and matching component colors, not a homemade lexer. Tokenize an entire block so multiline strings stay correct; preserve exact 1-based line wrappers for walkthroughs and copy only original source. Both libraries and WOFF2 math fonts are embedded in generated HTML; inspect `assets/vendor/manifest.json` and packaged MIT licenses for provenance.
采用内置KaTeX处理行内与独立公式并保留数学字体；不扫描pre/code或单美元价格。代码用内置PrismJS的Tomorrow配色并匹配组件色，不再自制词法着色。整块分词保证多行字符串，保留一基行包装与纯源码复制。两库与数学WOFF2字体内嵌HTML；来源及MIT许可见vendor清单和许可文件。

## Playback observability and recovery / 播放可观察性与恢复
A pressed button is not proof of autoplay. Show seconds until the next slide and localized waiting reasons. Observe all details toggle events with capture, including dynamically added nodes; use one cancellable deadline/timer with a recovery fallback. Reconcile modal/tab changes without resetting a live deadline. Real-time regression must run against the user's generated file and the generator output, including the non-code details close/resume path.
按钮按下不代表播放正常；显示下一页倒计时及等待原因。捕获所有details事件含动态节点，单可取消计时器/截止时间并有恢复兜底；弹窗/页签变化协调状态但不重置有效截止时间。真实计时回归同时覆盖用户文件及生成输出，包含非代码区详情收起恢复。
