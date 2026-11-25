---
name: gene-variant-pathogenicity
description: 对已检出的胚系 SNV、Indel 和组成型 CNV 做致病性解读：整理证据、按 ACMG/AMP 2015 + ClinGen SVI + ACGS 2024（及适用 VCEP）分级、生成中文十模块报告，支持家系、产前和批量场景。含 gnomAD 频率九态门控、PM2/BA1/BS1/BS2 阈值、PM4/BP3 重复区核查、本地 dbNSFP 5.4a 预测分与 CNV 五段评分。用于变异解读、外院报告独立辅助复核、ACMG/CNV 分级复核或数据库分类对比；不用于从测序原始数据检出变异，不替代实验室签发。
metadata:
  version: 0.8.2-local
  upstream: gene-variant-pathogenicity 2026-10-09
  upstream_commit: 83c2617fda
---

<!-- 版本: v0.8.2-local 2026-11-24（exon 两源核对工具）；上一版 v0.8.1-local 2026-11-19。在上游 2026-10-09 包基础上并入本机 v7 审核/报告层：
     频率九态门控、PM2/BA1/BS1/BS2 阈值、VCEP 频率阈值自动拉取、PM4/BP3 重复区强制核查、本地 dbNSFP 5.4a，
     以及 v7 的 PVS1/PM3/功能/家系/CNV Section2 审核引擎与十模块报告。 -->

# 遗传变异致病性解读：外院报告辅助复核（本地版）

## 1. 角色与默认模式

你是执行变异解读的遗传学分析者：一次完成必要的检索、证据判断、分级和中文报告，同时把"分析结论"与"实验室签发"分开。

默认模式是**外院报告的一次性独立辅助复核**（[自主复核规范](references/AUTONOMOUS_ASSIST.md)）：由 DeepSeek Harness 自主完成公开证据的判断并留痕，不要求用户逐项填审核清单，不以"联系不到外院、没有人工签字、缺 BAM"阻断整例。用户明确要求逐项人工审阅时才走严格模式。

- 交付：本次独立辅助评级（`independent_classification`）、证据链、积分与 2015 组合对照、外院评级差异、表型相关性、关键局限。
- `clinical_signoff` 始终为空：辅助分级不等于实验室签发。审核署名只能是 `DeepSeek Harness (autonomous evidence review)`，不得冒充用户、医师或实验室审核人。
- 公开证据能判断的由你判断；外院明确陈述的事实标 `external_report_explicit`，不虚构原始验证；查不到的数据写"未查询/未获取"，不写"阴性"。

**规则优先级**（本例必须在报告开头声明）：适用疾病/遗传模式的已发布 VCEP 定制标准 > 其明确继承的通用 ACMG/SVI 条款 > 本技能参考文件 > 实验室政策/课件（须人工确认后启用）。不同来源的片段不得无说明混算。

## 2. 版本与来源（上游同步）

| 项 | 值 |
|---|---|
| 本包版本 | `0.8.2-local`（2026-11-24） |
| 上游基线 | `gene-variant-pathogenicity` 2026-10-09 包（GitHub `claude/update-from-local-2026-10-09`，PR #3，commit `83c2617fda`） |
| 上游副本 | [`upstream-2026-10-09/`](upstream-2026-10-09/PROVENANCE.md)：逐字节档案 + SHA256 |
| 历史档案 | `original/` 为 2026-09-28 版，只作追溯；其"必须/禁止"、数值阈值与工具名不自动生效 |
| 同步说明 | [`references/UPSTREAM_SYNC.md`](references/UPSTREAM_SYNC.md) |

上游发布新版本时：整包替换 `upstream-2026-10-09/`（或新建日期目录），同步 `references/ACMG_CRITERIA.md`、`references/FREQUENCY_EVIDENCE.md` 与 `references/CNV_CRITERIA_UPSTREAM.md`，在 `references/UPSTREAM_SYNC.md` 登记哈希与差异，再重跑 `tests/`。

## 3. 运行环境（本机）

根目录为本文件所在目录，**脚本路径一律相对本技能根目录解析**，不相对用户当前目录。Python 3.10+，只用标准库。

| 资源 | 本机位置/说明 |
|---|---|
| Python | `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`（3.13.7 已验证） |
| tabix | `/Users/peter/miniforge3/envs/trio/bin/tabix`（不在 PATH 时设 `TABIX_BIN`） |
| dbNSFP 5.4a（GRCh38） | `/Volumes/T9/genomics/refs/annot/dbNSFP/5.4a/dbNSFP5.4a_grch38.gz` + `.tbi`（57 GB，T9 需挂载） |
| 本地 gnomAD r3.0 genomes | `/Volumes/T9/genomics/refs/GRCh38/gnomad.hg38.genomes.v3.fix.zip`（slivar 派生库，见 [LOCAL_T9](references/LOCAL_T9.md)） |
| 网络 | VariantValidator、GeneBe、gnomAD API、ClinGen Allele Registry、CSpec、UCSC、NCBI 均需联网 |

可选环境变量：

| 变量 | 作用 |
|---|---|
| `GENEBE_KEY`（+`GENEBE_EMAIL`） | GeneBe Basic Auth，避免 429；格式 `email:apikey`，用授权账号 |
| `DBNSFP54_TABIX` | 覆盖 dbNSFP 5.4a 的 `.gz` 路径（同目录需 `.tbi`） |
| `TABIX_BIN` | tabix 路径 |
| `NCBI_KEY` | 稳定 ClinVar/PubMed 查询 |
| `GNOMAD_API` | 仅测试回退用；不设则用官方地址 |

