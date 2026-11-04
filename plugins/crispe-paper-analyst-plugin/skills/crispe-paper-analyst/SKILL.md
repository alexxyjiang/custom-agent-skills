---
name: crispe-paper-analyst
description: >-
  Use when the user gives an academic paper -- a local PDF path, a bare arXiv ID like "2504.19874", an
  arxiv.org URL, or "下一篇"/"next one" meaning the next paper in a reading queue -- and wants an
  analysis report covering the core idea, key sections, and whether it's worth reading in depth, in
  Chinese or English. Trigger on "分析这篇论文", "读一下这个paper", "下一篇", "next paper", "analyze this
  paper", "summarize this arxiv paper", a bare arXiv id or arxiv.org link pasted on its own, "解析
  <arxiv-id>.pdf", "帮我看看这篇论文", "这篇论文讲了什么", or any request to summarize / evaluate an arXiv or
  conference paper. Can fetch the requested paper itself directly from arxiv.org when only given an
  ID/URL -- but never auto-downloads cited/reference papers without asking first. Also trigger
  proactively whenever the user points at a PDF in ~/Downloads/arxiv/ or similar, or pastes an arXiv
  id/link, and the ask is clearly "understand/evaluate this paper" rather than a narrow lookup (e.g.
  "what's the loss function on page 4"). Make sure to use this skill even if the user doesn't name it
  explicitly -- the point is to stop the model from skimming the abstract and calling it done.
version: 1.0.0
argument-hint: "[pdf-path|arxiv-id|arxiv-url] (optional) -- paper to analyze; if omitted, ask which paper or resolve 下一篇 from context"
---

# CRISPE Paper Analyst

Produces a report on an academic paper, in Chinese or English: 核心思想 (core idea) and 是否值得深度阅读
(a 1-4 score, worth-reading verdict) are always required, followed by three optional sections --
重点章节 (key sections), 重点公式/图表 (key formulas/figures), and 基础概念推荐 (background concepts) --
included only where they earn their place. The report must come from actually reading the paper, not
from paraphrasing its abstract -- that's the entire reason this skill exists instead of just letting
the model eyeball page 1. The paper itself can be fetched straight from arxiv.org when the user only
gives an ID or URL; anything it cites stays untouched unless the user says so.

---

## Language / 语言

