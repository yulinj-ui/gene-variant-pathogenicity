# 第五版：PVS1 全树可执行审核

## 能力与边界

`scripts/pvs1_review.py` 根据有出处的审核事实选择 2018 通用树路径，再应用 Table 1 机制门槛、正文全局排除和强度降级。35 条路径均有执行测试。它不从变异名称自动完成序列注释、NMD预测或文献评价；这些生物学事实必须有输入依据。

来源：[Abou Tayoun 2018 原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC6185798/)、[ClinGen 可编辑模板](https://www.clinicalgenome.org/docs/clingen-svi-pvs1-decision-tree-editable/)。原始节点清单见 [pvs1-inventory.json](pvs1-inventory.json)；其中 is_executable:false 是梳理时的历史记录，保留不改。当前路径测试覆盖见 [第五版路径验收](../review/PVS1_PATH_ACCEPTANCE.md)。

当前输出为临床审核辅助：`evidence_code/classification` 均为空，`automatic_score_import=false`。`adjusted_strength` 是通用树的测试强度，不是正式证据代码、诊断或基因专病规则审批。

## 输入结构

必需顶层字段：`kind/identity/review/mechanism/scenarios/basis_ids/facts_review/vcep_policy/source_version`。剪接另需 `splice_review`；依赖 exon 长度/相位的 PVS1 另须 `exon_check`（`scripts/exon_check.py` 的输出卡片，`status=PASS`）。未知字段拒绝，不能直接提供 path_id 或想要的强度。

- kind：`nonsense_frameshift/canonical_splice/deletion/duplication/initiation`。
- identity：`variant_id/build/genomic_change/transcript/gene/disease/inheritance`，均非空，transcript 必须带 `.版本号`。身份格式完整不等于已核对序列；审核人必须核实。
- source_version 固定 `AbouTayoun_2018_generic`。
- vcep_policy 仅接受 `reviewed_generic_applicable`，表示已检查本例可用通用规则；若需专病替代节点，当前阻断，不能自动选通用较强结果。
- basis_ids 为本例底层证据身份的非空、不重复列表。
- review：`identity_reviewed/disease_mechanism_reviewed/transcript_reviewed/exon_population_reviewed/vcep_reviewed/technical_quality_reviewed` 必须为布尔 true，且 `reviewer/reviewed_at/source/rationale` 非空。这些是调用者审阅声明，不是认证机制。
- facts_review 分组 `nmd_or_frame/exon_relevance/population_tolerance/critical_region_or_start/mechanism`，每组须有 `source/location/rationale`。不适用的分组仍写明为何不适用，不能空缺后声称已审核。

生物学事实的未知与明确为否不同。`region=assessed_unknown` 特指已查阅证据后关键性仍未知，不能拿来代替未查询。

## exon 两源核对（v0.8.2，强制）

任何依赖 exon 长度、exon skipping、in-frame/out-of-frame 或 NMD 的 PVS1，先运行：

```bash
python3 scripts/exon_check.py NM_000214.3 2
```

工具同时读取 NCBI GenBank 的 `exon` features（1-based 闭区间）与 Ensembl `Exon`（1-based 闭区间），输出 `exon_check` 卡片：

- `ncbi`: start/end、length、c_start/c_end、phase、mod3、aa_start/aa_end、frame；
- `ensembl`: transcript、start/end、length、canonical、mapping；
- `cross_check`: `passed`、`exon_count_match`、`all_exon_lengths_match`、`target_length_match`、messages。

规则：**exon 数或任一 exon 长度不一致 → `status=MISMATCH`，不得继续 PVS1**。JAG1 `NM_000214.3` exon 2 为 **551..856 = c.82..387 = 306 nt**，306 mod 3 = 0 → exon 2 skipping 为 in-frame；报告若写 307 nt，通常是把 UCSC BED/genePred 的 0-based 半开 `10672700..10673006` 当成了 1-based 闭区间，多算了 1 个碱基（c.388，intron 2 首碱基），会把 in-frame 误判为移码/NMD。

## Table 1机制判定

mechanism 字段：

|字段|输入|
|---|---|
|lof_mechanism|established／absent；unknown或缺失阻断|
|association|limited／moderate／strong／definitive|
|lof_evidence|可选列表；每条 `{variant, classification, criteria, pvs1_dependent, clinvar_id?}`。提供时脚本自动计算 `independent_pathogenic_lof_count` 与 `associated_lof_count` 并核对手工值，不一致直接拒绝|
|independent_pathogenic_lof_count|不依赖PVS1已判P的LoF变异数，非负整数；有 `lof_evidence` 时以脚本计算值为准|
|phenotype_lof_count / phenotype_total_count|相关表型LoF数与总变异数；分母必须正数，直接算精确比例|
|associated_lof_count|既往与表型关联的LoF数（有 `lof_evidence` 时须等于列表行数）|
|multiple_exons / single_exon_gene|严格布尔；单外显子基因免除跨多个外显子条件|
|null_mouse|布尔，或对象 `{model, pmid, phenotype, heterozygous_phenotype, recapitulates}`；`recapitulates` 为 `yes` 才按 true 处理，`no/partial` 按 false|

**G1 必须同时满足两条**：≥3 个不依赖 PVS1 的 P LoF **且** >10% 表型相关变异为 LoF（跨 >1 外显子）。SVI 2018 Table 1 原文为 AND；只满足 >10% 不得给原级。G1满足则不再叠加G2/G3降级。G2降一级、G3降两级。无LoF机制为not_applicable；资料不足或缺少适合分支为blocked。正好10%的Table 1图文差异保留blocked。降级低于Supporting也为blocked，不发明更弱代码。

## 逐类事实

scenarios 为 `{id, facts}` 对象数组。非剪接仅接受一个已审核转录本/后果；多个冲突转录本需先审查，不自动选最高强度。

所有局部变异 facts 均需：`exon_present`（相关转录本中存在）、`lof_common`（依据已审人群政策，该外显子高频LoF耐受）。全基因缺失不使用局部外显子检查。

|类型|其它字段|
|---|---|
|无义/移码|nmd：true/false；非NMD时 region；必要时 removed_aa/protein_length|
|剪接/缺失|consequence：out_of_frame_nmd / out_of_frame_no_nmd / in_frame；whole_gene 仅允许缺失。需要时 region及蛋白长度|
|重复|tandem：confirmed/presumed/non_tandem；effect：disrupts_frame_and_nmd / no_effect / assessed_unknown；length_known/whole_gene/external_insertion：严格布尔|
|起始丢失|alternative_start：是否另一功能转录本使用替代起始；upstream_pathogenic：最近下游潜在框内起始之前是否存在已知致病变异|

region 接受 critical、assessed_unknown、proven_noncritical；最后一种在原树无独立定义，返回blocked。critical必须由实验或临床证据支持，不能仅凭结构域名称。

removed_aa/protein_length 使用整数和精确分数比较。恰好10%不走任一强度；长度未知不猜测。去除长度应按已审核后果计算，程序不自动根据移码位置推算新蛋白。

NMD事实必须依据新提前终止的位置、相关转录本结构、通用预测原则及基因特例审阅。该模块没有自动坐标到NMD引擎，不能声称已经验证任何具体基因的50 nt边界。

## 剪接多情形

splice_review 必须明确：

- `canonical_gt_ag_plusminus_1_2=true`：仅GT–AG经典±1/±2。
- `cryptic_sites_within_20nt_reviewed=true`：已审核附近恢复/隐蔽位点。
- `scenarios_complete=true`：合理候选后果已完整列出。
- `later_splicing_guidance_reviewed=true`：已对照后续剪接规范适用性。
- `rna_data_present=false`：有RNA实验时分流到尚未实现的专项整合，不能以本版2018树代替2023 RNA规则。

各情形独立走树；取最低可用强度。一个情形明确不适用则联合不适用；一个情形资料不足则整体blocked，不忽略弱或未知结果。相关后续来源：[Walker 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10357475/)。本版仅设置分流和审核门控，没有宣称实现该篇全文。

## 输出与全局限制

- path_results：情形ID、源路径ID、完整节点链、源树输出、原始树强度、全局排除理由。
- mechanism_tier：G0/G1/G2/G3。
- tree_strength：经过全局排除和多情形最低强度处理后的、机制降级前的汇总值；各情形原始值另存。
- adjusted_strength：机制降级后结果，仅在 test_calculation_only 状态下有效。
- lof_evidence_audit：`{provided, computed_independent, computed_associated, manual_independent, manual_associated, consistent}`；提供 `lof_evidence` 时由脚本自动统计并与手工计数核对，不一致直接报错。
- counts_audited：`true` 表示独立计数由 `lof_evidence` 核对；**PVS1_VeryStrong 要求为 true**（`score.py` 的 provenance 门控会拒绝未核对的手工 Very Strong）。
- not_applicable 不等于良性；blocked 不等于不适用；原始路径结果只是审计轨迹，不能绕过blocked使用。

已实施：正文全局外显子LoF耐受/相关转录本排除；重复长度未知阻断、全基因重复或基因外插入排除；不自动执行全基因缺失脚注的最终P分类。

## 报告与主评分

报告 `review_calculations.pvs1` 接收原始输入并重算。需报告 `variant_id` 与模块identity一致；底层basis与主证据重叠报错。当前测试版不允许该辅助报告同时列入PVS1/PM4/PP3主评分证据；这是保守防重复隔离，不是所有PP3与PVS1永久互斥的医学断言。

CNV继续走独立整体解释；缺失/重复PVS1可单独作审核计算，但不能作为CNV分数导入。`score.py`拒绝pvs1_results/pvs1_review注入，积分优先及2015对照保留原有行为；但 `score(..., pvs1_review=..., enforce_pvs1_provenance=True)` 会把该审核结果用于**来源核对**（仅校验强度与机制档是否匹配，不把其分值导入积分）。

## 仍不能自动解决

基因—疾病LoF机制的证据真实性、表达相关转录本、外显子耐受阈值、关键区域实验/临床依据、串联位置、替代起始以及最新VCEP替代规则都需要逐例资料。模块不编造这些输入。下一阶段可选择特定基因及公开病例做外部验证；目前35路径验收为合成工程用例，不是临床有效性验证。