数据边界：对外只发送 HGVS/坐标/基因名，不发送患者姓名、病历号、家系成员身份；病例记录、原始响应与报告写入当前病例目录，不写入 T9。

本机 Python 为 python.org 框架构建，默认不带根证书：`scripts/source_http.py` 会优先加载 `certifi` 或系统 CA 包，`freq_evidence.py` 自带 curl 通道。仍报 `CERTIFICATE_VERIFY_FAILED` 时设 `SSL_CERT_FILE`，或改用 curl 取数并在报告注明。

耗时基线（本机）：`freq_evidence.py` 约 20–60 s；`genebe_fields.py --online` 约 1.5–2 min（大头是 57 GB dbNSFP 的 tabix 头解析）。

离线自检：`python3 -m unittest discover -s tests`（445 项，约 1 s，全部合成数据）。

## 4. 执行顺序（总览）

1. **Step 0** 输入解析、转录本与蛋白强制验证。
2. **Step 0.4** 三源结构化取数（VariantValidator/GeneBe/Worker）；**0.4b** 本地 dbNSFP 5.4a。
3. **Step 0.45** 频率/ClinVar/重复区结构化取数（强制门控，不可跳过）。
4. **Step 0.5–0.7** ClinVar 分流、邻近位点扩圈、产前预后检索。
5. **Step 1–4A** 数据库检索、分子定位、外部分类对标、功能预测、PVS1、VCEP。
6. **Step 5** 家系整合。
7. **ACMG 判定引擎**：证据代码 → 互斥/上限检查 → 积分 + 2015 组合 → 分级。
8. **Step 6 / 9-Verify**：VUS 报告取舍、PMID 反查。
9. 输出十模块报告；需要可核算留痕时走第 12 节管线。

缺 build、转录本版本、CNV 断点或蛋白反向映射不唯一时：列出缺口，先做不依赖它的工作，不因单项缺失停工。

## 5. Step 0：输入解析与蛋白强制验证

支持的输入：HGVS（转录本+cDNA / 基因+cDNA）、基因+蛋白、VCF 坐标、rsID、CNV 区间、自然语言描述。

> 输入格式示例只示格式，**等位基因本身由工具核对**。例：`NM_000527.5:c.1183C>T` 与当前参考不符（该位点 REF=G，ClinGen Allele Registry 报 `IncorrectReferenceAllele`），正确写法如 `NM_000527.5:c.1183G>A`（p.Val395Met）。

**蛋白改变强制验证门（MANDATORY）**：变异类型（missense/nonsense/synonymous/剪接）完全取决于验证后的蛋白改变，不可提前假设；蛋白未验证时**禁止赋 PVS1**。优先级：VariantValidator 与 GeneBe 双源一致（`protein_gate.passed`）> 单源经参考序列校验（`single_source`，可用于后果复核）> 冲突（不下结论）> 未解决（分流）。

转录本优先级：MANE Select > MANE Plus Clinical > RefSeq canonical。用户给的转录本与 MANE 不同时，给出两套命名对照，主分析用 MANE 并注明原始转录本。临床相关转录本可以不是 MANE，须写明选择依据。

## 6. Step 0.4：三源结构化取数

```bash
python3 scripts/genebe_fields.py "NM_017780.4:c.2831G>A" --online --card
python3 scripts/genebe_fields.py "NM_017780.4:c.2831G>A" --fixture tests/fixtures/xxx.json   # 离线回归
```

输出 `EV` 证据池，`EV._sources` 逐源给出状态；`--raw` 保留原始响应。字段用途：

| 键 | 用途 |
|---|---|
| `protein_gate` | Step 0 过门（transcript/hgvs_c/hgvs_p、身份与交叉校验状态） |
| `coords` | hg38/hg19/rsID，报告头与坐标核对 |
| `clinvar` | 分类/星级/提交摘要（Step 0.5 分流） |
| `frequency` | gnomAD 全局与 EAS 原始 AC/AN，仅作"是否常见"快速筛 |
| `predictors` | CADD/REVEL/phyloP/SIFT/PolyPhen/MetaSVM/SpliceAI + GeneBe 补 AlphaMissense/BayesDel |
| `dbnsfp54` | 本地 5.4a 原始归并值（含 `*_pred` 与 gnomAD4.1 joint 频率）；`found=false` = 库内无此等位 |
| `constraint` | pLI/LOEUF/mis_z/oe_mis |
| `codon_landscape` | 同密码子已分类变异（PS1/PM5 线索；空 ≠ 良性） |
| `acmg_benchmark` | GeneBe 自动 ACMG，只进模块 5 对标 |

Worker 没有默认地址：需要五源合并时显式 `--worker https://<trusted-host>`；不配置就跳过，不用未经验证的服务补数。

**必守 caveat**

1. 频率精判归 Step 0.45 的 `freq_evidence.py`；`EV.frequency` 的原始 AF 不是 PM2/BA1/BS1 判据。
2. GeneBe 自动标签（含 PM2_Supporting/BA1）不采信：反例 CUL7 c.4126_4128del（gnomAD AC=77，GeneBe 仍给 PM2_Supporting）。
3. 预测读 `value` 分数，按本技能阈值定 PP3/BP4，不读 `_prediction` 字符串。
4. 转录本以 `protein_gate.transcript`（RefSeq NM）为准。
5. `None`/`❌` 照标，不猜；单源失败时该源相关证据回落检索，不编造数值。

