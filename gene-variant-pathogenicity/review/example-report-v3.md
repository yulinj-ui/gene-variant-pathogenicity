# 遗传变异致病性分析（v0.3.0-test 离线草稿）

## 模块 1：Classification Hero

- 正式分类：未完成；本输出不可直接用于临床签发。
- 变异：SYNTHETIC-EXAMPLE (not a patient)
- 优先核查框架：Tavtigian_2020_points
- 测试候选分区：LP
- 积分：8
- 2015组合对照：P
- 对照状态：test_only
- 框架差异：True
- 基因—疾病关联：synthetic only
- 本样本检出可信度：not assessed
- 报告位置：仅建议；待本机构政策审核。

## 模块 2：Molecular Profile

未提供/未评估

样本质控：{"status": "not_evaluated", "automatic_acceptance": false, "mcc": null, "vaf": null, "depth": null, "mosaicism": null, "validated_lod": null, "gonadal_risk_upper_bound": null, "reason": "local assay validation and SOP absent; values retained for manual review"}

## 模块 3：ACMG证据链

| 证据ID | 代码 | 分值 | 原因 |
|---|---|---|---|
| e0 | PS1 | 4 | synthetic test |
| e1 | PS3 | 4 | synthetic test |

辅助计算（未导入主积分；正式证据代码为空）：

```json

{
  "pm3": {
    "tool": "pm3",
    "source": "https://www.clinicalgenome.org/site/assets/files/3717/svi_proposal_for_pm3_criterion_-_version_1.pdf",
    "status": "test_calculation_only",
    "blockers": [],
    "evidence_code": null,
    "classification": null,
    "case_audit": [
      {
        "id": "case0",
        "category": "plp",
        "case_points": "0.25",
        "blockers": []
      },
      {
        "id": "case1",
        "category": "plp",
        "case_points": "0.25",
        "blockers": []
      }
    ],
    "uncapped_subtotals": {
      "plp": "0.50",
      "homozygous": "0",
      "vus": "0"
    },
    "case_points": "0.50",
    "strength": "Supporting",
    "bayesian_weight": 1
  },
  "pp1pp4": {
    "tool": "pp1pp4",
    "source": "https://pmc.ncbi.nlm.nih.gov/articles/PMC10806742/",
    "status": "test_calculation_only",
    "blockers": [],
    "evidence_code": null,
    "classification": null,
    "reviewed_joint_points": "3.4",
    "maximum_code_options": [
      [
        "PP1_Supporting",
        "PP4_Moderate"
      ],
      [
        "PP4_Supporting",
        "PP1_Moderate"
      ]
    ],
    "selected_codes": null,
    "automatic_score_import": false,
    "note": "Code choice and complete 2024 workflow remain disabled; never add raw points and converted weights together"
  },
  "functional": {
    "tool": "functional",
    "source": "https://pmc.ncbi.nlm.nih.gov/articles/PMC6938631/",
    "status": "test_calculation_only",
    "blockers": [],
    "evidence_code": null,
    "classification": null,
    "band": "PS3_Strong",
    "odds_path": "18.7001"
  }
}

```

排除项：[]

阻断项：[]

组合命中/限制：{"framework": "ACMG_2015_Table5_on_reviewed_strengths", "candidate": "P", "matched_rules": ["P2"], "status": "test_only", "reasons": [], "note": "2015 combining structure on supplied strengths; no automatic strength restoration or later combination amendments"}

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

Evidence snapshot：offline-v0.2-demo
