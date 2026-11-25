# 第三版规则状态表

版本 0.3.0-test；2026-09-27。source_checked_test_only 仅表示限定测试计算，不表示病例适用性或临床分类获批。既有 R01–R20 审阅记录不覆盖删除；本表列第三版实际执行状态。

| ID | 功能 | 状态 | 范围 | 实现/来源定位 |
|---|---|---|---|---|
| V3-01 | Tavtigian 2020积分优先；2015组合并列 | source_checked_test_only | 维持整数阈值；不改为ACGS | score.py；Tavtigian 2020 Tables 2–3 |
| V3-02 | PVS1与PM4互斥 | implemented_guard | 所有强度、两种输入顺序均阻断候选 | score.py；Abou Tayoun 2018 PVS1 Strength Levels |
| V3-03 | PVS1完整决策树 | disabled_pending_validation | 门槛与限制补充说明；全树自动赋值禁用 | references/RULES_V3.md；Abou Tayoun 2018 Table 1/Figure 1 |
| V3-04 | PM3病例小计 | source_checked_test_only | 病例和家系标识、前提审核、P/LP区别、分类上限；不自动赋证据 | review_helpers.py pm3；SVI PM3 v1.0 Tables 1–2 |
| V3-05 | PS3/BS3 OddsPath查表 | source_checked_test_only | 先审核校准与机制；不由物种或数量自动赋强度 | review_helpers.py functional；Brnich 2020 Table 3 |
| V3-06 | PS3/BS3实验充分性自动判断 | disabled_pending_validation | 11对照不能单独放行；历史验证例外转人工 | references/RULES_V3.md；Brnich Step 3 |
| V3-07 | PP1/PP4 Table 4查表 | source_checked_test_only | 仅接收已审核分配及封顶的小计；不自动选代码或导入 | review_helpers.py pp1pp4；Biesecker 2024 Table 4 |
| V3-08 | PP1/BS4/PP4完整家系算法 | disabled_pending_validation | 概率分配、舍入、补充表及复杂家系统计仍禁用 | references/RULES_V3.md；Biesecker 2024 Tables 2–4/Table S1 |
| V3-09 | 基因—疾病关联自动上限 | disabled_pending_policy | 保留Moderate例外；查不到不等于Limited | references/RULES_V3.md；Bean 2020 Clinical validity; Clause 2023 |
| V3-10 | BA1自动裁决及例外匹配 | disabled_pending_validation | 历史清单有来源，未完成现行覆盖与标识匹配 | score.py；Ghosh 2018; ClinGen July 2018 list |
| V3-11 | ACGS及本地积分配置 | disabled_pending_policy | 显式非Tavtigian points_profile报错，不静默混用 | score.py；ACGS 2024 pp8/15 |
| V3-12 | 本地样本质控和风险参数 | disabled_local_parameters | MCC/VAF/LOD/亲缘阈值和个体风险不自动应用 | report_audit.py；需实验室验证 |
| V3-13 | CNV自动条目选择/4O频率映射 | disabled_pending_validation | 保留独立人工审核分值核算，不自动赋项 | score.py; cnv_interval.py；Riggs 2020 |
| V3-14 | 外部服务 | degraded_offline | 默认离线；缺失不补零、不生成阴性证据 | genebe_fields.py；DATA_CONTRACT.md |
| V3-15 | 报告及原始功能 | preserved | 十模块/产前矩阵/逐条对照/原始文件保留；辅助结果单列 | render_report.py; original；FEATURE_MAP.md |
| V3-16 | 正式分类、签发及安装 | disabled | classification=null；无安装或服务配置修改 | all；用户授权范围 |

未实施的自动功能不会因输入写入 reviewed 而被实现；但人工证据评分接口仍依赖提供者诚实、正确地完成医学审核，程序不能验证审阅人的资质或医学结论。
