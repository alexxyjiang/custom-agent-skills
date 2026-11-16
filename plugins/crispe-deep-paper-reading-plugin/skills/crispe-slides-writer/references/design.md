# Template-derived design / 模板提炼设计

## Provenance / 来源
Inspected local `~/paper-reading-slides`: `index.html`, `react.html`, `reflexion.html`, `hipporag.html`; the path is a session input, not an installed dependency. The bundled renderer is a new implementation of the observed design grammar, not a copy of paper-specific HTML or image payloads.
已检查上述本地索引、ReAct、Reflexion、HippoRAG 页面；该路径是本次输入，不是安装依赖。内置生成器重新实现所观察到的设计规则，不复制论文正文或图片负载。

## Tokens and layouts / 变量与版式
- Stage 1600×900, scaled uniformly inside a dark `#0b1120` viewport; slide `#f8fafc`, text `#0f172a`, body `#334155`, muted `#64748b`, border `#e2e8f0`.
  1600×900 固定画布，暗背景中等比例缩放；页面、正文、弱化文字及边框采用上述颜色。
- Indigo `#4f46e5`: mechanism; emerald `#059669`: evidence; amber `#d97706`: assumptions; rose `#e11d48`: failures. White/tinted cards, 16px radius, generous gutters; system Chinese/English fonts, monospace code.
  靛蓝对应机制，绿色对应证据，琥珀对应假设，玫红对应失败；白色/浅色卡片、16px 圆角、充分间距、系统双语字体和等宽代码。
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
