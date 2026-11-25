# 遗传变异致病性分析（v0.5.1-test 离线草稿）

## 模块 1：Classification Hero

- 正式分类：未完成；本输出不可直接用于临床签发。
- 变异：未提供/未评估
- 优先核查框架：Tavtigian_2020_points
- 测试候选分区：LP
- 积分：9
- 2015组合对照：VUS
- 对照状态：test_only
- 框架差异：True
- 基因—疾病关联：未提供/未评估
- 本样本检出可信度：未提供/未评估
- 报告位置：仅建议；待本机构政策审核。

## 模块 2：Molecular Profile

未提供/未评估

样本质控：{"status": "not_evaluated", "automatic_acceptance": false, "mcc": null, "vaf": null, "depth": null, "mosaicism": null, "validated_lod": null, "gonadal_risk_upper_bound": null, "reason": "local assay validation and SOP absent; values retained for manual review"}

## 模块 3：ACMG证据链

| 证据ID | 代码 | 分值 | 原因 |
|---|---|---|---|
| e0 | PM2_Supporting | 1 | synthetic test |
| admitted:a1:0 | PVS1_VeryStrong | 8 | synthetic test only |

按适用规则审核的候选：LP

通用积分对照（不得覆盖专病结论或流程阻断）：LP

逐例规则检索、辅助重算及审核接入轨迹：

```json

{
  "routing": {
    "identity": {
      "variant_id": "synthetic-v1",
      "gene": "SYNTHETIC",
      "disease": "synthetic disease",
      "inheritance": "AD",
      "subject_id": "synthetic-subject"
    },
    "review": {
      "approved": true,
      "reviewer": "synthetic reviewer",
      "reviewed_at": "2026-09-27",
      "source": "synthetic test NOT medical evidence",
      "location": "fixture",
      "rationale": "synthetic test only"
    },
    "search_completed": true,
    "outcome": "none_found",
    "searches": [
      {
        "url": "https://cspec.genome.network",
        "query": "SYNTHETIC",
        "accessed_at": "2026-09-27",
        "result": "synthetic negative; not an actual search"
      }
    ]
  },
  "admission_audit": [
    {
      "id": "a1",
      "kind": "pvs1",
      "recomputed": {
        "tool": "pvs1_review",
        "source": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6185798/",
        "status": "test_calculation_only",
        "blockers": [],
        "path_results": [
          {
            "scenario_id": "scenario1",
            "path_id": "N01",
            "nodes": [
              "60",
              "61",
              "63",
              "65"
            ],
            "source_tree_output": "PVS1",
            "tree_strength": "VeryStrong",
            "global_exclusions": []
          }
        ],
        "tree_strength": "VeryStrong",
        "adjusted_strength": "VeryStrong",
        "mechanism_tier": "G1",
        "automatic_score_import": false,
        "evidence_code": null,
        "classification": null
      },
      "selected_codes": [
        "PVS1_VeryStrong"
      ],
      "blockers": [],
      "basis_ids": [
        "synthetic-pvs1-basis"
      ],
      "source_ids": [
        "fixture"
      ]
    }
  ],
  "ba1_exception_check": null,
  "blockers": []
}

```

排除项：[]

阻断项：[]

组合命中/限制：{"framework": "ACMG_2015_Table5_on_reviewed_strengths", "candidate": "VUS", "matched_rules": [], "status": "test_only", "reasons": [], "note": "2015 combining structure on supplied strengths; no automatic strength restoration or later combination amendments"}

## 模块 4：临床数据库综合查询

未提供/未评估

## 模块 5：External Benchmarking

未提供/未评估

## 模块 6：判读决策报告

积分优先显示，2015组合按已审核强度独立对照；结果不一致时不自动取较高等级。

Compare strengths and framework versions; do not select the higher category

## 模块 7：关联遗传病画像

未提供/未评估

## 模块 8：临床证据补充与产前说明

保留家系、相位、第二打击和随访需求；本草稿不生成个体预后百分比或再发风险数值。

未提供/未评估

## 模块 9：References

实际核验：{"total": 0, "metadata_verified": 0, "claim_verified": 0, "fully_verified": 0, "coverage_percent": null, "status": "not_applicable"}

## 模块 10：局限性声明

AI辅助迁移测试报告；规则适用性、来源和最终结论需专业审核。离线测试不证明临床有效性。

Re-evaluation triggers：新表型、家系、功能数据、数据库或规则版本变化。

Evidence snapshot：未提供/未评估
