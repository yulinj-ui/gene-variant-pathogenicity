# 外院报告自主复核规范

## 目标与优先级

默认一次完成外院报告中变异的独立辅助评级、基因—表型复核和中文十模块报告。用户通常无法取得外部实验室原始数据，也不承担逐条医学规则审核；DeepSeek Harness应完成公开证据可支持的判断。本文覆盖旧版要求用户逐项签署的流程规定，不改变医学指南、证据强度或已禁用的未经核实规则。

“一次完成”指一次工作流中完成必要的多源查询、判断及交付，不限制只访问一次数据库，不保证在任何资料条件下都能产生确定等级。

## 自主工作的顺序

1. 识别变异身份和疾病范围。主动用可靠工具映射带版本HGVS、坐标和转录本；外院未写build但可唯一映射时列双版本，注明映射与原检测一致性未验证，不因此停工。命名有无法消除的歧义时才请求必要信息。
2. 每例查询适用VCEP并阅读当前规范；没有适用版本才回退ACMG2015及适用SVI。服务失败不等于无VCEP。无法获取已知适用规则时可继续证据草稿，但不声称完成该规范下评级。
3. 同时检索致病和良性证据、疾病机制、近邻/功能区、表型及技术局限。独立判断规则适用性，记录来源、版本和理由；不用用户逐项批准已能判断的医学事实。
4. 每个考虑过的条款采用include、exclude、unavailable或not_applicable。仅include进入主评分；其余记录不进入算术输入，避免把一个未满足条款变成整个计算失败。排除不等于计良性分。
5. 运行assisted_case.py；积分优先、2015正常列出；VCEP适用时按专病组合优先。两套结果不一致时解释实际条款差异，不选较高等级。CNV保留独立评分及五段核对。
6. 输出主评级及证据链、外院对照、基因—表型相关性、关键不确定性和必要的条件性分析。即使部分证据不可取得，也应给出目前可支持的结论，而非只交空白清单。

## 外院信息的使用

|信息|处理方式|
|---|---|
|明确报告某变异、转录本、杂合及父母均未检出|按外院陈述录入，标记external_report_explicit；可以支持相应事实的推理，但不声称已看原始读段或验证亲缘|
|仅病史称“新发”|标记user_history；亲代检测和亲缘分别记未知。按指南判断是否足以支持PS2/PM6及强度，不能自动当作已确认双亲关系|
|外院写LP/P等标签|仅用于差异对照，不能作为独立条款，也不反推PVS1等代码|
|未提供DP/VAF/MCC/验证方法|样本真实性/技术局限栏明确记录；一般不妨碍评估“该等位基因若存在”的致病性。若有实际证据提示假阳性或身份冲突，才进入关键问题|
|未提供父母或家系资料|不使用依赖这些资料的强证据，不默认健康或阴性；其他独立证据继续评分|
|没有RNA/功能实验|不是所有剪接/错义病例必须停工的理由。根据已有指南、机制和预测选择可支持强度；若疾病机制确有争议，应排除/降级相应条款并解释，而非臆测实验结果|
|数据库无记录/服务失败|成功查询未检出且检出能力可靠时，可审核采用PM2_Supporting；不要求AN、FAF等全部字段齐全。查询失败/AF空值不自动记AF=0。判断依据见[SOURCE_ACCESS](SOURCE_ACCESS.md)|

外院资料所支持的分类是针对明确陈述的等位基因及疾病范围，样本真实性单列。不能为获得一个等级而补造合子状态、亲缘关系、PVS1分母或功能结论。

## 什么会阻断整例，什么不会

- 仅仅没有用户签字、未取得BAM、外院不能答复、单项证据不满足：不作为整例阻断。
- 身份无法唯一确定、已知适用VCEP关键规则未获取、评分输入自相矛盾、重复计数未消除或未有任何可支持计分证据：保留未完成/证据不足，不自动用0分生成VUS。
- PVS1机制存在争议：自主评估现有文献能否解决；不能解决时该条款不计或按明确规范降级，其他有效证据可继续核算。如果其他证据组合支持VUS，明确给VUS并解释，不把“不能确认LP”与“已充分支持VUS”混为一谈。
- 每项缺资料均说明“是否可能改变等级”，不要将所有技术字段机械列成用户必答项。
- 对确实会跨级的假设，分别运行真实有来源的条件情景，清楚标为“仅若X得到证实时”。主评分不混入该情景。没有足够依据设置强度时，不编造LP/P情景。

## CNV

原12项核对保留为DeepSeek Harness工作底稿，默认不要求用户填表。review_mode=autonomous_assist、manual_review.reviewer_role=deepseek_harness_assistant，署名DeepSeek Harness (autonomous evidence review)；先把模式写入完整输入，再按cnv_manual_review.digest计算审核绑定。缺资料的事实可在有指南依据的未知/不适用分支处理；未查询或未完成判断仍不能伪装为完成。

当前单Section2综合贡献及未实现的多目标自动整合限制仍在；无法准确表达的条款不通过堆分绕过。重要冲突应先作有出处的取舍并记录，而非要求用户代为解决。原strict模式继续要求human_professional。

## 输入与署名

assisted_case顶层：framework（SNV/CNV）、case（既有病例入口结构）、assessment。

assessment包含performed_by=DeepSeek Harness、review_type=autonomous_assist、与case一致的identity。variant_identity、disease_mechanism、phenotype_fit、rule_search、pathogenic_evidence_search、benign_evidence_search、independence、external_report_comparison、limitations各记录finding/source/rationale。

critical_issues是确实影响可判定性的未解决问题列表；不能将所有未知机械放入。decisions逐条记录id/code/disposition/finding/source/rationale/origin；include另需applicability。origin分public_primary、external_report_explicit、user_history、unverified_assumption、external_classification。最后两种不能纳入主分。include的id须与case.scoring.evidence及admissions的id一致；CNV加cnv-section2。

case内审核声明的reviewer使用DeepSeek Harness (autonomous evidence review)，source/location/rationale如实填写。approved表示DeepSeek Harness已做本项证据审阅，不是用户已签字。不得伪造专业人员姓名或实验室认证。

## 报告

每例使用[统一临床报告模板](../assets/report-clinical.md)，按[临床分层输出规范](REPORT_PRESENTATION.md)固定十模块、结论卡、证据取舍和五点门诊沟通。默认交付Markdown正文及技术附录；不默认转换PDF、Word或HTML。

保留十模块结构；首页直接列本次独立辅助评级、积分、2015对照、外院原评级和差异原因。重要缺口集中列3–5项，非关键技术细节放局限性或附件。默认不附逐条待签的人工表；用户要求时再提供。

产前另列三段：变异本身评级、与当前胎儿表型的关联、未来预后及再发风险的可知边界。未知不能写正常；病例比例不当作胎儿风险；不作指令性妊娠决定。独立辅助分级不等于实验室签发。

输出independent_classification是本次辅助评级；clinical_signoff始终为空。用户可直接使用报告开展专业咨询，无需先完成表格往返。
