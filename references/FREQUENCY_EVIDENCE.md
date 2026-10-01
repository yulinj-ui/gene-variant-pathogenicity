# 频率相关证据（PM2 / BA1 / BS1 / BS2，及 PS4 / PM3 的频率前提）：规则与落地流程

> 版本：v2 草案，2026-09-29，Mac mini 起草，尚未并入 skill。
> 依据：潘丹丹《群体频率和计算证据介绍》（2026-09-04 讲座）、ACMG/AMP 2015、ClinGen SVI BA1 更新（Ghosh 2018，PMID 30311383）、SVI PM2 v1.0（2020-09-04）、Whiffin 2017（PMID 28518168）、ACGS 2024、gnomAD 官方帮助文档（FAF / grpmax / AC0 / 覆盖度），以及 ClinGen CSpec 各 VCEP 规范。
> 配套脚本：`freq_evidence.py`（同目录）。本文所有"实测"数据都在 2026-09-28/29 用该脚本或 curl 实际跑过。

---

## 0. 为什么还要再做一版

2026-09-28 的 CUL7 事故已经修掉了最直接的错误：取数失败被当成"不存在"，进而赋了 PM2_Supporting。Step 0.45 引入了三态门控，`NOT_QUERIED` 时不能赋 PM2。这次研究在同一条链上又找到三处漏洞，都能让流程**在查询"成功"的情况下**得出假的"确无"。

| # | 漏洞 | 实测复现（v1 脚本 `freq_repeat_lookup.py`） | 真实情况 |
|---|---|---|---|
| A | **indel 未左对齐 / 等价写法** | `6-43040322-CTCC-C` → `ABSENT_CONFIRMED`，门控"可赋 PM2_Supporting" | 与 `6-43040321-TCTC-T` 是同一变异，AC=77，EAS FAF95=6.3×10⁻⁴ |
| B | **REF 与参考基因组不符**（坐标写错，或把 hg19 当 hg38） | `17-43045712-C-GGG`（该处 REF 实为 T）→ `ABSENT_CONFIRMED`，"可赋 PM2" | 坐标本身无效 |
| C | **gnomAD GraphQL 是唯一来源** | 接口一挂，所有频率证据都"无法评估"，结论扣留 | gnomAD 公共存储桶的静态 VCF 可以作为独立的第二来源 |
| D | **自动评级工具的 PM2 被当成事实** | GeneBe 对 CUL7 c.4126_4128del 给出 `PM2_Supporting` | AC=77 |

另外两点结论会影响日常判读：
- **VCEP 阈值不能机械套用。** 例如 GJB2 c.35delG 的 NFE FAF95 为 0.81%，c.235delC 的 EAS FAF95 为 0.60%，两者都超过听力 VCEP 的 BA1 阈值（隐性 ≥0.5%），但都是公认的致病奠基者变异。
- **同一变异，VCEP 与通用规则的结论可以相反。** LDLR c.1187-10G>A 的 AC=20。按通用 AD 规则（要求 AC=0），PM2 不能赋。FH VCEP 的规定是 PopMax MAF ≤0.0002 即给 **PM2（Moderate）**，所以按 VCEP 反而能赋。

---

## 1. 规则层

### 1.1 统一数据口径（全流程只用这一套）

| 项目 | 规定 |
|---|---|
| 主库 | **gnomAD v4.1 joint**（外显子 + 基因组合并，GRCh38，807,162 人）。v2.1.1 只作补充（例如 EAS 亚群 KOR/JPN/OEA），不作判据 |
| 坐标 | **只接受经工具归一化的 GRCh38 左对齐 VCF**。来源依次为：HGVS → ClinGen Allele Registry（CAR）→ 本地左对齐。**禁止心算坐标** |
| "人群频率"指哪个数 | **BA1 / BS1 用 grpmax FAF95**（95% 置信下限，对良性结论保守）。**PM2 用 grpmax AF 点估计**（对致病结论保守）。有 VCEP 时按其规定的指标（有的用 PopMax MAF，有的用 FAF） |
| grpmax 包含的人群 | afr / amr / eas / mid / nfe / sas。**不含**瓶颈人群 ami / asj / fin / remaining（gnomAD 官方定义；genome 数据另不含 mid）。瓶颈人群高频只作参考，不触发 BA1/BS1 |
| 最小样本 | BA1/BS1 所用人群 AN ≥ 2000（SVI 2018）。v2 的 KOR（AN≈3,800）、JPN（AN≈150）之类的小亚群**不能单独触发 BA1** |
| 质控 | 只用两个数据集（exome/genome）中**至少一个 PASS** 的频率。全部未通过质控（包括 AC0、RF、InbreedingCoeff 等）→ `FOUND_FILTERED`：既不是"缺失"，也不作良性证据 |
| 版本 | 报告写明"gnomAD v4.1 joint，查询日期"。文献中"absent in gnomAD"的说法**不能代替实时查询** |

