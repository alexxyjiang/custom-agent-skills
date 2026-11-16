# Relation evidence and navigation / 关系证据与导航

## Type semantics / 类型语义

For `from=A, to=B`, write a statement in that direction. More than one edge type is possible only when each has its own evidence; a citation does not entail support or extension. Keep claims narrow enough that the supplied evidence can actually establish them.
当来源为 A、目标为 B，按该方向写表述。多类型须各自有证据；引用不自动代表支持或扩展。主张范围应窄到证据确能证明。

| Type / 类型 | Meaning and minimum evidence / 含义与最低证据 |
|---|---|
| `cites` | A explicitly references B. Locate A's citation context/reference entry and resolve B's exact identity/version. Bibliographic metadata may establish only a clearly labeled citation-record statement. / A 明确引用 B；定位 A 引文上下文/条目并核实 B 身份版本，元数据最多证明明确标注的引用记录。 |
| `extends` | A materially builds on or changes a specific component of B. Inspect A's modification and B's original component with locators; author self-description alone is not enough. / A 实质沿用或修改 B 的具体部件；须双端方法定位，仅作者自称不够。 |
| `supports` | A supplies relevant evidence consistent with a specific claim of B under stated conditions. Check both claims, outcome direction, design quality and scope. This is not automatically independent replication. / A 在限定条件下提供与 B 某主张一致的证据；核对双端主张、结果方向、设计质量和范围，不自动等于独立重复验证。 |
| `contradicts` | A supplies evidence incompatible with B's specific claim under sufficiently aligned assumptions/protocols. Different tasks or metric values alone do not contradict. If alignment is unproven, leave the contradiction provisional/unresolved. / A 在足够对齐的假设/协议下提供与 B 具体主张不相容的证据；任务/指标数值不同不算矛盾，对齐未证明则暂定或未解决。 |
| `similar` | A and B share a precisely identified idea, mechanism or setup. Inspect both described aspects; do not infer citation, influence, superiority or common lineage. Orient A→B for the selected reading route and explain that similarity itself is symmetric. / 共享明确思想、机制或设定，须检查双端对应部分；不推断引用、影响、优劣或共同源流。A→B 为阅读路线，说明相似本身对称。 |
| `replicates` | A independently tests a specified result of B using an adequately comparable method/protocol and reports the outcome, whether successful or failed. Check investigator independence, data/protocol provenance, execution and numerical evidence/uncertainty, and resource limitations; disclose shared artifacts. Code availability, author's rerun, a citation, reproduction intent or a toy run does not establish this relation. / A 独立以充分可比方法/协议检验 B 的指定结果并报告成功或失败；核查研究者独立性、数据/协议来源、执行、数值证据/不确定性及资源限制，披露共享材料。开源、作者重跑、引用、复现意图或玩具运行均不够。 |

A failed independent replication may be `replicates` with an explicitly negative outcome and also `contradicts` if that separate statement is justified. Never equate `replicates` with success. If independence or comparability is unknown, the replication edge cannot be verified; use a narrower verified `supports`/`similar` only if its own evidence suffices, not as a cosmetic downgrade.
独立重复验证失败仍可为 replicates 并明确负面结果；若另有依据也可建立 contradicts。replicates 不等于成功。独立性或可比未知不能核实复现边；只有独立证据足够时才选更窄的 supports/similar，不能为美化而降级替换。

## Endpoint evidence protocol / 双端证据流程

1. Resolve exact paper/version and distinguish preprint vs publication from independent studies. Do not mix v1 claims with v3 locators without checking them. Store versioned paper `source_url`/`version`, and endpoint claim `url`, `locator`, `kind`, `limits`.
   核实精确论文/版本，区分预印本/正式版与独立研究；未检查不能混用 v1 主张与 v3 定位。记录版本来源和双端主张 URL、定位、种类及局限。
2. Inspect the actual relevant passages and table/figure/proof when available within approval. Add claims for the inspected citation context or identity if needed. The relation evidence list resolves to claims on both `from` and `to`; optional third-paper evidence supplements but cannot replace the endpoints.
   在授权内检查实际相关段落与图表/证明；必要时添加引用上下文或身份主张。证据列表须能解析到来源与目标双方主张，第三方证据只能补充，不能代替双端。
3. Record what was read and what remains unread. A paper-wide `partial` status does not prevent verification of a narrowly supported citation, but cannot justify uninspected methods/results. Metadata-only evidence cannot verify scientific replication or causal validity.
   记录已读/未读。部分覆盖不阻止核实证据充分的窄引用，但不能支持未检查的方法/结果；元数据不能核实科学重复验证或因果有效性。
4. State comparability with specific reasons: tasks/populations, splits/data versions, metrics/scales/direction, evaluation/tuning, compute and uncertainty/seeds. `comparable` is claim-specific, not a blanket paper endorsement. If not comparable, describe differences qualitatively without normalizing numbers by guesswork.
   按任务/人群、划分/数据版本、指标/量纲/方向、评测/调参、算力和不确定性/种子说明可比性。可比仅针对具体主张，不是整篇认可；不可比则定性说明，不猜测归一化数值。
5. Choose status and show gaps. Store missing checks in relation `statement`, evidence claim `limits`, and the report review table. An unresolved edge can have an empty evidence array, but may not have dangling claim references or fake source passages.
   选状态并显式写缺口，放关系表述、证据主张局限及报告复核表。未解决边证据可空，但不能引用悬空主张或伪造来源段落。

## Navigation handoff / 导航交接

Use stable `(paper_id, slide_id)` pairs. Example: relation `from: paper-a`, `to: paper-b`, `navigation: {"from_slide":"method", "to_slide":"baseline"}` resolves `method` inside paper-a and `baseline` inside paper-b. Source slide links contain `{"paper_id":"paper-b","slide_id":"baseline","label":"Extends baseline — provisional / 扩展基线—暂定"}`. The label must match the actual edge type/status. Both papers may have a `method` slide; never resolve by slide id globally.
使用稳定论文/页二元组。上述例子中 method 属于 paper-a，baseline 属于 paper-b；来源链接按示例指向目标并显示实际类型/状态。两篇可同有 method 页，不能全局仅按页 id 查找。

Author focused relation explanations, evidence/gap cards and navigation data in the bundle. Let the writer choose layout, rendering technology, global controls and final HTML integration. Do not generate a competing complete HTML application. Validate references again if the writer changes anchors; building is not verification of the graph.
在包内写聚焦关系说明、证据/缺口卡片和导航数据；布局、渲染技术、全局控件及最终 HTML 集成由 writer 负责，不另造竞争性完整 HTML 应用。writer 改锚点后重查引用；构建不等于图已核实。