### 6.1 Step 0.4b：本地 dbNSFP 5.4a（2026-10-09 接入）

- hg38 坐标解析后，`genebe_fields.py` 对 T9 上 dbNSFP 5.4a 做 tabix 查询（完全本地、无外发）。`_sources.dbnsfp54_local = ok` 即生效；`unavailable` 表示 T9 未挂载/无 tabix，已回落在线值——报告须注明"预测分来自在线源，非本地 5.4a"。
- 命中时 `REVEL / ALPHAMISSENSE / BAYESDEL_NOAF / METARNN / PRIMATEAI / VARITY_R / ESM1B / CADD_PHRED` 以 `source="dbNSFP5.4a(local)"` 覆盖在线值；**SIFT/PolyPhen 不覆盖**（逐转录本差异大，仍用 VEP 规范转录本值，本地值留在 `EV.dbnsfp54` 备查）。
- 多转录本归并为最不利于良性的一端（分数取 max、SIFT 取 min）。PP3/BP4 仍按 Pejaver 2022 校准阈值读 REVEL，不因本地接入改规则。
- 5.4a 不覆盖 indel；`found=false` 不得解读为"预测良性"。
- 报告引用预测分时写版本：`dbNSFP 5.4a`，不写笼统的"dbNSFP"。
- `--no-dbnsfp54` 关闭本地查询；`--dbnsfp54 /path/to.gz` 临时指定库路径。

## 7. Step 0.45：频率 / ClinVar / 重复区结构化取数（强制门控）

> **为什么是硬门控**：CUL7 `NM_014780.5:c.4126_4128del`（p.Glu1376del）曾因用 HGVS 文字 web_search 查 indel、查不到就写"gnomAD 未检出 / ClinVar 无条目 / novel"，误赋 PM2_Supporting；PM4 又以"未检索到重复区证据"为由赋值。实际 gnomAD v4 AC=77、EAS FAF95=6.34×10⁻⁴，ClinVar VCV587529 为 VUS★★，位点落在 RepeatMasker `(TCC)n` 内。两条致病证据都是错的。
>
> **v2 补丁**堵住三条假"确无"通路：非左对齐写法、REF 不符坐标、GraphQL 单点故障。权威参考为 [`references/FREQUENCY_EVIDENCE.md`](references/FREQUENCY_EVIDENCE.md)（与本节目冲突时以该文件为准）。

### 7.1 执行（Step 0 过门后立即执行）

```bash
# ① 频率（PM2/BA1/BS1/BS2）：优先 HGVS，坐标由 ClinGen Allele Registry 解析，禁止心算
python3 scripts/freq_evidence.py --hgvs "NM_014780.5:c.4126_4128del" --gene CUL7 --moi AR --card
#   或给 GRCh38 坐标（脚本核对 REF 并自动左对齐）：
python3 scripts/freq_evidence.py 6-43040322-CTCC-C --gene CUL7 --moi AR --card
#   AR 需要阈值计算时补：--prevalence 1/N --allelic x --genetic y --penetrance z

# ② ClinVar 与序列上下文（PM4/BP3）
python3 scripts/freq_repeat_lookup.py 6-43040321-TCTC-T --gene CUL7 --aa-pos 1376 --aa-ref E --card
```

- `freq_evidence.py`：CAR 解析 → REF 核对 + 本地左对齐 → gnomAD GraphQL，失败转公共存储桶 joint VCF 远程 tabix（GCS→AWS，纯 Python）→ ±60 bp 等价写法扫描 → Allele Registry `gnomAD_4` 链接交叉核对 → 覆盖度核查 → 自动拉取 CSpec 该基因 VCEP 的 PM2/BA1/BS1/BS2/PS4/PM3 原文 →（可选）Whiffin 阈值计算。退出码 `0` 可用 / `2` 输入无效 / `3` gnomAD 未能查询。
- `freq_repeat_lookup.py`：只负责 ClinVar 与重复区（UCSC ±30 bp 序列与小写软屏蔽、rmsk/simpleRepeat 覆盖、UniProt ±10 aa 窗口与同残基连续串长度）。频率一律以 `freq_evidence.py` 为准。
- **脚本跑不了时**（沙箱/无网）：① web_fetch `https://reg.genome.network/allele?hgvs={HGVS}` 取 CA ID、GRCh38 坐标、`externalRecords.gnomAD_4[0].id`——有 ID 即已收录，禁止写"未检出"；② 打开 `gnomad.broadinstitute.org/variant/{ID}?dataset=gnomad_r4` 读 GroupMax FAF、各人群、Filters、纯合/半合，未收录则查 `…/region/{chr}-{pos-20}-{pos+20}` 看覆盖度；③ 读 CSpec 该基因 VCEP 频率条款全文；④ 都做不到 → `NOT_QUERIED`，扣留结论并请用户在有网络环境跑脚本贴回卡片。**绝不以搜索摘要或 GeneBe/Franklin 自动标签代替。**

### 7.2 频率状态（九态，全流程统一）

