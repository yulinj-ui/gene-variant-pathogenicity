# v0.8.1-local 变更与验收（2026-11-19）

## 触发案例

FRYL `NM_015030.2:c.8547_8560del`（p.Tyr2849Ter）产前复核：网页端报告把 `PVS1_VeryStrong` 判为
"机制门槛 G1"，最终积分 9 → LP。复核发现：

- Pan 2024（PMID 38479391）表 1 的 9 个预测 LoF **全部按 `PVS1+PS2+PM2` 判 LP**，去掉 PVS1 后
  PS2+PM2=5 分（VUS），**不依赖 PVS1 的致病 LoF 计数为 0**；
- 按 SVI 2018 Table 1，原级要求"≥3 个不依赖 PVS1 的 P LoF **AND** >10% LoF"，本例只满足后者；
- 技能 `ACMG_CRITERIA.md` §1.2 第 3 条把 **AND 写成了"或"**，且 `SKILL.md` 未要求运行
  `pvs1_review.py`，`score.py` 对 PVS1 强度无来源核对，网页端把 `pvs1_review.py` 标为"可选"。

按正确机制档计算：G3 → `PVS1_Moderate`（+2）+ PM2_Supporting（+1）= 3 分 → **VUS**。

## 变更清单

| 文件 | 变更 |
|---|---|
| `references/ACMG_CRITERIA.md` | §1.2 第 3 条"或"→"**且**"，附 SVI 2018 Table 1 英文原文与 FRYL 反例；§1.2 有效性表行同步；新增 §1.2.1"PVS1 机制档强制输入"（`lof_evidence` / `null_mouse` 对象 / 输出字段） |
| `references/PVS1_V5.md` | 输入契约新增 `lof_evidence`、结构化 `null_mouse`；明确 G1 为 AND；输出新增 `lof_evidence_audit` / `counts_audited`；说明 score 的 provenance 核对不导入分值 |
| `scripts/pvs1_review.py` | 新增 `audit_lof_evidence`：逐条校验 LoF 清单并**自动计算** `independent_pathogenic_lof_count` 与 `associated_lof_count`，与手工值不符直接拒绝；`null_mouse` 支持对象并校验 `recapitulates`；输出 `counts_audited` / `lof_evidence_audit` / `mechanism_counts` |
| `scripts/report_audit.py` | 新增 `pvs1_provenance`（缺 review / review blocked / 强度不符 / VeryStrong 非 G1 / 计数未核对 → blockers）与 `framework_reaudit`（两框架不一致且最强证据为 PVS1/PS2/PS3 时要求复核） |
| `scripts/score.py` | `score(data, pvs1_review=None, enforce_pvs1_provenance=False)`；PVS1 provenance 门控（不导入 review 分值）；输出 `pvs1_gate`、`reaudit_required`；limitations 增补 |
| `scripts/case_pipeline.py` | PVS1 admission 的结果强制传入 `score(..., enforce_pvs1_provenance=True)`；多个 PVS1 admission 直接阻断 |
| `SKILL.md` | 版本 0.8.1-local；Step 4-PVS1 强制门控；§11.1 新增 0″ PVS1 门控；§12 由"可选管线"改为"pvs1_review.py 必跑"并加一致性守卫说明；§15 模块 3 固定字段 |
| `tests/fixtures/case-v5.json` | 机制块补 `lof_evidence`（3 条独立 P/LP）以满足新契约 |
| `tests/test_v9_pvs1_gate.py` | 新增 16 项回归：FRYL G3/Moderate、计数不符拒绝、手工 VeryStrong 未核对拦截、强度不符拦截、Moderate→VUS、G1 核对后放行、`reaudit_required`、case_pipeline 未核对拦截/已核对放行 |

## 验收

| 项 | 结果 |
|---|---|
| `python3 scripts/run_offline_tests.py` | **461 项全部通过**（原 445 + 新增 16） |
| `python3 scripts/validate_package.py` | PASS（version 0.8.1-local） |
| FRYL 案例（`lof_evidence` 9 条均为 PVS1 依赖，`null_mouse` recapitulates=no） | 机制档 **G3**，调整后 **Moderate**，`counts_audited=true` |
| 同案例 + PVS1_VeryStrong 声明 | `pvs1_very_strong_requires_G1` + `pvs1_strength_mismatch` 拦截 |
| 同案例 PVS1_Moderate + PM2_Supporting | 3 分，VUS（2015 表5 亦 VUS） |
| 手工计数 3、无 `lof_evidence` | `counts_audited=false`，VeryStrong 被拦截 |
| 网页端适配（variant-clinic） | 无 `pvs1` 摘要 → `pvs1_mechanism_review_missing`；证据 VeryStrong 而 review 为 Moderate → 拦截并显示门控提示；Moderate → VUS |

## 兼容与迁移

- `score(data)` 默认不启用 provenance 强制（保持既有离线测试与旧调用可用）；网页端与
  `case_pipeline.py` 显式 `enforce_pvs1_provenance=True`。
- 旧格式 `null_mouse: true/false` 仍接受；对象格式推荐用于新报告。
- 未提供 `lof_evidence` 时手工计数仍可计算，但 `counts_audited=false`，**不允许** `PVS1_VeryStrong`
  （适用于需要原级的真实报告；纯合成测试可用旧 fixture 计算路径强度）。
- 网页端要求 agent 在 `summary.json` 增加 `pvs1` 对象；未提供时 PVS1 报告会显示"门控未通过、不显示 LP/P"。

## 未解决 / 后续

- GenCC 冲突检查仍靠报告写作规范（本版只在 SKILL.md 要求按最低共识档并在模块 6 写明），未做自动抓取。
- `null_mouse` 的"是否重现人类表型"仍需人工判断；脚本只保证字段与 `recapitulates` 一致。
- 2026-11-19 复核的 FRYL 网页报告尚未按新规则改写（旧任务数据保留，需重跑或手工修订）。
