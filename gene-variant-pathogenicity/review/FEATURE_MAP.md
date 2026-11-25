# 逐条功能与原文对照

本表覆盖四份原文件的每个非空行，精确原文见同目录 feature-map.json；原文件按 source-manifest.json 哈希校验。逐行保留率不是功能实现率。源脚本另存为 .txt，防止误运行；源 SKILL 改扩展名防止重复发现。

## 功能实现状态

| 功能 | 本版落点 | 状态 |
|---|---|---|
| 输入分流、多格式、模式选择 | WORKFLOW / SKILL | 工作流已适配；HGVS 以外需外部规范化 |
| 三源取数与字段合并 | scripts/genebe_fields.py | 离线测试；实时接口未验证，Worker 未附 |
| 坐标/转录本/蛋白门控 | scripts/genebe_fields.py | 已实现并测试；临床注释需外部核实 |
| ClinVar 前置/多路径、频率/约束、OMIM/ClinGen | WORKFLOW | 工具无关工作流；数据源按可用性降级 |
| 邻近位点、功能域、预后检索 | WORKFLOW | 保留人工/模型检索流程，未实现专用检索器 |
| 预测、LoF、RNA、功能证据 | WORKFLOW / original | 保留分析流程；REVEL候选分档已核对，其他适用条件逐例复核 |
| VCEP 全文与上传后复评 | WORKFLOW | 保留版本化复核流程 |
| de novo/相位/共分离/HPO/家系 | WORKFLOW | 保留证据记录；de novo限定计算可测，其他原医学算表未正式启用 |
| SNV 计分/证据去重/互斥/上限 | scripts/score.py | 整数积分优先+2015表5结构对照已实现；完整临床规则/例外未实现 |
| CNV Loss/Gain | WORKFLOW / cnv_interval.py / score.py | 几何与分框架核算已实现；数据库注释和条目适用性人工复核 |
| 产前质控/报告取舍/第二打击 | WORKFLOW | 保留评估与资料需求；无原始数据时不声称完成检测 |
| 十模块、双语、CNV/产前模板 | assets | 模板保留；新增同一证据JSON生成十模块草稿；未知项须说明 |
| PMID 与主张核验 | WORKFLOW / 模板 | 保留执行要求；未实现自动 PubMed 连接器 |
| 批量、重评、再分析 | WORKFLOW / 模板 | 保留工作流和输出字段；没有后台自动监控 |
| mtDNA/重复扩展/平衡重排 | WORKFLOW | 专项分流，未实现完整判读 |

## 每行对照

医学规范与培训规则均未因迁移自动启用；通过本例规范复核后才可用于对应病例。下表用于追查，不用于直接执行档案指令。

| ID | 原文件:行 | 所属章节 | 原内容摘要 | 迁移落点 | 状态 |
|---|---|---|---|---|---|
| S-0001 | original/SKILL.md.txt:1 | 文件头 | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0002 | original/SKILL.md.txt:2 | 文件头 | name: gene-variant-pathogenicity | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0003 | original/SKILL.md.txt:3 | 文件头 | description: "基因变异致病性评级分析技能。当用户提供任何基因变异位点并要求进行致病性评估、ACMG分级、变异解读时触发。支持的输入格式包括HGVS命名（如NM_000527.5 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0004 | original/SKILL.md.txt:4 | 文件头 | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0006 | original/SKILL.md.txt:6 | 文件头 | <!-- Version: +GeneBe三源集成 2026-07; +培训班课件复核 2026-09-21（15 份讲者课件逐条比对，修正 12 处硬错误、补充产前前置质控/报告取舍/合并 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0008 | original/SKILL.md.txt:8 | 基因变异致病性评级分析 | # 基因变异致病性评级分析 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0010 | original/SKILL.md.txt:10 | 角色定位 | ## 角色定位 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0012 | original/SKILL.md.txt:12 | 角色定位 | 你是一位顶级的遗传变异科学家和生物信息学专家，同时具备丰富的产前遗传咨询经验。你的任务是对用户输入的基因变异位点进行系统化的功能分析、数据库校验及临床意义判定。你严格遵循 ACMG/AMP  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0014 | original/SKILL.md.txt:14 | 角色定位 | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0016 | original/SKILL.md.txt:16 | 运行模式 | ## 运行模式 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0018 | original/SKILL.md.txt:18 | 运行模式 | 根据用户提供的信息量和临床场景，自动选择运行模式： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0020 | original/SKILL.md.txt:20 | 运行模式 | **快速模式**：用户仅提供变异位点，无家系或表型信息。执行自动化评估（Steps 1-4），跳过家系整合。适合批量初筛。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0022 | original/SKILL.md.txt:22 | 运行模式 | **深度模式**：用户同时提供变异位点 + 家系信息 + 临床表型。执行完整五重校验（Steps 1-5），包括家系证据整合。适合疑难病例讨论。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0024 | original/SKILL.md.txt:24 | 运行模式 | **产前模式**：满足以下任一条件时自动激活： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0025 | original/SKILL.md.txt:25 | 运行模式 | - 用户提及"胎儿"、"孕"、"产前"、"prenatal"、"胎儿 MRI"、"超声发现" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0026 | original/SKILL.md.txt:26 | 运行模式 | - 变异发现背景为产前 WES/WGS/panel 检测 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0027 | original/SKILL.md.txt:27 | 运行模式 | - 用户问题涉及"出生后表现"、"预后"、"孩子会怎样" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0029 | original/SKILL.md.txt:29 | 运行模式 | 产前模式在标准分析流程基础上，**额外激活以下两个专项模块**（详见下文 Step 0.7 和模块8'）： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0030 | original/SKILL.md.txt:30 | 运行模式 | 1. **预后导向文献检索**（Step 0.7）：替代通用文献搜索策略，聚焦神经发育结局、影像学表现、出生后表型谱 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0031 | original/SKILL.md.txt:31 | 运行模式 | 2. **产前预后矩阵输出**（模块8'）：替代通用模块8，以预后维度重构临床建议 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0033 | original/SKILL.md.txt:33 | 运行模式 | 如果用户仅提供变异但该变异为 VUS 或接近判定边界，主动提示用户补充家系信息以完成深度分析。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0035 | original/SKILL.md.txt:35 | 运行模式 | **CNV 路由**：当输入为拷贝数变异（缺失/重复，如 chr11:19076957-36302387_del、Exon 10-12 dup、CMA/CNV-seq 报告）时，分类框架不同 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0037 | original/SKILL.md.txt:37 | 运行模式 | **不适用本框架的变异类型路由**（references/ACMG_CRITERIA.md §4.12）：重复扩展/动态突变（FMR1、HTT、DMPK、ATXN 等）按各病重复数阈值解读并 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0039 | original/SKILL.md.txt:39 | 运行模式 | **🤰 产前样本前置质控（产前模式强制，评级前执行）**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0040 | original/SKILL.md.txt:40 | 运行模式 | 1. **母体细胞污染（MCC）**：要求用户提供或从 trio VCF 推算 MCC 比例（阈值 5%；≥20% 基因型不可靠，报告置信度降为 Low）；未定量时 de novo/PS2  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0041 | original/SKILL.md.txt:41 | 运行模式 | 2. **VAF 核查**：先证者与亲代 VAF 是否在 40–60%；偏离者先排除伪影，再按嵌合处理（ACMG_CRITERIA.md §4.1.8/4.1.9），再发风险改为区间表述。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0042 | original/SKILL.md.txt:42 | 运行模式 | 3. **可比对性**：变异是否落在高同源/假基因/低 mappability 区（NOTCH2/NOTCH2NL、SMN1/2、PKD1、CYP21A2、GBA1、STRC、HBA1/2、 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0043 | original/SKILL.md.txt:43 | 运行模式 | 4. **Call 质量**：深度、VAF、链偏倚、是否 PASS；gnomAD 带过滤标记的位点不作频率证据。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0044 | original/SKILL.md.txt:44 | 运行模式 | 5. **胎儿期表型谱核对（Step 0.7 P0）**：检索"[基因] prenatal/fetal phenotype"，把胎儿表型按 HPO 三态（存在 / 不存在 / 本孕周不可评估 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0046 | original/SKILL.md.txt:46 | 运行模式 | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0048 | original/SKILL.md.txt:48 | Step 0：输入解析与标准化 | ## Step 0：输入解析与标准化 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0050 | original/SKILL.md.txt:50 | Step 0：输入解析与标准化 | 接收到用户输入后，首先进行格式识别和标准化处理。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0052 | original/SKILL.md.txt:52 | 支持的输入格式 | ### 支持的输入格式 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0054 | original/SKILL.md.txt:54 | 支持的输入格式 | \| 输入格式 \| 示例 \| 处理方式 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0055 | original/SKILL.md.txt:55 | 支持的输入格式 | \|---------\|------\|---------\| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0056 | original/SKILL.md.txt:56 | 支持的输入格式 | \| HGVS cDNA（含转录本） \| NM_000527.5:c.1183C>T \| 直接使用，校验转录本是否为 MANE Select \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0057 | original/SKILL.md.txt:57 | 支持的输入格式 | \| HGVS cDNA（含基因名） \| LDLR:c.1183C>T 或 LDLR c.1183C>T \| 查询 MANE Select 转录本后补全 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0058 | original/SKILL.md.txt:58 | 支持的输入格式 | \| 蛋白变异 \| BRCA1 p.Arg1699Trp 或 BRCA1 p.R1699W \| 反向映射至 cDNA 变异，确认转录本 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0059 | original/SKILL.md.txt:59 | 支持的输入格式 | \| VCF 格式 \| chr19-11116839-G-A (GRCh38) \| 注释对应基因、转录本、HGVS 命名 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0060 | original/SKILL.md.txt:60 | 支持的输入格式 | \| 自然语言 \| "LDLR基因第8外显子的一个错义变异 c.1183C>T" \| 提取关键信息，标准化 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0061 | original/SKILL.md.txt:61 | 支持的输入格式 | \| 批量输入 \| 多个变异以列表或表格形式提供 \| 逐一处理，按序输出 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0063 | original/SKILL.md.txt:63 | 标准化输出 | ### 标准化输出 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0065 | original/SKILL.md.txt:65 | 标准化输出 | 将用户输入统一转换为以下标准格式后再进入后续流程： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0066 | original/SKILL.md.txt:66 | 标准化输出 | - Gene: [基因名] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0067 | original/SKILL.md.txt:67 | 标准化输出 | - MANE Select Transcript: [NM_xxxxxx.x] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0068 | original/SKILL.md.txt:68 | 标准化输出 | - HGVSc: [cDNA 命名] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0069 | original/SKILL.md.txt:69 | 标准化输出 | - HGVSp: [蛋白命名] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0070 | original/SKILL.md.txt:70 | 标准化输出 | - Genome Build: [GRCh37/GRCh38] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0072 | original/SKILL.md.txt:72 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | ### ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0074 | original/SKILL.md.txt:74 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | 当用户仅提供 cDNA 命名（如 c.6001C>T）而未提供蛋白命名时，**禁止通过心算/推导来确定蛋白改变和变异类型**。密码子序列的微小差异（如 CGA vs CGC）可导致变异类型从 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0076 | original/SKILL.md.txt:76 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | **Layer 0 — Step 0.4 三源门控（最优先，若本轮已执行 Step 0.4）：** 若 EV.protein_gate.passed 为 true，直接采信其 Variant | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0078 | original/SKILL.md.txt:78 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | **Layer 1 — web_search 多源交叉验证（首选，成功率最高）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0080 | original/SKILL.md.txt:80 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | 同时发起以下 2-3 条 web_search 查询，从多个独立来源交叉确认蛋白改变： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0081 | original/SKILL.md.txt:81 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0082 | original/SKILL.md.txt:82 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | web_search: "VariantValidator [NM转录本] c.[变异]" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0083 | original/SKILL.md.txt:83 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | web_search: "[基因名] c.[变异] protein change" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0084 | original/SKILL.md.txt:84 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | web_search: "ClinVar [基因名] c.[变异]" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0085 | original/SKILL.md.txt:85 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0086 | original/SKILL.md.txt:86 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | - 从搜索结果摘要中提取蛋白改变信息（ClinVar 条目通常同时显示 cDNA 和蛋白命名） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0087 | original/SKILL.md.txt:87 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | - **至少需要 2 个独立来源一致**才视为验证通过 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0088 | original/SKILL.md.txt:88 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | - 若搜索结果中发现 ClinVar 变异页面 URL，用 web_fetch 获取完整页面以提取精确的 HGVSp | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0090 | original/SKILL.md.txt:90 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | **Layer 2 — web_fetch 直接访问注释工具（回退）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0092 | original/SKILL.md.txt:92 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | 若 Layer 1 未能获取一致结果，尝试直接访问： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0093 | original/SKILL.md.txt:93 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0094 | original/SKILL.md.txt:94 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | web_fetch: https://rest.variantvalidator.org/VariantValidator/variantvalidator/GRCh38/[NM_XXXXX | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0095 | original/SKILL.md.txt:95 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0096 | original/SKILL.md.txt:96 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | ⚠️ 注意：此 API 端点可用性不稳定，约 50% 的情况下可能超时或返回错误。不要将其作为唯一验证路径。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0098 | original/SKILL.md.txt:98 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | **Layer 3 — NCBI RefSeq 序列回溯验证（深度回退）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0100 | original/SKILL.md.txt:100 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | 当 Layer 1-2 均失败时： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0101 | original/SKILL.md.txt:101 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0102 | original/SKILL.md.txt:102 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | web_search: "NCBI RefSeq [NM转录本] CDS sequence" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0103 | original/SKILL.md.txt:103 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | web_search: "[基因名] exon [N] coding sequence reference" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0104 | original/SKILL.md.txt:104 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0105 | original/SKILL.md.txt:105 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | - 尝试从 NCBI Gene 或 RefSeq 页面获取参考序列信息 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0106 | original/SKILL.md.txt:106 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | - 结合 cDNA 位置定位密码子，交叉验证蛋白改变 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0108 | original/SKILL.md.txt:108 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | **Layer 4 — 最终回退（所有自动化验证失败）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0110 | original/SKILL.md.txt:110 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | 若以上三层均失败，必须在报告中以 ⛔ 醒目标注： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0111 | original/SKILL.md.txt:111 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | "蛋白改变未经外部工具验证，以下分析基于 AI 推导，可能存在根本性错误。请用户在 https://variantvalidator.org/ 或 https://mutalyzer.nl/ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0112 | original/SKILL.md.txt:112 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | 同时提供一键验证链接：https://rest.variantvalidator.org/VariantValidator/variantvalidator/GRCh38/[完整HGVS]/ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0114 | original/SKILL.md.txt:114 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | **门控规则**: | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0115 | original/SKILL.md.txt:115 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | - 变异类型（missense/nonsense/synonymous 等）的确定 **完全取决于验证后的蛋白改变**，不可提前假设 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0116 | original/SKILL.md.txt:116 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | - 在蛋白改变未验证的情况下，**禁止赋予 PVS1** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0117 | original/SKILL.md.txt:117 | ⚠️ 蛋白改变强制验证（MANDATORY GATE — 不可跳过） | - 仅当用户已提供完整的 HGVSp 命名时可跳过此步骤 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0119 | original/SKILL.md.txt:119 | 转录本校验规则 | ### 转录本校验规则 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0121 | original/SKILL.md.txt:121 | 转录本校验规则 | 转录本来源优先级：MANE Select > MANE Plus Clinical > RefSeq canonical | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0123 | original/SKILL.md.txt:123 | 转录本校验规则 | 当用户提供的转录本与 MANE Select 不同时： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0124 | original/SKILL.md.txt:124 | 转录本校验规则 | 1. 明确提示差异 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0125 | original/SKILL.md.txt:125 | 转录本校验规则 | 2. 同时给出两个转录本下的变异命名对照 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0126 | original/SKILL.md.txt:126 | 转录本校验规则 | 3. 后续分析以 MANE Select 为主，但注明用户原始转录本的命名 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0128 | original/SKILL.md.txt:128 | 转录本校验规则 | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0130 | original/SKILL.md.txt:130 | Step 0.4:三源结构化取数(High-Priority Layer 0) | ## Step 0.4:三源结构化取数(High-Priority Layer 0) | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0132 | original/SKILL.md.txt:132 | Step 0.4:三源结构化取数(High-Priority Layer 0) | 标准化输入后,**优先用 references/genebe_fields.py 一次性获取三源合并证据**,以坍缩后续 Step 0.5 / 1.x / 模块5 的零散 web_searc | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0134 | original/SKILL.md.txt:134 | 0.4.1 执行(按界面) | ### 0.4.1 执行(按界面) | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0136 | original/SKILL.md.txt:136 | 0.4.1 执行(按界面) | **Claude Code / 有开放网络** —— 首选,直接跑: | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0137 | original/SKILL.md.txt:137 | 0.4.1 执行(按界面) | bash | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0138 | original/SKILL.md.txt:138 | 0.4.1 执行(按界面) | python3 references/genebe_fields.py "{转录本:cDNA}"        # 输出 evidence JSON | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0139 | original/SKILL.md.txt:139 | 例:python3 references/genebe_fields.py "NM_017780.4:c.2831G>A" | # 例:python3 references/genebe_fields.py "NM_017780.4:c.2831G>A" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0140 | original/SKILL.md.txt:140 | 例:python3 references/genebe_fields.py "NM_017780.4:c.2831G>A" |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0141 | original/SKILL.md.txt:141 | 例:python3 references/genebe_fields.py "NM_017780.4:c.2831G>A" | 把 stdout 的 JSON 读入为本轮**证据池 EV**;EV["_sources"] 三源应为 ok。人工核对可加 --card。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0143 | original/SKILL.md.txt:143 | 例:python3 references/genebe_fields.py "NM_017780.4:c.2831G>A" | **网页/App 沙箱**(够不到三源)——降级: | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0144 | original/SKILL.md.txt:144 | 例:python3 references/genebe_fields.py "NM_017780.4:c.2831G>A" | - 若用户提供了 Worker 的**完整 /annotate URL** → web_fetch 之(仅得五源部分,GeneBe/VV 缺); | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0145 | original/SKILL.md.txt:145 | 例:python3 references/genebe_fields.py "NM_017780.4:c.2831G>A" | - 否则请用户在 Code 跑上面命令、把 JSON 贴回; | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0146 | original/SKILL.md.txt:146 | 例:python3 references/genebe_fields.py "NM_017780.4:c.2831G>A" | - 再不行 → 回落原 web_search 流程。**在此之前不臆造。** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0148 | original/SKILL.md.txt:148 | 0.4.2 字段 → 下游模块(键名见 genebe_fields.py 的 to_evidence) | ### 0.4.2 字段 → 下游模块(键名见 genebe_fields.py 的 to_evidence) | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0150 | original/SKILL.md.txt:150 | 0.4.2 字段 → 下游模块(键名见 genebe_fields.py 的 to_evidence) | \| 证据键 \| 喂给 \| 说明 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0151 | original/SKILL.md.txt:151 | 0.4.2 字段 → 下游模块(键名见 genebe_fields.py 的 to_evidence) | \|---\|---\|---\| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0152 | original/SKILL.md.txt:152 | 0.4.2 字段 → 下游模块(键名见 genebe_fields.py 的 to_evidence) | \| EV.protein_gate(transcript/hgvs_c/hgvs_p) \| **Step 0 蛋白强制验证门** \| VV 权威 HGVSp + GeneBe 交叉;p | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0153 | original/SKILL.md.txt:153 | 0.4.2 字段 → 下游模块(键名见 genebe_fields.py 的 to_evidence) | \| EV.coords(hg19/hg38/rsid) \| 报告头 \| 双坐标已 VV 互证 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0154 | original/SKILL.md.txt:154 | 0.4.2 字段 → 下游模块(键名见 genebe_fields.py 的 to_evidence) | \| EV.clinvar \| Step 0.5 分流 \| 变异自身 ClinVar 分类/星级/提交 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0155 | original/SKILL.md.txt:155 | 0.4.2 字段 → 下游模块(键名见 genebe_fields.py 的 to_evidence) | \| EV.frequency(global/eas/hint) \| Step 1.2 \| **EAS 原始 AC/AN;BA1/BS1 的 FAF95 见 caveat** \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0156 | original/SKILL.md.txt:156 | 0.4.2 字段 → 下游模块(键名见 genebe_fields.py 的 to_evidence) | \| EV.predictors(dict,读 value) \| Step 1.2 / PP3-BP4 \| CADD/REVEL/phyloP/SIFT/PolyPhen/MetaSVM | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0157 | original/SKILL.md.txt:157 | 0.4.2 字段 → 下游模块(键名见 genebe_fields.py 的 to_evidence) | \| EV.constraint \| PVS1/PM2/PP2/BP1 背景 \| pLI/LOEUF/mis_z/oe_mis \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0158 | original/SKILL.md.txt:158 | 0.4.2 字段 → 下游模块(键名见 genebe_fields.py 的 to_evidence) | \| EV.codon_landscape \| **PS1/PM5** \| 同密码子已分类变异;空=ClinVar 暂无,非良性证据 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0159 | original/SKILL.md.txt:159 | 0.4.2 字段 → 下游模块(键名见 genebe_fields.py 的 to_evidence) | \| EV.acmg_benchmark \| **模块5 外部对标** \| GeneBe 自动 ACMG,仅基准 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0161 | original/SKILL.md.txt:161 | 0.4.3 CAVEAT(必守,防误用) | ### 0.4.3 CAVEAT(必守,防误用) | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0163 | original/SKILL.md.txt:163 | 0.4.3 CAVEAT(必守,防误用) | 1. **频率精判归 gnomAD FAF95,不归本工具**:EV.frequency.eas 是原始 AC/AN,仅作"东亚是否常见"快速筛。BA1/BS1 严格赋值须用 gnomAD  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0164 | original/SKILL.md.txt:164 | 0.4.3 CAVEAT(必守,防误用) | 2. **EV.acmg_benchmark(GeneBe)只进模块5对标,绝不覆盖本技能专家评级**:Step 0.6 邻近扫描、产前预后、VCEP 全文门控、家系/功能/表型证据仍由主流 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0165 | original/SKILL.md.txt:165 | 0.4.3 CAVEAT(必守,防误用) | 3. **预测读 value(即 *_score)+ 技能阈值自定 PP3/BP4**;不依赖任何 _prediction 字符串。REVEL 灰区(~0.5)不轻给 PP3。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0166 | original/SKILL.md.txt:166 | 0.4.3 CAVEAT(必守,防误用) | 4. **转录本以 EV.protein_gate.transcript(RefSeq NM)为准**。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0167 | original/SKILL.md.txt:167 | 0.4.3 CAVEAT(必守,防误用) | 5. **EAS/中国人群缺口**:EAS FAF95 → gnomAD GraphQL;ChinaMAP/WBBC/NyuWa → 门户人工(EV._needs_manual 已列)。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0168 | original/SKILL.md.txt:168 | 0.4.3 CAVEAT(必守,防误用) | 6. **零编造**:EV 中为 None/❌ 的字段一律照标;单源 ❌ 时该源相关证据回落 web_search,不猜。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0169 | original/SKILL.md.txt:169 | 0.4.3 CAVEAT(必守,防误用) | 7. **同位点空 ≠ 良性**:EV.codon_landscape 为空仅代表 ClinVar 无同密码子记录。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0171 | original/SKILL.md.txt:171 | 0.4.4 取数状态并入报告 | ### 0.4.4 取数状态并入报告 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0172 | original/SKILL.md.txt:172 | 0.4.4 取数状态并入报告 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0173 | original/SKILL.md.txt:173 | 0.4.4 取数状态并入报告 | ── 三源取数状态 ── | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0174 | original/SKILL.md.txt:174 | 0.4.4 取数状态并入报告 | _sources : {EV._sources} | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0175 | original/SKILL.md.txt:175 | 0.4.4 取数状态并入报告 | 过门     : protein_gate.passed | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0176 | original/SKILL.md.txt:176 | 0.4.4 取数状态并入报告 | 警告     : {EV._warnings}   # 如 ClinVar 429 → 同位点地形可能缺 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0177 | original/SKILL.md.txt:177 | 0.4.4 取数状态并入报告 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0179 | original/SKILL.md.txt:179 | 0.4.4 取数状态并入报告 | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0181 | original/SKILL.md.txt:181 | Step 0.5：ClinVar 前置快速筛查（Rapid Triage） | ## Step 0.5：ClinVar 前置快速筛查（Rapid Triage） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0183 | original/SKILL.md.txt:183 | Step 0.5：ClinVar 前置快速筛查（Rapid Triage） | **若 EV.clinvar（Step 0.4 已取）已有分类，直接用于本步分流；web_search 仅用于补充星级与提交机构信息。** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0185 | original/SKILL.md.txt:185 | Step 0.5：ClinVar 前置快速筛查（Rapid Triage） | 在完成 Step 0 标准化后，**立即执行一次快速 ClinVar 检索**（使用 cDNA 命名，不依赖蛋白命名）： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0187 | original/SKILL.md.txt:187 | Step 0.5：ClinVar 前置快速筛查（Rapid Triage） | 1. web_search ClinVar [基因名] c.[变异] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0188 | original/SKILL.md.txt:188 | Step 0.5：ClinVar 前置快速筛查（Rapid Triage） | 2. 若命中 ClinVar 条目，快速提取： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0189 | original/SKILL.md.txt:189 | Step 0.5：ClinVar 前置快速筛查（Rapid Triage） |    - 聚合分类（Pathogenic / VUS / Benign 等） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0190 | original/SKILL.md.txt:190 | Step 0.5：ClinVar 前置快速筛查（Rapid Triage） |    - Review status 星级 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0191 | original/SKILL.md.txt:191 | Step 0.5：ClinVar 前置快速筛查（Rapid Triage） |    - 提交机构数量和一致性 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0193 | original/SKILL.md.txt:193 | Step 0.5：ClinVar 前置快速筛查（Rapid Triage） | **分流规则**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0194 | original/SKILL.md.txt:194 | Step 0.5：ClinVar 前置快速筛查（Rapid Triage） | - 若 ClinVar ≥2星 + 多机构一致 Pathogenic → 进入**确认模式**（重点验证而非发现） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0195 | original/SKILL.md.txt:195 | Step 0.5：ClinVar 前置快速筛查（Rapid Triage） | - 若 ClinVar ≥2星 + 多机构一致 Benign/Likely Benign → 进入**确认模式**，重点核实群体频率和预测评分是否支持良性判定 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0196 | original/SKILL.md.txt:196 | Step 0.5：ClinVar 前置快速筛查（Rapid Triage） | - 若 ClinVar 有冲突 / VUS / 无条目 → 进入**完整分析模式**（Steps 1-4 全展开） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0198 | original/SKILL.md.txt:198 | Step 0.5：ClinVar 前置快速筛查（Rapid Triage） | **注意**: 前置筛查结果不替代后续独立分析，但可显著提高分析效率并避免方向性错误。如果独立分析结论与 ClinVar 多机构共识严重不一致（如自己判 Pathogenic 而 ClinV | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0200 | original/SKILL.md.txt:200 | Step 0.5：ClinVar 前置快速筛查（Rapid Triage） | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0202 | original/SKILL.md.txt:202 | Step 0.6：Novel Variant 邻近位点扩圈检索（Neighborhood Scan） | ## Step 0.6：Novel Variant 邻近位点扩圈检索（Neighborhood Scan） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0204 | original/SKILL.md.txt:204 | Step 0.6：Novel Variant 邻近位点扩圈检索（Neighborhood Scan） | **触发条件**：Step 0.5 ClinVar 前置筛查结果为"无条目"或"仅1条低星级提交"时，**必须强制执行本步骤**。不可跳过。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0206 | original/SKILL.md.txt:206 | 设计动机 | ### 设计动机 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0208 | original/SKILL.md.txt:208 | 设计动机 | ClinVar 无记录不等于"无参照"——它意味着检索半径需要扩大。对于 novel variant，同功能域内邻近位点的已报道变异是证据等级最高的临床参照来源，其价值远超计算预测评分。本步 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0210 | original/SKILL.md.txt:210 | 执行策略：三圈扩展检索 | ### 执行策略：三圈扩展检索 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0212 | original/SKILL.md.txt:212 | 执行策略：三圈扩展检索 | **第一圈（±10 aa，同密码子区）— 最高优先级** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0214 | original/SKILL.md.txt:214 | 执行策略：三圈扩展检索 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0215 | original/SKILL.md.txt:215 | 执行策略：三圈扩展检索 | web_search: "[基因名] p.[氨基酸位置±5] missense variant" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0216 | original/SKILL.md.txt:216 | 执行策略：三圈扩展检索 | web_search: "[基因名] c.[cDNA坐标-30到+30范围] pathogenic" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0217 | original/SKILL.md.txt:217 | 执行策略：三圈扩展检索 | web_search: "ClinVar [基因名] [氨基酸位置号±5]" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0218 | original/SKILL.md.txt:218 | 执行策略：三圈扩展检索 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0219 | original/SKILL.md.txt:219 | 执行策略：三圈扩展检索 | → 目标：同密码子或紧邻位点的已报道变异（可直接用于 PS1/PM5 评估） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0221 | original/SKILL.md.txt:221 | 执行策略：三圈扩展检索 | **第二圈（同功能子域）— 高优先级** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0223 | original/SKILL.md.txt:223 | 执行策略：三圈扩展检索 | 须先确认变异所在的精确结构域（需查阅 UniProt/文献确认域边界），再执行： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0224 | original/SKILL.md.txt:224 | 执行策略：三圈扩展检索 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0225 | original/SKILL.md.txt:225 | 执行策略：三圈扩展检索 | web_search: "[基因名] [结构域名] variant clinical" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0226 | original/SKILL.md.txt:226 | 执行策略：三圈扩展检索 | web_search: "[基因名] [结构域名] missense phenotype" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0227 | original/SKILL.md.txt:227 | 执行策略：三圈扩展检索 | web_search: "[基因名] [结构域名] de novo pathogenic" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0228 | original/SKILL.md.txt:228 | 执行策略：三圈扩展检索 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0229 | original/SKILL.md.txt:229 | 执行策略：三圈扩展检索 | → 目标：同功能子域变异的表型规律（如 DYNC1H1 AAA6 域的 L4179S） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0231 | original/SKILL.md.txt:231 | 执行策略：三圈扩展检索 | **第三圈（预后导向反向检索）— 中优先级** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0233 | original/SKILL.md.txt:233 | 执行策略：三圈扩展检索 | 根据基因已知的表型谱，执行表型关键词检索： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0234 | original/SKILL.md.txt:234 | 执行策略：三圈扩展检索 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0235 | original/SKILL.md.txt:235 | 执行策略：三圈扩展检索 | web_search: "[基因名] [最可能表型A] variant" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0236 | original/SKILL.md.txt:236 | 执行策略：三圈扩展检索 | web_search: "[基因名] [最可能表型B] without [对立表型]" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0237 | original/SKILL.md.txt:237 | 执行策略：三圈扩展检索 | web_search: "[基因名] novel variant [相关疾病名]" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0238 | original/SKILL.md.txt:238 | 执行策略：三圈扩展检索 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0239 | original/SKILL.md.txt:239 | 执行策略：三圈扩展检索 | → 目标：发现该域/位置变异的特异性表型模式，辅助预后判断 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0241 | original/SKILL.md.txt:241 | 邻近变异优先级评分体系 | ### 邻近变异优先级评分体系 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0243 | original/SKILL.md.txt:243 | 邻近变异优先级评分体系 | 检索到邻近变异后，按以下优先级评估其参考价值： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0245 | original/SKILL.md.txt:245 | 邻近变异优先级评分体系 | \| 级别 \| 距离 / 关系 \| 参考价值 \| ACMG 证据用途 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0246 | original/SKILL.md.txt:246 | 邻近变异优先级评分体系 | \|------\|------------\|---------\|--------------\| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0247 | original/SKILL.md.txt:247 | 邻近变异优先级评分体系 | \| L1 \| 同密码子，不同核苷酸 \| 最高 \| PS1（直接）或 PM5（不同氨基酸替换）\| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0248 | original/SKILL.md.txt:248 | 邻近变异优先级评分体系 | \| L2 \| ±10 aa 内 \| 高 \| **不直接赋 PM5**（PM5 严格限同一残基）；作为 PM1 热点门槛 3 的支撑与表型参照 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0249 | original/SKILL.md.txt:249 | 邻近变异优先级评分体系 | \| L3 \| 同功能子域 \| 中-高 \| 提供表型倾向方向；不直接赋 ACMG 代码 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0250 | original/SKILL.md.txt:250 | 邻近变异优先级评分体系 | \| L4 \| 同大结构域 \| 中 \| 辅助支持 PM1 赋值；提供背景参考 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0252 | original/SKILL.md.txt:252 | 强制输出：邻近变异地形报告 | ### 强制输出：邻近变异地形报告 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0254 | original/SKILL.md.txt:254 | 强制输出：邻近变异地形报告 | 本步骤完成后，**必须在模块2（Molecular Profile）中增加"邻近变异地形"字段**，格式如下： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0256 | original/SKILL.md.txt:256 | 强制输出：邻近变异地形报告 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0257 | original/SKILL.md.txt:257 | 强制输出：邻近变异地形报告 | Nearest reported variant:  p.[变异名]（L[优先级]，距本变异 [N] aa，[来源文献/数据库]） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0258 | original/SKILL.md.txt:258 | 强制输出：邻近变异地形报告 |                            表型摘要：[一句话摘要] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0259 | original/SKILL.md.txt:259 | 强制输出：邻近变异地形报告 | Domain landscape:          [本变异所在结构域的变异密度描述：高/中/低研究密度] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0260 | original/SKILL.md.txt:260 | 强制输出：邻近变异地形报告 | Literature gap:            [该域变异的文献缺口说明] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0261 | original/SKILL.md.txt:261 | 强制输出：邻近变异地形报告 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0263 | original/SKILL.md.txt:263 | 强制输出：邻近变异地形报告 | 若三圈检索均无发现，标注：Nearest reported variant: None found within same domain（文献稀缺域），并在模块6中专节讨论这一知识空白对分类 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0265 | original/SKILL.md.txt:265 | 邻近变异对 ACMG 证据代码的影响 | ### 邻近变异对 ACMG 证据代码的影响 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0267 | original/SKILL.md.txt:267 | 邻近变异对 ACMG 证据代码的影响 | - **L1 同密码子变异已报道为致病性** → 可赋 PS1（氨基酸改变相同）或 PM5（不同氨基酸替换但同样有害）；同密码子 ≥2 个不同致病错义且 VCEP/SVI 支持 → PM5_ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0268 | original/SKILL.md.txt:268 | 邻近变异对 ACMG 证据代码的影响 | - **L2-L3 邻近变异的表型数据** → 不直接影响 ACMG 积分，但进入模块6的预后分析，并在模块8的临床建议中引用 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0269 | original/SKILL.md.txt:269 | 邻近变异对 ACMG 证据代码的影响 | - **同域变异缺乏 MCD 的系统性证据** → 可降低对 MCD 风险的预测（如 AAA6 域变异），并在预后矩阵中明确体现 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0271 | original/SKILL.md.txt:271 | 邻近变异对 ACMG 证据代码的影响 | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0273 | original/SKILL.md.txt:273 | Step 0.7：产前预后导向检索（Prenatal Prognosis Search） | ## Step 0.7：产前预后导向检索（Prenatal Prognosis Search） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0275 | original/SKILL.md.txt:275 | Step 0.7：产前预后导向检索（Prenatal Prognosis Search） | **触发条件**：**仅在产前模式下执行**。在 Step 0.6 完成后立即执行，不等待 Step 1。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0277 | original/SKILL.md.txt:277 | 设计动机 | ### 设计动机 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0279 | original/SKILL.md.txt:279 | 设计动机 | 产前遗传咨询的核心临床问题是"**这个孩子出生后会是什么表现**"，而非仅仅"变异是否致病"。ACMG 分类框架回答的是第一个问题，而本步骤专门收集回答第二个问题所需的证据。两者互补，缺一不 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0281 | original/SKILL.md.txt:281 | P1：影像学预后检索（必须执行） | ### P1：影像学预后检索（必须执行） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0283 | original/SKILL.md.txt:283 | P1：影像学预后检索（必须执行） | 聚焦神经系统发育影像学结局，尤其适用于神经发育基因： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0285 | original/SKILL.md.txt:285 | P1：影像学预后检索（必须执行） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0286 | original/SKILL.md.txt:286 | P1：影像学预后检索（必须执行） | web_search: "[基因名] prenatal MRI cortical development" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0287 | original/SKILL.md.txt:287 | P1：影像学预后检索（必须执行） | web_search: "[基因名] brain malformation MRI normal" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0288 | original/SKILL.md.txt:288 | P1：影像学预后检索（必须执行） | web_search: "[基因名] [Step 0.6 发现的最近邻近变异] brain MRI" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0289 | original/SKILL.md.txt:289 | P1：影像学预后检索（必须执行） | web_search: "[基因名] [功能域名] without malformation" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0290 | original/SKILL.md.txt:290 | P1：影像学预后检索（必须执行） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0292 | original/SKILL.md.txt:292 | P1：影像学预后检索（必须执行） | → 目标问题：同域变异中，MRI 正常的比例是多少？皮质发育畸形（MCD）的风险有多高？ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0294 | original/SKILL.md.txt:294 | P2：神经发育结局检索（必须执行） | ### P2：神经发育结局检索（必须执行） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0296 | original/SKILL.md.txt:296 | P2：神经发育结局检索（必须执行） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0297 | original/SKILL.md.txt:297 | P2：神经发育结局检索（必须执行） | web_search: "[基因名] neurodevelopmental outcome intellectual disability" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0298 | original/SKILL.md.txt:298 | P2：神经发育结局检索（必须执行） | web_search: "[基因名] epilepsy ASD seizure onset" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0299 | original/SKILL.md.txt:299 | P2：神经发育结局检索（必须执行） | web_search: "[基因名] [功能域名] developmental delay follow-up" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0300 | original/SKILL.md.txt:300 | P2：神经发育结局检索（必须执行） | web_search: "[基因名] [最近邻近变异名] clinical course" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0301 | original/SKILL.md.txt:301 | P2：神经发育结局检索（必须执行） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0303 | original/SKILL.md.txt:303 | P2：神经发育结局检索（必须执行） | → 目标问题：智力障碍/ASD/癫痫的发生率？起病年龄？严重程度范围？ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0305 | original/SKILL.md.txt:305 | P3：主动用户文献补充请求（Novel Variant 时必须执行） | ### P3：主动用户文献补充请求（Novel Variant 时必须执行） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0307 | original/SKILL.md.txt:307 | P3：主动用户文献补充请求（Novel Variant 时必须执行） | 当本例为 novel variant（Step 0.5 无记录）时，在完成 P1-P2 检索后，**必须向用户发出以下标准化请求**，插入分析过程的早期（Step 0.7 完成后即输出，不等 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0309 | original/SKILL.md.txt:309 | P3：主动用户文献补充请求（Novel Variant 时必须执行） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0310 | original/SKILL.md.txt:310 | P3：主动用户文献补充请求（Novel Variant 时必须执行） | 【产前 Novel Variant 文献补充请求】 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0312 | original/SKILL.md.txt:312 | P3：主动用户文献补充请求（Novel Variant 时必须执行） | 本变异（[变异名]）在公共数据库中无先例记录，属于首次报道位点。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0313 | original/SKILL.md.txt:313 | P3：主动用户文献补充请求（Novel Variant 时必须执行） | 目前已识别的最近参照变异为： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0315 | original/SKILL.md.txt:315 | P3：主动用户文献补充请求（Novel Variant 时必须执行） |   · [Step 0.6 L1/L2 变异]（距本例 [N] aa，[来源]）— [表型一句话摘要] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0316 | original/SKILL.md.txt:316 | P3：主动用户文献补充请求（Novel Variant 时必须执行） |   · [Step 0.6 L3 变异（若有）]（同[域名]域，[来源]）— [表型一句话摘要] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0318 | original/SKILL.md.txt:318 | P3：主动用户文献补充请求（Novel Variant 时必须执行） | 如您持有以下类型文献，上传后可显著提升产前预后分析的准确性： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0319 | original/SKILL.md.txt:319 | P3：主动用户文献补充请求（Novel Variant 时必须执行） |   1. 上述邻近变异的完整病例报告（尤其是 MRI 结果和出生后随访数据） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0320 | original/SKILL.md.txt:320 | P3：主动用户文献补充请求（Novel Variant 时必须执行） |   2. [基因名] [功能域名] 变异的系统综述或病例系列 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0321 | original/SKILL.md.txt:321 | P3：主动用户文献补充请求（Novel Variant 时必须执行） |   3. 该基因的产前表型相关任何报道 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0323 | original/SKILL.md.txt:323 | P3：主动用户文献补充请求（Novel Variant 时必须执行） | 这是产前 novel variant 分析中最关键的证据来源， | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0324 | original/SKILL.md.txt:324 | P3：主动用户文献补充请求（Novel Variant 时必须执行） | 无法通过自动检索完全替代，请优先提供。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0325 | original/SKILL.md.txt:325 | P3：主动用户文献补充请求（Novel Variant 时必须执行） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0327 | original/SKILL.md.txt:327 | P4：产前检查窗口建议（基于检索结果生成） | ### P4：产前检查窗口建议（基于检索结果生成） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0329 | original/SKILL.md.txt:329 | P4：产前检查窗口建议（基于检索结果生成） | 根据 P1-P2 检索结果，生成具体的超声/MRI 监测建议列表，供模块8'使用： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0331 | original/SKILL.md.txt:331 | P4：产前检查窗口建议（基于检索结果生成） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0332 | original/SKILL.md.txt:332 | P4：产前检查窗口建议（基于检索结果生成） | 产前影像监测建议（基于 [基因名] [域名] 变异的文献证据）： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0333 | original/SKILL.md.txt:333 | P4：产前检查窗口建议（基于检索结果生成） |   高优先级：[基于文献发现率 >30% 的异常项目] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0334 | original/SKILL.md.txt:334 | P4：产前检查窗口建议（基于检索结果生成） |   中优先级：[基于文献发现率 10-30% 的异常项目] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0335 | original/SKILL.md.txt:335 | P4：产前检查窗口建议（基于检索结果生成） |   参考监测：[罕见但有报道的异常项目] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0337 | original/SKILL.md.txt:337 | P4：产前检查窗口建议（基于检索结果生成） | 建议孕周：[基于胎儿发育时间轴和异常可检出窗口] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0338 | original/SKILL.md.txt:338 | P4：产前检查窗口建议（基于检索结果生成） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0340 | original/SKILL.md.txt:340 | P4：产前检查窗口建议（基于检索结果生成） | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0342 | original/SKILL.md.txt:342 | Step 1：数据库检索（Database Retrieval） | ## Step 1：数据库检索（Database Retrieval） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0344 | original/SKILL.md.txt:344 | 🔧 数据获取可靠性框架（适用于所有子步骤） | ### 🔧 数据获取可靠性框架（适用于所有子步骤） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0346 | original/SKILL.md.txt:346 | 🔧 数据获取可靠性框架（适用于所有子步骤） | **核心原则变更**：优先 web_search 定位信息 → 用 web_fetch 深化获取。不再依赖直接构造 API URL 或数据库查询 URL 进行 web_fetch（这些端点的 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0348 | original/SKILL.md.txt:348 | 🔧 数据获取可靠性框架（适用于所有子步骤） | **通用三层获取策略**（每个数据源均按此框架执行）： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0350 | original/SKILL.md.txt:350 | 🔧 数据获取可靠性框架（适用于所有子步骤） | \| Layer \| 方法 \| 预期成功率 \| 用途 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0351 | original/SKILL.md.txt:351 | 🔧 数据获取可靠性框架（适用于所有子步骤） | \|-------\|------\|-----------\|------\| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0352 | original/SKILL.md.txt:352 | 🔧 数据获取可靠性框架（适用于所有子步骤） | \| L1 \| web_search 短查询（1-4词） \| ~85% \| 从搜索摘要直接提取关键数据点 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0353 | original/SKILL.md.txt:353 | 🔧 数据获取可靠性框架（适用于所有子步骤） | \| L2 \| web_fetch 从 L1 结果中获取的具体 URL \| ~60% \| 获取完整页面的结构化数据 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0354 | original/SKILL.md.txt:354 | 🔧 数据获取可靠性框架（适用于所有子步骤） | \| L3 \| web_search 替代查询 + 间接来源 \| ~70% \| 当 L1 查询词未命中时，换词重试 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0356 | original/SKILL.md.txt:356 | 🔧 数据获取可靠性框架（适用于所有子步骤） | **并行效率规则**：每轮工具调用尽量同时发起 2-3 条 web_search（不同数据源或不同查询策略），而非串行等待。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0358 | original/SKILL.md.txt:358 | 🔧 数据获取可靠性框架（适用于所有子步骤） | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0360 | original/SKILL.md.txt:360 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | ### 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0362 | original/SKILL.md.txt:362 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | **路径A — cDNA 命名（必须始终执行，最高优先级）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0364 | original/SKILL.md.txt:364 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | 第一轮（并行发起）： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0365 | original/SKILL.md.txt:365 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0366 | original/SKILL.md.txt:366 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | web_search: "ClinVar [基因名] c.[cDNA变异]"          ← 最核心查询 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0367 | original/SKILL.md.txt:367 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | web_search: "[基因名] c.[cDNA变异] pathogenic"         ← 补充临床意义信息 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0368 | original/SKILL.md.txt:368 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0369 | original/SKILL.md.txt:369 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | - 从搜索结果摘要中直接提取：ClinVar 分类、Variation ID、提交数 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0370 | original/SKILL.md.txt:370 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | - 若搜索结果包含 ClinVar 页面 URL（格式如 ncbi.nlm.nih.gov/clinvar/variation/XXXXXX），用 web_fetch 获取完整页面 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0371 | original/SKILL.md.txt:371 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | - ⚠️ 注意：直接构造 ClinVar 查询 URL（如 clinvar/?term=...）进行 web_fetch 成功率低，因为 NCBI 动态页面通常返回空壳 HTML。**始终先 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0373 | original/SKILL.md.txt:373 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | **路径B — 蛋白命名（仅在 Step 0 已验证蛋白改变后使用）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0374 | original/SKILL.md.txt:374 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0375 | original/SKILL.md.txt:375 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | web_search: "ClinVar [基因名] p.[蛋白变异]" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0376 | original/SKILL.md.txt:376 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | web_search: "[基因名] [p.变异] clinical significance" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0377 | original/SKILL.md.txt:377 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0379 | original/SKILL.md.txt:379 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | **路径C — 基因组坐标（推荐作为独立验证路径）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0380 | original/SKILL.md.txt:380 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0381 | original/SKILL.md.txt:381 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | web_search: "ClinVar [chr] [position] [ref] [alt]" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0382 | original/SKILL.md.txt:382 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0384 | original/SKILL.md.txt:384 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | **路径D — dbSNP rsID（当路径A-C均未精确命中时）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0385 | original/SKILL.md.txt:385 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0386 | original/SKILL.md.txt:386 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | web_search: "dbSNP [基因名] c.[cDNA变异]"          ← 获取 rsID | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0387 | original/SKILL.md.txt:387 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | web_search: "ClinVar rs[XXXXXXX]"                    ← 用 rsID 检索 ClinVar | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0388 | original/SKILL.md.txt:388 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0390 | original/SKILL.md.txt:390 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | **路径E — 氨基酸位置模糊搜索（最终回退）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0391 | original/SKILL.md.txt:391 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0392 | original/SKILL.md.txt:392 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | web_search: "ClinVar [基因名] [氨基酸位置号]" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0393 | original/SKILL.md.txt:393 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0394 | original/SKILL.md.txt:394 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | - 这可以在蛋白改变不确定时仍然找到该位点的所有变异 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0396 | original/SKILL.md.txt:396 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | **关键规则**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0397 | original/SKILL.md.txt:397 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | - 路径A（cDNA命名 web_search）必须始终执行，因为它不依赖蛋白改变的正确性且成功率最高 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0398 | original/SKILL.md.txt:398 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | - 当路径A未命中时，不能仅依赖路径B，必须尝试路径C或D | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0399 | original/SKILL.md.txt:399 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | - 若所有路径均未命中，在报告中标注并提供直接查询链接：https://www.ncbi.nlm.nih.gov/clinvar/?term=[基因名]+[cDNA变异] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0401 | original/SKILL.md.txt:401 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | **提取信息：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0402 | original/SKILL.md.txt:402 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | - 当前临床意义评级（Clinical significance） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0403 | original/SKILL.md.txt:403 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | - 提交记录数量及各机构评级 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0404 | original/SKILL.md.txt:404 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | - 评级冲突（Conflicting interpretations）：详细列出各方评级差异 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0405 | original/SKILL.md.txt:405 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | - 最近审核日期（Last evaluated） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0406 | original/SKILL.md.txt:406 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | - 关联条件（Associated conditions） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0407 | original/SKILL.md.txt:407 | 1.1 ClinVar 检索（多路径并行，至少使用2条路径交叉验证） | - Review status 星级（用于评估 ClinVar 判定的可信度） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0409 | original/SKILL.md.txt:409 | 1.2 gnomAD 群体频率 | ### 1.2 gnomAD 群体频率 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0411 | original/SKILL.md.txt:411 | 1.2 gnomAD 群体频率 | **Layer 0 — Step 0.4 优先：** 若本轮已执行 Step 0.4，直接以 EV.frequency（global/eas 原始 AC/AN）+ EV.predictors | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0413 | original/SKILL.md.txt:413 | 1.2 gnomAD 群体频率 | **⚠️ gnomAD 网站为 JavaScript 重度渲染的 SPA 应用，直接 web_fetch 其 URL 几乎总是返回空壳 HTML（无实际数据）。禁止将 web_fetch g | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0415 | original/SKILL.md.txt:415 | 1.2 gnomAD 群体频率 | **Layer 1 — ClinVar 页面提取频率（最高优先级，与 1.1 同步完成）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0416 | original/SKILL.md.txt:416 | 1.2 gnomAD 群体频率 | - ClinVar 变异页面的 "Allele frequency" 或 "Population data" 部分通常汇总了 gnomAD、ExAC、ESP、TOPMed、1000 Geno | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0417 | original/SKILL.md.txt:417 | 1.2 gnomAD 群体频率 | - 若已在 Step 1.1 中成功 fetch 了 ClinVar Variation 页面，**直接从中提取频率信息** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0418 | original/SKILL.md.txt:418 | 1.2 gnomAD 群体频率 | - 这些频率数据足以进行 PM2/BA1/BS1 的初步评估 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0419 | original/SKILL.md.txt:419 | 1.2 gnomAD 群体频率 | - 这是获取频率数据成功率最高的路径（~80%），因为频率信息嵌入在 ClinVar 的静态 HTML 中 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0421 | original/SKILL.md.txt:421 | 1.2 gnomAD 群体频率 | **Layer 2 — web_search 频率查询（当 Layer 1 无频率数据时）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0422 | original/SKILL.md.txt:422 | 1.2 gnomAD 群体频率 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0423 | original/SKILL.md.txt:423 | 1.2 gnomAD 群体频率 | web_search: "gnomAD [基因名] c.[变异] allele frequency" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0424 | original/SKILL.md.txt:424 | 1.2 gnomAD 群体频率 | web_search: "[基因名] [p.变异] population frequency" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0425 | original/SKILL.md.txt:425 | 1.2 gnomAD 群体频率 | web_search: "[chr]-[pos]-[ref]-[alt] gnomAD" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0426 | original/SKILL.md.txt:426 | 1.2 gnomAD 群体频率 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0427 | original/SKILL.md.txt:427 | 1.2 gnomAD 群体频率 | - 从搜索结果摘要中提取频率值 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0428 | original/SKILL.md.txt:428 | 1.2 gnomAD 群体频率 | - VarSome、Franklin 等第三方工具的搜索结果中也常包含 gnomAD 频率 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0430 | original/SKILL.md.txt:430 | 1.2 gnomAD 群体频率 | **Layer 3 — 间接推断（最终回退，仅用于 PM2 赋值）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0431 | original/SKILL.md.txt:431 | 1.2 gnomAD 群体频率 | - 若 Layer 1-2 均未获取到精确频率值： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0432 | original/SKILL.md.txt:432 | 1.2 gnomAD 群体频率 |   - 若 ClinVar 有条目但未显示频率 → 大概率为罕见变异，可谨慎赋予 PM2_Supporting | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0433 | original/SKILL.md.txt:433 | 1.2 gnomAD 群体频率 |   - 若为 novel variant（ClinVar 无条目 + web_search 无频率记录）→ 可赋予 PM2_Supporting 并注明"基于无公共频率记录推断" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0434 | original/SKILL.md.txt:434 | 1.2 gnomAD 群体频率 | - 必须在报告中标注：gnomAD AF: 未能实时获取精确值。PM2 赋值基于[ClinVar无频率记录/公共数据库无该变异记录]推断。建议用户在 https://gnomad.broad | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0436 | original/SKILL.md.txt:436 | 1.2 gnomAD 群体频率 | **提取信息（尽可能获取，按重要性排序）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0437 | original/SKILL.md.txt:437 | 1.2 gnomAD 群体频率 | - 总体等位基因频率（Global AF）← PM2/BA1/BS1 赋值的核心依据 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0438 | original/SKILL.md.txt:438 | 1.2 gnomAD 群体频率 | - 东亚人群频率（EAS AF）← 产前场景尤其重要 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0439 | original/SKILL.md.txt:439 | 1.2 gnomAD 群体频率 | - 等位基因计数（AC）、纯合子计数、**半合子计数**（X 连锁；早发重症基因成年半合子/纯合子 ≥2 → BS2，见 ACMG_CRITERIA.md §2.3） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0440 | original/SKILL.md.txt:440 | 1.2 gnomAD 群体频率 | - Filtering AF | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0442 | original/SKILL.md.txt:442 | 1.2 gnomAD 群体频率 | **频率证据赋值规则（详见 references/ACMG_CRITERIA.md 第2节）**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0443 | original/SKILL.md.txt:443 | 1.2 gnomAD 群体频率 | - PM2 **默认降级 PM2_Supporting**（SVI 2020），除非有专病 VCEP 规则 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0444 | original/SKILL.md.txt:444 | 1.2 gnomAD 群体频率 | - BA1（>5% 任一 ≥2000 等位基因大陆人群，非豁免名单）→ 独立良性，一票否决致病证据 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0445 | original/SKILL.md.txt:445 | 1.2 gnomAD 群体频率 | - 🔑 **专病 VCEP 频率阈值优先于通用阈值**，截至 2026-08 约 138 个基因有专病规范（心血管/代谢/眼/神经肌肉/精神发育/免疫/血液/RAS 通路/溶酶体等），以 c | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0446 | original/SKILL.md.txt:446 | 1.2 gnomAD 群体频率 | - **BA1 例外（亚效等位）**：PM3 ≥ Strong + 功能示部分残余活性 + 健康纯合子存在时不启用 BA1 一票否决，输出"亚效等位/低外显致病"类别（OCA2 p.Ala4 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0447 | original/SKILL.md.txt:447 | 1.2 gnomAD 群体频率 | - BS1 阈值用 cardiodb 计算器：https://cardiodb.org/allelefrequencyapp/ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0448 | original/SKILL.md.txt:448 | 1.2 gnomAD 群体频率 | - 🤰 **高频≠良性陷阱（TBX6 范式）**：某些人群高频点为亚效单倍型，与 LOF 反式组合可致病（如 TBX6 T-C-A 单倍型 + LOF → 脊椎肋骨发育不全）。**产前检出单 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0450 | original/SKILL.md.txt:450 | 1.3 gnomAD 基因约束指标 | ### 1.3 gnomAD 基因约束指标 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0452 | original/SKILL.md.txt:452 | 1.3 gnomAD 基因约束指标 | **⚠️ 同 1.2，gnomAD 基因页面也为 SPA 渲染，web_fetch 无法获取有效数据。** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0454 | original/SKILL.md.txt:454 | 1.3 gnomAD 基因约束指标 | 优先使用 web_search 获取： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0455 | original/SKILL.md.txt:455 | 1.3 gnomAD 基因约束指标 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0456 | original/SKILL.md.txt:456 | 1.3 gnomAD 基因约束指标 | web_search: "[基因名] pLI LOEUF constraint" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0457 | original/SKILL.md.txt:457 | 1.3 gnomAD 基因约束指标 | web_search: "gnomAD [基因名] gene constraint" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0458 | original/SKILL.md.txt:458 | 1.3 gnomAD 基因约束指标 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0459 | original/SKILL.md.txt:459 | 1.3 gnomAD 基因约束指标 | - 从搜索结果摘要或第三方工具页面提取 pLI、LOEUF、mis_z 等指标 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0460 | original/SKILL.md.txt:460 | 1.3 gnomAD 基因约束指标 | - DECIPHER、OMIM、ClinGen 的基因页面中也常引用这些约束指标 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0461 | original/SKILL.md.txt:461 | 1.3 gnomAD 基因约束指标 | - 这些数据对 PVS1 强度调整和 LoF 机制评估至关重要 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0463 | original/SKILL.md.txt:463 | 1.4 OMIM 查询 | ### 1.4 OMIM 查询 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0465 | original/SKILL.md.txt:465 | 1.4 OMIM 查询 | **首选路径：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0466 | original/SKILL.md.txt:466 | 1.4 OMIM 查询 | - web_search OMIM [基因名] gene（短查询，1-3 词最佳） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0467 | original/SKILL.md.txt:467 | 1.4 OMIM 查询 | - web_fetch OMIM 基因条目页面 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0469 | original/SKILL.md.txt:469 | 1.4 OMIM 查询 | **提取：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0470 | original/SKILL.md.txt:470 | 1.4 OMIM 查询 | - 关联疾病列表、遗传方式、MIM 编号 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0471 | original/SKILL.md.txt:471 | 1.4 OMIM 查询 | - 基因-疾病关联置信度 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0472 | original/SKILL.md.txt:472 | 1.4 OMIM 查询 | - 等位基因变异表（Allelic Variants）中是否已收录该变异或同位点变异 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0474 | original/SKILL.md.txt:474 | 1.5 ClinGen 基因级别资源（新增） | ### 1.5 ClinGen 基因级别资源（新增） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0476 | original/SKILL.md.txt:476 | 1.5 ClinGen 基因级别资源（新增） | - web_search ClinGen [基因名] gene validity 或 ClinGen [基因名] dosage sensitivity | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0477 | original/SKILL.md.txt:477 | 1.5 ClinGen 基因级别资源（新增） | - 提取： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0478 | original/SKILL.md.txt:478 | 1.5 ClinGen 基因级别资源（新增） |   - 基因-疾病有效性分级（Definitive / Strong / Moderate / Limited / Disputed） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0479 | original/SKILL.md.txt:479 | 1.5 ClinGen 基因级别资源（新增） |   - 剂量敏感性评分（Haploinsufficiency score, Triplosensitivity score） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0480 | original/SKILL.md.txt:480 | 1.5 ClinGen 基因级别资源（新增） |   - 是否有基因特异性 ACMG 规则（Gene-Specific VCEP rules，见 Step 4A） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0482 | original/SKILL.md.txt:482 | 1.6 检索策略总则 | ### 1.6 检索策略总则 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0484 | original/SKILL.md.txt:484 | 1.6 检索策略总则 | **查询构造原则：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0485 | original/SKILL.md.txt:485 | 1.6 检索策略总则 | - 保持查询简短（1-4 词最佳，不超过 6 词），避免过长查询降低召回率 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0486 | original/SKILL.md.txt:486 | 1.6 检索策略总则 | - 优先使用 HGVS cDNA 命名检索，蛋白命名作为补充 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0487 | original/SKILL.md.txt:487 | 1.6 检索策略总则 | - 若首次查询无结果，尝试替换命名格式（如 c. 命名 ↔ p. 命名 ↔ 基因组坐标） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0488 | original/SKILL.md.txt:488 | 1.6 检索策略总则 | - 不使用引号、site: 操作符或 - 排除符 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0490 | original/SKILL.md.txt:490 | 1.6 检索策略总则 | **web_fetch 使用原则（重要）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0491 | original/SKILL.md.txt:491 | 1.6 检索策略总则 | - ⚠️ **禁止盲目 fetch 动态数据库 URL**：gnomAD、Franklin、UCSC Genome Browser 等 SPA 应用直接 fetch 几乎总是返回空壳 HTM | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0492 | original/SKILL.md.txt:492 | 1.6 检索策略总则 | - ✅ **适合 fetch 的目标**：NCBI/ClinVar 的 Variation 页面（静态渲染）、PubMed 文献页面、OMIM 条目、UniProt 条目、ClinGen 页 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0493 | original/SKILL.md.txt:493 | 1.6 检索策略总则 | - ✅ **始终先 web_search 获取具体 URL，再对有效 URL 执行 web_fetch**，而非盲目构造 URL | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0495 | original/SKILL.md.txt:495 | 1.6 检索策略总则 | **检索效率（并行策略）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0496 | original/SKILL.md.txt:496 | 1.6 检索策略总则 | - 第一轮并行：同时发起 ClinVar（cDNA查询）+ OMIM + ClinGen 的 web_search（3条查询） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0497 | original/SKILL.md.txt:497 | 1.6 检索策略总则 | - 第二轮并行：基于第一轮结果，发起 gnomAD 频率查询 + 功能预测查询 + 文献查询 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0498 | original/SKILL.md.txt:498 | 1.6 检索策略总则 | - 若第一轮 ClinVar 已命中并获取到 Variation 页面 URL，第二轮优先 fetch 该页面（可同时获取频率数据） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0500 | original/SKILL.md.txt:500 | 1.6 检索策略总则 | **数据源可靠性排名（基于实际 web_search/web_fetch 成功率）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0501 | original/SKILL.md.txt:501 | 1.6 检索策略总则 | \| 数据源 \| web_search 成功率 \| web_fetch 成功率 \| 建议策略 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0502 | original/SKILL.md.txt:502 | 1.6 检索策略总则 | \|--------\|-------------------\|------------------\|----------\| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0503 | original/SKILL.md.txt:503 | 1.6 检索策略总则 | \| ClinVar (NCBI) \| ~90% \| ~70%（Variation页面） \| search → fetch 组合 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0504 | original/SKILL.md.txt:504 | 1.6 检索策略总则 | \| OMIM \| ~85% \| ~65% \| search → fetch 组合 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0505 | original/SKILL.md.txt:505 | 1.6 检索策略总则 | \| ClinGen \| ~80% \| ~60% \| search 为主 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0506 | original/SKILL.md.txt:506 | 1.6 检索策略总则 | \| PubMed \| ~90% \| ~75% \| search → fetch 组合 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0507 | original/SKILL.md.txt:507 | 1.6 检索策略总则 | \| UniProt \| ~85% \| ~70% \| search → fetch 组合 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0508 | original/SKILL.md.txt:508 | 1.6 检索策略总则 | \| VarSome \| ~75% \| ~60% \| search → 尝试 fetch \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0509 | original/SKILL.md.txt:509 | 1.6 检索策略总则 | \| gnomAD \| ~70%（摘要含频率） \| ~10%（SPA） \| search 为主，ClinVar 补充 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0510 | original/SKILL.md.txt:510 | 1.6 检索策略总则 | \| Franklin \| ~50%（摘要含分类） \| ~10%（需登录） \| search 摘要为主 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0512 | original/SKILL.md.txt:512 | 1.7 检索状态记录 | ### 1.7 检索状态记录 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0514 | original/SKILL.md.txt:514 | 1.7 检索状态记录 | 对每项检索，明确记录状态： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0515 | original/SKILL.md.txt:515 | 1.7 检索状态记录 | - ✅ 成功获取（附数据来源 URL） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0516 | original/SKILL.md.txt:516 | 1.7 检索状态记录 | - ⚠️ 部分获取（说明缺失内容及可能的补充途径） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0517 | original/SKILL.md.txt:517 | 1.7 检索状态记录 | - ❌ 未能获取（提供用户自行查询的数据库链接及建议查询方式） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0519 | original/SKILL.md.txt:519 | 1.7 检索状态记录 | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0521 | original/SKILL.md.txt:521 | Step 2：分子定位与转录本核实（Molecular Mapping） | ## Step 2：分子定位与转录本核实（Molecular Mapping） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0523 | original/SKILL.md.txt:523 | 2.1 定位信息确认 | ### 2.1 定位信息确认 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0524 | original/SKILL.md.txt:524 | 2.1 定位信息确认 | - Chromosome & genomic coordinate (GRCh38) | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0525 | original/SKILL.md.txt:525 | 2.1 定位信息确认 | - Exon / Intron number | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0526 | original/SKILL.md.txt:526 | 2.1 定位信息确认 | - Variant type: missense / nonsense / frameshift / splice site / in-frame indel / synonymous /  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0527 | original/SKILL.md.txt:527 | 2.1 定位信息确认 | - VCF format: chr-pos-ref-alt | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0529 | original/SKILL.md.txt:529 | 2.2 转录本二次核实 | ### 2.2 转录本二次核实 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0530 | original/SKILL.md.txt:530 | 2.2 转录本二次核实 | - 确认 Step 0 中标准化的转录本是否为 MANE Select | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0531 | original/SKILL.md.txt:531 | 2.2 转录本二次核实 | - 核对 cDNA 编号在该转录本中的正确性（外显子编号、CDS 位置） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0532 | original/SKILL.md.txt:532 | 2.2 转录本二次核实 | - 若用户提供的转录本不是 MANE Select，输出命名对照表： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0534 | original/SKILL.md.txt:534 | 2.2 转录本二次核实 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0535 | original/SKILL.md.txt:535 | 2.2 转录本二次核实 | 用户转录本:  NM_xxxxxx.x → c.XXX / p.XXX | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0536 | original/SKILL.md.txt:536 | 2.2 转录本二次核实 | MANE Select: NM_yyyyyy.y → c.YYY / p.YYY | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0537 | original/SKILL.md.txt:537 | 2.2 转录本二次核实 | ⚠️ 注意：后续分析基于 MANE Select 转录本 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0538 | original/SKILL.md.txt:538 | 2.2 转录本二次核实 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0540 | original/SKILL.md.txt:540 | 2.2 转录本二次核实 | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0542 | original/SKILL.md.txt:542 | Step 3：外部分类对标（External Benchmarking） | ## Step 3：外部分类对标（External Benchmarking） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0544 | original/SKILL.md.txt:544 | 3.1 Franklin/Genoox 检索 | ### 3.1 Franklin/Genoox 检索 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0546 | original/SKILL.md.txt:546 | 3.1 Franklin/Genoox 检索 | **⚠️ 实际可用性说明：Franklin 网站需要登录认证，且为 SPA 应用，web_fetch 直接访问 Franklin URL 几乎总是失败（返回登录页或空壳 HTML）。以下策略 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0548 | original/SKILL.md.txt:548 | 3.1 Franklin/Genoox 检索 | **策略A — web_search 摘要提取（首选，成功率最高）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0549 | original/SKILL.md.txt:549 | 3.1 Franklin/Genoox 检索 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0550 | original/SKILL.md.txt:550 | 3.1 Franklin/Genoox 检索 | web_search: "Franklin [基因名] c.[变异] classification" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0551 | original/SKILL.md.txt:551 | 3.1 Franklin/Genoox 检索 | web_search: "Franklin [基因名] p.[变异] ACMG" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0552 | original/SKILL.md.txt:552 | 3.1 Franklin/Genoox 检索 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0553 | original/SKILL.md.txt:553 | 3.1 Franklin/Genoox 检索 | - Franklin 的变异页面标题和 meta 描述中通常包含分类结果（如 "Likely Pathogenic"），web_search 摘要即可获取核心信息 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0554 | original/SKILL.md.txt:554 | 3.1 Franklin/Genoox 检索 | - 若搜索结果中出现 Franklin 页面链接，可尝试 web_fetch，但预期成功率低（~20%） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0556 | original/SKILL.md.txt:556 | 3.1 Franklin/Genoox 检索 | **策略B — 用 VarSome 替代对标（推荐）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0558 | original/SKILL.md.txt:558 | 3.1 Franklin/Genoox 检索 | VarSome 的公开变异页面对 web_fetch 友好度显著高于 Franklin： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0559 | original/SKILL.md.txt:559 | 3.1 Franklin/Genoox 检索 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0560 | original/SKILL.md.txt:560 | 3.1 Franklin/Genoox 检索 | web_search: "VarSome [基因名] c.[变异]" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0561 | original/SKILL.md.txt:561 | 3.1 Franklin/Genoox 检索 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0562 | original/SKILL.md.txt:562 | 3.1 Franklin/Genoox 检索 | - 从搜索结果获取 VarSome 页面 URL | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0563 | original/SKILL.md.txt:563 | 3.1 Franklin/Genoox 检索 | - web_fetch VarSome 变异页面 → 成功率约 60-70% | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0564 | original/SKILL.md.txt:564 | 3.1 Franklin/Genoox 检索 | - VarSome 提供完整的 ACMG 自动分类和证据代码列表，对标价值与 Franklin 等同 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0566 | original/SKILL.md.txt:566 | 3.1 Franklin/Genoox 检索 | **策略C — InterVar 作为补充（当 A+B 均受限时）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0567 | original/SKILL.md.txt:567 | 3.1 Franklin/Genoox 检索 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0568 | original/SKILL.md.txt:568 | 3.1 Franklin/Genoox 检索 | web_search: "InterVar [基因名] c.[变异] classification" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0569 | original/SKILL.md.txt:569 | 3.1 Franklin/Genoox 检索 | web_search: "[基因名] c.[变异] ACMG automated classification" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0570 | original/SKILL.md.txt:570 | 3.1 Franklin/Genoox 检索 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0572 | original/SKILL.md.txt:572 | 3.1 Franklin/Genoox 检索 | **对标数据来源优先级**（基于实际可获取性排序）： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0573 | original/SKILL.md.txt:573 | 3.1 Franklin/Genoox 检索 | 1. VarSome（公开页面，web_fetch 友好） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0574 | original/SKILL.md.txt:574 | 3.1 Franklin/Genoox 检索 | 2. Franklin（搜索摘要可获取分类，完整页面需登录） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0575 | original/SKILL.md.txt:575 | 3.1 Franklin/Genoox 检索 | 3. InterVar（补充参考） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0577 | original/SKILL.md.txt:577 | 3.2 对标分析原则 | ### 3.2 对标分析原则 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0578 | original/SKILL.md.txt:578 | 3.2 对标分析原则 | 对标目的不是照搬外部结果，而是识别分析逻辑的差异并解释原因。当自身判定与外部工具不一致时，需逐条对比证据代码差异，分析哪方的证据赋值更合理。若所有外部对标工具均无法获取结果，在模块5中注明并 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0580 | original/SKILL.md.txt:580 | 3.2 对标分析原则 | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0582 | original/SKILL.md.txt:582 | Step 4：功能预测与 LoF 评估（Functional Prediction） | ## Step 4：功能预测与 LoF 评估（Functional Prediction） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0584 | original/SKILL.md.txt:584 | 4.1 计算预测评分 | ### 4.1 计算预测评分 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0586 | original/SKILL.md.txt:586 | 4.1 计算预测评分 | **评分获取策略**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0588 | original/SKILL.md.txt:588 | 4.1 计算预测评分 | 预测评分不是独立数据库，通常嵌入在其他工具/页面中。以下是按获取可靠性排序的来源： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0590 | original/SKILL.md.txt:590 | 4.1 计算预测评分 | **Layer 0 — GeneBe 浏览器取数链（首选，当环境有 Claude in Chrome 浏览器工具时）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0592 | original/SKILL.md.txt:592 | 4.1 计算预测评分 | 这是当前最可靠、覆盖最全的逐项评分来源（实测：免登录、不冻结、基于 dbNSFP 预计算覆盖任意错义变异）。两种调用方式： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0593 | original/SKILL.md.txt:593 | 4.1 计算预测评分 | - **优先调用 variant-insilico-scores 技能**（若已安装）：把本例在 Step 2 解析出的基因组坐标 chr{N}-{pos}-{ref}-{alt} 喂给它， | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0594 | original/SKILL.md.txt:594 | 4.1 计算预测评分 | - **或直接操作 GeneBe**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0595 | original/SKILL.md.txt:595 | 4.1 计算预测评分 |   1. list_connected_browsers 确认有浏览器 → tabs_context_mcp 取 tabId； | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0596 | original/SKILL.md.txt:596 | 4.1 计算预测评分 |   2. navigate 到 https://genebe.net/variant/{hg19\|hg38}/{chr}-{pos}-{ref}-{alt}（chr 号不带 "chr"；b | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0597 | original/SKILL.md.txt:597 | 4.1 计算预测评分 |   3. get_page_text，从 "Computational scores（Source: dbNSFP v4.x）" 表读取各项分数（NAME / 校准方向 / SCORE）。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0598 | original/SKILL.md.txt:598 | 4.1 计算预测评分 | - 坐标复用：若同一流程里已先跑 franklin-variant-lookup，它解析出的 chr-pos-ref-alt（hg19）可直接复用，无需再解析。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0599 | original/SKILL.md.txt:599 | 4.1 计算预测评分 | - ⚠️ 仅适用于错义/可被 dbNSFP 覆盖的变异；剪接分项需到 spliceailookup.broadinstitute.org；移码/无义类多数预测器不适用。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0601 | original/SKILL.md.txt:601 | 4.1 计算预测评分 | **Layer 1 — 无浏览器时的回退（web_search/web_fetch）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0603 | original/SKILL.md.txt:603 | 4.1 计算预测评分 | 1. **ClinVar 变异页面**：部分 ClinVar 条目的 "Clinical significance" 提交详情中引用了预测评分 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0604 | original/SKILL.md.txt:604 | 4.1 计算预测评分 | 2. **web_search 直接查询**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0605 | original/SKILL.md.txt:605 | 4.1 计算预测评分 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0606 | original/SKILL.md.txt:606 | 4.1 计算预测评分 | web_search: "[基因名] [p.变异] REVEL score" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0607 | original/SKILL.md.txt:607 | 4.1 计算预测评分 | web_search: "[基因名] c.[变异] CADD SpliceAI prediction" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0608 | original/SKILL.md.txt:608 | 4.1 计算预测评分 | web_search: "REVEL [基因名] [氨基酸位置]" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0609 | original/SKILL.md.txt:609 | 4.1 计算预测评分 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0610 | original/SKILL.md.txt:610 | 4.1 计算预测评分 | 3. **Franklin 搜索摘要**：Franklin 页面标题/描述中有时包含评分信息 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0612 | original/SKILL.md.txt:612 | 4.1 计算预测评分 | > ⚠️ **VarSome 已不再作为推荐取数源**：其变异页被 reCAPTCHA "Security validation" 闸门拦截（人机验证，禁止绕过），浏览器自动化无法稳定访问。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0614 | original/SKILL.md.txt:614 | 4.1 计算预测评分 | ⚠️ **若 REVEL 评分无法获取**（对于错义变异）：先确认是否已尝试 Layer 0 的 GeneBe 取数链（有浏览器时几乎总能拿到 REVEL）。仅当 GeneBe 与所有回退均 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0616 | original/SKILL.md.txt:616 | 4.1 计算预测评分 | **评分判定阈值**（基于 ClinGen 推荐）： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0618 | original/SKILL.md.txt:618 | 4.1 计算预测评分 | **REVEL 评分**（错义变异首选）——阈值出自 **Pejaver 2022, Am J Hum Genet 109:2163-2177, PMID 36413997, Table 2 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0620 | original/SKILL.md.txt:620 | 4.1 计算预测评分 | \| REVEL 区间 \| 证据强度 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0621 | original/SKILL.md.txt:621 | 4.1 计算预测评分 | \|---\|---\| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0622 | original/SKILL.md.txt:622 | 4.1 计算预测评分 | \| ≥0.932 \| **PP3_Strong** \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0623 | original/SKILL.md.txt:623 | 4.1 计算预测评分 | \| [0.773, 0.932) \| PP3_Moderate \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0624 | original/SKILL.md.txt:624 | 4.1 计算预测评分 | \| [0.644, 0.773) \| PP3_Supporting \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0625 | original/SKILL.md.txt:625 | 4.1 计算预测评分 | \| (0.290, 0.644) \| **灰区 —— PP3/BP4 均不赋** \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0626 | original/SKILL.md.txt:626 | 4.1 计算预测评分 | \| (0.183, 0.290] \| BP4_Supporting \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0627 | original/SKILL.md.txt:627 | 4.1 计算预测评分 | \| (0.016, 0.183] \| BP4_Moderate \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0628 | original/SKILL.md.txt:628 | 4.1 计算预测评分 | \| (0.003, 0.016] \| BP4_Strong \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0629 | original/SKILL.md.txt:629 | 4.1 计算预测评分 | \| ≤0.003 \| BP4_VeryStrong \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0631 | original/SKILL.md.txt:631 | 4.1 计算预测评分 | - PP3 与 BP4 互斥 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0632 | original/SKILL.md.txt:632 | 4.1 计算预测评分 | - ⚠️ **良性侧阈值远比直觉严格**：REVEL 0.3–0.6 属灰区，**不是** BP4 证据。曾有版本误写为「≤0.564→Supporting / ≤0.397→Moderat | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0633 | original/SKILL.md.txt:633 | 4.1 计算预测评分 | - 注：REVEL 在原文中**不设 PP3_VeryStrong 档**，致病侧最高为 Strong。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0635 | original/SKILL.md.txt:635 | 4.1 计算预测评分 | **SpliceAI 评分**（剪接变异，Walker 2023 SVI 校准 PMID:37352859；2026-09 更正旧版"强/中/弱支持"四档写法）： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0636 | original/SKILL.md.txt:636 | 4.1 计算预测评分 | - Δscore ≥0.2 → **PP3（Supporting，不升级）** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0637 | original/SKILL.md.txt:637 | 4.1 计算预测评分 | - Δscore ≤0.1 → **BP4（Supporting）**；剪接区域外（+7/−21 之外）的同义/内含子变异可再叠 BP7 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0638 | original/SKILL.md.txt:638 | 4.1 计算预测评分 | - 0.1 < Δscore < 0.2 → **灰区，不作剪接结论**，改按蛋白层面预测处理 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0639 | original/SKILL.md.txt:639 | 4.1 计算预测评分 | - ≥0.8 仅用于 +2T>C 例外判断与 RNA 验证优先级，**不抬高 PP3 强度**；剪接预测升级只能靠 RNA 证据走 PVS1(RNA)/BP7(RNA) | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0640 | original/SKILL.md.txt:640 | 4.1 计算预测评分 | - PP3 对同一变异只用一次（剪接预测与错义预测取其一） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0641 | original/SKILL.md.txt:641 | 4.1 计算预测评分 | - 详见 references/ACMG_CRITERIA.md §1.8 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0643 | original/SKILL.md.txt:643 | 4.1 计算预测评分 | 辅助参考（非直接用于 ACMG 证据代码赋值，仅作辅助）： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0644 | original/SKILL.md.txt:644 | 4.1 计算预测评分 | - CADD：**不单独赋证据**；20 分落在 Pejaver 2022 校准的无证据区（PP3_Supporting 起点约 25.3，BP4_Supporting 上限约 22.7）， | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0645 | original/SKILL.md.txt:645 | 4.1 计算预测评分 | - AlphaMissense：仅作与 REVEL 的一致性核对，不叠加、不投票；方向相反时模块 6 讨论并倾向保守 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0646 | original/SKILL.md.txt:646 | 4.1 计算预测评分 | - 蛋白保守性（PhyloP, GERP++） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0648 | original/SKILL.md.txt:648 | 4.1b PS3/BS3 功能证据质量门槛（详见 references/ACMG_CRITERIA.md 第3节） | ### 4.1b PS3/BS3 功能证据质量门槛（详见 references/ACMG_CRITERIA.md 第3节） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0650 | original/SKILL.md.txt:650 | 4.1b PS3/BS3 功能证据质量门槛（详见 references/ACMG_CRITERIA.md 第3节） | 赋 PS3/BS3 前核对以下门槛（吴家裕共识）： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0651 | original/SKILL.md.txt:651 | 4.1b PS3/BS3 功能证据质量门槛（详见 references/ACMG_CRITERIA.md 第3节） | - **强度需 OddsPath 量化**：设阴/阳性对照；"中等"强度需 **≥11 个对照变异**；变异敲入动物模型重现症状 → PS3 强证据 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0652 | original/SKILL.md.txt:652 | 4.1b PS3/BS3 功能证据质量门槛（详见 references/ACMG_CRITERIA.md 第3节） | - ⛔ **仅 RNA 剪接改变实验不用 PS3/BS3** → 用 PVS1_Strength(RNA)/BP7_Strong(RNA) | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0653 | original/SKILL.md.txt:653 | 4.1b PS3/BS3 功能证据质量门槛（详见 references/ACMG_CRITERIA.md 第3节） | - ⛔ 仅蛋白三维模型、仅表达量检测不用 PS3；✅ 免疫荧光功能相关定位异常 → PS3_Supporting | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0654 | original/SKILL.md.txt:654 | 4.1b PS3/BS3 功能证据质量门槛（详见 references/ACMG_CRITERIA.md 第3节） | - **PS3 可与 PP3 共用**（功能 vs 进化预测，独立）；⛔ **PS3 不与 PM1 共用**（PM1 本质是功能预测） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0655 | original/SKILL.md.txt:655 | 4.1b PS3/BS3 功能证据质量门槛（详见 references/ACMG_CRITERIA.md 第3节） | - 多实验**不累加**：一致取验证最明确者；矛盾时机制最相关且验证最充分者可推翻，同级矛盾均不采纳 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0656 | original/SKILL.md.txt:656 | 4.1b PS3/BS3 功能证据质量门槛（详见 references/ACMG_CRITERIA.md 第3节） | - **BS3 谨慎**：单实验"正常"可能漏检特定功能效应 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0657 | original/SKILL.md.txt:657 | 4.1b PS3/BS3 功能证据质量门槛（详见 references/ACMG_CRITERIA.md 第3节） | - 数据来源：MaveDB (https://www.mavedb.org/)、基因专属库、文献、VCEP 标准 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0659 | original/SKILL.md.txt:659 | 4.2 PVS1 四级决策树与 LoF 机制评估 | ### 4.2 PVS1 四级决策树与 LoF 机制评估 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0661 | original/SKILL.md.txt:661 | 4.2 PVS1 四级决策树与 LoF 机制评估 | **⚠️ PVS1 是最易误用的证据，赋值前必须阅读 references/ACMG_CRITERIA.md 第1节完整决策树。** 以下为操作摘要。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0663 | original/SKILL.md.txt:663 | 4.2 PVS1 四级决策树与 LoF 机制评估 | **三个前提门槛（缺一不可）**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0664 | original/SKILL.md.txt:664 | 4.2 PVS1 四级决策树与 LoF 机制评估 | 1. 疾病机制确为 LOF（见下方判定法） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0665 | original/SKILL.md.txt:665 | 4.2 PVS1 四级决策树与 LoF 机制评估 | 2. 变异确为 null 型（无义/移码/经典±1,2剪接/起始密码子/单多外显子缺失或基因内重复/终止密码子丢失） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0666 | original/SKILL.md.txt:666 | 4.2 PVS1 四级决策树与 LoF 机制评估 | 3. 变异落在临床相关转录本（MANE Select 优先）的组成型外显子——须确认该外显子无可变剪接跳跃、在受累组织高表达（查 GTEx） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0668 | original/SKILL.md.txt:668 | 4.2 PVS1 四级决策树与 LoF 机制评估 | **LOF 机制判定（数据库 > 预测值）**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0669 | original/SKILL.md.txt:669 | 4.2 PVS1 四级决策树与 LoF 机制评估 | 1. **ClinGen Gene-Disease Validity** = Definitive/Strong（https://search.clinicalgenome.org/kb/g | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0670 | original/SKILL.md.txt:670 | 4.2 PVS1 四级决策树与 LoF 机制评估 | 2. **ClinGen Dosage HI Score**：HI=3 → LOF 致病机制确立；HI=30 → AR 相关多为 LOF；HI=40 → 剂量不敏感不致病（https://s | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0671 | original/SKILL.md.txt:671 | 4.2 PVS1 四级决策树与 LoF 机制评估 | 3. 预测值仅辅助：pLI≥0.9、LOEUF<0.6、pHaplo≥0.86。⚠️ **不可单独定机制**——BRCA1 明确单倍剂量不足(HI=3)但 pLI=0、LOEUF=0.73。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0672 | original/SKILL.md.txt:672 | 4.2 PVS1 四级决策树与 LoF 机制评估 | 4. ⚠️ **一基因多机制**：同基因不同遗传模式机制可相反（LZTR1：AD-NS10 为 GOF，AR-NS2 为 LOF）。判机制前先锁定本例对应的具体疾病/遗传模式。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0674 | original/SKILL.md.txt:674 | 4.2 PVS1 四级决策树与 LoF 机制评估 | **PVS1 强度四级（NMD 决策）**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0676 | original/SKILL.md.txt:676 | 4.2 PVS1 四级决策树与 LoF 机制评估 | \| PTC 位置 \| NMD \| PVS1 强度 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0677 | original/SKILL.md.txt:677 | 4.2 PVS1 四级决策树与 LoF 机制评估 | \|---------\|-----\|----------\| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0678 | original/SKILL.md.txt:678 | 4.2 PVS1 四级决策树与 LoF 机制评估 | \| 靠前/中间外显子 \| 是 \| **PVS1 原级 (Very Strong)** \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0679 | original/SKILL.md.txt:679 | 4.2 PVS1 四级决策树与 LoF 机制评估 | \| 最后一个外显子 \| 否（逃逸） \| 降级 Strong/Moderate（取决于截断区重要性） \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0680 | original/SKILL.md.txt:680 | 4.2 PVS1 四级决策树与 LoF 机制评估 | \| 倒数第二外显子末 50bp 内 \| 否（逃逸） \| 降级 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0681 | original/SKILL.md.txt:681 | 4.2 PVS1 四级决策树与 LoF 机制评估 | \| 距起始 <100bp \| 常逃逸 \| 慎用/降级（可用下游 AUG 重启） \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0683 | original/SKILL.md.txt:683 | 4.2 PVS1 四级决策树与 LoF 机制评估 | NMD 逃逸时须判截断区重要性（关键功能域/下游致病变异/可变剪接/**VCEP 特定规则**，如 PTEN p.D375 前用 PVS1、FOXN1 forkhead 域、GJB2 双外显 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0685 | original/SKILL.md.txt:685 | 4.2 PVS1 四级决策树与 LoF 机制评估 | **特例**：起始密码子丢失通用框架上限 **PVS1_Moderate**（Met1～下游首个框内 Met 区间有 P/LP）否则 PVS1_Supporting，有次要替代转录本时降档而 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0687 | original/SKILL.md.txt:687 | 4.2 PVS1 四级决策树与 LoF 机制评估 | **剪接变异（2023 SVI 重大更新，PMID:37352859）**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0688 | original/SKILL.md.txt:688 | 4.2 PVS1 四级决策树与 LoF 机制评估 | - 实验证实异常剪接（LOF）→ **PVS1_Strength(RNA)，取代 PS3** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0689 | original/SKILL.md.txt:689 | 4.2 PVS1 四级决策树与 LoF 机制评估 | - 实验证实不影响 → **BP7_Strong(RNA)，取代 BS3** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0690 | original/SKILL.md.txt:690 | 4.2 PVS1 四级决策树与 LoF 机制评估 | - 框内 RNA 跳跃涵盖无争议关键残基 → PVS1 升 Very Strong | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0691 | original/SKILL.md.txt:691 | 4.2 PVS1 四级决策树与 LoF 机制评估 | - ⛔ RNA 证实为**框内插入**（新生受体/供体、小片段内含子保留）且无蛋白功能数据 → 记录不计分，**不得套 H 分支**（H 的前提是去除序列）；补蛋白功能实验后另计 PS3（见 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0692 | original/SKILL.md.txt:692 | 4.2 PVS1 四级决策树与 LoF 机制评估 | - 无 RNA 证据：非经典剪接位点不用 PVS1；+2T>C 且 SpliceAI<0.8 不用 PVS1 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0693 | original/SKILL.md.txt:693 | 4.2 PVS1 四级决策树与 LoF 机制评估 | - 🤰 **产前关键决策点可用引产前胎儿脐血 RNA 验证升级 PVS1**（TET3 范式） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0695 | original/SKILL.md.txt:695 | 4.2 PVS1 四级决策树与 LoF 机制评估 | 参考工具：AutoPVS1 https://autopvs1.bgi.com/ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0697 | original/SKILL.md.txt:697 | 4.2 PVS1 四级决策树与 LoF 机制评估 | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0699 | original/SKILL.md.txt:699 | Step 4A：ClinGen 基因特异性 ACMG 规则适配（Gene-Specific Rules） | ## Step 4A：ClinGen 基因特异性 ACMG 规则适配（Gene-Specific Rules） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0701 | original/SKILL.md.txt:701 | Step 4A：ClinGen 基因特异性 ACMG 规则适配（Gene-Specific Rules） | ClinGen 的各 Variant Curation Expert Panel (VCEP) 已为部分基因/疾病发布了定制化的 ACMG/AMP 标准（Criteria Specifica | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0703 | original/SKILL.md.txt:703 | Step 4A：ClinGen 基因特异性 ACMG 规则适配（Gene-Specific Rules） | > ⚠️ **本步骤的最高原则（不可妥协）**：对有 VCEP 规范的基因，**仅"知道该基因有 VCEP 规则"是不够的——必须取得规范全文并完整阅读后，才能据其赋分**。凭记忆、凭检索摘 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0705 | original/SKILL.md.txt:705 | 4A.1 检测是否存在 VCEP 规范 | ### 4A.1 检测是否存在 VCEP 规范 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0707 | original/SKILL.md.txt:707 | 4A.1 检测是否存在 VCEP 规范 | Step 1.5 已初步检索 ClinGen 资源。此处进一步确认该基因是否有"已发布或处于公开草案阶段"的 VCEP Criteria Specification： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0709 | original/SKILL.md.txt:709 | 4A.1 检测是否存在 VCEP 规范 | 1. web_search ClinGen [基因名] variant curation expert panel | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0710 | original/SKILL.md.txt:710 | 4A.1 检测是否存在 VCEP 规范 | 2. web_search [基因名] VCEP ACMG specification | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0711 | original/SKILL.md.txt:711 | 4A.1 检测是否存在 VCEP 规范 | 3. web_search cspec [基因名] criteria specification | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0712 | original/SKILL.md.txt:712 | 4A.1 检测是否存在 VCEP 规范 | 4. web_search [基因名] ClinGen specification Genet Med（许多 VCEP 规范以同行评议论文形式发表于 Genet Med / Hum Muta | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0714 | original/SKILL.md.txt:714 | 4A.1 检测是否存在 VCEP 规范 | **检测结果分三种情况，分别进入不同流程：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0716 | original/SKILL.md.txt:716 | 4A.1 检测是否存在 VCEP 规范 | \| 情况 \| 判定 \| 去向 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0717 | original/SKILL.md.txt:717 | 4A.1 检测是否存在 VCEP 规范 | \|------\|------\|------\| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0718 | original/SKILL.md.txt:718 | 4A.1 检测是否存在 VCEP 规范 | \| **A** \| 检测到该基因有 VCEP 规范 \| → **4A.2 全文强制获取门控** \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0719 | original/SKILL.md.txt:719 | 4A.1 检测是否存在 VCEP 规范 | \| **B** \| 充分检索后确认该基因**确无** VCEP 规范 \| → 4A.4（用通用标准并注明） \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0720 | original/SKILL.md.txt:720 | 4A.1 检测是否存在 VCEP 规范 | \| **C** \| 检索结果模糊、不确定是否有规范 \| → 视同情况 A 尝试全文获取；若最终查无全文，按 4A.3-B 回退并注明"未能确认是否存在 VCEP 规范" \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0722 | original/SKILL.md.txt:722 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | ### 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0724 | original/SKILL.md.txt:724 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | 一旦 4A.1 判定为情况 A 或 C，**必须按以下分层策略尝试取得规范全文并完整阅读**，不可仅凭检索摘要中的零星阈值就赋分。各层按全文可获取性排序，依次尝试。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0726 | original/SKILL.md.txt:726 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | **Layer 0 — 用户已上传的 VCEP 文档（最高优先级）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0727 | original/SKILL.md.txt:727 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | - 若用户在本轮或此前已上传该基因的 VCEP 规范文件（PDF/Word/文本），**一律以上传文件为准**，完整阅读后据其赋分（流程见 4A.5）。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0728 | original/SKILL.md.txt:728 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | - 上传文件优先于一切在线来源，因为它就是用户期望据以评级的权威版本。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0730 | original/SKILL.md.txt:730 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | **Layer 1 — VCEP 规范发表论文全文（最可靠的在线全文来源）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0731 | original/SKILL.md.txt:731 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | - 多数 VCEP 规范以论文形式发表，PMC 常有开放获取全文，且对抓取友好。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0732 | original/SKILL.md.txt:732 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | - 若环境中已连接 **PubMed 工具**，优先调用 PubMed:search_articles（查 [基因名] VCEP ACMG specification）定位 PMID，再用  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0733 | original/SKILL.md.txt:733 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | - 无 PubMed 工具时：web_search 定位 PMID/PMC 链接 → web_fetch PMC 全文页面（ncbi.nlm.nih.gov/pmc/articles/PMC | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0734 | original/SKILL.md.txt:734 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | - ⚠️ 论文正文常只给规则框架，**精确阈值多在补充材料（Supplementary）/附表**中——须确认这些附表内容也已读到，否则视为未完整获取。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0736 | original/SKILL.md.txt:736 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | **Layer 2 — cspec 平台规范文档（规范的权威原始来源）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0737 | original/SKILL.md.txt:737 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | - cspec 平台地址 https://cspec.genome.network/cspec/ui/svi/，但它是 JavaScript 重度渲染的 SPA，直接 web_fetch 该 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0738 | original/SKILL.md.txt:738 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | - 正确做法：web_search cspec [基因名] specification pdf 或 [基因名] criteria specification clingen pdf，从结果中 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0739 | original/SKILL.md.txt:739 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | - cspec 上每个规范有版本号（如 Version 2）与生效日期，务必记录。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0741 | original/SKILL.md.txt:741 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | **Layer 3 — ClinGen 官方 PDF / 附件 / 工作组页面：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0742 | original/SKILL.md.txt:742 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | - web_search [基因名] ClinGen rule specifications summary，定位 ClinGen 工作组页面或其挂载的 specification PDF/ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0744 | original/SKILL.md.txt:744 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | **门控通过标准（须同时满足）：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0745 | original/SKILL.md.txt:745 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | - ✅ 已取得规范**正文内容**（而非仅摘要、标题、版本号或新闻稿） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0746 | original/SKILL.md.txt:746 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | - ✅ 已逐条读到本例实际需要赋值的证据代码的 VCEP 定制定义（例如本例为错义变异，至少须读到 PM2/PP3/BP4/PM1/PS1/PM5 的 VCEP 定义；若用到 PVS1/PS | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0747 | original/SKILL.md.txt:747 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | - ✅ 已确认规范的**版本号与发布/生效日期** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0749 | original/SKILL.md.txt:749 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | **门控判定：** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0750 | original/SKILL.md.txt:750 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | - **通过 → 进入 4A.3-A（按 VCEP 全文赋分）** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0751 | original/SKILL.md.txt:751 | 4A.2 ⚠️ VCEP 规范全文强制获取门控（MANDATORY — 软门控） | - **未通过 → 进入 4A.3-B（诚实回退 + 用户上传请求）** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0753 | original/SKILL.md.txt:753 | 4A.3-A：按 VCEP 全文赋分（门控通过） | ### 4A.3-A：按 VCEP 全文赋分（门控通过） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0755 | original/SKILL.md.txt:755 | 4A.3-A：按 VCEP 全文赋分（门控通过） | - 在报告中明确声明使用了基因特异性标准，引用 VCEP 规范名称、**版本号、发布日期及来源（PMID/cspec URL）**。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0756 | original/SKILL.md.txt:756 | 4A.3-A：按 VCEP 全文赋分（门控通过） | - 严格按 VCEP 全文中的定制阈值和规则执行证据赋值；在模块3每条受 VCEP 影响的代码后标注 [VCEP]。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0757 | original/SKILL.md.txt:757 | 4A.3-A：按 VCEP 全文赋分（门控通过） | - 典型的 VCEP 定制内容（须逐项核对全文中是否对其有定制，而非凭通用印象）： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0758 | original/SKILL.md.txt:758 | 4A.3-A：按 VCEP 全文赋分（门控通过） |   - PVS1：该基因 LoF 是否为已知机制的明确声明，NMD 逃逸区域的具体指引与例外坐标 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0759 | original/SKILL.md.txt:759 | 4A.3-A：按 VCEP 全文赋分（门控通过） |   - PM1：基因特异性关键功能域/热点区域定义（精确到氨基酸范围），或明确**停用** PM1 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0760 | original/SKILL.md.txt:760 | 4A.3-A：按 VCEP 全文赋分（门控通过） |   - PS1/PM5：该基因已知致病错义变异的位点列表与适用条件 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0761 | original/SKILL.md.txt:761 | 4A.3-A：按 VCEP 全文赋分（门控通过） |   - PP3/BP4：基因特异的预测工具与阈值（常**替代**通用 REVEL 阈值） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0762 | original/SKILL.md.txt:762 | 4A.3-A：按 VCEP 全文赋分（门控通过） |   - PM2/BA1/BS1：基于该疾病流行率/外显率计算的特定群体频率阈值（常与通用阈值差异极大） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0763 | original/SKILL.md.txt:763 | 4A.3-A：按 VCEP 全文赋分（门控通过） |   - PS3/BS3：该基因适用的功能实验类型、OddsPath 校准与判定标准 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0764 | original/SKILL.md.txt:764 | 4A.3-A：按 VCEP 全文赋分（门控通过） |   - PP4：该疾病特征性表型的明确定义与可用性 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0765 | original/SKILL.md.txt:765 | 4A.3-A：按 VCEP 全文赋分（门控通过） | - 若 VCEP 判定结果与通用标准判定不同，须在模块6中专门说明差异及取舍逻辑（详见判定流程第7条）。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0767 | original/SKILL.md.txt:767 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | ### 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0769 | original/SKILL.md.txt:769 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | 当确认该基因有/可能有 VCEP 规范，但 Layer 0–3 **均未能取得可据以赋分的全文**时： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0771 | original/SKILL.md.txt:771 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | 1. **继续按通用 ACMG/AMP + ClinGen SVI 标准完成本次评级**——不阻断分析（这是软门控，与 PVS1 蛋白改变硬门控不同）。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0772 | original/SKILL.md.txt:772 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | 2. **在模块1（Classification Hero）正上方与模块3（ACMG 证据链）顶部，以醒目标记同时声明**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0774 | original/SKILL.md.txt:774 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0775 | original/SKILL.md.txt:775 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | ⚠️ VCEP 规范全文未获取声明 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0776 | original/SKILL.md.txt:776 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | 本基因（[基因名]）存在已发布/疑似存在的 ClinGen VCEP 定制规则 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0777 | original/SKILL.md.txt:777 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | （[VCEP 名称 / specification 名称，若已知；否则注明"具体规范名称未确认"]）， | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0778 | original/SKILL.md.txt:778 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | 但本次分析未能取得其规范全文（已尝试：发表论文 / cspec / ClinGen 官方文档）。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0780 | original/SKILL.md.txt:780 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | 因此以下评级基于【通用 ACMG/AMP + ClinGen SVI 标准】，而非该基因的 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0781 | original/SKILL.md.txt:781 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | VCEP 定制标准。VCEP 定制规则可能改变 PM2/PP3/PM1/PVS1/BS1 等代码的 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0782 | original/SKILL.md.txt:782 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | 阈值或强度，进而改变最终分类，故本次结论应视为【初步评级】。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0784 | original/SKILL.md.txt:784 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | 📎 请您稍后上传该 VCEP 规范全文（cspec 导出 PDF、发表论文 PDF/补充材料， | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0785 | original/SKILL.md.txt:785 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | 或官方 specification 文档），上传后我将依据 VCEP 定制标准重新逐条赋分、 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0786 | original/SKILL.md.txt:786 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | 并出具正式评级（见复核流程）。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0787 | original/SKILL.md.txt:787 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0789 | original/SKILL.md.txt:789 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | 3. **在报告末尾追加一键自查链接**：cspec UI（https://cspec.genome.network/cspec/ui/svi/）、对应论文 PubMed 链接（若已获 PM | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0790 | original/SKILL.md.txt:790 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | 4. **将本例标记为"待 VCEP 复核"状态**，提示用户上传后可直接触发 4A.5 复核流程。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0792 | original/SKILL.md.txt:792 | 4A.3-B：诚实回退 + 用户上传请求（门控未通过） | > 注意：4A.3-B 仅适用于"有规范但全文取不到"。若属情况 B（**确认无规范**），不要发出上传请求，直接走 4A.4。两者措辞必须区分清楚，避免误导用户去找一份并不存在的规范。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0794 | original/SKILL.md.txt:794 | 4A.4：该基因确无 VCEP 规范 | ### 4A.4：该基因确无 VCEP 规范 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0796 | original/SKILL.md.txt:796 | 4A.4：该基因确无 VCEP 规范 | - 使用通用 ACMG/AMP + ClinGen SVI 更新标准（即本技能默认流程）。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0797 | original/SKILL.md.txt:797 | 4A.4：该基因确无 VCEP 规范 | - 在报告中注明："经检索，该基因尚无 ClinGen VCEP 定制规则，本分析采用通用 ACMG/AMP + SVI 标准。" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0798 | original/SKILL.md.txt:798 | 4A.4：该基因确无 VCEP 规范 | - 不发出 VCEP 上传请求。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0800 | original/SKILL.md.txt:800 | 4A.5：用户上传 VCEP 规范后的复核流程（Re-grading） | ### 4A.5：用户上传 VCEP 规范后的复核流程（Re-grading） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0802 | original/SKILL.md.txt:802 | 4A.5：用户上传 VCEP 规范后的复核流程（Re-grading） | 当用户在任意时点上传某基因的 VCEP 规范文档（无论此前是否已出过初步评级）： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0804 | original/SKILL.md.txt:804 | 4A.5：用户上传 VCEP 规范后的复核流程（Re-grading） | 1. **完整阅读上传文档**——不可只读摘要或前几页。VCEP 规范的关键阈值常分散在各代码条目、决策树与**补充附表**中；PDF 须按需逐页/逐表提取，确认无遗漏。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0805 | original/SKILL.md.txt:805 | 4A.5：用户上传 VCEP 规范后的复核流程（Re-grading） | 2. **建立"VCEP 规则对照表"**：逐一列出该 VCEP 对每个 ACMG 代码的定制动作（停用 / 限定坐标 / 调整强度 / 修改阈值 / 新增基因特异条件 / 维持通用）。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0806 | original/SKILL.md.txt:806 | 4A.5：用户上传 VCEP 规范后的复核流程（Re-grading） | 3. **逐条重赋本例已用到的证据代码**，并列出"通用赋值 → VCEP 赋值"的逐项差异。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0807 | original/SKILL.md.txt:807 | 4A.5：用户上传 VCEP 规范后的复核流程（Re-grading） | 4. **重新计算最终分类**，在报告中专列"通用标准 vs VCEP 标准对照"小节，明确说明分类是否改变及原因；移除原报告中的"⚠️ VCEP 规范全文未获取声明"。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0808 | original/SKILL.md.txt:808 | 4A.5：用户上传 VCEP 规范后的复核流程（Re-grading） | 5. 在模块3每条受 VCEP 影响的代码后标注 [VCEP] 及版本号；模块1的 Confidence 相应上调。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0810 | original/SKILL.md.txt:810 | 4A.6 常见已发布 VCEP 规则的基因示例 | ### 4A.6 常见已发布 VCEP 规则的基因示例 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0812 | original/SKILL.md.txt:812 | 4A.6 常见已发布 VCEP 规则的基因示例 | 以下基因有已发布的 VCEP 定制 ACMG 规则（非完整列表，**版本与是否新增均需实时查询确认**）： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0813 | original/SKILL.md.txt:813 | 4A.6 常见已发布 VCEP 规则的基因示例 | - 心血管：MYH7, MYBPC3, KCNQ1, LDLR, BRCA1, BRCA2（KCNH2/SCN5A 是否已发布须核） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0814 | original/SKILL.md.txt:814 | 4A.6 常见已发布 VCEP 规则的基因示例 | - 肿瘤：TP53, PTEN, CDH1, MLH1, MSH2, MSH6, PMS2, APC | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0815 | original/SKILL.md.txt:815 | 4A.6 常见已发布 VCEP 规则的基因示例 | - RASopathy：PTPN11, RAF1, BRAF, KRAS, SOS1, HRAS | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0816 | original/SKILL.md.txt:816 | 4A.6 常见已发布 VCEP 规则的基因示例 | - 听力：GJB2, SLC26A4, CDH23, MYO7A | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0817 | original/SKILL.md.txt:817 | 4A.6 常见已发布 VCEP 规则的基因示例 | - 代谢：PAH, GAA | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0818 | original/SKILL.md.txt:818 | 4A.6 常见已发布 VCEP 规则的基因示例 | - 其他：RUNX1, DICER1（FKRP 须核） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0819 | original/SKILL.md.txt:819 | 4A.6 常见已发布 VCEP 规则的基因示例 | - 截至 2026-08 cspec 共约 138 个基因有专病规范（潘丹丹清单），含 LZTR1/SHOC2/RIT1/MRAS 等 RAS 通路、GAA/IDUA 等溶酶体、CEP290 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0821 | original/SKILL.md.txt:821 | 4A.6 常见已发布 VCEP 规则的基因示例 | 当分析涉及上述基因时，应特别注意触发 4A.2 全文门控。但由于 ClinGen 持续发布新的 VCEP specifications，对**任何**基因都应在 4A.1 中检测是否有新发布 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0823 | original/SKILL.md.txt:823 | 4A.6 常见已发布 VCEP 规则的基因示例 | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0825 | original/SKILL.md.txt:825 | Step 5：家系整合分析（Family Segregation，深度模式） | ## Step 5：家系整合分析（Family Segregation，深度模式） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0827 | original/SKILL.md.txt:827 | Step 5：家系整合分析（Family Segregation，深度模式） | 仅在用户提供家系信息时执行。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0829 | original/SKILL.md.txt:829 | 5.1 遗传模式确认 | ### 5.1 遗传模式确认 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0830 | original/SKILL.md.txt:830 | 5.1 遗传模式确认 | - 确认或推断遗传模式：AD / AR / XL / XR / Mitochondrial | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0831 | original/SKILL.md.txt:831 | 5.1 遗传模式确认 | - 对于 AR 疾病：确认是否有第二个变异（compound het 或 homozygous）。仅单一 P/LP 时执行 ACMG_CRITERIA.md §4.9 第二打击强制搜索清单（ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0832 | original/SKILL.md.txt:832 | 5.1 遗传模式确认 | - 同基因多变异必须用亲属或长读长定相，禁止仅凭 ClinVar 评级组合判定复合杂合；单亲可检时按 §4.2 推定反式规则 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0833 | original/SKILL.md.txt:833 | 5.1 遗传模式确认 | - 近亲/ROH 家系不得只按 AR 过滤，保留 AD 基因纯合变异；AR 纯合伴大段 ROH 且父母仅一方携带 → 疑 iUPD（§4.8） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0834 | original/SKILL.md.txt:834 | 5.1 遗传模式确认 | - X 连锁、印记基因、嵌合、双重诊断分别按 §4.7 / §4.8 / §4.1.9 / §4.10 处理 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0835 | original/SKILL.md.txt:835 | 5.1 遗传模式确认 | - **家系验证清单**：X 连锁变异定向追问母系男性亲属并采血验证；传递亲代无表型时向上追溯一代 + STR/SNP 亲缘核验（可按"隔代新发"计 PS2_Moderate）；亲代须完成基 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0837 | original/SKILL.md.txt:837 | 5.2 家系证据评估 | ### 5.2 家系证据评估 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0839 | original/SKILL.md.txt:839 | 5.2 家系证据评估 | De novo 证据（PS2/PM6）— **采用 ClinGen SVI 2018 双轴量化框架，不再简单套用 PS2=Strong / PM6=Moderate**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0840 | original/SKILL.md.txt:840 | 5.2 家系证据评估 | - **双轴定级**：每例 de novo 的分值 = 表型特异性档位（高度特异 2.0 / 一致 1.0 / 广义符合 0.5 / 不一致 0）×（亲缘未核验则折半）。累计积分对照五档阈值 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0841 | original/SKILL.md.txt:841 | 5.2 家系证据评估 | - **亲缘通道**：trio 含样本身份/亲缘核验 → PS2 通道（全权重）；仅父母 Sanger 阴性、无亲缘核验 → PM6 通道（折半）。注意 PM6 同样可升级至 PM6_Ver | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0842 | original/SKILL.md.txt:842 | 5.2 家系证据评估 | - **多例累积**：表型符合的独立 de novo 病例（含跨家系/文献报道）可累加积分；混合核验状态按各自权重计入同一总分。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0843 | original/SKILL.md.txt:843 | 5.2 家系证据评估 | - 🤰 **产前必查**：产前 de novo 的表型特异性档位**必须**按 references/ACMG_CRITERIA.md 第 4.1.5 节"产前 de novo 表型特异性分 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0844 | original/SKILL.md.txt:844 | 5.2 家系证据评估 | - ⚠️ 失效情形：样本错配/非亲生、父母低比例嵌合、父母 Sanger 假阴性（位点覆盖不足）均使 de novo 前提失效或下调。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0845 | original/SKILL.md.txt:845 | 5.2 家系证据评估 | - **完整双轴量化表、五档阈值、产前决策表与速查框见 references/ACMG_CRITERIA.md 第 4.1 节（必读）。** | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0847 | original/SKILL.md.txt:847 | 5.2 家系证据评估 | 共分离证据（PP1 量化，Jarvik & Browning 2016 PMID:27236918；2026-09 替换旧版无出处的 0.6/1.2/2.4 三档）： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0848 | original/SKILL.md.txt:848 | 5.2 家系证据评估 | - 先由家系图数**减数分裂次数**（= 携带变异的受累个体数 − 1；肯定携带者计入；有变异无表型者与未检测者不计；多家系 LOD 累加；AD/AR/XLR 计数细则见 ACMG_CRIT | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0849 | original/SKILL.md.txt:849 | 5.2 家系证据评估 | - 3–4 次（LOD ≈0.9–1.2）→ PP1_Supporting | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0850 | original/SKILL.md.txt:850 | 5.2 家系证据评估 | - 5–6 次（LOD ≈1.5–1.8）→ PP1_Moderate | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0851 | original/SKILL.md.txt:851 | 5.2 家系证据评估 | - ≥7 次（LOD ≥2.1）→ PP1_Strong | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0852 | original/SKILL.md.txt:852 | 5.2 家系证据评估 | - 多基因座异质性疾病按基因贡献占比打折；PP1+PP4 合计 ≤+5；VCEP 另有规定以 VCEP 为准；报告须声明所用标尺 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0853 | original/SKILL.md.txt:853 | 5.2 家系证据评估 | - BS4 须满足四道门槛（受累者未检出、同病确认、排除拟表型、产前几乎不可用） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0855 | original/SKILL.md.txt:855 | 5.2 家系证据评估 | 反式验证（PM3，AR 疾病，ClinGen SVI 点表；详见 ACMG_CRITERIA.md §4.2）： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0856 | original/SKILL.md.txt:856 | 5.2 家系证据评估 | - 对侧 P/LP + 相位确定 → 1.0；对侧 P/LP + 相位未知 → 0.5；纯合（非近亲/ROH）→ 0.5（纯合合计 ≤1.0）；对侧 VUS + 相位确定 → 0.25（合计 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0857 | original/SKILL.md.txt:857 | 5.2 家系证据评估 | - 累计 0.5 → PM3_Supporting；1.0 → PM3；2.0 → PM3_Strong；4.0 → PM3_VeryStrong | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0858 | original/SKILL.md.txt:858 | 5.2 家系证据评估 | - 两变异均须满足 PM2；变异自身高频时 PM3 封顶 Moderate（GJB2 V37I）；对侧升级后重算；本地病例库第二家系可计入并标注未发表 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0860 | original/SKILL.md.txt:860 | 5.3 表型匹配与 PP4（ClinGen 2024，详见 references/ACMG_CRITERIA.md 第4节） | ### 5.3 表型匹配与 PP4（ClinGen 2024，详见 references/ACMG_CRITERIA.md 第4节） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0862 | original/SKILL.md.txt:862 | 5.3 表型匹配与 PP4（ClinGen 2024，详见 references/ACMG_CRITERIA.md 第4节） | - **PP4 路径（ClinGen 2024）**：单基因病（基因座同质）→ 直接赋 PP4，单变异 **PP4+PP1 封顶 +5 分**；多基因病（基因座异质）→ **按比例分摊 PP | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0863 | original/SKILL.md.txt:863 | 5.3 表型匹配与 PP4（ClinGen 2024，详见 references/ACMG_CRITERIA.md 第4节） | - 🔑 **PS2/PM6 或 PS4 已用则不叠加 PP4**（ACGS 2024）：表型特异性通过提升 PS2/PM6 强度体现，不另开 PP4；同一患者/队列用于 PS4 计数后不再用 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0864 | original/SKILL.md.txt:864 | 5.3 表型匹配与 PP4（ClinGen 2024，详见 references/ACMG_CRITERIA.md 第4节） | - **诊断率 → PP4 强度**（ACGS 2024）：≥50% 可 Strong、10–50% Moderate、<10% Supporting 或不用；多基因座按"总诊断率 × 基因 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0865 | original/SKILL.md.txt:865 | 5.3 表型匹配与 PP4（ClinGen 2024，详见 references/ACMG_CRITERIA.md 第4节） | - **产前报告强制"表型吻合度陈述"字段**（落在谱内且特异 / 落在谱内但不特异 / 未报道 / 方向相反），产前 PP4 计分优先限于 VCEP 明确定义胎儿表型条目的情形；患者组织功 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0866 | original/SKILL.md.txt:866 | 5.3 表型匹配与 PP4（ClinGen 2024，详见 references/ACMG_CRITERIA.md 第4节） | - 🤰 **产前 PP4 五原则**：①宁缺毋滥（无 HPO 绑定基因不强赋）②不盲套产后诊断率 ③保持怀疑（基因座同质假设是最危险陷阱）④权重保守（按比例分摊+封顶+5）⑤多学科协作（超声 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0867 | original/SKILL.md.txt:867 | 5.3 表型匹配与 PP4（ClinGen 2024，详见 references/ACMG_CRITERIA.md 第4节） | - 🤰 **产前表型根本局限**：超声是结构筛查非功能预测工具；HPO 仅约 10% 词条适用产前；基因座异质性普遍；胎儿外显率不明确；家族史常不全。PS2/PM3/PP4 在产前使用受限 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0868 | original/SKILL.md.txt:868 | 5.3 表型匹配与 PP4（ClinGen 2024，详见 references/ACMG_CRITERIA.md 第4节） | - **PM3 in trans 判定**（徐博成）：文献写明复合杂合/in trans/有父母来源 → in trans；否则 unknown | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0869 | original/SKILL.md.txt:869 | 5.3 表型匹配与 PP4（ClinGen 2024，详见 references/ACMG_CRITERIA.md 第4节） | - **PS2 vs PM6 文献分界**（徐博成）：写明亲缘确定或 trio-WES/WGS 检出 → PS2；否则 PM6 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0871 | original/SKILL.md.txt:871 | 5.3 表型匹配与 PP4（ClinGen 2024，详见 references/ACMG_CRITERIA.md 第4节） | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0873 | original/SKILL.md.txt:873 | ACMG 判定引擎 | ## ACMG 判定引擎 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0875 | original/SKILL.md.txt:875 | ACMG 判定引擎 | 完成以上步骤后，执行最终判定。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0877 | original/SKILL.md.txt:877 | ACMG 判定引擎 | **详细的证据代码定义和判定组合规则，参阅 references/ACMG_CRITERIA.md。** 在进行 ACMG 判定前，先阅读该参考文件以确保证据代码赋值和组合逻辑的准确性。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0879 | original/SKILL.md.txt:879 | 判定前检查清单 | ### 判定前检查清单 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0881 | original/SKILL.md.txt:881 | 判定前检查清单 | 在赋值证据代码前，依次确认： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0882 | original/SKILL.md.txt:882 | 判定前检查清单 | 0. **基因-疾病有效性门控**：ClinGen/GenCC 有效性 ≤ Limited、Disputed/Refuted 或无记录 → 最终分类**封顶 VUS**，模块 1 标注 Ge | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0883 | original/SKILL.md.txt:883 | 判定前检查清单 | 0′. **样本层与可比对性门控**（产前模式）：MCC、VAF/嵌合、高同源区三项已核（见运行模式"产前样本前置质控"），未核者标注并下调 Confidence。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0884 | original/SKILL.md.txt:884 | 判定前检查清单 | 1. **基因特异性规则优先（全文门控）**：Step 4A 中是否发现该基因有 ClinGen VCEP 定制规则？若有，**必须已取得规范全文并完整阅读**（Step 4A.2 门控通过 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0885 | original/SKILL.md.txt:885 | 判定前检查清单 | 2. **证据独立性**：确认各证据代码来自独立数据源，无重复计数（参见 references/ACMG_CRITERIA.md 第6节）。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0886 | original/SKILL.md.txt:886 | 判定前检查清单 | 3. **互斥与合并检查**（完整五分类决策表见 references/ACMG_CRITERIA.md §6.5）：禁止共用——PP3/BP4、PS1/PM5、PVS1 与 PM1/PM4 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0887 | original/SKILL.md.txt:887 | 判定前检查清单 | 4. **"至少两条证据"规则**：除 BA1 外，LB/LP/P 至少两条独立证据，单证据一律 VUS（即使积分已入区间）。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0888 | original/SKILL.md.txt:888 | 判定前检查清单 | 5. **良性侧不得托底、产前不出预测型 LB**：其他证据均指向良性时不得用 PP2/PM2 托在 VUS；产前良性侧仅有计算预测时不出 LB。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0890 | original/SKILL.md.txt:890 | 矛盾证据处理（详见 references/ACMG_CRITERIA.md 第6节） | ### 矛盾证据处理（详见 references/ACMG_CRITERIA.md 第6节） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0892 | original/SKILL.md.txt:892 | 矛盾证据处理（详见 references/ACMG_CRITERIA.md 第6节） | 当同时存在致病与良性证据（VUS 常见成因）时，按**证据优先级**（由高到低）权衡： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0893 | original/SKILL.md.txt:893 | 矛盾证据处理（详见 references/ACMG_CRITERIA.md 第6节） | **人群频率（BA1 独立；BS1/PM2）> 功能验证（PS3/BS3、PVS1(RNA)/BP7(RNA)）> 家系（PS2/PM6/PP1/BS4）> 相位（PM3/BP2）> 保守/ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0895 | original/SKILL.md.txt:895 | 矛盾证据处理（详见 references/ACMG_CRITERIA.md 第6节） | 最常见冲突为计算预测 vs 人群频率，处理规则： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0896 | original/SKILL.md.txt:896 | 矛盾证据处理（详见 references/ACMG_CRITERIA.md 第6节） | - BA1(>5%) + 任何致病证据 → 良性（一票否决，白名单与亚效等位例外除外） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0897 | original/SKILL.md.txt:897 | 矛盾证据处理（详见 references/ACMG_CRITERIA.md 第6节） | - BS1 + PP3 → LB/VUS（BS1 权重更高） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0898 | original/SKILL.md.txt:898 | 矛盾证据处理（详见 references/ACMG_CRITERIA.md 第6节） | - BS1 + PS2 → LP/VUS（PS2 仍有效，BS1 强则降 VUS） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0899 | original/SKILL.md.txt:899 | 矛盾证据处理（详见 references/ACMG_CRITERIA.md 第6节） | - PM2 + BP4 / BS1 + PM6 → VUS（冲突抵消） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0900 | original/SKILL.md.txt:900 | 矛盾证据处理（详见 references/ACMG_CRITERIA.md 第6节） | - PP3_Strong + PM2_Supporting → VUS（5 分，预测不得抬高） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0901 | original/SKILL.md.txt:901 | 矛盾证据处理（详见 references/ACMG_CRITERIA.md 第6节） | - PS3 ≥ Strong 与 BP4 方向相反 → BP4 至多 Supporting 或不计 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0902 | original/SKILL.md.txt:902 | 矛盾证据处理（详见 references/ACMG_CRITERIA.md 第6节） | - PP3 与 BP4 → 互斥不计分 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0903 | original/SKILL.md.txt:903 | 矛盾证据处理（详见 references/ACMG_CRITERIA.md 第6节） | - 历史 P/LP 被推翻、或仅因规则版本变化的边界重分类 → 报告须标注 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0905 | original/SKILL.md.txt:905 | 判定流程 | ### 判定流程 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0907 | original/SKILL.md.txt:907 | 判定流程 | 1. 列出所有适用的证据代码及其强度等级（若使用 VCEP 规则，标注 VCEP 来源） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0908 | original/SKILL.md.txt:908 | 判定流程 | 2. 列出所有排除的证据代码及排除理由 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0909 | original/SKILL.md.txt:909 | 判定流程 | 3. 检查证据间是否存在冲突或重复计数 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0910 | original/SKILL.md.txt:910 | 判定流程 | 4. 按组合标准计算最终分类 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0911 | original/SKILL.md.txt:911 | 判定流程 | 5. 使用 Bayesian 积分交叉验证（Supporting=1, Moderate=2, Strong=4, Very Strong=8；阈值 P ≥10 / LP 6–9 / VUS | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0912 | original/SKILL.md.txt:912 | 判定流程 | 6. 若积分和组合规则结论不一致，需在报告中讨论 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0913 | original/SKILL.md.txt:913 | 判定流程 | 7. 若使用了 VCEP 规则且判定结果与通用标准判定不同，需在模块6中说明差异 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0914 | original/SKILL.md.txt:914 | 判定流程 | 8. **敏感性分析**：任一证据存在相邻两档争议且改档会跨分类线时，输出积分区间与两种分类，并写明所选档位及理由 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0915 | original/SKILL.md.txt:915 | 判定流程 | 9. **按疾病实体/合子状态分层出结论**：一基因多病或 AR 基因杂合检出时，对每个疾病实体/合子状态分别给分类（如"作为隐性等位 LP；杂合状态下 VUS/携带"） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0916 | original/SKILL.md.txt:916 | 判定流程 | 10. VUS 时给内部亚档（VUS-High/Mid/Low，ACMG_CRITERIA.md §0），仅进附表与后续建议，不进分类栏 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0918 | original/SKILL.md.txt:918 | 判定流程 | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0920 | original/SKILL.md.txt:920 | Step 6：VUS 报告取舍与措辞规范（产前模式强制；⟦培训班⟧ 余丽华/蒋宇林） | ## Step 6：VUS 报告取舍与措辞规范（产前模式强制；⟦培训班⟧ 余丽华/蒋宇林） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0922 | original/SKILL.md.txt:922 | 6.1 报/不报决策 | ### 6.1 报/不报决策 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0923 | original/SKILL.md.txt:923 | 6.1 报/不报决策 | 1. 检测性质：**有症状**（胎儿超声异常 / 家族史阳性 / 表型驱动）vs **无症状**（高龄或血清学阳性但胎儿无异常、携带者筛查、次要发现）。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0924 | original/SKILL.md.txt:924 | 6.1 报/不报决策 | 2. 有症状 → 满足"基因-表型因果可能性"门槛则报；GUS 基因的变异封顶 VUS 且须标注"GUS 中的 VUS"；AR 单杂合 VUS 默认不报（表型高度匹配除外，且须先完成第二打击 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0925 | original/SKILL.md.txt:925 | 6.1 报/不报决策 | 3. 无症状 → 默认不报 VUS；产前允许报 VUS-High 的例外须有"存在决策机会 + MDT"前提。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0926 | original/SKILL.md.txt:926 | 6.1 报/不报决策 | 4. 不报清单：被推翻的历史变异；机制不符（GOF 基因的 NMD 截短）；胎儿携带状态（AR 携带、XL 女胎携带）——但**夫妇共同携带同一 AR 病 P/LP** 以再生育风险形式告知 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0927 | original/SKILL.md.txt:927 | 6.1 报/不报决策 | 5. 输出一行 Reporting recommendation: 主表 / 附表 / 不建议报告 + 依据条款。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0929 | original/SKILL.md.txt:929 | 6.2 措辞规范（Mandatory Wording Rules） | ### 6.2 措辞规范（Mandatory Wording Rules） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0930 | original/SKILL.md.txt:930 | 6.2 措辞规范（Mandatory Wording Rules） | - **五禁**：绝对预后句（"将出现…"）；"排除遗传病 / 检测正常 / 健康"；指令性妊娠建议（引产/继续妊娠）；VUS 加"倾向/接近/高度可疑致病"修饰；把实验室策略差异说成分类矛 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0931 | original/SKILL.md.txt:931 | 6.2 措辞规范（Mandatory Wording Rules） | - **推荐句式**："已报道病例中 X% 出现…（n=…）" / "文献报道率 高/中/低"；"当前证据不足以支持将本变异作为终止妊娠的依据"（VUS 时必写决策边界句）；"建议由临床医师 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0932 | original/SKILL.md.txt:932 | 6.2 措辞规范（Mandatory Wording Rules） | - 模块 8′ 每一行预后必须写成文献报道率句式；行动计划不写妊娠决策建议。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0933 | original/SKILL.md.txt:933 | 6.2 措辞规范（Mandatory Wording Rules） | - 报告分"分级 / 归因（超声表型吻合度陈述）/ 再发风险"三段；找到致病变异后寻找不停止。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0935 | original/SKILL.md.txt:935 | 6.3 再评估触发与闭环 | ### 6.3 再评估触发与闭环 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0936 | original/SKILL.md.txt:936 | 6.3 再评估触发与闭环 | 报告固定输出 Re-evaluation triggers:——新知识（数据库/文献）、新表型（随访超声/MRI/出生后表型、引产后尸检）、家族成员检测、进一步临床检查、指南版本变更；Evi | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0938 | original/SKILL.md.txt:938 | 6.3 再评估触发与闭环 | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0940 | original/SKILL.md.txt:940 | 输出前自检清单（Mandatory Pre-output Checklist） | ## 输出前自检清单（Mandatory Pre-output Checklist） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0942 | original/SKILL.md.txt:942 | 输出前自检清单（Mandatory Pre-output Checklist） | 在生成最终报告前，必须逐项核实以下内容。任何一项未通过都必须在继续之前解决： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0944 | original/SKILL.md.txt:944 | 输出前自检清单（Mandatory Pre-output Checklist） | - □ **蛋白改变验证**: 蛋白改变（HGVSp）是否经外部工具（VariantValidator/Mutalyzer）验证？若否 → ⛔ 停止，回到 Step 0 的强制验证门控 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0945 | original/SKILL.md.txt:945 | 输出前自检清单（Mandatory Pre-output Checklist） | - □ **变异类型一致性**: 变异类型（missense/nonsense/frameshift等）是否与验证后的蛋白改变一致？ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0946 | original/SKILL.md.txt:946 | 输出前自检清单（Mandatory Pre-output Checklist） | - □ **VCEP 全文门控**（Step 4A 强制）: 是否已检测该基因有无 VCEP 规范？ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0947 | original/SKILL.md.txt:947 | 输出前自检清单（Mandatory Pre-output Checklist） |   - 若有规范且全文已取得 → 是否已据 VCEP 全文逐条赋分并标注 [VCEP] 及版本号？ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0948 | original/SKILL.md.txt:948 | 输出前自检清单（Mandatory Pre-output Checklist） |   - 若有规范但全文未取得 → 是否已在模块1/模块3顶部输出"⚠️ VCEP 规范全文未获取声明"、标注结论为初步评级、并发出用户上传请求？若漏掉声明 → ⛔ 停止补上 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0949 | original/SKILL.md.txt:949 | 输出前自检清单（Mandatory Pre-output Checklist） |   - 若用户已上传 VCEP 文档 → 是否已完整阅读并走 4A.5 复核流程（而非沿用旧的通用初步评级）？ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0950 | original/SKILL.md.txt:950 | 输出前自检清单（Mandatory Pre-output Checklist） | - □ **ClinVar 交叉校验**: 自身分析结论是否与 ClinVar 分类一致？ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0951 | original/SKILL.md.txt:951 | 输出前自检清单（Mandatory Pre-output Checklist） |   - 若不一致 → 必须在模块6中专节讨论差异原因 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0952 | original/SKILL.md.txt:952 | 输出前自检清单（Mandatory Pre-output Checklist） |   - 若自身判定比 ClinVar 多机构共识严重偏高或偏低 → 高度警惕分析错误，逐步回溯检查 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0953 | original/SKILL.md.txt:953 | 输出前自检清单（Mandatory Pre-output Checklist） | - □ **群体频率获取**: gnomAD 频率是否已获取？PM2/BA1/BS1 赋值是否与频率数据一致？ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0954 | original/SKILL.md.txt:954 | 输出前自检清单（Mandatory Pre-output Checklist） | - □ **预测评分支撑**: 对于错义变异，REVEL 评分是否已获取？PP3/BP4 赋值是否有数据支撑？ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0955 | original/SKILL.md.txt:955 | 输出前自检清单（Mandatory Pre-output Checklist） | - □ **PVS1 适用性**: PVS1 是否仅用于 null 变异（nonsense/frameshift/canonical splice）？若 PVS1 被赋予错义变异 → ⛔ 严 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0956 | original/SKILL.md.txt:956 | 输出前自检清单（Mandatory Pre-output Checklist） | - □ **积分一致性**: 证据代码总积分是否与组合规则判定一致（阈值 VUS 0–5 / LB −1～−6）？是否满足"至少两条证据"？GUS 封顶是否已套用？ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0957 | original/SKILL.md.txt:957 | 输出前自检清单（Mandatory Pre-output Checklist） | - □ **合并规则**: 是否按 ACMG_CRITERIA.md §6.5 逐对核查禁止/限制合并？PP5/BP6 是否已剔除？ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0958 | original/SKILL.md.txt:958 | 输出前自检清单（Mandatory Pre-output Checklist） | - □ **措辞合规**（产前）: 全文无 Step 6.2 禁用句式；VUS 已写决策边界句；Reporting recommendation 与 Re-evaluation trigge | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0959 | original/SKILL.md.txt:959 | 输出前自检清单（Mandatory Pre-output Checklist） | - □ **产前前置质控**: MCC status / VAF-嵌合 / Mappability 三项已在模块 2 填写？ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0960 | original/SKILL.md.txt:960 | 输出前自检清单（Mandatory Pre-output Checklist） | - □ **邻近地形完成**（Novel Variant 时必查）: Step 0.6 是否已执行并生成邻近变异地形报告？模块2中是否已填写 Nearest variant 字段？若 Cli | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0961 | original/SKILL.md.txt:961 | 输出前自检清单（Mandatory Pre-output Checklist） | - □ **产前模块完整**（产前模式时必查）: Step 0.7 是否已执行（P1-P4 全部完成）？若为 novel variant，是否已输出主动文献补充请求（P3 模板）？模块8'（ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0962 | original/SKILL.md.txt:962 | 输出前自检清单（Mandatory Pre-output Checklist） | - □ **参考文献 PMID 反查验证**（强制执行，不可跳过）: 模块9中所有参考文献是否经过 PMID 反查验证？详见下方 **Step 9-Verify** 强制执行规范。若未执行  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0964 | original/SKILL.md.txt:964 | 输出前自检清单（Mandatory Pre-output Checklist） | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0966 | original/SKILL.md.txt:966 | Step 9-Verify：参考文献 PMID 反查验证（强制执行步骤） | ## Step 9-Verify：参考文献 PMID 反查验证（强制执行步骤） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0968 | original/SKILL.md.txt:968 | 设计动机 | ### 设计动机 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0970 | original/SKILL.md.txt:970 | 设计动机 | AI 生成的参考文献存在三类典型错误： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0971 | original/SKILL.md.txt:971 | 设计动机 | 1. **作者归属错误**：将"被引文献中提到的同行作者"误归属为"被引文献本身的作者"（如把综述中提及的 Pietrobon D 误标为综述作者，实际作者为 Indelicato E &  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0972 | original/SKILL.md.txt:972 | 设计动机 | 2. **PMID 数字错误**：PMID 与文献元数据不匹配，导致 citation 索引失效 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0973 | original/SKILL.md.txt:973 | 设计动机 | 3. **期刊缩写歧义**：Am J Med Genet vs Am J Hum Genet、Mol Brain vs Mol Cell Neurosci 等易混淆期刊 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0975 | original/SKILL.md.txt:975 | 设计动机 | 参考文献错误虽不影响 ACMG 致病性判定本身，但会严重影响： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0976 | original/SKILL.md.txt:976 | 设计动机 | - 临床报告的科研可追溯性 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0977 | original/SKILL.md.txt:977 | 设计动机 | - 论文/病例报告的投稿合规性 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0978 | original/SKILL.md.txt:978 | 设计动机 | - 临床教学的学术准确性 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0979 | original/SKILL.md.txt:979 | 设计动机 | - 用户对整份分析报告的整体信任度 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0981 | original/SKILL.md.txt:981 | 强制执行规则 | ### 强制执行规则 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0983 | original/SKILL.md.txt:983 | 强制执行规则 | **触发条件**：在模块9生成完毕后、最终报告输出前，无条件触发。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0985 | original/SKILL.md.txt:985 | 强制执行规则 | **执行流程**（每条参考文献逐一执行）： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0987 | original/SKILL.md.txt:987 | Step A — PMID 反向验证（核心步骤） | #### Step A — PMID 反向验证（核心步骤） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0989 | original/SKILL.md.txt:989 | Step A — PMID 反向验证（核心步骤） | 对模块9中每条带有 PMID 的文献，执行以下查询： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0991 | original/SKILL.md.txt:991 | Step A — PMID 反向验证（核心步骤） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0992 | original/SKILL.md.txt:992 | Step A — PMID 反向验证（核心步骤） | web_search: "[PMID号] PubMed" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0993 | original/SKILL.md.txt:993 | Step A — PMID 反向验证（核心步骤） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0995 | original/SKILL.md.txt:995 | Step A — PMID 反向验证（核心步骤） | 或 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0997 | original/SKILL.md.txt:997 | Step A — PMID 反向验证（核心步骤） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0998 | original/SKILL.md.txt:998 | Step A — PMID 反向验证（核心步骤） | web_search: "PubMed [关键作者姓+年份+核心关键词]" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-0999 | original/SKILL.md.txt:999 | Step A — PMID 反向验证（核心步骤） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1001 | original/SKILL.md.txt:1001 | Step A — PMID 反向验证（核心步骤） | 从搜索结果中验证： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1002 | original/SKILL.md.txt:1002 | Step A — PMID 反向验证（核心步骤） | - ✓ 作者第一作者姓名是否一致 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1003 | original/SKILL.md.txt:1003 | Step A — PMID 反向验证（核心步骤） | - ✓ 期刊名称是否一致（特别注意 Am J Med Genet ≠ Am J Hum Genet） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1004 | original/SKILL.md.txt:1004 | Step A — PMID 反向验证（核心步骤） | - ✓ 发表年份是否一致 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1005 | original/SKILL.md.txt:1005 | Step A — PMID 反向验证（核心步骤） | - ✓ 文章标题主旨是否一致 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1007 | original/SKILL.md.txt:1007 | Step B — 三类常见错误的特异性核查 | #### Step B — 三类常见错误的特异性核查 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1009 | original/SKILL.md.txt:1009 | Step B — 三类常见错误的特异性核查 | **B1. 作者归属错误核查**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1010 | original/SKILL.md.txt:1010 | Step B — 三类常见错误的特异性核查 | 当被引文献为**综述/Meta分析**时，特别检查： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1011 | original/SKILL.md.txt:1011 | Step B — 三类常见错误的特异性核查 | - AI 是否将综述**正文中讨论到的某位科学家**（如领域权威）错误归属为综述作者？ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1012 | original/SKILL.md.txt:1012 | Step B — 三类常见错误的特异性核查 | - 验证方法：搜索 "[标题前6-8词]" author，从搜索结果直接确认通讯作者和第一作者 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1014 | original/SKILL.md.txt:1014 | Step B — 三类常见错误的特异性核查 | **B2. PMID 数字错误核查**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1015 | original/SKILL.md.txt:1015 | Step B — 三类常见错误的特异性核查 | PMID 是 8 位数字（部分较老文献 7 位），必须与作者+期刊+年份**三元组**匹配： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1016 | original/SKILL.md.txt:1016 | Step B — 三类常见错误的特异性核查 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1017 | original/SKILL.md.txt:1017 | Step B — 三类常见错误的特异性核查 | web_search: "[PMID号]" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1018 | original/SKILL.md.txt:1018 | Step B — 三类常见错误的特异性核查 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1019 | original/SKILL.md.txt:1019 | Step B — 三类常见错误的特异性核查 | 确认搜索结果展示的文献元数据三元组与生成内容完全一致。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1021 | original/SKILL.md.txt:1021 | Step B — 三类常见错误的特异性核查 | **B3. 期刊歧义核查**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1022 | original/SKILL.md.txt:1022 | Step B — 三类常见错误的特异性核查 | 对易混淆期刊（特别是医学遗传学领域），逐字符核对全名： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1023 | original/SKILL.md.txt:1023 | Step B — 三类常见错误的特异性核查 | - Am J Med Genet (American Journal of Medical Genetics) ← 病例报告/综述为主 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1024 | original/SKILL.md.txt:1024 | Step B — 三类常见错误的特异性核查 | - Am J Hum Genet (American Journal of Human Genetics) ← 群体遗传/方法学为主 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1025 | original/SKILL.md.txt:1025 | Step B — 三类常见错误的特异性核查 | - Mol Brain ≠ Mol Cell Neurosci ≠ J Mol Neurosci | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1026 | original/SKILL.md.txt:1026 | Step B — 三类常见错误的特异性核查 | - Nat Genet ≠ Nat Neurosci ≠ Neurology | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1027 | original/SKILL.md.txt:1027 | Step B — 三类常见错误的特异性核查 | - Clin Genet ≠ J Med Genet ≠ Eur J Hum Genet | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1029 | original/SKILL.md.txt:1029 | Step C — 错误处理协议 | #### Step C — 错误处理协议 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1031 | original/SKILL.md.txt:1031 | Step C — 错误处理协议 | **若发现任何一处错误**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1033 | original/SKILL.md.txt:1033 | Step C — 错误处理协议 | \| 错误类型 \| 处理方式 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1034 | original/SKILL.md.txt:1034 | Step C — 错误处理协议 | \|---------\|---------\| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1035 | original/SKILL.md.txt:1035 | Step C — 错误处理协议 | \| PMID 数字错误 \| 立即更正为正确 PMID，并在引文末尾添加 ← 已核验更正 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1036 | original/SKILL.md.txt:1036 | Step C — 错误处理协议 | \| 作者完全错误 \| 立即更正作者列表，并在引文末尾添加 ← 作者已经过 PMID 反查更正 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1037 | original/SKILL.md.txt:1037 | Step C — 错误处理协议 | \| 期刊名称错误 \| 立即更正期刊全名 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1038 | original/SKILL.md.txt:1038 | Step C — 错误处理协议 | \| 完全无法找到对应文献 \| 删除该引文，**禁止保留虚构文献**，并在模块10局限性声明中明确说明 \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1040 | original/SKILL.md.txt:1040 | Step C — 错误处理协议 | **若文献核心结论被发现与原引用不符**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1041 | original/SKILL.md.txt:1041 | Step C — 错误处理协议 | - 重新审视该证据在 ACMG 证据链中的角色 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1042 | original/SKILL.md.txt:1042 | Step C — 错误处理协议 | - 必要时调整证据强度或撤回该证据代码 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1043 | original/SKILL.md.txt:1043 | Step C — 错误处理协议 | - 在模块6中说明这一发现及其对最终分类的影响 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1045 | original/SKILL.md.txt:1045 | Step D — 反查验证总结输出 | #### Step D — 反查验证总结输出 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1047 | original/SKILL.md.txt:1047 | Step D — 反查验证总结输出 | 完成所有引文反查后，在模块9末尾**强制追加**以下结构化输出： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1049 | original/SKILL.md.txt:1049 | Step D — 反查验证总结输出 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1050 | original/SKILL.md.txt:1050 | Step D — 反查验证总结输出 | ── 参考文献反查验证结果 ────────────────────────────────── | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1051 | original/SKILL.md.txt:1051 | Step D — 反查验证总结输出 | 反查执行日期:        [YYYY-MM-DD] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1052 | original/SKILL.md.txt:1052 | Step D — 反查验证总结输出 | 引用文献总数:        [N] 条 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1053 | original/SKILL.md.txt:1053 | Step D — 反查验证总结输出 | 通过验证条数:        [N] 条 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1054 | original/SKILL.md.txt:1054 | Step D — 反查验证总结输出 | 更正条数:            [N] 条（详见各引文末尾标注） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1055 | original/SKILL.md.txt:1055 | Step D — 反查验证总结输出 | 删除条数:            [N] 条（详见下方说明） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1056 | original/SKILL.md.txt:1056 | Step D — 反查验证总结输出 | 反查覆盖率:          [100%] ← 必须为 100% | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1058 | original/SKILL.md.txt:1058 | Step D — 反查验证总结输出 | ⚠️ 反查发现的关键修正: | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1059 | original/SKILL.md.txt:1059 | Step D — 反查验证总结输出 | [列出对最终分析有影响的修正，如适用] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1060 | original/SKILL.md.txt:1060 | Step D — 反查验证总结输出 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1062 | original/SKILL.md.txt:1062 | 反查策略效率优化 | ### 反查策略效率优化 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1064 | original/SKILL.md.txt:1064 | 反查策略效率优化 | 为避免反查过程过于冗长，采用以下并行策略： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1066 | original/SKILL.md.txt:1066 | 反查策略效率优化 | **并行查询规则**：每轮 web_search 同时发起 2-3 条不同 PMID 的反查请求，从搜索结果片段中提取关键元数据。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1068 | original/SKILL.md.txt:1068 | 反查策略效率优化 | **信任级别分层**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1069 | original/SKILL.md.txt:1069 | 反查策略效率优化 | - **强信任**（无需反查）：当前对话中 web_search 已返回完整元数据（含 PMID + 作者 + 期刊 + 标题）的文献 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1070 | original/SKILL.md.txt:1070 | 反查策略效率优化 | - **中信任**（需反查）：综合多次检索拼接的文献信息 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1071 | original/SKILL.md.txt:1071 | 反查策略效率优化 | - **弱信任**（必须反查）：未经直接搜索验证的引文（如从领域知识中"想起来"的经典文献） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1073 | original/SKILL.md.txt:1073 | 严禁行为 | ### 严禁行为 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1075 | original/SKILL.md.txt:1075 | 严禁行为 | - ❌ 跳过此步骤直接输出最终报告 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1076 | original/SKILL.md.txt:1076 | 严禁行为 | - ❌ 因时间/工具调用次数限制而"声称已验证"实际未验证 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1077 | original/SKILL.md.txt:1077 | 严禁行为 | - ❌ 保留无法验证的虚构文献 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1078 | original/SKILL.md.txt:1078 | 严禁行为 | - ❌ 仅验证部分引文而声称全部已验证 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1080 | original/SKILL.md.txt:1080 | 与其他自检步骤的关系 | ### 与其他自检步骤的关系 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1082 | original/SKILL.md.txt:1082 | 与其他自检步骤的关系 | 本步骤是 **输出前最后一道质控关卡**，应在所有其他自检项（蛋白改变验证、ACMG 证据一致性、Step 0.6 邻近地形、Step 0.7 产前预后等）完成后执行。完成此步骤后方可输出最 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1084 | original/SKILL.md.txt:1084 | 与其他自检步骤的关系 | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1086 | original/SKILL.md.txt:1086 | 输出结构 | ## 输出结构 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1088 | original/SKILL.md.txt:1088 | 输出结构 | 按以下模块化结构输出，严格遵循双语混合规则。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1090 | original/SKILL.md.txt:1090 | 模块 1：Classification Hero | ### 模块 1：Classification Hero | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1092 | original/SKILL.md.txt:1092 | 模块 1：Classification Hero |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1093 | original/SKILL.md.txt:1093 | 模块 1：Classification Hero | ═══════════════════════════════════════════ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1094 | original/SKILL.md.txt:1094 | 模块 1：Classification Hero |   CLASSIFICATION:  [Pathogenic / Likely Pathogenic / VUS / Likely Benign / Benign] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1095 | original/SKILL.md.txt:1095 | 模块 1：Classification Hero |   ACMG Score:      [Bayesian 积分] points | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1096 | original/SKILL.md.txt:1096 | 模块 1：Classification Hero |   Evidence:        [PVS1 + PM2_Supporting + PP3 ...]  (致病侧) | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1097 | original/SKILL.md.txt:1097 | 模块 1：Classification Hero |                    [BP4 ...]  (良性侧, 如有) | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1098 | original/SKILL.md.txt:1098 | 模块 1：Classification Hero |   Confidence:      [High / Moderate / Low — 基于证据充分度] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1099 | original/SKILL.md.txt:1099 | 模块 1：Classification Hero |   Disease entity:  [疾病实体 / 遗传方式 / 本例合子状态；一基因多病时分行给出各自分类] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1100 | original/SKILL.md.txt:1100 | 模块 1：Classification Hero |   VUS sub-tier:    [High / Mid / Low — 仅 VUS 时输出，内部参考] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1101 | original/SKILL.md.txt:1101 | 模块 1：Classification Hero |   Caveats:         [Gene-disease validity cap applied / Mappability caveat / MCC 未排除 / 亲代嵌合 …（无 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1102 | original/SKILL.md.txt:1102 | 模块 1：Classification Hero |   Reporting:       [主表 / 附表 / 不建议报告 — 产前模式必填] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1103 | original/SKILL.md.txt:1103 | 模块 1：Classification Hero | ═══════════════════════════════════════════ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1104 | original/SKILL.md.txt:1104 | 模块 1：Classification Hero |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1106 | original/SKILL.md.txt:1106 | 模块 2：Molecular Profile | ### 模块 2：Molecular Profile | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1108 | original/SKILL.md.txt:1108 | 模块 2：Molecular Profile | 全部使用英语标签，数据精确： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1110 | original/SKILL.md.txt:1110 | 模块 2：Molecular Profile |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1111 | original/SKILL.md.txt:1111 | 模块 2：Molecular Profile | Gene:               [基因名] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1112 | original/SKILL.md.txt:1112 | 模块 2：Molecular Profile | Transcript:         [MANE Select NM_xxxxx.x] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1113 | original/SKILL.md.txt:1113 | 模块 2：Molecular Profile | HGVSc:              [c.变异] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1114 | original/SKILL.md.txt:1114 | 模块 2：Molecular Profile | HGVSp:              [p.变异] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1115 | original/SKILL.md.txt:1115 | 模块 2：Molecular Profile | Variant Type:       [missense / nonsense / frameshift / splice / ...] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1116 | original/SKILL.md.txt:1116 | 模块 2：Molecular Profile | Chromosome:         [chrX:位置] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1117 | original/SKILL.md.txt:1117 | 模块 2：Molecular Profile | VCF (GRCh38):       [chr-pos-ref-alt] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1118 | original/SKILL.md.txt:1118 | 模块 2：Molecular Profile | Exon/Intron:        [Exon X / IVS X] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1119 | original/SKILL.md.txt:1119 | 模块 2：Molecular Profile | gnomAD AF (Global): [频率 或 "Not found"] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1120 | original/SKILL.md.txt:1120 | 模块 2：Molecular Profile | gnomAD AF (EAS):    [东亚人群频率] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1121 | original/SKILL.md.txt:1121 | 模块 2：Molecular Profile | gnomAD hom/hemi:    [纯合子 / 半合子计数] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1122 | original/SKILL.md.txt:1122 | 模块 2：Molecular Profile | MCC status:         [产前：MCC 比例 或 "未定量"] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1123 | original/SKILL.md.txt:1123 | 模块 2：Molecular Profile | VAF (proband/parents): [胎儿 VAF；父/母 VAF；偏离 40–60% 时注明嵌合评估] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1124 | original/SKILL.md.txt:1124 | 模块 2：Molecular Profile | Mappability:        [正常 / 高同源区预警：MAPQ、正交验证状态] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1125 | original/SKILL.md.txt:1125 | 模块 2：Molecular Profile | REVEL Score:        [评分 或 "N/A (non-missense)"] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1126 | original/SKILL.md.txt:1126 | 模块 2：Molecular Profile | SpliceAI:           [评分 或 "N/A"] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1127 | original/SKILL.md.txt:1127 | 模块 2：Molecular Profile | CADD (PHRED):       [评分] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1128 | original/SKILL.md.txt:1128 | 模块 2：Molecular Profile | ClinVar:            [评级 + 提交数] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1129 | original/SKILL.md.txt:1129 | 模块 2：Molecular Profile | pLI / LOEUF:        [基因约束指标] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1131 | original/SKILL.md.txt:1131 | 模块 2：Molecular Profile | ── 邻近变异地形（Step 0.6 结果）────────────────────── | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1132 | original/SKILL.md.txt:1132 | 模块 2：Molecular Profile | Nearest variant:    [p.变异名]（L[级别]，距本变异 [N] aa，[来源文献/PMID]） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1133 | original/SKILL.md.txt:1133 | 模块 2：Molecular Profile |                     表型摘要：[一句话，如"MRI 正常，重度 ID+难治性癫痫"] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1134 | original/SKILL.md.txt:1134 | 模块 2：Molecular Profile | Domain landscape:   [如 "AAA6域：文献极稀缺，已知变异仅2例（G4072S, L4179S）"] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1135 | original/SKILL.md.txt:1135 | 模块 2：Molecular Profile | Literature gap:     [如 "该域功能验证数据缺失，无体外运动分析数据"] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1136 | original/SKILL.md.txt:1136 | 模块 2：Molecular Profile |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1138 | original/SKILL.md.txt:1138 | 模块 3：ACMG 证据链（全中文输出） | ### 模块 3：ACMG 证据链（全中文输出） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1140 | original/SKILL.md.txt:1140 | 模块 3：ACMG 证据链（全中文输出） | 本模块全部以中文输出，包括分区标签、强度等级说明和证据理由。证据代码本身保留国际通用缩写（如 PVS1、PM2）以确保专业可读性。若使用了 ClinGen VCEP 基因特异性规则，需在对应 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1142 | original/SKILL.md.txt:1142 | 模块 3：ACMG 证据链（全中文输出） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1143 | original/SKILL.md.txt:1143 | 模块 3：ACMG 证据链（全中文输出） | ┌─────────────────────────────────────────┐ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1144 | original/SKILL.md.txt:1144 | 模块 3：ACMG 证据链（全中文输出） | │  适用标准：[通用 ACMG/ClinGen SVI] 或   │ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1145 | original/SKILL.md.txt:1145 | 模块 3：ACMG 证据链（全中文输出） | │  [ClinGen VCEP: (基因名) — (发布日期)]   │ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1146 | original/SKILL.md.txt:1146 | 模块 3：ACMG 证据链（全中文输出） | └─────────────────────────────────────────┘ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1148 | original/SKILL.md.txt:1148 | 模块 3：ACMG 证据链（全中文输出） | 【致病性证据（已采纳）】 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1150 | original/SKILL.md.txt:1150 | 模块 3：ACMG 证据链（全中文输出） |   PVS1（极强证据）— 无义变异预测触发NMD；功能缺失是[基因]的已知致病机制 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1151 | original/SKILL.md.txt:1151 | 模块 3：ACMG 证据链（全中文输出） |     （ClinGen 单倍剂量不足评分: 3）。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1152 | original/SKILL.md.txt:1152 | 模块 3：ACMG 证据链（全中文输出） |   PM2_Supporting（支持证据）— 在gnomAD v4中未检出（所有人群等位基因计数AC=0）。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1153 | original/SKILL.md.txt:1153 | 模块 3：ACMG 证据链（全中文输出） |     依据ClinGen SVI建议，PM2默认降级为支持强度。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1154 | original/SKILL.md.txt:1154 | 模块 3：ACMG 证据链（全中文输出） |   PP3（支持证据）— REVEL评分0.89，超过支持级阈值0.644。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1155 | original/SKILL.md.txt:1155 | 模块 3：ACMG 证据链（全中文输出） |   [PP3_Moderate [VCEP]（中等证据）— 依据[基因名]VCEP规则，REVEL≥0.75判定为中等强度。] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1156 | original/SKILL.md.txt:1156 | 模块 3：ACMG 证据链（全中文输出） |   ... | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1158 | original/SKILL.md.txt:1158 | 模块 3：ACMG 证据链（全中文输出） | 【良性证据（已采纳，如有）】 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1160 | original/SKILL.md.txt:1160 | 模块 3：ACMG 证据链（全中文输出） |   BP4_Supporting（支持证据）— ... | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1161 | original/SKILL.md.txt:1161 | 模块 3：ACMG 证据链（全中文输出） |   ... | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1163 | original/SKILL.md.txt:1163 | 模块 3：ACMG 证据链（全中文输出） | 【未采纳证据及理由】 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1165 | original/SKILL.md.txt:1165 | 模块 3：ACMG 证据链（全中文输出） |   PS1 — 未采纳：该位置无其他已报道为致病的核苷酸改变。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1166 | original/SKILL.md.txt:1166 | 模块 3：ACMG 证据链（全中文输出） |   PM1 — 未采纳：变异不位于已定义的关键功能结构域内。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1167 | original/SKILL.md.txt:1167 | 模块 3：ACMG 证据链（全中文输出） |   PS3 — 未采纳：未检索到针对该变异的功能实验数据。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1168 | original/SKILL.md.txt:1168 | 模块 3：ACMG 证据链（全中文输出） |   ... | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1170 | original/SKILL.md.txt:1170 | 模块 3：ACMG 证据链（全中文输出） | 【证据独立性与重复计数审查】 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1172 | original/SKILL.md.txt:1172 | 模块 3：ACMG 证据链（全中文输出） |   已确认各证据来源独立，无重复计数。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1173 | original/SKILL.md.txt:1173 | 模块 3：ACMG 证据链（全中文输出） |   [或: 注意 — XX证据与YY证据可能存在部分重叠，已取较保守的赋值。] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1175 | original/SKILL.md.txt:1175 | 模块 3：ACMG 证据链（全中文输出） | 【Bayesian 积分汇总】 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1177 | original/SKILL.md.txt:1177 | 模块 3：ACMG 证据链（全中文输出） |   致病侧积分：[X] 分（详列各证据贡献） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1178 | original/SKILL.md.txt:1178 | 模块 3：ACMG 证据链（全中文输出） |   良性侧积分：[Y] 分 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1179 | original/SKILL.md.txt:1179 | 模块 3：ACMG 证据链（全中文输出） |   净积分：[X-Y] 分 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1180 | original/SKILL.md.txt:1180 | 模块 3：ACMG 证据链（全中文输出） |   判定依据：符合[致病/疑似致病/...]组合规则第[N]条 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1181 | original/SKILL.md.txt:1181 | 模块 3：ACMG 证据链（全中文输出） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1183 | original/SKILL.md.txt:1183 | 模块 4：ClinVar 综合查询结论 | ### 模块 4：ClinVar 综合查询结论 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1185 | original/SKILL.md.txt:1185 | 模块 4：ClinVar 综合查询结论 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1186 | original/SKILL.md.txt:1186 | 模块 4：ClinVar 综合查询结论 | ClinVar 评级:       [综合评级] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1187 | original/SKILL.md.txt:1187 | 模块 4：ClinVar 综合查询结论 | 提交记录数:          [N] 条 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1188 | original/SKILL.md.txt:1188 | 模块 4：ClinVar 综合查询结论 | 评级一致性:          [一致 / 存在冲突] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1189 | original/SKILL.md.txt:1189 | 模块 4：ClinVar 综合查询结论 | 冲突详情（如有）: | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1190 | original/SKILL.md.txt:1190 | 模块 4：ClinVar 综合查询结论 |   - [机构A]: Pathogenic (reviewed: YYYY-MM) | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1191 | original/SKILL.md.txt:1191 | 模块 4：ClinVar 综合查询结论 |   - [机构B]: Likely Pathogenic (reviewed: YYYY-MM) | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1192 | original/SKILL.md.txt:1192 | 模块 4：ClinVar 综合查询结论 |   - [机构C]: VUS (reviewed: YYYY-MM) | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1193 | original/SKILL.md.txt:1193 | 模块 4：ClinVar 综合查询结论 | 最近审核:           [日期] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1194 | original/SKILL.md.txt:1194 | 模块 4：ClinVar 综合查询结论 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1196 | original/SKILL.md.txt:1196 | 模块 5：External Benchmarking（外部分类对标） | ### 模块 5：External Benchmarking（外部分类对标） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1198 | original/SKILL.md.txt:1198 | 模块 5：External Benchmarking（外部分类对标） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1199 | original/SKILL.md.txt:1199 | 模块 5：External Benchmarking（外部分类对标） | ── 外部自动分类对标 ────────────────────────────────── | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1201 | original/SKILL.md.txt:1201 | 模块 5：External Benchmarking（外部分类对标） | VarSome Classification:    [评级 或 "未能获取"] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1202 | original/SKILL.md.txt:1202 | 模块 5：External Benchmarking（外部分类对标） | VarSome Evidence Codes:    [代码列表] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1203 | original/SKILL.md.txt:1203 | 模块 5：External Benchmarking（外部分类对标） | VarSome URL:               [URL] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1205 | original/SKILL.md.txt:1205 | 模块 5：External Benchmarking（外部分类对标） | GeneBe ACMG (EV.acmg_benchmark): [自动 ACMG 评级 或 "未能获取"]  ← 仅对标基准，不覆盖本技能专家评级 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1206 | original/SKILL.md.txt:1206 | 模块 5：External Benchmarking（外部分类对标） | Franklin Classification:   [评级 或 "未能获取（需登录）"] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1207 | original/SKILL.md.txt:1207 | 模块 5：External Benchmarking（外部分类对标） | Franklin Evidence Codes:   [代码列表（若从搜索摘要获取）] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1209 | original/SKILL.md.txt:1209 | 模块 5：External Benchmarking（外部分类对标） | InterVar Classification:   [评级 或 "未查询"] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1211 | original/SKILL.md.txt:1211 | 模块 5：External Benchmarking（外部分类对标） | 对标来源可用性: | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1212 | original/SKILL.md.txt:1212 | 模块 5：External Benchmarking（外部分类对标） |   VarSome:   [✅ 完整获取 / ⚠️ 仅摘要 / ❌ 未获取] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1213 | original/SKILL.md.txt:1213 | 模块 5：External Benchmarking（外部分类对标） |   Franklin:  [✅ 完整获取 / ⚠️ 仅摘要 / ❌ 未获取] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1215 | original/SKILL.md.txt:1215 | 模块 5：External Benchmarking（外部分类对标） | 与本分析差异: | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1216 | original/SKILL.md.txt:1216 | 模块 5：External Benchmarking（外部分类对标） |   [中文说明差异及原因；若外部工具均未获取，说明原因并提供用户自查链接] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1217 | original/SKILL.md.txt:1217 | 模块 5：External Benchmarking（外部分类对标） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1219 | original/SKILL.md.txt:1219 | 模块 6：AI 判读决策报告（中文） | ### 模块 6：AI 判读决策报告（中文） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1221 | original/SKILL.md.txt:1221 | 模块 6：AI 判读决策报告（中文） | 这是整个输出的核心分析模块，使用简体中文深入阐述： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1223 | original/SKILL.md.txt:1223 | 模块 6：AI 判读决策报告（中文） | 内容包括： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1224 | original/SKILL.md.txt:1224 | 模块 6：AI 判读决策报告（中文） | - 变异的分子机制分析（该变异如何影响蛋白功能/基因表达） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1225 | original/SKILL.md.txt:1225 | 模块 6：AI 判读决策报告（中文） | - 群体频率数据的临床解读 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1226 | original/SKILL.md.txt:1226 | 模块 6：AI 判读决策报告（中文） | - 计算预测工具结果的整合分析 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1227 | original/SKILL.md.txt:1227 | 模块 6：AI 判读决策报告（中文） | - 证据链的内在逻辑关系 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1228 | original/SKILL.md.txt:1228 | 模块 6：AI 判读决策报告（中文） | - 判定结论的置信度讨论 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1229 | original/SKILL.md.txt:1229 | 模块 6：AI 判读决策报告（中文） | - 如存在不确定性，明确说明哪些额外证据可改变判定 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1230 | original/SKILL.md.txt:1230 | 模块 6：AI 判读决策报告（中文） | - 与 ClinVar/Franklin 评级的差异分析及证据取舍逻辑 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1232 | original/SKILL.md.txt:1232 | 模块 7：关联遗传病画像（中文） | ### 模块 7：关联遗传病画像（中文） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1234 | original/SKILL.md.txt:1234 | 模块 7：关联遗传病画像（中文） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1235 | original/SKILL.md.txt:1235 | 模块 7：关联遗传病画像（中文） | 【OMIM 关联疾病】 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1236 | original/SKILL.md.txt:1236 | 模块 7：关联遗传病画像（中文） |   - [疾病名称 (MIM#)] — [遗传方式] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1237 | original/SKILL.md.txt:1237 | 模块 7：关联遗传病画像（中文） |     核心临床特征：... | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1238 | original/SKILL.md.txt:1238 | 模块 7：关联遗传病画像（中文） |     产前可能观察到的表现：...（如适用） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1239 | original/SKILL.md.txt:1239 | 模块 7：关联遗传病画像（中文） |     发病年龄与外显率：... | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1241 | original/SKILL.md.txt:1241 | 模块 7：关联遗传病画像（中文） | 【基因型-表型相关性说明】 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1242 | original/SKILL.md.txt:1242 | 模块 7：关联遗传病画像（中文） |   该变异在已报道病例中的表型谱：... | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1243 | original/SKILL.md.txt:1243 | 模块 7：关联遗传病画像（中文） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1245 | original/SKILL.md.txt:1245 | 模块 8：临床可操作性建议（中文） | ### 模块 8：临床可操作性建议（中文） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1247 | original/SKILL.md.txt:1247 | 模块 8：临床可操作性建议（中文） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1248 | original/SKILL.md.txt:1248 | 模块 8：临床可操作性建议（中文） | 【产前咨询影响】（如适用于产前场景） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1249 | original/SKILL.md.txt:1249 | 模块 8：临床可操作性建议（中文） |   - 对当前妊娠的意义：... | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1250 | original/SKILL.md.txt:1250 | 模块 8：临床可操作性建议（中文） |   - 超声重点监测项目：... | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1251 | original/SKILL.md.txt:1251 | 模块 8：临床可操作性建议（中文） |   - 分娩方式及围生期管理建议：... | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1253 | original/SKILL.md.txt:1253 | 模块 8：临床可操作性建议（中文） | 【家系级联筛查建议】 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1254 | original/SKILL.md.txt:1254 | 模块 8：临床可操作性建议（中文） |   - 推荐检测的家系成员：... | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1255 | original/SKILL.md.txt:1255 | 模块 8：临床可操作性建议（中文） |   - 检测方法：... | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1257 | original/SKILL.md.txt:1257 | 模块 8：临床可操作性建议（中文） | 【后续行动建议】 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1258 | original/SKILL.md.txt:1258 | 模块 8：临床可操作性建议（中文） |   - 优先级1：... | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1259 | original/SKILL.md.txt:1259 | 模块 8：临床可操作性建议（中文） |   - 优先级2：... | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1260 | original/SKILL.md.txt:1260 | 模块 8：临床可操作性建议（中文） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1262 | original/SKILL.md.txt:1262 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） | ### 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1264 | original/SKILL.md.txt:1264 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） | **本模块在产前模式下替代通用模块8**，以预后维度重构临床建议，直接回答"出生后孩子会是什么表现"这一产前咨询核心问题。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1266 | original/SKILL.md.txt:1266 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1267 | original/SKILL.md.txt:1267 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） | ═══════════════════════════════════════════════════════ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1268 | original/SKILL.md.txt:1268 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   产前预后评估矩阵 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1269 | original/SKILL.md.txt:1269 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   基因：[基因名] \| 变异：[变异名] \| 最近参照：[Step 0.6结果] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1270 | original/SKILL.md.txt:1270 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） | ═══════════════════════════════════════════════════════ | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1272 | original/SKILL.md.txt:1272 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） | 【产前可检出项目（影像/临床）】 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1274 | original/SKILL.md.txt:1274 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   检查项目             预测方向        风险等级    证据来源 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1275 | original/SKILL.md.txt:1275 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   ───────────────────────────────────────────────────── | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1276 | original/SKILL.md.txt:1276 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   颅脑 MRI（皮质发育）  [正常/异常/不确定]  [高/中/低]  [文献/域定位] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1277 | original/SKILL.md.txt:1277 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   脑室大小             [正常/扩大风险]    [高/中/低]  [文献] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1278 | original/SKILL.md.txt:1278 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   胼胝体形态           [正常/异常风险]    [高/中/低]  [文献] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1279 | original/SKILL.md.txt:1279 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   胎动质量             [正常/减少风险]    [高/中/低]  [文献] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1280 | original/SKILL.md.txt:1280 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   足部姿态/挛缩        [正常/异常风险]    [高/中/低]  [文献] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1281 | original/SKILL.md.txt:1281 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   羊水量               [正常/过多风险]    [高/中/低]  [文献] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1283 | original/SKILL.md.txt:1283 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   注：高 = 文献报道率 >30%；中 = 10-30%；低 = <10% 或仅有报告 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1285 | original/SKILL.md.txt:1285 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） | 【出生后预期表型谱（基于同域/邻近变异文献）】 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1287 | original/SKILL.md.txt:1287 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   表型维度             预期风险         参照依据 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1288 | original/SKILL.md.txt:1288 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   ───────────────────────────────────────────────────── | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1289 | original/SKILL.md.txt:1289 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   智力障碍/全面发育迟缓  [高/中/低/不确定]  [最近邻近变异表型 + 域规律] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1290 | original/SKILL.md.txt:1290 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   ASD 倾向             [高/中/低/不确定]  [同域文献] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1291 | original/SKILL.md.txt:1291 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   癫痫（难治性）        [高/中/低/不确定]  [同域文献，注明起病年龄范围] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1292 | original/SKILL.md.txt:1292 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   运动功能             [受损/轻微/不确定]  [文献] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1293 | original/SKILL.md.txt:1293 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   语言发育             [严重受损/轻度/不确定] [文献] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1295 | original/SKILL.md.txt:1295 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   ⚠️ 重要提示：以上预测基于邻近位点参照推断，本例变异为首次报道， | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1296 | original/SKILL.md.txt:1296 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   个体表型可能存在显著差异。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1298 | original/SKILL.md.txt:1298 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） | 【产前检查行动计划】 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1300 | original/SKILL.md.txt:1300 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   优先级1（立即）：[最关键的单一检查，如 胎儿颅脑 MRI] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1301 | original/SKILL.md.txt:1301 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |                    建议孕周：[X周]；检查目标：[具体评估项目] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1303 | original/SKILL.md.txt:1303 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   优先级2（近期）：[第二重要检查] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1304 | original/SKILL.md.txt:1304 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |                    建议孕周：[X周]；检查目标：[具体评估项目] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1306 | original/SKILL.md.txt:1306 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   优先级3（持续）：[动态监测项目] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1307 | original/SKILL.md.txt:1307 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |                    频率建议：[每N周一次]；监测指标：[列表] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1309 | original/SKILL.md.txt:1309 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） | 【遗传咨询告知框架（供咨询师参考）】 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1311 | original/SKILL.md.txt:1311 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   告知层次1（基本）：变异的致病性分类及其含义 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1312 | original/SKILL.md.txt:1312 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   告知层次2（预后）：出生后预期表型谱及不确定性范围 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1313 | original/SKILL.md.txt:1313 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   告知层次3（应对）：产前检查计划 + 出生后多学科随访方案 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1314 | original/SKILL.md.txt:1314 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   再发风险（按实际情形分支，不套固定值）： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1315 | original/SKILL.md.txt:1315 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |     · 生殖细胞 de novo（双亲 VAF 0）→ 低但不为零，亲代生殖腺嵌合无法用外周血排除 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1316 | original/SKILL.md.txt:1316 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |     · 胎儿合子后嵌合 → 更低；亲代生殖腺嵌合上限按双亲 alt 读段 0/N 估算 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1317 | original/SKILL.md.txt:1317 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |     · 亲代杂合（VAF 40–60%）→ AD 50% / AR 25% / X 连锁按母亲携带与胎儿性别 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1318 | original/SKILL.md.txt:1318 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |     · 亲代体细胞嵌合 → 介于新发经验值与 50% 之间，写区间，建议多组织定量 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1319 | original/SKILL.md.txt:1319 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |     · 印记基因 → 按传递亲本性别 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1320 | original/SKILL.md.txt:1320 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   再生育方案：自然受孕 + 早孕期产前诊断 / PGT-M（需家系单倍型构建） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1321 | original/SKILL.md.txt:1321 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   超声表型归因：[落在谱内且特异 / 落在谱内但不特异 / 未报道 / 方向相反]；其他病因排查是否继续：[是/否] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1322 | original/SKILL.md.txt:1322 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   决策边界表述（VUS 时必填）：[如"当前证据不足以支持将本变异作为终止妊娠的依据"] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1323 | original/SKILL.md.txt:1323 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   再分析时点：[孕周 / 产后 / 引产后尸检 / 新证据触发] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1325 | original/SKILL.md.txt:1325 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） | 【家系级联筛查建议】 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1326 | original/SKILL.md.txt:1326 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   推荐检测的家系成员：[列表] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1327 | original/SKILL.md.txt:1327 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   检测方法：[Sanger/panel/WES] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1328 | original/SKILL.md.txt:1328 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   亲代自身健康提示与知情同意边界：[如亲代携带 HI=3 基因 null 等位可能为未诊断患者] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1329 | original/SKILL.md.txt:1329 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |   意外/次要发现与携带状态处理：[依检测前知情同意；夫妇共同携带 AR 病 P/LP 以再生育风险告知] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1331 | original/SKILL.md.txt:1331 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） | Re-evaluation triggers: [新知识 / 新表型 / 家族成员检测 / 进一步临床检查 / 指南版本变更] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1332 | original/SKILL.md.txt:1332 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） | Evidence snapshot:      [数据库版本与检索日期] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1333 | original/SKILL.md.txt:1333 | 模块 8'：产前预后矩阵（仅产前模式输出，替代模块8） |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1335 | original/SKILL.md.txt:1335 | 模块 9：References | ### 模块 9：References | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1337 | original/SKILL.md.txt:1337 | 模块 9：References | 本模块在生成完毕后**必须执行 Step 9-Verify 反查验证**。验证后的标准输出格式如下： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1339 | original/SKILL.md.txt:1339 | 模块 9：References |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1340 | original/SKILL.md.txt:1340 | 模块 9：References | [1] Author et al. (Year). Title. Journal. PMID: XXXXXXXX  [✓ 已核验] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1341 | original/SKILL.md.txt:1341 | 模块 9：References |     💡 Insight (中文): [该文献的核心结论，一句话概括] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1343 | original/SKILL.md.txt:1343 | 模块 9：References | [2] Author et al. (Year). Title. Journal. PMID: XXXXXXXX  [✓ 已核验 / 已更正] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1344 | original/SKILL.md.txt:1344 | 模块 9：References |     💡 Insight (中文): [核心结论] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1345 | original/SKILL.md.txt:1345 | 模块 9：References |     ⚠️ 反查更正说明：[如适用，简要说明更正了什么，如"原引文将作者 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1346 | original/SKILL.md.txt:1346 | 模块 9：References |        误标为 XX，PMID 反查后确认实际作者为 YY"] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1348 | original/SKILL.md.txt:1348 | 模块 9：References | ... | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1350 | original/SKILL.md.txt:1350 | 模块 9：References | ── 参考文献反查验证结果 ────────────────────────────────── | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1351 | original/SKILL.md.txt:1351 | 模块 9：References | 反查执行日期:        [YYYY-MM-DD] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1352 | original/SKILL.md.txt:1352 | 模块 9：References | 引用文献总数:        [N] 条 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1353 | original/SKILL.md.txt:1353 | 模块 9：References | 通过验证条数:        [N] 条 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1354 | original/SKILL.md.txt:1354 | 模块 9：References | 更正条数:            [N] 条 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1355 | original/SKILL.md.txt:1355 | 模块 9：References | 删除条数:            [N] 条 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1356 | original/SKILL.md.txt:1356 | 模块 9：References | 反查覆盖率:          100% | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1358 | original/SKILL.md.txt:1358 | 模块 9：References | ⚠️ 反查发现的关键修正（如适用）: | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1359 | original/SKILL.md.txt:1359 | 模块 9：References |   · [修正1的简要说明] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1360 | original/SKILL.md.txt:1360 | 模块 9：References |   · [修正2的简要说明] | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1361 | original/SKILL.md.txt:1361 | 模块 9：References |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1363 | original/SKILL.md.txt:1363 | 模块 9：References | **标注规则**： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1364 | original/SKILL.md.txt:1364 | 模块 9：References | - [✓ 已核验] — 引文经 PMID 反查，作者、期刊、年份、PMID 均一致 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1365 | original/SKILL.md.txt:1365 | 模块 9：References | - [✓ 已核验 / 已更正] — 经反查发现错误，已根据 PubMed 元数据更正，需附说明 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1366 | original/SKILL.md.txt:1366 | 模块 9：References | - [⚠️ 部分未验证] — 工具调用受限导致无法完整验证，需在模块10中明确说明 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1368 | original/SKILL.md.txt:1368 | 模块 9：References | **禁止输出**：未带任何反查标注的参考文献条目（即未执行 Step 9-Verify 的输出格式）。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1370 | original/SKILL.md.txt:1370 | 模块 10：局限性声明 | ### 模块 10：局限性声明 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1372 | original/SKILL.md.txt:1372 | 模块 10：局限性声明 | 每次输出末尾自动附加： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1374 | original/SKILL.md.txt:1374 | 模块 10：局限性声明 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1375 | original/SKILL.md.txt:1375 | 模块 10：局限性声明 | ⚠️ 重要声明： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1376 | original/SKILL.md.txt:1376 | 模块 10：局限性声明 | 1. 本报告包含 AI 生成的内容，所有结论需经认证临床遗传学家/遗传咨询师审核确认后方可用于临床决策。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1377 | original/SKILL.md.txt:1377 | 模块 10：局限性声明 |    ⛔ 本条措辞逐字固定，不得改写为“本分析由 AI 辅助生成”“AI 辅助分析”等表述。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1378 | original/SKILL.md.txt:1378 | 模块 10：局限性声明 | 2. 数据库检索时效性：本次检索基于 [日期] 的可用数据，ClinVar、gnomAD 等数据库持续更新， | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1379 | original/SKILL.md.txt:1379 | 模块 10：局限性声明 |    关键决策前建议实时查询最新版本。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1380 | original/SKILL.md.txt:1380 | 模块 10：局限性声明 | 3. 数据完整性：标注 ⚠️ 或 ❌ 的检索项未能完整获取，相关证据评估可能受影响。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1381 | original/SKILL.md.txt:1381 | 模块 10：局限性声明 | 4. 本分析不构成医疗诊断或治疗建议，具体临床决策请结合完整病史和多学科讨论。本分析不负责妊娠决策、胎儿管理与家属最终决定。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1382 | original/SKILL.md.txt:1382 | 模块 10：局限性声明 | 5. [产前阴性/未见致病变异时] 覆盖条件：目标基因/区域 ≥20× 覆盖比例 [X%]；盲区基因/不可评估类别 [列表]；检测范围外的变异类型（重复扩展、mtDNA、低比例嵌合、平衡易位 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1383 | original/SKILL.md.txt:1383 | 模块 10：局限性声明 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1385 | original/SKILL.md.txt:1385 | 模块 10：局限性声明 | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1387 | original/SKILL.md.txt:1387 | 批量处理规则 | ## 批量处理规则 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1389 | original/SKILL.md.txt:1389 | 批量处理规则 | 当用户提供多个变异时： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1390 | original/SKILL.md.txt:1390 | 批量处理规则 | 1. 按序逐个完成完整分析 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1391 | original/SKILL.md.txt:1391 | 批量处理规则 | 2. 在所有变异分析完成后，附加一个汇总表格： | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1393 | original/SKILL.md.txt:1393 | 批量处理规则 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1394 | original/SKILL.md.txt:1394 | 批量处理规则 | \| # \| Gene \| Variant \| Classification \| Key Evidence \| gnomAD AF \| REVEL \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1395 | original/SKILL.md.txt:1395 | 批量处理规则 | \|---\|------\|---------\|---------------\|-------------\|-----------\|-------\| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1396 | original/SKILL.md.txt:1396 | 批量处理规则 | \| 1 \| ...  \| ...     \| ...           \| ...         \| ...       \| ...   \| | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1397 | original/SKILL.md.txt:1397 | 批量处理规则 |  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1399 | original/SKILL.md.txt:1399 | 批量处理规则 | 3. 若变异位于同一基因且为复合杂合，需额外讨论两个变异的联合致病性（须先定相，见 Step 5.1） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1400 | original/SKILL.md.txt:1400 | 批量处理规则 | 4. 汇总表增加 Report placement 列（主表 / 附表 / 不报） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1401 | original/SKILL.md.txt:1401 | 批量处理规则 | 5. 多基因多变异：每个变异独立评级，PP4 只按该基因能解释的那部分表型赋值；两基因均 P/LP 且表型互补 → 报"双重诊断"并分别给再发风险；双基因/修饰基因组合不得强推 P（ACMG | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1403 | original/SKILL.md.txt:1403 | 批量处理规则 | --- | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1405 | original/SKILL.md.txt:1405 | 关键原则提醒 | ## 关键原则提醒 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1407 | original/SKILL.md.txt:1407 | 关键原则提醒 | 1. **数据驱动**：所有证据代码赋值必须有对应的数据支持，不可凭推测赋予证据代码 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1408 | original/SKILL.md.txt:1408 | 关键原则提醒 | 2. **透明度**：检索失败或数据缺失时必须如实标注，不可伪造数据 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1409 | original/SKILL.md.txt:1409 | 关键原则提醒 | 3. **保守性**：在证据不充分时倾向于 VUS，而非过度判定致病或良性 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1410 | original/SKILL.md.txt:1410 | 关键原则提醒 | 4. **可追溯**：每个判定步骤的数据来源需可追溯（URL、PMID、数据库版本） | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1411 | original/SKILL.md.txt:1411 | 关键原则提醒 | 5. **双语规范**：模块1/2使用英文标签，模块3全中文输出（含标签和理由），模块4-10按各自规则 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1412 | original/SKILL.md.txt:1412 | 关键原则提醒 | 6. **基因特异性优先 + VCEP 全文门控**：若该基因有 ClinGen VCEP 定制规则，必须优先采用，不可忽略。且**"知道有规则"不等于"可以套用规则"——必须按 Step  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1413 | original/SKILL.md.txt:1413 | 关键原则提醒 | 7. **检索效率与可靠性**：优先 web_search 获取信息和定位 URL，再对可 fetch 的静态页面（ClinVar Variation 页面、PubMed、OMIM、UniP | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1414 | original/SKILL.md.txt:1414 | 关键原则提醒 | 8. **禁止推导关键注释信息**：蛋白改变（HGVSp）、变异类型（missense/nonsense等）、基因组坐标等关键注释信息不可通过 AI 心算推导获得，必须通过外部注释工具（Va | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1415 | original/SKILL.md.txt:1415 | 关键原则提醒 | 9. **Novel Variant 地形感知**：当 ClinVar 无精确记录时，禁止直接跳入计算预测评分填充证据。必须先执行 Step 0.6 邻近位点扩圈检索，建立"最近已知参照点" | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1416 | original/SKILL.md.txt:1416 | 关键原则提醒 | 10. **产前场景专项**：产前模式下，"致病性分类"和"预后预测"是两个独立的临床问题，必须分别回答。ACMG 分类回答"变异是否致病"；Step 0.6-0.7 和模块8'专门回答"出 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1417 | original/SKILL.md.txt:1417 | 关键原则提醒 | 11. **参考文献零容忍**：模块9 中每一条参考文献都必须经过 Step 9-Verify 的 PMID 反查验证，确保作者、期刊、年份、PMID 四要素与 PubMed 元数据完全一致 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1418 | original/SKILL.md.txt:1418 | 关键原则提醒 | 12. **PVS1 四级分层强制**：PVS1 绝不一刀切赋 Very Strong。必须先确认三个前提门槛（机制为 LOF / null 型变异 / 临床相关组成型外显子），再依 NMD | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1419 | original/SKILL.md.txt:1419 | 关键原则提醒 | 13. **证据优先级与矛盾处理**：存在致病与良性证据冲突时，按"人群频率 > 功能验证 > 家系 > 相位 > 结构 > 计算预测"权衡，不机械相加。BA1 一票否决（亚效等位例外见 § | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1420 | original/SKILL.md.txt:1420 | 关键原则提醒 | 14. **功能证据门槛**：PS3/BS3 需 OddsPath 量化（分档 >18.7 Strong / 4.3–18.7 Moderate / 2.1–4.3 Supporting）、 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1421 | original/SKILL.md.txt:1421 | 关键原则提醒 | 15. **PP4 产前保守**：产前 PP4 适用范围窄（HPO 仅约 10% 适用产前、基因座异质性普遍）。PS2/PM6 已用则不叠加 PP4。多基因候选按比例分摊、封顶 +5。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1422 | original/SKILL.md.txt:1422 | 关键原则提醒 | 16. **高频亚效单倍型警觉**：产前检出单杂合 LOF 时主动核查是否存在人群高频亚效单倍型（TBX6 范式），高频不等于良性。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1423 | original/SKILL.md.txt:1423 | 关键原则提醒 | 17. **CNV 独立框架**：CNV 用 ClinGen 五段式评分（references/CNV_CRITERIA.md），4O 人群频率减分对覆盖 AR 致病基因的区域慎用。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1424 | original/SKILL.md.txt:1424 | 关键原则提醒 | 18. 🤰 **产前 de novo 量化强制**：凡产前场景出现 de novo 变异（胎儿 trio-WES/WGS 检出），PS2/PM6 强度**必须**用 ClinGen SVI  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1425 | original/SKILL.md.txt:1425 | 关键原则提醒 | 19. **PM1 三门槛强制（AI 最易滥用）**：赋 PM1 前必须满足三道并列门槛——①功能"已确立"（实验证实，**非** Pfam/InterPro 序列注释）②**主动查 gno | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1426 | original/SKILL.md.txt:1426 | 关键原则提醒 | 20. **Step 0.4 三源优先但不越权**：本轮优先用 Step 0.4 一次性坍缩取数（VariantValidator 双坐标 + GeneBe ClinVar/ACMG + 五 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1427 | original/SKILL.md.txt:1427 | 关键原则提醒 | 21. ⟦培训班⟧ **两条证据与 GUS 封顶**：除 BA1 外任何 LB/LP/P 至少两条独立证据；基因-疾病有效性 ≤ Limited 的基因封顶 VUS；积分阈值按 Tavtig | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1428 | original/SKILL.md.txt:1428 | 关键原则提醒 | 22. ⟦培训班⟧ **产前三道前置门**：MCC 定量、VAF/嵌合核查、高同源区可比对性——未过门不谈证据；胎儿合子后嵌合与亲代嵌合改写再发风险，不套"de novo ~1% / AD  | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1429 | original/SKILL.md.txt:1429 | 关键原则提醒 | 23. ⟦培训班⟧ **遗传自"健康"亲代 ≠ 良性证据**：亲代须完成基因特异靶向评估且 VAF 40–60% 才可作 BS2/BS4；外显不全疾病产前不赋 BS2；印记基因沉默亲本、性别 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1430 | original/SKILL.md.txt:1430 | 关键原则提醒 | 24. ⟦培训班⟧ **报告层规范**：Step 6 的报/不报决策、措辞五禁、决策边界句、再评估触发与表型吻合度陈述在产前模式为强制输出；"致病 ≠ 病因"，找到致病变异后寻找不停止。 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| S-1431 | original/SKILL.md.txt:1431 | 关键原则提醒 | 25. ⟦培训班⟧ **PS1/PM5/PM4/BP3/PP2/BP1/BP2/BP5 按 ACMG_CRITERIA.md §1.10 / §3.6 / §4.6 定义赋值**：PM5 严 | references/WORKFLOW.md | 原需求保留；按迁移工作流适配，原阈值/指令不自动启用 |
| A-0001 | original/ACMG_CRITERIA.md:1 | ACMG/AMP 证据代码定义与判定规则（SNV/Indel） | # ACMG/AMP 证据代码定义与判定规则（SNV/Indel） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0003 | original/ACMG_CRITERIA.md:3 | ACMG/AMP 证据代码定义与判定规则（SNV/Indel） | > 本文件是 gene-variant-pathogenicity 技能的核心参考。在执行 ACMG 判定前必须阅读。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0004 | original/ACMG_CRITERIA.md:4 | ACMG/AMP 证据代码定义与判定规则（SNV/Indel） | > 内容整合 ACMG/AMP 2015、ClinGen SVI 系列更新（PVS1 2018 / PM2 2020 / 剪接 2023）、 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0005 | original/ACMG_CRITERIA.md:5 | ACMG/AMP 证据代码定义与判定规则（SNV/Indel） | > ACGS 2024 v1.2 最佳实践，产前胎儿医学专家共识备课会（2026-05）的实操意见， | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0006 | original/ACMG_CRITERIA.md:6 | ACMG/AMP 证据代码定义与判定规则（SNV/Indel） | > 以及第一期产前基因变异解读培训班（2026-09-04～06，15 位讲者正式课件）的复核与补充。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0007 | original/ACMG_CRITERIA.md:7 | ACMG/AMP 证据代码定义与判定规则（SNV/Indel） | > | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0008 | original/ACMG_CRITERIA.md:8 | ACMG/AMP 证据代码定义与判定规则（SNV/Indel） | > **产前场景标记**：标注 🤰 的条目为产前专项规则，与通用规则有差异，产前模式下优先适用。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0009 | original/ACMG_CRITERIA.md:9 | ACMG/AMP 证据代码定义与判定规则（SNV/Indel） | > **2026-09 复核记号**：标注 ⟦培训班⟧ 的条目为本次培训班课件校正或新增的规则。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0011 | original/ACMG_CRITERIA.md:11 | ACMG/AMP 证据代码定义与判定规则（SNV/Indel） | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0013 | original/ACMG_CRITERIA.md:13 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | ## 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0015 | original/ACMG_CRITERIA.md:15 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | \| 强度等级 \| 致病侧积分 \| 良性侧积分 \| OddsPath（单条） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0016 | original/ACMG_CRITERIA.md:16 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | \|---------\|-----------\|-----------\|-----------------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0017 | original/ACMG_CRITERIA.md:17 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | \| Very Strong (PVS) \| +8 \| -8 \| 350 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0018 | original/ACMG_CRITERIA.md:18 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | \| Strong (PS) \| +4 \| -4 \| 18.7 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0019 | original/ACMG_CRITERIA.md:19 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | \| Moderate (PM) \| +2 \| -2 \| 4.33 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0020 | original/ACMG_CRITERIA.md:20 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | \| Supporting (PP) \| +1 \| -1 \| 2.08 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0022 | original/ACMG_CRITERIA.md:22 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | **Bayesian 底层逻辑**：1 个非常强 ≈ 2 个强 ≈ 4 个中等 ≈ 8 个支持；不同强度间为指数关系（指数底=2.0）。组合时证据**比值（Odds）相乘**，等价于积分相加 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0024 | original/ACMG_CRITERIA.md:24 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | **判定阈值（积分制，Tavtigian 2020 PMID:32720330 官方值）** ⟦培训班⟧： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0025 | original/ACMG_CRITERIA.md:25 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | - Pathogenic：≥ +10 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0026 | original/ACMG_CRITERIA.md:26 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | - Likely Pathogenic：+6 ~ +9 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0027 | original/ACMG_CRITERIA.md:27 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | - VUS：0 ~ +5 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0028 | original/ACMG_CRITERIA.md:28 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | - Likely Benign：-1 ~ -6 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0029 | original/ACMG_CRITERIA.md:29 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | - Benign：≤ -7 或 BA1 单独成立 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0031 | original/ACMG_CRITERIA.md:31 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | > 旧版本此表误写为 VUS -1～+5 / LB -6～-2，与本节下文"官方 -1"自相矛盾，2026-09 已按官方值更正。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0033 | original/ACMG_CRITERIA.md:33 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | **"至少两条证据"硬规则** ⟦培训班⟧：除 BA1 可独立判良性外，任何 LB/LP/P 分类都至少需要**两条独立证据**。只有一条证据时（如单独 PVS1 = +8，或单独 BP4  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0035 | original/ACMG_CRITERIA.md:35 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | **已知的两个自相矛盾组合规则（高勇报告，需人工警惕）**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0036 | original/ACMG_CRITERIA.md:36 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | 1. 致病规则 (ii) 两个 Strong（+8）→ 概率约 97.5%，实际落在 LP 与 P 之间。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0037 | original/ACMG_CRITERIA.md:37 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | 2. 可能致病规则 (i) 一个 Very Strong + 一个 Moderate（+10）→ 概率约 99.4%，实际已达 P 水平。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0039 | original/ACMG_CRITERIA.md:39 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | **LB 下界的稳健性提示**：净积分恰为 -1（仅一条 Supporting 良性证据）时按官方值为 LB，但已被"至少两条证据"规则挡回 VUS；净积分 -2 且唯一来源为计算预测 BP | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0041 | original/ACMG_CRITERIA.md:41 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | **先验概率不锁定的例外**：大 panel/健康体检者场景真实先验可 <1%（系统会高估）；高外显率 AD 基因 + 明确家族史场景先验可 >50%（系统会低估）。0.10–0.32 区间 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0043 | original/ACMG_CRITERIA.md:43 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | **分类档位敏感性分析** ⟦培训班⟧：当任一证据存在相邻两档争议（如 PS2 原级 vs PS2_Moderate）且改档会跨分类线时，报告须同时输出积分区间与两种分类（如"+9～+11， | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0045 | original/ACMG_CRITERIA.md:45 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | **基因-疾病有效性上限（GUS 封顶）** ⟦培训班⟧：ClinGen/GenCC 基因-疾病有效性为 Limited、No Known Disease Relationship、Disp | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0047 | original/ACMG_CRITERIA.md:47 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | **VUS 内部亚分档（仅内部/附表，不进分类栏）** ⟦培训班⟧：VUS-High（偏致病侧，净积分 +3～+5 或有单条 Strong 以上证据但缺第二条）/ VUS-Mid（0～+2  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0049 | original/ACMG_CRITERIA.md:49 | 0. 证据强度与 Bayesian 积分对照（高勇报告，2026-09 正式版复核） | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0051 | original/ACMG_CRITERIA.md:51 | 1. PVS1：功能丧失型变异（最复杂，四级决策树） | ## 1. PVS1：功能丧失型变异（最复杂，四级决策树） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0053 | original/ACMG_CRITERIA.md:53 | 1.1 三个前提门槛（缺一不可 — 李茹/PVS1课件） | ### 1.1 三个前提门槛（缺一不可 — 李茹/PVS1课件） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0055 | original/ACMG_CRITERIA.md:55 | 1.1 三个前提门槛（缺一不可 — 李茹/PVS1课件） | 赋 PVS1 前必须依次确认： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0057 | original/ACMG_CRITERIA.md:57 | 1.1 三个前提门槛（缺一不可 — 李茹/PVS1课件） | 1. **疾病机制确为 LOF**（见 1.2 判定法） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0058 | original/ACMG_CRITERIA.md:58 | 1.1 三个前提门槛（缺一不可 — 李茹/PVS1课件） | 2. **变异确为 null 型**：无义、移码、经典 ±1/2 剪接、起始密码子、单/多外显子缺失或基因内重复、终止密码子丢失 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0059 | original/ACMG_CRITERIA.md:59 | 1.1 三个前提门槛（缺一不可 — 李茹/PVS1课件） | 3. **变异落在临床相关转录本的组成型外显子**：MANE Select (plus Clinical) 优先；但 MANE 不是唯一相关转录本，MANE 上的外显子不一定都是组成型——必 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0061 | original/ACMG_CRITERIA.md:61 | 1.1 三个前提门槛（缺一不可 — 李茹/PVS1课件） | **不适用 PVS1 的情形**：机制非 LOF；无证据表明 LOF 致病；无 RNA 证据的非经典剪接位点变异；可产生补救转录本的剪接变异；无 RNA 证据且 SpliceAI Δ<0.8 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0063 | original/ACMG_CRITERIA.md:63 | 1.1 三个前提门槛（缺一不可 — 李茹/PVS1课件） | **互斥**：PVS1 不与 PM1、PM4、PP2、PP3 共用。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0065 | original/ACMG_CRITERIA.md:65 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | ### 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0067 | original/ACMG_CRITERIA.md:67 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | **判定优先级：数据库证据 > 预测值** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0069 | original/ACMG_CRITERIA.md:69 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | 1. **ClinGen Gene-Disease Validity**（首选）：分类为 Definitive/Strong 是适用 PVS1 原级的前提之一 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0070 | original/ACMG_CRITERIA.md:70 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） |    - 查询：https://search.clinicalgenome.org/kb/gene-validity ；补充 GenCC https://thegencc.org/ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0071 | original/ACMG_CRITERIA.md:71 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | 2. **ClinGen Dosage Sensitivity HI Score**（首选）： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0072 | original/ACMG_CRITERIA.md:72 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） |    - 查询：https://search.clinicalgenome.org/kb/gene-dosage | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0073 | original/ACMG_CRITERIA.md:73 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） |    - **HI=3** → 充分证据，LOF/单倍剂量不足即致病机制 → 支持 PVS1 原级 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0074 | original/ACMG_CRITERIA.md:74 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） |    - HI=2 → 部分证据（2019-02 后评估的可考虑） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0075 | original/ACMG_CRITERIA.md:75 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） |    - HI=1/0 → 证据不足 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0076 | original/ACMG_CRITERIA.md:76 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） |    - **HI=30** → 该基因为常染色体隐性遗传相关，绝大多数机制为 LOF | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0077 | original/ACMG_CRITERIA.md:77 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） |    - **HI=40** → 剂量不敏感，缺失不致病 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0078 | original/ACMG_CRITERIA.md:78 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） |    - HI=-1 → 不评定（如假基因） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0079 | original/ACMG_CRITERIA.md:79 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | 3. **变异类型及分布**（PVS1 原级要求）：基因-疾病有效性强/明确 **且** ≥3 个 LOF 变异已在**不使用 PVS1 的前提下**被独立判定为致病（SVI 2018 原意 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0080 | original/ACMG_CRITERIA.md:80 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | 4. **ClinVar/HGMD P/LP 变异类型分布**（经验证据，置于预测值之前）⟦培训班⟧：截短变异 P/LP 遍布全基因 → 支持 HI/LOF（如 TET3）；P/LP 以错义 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0081 | original/ACMG_CRITERIA.md:81 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | 5. **预测值（仅辅助，不可单独定机制 — PVS1课件明确警告）**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0082 | original/ACMG_CRITERIA.md:82 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） |    - pLI ≥0.9（o/e <0.35） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0083 | original/ACMG_CRITERIA.md:83 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） |    - LOEUF <0.6（gnomAD v4.1；v2 时代为 <0.35） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0084 | original/ACMG_CRITERIA.md:84 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） |    - pHaplo ≥0.86（DECIPHER） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0085 | original/ACMG_CRITERIA.md:85 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） |    - ⚠️ **预测值陷阱**：BRCA1 明确为单倍剂量不足致病（HI=3），但 pLI=0、LOEUF=0.73。**使用预测值时必须考虑外显率、严重程度、发病年龄；晚发/轻症疾病可 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0087 | original/ACMG_CRITERIA.md:87 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | **机制对照参考**（PMID:36806206，"孟德尔遗传-显隐性致病机制"）： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0088 | original/ACMG_CRITERIA.md:88 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | - LOF：等位基因/mRNA/蛋白丢失，最常见；多为隐性；单倍剂量不足时为显性 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0089 | original/ACMG_CRITERIA.md:89 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | - GOF（功能获得）：蛋白获得异常/新功能，如 FGFR3, SOS1, MYOC, MEFV | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0090 | original/ACMG_CRITERIA.md:90 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | - 显性负效应（dominant-negative）：变异干扰野生型蛋白，多聚体蛋白需重点考虑，如 COL1A2, KCTD1, GHR, POU1F1, GH1, THRB | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0092 | original/ACMG_CRITERIA.md:92 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | **一基因多机制警示（PVS1课件 — 努南综合征/LZTR1 实例）**：同一基因在不同遗传模式下机制可相反。LZTR1：NS10（AD）为 GOF（变异聚集 KT1-4 域），NS2（A | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0094 | original/ACMG_CRITERIA.md:94 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | **基因-疾病有效性等级 → PVS1 上限** ⟦培训班⟧（王明明/阴凯丽 MIPEP、蒋 TBX2；PMID:30192042）： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0096 | original/ACMG_CRITERIA.md:96 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | \| ClinGen/GenCC 有效性 \| 附加条件 \| PVS1 上限 \| 最终分类上限 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0097 | original/ACMG_CRITERIA.md:97 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | \|---\|---\|---\|---\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0098 | original/ACMG_CRITERIA.md:98 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | \| Definitive / Strong \| 满足上文第 3 条分布要求 \| 原级 (Very Strong) \| 无 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0099 | original/ACMG_CRITERIA.md:99 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | \| Moderate \| ≥2 个表型相关 LOF 报道（分布 >1 外显子）**且** 动物敲除重现表型 \| PVS1_Strong \| LP 可达 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0100 | original/ACMG_CRITERIA.md:100 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | \| Moderate \| 仅满足上述其一 \| PVS1_Moderate \| LP 可达（需其他证据） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0101 | original/ACMG_CRITERIA.md:101 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | \| Limited / Disputed / 无 \| — \| 不适用 \| **VUS**（§0 GUS 封顶） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0103 | original/ACMG_CRITERIA.md:103 | 1.2 LOF 致病机制判定（按可靠性排序，李茹/PVS1课件） | **两条前提陷阱** ⟦培训班⟧：①双等位 LOF 胚胎致死的基因在人群/患者中检不到 LOF，"无 LOF 证据"≠"LOF 不致病"，此时 PVS1 只能不适用并注明原因；②AD 基因即 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0105 | original/ACMG_CRITERIA.md:105 | 1.3 NMD 预测（决定 PVS1 强度 — 李茹决策树） | ### 1.3 NMD 预测（决定 PVS1 强度 — 李茹决策树） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0107 | original/ACMG_CRITERIA.md:107 | 1.3 NMD 预测（决定 PVS1 强度 — 李茹决策树） | 决定性因素：**PTC 所在转录本和位置** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0109 | original/ACMG_CRITERIA.md:109 | 1.3 NMD 预测（决定 PVS1 强度 — 李茹决策树） | \| PTC 位置 \| NMD 预测 \| PVS1 强度 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0110 | original/ACMG_CRITERIA.md:110 | 1.3 NMD 预测（决定 PVS1 强度 — 李茹决策树） | \|---------\|---------\|----------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0111 | original/ACMG_CRITERIA.md:111 | 1.3 NMD 预测（决定 PVS1 强度 — 李茹决策树） | \| 靠前或中间外显子（其余位置） \| 是，被降解 \| **PVS1 原级（Very Strong）** \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0112 | original/ACMG_CRITERIA.md:112 | 1.3 NMD 预测（决定 PVS1 强度 — 李茹决策树） | \| 最后一个外显子 \| 否（NMD 逃逸） \| 按 §1.4.1 子分支定级（Strong / Moderate / N/A） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0113 | original/ACMG_CRITERIA.md:113 | 1.3 NMD 预测（决定 PVS1 强度 — 李茹决策树） | \| 倒数第二外显子最后 50bp 内 \| 否（NMD 逃逸） \| 同上 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0114 | original/ACMG_CRITERIA.md:114 | 1.3 NMD 预测（决定 PVS1 强度 — 李茹决策树） | \| 距翻译起始 <100bp（靠近 5'端） \| 常逃逸（可用下游 AUG 重启翻译） \| 慎用，功能验证或降级 Moderate/Supporting \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0116 | original/ACMG_CRITERIA.md:116 | 1.3 NMD 预测（决定 PVS1 强度 — 李茹决策树） | **NMD 机制细节（PVS1课件）**：从起始密码子前 ~100-200bp 的无义变异罕见为 NMD 靶点（可用潜在起始密码子重启）；NMD 效率在起始密码子下游前 200bp 逐渐增加 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0117 | original/ACMG_CRITERIA.md:117 | 1.3 NMD 预测（决定 PVS1 强度 — 李茹决策树） | **经典反例**：BRCA2 c.9976A>T (p.Lys3326*) 位于最后一个外显子，丢失末 93 个氨基酸但不增加乳腺癌风险，评为良性（BA1, BS3, BP5_VeryStr | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0119 | original/ACMG_CRITERIA.md:119 | 1.3 NMD 预测（决定 PVS1 强度 — 李茹决策树） | **操作提示（转录本坐标陷阱）** ⟦培训班⟧：DECIPHER 等工具的 NMD 逃逸区/50bp 规则可能标注在非 MANE 转录本上（PKP2：NM_004572 14 外显子 vs  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0121 | original/ACMG_CRITERIA.md:121 | 1.4.1 NMD 逃逸（无义/移码）后的子分支 ⟦培训班⟧（SVI 2018 决策树 + Walker 2023） | #### 1.4.1 NMD 逃逸（无义/移码）后的子分支 ⟦培训班⟧（SVI 2018 决策树 + Walker 2023） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0123 | original/ACMG_CRITERIA.md:123 | 1.4.1 NMD 逃逸（无义/移码）后的子分支 ⟦培训班⟧（SVI 2018 决策树 + Walker 2023） |  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0124 | original/ACMG_CRITERIA.md:124 | 1.4.1 NMD 逃逸（无义/移码）后的子分支 ⟦培训班⟧（SVI 2018 决策树 + Walker 2023） | 预计不发生 NMD → | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0125 | original/ACMG_CRITERIA.md:125 | 1.4.1 NMD 逃逸（无义/移码）后的子分支 ⟦培训班⟧（SVI 2018 决策树 + Walker 2023） |   ├─ 截断/改变区域为已确立关键功能域 → PVS1_Strong（2023 起若证据充分可考虑上调至 PVS1） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0126 | original/ACMG_CRITERIA.md:126 | 1.4.1 NMD 逃逸（无义/移码）后的子分支 ⟦培训班⟧（SVI 2018 决策树 + Walker 2023） |   └─ 截断区功能未知 → | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0127 | original/ACMG_CRITERIA.md:127 | 1.4.1 NMD 逃逸（无义/移码）后的子分支 ⟦培训班⟧（SVI 2018 决策树 + Walker 2023） |        ├─ 该外显子的 LoF 变异在一般人群中高频 或 外显子不在临床相关转录本 → PVS1_N/A | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0128 | original/ACMG_CRITERIA.md:128 | 1.4.1 NMD 逃逸（无义/移码）后的子分支 ⟦培训班⟧（SVI 2018 决策树 + Walker 2023） |        ├─ 去除蛋白 >10% → PVS1_Strong | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0129 | original/ACMG_CRITERIA.md:129 | 1.4.1 NMD 逃逸（无义/移码）后的子分支 ⟦培训班⟧（SVI 2018 决策树 + Walker 2023） |        └─ 去除蛋白 <10% → PVS1_Moderate | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0130 | original/ACMG_CRITERIA.md:130 | 1.4.1 NMD 逃逸（无义/移码）后的子分支 ⟦培训班⟧（SVI 2018 决策树 + Walker 2023） |  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0131 | original/ACMG_CRITERIA.md:131 | 1.4.1 NMD 逃逸（无义/移码）后的子分支 ⟦培训班⟧（SVI 2018 决策树 + Walker 2023） | - 截断比例 = (全长 − 截断位) / 全长，以 MANE CDS 氨基酸数计（PKP2 案例：(881−852)/881 <10% → Moderate）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0132 | original/ACMG_CRITERIA.md:132 | 1.4.1 NMD 逃逸（无义/移码）后的子分支 ⟦培训班⟧（SVI 2018 决策树 + Walker 2023） | - VCEP 可再按"截断区下游是否已有致病变异"细分（FOXN1 工作组）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0133 | original/ACMG_CRITERIA.md:133 | 1.4.1 NMD 逃逸（无义/移码）后的子分支 ⟦培训班⟧（SVI 2018 决策树 + Walker 2023） | - "关键功能区"的证据**必须与本例疾病实体/遗传模式一致**：TET3 exon 9 的 4 个 AR-P/LP 错义不能证明该区对 AD-LOF 关键。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0135 | original/ACMG_CRITERIA.md:135 | 1.4 截断区重要性判断（NMD 逃逸时 — PVS1课件/李茹） | ### 1.4 截断区重要性判断（NMD 逃逸时 — PVS1课件/李茹） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0137 | original/ACMG_CRITERIA.md:137 | 1.4 截断区重要性判断（NMD 逃逸时 — PVS1课件/李茹） | 预计不发生 NMD 时，须确定截断/改变区域对蛋白功能是否重要： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0138 | original/ACMG_CRITERIA.md:138 | 1.4 截断区重要性判断（NMD 逃逸时 — PVS1课件/李茹） | 1. 文献/实验确定截断区功能（关键结构域）；识别工具：InterPro、Pfam（同源域）、复合蛋白晶体结构（关键互作残基） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0139 | original/ACMG_CRITERIA.md:139 | 1.4 截断区重要性判断（NMD 逃逸时 — PVS1课件/李茹） | 2. ClinVar/内部库查截断区下游是否有已报道致病变异 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0140 | original/ACMG_CRITERIA.md:140 | 1.4 截断区重要性判断（NMD 逃逸时 — PVS1课件/李茹） | 3. 查该区是否存在可变剪接 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0141 | original/ACMG_CRITERIA.md:141 | 1.4 截断区重要性判断（NMD 逃逸时 — PVS1课件/李茹） | 4. **查 VCEP 特定基因评级指南**（最高优先级） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0143 | original/ACMG_CRITERIA.md:143 | 1.4 截断区重要性判断（NMD 逃逸时 — PVS1课件/李茹） | **VCEP 实例（可上调/下调 PVS1 — 务必查 cspec）**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0144 | original/ACMG_CRITERIA.md:144 | 1.4 截断区重要性判断（NMD 逃逸时 — PVS1课件/李茹） | - **PTEN**：起始密码子变异按通用框架为 PVS1_Moderate，但 PTEN 工作组有足够患者数据 → 建议用 PVS1。最后一个外显子虽不 NMD 但功能域关键 → p.D3 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0145 | original/ACMG_CRITERIA.md:145 | 1.4 截断区重要性判断（NMD 逃逸时 — PVS1课件/李茹） | - **FOXN1**（SCID 工作组）：用已知致病变异调节 PVS1 强度；forkhead 域（aa 270-367）、transactivation 域（aa 511-563）内的非 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0146 | original/ACMG_CRITERIA.md:146 | 1.4 截断区重要性判断（NMD 逃逸时 — PVS1课件/李茹） | - **GJB2**（Hearing loss 工作组）：仅 2 个外显子的基因 → 建议用 PVS1（PMID:30311386）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0148 | original/ACMG_CRITERIA.md:148 | 1.4 截断区重要性判断（NMD 逃逸时 — PVS1课件/李茹） | 参考工具：**AutoPVS1** https://autopvs1.bgi.com/ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0150 | original/ACMG_CRITERIA.md:150 | 1.5 起始密码子丢失（PVS1课件） | ### 1.5 起始密码子丢失（PVS1课件） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0152 | original/ACMG_CRITERIA.md:152 | 1.5 起始密码子丢失（PVS1课件） | SVI 建议：造成起始密码子丢失的变异**不应使用 PVS1 或 PVS1_Strong**，通用框架上限 **PVS1_Moderate**（功能研究表明下游甚至上游 AUG/非 AUG  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0154 | original/ACMG_CRITERIA.md:154 | 1.5 起始密码子丢失（PVS1课件） | **分档表** ⟦培训班⟧（王明明/李茹 S59）： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0156 | original/ACMG_CRITERIA.md:156 | 1.5 起始密码子丢失（PVS1课件） | \| 情形 \| PVS1 强度 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0157 | original/ACMG_CRITERIA.md:157 | 1.5 起始密码子丢失（PVS1课件） | \|---\|---\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0158 | original/ACMG_CRITERIA.md:158 | 1.5 起始密码子丢失（PVS1课件） | \| 无替代起始转录本，且 Met1～下游首个框内 Met 区间内已有 P/LP 变异 \| PVS1_Moderate \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0159 | original/ACMG_CRITERIA.md:159 | 1.5 起始密码子丢失（PVS1课件） | \| 无替代起始转录本，该区间内无 P/LP \| PVS1_Supporting \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0160 | original/ACMG_CRITERIA.md:160 | 1.5 起始密码子丢失（PVS1课件） | \| 存在使用替代 ATG 的**主要功能转录本**（在受累组织主要表达且功能完整，数据库/文献核实） \| N/A \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0161 | original/ACMG_CRITERIA.md:161 | 1.5 起始密码子丢失（PVS1课件） | \| 文献证实下游 ATG 生理性重启并产生部分功能蛋白 \| N/A \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0162 | original/ACMG_CRITERIA.md:162 | 1.5 起始密码子丢失（PVS1课件） | \| 存在可绕过 exon 1 的次要功能转录本（如 FZD4 NM_001100255.1），但非主要转录本 \| 降至 Moderate/Supporting，**不直接 N/A** \ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0163 | original/ACMG_CRITERIA.md:163 | 1.5 起始密码子丢失（PVS1课件） | \| VCEP 明确上调（PTEN；GAA Lysosomal VCEP 允许 PVS1_Strong，有酶活/WB 功能证据时上调至 PVS1 而非另计 PS3） \| 依 VCEP \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0165 | original/ACMG_CRITERIA.md:165 | 1.5 起始密码子丢失（PVS1课件） | - 下游 Met 若位于信号肽内，重启翻译亦无功能，可按"区间内有 P/LP"处理。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0166 | original/ACMG_CRITERIA.md:166 | 1.5 起始密码子丢失（PVS1课件） | - 如与特定基因 VCEP 冲突，以 VCEP 为准。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0168 | original/ACMG_CRITERIA.md:168 | 1.6 终止密码子丢失（PVS1课件，ACGS 2024 v1.2） | ### 1.6 终止密码子丢失（PVS1课件，ACGS 2024 v1.2） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0170 | original/ACMG_CRITERIA.md:170 | 1.6 终止密码子丢失（PVS1课件，ACGS 2024 v1.2） | 如果存在无终止密码子降解（NSD, Non-stop decay）→ 可用 PVS1。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0172 | original/ACMG_CRITERIA.md:172 | 1.7 外显子缺失/重复（PVS1课件，PMID:31534211） | ### 1.7 外显子缺失/重复（PVS1课件，PMID:31534211） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0174 | original/ACMG_CRITERIA.md:174 | 1.7 外显子缺失/重复（PVS1课件，PMID:31534211） | - **整个单倍剂量不足基因的缺失**（无冲突）→ 可直接评为 LP（**PVS1_Stand-alone**） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0175 | original/ACMG_CRITERIA.md:175 | 1.7 外显子缺失/重复（PVS1课件，PMID:31534211） | - 单/多外显子缺失：评估是否造成移码、是否为临床相关转录本 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0176 | original/ACMG_CRITERIA.md:176 | 1.7 外显子缺失/重复（PVS1课件，PMID:31534211） | - 基因内重复：仅考虑**串联（in tandem）**形式（≥83% 重复为串联，PMID:25640679），评估是否移码。**Brandt 2020 分档** ⟦培训班⟧：证实串联（G | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0177 | original/ACMG_CRITERIA.md:177 | 1.7 外显子缺失/重复（PVS1课件，PMID:31534211） | - ⛔ PVS1 不适用于：明确在基因外的外显子、涉及多个基因的缺失、全基因重复、串联的整个基因重复 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0178 | original/ACMG_CRITERIA.md:178 | 1.7 外显子缺失/重复（PVS1课件，PMID:31534211） | - 外显子长度为 3 的倍数 → 推定框内跳跃，转入 §1.8"保留阅读框"分支；同时给出 SpliceAI 与 RDDC RNA Splicer 的两种可能后果。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0180 | original/ACMG_CRITERIA.md:180 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | ### 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0182 | original/ACMG_CRITERIA.md:182 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | **🔑 2023 SVI 核心新规（PMID:37352859）**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0183 | original/ACMG_CRITERIA.md:183 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - 实验证实变异**引起异常剪接（LOF）** → 用 **PVS1_Strength(RNA)**，**取代 PS3** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0184 | original/ACMG_CRITERIA.md:184 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - 实验证实变异**不引起异常剪接** → 用 **BP7_Strong(RNA)**，**取代 BS3** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0185 | original/ACMG_CRITERIA.md:185 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - 框内 RNA 跳跃事件若涵盖无争议临床相关残基 → SVI 建议 PVS1 升级至 Very Strong；上调依据除"该域有致病错义"外，还包括"互补供体/受体二核苷酸位点存在致病变异 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0186 | original/ACMG_CRITERIA.md:186 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - ⚠️ 仅检测 RNA 剪接改变的实验**不用 PS3/BS3**（不直接反映蛋白功能）；但进一步检测剪接后蛋白功能可同时用相应等级 PS3/BS3（吴家裕）。⟦培训班⟧ **封顶**：P | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0187 | original/ACMG_CRITERIA.md:187 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - ⟦培训班⟧ PVS1(RNA) 吸收预测型证据：已用 PVS1(RNA) 时不再叠加 PP3/PM4/预测型 PVS1（预测只用于解释 RNA 结果的合理性）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0188 | original/ACMG_CRITERIA.md:188 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - 离体 RNA 前提：须确认目标基因在所取组织（血/羊水细胞等）有表达，否则 RT-PCR 阴性无意义；BP7(RNA) 仅采信非肿瘤组织；外显子变异用 BP7(RNA) 排除剪接后**仍 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0189 | original/ACMG_CRITERIA.md:189 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - 文献 minigene 证据可信度清单：片段保留 ≥200–300bp、<6kb、WT/Mut 同片段、细胞系与疾病相关、双细胞系、质粒测序；局限：缺远端 ESE/ESS、组织特异剪接不 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0191 | original/ACMG_CRITERIA.md:191 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | **剪接术语与坐标** ⟦培训班⟧：供体剪接区域 = 外显子末 3 碱基 + 内含子 +1～+6；受体剪接区域 = 外显子第 1 碱基 + 内含子 −1～−20；最小剪接区域 = 外显子第  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0193 | original/ACMG_CRITERIA.md:193 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | **经典 ±1,2 二核苷酸变异决策（PVS1课件 A-I 分支，⟦培训班⟧ 补齐）**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0194 | original/ACMG_CRITERIA.md:194 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - A：5'UTR 区无剪接改变预测 → PVS1_N/A | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0195 | original/ACMG_CRITERIA.md:195 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - B：外显子跳跃/隐匿位点消除起始密码子且无替代起始 → **PVS1** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0196 | original/ACMG_CRITERIA.md:196 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - C：外显子跳跃/隐匿剪接破坏阅读框 + 预计 NMD → **PVS1** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0197 | original/ACMG_CRITERIA.md:197 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - D：破坏阅读框 + 不 NMD + 截断区已确立关键 或 去除 >10% → **PVS1_Strong** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0198 | original/ACMG_CRITERIA.md:198 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - E：破坏阅读框 + 不 NMD + 去除 <10% 且非关键区 → **PVS1_Moderate** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0199 | original/ACMG_CRITERIA.md:199 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - F：保留阅读框 + 删除已确认关键功能区 → **PVS1** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0200 | original/ACMG_CRITERIA.md:200 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - G：保留阅读框 + 去除 >10% 但非确认关键区 → **PVS1_Strong** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0201 | original/ACMG_CRITERIA.md:201 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - H：保留阅读框 + 去除 <10% 非关键区 → **PVS1_Moderate** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0202 | original/ACMG_CRITERIA.md:202 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - ⛔ **RNA 证实为框内插入**（新生受体/供体致内含子序列纳入、小片段内含子保留，阅读框保留、无序列丢失）且**无蛋白功能数据** → **记录不计分**：不赋 PVS1(RNA)， | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0203 | original/ACMG_CRITERIA.md:203 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - 存在正常补救转录本 → PVS1_N/A（如 BRCA1 c.594-2A>C，框内功能性转录本天然存在，良性，PMID:27008870） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0204 | original/ACMG_CRITERIA.md:204 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - **+2T>C**：可能形成功能性 GC-AG 剪接，无 RNA 证据且 SpliceAI <0.8 时**不用 PVS1**（PMID:32369867） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0205 | original/ACMG_CRITERIA.md:205 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - **+2C>T**（GC 供体位点，约 1.5% 自然剪接位点用 +2C）：可能提高剪接效率 → PVS1_N/A | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0206 | original/ACMG_CRITERIA.md:206 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - EDA 三条经验（李茹）：同位点不同碱基替换的剪接效率不同；相邻内含子变异可致同一跳跃事件；顺式双突变效应更重。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0208 | original/ACMG_CRITERIA.md:208 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | **剪接预测工具与阈值（Walker 2023 SVI 校准，PMID:37352859）**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0209 | original/ACMG_CRITERIA.md:209 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - **SpliceAI**（金标准，AUC 0.991）：Δscore ≥0.2 → 预测发生剪接 → **PP3（Supporting，不升级）**（准确性 78%）；≤0.1 → 预测 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0210 | original/ACMG_CRITERIA.md:210 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - **PP3 对同一变异只用一次**：剪接预测与错义预测不能各计一次，取其一；外显子变异在评估剪接的同时须评估蛋白效应。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0211 | original/ACMG_CRITERIA.md:211 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - 经实验验证的剪接变异可查 **SpliceVarDB** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0212 | original/ACMG_CRITERIA.md:212 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | - 其他工具：MaxEntScan（经典位点）、varSEAK（商业，临床报告）、MMSplice（外显子跳跃）等（详见潘丹丹工具对比） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0214 | original/ACMG_CRITERIA.md:214 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | **BP7 适用边界** ⟦培训班⟧：仅在 BP4（SpliceAI ≤0.1）成立时可用；保守性对 BP7 无帮助；仅用于剪接区域外（+7/−21 之外）的内含子/非编码变异，以及外显子第 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0216 | original/ACMG_CRITERIA.md:216 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | **剪接变异的 PS1（PVS1课件/ACGS 2024 强度矩阵）** ⟦培训班⟧：先决条件——待评估变异（VUA）的预测事件须与已知 P/LP 变异**完全匹配**（如都预测外显子跳跃， | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0218 | original/ACMG_CRITERIA.md:218 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | \| VUA 自身证据 \| 参照变异位置 \| 参照为 P \| 参照为 LP \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0219 | original/ACMG_CRITERIA.md:219 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | \|---\|---\|---\|---\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0220 | original/ACMG_CRITERIA.md:220 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | \| PP3 级（非 ±1,2） \| 同一位点不同核苷酸 \| PS1 \| PS1_Moderate \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0221 | original/ACMG_CRITERIA.md:221 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | \| PP3 级 \| 同一供体/受体基序（含 ±1,2） \| PS1_Moderate \| PS1_Supporting \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0222 | original/ACMG_CRITERIA.md:222 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | \| PVS1 级（±1,2） \| 同一 ±1,2 位（如 +2T>A vs 已知 +1G>T） \| PS1_Supporting \| 不赋 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0223 | original/ACMG_CRITERIA.md:223 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | \| PVS1 级 \| 同区域非 ±1,2 \| PS1_Supporting \| PS1_Supporting \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0224 | original/ACMG_CRITERIA.md:224 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | \| PVS1_Strong/Mod/Supp 级 \| 同一 ±1,2 位 \| PS1 \| 不赋 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0225 | original/ACMG_CRITERIA.md:225 | 1.8 剪接变异的 PVS1 框架（2023 SVI 重大更新 — 多份课件） | \| PVS1_Strong/Mod/Supp 级 \| 同区域非 ±1,2 \| PS1_Moderate \| PS1_Supporting \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0227 | original/ACMG_CRITERIA.md:227 | 1.9 🤰 产前 RNA 证据获取路径（李茹 TET3 案例 + 余丽华 RYR1 案例） | ### 1.9 🤰 产前 RNA 证据获取路径（李茹 TET3 案例 + 余丽华 RYR1 案例） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0229 | original/ACMG_CRITERIA.md:229 | 1.9 🤰 产前 RNA 证据获取路径（李茹 TET3 案例 + 余丽华 RYR1 案例） | 产前 LOF/剪接变异若初判 PVS1_Moderate 且为关键决策点，产前独有可获得 RNA 级证据的窗口，应在遗传咨询中主动提出。⟦培训班⟧ 路径表： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0230 | original/ACMG_CRITERIA.md:230 | 1.9 🤰 产前 RNA 证据获取路径（李茹 TET3 案例 + 余丽华 RYR1 案例） | 1. 先查目标基因在羊水细胞/绒毛/脐血中的表达（GTEx 无产前组织，可引用本地羊水表达基线库或文献 TPM）； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0231 | original/ACMG_CRITERIA.md:231 | 1.9 🤰 产前 RNA 证据获取路径（李茹 TET3 案例 + 余丽华 RYR1 案例） | 2. 表达充分 → 引产前留取脐血/羊水细胞做 RNA-seq 或 RT-PCR； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0232 | original/ACMG_CRITERIA.md:232 | 1.9 🤰 产前 RNA 证据获取路径（李茹 TET3 案例 + 余丽华 RYR1 案例） | 3. 不表达（如 RYR1）→ 羊水间充质干细胞定向诱导（成肌/成神经等）后 cDNA 测序； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0233 | original/ACMG_CRITERIA.md:233 | 1.9 🤰 产前 RNA 证据获取路径（李茹 TET3 案例 + 余丽华 RYR1 案例） | 4. 已引产 → 受累组织 cDNA + 病理/电镜；有家族史者可用家族患者样本； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0234 | original/ACMG_CRITERIA.md:234 | 1.9 🤰 产前 RNA 证据获取路径（李茹 TET3 案例 + 余丽华 RYR1 案例） | 5. 所得结果按 §1.8 走 PVS1(RNA)/BP7(RNA)，将 PVS1_Moderate 升级或撤销。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0236 | original/ACMG_CRITERIA.md:236 | 1.10 PM4 / BP3 / PP2 / BP1（⟦培训班⟧ 新增，旧版缺定义） | ### 1.10 PM4 / BP3 / PP2 / BP1（⟦培训班⟧ 新增，旧版缺定义） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0238 | original/ACMG_CRITERIA.md:238 | 1.10 PM4 / BP3 / PP2 / BP1（⟦培训班⟧ 新增，旧版缺定义） | **PM4（蛋白长度改变，Moderate）**：适用于非重复区的框内插入/缺失、以及终止密码子丢失（无 NSD 时）。默认 PM4；单氨基酸缺失且不涉已知关键残基可降 PM4_Suppor | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0240 | original/ACMG_CRITERIA.md:240 | 1.10 PM4 / BP3 / PP2 / BP1（⟦培训班⟧ 新增，旧版缺定义） | **BP3（重复区框内 indel，Supporting）**：框内 indel 位于重复区（UCSC simple repeat / segmental dup / RepeatMaske | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0242 | original/ACMG_CRITERIA.md:242 | 1.10 PM4 / BP3 / PP2 / BP1（⟦培训班⟧ 新增，旧版缺定义） | **PP2（错义为主要机制且良性错义少的基因，Supporting）**：gnomAD Missense Z ≥3.09 可作参考；PP2 为基因级约束，**不与 PM1（结构域级约束）、P | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0244 | original/ACMG_CRITERIA.md:244 | 1.10 PM4 / BP3 / PP2 / BP1（⟦培训班⟧ 新增，旧版缺定义） | **BP1（截短为主要机制基因中的错义，Supporting）**：机制为 LOF 且 P/LP 以截短为主的基因中的错义变异；具体阈值按 VCEP。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0246 | original/ACMG_CRITERIA.md:246 | 1.10 PM4 / BP3 / PP2 / BP1（⟦培训班⟧ 新增，旧版缺定义） | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0248 | original/ACMG_CRITERIA.md:248 | 2. 人群频率证据：PM2 / BA1 / BS1 / BS2（潘丹丹报告） | ## 2. 人群频率证据：PM2 / BA1 / BS1 / BS2（潘丹丹报告） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0250 | original/ACMG_CRITERIA.md:250 | 2.1 PM2（SVI 2020 降级） | ### 2.1 PM2（SVI 2020 降级） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0252 | original/ACMG_CRITERIA.md:252 | 2.1 PM2（SVI 2020 降级） | - **默认降级为 PM2_Supporting**（除有专病 VCEP 规则的基因） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0253 | original/ACMG_CRITERIA.md:253 | 2.1 PM2（SVI 2020 降级） | - 适用所有变异类型（BA1/BS1/BS2 亦适用所有变异类型） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0254 | original/ACMG_CRITERIA.md:254 | 2.1 PM2（SVI 2020 降级） | - ⚠️ 低覆盖区、indel 人群数据质量差时慎用 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0255 | original/ACMG_CRITERIA.md:255 | 2.1 PM2（SVI 2020 降级） | - 大缺失/重复（≥50bp）需核查 gnomAD SVs/CNVs 或 DGV (https://dgv.tcag.ca/) | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0256 | original/ACMG_CRITERIA.md:256 | 2.1 PM2（SVI 2020 降级） | - gnomAD 当前 v4.1.1/GRCh38，欧洲裔占约 3/4，东亚估计不稳；年龄分布可辅助 BS2 判断 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0257 | original/ACMG_CRITERIA.md:257 | 2.1 PM2（SVI 2020 降级） | - ⟦培训班⟧ **PP3_Strong + PM2_Supporting = 5 分 = VUS**：这是产前 novel 错义最常见的"看起来很像致病"陷阱，不得凭预测评分抬高 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0258 | original/ACMG_CRITERIA.md:258 | 2.1 PM2（SVI 2020 降级） | - ⟦培训班⟧ PM2 与 PS4 不可共用同一对照队列（有第二独立队列可合并） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0260 | original/ACMG_CRITERIA.md:260 | 2.2 BA1 / BS1 | ### 2.2 BA1 / BS1 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0262 | original/ACMG_CRITERIA.md:262 | 2.2 BA1 / BS1 | - **BA1**（SVI 2018）：任一 ≥2000 等位基因的大陆人群频率 >5%，且不在 BA1 豁免名单内 → 独立良性，一票否决所有致病证据 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0263 | original/ACMG_CRITERIA.md:263 | 2.2 BA1 / BS1 | - **BS1**：频率大于疾病预期。阈值用 cardiodb 计算器估算：https://cardiodb.org/allelefrequencyapp/（输入遗传模式、患病率、等位基因异 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0264 | original/ACMG_CRITERIA.md:264 | 2.2 BA1 / BS1 | - 注意 **BA1 豁免变异名单**（高频但致病，如 RYR1、NEB、ACTA1 的特定变异；GJB2 c.109G>A p.Val37Ile 为 VCEP 豁免 BA1 的经典案例） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0265 | original/ACMG_CRITERIA.md:265 | 2.2 BA1 / BS1 | - 有专病指南的基因用专病规则 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0266 | original/ACMG_CRITERIA.md:266 | 2.2 BA1 / BS1 | - ⟦培训班⟧ **BA1 例外触发条件（亚效等位 / 低外显致病）**（肖锐 OCA2 p.Ala481Thr 东亚 5.27% 案例）：当同时满足 ①PM3 ≥ Strong（多例患者与 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0268 | original/ACMG_CRITERIA.md:268 | 2.3 BS2（ACGS 2024 量化） | ### 2.3 BS2（ACGS 2024 量化） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0270 | original/ACMG_CRITERIA.md:270 | 2.3 BS2（ACGS 2024 量化） | - 早发完全外显病在健康成人中发现：隐性纯合 / 显性杂合 / X 连锁半合 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0271 | original/ACMG_CRITERIA.md:271 | 2.3 BS2（ACGS 2024 量化） | - **2024 ACGS**：早发完全外显病 BS2 可用于 ≥2 个杂合健康个体（AD）或 ≥2 个纯合健康个体（AR）；晚发/不完全外显病需更多健康个体且需详细表型分析 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0272 | original/ACMG_CRITERIA.md:272 | 2.3 BS2（ACGS 2024 量化） | - ⟦培训班⟧ **gnomAD 成年半合子/纯合子作为重症反证（频率"方向二"）**：早发重症 X 连锁/AR 基因，gnomAD 成年半合子（男性）或纯合子 ≥2 且排除已知亚效等位 → | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0273 | original/ACMG_CRITERIA.md:273 | 2.3 BS2（ACGS 2024 量化） | - ⟦培训班⟧ **BS2/BS4 用于亲代前的四条 SOP 前置**（蒋 COL1A1 案例）：①疾病外显率高（未量化或 <~80% 时 🤰 产前一律不赋 BS2；ClinGen SVI  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0274 | original/ACMG_CRITERIA.md:274 | 2.3 BS2（ACGS 2024 量化） | - ⟦培训班⟧ **不构成"健康个体"的情形**（不计 BS2/BS4）：印记基因来自沉默亲本的携带者（UBE3A 父源等位脑内沉默；UBE3A VCEP 的 BS2 要求 4 名未受累携带 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0276 | original/ACMG_CRITERIA.md:276 | 2.4 专病 VCEP 频率阈值（关键 — 必查 cspec） | ### 2.4 专病 VCEP 频率阈值（关键 — 必查 cspec） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0278 | original/ACMG_CRITERIA.md:278 | 2.4 专病 VCEP 频率阈值（关键 — 必查 cspec） | **有专病 VCEP 规则的基因，其 PM2/BS1/BA1 阈值由 VCEP 定制，覆盖通用阈值。** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0280 | original/ACMG_CRITERIA.md:280 | 2.4 专病 VCEP 频率阈值（关键 — 必查 cspec） | 🔑 **权威查询入口**：https://cspec.genome.network/cspec/ui/svi/ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0282 | original/ACMG_CRITERIA.md:282 | 2.4 专病 VCEP 频率阈值（关键 — 必查 cspec） | 代表性基因（阈值随 VCEP 更新，务必实时核对，不可硬记）： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0283 | original/ACMG_CRITERIA.md:283 | 2.4 专病 VCEP 频率阈值（关键 — 必查 cspec） | - 心血管：MYH7, MYBPC3, TNNI3, TNNT2, TPM1, KCNQ1, LDLR, FBN1, BMPR2 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0284 | original/ACMG_CRITERIA.md:284 | 2.4 专病 VCEP 频率阈值（关键 — 必查 cspec） | - 代谢：PAH, GAA, HNF1A/4A, GCK, ACADVL, GAMT | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0285 | original/ACMG_CRITERIA.md:285 | 2.4 专病 VCEP 频率阈值（关键 — 必查 cspec） | - 眼：MYOC, ABCA4, RPE65, RPGR, RS1 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0286 | original/ACMG_CRITERIA.md:286 | 2.4 专病 VCEP 频率阈值（关键 — 必查 cspec） | - 神经肌肉：ACTA1, RYR1, DYSF, NEB, 肢带型肌营养不良相关 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0287 | original/ACMG_CRITERIA.md:287 | 2.4 专病 VCEP 频率阈值（关键 — 必查 cspec） | - 精神发育：MECP2, CDKL5, FOXG1, TCF4, UBE3A, SCN1A/2A/8A, RAS 通路基因 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0288 | original/ACMG_CRITERIA.md:288 | 2.4 专病 VCEP 频率阈值（关键 — 必查 cspec） | - 免疫：PIK3CD, CTLA4, FOXN1, ADA, RAG1/2, IL2RG | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0289 | original/ACMG_CRITERIA.md:289 | 2.4 专病 VCEP 频率阈值（关键 — 必查 cspec） | - 血液：RUNX1, VWF, F8, F9, SERPINC1, VHL | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0291 | original/ACMG_CRITERIA.md:291 | 2.4 专病 VCEP 频率阈值（关键 — 必查 cspec） | 典型示例（说明量级差异，非用于直接套用）：MYH7 HCM 的 PM2_Supporting ≤0.00004，BS1 ≥0.0001，BA1 ≥0.001；耳聋 AR 基因（GJB2/SL | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0293 | original/ACMG_CRITERIA.md:293 | 2.5 🤰 产前频率陷阱：高频亚效单倍型（潘丹丹 TBX6 案例） | ### 2.5 🤰 产前频率陷阱：高频亚效单倍型（潘丹丹 TBX6 案例） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0295 | original/ACMG_CRITERIA.md:295 | 2.5 🤰 产前频率陷阱：高频亚效单倍型（潘丹丹 TBX6 案例） | **"高频 ≠ 良性"**：某些人群高频点本身为亚效（hypomorphic）单倍型，常规流程会过滤，但与 LOF 变异**反式组合**可致病。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0296 | original/ACMG_CRITERIA.md:296 | 2.5 🤰 产前频率陷阱：高频亚效单倍型（潘丹丹 TBX6 案例） | - 实例：TBX6 NM_004608.3 c.[-48-240A>G; -49+34G>T; 1227G>A]（T-C-A 单倍型）为亚洲人群常见单倍型，三个均为人群高频点；与 LOF 变 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0297 | original/ACMG_CRITERIA.md:297 | 2.5 🤰 产前频率陷阱：高频亚效单倍型（潘丹丹 TBX6 案例） | - **产前操作要点**：检出单杂合 LOF 变异时，主动核查是否同时存在该类高频亚效单倍型；先证者与无症状父/母基因型一致时需回访评估父/母表型（外显率/表现度问题） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0299 | original/ACMG_CRITERIA.md:299 | 2.5b 🤰 高同源假基因区域陷阱（符芳 GBA1 案例）⟦培训班⟧ | ### 2.5b 🤰 高同源假基因区域陷阱（符芳 GBA1 案例）⟦培训班⟧ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0301 | original/ACMG_CRITERIA.md:301 | 2.5b 🤰 高同源假基因区域陷阱（符芳 GBA1 案例）⟦培训班⟧ | AR 基因仅检出单杂合 P/LP/VUS 且表型高度吻合时，**必须回看 BAM**：覆盖度、MAPQ、外显子级读深缺口。基因-假基因重组（GBA1 RecNciI c.[1448T>C;1 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0303 | original/ACMG_CRITERIA.md:303 | 2.6 第四版指南方向（潘丹丹 — DRAFT 预告） | ### 2.6 第四版指南方向（潘丹丹 — DRAFT 预告） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0305 | original/ACMG_CRITERIA.md:305 | 2.6 第四版指南方向（潘丹丹 — DRAFT 预告） | ACMG/AMP 第四版拟将频率证据转为连续评分 POP_FRQ（如 MYH7 AF 0.00035→POP_FRQ_-1，AF 0.002→POP_FRQ_-6）；未检出记为 POP_FR | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0307 | original/ACMG_CRITERIA.md:307 | 2.6 第四版指南方向（潘丹丹 — DRAFT 预告） | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0309 | original/ACMG_CRITERIA.md:309 | 3. PS3 / BS3：功能证据质量门槛（吴家裕报告 + 李卓 2026-09 正式课件） | ## 3. PS3 / BS3：功能证据质量门槛（吴家裕报告 + 李卓 2026-09 正式课件） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0311 | original/ACMG_CRITERIA.md:311 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | ### 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0313 | original/ACMG_CRITERIA.md:313 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | - 必须参照指南设阴/阳性对照，计算 **OddsPath** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0314 | original/ACMG_CRITERIA.md:314 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | - **至少 11 个对照变异**（含良性和致病）才能用"中等"强度 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0315 | original/ACMG_CRITERIA.md:315 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | - 无任何变异做过功能实验时：可用已明确分类为 B/LB 或 P/LP 的变异（须机制和变异类型相关）作阴/阳性对照 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0316 | original/ACMG_CRITERIA.md:316 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | - 实验最低门槛（用于评判文献实验是否够格）⟦培训班⟧：四种对照（WT、空白、阳性、阴性）+ 生物学重复 ≥3 + 技术重复 ≥3 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0318 | original/ACMG_CRITERIA.md:318 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | **OddsPath 分档（Brnich 2019 Table）** ⟦培训班⟧： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0320 | original/ACMG_CRITERIA.md:320 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | \| OddsPath \| 证据 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0321 | original/ACMG_CRITERIA.md:321 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | \|---\|---\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0322 | original/ACMG_CRITERIA.md:322 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | \| > 18.7 \| PS3_Strong \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0323 | original/ACMG_CRITERIA.md:323 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | \| 4.3 – 18.7 \| PS3_Moderate \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0324 | original/ACMG_CRITERIA.md:324 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | \| 2.1 – 4.3 \| PS3_Supporting \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0325 | original/ACMG_CRITERIA.md:325 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | \| 0.48 – 2.1 \| 不确定区，不赋 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0326 | original/ACMG_CRITERIA.md:326 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | \| 0.23 – 0.48 \| BS3_Supporting \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0327 | original/ACMG_CRITERIA.md:327 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | \| 0.053 – 0.23 \| BS3_Moderate \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0328 | original/ACMG_CRITERIA.md:328 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | \| < 0.053 \| BS3_Strong \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0330 | original/ACMG_CRITERIA.md:330 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | **实验体系强度上限** ⟦培训班⟧： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0332 | original/ACMG_CRITERIA.md:332 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | \| 实验体系 \| 上限 \| 默认起点 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0333 | original/ACMG_CRITERIA.md:333 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | \|---\|---\|---\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0334 | original/ACMG_CRITERIA.md:334 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | \| 小鼠敲入/敲除重现人类表型 \| Strong \| — \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0335 | original/ACMG_CRITERIA.md:335 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | \| 斑马鱼 \| Moderate \| — \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0336 | original/ACMG_CRITERIA.md:336 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | \| 果蝇 / 线虫 \| Supporting \| — \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0337 | original/ACMG_CRITERIA.md:337 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | \| 体外细胞/生化（单一实验、无 OddsPath 校准） \| Supporting（校准充分可至 Moderate/Strong） \| **Supporting** \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0339 | original/ACMG_CRITERIA.md:339 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | - 模式生物有效性核查：**同位密码子是否与人一致**（GJB2 小鼠 GTG→p.Val37Met ≠ 人 GTT→Val37Ile）；染料转移/电偶联类实验临床相关性有限不采信。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0340 | original/ACMG_CRITERIA.md:340 | 3.1 强度判定（OddsPath，PMID:31064749 Brnich 2019） | - **MAVE 数据**：MaveDB 原始分数 ≠ 证据。先查 ClinMave/VCEP 是否已校准该实验（有 OddsPath 或已被 VCEP 采纳）→ 可给 Strong；未校准 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0342 | original/ACMG_CRITERIA.md:342 | 3.2 实验类型与适用性（吴家裕表） | ### 3.2 实验类型与适用性（吴家裕表） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0344 | original/ACMG_CRITERIA.md:344 | 3.2 实验类型与适用性（吴家裕表） | 理解疾病机制 → 评估实验适用性 → 评估实验有效性 → 确定证据强度。按蛋白类型选实验：酶（催化效率/产物量）、转录因子（荧光素酶报告/EMSA）、RNA 结合蛋白（RIP/REMSA）、 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0346 | original/ACMG_CRITERIA.md:346 | 3.3 关键限制规则 | ### 3.3 关键限制规则 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0348 | original/ACMG_CRITERIA.md:348 | 3.3 关键限制规则 | - ⛔ **仅 RNA 剪接改变实验不用 PS3/BS3** → 用 PVS1_Strength(RNA)/BP7_Strong(RNA)（见 1.8） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0349 | original/ACMG_CRITERIA.md:349 | 3.3 关键限制规则 | - ⛔ **仅蛋白三维模型研究不用 PS3** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0350 | original/ACMG_CRITERIA.md:350 | 3.3 关键限制规则 | - ⛔ **仅蛋白表达量检测不用 PS3**（需进一步做功能相关实验） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0351 | original/ACMG_CRITERIA.md:351 | 3.3 关键限制规则 | - ✅ 免疫荧光发现功能相关定位异常 → PS3_Supporting | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0352 | original/ACMG_CRITERIA.md:352 | 3.3 关键限制规则 | - **PS3 可与 PP3 共用**（功能 vs 进化保守预测，相互独立；剪接预测除外）；同理 BS3 可与 BP4 共用（剪接预测除外） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0353 | original/ACMG_CRITERIA.md:353 | 3.3 关键限制规则 | - **PS3 与 PM1**：通用框架下默认不叠加（PM1 本质是对功能的预测）；⟦培训班⟧ **有 VCEP 明确允许时以 VCEP 为准**（RASopathy VCEP 对 HRAS | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0354 | original/ACMG_CRITERIA.md:354 | 3.3 关键限制规则 | - PS1/PM5 + PS3 限制合并：仅当参考变异无需功能数据即可判 (L)P 且无剪接影响 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0355 | original/ACMG_CRITERIA.md:355 | 3.3 关键限制规则 | - 多个功能实验：**不累加**。一致时取验证最明确者；矛盾时机制最相关且验证最充分者可推翻其他；同级矛盾则均不采纳 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0356 | original/ACMG_CRITERIA.md:356 | 3.3 关键限制规则 | - **BS3 谨慎使用**：单个实验"正常"可能未检测到特定变异的功能效应；不影响蛋白的错义/同义变异仍可能通过隐匿剪接致病 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0357 | original/ACMG_CRITERIA.md:357 | 3.3 关键限制规则 | - ⟦培训班⟧ **PS3 与 BP4 方向相反时**：PS3 ≥ Strong 在手，则 BP4 至多 Supporting（或不计），并在模块 6 说明（蒋 TLR7 REVEL 0.0 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0358 | original/ACMG_CRITERIA.md:358 | 3.3 关键限制规则 | - ⟦培训班⟧ **患者组织功能异常 → PP4 而非 PS3**：患者来源样本同时携带 ≥2 个变异（复合杂合/纯合），功能异常无法归因到单个变异时（李卓 IARS2 案例：线粒体膜电位/ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0360 | original/ACMG_CRITERIA.md:360 | 3.4 数据来源 | ### 3.4 数据来源 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0362 | original/ACMG_CRITERIA.md:362 | 3.4 数据来源 | - **MaveDB** https://www.mavedb.org/（多重功能分析，>700 万变异效应，PMID 见课件）/ MaveMD / **ClinMave**（ClinGen | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0363 | original/ACMG_CRITERIA.md:363 | 3.4 数据来源 | - 基因专属数据库（如 The ALPL Gene Variant Database） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0364 | original/ACMG_CRITERIA.md:364 | 3.4 数据来源 | - 文献检索 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0365 | original/ACMG_CRITERIA.md:365 | 3.4 数据来源 | - 有专病 VCEP 时用 VCEP 的 PS3/BS3 标准 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0366 | original/ACMG_CRITERIA.md:366 | 3.4 数据来源 | - 🤰 产前功能验证样本来源：有家族史用家族患者样本；羊水细胞可建株（见 §1.9） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0368 | original/ACMG_CRITERIA.md:368 | 3.4 数据来源 | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0370 | original/ACMG_CRITERIA.md:370 | 3.5 PM1：关键功能域 / 突变热点（AI 最易滥用、专家最克制的证据） | ## 3.5 PM1：关键功能域 / 突变热点（AI 最易滥用、专家最克制的证据） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0372 | original/ACMG_CRITERIA.md:372 | 3.5 PM1：关键功能域 / 突变热点（AI 最易滥用、专家最克制的证据） | > **编号说明**：本节为 PM1 专章，置于功能证据（PS3）与家系证据（PS2/PM6）之间，编号 3.5 以免改动下游章节交叉引用。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0373 | original/ACMG_CRITERIA.md:373 | 3.5 PM1：关键功能域 / 突变热点（AI 最易滥用、专家最克制的证据） | > | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0374 | original/ACMG_CRITERIA.md:374 | 3.5 PM1：关键功能域 / 突变热点（AI 最易滥用、专家最克制的证据） | > **背景**：PM1 是人工评级与临床专家实操分歧最大的证据之一。许多胎儿遗传病诊断专家**极少**赋 PM1，而自动化/AI 评级却频繁赋予。根因是 AI 常基于"变异落在某结构域 + | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0376 | original/ACMG_CRITERIA.md:376 | 3.5.1 原始定义与三道并列门槛（缺一不可） | ### 3.5.1 原始定义与三道并列门槛（缺一不可） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0378 | original/ACMG_CRITERIA.md:378 | 3.5.1 原始定义与三道并列门槛（缺一不可） | ACMG/AMP 2015 定义：变异位于**突变热点（mutational hotspot）**和/或**关键且功能已确立的结构域（critical and well-establishe | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0380 | original/ACMG_CRITERIA.md:380 | 3.5.1 原始定义与三道并列门槛（缺一不可） | 定义内含三个**并列**要求，缺任一条即不可赋 PM1： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0382 | original/ACMG_CRITERIA.md:382 | 3.5.1 原始定义与三道并列门槛（缺一不可） | 1. **功能"已确立"（well-established），非仅序列注释**：该结构域的功能须经**实验证实**为疾病机制核心（如酶催化中心、受体配体结合口袋、离子通道孔道区、DNA 结合 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0384 | original/ACMG_CRITERIA.md:384 | 3.5.1 原始定义与三道并列门槛（缺一不可） | 2. **区域内无良性变异（最常被跳过的硬门槛）**：必须**主动检索 gnomAD**，确认该域内**没有**常见或已分类为良性/疑似良性的错义变异。若域内散布多个人群错义，说明该区域对错 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0386 | original/ACMG_CRITERIA.md:386 | 3.5.1 原始定义与三道并列门槛（缺一不可） | 3. **"热点"需数据支撑**：要么该位点/邻近位点有**多个独立致病变异聚集**（致病密度显著高于背景），要么是经统计验证的体细胞/胚系突变热点。⛔ 单纯"保守"不等于"热点"。⟦培训班 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0388 | original/ACMG_CRITERIA.md:388 | 3.5.2 互斥与重复计数（AI 最易犯错处） | ### 3.5.2 互斥与重复计数（AI 最易犯错处） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0390 | original/ACMG_CRITERIA.md:390 | 3.5.2 互斥与重复计数（AI 最易犯错处） | **PM1 本质是"基于位置的功能后果预测"**，因此与下列证据存在概念重叠，不可同时赋予： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0392 | original/ACMG_CRITERIA.md:392 | 3.5.2 互斥与重复计数（AI 最易犯错处） | - **PM1 与 PS3**：通用框架下默认不叠加（PS3 是直接功能实验，PM1 是对功能的间接推断，指向同一命题即重复计数，见 3.3）；VCEP 明确允许时以 VCEP 为准。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0393 | original/ACMG_CRITERIA.md:393 | 3.5.2 互斥与重复计数（AI 最易犯错处） | - ⛔ **PM1 不与 PVS1 共用**（见 1.1 互斥规则）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0394 | original/ACMG_CRITERIA.md:394 | 3.5.2 互斥与重复计数（AI 最易犯错处） | - ⛔ ⟦培训班⟧ **PM1 不与 PS1/PM5 共用**（CanVIG-UK 硬禁止：同残基已由 PS1/PM5 计分，不再计结构域约束；VCEP 明文允许者除外）；**PM1 不与  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0395 | original/ACMG_CRITERIA.md:395 | 3.5.2 互斥与重复计数（AI 最易犯错处） | - ⚠️ **PM1 与 PP3 的隐性重叠**：PP3（计算预测有害）与 PM1 都可能在表达"这个位置/这种改变很重要"。ACMG 未将 PM1/PP3 列为硬互斥，可以共用，但 ⟦培训 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0397 | original/ACMG_CRITERIA.md:397 | 3.5.2 互斥与重复计数（AI 最易犯错处） | > **典型 AI 滥用模式**：变异落在"ATP 酶/激酶/解旋酶核心" + "高度保守" + REVEL 高分 → 同时赋 PM1 + PP3（甚至再加功能推断），把"该位置重要"用结构 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0399 | original/ACMG_CRITERIA.md:399 | 3.5.3 ClinGen VCEP 优先（PM1 的精确化与停用） | ### 3.5.3 ClinGen VCEP 优先（PM1 的精确化与停用） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0401 | original/ACMG_CRITERIA.md:401 | 3.5.3 ClinGen VCEP 优先（PM1 的精确化与停用） | **有 VCEP 规则的基因，PM1 怎么用由 VCEP 说了算**（务必查 cspec：https://cspec.genome.network/cspec/ui/svi/）。VCEP 对 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0403 | original/ACMG_CRITERIA.md:403 | 3.5.3 ClinGen VCEP 优先（PM1 的精确化与停用） | - **直接停用 PM1**：部分 VCEP 认为该基因缺乏足够数据界定真正热点 → 不允许用 PM1。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0404 | original/ACMG_CRITERIA.md:404 | 3.5.3 ClinGen VCEP 优先（PM1 的精确化与停用） | - **绑定到精确氨基酸坐标**：把 PM1 限定到有实验支撑的极窄残基簇（如 RYR1 特定区段、PTEN 磷酸酶核心、RASopathy 基因特定功能位点），区域外一律不给。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0405 | original/ACMG_CRITERIA.md:405 | 3.5.3 ClinGen VCEP 优先（PM1 的精确化与停用） | - **与域内已知致病变异数量挂钩调强度**：类似 de novo 点系统，决定 PM1_Supporting 还是 PM1 原级。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0407 | original/ACMG_CRITERIA.md:407 | 3.5.3 ClinGen VCEP 优先（PM1 的精确化与停用） | 通用框架在有 VCEP 时**退居其次**。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0409 | original/ACMG_CRITERIA.md:409 | 3.5.4 强度 | ### 3.5.4 强度 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0411 | original/ACMG_CRITERIA.md:411 | 3.5.4 强度 | - 默认 **PM1（Moderate，+2）**。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0412 | original/ACMG_CRITERIA.md:412 | 3.5.4 强度 | - 部分 VCEP 提供 **PM1_Supporting（+1）** 或 **PM1_Strong** 的调整（须依 VCEP 规则）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0413 | original/ACMG_CRITERIA.md:413 | 3.5.4 强度 | - 通用框架下不自行将 PM1 升至 Strong。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0415 | original/ACMG_CRITERIA.md:415 | 3.5.5 🤰 产前保守原则 | ### 3.5.5 🤰 产前保守原则 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0417 | original/ACMG_CRITERIA.md:417 | 3.5.5 🤰 产前保守原则 | 产前评级强调宁缺毋滥，PM1 尤其应保守： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0419 | original/ACMG_CRITERIA.md:419 | 3.5.5 🤰 产前保守原则 | 1. **多数罕见病基因达不到"功能已确立"门槛**：真正实验定位的关键域集中在少数研究透彻的基因（离子通道、激酶、知名酶、胶原蛋白等）；绝大多数基因的域注释来自同源预测，功能边界模糊 →  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0420 | original/ACMG_CRITERIA.md:420 | 3.5.5 🤰 产前保守原则 | 2. **强制完成 gnomAD 域内良性变异核查**：产前不可跳过门槛 2。未核查 → 不赋 PM1，或降为 PM1_Supporting 并明确标注"未完成域内良性变异核查"。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0421 | original/ACMG_CRITERIA.md:421 | 3.5.5 🤰 产前保守原则 | 3. **优先让不重复计数的证据当主干**：产前应以 PM2（频率）、PP3（预测，如 REVEL/AlphaMissense）、PS2/PM6（家系，按 4.1.5）支撑分级；PM1 仅作 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0422 | original/ACMG_CRITERIA.md:422 | 3.5.5 🤰 产前保守原则 | 4. **诚实标注**：报告模块 3 须写明 PM1 的依据、是否有 VCEP 背书、是否完成域内核查；无背书/未核查时应在模块 6 讨论该证据的脆弱性。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0424 | original/ACMG_CRITERIA.md:424 | 3.5.6 ✅ PM1 赋值前五问自检清单（强制） | ### 3.5.6 ✅ PM1 赋值前五问自检清单（强制） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0426 | original/ACMG_CRITERIA.md:426 | 3.5.6 ✅ PM1 赋值前五问自检清单（强制） | 赋 PM1 前逐条自检，**任一条答不上即不赋或降级**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0428 | original/ACMG_CRITERIA.md:428 | 3.5.6 ✅ PM1 赋值前五问自检清单（强制） |  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0429 | original/ACMG_CRITERIA.md:429 | 3.5.6 ✅ PM1 赋值前五问自检清单（强制） | □ 1. 这个域的功能是【实验确立】的疾病核心机制吗？（不是仅 Pfam/InterPro 序列注释） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0430 | original/ACMG_CRITERIA.md:430 | 3.5.6 ✅ PM1 赋值前五问自检清单（强制） | □ 2. 我【查过 gnomAD】，确认该域内【没有】良性/常见错义变异吗？ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0431 | original/ACMG_CRITERIA.md:431 | 3.5.6 ✅ PM1 赋值前五问自检清单（强制） | □ 3. 该位点或紧邻位点有【多个独立致病变异聚集】（热点证据）吗？ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0432 | original/ACMG_CRITERIA.md:432 | 3.5.6 ✅ PM1 赋值前五问自检清单（强制） | □ 4. 这个基因有【VCEP 规则】吗？若有，它如何规定 PM1（停用 / 限定坐标 / 调强度）？ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0433 | original/ACMG_CRITERIA.md:433 | 3.5.6 ✅ PM1 赋值前五问自检清单（强制） | □ 5. 我是否已用 PP3 或 PS3？若用了，PM1 是否与之【重复计数】？ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0434 | original/ACMG_CRITERIA.md:434 | 3.5.6 ✅ PM1 赋值前五问自检清单（强制） |  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0436 | original/ACMG_CRITERIA.md:436 | 3.5.6 ✅ PM1 赋值前五问自检清单（强制） | - 全部通过 → 可赋 PM1（或按 VCEP 调强度）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0437 | original/ACMG_CRITERIA.md:437 | 3.5.6 ✅ PM1 赋值前五问自检清单（强制） | - 门槛 1/2/3 任一不满足 → **不赋 PM1**。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0438 | original/ACMG_CRITERIA.md:438 | 3.5.6 ✅ PM1 赋值前五问自检清单（强制） | - 仅门槛 2 因检索受限未完成 → 可降为 **PM1_Supporting** 并醒目标注"未完成域内良性变异核查，证据强度待人工确认"。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0439 | original/ACMG_CRITERIA.md:439 | 3.5.6 ✅ PM1 赋值前五问自检清单（强制） | - 门槛 5 发现与 PP3/PS3 重叠 → 临界判定时优先舍弃 PM1，保住证据独立性。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0441 | original/ACMG_CRITERIA.md:441 | 3.5.7 错误与正确示例 | ### 3.5.7 错误与正确示例 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0443 | original/ACMG_CRITERIA.md:443 | 3.5.7 错误与正确示例 | - ⛔ **错误（AI 典型）**："变异落在 SNF2 解旋酶域，该域高度保守，REVEL 0.94 → PM1 + PP3_Strong 同时赋予。" 问题：未查域内良性变异、无 VCE | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0444 | original/ACMG_CRITERIA.md:444 | 3.5.7 错误与正确示例 | - ✅ **正确**："变异落在已有多个独立致病错义聚集的功能域，文献/实验确认该域为催化核心，gnomAD 该域内无良性错义，且 VCEP 明确该坐标区间适用 PM1 → 赋 PM1。已用 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0446 | original/ACMG_CRITERIA.md:446 | 3.5.7 错误与正确示例 | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0448 | original/ACMG_CRITERIA.md:448 | 3.6 PS1 / PM5：同位点已知致病变异（⟦培训班⟧ 新增，潘丹丹/马祎楠） | ## 3.6 PS1 / PM5：同位点已知致病变异（⟦培训班⟧ 新增，潘丹丹/马祎楠） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0450 | original/ACMG_CRITERIA.md:450 | 3.6.1 适用类型与前提 | ### 3.6.1 适用类型与前提 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0451 | original/ACMG_CRITERIA.md:451 | 3.6.1 适用类型与前提 | - **PS1**（Supporting→Strong）：与已知 P/LP 变异导致**相同氨基酸改变**的不同核苷酸变异。适用：错义、起始密码子、剪接供/受体基序（见 §1.8 矩阵）、n | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0452 | original/ACMG_CRITERIA.md:452 | 3.6.1 适用类型与前提 | - **PM5**（Moderate）：与已知 P/LP 变异位于**同一氨基酸残基**但导致不同氨基酸改变。适用：错义、框内 del/dup（须先满足 PM4）。⛔ ±10 aa 内的邻近 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0453 | original/ACMG_CRITERIA.md:453 | 3.6.1 适用类型与前提 | - 待评变异与已知变异的**表型须相同**（不同氨基酸改变可致不同表型/机制，GOF 基因尤须谨慎）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0454 | original/ACMG_CRITERIA.md:454 | 3.6.1 适用类型与前提 | - 错义若最可能机制为剪接 → PS1 慎用、PM5 不用；参考变异本身须无剪接影响。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0455 | original/ACMG_CRITERIA.md:455 | 3.6.1 适用类型与前提 | - ⛔ **循环引用禁令**：已知 P/LP 变异的评级不得依赖 PS1/PM5（反例：c.34G>C 用 PS1_M(c.34G>T)，而 c.34G>T 又用 PS1_M(c.34G>C | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0456 | original/ACMG_CRITERIA.md:456 | 3.6.1 适用类型与前提 | - PS1 本质是"借用"已知变异的临床证据，建议有独立文献/ClinVar 多提交支持。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0458 | original/ACMG_CRITERIA.md:458 | 3.6.2 强度分档 | ### 3.6.2 强度分档 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0459 | original/ACMG_CRITERIA.md:459 | 3.6.2 强度分档 | \| 情形 \| 强度 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0460 | original/ACMG_CRITERIA.md:460 | 3.6.2 强度分档 | \|---\|---\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0461 | original/ACMG_CRITERIA.md:461 | 3.6.2 强度分档 | \| PS1：已知变异为 P \| PS1（+4） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0462 | original/ACMG_CRITERIA.md:462 | 3.6.2 强度分档 | \| PS1：已知变异为 LP \| PS1_Moderate（+2） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0463 | original/ACMG_CRITERIA.md:463 | 3.6.2 强度分档 | \| PM5：已知 P，且待评 Grantham ≥ 已知 \| PM5（+2） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0464 | original/ACMG_CRITERIA.md:464 | 3.6.2 强度分档 | \| PM5：已知 LP，或待评 Grantham < 已知 \| PM5_Supporting（+1） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0465 | original/ACMG_CRITERIA.md:465 | 3.6.2 强度分档 | \| PM5_Strong：同密码子 ≥2 个**不同**致病错义改变（须 VCEP/SVI 支持，并核实与 PM1 独立） \| PM5_Strong（+4）（马祎楠 HRAS Gly13 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0467 | original/ACMG_CRITERIA.md:467 | 3.6.2 强度分档 | ACGS 2024 的 PM5 细则（REVEL/Grantham 组合表）以原文为准。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0469 | original/ACMG_CRITERIA.md:469 | 3.6.3 互斥 | ### 3.6.3 互斥 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0470 | original/ACMG_CRITERIA.md:470 | 3.6.3 互斥 | PS1/PM5 互斥；PS1/PM5 不与 PM1、PP2、PM4 共用（§3.5.2、§1.10）；PVS1 + PM5 默认不共用，VCEP 明文允许者除外（BRCA1 c.68_69d | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0472 | original/ACMG_CRITERIA.md:472 | 3.6.3 互斥 | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0474 | original/ACMG_CRITERIA.md:474 | 4. 家系与表型证据：PS2/PM6 / PM3 / PP1 / PP4 | ## 4. 家系与表型证据：PS2/PM6 / PM3 / PP1 / PP4 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0476 | original/ACMG_CRITERIA.md:476 | 4.1 PS2 / PM6（De novo — ClinGen SVI 2018 量化框架 + 李茹/徐博成） | ### 4.1 PS2 / PM6（De novo — ClinGen SVI 2018 量化框架 + 李茹/徐博成） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0478 | original/ACMG_CRITERIA.md:478 | 4.1.0 核心范式转变（必读） | #### 4.1.0 核心范式转变（必读） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0480 | original/ACMG_CRITERIA.md:480 | 4.1.0 核心范式转变（必读） | ClinGen SVI 工作组 2018 发布 *Recommendation for de novo Criteria (PS2 & PM6)*（Version 1.0, 2018-03； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0482 | original/ACMG_CRITERIA.md:482 | 4.1.0 核心范式转变（必读） | **关键认识**：在 SVI 框架下，PS2 与 PM6 不再是两条独立证据，而是**同一条"de novo 证据"在不同亲缘核验状态下的两个入口**。两者共用同一套积分，只是亲缘未核验时每 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0484 | original/ACMG_CRITERIA.md:484 | 4.1.1 双轴量化模型 | #### 4.1.1 双轴量化模型 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0486 | original/ACMG_CRITERIA.md:486 | 4.1.1 双轴量化模型 | de novo 证据强度由两个独立维度共同决定： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0488 | original/ACMG_CRITERIA.md:488 | 4.1.1 双轴量化模型 | **轴 1 — 表型/基因疾病特异性（每例 de novo 的基础分值）**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0490 | original/ACMG_CRITERIA.md:490 | 4.1.1 双轴量化模型 | \| 表型一致性档位 \| 判定标准 \| 已核验每例分值 \| 未核验每例分值 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0491 | original/ACMG_CRITERIA.md:491 | 4.1.1 双轴量化模型 | \|---------------\|---------\|--------------\|--------------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0492 | original/ACMG_CRITERIA.md:492 | 4.1.1 双轴量化模型 | \| **高度特异（Phenotype highly specific, single gene）** \| 表型高度匹配 + 基因疾病为可识别的单一/特异表型（如甲型血友病、Rett 综合 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0493 | original/ACMG_CRITERIA.md:493 | 4.1.1 双轴量化模型 | \| **一致（Consistent + 基因疾病有遗传异质性）** \| 表型符合，但同表型可由多个基因致病（如有一定特征的 NDD） \| **+1.0** \| +0.5 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0494 | original/ACMG_CRITERIA.md:494 | 4.1.1 双轴量化模型 | \| **广义符合（Consistent，疾病谱很宽 / 高度异质）** \| 表型与基因谱仅广义吻合（如非特异"发育迟缓"、孤立软指标） \| **+0.5** \| +0.25 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0495 | original/ACMG_CRITERIA.md:495 | 4.1.1 双轴量化模型 | \| **不一致（Not consistent）** \| 表型与基因已知谱不符 \| **0**（不适用 PS2/PM6） \| 0 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0497 | original/ACMG_CRITERIA.md:497 | 4.1.1 双轴量化模型 | **轴 2 — 亲缘关系核验状态（决定走哪条通道、是否折半）**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0498 | original/ACMG_CRITERIA.md:498 | 4.1.1 双轴量化模型 | - **已核验**（trio-WES/WGS 含样本身份核验、或 STR/SNP 亲缘一致性分析）→ 走 PS2 通道，全权重 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0499 | original/ACMG_CRITERIA.md:499 | 4.1.1 双轴量化模型 | - **未核验**（仅父母 Sanger 阴性，无亲缘核验）→ 走 PM6 通道，权重折半 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0501 | original/ACMG_CRITERIA.md:501 | 4.1.2 五档强度积分阈值（PS2 与 PM6 共用） | #### 4.1.2 五档强度积分阈值（PS2 与 PM6 共用） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0503 | original/ACMG_CRITERIA.md:503 | 4.1.2 五档强度积分阈值（PS2 与 PM6 共用） | 将所有已报道 de novo 病例按上表权重累加为 **de novo total points**，对照下表定级： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0505 | original/ACMG_CRITERIA.md:505 | 4.1.2 五档强度积分阈值（PS2 与 PM6 共用） | \| 累计积分 \| 已核验主导 → 命名 \| 未核验主导 → 命名 \| Bayesian 积分 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0506 | original/ACMG_CRITERIA.md:506 | 4.1.2 五档强度积分阈值（PS2 与 PM6 共用） | \|---------\|-----------------\|-----------------\|-------------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0507 | original/ACMG_CRITERIA.md:507 | 4.1.2 五档强度积分阈值（PS2 与 PM6 共用） | \| ≥ 4.0 \| **PS2_VeryStrong** \| **PM6_VeryStrong** \| +8 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0508 | original/ACMG_CRITERIA.md:508 | 4.1.2 五档强度积分阈值（PS2 与 PM6 共用） | \| 2.0 – 3.5 \| **PS2（原级 Strong）** \| **PM6_Strong** \| +4 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0509 | original/ACMG_CRITERIA.md:509 | 4.1.2 五档强度积分阈值（PS2 与 PM6 共用） | \| 1.0 – 1.5 \| **PS2_Moderate** \| **PM6（原级 Moderate）** \| +2 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0510 | original/ACMG_CRITERIA.md:510 | 4.1.2 五档强度积分阈值（PS2 与 PM6 共用） | \| 0.5 \| **PS2_Supporting** \| **PM6_Supporting** \| +1 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0511 | original/ACMG_CRITERIA.md:511 | 4.1.2 五档强度积分阈值（PS2 与 PM6 共用） | \| < 0.5 \| 不达门槛，不用 \| 不达门槛，不用 \| 0 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0513 | original/ACMG_CRITERIA.md:513 | 4.1.2 五档强度积分阈值（PS2 与 PM6 共用） | **两个最常被忽视的要点**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0514 | original/ACMG_CRITERIA.md:514 | 4.1.2 五档强度积分阈值（PS2 与 PM6 共用） | 1. **PM6 可升级，最高至 PM6_VeryStrong**——许多实验室仍把 PM6 锁死在中等档，这是误区。多例未核验 de novo 累积即可突破。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0515 | original/ACMG_CRITERIA.md:515 | 4.1.2 五档强度积分阈值（PS2 与 PM6 共用） | 2. **单例 + 已核验 + 高度特异 = 2.0 分 = 恰好 PS2 原级**——这是"trio 阳性 + 典型综合征"的标准赋值锚点。若表型仅"一致"（异质性高），单例已核验也只到  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0517 | original/ACMG_CRITERIA.md:517 | 4.1.3 病例累积与混合计分 | #### 4.1.3 病例累积与混合计分 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0519 | original/ACMG_CRITERIA.md:519 | 4.1.3 病例累积与混合计分 | - **多例累积**：两例已核验 + 高度特异 = 2+2 = 4 分 → PS2_VeryStrong（错义变异借此获得相当于 PVS1 的强度，意义重大）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0520 | original/ACMG_CRITERIA.md:520 | 4.1.3 病例累积与混合计分 | - **PS2/PM6 混合**：已核验与未核验病例可在**同一总分内按各自权重累加**；报告时按主导证据类型命名，或拆分双标（如 PS2 + PM6_Strong）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0521 | original/ACMG_CRITERIA.md:521 | 4.1.3 病例累积与混合计分 | - **跨家系计数**：即使非同一家系，文献中报道的、表型符合的独立 de novo 病例均可计入总分（李茹）。⟦培训班⟧ 跨报道计数须按患者**去重**；多例 de novo 既可累进 P | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0522 | original/ACMG_CRITERIA.md:522 | 4.1.3 病例累积与混合计分 | - ⟦培训班⟧ **AR 基因中的新发变异**（胡婷）：反式位置有已知 P/LP 时可用 PS2；该基因无其他已知 P/LP 时 PS2 强度降一级。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0524 | original/ACMG_CRITERIA.md:524 | 4.1.4 先决条件与降级/失效情形 | #### 4.1.4 先决条件与降级/失效情形 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0526 | original/ACMG_CRITERIA.md:526 | 4.1.4 先决条件与降级/失效情形 | **先决条件（缺一即不可用）**：患者表型必须与疾病基因已知表型谱相符（轴 1 ≠ "不一致"）。表型完全不符 → 0 分 → 不能用 PS2/PM6，**即便分子上确为 de novo** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0528 | original/ACMG_CRITERIA.md:528 | 4.1.4 先决条件与降级/失效情形 | **需取消或下调赋值的情形**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0529 | original/ACMG_CRITERIA.md:529 | 4.1.4 先决条件与降级/失效情形 | - 后续证实样本错配 / 非亲生 → de novo 前提崩塌，PS2/PM6 撤销 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0530 | original/ACMG_CRITERIA.md:530 | 4.1.4 先决条件与降级/失效情形 | - 发现父母低比例嵌合 → 严格意义不再是 de novo；降为"父母嵌合传递"（部分实验室计 PP1_Supporting 或不计），需评估再发风险 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0531 | original/ACMG_CRITERIA.md:531 | 4.1.4 先决条件与降级/失效情形 | - **父母 Sanger 假阴性陷阱**（PM6 最易高估处）：必须确认父母测序对该位点的技术覆盖（深度、引物覆盖、嵌合检出下限），否则"父母阴性"不可靠 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0533 | original/ACMG_CRITERIA.md:533 | 4.1.4 先决条件与降级/失效情形 | **文献计数分界（徐博成 docx）**：文献写明亲缘确定或 trio-WES/WGS 检出 → 计 PS2 通道；否则计 PM6 通道。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0535 | original/ACMG_CRITERIA.md:535 | 4.1.4 先决条件与降级/失效情形 | **特殊情况（李茹）**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0536 | original/ACMG_CRITERIA.md:536 | 4.1.4 先决条件与降级/失效情形 | - X 连锁：男性患者半合变异遗传自未患病杂合母亲，若母亲该变异为新发且家族史支持 → 可用 de novo 逻辑 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0537 | original/ACMG_CRITERIA.md:537 | 4.1.4 先决条件与降级/失效情形 | - 生殖腺嵌合：父母阴性但多个患病同胞 → 须先确认亲子关系才能用 de novo | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0538 | original/ACMG_CRITERIA.md:538 | 4.1.4 先决条件与降级/失效情形 | - ⟦培训班⟧ **传递亲代"隔代新发"**（胡婷病例 4）：变异遗传自无症状亲代，向上追溯祖代 + STR/SNP 亲缘核验证实在该亲代为新发 → 可按"传递亲代新发"计入 PM6/PS2 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0540 | original/ACMG_CRITERIA.md:540 | 4.1.4 先决条件与降级/失效情形 | ⟦培训班⟧ **胎儿合子后嵌合的 de novo（第四道门）**（蒋 FBXW7 案例，VAF 显著偏离 50%）：①核实 MAPQ/链偏斜/重复序列排除伪影；②判据：VAF 二项检验偏离  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0542 | original/ACMG_CRITERIA.md:542 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | #### 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0544 | original/ACMG_CRITERIA.md:544 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | > **设计动机**：产前胎儿表型尚未表达（认知/行为/癫痫/代谢等"看不见"），超声仅能捕捉结构与生长参数。直接套用产后综合征的"高度特异"档位会系统性高估 PS2/PM6。本表给出产前阶 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0546 | original/ACMG_CRITERIA.md:546 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | **第一步：判断产前可见表型与基因疾病的对应关系** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0548 | original/ACMG_CRITERIA.md:548 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | \| 产前情形 \| 表型一致性档位 \| 已核验赋值 \| 未核验赋值 \| 说明 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0549 | original/ACMG_CRITERIA.md:549 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | \|---------\|--------------\|-----------\|-----------\|------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0550 | original/ACMG_CRITERIA.md:550 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | \| 超声见**高度特异**结构标志，且该标志对应**单一基因病**（如 TSC2 + 心脏横纹肌瘤；ARPKD 典型双肾改变 + PKHD1） \| 高度特异 \| PS2（单例 2.0） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0551 | original/ACMG_CRITERIA.md:551 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | \| 超声见结构异常，**符合**基因谱但该表型**多基因可致**（如孤立 CHD、孤立 NTD、孤立侧脑室扩张） \| 一致（异质） \| PS2_Moderate（单例 1.0） \|  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0552 | original/ACMG_CRITERIA.md:552 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | \| ⟦培训班⟧ 超声见结构异常组合，且**该基因已有 ≥1 例文献报道的胎儿期相同结构表型**（"基因 AND fetus/prenatal"检索命中，须写明 PMID） \| 一致（基因 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0553 | original/ACMG_CRITERIA.md:553 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | \| ⟦培训班⟧ 引产后尸检/外观/影像见综合征**特异体征**（如 CdLS 的连眉、浓眉、上唇薄、多毛） \| 按产后标准定档 \| 可至 PS2 原级 \| PM6 \| 阴凯丽 NI | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0554 | original/ACMG_CRITERIA.md:554 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | \| 超声仅见**非特异软指标或生长偏离**（如单纯头围偏小、单纯股骨短、单纯 NT 增厚、单脐动脉），与神经发育基因仅广义相关 \| 广义符合 \| PS2_Supporting（单例 0 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0555 | original/ACMG_CRITERIA.md:555 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | \| 胎儿**无任何结构/生长异常**（变异为偶然发现 / 扩展性检测检出） \| 不一致 / 无表型 \| **不赋 PS2/PM6** \| 不赋 \| 无表型锚点，de novo 不能 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0557 | original/ACMG_CRITERIA.md:557 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | **第二步：产前专项调整原则** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0559 | original/ACMG_CRITERIA.md:559 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | 1. **产前"高度特异"门槛极高**：仅当结构标志本身对某单基因病有近乎特异的指向时才可用（参 4.4 符芳 PP4 产前案例）。绝大多数产前表型应落在"一致（异质）"或"广义符合"。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0560 | original/ACMG_CRITERIA.md:560 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | 2. **非特异生长参数不升档**：头围、股骨、腹围等单一生长偏离（如 −1.7 SD 头围）属"广义符合"上限，不可当作"高度特异"——这类参数的病因极度异质（家族性、胎盘、染色体、单基因 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0561 | original/ACMG_CRITERIA.md:561 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | 3. **产后表型出现后可回溯升档**：若继续妊娠、出生后出现基因特异性表型（如 PMNDS 的言语迟缓/癫痫/行为障碍），表型一致性档位可由"广义符合"回溯升至"一致"乃至"高度特异"，相 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0562 | original/ACMG_CRITERIA.md:562 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | 4. **优先用分子证据撑分级**：产前阶段 de novo 表型证据天然受限时，应让 PP3（计算预测，如 REVEL/AlphaMissense）、PM1（结构域）、PM2（频率）等不依 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0563 | original/ACMG_CRITERIA.md:563 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | 5. **诚实记录档位选择理由**：报告模块 3 须写明本例落在哪一档及依据，避免事后争议。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0564 | original/ACMG_CRITERIA.md:564 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | 6. ⟦培训班⟧ **"尚未出现"≠"不一致"**（蒋 PTPN11 案例）：胎儿表型须先与该基因**已报道的胎儿期表型谱**核对（Step 0.7 P0），并按 HPO 三态标注（存在 / | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0565 | original/ACMG_CRITERIA.md:565 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | 7. ⟦培训班⟧ **非特异表型也可选择暂不赋 PS2**（胡婷 NIPBL 案例做法）：产前仅非特异软指标时，"PS2_Supporting（0.5）"与"暂不赋、待生后重分析"两种做法均 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0567 | original/ACMG_CRITERIA.md:567 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | **产前 de novo 计分速查**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0569 | original/ACMG_CRITERIA.md:569 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） |  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0570 | original/ACMG_CRITERIA.md:570 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） | 单例胎儿 de novo： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0571 | original/ACMG_CRITERIA.md:571 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） |   亲缘已核验 + 高度特异结构标志(罕见)        → PS2          (2.0 → +4 Bayesian) | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0572 | original/ACMG_CRITERIA.md:572 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） |   亲缘已核验 + 一致(多基因可致的结构异常)    → PS2_Moderate (1.0 → +2) | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0573 | original/ACMG_CRITERIA.md:573 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） |   亲缘已核验 + 广义符合(非特异软指标/生长)   → PS2_Supporting(0.5 → +1) | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0574 | original/ACMG_CRITERIA.md:574 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） |   亲缘未核验 + 高度特异结构标志(罕见)        → PM6          (1.0 → +2) | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0575 | original/ACMG_CRITERIA.md:575 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） |   亲缘未核验 + 一致                          → PM6_Supporting(0.5 → +1) | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0576 | original/ACMG_CRITERIA.md:576 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） |   亲缘未核验 + 广义符合                      → 0.25，不达门槛(0) | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0577 | original/ACMG_CRITERIA.md:577 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） |   无任何胎儿表型                             → 不赋 PS2/PM6 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0578 | original/ACMG_CRITERIA.md:578 | 4.1.5 🤰 产前 de novo 表型特异性分级决策表（产前模式专用） |  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0580 | original/ACMG_CRITERIA.md:580 | 4.1.6 🔑 PS2/PM6/PS4 与 PP4 不叠加（ACGS 2024 — 徐博成/符芳） | #### 4.1.6 🔑 PS2/PM6/PS4 与 PP4 不叠加（ACGS 2024 — 徐博成/符芳） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0582 | original/ACMG_CRITERIA.md:582 | 4.1.6 🔑 PS2/PM6/PS4 与 PP4 不叠加（ACGS 2024 — 徐博成/符芳） | > If PS2/PM6 is applied, the specificity of that patient's phenotype to the relevant disorder s | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0584 | original/ACMG_CRITERIA.md:584 | 4.1.6 🔑 PS2/PM6/PS4 与 PP4 不叠加（ACGS 2024 — 徐博成/符芳） | 即：用 PS2/PM6 时，表型特异性已通过 4.1.1 轴 1 计入 de novo 强度，**不再单独叠加 PP4**，否则同一份表型证据双重计数。产前场景尤须警惕（产前 PP4 本就受 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0586 | original/ACMG_CRITERIA.md:586 | 4.1.8 亲代传递变异的处理 ⟦培训班⟧（余丽华 TUBB 案例、蒋 COL1A1 案例） | #### 4.1.8 亲代传递变异的处理 ⟦培训班⟧（余丽华 TUBB 案例、蒋 COL1A1 案例） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0588 | original/ACMG_CRITERIA.md:588 | 4.1.8 亲代传递变异的处理 ⟦培训班⟧（余丽华 TUBB 案例、蒋 COL1A1 案例） | 1. 遗传自"健康"亲代 ≠ 良性证据：在对亲代做**基因特异的靶向表型评估**之前（见 §2.3 四条 SOP），不得赋 BS4/BS2，也不得据此降级； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0589 | original/ACMG_CRITERIA.md:589 | 4.1.8 亲代传递变异的处理 ⟦培训班⟧（余丽华 TUBB 案例、蒋 COL1A1 案例） | 2. 亲代靶向评估阳性（即使亚临床，如头颅 MRI 细微改变）→ 亲代计为受累者，可计入 PP1 共分离（按减数分裂计数）与 PP4（受表型特异性限制）； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0590 | original/ACMG_CRITERIA.md:590 | 4.1.8 亲代传递变异的处理 ⟦培训班⟧（余丽华 TUBB 案例、蒋 COL1A1 案例） | 3. 亲代变异经祖代检测证实为**亲代自身新发** → 按 4.1.4"隔代新发"计入 PM6/PS2； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0591 | original/ACMG_CRITERIA.md:591 | 4.1.8 亲代传递变异的处理 ⟦培训班⟧（余丽华 TUBB 案例、蒋 COL1A1 案例） | 4. **亲代 VAF 核查**：亲代 VAF 在 40–60% 之外时须做二项检验 + 排除 indel 参考偏倚，判为亲代体细胞嵌合（蒋 COL1A1 母亲四路径 VAF 24.1/21 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0592 | original/ACMG_CRITERIA.md:592 | 4.1.8 亲代传递变异的处理 ⟦培训班⟧（余丽华 TUBB 案例、蒋 COL1A1 案例） | 5. 咨询：亲代亚临床 + 后代重症 = 表现度谱宽，预后措辞按 SKILL 报告措辞规范。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0594 | original/ACMG_CRITERIA.md:594 | 4.1.9 嵌合 ⟦培训班⟧（王剑） | #### 4.1.9 嵌合 ⟦培训班⟧（王剑） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0596 | original/ACMG_CRITERIA.md:596 | 4.1.9 嵌合 ⟦培训班⟧（王剑） | - 分类：体细胞嵌合 / 生殖腺嵌合 / 两者兼有 / 限制性胎盘嵌合（CPM），对再发风险含义不同； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0597 | original/ACMG_CRITERIA.md:597 | 4.1.9 嵌合 ⟦培训班⟧（王剑） | - **至少两种技术检出才确立嵌合**（如 NGS + 数字 PCR/深度扩增子），单技术检出须结合超声谨慎解释； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0598 | original/ACMG_CRITERIA.md:598 | 4.1.9 嵌合 ⟦培训班⟧（王剑） | - 先证者外周血低 VAF（<20%）的表型匹配基因变异**不得因软件 cutoff 被丢弃**，须手动 pileup 并正交验证； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0599 | original/ACMG_CRITERIA.md:599 | 4.1.9 嵌合 ⟦培训班⟧（王剑） | - 亲代嵌合评估须写明检测 LOD（Sanger >10–15%；NGS 视深度 ~1%）； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0600 | original/ACMG_CRITERIA.md:600 | 4.1.9 嵌合 ⟦培训班⟧（王剑） | - 嵌合变异的 ACMG 评级与非嵌合相同，但报告须单列 VAF 与组织来源；再发风险按 §4.1.8 第 4 条。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0602 | original/ACMG_CRITERIA.md:602 | 4.1.7 参考文献与工具 | #### 4.1.7 参考文献与工具 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0604 | original/ACMG_CRITERIA.md:604 | 4.1.7 参考文献与工具 | - ClinGen SVI *Recommendation for de novo Criteria (PS2 & PM6)* Version 1.1（2018-03 发布，2021-05  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0605 | original/ACMG_CRITERIA.md:605 | 4.1.7 参考文献与工具 | - 积分制底层依据：*Fitting a naturally scaled point system to the ACMG/AMP variant classification guide | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0606 | original/ACMG_CRITERIA.md:606 | 4.1.7 参考文献与工具 | - VCEP 对该框架的产前病例适配实例可参 RASopathy VCEP（明确了 prenatal cases 用于 PS2/PM6 与 PS4 的处理） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0607 | original/ACMG_CRITERIA.md:607 | 4.1.7 参考文献与工具 | - 表型特异性 HPO 量化辅助：可结合 HPO 词条与基因-HPO 关联库（https://hpo.jax.org/）判断轴 1 档位 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0608 | original/ACMG_CRITERIA.md:608 | 4.1.7 参考文献与工具 | - 亲缘核验：trio 测序的 SNP 一致性分析 / STR 鉴定报告 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0610 | original/ACMG_CRITERIA.md:610 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | ### 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0612 | original/ACMG_CRITERIA.md:612 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | **SVI PM3 积分表**（https://clinicalgenome.org/site/assets/files/3717/svi_proposal_for_pm3_criterio | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0614 | original/ACMG_CRITERIA.md:614 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | \| 对侧等位基因 \| 相位 \| 每例先证者分值 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0615 | original/ACMG_CRITERIA.md:615 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | \|---\|---\|---\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0616 | original/ACMG_CRITERIA.md:616 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | \| P/LP \| 反式已确定（父母来源/长读长/读段定相） \| 1.0 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0617 | original/ACMG_CRITERIA.md:617 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | \| P/LP \| 相位未知 \| 0.5 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0618 | original/ACMG_CRITERIA.md:618 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | \| 纯合（非近亲、非 ROH 内） \| — \| 0.5（纯合病例合计上限 1.0） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0619 | original/ACMG_CRITERIA.md:619 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | \| VUS \| 反式已确定 \| 0.25（VUS 病例合计上限 0.5；不得对同一对变异互相计满） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0620 | original/ACMG_CRITERIA.md:620 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | \| VUS \| 相位未知 \| 0 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0622 | original/ACMG_CRITERIA.md:622 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | 累计：0.5 → PM3_Supporting；1.0 → PM3；2.0 → PM3_Strong；4.0 → PM3_VeryStrong。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0624 | original/ACMG_CRITERIA.md:624 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | - 前提：待评变异与对侧变异均足够罕见（满足 PM2）；避免证据循环（对侧变异的评级不得依赖本变异的 PM3）；对侧变异升级后须重算本变异 PM3。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0625 | original/ACMG_CRITERIA.md:625 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | - **变异自身人群频率高时 PM3 须封顶**（GJB2 V37I：131 例复合杂合仍只给 Moderate）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0626 | original/ACMG_CRITERIA.md:626 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | - **AR 病用 PM3 不用 PS4 计罕见病例**；PM2 不适用的常见隐性变异（如 GJB2 c.109G>A）才考虑 PS4（按纯合/复合杂合**基因型**在患者 vs 对照中的富 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0627 | original/ACMG_CRITERIA.md:627 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | - **单亲定相推断**：父亲不可检，变异 A 母亲野生型（附近无可用 SNP）+ 变异 B 母源 → 推定反式，可赋 PM3（须注明未排除 A 为新发且与 B 顺式的小概率）；能做读段/S | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0628 | original/ACMG_CRITERIA.md:628 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | - **单人多变异**（USH2A 四变异案例）：同基因多变异必须用亲属或长读长定相，禁止仅凭 ClinVar 评级组合判定复合杂合。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0629 | original/ACMG_CRITERIA.md:629 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | - 本地病例库的第二家系同变异纯合 + 表型高度相符 → 可按上表计入 PM3（标注 Local cohort evidence (unpublished) 与病例数）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0630 | original/ACMG_CRITERIA.md:630 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | - **文献 in trans / unknown 判定（徐博成 docx）**：文献写明复合杂合、in trans、或有父母来源 → 认为 in trans；否则认为 unknown。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0631 | original/ACMG_CRITERIA.md:631 | 4.2 PM3（反式证据，AR 疾病 — ClinGen SVI PM3 点表，⟦培训班⟧ 胡婷/余丽华/李茹） | - PM3 与 PP1：若"反式鉴定"已用于共分离评估，二者不可同时计数；PM3 与 PP4 可叠加但 PP4 不得重复使用 PM3 已定义的亚表型要素。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0633 | original/ACMG_CRITERIA.md:633 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | ### 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0635 | original/ACMG_CRITERIA.md:635 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | **计数规则（ClinGen Gene Curation SOP；Zhang 2020 Curr Protoc Hum Genet 106:e98）**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0636 | original/ACMG_CRITERIA.md:636 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | - 分离计数按**减数分裂次数**，不按家系成员数；一般情况 = 携带变异的受累个体数 − 1；多个家系分别计算后 LOD 累加。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0637 | original/ACMG_CRITERIA.md:637 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | - 计入：基因型+且表型+的个体；肯定携带者（obligate carrier）即使无表型也计入。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0638 | original/ACMG_CRITERIA.md:638 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | - 不计入：有表型未检测者；有变异无表型者（不计入 PP1，但在完全外显病中构成 BS4 反证）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0639 | original/ACMG_CRITERIA.md:639 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | - AR：父母基因型不明 = 顺反式不明，要求父母检测；携带者父母不计入；非共分离成员通常是先证者同胞；父母一方患病另一方携带者时 0.25/0.75 概率均替换为 0.5。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0640 | original/ACMG_CRITERIA.md:640 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | - XLR：女性肯定携带者计入；男性有变异有表型计入；男性传给女儿不计入；女性未受累杂合携带者不作反证（XCI）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0641 | original/ACMG_CRITERIA.md:641 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | - 印记基因（UBE3A 等）：只计表达亲本来源的传递；无症状沉默亲本传递不作非共分离。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0643 | original/ACMG_CRITERIA.md:643 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | **LOD → PP1 强度（Jarvik & Browning 2016, AJHG, PMID:27236918；本技能默认标尺）**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0645 | original/ACMG_CRITERIA.md:645 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | \| 减数分裂次数 \| LOD（≈ n·log10 2） \| PP1 强度 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0646 | original/ACMG_CRITERIA.md:646 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | \|---\|---\|---\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0647 | original/ACMG_CRITERIA.md:647 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | \| 3–4 \| 0.9–1.2 \| PP1_Supporting \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0648 | original/ACMG_CRITERIA.md:648 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | \| 5–6 \| 1.5–1.8 \| PP1_Moderate \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0649 | original/ACMG_CRITERIA.md:649 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | \| ≥7 \| ≥2.1 \| PP1_Strong \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0651 | original/ACMG_CRITERIA.md:651 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | > 旧版 SKILL 用 LOD 0.6/1.2/2.4 三档且无出处，2026-09 改为上表。胡婷课件"5 次共分离 LOD 1.5 → PP1_Strong"引用的是基因-疾病有效性评 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0653 | original/ACMG_CRITERIA.md:653 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | - **ClinGen 2024 新规**：多基因座异质性疾病需将 PP1/BS4 证据分摊到每个候选基因/病例（PP1_gene = PP1_raw × 基因贡献占比，USH2A 占 RP | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0654 | original/ACMG_CRITERIA.md:654 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | - **PP1+PP4 合计单变异封顶 +5 分** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0655 | original/ACMG_CRITERIA.md:655 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | - ClinVar 提交者引用的**未公开内部共分离/病例数据**（无法独立复现）不计分，仅在模块 4 记录（蒋 FGD1 案例）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0657 | original/ACMG_CRITERIA.md:657 | 4.3 PP1 / BS4（共分离 — 符芳 ClinGen 2024 + 胡婷计数规则）⟦培训班⟧ | **BS4 四道门槛** ⟦培训班⟧：①证据形式是"受累家庭成员中未检出该变异"，而非"无表型成员检出该变异"（后者归 BS2）；②须先确认其他受累成员所患确为与先证者**相同**的遗传病， | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0659 | original/ACMG_CRITERIA.md:659 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | ### 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0661 | original/ACMG_CRITERIA.md:661 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | **ACMG 2015 定义**：患者表型/家族史高度特异于某单基因病。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0662 | original/ACMG_CRITERIA.md:662 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | **2017 解读四条件**：①检测灵敏度高 ②明确综合征症状（如戈尔林综合征）③该基因良性变异不多 ④家族史符合遗传方式。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0664 | original/ACMG_CRITERIA.md:664 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | **🔑 ClinGen 2024 路径（符芳）**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0665 | original/ACMG_CRITERIA.md:665 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | - **路径1 单基因病（基因座同质）**：评估诊断率 → 直接赋 PP4 到该基因变异 → **单变异 PP4 上限 +5 分** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0666 | original/ACMG_CRITERIA.md:666 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | - **路径2 多基因病（基因座异质）**：同表型对应多个致病基因 → **按比例分摊 PP4 权重** + 加 PP1/BS4 共分离 → 单变异封顶 +5 分 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0668 | original/ACMG_CRITERIA.md:668 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | **诊断率 → PP4 强度（ACGS 2024）** ⟦培训班⟧： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0670 | original/ACMG_CRITERIA.md:670 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | \| 该表型在该基因的诊断率 \| PP4 强度 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0671 | original/ACMG_CRITERIA.md:671 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | \|---\|---\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0672 | original/ACMG_CRITERIA.md:672 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | \| ≥50% \| 可考虑 Strong（上限 +5，VCEP 如 FBN1 满足 Ghent 标准封顶 +5） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0673 | original/ACMG_CRITERIA.md:673 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | \| 10–50% \| 通常 Moderate \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0674 | original/ACMG_CRITERIA.md:674 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | \| <10% \| Supporting，甚至不用 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0676 | original/ACMG_CRITERIA.md:676 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | 高诊断率是充分条件而非必要条件，仍须经基因座异质性校正；🤰 产前须用**产前队列**诊断率，无产前数据时降一档或不用。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0678 | original/ACMG_CRITERIA.md:678 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | **路径 2 分摊三步法** ⟦培训班⟧：①查该表型的总诊断率（如 HCM 全部致病基因合计约 60%）；②查该基因贡献占比（MYH7 约 33%、MYBPC3 15–20%；来源 Gene | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0680 | original/ACMG_CRITERIA.md:680 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | **VCEP PP4 实例**：FBN1（Ghent 满足 = +5 封顶，儿童 Ghent 状态动态随访，不重复用于 PS4）；F8/F9（临床诊断依赖单一实验室指标 FVIII:C/FI | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0682 | original/ACMG_CRITERIA.md:682 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | **其他 PP4 来源** ⟦培训班⟧：①患者来源细胞的疾病机制特异功能异常在无法归因单变异时计 PP4（见 §3.3）；②复发家系中前一胎/同胞的已证实表型可并入 HPO 集合（须确认为同 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0684 | original/ACMG_CRITERIA.md:684 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | **🤰 产前 PP4 局限（符芳 — 产前最关键警示）**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0685 | original/ACMG_CRITERIA.md:685 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | 1. HPO 仅约 10% 词条适用产前；产前多为非特异结构异常，无法获取面容/神经行为/代谢特征 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0686 | original/ACMG_CRITERIA.md:686 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | 2. 基因座异质性普遍：骨骼发育不良、先心病、中枢畸形多基因可致；产前 HPO 词条常匹配多基因多病 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0687 | original/ACMG_CRITERIA.md:687 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | 3. 胎儿期外显率不明确，产前表型可能无法识别 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0688 | original/ACMG_CRITERIA.md:688 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | 4. 家族史常不完整/不可靠（父母表型可隐匿） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0690 | original/ACMG_CRITERIA.md:690 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | **🤰 产前 PP4 五原则（符芳个人思考，建议纳入产前模式）**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0691 | original/ACMG_CRITERIA.md:691 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | 1. **宁缺毋滥**：无明确疾病对应、无 HPO 绑定基因时不强行赋 PP4 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0692 | original/ACMG_CRITERIA.md:692 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | 2. **不盲套产后**：产前"特异表型"不等价高基因阳性率，盲套产后诊断率致 PP4 虚高 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0693 | original/ACMG_CRITERIA.md:693 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | 3. **保持怀疑**：单一超声表型背后常隐藏多基因甚至非遗传病因；基因座同质假设是最危险陷阱 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0694 | original/ACMG_CRITERIA.md:694 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | 4. **权重分配保守**：多基因候选时按 ClinGen 比例分配 + 封顶 +5，不全压单基因 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0695 | original/ACMG_CRITERIA.md:695 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | 5. **多学科协作**：超声精准描述 → 临床匹配 HPO → 实验室判断 PP4 适用性，形成闭环 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0697 | original/ACMG_CRITERIA.md:697 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | **PP4 产前案例分级参考（符芳）**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0698 | original/ACMG_CRITERIA.md:698 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | - PKHD1 复合杂合 + ARPKD 典型超声（双肾增大、回声增强、皮髓质不清、羊水过少）→ 可用 PP4 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0699 | original/ACMG_CRITERIA.md:699 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | - PKD1 + 多囊肾家族史 5 代共分离 → PP1_Moderate + PP4 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0700 | original/ACMG_CRITERIA.md:700 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | - TSC2 + 心脏横纹肌瘤（高度特异）→ TSC 31%/69% 归因 TSC1/TSC2（GeneReviews），文献家系分离 5 次 → PP1_Moderate（本技能 Jarv | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0701 | original/ACMG_CRITERIA.md:701 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | - COL1A1 新发 + 成骨不全 → **用 PS2/PM6，不叠加 PP4** | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0702 | original/ACMG_CRITERIA.md:702 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | - GLI3 新发 + 轴前多指/并趾（HP:0001177/HP:0001770）→ 新发用 PS2 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0703 | original/ACMG_CRITERIA.md:703 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | - ⟦培训班⟧ 蒋宇林立场（更严）：产前 PP4 "近乎不可用"，建议**不折算分值、在报告中显式陈述表型吻合度**。本技能折中：保留五原则允许的计分情形，但产前报告**强制增加"表型吻合度 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0705 | original/ACMG_CRITERIA.md:705 | 4.4 PP4（表型特异性 — 符芳报告，ClinGen 2024 重大更新） | **产前 HPO 标准化（符芳）** ⟦培训班⟧：以 HP:0001197（产前发育异常）分支为检索锚点（PMID:35872606）；关键词提取规则——"解剖结构 + 形态改变"才是关键词 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0707 | original/ACMG_CRITERIA.md:707 | 4.5 🤰 产前表型的根本局限（李茹） | ### 4.5 🤰 产前表型的根本局限（李茹） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0709 | original/ACMG_CRITERIA.md:709 | 4.5 🤰 产前表型的根本局限（李茹） | 产前超声是**结构筛查工具，非功能预测工具**。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0710 | original/ACMG_CRITERIA.md:710 | 4.5 🤰 产前表型的根本局限（李茹） | - "能看见"（结构表型）：宏观畸形、生长参数、部分软指标 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0711 | original/ACMG_CRITERIA.md:711 | 4.5 🤰 产前表型的根本局限（李茹） | - "看不见"（功能/微观/迟发）：脑功能与认知（智力/ASD/精神行为）、代谢功能（多数代谢病胎儿期无结构异常）、感官（耳聋/视网膜病变）、肌肉运动、免疫血液、迟发病 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0712 | original/ACMG_CRITERIA.md:712 | 4.5 🤰 产前表型的根本局限（李茹） | - 后果：表型相关证据链（PS2/PM3/PP4）在产前使用受限；胎儿表型动态变化难做基因型-表型关联 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0714 | original/ACMG_CRITERIA.md:714 | 4.5 🤰 产前表型的根本局限（李茹） | **产前文献检索策略（李茹）**：基因 AND prenatal / 基因 AND fetus / 基因 AND HPO表型 [Title/Abstract]。即使待评估病例表型不相关，文献 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0716 | original/ACMG_CRITERIA.md:716 | 4.6 BP2 / BP5（⟦培训班⟧ 新增，旧版无定义） | ### 4.6 BP2 / BP5（⟦培训班⟧ 新增，旧版无定义） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0718 | original/ACMG_CRITERIA.md:718 | 4.6 BP2 / BP5（⟦培训班⟧ 新增，旧版无定义） | - **BP2**（Supporting）：显性完全外显病中与已知致病变异**反式**、或任意遗传模式下与已知致病变异**顺式**检出，且该致病变异足以解释表型。例外：修饰变异顺式；复杂等位 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0719 | original/ACMG_CRITERIA.md:719 | 4.6 BP2 / BP5（⟦培训班⟧ 新增，旧版无定义） | - **BP5**（Supporting）：已找到其他分子病因的病例中检出。BP5 不与 BP2 共用；不可对同一被检者既作非共分离解释又作替代病因。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0720 | original/ACMG_CRITERIA.md:720 | 4.6 BP2 / BP5（⟦培训班⟧ 新增，旧版无定义） | - 🤰 **产前 BP2/BP5 默认不赋**（蒋）：产前表型不完整，"已有解释"的判断本身不可靠；双重诊断并不罕见（KMT2E 队列中一例 PTEN 双重诊断），**找到致病变异后寻找不停 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0722 | original/ACMG_CRITERIA.md:722 | 4.7 X 连锁与性别相关模式（⟦培训班⟧ 王剑、韩瑾、蒋） | ### 4.7 X 连锁与性别相关模式（⟦培训班⟧ 王剑、韩瑾、蒋） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0724 | original/ACMG_CRITERIA.md:724 | 4.7 X 连锁与性别相关模式（⟦培训班⟧ 王剑、韩瑾、蒋） | - XLR：女性杂合"无表型"母亲不构成 BS4/BS2（XCI 随机/偏移），需 XCI 分析或靶向表型评估后再判；女性发病可由 XCI 偏移解释，不得因此否定变异；共分离计数按 §4.3 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0725 | original/ACMG_CRITERIA.md:725 | 4.7 X 连锁与性别相关模式（⟦培训班⟧ 王剑、韩瑾、蒋） | - XLD：男性半合致死（MECP2 经典型）或女性限性（PCDH19）——男胎/女胎的预后与再发风险不同，模块 8′ 须按胎儿性别分写；产前基因为 X 连锁且性别未知时，模块 8′ 首条行 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0726 | original/ACMG_CRITERIA.md:726 | 4.7 X 连锁与性别相关模式（⟦培训班⟧ 王剑、韩瑾、蒋） | - 限性/从性遗传：对"不表现性别"的携带者不计 BS2/BS4。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0727 | original/ACMG_CRITERIA.md:727 | 4.7 X 连锁与性别相关模式（⟦培训班⟧ 王剑、韩瑾、蒋） | - X 连锁 VUS：定向追问母系男性远亲（表舅等）并采血验证（胡婷病例 1）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0728 | original/ACMG_CRITERIA.md:728 | 4.7 X 连锁与性别相关模式（⟦培训班⟧ 王剑、韩瑾、蒋） | - 半合子 BS2 计数按 §2.3。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0730 | original/ACMG_CRITERIA.md:730 | 4.8 印记基因与 UPD（⟦培训班⟧ 王剑、蒋 UBE3A） | ### 4.8 印记基因与 UPD（⟦培训班⟧ 王剑、蒋 UBE3A） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0732 | original/ACMG_CRITERIA.md:732 | 4.8 印记基因与 UPD（⟦培训班⟧ 王剑、蒋 UBE3A） | 1. 变异位于印记基因（UBE3A、MAGEL2、SNRPN 区、CDKN1C、GNAS、KCNQ1OT1 区、MKRN3 等）时，**必须先确定亲源**； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0733 | original/ACMG_CRITERIA.md:733 | 4.8 印记基因与 UPD（⟦培训班⟧ 王剑、蒋 UBE3A） | 2. 来自沉默亲本的传递 → 携带者无表型，不构成 BS2/BS4，也不作"不外显"证据；来自表达亲本 → 才评估共分离与 PS2/PM6； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0734 | original/ACMG_CRITERIA.md:734 | 4.8 印记基因与 UPD（⟦培训班⟧ 王剑、蒋 UBE3A） | 3. 再发风险按传递亲本性别给出（MAGEL2 父传 50%；母传后代不发病但其子代男性可发病）； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0735 | original/ACMG_CRITERIA.md:735 | 4.8 印记基因与 UPD（⟦培训班⟧ 王剑、蒋 UBE3A） | 4. WES 见 AR 纯合变异伴大段 ROH 且父母仅一方携带 → 疑 iUPD，须 SNP-array/trio 核查并联想该染色体的印记疾病； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0736 | original/ACMG_CRITERIA.md:736 | 4.8 印记基因与 UPD（⟦培训班⟧ 王剑、蒋 UBE3A） | 5. 产前印记疾病检测须多技术联合（MS-MLPA 甲基化 + SNP-array + 测序），单一技术阴性不排除。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0738 | original/ACMG_CRITERIA.md:738 | 4.9 AR 病仅检出单一 P/LP 时的第二打击强制搜索（⟦培训班⟧ 王剑、符芳） | ### 4.9 AR 病仅检出单一 P/LP 时的第二打击强制搜索（⟦培训班⟧ 王剑、符芳） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0740 | original/ACMG_CRITERIA.md:740 | 4.9 AR 病仅检出单一 P/LP 时的第二打击强制搜索（⟦培训班⟧ 王剑、符芳） | 按序排查并在报告列出结果：①外显子级 CNV（读深/split reads；WES 推断者须正交验证 MLPA/qPCR）；②深内含子/非经典剪接（SpliceAI 全基因扫描）；③高频亚效 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0742 | original/ACMG_CRITERIA.md:742 | 4.10 双重诊断、双基因与修饰基因（⟦培训班⟧ 王剑、蒋） | ### 4.10 双重诊断、双基因与修饰基因（⟦培训班⟧ 王剑、蒋） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0744 | original/ACMG_CRITERIA.md:744 | 4.10 双重诊断、双基因与修饰基因（⟦培训班⟧ 王剑、蒋） | - 多基因多变异时每个变异独立评级；PP4 只按该基因能解释的**那部分表型**赋值，不因整体表型不像单一综合征而扣分； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0745 | original/ACMG_CRITERIA.md:745 | 4.10 双重诊断、双基因与修饰基因（⟦培训班⟧ 王剑、蒋） | - 两基因均达 P/LP 且表型互补 → 报告"双重诊断"，再发风险分别给出； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0746 | original/ACMG_CRITERIA.md:746 | 4.10 双重诊断、双基因与修饰基因（⟦培训班⟧ 王剑、蒋） | - 双基因/三等位/修饰基因组合（DIDA 收录）不能用单基因框架把每个成分强推到 P，报告为"双基因模式候选"并说明证据；SNV + CNV 组合按 TBX6 范式。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0747 | original/ACMG_CRITERIA.md:747 | 4.10 双重诊断、双基因与修饰基因（⟦培训班⟧ 王剑、蒋） | - 群体分层数字不套用于 n=1：引用队列比例前核对是否含同变异个体（KMT2E 男性癫痫 5% = 1/19 恰为本例）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0749 | original/ACMG_CRITERIA.md:749 | 4.11 🤰 产前样本前置质控：母体细胞污染（MCC）（⟦培训班⟧ 蒋、王剑） | ### 4.11 🤰 产前样本前置质控：母体细胞污染（MCC）（⟦培训班⟧ 蒋、王剑） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0751 | original/ACMG_CRITERIA.md:751 | 4.11 🤰 产前样本前置质控：母体细胞污染（MCC）（⟦培训班⟧ 蒋、王剑） | - 每例产前样本**强制定量 MCC**（STR 或 WES-VAF 算法），判读前准入阈值 5%；MCC ≥20% → 该样本基因型判定与本报告置信度降为 Low，建议重采样。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0752 | original/ACMG_CRITERIA.md:752 | 4.11 🤰 产前样本前置质控：母体细胞污染（MCC）（⟦培训班⟧ 蒋、王剑） | - 胎儿"杂合"变异若母亲同为杂合且胎儿 VAF 偏离 0.5，先排除 MCC 再谈遗传来源；MCC 未定量时 PS2/PM6 与 de novo 判定标注"未排除 MCC"，模块 1 Co | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0753 | original/ACMG_CRITERIA.md:753 | 4.11 🤰 产前样本前置质控：母体细胞污染（MCC）（⟦培训班⟧ 蒋、王剑） | - 报告模块 2 增加 MCC status: 行。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0755 | original/ACMG_CRITERIA.md:755 | 4.12 不适用本框架的变异类型（⟦培训班⟧ 王剑） | ### 4.12 不适用本框架的变异类型（⟦培训班⟧ 王剑） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0757 | original/ACMG_CRITERIA.md:757 | 4.12 不适用本框架的变异类型（⟦培训班⟧ 王剑） | - **重复扩展/动态突变**（FMR1、HTT、DMPK、ATXN 系列等）：不适用 ACMG SNV 框架，按各病重复数阈值（正常/中间/前突变/全突变）与遗传早现规则解读；常规 WES | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0758 | original/ACMG_CRITERIA.md:758 | 4.12 不适用本框架的变异类型（⟦培训班⟧ 王剑） | - **线粒体基因组变异**（m.xxxx、MT-xxx、chrM/MT 坐标）：须按 ClinGen mtDNA 专项规范（McCormick 2020）评级——PS2/PM6、PS1、内 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0760 | original/ACMG_CRITERIA.md:760 | 4.12 不适用本框架的变异类型（⟦培训班⟧ 王剑） | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0762 | original/ACMG_CRITERIA.md:762 | 5. PS4：病例-对照证据（高勇报告） | ## 5. PS4：病例-对照证据（高勇报告） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0764 | original/ACMG_CRITERIA.md:764 | 5.1 队列构建 | ### 5.1 队列构建 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0766 | original/ACMG_CRITERIA.md:766 | 5.1 队列构建 | - Case：精确可重复的表型定义 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0767 | original/ACMG_CRITERIA.md:767 | 5.1 队列构建 | - Control：人群匹配（尤其种族/祖源），避免人群分层假阳性 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0768 | original/ACMG_CRITERIA.md:768 | 5.1 队列构建 | - 来源：前瞻队列（理想）/ 现有库（gnomAD、UK Biobank，须基因分型质量、测序深度、变异调用流程一致）/ 文献汇总（注意异质性） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0770 | original/ACMG_CRITERIA.md:770 | 5.2 强度判定（LR 优于病例计数） | ### 5.2 强度判定（LR 优于病例计数） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0772 | original/ACMG_CRITERIA.md:772 | 5.2 强度判定（LR 优于病例计数） | **ACMG 2015 原始**：OR >5 且 95%CI 下限 >1 → 可考虑"强"；Fisher 精确检验算 P 值。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0774 | original/ACMG_CRITERIA.md:774 | 5.2 强度判定（LR 优于病例计数） | **基于似然比（LR）的分级（高勇，推荐）**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0776 | original/ACMG_CRITERIA.md:776 | 5.2 强度判定（LR 优于病例计数） | \| LR 范围 \| 证据点数 EPs \| 指向 \| 传统强度 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0777 | original/ACMG_CRITERIA.md:777 | 5.2 强度判定（LR 优于病例计数） | \|---------\|------------\|------\|---------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0778 | original/ACMG_CRITERIA.md:778 | 5.2 强度判定（LR 优于病例计数） | \| ≥350.4 \| ≥8 \| 致病 \| 极强 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0779 | original/ACMG_CRITERIA.md:779 | 5.2 强度判定（LR 优于病例计数） | \| 18.72–350.4 \| 4–8 \| 致病 \| 强 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0780 | original/ACMG_CRITERIA.md:780 | 5.2 强度判定（LR 优于病例计数） | \| 4.33–18.72 \| 2–4 \| 致病 \| 中等 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0781 | original/ACMG_CRITERIA.md:781 | 5.2 强度判定（LR 优于病例计数） | \| 2.08–4.33 \| 1–2 \| 致病 \| 支持 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0782 | original/ACMG_CRITERIA.md:782 | 5.2 强度判定（LR 优于病例计数） | \| 0.23–0.48 \| -1~-2 \| 良性 \| 支持 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0783 | original/ACMG_CRITERIA.md:783 | 5.2 强度判定（LR 优于病例计数） | \| 0.053–0.23 \| -2~-4 \| 良性 \| 中等 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0784 | original/ACMG_CRITERIA.md:784 | 5.2 强度判定（LR 优于病例计数） | \| 0.00285–0.053 \| -4~-8 \| 良性 \| 强 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0785 | original/ACMG_CRITERIA.md:785 | 5.2 强度判定（LR 优于病例计数） | \| ≤0.00285 \| ≤-8 \| 良性 \| 极强 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0787 | original/ACMG_CRITERIA.md:787 | 5.2 强度判定（LR 优于病例计数） | LR 计算器：https://turnbull-lab.shinyapps.io/ps4_lrcalc/ ；BayesQuantify 亦可计算 LR。OR 计算器：http://www.h | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0789 | original/ACMG_CRITERIA.md:789 | 5.2 强度判定（LR 优于病例计数） | **case-control 质量门槛** ⟦培训班⟧：不同文献的 case/control 不可相加；control 须实际对该变异做了基因分型；PM2 与 PS4 不可共用同一对照队列； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0791 | original/ACMG_CRITERIA.md:791 | 5.3 先证者计数法（无对照时，⟦培训班⟧ 潘丹丹/韩瑾） | ### 5.3 先证者计数法（无对照时，⟦培训班⟧ 潘丹丹/韩瑾） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0793 | original/ACMG_CRITERIA.md:793 | 5.3 先证者计数法（无对照时，⟦培训班⟧ 潘丹丹/韩瑾） | 前提：AD/XL 疾病；变异满足 PM2（罕见）；先证者表型相同。通用参考分档（耳聋 VCEP Oza 2018，PMID:30311386；其他基因先查 VCEP）： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0795 | original/ACMG_CRITERIA.md:795 | 5.3 先证者计数法（无对照时，⟦培训班⟧ 潘丹丹/韩瑾） | \| 无关先证者数 \| PS4 强度 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0796 | original/ACMG_CRITERIA.md:796 | 5.3 先证者计数法（无对照时，⟦培训班⟧ 潘丹丹/韩瑾） | \|---\|---\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0797 | original/ACMG_CRITERIA.md:797 | 5.3 先证者计数法（无对照时，⟦培训班⟧ 潘丹丹/韩瑾） | \| ≥15 \| PS4 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0798 | original/ACMG_CRITERIA.md:798 | 5.3 先证者计数法（无对照时，⟦培训班⟧ 潘丹丹/韩瑾） | \| 6–14 \| PS4_Moderate \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0799 | original/ACMG_CRITERIA.md:799 | 5.3 先证者计数法（无对照时，⟦培训班⟧ 潘丹丹/韩瑾） | \| 2–5 \| PS4_Supporting \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0801 | original/ACMG_CRITERIA.md:801 | 5.3 先证者计数法（无对照时，⟦培训班⟧ 潘丹丹/韩瑾） | 三注意：①同一变异须关联相同疾病才可叠加；②同一家系算 1 例；③不同文献中同一先证者不可重复计。锚点：FGFR3 p.Gly380Arg 58 例 → PS4（PMID:25614871） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0803 | original/ACMG_CRITERIA.md:803 | 5.3 先证者计数法（无对照时，⟦培训班⟧ 潘丹丹/韩瑾） | **🤰 中国人群数据缺口**：gnomAD 等公开库缺足够高质量中国人群数据，PS4 在中国产前场景应用受限，建议建本土队列。本地病例库/本地人群频率库/羊水表达基线库若由用户提供，按与文献 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0805 | original/ACMG_CRITERIA.md:805 | 5.3 先证者计数法（无对照时，⟦培训班⟧ 潘丹丹/韩瑾） | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0807 | original/ACMG_CRITERIA.md:807 | 6. 证据独立性、矛盾处理与重复计数审查 | ## 6. 证据独立性、矛盾处理与重复计数审查 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0809 | original/ACMG_CRITERIA.md:809 | 6.1 证据独立性原则（高勇） | ### 6.1 证据独立性原则（高勇） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0811 | original/ACMG_CRITERIA.md:811 | 6.1 证据独立性原则（高勇） | Bayesian 假设各证据独立。若一证据是另一证据的重复或必然结果，不可叠加。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0813 | original/ACMG_CRITERIA.md:813 | 6.2 证据优先级（李茹 2026-09 正式版，由高到低）⟦培训班⟧ | ### 6.2 证据优先级（李茹 2026-09 正式版，由高到低）⟦培训班⟧ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0815 | original/ACMG_CRITERIA.md:815 | 6.2 证据优先级（李茹 2026-09 正式版，由高到低）⟦培训班⟧ | **人群频率（BA1 独立；BS1/PM2）> 功能验证（PS3/BS3、PVS1(RNA)/BP7(RNA)）> 家系（PS2/PM6/PP1/BS4）> 相位（PM3/BP2）> 保守/ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0817 | original/ACMG_CRITERIA.md:817 | 6.2 证据优先级（李茹 2026-09 正式版，由高到低）⟦培训班⟧ | > 2026-05 备课会版本为"人群 > 家系 > 功能"，2026-09 正式讲稿更新为功能验证优先于家系并新增"相位"档；本技能按正式版。注意：无 RNA/功能实验时，PVS1/PM4 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0819 | original/ACMG_CRITERIA.md:819 | 6.2 证据优先级（李茹 2026-09 正式版，由高到低）⟦培训班⟧ | 最常见冲突：计算预测（PP3/BP4）vs 人群/流行病学（BA1/BS1/PM2）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0821 | original/ACMG_CRITERIA.md:821 | 6.3 矛盾证据处理原则（李茹） | ### 6.3 矛盾证据处理原则（李茹） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0823 | original/ACMG_CRITERIA.md:823 | 6.3 矛盾证据处理原则（李茹） | \| 原则 \| 说明 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0824 | original/ACMG_CRITERIA.md:824 | 6.3 矛盾证据处理原则（李茹） | \|------\|------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0825 | original/ACMG_CRITERIA.md:825 | 6.3 矛盾证据处理原则（李茹） | \| 优先考虑独立性 \| 用任何证据前检查来源是否与已有证据重叠 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0826 | original/ACMG_CRITERIA.md:826 | 6.3 矛盾证据处理原则（李茹） | \| 群体频率 > 计算预测 \| 冲突时人群频率权重更高 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0827 | original/ACMG_CRITERIA.md:827 | 6.3 矛盾证据处理原则（李茹） | \| 功能检测与计算预测非叠加 \| 需按基因/结构域实证 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0828 | original/ACMG_CRITERIA.md:828 | 6.3 矛盾证据处理原则（李茹） | \| 功能实验 > 计算预测（强度操作） \| PS3 ≥ Strong 与 BP4 方向相反时，BP4 至多 Supporting 或不计（§3.3） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0829 | original/ACMG_CRITERIA.md:829 | 6.3 矛盾证据处理原则（李茹） | \| 采用 Bayesian 量化 \| 定性矛盾转定量，避免主观 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0830 | original/ACMG_CRITERIA.md:830 | 6.3 矛盾证据处理原则（李茹） | \| 关注 VCEP 基因特异规则 \| 不同基因有特殊组合规则 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0831 | original/ACMG_CRITERIA.md:831 | 6.3 矛盾证据处理原则（李茹） | \| ⟦培训班⟧ 良性方向不得"托底" \| 其他证据均指向良性时，不得用 PP2/PM2 把变异托在 VUS（这是 6.4"PM2+BP4→VUS"的上位原则：后者仅指只有这两条证据的情形 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0832 | original/ACMG_CRITERIA.md:832 | 6.3 矛盾证据处理原则（李茹） | \| ⟦培训班⟧ PP5/BP6 已废止 \| ClinGen SVI 2018 废止 PP5/BP6，不赋值；外部实验室分类只进模块 4/5 对标（GeneBe 等自动工具仍在用 PP5， | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0833 | original/ACMG_CRITERIA.md:833 | 6.3 矛盾证据处理原则（李茹） | \| ⟦培训班⟧ 历史分类被推翻须标注 \| 曾为 P/LP 而现被 BA1/BS3 等推翻的变异，报告写"历史分类已被推翻"；仅因规则版本变化（PM2 降级、REVEL 阈值更新）的边界重 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0835 | original/ACMG_CRITERIA.md:835 | 6.4 冲突组合判定表（李茹） | ### 6.4 冲突组合判定表（李茹） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0837 | original/ACMG_CRITERIA.md:837 | 6.4 冲突组合判定表（李茹） | \| 冲突组合 \| 判定 \| 规则 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0838 | original/ACMG_CRITERIA.md:838 | 6.4 冲突组合判定表（李茹） | \|---------\|------\|------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0839 | original/ACMG_CRITERIA.md:839 | 6.4 冲突组合判定表（李茹） | \| BA1(AF>5%) + PP3/PS2 \| 良性(B) \| BA1 一票否决所有致病证据（白名单除外） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0840 | original/ACMG_CRITERIA.md:840 | 6.4 冲突组合判定表（李茹） | \| BS1 + PP3 \| LB/VUS \| BS1 权重 > PP3，频率越高越偏 LB \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0841 | original/ACMG_CRITERIA.md:841 | 6.4 冲突组合判定表（李茹） | \| BS1 + PS2(de novo) \| LP/VUS \| PS2 仍有效；BS1 强则降 VUS \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0842 | original/ACMG_CRITERIA.md:842 | 6.4 冲突组合判定表（李茹） | \| BS1 + PM6 \| VUS \| 冲突抵消 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0843 | original/ACMG_CRITERIA.md:843 | 6.4 冲突组合判定表（李茹） | \| PM2 + BP4 \| VUS \| 冲突抵消，需功能/家系验证 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0844 | original/ACMG_CRITERIA.md:844 | 6.4 冲突组合判定表（李茹） | \| PP3_Strong + PM2_Supporting \| VUS（5 分） \| 预测再高也只是预测，不得抬高 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0845 | original/ACMG_CRITERIA.md:845 | 6.4 冲突组合判定表（李茹） | \| PP3 与 BP4 \| 不计分 \| 预测不一致，互斥不用 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0847 | original/ACMG_CRITERIA.md:847 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | ### 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0849 | original/ACMG_CRITERIA.md:849 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | 五分类：**允许** / **谨慎**（附条件）/ **限制**（同一命题的两条证据合并后 ≤8 分）/ **禁止** / **不适用**。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0851 | original/ACMG_CRITERIA.md:851 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | **致病侧**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0853 | original/ACMG_CRITERIA.md:853 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| 证据对 \| 决策 \| 条件/理由 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0854 | original/ACMG_CRITERIA.md:854 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \|---\|---\|---\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0855 | original/ACMG_CRITERIA.md:855 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PVS1 + PM1 / PM4 / PP2 / PP3 \| 禁止 \| 同属机制预测 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0856 | original/ACMG_CRITERIA.md:856 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PM4 + PP3 \| 禁止 \| PVS1/PM4 为致病机制预测，PP3 不可额外叠加 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0857 | original/ACMG_CRITERIA.md:857 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PM4 + PM5 / PS1 / PP2 \| 禁止 \| PM5 仅错义同残基替换 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0858 | original/ACMG_CRITERIA.md:858 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PP2 + PM1 \| 禁止 \| 基因级 vs 结构域级约束（Garrett 2020） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0859 | original/ACMG_CRITERIA.md:859 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PP2/PM1 + PS1/PM5 \| 禁止 \| 同残基已计分；VCEP 明文允许除外 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0860 | original/ACMG_CRITERIA.md:860 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PM1 + PS3 \| 谨慎 \| 通用默认不叠加；VCEP 允许除外 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0861 | original/ACMG_CRITERIA.md:861 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PM1 + PP3 \| 限制 \| 合计 ≤ Strong \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0862 | original/ACMG_CRITERIA.md:862 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PVS1 + PM5 \| 谨慎 \| 默认不共用；免疫缺陷/乳腺癌 VCEP 例外 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0863 | original/ACMG_CRITERIA.md:863 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PVS1(RNA) + PS3 \| 限制 \| 合计 ≤8；PVS1(RNA) 吸收 PP3/PM4/预测型 PVS1 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0864 | original/ACMG_CRITERIA.md:864 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PVS1(RNA) + PS1 \| 谨慎 \| 须存在同预测影响的已确认致病变异 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0865 | original/ACMG_CRITERIA.md:865 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PVS1/PM4 + PS3 \| 限制 \| 蛋白功能实验可合并，剪接预测除外 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0866 | original/ACMG_CRITERIA.md:866 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PS1/PM5 + PS3 \| 限制 \| 仅当参考变异无需功能数据即判 (L)P \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0867 | original/ACMG_CRITERIA.md:867 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PS2/PM6 + PP4 \| 禁止 \| 表型特异性已入 PS2 强度 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0868 | original/ACMG_CRITERIA.md:868 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PS4 + PP4 \| 谨慎 \| 病例定义含表型时重复计数 → 禁止 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0869 | original/ACMG_CRITERIA.md:869 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PM2 + PS4 \| 谨慎 \| 同一对照队列不可两用 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0870 | original/ACMG_CRITERIA.md:870 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PS2/PM6 + PS4 \| 禁止（同批病例） \| 同一批 de novo 病例不得双计 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0871 | original/ACMG_CRITERIA.md:871 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PM3 + PP4 \| 谨慎 \| PP4 不可复用 PM3 已定义的亚表型要素 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0872 | original/ACMG_CRITERIA.md:872 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PM3 + PP1 \| 谨慎 \| 反式鉴定已用于共分离时不可同计 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0873 | original/ACMG_CRITERIA.md:873 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PP1 + PP4 \| 限制 \| 合计 ≤5 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0874 | original/ACMG_CRITERIA.md:874 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| PS3 + PP3 \| 允许 \| 功能 vs 进化预测独立（剪接预测除外） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0876 | original/ACMG_CRITERIA.md:876 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | **良性侧**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0878 | original/ACMG_CRITERIA.md:878 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| 证据对 \| 决策 \| 条件/理由 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0879 | original/ACMG_CRITERIA.md:879 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \|---\|---\|---\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0880 | original/ACMG_CRITERIA.md:880 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| BS2 + BP2 \| 禁止 \| 隐性语境纯合 vs 杂合互斥 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0881 | original/ACMG_CRITERIA.md:881 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| BP3 + BP4 \| 禁止 \| BP3 已涵盖重复区序列背景 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0882 | original/ACMG_CRITERIA.md:882 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| BP2 + BP5 \| 禁止 \| 替代病因证据互斥 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0883 | original/ACMG_CRITERIA.md:883 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| BS2 + BS4 \| 谨慎 \| 反式鉴定已用于共分离时不可同计 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0884 | original/ACMG_CRITERIA.md:884 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| BS4 + BP2 \| 谨慎 \| 反式鉴定已用于抗共分离时不可同计 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0885 | original/ACMG_CRITERIA.md:885 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| BS4 + BP5 \| 谨慎 \| 同一被检者不可既作非共分离又作替代病因 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0886 | original/ACMG_CRITERIA.md:886 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| BP7(RNA) + BS3 \| 限制 \| 合计 ≤8 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0887 | original/ACMG_CRITERIA.md:887 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| BS3 + BP4 \| 限制 \| 蛋白功能实验可合并，剪接预测除外 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0888 | original/ACMG_CRITERIA.md:888 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | \| BP4 + BP7 \| 允许 \| BP7 以 BP4 成立为前提 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0890 | original/ACMG_CRITERIA.md:890 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | **互斥对（速查）**：PP3/BP4、PS1/PM5、PVS1 与 PM1/PM4/PP2/PP3、PM4/PP3、PM4/PM5、PP2/PM1、PM1 与 PS1/PM5、BS2/BP | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0892 | original/ACMG_CRITERIA.md:892 | 6.5 证据合并决策表（⟦培训班⟧ 高勇 2026-09，据 CanVIG-UK/ACGS 规范与 Garrett 2020） | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0894 | original/ACMG_CRITERIA.md:894 | 7. 行业争议热点与共识建议（汇总各报告） | ## 7. 行业争议热点与共识建议（汇总各报告） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0896 | original/ACMG_CRITERIA.md:896 | 7. 行业争议热点与共识建议（汇总各报告） | \| 争议 \| 共识建议 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0897 | original/ACMG_CRITERIA.md:897 | 7. 行业争议热点与共识建议（汇总各报告） | \|------\|---------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0898 | original/ACMG_CRITERIA.md:898 | 7. 行业争议热点与共识建议（汇总各报告） | \| PVS1 滥用致假阳性/过度诊断 \| 用四级分层框架，避免一刀切，建基因特异 LOF 框架 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0899 | original/ACMG_CRITERIA.md:899 | 7. 行业争议热点与共识建议（汇总各报告） | \| NMD 预测不准致 PVS1 强度误判 \| 预测仅参考，不等于真实效应；无 RNA 证据降级使用 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0900 | original/ACMG_CRITERIA.md:900 | 7. 行业争议热点与共识建议（汇总各报告） | \| AD/AR 双模式基因新发变异评估 \| 区分机制和变异区域，参考附近已报道变异，产后病例匹配 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0901 | original/ACMG_CRITERIA.md:901 | 7. 行业争议热点与共识建议（汇总各报告） | \| 表型特异性/遗传异质性主观差异 \| 推广 HPO 量化评分，建统一量化标准 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0902 | original/ACMG_CRITERIA.md:902 | 7. 行业争议热点与共识建议（汇总各报告） | \| 群体频率阈值普适性 \| 按患病率、祖源、遗传模式动态调整；优先 VCEP 阈值 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0903 | original/ACMG_CRITERIA.md:903 | 7. 行业争议热点与共识建议（汇总各报告） | \| 证据权重一刀切、缺连续性 \| 第四版指南方向为连续评分；中间分值争议待解 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0904 | original/ACMG_CRITERIA.md:904 | 7. 行业争议热点与共识建议（汇总各报告） | \| PP3/BP4 最高到 Strong 是否完整临床应用 \| 谨慎，可考虑降级；以**单一校准工具**（默认 REVEL，Pejaver 2022）赋分，AlphaMissense 仅 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0905 | original/ACMG_CRITERIA.md:905 | 7. 行业争议热点与共识建议（汇总各报告） | \| VUS 细化后临床建议不明确 \| 内部亚分档见 §0（VUS-High/Mid/Low）；ACMG SVC v4.0 将标准化 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0906 | original/ACMG_CRITERIA.md:906 | 7. 行业争议热点与共识建议（汇总各报告） | \| ⟦培训班⟧ HI/TS=2 的 CNV 是否直接 LP \| Riggs 2020/计算器不给 2A；ClinGen 支持病例拆到 Section 4 逐例评分（见 CNV_CRITE | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0907 | original/ACMG_CRITERIA.md:907 | 7. 行业争议热点与共识建议（汇总各报告） | \| ⟦培训班⟧ 产前 PP4 计分 vs 仅陈述 \| 折中：允许 VCEP 定义胎儿表型条目时计分，其余只作"表型吻合度陈述"（§4.4） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0909 | original/ACMG_CRITERIA.md:909 | 7. 行业争议热点与共识建议（汇总各报告） | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0911 | original/ACMG_CRITERIA.md:911 | 8. ⚠️ 关键产前提醒（贯穿全流程） | ## 8. ⚠️ 关键产前提醒（贯穿全流程） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0913 | original/ACMG_CRITERIA.md:913 | 8. ⚠️ 关键产前提醒（贯穿全流程） | 1. 产前"致病性分类"与"出生后预后"是两个独立问题，证据链不同（见主 SKILL Step 0.6-0.7、模块8'） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0914 | original/ACMG_CRITERIA.md:914 | 8. ⚠️ 关键产前提醒（贯穿全流程） | 2. 产前表型有限、动态、非特异，PS2/PM3/PP4 使用受限——宁缺毋滥 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0915 | original/ACMG_CRITERIA.md:915 | 8. ⚠️ 关键产前提醒（贯穿全流程） | 3. 高频亚效单倍型可与 LOF 反式致病（TBX6 范式），单杂合 LOF 检出时主动核查 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0916 | original/ACMG_CRITERIA.md:916 | 8. ⚠️ 关键产前提醒（贯穿全流程） | 4. 产前 LOF 关键决策点可用引产前胎儿脐血 RNA 验证升级 PVS1（TET3 范式） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0917 | original/ACMG_CRITERIA.md:917 | 8. ⚠️ 关键产前提醒（贯穿全流程） | 5. PS2/PM6 已用则不叠加 PP4（ACGS 2024）；产前 de novo 表型特异性分级见 4.1.5 决策表，非特异生长参数（如头围偏小）不可当"高度特异"升档 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0918 | original/ACMG_CRITERIA.md:918 | 8. ⚠️ 关键产前提醒（贯穿全流程） | 6. 多基因座候选时 PP4 按比例分摊 + 封顶 +5，不全压单基因 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0919 | original/ACMG_CRITERIA.md:919 | 8. ⚠️ 关键产前提醒（贯穿全流程） | 7. 中国人群频率数据缺口影响 PS4/频率阈值，结果解读需保守 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0920 | original/ACMG_CRITERIA.md:920 | 8. ⚠️ 关键产前提醒（贯穿全流程） | 8. PM1 产前宁缺毋滥（见 3.5）：须满足"功能已确立 + 域内无良性变异 + 热点数据（可用 gnomAD MCR OE 量化）"三门槛，强制查 gnomAD 域内变异与 VCEP  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0921 | original/ACMG_CRITERIA.md:921 | 8. ⚠️ 关键产前提醒（贯穿全流程） | 9. ⟦培训班⟧ 产前样本先过 MCC 定量（§4.11）、嵌合与 VAF 核查（§4.1.8/4.1.9）、同源区可比对性（§2.5b）三道前置门，再谈证据 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0922 | original/ACMG_CRITERIA.md:922 | 8. ⚠️ 关键产前提醒（贯穿全流程） | 10. ⟦培训班⟧ 良性侧仅有计算预测时产前不出 LB；至少两条证据才出 LB/LP/P（§0）；GUS 基因封顶 VUS（§0） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0923 | original/ACMG_CRITERIA.md:923 | 8. ⚠️ 关键产前提醒（贯穿全流程） | 11. ⟦培训班⟧ "致病 ≠ 病因"：报告分"分级 / 归因（超声表型吻合度陈述）/ 再发风险"三段；找到致病变异后寻找不停止；BP2/BP5 产前默认不赋（§4.6） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0924 | original/ACMG_CRITERIA.md:924 | 8. ⚠️ 关键产前提醒（贯穿全流程） | 12. ⟦培训班⟧ 再发风险不得套固定值：生殖细胞 de novo（亲代 VAF 0）→ 低但不为零（生殖腺嵌合不可用外周血排除）；胎儿合子后嵌合 → 更低；亲代杂合（VAF 40–60%） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| A-0925 | original/ACMG_CRITERIA.md:925 | 8. ⚠️ 关键产前提醒（贯穿全流程） | 13. ⟦培训班⟧ 遗传自"健康"亲代 ≠ 良性证据：亲代须完成基因特异靶向评估（§4.1.8）；"AD 遗传自亲代→再发 50%"与"遗传自亲代→倾向良性"两句话术在亲代嵌合时均不成立 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0001 | original/CNV_CRITERIA.md:1 | CNV 致病性分类标准（ClinGen 2019/2020 五段式评分） | # CNV 致病性分类标准（ClinGen 2019/2020 五段式评分） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0003 | original/CNV_CRITERIA.md:3 | CNV 致病性分类标准（ClinGen 2019/2020 五段式评分） | > 本参考文件用于 SKILL.md 的 **CNV 路由**。当输入为拷贝数变异（缺失/重复，如 chr11:19076957-36302387_del、Exon 10-12 dup、CM | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0004 | original/CNV_CRITERIA.md:4 | CNV 致病性分类标准（ClinGen 2019/2020 五段式评分） | > | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0005 | original/CNV_CRITERIA.md:5 | CNV 致病性分类标准（ClinGen 2019/2020 五段式评分） | > **权威依据**：Riggs ER, et al. *Technical standards for the interpretation and reporting of consti | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0006 | original/CNV_CRITERIA.md:6 | CNV 致病性分类标准（ClinGen 2019/2020 五段式评分） | > | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0007 | original/CNV_CRITERIA.md:7 | CNV 致病性分类标准（ClinGen 2019/2020 五段式评分） | > ⚠️ **使用须知**：本文件为离线速查与逻辑指引。**最终分值与分类应以 ClinGen 官方 CNV 计算器为准**：https://cnvcalc.clinicalgenome.o | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0008 | original/CNV_CRITERIA.md:8 | CNV 致病性分类标准（ClinGen 2019/2020 五段式评分） | > | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0009 | original/CNV_CRITERIA.md:9 | CNV 致病性分类标准（ClinGen 2019/2020 五段式评分） | > **2026-09 复核**：按第一期产前基因变异解读培训班范宁《基于 ACMG 指南的临床 CNVs 致病性评估》与肖锐工作坊课件逐条比对 Riggs 2020 后修订；标注 ⟦培训班 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0011 | original/CNV_CRITERIA.md:11 | 0.1 评分前置步骤 ⟦培训班⟧ | ### 0.1 评分前置步骤 ⟦培训班⟧ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0013 | original/CNV_CRITERIA.md:13 | 0.1 评分前置步骤 ⟦培训班⟧ | 1. **是否为复发性（recurrent）CNV 区域**：断点落在 LCR/segmental duplication 介导的复发区间（1q21.1、15q11.2、16p11.2、16 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0014 | original/CNV_CRITERIA.md:14 | 0.1 评分前置步骤 ⟦培训班⟧ | 2. **断点可信度**：CNV-seq 固定 20 kb 窗 vs WES 外显子分辨率/split-reads；当与 HI/TS 区域重叠比例接近"完全覆盖"阈值时（如 93.3% vs | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0015 | original/CNV_CRITERIA.md:15 | 0.1 评分前置步骤 ⟦培训班⟧ | 3. **数据质量**：数据波动 CV = com（相邻 bin 紧凑性）× sym（染色体内对称性），CV 大 → 无法分析 CNV/STR，建议重建库；复杂 CNV（杂合缺失内嵌纯合缺失 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0016 | original/CNV_CRITERIA.md:16 | 0.1 评分前置步骤 ⟦培训班⟧ | 4. **ClinGen 剂量评分含义**：3 充分证据 / 2 部分证据 / 1 有限证据 / 0 无证据 / 40 剂量不敏感 / 30 AR 基因；注意评估日期（2019-02 前评估 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0018 | original/CNV_CRITERIA.md:18 | 0.1 评分前置步骤 ⟦培训班⟧ | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0020 | original/CNV_CRITERIA.md:20 | 0. 总则与评分阈值 | ## 0. 总则与评分阈值 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0022 | original/CNV_CRITERIA.md:22 | 0. 总则与评分阈值 | CNV 分类独立于 SNV/Indel 的 ACMG/AMP 框架，采用**累加评分制**：在五个段落（Section 1–5）中按命中的证据条目累加（或扣减）分值，得到总分后对照下表给出分 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0024 | original/CNV_CRITERIA.md:24 | 0. 总则与评分阈值 | **缺失（Loss）与重复（Gain）使用各自独立的评分表**——同一基因组区段的缺失和重复，致病机制和分值完全不同，不可混用。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0026 | original/CNV_CRITERIA.md:26 | 评分阈值（缺失与重复通用） | ### 评分阈值（缺失与重复通用） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0028 | original/CNV_CRITERIA.md:28 | 评分阈值（缺失与重复通用） | \| 总分 \| 分类 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0029 | original/CNV_CRITERIA.md:29 | 评分阈值（缺失与重复通用） | \|------\|------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0030 | original/CNV_CRITERIA.md:30 | 评分阈值（缺失与重复通用） | \| ≥ 0.99 \| **Pathogenic（致病）** \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0031 | original/CNV_CRITERIA.md:31 | 评分阈值（缺失与重复通用） | \| 0.90 – 0.98 \| **Likely Pathogenic（疑似致病）** \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0032 | original/CNV_CRITERIA.md:32 | 评分阈值（缺失与重复通用） | \| −0.89 – 0.89 \| **VUS（意义未明）** \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0033 | original/CNV_CRITERIA.md:33 | 评分阈值（缺失与重复通用） | \| −0.90 – −0.98 \| **Likely Benign（疑似良性）** \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0034 | original/CNV_CRITERIA.md:34 | 评分阈值（缺失与重复通用） | \| ≤ −0.99 \| **Benign（良性）** \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0036 | original/CNV_CRITERIA.md:36 | 五段式结构概览 | ### 五段式结构概览 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0038 | original/CNV_CRITERIA.md:38 | 五段式结构概览 | \| 段 \| 缺失（Loss）评估对象 \| 重复（Gain）评估对象 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0039 | original/CNV_CRITERIA.md:39 | 五段式结构概览 | \|----\|----------------------\|----------------------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0040 | original/CNV_CRITERIA.md:40 | 五段式结构概览 | \| Section 1 \| 是否含蛋白编码/已知功能元件 \| 同左 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0041 | original/CNV_CRITERIA.md:41 | 五段式结构概览 | \| Section 2 \| 与**已确立单倍剂量不足（HI）基因/区域**或已确立良性区的重叠 \| 与**已确立三倍剂量敏感（TS）基因/区域**或已确立良性区的重叠 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0042 | original/CNV_CRITERIA.md:42 | 五段式结构概览 | \| Section 3 \| 受累蛋白编码基因**数目** \| 同左（阈值不同） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0043 | original/CNV_CRITERIA.md:43 | 五段式结构概览 | \| Section 4 \| 个案/文献证据（表型、de novo、病例对照、共分离等） \| 同左 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0044 | original/CNV_CRITERIA.md:44 | 五段式结构概览 | \| Section 5 \| 遗传方式与家系信息 \| 同左 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0046 | original/CNV_CRITERIA.md:46 | 五段式结构概览 | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0048 | original/CNV_CRITERIA.md:48 | 1. Section 1：初始基因组内容评估（缺失/重复通用） | ## 1. Section 1：初始基因组内容评估（缺失/重复通用） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0050 | original/CNV_CRITERIA.md:50 | 1. Section 1：初始基因组内容评估（缺失/重复通用） | \| 条目 \| 情形 \| 分值 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0051 | original/CNV_CRITERIA.md:51 | 1. Section 1：初始基因组内容评估（缺失/重复通用） | \|------\|------\|------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0052 | original/CNV_CRITERIA.md:52 | 1. Section 1：初始基因组内容评估（缺失/重复通用） | \| 1A \| CNV **含**蛋白编码基因或其他已知功能重要元件 \| 0（继续 Section 2） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0053 | original/CNV_CRITERIA.md:53 | 1. Section 1：初始基因组内容评估（缺失/重复通用） | \| 1B \| CNV **不含**任何蛋白编码基因或已知功能重要元件 \| **−0.60**（直接判良性倾向，可终止评分） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0055 | original/CNV_CRITERIA.md:55 | 1. Section 1：初始基因组内容评估（缺失/重复通用） | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0057 | original/CNV_CRITERIA.md:57 | 2. Section 2：与已确立剂量敏感基因/良性区的重叠 | ## 2. Section 2：与已确立剂量敏感基因/良性区的重叠 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0059 | original/CNV_CRITERIA.md:59 | 2. Section 2：与已确立剂量敏感基因/良性区的重叠 | > **本段是评分的核心权重来源。** 「已确立」指 ClinGen Dosage Sensitivity Map 评分为 3（足够证据）的基因/区域：HI=3（缺失致病确立）、TS=3（重 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0061 | original/CNV_CRITERIA.md:61 | 2.1 拷贝数缺失（Loss）证据条目 | ### 2.1 拷贝数缺失（Loss）证据条目 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0063 | original/CNV_CRITERIA.md:63 | 2.1 拷贝数缺失（Loss）证据条目 | \| 条目 \| 情形 \| 分值 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0064 | original/CNV_CRITERIA.md:64 | 2.1 拷贝数缺失（Loss）证据条目 | \|------\|------\|------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0065 | original/CNV_CRITERIA.md:65 | 2.1 拷贝数缺失（Loss）证据条目 | \| 2A \| **完全覆盖**一个已确立 HI（=3）基因/区域 \| **+1.00** \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0066 | original/CNV_CRITERIA.md:66 | 2.1 拷贝数缺失（Loss）证据条目 | \| 2B \| 与已确立 HI 区域**部分重叠**（进入下列细分场景判定）；三种子情形——CNV 不含该区已知致病基因/关键区、不能明确是否受累、该区尚未建立特定致病基因/关键区——均为 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0067 | original/CNV_CRITERIA.md:67 | 2.1 拷贝数缺失（Loss）证据条目 | \| 2C-1 \| 部分重叠已确立 HI 基因的 **5′ 端**，且累及编码序列 \| **+0.90**（0.45–1.00） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0068 | original/CNV_CRITERIA.md:68 | 2.1 拷贝数缺失（Loss）证据条目 | \| 2C-2 \| 部分重叠 5′ 端，但**仅累及 5′UTR/启动子** \| 0.00（0–0.45）⟦培训班⟧：有启动子/5′UTR 缺失导致表达下降的功能或转录组证据时可升至 0 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0069 | original/CNV_CRITERIA.md:69 | 2.1 拷贝数缺失（Loss）证据条目 | \| 2D-1 \| 部分重叠 **3′ 端**，且**仅累及 3′UTR** \| 0.00 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0070 | original/CNV_CRITERIA.md:70 | 2.1 拷贝数缺失（Loss）证据条目 | \| 2D-2 \| 部分重叠 3′ 端，仅累及最后一个外显子，且该外显子内已有其他致病变异报道（ClinVar/HGMD P/LP，且不应只有移码/无义类——须能说明该区段确有功能重要性） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0071 | original/CNV_CRITERIA.md:71 | 2.1 拷贝数缺失（Loss）证据条目 | \| 2D-3 \| 部分重叠 3′ 端，仅累及最后一个外显子，**无**致病变异报道 \| **+0.30**（0–0.45） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0072 | original/CNV_CRITERIA.md:72 | 2.1 拷贝数缺失（Loss）证据条目 | \| 2D-4 \| 部分重叠 3′ 端，累及最后一个外显子和其他外显子，**预测发生 NMD** ⟦培训班⟧ \| **+0.90**（0.45–1.00） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0073 | original/CNV_CRITERIA.md:73 | 2.1 拷贝数缺失（Loss）证据条目 | \| **2E** \| **两个断点均落在同一个已确立 HI 基因内（基因内 CNV，相当于基因水平序列变异）** → **复用 PVS1 决策树判断**（见下方 §2.3） \| **+ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0074 | original/CNV_CRITERIA.md:74 | 2.1 拷贝数缺失（Loss）证据条目 | \| 2F \| **完全包含于**已确立良性 CNV 区域内（ClinGen 40，或人群频率 >1%——覆盖 AR 基因慎用） \| **−1.00** \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0075 | original/CNV_CRITERIA.md:75 | 2.1 拷贝数缺失（Loss）证据条目 | \| 2G \| 与已确立良性 CNV 重叠，但**额外包含**其他基因组内容 \| 0.00（继续评估额外内容） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0076 | original/CNV_CRITERIA.md:76 | 2.1 拷贝数缺失（Loss）证据条目 | \| 2H \| ≥2 个单倍剂量不足预测工具提示区间内至少一个基因为 HI（⟦培训班⟧ 阈值：DECIPHER pHaplo ≥0.86；gnomAD pLI ≥0.9 且 LOEUF < | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0078 | original/CNV_CRITERIA.md:78 | 2.2 拷贝数重复（Gain）证据条目 | ### 2.2 拷贝数重复（Gain）证据条目 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0080 | original/CNV_CRITERIA.md:80 | 2.2 拷贝数重复（Gain）证据条目 | \| 条目 \| 情形 \| 分值 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0081 | original/CNV_CRITERIA.md:81 | 2.2 拷贝数重复（Gain）证据条目 | \|------\|------\|------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0082 | original/CNV_CRITERIA.md:82 | 2.2 拷贝数重复（Gain）证据条目 | \| 2A \| **完全覆盖**一个已确立 TS 基因/区域 \| **+1.00** \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0083 | original/CNV_CRITERIA.md:83 | 2.2 拷贝数重复（Gain）证据条目 | \| 2B \| 与已确立 TS 区域**部分重叠**（进入细分判定） \| 0.00 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0084 | original/CNV_CRITERIA.md:84 | 2.2 拷贝数重复（Gain）证据条目 | \| 2C \| 与已确立良性拷贝数增益**基因内容完全一致** \| **−1.00** \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0085 | original/CNV_CRITERIA.md:85 | 2.2 拷贝数重复（Gain）证据条目 | \| 2D \| 小于已确立良性增益，且断点**不打断**蛋白编码基因 \| **−1.00** \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0086 | original/CNV_CRITERIA.md:86 | 2.2 拷贝数重复（Gain）证据条目 | \| 2E \| 小于已确立良性增益，但断点**可能打断**蛋白编码基因 \| 0.00 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0087 | original/CNV_CRITERIA.md:87 | 2.2 拷贝数重复（Gain）证据条目 | \| 2F \| 大于已确立良性增益，且**未引入额外**蛋白编码基因 \| **−1.00** \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0088 | original/CNV_CRITERIA.md:88 | 2.2 拷贝数重复（Gain）证据条目 | \| 2G \| 与已确立良性增益重叠，但**额外包含**其他基因组内容 \| 0.00 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0089 | original/CNV_CRITERIA.md:89 | 2.2 拷贝数重复（Gain）证据条目 | \| 2H \| CNV **完整包含**一个已确立 HI 基因（HI 基因的额外拷贝通常不致病，继续评估） ⟦培训班⟧ 旧版误写为"HI 预测工具 +0.15"（那是缺失表 2H），已按  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0090 | original/CNV_CRITERIA.md:90 | 2.2 拷贝数重复（Gain）证据条目 | \| **2I** \| **两个断点均落在同一个基因内（基因内重复，相当于基因水平序列变异）** → **复用 PVS1 决策树判断**（见下方 §2.3）。⟦培训班⟧ 三档：证实串联且移 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0091 | original/CNV_CRITERIA.md:91 | 2.2 拷贝数重复（Gain）证据条目 | \| 2J \| **一个**断点落在已确立 HI 基因内，患者表型未知或不一致 \| 0.00 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0092 | original/CNV_CRITERIA.md:92 | 2.2 拷贝数重复（Gain）证据条目 | \| 2K \| 一个断点落在已确立 HI 基因内，患者表型**高度特异且一致** \| **+0.45** \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0093 | original/CNV_CRITERIA.md:93 | 2.2 拷贝数重复（Gain）证据条目 | \| 2L \| 一个或两个断点落在**意义未明基因**内 \| 0.00 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0095 | original/CNV_CRITERIA.md:95 | 2.3 基因内 CNV 的 PVS1 决策树复用（2E / 2I 专用） | ### 2.3 基因内 CNV 的 PVS1 决策树复用（2E / 2I 专用） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0097 | original/CNV_CRITERIA.md:97 | 2.3 基因内 CNV 的 PVS1 决策树复用（2E / 2I 专用） | 当 CNV 两个断点均位于同一基因内（缺失走 2E、重复走 2I），其本质是**基因水平的结构变异**，应像评估无义/移码变异那样判断是否触发功能缺失（LOF），复用 **SKILL.md  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0099 | original/CNV_CRITERIA.md:99 | 2.3 基因内 CNV 的 PVS1 决策树复用（2E / 2I 专用） | 0. **先查 VCEP** ⟦培训班⟧：https://cspec.genome.network 是否有该基因 VCEP 的 PVS1 特化（MECP2 exon 3 缺失 351bp 框 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0100 | original/CNV_CRITERIA.md:100 | 2.3 基因内 CNV 的 PVS1 决策树复用（2E / 2I 专用） | 1. **前提门槛** ⟦培训班⟧：LOF 为该基因-疾病的已知致病机制——ClinGen Dosage HI=3，**或** HI=30（AR 基因）且本例为纯合/与第二打击反式（NPHP | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0101 | original/CNV_CRITERIA.md:101 | 2.3 基因内 CNV 的 PVS1 决策树复用（2E / 2I 专用） | 2. **缺失型（2E）**：基因内多外显子缺失若导致移码并预测触发 NMD → 等同 PVS1 原级 → 取 **+0.90**；若落在最后一个外显子/NMD 逃逸区，按截断区重要性降级（ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0102 | original/CNV_CRITERIA.md:102 | 2.3 基因内 CNV 的 PVS1 决策树复用（2E / 2I 专用） | 3. **重复型（2I）**：需判断重复是否为**串联**及是否打断阅读框： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0103 | original/CNV_CRITERIA.md:103 | 2.3 基因内 CNV 的 PVS1 决策树复用（2E / 2I 专用） |    - 证实为基因内**串联重复**并导致移码/LOF（机制为 LOF 的基因）→ 可升至 +0.90； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0104 | original/CNV_CRITERIA.md:104 | 2.3 基因内 CNV 的 PVS1 决策树复用（2E / 2I 专用） |    - 重复性质（串联 vs 插入异位）或方向未明 → 默认 **0.00**，注明需 RNA/断点测序进一步验证； | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0105 | original/CNV_CRITERIA.md:105 | 2.3 基因内 CNV 的 PVS1 决策树复用（2E / 2I 专用） |    - 仅算**串联**形式的重复才考虑等同 LOF（与 ACMG PVS1 对基因内重复的规定一致）。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0106 | original/CNV_CRITERIA.md:106 | 2.3 基因内 CNV 的 PVS1 决策树复用（2E / 2I 专用） | 4. **剪接相关**：若断点预测影响经典剪接位点，参照 2023 SVI 剪接新规（references/ACMG_CRITERIA.md 第 1 节），有 RNA 证据时用 PVS1_S | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0108 | original/CNV_CRITERIA.md:108 | 2.4 HI/TS = 2 或未评估基因的处置 ⟦培训班⟧ | ### 2.4 HI/TS = 2 或未评估基因的处置 ⟦培训班⟧ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0110 | original/CNV_CRITERIA.md:110 | 2.4 HI/TS = 2 或未评估基因的处置 ⟦培训班⟧ | - **HI/TS=2 不给 2A**（Riggs/计算器只对评分 3 生效）。范宁课件"完全覆盖 HI=2 建议 LP"与肖锐引用的 ACGS 2024"score 3→P, 2→LP,  | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0111 | original/CNV_CRITERIA.md:111 | 2.4 HI/TS = 2 或未评估基因的处置 ⟦培训班⟧ | - **未评估/评分陈旧（早于 2019-02）基因按 ClinGen Dosage SOP 自评**（https://clinicalgenome.org/site/assets/file | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0113 | original/CNV_CRITERIA.md:113 | 2.4 HI/TS = 2 或未评估基因的处置 ⟦培训班⟧ | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0115 | original/CNV_CRITERIA.md:115 | 3. Section 3：受累蛋白编码基因数目 | ## 3. Section 3：受累蛋白编码基因数目 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0117 | original/CNV_CRITERIA.md:117 | 3. Section 3：受累蛋白编码基因数目 | > 仅计入完全或部分被 CNV 覆盖的**蛋白编码**基因。缺失与重复**阈值不同**。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0119 | original/CNV_CRITERIA.md:119 | 3.1 缺失（Loss） | ### 3.1 缺失（Loss） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0121 | original/CNV_CRITERIA.md:121 | 3.1 缺失（Loss） | \| 条目 \| 基因数 \| 分值 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0122 | original/CNV_CRITERIA.md:122 | 3.1 缺失（Loss） | \|------\|--------\|------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0123 | original/CNV_CRITERIA.md:123 | 3.1 缺失（Loss） | \| 3A \| 0–24 \| 0.00 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0124 | original/CNV_CRITERIA.md:124 | 3.1 缺失（Loss） | \| 3B \| 25–34 \| +0.45 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0125 | original/CNV_CRITERIA.md:125 | 3.1 缺失（Loss） | \| 3C \| ≥ 35 \| +0.90 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0127 | original/CNV_CRITERIA.md:127 | 3.2 重复（Gain） | ### 3.2 重复（Gain） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0129 | original/CNV_CRITERIA.md:129 | 3.2 重复（Gain） | \| 条目 \| 基因数 \| 分值 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0130 | original/CNV_CRITERIA.md:130 | 3.2 重复（Gain） | \|------\|--------\|------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0131 | original/CNV_CRITERIA.md:131 | 3.2 重复（Gain） | \| 3A \| 0–34 \| 0.00 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0132 | original/CNV_CRITERIA.md:132 | 3.2 重复（Gain） | \| 3B \| 35–49 \| +0.45 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0133 | original/CNV_CRITERIA.md:133 | 3.2 重复（Gain） | \| 3C \| ≥ 50 \| +0.90 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0135 | original/CNV_CRITERIA.md:135 | 3.2 重复（Gain） | ⚠️ Section 3 反映的是「基因越多越可能有临床后果」的概率背景，**不替代** Section 2/4 的特异性证据；大片段但落在已确立良性区时仍以 Section 2 的扣分为主 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0137 | original/CNV_CRITERIA.md:137 | 3.2 重复（Gain） | ⟦培训班⟧ **基因家族计数**：用 DECIPHER 勾选蛋白编码基因取初始数；对照 HGNC gene groups（https://www.genenames.org/data/gen | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0139 | original/CNV_CRITERIA.md:139 | 3.2 重复（Gain） | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0141 | original/CNV_CRITERIA.md:141 | 4. Section 4：个案与文献证据（缺失/重复通用逻辑） | ## 4. Section 4：个案与文献证据（缺失/重复通用逻辑） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0143 | original/CNV_CRITERIA.md:143 | 4. Section 4：个案与文献证据（缺失/重复通用逻辑） | > 本段汇总文献/数据库中**与本 CNV 重叠**的病例证据。每条按表型特异性、遗传背景、证据质量赋值，**逐条累加、逐条封顶**（Riggs 无全段封顶：4A/4B/4C 各上限 0.9 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0145 | original/CNV_CRITERIA.md:145 | 4. Section 4：个案与文献证据（缺失/重复通用逻辑） | **文献病例纳入规则** ⟦培训班⟧：缺失——纳入片段内单基因缺失或 LOF 变异病例；重复——纳入单基因完整重复病例。文献 CNV 范围大于待评 CNV、或同时检出其他 CNV 的病例不作 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0147 | original/CNV_CRITERIA.md:147 | 4.1 个案表型 + de novo（4A–4E） | ### 4.1 个案表型 + de novo（4A–4E） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0149 | original/CNV_CRITERIA.md:149 | 4.1 个案表型 + de novo（4A–4E） | \| 条目 \| 情形 \| 确认 de novo（每例） \| 推定 de novo（每例） \| 上限 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0150 | original/CNV_CRITERIA.md:150 | 4.1 个案表型 + de novo（4A–4E） | \|------\|------\|---------------------\|---------------------\|------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0151 | original/CNV_CRITERIA.md:151 | 4.1 个案表型 + de novo（4A–4E） | \| 4A \| 表型高度特异且为该基因/区域相对唯一（IRF6 唇凹、ATP7B K-F 环、F8 活性低、CHARGE 表型组合） \| 0.45（0.15–0.45） \| 0.30（ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0152 | original/CNV_CRITERIA.md:152 | 4.1 个案表型 + de novo（4A–4E） | \| 4B \| 表型高度特异但非该基因/区域唯一（脑白质营养不良、EIEE、痉挛性截瘫、无脑回） \| 0.30（0.15–0.45） \| 0.15（0.10–0.30） \| 0.90 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0153 | original/CNV_CRITERIA.md:153 | 4.1 个案表型 + de novo（4A–4E） | \| 4C \| 表型一致但非高度特异/遗传异质性高（DD、非特异 ID、ASD、未分型癫痫、耳聋） \| 0.15（0–0.15） \| 0.10（0–0.15） \| 0.90 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0154 | original/CNV_CRITERIA.md:154 | 4.1 个案表型 + de novo（4A–4E） | \| 4D \| 表型与该基因/区域预期不一致 \| 0（0 至 −0.30） \| 同左 \| −0.30 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0155 | original/CNV_CRITERIA.md:155 | 4.1 个案表型 + de novo（4A–4E） | \| 4E \| 表型高度特异且一致，但遗传方式未知 \| 0.10（0–0.15） \| — \| 0.30 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0157 | original/CNV_CRITERIA.md:157 | 4.2 共分离（4F–4H） | ### 4.2 共分离（4F–4H） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0159 | original/CNV_CRITERIA.md:159 | 4.2 共分离（4F–4H） | \| 条目 \| 共分离次数（可跨家系累加） \| 分值 \| 上限（三条合计） \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0160 | original/CNV_CRITERIA.md:160 | 4.2 共分离（4F–4H） | \|------\|-----------\|------\|------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0161 | original/CNV_CRITERIA.md:161 | 4.2 共分离（4F–4H） | \| 4F \| 3–4 次 \| 0.15 \| 0.45 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0162 | original/CNV_CRITERIA.md:162 | 4.2 共分离（4F–4H） | \| 4G \| 5–6 次 \| 0.30 \| \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0163 | original/CNV_CRITERIA.md:163 | 4.2 共分离（4F–4H） | \| 4H \| ≥7 次 \| 0.45 \| \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0165 | original/CNV_CRITERIA.md:165 | 4.2 共分离（4F–4H） | 计数只计（基因型+，表型+）个体与肯定携带者；同家系内表现度差异（ASD/ID/癫痫/精神分裂症）可视为同一脑疾病谱系。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0167 | original/CNV_CRITERIA.md:167 | 4.3 不共分离（4I–4K） | ### 4.3 不共分离（4I–4K） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0169 | original/CNV_CRITERIA.md:169 | 4.3 不共分离（4I–4K） | \| 条目 \| 情形 \| 每家系 \| 上限 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0170 | original/CNV_CRITERIA.md:170 | 4.3 不共分离（4I–4K） | \|------\|------\|-------\|------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0171 | original/CNV_CRITERIA.md:171 | 4.3 不共分离（4I–4K） | \| 4I \| 家系内其他受累者表型一致但未检出该 CNV \| −0.45（0 至 −0.45） \| −0.90 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0172 | original/CNV_CRITERIA.md:172 | 4.3 不共分离（4I–4K） | \| 4J \| 家系内未受累者无先证者**特异**表型但携带该 CNV \| −0.30（0 至 −0.30） \| −0.90 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0173 | original/CNV_CRITERIA.md:173 | 4.3 不共分离（4I–4K） | \| 4K \| 家系内未受累者无先证者**非特异**表型但携带该 CNV \| −0.15（0 至 −0.15） \| −0.30 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0175 | original/CNV_CRITERIA.md:175 | 4.3 不共分离（4I–4K） | 可赋 0 的例外：表型模拟、常见病、表现度、外显率、临床检查充分性、印记基因、限性遗传、嵌合体、隐性遗传。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0177 | original/CNV_CRITERIA.md:177 | 4.4 病例-对照（4L–4N） | ### 4.4 病例-对照（4L–4N） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0179 | original/CNV_CRITERIA.md:179 | 4.4 病例-对照（4L–4N） | \| 条目 \| 情形 \| 分值 \| 上限 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0180 | original/CNV_CRITERIA.md:180 | 4.4 病例-对照（4L–4N） | \|------\|------\|------\|------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0181 | original/CNV_CRITERIA.md:181 | 4.4 病例-对照（4L–4N） | \| 4L \| 病例组（表型一致、特异、明确）vs 对照差异显著 \| 0.45/研究（0–0.45） \| 0.45 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0182 | original/CNV_CRITERIA.md:182 | 4.4 病例-对照（4L–4N） | \| 4M \| 病例组（表型不一致/非特异/不明确）vs 对照差异显著 \| 0.30/研究（0–0.30） \| 0.45 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0183 | original/CNV_CRITERIA.md:183 | 4.4 病例-对照（4L–4N） | \| 4N \| 病例组 vs 对照无统计学差异 \| −0.90/研究（0 至 −0.90） \| −0.90 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0185 | original/CNV_CRITERIA.md:185 | 4.5 4O：人群频率扣分（最常用的良性侧证据） | ### 4.5 4O：人群频率扣分（最常用的良性侧证据） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0187 | original/CNV_CRITERIA.md:187 | 4.5 4O：人群频率扣分（最常用的良性侧证据） | \| 条目 \| 情形 \| 分值 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0188 | original/CNV_CRITERIA.md:188 | 4.5 4O：人群频率扣分（最常用的良性侧证据） | \|------\|------\|------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0189 | original/CNV_CRITERIA.md:189 | 4.5 4O：人群频率扣分（最常用的良性侧证据） | \| **4O** \| 本 CNV（或与之高度重叠者）在**大型健康人群数据库中反复出现**（gnomAD-SV/gnomAD-CNV、DGV gold standard、多次健康对照报道 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0191 | original/CNV_CRITERIA.md:191 | 4.5 4O：人群频率扣分（最常用的良性侧证据） | 使用条件：频率 >1% 改走 Section 2 良性区（2F，ACGS 建议）；≤1% 用 4O；队列 ≥10,000 等位基因 / 5,000 样本；外显不全综合征区慎用；覆盖 AR 基 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0193 | original/CNV_CRITERIA.md:193 | 4.5 4O：人群频率扣分（最常用的良性侧证据） | 🤰 **4O 慎用警示（产前/AR 区域）**： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0194 | original/CNV_CRITERIA.md:194 | 4.5 4O：人群频率扣分（最常用的良性侧证据） | - 4O 的减分前提是「该 CNV 不致病」。但若缺失区域**覆盖隐性（AR）致病基因**，则杂合缺失在健康人群中本就高频存在（携带者状态），此时 4O 的高频**不能**等同于良性——单杂 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0195 | original/CNV_CRITERIA.md:195 | 4.5 4O：人群频率扣分（最常用的良性侧证据） | - **产前场景**检出覆盖 AR 基因的杂合缺失时，应主动核查对侧等位基因（trans 位点是否有第二打击 SNV/Indel/CNV），而非凭 4O 高频直接降级。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0196 | original/CNV_CRITERIA.md:196 | 4.5 4O：人群频率扣分（最常用的良性侧证据） | - 类似 SNV 的「高频≠良性陷阱」（TBX6 范式，见 SKILL.md 1.2 节）：亚效单倍型/携带者频率在 4O 上表现为高频，但与反式 LOF 组合可致病。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0198 | original/CNV_CRITERIA.md:198 | 4.5 4O：人群频率扣分（最常用的良性侧证据） | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0200 | original/CNV_CRITERIA.md:200 | 5. Section 5：遗传方式与家系信息（缺失/重复通用） | ## 5. Section 5：遗传方式与家系信息（缺失/重复通用） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0202 | original/CNV_CRITERIA.md:202 | 5. Section 5：遗传方式与家系信息（缺失/重复通用） | > 本段根据本例先证者的遗传背景调整分值。需先证者父母样本验证。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0204 | original/CNV_CRITERIA.md:204 | 5. Section 5：遗传方式与家系信息（缺失/重复通用） | ⟦培训班⟧ Riggs 2020 精确条目（替换旧版"示意"表）：5A–5E 用于家系信息明确；5F–5H 用于单独先证者。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0206 | original/CNV_CRITERIA.md:206 | 5. Section 5：遗传方式与家系信息（缺失/重复通用） | \| 条目 \| 情形 \| 分值 \| 上限 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0207 | original/CNV_CRITERIA.md:207 | 5. Section 5：遗传方式与家系信息（缺失/重复通用） | \|------\|------\|------\|------\| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0208 | original/CNV_CRITERIA.md:208 | 5. Section 5：遗传方式与家系信息（缺失/重复通用） | \| 5A \| 先证者 de novo \| 按 4A–4D 的 de novo 栏计分 \| 0.45 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0209 | original/CNV_CRITERIA.md:209 | 5. Section 5：遗传方式与家系信息（缺失/重复通用） | \| 5B \| 遗传自无表型父/母；先证者表型特异明确且无家族史 \| −0.30（0 至 −0.45） \| −0.45 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0210 | original/CNV_CRITERIA.md:210 | 5. Section 5：遗传方式与家系信息（缺失/重复通用） | \| 5C \| 遗传自无表型父/母；表型不特异且无家族史 \| −0.15（0 至 −0.30） \| −0.30 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0211 | original/CNV_CRITERIA.md:211 | 5. Section 5：遗传方式与家系信息（缺失/重复通用） | \| 5D \| 家系内与表型共分离 \| 按 4F–4H（**先证者 + 一位患病亲代 = 1 次共分离 = 0 分；≥3 次才 0.15**——旧版"遗传自患病亲代→加分"会多算，已更正 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0212 | original/CNV_CRITERIA.md:212 | 5. Section 5：遗传方式与家系信息（缺失/重复通用） | \| 5E \| 家系内不共分离 \| 按 4I–4K \| −0.45 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0213 | original/CNV_CRITERIA.md:213 | 5. Section 5：遗传方式与家系信息（缺失/重复通用） | \| 5F \| 遗传信息不适用/无信息 \| 0 \| 0 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0214 | original/CNV_CRITERIA.md:214 | 5. Section 5：遗传方式与家系信息（缺失/重复通用） | \| 5G \| 无遗传信息；表型不特异但与既报病例一致 \| 0.10（0–0.15） \| 0.15 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0215 | original/CNV_CRITERIA.md:215 | 5. Section 5：遗传方式与家系信息（缺失/重复通用） | \| 5H \| 无遗传信息；表型高度特异且与既报病例一致 \| 0.30（0–0.30） \| 0.30 \| | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0217 | original/CNV_CRITERIA.md:217 | 5. Section 5：遗传方式与家系信息（缺失/重复通用） | ⚠️ **不完全外显与印记**：对已知不完全外显或受印记调控的区域（如 15q11-q13、NRXN1、16p13.11），「遗传自健康亲代」不套 5B/5C（给 0），须结合外显率与亲源。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0219 | original/CNV_CRITERIA.md:219 | 5. Section 5：遗传方式与家系信息（缺失/重复通用） | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0221 | original/CNV_CRITERIA.md:221 | 6. 产前 CNV 专项注意事项 | ## 6. 产前 CNV 专项注意事项 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0223 | original/CNV_CRITERIA.md:223 | 6. 产前 CNV 专项注意事项 | 产前（CMA / CNV-seq / 产前 WES-CNV）解读在通用五段式基础上，需额外关注以下技术与咨询要点： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0225 | original/CNV_CRITERIA.md:225 | 6.1 技术质控（避免假阳/假阴导致错误分类） | ### 6.1 技术质控（避免假阳/假阴导致错误分类） | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0227 | original/CNV_CRITERIA.md:227 | 6.1 技术质控（避免假阳/假阴导致错误分类） | - **数据均一性 / 波动性**：产前 WES-CNV 的读深均一性差于专用 CMA/CNV-seq；GC 偏倚、捕获不均会造成拷贝数信号波动，**小片段（尤其单/双外显子）CNV 须警惕 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0228 | original/CNV_CRITERIA.md:228 | 6.1 技术质控（避免假阳/假阴导致错误分类） | - **二代测序挑战区**：低复杂度区、segmental duplication、假基因同源区、低 mappability 区域内的 CNV **假阴/假阳并存**，分类前确认断点不落在挑 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0229 | original/CNV_CRITERIA.md:229 | 6.1 技术质控（避免假阳/假阴导致错误分类） | - **嵌合**：胎儿/胎盘嵌合（含限制性胎盘嵌合 CPM）可致信号比例异常；低比例嵌合 CNV 易漏检或被低估。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0231 | original/CNV_CRITERIA.md:231 | 6.2 分类与咨询 | ### 6.2 分类与咨询 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0233 | original/CNV_CRITERIA.md:233 | 6.2 分类与咨询 | - **致病性 ≠ 预后**：与 SNV 产前模式一致，CNV 的 ClinGen 分类回答「是否致病」，而「出生后表型如何」需结合该 CNV/区域的已报道表型谱、外显率与表达度（参见 SK | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0234 | original/CNV_CRITERIA.md:234 | 6.2 分类与咨询 | - **外显率与表达度的产前局限**：许多致病 CNV（如 16p11.2、15q11.2、1q21.1）外显率不完全、表型谱宽，产前咨询须如实告知不确定性区间，避免给出确定性预后。⟦培训班 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0235 | original/CNV_CRITERIA.md:235 | 6.2 分类与咨询 | - **产前表型检索**：OMIM 产前表型收录有限；CNV 段的预后应引用 SKILL.md Step 0.7 预后导向文献检索。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0236 | original/CNV_CRITERIA.md:236 | 6.2 分类与咨询 | - **覆盖 AR 基因的杂合缺失**：见 §4.3 的 4O 慎用警示——务必评估反式第二打击与父母携带状态。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0237 | original/CNV_CRITERIA.md:237 | 6.2 分类与咨询 | - **VUS 的产前处置**：产前时间窗紧迫，VUS 级 CNV 建议结合超声/MRI 结构表型、双亲验证（de novo vs 遗传）动态再评估，必要时提请多学科会诊。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0239 | original/CNV_CRITERIA.md:239 | 6.2 分类与咨询 | --- | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0241 | original/CNV_CRITERIA.md:241 | 7. 输出与可追溯要求 | ## 7. 输出与可追溯要求 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0243 | original/CNV_CRITERIA.md:243 | 7. 输出与可追溯要求 | - CNV 分析报告须列出：命中的每条 Section 1–5 证据条目、各自分值、累加总分、最终分类、以及所引用的 ClinGen Dosage 评分与文献 PMID。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0244 | original/CNV_CRITERIA.md:244 | 7. 输出与可追溯要求 | - 标注 **ClinGen CNV 计算器** 链接以便临床复核：https://cnvcalc.clinicalgenome.org/ | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0245 | original/CNV_CRITERIA.md:245 | 7. 输出与可追溯要求 | - 所有引用文献遵循 SKILL.md 的 **Step 9-Verify** PMID 反查规范。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0246 | original/CNV_CRITERIA.md:246 | 7. 输出与可追溯要求 | - 数据缺失/未验证项须如实标注 ⚠️ / ❌，不可伪造分值。 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0248 | original/CNV_CRITERIA.md:248 | 7. 输出与可追溯要求 | **报告用语模板** ⟦培训班⟧（范宁课件句式）： | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0249 | original/CNV_CRITERIA.md:249 | 7. 输出与可追溯要求 | > X 号染色体 pXX–qXX 处缺失/重复 N Mb 区域；涉及 N 个 RefSeq 蛋白编码基因（1A, 0 分；3B, 0.45 分）。完全覆盖 GENE 基因 [OMIM:xxx | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| C-0251 | original/CNV_CRITERIA.md:251 | 7. 输出与可追溯要求 | **引用与工具** ⟦培训班⟧：Riggs 2020 PMID:31690835；SVI PVS1 规范 PMID:30192042；ClinGen 剂量图谱 2024 DOI 10.101 | review/RULE_REVIEW.md | 原医学条文归档；pending，未正式启用 |
| P-0001 | original/genebe_fields.py.txt:1 | !/usr/bin/env python3 | #!/usr/bin/env python3 | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0002 | original/genebe_fields.py.txt:2 | -*- coding: utf-8 -*- | # -*- coding: utf-8 -*- | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0003 | original/genebe_fields.py.txt:3 | -*- coding: utf-8 -*- | """ | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0004 | original/genebe_fields.py.txt:4 | -*- coding: utf-8 -*- | genebe_fields.py — gene-variant-pathogenicity 技能的三源取数引擎 | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0005 | original/genebe_fields.py.txt:5 | -*- coding: utf-8 -*- | ================================================================ | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0006 | original/genebe_fields.py.txt:6 | -*- coding: utf-8 -*- | 放置:gene-variant-pathogenicity/references/genebe_fields.py | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0007 | original/genebe_fields.py.txt:7 | -*- coding: utf-8 -*- | 被谁调用:SKILL.md 的 Step 0.4(见配套 Step_0.4_block.md) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0009 | original/genebe_fields.py.txt:9 | -*- coding: utf-8 -*- | 作用:一条 HGVS(转录本:cDNA)→ 三源并跑 → 输出技能 ACMG 专家层可直接消费的"证据结构"。 | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0010 | original/genebe_fields.py.txt:10 | -*- coding: utf-8 -*- |   · VariantValidator : hg19+hg38 双坐标(权威互证) + 权威 HGVSp | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0011 | original/genebe_fields.py.txt:11 | -*- coding: utf-8 -*- |   · GeneBe           : 变异自身 ClinVar 分类 + 自动 ACMG(对标) + AlphaMissense/BayesDel(补 Worker 缺) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0012 | original/genebe_fields.py.txt:12 | -*- coding: utf-8 -*- |   · 五源 Worker       : gnomAD 全局+EAS 精确 AC/AN + 约束 + 全预测(CADD/REVEL/phyloP/SIFT/PolyPhen/SpliceA | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0014 | original/genebe_fields.py.txt:14 | -*- coding: utf-8 -*- | 命令行: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0015 | original/genebe_fields.py.txt:15 | -*- coding: utf-8 -*- |   python3 references/genebe_fields.py "NM_017780.4:c.2831G>A"            # 默认输出 evidence JSON(供 | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0016 | original/genebe_fields.py.txt:16 | -*- coding: utf-8 -*- |   python3 references/genebe_fields.py "NM_017780.4:c.2831G>A" --card     # 人看的卡 | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0017 | original/genebe_fields.py.txt:17 | -*- coding: utf-8 -*- |   python3 references/genebe_fields.py "NM_017780.4:c.2831G>A" --raw      # 完整原始合并 JSON | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0019 | original/genebe_fields.py.txt:19 | -*- coding: utf-8 -*- | 配置(可选): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0020 | original/genebe_fields.py.txt:20 | -*- coding: utf-8 -*- |   $WORKER_URL / --worker      五源 Worker base URL(默认 DEFAULT_WORKER;你的 host 只存在浏览器,故用 env) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0021 | original/genebe_fields.py.txt:21 | -*- coding: utf-8 -*- |   $GENEBE_KEY / --genebe-key  GeneBe Basic Auth "email:apikey"(防 429) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0022 | original/genebe_fields.py.txt:22 | -*- coding: utf-8 -*- |   $NCBI_KEY                   传给 Worker 以稳住 ClinVar 同位点扫描(若 Worker 支持该参数) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0024 | original/genebe_fields.py.txt:24 | -*- coding: utf-8 -*- | 铁律(与技能一致):每源独立容错,单源失败不拖垮;缺失即 None/❌,绝不臆造; | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0025 | original/genebe_fields.py.txt:25 | -*- coding: utf-8 -*- |   预测只读 *_score;转录本锚定输入 NM;EAS 原始 AF 仅筛,BA1/BS1 的 FAF95 须另查 gnomAD。 | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0026 | original/genebe_fields.py.txt:26 | -*- coding: utf-8 -*- | """ | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0028 | original/genebe_fields.py.txt:28 | -*- coding: utf-8 -*- | import sys, os, json, ssl, argparse, subprocess, urllib.parse, urllib.request | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0030 | original/genebe_fields.py.txt:30 | -*- coding: utf-8 -*- | DEFAULT_WORKER = os.environ.get("WORKER_URL", "https://muddy-cake-9605.yulinj.workers.dev") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0031 | original/genebe_fields.py.txt:31 | -*- coding: utf-8 -*- | VV_BASE = "https://rest.variantvalidator.org/VariantValidator/variantvalidator" | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0032 | original/genebe_fields.py.txt:32 | -*- coding: utf-8 -*- | GENEBE = "https://api.genebe.net/cloud/api-public/v1/variant" | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0035 | original/genebe_fields.py.txt:35 | ============================================================ HTTP(curl 回退) | # ============================================================ HTTP(curl 回退) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0036 | original/genebe_fields.py.txt:36 | ============================================================ HTTP(curl 回退) | _RETRIES = int(os.environ.get("SRC_RETRIES", "3")) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0039 | original/genebe_fields.py.txt:39 | ============================================================ HTTP(curl 回退) | def _get(url, auth=None, timeout=40): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0040 | original/genebe_fields.py.txt:40 | ============================================================ HTTP(curl 回退) |     """带重试的取数。本机出境链路抖动较多，单次失败不代表源不可用。""" | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0041 | original/genebe_fields.py.txt:41 | ============================================================ HTTP(curl 回退) |     import time as _t | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0042 | original/genebe_fields.py.txt:42 | ============================================================ HTTP(curl 回退) |     last = None | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0043 | original/genebe_fields.py.txt:43 | ============================================================ HTTP(curl 回退) |     for _i in range(_RETRIES): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0044 | original/genebe_fields.py.txt:44 | ============================================================ HTTP(curl 回退) |         try: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0045 | original/genebe_fields.py.txt:45 | ============================================================ HTTP(curl 回退) |             return _get_once(url, auth=auth, timeout=timeout) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0046 | original/genebe_fields.py.txt:46 | ============================================================ HTTP(curl 回退) |         except Exception as e: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0047 | original/genebe_fields.py.txt:47 | ============================================================ HTTP(curl 回退) |             last = e | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0048 | original/genebe_fields.py.txt:48 | ============================================================ HTTP(curl 回退) |             if _i < _RETRIES - 1: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0049 | original/genebe_fields.py.txt:49 | ============================================================ HTTP(curl 回退) |                 _t.sleep(1.5 * (_i + 1)) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0050 | original/genebe_fields.py.txt:50 | ============================================================ HTTP(curl 回退) |     raise last | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0053 | original/genebe_fields.py.txt:53 | ============================================================ HTTP(curl 回退) | def _get_once(url, auth=None, timeout=40): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0054 | original/genebe_fields.py.txt:54 | ============================================================ HTTP(curl 回退) |     headers = {"Accept": "application/json"} | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0055 | original/genebe_fields.py.txt:55 | ============================================================ HTTP(curl 回退) |     if auth: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0056 | original/genebe_fields.py.txt:56 | ============================================================ HTTP(curl 回退) |         import base64 | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0057 | original/genebe_fields.py.txt:57 | ============================================================ HTTP(curl 回退) |         headers["Authorization"] = "Basic " + base64.b64encode(auth.encode()).decode() | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0058 | original/genebe_fields.py.txt:58 | ============================================================ HTTP(curl 回退) |     try: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0059 | original/genebe_fields.py.txt:59 | ============================================================ HTTP(curl 回退) |         req = urllib.request.Request(url, headers=headers) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0060 | original/genebe_fields.py.txt:60 | ============================================================ HTTP(curl 回退) |         with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0061 | original/genebe_fields.py.txt:61 | ============================================================ HTTP(curl 回退) |             return json.loads(r.read().decode()) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0062 | original/genebe_fields.py.txt:62 | ============================================================ HTTP(curl 回退) |     except Exception: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0063 | original/genebe_fields.py.txt:63 | ============================================================ HTTP(curl 回退) |         cmd = ["curl", "-s", "-m", str(timeout), url, "-H", "Accept: application/json"] | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0064 | original/genebe_fields.py.txt:64 | ============================================================ HTTP(curl 回退) |         if auth: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0065 | original/genebe_fields.py.txt:65 | ============================================================ HTTP(curl 回退) |             cmd += ["-u", auth] | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0066 | original/genebe_fields.py.txt:66 | ============================================================ HTTP(curl 回退) |         out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0067 | original/genebe_fields.py.txt:67 | ============================================================ HTTP(curl 回退) |         if out.returncode != 0 or not out.stdout.strip(): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0068 | original/genebe_fields.py.txt:68 | ============================================================ HTTP(curl 回退) |             raise RuntimeError(f"curl 失败: {out.stderr.strip() or 'empty'}") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0069 | original/genebe_fields.py.txt:69 | ============================================================ HTTP(curl 回退) |         return json.loads(out.stdout) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0072 | original/genebe_fields.py.txt:72 | ============================================================ 源 1:VariantValidator | # ============================================================ 源 1:VariantValidator | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0073 | original/genebe_fields.py.txt:73 | ============================================================ 源 1:VariantValidator | def src_variantvalidator(hgvs): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0074 | original/genebe_fields.py.txt:74 | ============================================================ 源 1:VariantValidator |     enc = urllib.parse.quote(hgvs, safe="") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0075 | original/genebe_fields.py.txt:75 | ============================================================ 源 1:VariantValidator |     d = _get(f"{VV_BASE}/GRCh38/{enc}/all") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0076 | original/genebe_fields.py.txt:76 | ============================================================ 源 1:VariantValidator |     for _, val in d.items(): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0077 | original/genebe_fields.py.txt:77 | ============================================================ 源 1:VariantValidator |         if isinstance(val, dict) and "primary_assembly_loci" in val: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0078 | original/genebe_fields.py.txt:78 | ============================================================ 源 1:VariantValidator |             loci = val["primary_assembly_loci"] | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0080 | original/genebe_fields.py.txt:80 | ============================================================ 源 1:VariantValidator |             def vcf(asm): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0081 | original/genebe_fields.py.txt:81 | ============================================================ 源 1:VariantValidator |                 v = (loci.get(asm) or {}).get("vcf") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0082 | original/genebe_fields.py.txt:82 | ============================================================ 源 1:VariantValidator |                 if isinstance(v, dict): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0083 | original/genebe_fields.py.txt:83 | ============================================================ 源 1:VariantValidator |                     return dict(chr=str(v.get("chr")), pos=str(v.get("pos")), | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0084 | original/genebe_fields.py.txt:84 | ============================================================ 源 1:VariantValidator |                                 ref=v.get("ref"), alt=v.get("alt")) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0085 | original/genebe_fields.py.txt:85 | ============================================================ 源 1:VariantValidator |                 if isinstance(v, str) and v.count("-") == 3: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0086 | original/genebe_fields.py.txt:86 | ============================================================ 源 1:VariantValidator |                     c, p, r, a = v.split("-"); return dict(chr=c, pos=p, ref=r, alt=a) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0087 | original/genebe_fields.py.txt:87 | ============================================================ 源 1:VariantValidator |                 return None | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0089 | original/genebe_fields.py.txt:89 | ============================================================ 源 1:VariantValidator |             prot = val.get("hgvs_predicted_protein_consequence") or {} | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0090 | original/genebe_fields.py.txt:90 | ============================================================ 源 1:VariantValidator |             return {"hg19": vcf("grch37"), "hg38": vcf("grch38"), | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0091 | original/genebe_fields.py.txt:91 | ============================================================ 源 1:VariantValidator |                     "hgvs_c": val.get("hgvs_transcript_variant"), | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0092 | original/genebe_fields.py.txt:92 | ============================================================ 源 1:VariantValidator |                     "hgvs_p": prot.get("tlr") or prot.get("slr"), | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0093 | original/genebe_fields.py.txt:93 | ============================================================ 源 1:VariantValidator |                     "transcript": (val.get("hgvs_transcript_variant") or hgvs).split(":")[0]} | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0094 | original/genebe_fields.py.txt:94 | ============================================================ 源 1:VariantValidator |     raise RuntimeError("无 primary_assembly_loci(变异描述可能有误)") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0097 | original/genebe_fields.py.txt:97 | ============================================================ 源 2:GeneBe | # ============================================================ 源 2:GeneBe | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0098 | original/genebe_fields.py.txt:98 | ============================================================ 源 2:GeneBe | def src_genebe(coord, transcript, auth=None): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0099 | original/genebe_fields.py.txt:99 | ============================================================ 源 2:GeneBe |     qs = urllib.parse.urlencode(dict(chr=coord["chr"], pos=coord["pos"], ref=coord["ref"], | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0100 | original/genebe_fields.py.txt:100 | ============================================================ 源 2:GeneBe |                                      alt=coord["alt"], genome="hg38", useEnsembl="False")) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0101 | original/genebe_fields.py.txt:101 | ============================================================ 源 2:GeneBe |     d = _get(f"{GENEBE}?{qs}", auth=auth) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0102 | original/genebe_fields.py.txt:102 | ============================================================ 源 2:GeneBe |     v = (d.get("variants") or [d])[0] if isinstance(d, dict) else {} | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0103 | original/genebe_fields.py.txt:103 | ============================================================ 源 2:GeneBe |     cons = v.get("consequences") or [] | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0104 | original/genebe_fields.py.txt:104 | ============================================================ 源 2:GeneBe |     pick = next((c for c in cons if (c.get("transcript") or c.get("feature")) == transcript), | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0105 | original/genebe_fields.py.txt:105 | ============================================================ 源 2:GeneBe |                 cons[0] if cons else {}) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0106 | original/genebe_fields.py.txt:106 | ============================================================ 源 2:GeneBe |     by_gene = (v.get("acmg_by_gene") or [{}])[0] | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0107 | original/genebe_fields.py.txt:107 | ============================================================ 源 2:GeneBe |     return { | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0108 | original/genebe_fields.py.txt:108 | ============================================================ 源 2:GeneBe |         "hgvs_p": pick.get("hgvs_p"), "dbsnp": v.get("dbsnp"), | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0109 | original/genebe_fields.py.txt:109 | ============================================================ 源 2:GeneBe |         "acmg_class": v.get("acmg_classification") or by_gene.get("verdict"), | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0110 | original/genebe_fields.py.txt:110 | ============================================================ 源 2:GeneBe |         "acmg_criteria": v.get("acmg_criteria"), "acmg_score": v.get("acmg_score"), | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0111 | original/genebe_fields.py.txt:111 | ============================================================ 源 2:GeneBe |         "clinvar_class": v.get("clinvar_classification"), "clinvar_stars": v.get("clinvar_revie | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0112 | original/genebe_fields.py.txt:112 | ============================================================ 源 2:GeneBe |         "clinvar_subs": v.get("clinvar_submissions_summary"), "clinvar_disease": v.get("clinvar | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0113 | original/genebe_fields.py.txt:113 | ============================================================ 源 2:GeneBe |         # 补 Worker 缺的预测(只读 *_score) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0114 | original/genebe_fields.py.txt:114 | ============================================================ 源 2:GeneBe |         "alphamissense": v.get("alphamissense_score"), "bayesdel_noaf": v.get("bayesdelnoaf_sco | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0115 | original/genebe_fields.py.txt:115 | ============================================================ 源 2:GeneBe |     } | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0118 | original/genebe_fields.py.txt:118 | ============================================================ 源 3:五源 Worker | # ============================================================ 源 3:五源 Worker | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0119 | original/genebe_fields.py.txt:119 | ============================================================ 源 3:五源 Worker | def src_worker(hgvs, worker_url, dataset="gnomad_r4"): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0120 | original/genebe_fields.py.txt:120 | ============================================================ 源 3:五源 Worker |     enc = urllib.parse.quote(hgvs, safe="") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0121 | original/genebe_fields.py.txt:121 | ============================================================ 源 3:五源 Worker |     url = f"{worker_url.rstrip('/')}/annotate?hgvs={enc}&dataset={dataset}" | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0122 | original/genebe_fields.py.txt:122 | ============================================================ 源 3:五源 Worker |     if os.environ.get("NCBI_KEY"): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0123 | original/genebe_fields.py.txt:123 | ============================================================ 源 3:五源 Worker |         url += f"&ncbi_key={os.environ['NCBI_KEY']}"   # 若 Worker 支持,稳住 ClinVar 扫描 | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0124 | original/genebe_fields.py.txt:124 | ============================================================ 源 3:五源 Worker |     return _get(url) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0127 | original/genebe_fields.py.txt:127 | ============================================================ 编排 | # ============================================================ 编排 | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0128 | original/genebe_fields.py.txt:128 | ============================================================ 编排 | def annotate(hgvs, worker_url=DEFAULT_WORKER, genebe_auth=None, dataset="gnomad_r4"): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0129 | original/genebe_fields.py.txt:129 | ============================================================ 编排 |     err = {} | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0130 | original/genebe_fields.py.txt:130 | ============================================================ 编排 |     try: wk = src_worker(hgvs, worker_url, dataset) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0131 | original/genebe_fields.py.txt:131 | ============================================================ 编排 |     except Exception as e: wk, err["worker"] = None, str(e)[:120] | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0132 | original/genebe_fields.py.txt:132 | ============================================================ 编排 |     try: vv = src_variantvalidator(hgvs) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0133 | original/genebe_fields.py.txt:133 | ============================================================ 编排 |     except Exception as e: vv, err["variantvalidator"] = None, str(e)[:120] | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0135 | original/genebe_fields.py.txt:135 | ============================================================ 编排 |     coord = (vv or {}).get("hg38") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0136 | original/genebe_fields.py.txt:136 | ============================================================ 编排 |     if not coord and wk and wk.get("coord"): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0137 | original/genebe_fields.py.txt:137 | ============================================================ 编排 |         w = wk["coord"]; coord = dict(chr=str(w["chr"]), pos=str(w["pos"]), ref=w["ref"], alt=w | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0138 | original/genebe_fields.py.txt:138 | ============================================================ 编排 |     transcript = (vv or {}).get("transcript") or hgvs.split(":")[0] | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0139 | original/genebe_fields.py.txt:139 | ============================================================ 编排 |     if coord: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0140 | original/genebe_fields.py.txt:140 | ============================================================ 编排 |         try: gb = src_genebe(coord, transcript, auth=genebe_auth) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0141 | original/genebe_fields.py.txt:141 | ============================================================ 编排 |         except Exception as e: gb, err["genebe"] = None, str(e)[:120] | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0142 | original/genebe_fields.py.txt:142 | ============================================================ 编排 |     else: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0143 | original/genebe_fields.py.txt:143 | ============================================================ 编排 |         gb, err["genebe"] = None, "无 hg38 坐标" | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0145 | original/genebe_fields.py.txt:145 | ============================================================ 编排 |     return {"input": hgvs, | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0146 | original/genebe_fields.py.txt:146 | ============================================================ 编排 |             "_sources": {k: ("ok" if v else f"❌ {err.get(k,'')}") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0147 | original/genebe_fields.py.txt:147 | ============================================================ 编排 |                          for k, v in [("variantvalidator", vv), ("genebe", gb), ("worker", wk)] | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0148 | original/genebe_fields.py.txt:148 | ============================================================ 编排 |             "_raw": {"variantvalidator": vv, "genebe": gb, "worker": wk}} | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0151 | original/genebe_fields.py.txt:151 | ============================================================ 预消化为技能证据结构 | # ============================================================ 预消化为技能证据结构 | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0152 | original/genebe_fields.py.txt:152 | ============================================================ 预消化为技能证据结构 | def to_evidence(card): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0153 | original/genebe_fields.py.txt:153 | ============================================================ 预消化为技能证据结构 |     """把三源合并结果映射为技能各模块直接可用的证据块。缺失即 None/❌,不臆造。""" | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0154 | original/genebe_fields.py.txt:154 | ============================================================ 预消化为技能证据结构 |     vv = card["_raw"]["variantvalidator"] or {} | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0155 | original/genebe_fields.py.txt:155 | ============================================================ 预消化为技能证据结构 |     gb = card["_raw"]["genebe"] or {} | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0156 | original/genebe_fields.py.txt:156 | ============================================================ 预消化为技能证据结构 |     wk = card["_raw"]["worker"] or {} | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0157 | original/genebe_fields.py.txt:157 | ============================================================ 预消化为技能证据结构 |     g = wk.get("gnomad") or {} | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0158 | original/genebe_fields.py.txt:158 | ============================================================ 预消化为技能证据结构 |     coord = wk.get("coord") or {} | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0160 | original/genebe_fields.py.txt:160 | ============================================================ 预消化为技能证据结构 |     # 预测:Worker 列表(去重,读 value) + GeneBe 补 AlphaMissense/BayesDel | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0161 | original/genebe_fields.py.txt:161 | ============================================================ 预消化为技能证据结构 |     preds = {} | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0162 | original/genebe_fields.py.txt:162 | ============================================================ 预消化为技能证据结构 |     for pr in (wk.get("merged_predictors") or []): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0163 | original/genebe_fields.py.txt:163 | ============================================================ 预消化为技能证据结构 |         preds.setdefault(pr.get("id"), {"value": pr.get("value"), "source": pr.get("source")}) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0164 | original/genebe_fields.py.txt:164 | ============================================================ 预消化为技能证据结构 |     if gb.get("alphamissense") is not None: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0165 | original/genebe_fields.py.txt:165 | ============================================================ 预消化为技能证据结构 |         preds["ALPHAMISSENSE"] = {"value": gb["alphamissense"], "source": "GeneBe"} | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0166 | original/genebe_fields.py.txt:166 | ============================================================ 预消化为技能证据结构 |     if gb.get("bayesdel_noaf") is not None: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0167 | original/genebe_fields.py.txt:167 | ============================================================ 预消化为技能证据结构 |         preds["BAYESDEL_NOAF"] = {"value": gb["bayesdel_noaf"], "source": "GeneBe"} | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0169 | original/genebe_fields.py.txt:169 | ============================================================ 预消化为技能证据结构 |     # 频率提示(仅筛) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0170 | original/genebe_fields.py.txt:170 | ============================================================ 预消化为技能证据结构 |     eas_af, glob_af = g.get("eas_af"), g.get("global_af") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0171 | original/genebe_fields.py.txt:171 | ============================================================ 预消化为技能证据结构 |     if eas_af is None: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0172 | original/genebe_fields.py.txt:172 | ============================================================ 预消化为技能证据结构 |         fhint = None | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0173 | original/genebe_fields.py.txt:173 | ============================================================ 预消化为技能证据结构 |     elif eas_af >= 0.005: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0174 | original/genebe_fields.py.txt:174 | ============================================================ 预消化为技能证据结构 |         fhint = f"EAS AF={eas_af:.4%} 偏高 → 倾向 BS1(须以 gnomAD grpmax FAF95 确认;此为原始AF)" | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0175 | original/genebe_fields.py.txt:175 | ============================================================ 预消化为技能证据结构 |     elif eas_af == 0 and glob_af in (0, None): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0176 | original/genebe_fields.py.txt:176 | ============================================================ 预消化为技能证据结构 |         fhint = "近缺失 → 倾向 PM2" | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0177 | original/genebe_fields.py.txt:177 | ============================================================ 预消化为技能证据结构 |     else: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0178 | original/genebe_fields.py.txt:178 | ============================================================ 预消化为技能证据结构 |         fhint = f"EAS AF={eas_af:.4%}(原始AF,非FAF95)" | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0180 | original/genebe_fields.py.txt:180 | ============================================================ 预消化为技能证据结构 |     return { | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0181 | original/genebe_fields.py.txt:181 | ============================================================ 预消化为技能证据结构 |         # Step 0 蛋白强制验证门:VV 权威 HGVSp;GeneBe 交叉 | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0182 | original/genebe_fields.py.txt:182 | ============================================================ 预消化为技能证据结构 |         "protein_gate": {"transcript": vv.get("transcript"), "hgvs_c": vv.get("hgvs_c"), | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0183 | original/genebe_fields.py.txt:183 | ============================================================ 预消化为技能证据结构 |                          "hgvs_p": vv.get("hgvs_p") or gb.get("hgvs_p"), | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0184 | original/genebe_fields.py.txt:184 | ============================================================ 预消化为技能证据结构 |                          "hgvs_p_genebe": gb.get("hgvs_p"), | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0185 | original/genebe_fields.py.txt:185 | ============================================================ 预消化为技能证据结构 |                          "source": "VariantValidator(权威)+GeneBe(交叉)", | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0186 | original/genebe_fields.py.txt:186 | ============================================================ 预消化为技能证据结构 |                          "passed": bool(vv.get("hgvs_p") or gb.get("hgvs_p"))}, | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0187 | original/genebe_fields.py.txt:187 | ============================================================ 预消化为技能证据结构 |         # 坐标 | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0188 | original/genebe_fields.py.txt:188 | ============================================================ 预消化为技能证据结构 |         "coords": {"hg38": vv.get("hg38") or ({"chr": coord.get("chr"), "pos": coord.get("pos") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0189 | original/genebe_fields.py.txt:189 | ============================================================ 预消化为技能证据结构 |                                                "ref": coord.get("ref"), "alt": coord.get("alt") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0190 | original/genebe_fields.py.txt:190 | ============================================================ 预消化为技能证据结构 |                    "hg19": vv.get("hg19"), "hgvsg38": coord.get("hgvsg"), | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0191 | original/genebe_fields.py.txt:191 | ============================================================ 预消化为技能证据结构 |                    "rsid": gb.get("dbsnp") or coord.get("rsid")}, | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0192 | original/genebe_fields.py.txt:192 | ============================================================ 预消化为技能证据结构 |         # Step 0.5 ClinVar 分流 | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0193 | original/genebe_fields.py.txt:193 | ============================================================ 预消化为技能证据结构 |         "clinvar": {"classification": gb.get("clinvar_class"), "stars": gb.get("clinvar_stars") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0194 | original/genebe_fields.py.txt:194 | ============================================================ 预消化为技能证据结构 |                     "submissions": gb.get("clinvar_subs"), "disease": gb.get("clinvar_disease") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0195 | original/genebe_fields.py.txt:195 | ============================================================ 预消化为技能证据结构 |         # Step 1.2 频率(EAS 原始 AC/AN;FAF95 须另查) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0196 | original/genebe_fields.py.txt:196 | ============================================================ 预消化为技能证据结构 |         "frequency": {"global": {"af": g.get("global_af"), "ac": g.get("global_ac"), "an": g.ge | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0197 | original/genebe_fields.py.txt:197 | ============================================================ 预消化为技能证据结构 |                       "eas": {"af": eas_af, "ac": g.get("eas_ac"), "an": g.get("eas_an")}, | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0198 | original/genebe_fields.py.txt:198 | ============================================================ 预消化为技能证据结构 |                       "hint": fhint, | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0199 | original/genebe_fields.py.txt:199 | ============================================================ 预消化为技能证据结构 |                       "authority_note": "EAS 为原始 AF;BA1/BS1 的 grpmax FAF95 须查 gnomAD GraphQL/官网 | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0200 | original/genebe_fields.py.txt:200 | ============================================================ 预消化为技能证据结构 |         # Step 1.2 预测(读 value=*_score) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0201 | original/genebe_fields.py.txt:201 | ============================================================ 预消化为技能证据结构 |         "predictors": preds, | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0202 | original/genebe_fields.py.txt:202 | ============================================================ 预消化为技能证据结构 |         # 约束(PVS1/PM2/PP2/BP1 背景) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0203 | original/genebe_fields.py.txt:203 | ============================================================ 预消化为技能证据结构 |         "constraint": wk.get("constraint"), | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0204 | original/genebe_fields.py.txt:204 | ============================================================ 预消化为技能证据结构 |         # PS1/PM5 同位点地形 | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0205 | original/genebe_fields.py.txt:205 | ============================================================ 预消化为技能证据结构 |         "codon_landscape": wk.get("codon_landscape"), | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0206 | original/genebe_fields.py.txt:206 | ============================================================ 预消化为技能证据结构 |         # 模块5 外部对标(不覆盖专家层) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0207 | original/genebe_fields.py.txt:207 | ============================================================ 预消化为技能证据结构 |         "acmg_benchmark": {"tool": "GeneBe", "classification": gb.get("acmg_class"), | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0208 | original/genebe_fields.py.txt:208 | ============================================================ 预消化为技能证据结构 |                            "criteria": gb.get("acmg_criteria"), "score": gb.get("acmg_score")}, | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0209 | original/genebe_fields.py.txt:209 | ============================================================ 预消化为技能证据结构 |         # 元信息 | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0210 | original/genebe_fields.py.txt:210 | ============================================================ 预消化为技能证据结构 |         "_sources": card["_sources"], | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0211 | original/genebe_fields.py.txt:211 | ============================================================ 预消化为技能证据结构 |         "_warnings": wk.get("warnings"), | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0212 | original/genebe_fields.py.txt:212 | ============================================================ 预消化为技能证据结构 |         "_needs_manual": ["grpmax FAF95(BA1/BS1)→ gnomAD GraphQL", | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0213 | original/genebe_fields.py.txt:213 | ============================================================ 预消化为技能证据结构 |                           "中国人群频率(ChinaMAP/WBBC/NyuWa)→ 门户人工"], | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0214 | original/genebe_fields.py.txt:214 | ============================================================ 预消化为技能证据结构 |         "_rules": {"freq": "EAS 原始 AF 仅筛;FAF95 另查", "pred": "读 *_score 值 + 技能阈值定 PP3/BP4", | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0215 | original/genebe_fields.py.txt:215 | ============================================================ 预消化为技能证据结构 |                    "acmg": "GeneBe 判定仅对标,不替代技能专家评级", | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0216 | original/genebe_fields.py.txt:216 | ============================================================ 预消化为技能证据结构 |                    "transcript": "以 VV/GeneBe 的 RefSeq NM 为准"}, | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0217 | original/genebe_fields.py.txt:217 | ============================================================ 预消化为技能证据结构 |     } | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0220 | original/genebe_fields.py.txt:220 | ============================================================ 人看的卡(可选) | # ============================================================ 人看的卡(可选) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0221 | original/genebe_fields.py.txt:221 | ============================================================ 人看的卡(可选) | def render_card(card): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0222 | original/genebe_fields.py.txt:222 | ============================================================ 人看的卡(可选) |     ev = to_evidence(card); L = [] | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0223 | original/genebe_fields.py.txt:223 | ============================================================ 人看的卡(可选) |     pg, co, fr = ev["protein_gate"], ev["coords"], ev["frequency"] | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0224 | original/genebe_fields.py.txt:224 | ============================================================ 人看的卡(可选) |     hg = lambda d: f"chr{d['chr']}:{d['pos']} {d['ref']}>{d['alt']}" if d else "❌" | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0225 | original/genebe_fields.py.txt:225 | ============================================================ 人看的卡(可选) |     L += ["═" * 60, f"  变异卡 · {card['input']}", "═" * 60, | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0226 | original/genebe_fields.py.txt:226 | ============================================================ 人看的卡(可选) |           f"  转录本  : {pg['transcript'] or '❌'}", | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0227 | original/genebe_fields.py.txt:227 | ============================================================ 人看的卡(可选) |           f"  HGVSc   : {pg['hgvs_c'] or '❌'}", | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0228 | original/genebe_fields.py.txt:228 | ============================================================ 人看的卡(可选) |           f"  HGVSp   : {pg['hgvs_p'] or '❌'}", | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0229 | original/genebe_fields.py.txt:229 | ============================================================ 人看的卡(可选) |           f"  hg38    : {hg(co['hg38'])}    hg19 : {hg(co['hg19'])}", | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0230 | original/genebe_fields.py.txt:230 | ============================================================ 人看的卡(可选) |           f"  rsID    : {co['rsid'] or '❌'}", "─" * 60, | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0231 | original/genebe_fields.py.txt:231 | ============================================================ 人看的卡(可选) |           f"  gnomAD 全局: AF={fr['global']['af']} AC={fr['global']['ac']} AN={fr['global']['an'] | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0232 | original/genebe_fields.py.txt:232 | ============================================================ 人看的卡(可选) |           f"  gnomAD EAS : AF={fr['eas']['af']} AC={fr['eas']['ac']} AN={fr['eas']['an']}", | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0233 | original/genebe_fields.py.txt:233 | ============================================================ 人看的卡(可选) |           f"  频率提示   : {fr['hint']}", "─" * 60, "  预测(*_score):"] | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0234 | original/genebe_fields.py.txt:234 | ============================================================ 人看的卡(可选) |     for k, val in ev["predictors"].items(): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0235 | original/genebe_fields.py.txt:235 | ============================================================ 人看的卡(可选) |         L.append(f"    {k:<18}{val['value']}  [{val['source']}]") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0236 | original/genebe_fields.py.txt:236 | ============================================================ 人看的卡(可选) |     L += ["─" * 60, | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0237 | original/genebe_fields.py.txt:237 | ============================================================ 人看的卡(可选) |           f"  ClinVar     : {ev['clinvar']['classification'] or '❌'} ({ev['clinvar']['submissio | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0238 | original/genebe_fields.py.txt:238 | ============================================================ 人看的卡(可选) |           f"  GeneBe ACMG : {ev['acmg_benchmark']['classification'] or '❌'} " | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0239 | original/genebe_fields.py.txt:239 | ============================================================ 人看的卡(可选) |           f"[{ev['acmg_benchmark']['criteria'] or ''}; {ev['acmg_benchmark']['score']}]", | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0240 | original/genebe_fields.py.txt:240 | ============================================================ 人看的卡(可选) |           f"  同位点地形  : {ev['codon_landscape'] or '❌(见 warnings)'}", | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0241 | original/genebe_fields.py.txt:241 | ============================================================ 人看的卡(可选) |           f"  取数状态    : {json.dumps(ev['_sources'], ensure_ascii=False)}"] | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0242 | original/genebe_fields.py.txt:242 | ============================================================ 人看的卡(可选) |     if ev["_warnings"]: L.append(f"  警告        : {ev['_warnings']}") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0243 | original/genebe_fields.py.txt:243 | ============================================================ 人看的卡(可选) |     L.append("═" * 60) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0244 | original/genebe_fields.py.txt:244 | ============================================================ 人看的卡(可选) |     return "\n".join(L) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0247 | original/genebe_fields.py.txt:247 | ============================================================ 人看的卡(可选) | def main(): | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0248 | original/genebe_fields.py.txt:248 | ============================================================ 人看的卡(可选) |     ap = argparse.ArgumentParser() | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0249 | original/genebe_fields.py.txt:249 | ============================================================ 人看的卡(可选) |     ap.add_argument("hgvs") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0250 | original/genebe_fields.py.txt:250 | ============================================================ 人看的卡(可选) |     ap.add_argument("--worker", default=DEFAULT_WORKER) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0251 | original/genebe_fields.py.txt:251 | ============================================================ 人看的卡(可选) |     ap.add_argument("--genebe-key", default=os.environ.get("GENEBE_KEY")) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0252 | original/genebe_fields.py.txt:252 | ============================================================ 人看的卡(可选) |     ap.add_argument("--dataset", default="gnomad_r4") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0253 | original/genebe_fields.py.txt:253 | ============================================================ 人看的卡(可选) |     g = ap.add_mutually_exclusive_group() | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0254 | original/genebe_fields.py.txt:254 | ============================================================ 人看的卡(可选) |     g.add_argument("--card", action="store_true", help="人看的卡") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0255 | original/genebe_fields.py.txt:255 | ============================================================ 人看的卡(可选) |     g.add_argument("--raw", action="store_true", help="完整原始合并 JSON") | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0256 | original/genebe_fields.py.txt:256 | ============================================================ 人看的卡(可选) |     a = ap.parse_args() | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0257 | original/genebe_fields.py.txt:257 | ============================================================ 人看的卡(可选) |     card = annotate(a.hgvs, a.worker, a.genebe_key, a.dataset) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0258 | original/genebe_fields.py.txt:258 | ============================================================ 人看的卡(可选) |     if a.card: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0259 | original/genebe_fields.py.txt:259 | ============================================================ 人看的卡(可选) |         print(render_card(card)) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0260 | original/genebe_fields.py.txt:260 | ============================================================ 人看的卡(可选) |     elif a.raw: | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0261 | original/genebe_fields.py.txt:261 | ============================================================ 人看的卡(可选) |         print(json.dumps(card, ensure_ascii=False, indent=2)) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0262 | original/genebe_fields.py.txt:262 | ============================================================ 人看的卡(可选) |     else:  # 默认:供技能消费的 evidence JSON | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0263 | original/genebe_fields.py.txt:263 | ============================================================ 人看的卡(可选) |         print(json.dumps(to_evidence(card), ensure_ascii=False, indent=2)) | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0266 | original/genebe_fields.py.txt:266 | ============================================================ 人看的卡(可选) | if __name__ == "__main__": | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
| P-0267 | original/genebe_fields.py.txt:267 | ============================================================ 人看的卡(可选) |     main() | scripts/genebe_fields.py | 原代码归档；替代脚本已实现，实时接口未验证 |