Support Chinese and English equally. When the user gives an explicit language instruction ("in
English", "用中文", "双语对照"/"bilingual"), follow it exactly -- that overrides everything else below.
Absent an explicit instruction, mirror whichever language the user's own message is written in: a
Chinese prompt gets a Chinese report, an English prompt gets an English report. If the request carries
no language signal at all (e.g. a bare arXiv ID or URL pasted with no surrounding sentence), stay
compatible with both -- keep headings/structure language-neutral where possible and don't force a
default; only fall back to Chinese if you genuinely have nothing else to go on (e.g. no prior
conversation language to mirror either). Keep paper-specific vocabulary unchanged regardless of output
language -- method/model names, equation symbols, figure/table numbers, citation numbers -- translate
the surrounding explanation, not the terms a reader will cross-reference against the PDF.

| 中文标题 | English heading | 是否必须 / Required? |
|---|---|---|
| 一、核心思想 | 1. Core Idea | 必须 / Required |
| 二、是否值得深度阅读 | 2. Worth Reading In-Depth | 必须 / Required |
| 三、重点章节 | 3. Key Sections | 评分 ≥2 必须写；评分 1 分可选省略 / Required for score ≥2, optional only at score 1 |
| 四、重点公式 / 图表 | 4. Key Formulas / Figures | 可选 / Optional -- 需要深入讲解时才写 |
| 五、基础概念推荐 | 5. Background Concepts | 可选 / Optional -- 用到近期论文提出的专有概念时才写 |

The numbers 三/四/五 above show the full sequence when every optional section is included. When one is
omitted, renumber the rest to stay sequential (no gaps) while keeping this same relative order -- see
[Specification] for the exact rule.

## Locating or Fetching the Paper

The user may hand you any of these -- resolve to a local PDF path before reading anything:

1. **A local path** (absolute, `~`-relative, or just a filename to `find`) -- use it directly. If
   multiple similarly-named files could match, disambiguate via file metadata (see Behavioral Rules).
2. **A bare arXiv ID**, e.g. `2504.19874` or `2504.19874v2` -- build the PDF URL
   `https://arxiv.org/pdf/<id>` (a `v2`-style version suffix is optional and valid) and download it.
3. **An arxiv.org URL** (`/abs/<id>` or `/pdf/<id>`) -- extract the ID and download the same way.

**Downloading the target paper itself is expected and needs no confirmation** -- it's the paper the
user asked you to read. Save it to `~/Downloads/arxiv/<id>.pdf` (create the folder if missing, matching
where the user already keeps their reading queue) with `curl -L -o <path> https://arxiv.org/pdf/<id>`,
then read it with the Read tool's `pages` parameter as usual.

**Never auto-download a paper that only shows up in Related Work / References.** Those exist for
comparison context, not full reading -- if digging into a cited paper would genuinely sharpen the
行业定位/positioning judgment, name which one and ask the user before fetching it. This keeps the skill
from quietly spidering out across a citation graph when the user asked about one specific paper.

---

## [Behavioral Rules]

- Do NOT write the 核心思想 section from the Abstract alone. The abstract is a marketing summary written
  by the authors; it tells you what they claim, not what the paper actually does well or poorly. Read
  the Introduction, Method, and Conclusion before writing a single sentence of the report.
  不要仅凭摘要撰写核心思想——摘要是作者自己的宣传语，只说明他们声称做了什么，不代表论文实际做得好不好；必须先读完
  引言、方法和结论再下笔。
- Do NOT skip pages because "the abstract already covered it." Read every page of the PDF, including
  figures, tables, equations, and the Related Work / References section -- those are exactly the pages
  that abstracts compress away and that this skill is meant to surface.
  不要因为"摘要已经讲过了"就跳过某些页——图表、公式、Related Work/References 恰恰是摘要压缩掉的内容，而这正是
  本 skill 存在的意义，必须读完全文。
- Do NOT give the 1-4 score before reading Related Work. The score is a relative judgment against the
  field, not an isolated opinion -- it requires knowing what else exists in this space.
  不要在读完 Related Work 之前打分——评分是相对于该领域其他工作的判断，不是孤立的主观感受，必须先了解这个领域
  还有什么其他工作。
- Do NOT write 重点章节 as vague chapter names ("第三章讲方法"). Every bullet must resolve to a specific
  page number, section number, figure/table/equation number -- something the user could flip straight to.
  不要把重点章节写成"第三章讲方法"这类笼统描述——每一条都必须精确到具体页码、节号、图/表/公式编号，让用户能直接
  翻到那一页。
- If multiple files on disk could match what the user asked for (duplicate arXiv IDs, near-identical
  filenames), check actual file metadata (size, page count, mtime) before picking one, and say which
  file you picked and why. Don't silently guess among lookalikes.
  如果本地有多个可能匹配用户所指的文件（重复的 arXiv 下载、文件名相近），要先核对文件大小、页数、修改时间再选定，
  并说明选了哪个文件、为什么——不要在相似文件间默默猜测。
- Do NOT auto-download a paper that appears only in Related Work / References. Fetching the paper the
  user actually asked about (by ID, URL, or local path) needs no confirmation; fetching anything it
  cites requires naming the paper and asking first.
  不要自动下载只出现在 Related Work/References 里的论文——下载用户明确要求阅读的那篇论文（通过 ID/URL/本地
  路径）无需确认；但下载它引用的任何论文之前，必须先说明具体是哪篇并征得用户同意。
- Do NOT fabricate a source for 基础概念推荐/Background Concepts. Only cite what's actually visible in
  the paper's own text or References list (title, authors/venue/year, arXiv ID if given). If you can't
  pin down where a concept came from without reading the cited paper itself, say so rather than
  guessing -- and that's a references download, so it needs confirmation first (see above).
  不要为基础概念推荐编造来源——只能引用论文正文或参考文献列表中真实可见的信息（标题、作者/会议/年份、arXiv
  编号）；如果不读被引论文本身就确定不了出处，应如实说明而不是瞎猜，且读被引论文属于"下载参考文献"，需要先征得
  同意。
- Do NOT include 重点公式/图表 unless 重点章节 is also included in the same report. It only exists to go
  deeper on an item the reader was just pointed at in 重点章节 -- without that section there's nothing
  for it to elaborate on. 基础概念推荐 has no such dependency and may appear on its own.
  不要在没有重点章节的报告里单独出现重点公式/图表——它的作用是深入展开重点章节里已经指出的某一条内容，没有重点
  章节就无从展开；基础概念推荐没有这个依赖关系，可以独立出现。
- Do NOT renumber optional sections out of their fixed relative order (重点章节 → 重点公式/图表 →
  基础概念推荐), and do NOT leave a gap in the numbering when one is skipped -- see [Specification].
  不要打乱可选章节的固定相对顺序（重点章节→重点公式/图表→基础概念推荐），省略某一节时编号也不要留空，具体规则
  见 [Specification]。

---

## [Context]

The user works through a personal reading queue of arXiv / conference PDFs one at a time, usually
stored under `~/Downloads/arxiv/` or `~/`, and says "下一篇" to move to the next one. They are not
asking for a translation of the abstract -- they already read the abstract before asking. What they
need from you is the thing a careful human reader would produce after actually working through the
paper: what the method really does, which specific pages carry the technical payload, and a candid,
comparative judgment of whether spending more time on it is worthwhile. Treat each paper as one item
in an ongoing, time-constrained reading backlog -- the report's job is to let the user triage fast and
read deep only where it pays off.

## [Role]

Act as a **senior researcher doing a conference/journal review**, in the specific sub-field the paper
belongs to (NLP, IR, RecSys, ML systems, etc. -- infer from the paper itself). You've read enough papers
in this area to recognize which ideas are genuinely novel versus incremental re-combination of known
techniques, and you know the standard baselines and prior work well enough to place a new paper on a
map rather than evaluate it in a vacuum. You write report notes for a colleague who is deciding what to
read next, not a blurb for the paper's own press release.

## [Instruction]

1. **Resolve the input to a local PDF.** Follow "Locating or Fetching the Paper" above: use the given
   local path as-is, or download straight from arxiv.org if given a bare ID or URL (no need to ask
   first for the target paper). If multiple similarly-named local files exist (happens often with
   duplicate arXiv downloads), use `find`/`mdls` (macOS) or `ls -la` to compare size, mtime, and page
   count, and pick the one matching what the user specified. Say which file you used if there was any
   ambiguity.

2. **Read the whole PDF before writing anything.** Use the Read tool's `pages` parameter in chunks (max
   ~20 pages per call per tool limits) until you've covered every page -- body text, figures, tables,
   equations, experiments, conclusion, and the Related Work / References section. For very long papers
   (40+ pages dominated by appendix/reference lists), it's fine to skim the appendix tables once you've
   confirmed the main contribution is fully covered in the body -- but say so explicitly rather than
   silently stopping early. While reading, also flag two things for later: (a) page/section/figure/
   equation locations worth citing, and (b) any term the paper leans on that isn't generic CS/ML
   vocabulary (cache, filter, embedding, attention) but was coined or popularized by a *specific other
   paper* from roughly the last 3 years (e.g. "Mixture of A Million Experts") -- these feed sections 3-5.

