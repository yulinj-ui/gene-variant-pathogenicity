# 证据项查表助手与 CNV 2H 双档案（0.6.1-lookup）

## 依据

2026-09 培训班 15 份课件逐项比对后，经用户确认启用 P0/P1 证据项查表与 D3 CNV 2H v4 指标。与既有无差别：全部为 reviewed-input 查表，不自动赋码、不自动写主评分、classification=null。

## 修复

- **PM3 反式 LP 计分**：`review_helpers.py` 反式分支按 P=1.0/LP=0.5/VUS=0.25 分档（原误将 LP 计 1.0）。`references/RULES_V2.md` 补全 PM3 点表并注明档案 original 表的合并写法错误。新增 `tests/test_v3.py::test_pm3_trans_LP_is_half_point`。

## 新增：证据项查表助手（scripts/evidence_lookup.py）

| 助手 | 覆盖证据项 | 要点 |
|---|---|---|
| `ps1pm5` | PS1 / PM5 | 同氨基酸改变化 vs 同残基不同氨基酸；P/LP 与 Grantham 分档；PM5_Strong 仅 VCEP |
| `pm4` | PM4 | 框内 indel / 终止密码子丢失 / GOF 末外显子截短；重复区→BP3、NSD→PVS1 分流 |
| `ps4` | PS4 | LR→EP→强度查表 + 先证者计数（AD/XL） |
| `bs2` | BS2 | 健康携带者计数（AD/AR/XL，≥2） |
| `pp1_lod` | PP1 | Jarvik 共分离标尺（3–4/5–6/≥7） |
| `ba1_threshold` | BA1 | AF>5% 且 ≥2000 等位基因 + 豁免名单 |

输入契约见 `references/EVIDENCE_LOOKUP.md`；测试见 `tests/test_v7.py`。

## 修改：CNV 2H 双预测器档案（D3）

`cnv_section2.py` 的 `predictor_profile` 现支持两套档案，均须绑定来源版本：
- `Riggs2020_original`：pLI≥0.9、o/e CI 上限<0.35（gnomAD v2）、DECIPHER HI index≤10%。
- `ClinGen_current_v4`：pLI≥0.9、LOEUF<0.6（gnomAD v4.1）、pHaplo≥0.86（DECIPHER）。

`references/CNV_CRITERIA.md` 同步更新；`metric_equivalence_review` 仍为必填，防止字段名相似即默认等价。

## 新增：接入 case_pipeline admission 流程

`case_pipeline.py` 现支持 `ps1pm5`、`pm4`、`ps4`、`bs2`、`pp1_lod` 五种 admission kind（走既有签署/去重/重算门控）；`pp1_lod` 需附 pedigree 工作底稿，`ps4` 良性 LR 方向阻断（无标准代码）。`ba1_threshold` 作为顶层检查（`ba1_threshold` → `ba1_threshold_check`），仅报告、不自动判 Benign。集成测试见 `tests/test_v7.py::CasePipelineAdmissionTests`。

## 新增：score.py 硬互斥守卫 + 逐 kind 真实形态 fixture

`score.py` 新增新接入证据的硬互斥对（ACMG/AMP + ACGS/CanVIG「禁止」组合）：`PS1/PM5`、`PM4` 与 `PS1/PM5/PP2/PP3`、`PM1/PM5`、`PP2/PM5`、`PS4` 与 `PS2/PM6`、`BS2/BP2`。命中即在候选输出阻断（`mutually_exclusive:<pair>`）。涉及既有代码、2015 表5结构仍合法组合的（如 PVS1+PM1、PS1+PM1 等）不硬编码，留给 `combination_policy`。

新增 5 份真实形态 pipeline fixture（含完整 rule/approval/assessment）：`tests/fixtures/pipeline-{ps1pm5,pm4,ps4,bs2,pp1-lod}-v7.json`；`tests/test_v7.py` 增 `ScoreMutexTests`、`PipelineFixtureTests`。

## 边界不变

完整家系统计、不等权分配、直接小数主评分、BA1 自动裁决、PM1 自动赋值、2023 RNA 引擎均仍禁用。全量测试 435 项通过（工程验收，非临床验证）。
