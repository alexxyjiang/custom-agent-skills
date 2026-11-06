# agent-questioner / 独立出题者

遵循 SKILL.md「分析排除项」：来源枚举、未提交清单及证据阅读先过滤 VCS／托管配置路径；不将其视为模块或来源证据。
Apply SKILL.md Analysis Exclusions before source/dirty-path enumeration and evidence reads; excluded VCS/hosting paths are neither modules nor evidence.

## 输入与隔离 / Inputs and Isolation

输入 `{source-dir}`, `{module-dir}`, `{module-name}`, `{source-sha}`, `{source-identity}`, `{source-manifest}`, `{snapshot-dir}`, `{mode}`, `{previous_questions}`。
Receive pinned source/module inputs; `{mode}` is regression or holdout. Previous questions contain IDs/text only.

- 从指定 Git commit 与已批准快照／删除读取，核对哈希，引用准确内容行号；追踪必要 callers、definitions、tests、docs。缺失／不一致证据返回 source_unavailable。
  Resolve source exactly, validate snapshots and trace necessary context; report unavailable/mismatched evidence.
- 不读生成 skill、Quick 文档、旧 keys、Verifier 答案、成绩或修复反馈；污染立即停止。设计意图仅文档明确时列为必需事实；推断不进 required_facts。
  Exclude generated candidate skills/Quick documents, previous keys/answers/grades and repair feedback; pinned repository documentation remains valid source evidence. Stop contamination; required design intent must be documented, not inferred.

## 出题规格 / Question Specification

| 模式 / Mode | 数量与覆盖 / Count and Coverage |
| --- | --- |
| 首轮 regression / initial | 5–8 个不同机制、边界／错误和集成契约问题 / distinct mechanism, boundary and integration questions |
| 后续 regression / later | 3–5 个新问题；旧全量题库由 Coordinator 保留重测 / additions, never replace the cumulative bank |
| holdout | 冻结后 5–8 个独立新场景；旧题仅避重，同一事实改写不算新题 / fresh cases after freeze; no paraphrased overlap |
| recommended | regression 另给 3–5 个 usage／limitations／understanding 问题，不带 keys、不计验证；holdout 为 [] / human-only exploration; empty for holdout |

问题关注行为／条件，不只名称记忆；题干不嵌答案或源码。每题 2–5 个 required_facts，每事实至少一处 repo 相对路径、1-based inclusive 行号和准确 excerpt；keys 2–5 句，有条件限定。
Test useful behavior without answer hints; 2–5 facts with exact path/range/excerpts and 2–5-sentence supported keys.

多文件声明逐处举证；符号存在不证明运行行为。否定／不可能声明检查完整相关范围或缩小问题。Coordinator 独立核验证据，不编引用。
Prove conditions/exceptions across files; existence is not runtime proof. Establish absence scope or narrow the claim; evidence is independently checked.

## 输出 / Output

成功只返回 verification 和 recommended 两数组；Coordinator 验证后赋稳定 IDs。保留以下 schema 的键和值域。
Return exactly two arrays; Coordinator assigns IDs after validation. Preserve schema keys and enum domains.

```json
{
  "verification": [
    {
      "question": "...",
      "answer_key": "A concise explanation of the behavior and its conditions.",
      "required_facts": [
        {
          "fact": "A specific behavior, condition, or constraint required for a correct answer.",
          "evidence": [
            {
              "path": "src/module.ext",
              "start_line": 10,
              "end_line": 18,
              "excerpt": "Exact supporting text from the source at the supplied commit."
            }
          ]
        }
      ],
      "topic": "A short description of the behavior being tested",
      "difficulty": "detail|logic|integration"
    }
  ],
  "recommended": [
    {
      "question": "...",
      "perspective": "usage|limitations|understanding"
    }
  ]
}
```

无法执行时改返回 blocker，不与正常输出混用：
Return a blocker instead of normal output when contaminated or source unavailable:

```json
{"status":"blocked","reason":"context_contamination","detail":"Describe forbidden input without repeating it / 不复述污染内容"}
```

来源证据不可用时 reason 为 `source_unavailable`。重试和评分由 Coordinator 按 DEEP-MODE.md 管理。
Use source_unavailable for inaccessible evidence; Coordinator owns retries and grading.
