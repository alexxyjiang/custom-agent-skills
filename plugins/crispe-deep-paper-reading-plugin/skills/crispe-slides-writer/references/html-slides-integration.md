# html-slides dependency and Reveal adapter / 外部依赖与Reveal适配

## Dependency discovery / 依赖发现
Source: claude-office-skills/skills, skill html-slides. Prefer the host loader/registry, then configured project/user roots and common ~/.agents/skills or ~/.claude/skills fallbacks. Read the actual definition before using it. Resolve helpers relative to the loaded skill. The currently inspected definition contains reveal.js guidance/examples only, no executable generation service; its description may be merely “>”. Explicit name/path loading is therefore important. Do not edit the external definition or assume its office-mcp metadata is a required runtime.
来源如上，优先宿主再配置及常见根目录；使用前读真实定义，脚本相对所加载目录。当前外部定义只有Reveal指导示例，无生成服务，描述可能只是大于号，需显式名称/路径加载。不改外部定义，也不把office-mcp元数据当必需运行依赖。

```bash
npx skills add claude-office-skills/skills --skill html-slides -g -a claude-code -a github-copilot -a opencode
```

Show the verified command only for missing dependencies; execute installs only on explicit request. Distinguish definition-readable, missing and installed-but-unusable with the actual cause. A resolved-definition hash is provenance, not proof of agent execution. The assembler checks readable dependency presence for generation; --check remains dependency-free. No plugin manifest field pretends to auto-install external skills.
仅缺失提示核实命令，明确要求才安装；区分定义可读、缺失、运行不可用。哈希只是来源不代表执行，生成装配检查可读依赖，check不依赖外部；不造插件自动安装字段。

## One-way authoring handoff / 单向写作交接
Orchestrator → writer → html-slides, once per site. Supply approved versions/scope, project.<locale>.json, reports/claims, original figures, code/actual execution records, output directory and all design constraints. Request reveal.js section structure and events with no research, no extra full texts, installs, paid calls or deployment. The same agent may load and execute the external instructions; no subagent is implied. Keep authored output and verification records in examples for the regression run.
编排→writer→外部技能，每站一次。传授权版本范围、项目、证据原图、代码实际运行及输出目录和全部视觉要求；只求Reveal结构事件，不研究/扩全文/安装/付费/部署。同一agent可执行，不隐含委派；回归保留写作结果及记录。

## Ownership and conflicts / 职责与冲突
- Reveal owns stage scaling, slide state, navigation/touch and fragments. The adapter handles fixed reading chrome, legacy #slide-id hashes, title updates, TOC/focus and locale links. No second show/hide engine or custom scale calculation.
  Reveal负责画布缩放、状态、导航触控及fragments；适配保留阅读框架、旧锚点、标题/目录焦点/语言链接，无第二显隐或缩放引擎。
- Prism is the only tokenizer/theme. Do not load RevealHighlight/highlight.js or Monokai. Fragments/step controls drive the existing exact line wrappers; current lines scroll into view and copy is source-only. Page autoplay skips remaining fragments by calling Reveal.slide for the next page, avoiding hidden extra timing.
  Prism唯一分词配色，不启Highlight插件；fragments和按钮驱动精确行包装，滚动当前行并纯源码复制。页面播放直接下一页，不受隐藏步骤多计时影响。
- Keep one observable autoplay scheduler for four durations, waits and recovery. Reveal autoSlide is disabled to avoid two timers. Native Reveal basics replace generic mechanics; paper-specific recovery is retained and tested.
  一套可观察播放调度，Reveal autoSlide关闭，避免双计时；保留并测试论文专门恢复。
- Keep KaTeX, math/layout fitting, original-figure extraction/masks and locale/score/evidence schema. Do not use stock themes or r-fit-text to erase specified design/type sizes. All Reveal/Prism/KaTeX runtime resources are pinned and embedded offline; only external skill knowledge is an external dependency.
  保留数学/图布局、原图蒙版及语言评分证据；不套默认主题或缩字抹设计。三个运行库固定内嵌离线，外部技能为知识依赖。
- PDF uses print-pdf, pdfSeparateFragments=false, stopped playback and complete code states. crispe-slides-to-pdf owns actual file export/checks. Overflow is rejected, never hidden with a one-page print limit.
  PDF用专门打印模式、步骤合并、停播及完整代码，独立技能导出验证；溢出拒绝，不靠单页限制隐藏。

## Compatibility and cleanup / 兼容与清理
The assembler keeps the v1 project contract/CLI, plus optional --html-slides for an explicitly resolved external definition. General reveal.js tutorial prose belongs externally, not duplicated in this plugin. The old custom stage scaler and slide visibility implementation are replaced; unused Tomorrow theme/reset distribution are removed. Tests query actual section.slide, never Reveal-generated slide-background divs. Existing #slide-id entry links and cross-paper identities remain stable. Do not remove specialized tools until corresponding output regressions pass.
装配保留v1项目/CLI，可用可选参数显式外部路径。通用Reveal教程归外部不复制；旧缩放/显隐替换，未用主题资源删除。测试查真实section而非背景div；旧锚点/论文身份保留，专门工具仅替代回归通过才移除。
