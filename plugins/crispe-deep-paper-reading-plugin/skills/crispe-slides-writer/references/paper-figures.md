# Original paper figures and screenshots / 论文原图与截图

## Selection / 选择
Inventory every figure/table mentioned in the narrative or used as evidence. Make slides self-contained: embed a key original figure/table directly with its main argument, or place a reference-only figure on one appendix slide, rather than asking the reader to open the paper. Use one unique occurrence per original; related groups of up to three may share an appendix page; reuse its target for repeated references and provide return links. Source links and a complete appendix supplement this presentation rather than replace it. Prioritize exact-version original assets, then embedded PDF artwork, then a faithful PDF region/page screenshot. HTML figure screenshots are a fallback when a PDF/asset is unavailable. Use host tools already available; the helper below optionally requires PyMuPDF. Do not fetch other paper full texts or silently install dependencies.
清点叙事中提及或作为证据的每个图表。为让slides独立阅读，将重点完整图直接嵌入主论点，参考级图才放附录并从正文链接，不要求打开论文；每图唯一展示，可将至多三张关联图表组合一页，重复引用复用目标并提供回链。来源链接和完整附录是补充，不能代替当前讲解所需的图表。优先同版本原始资源，其次PDF内嵌图，再次忠实区域/整页截图；PDF/资源不可得才用HTML图截图。可用宿主工具，辅助脚本可选依赖PyMuPDF；不因此取其他全文或静默安装依赖。

## Extract / 提取
First inspect the pinned PDF page and caption. Physical PDF page indices are 1-based and may differ from printed article pages. The image inventory gives bboxes; image index alone is not semantic evidence. Confirm the figure number, caption and surrounding text visually. Embedded artwork can omit vector/text overlays: if any labels, axes, legends or panels are missing, render the full region instead. Keep all panels/units/labels; do not redraw quantitative data with a generative model.
先检查固定版本页和图注；物理PDF页一基，可能不同于印刷页。清单提供bbox，图片索引不等于语义证据；须目视核对图号/图注/正文。内嵌图可能缺向量或文字叠层，缺轴/标签/面板则渲染完整区域；保留所有面板、单位和图例，不用生成模型重画数据。

```bash
# Inventory only / 仅清点
uv run --with pymupdf python <skill-dir>/scripts/extract_paper_figure.py paper-v2.pdf --source-url https://arxiv.org/abs/2304.03442v2 --page 10 --caption-text "Figure 7:" --inspect
# Original embedded image; choose index after inspecting / 核对后选原图索引
uv run --with pymupdf python <skill-dir>/scripts/extract_paper_figure.py paper-v2.pdf --source-url https://arxiv.org/abs/2304.03442v2 --page 10 --caption-text "Figure 7:" --mode embedded --image-index 0 --bundle-root ./bundle --output ./bundle/assets/figure-7.png --locator "§4.2, Figure 7, PDF p.10" --alt "Klaus reflection tree" --caption "Original Figure 7: reflection tree"
# Vector/text-preserving raster screenshot of a region / 保留向量文字叠层的区域截图
uv run --with pymupdf python <skill-dir>/scripts/extract_paper_figure.py paper-v2.pdf --source-url https://arxiv.org/abs/2304.03442v2 --page 10 --caption-text "Figure 7:" --mode crop --clip 73 83 539 321 --dpi 200 --bundle-root ./bundle --output ./bundle/assets/figure-7-crop.png --locator "§4.2, Figure 7, PDF p.10" --alt "Reflection tree" --caption "Figure 7: Klaus reflection tree"
```

Create/verify the output parent beforehand. `--mode page` captures a full page; `--overwrite` is explicit. Extraction saves PNG and `.source.json`: PDF/asset SHA-256, page, bbox, method, dimensions, source URL and figure fields. Extraction is not visual approval; inspect the saved image, then record review status. If matching fails, stop and disclose the gap instead of silently substituting another version/figure.
预先创建/核对输出父目录；page模式整页截图，覆盖需显式参数。输出PNG和来源sidecar，含哈希、页、bbox、方法、尺寸和来源字段。提取不等于目视通过，查看后更新复核状态。匹配失败如实标缺口，不换版本/错图冒充。

## Handoff and presentation / 交接与展示
Use the existing slide.figure contract: relative src, localized alt/caption, exact version source_url and page/section/figure locator. Keep provenance sidecar beside the asset. Do not inline arbitrary HTML or remote image dependencies. The builder embeds image bytes offline; image+cards use a figure-left/explanation-right layout. Limit notes to a few short teaching points; move unrelated material to a linked continuation/appendix instead of shrinking the figure. Preserve stable existing slide ids.
沿用slide.figure字段：相对资源、随页面语言的替代文字/图注、同版本来源和页/节/图定位；来源sidecar随图。不要原始HTML或远程图片依赖。构建器离线内嵌字节，图与卡片使用左图右解释；讲解保留少量重点，其他内容放互链续页/附录，不缩图塞文字，保留现有页id。

Test original image load/dimensions, byte fidelity where possible, caption/source accuracy, no image-button/caption overlap, readable labels or full-resolution zoom, Escape/focus and autoplay modal hold/resume at desktop and phone sizes. A crop is original-derived; an annotated/redrawn teaching diagram is different and must be labeled. Never use a paper illustration as proof of empirical efficacy beyond its actual scope.
检查加载/尺寸、可行时字节一致、图注/来源、图与按钮/图注不重叠、文字可读或全分辨率放大、Escape/焦点及播放弹窗暂停恢复，覆盖桌面/手机。裁图为原文派生；标注/重绘教学图另标性质，不能把示意图当超出范围的功效证据。