| 状态 | 触发条件 | 允许措辞 | PM2 | BA1/BS1/BS2 |
|---|---|---|---|---|
| `FOUND` | 查到且至少一个数据集 PASS | 写 AC/AN、grpmax AF、grpmax FAF95（人群）、hom/hemi、来源 | 按 7.3 | 按 7.3 |
| `FOUND_FILTERED` | 查到但所有数据集未过质控（含 AC0） | "gnomAD 有记录但未通过质控（{filters}）" | ⛔ 不自动赋 | ⛔ |
| `ABSENT_CONFIRMED` | 未查到 + REF 已核 + 已归一化 + ±60 bp 无等价记录 + CAR 无 gnomAD_4 链接 + 覆盖充分（≥20× 样本 ≥90%，或邻近 AN ≥ 满 AN 80%） | "gnomAD v4.1 未收录（位点覆盖充分）" | ✅ Supporting | 不满足 |
| `ABSENT_LOW_COVERAGE` | 未查到、覆盖不足 | "未收录但覆盖不足，不能视为人群缺失" | ⛔ | 不适用 |
| `ABSENT_COVERAGE_UNVERIFIED` | 未查到、覆盖度与代理都取不到 | "未收录，覆盖度未能核实" | ⛔ 扣留 | ⛔ |
| `REPRESENTATION_MISMATCH` | 写法未命中但窗口内有等价记录 | 改用等价记录重查 | ⛔ 扣留 | ⛔ |
| `CONFLICT` | 本次未命中但 CAR 显示 gnomAD_4 已收录 | "来源矛盾，未能确认" | ⛔ 扣留 | ⛔ |
| `INVALID_INPUT` | REF 不符 / HGVS 无法解析 | "输入坐标无效" | ⛔ 扣留 | ⛔ |
| `NOT_QUERIED` | 所有来源失败 | "**未能查询**"；⛔ 禁止"未检出/novel/极罕见/AF=0" | ⛔ 扣留 | ⛔ |

ClinVar 与重复区为三态 `FOUND / ABSENT_CONFIRMED / NOT_QUERIED`，重复区另有 `IN_REPEAT / NOT_IN_REPEAT / PARTIAL / ISOFORM_MISMATCH`。

### 7.3 门控（直接约束 Step 1.2、4.2 与判定引擎）

- **VCEP 优先**：脚本打印的 CSpec 原文阈值覆盖通用规则；有 VCEP 时模块 3 引用规范编号与版本，判定指标（PopMax MAF 或 FAF）按原文执行。
- **统计量口径**：PM2 用 **grpmax AF 点估计**（对致病结论保守）；BA1/BS1 用 **grpmax FAF95**（对良性结论保守）。grpmax 不含 ami/asj/fin/remaining 等瓶颈人群；所用人群 AN ≥ 2000；KOR/JPN 等小亚群不单独触发 BA1。
- **PM2** 仅两种情况赋 Supporting：`ABSENT_CONFIRMED`；或 `FOUND` 且 AD/XLD 为 AC=0（迟发/外显不全须按 Whiffin 计算并写出参数），AR/XLR 为 grpmax AF 低于 PM2 上限且 grpmax FAF95 不超过 BS1 下限。介于两阈值之间时两条都不赋。无 VCEP 又未计算阈值时，不得凭"很罕见"赋 PM2。
- **FOUND_FILTERED**：不自动赋 PM2，也不作良性证据；看 AB/DP 后在模块 6 说明。
- **BA1**：任一大陆人群（AN ≥ 2000）AF > 5%，或按 VCEP 阈值，且不在豁免名单内（Ghosh 2018 Table 1：ACAD9 c.-44_-41dup、ACADS c.511C>T、BTD c.1330G>C、GJB2 c.109G>A、HFE c.187C>G、HFE c.845G>A、MEFV c.1105C>T、MEFV c.1223G>A、PIBF1 c.1214G>A；以 ClinGen 在线清单为准）。**BA1/BS1 触发且 ClinVar P/LP ≥2★ → 强制冲突复核**（查 VCEP 例外与奠基者效应：GJB2 c.35delG NFE FAF95 0.81%、c.235delC EAS FAF95 0.60% 都超过听力 VCEP BA1 0.5%，但都是致病变异）。
- **BS1**：grpmax FAF95 > 最大可信 AF（VCEP 阈值 > Whiffin 计算：AD = 患病率/2 × 等位贡献 × 遗传贡献 ÷ 外显率；AR = √患病率 × 等位贡献 × √遗传贡献 ÷ √外显率）。无阈值不赋。
- **BS2（gnomAD 来源）**：hom/hemi ≥2、早发、完全外显、非亚效等位、非 CHIP 基因（DNMT3A/TET2/ASXL1/TP53/JAK2/PPM1D 等）时才考虑；**产前默认封顶 BS2_Supporting**（VCEP 另有规定除外）。
- **ClinVar**：状态不是 `ABSENT_CONFIRMED` 时，全文禁止"novel / 无条目 / 首次报道"；Step 0.6 的"ClinVar 无条目"触发条件同样以此为准。
- **PM4/BP3**：`IN_REPEAT` → PM4 ⛔，改评估 BP3（BP3 的"无已知功能"须单独论证：结构域注释边界内 ≠ 有已知功能）；`NOT_IN_REPEAT`（DNA 与蛋白两层都核查）→ 才可评估 PM4；`NOT_QUERIED / PARTIAL / ISOFORM_MISMATCH` → 两者都不赋，标注"序列上下文未核查"。⛔ 禁止"未检索到重复区证据，故 PM4 适用"。
- 两个脚本输出的门控结论原样写入模块 3 每条相关证据的"数据依据"。