### 1.2 PM2（SVI 2020：默认 PM2_Supporting）

SVI v1.0 原文只做了两件事：①把 PM2 从 Moderate 降为 Supporting；②新增组合规则 "1 条 Very Strong + 1 条 Supporting = LP"，使 PVS1 + PM2_Supporting 的新 LOF 变异仍可评为 LP。**原文没有给频率阈值**，操作层面的规则来自 VCEP 和本节。

**判定树**（先查 VCEP，没有 VCEP 才走通用规则）：

```
gnomAD 状态 ─┬─ NOT_QUERIED / INVALID_INPUT / CONFLICT /
             │  REPRESENTATION_MISMATCH / ABSENT_COVERAGE_UNVERIFIED → ⛔ 无法评估，不赋，扣留结论
             ├─ ABSENT_LOW_COVERAGE  → ⛔ 不赋（位点覆盖不足）
             ├─ FOUND_FILTERED       → ⛔ 不自动赋；人工看 AB/DP；AC0 须注明
             ├─ ABSENT_CONFIRMED     → ✅ PM2_Supporting（VCEP 可升/降）
             └─ FOUND（PASS）
                  ├─ 有 VCEP → 按 CSpec 原文阈值（脚本自动拉取）
                  ├─ AD / XLD：默认要求 AC=0；AC>0 → 不赋
                  │    例外：迟发或外显不全疾病，按 Whiffin 计算 AD 最大可信 AF，
                  │    grpmax AF 低于该值时可赋，须在模块3 写出参数与计算过程
                  ├─ AR：grpmax AF < PM2 上限（"典型参数"计算）→ PM2_Supporting
                  │    grpmax FAF95 > BS1 下限（"最大参数"计算）→ BS1
                  │    介于两者之间 → 两条都不赋，写出计算
                  └─ XLR：用 XY（半合子）频率与男性患病率计算
```

**PM2 上限与 BS1 下限要用两组不同的参数**（ACADVL VCEP 就是这样做的，已从 CSpec 核实）：
- PM2 上限代表"一个典型致病等位该有的频率"：患病率取点估计，等位贡献取典型值（ACADVL 用 1:100,000、0.2、外显率 0.75，再 ×1.5 → **<0.001**）。
- BS1 下限代表"任何单一致病等位都不可能超过的频率"：患病率取上限，等位贡献取最大值（ACADVL 用 1:30,000、0.5、外显率 0.75 → **≥0.0035**）。BA1 用等位贡献 1 → **≥0.007**。

**其他注意**：
- 大缺失/重复（≥50 bp、外显子级）：查 gnomAD SV v4.1 / gnomAD exome CNV / DGV，不能用 SNV 频率。
- 产前特有的陷阱：**PP3_Strong + PM2_Supporting = 5 分 = VUS**。计算预测不能把新发错义变异抬到 LP（讲座第 30 页）。
- PM2 与 PS4 不得共用同一对照队列。

### 1.3 BA1

- 规则（Ghosh 2018 原文）：任一 AN ≥ 2000 的大陆人群中 AF > 0.05，且该基因/变异没有 BA1 修订 → 独立良性。
- **豁免名单**（Ghosh 2018 Table 1，已核实；ClinGen 在线维护，使用前以最新版为准）：
  ACAD9 c.-44_-41dup；ACADS c.511C>T（p.Arg171Trp）；BTD c.1330G>C（p.Asp444His）；GJB2 c.109G>A（p.Val37Ile）；HFE c.187C>G（p.His63Asp）；HFE c.845G>A（p.Cys282Tyr）；MEFV c.1105C>T（p.Pro369Ser）；MEFV c.1223G>A（p.Arg408Gln）；PIBF1 c.1214G>A（p.Arg405Gln）。
