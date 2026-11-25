# 第三版辅助计算输入

全部脚本仅依赖Python标准库，默认离线。三个完整合成JSON示例位于tests/fixtures/helper-pm3-v3.json、helper-pp1pp4-v3.json、helper-functional-v3.json；所有review字段必须为真正布尔值true，并附reviewer、reviewed_at、source、rationale非空文字。它们是调用者的审阅声明，程序不能验证其真实性。

```bash
python3 scripts/review_helpers.py pm3 tests/fixtures/helper-pm3-v3.json
python3 scripts/review_helpers.py pp1pp4 tests/fixtures/helper-pp1pp4-v3.json
python3 scripts/review_helpers.py functional tests/fixtures/helper-functional-v3.json
python3 scripts/render_report.py tests/fixtures/case-v3.json --output /tmp/variant-v3.md
```

## PM3

顶层review包含recessive_disease、disease_applicability、frequency_threshold_validated、case_independence_reviewed、vcep_checked。cases每项含唯一id及family_id、phase（trans/unknown/homozygous）、partner_class（非纯合时P/LP/VUS）、partner_variant_id、source_ids。逐例review含affected、target_rare、partner_rare、independent_partner_classification、phase_or_homozygosity_reviewed。纯合例的partner_rare表示同一变异的稀有性复核，independent_partner_classification表示无循环论证审核，不要求目标变异预先判P/LP。

任一前提缺失，整体不显示候选小计/强度，仅返回逐例审核及阻断原因；输入错误或重复id/family_id抛出错误。小计权重与bayesian_weight分开。该计算器不生成主评分可用的证据记录。

## PP1/PP4

joint_points为已完成概率分配和封顶的0–5小计。review需applicability_reviewed、phase_reviewed、penetrance_reviewed、independence_reviewed、probability_allocation_reviewed、cap_reviewed。输出maximum_code_options只是原表最大组合选项；selected_codes为空，automatic_score_import=false。缺审核则无选项。额外精度不自动舍入，超5不自动封顶。

本版主评分尚未实现联合证据对象；不要把这些选项作为两条新独立观察输入，也不要同时加原始小数。需人工确定完整兼容策略后另行实现。

## 功能实验

odds_path须为正有限值；review需mechanism_matched、assay_validated、controls_independently_classified、replicates_reviewed、calibration_reviewed、vcep_checked。缺OddsPath不能用对照数量或物种代替。输出band是校准区间，非正式证据代码。

## 报告及评分边界

render_report接受review_calculations对象，其键限pm3、pp1pp4、functional，值为相应原始辅助输入；重新计算后单列。CNV报告拒绝SNV辅助计算，未知键报错。主score拒绝helper_results自动导入字段；即使辅助结果无阻断，也必须通过正常证据审核流程，不能自动升级分类。三个辅助输出均为evidence_code=null、classification=null。