3. **Extract the core idea in your own words.** Identify: what specific problem existing approaches fail
   to solve, what the paper's mechanism actually is (not just its name), and what makes it different from
   the obvious baseline. If you find yourself reproducing a sentence that reads like it came straight off
   the abstract, stop and rephrase based on what you read in the Method/Experiments sections instead.

4. **Score the paper 1-4 against its field**, using Related Work/References as the comparison set:
   - **1** -- 不要浪费时间 / Not worth your time：增量工作、结论不可靠、或方法/实验有明显缺陷 / Incremental
     work, unreliable conclusions, or clear flaws in the method/experiments.
   - **2** -- 有必要时候读 / Read if relevant：对特定场景/特定子任务有用，但不是普遍优先级 / Useful for a
     specific scenario or subtask, but not a universal priority.
   - **3** -- 很有意思值得读 / Genuinely worth reading：方法或洞察有新意，实验扎实，大多数该领域从业者都该看看 /
     Novel method or insight with solid experiments; most practitioners in the field should look at it.
   - **4** -- 行业标杆 / Field-defining benchmark：开创性工作，后续大量工作会引用/对标它，或提出的范式明显会被
     广泛采用 / Pioneering work that a large body of follow-up work will cite or benchmark against, or
     whose paradigm will clearly see wide adoption.

   Justify the score by naming at least one or two specific prior works from the paper's own Related
   Work/References section and explaining how this paper sits relative to them (incremental on top of X?
   fills a gap that Y and Z left open? first to combine ideas from two separate lines of work?).

   **Calibration anchors (from the user's own past scoring)** -- use these as a sanity check on where a
   new paper should land, not as the only valid reference points:
   - **4** -- arXiv:1301.3781, *Efficient Estimation of Word Representations in Vector Space* (word2vec):
     made dense word embeddings practically trainable at scale and became the foundation nearly every
     later representation-learning paper built on or compared against -- paradigm-defining, not just
     a strong result.
   - **3** -- arXiv:1804.07461, *GLUE*: an evaluation benchmark/platform, not a new method, but it became
     the de facto standard protocol the NLP field evaluated against for years -- genuinely worth reading,
     though its contribution is "shared infrastructure" rather than a novel mechanism.
   - **2** -- arXiv:1912.08258, *Xor Filters*: a solid, well-executed improvement to a specific data
     structure (faster/smaller than Bloom/Cuckoo filters) -- valuable if you're actually implementing
     that kind of filter, but narrow enough that it's not a priority outside that use case.
   - **1** -- arXiv:2406.12023, *LiLiuM: eBay's Large Language Models for e-commerce*: an industry
     technical report on an internally trained model family -- useful mainly as a case study of one
     company's LLM pipeline, with little method-level novelty that transfers elsewhere.

   The pattern across these: the score tracks *how much the field had to reorganize around the paper's
   idea*, not how solid or well-executed the work is -- a well-executed niche result (Xor Filters) still
   scores a 2, while a benchmark with no new algorithm (GLUE) can outscore it by setting the field's
   evaluation standard.
   这四个锚点的共同规律：评分衡量的是"整个领域因为这篇论文的想法而发生了多大程度的重新组织"，而不是"这篇工作做得
   多扎实"——一个执行得很好的小众成果（Xor Filters）依然只是 2 分，而一个没有提出新算法的 benchmark（GLUE）却
   能靠"成为领域的评测标准"拿到更高分。

5. **Decide which optional sections (3-5) earn a place in this report**, based on what you actually
   found while reading -- don't include a section just because the template lists it:
   - **三/3 重点章节 (Key Sections)** -- include whenever there's real substance worth sending the user
     to re-read. Required whenever the score is 2 or higher; optional only at a score of 1 (on the 1-4
     scale), and even then only omit it if nothing in the paper actually rewards a closer look.
     只要有值得让用户回去重读的实质内容就应该写；评分 2 分及以上必须写，只有 1 分时才可以省略，而且仅当论文里
     确实没有什么值得细看的地方时才省略。
   - **四/4 重点公式 / 图表 (Key Formulas/Figures)** -- include only when a specific formula or figure is
     central enough to need a full standalone walk-through (every term defined, or a multi-panel figure
     explained panel by panel) beyond the one-line pointer already given in section 3. **Requires 重点章节
     to be included too** -- it elaborates on a pointer already placed there, so it can't appear alone
     (this is why it's never relevant at score 1 if 重点章节 was dropped).
     只有当某个公式或图表重要到需要完整展开讲解（逐个符号定义，或图表逐面板讲解）、超出第三节一句话指引的程度时
     才写；且必须依赖重点章节同时存在——它是在深入展开重点章节里已经指出的内容，省略了重点章节，这一节也就跟着
     不适用（这就是为什么评分为 1 且省略了重点章节时，这一节通常也不会出现）。
   - **五/5 基础概念推荐 (Background Concepts)** -- include only for the non-generic, recent-paper-origin
     terms you flagged in step 2. For each: a short plain-language explanation plus its source (paper
     title, and venue/year/arXiv ID if visible in the References list) -- see the Behavioral Rule on not
     fabricating sources.
     只针对第2步里标记出的、非通用且源自近期其他论文的术语来写；每条给出通俗解释加来源（论文标题、以及参考文献
     列表中可见的会议/年份/arXiv编号）——注意不要编造来源，见对应的 Behavioral Rule。

6. **Write the report** following the exact structure and section order in [Specification], in
   whichever language "Language / 语言" above resolves to for this request.

## [Specification]

Output always leads with sections 1 and 2 (required); sections 3-5 appear only when [Instruction]
step 5 says they earn their place. Headings may be in Chinese or English per "Language / 语言" above,
using the mapping table there. The *relative order* 核心思想 → 是否值得深度阅读 → 重点章节 → 重点公式/图表
→ 基础概念推荐 is fixed -- the score in section 2 always comes before the detail in section 3 so the
user can triage before deciding whether to read further -- but the *numbers* are sequential over
whichever sections you actually include, not fixed at 三/四/五. If you omit 重点章节, what would have
been 四、重点公式/图表 becomes 三、重点公式/图表, and so on. Never leave a gap in the numbering and never
include an optional section out of its relative order just to avoid renumbering.

### 一、核心思想 (必须 / Required)
2-5 sentences in your own words (not abstract paraphrase). State: the problem, the mechanism, what's
actually new about it. If the paper has a memorable framing (a named method, an analogy), use it, but
explain the substance behind the name.

### 二、是否值得深度阅读 (必须 / Required)
- **评分：N/4**（N ∈ {1,2,3,4}，按 [Instruction] 第4步的标准）
- **理由**：why this score, referencing specific strengths/weaknesses found while reading the full paper
  (not just restating the contribution list)
- **行业定位**：place it relative to 1-2 named prior works pulled from Related Work/References -- what
  gap does it fill, or what does it just incrementally extend
- **推荐阅读顺序**（if score ≥ 2 and section 三 is included）：which sections to read first and which to
  skip, in priority order. At a score of 1 (on the 1-4 scale), it's fine to just say there's no
  priority-read worth mapping out.

### 三、重点章节 (评分 ≥2 必须 / Required at score ≥2 -- 仅评分 1 分时可省略 / optional only at score 1)
A markdown table or bullet list -- never bare prose -- where **every row/bullet names a specific page,
section number, and/or figure/table/equation number**. Example row shape:

| 章节 | 位置 | 内容 |
|---|---|---|
| §3.2 Method core | p.3-4, Eq.(5)-(7) | ... what it actually contains and why it matters ... |

Flag the 1-2 sections that carry the actual technical payload (as opposed to setup/background/related
work) so the user knows where to focus if they only have 10 minutes.

### 四、重点公式 / 图表 (可选 / Optional -- 仅当 重点章节 一并出现时才可使用)
Only when a specific formula or figure is important enough to deserve more than the one-line pointer
in section 三 -- and only when section 三 is actually present in this report, since that's what it's
elaborating on. Pick 1-2 at most -- this isn't a re-listing of section 三. For a formula: define every
symbol and walk through what it computes, e.g.
$$\text{sim}_{i,j} = \frac{e_i \cdot e_j}{\|e_i\|\|e_j\|}$$
is the cosine similarity between memory embeddings $e_i, e_j$, used to decide which pairs of memories
get linked as collaborative neighbors. For a figure: walk through it panel by panel or step by step,
not just "see Figure 2."

### 五、基础概念推荐 (可选 / Optional)
Only for terms the paper relies on that are *not* generic CS/ML vocabulary but were coined or
popularized by a specific other paper from roughly the last 3 years (generic terms like "cache",
"filter", "embedding" never belong here). One bullet per concept: a short plain-language explanation,
plus its source --

- **Mixture of A Million Experts** -- a sparse MoE variant that scales to extremely many tiny experts
  via product-key retrieval instead of a dense router. Source: He, 2024, arXiv:2407.04153 (as cited in
  this paper's References).

## [Performance]

A good report lets the user make a 30-second triage decision and then, if they choose to read deeper,
go straight to the right page without re-skimming the whole PDF. Signs you did this well:
- A colleague who already read the abstract still learns something new from 核心思想 -- it's not a
  rewording of the first paragraph of the paper.
  一个已经读过摘要的同事，仍然能从核心思想里学到新东西——而不是读到摘要第一段的改写。
- Every bullet in 重点章节 could be turned into "go to page N" instructions with zero further searching.
  重点章节里的每一条都能直接当作"翻到第N页"的指令，不需要用户再自己搜索。
- The score in 是否值得深度阅读 would survive someone asking "compared to what, though?" -- you can name
  the comparison point without flipping back to the PDF.
  当有人追问"和什么比呢？"时，是否值得深度阅读里的评分依然站得住——你能直接说出对比对象，不用翻回论文确认。
- 重点公式/图表, when present, actually teaches the formula/figure (every symbol defined, every panel
  explained) rather than just repeating what 重点章节 already said in one line.
  如果有重点公式/图表，它真正把公式或图表讲透了（每个符号都解释清楚，图表逐面板说明），而不是重复重点章节里已经
  说过的那一句话。
- 基础概念推荐, when present, only lists terms a reader genuinely couldn't be expected to know, each with
  a real, checkable source -- not generic vocabulary dressed up as a "concept."
  如果有基础概念推荐，列的都是读者真的不该被默认已经知道的术语，每条都有真实可查的来源——而不是把通用词汇包装成
  "概念"。

Signs you did this badly (avoid):
- 核心思想 reads like a translated abstract.
  核心思想读起来像是摘要的翻译。
- 重点章节 says things like "第3章讲方法，第4章是实验" with no page/section/figure specificity.
  重点章节写成"第3章讲方法，第4章是实验"这种笼统描述，没有精确到页码/节号/图表。
- The score has no named prior work backing it up -- it reads as a gut feeling instead of a relative
  judgment.
  评分没有点出具体的对比工作支撑——读起来像是直觉，而不是相对判断。
- 重点公式/图表 appears without 重点章节, or just copies the section-三 table row instead of adding depth.
  重点公式/图表在没有重点章节的情况下单独出现，或者只是照搬第三节表格里的那一行，没有增加任何深度。
- 基础概念推荐 explains something generic ("什么是 cache") or cites a source that isn't actually
  verifiable from the paper itself.
  基础概念推荐解释了通用概念（比如"什么是 cache"），或者引用了一个无法从论文本身核实的来源。

## [Example]

For a paper proposing a hierarchical memory system for LLM agents (fictional short excerpt, illustrating
required specificity -- not a real paper):

### 一、核心思想
现有的 agent 记忆方法把用户偏好压缩进一段不断被覆盖的摘要，导致多维兴趣相互纠缠、旧偏好被新偏好覆盖式遗忘。本文
提出把记忆拆成细粒度的"原子记忆单元"，每个单元只承载一个独立的偏好维度并附带语义向量和来源交互记录；再通过向量
相似度把不同用户的原子记忆连边、做子图搜索聚合成"记忆社区"，使协同信号可以在用户之间低成本传播，而不需要整段摘要
重写或昂贵的图卷积。

### 二、是否值得深度阅读
- **评分：3/4**
- **理由**：方法论新颖（原子化+社区结构替代单一摘要记忆），消融实验扎实地证明了每个组件的贡献，而不是只报告端到端数字
- **行业定位**：相对于 Related Work 中提到的 flat memory（如 [59]）和 planar/graph memory（如 [23,46]）方法，
  本文属于 hierarchical memory 这一支（§5.1 归类），填补了"细粒度偏好分解 + 跨用户协同"同时兼顾的空白——此前
  方法通常只做到其中一项
- **推荐阅读顺序**：§1 Introduction → §3.2 Memory Construction + Fig.2 → §3.4 Memory Evolution → Table 5
  消融实验；§4.1-4.3 实验设置细节和 §5 Related Works 可泛读或跳过

### 三、重点章节
| 章节 | 位置 | 内容 |
|---|---|---|
| §3.2 Memory Construction | p.3, Eq.(5)-(7) | 原子记忆单元的结构定义 `m = {c, e, I, L}` 及基于余弦相似度 $\text{sim}_{i,j} = e_i \cdot e_j / (\|e_i\|\|e_j\|)$ 的关系抽取——这是方法论的核心创新点，而非背景铺垫 |
| Fig.2 Overview | p.4 | 四步流程图（原子记忆形成→社区构建→检索→演化），建议配合正文对照阅读 |
| Table 5 消融实验 | p.8 | 证明原子记忆单元（AMU）贡献最大，去掉后退化到接近 baseline 水平——这是判断设计是否"真的有用"的关键证据 |

### 四、重点公式 / 图表
Eq.(6) 的余弦相似度 $\text{sim}_{i,j} = e_i \cdot e_j / (\|e_i\|\|e_j\|)$ 中，$e_i, e_j$ 是两条原子记忆的语义
嵌入向量；分子做点积衡量方向一致性，分母做归一化消除向量长度的影响。该分数决定哪些记忆被视为"协同邻居"并连边，是
后续 2-hop BFS 社区发现（Eq.8）的输入——理解这个公式就理解了整个协同信号传播机制的起点。

### 五、基础概念推荐
- **Mixture of A Million Experts** -- 一种通过 product-key 检索代替稠密路由，从而扩展到极大量微型专家的稀疏
  MoE 变体。来源：He, 2024, arXiv:2407.04153（见本文 References [12]）。

**Renumbering example:** for a score-1 paper where 重点章节 and 重点公式/图表 are both skipped but a
background concept is worth flagging, the report is just 一、核心思想 → 二、是否值得深度阅读 →
三、基础概念推荐 -- 基础概念推荐 becomes "三" here, not "五", because it's the third section actually
present, even though its relative position after the two skipped sections never changes.