- **VCEP 的 BA1 阈值往往远低于 5%**（听力隐性 0.5%、FH 0.5%、ACADVL 0.7%），这时撞上奠基者致病变异的概率高得多。**BA1/BS1 触发 + ClinVar P/LP ≥2 星 → 强制冲突复核**：查 VCEP 规范的例外说明、VCEP 自己的 ClinVar 评级，并考虑亚效等位（沿用 skill 现有 §2.2 的 OCA2 / TBX6 规则）。实测例子：GJB2 c.35delG（NFE FAF95 0.81%）、c.235delC（EAS FAF95 0.60%）。

### 1.4 BS1

- 优先级：**VCEP 阈值 > 按 Whiffin 计算 > 不赋**。没有阈值时，不能凭"感觉频率偏高"赋 BS1（缺数据对称原则）。
- Whiffin 公式（AD 形式已从原文核实，HCM 例：1/500 ÷ 2 × 0.02 ÷ 0.5 = 4.0×10⁻⁵）：
  - AD / XLD：`maxAF = (患病率 / 2) × 最大等位贡献 × 遗传贡献 / 外显率`
  - AR：`maxAF = √患病率 × 最大等位贡献 × √遗传贡献 / √外显率`
  - 最大容许 AC：Poisson 95% 上界，λ = AN × maxAF（原文例：AF 1e-4、AN 100,000 → ≤15）
- 比较对象：**grpmax FAF95 > maxAF → BS1**。
- 参数来源须在报告中写明，例如患病率取自 Orphanet/GeneReviews 并注明区间，等位贡献依据该基因最常见致病等位在患者中的占比。

### 1.5 BS2（gnomAD 作"健康个体"来源）

- gnomAD 个体**没有做表型评估**，只是"未知有无重症儿科疾病"的成年人群。gnomAD 纯合/半合只能作为 BS2 的**线索**，并且要同时满足：疾病早发、完全外显、属于重症；≥2 例（ACGS 2024）；排除亚效等位；非 CHIP 基因（见 1.8）。
- 产前默认最多作 **BS2_Supporting** 参考，除非 VCEP 另有规定。例如 FH VCEP 的 BS2 要求"≥3 名表型明确、未治疗、血脂正常的成人杂合子"，gnomAD 不满足。
- 家系亲代作为 BS2 来源时，沿用 skill 现有 §2.3 的四条 SOP。

### 1.6 PS4 / PM3 的频率前提

- PS4（病例计数法、AD）与 PM3（AR）都以"变异本身罕见（满足 PM2）"为前提。PM2 = `NOT_QUERIED` 时，PS4 计数法和 PM3 的 0.5 分档（"两个都满足 PM2 的变异反式"）同样无法评估。
- PS4 病例-对照：gnomAD 可以作对照，用 cardiodb 的 case-control 工具或 Fisher 检验，但对照须与病例祖源匹配。讲座示例：MYBPC3 p.Arg502Trp，病例 159/20800 vs gnomAD 87/584196。
- 自身频率高的常见隐性致病变异（如 GJB2 V37I）走 PS4 的**基因型**富集，PM3 封顶（沿用现有规则）。

### 1.7 中国/东亚人群

| 来源 | 规模 | 能否程序化 | 用法 |
|---|---|---|---|
| gnomAD v4.1 joint EAS | AN≈44,850（约 2.2 万人） | ✅ GraphQL / tabix | 主判据。注意：EAS 中 AC=0 的统计效力有限，"EAS 未见" ≠ "中国人罕见" |
| gnomAD v2.1.1 EAS 亚群 KOR/JPN/OEA | 小 | ✅ myvariant.info | 只作参考，不单独触发 BA1 |
| dbSNP 各研究（TOMMO 日本 ~77k、Korea4K、KOREAN、Vietnamese、部分位点有 ChinaMAP） | 中 | ✅ NCBI Variation API（需 rsID） | 东亚交叉核对。脚本自动列出 |
| ChinaMAP（10,588 WGS） | 中 | ❌ 需登录（chinamapwgs.mbiobank.com/search/?searchContent=…） | 用户自行登录后，用 Claude in Chrome 读取 |
| CMDB（CNGBdb 百万中国人） | 大（低深度） | ❌ 2026-09-29 实测页面已不存在 | 暂不可用 |
| WBBC（西湖） | 4,480 WGS | ❌ 站点改版，未见检索入口 | 暂不可用 |
| 本实验室 / 本院数据库 | — | 视情况 | 按 skill 现有规则标 `Local cohort evidence (unpublished)`；本地频率高于 gnomAD EAS 时优先用于 BS1 |

