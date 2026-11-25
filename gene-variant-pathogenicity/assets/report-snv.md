# 遗传变异独立辅助复核报告

正文使用中文临床表达；完整数据、评分输入输出和执行核验另存技术附录。遵循 references/REPORT_PRESENTATION.md。

## 模块 1：结论速览

- 本次独立辅助评级：使用assisted_case核实结果；未完成时说明关键原因，不把实验室签发状态与独立辅助评级混同。
- Report status：测试 / 初步 / 待外部注释 / 待 VCEP 复核
- Primary framework：Tavtigian 2020积分优先（测试候选）
- ACMG 2015 comparison：表5结构按已审核强度对照，正常列出结果/命中条款/不可用原因
- Framework disagreement：两者差异与版本理由；不自动取高等级
- ACMG Score：仅列经复核证据的核算值；无有效证据写 N/A
- Evidence：逐条代码与强度；无则未赋值
- Gene–disease validity：单独列出状态及依据，不由数据库未收录自动设上限
- Sample detection confidence：本样本检出可信度，单独列出
- Confidence：基于证据完整性说明，不等于致病概率
- Disease entity / Inheritance / Zygosity：分疾病实体描述
- Caveats：身份、检测质量、证据或规则缺口
- Reporting：主表 / 附表 / 待实验室确认，并说明原因

## 模块 2：病例与变异概况

Gene / Original input / Transcript / Clinical transcript rationale / HGVSc / HGVSp / Variant Type / Genome Build / VCF / Exon-Intron。

gnomAD AF Global / EAS / AC-AN / hom-hemi / FAF / Coverage / Filters / Dataset version。

REVEL / SpliceAI / CADD / AlphaMissense / pLI-LOEUF：写来源、版本、适用性；未知不填0。

ClinVar ID / Classification / Review status / Last evaluated。

Nearest variant / Distance / Domain landscape / Literature gap：注明检索范围和来源。

产前追加 MCC status / VAF proband-parents / Depth / Mappability / Validation method / LOD / HPO present-absent-not assessable。

## 模块 3：ACMG 证据链（中文）

适用标准、版本、疾病与遗传模式；未获 VCEP 全文时注明。

| 证据ID | 代码/强度 | 规则状态及出处 | 原始证据/来源ID | 底层观察ID | 采纳/排除及理由 | 分值 |
|---|---|---|---|---|---|---|

证据独立性与重复计数审查；冲突和未通过门控；积分汇总与敏感性分析。使用已实现的表5结构对照时列出实际命中条款；BA1、未支持强度和疾病适用性尚未完成时明确说明，不编造已完成临床核查。

## 模块 4：ClinVar 综合查询结论

聚合分类、疾病、提交者/SCV、星级、日期、一致性与冲突；共享来源去重；本分析与数据库的差异。

## 模块 5：与外院及外部分类的对照

GeneBe / Franklin / VarSome / InterVar：分类、证据代码、URL、获取时间、状态。仅作为对标；未获得写未获得。自动分类不能替代本例证据。

## 模块 6：关键判断与取舍

先写支持依据，再写相反/限制依据，最后说明本次取舍。突出真正改变等级的分歧；有必要时列固定其他证据的条件性敏感性表，不把假设写成已采纳或可保证的升级路径。分子机制、频率、功能/家系和临床归因分别解释。

## 模块 7：关联遗传病画像（中文）

疾病/MIM、遗传模式、基因关联有效性及机制；发病年龄、外显率、产前表型、基因型-表型数据，注明来源。

## 模块 8：临床可操作性建议（中文）

按现在可做、条件触发、可能改变什么列临床建议；附可直接转述的门诊沟通要点。后续证据获取、家系、第二打击和随访只列有本例依据的项目，不默认要求用户逐项答复。产前用 prenatal.md 替代本模块。

## 模块 9：核心文献及其用途

每条列作者、年份、标题、期刊、PMID/DOI/URL；中文核心结论；元数据核验状态与主张核验状态、页/表位置。

反查执行日期 / 引文数 / 已验证数 / 部分验证数 / 更正或删除数 / 实际覆盖率（无引用为N/A）。不预填100%。

## 模块 10：局限性声明

1. 本报告包含 AI 生成的内容，所有结论需经认证临床遗传学家/遗传咨询师审核确认后方可用于临床决策。
2. 数据库检索日期与版本、未获取/冲突/不适用项、原规范未复核项逐条列出。
3. 本包为迁移测试版，离线测试不证明临床有效性；本分析不构成医疗诊断或治疗建议。
4. 检测范围、覆盖度、盲区与未排除的变异类别仅按实际检测资料填写。

Re-evaluation triggers：新知识、表型、家系、功能数据、指南版本变化。
Evidence snapshot：本例原始响应、来源、时间、规则记录和报告版本。

批量附表：Gene / Variant / Report status / Classification / Key evidence / AF / REVEL / Report placement；同基因多变异另述定相和联合解释。VUS 内部亚档仅在审定政策允许时写入附表。
