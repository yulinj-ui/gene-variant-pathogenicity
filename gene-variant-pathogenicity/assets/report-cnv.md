# CNV 致病性分析（迁移测试版）

## 模块 1：Classification Hero

CLASSIFICATION：未完成正式评级 / 待规则复核。
Report status / CNV framework（Loss 或 Gain）/ CNV score / Evidence / Confidence / Disease entity / Inheritance / Copy number / Caveats / Reporting。

此处使用 CNV 独立总分，不显示 SNV Bayesian 分值；没有有效证据写N/A，不自动判VUS。

## 模块 2：Molecular Profile

Original input / Genome Build / Coordinate system / Chromosome / Start-End / Size / Loss-Gain / Copy number / Breakpoint uncertainty / Orientation / Mosaic fraction / Detection method / Validation / LOD。

涉及基因与转录本版本、编码基因计数依据、受累外显子、HI/TS 基因或区域及评分日期；与每个区域的交集、双向覆盖比例；复发区域亚型；已知良性/人群区间；基因内断点、串联证据、阅读框与 LOF 机制。

蛋白、REVEL 等不适用字段写 N/A 及理由；不强制 CNV 经过 HGVSp 门控。产前加 MCC、VAF/拷贝信号、样本来源与质量。

## 模块 3：CNV 五段式证据链（中文）

标准版本、Loss/Gain 表、条目适用性、外部计算器核对状态。

| Section | 条目 | 规则版本/状态 | 证据及底层病例ID | 推荐值/允许范围 | 本例分值 | 纳入或排除理由 |
|---|---|---|---|---|---|---|

依次记录 Section 1 内容、2 剂量/良性区域与基因内结构、3 编码基因数、4 文献/人群、5 本家系。按条目限额和证据独立性审查；Section 4/5 不重复计本家系。断点不明时给条件性分值范围，不自动挑高分。

## 模块 4：临床数据库综合查询

ClinVar / ClinGen Dosage / DECIPHER：区间、build、病例表型、遗传背景、去重、版本、日期、冲突。没有权限只说明未获取。

## 模块 5：External Benchmarking

ClinGen CNV Calculator、其他实际取得的分类与条目对标；URL、版本、访问状态、差异。不得声称未执行的在线核对已完成。

## 模块 6：AI 判读决策报告（中文）

剂量效应、完整/部分重叠、基因内后果、断点敏感性、病例证据、继承方式、外显率与替代病因。区分 CNV 分类、AR 致病等位基因/携带状态和本例诊断归因。

## 模块 7：关联遗传病画像（中文）

区域/基因、疾病、遗传模式、外显率与表达度、复发区域精确亚型及预后资料。

## 模块 8：临床可操作性建议（中文）

父母/家系验证、断点/方向确认、正交检测、对侧 SNV/Indel/CNV 搜索、印记/UPD、随访。产前替换为 prenatal.md。

## 模块 9：References

PMID/DOI/URL、元数据、中文核心结论、元数据及主张核验状态、页表位置。列实际验证数和覆盖率；无引用写N/A。

## 模块 10：局限性声明

1. 本报告包含 AI 生成的内容，所有结论需经认证临床遗传学家/遗传咨询师审核确认后方可用于临床决策。
2. 本包为迁移测试版；规则审定、数据库版本、未获取项目、断点不确定性和检测盲区必须披露。
3. 本分析不构成医疗诊断或治疗建议。分类、个体预后及报告政策分别说明。

Re-evaluation triggers / Evidence snapshot / Reporting recommendation。
批量：区间、类型、状态、分类、关键条目、总分、Report placement；SNV+CNV 联合结果独立说明相位和疾病归因。

分类、基因—疾病关联、样本检出可信度三栏分列；官方HI/TS与内部剂量评估分列。基因家族自动合并关闭；1B不作为提前终止并判良性的规则；4O频率自动映射关闭。