**中国人群已知的高频致病/亚效等位（不能被"频率高"一票否决）**：GJB2 c.235delC、c.109G>A；SLC26A4 c.919-2A>G；TBX6 T-C-A 亚效单倍型（讲座第 22–24 页）。

### 1.8 特殊情形

- **CHIP 基因**（DNMT3A、TET2、ASXL1、TP53、JAK2、PPM1D 等）：gnomAD 携带者可能是克隆性造血，AB 偏低。这类频率既不能直接作 BS1/BS2，也不能反推"真实罕见"。
- **低复杂度 / 片段重复 / 假基因区**：gnomAD 会标 `lcr` / `segdup` flag。沿用现有 §2.5b，分类封顶 VUS 并加 `Mappability caveat`。
- **线粒体**：用 gnomAD mtDNA（按同质性/异质性分别计数）+ MITOMAP + HelixMTdb，阈值以线粒体 VCEP 为准。本脚本**不支持 MT**。
- **X 连锁**：看 XY 半合子计数与 XY AF；AN 本身比常染色体低，覆盖度代理（见 3.2）对 X/Y 不启用。
- **重复扩展 / STR**：不适用本框架。

---

## 2. 状态机（替代 Step 0.45 的三态表）

| 状态 | 触发条件 | 允许的报告措辞 | PM2 | BA1/BS1/BS2 |
|---|---|---|---|---|
| `FOUND` | 查到，且至少一个数据集 PASS | 写 AC/AN、grpmax AF、FAF95（人群）、hom/hemi、来源 | 按 §1.2 | 按 §1.3–1.5 |
| `FOUND_FILTERED` | 查到，但所有数据集都未通过质控 | "gnomAD 有记录但未通过质控（{filters}）" | ⛔ 人工 | ⛔ |
| `ABSENT_CONFIRMED` | 未查到 + REF 已核对 + 已归一化 + 窗口内无等价记录 + CAR 无 gnomAD_4 链接 + 覆盖充分（≥20× 样本 ≥90%，或邻近 AN ≥ 满 AN 的 80%） | "gnomAD v4.1 未收录（位点覆盖充分）" | ✅ Supporting | 不满足 |
| `ABSENT_LOW_COVERAGE` | 未查到，覆盖不足 | "未收录但覆盖不足，不能视为人群缺失" | ⛔ | 不适用 |
| `ABSENT_COVERAGE_UNVERIFIED` | 未查到，覆盖度与代理都取不到 | "未收录，覆盖度未能核实" | ⛔ | ⛔ |
| `REPRESENTATION_MISMATCH` | 查询写法未命中，但窗口内有等价记录 | 必须改用等价记录重查 | ⛔ | ⛔ |
| `CONFLICT` | 本次未命中，但 CAR 显示 gnomAD_4 已收录 | "来源矛盾，未能确认" | ⛔ | ⛔ |
| `INVALID_INPUT` | REF 不符 / HGVS 无法解析 | "输入坐标无效" | ⛔ 扣留 | ⛔ |
| `NOT_QUERIED` | 所有来源都失败 | "**未能查询**"（禁止写"未检出 / novel / 极罕见 / AF=0"） | ⛔ 扣留 | ⛔ |

---

## 3. 落地路径（按运行环境）

### 3.1 取数阶梯

```
输入（HGVS c./g. 或 VCF 坐标）
  │
  ├─①  归一化 + 校验
  │     HGVS → ClinGen Allele Registry（reg.genome.network/allele?hgvs=…）
  │           得到 CA ID、GRCh38 坐标、gnomAD_4 ID（若 gnomAD 收录）
  │     VCF  → UCSC 参考序列核对 REF → 本地左对齐 → 再交 CAR 交叉核对
  │
  ├─②  gnomAD v4.1 取数（任一成功即可）
  │     a. GraphQL  gnomad.broadinstitute.org/api
  │     b. 远程 tabix  GCS  storage.googleapis.com/gcp-public-data--gnomad/release/4.1/vcf/joint/…
  │     c. 远程 tabix  AWS  gnomad-public-us-east-1.s3.amazonaws.com/release/4.1/vcf/joint/…
  │     （b/c 是官方静态文件，按字节区间读取，无需 htslib，也没有 API 限流）
  │
  ├─③  防假阴性
  │     ±60 bp 窗口扫描：等价写法 / 同位点其他等位 / 重叠 indel
  │     CAR gnomAD_4 链接与本次结果交叉核对
  │     覆盖度：GraphQL coverage → 失败则用邻近变异 AN 作代理
  │
  ├─④  VCEP 规范：CSpec API（cspec.genome.network/cspec/api/svis?detail=high）
  │     自动输出该基因的 PM2/BA1/BS1/BS2/PS4/PM3 原文
  │
  ├─⑤  东亚补充：dbSNP 研究频率（TOMMO / Korea4K / ChinaMAP …）
  │
  └─⑥  阈值计算（Whiffin）与门控输出 → 写入模块3"数据依据"
```

