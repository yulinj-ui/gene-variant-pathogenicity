# 输入、证据与降级契约

## 注释适配器

`genebe_fields.py HGVS --fixture file.json` 不联网。fixture 顶层键为 variantvalidator、genebe、worker，值为原始 JSON 或 null。fixture 是测试输入，不表示数据已从真实服务取得。

- VV：唯一一条 `hgvs_transcript_variant` 必须精确等于输入；含 `primary_assembly_loci.grch38.vcf`，可选 grch37；`hgvs_predicted_protein_consequence.tlr/slr`；警告阻断该源。
- GeneBe：顶层单变异或 variants 单元素列表；chr/pos/ref/alt 与 VV 一致；genome 明确 hg38/GRCh38；consequences 中必须有唯一精确 transcript/feature（含版本）。实际接口不提供这些字段时需更新适配器并离线测试，不能放宽到默认相信第一条。
- Worker：必须回显 input、build、coord 与 VV 一致；gnomad 可含 global_af/ac/an 和 eas_af/ac/an；merged_predictors 列表为 id/value/source；constraint、codon_landscape 可为空。未附 Worker 服务实现，不能保证其真实输出符合契约。
- 原始频率与字段版本仍需人工核实；不会从空值推断 PM2，不会自动赋任何医学代码。PM2_Supporting不以AN、FAF等所有字段齐全为必要条件；可靠的成功查询缺失及适当的位点/区域检出能力依据可经逐例审阅支持采纳，详见[SOURCE_ACCESS](SOURCE_ACCESS.md)。`passed` 只代表两个已校验来源的标准化蛋白字符串一致，不证明注释本身正确或两个证据独立。
- p.? 为 unresolved；一源有明确后果为 single_source；后果冲突为 conflict；一字母/三字母未做转换时保守视为冲突，需人工核实。CNV/非编码是否 not_applicable 由实际分析记录，不由本脚本猜测。

联网模式仅在显式 `--online` 时使用。Worker 没有默认值，需 `--worker https://trusted-host`；不会读取或转发 NCBI_KEY。GeneBe 凭据可由 GENEBE_KEY 环境变量提供，不写入包、输出或命令行。请求 URL 含变异，应作为病例记录保护。联网请求每次超时 15 秒、最多 2 次；无 curl 回退。服务结构尚未实时验证。

## 评分输入

示例见 `tests/fixtures/score-reviewed.json`（合成数据，只用于测试）。

顶层：framework=SNV/CNV_LOSS/CNV_GAIN；rules 为规则字典；evidence 为证据列表；combination_policy 为本次经复核的合并策略。

规则必须包含 code（与证据代码一致）、status=reviewed、framework、source、version、location、reviewer、reviewed_at、applicability、allowed_points。证据必须包含 id、rule_id、code、framework、status=reviewed、gate=passed、points、source_ids、basis_ids、rationale。basis_ids 代表同一底层患者/实验/频率观察，可跨网站重复；source_ids 是获取位置。不同证据允许共享文献，但不能复用同一底层观察。

合并策略字段：status、framework、source、version、reviewer、reviewed_at；mutually_exclusive 为代码对；caps 为 `{codes:[...], max_abs_points:...}`。不提供审定合并策略则不显示测试候选分区。原文规则待复核，不会自动加载。

分类始终为 null。即便所有结构校验通过也仅显示 sandbox_partition；已实现2015表5组合结构的测试对照；未实现BA1例外、疾病适用性及完整临床冲突裁决。不得将此输出改写成正式诊断或正式分级。

## CNV 几何输入

`cnv_interval.py file.json` 顶层 query/region，各含 build、chr、start、end、system。system 为 one_based_closed 或 zero_based_half_open。不同 build 报错；不做 liftover；返回交集长度、双向覆盖比例和全覆盖布尔值。没有自动剂量注释或评分。

## 病例审计记录

每例另存原输入、规范化输入、数据源原始响应、检索时间、数据库版本、规则复核表、证据记录、报告。未提供字段写 null 并标原因。预测面板无值不推断方向；ClinVar 无记录不称首次报道；功能未执行、结果阴性、未知三个状态分开。

引文分别记录 metadata_verified 与 claim_verified、PMID/DOI、文章元数据、页/表位置、支持的证据 ID、获取时间。没有 PMID 的真实文献可用 DOI/正式 URL 核验，不伪造 PMID。

## v0.2新增字段与使用

- 注释protein_gate：`usable_for_consequence_review`允许VV身份校验后的single_source或verified；`passed`继续只表示双源一致，兼容旧调用者；`identity_status`与`crosscheck_status`分开。
- 评分：`primary_framework`、`point_candidate`、`acmg_2015_comparison`、`framework_disagreement`、`difference_note`。正式`classification`仍为null。空证据或阻断时不输出候选分区。
- 同一SNV代码家族不能重复输入；例如PP3和PP3_Strong冲突。代码与分值必须一致。PS2/PM6须先汇总，不双列；PM1与PP3同时使用合计超过4分则阻断，不擅自降档。PVS1/PP3须填写mechanism，不明或相同机制阻断。
- BA1例外流程未实现，BA1不进入自动核算；PP5/BP6转载分类不支持。2015表无对应的良性Moderate/VeryStrong不强行映射，保留积分并显示对照不可用。小数SNV分值仍禁用。
- score接受显式自定义TEST代码用于纯算术测试；此类代码的2015对照不可用，不用于真实病例。`reviewed`元数据不能证明临床正确。
- `evidence_helpers.de_novo_strength(case_points, heterogeneity_points)`中两参数是互不包含的小计。输出是遗传模式修正前强度；AR、X连锁、嵌合例外与病例去重仍需复核，输出不含正式证据代码。
- `evidence_helpers.revel_band`只返回Pejaver 2022表2区间。必须显式传入missense、identity_validated、calibration_selected三个布尔true。没有gene-specific评估或独立性核验，不自动使用该代码。
- `report_audit.sample_qc`无论输入怎样都不启用本地自动质控，不估算LOD、生殖腺风险或嵌合诊断。
- `render_report.py`输入含scoring（原评分契约）、可选variant、gene_disease_validity、sample_detection_confidence、molecular_profile、sample、database_findings、external_benchmarks、disease_profile、follow_up、snapshot_id、citations。citation每条含唯一id、citation、metadata_verified与claim_verified；核验率分母为引用条数，分子为两类核验均为true的条数。无引用为null/N/A。合成示例见tests/fixtures/case-v2.json。

离线草稿生成器填充十模块的核心数据；产前详细矩阵、病例论证、外部查询和临床审核按模板继续完成，不能声称生成草稿即完成全部判读。

CNV代码只接受形如1B/2I/2D-1的条款格式及单条绝对值≤1的点值，排除SNV代码与未转换分值；这只是形状/范围校验，不验证该条款确实存在、Loss/Gain适用性、方向或条目限额。实际条目仍需调用者逐条审核。通用保护不支持自动覆盖为VCEP例外，遇到专用例外转人工对照并注明。


## 第三版增量

当前增量以 [RULES_V3](RULES_V3.md) 和 [HELPERS_V3](HELPERS_V3.md) 为准；第二版规则不被整体替换。辅助小计、候选代码选项不自动写入主评分。新增PVS1/PM4全强度互斥、非Tavtigian points_profile拒绝；BA1、本地参数和未核实完整算法保持禁用。
