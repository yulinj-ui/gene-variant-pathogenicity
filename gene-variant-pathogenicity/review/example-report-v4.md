# 遗传变异致病性分析（v0.4.0-test 离线草稿）

## 模块 1：Classification Hero

- 正式分类：未完成；本输出不可直接用于临床签发。
- 变异：未提供/未评估
- 优先核查框架：Tavtigian_2020_points
- 测试候选分区：VUS
- 积分：1
- 2015组合对照：VUS
- 对照状态：test_only
- 框架差异：False
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

辅助计算（未导入主积分；正式证据代码为空）：

```json

{
  "locus_review": {
    "tool": "locus_review",
    "rule_source": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10806742/",
    "status": "test_calculation_only",
    "packets": [
      {
        "packet_id": "demo-packet",
        "subject_id": "synthetic-subject",
        "allele_id": "paternal",
        "variant_ids": [
          "demo-v0",
          "demo-v1"
        ],
        "basis_ids": [
          "synthetic-observation"
        ],
        "mode": "pp4_equal",
        "source": {
          "kind": "published",
          "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10806742/",
          "version": "2024",
          "location": "Figure 2; synthetic fixture, not a patient",
          "gene": "CTNS",
          "disease": "synthetic cystinosis scenario",
          "phenotype_definition": "synthetic matched phenotype",
          "testing_method": "synthetic matched method"
        },
        "status": "test_calculation_only",
        "blockers": [],
        "results": [
          {
            "variant_id": "demo-v0",
            "allocated_probability": "0.479",
            "table2_points_before_cap": "2.5",
            "review_points": "2.5",
            "table4_maximum_options": null,
            "evidence_code": null,
            "classification": null
          },
          {
            "variant_id": "demo-v1",
            "allocated_probability": "0.479",
            "table2_points_before_cap": "2.5",
            "review_points": "2.5",
            "table4_maximum_options": null,
            "evidence_code": null,
            "classification": null
          }
        ],
        "automatic_score_import": false,
        "evidence_code": null,
        "classification": null,
        "allocation": {
          "input_probability": "0.958",
          "allocated_sum": "0.958",
          "method": "probability_first_equal_split_then_Table2_floor_then_per_variant_cap"
        }
      }
    ],
    "automatic_score_import": false,
    "evidence_code": null,
    "classification": null,
    "limitations": [
      "No automated pedigree counts, BS4, unequal allocation or main-score import",
      "Printed Table2 bounds only; no formula extrapolation or invented zero/benign evidence",
      "Review flags are caller attestations, not authentication or independent medical verification"
    ]
  }
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

未提供/未评估

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
