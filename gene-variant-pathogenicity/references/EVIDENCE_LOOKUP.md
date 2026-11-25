# 证据项查表助手：PS1/PM5、PM4、PS4、BS2、PP1、BA1

`scripts/evidence_lookup.py` 提供 6 个 reviewed-input 查表助手。全部离线、仅依赖标准库，输出 `status=test_calculation_only`、`evidence_code=null`、`classification=null`，**不自动写入主评分**（与 `review_helpers.py` 的 pm3/pp1pp4/functional 同款护栏）。输入是调用者已完成医学审核的事实，程序只做结构校验 + 有出处的查表。

```bash
python3 scripts/evidence_lookup.py ps1pm5 input.json
python3 scripts/evidence_lookup.py pm4 input.json
python3 scripts/evidence_lookup.py ps4 input.json
python3 scripts/evidence_lookup.py bs2 input.json
python3 scripts/evidence_lookup.py pp1_lod input.json
python3 scripts/evidence_lookup.py ba1_threshold input.json
```

所有 review 字段必须为真正布尔 `true`，并附 `reviewer/reviewed_at/source/rationale` 非空文字；缺失即 `blocked`。数字阈值用精确十进制字符串，严格保留 `>`/`<`（恰等于阈值落入较弱档）。来源见各函数 `SOURCES` 字典。

## 1. PS1 / PM5（`ps1pm5`）

- 来源：ACMG/AMP 2015；ACGS 2024 v1.2 强度矩阵。
- 输入：`relationship`（`same_amino_acid`→PS1 / `same_residue_diff_aa`→PM5）、`reference_class`（`P`/`LP`）、PM5 另需 `grantham_not_less`（布尔）或 `pm5_strong`（布尔，可选）。
- review 门槛：`reference_independently_classified`（防循环论证）、`phenotype_matched`、`reference_no_splice_effect`、`vcep_checked`。

| 情形 | 输出 code | 强度 / 权重 |
|---|---|---|
| PS1 + 已知 P | PS1 | Strong / +4 |
| PS1 + 已知 LP | PS1_Moderate | Moderate / +2 |
| PM5 + 已知 P 且待评 Grantham ≥ 已知 | PM5 | Moderate / +2 |
| PM5 + 已知 LP 或待评 Grantham < 已知 | PM5_Supporting | Supporting / +1 |
| PM5_Strong（≥2 个不同致病错义，须 VCEP） | PM5_Strong | Strong / +4 |

- 注意：PM5_Strong 仅当 `reference_class=P` 时可用；PM5 缺失 `grantham_not_less` 且 `pm5_strong` 未置位时阻断。PS1/PM5 与 PM1、PP2、PM4、PVS1 的互斥由调用方执行。

## 2. PM4（`pm4`）

- 来源：ACMG/AMP 2015；ACGS 2024 v1.2。
- 输入：`variant_type`（`in_frame_indel` / `stop_loss` / `last_exon_truncation_gof`）；按类型另需 `in_repeat_region`、`single_aa_noncritical`、`nsd_present`、`gof_mechanism_established`（严格布尔）。
- review 门槛：`mechanism_matched`、`not_redundant_with_pvs1`、`not_redundant_with_ps1_pm5`、`vcep_checked`。

| 情形 | 输出 |
|---|---|
| 非重复区框内 indel | PM4（Moderate） |
| 非重复区框内 indel，单氨基酸且非关键残基 | PM4_Supporting |
| 重复区框内 indel | 阻断（指向 BP3） |
| 终止密码子丢失且无 NSD | PM4（Moderate） |
| 终止密码子丢失且有 NSD | 阻断（指向 PVS1） |
| GOF 基因末外显子截短且 GOF 已确立 | PM4（Moderate） |
| GOF 未确立 | 阻断 |

## 3. PS4（`ps4`）

两种模式，来源：ACMG/AMP 2015（OR>5）；Tavtigian 2020（LR→EP）；Oza 2018 PMID:30311386（先证者计数）。