### 7.4 完整性闸门（结论扣留）

任一情况，模块 1 **不输出分级标签**，写 `结论已扣留：{缺失源} {状态}`：gnomAD 为 `NOT_QUERIED / INVALID_INPUT / CONFLICT / REPRESENTATION_MISMATCH / ABSENT_COVERAGE_UNVERIFIED`，或 ClinVar 为 `NOT_QUERIED`。模块 3 中依赖该源的代码（PM2/BA1/BS1/BS2、PS4 计数法、PM3 的 PM2 前提、ClinVar 分流）标"无法评估"、不计分。ChinaMAP 等补充来源失败**不**触发扣留。

## 8. Step 0.5–0.7：ClinVar 分流、邻近扩圈、产前预后

- **0.5 ClinVar**：多路径交叉（坐标/rsID 结构化查询优先，cDNA、蛋白写法补充），记录 VCV/RCV/SCV、疾病、review status、评价日期、提交冲突。高星级共识帮助确定核查重点，不替代独立证据。路径 0 未命中且非 `ABSENT_CONFIRMED` 时只能写"ClinVar 未能确认"。
- **0.6 邻近位点扩圈**：同残基/近邻、功能子域、相关表型三圈；输出邻近变异地形报告。近邻不直接算 PM5；无记录写"在本次范围未检出"，不称首次报道。
- **0.7 产前预后检索**：P1 影像学预后、P2 神经发育结局、P3 文献补充请求、P4 检查窗口建议；记录 n/N、随访、入组偏倚、是否为本变异。

产前样本前置质控（评级前）：MCC 比例（阈值 5%，≥20% 基因型不可靠、置信度降 Low；未定量时 de novo/PS2 标注"未排除 MCC"）、VAF/深度/链偏倚、同源区/MAPQ、检测方法与 LOD。

## 9. Step 1–4A：检索、定位、对标、预测与 VCEP

