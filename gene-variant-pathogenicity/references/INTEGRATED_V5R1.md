# 第五版修订：逐例规则选择与审核后评分

版本0.5.1-test。此文件优先于旧版“辅助结果完全不能接入”的描述。旧脚本仍为算术工具；真实病例使用 `case_pipeline.py` 和相应报告入口。未安装，正式classification仍为空。

## 1. 每例必须查询VCEP

VCEP（Variant Curation Expert Panel）按基因、疾病和遗传方式检索，不能只查基因名称。每个疾病指向分别建档。

1. 查询[ClinGen CSpec](https://cspec.genome.network/cspec/ui/svi/)及对应专家组页面；记录查询词、URL、日期、成功/失败和结果。失败或未完成不等于不存在。
2. 找到候选时，核对已发布状态、版本、基因、疾病实体、遗传方式、变异类别及限制；疾病别名或父子实体需保存映射理由，不能靠字符串相近判断适用。
3. 适用时获取并阅读全文规范、相关原始论文、附录、补充材料和勘误；按本次需要的条目逐条定位。网页本身若是正式完整规则也保存快照；不能只读摘要。记录版本与SHA256，并说明所需材料为何完整。
4. 证据强度、阈值、互斥条件和组合评级均按适用版本。专病规则未修改的部分依其引用的ACMG/SVI执行，不凭经验把通用规则拼入。每条rule绑定specification_url/version。
5. 没有适用版本时，记录none_found；有版本但疾病、遗传方式等不适用时记录not_applicable及逐候选排除原因，然后使用ACMG2015和适用SVI补充文件。积分优先、2015组合并列，不取较高结论。
6. 已知有适用规范但全文或关键附录未获取，先完成独立证据整理，阻断依赖该材料的候选评级，不把缺材料当作回退理由。

**实现范围：**程序校验检索记录、范围、文档声明和版本绑定，不自行联网，也不能认证阅读是否真实。DeepSeek Harness负责当次检索和证据解读。任意基因VCEP组合尚无通用执行器；采用带证据ID、命中规则位置及签署的人工组合结论，与通用积分和2015对照分别展示。不得称“所有VCEP已自动编码”。

## 2. 辅助结果接入

运行 `python3 scripts/case_pipeline.py case.json`。输入示例见tests/fixtures/pipeline-pvs1-v5r1.json、pipeline-functional-v5r1.json、pipeline-locus-v5r1.json，均为合成工程用例，不能当真实审核记录。

顶层包含identity、routing、scoring、admissions，可选assessments、ba1_identity、vcep_combination_review。identity包含variant_id/gene/disease/inheritance，家系模块另含subject_id。

- 每个admission提供id、kind、同一identity、原始input、底层basis_ids、source_ids、selected_codes、rule_ids、approval。可用kind为pvs1/pm3/functional/locus。
- approval包含approved=true、reviewer/reviewed_at/source/location/rationale；它代表已完成具体病例审核，不能由运行程序自动生成。
- 原始辅助input必须重新计算，helper返回blocked、unmapped或Indeterminate不能接入。代码必须与重算支持的选项一致，并对应已审核scoring.rules。
- 底层证据在主证据与各admission间检查重复。Table4双代码选项作为同一个受上限约束的联合分配，保存共同原始basis，不将它们当成两份独立原始证据。
- 通用helper在VCEP路径下还需vcep_adoption_review，确认所用公式和强度与该规范一致。不同阈值不能靠签署改写计算结果，须另作逐条人工证据审核。
- 不允许把已算好的helper结果直接塞进scoring，也不把原始小数与转换代码同时累计。
- 存在阻断时authoritative_candidate为空。score_comparison保留算术审计轨迹，不可绕过阻断作为本例候选。

报告输入用case_pipeline代替scoring和review_calculations；variant_id须一致。十模块结构保持。正式分类和签发仍需实验室工作流完成。

## 3. PVS1与RNA：现有能力的衔接

2018通用35路径维持，通过完整适用性核验后可以审核接入主评分。机制资料使用review/lof-dossier，未知不是否；档案中公开证据的使用是可追溯工作流程安排，不伪称2018论文原句。

RNA及非经典剪接采用2023专项审核记录，字段见assets/assessment-templates-v5r1.json。记录组织/转录本、实验设计、对照、等位来源、NMD抑制、转录本定量、LoF后果、救援转录本、强度和预测证据重叠。**本版不从RNA百分比或预测软件直接决定强度。**

RNA实验证实剪接LoF时，按适用指南审阅PVS1_Strength；无剪接影响的内含子/同义变异审阅BP7路径，不能自动转换为BS3。用既有代码及mechanism=rna_splicing记录RNA来源，人工选择的强度须有原文与病例依据。同一剪接效应不再叠加预测证据；蛋白功能与RNA机制分离须另有依据。2023主文涉及的PS1、部分剪接和复杂转录本路径保留专项人工审核，不声称已实现全自动RNA引擎。

来源：[Walker 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10357475/)，重点Summary及RNA证据段。适用VCEP优先；未定义的10%边界和低于Supporting仍阻断。

## 4. PP1／BS4／PP4：推荐采用两阶段实现

**本版已纳入：**已核实的有限概率分配/联合小计重算后按Table4选代码，审核接入。2.5分对应2–2.9档；6.5联合分先按适用上限封顶，再转换。原始小数仍在轨迹中，主评分只加选定代码的权重。不能把2.5任意四舍五入或额外叠加。

**完整家系的推荐：**先建立逐人的家系表、表型和年龄、基因型/相位、遗传模式、外显率、拟表型、招募方式和独立减数分裂；再由明确的方法计算家系似然或允许的小计。不要按“患病人数”代替有效共分离次数。复杂家系须专家审核模型与参数，保留计算文件和可复算结果。

**BS4：**患病非携带者应核对表型一致性、样本/亲缘关系、位点检出能力、拟表型和其他致病原因；健康携带者要考虑发病年龄、外显率和遗传方式，不能直接认定非共分离。本版接收有完整pedigree审核记录的手工BS4证据，不从一个病例自动赋BS4。PP1与BS4并列输入先阻断，要求统一模型处理相反家系信息。

**不等权分配：**Table S1已取得，但既有审计的行号/公式及概率比与优势比差异未被正式澄清。本版不选一种解释作为正式算法。可记录专家审定的外部分配结果，经reviewed_joint_cap审阅后转换；程序不声称独立重建了该统计模型。

**直接小数主评分：**暂不启用。若以后启用，需要单独定义概率/优势到积分转换、截断或取整、联合封顶、良性负分、2015对照和外部标准答案。当前采用论文Table4已明确给出的代码转换路径，避免混用不同积分体系。

来源：[Biesecker 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10806742/)，Tables2–4、Supplement Table S1；原文XML已在references/sources。

## 5. PS3／BS3：程序检查资料，专业审核实验

新增functional审核记录要求逐项写finding/source/location/conclusion：机制、实验类别、细胞或样本系统、对照、重复、校准、待判变异读数、正常结果覆盖范围、冲突处理。每项是证据记录，不能只勾选true。

- 对照须有不依赖相同功能标准的分类依据；不能把VUS当已知P/B校准对照。
- 同时记录技术/生物重复、实验动态范围、对照构成和读数阈值；11个对照不自动获得任何强度。
- 有充分校准时使用该实验版本的OddsPath；无校准时按原文/VCEP的适用路径人工确定，不反推或编造OddsPath。
- 结果normal/abnormal必须与所选BS3/PS3方向一致；中间效应、机制不符或未解决冲突阻断自动接入。针对低功能/部分功能需专项人工审阅。
- 多个一致实验不自动叠加升档。存在冲突时记录为何较充分验证且更贴近机制的实验可优先；无法区分时不使用相冲突功能证据。程序只检查该决策记录，不能取代专业判断。
- 仅测RNA剪接的实验分流到RNA规则；“正常蛋白实验”不能排除未测的剪接机制。

来源：[Brnich 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC6938631/)，四步框架、Step3/4及Table3。原始XML保存。此前MSH2精确校准值和MSH6合并模型的未复现问题仍保留，不使用混合公式修补。

## 6. BA1：先自动匹配例外，不自动宣布良性

`ba1_review.py`实现官方2018清单9项匹配：CA ID、ClinVar Variation ID、精确带版本HGVS或GRCh37规范化坐标。每个匹配字段有明确类型；多个标识冲突、不同build或只有蛋白名称时返回identity_unresolved。版本不会被自动删除；相同基因或相同蛋白变化不足以证明同一等位基因。

命中清单即提示不能按通用BA1直接裁决。未命中仅为not_in_snapshot，不能证明BA1适用。本次官方指导页仍链接July2018清单，但历史清单不等于全部现行例外。每例另查最新清单及基因/疾病特异修改。

后续BA1判定必须核实具体祖源人群、分母、质量过滤、频率和疾病/遗传方式：通用2018定义为一般大陆人群数据中AF>0.05且观察等位基因至少2000，并无基因或变异特异修改；不能把创始人群结果、总样本数或低质量记录直接代入。专病阈值须遵循适用VCEP。BA1是stand-alone逻辑，不自行折算为-8分。**本次仅启用例外匹配；BA1正式自动裁决继续禁用。**

来源：[官方指导目录](https://www.clinicalgenome.org/tools/clingen-variant-classification-guidance/)、[清单PDF](https://www.clinicalgenome.org/docs/ba1-exception-list/)、[Ghosh 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6188666/)。清单原PDF及人工逐行转录JSON随包保存。

## 7. CNV究竟缺什么

现有CNV引擎能核算人工已审核的Loss/Gain条目；区间脚本能核对坐标和重叠。它尚不能完整地从坐标与数据库证据自动选择医学评分条款，也未对全部条目的分值、互斥和上限完成独立验收。因此不能仅凭分值已加总就认为条目选择正确。

例子（假设情形）：

|输入证据|仍需判定的问题|
|---|---|
|缺失与一个HI敏感基因相交|是否完整包含，还是只涉及部分外显子/非编码区？应走哪个Loss条目？|
|重复完整覆盖一个HI基因|HI说明少一份的效应，不能由此推出多一份致病；需另查TS和重复结构。|
|某CNV在数据库中多次出现|是否同一断点范围、同类事件、相同祖源及独立样本？有没有可用频率分母？|
|发现基因内部缺失|需要转录本/阅读框/PVS1辅助分析，但不把SNV的8分加入CNV总分。|

4O属于人群证据条款，不能仅因“数据库里找得到”就赋良性分，更不能用未经核实的频率阈值自动分档。完整覆盖、部分覆盖、基因数量、病例/人群证据和遗传情况分别审核后，才能核算CNV总分。

来源：[Riggs 2020原始标准](https://pmc.ncbi.nlm.nih.gov/articles/PMC7313390/)，Loss/Gain评分表及VUS讨论。本次解释并保留独立CNV流程，未宣称实现全部CNV自动条目选择。
