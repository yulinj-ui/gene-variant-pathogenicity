# 遗传变异致病性分析（v0.5.2-test 离线草稿）

## 模块 1：Classification Hero

- 正式分类：未完成；本输出不可直接用于临床签发。
- 变异：未提供/未评估
- 优先核查框架：Riggs_2020
- 测试候选分区：P
- 积分：1.00
- 2015组合对照：不适用（CNV独立框架）
- 对照状态：not_applicable
- 框架差异：未提供/未评估
- 基因—疾病关联：未提供/未评估
- 本样本检出可信度：未提供/未评估
- 报告位置：仅建议；待本机构政策审核。

## 模块 2：Molecular Profile

未提供/未评估

样本质控：{"status": "not_evaluated", "automatic_acceptance": false, "mcc": null, "vaf": null, "depth": null, "mosaicism": null, "validated_lod": null, "gonadal_risk_upper_bound": null, "reason": "local assay validation and SOP absent; values retained for manual review"}

## 模块 3：CNV五段式证据链

| 证据ID | 代码 | 分值 | 原因 |
|---|---|---|---|
| cnv-section2 | 2A | 1.00 | synthetic test only |

按适用规则审核的候选：P

通用积分对照（不得覆盖专病结论或流程阻断）：P

逐例规则检索、辅助重算及审核接入轨迹：

```json

{
  "routing": {
    "framework": "CNV_LOSS",
    "integration_review": {
      "approved": true,
      "reviewer": "synthetic reviewer",
      "reviewed_at": "2026-09-27",
      "source": "synthetic test NOT medical evidence",
      "location": "fixture",
      "rationale": "synthetic test only",
      "all_targets_and_transcripts_reviewed": true,
      "uncertain_breakpoints_reviewed": true,
      "other_sections_reviewed": true,
      "section4_skip_rule_reviewed": true,
      "independence_and_caps_reviewed": true,
      "dosage_date_reviewed": true,
      "clinical_context_reviewed": true
    }
  },
  "admission_audit": [
    {
      "status": "reviewed_section2_candidate",
      "blockers": [],
      "code": "2A",
      "default_points": "1.00",
      "allowed_range": [
        "1.00",
        "1.00"
      ],
      "assigned_points": "1.00",
      "classification": null,
      "automatic_score_import": false,
      "pvs1_audit": null
    }
  ],
  "ba1_exception_check": null,
  "blockers": []
}

```

排除项：[]

阻断项：[]

组合命中/限制：{"candidate": null, "status": "not_applicable", "reasons": []}

## 模块 4：临床数据库综合查询

未提供/未评估

## 模块 5：External Benchmarking

未提供/未评估

## 模块 6：判读决策报告

CNV使用独立总分；本工具不自动识别或赋予Loss/Gain条目。

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