## Completeness gate / 完整性门槛
Preserve every referenced body figure/table with all panels, axes, legends and notes. Preserve the full original caption separately in provenance, while publishing one accurate page-language figure.caption as slide text. Artwork-only direct embedding and artwork-only PDF crops are both valid; local screenshots are optional. Caption mentions elsewhere in body text must not be mistaken for the original caption. Multi-block/page-spanning captions need explicit provenance review rather than an automatic completeness claim.
被引正文图表保留全部面板、坐标、图例及注释；完整原图注另存溯源，页面仅展示一份准确的figure.caption文字。可直接嵌入图本体或用不含图注的PDF裁图，截图可选。正文提及不能误认图注，跨块/跨页图注需显式溯源检查，不自动宣称完整。

## Caption-once publication rule / 单次图注发布规则
Display artwork without the printed caption, plus exactly one semantic figure.caption in the page language. Retain the full original_caption only as provenance, not as a second visible caption. If a graphic contains a printed caption, extract/crop the complete graphic separately; do not remove legends, panel labels, axis labels or table footnotes as if they were captions. Archival with-caption captures may remain in assets but must not be used by slide.figure.src. Keep reader copy about the paper's ideas, with only necessary zoom instructions; remove production-method claims. Primary accent: RoyalBlue #4169e1.
展示不含印刷图注的完整图本体，以及页面语言的一份figure.caption；完整original_caption仅供溯源，不重复可见。图内若含印刷图注则单独提取/裁出完整图，勿把图例/面板标签/坐标/表注当caption删掉。含图注存档可留assets但不被展示src引用。读者文案围绕论文思想，只留必要放大提示，删除制作过程自述；主色皇家蓝#4169e1。

## Figure readability and PDF masks / 图表可读性与PDF蒙版
Use a neutral #ffffff background for paper figure surfaces, including full-resolution viewers. Preserve original chart colors; never apply theme tinting, inversion, opacity or blend filters. PDF embedded artwork may store a separate soft mask: reconstruct that mask and composite transparency onto white before saving. If labels/axes are absent or contrast differs from the PDF, render the complete PDF region instead of publishing raw image bytes. Visually check ticks, category labels, error bars, legend and all panels at normal slide size and in the enlarged view; image loading alone is not a readability test.
论文图表及放大窗口使用中性#ffffff白底，保留原始配色，不套主题染色、反相、透明度或混合滤镜。PDF内嵌图可能有独立软蒙版，保存前恢复蒙版并合成白底；若标签/坐标缺失或对比不同，直接渲染完整PDF区域。正常页和放大均须目视核对刻度、类别、误差线、图例及面板，加载成功不等于可读。

## Narrative and reference figures / 主线与参考图表
Set figure_role=key for figures essential to the argument and embed them in the main narrative with meaningful notes. Set reference for supplemental lookup figures collected in the appendix. Keep one complete occurrence, shared references and return links; do not create caption-only narrative placeholders. Adaptive layouts apply to both roles, with image/text regions each >=30% of width (left/right) or height (top/bottom).
论点关键图设key，在主线配实质说明；补充查阅图设reference放附录。保持唯一完整图、共享引用与回链，不造仅复述图注的正文占位。两类均自适应，左右图文各至少30%宽，上下各至少30%高。

## Mandatory main-point gate / 主线重点强制门槛
When a selected main point explains or relies on an original figure/table, including qualitative trends, comparisons or the method pipeline, carry that original into the main deck. Inventory it before generation in paper.visuals and map each dependent page with visual_refs. Missing assets are a pending handoff, not permission to publish text-only evidence. Keep one original target and explicit links when several main pages share it; reference-only appendix treatment is reserved for genuinely supplemental visuals.
主线重点解释或依赖原图表（趋势、比较、方法流程均含）时，原图必须进入主线；生成前清单化并映射依赖。缺资源交接待完成，不允许只发文字证据。多页共享同图则唯一主线目标加明确链接，真正补充图才放附录。

## Related visual groups / 关联图表组合
A slide may use figures (an array of one to three complete original figure objects) instead of figure. Never use both. Record figure_group_context explaining their shared question, experiment, mechanism or comparison; unrelated artwork must stay separate. Each original keeps its own localized caption, provenance and zoom, and appears only once in the deck. visual_refs may map several inventory items to this one group slide.
单页可用figures数组代替figure，含一至三张完整原图，不可两字段并用。figure_group_context说明共同问题、实验、机制或比较，无上下文关联不可拼图。每图保留独立本地化图注、溯源及放大，全站仅唯一展示；多个visual_refs可映射同一组合页。
For left/right image-text modes, stack the related originals vertically inside the image region; for top/bottom modes, arrange them horizontally. The image region and prose region still each require >=30% of total layout width/height respectively; this is a region-level minimum, not a license to make individual figures unreadable. Preserve ratio, complete artwork and font sizes; fall back or split if captions, labels or notes do not fit. No prose scrolling as a routine fallback.
左右图文时图区上下排，上下图文时图区左右排，最多三张。图文区原先各至少30%宽/高不变；这针对区域，不代表允许单图不可读。保留比例、完整图及字号，图注标签说明放不下则回退/拆页，不以文字滚动常规兜底。

### Co-locate grouped explanations / 多图说明同页
When related originals share a slide, place their shared context and per-figure explanations together in figure_notes, stacking short cards in the available text region. Use the existing blank space before adding a separate text-only continuation. Split only if complete artwork and readable prose cannot fit without scrolling; old removed slide ids may be retained as aliases on the merged target.
关联图表同页时，将共同背景和各图说明合入figure_notes，在可用文字区叠放短卡片；先利用留白，不额外创建只有说明的续页。完整图与可读文字确实无法无滚动适配才拆页；被合并旧页id可在目标aliases中保留跳转。
