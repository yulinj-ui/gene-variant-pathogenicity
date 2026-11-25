# 医学规则待复核登记

> **v0.8.0-local（2026-10-18）状态说明**：自本版起，作者 2026-10-09 发布包中的
> `references/ACMG_CRITERIA.md`、`references/FREQUENCY_EVIDENCE.md`、`references/CNV_CRITERIA.md`（存为 `CNV_CRITERIA_UPSTREAM.md`）
> 是**已发布、可执行**的标准，不再要求逐条重新登记为 pending；其条文与引用见文件本身及 `upstream-2026-10-09/PROVENANCE.md`。
> 本表以下条目针对的是 `original/`（2026-09-28 档案）中的旧文句，保留作追溯；已被上游新条文取代的条目在"处理"列注明。
> 规则优先级与同步流程见 `references/UPSTREAM_SYNC.md`。

第二版落实与限定核查状态见[变更对照](CHANGELOG_V2.md)及[来源登记](SOURCE_CHECKS.md)。以下保留初版问题和原文定位，不表示第二版没有修复工程部分。R12实际MCC段为原ACMG第749–758行，R13见原SKILL第1315–1318行。

**下表针对 `original/`（2026-09-28 档案）的旧文句，默认仍为 pending，不据此执行。** 现行执行标准是上游已发布条文（见上方说明）。下表是重点问题，不是全部已审定清单。逐行对照表覆盖其余条文。原文全文留在 original，下面按精确引用保存待核片段。行号是定位范围，不代表该范围外的同类规则已获认可。

审定需填写：规则ID、出处URL/DOI、版本/发布状态、页表位置、疾病及遗传模式、核实后的条件/数值、替代关系、审定人/日期、是否允许用于临床。不能仅把 pending 字符串改成 reviewed。

## R01 检索失败推断 PM2

- 状态：pending
- 原文：original/SKILL.md.txt:430–437
- 处理：明确缺陷：不赋值，记录人群证据未获取
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R02 公共库无记录称首次报道

- 状态：pending
- 原文：original/SKILL.md.txt:307–328
- 处理：改为本次检索未发现；保留检索范围
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R03 蛋白门控的推导/跳过/停止出口冲突

- 状态：pending
- 原文：original/SKILL.md.txt:71–119
- 处理：已修工程门控；原出口不启用
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R04 未收录与 GUS 混同、检测质量重写分类

- 状态：pending
- 原文：original/SKILL.md.txt:882–888
- 处理：待疾病关联及检测真实性分层复核
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R05 两证据规则与 PVS1 stand-alone、CNV 冲突

- 状态：pending
- 原文：original/ACMG_CRITERIA.md:33–39
- 处理：待框架和例外归属审定
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R06 推定串联与方向不明的 0.45/0 分支

- 状态：pending
- 原文：original/CNV_CRITERIA.md:90–105
- 处理：待规范定义及断点条件审定
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R07 外显率低于10%直接 VUS/B

- 状态：pending
- 原文：original/CNV_CRITERIA.md:234–234
- 处理：不启用自动降级；分级/风险/报告分开
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R08 11对照、实验体系上限与 PS3 校准

- 状态：pending
- 原文：original/ACMG_CRITERIA.md:316–360
- 处理：核实正式原文条件；不固化课件为通用标准
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R09 PM1 三门槛及缺核查降级例外

- 状态：pending
- 原文：original/ACMG_CRITERIA.md:382–448
- 处理：待原始标准/VCEP核实；缺证不加分
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R10 de novo分数区间空档、trio与亲缘、相位推断

- 状态：pending
- 原文：original/ACMG_CRITERIA.md:474–641
- 处理：待连续区间和证明标准核实；不默认 confirmed
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R11 PP1/PP4分摊与诊断率换算

- 状态：pending
- 原文：original/ACMG_CRITERIA.md:642–707
- 处理：待来源和适用疾病复核
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R12 MCC/VAF/LOD统一阈值

- 状态：pending
- 原文：original/ACMG_CRITERIA.md:772–779
- 处理：待检测方法及实验室 SOP 审定
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R13 亲代嵌合与再发风险估计

- 状态：pending
- 原文：original/SKILL.md.txt:1320–1330
- 处理：不由外周血0/N推生殖腺上限；核实际家系
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R14 预后矩阵把邻近病例转个体风险

- 状态：pending
- 原文：original/SKILL.md.txt:1237–1347
- 处理：保留矩阵，增加n/N、偏倚、未知；不自动分高低风险
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R15 产前报/不报与 VUS 亚档

- 状态：pending
- 原文：original/SKILL.md.txt:924–942
- 处理：待实验室政策；测试版保留所有记录
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R16 指南、课件、个人推论、草案混合

- 状态：pending
- 原文：original/ACMG_CRITERIA.md:1–925
- 处理：全部原医学条文 pending；逐项溯源才启用
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R17 CNV 1B、基因家族计数、4O及剂量自评

- 状态：pending
- 原文：original/CNV_CRITERIA.md:1–251
- 处理：全部原医学条文 pending；与正式 Loss/Gain 表逐项核实
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R18 报告例子与积分/禁叠规则不一致

- 状态：pending
- 原文：original/SKILL.md.txt:1088–1430
- 处理：模板去掉预填证据与风险；保留字段
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R19 框内插入的RNA类推与剪接规则

- 状态：pending
- 原文：original/ACMG_CRITERIA.md:187–227
- 处理：保留原推论但不正式启用；需原文和疾病适用性审定
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

## R20 上传规范优先与版本/权威性

- 状态：pending
- 原文：original/SKILL.md.txt:745–826
- 处理：上传后核来源、版本、状态，不能自动视作现行规范
- 精确原文见 rule-review.json 的 original_text；对应文件原文完整保留。

