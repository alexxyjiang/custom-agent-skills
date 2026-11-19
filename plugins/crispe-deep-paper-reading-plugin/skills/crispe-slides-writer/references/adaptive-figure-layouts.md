# Adaptive figure layouts / 自适应图文布局

## Reference reading / 模板通读
Read the local ReAct template's 59 slide sections (25 narrative, appendix index and 33 appendix pages), its style layers and interaction runtime. Useful patterns include p.3/5 wide image above explanation cards, p.6 vertically stacked retrieval strips with narrow labels, p.7/12–14/18/21/23/45/56 asymmetric image+commentary columns, p.4 side-by-side comparisons, and p.57–58 stacked original-text regions. These are geometry and narrative lessons, not paper claims to copy. Our output uses one unique figure target: key figures in the narrative and reference figures in the appendix; do not copy the template's repeated crops or duplicate images across pages.
通读本地ReAct模板59个section（25正文、附录目录、33附录）及样式与交互。可借鉴3/5页宽图在上说明在下、6页竖向检索条与窄标签、7/12–14/18/21/23/45/56页非对称图文栏、4页并排对比、57–58页上下原文区域。借鉴几何和叙事，不复制论文主张。输出按关键图在主线、参考图在附录分流，每图唯一，不照搬重复裁图和跨页重复图片。

## Authoring / 编写
Use slide.figure_notes (optional array of title/text/tone card objects) for short figure-specific explanation. Existing narrative cards remain narrative. Optional slide.figure_layout accepts auto/left/right/top/bottom/full; auto is the normal choice. Explicit directions encode reading order (e.g. explain left, chart right) and fall back if they cannot fit. Without notes use the full image stage. Preserve one complete original, one localized text caption, white figure/viewer backgrounds and full-resolution zoom. Scientific relationships cannot be inferred merely to decorate unused space.
用可选figure_notes卡片数组放简短读图说明，原正文卡片继续正文。可选figure_layout支持auto/left/right/top/bottom/full，常用auto；指定方向表达阅读顺序，放不下可回退。无说明用全幅。保留唯一完整原图、单份本地化图注、白底与放大；不为填空补造关系。

## Candidate selection / 候选选择
- Left/right: portrait, tall table, nearly square diagram, or notes that need a vertical rail. Notes use a bounded rail; both regions retain the 30% minimum.
  左右：竖图、长表、接近方形图或适合竖栏的说明；说明栏受区域约束，图文均保持30%下限。
- Top/bottom: panoramic chart, horizontal pipeline, short figure strip with compact notes. Keep the wide axis/labels legible.
  上下：全景图、横向流程、短宽图配简短说明，保证横轴标签可读。
- Full: no explanatory cards; maximize image with caption and return links. One source image may contain original panels; keep them together.
  全幅：无卡片时最大图加图注/回链；原图内面板整体保留。

Image aspect ratio and note character counts order candidates, but are not the final proof. The browser evaluates actual text/caption heights, image contain size and box/text overflow; among feasible candidates it keeps the largest image (within a small tie tolerance). Run again after fonts ready, image load, slide activation and resize; selection uses stage coordinates so phones uniformly scale the same 16:9 design, not arbitrary mobile reflow. Controls, sources and caption retain their assigned space.
宽高比与字数仅决定候选顺序，不是最终依据。浏览器实测文字/图注高度、等比图像尺寸和盒/文字溢出，在可行候选中尽量放大图。字体/图片就绪、切页及resize后重算；用画布坐标，手机仍等比16:9而非随意重排。控件、来源和图注有独立空间。

## Failure and verification / 失败与验证
The renderer exposes data-layout, data-layout-status, candidate overflow and image ratio for checks. If no candidate fits, mark overflow; do not silently cut text, hide limitations or reduce font size. Shorten redundant prose or put detailed explanation on a linked text-only continuation, leaving the full figure on its single narrative/appendix target. Review actual labels/axes: large file resolution does not guarantee legibility at slide scale. Zoom supplements the overview, not an excuse for unreadable primary labels. Check desktop/phone bounds, text-panel separation, caption edges, ratio preservation, copy/navigation and repeat-build figure uniqueness.
渲染器暴露版式/状态/候选溢出/宽高比。全不满足则标overflow，不静默截文字、藏局限或缩字号。精简赘述或详细说明放互链纯文字续页，完整原图仍只有一个正文/附录目标。核对实际轴/标签，源分辨率大不等于页面可读，放大是补充不是主标签过小的借口。检查桌面手机边界、文字分区、图注、比例、导航及重建唯一性。

## Region proportions and significance / 区域占比与图表层级
For left/right layouts, both figure and explanation regions must each span >=30% of the entire figure-layout width. For top/bottom, each spans >=30% of its height. Measure final region rectangles after layout, including the actual available content space; gutters do not excuse undersized regions. A failed minimum marks that candidate unfit. Full mode is only for images without notes; do not hide notes to fit. Key figures remain in the main narrative with substantive explanation; reference figures remain in the appendix. Do not generate “Reading the figure” caption-only placeholder pages.
左右图文区域各不少于整体布局宽度30%，上下各不少于高度30%；实际渲染后测量区域矩形，间距不能抵消最小占比。不满足即候选不合格；full仅限无说明图，不藏说明凑版。关键图随实质解释进主线，参考图留附录，不生成图注式读图要点占位。