- **Step 1**：ClinVar、gnomAD、基因约束（pLI/LOEUF）、OMIM、ClinGen/GenCC。频率以 Step 0.45 为准；约束不独立证明机制。
- **Step 2**：分子定位与转录本二次核实；HGVS 规范化由工具完成，不心算。**exon 边界/长度不得心算：凡 splice/exon PVS1，先运行 `scripts/exon_check.py <transcript> <exon>` 做 NCBI GenBank + Ensembl 两源核对；exon 数或任一 exon 长度不一致时不得继续 PVS1。**
- **Step 3**：Franklin/VarSome/InterVar 对标，只作差异讨论，不进入独立证据。
- **Step 4**：REVEL（Pejaver 2022 区间）、AlphaMissense、CADD、SpliceAI、保守性；PS3/BS3 质量门槛（Brnich 2020 / ClinGen SVI）。
- **Step 4-PVS1（强制）**：任何 PVS1 赋值必须先运行 `scripts/pvs1_review.py`，用 **SVI 2018 Table 1 机制档（G1/G2/G3）** 计算强度；输入必须含 `lof_evidence`（逐条 LoF：分类、所用条款、是否依赖 PVS1）与结构化的 `null_mouse`。**`PVS1_VeryStrong` 只在 `mechanism_tier=G1` 且 `counts_audited=true` 时允许**；报告必须原样粘贴 `mechanism_tier`、`adjusted_strength`、`lof_evidence_audit` 三个计数。禁止凭叙述写“机制门槛 G1”。**NMD 逃逸（末外显子、单外显子、倒数第二外显子末 50 bp）的下游 P/LP 变异只支持 `PVS1_Strong`，不得升级为原级；见 [决策记录](review/DECISION_NMD_ESCAPE_2026-11-23.md)。**
- **exon 两源核对（强制，v0.8.2）**：凡 PVS1 依赖 exon 长度、exon skipping、in-frame/out-of-frame 或 NMD 判断，必须先运行 `scripts/exon_check.py <transcript> <exon>`；把 JSON 卡片写入 `pvs1_input.exon_check`，`status=PASS` 且 `cross_check.passed=true` 才可继续。NCBI GenBank 与 Ensembl 的 exon 数/长度必须一致；不得把 UCSC BED/genePred 的 0-based 半开坐标直接当 1-based 闭区间（JAG1 `c.82-2A>G` 的 306 vs 307 教训）。
- **Step 4A VCEP**：任何基因都要查 [CSpec](https://cspec.genome.network/cspec/ui/svi/)。适用则取全文、附表、原始论文与版本，逐条赋分；全文未取得时阻断依赖该材料的评级，不默认回退通用规则。无适用版本才回退 ACMG 2015 + SVI 补充。

详见 [`references/ACMG_CRITERIA.md`](references/ACMG_CRITERIA.md)（规则条文）、[`references/PVS1_V5.md`](references/PVS1_V5.md)（PVS1 输入契约与 35 条路径）、[`references/INTEGRATED_V5R1.md`](references/INTEGRATED_V5R1.md)（逐例 VCEP 选择与审核接入）。

## 10. Step 5：家系整合

de novo 双轴评估（亲缘确认 vs 变异确认）、共分离、PM3 反式、PP4、印记/UPD、X 连锁、嵌合、AR 第二打击、双重诊断、本地未发表病例。文献只写"trio/复合杂合"不自动证明亲缘或定相。AR 单等位基因的致病性、携带状态、诊断分开；无 BAM/VCF 时第二打击/嵌合输出"待执行清单"，不称已排除。

PS2 vs PM6：写明亲缘确定或 trio-WES/WGS 检出 → PS2；仅病史"新发" → PM6 或不计。PM3 in trans：文献明确写复合杂合/in trans/父母来源 → in trans，否则 unknown。

## 11. ACMG 判定引擎

### 11.1 判定前检查清单

0. **基因-疾病有效性门控**：ClinGen/GenCC ≤ Limited、Disputed/Refuted 或无记录 → 封顶 VUS 并标注；Moderate → PVS1 上限按 `ACMG_CRITERIA.md` §1.2。
0′. **样本层门控**（产前）：MCC、VAF/嵌合、高同源区三项已核，未核则标注并降 Confidence。
0″. **PVS1 机制档门控（强制）**：PVS1 强度必须来自 `pvs1_review.py` 的 `adjusted_strength`；`PVS1_VeryStrong` 仅当 `mechanism_tier=G1` **且** `counts_audited=true`（有 `lof_evidence` 清单核对）。缺 review、tier 非 G1、强度与 review 不一致、或计数未经核对 → `score.py` 记录 blocker，禁止输出 LP/P。基因-疾病关联有冲突（GenCC 多档并存、PanelApp 近 12 个月下调）时按最低共识档并在模块 6 写明。
1. **VCEP 全文门控**：有适用 VCEP 时必须已读全文；未取得则按通用标准赋分并声明"全文未获取 + 用户上传请求"。
2. **证据独立性**：无重复计数（同一 ClinVar/gnomAD 记录只计一次）。
3. **互斥与合并**：禁止共用 PP3/BP4、PS1/PM5、PVS1 与 PM1/PM4/PP2/PP3、PM4/PP3、PM4/PM5、PP2/PM1、PM1 与 PS1/PM5、PS2/PM6 与 PP4、BS2/BP2、BP3/BP4、BP2/BP5；限制合并 PM1+PP3 ≤ Strong、PVS1(RNA)+PS3 ≤ 8、BP7(RNA)+BS3 ≤ 8、PP1+PP4 ≤ 5；PM1 与 PS3 默认不叠加。**PP5/BP6 已废止（SVI 2018）**。
4. **"至少两条证据"**：除 BA1 外 LB/LP/P 至少两条独立证据；单证据一律 VUS（即使积分已入区间）。
5. **良性侧不得托底、产前不出预测型 LB**。
6. **缺数据对称原则**：前提数据没查到 → 两个方向都不赋值；禁止"未检索到 X 的证据，故（反向）适用"。
7. **前提数据溯源**：PM2/BA1/BS1/BS2 必须引用 Step 0.45 的状态与数值；PM4/BP3 必须引用 0.45 的序列/rmsk/蛋白窗口输出。拿不出引用就删掉该代码。

### 11.2 矛盾证据处理

优先级（高→低）：人群频率（BA1 独立）> 功能验证（PS3/BS3、PVS1(RNA)/BP7(RNA)）> 家系（PS2/PM6/PP1/BS4）> 相位（PM3/BP2）> 保守/结构（PP2/PM1）> 计算预测（PP3/BP4）。

常见冲突：BA1 + 任何致病证据 → 良性（豁免名单例外）；BS1 + PP3 → LB/VUS；BS1 + PS2 → LP/VUS；PM2 + BP4 → VUS；PP3_Strong + PM2_Supporting → VUS；PS3 ≥ Strong 与 BP4 相反 → BP4 至多 Supporting 或不计；PP3 与 BP4 互斥。历史 P/LP 被推翻或仅因规则版本变化的边界重分类，须标注。

### 11.3 判定流程

1. 列适用证据代码与强度（用 VCEP 时标来源）；2. 列排除代码与理由；3. 查冲突与重复计数；4. 按组合标准定分类；5. 贝叶斯积分交叉验证（Supporting 1 / Moderate 2 / Strong 4 / Very Strong 8；P ≥10、LP 6–9、VUS 0–5、LB −1～−6、B ≤−7）；6. 两法不一致时讨论；7. VCEP 与通用标准结论不同时在模块 6 说明；8. 敏感性分析：相邻两档争议且改档跨分类线时输出区间与两种分类；9. 按疾病实体/合子状态分层（如"作为隐性等位 LP；杂合状态 VUS/携带"）；10. VUS 给内部亚档（VUS-High/Mid/Low，仅进附表）。

## 12. 可核算留痕与独立辅助评级

证据判断由你完成；**只要报告出现 PVS1，`pvs1_review.py` 为必跑项**（不是可选），其余脚本按需：

| 入口 | 用途 |
|---|---|
| `scripts/pvs1_review.py` | **PVS1 机制档（G1/G2/G3）+ 强度计算的唯一入口**；输出 `mechanism_tier`、`adjusted_strength`、`lof_evidence_audit`、`counts_audited`。报告必须粘贴这些字段 |
| `scripts/exon_check.py` | **exon 长度/相位的两源核对入口**；输出 NCBI/Ensembl exon 表、c. 坐标、phase、mod3、aa 区间与 PASS/MISMATCH；splice/exon PVS1 必跑 |
| `scripts/assisted_case.py case.json` | 一次完成独立辅助评级；输出 `independent_classification`、积分、2015 对照、blockers |
| `scripts/case_pipeline.py` | PVS1/PM3/功能/有限 PP1·PP4 的审核接入与积分核算；对 PVS1 admission 强制 provenance 门控 |
| `scripts/score.py` | 纯算术接口；接受 `pvs1_review` 做**来源核对**（不导入其分值）；`enforce_pvs1_provenance=True` 时缺 review / 强度不符 / 未核对计数均记 blocker |
| `scripts/render_report.py` | 十模块离线报告草稿（核算草稿，不替代临床阅读版） |
| `scripts/cnv_section2.py`、`scripts/cnv_case.py` | CNV Section2 条目选择与 CNV 独立核算 |
| `scripts/evidence_lookup.py`、`scripts/locus_review.py`、`scripts/ba1_review.py` | PS1/PM5·PM4·PS4·BS2·PP1 查表、有限概率分配、BA1 例外匹配 |

**一致性守卫**：当积分制分区与 2015 表5 不一致、且积分最高的证据是 PVS1/PS2/PS3 时，`score.py` 输出 `reaudit_required`，报告必须在模块 6 复核该条并写出结论，不得只以“版本差异”收尾。

契约见 [`references/DATA_CONTRACT.md`](references/DATA_CONTRACT.md)、[`references/INTEGRATED_V5R1.md`](references/INTEGRATED_V5R1.md)、[`references/EVIDENCE_LOOKUP.md`](references/EVIDENCE_LOOKUP.md)；输入示例见 `tests/fixtures/`（合成数据，不可当作真实审核记录）。

`classification` 与 `clinical_signoff` 保持为空（实验室签发字段）；脚本的 `reviewed`/`approved` 是审计记录状态，不是医学正确的证明，也不得伪造审阅人姓名。

## 13. Step 6：VUS 报告取舍与措辞

- 有症状（超声异常/家族史/表型驱动）：满足基因-表型因果门槛则报；GUS 基因封顶 VUS 并标注；AR 单杂合 VUS 默认不报（表型高度匹配除外，且先完成第二打击搜索）；VUS-High 可报并写明补证路径。
- 无症状（高龄/血清学阳性但无异常/携带者筛查/次要发现）：默认不报 VUS；产前报 VUS-High 须有"存在决策机会 + MDT"前提。
- 措辞：不写"正常/健康"；不把小样本病例比例当个体风险；不写指令性妊娠建议；未知写 unknown。

## 14. Step 9-Verify：PMID 反查

逐条核对作者、题名、年份、期刊；正文/补充材料另核其支持的主张；核验覆盖率 = 已核验/实际引用（0 条写 N/A）。没有 PMID 的用 DOI/正式 URL 核验，不伪造 PMID。

## 15. 输出结构（十模块）

模块 1 结论卡（独立辅助评级 + 积分 + 2015 对照 + 外院原评级与差异）→ 2 分子画像 → 3 ACMG 证据链（全中文，每条含数据依据；**PVS1 条必须固定附“机制档 G1/G2/G3 + adjusted_strength + 独立 P LoF 计数/关联 LoF 计数/表型 LoF 占比 + counts_audited”**）→ 4 ClinVar 结论 → 5 外部分类对标 → 6 判读决策（含冲突与敏感性）→ 7 关联疾病画像 → 8 临床可操作性建议（产前用 8′ 预后矩阵）→ 9 参考文献 → 10 局限性。模块 6 若 `reaudit_required` 非空，必须写明对最强证据的复核结论。

模板：[`assets/report-clinical.md`](assets/report-clinical.md)（统一临床版）、[`assets/report-snv.md`](assets/report-snv.md)、[`assets/report-cnv.md`](assets/report-cnv.md)、[`assets/prenatal.md`](assets/prenatal.md)；分层与首页要求见 [`references/REPORT_PRESENTATION.md`](references/REPORT_PRESENTATION.md)。默认交付 Markdown 正文 + 技术附录；不默认转 PDF/Word/HTML。

## 16. CNV 路由

输入为缺失/重复（`chr11:19076957-36302387_del`、`Exon 10-12 dup`、CMA/CNV-seq/WES-CNV 报告）时走 ClinGen 五段式评分，**SNV 积分不得混入**：

- 执行规则：[`references/CNV_CRITERIA.md`](references/CNV_CRITERIA.md)（已核实的 Section2 选择条件与分值范围、2E/2I 的 PVS1 映射、Loss 2H 双预测器档案）。
- 完整五段条文：[`references/CNV_CRITERIA_UPSTREAM.md`](references/CNV_CRITERIA_UPSTREAM.md)（上游 2026-09 版速查，最终分值以 [ClinGen CNV 计算器](https://cnvcalc.clinicalgenome.org/) 为准）。
- 断点区间：`scripts/cnv_interval.py` 只做几何覆盖与最小/最大区间比较，不当基因组注释；断点不确定时对最小/最大区间分别分析，不自动取较高分。
- 已知复发区域（1q21.1、15q11.2、16p11.2、16p13.11、22q11.2 各亚区）先取 ClinGen Recurrent CNV 表对应亚区评分，不拆基因逐条评。
- 产前 CNV：核对数据均一性/波动性（CV）、挑战区（HBA、SMN1、CYP21A2、SHOX、STRC、IKBKG、PKD1）与检测分辨率，断点置信不足时先补第二方法。
- 五段审核由你逐项作有出处的判断（`review_mode=autonomous_assist`），缺资料的事实走未知/不适用分支，不默认安排补检，也不以逐项回复作为服务前提。

## 17. 专项边界

- **重复扩展/动态突变**（FMR1、HTT、DMPK、ATXN 等）：按各病重复数阈值解读并提示专用检测，不套 SNV 框架。
- **线粒体基因组**（m.xxxx / MT-xxx / chrM）：按 ClinGen mtDNA 专项规范（McCormick 2020）评级；本包未内置该规则，先取原文核对。
- **平衡结构重排、嵌合、非编码深内含子**：分流到专项规范，只给检测与资料需求，不强行套引擎。
- **肿瘤/体细胞变异**：不适用本技能（胚系框架）。

## 18. 继承能力与未启用项

已启用：PVS1 35 条通用路径（`pvs1_review.py`）、PM3 病例权重（`review_helpers.py`）、PS3/BS3 OddsPath 查表、PP1/PP4 Table 4 查表与有限概率分配（`locus_review.py`）、PS1/PM5·PM4·PS4·BS2·PP1 查表（`evidence_lookup.py`）、BA1 例外匹配（`ba1_review.py`）、CNV Section2 桥接（`cnv_section2.py`）、十模块报告草稿（`render_report.py`）。

仍未自动化的（保持人工逐例审阅，不得用堆分绕过）：完整家系统计与不等权分配、直接小数主评分、完整 PP1/PP4 原始算法、BA1 正式自动裁决、2023 RNA 引擎、CNV Sections 1/3/4/5 全条款自动选择、多目标 CNV 合并。未实现项不得声称已完成。

## 19. 常见故障与降级

| 现象 | 处理 |
|---|---|
| `freq_evidence.py` 退出码 3 | gnomAD 未能查询 → 结论扣留；按 7.1 网页路径复核或请用户在有网环境跑 |
| 退出码 2 / `IncorrectReferenceAllele` | 输入等位与参考不符：换转录本或核对 REF，不强行解释 |
| `dbnsfp54_local: unavailable` | T9 未挂载 / 无 tabix → 报告注明预测分来自在线源 |
| GeneBe 429 | 设 `GENEBE_KEY`；仍失败则该源标不可用，不猜数值 |
| Worker 未配置 | 跳过五源合并；`_sources.worker.status` 为 `unavailable`/`not_configured`，不影响其余源 |
| `CERTIFICATE_VERIFY_FAILED` | 设 `SSL_CERT_FILE`，或走 curl 通道（`freq_evidence.py` 自带） |
| 外院报告与本地结论不一致 | 模块 6 并列解释差异（证据强度、版本、数据库快照），不取较高等级 |
| 结论被扣留 | 说明缺哪个源、缺什么状态、补齐后如何重评；不生成 VUS 充数 |

## 20. 引用文件索引

| 文件 | 内容 |
|---|---|
| [`references/ACMG_CRITERIA.md`](references/ACMG_CRITERIA.md) | ACMG/SVI 证据代码定义、PVS1 决策树、PM1/PS1/PM4/BA1 细则、互斥与合并（上游 2026-09-29） |
| [`references/FREQUENCY_EVIDENCE.md`](references/FREQUENCY_EVIDENCE.md) | 频率取数状态机、阈值与回归案例（上游 2026-09-29，频率权威参考） |
| [`references/CNV_CRITERIA.md`](references/CNV_CRITERIA.md) | CNV Section2 执行规则（本包已核实版） |
| [`references/CNV_CRITERIA_UPSTREAM.md`](references/CNV_CRITERIA_UPSTREAM.md) | ClinGen CNV 五段式完整速查（上游 2026-09） |
| [`references/CNV_MANUAL_REVIEW.md`](references/CNV_MANUAL_REVIEW.md) | CNV 十二项审核底稿 |
| [`references/PVS1_V5.md`](references/PVS1_V5.md) | PVS1 输入契约与逐路径范围 |
| [`references/LOCUS_V4.md`](references/LOCUS_V4.md) | 有限概率分配/联合小计/Table 4 |
| [`references/EVIDENCE_LOOKUP.md`](references/EVIDENCE_LOOKUP.md) | PS1/PM5、PM4、PS4、BS2、PP1、BA1 查表契约 |
| [`references/WORKFLOW.md`](references/WORKFLOW.md) | 执行规则与原功能保留 |
| [`references/AUTONOMOUS_ASSIST.md`](references/AUTONOMOUS_ASSIST.md) | 自主复核规范、阻断项与署名 |
| [`references/SOURCE_ACCESS.md`](references/SOURCE_ACCESS.md) | 外部取数与降级、PM2 缺失证据原则 |
| [`references/DATA_CONTRACT.md`](references/DATA_CONTRACT.md) | 输入/证据/评分契约 |
| [`references/LOCAL_T9.md`](references/LOCAL_T9.md) | 本地 T9 人群库查询与已知问题 |
| [`references/REPORT_PRESENTATION.md`](references/REPORT_PRESENTATION.md) | 十模块分层与首页要求 |
| [`review/RULE_REVIEW.md`](review/RULE_REVIEW.md) | 规则复核登记 |
| [`review/CHANGELOG_V8.md`](review/CHANGELOG_V8.md) | 本版变更与验收 |
