# gene-variant-pathogenicity

> 基因变异致病性评级分析技能 —— 一个为 Claude（Claude Code / Agent Skills）设计的、遵循 **ACMG/AMP 2015 + ClinGen SVI 系列更新 + ACGS 2024** 的临床级变异解读工作流，内置**三源结构化取数引擎**、**产前遗传咨询专项模块**与**多重质控门控**。

<!-- Version: +GeneBe 三源集成 2026-07 -->

---

## 目录

- [这是什么](#这是什么)
- [核心特性](#核心特性)
- [仓库结构](#仓库结构)
- [安装与触发](#安装与触发)
- [支持的输入格式](#支持的输入格式)
- [运行模式](#运行模式)
- [工作流程总览（Step 0–9）](#工作流程总览step-09)
- [三源取数引擎 `genebe_fields.py`](#三源取数引擎-genebe_fieldspy)
- [参考知识库](#参考知识库)
- [输出结构（模块 1–10）](#输出结构模块-110)
- [关键质控门控](#关键质控门控)
- [环境依赖](#环境依赖)
- [使用示例](#使用示例)
- [设计原则](#设计原则)
- [局限性与免责声明](#局限性与免责声明)
- [数据来源与致谢](#数据来源与致谢)
- [版本历史](#版本历史)

---

## 这是什么

`gene-variant-pathogenicity` 是一个 **Agent Skill**（技能包）。当用户提供任意基因变异位点并要求做致病性评估 / ACMG 分级 / 变异解读时，Claude 会加载本技能的 `SKILL.md` 指令，按标准化流程完成：

1. **输入解析与标准化**（HGVS / 蛋白 / cDNA / VCF / 自然语言 → 统一格式）
2. **多源数据检索与交叉校验**（ClinVar、gnomAD、OMIM、ClinGen、UniProt、文献）
3. **ACMG/AMP 证据代码逐条赋值**（含 ClinGen SVI 最新细则与基因特异性 VCEP 规则）
4. **家系 / 表型证据整合**（de novo 双轴量化、PM3 反式、共分离、PP4）
5. **中文深度分析报告 + 临床可操作性建议**（产前场景另有预后矩阵）

技能的定位角色是"顶级遗传变异科学家 + 生物信息学专家 + 资深产前遗传咨询师"，强调**数据驱动、透明、保守、可追溯、零编造**。

> ⚠️ **本技能为临床决策辅助工具，所有结论必须经认证临床遗传学家 / 遗传咨询师审核后方可用于临床。**

---

## 核心特性

| 特性 | 说明 |
|---|---|
| 🧬 **全格式输入** | HGVS(cDNA/蛋白)、基因+变异、VCF 坐标、rsID、自然语言，均可解析标准化 |
| 🔀 **三源取数引擎** | `genebe_fields.py` 一条命令并跑 VariantValidator + GeneBe + 五源 Worker，坍缩零散检索 |
| 🚦 **智能运行模式** | 快速 / 深度 / **产前**三模式自动切换；CNV 自动路由到独立评分框架 |
| 📐 **完整 ACMG 引擎** | PVS1 四级决策树、PM2 降级、PS3/BS3 OddsPath 门槛、PM1 三门槛五问、de novo 双轴量化、Bayesian 积分交叉验证 |
| 🏥 **ClinGen VCEP 全文门控** | 有基因特异性规范时**强制取得全文**后才据其赋分，取不到则诚实回退并请求上传 |
| 🤰 **产前专项** | 邻近位点扩圈检索、预后导向文献检索、产前 de novo 表型特异性分级、产前预后矩阵输出 |
| 🔎 **Novel Variant 地形感知** | ClinVar 无记录时三圈扩展检索建立"最近已知参照点"，而非直接跳计算预测 |
| ✅ **参考文献 PMID 反查** | 输出前强制逐条反查作者 / 期刊 / 年份 / PMID，杜绝虚构或错误归属引文 |
| 🈶 **双语规范输出** | 分子信息英文标签、证据链全中文、报告深度分析中文 |

---

## 仓库结构

```
gene-variant-pathogenicity/
├── SKILL.md                    # 技能主指令（工作流全文，Claude 加载入口）
├── README.md                   # 本文件
└── references/
    ├── ACMG_CRITERIA.md        # SNV/Indel 的 ACMG 证据代码定义与判定规则（核心必读）
    ├── CNV_CRITERIA.md         # 拷贝数变异 ClinGen 五段式评分框架
    └── genebe_fields.py        # 三源结构化取数引擎（Step 0.4 调用）
```

| 文件 | 行数 | 作用 |
|---|---|---|
| `SKILL.md` | ~1336 | 技能主体：角色、运行模式、Step 0–9、判定引擎、输出结构、关键原则 |
| `references/ACMG_CRITERIA.md` | ~576 | PVS1 决策树、PM2/BA1/BS1、PS3/BS3、PM1、家系证据、矛盾处理、产前提醒 |
| `references/CNV_CRITERIA.md` | ~197 | CNV 五段式评分、基因内 CNV 的 PVS1 复用、产前 CNV 专项 |
| `references/genebe_fields.py` | ~250 | VariantValidator + GeneBe + 五源 Worker 并跑，输出证据 JSON |

---

## 安装与触发

### 作为 Claude Code / Agent Skill 使用

将整个 `gene-variant-pathogenicity/` 目录放入 Claude 的 skills 目录（或按你的 Agent SDK / 插件加载方式注册）。技能通过 `SKILL.md` 顶部 frontmatter 的 `description` 自动触发——用户无需记忆技能名，只要出现变异评级意图即可命中。

### 触发关键词（示例）

> "帮我评级这个变异" · "这个突变致病吗" · "ACMG 分类" · "分析一下这个位点" · "variant classification" · "对比一下 ClinVar / Franklin 评级" · "评估家系共分离证据" · 直接粘贴变异信息

---

## 支持的输入格式

| 格式 | 示例 | 处理方式 |
|---|---|---|
| HGVS cDNA（含转录本） | `NM_000527.5:c.1183C>T` | 直接使用，校验是否 MANE Select |
| HGVS cDNA（含基因名） | `LDLR c.1183C>T` | 查 MANE Select 补全 |
| 蛋白变异 | `BRCA1 p.Arg1699Trp` / `p.R1699W` | 反向映射至 cDNA |
| VCF 坐标 | `chr19-11116839-G-A` (GRCh38) | 注释基因 / 转录本 / HGVS |
| rsID | `rs745738318` | 解析变异 |
| CNV | `chr11:19076957-36302387_del` / `Exon 10-12 dup` | 路由到 `CNV_CRITERIA.md` |
| 自然语言 | "LDLR 基因第 8 外显子错义变异 c.1183C>T" | 提取关键信息标准化 |
| 批量 | 多变异列表 / 表格 | 逐一处理 + 汇总表 |

---

## 运行模式

技能根据信息量与临床场景**自动**选择模式：

- **快速模式** — 仅提供变异，无家系 / 表型。执行 Step 1–4，跳过家系整合。适合批量初筛。
- **深度模式** — 变异 + 家系 + 表型。执行完整 Step 1–5（含家系证据整合）。适合疑难病例讨论。
- **产前模式** — 出现"胎儿 / 孕 / 产前 / prenatal / 超声发现 / 出生后表现 / 预后"等信号即激活，**额外**执行：
  - Step 0.7 产前预后导向文献检索（影像学结局、神经发育结局、监测窗口）
  - 模块 8′ 产前预后矩阵（回答"出生后孩子会是什么表现"）
- **CNV 路由** — 输入为拷贝数变异时切换到 `references/CNV_CRITERIA.md` 的 ClinGen 五段式评分。

---

## 工作流程总览（Step 0–9）

```
Step 0    输入解析与标准化 + 蛋白改变强制验证门控（禁止心算推导 HGVSp）
Step 0.4  三源结构化取数（genebe_fields.py，High-Priority Layer 0）
Step 0.5  ClinVar 前置快速筛查（确认模式 vs 完整分析模式分流）
Step 0.6  Novel Variant 邻近位点三圈扩展检索（ClinVar 无记录时强制）
Step 0.7  产前预后导向检索（仅产前模式）
Step 1    数据库检索（ClinVar / gnomAD / OMIM / ClinGen，三层可靠性框架）
Step 2    分子定位与转录本核实（MANE Select 校验）
Step 3    外部分类对标（VarSome / Franklin / InterVar）
Step 4    功能预测与 LoF 评估（REVEL/SpliceAI 阈值 + PVS1 四级决策树）
Step 4A   ClinGen 基因特异性 VCEP 规则适配（全文强制获取门控）
Step 5    家系整合分析（de novo 双轴量化 / PM3 / 共分离 / PP4，深度模式）
──────    ACMG 判定引擎（证据赋值 → 冲突审查 → 组合规则 + Bayesian 积分交叉验证）
Step 9-V  参考文献 PMID 反查验证（输出前最后一道质控关卡）
```

每一步都内置"检索状态记录"（✅ 成功 / ⚠️ 部分 / ❌ 失败），失败即如实标注并给出用户自查链接，绝不伪造数据。

---

## 三源取数引擎 `genebe_fields.py`

一条 HGVS（`转录本:cDNA`）→ 三源并跑 → 输出技能 ACMG 专家层可直接消费的"证据结构"，用于坍缩后续零散的 web_search。

### 三个数据源

| 源 | 提供 |
|---|---|
| **VariantValidator** | hg19 + hg38 双坐标（权威互证）+ 权威 HGVSp |
| **GeneBe** | 变异自身 ClinVar 分类 + 自动 ACMG（仅对标）+ AlphaMissense / BayesDel |
| **五源 Worker** | gnomAD 全局 + EAS 精确 AC/AN + 约束 + 全预测（CADD/REVEL/phyloP/SIFT/PolyPhen/SpliceAI）+ 同位点地形 |

### 命令行

```bash
# 默认输出 evidence JSON（供技能消费）
python3 references/genebe_fields.py "NM_017780.4:c.2831G>A"

# 人类可读卡片
python3 references/genebe_fields.py "NM_017780.4:c.2831G>A" --card

# 完整原始合并 JSON
python3 references/genebe_fields.py "NM_017780.4:c.2831G>A" --raw
```

### 可选配置（环境变量 / 参数）

| 变量 / 参数 | 作用 |
|---|---|
| `$WORKER_URL` / `--worker` | 五源 Worker base URL |
| `$GENEBE_KEY` / `--genebe-key` | GeneBe Basic Auth `email:apikey`（防 429） |
| `$NCBI_KEY` | 传给 Worker 稳定 ClinVar 同位点扫描 |

### 输出字段 → 下游模块

| 证据键 | 喂给 | 说明 |
|---|---|---|
| `protein_gate` | Step 0 蛋白强制验证门 | `passed=true` 即过门，不再心算 |
| `coords` | 报告头 | 双坐标已 VV 互证 |
| `clinvar` | Step 0.5 分流 | 变异自身分类 / 星级 / 提交 |
| `frequency` | Step 1.2 | EAS 原始 AC/AN（仅筛；FAF95 另查 gnomAD） |
| `predictors` | PP3/BP4 | 读 `*_score` + 技能阈值自定 |
| `constraint` | PVS1/PM2 背景 | pLI / LOEUF / mis_z |
| `codon_landscape` | PS1/PM5 | 同密码子已分类变异 |
| `acmg_benchmark` | 模块 5 外部对标 | GeneBe 自动 ACMG，**仅基准，绝不覆盖专家评级** |

> **铁律**：每源独立容错，单源失败不拖垮整体；缺失即 `None`/`❌`，绝不臆造；预测只读 `*_score`；转录本锚定输入 NM；**EAS 原始 AF 仅作快速筛，BA1/BS1 的 FAF95 必须另查 gnomAD grpmax**；GeneBe 自动 ACMG 只进模块 5 对标，**不覆盖本技能专家评级**。

无网络 / 沙箱环境够不到三源时，技能会无缝回落到原生 web_search 流程。

---

## 参考知识库

### `references/ACMG_CRITERIA.md`（SNV/Indel，核心必读）

在做 ACMG 判定前必读。整合 ACMG/AMP 2015、ClinGen SVI 系列更新（PVS1 2018 / PM2 2020 / 剪接 2023）、ACGS 2024 v1.2 及产前胎儿医学专家共识。主要章节：

- **0.** 证据强度与 Bayesian 积分对照（Very Strong ±8 / Strong ±4 / Moderate ±2 / Supporting ±1）
- **1.** PVS1 四级决策树（三前提门槛、LOF 机制判定、NMD 预测、截断区重要性、起始/终止密码子、外显子缺失重复、**2023 剪接框架**、产前 PVS1 工作流）
- **2.** PM2 / BA1 / BS1 / BS2（含专病 VCEP 频率阈值、产前高频亚效单倍型陷阱 TBX6 范式）
- **3.** PS3 / BS3 功能证据 OddsPath 门槛
- **3.5** PM1 三道并列门槛 + 五问自检清单（AI 最易滥用）
- **4.** 家系与表型（PS2/PM6 de novo 双轴量化、PM3 反式、PP1 共分离、PP4）
- **5.** PS4 病例-对照
- **6.** 证据独立性、优先级、矛盾处理与冲突组合判定表
- **7–8.** 行业争议热点 + 关键产前提醒

> 标注 🤰 的条目为产前专项规则，产前模式下优先适用。

### `references/CNV_CRITERIA.md`（拷贝数变异）

ClinGen 2019/2020 五段式评分框架：初始基因组内容 → 与剂量敏感基因/良性区重叠 → 受累基因数目 → 个案与文献证据 → 遗传方式与家系。含基因内 CNV 的 PVS1 决策树复用、4O 人群频率扣分、产前 CNV 技术质控与咨询要点。

---

## 输出结构（模块 1–10）

技能按固定模块化结构输出，严格遵循双语混合规范：

| 模块 | 内容 | 语言 |
|---|---|---|
| 1 | Classification Hero（分类 / 积分 / 证据 / 置信度） | 英文标签 |
| 2 | Molecular Profile（分子信息 + 邻近变异地形） | 英文标签 |
| 3 | ACMG 证据链（已采纳 / 未采纳 / 独立性审查 / Bayesian 积分） | 全中文 |
| 4 | ClinVar 综合查询结论 | 中文 |
| 5 | External Benchmarking（VarSome / Franklin / GeneBe / InterVar） | 中文 |
| 6 | AI 判读决策报告（核心深度分析） | 中文 |
| 7 | 关联遗传病画像（OMIM / 基因型-表型） | 中文 |
| 8 | 临床可操作性建议 | 中文 |
| **8′** | **产前预后矩阵（仅产前模式，替代模块 8）** | 中文 |
| 9 | References（PMID 已反查） | 混合 |
| 10 | 局限性声明 | 中文 |

批量输入时附加汇总表（Gene / Variant / Classification / Key Evidence / gnomAD AF / REVEL）。

---

## 关键质控门控

技能内置多道"硬门控 / 软门控"，防止 AI 常见错误：

1. **蛋白改变强制验证（硬门控）** — 禁止心算推导 HGVSp；密码子微差（CGA vs CGC）可致变异类型从 nonsense 变 missense、从根本上改变评级。未验证前禁止赋 PVS1。
2. **ClinGen VCEP 全文门控（软门控）** — 有基因特异性规范时**必须取得全文并完整阅读**后才据其赋分；取不到则改用通用标准、醒目声明"初步评级"、并请求用户上传规范全文触发复核。
3. **Novel Variant 地形感知** — ClinVar 无记录 ≠ 无参照；强制三圈扩展检索建立最近已知参照点。
4. **PVS1 四级分层强制** — 绝不一刀切赋 Very Strong；先过三前提门槛，再依 NMD 决策树定强度。
5. **PM1 五问自检** — 落在某结构域 + 保守 ≠ 可赋 PM1；须过三门槛五问清单。
6. **参考文献 PMID 反查（输出前最后一关）** — 逐条反查作者 / 期刊 / 年份 / PMID，识别并更正三类典型错误（作者归属错误、PMID 数字错误、期刊缩写歧义），无法验证的虚构文献一律删除。
7. **输出前自检清单** — 蛋白验证、VCEP 门控、ClinVar 交叉、频率、预测、PVS1 适用性、积分一致性、邻近地形、产前模块、PMID 反查逐项核实。

---

## 环境依赖

| 能力 | 用途 | 必需性 |
|---|---|---|
| `web_search` / `web_fetch` | ClinVar / OMIM / ClinGen / PubMed / UniProt 检索 | 强烈建议 |
| Python 3 | 运行 `genebe_fields.py`（标准库 `urllib` 即可，无第三方依赖） | Step 0.4 建议 |
| 浏览器工具（Claude in Chrome / 内置浏览器） | GeneBe 逐项评分、SpliceAI、gnomAD SPA 页面取数 | 可选增强 |
| PubMed MCP（如已连接） | VCEP 规范全文、文献 PMID 反查 | 可选增强 |

> 无网络 / 沙箱时技能自动降级：优先请用户在有网环境跑 `genebe_fields.py` 贴回 JSON，再不行回落 web_search，**在此之前不臆造**。

---

## 使用示例

**单变异（自然语言）**
```
帮我评级 LDLR c.1183C>T
```

**深度模式（含家系 + 表型）**
```
BRCA1 p.Arg1699Trp，母源杂合，先证者及母亲均患乳腺癌，请评级并评估共分离
```

**产前模式**
```
胎儿 WES 检出 EXT2 NM_207122.2 c.1789del（父源）与 c.940-3C>G（母源）复合杂合，
超声见脊柱/肋骨发育不良、双肾小、FGR，请做致病性判断
```

**批量**
```
批量评级：
1) SCN1A c.4933C>T
2) chr19-11116839-G-A
3) DYNC1H1 p.Leu4179Ser
```

**CNV**
```
CMA 报告 arr[GRCh37] 11p11.2(44,100,000-44,300,000)x1，请分类
```

---

## 设计原则

1. **数据驱动** — 每个证据代码必须有对应数据支持，不凭推测赋值。
2. **透明度** — 检索失败 / 数据缺失必须如实标注，不伪造。
3. **保守性** — 证据不足时倾向 VUS，而非过度判定。
4. **可追溯** — 每步数据来源可追溯（URL / PMID / 数据库版本）。
5. **基因特异性优先** — VCEP 规则优先于通用标准，且"知道有规则 ≠ 可套用"，须取得全文。
6. **禁止推导关键注释** — HGVSp / 变异类型 / 坐标必须经外部工具验证。
7. **参考文献零容忍** — 虚构或错误归属的引文不可接受。
8. **三源优先但不越权** — GeneBe 自动 ACMG 仅对标，绝不覆盖专家评级；频率精判归 gnomAD FAF95。

---

## 局限性与免责声明

- 本技能由 **AI 辅助生成**，所有结论**必须**经认证临床遗传学家 / 遗传咨询师审核确认后方可用于临床决策。
- 数据库（ClinVar / gnomAD 等）持续更新，关键决策前请**实时查询最新版本**。
- 标注 ⚠️ / ❌ 的检索项未能完整获取，相关证据评估可能受影响。
- 本技能**不构成医疗诊断或治疗建议**，具体临床决策请结合完整病史与多学科讨论。

---

## 数据来源与致谢

本技能整合以下公共资源的公开数据与指南（版权归各自所有者）：

- **ACMG/AMP 2015** 变异解读指南
- **ClinGen** Sequence Variant Interpretation（SVI）系列更新、Gene-Disease Validity、Dosage Sensitivity、VCEP Criteria Specifications
- **ACGS 2024 v1.2** Best Practice Guidelines
- **ClinVar**（NCBI）、**gnomAD**（Broad Institute）、**OMIM**、**UniProt**、**DECIPHER**
- **VariantValidator**、**GeneBe**、**SpliceAI**、**REVEL**、**AlphaMissense**、**dbNSFP**、**dbscSNV**
- 产前胎儿医学专家共识备课会（2026）实操意见

---

## 版本历史

| 版本 | 时间 | 说明 |
|---|---|---|
| `+GeneBe 三源集成` | 2026-07 | 引入 Step 0.4 三源结构化取数引擎（VariantValidator + GeneBe + 五源 Worker） |

---

> 如需修改 License、贡献指南（CONTRIBUTING）或问题模板（issue template），请根据你的仓库政策自行补充。