### 3.2 各环境的执行方法

**A. Claude Code（本机，首选）**
```bash
python3 references/freq_evidence.py --hgvs "{NM_…:c.…}" --gene {基因} --moi {AD|AR|XLD|XLR} \
        [--prevalence 1/N --allelic x --genetic y --penetrance z] --card
```
- 退出码 0 = 可用；2 = 输入无效；3 = gnomAD 未能查询（此时模块1 扣留结论）。
- 优先用 `--hgvs` 输入，让 CAR 解析坐标，这样从根上避免心算坐标和 indel 位置写错。

**B. 网页 / 手机 App（跑不了脚本）**
1. CAR 网页：`https://reg.genome.network/allele?hgvs={HGVS}`（返回 JSON，可直接 web_fetch），取 `externalRecords.gnomAD_4[0].id`。
   - **有 ID**：说明 gnomAD 已收录，禁止写"未检出"。
   - **没有 ID**：只说明"CAR 未链接到 gnomAD"，还要做第 2 步才能下结论。
2. 用浏览器（Claude in Chrome / 内置浏览器）打开 `https://gnomad.broadinstitute.org/variant/{gnomAD_4 ID 或归一化坐标}?dataset=gnomad_r4`，读取 GroupMax FAF、各人群表、Filters、纯合/半合计数。未收录时，改用区域页 `…/region/{chr}-{pos-20}-{pos+20}?dataset=gnomad_r4` 看覆盖度曲线。
3. VCEP：`https://cspec.genome.network/cspec/ui/svi/` 按基因检索，读 PM2/BA1/BS1 全文。
4. 以上都做不到时 → `NOT_QUERIED`，扣留结论，请用户在 Claude Code 里运行脚本并把卡片贴回。
5. ⛔ **web_search 摘要、GeneBe/Franklin 的自动 PM2 标签都不能作为频率判据**。它们给出的频率数值可以写进模块5 作对标。

**C. 辅助来源的定位**

| 来源 | 实测（2026-09-28） | 定位 |
|---|---|---|
| gnomAD GraphQL | ✅ 约 1 s；连续 20 次无限流 | 主来源 |
| gnomAD 远程 tabix（GCS / AWS） | ✅ 约 3–5 s；GraphQL 故障演练中成功接管，数值与 GraphQL 一致（AC=77，FAF95=6.34×10⁻⁴） | 第二来源（新增） |
| ClinGen Allele Registry | ✅ 约 2 s；HGVS→坐标→gnomAD_4 ID | 归一化 + 交叉核对（新增） |
| ClinGen CSpec API | ✅ 208 份规范 / 192 个基因（其中 Released 123 份） | VCEP 原文（新增） |
| NCBI Variation API | ✅ | 东亚研究频率（新增） |
| myvariant.info | ✅ 但只有 gnomAD v2 exome / v3 genome，没有 v4 | 仅作 v2 EAS 亚群参考 |
| Ensembl VEP REST | ✅ 可用 | 只有 AF，没有 AC/AN/FAF，不作判据 |
| GeneBe API | ✅ 数据通，但**自动 PM2 在 AC=77 时仍给 PM2_Supporting** | 只作对标 |
| gnomAD 网页 web_fetch | ❌ SPA 空壳 | 禁用；浏览器渲染后可读 |

---

## 4. 报告写法（模块3 每条频率证据的"数据依据"行）

