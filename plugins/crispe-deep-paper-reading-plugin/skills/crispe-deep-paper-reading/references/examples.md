# Examples / 示例

## 1. Named offline set / 具名离线集合

**EN request:** "Read the two supplied versioned PDFs A v2 and B v1 fully, then make a linked Chinese reading deck. Stay offline; do not execute examples."
**中文请求：** “完整阅读提供的 A v2、B v1，做互链中文阅读演示。离线，不运行示例。”

**Expected:** set `language: zh-CN`, metadata budget 0, full-text cap 2 and approved identities A v2/B v1. Read all pages with the analyst; create relative reports and accurate coverage. Cross-link only supported claims, use `not-run` for examples, and hand the bundle to the writer. No new approval for those targets, no online lookup/install, no claim of external impact verification. If public pinned URLs cannot be resolved offline from supplied provenance, report the final-handoff blocker rather than inventing URLs.
**预期：** 中文、元数据预算零、全文上限二及双目标版本授权；分析师逐页读，生成相对报告与真实覆盖，关系有证据才建，示例未运行，交包给 writer。不重复授权、不联网/安装、不声称外部影响已核实；现有材料无法提供固定公开 URL 时报告最终交接阻塞，不伪造。

## 2. Topic discovery with bounded approval / 主题发现与有界授权

**EN request:** "Find a small reading set on retrieval memory: at most 8 metadata records and 2 full texts; ask me before reading discovered papers. Stop after 2 queries or 10 minutes."
**中文请求：** “找检索记忆小型阅读集：最多 8 条元数据、2 篇全文，新发现论文先问我；2 次查询或 10 分钟即停。”

**Expected:** log queries and all candidate decisions/counts before deduplication, stop on the earliest condition, propose named versioned targets A/B, and wait before fetching either. If only A is approved, read only A and leave B deferred. Do not chase A's references or retrieve a third paper via a companion. A one-paper bundle with no relations is valid.
**预期：** 记录查询、全部候选决策与去重前计数，最先条件触发即停；提具名版本 A/B 并等待全文授权。只批 A 就只读 A，B 暂缓；不追 A 引文或借协作取第三篇。单论文无关系包有效。

## 3. Partial access and unavailable writer / 部分访问与写作器不可用

**EN request:** "Turn these approved papers into a linked deck; one PDF has unreadable appendix pages and the slides writer is not available."
**中文请求：** “把获批论文做互链演示；一篇附录页无法读取，且 slides writer 不可用。”

**Expected:** retain `partial`, enumerate unread appendix pages/reasons, preserve the analyst's full-reading requirement and mark its checkpoint incomplete. Use only supported narrow relations, show missing writer original-source guidance before handoff, and deliver an honestly limited bundle/pending presentation status. Do not call it full reading or completed HTML, fabricate replication, or use builder success as evidence.
**预期：** 保留部分覆盖，列未读附录页及原因，保留全文义务并标检查点未完成；只建证据充分窄边，交接前提示 writer 原始来源安装命令，交有限包并标待呈现。不冒称全文完成/HTML 完成、不编复现、不把构建当证据。
