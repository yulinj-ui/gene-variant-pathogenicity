# 第四版：PP1／PP4 有限计算输入与执行范围

本页是本版新增功能的当前说明；第三版文件保留作历史记录。来源：[Biesecker 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10806742/)，Table 2、Table 4、Figure 2。Table S1 不等权算法仍未启用。

## 使用范围

`scripts/locus_review.py input.json` 接收仅含 `packets` 非空数组的对象。它只生成审计计算，不生成临床证据、最终分类或主评分输入。

### 模式一：pp4_equal

限已经审核符合 Figure 2 的 AR、位点同质、无额外共分离合并、同一等位基因 1 或 2 个等权候选场景。这里的“无额外共分离合并”指工具不处理额外 PP1 输入；不能把 PP1 值塞入诊断率字段。

- `diagnostic_yield` 是精确十进制**字符串比例**，例如 `"0.958"`，不是 `95.8`，不接收浮点数。
- `inheritance: "AR"`；`locus_model: "homogeneous"`；`allocation: "equal"`；`segregation_present: false`。
- 先用精确有理数分配概率，再向下查印刷 Table 2，最后逐变异封顶 5 分。
- 印刷表范围为 0.191–0.999。分配后的概率在范围外时返回 unmapped；不外推、不给零分或良性证据。输入原始概率须在 0–1。
- 例如 0.958、两个候选：每个 0.479，Table 2 各为 2.5 分；一个候选时 Table 2 为 7，封顶后为 5。
- 不从本模式自动产生 PP1，不选择证据代码，也不把 Table 2 的小数值当成 Tavtigian 2020 代码权重。

### 模式二：reviewed_joint_cap

接收**外部已人工审核、已完成概率分配**的单变异 PP1/PP4 联合小计 `joint_points`，只实施封顶和 Table 4 代码组合上限查表。

- 小计必须为非负精确十进制字符串，已经不多于一位有效小数；2.59 拒绝，2.50 与 2.5 等值，无自动舍入。
- 一个 packet 只能有一个变异。多候选仍需上游独立复核，不能用此入口绕过未启用的不等权分配。
- 工具不计算家系人数、不计算 PP1、不赋 BS4；传入这些额外字段会报错。
- 小计大于 5 时降至 5，再返回 Table 4 的最大允许组合选项。原始小计保留，`selected_codes` 为空。
- Table 4 选项是上限，不证明某条 PP1/PP4 对本例成立；主积分不会加入选项或原始小计。

## 两模式共有字段

每个 packet 必须提供：`packet_id`、`subject_id`、`allele_id`、`variant_ids`、`basis_ids`、`mode`、`source`、`review`。

- ID 必须是非空字符串，列表内部不得重复。
- 同一批次 packet_id、变异 ID、basis ID 重复即拒绝；同一等位基因两个候选应放在一个 packet。暂不跨家系合并，也不对纯合变异的两个拷贝各计一份。
- `basis_ids` 表示底层观察/证据身份，不是论文 URL。不同网站转载同一观察不能换 ID 当成独立证据。工具只能检查调用方提供的身份，无法识别故意或错误换号。
- `source.kind` 必须为 `published`；未经核实的本地参数继续禁用。还需 `url/version/location/gene/disease` 非空字符串；pp4_equal 另需 `phenotype_definition/testing_method`。
- `review` 共需布尔 true：`applicability_reviewed/phase_reviewed/penetrance_reviewed/vcep_checked/basis_independence_reviewed`。
- pp4_equal 另需：`phenotype_matched/testing_method_matched/yield_source_verified/equal_plausibility_reviewed/single_locus_model_reviewed`。
- reviewed_joint_cap 另需：`joint_points_reviewed/allocation_already_completed/joint_independence_reviewed/cap_applicable`。
- review 中 `reviewer/reviewed_at/source/rationale` 必须为非空字符串。字段为调用方审核声明，不是身份认证，也不自动证明来源真实。

任何缺审核或缺来源的 packet 不输出计算结果。批次内有一个 blocked/unmapped，批次状态为 blocked；其它 packet 的可计算结果仍保留供审查，不能把批次宣称为全部通过。

## 报告与防重复

`render_report.py` 的 `review_calculations.locus_review` 接收原始输入并重新计算，保留十模块。报告须有 `subject_id`、`variant_id`，且与 packet 一致。计算过程单列，主积分与 2015 对照继续只来自独立审核的既有证据。

- 新模块与旧 `pp1pp4` helper 不可在同一报告并用。
- packet 底层 basis 与任何主评分证据重叠即报错。
- 报告带有本模块时，主评分不得另含 PP1/PP4/BS4，即便改换 basis ID 也拒绝。此为本测试版的保守隔离措施，不是医学上永久互斥规则。
- CNV 报告不得附加 SNV 辅助模块。
- `score.py` 拒绝 `locus_packets/locus_results/fractional_points/review_calculations` 直接注入，原有 helper_results 及小数 SNV 拒绝逻辑保留。

## 主评分接入验收条件

本轮已实现报告整合和拒绝误导入，**尚未实现小数体系主评分导入**。接入前需要：

1. 固定小数框架配置与证据来源、Table 2/4 的转换含义；不可把小数小计和转换代码权重两次相加。
2. 定义同一底层证据在病例、家系、位点和变异层面的身份与归属。
3. 对2015对照明确采用的代码选项和适用性；不能仅因分值够高就自动选择 PP1 或 PP4。
4. 完成相应路径病例验收；争议分支必须显式停用，不能产生“缺失即零”的候选分类。

不等权分配、复杂家系、BS4 自动赋值与当前未核实参数，不是等待某个外部服务恢复即可启用的功能；需要进一步规则和统计验证。