### 3a. `mode="likelihood_ratio"`
- 输入：`lr`（正有限十进制）。
- review 门槛：`cohort_definitions_reviewed`、`population_matched`、`genotyping_reviewed`、`vcep_checked`。
- 输出 `band`（VeryStrong/Strong/Moderate/Supporting/Indeterminate）与 `direction`（pathogenic/benign）；LR→EP 分档：≥350.4 / 18.72 / 4.33 / 2.08（致病侧），<0.48 / <0.23 / <0.053 / <0.00285（良性侧）。代码选择（PS4 或 BS4）由调用方决定。

### 3b. `mode="proband_count"`
- 输入：`inheritance`（仅 `AD`/`XL`）、`pm2_met`（布尔）、`unrelated_probands`（整数）。
- review 门槛：`phenotype_consistent`、`case_independence_reviewed`、`deduplication_reviewed`、`vcep_checked`。
- 输出：≥15→Strong、6–14→Moderate、2–5→Supporting、<2→阻断。AR 病拒绝（走 PM3）。

## 4. BS2（`bs2`）

- 来源：ACGS 2024 v1.2。
- 输入：`inheritance`（`AD`/`AR`/`XL`）、`healthy_carrier_count`（整数，AD=健康杂合、AR=健康纯合、XL=健康半合子）。
- review 门槛：`disease_applicability`、`early_onset_full_penetrant`、`phenotype_assessed`、`vcep_checked`。
- 输出：≥2 → `bs2_met=true`，否则 `false`。外显不全、印记、限性/从性携带者不计。

## 5. PP1 共分离（`pp1_lod`）

- 来源：Jarvik & Browning 2016 PMID:27236918（本技能默认标尺）。
- 输入：`meiosis_count`（有效减数分裂次数，整数）。
- review 门槛：`phase_reviewed`、`penetrance_reviewed`、`counted_by_meiosis`、`vcep_checked`。
- 输出：3–4→PP1_Supporting、5–6→PP1_Moderate、≥7→PP1_Strong、<3→阻断。VCEP 另有规定时以 VCEP 为准。

## 6. BA1 阈值核对（`ba1_threshold`）

- 来源：Ghosh 2018 PMC6188666；ClinGen SVI 2018。
- 输入：`af`（等位基因频率，十进制）、`allele_count`（观测等位基因数，整数）、可选 `exception_matched_ids`（来自 `ba1_review.py` 的命中）。
- review 门槛：`population_verified`、`denominator_verified`、`quality_filter_verified`、`gene_disease_inheritance_reviewed`、`vcep_checked`、`exception_list_current`。
- 输出：`ba1_applies`（AF>0.05 且 allele_count≥2000 且不在豁免名单）。BA1 为 stand-alone 逻辑，不折算 -8 分。

## 与主评分的关系

这些助手只做「已审核事实 → 查表强度」。要进入主评分，走 `case_pipeline.py` 的 admission 流程（签署 / 底层证据去重 / 重算一致校验）：

- `admissions[].kind` 取 `ps1pm5` / `pm4` / `ps4` / `bs2` / `pp1_lod`；`input` 为本文件对应助手的原始输入，`selected_codes` 必须与重算结果一致（否则 `selected_codes_not_supported_by_recalculation` 阻断）。
- `pp1_lod`（产出 PP1 代码）与 `locus` 一样需要附 `assessment`（pedigree）工作底稿。
- `ps4` 的 LR 良性方向无标准 ACMG 代码 → 阻断（`PS4_benign_LR_has_no_standard_code`），应改用 BS1 频率或 BS4 共分离。
- `ba1_threshold` 不作为 admission（BA1 是 stand-alone，`score.py` 拒绝 BA1 代码），而是顶层 `ba1_threshold` 输入 → 输出 `ba1_threshold_check`，仅报告是否适用、不自动判 Benign。
- 每个 admitted 代码仍需 `scoring.rules` 中存在对应已审核规则（`rule_ids[code]`），并遵守 `score.py` 的互斥/封顶与 `DATA_CONTRACT.md`。
- `score.py` 已对新接入证据内置硬互斥：`PS1/PM5`、`PM4` 与 `PS1/PM5/PP2/PP3`、`PM1/PM5`、`PP2/PM5`、`PS4` 与 `PS2/PM6`、`BS2/BP2`；命中即 `mutually_exclusive:<pair>` 阻断候选。

禁止把这里的原始强度直接塞进主评分，也禁止原始小数与转换代码重复累计。
