# 第二版逐条变更对照
v0.1.0-test → v0.2.0-test。用户最终选择积分优先、2015组合正常列出。原包4文件保持字节不变，原2154行对照表继续保留；本表补充本轮修订，未把原条文整体标为reviewed。
| 项目 | 本轮落实 | 状态 | 实现/验证 | 仍待补充 |
|---|---|---|---|---|
| R01 | 失败不赋PM2；缺失频率null；本地库停用 | source_checked_workflow | 注释/缺失测试；WORKFLOW | 数据版本、覆盖、过滤及疾病频率阈值逐例核查 |
| R02 | 检索结论限定日期和范围；不称首次报道 | engineering_enabled | report_audit.search_statement | 无 |
| R03 | 单源允许复核、身份与双源一致分开 | engineering_enabled | genebe_fields；单源/冲突测试 | 线上VV/GeneBe契约待实时核验；VEP/Mutalyzer未新增连接器 |
| R04 | 分类/关联/样本可信度三栏 | workflow_enabled_limits_pending | 两类报告模板及生成器 | Limited上限等自动裁决继续禁用 |
| R05 | 积分优先+2015组合对照，CNV独立 | source_checked_test_only | score/compare_frameworks；各组合与边界测试 | BA1例外、疾病规则、小数积分未实现 |
| R06 | 未知插入位点不默认0；保留完整前提 | source_checked_manual_only | RULES_V2；CNV模板 | 具体断点、长度、转录本、NMD/LoF逐例审核 |
| R07 | 删除低外显率自动降级 | workflow_enabled | CNV报告：分类/预后分开 | 易感CNV主报告仅建议，机构政策待补 |
| R08 | 删除物种上限和只凭对照数自动赋值 | source_checked_manual_only | RULES_V2 | 实验清单、性能、VCEP与适用性 |
| R09 | PM1和/或路径；PM1+PP3上限保护 | source_checked_test_only | score上限阻断测试 | 热点/功能域和反证仍须人工证据 |
| R10 | de novo连续门槛和高异质性上限；更正PM3简表 | source_checked_test_only | evidence_helpers与测试；PM3仅文档 | 亲缘SOP及遗传模式例外，PM3不自动赋值 |
| R11 | 删除线性乘分；暂不实现小数/取整方案 | disabled_pending | score拒绝小数测试 | 完整2024框架、去重、上限验证 |
| R12 | 本地阈值关闭，只留值与提示 | disabled_local_policy | report_audit.sample_qc测试 | 本地方法验证与SOP；文献不能代替本地验证 |
| R13 | 咨询模块保留，自动再发数值关闭 | disabled_local_policy | 产前模板、sample_qc | 具体家系、组织、方法、审核责任 |
| R14 | 资料三态+n/N/年龄/来源；不推个体风险 | workflow_enabled | 产前模板 | 适用队列和个体模型缺失时未评估 |
| R15 | VUS内部亚档；报告仅建议；2026来源确认 | workflow_enabled_policy_pending | 两类报告模板 | 机构SOP、知情同意、MDT流程 |
| R16 | 规则来源分层与限定核查状态 | engineering_enabled | source-checks.json、RULES_V2 | 逐疾病VCEP与本地中文共识版本 |
| R17 | 保留1B；关闭家族合并/4O固定映射/内部HI冒充官方 | source_checked_manual_only | CNV −0.60边界测试；模板 | CNV补充材料、病例级条目适用性；自动−1仍关闭 |
| R18 | 同一数据源生成证据/分数，实际核验率，REVEL互斥区间 | source_checked_test_only | render_report/report_audit/evidence_helpers；边界/报告测试 | 极低REVEL强度上限及VCEP逐例声明 |
| R19 | 删除框内插入永久禁令，保留机制复核 | source_checked_manual_only | RULES_V2 | RNA原始实验、组织、比例和蛋白数据 |
| R20 | 上传资料登记；固定版本，不自动增信 | engineering_enabled | USER_REVIEW归档、SOURCE_CHECKS | 完整规范附件与版本更新流程 |

## 新确认的审阅差异
- PM3相位未知对侧LP为0.25病例分，不是审阅简表中的0.5；不自动录入简表。
- 2020 PM2建议已允许PVS1+Supporting到LP；原2015表5对照与后续修订需区分。
- REVEL表2包含极低分更强区间；本轮只显示研究分档，不擅自扩展2015良性组合。
- 附录亲缘/深度阈值和4O自动−1仍不启用。
- 老版本验收与独立评审记录保留为v0.1-*文件，仅代表第一版。

临床启用状态：本轮20项均未取得临床签发授权；工程、流程和测试计算状态分别列示，不等同于临床启用。
