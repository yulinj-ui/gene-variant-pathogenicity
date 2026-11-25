# v0.8.0-local 变更与验收（2026-10-18）

## 目标

把本机 DeepSeek Harness 技能从 v0.6.6-assist（基于上游 2026-09-28 版）对齐到作者 2026-10-09 发布包，并保持本机已验证的审核引擎、报告层与离线测试；目标是能在本机直接做变异解读，而不是只做规则迁移审计。

规则来源与哈希见 `../upstream-2026-10-09/PROVENANCE.md`，映射与更新流程见 `references/UPSTREAM_SYNC.md`。

## 变更清单

### 新增

| 文件 | 说明 |
|---|---|
| `upstream-2026-10-09/` | 上游 2026-10-09 包逐字节档案（SKILL.md.txt、ACMG_CRITERIA、CNV_CRITERIA、FREQUENCY_EVIDENCE、三个脚本、交接文档）+ PROVENANCE |
| `references/ACMG_CRITERIA.md` | 上游 2026-09-29 规则条文（此前只在 `original/` 存 2026-09-28 旧版） |
| `references/FREQUENCY_EVIDENCE.md` | 频率取数状态机、阈值、回归案例（频率权威参考） |
| `references/CNV_CRITERIA_UPSTREAM.md` | ClinGen CNV 五段式完整速查（上游副本） |
| `references/UPSTREAM_SYNC.md` | 上游映射、优先级、更新步骤、已知问题 |
| `scripts/freq_evidence.py` | 频率/ClinVar/VCEP 频率阈值取数与九态门控（上游，可执行） |
| `scripts/freq_repeat_lookup.py` | ClinVar 与重复区序列上下文（上游，可执行） |
| `review/CHANGELOG_V8.md` | 本文件 |

### 修改

| 文件 | 说明 |
|---|---|
| `SKILL.md` | 重写为 0.8.0-local：新增 Step 0.45 频率门控（九态/阈值/完整性闸门）、PM4·BP3 重复区核查、本地 dbNSFP 5.4a、VCEP 频率阈值；补齐 Step 0–9 主流程与十模块；保留 v7 的审核/报告层；版本表与引用索引更新 |
| `scripts/genebe_fields.py` | 加入 dbNSFP 5.4a 本地 tabix 查询（`src_dbnsfp54`、`dbnsfp54` 输出、预测值覆盖、`--dbnsfp54/--no-dbnsfp54`）；`annotate(..., dbnsfp54=True)` |
| `scripts/source_http.py` | HTTPS 优先加载 `certifi`/系统 CA 包（本机框架 Python 无根证书，原实现 VV 全失败） |
| `references/LOCAL_T9.md` | 更新 dbNSFP 状态：5.3.1a 损坏 → 5.4a 已就绪并接入 |
| `review/RULE_REVIEW.md` | 抬头注明上游已发布条文可执行、`original/` 仍为档案 |

## 行为变化

1. **频率成为硬门控**：PM2/BA1/BS1/BS2 只能依据 `freq_evidence.py` 的状态与数值；`NOT_QUERIED` 等状态扣留结论，禁止写"未检出/novel/AF=0"。
2. **PM2 口径**：grpmax AF 点估计；AD/XLD 需 AC=0（或 Whiffin 参数），AR/XLR 需低于 PM2 上限且 FAF95 不超过 BS1 下限。
3. **BA1/BS1 口径**：grpmax FAF95；BA1 豁免名单与"BA1/BS1 + ClinVar P/LP ≥2★ 强制冲突复核"。
4. **PM4/BP3**：必须先有 rmsk/simpleRepeat + 蛋白同残基窗口结果，`IN_REPEAT` 时 PM4 不可赋。
5. **预测分版本化**：本地 dbNSFP 5.4a 命中时覆盖 8 个预测指标并标注来源；SIFT/PolyPhen 不覆盖。
6. **不做的事**：`classification` / `clinical_signoff` 仍为空；Worker 仍需显式地址；BA1 不自动裁决；未核实规则仍不计分。

## 本地偏离上游之处（有意保留）