```
PM2_Supporting — gnomAD v4.1 joint 未收录（freq_evidence: ABSENT_CONFIRMED；CA{…}；
  REF 已核对、已左对齐、±60bp 无等价记录；位点 ≥20× 样本比例 外显子 100% / 基因组 97%；查询 2026-09-29）
BS1 — grpmax FAF95 = 6.34×10⁻⁴（EAS，AC 38/AN 44,850）> 最大可信 AF 5.0×10⁻⁴
  （AR；患病率 1/1,000,000 [来源]、等位贡献 0.5、遗传贡献 1、外显率 1）
PM2 — 不赋：gnomAD 未能查询（GraphQL 与 tabix 均失败）。频率证据无法评估，结论扣留。
```

---

## 5. 回归测试集（每次改脚本后跑一遍）

| 输入 | 期望 | 2026-09-29 实测 |
|---|---|---|
| `--hgvs NM_014780.5:c.4126_4128del` | FOUND，AC=77，EAS FAF95 6.34e-4 | ✅ |
| `6-43040322-CTCC-C`（非左对齐） | 自动纠正为 6-43040321-TCTC-T → FOUND | ✅（v1 给出 ABSENT_CONFIRMED ✗） |
| `17-43045712-C-GGG`（REF 错误） | INVALID_INPUT，退出码 2 | ✅（v1 给出 ABSENT_CONFIRMED ✗） |
| `6-43040321-T-A` | ABSENT_CONFIRMED（覆盖 100%/97%） | ✅ |
| GraphQL 故障（`GNOMAD_API=…/api-DOWN`）+ CUL7 | tabix 接管，FOUND，数值一致 | ✅ |
| GraphQL 故障 + `6-43040321-T-A` | ABSENT_CONFIRMED（邻近 AN 代理 99.99%） | ✅ |
| `X-153724000-A-C` | FOUND_FILTERED（exome AC0） | ✅ |
| `--hgvs NM_004004.6:c.109G>A --gene GJB2` | 命中 BA1 豁免；拉取听力 VCEP 原文；hom=101 | ✅ |
| `--hgvs NM_000527.5:c.1187-10G>A --gene LDLR` | AC=20；通用 AD 规则不赋 PM2；FH VCEP 规定 PM2(Moderate) ≤0.0002 | ✅ |
| GJB2 c.35del / c.35dup / c.235del | 由 CAR 归一化后均为 FOUND | ✅ |

---

## 6. 已定事项（2026-09-29 用户确认）

1. ✅ **PM2 用 grpmax AF 点估计**，BA1/BS1 用 grpmax FAF95。这取代现行 skill 中隐性病 PM2 用 FAF95 的做法。
2. ✅ **FOUND_FILTERED（所有数据集都未通过质控，含 AC0）一律不自动赋 PM2**，改为人工判断，并在报告中写明 filters。
3. ✅ **gnomAD 纯合/半合作 BS2 时，产前默认封顶 BS2_Supporting**（VCEP 另有规定的除外）。
4. ✅ **ChinaMAP 作补充来源**：用户在自己的 Chrome 中登录，由 Claude in Chrome 读取。规则见 §7。

## 7. ChinaMAP 使用规则

- **数据范围**（官方帮助页已核实）：phase1，10,588 例约 40× WGS，GRCh38；**只有常染色体**，**不含 LCR 区变异和低质量被过滤的变异**；结果表有 AC/AN。
- **"ChinaMAP 未见"只能作为弱信息，不能单独支持 PM2**：X 连锁基因根本查不到；重复区和低复杂度区的 indel（例如 CUL7 那种 `(TCC)n` 内缺失）会因为 LCR 过滤而假阴性。
- **ChinaMAP 有记录**：频率可作为中国人群参考写进模块4/5；其 AF 高于 gnomAD EAS 时，可用于 BS1 的补充论证（样本量约 2.1 万等位，须满足 AN ≥ 2000）。
- **只作补充，不作门控**：ChinaMAP 读取失败（登录过期、站点不可达、页面改版）时记 `NOT_QUERIED(ChinaMAP)`，不扣留结论、不影响 PM2 判定。PM2 的判据仍然只来自 gnomAD（§2）。
- **登录由用户完成**，Claude 不输入账号密码、不做验证码。检索 URL：`http://chinamapwgs.mbiobank.com/search/?searchContent={坐标/rsID/基因}`。
- **合规**：该库条款限定"学术研究、非商业用途"，禁止与第三方数据库关联、禁止转发数据，并要求遵守人类遗传资源管理规定。用于临床报告前，须先向本单位或 support@mbiobank.com 确认；报告中只引用单个位点的频率，不做批量抓取。
