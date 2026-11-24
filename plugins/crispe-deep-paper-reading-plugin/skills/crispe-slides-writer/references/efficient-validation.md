# Efficient loading and verification / 高效加载与验证

## Load by task / 按任务加载
| Task / 任务 | Load / 加载 |
|---|---|
| Existing prose correction / 既有文字纠正 | affected JSON/claims + contract only if fields change / 改动JSON与主张，字段变化才读契约 |
| New deck or layout change / 新deck或版式变化 | contract + design; adaptive/figure guidance only for affected visuals / 契约与设计，涉及图才加载图参考 |
| Formula or walkthrough repair / 公式或步骤修复 | affected slide/example + design's matching section / 改页或示例与设计对应章节 |
| External authoring setup / 外部写作配置 | html-slides integration, once per revision / 集成参考每版本一次 |
| PDF requested / 请求PDF | PDF skill after HTML verifies / HTML验过再读PDF技能 |

Use existing structured claims/visuals/reports. Read original paper passages only for missing/conflicting evidence; do not repeat scientific reading for a presentation-only change. Keep Chinese/English requirements paired but hand off ids, paths and gaps rather than repeat every rule.
复用结构化主张/图/报告；缺证据或冲突才回查原文，呈现改动不重复科学阅读。保留双语规范，交接传id/路径/缺口，不重述全部规则。

## Verification levels / 验证分级
- **content**: require explicit deck and canonical slide ids; test those pages at desktop/phone, including all steps/details, figure zoom, bounds and canonical links. Changes to cached shared scripts/styles, tool fingerprint or environment promote to layout across the locale. Use layout for changed anchors/order/links or unknown scope.
  内容档须指定deck及正式页id，桌面/手机检查改页所有步骤/详情、图放大、边界和链接。缓存的共享脚本样式/工具/环境变动升级到语言目录版式档；锚点/顺序/链接变动或范围不明直接用版式档。
- **layout**: test all slides in selected decks at 1600×900 and 390×844; shared generator changes require every affected locale/deck. Includes basic navigation and each interactive state; no research/benchmark rerun.
  版式档测选定deck全部页及交互状态，共享生成器变动覆盖所有受影响语言/deck；无需重跑研究/模型基准。
- **full**: runner tests every locale deck at four viewport sizes over file. For publication/runtime changes also run the existing file/HTTP browser suite, real/virtual autoplay regression and PDF export checks when requested. Runner's full level alone is not this complete release gate.
  完整档入口对语言目录全部deck测四视口/file。发布或运行库改动还须原file/HTTP浏览器套件、真实/虚拟计时及请求的PDF导出；入口full不单独代表整个发布门禁。

```bash
uv run --offline --with playwright python <skill-dir>/scripts/verify_site.py site/zh-CN --level layout --cache ./checks.zh-CN.json
uv run --offline --with playwright python <skill-dir>/scripts/verify_site.py site/zh-CN --level content --deck paper.html --slide slide-method --cache ./checks.zh-CN.json
# Explicit rerun / 强制重跑
uv run --offline --with playwright python <skill-dir>/scripts/verify_site.py site/zh-CN --level full --fresh --cache ./checks.zh-CN.json
```

## Fingerprints and reports / 指纹与报告
Cache only passed results keyed by exact site bytes, checker/runtime assets, browser/Playwright/platform/font inventory, level, selected slides and viewports. Default expiry is 24 hours; --fresh bypasses reuse. Hash site bytes once before and once after the batch, not around every DOM assertion. Changes during checks prevent cache publication. Reports list actual executed/reused deck coverage and elapsed seconds; output only a short summary/failures, retain detailed bounds in the report. No screenshot or human visual approval is inferred. Cache is a local optimization, not signed proof: do not accept untrusted cache files as certification.
缓存仅存通过结果，键含站点字节、检查器/运行资源、浏览器/Playwright/平台/字体清单、档位/选页/视口；默认24小时过期，fresh不复用。整批前后各哈希一次，不每次DOM断言重读站点；中途变动不发布缓存。报告标真实执行/复用覆盖及秒数，终端仅摘要/失败，详细边界存报告。不推断截图或人工视觉通过；本地缓存不是签名证明，不把不可信缓存作认证。

Keep research coverage, source approvals, visual provenance and explicit dependency setup unchanged. Record token counts only if the host supplies them; bytes/word counts are size proxies, not measured tokens.
阅读覆盖、来源授权、原图溯源及依赖配置要求保留。token只记录宿主提供值，字节/词数只是体积代理而非实测tokens。

## Measured regression / 实测回归
On the existing 15-slide InstructGPT locale deck, one local run measured the verification loop at about 2.8s for layout, 1.6s for one-page content and 0.27s for exact-result reuse. These figures exclude process startup, dependency/browser-version and font inventory setup; they are not end-to-end or token savings guarantees. The optimization regression works in a temporary copy and verifies byte changes, runtime promotion, fresh reruns, overflow rejection and failure nonreuse.
既有15页InstructGPT目录实测检查循环：版式约2.8秒，单页约1.6秒，精确复用约0.27秒。该数值不含进程启动、依赖/浏览器版本及字体清单准备，不是端到端或token节省承诺。回归只在临时副本操作，验证字节变化、运行升级、强制重跑、溢出失败及失败不复用。

```bash
uv run --offline --with playwright python <skill-dir>/evals/optimization_check.py site/zh-CN --deck paper.html --slide slide-method
```
The new runner checks paper decks over file only, not collection-entry interactions, cross-locale switching, real-time autoplay, PDF bytes or scientific content. Retain the existing suites for those release gates; never report this narrower pass as full end-to-end acceptance. No source site is rewritten by verification.
新入口仅检查论文deck/file，不测集合入口交互、跨语言切换、真实自动播放、PDF字节或科学内容；相应发布门禁继续使用原套件，不把窄范围通过称为全链验收。验证不改源站点。

## Parallel batches / 并行批次
For independent frozen decks/locales, dispatch bounded verification workers with separate cache/report paths (never concurrent writers to one cache). Reuse first, then check disjoint inputs. Final site consistency, collection links and aggregate release status are coordinated after all relevant workers complete. PDF exports follow the same path isolation and browser-memory limit. Parallelism reduces wall-clock latency, not necessarily total tokens/CPU; per-worker lean context and reuse address those costs.
冻结后独立deck/语言可有限并行验证，缓存报告独立，禁止同时写同缓存；先复用再检查独立输入。全部相关worker完成后主控核对整站/集合链接及汇总发布状态。PDF同样输出隔离并限制浏览器内存。并行主要降低墙钟延迟，不保证总token/CPU下降；精简worker上下文和复用才减少总成本。