| 位置 | 偏离 | 原因 |
|---|---|---|
| `scripts/genebe_fields.py` | 保留本包 fixture/审核契约，dbNSFP 查询为增量 | 离线回归与来源留痕是本包基础 |
| `scripts/source_http.py` | HTTPS 增加 certifi/系统 CA 回退 | 本机框架 Python 无根证书 |
| `scripts/freq_evidence.py` | 有 VCEP 时不再附加"两条都不赋"（改为提示按 CSpec 重判 PM2） | 通用 AD 的 AC=0 规则不适用于 VCEP 定制阈值（如 LDLR GN013 的 PM2 Moderate ≤0.0002） |
| `references/CNV_CRITERIA.md` | 执行版保留本包已核实 Section2 规则 | 比上游速查更细，且与 `cnv_section2.py` 一致 |

## 验收记录（本机实测）

| 项 | 命令 | 结果 |
|---|---|---|
| 离线单测 | `python3 -m unittest discover -s tests` | 445 项通过（新增文件后仍单 SKILL.md） |
| 频率取数（阳性对照） | `freq_evidence.py --hgvs NM_004004.6:c.35delG --gene GJB2 --moi AR --card` | `FOUND`；AC=11375/AN=1613482，grpmax FAF95=0.0081339（nfe）；CSpec GN005 阈值原文输出；BA1 不满足 |
| 重复区/ClinVar（事故复现） | `freq_repeat_lookup.py 6-43040321-TCTC-T --gene CUL7 --aa-pos 1376 --aa-ref E --card` | ClinVar 587529 VUS；`IN_REPEAT`（rmsk `(TCC)n`）；蛋白 `EEEEEE` 串长 6；PM4 ⛔、BP3 候选 |
| 三源 + 本地 dbNSFP | `genebe_fields.py NM_000527.5:c.1183G>A --online --card` | 蛋白门 `verified`（p.Val395Met）；hg38 chr19:11111636 G>A；REVEL 0.492、AlphaMissense 0.1404、CADD 9.251 等来自 `dbNSFP5.4a(local)`；`dbnsfp54_local: ok` |
| 无效等位（阴性对照） | `freq_evidence.py --hgvs NM_000527.5:c.1183C>T ...` | CAR 报 `IncorrectReferenceAllele`（REF=G），退出码 2；不解释为频率缺失 |
| VCEP 阈值优先 | `freq_evidence.py --hgvs NM_000527.5:c.1183G>A --gene LDLR --moi AD --prevalence 1/250 --allelic 0.05 --penetrance 0.8 --card` | `FOUND`（AC=1/AN=1613310，nfe）；拉取 GN013 v1.2：PM2 Moderate ≤0.0002、BS1 ≥0.002、BA1 ≥0.005；通用 AD 的 PM2 提示已改为"按 CSpec 重判" |

耗时：单测 ~1 s；`freq_evidence.py` 20–60 s；`genebe_fields.py --online` 约 1.5–2 min（dbNSFP 57 GB 表头解析）。

## 已知问题与待办

1. **上游示例等位错误**：`NM_000527.5:c.1183C>T` REF 不符（应为 `c.1183G>A`）。本包已改示例；上游 README/交接文档仍建议作者修正。
2. **dbNSFP 5.4a 不覆盖 indel**：`found=false` 只能说明库内无此等位，不能作预测良性。
3. **Worker 五源未配置**：`genebe_fields.py` 的 gnomAD 原始频率为空属预期，频率证据以 `freq_evidence.py` 为准。
4. **CNV Sections 1/3/4/5** 仍为人工逐条审阅，未自动选择；`CNV_CRITERIA.md` 与上游速查并存，执行以本包版为准。
5. **TA 级 VCEP 频率阈值** 依赖 CSpec 在线；离网时按 `FREQUENCY_EVIDENCE.md` 的降级路径处理，不猜阈值。
6. **未回归**：`assisted_case.py` 端到端病例与 CNV 桥接仍用 v7 合成 fixture，未用真实病例复核；规则改动后应各跑一例真实（去标识）病例。

## 回滚

安装前的完整副本在 workspace `gvp-v7-merged/`（与安装目录逐字节一致）与 `gvp-v8-preinstall/`（本次安装前快照）。回滚即把该目录内容复制回 `~/.dsh/skills/gene-variant-pathogenicity`。
