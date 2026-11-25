# 上游版本固定：gene-variant-pathogenicity 2026-10-09

本目录是作者发布包的**逐字节副本**，只读留存，用于追溯本技能（v0.8.0-local）引用的上游条文、脚本与哈希。

## 来源

| 项 | 值 |
|---|---|
| 仓库 | https://github.com/yulinj-ui/gene-variant-pathogenicity |
| 分支 | `claude/update-from-local-2026-10-09`（PR #3，2026-10-18 仍为 open） |
| 提交 | `83c2617fda`（`Add agent handoff guide for installing the skill`，2026-10-18T05:56:56Z） |
| 内容提交 | `84e3198829`（`Update skill to local version (2026-10-09)`，2026-10-18T05:51:00Z） |
| 包文件 | `gene-variant-pathogenicity.zip`（135,975 字节，包内时间戳 2026-10-09 07:22–07:23） |
| 对照 | 本机 Dropbox 权威副本 `~/Library/CloudStorage/Dropbox/工作文件筐/claude code working zone/claude-skills/gene-variant-pathogenicity` 与本包 SHA256 一致（SKILL.md `da1875615c910c95a4fc14ce93e10b9a` md5；字节数 112,667） |

`main` 分支当前仍发布 2026-09-29 包（111,405 字节 SKILL.md），**不要用 main 的 zip 覆盖本地**。

## 哈希（SHA256）

```
71b8c2016de5bc09935535f01917721c6e911c475475a1f54b3d940e9bfc95c3  SKILL.md
a93c7df8625fa271bfe8523c8336dca1b06fab141958fb8674fb82611abee2e1  references/ACMG_CRITERIA.md
a2ab6a5622d9ee348d64c3b66f8717590b334ec9cd25d5a9f38cc7cc48e25822  references/CNV_CRITERIA.md
4de3cd2100e0bfa52f525da95a0843ba20a92fac0c9be5a33be1623e4c5abb5b  references/FREQUENCY_EVIDENCE.md
1ca18d8e114d73317749f623be01c50519101ef61bf66837b5c7f9a9e13a379e  references/freq_evidence.py
f15896ae8253dba631ba7fea0b960e1f1dc09ec3384e1eadca00c31aacdd1d45  references/freq_repeat_lookup.py
8fd0f08b0472f3f6bd8c2b76aec4473c0ff71b37caf25c5e2593a305d9ff0b5d  references/genebe_fields.py
4b14134fdc43a58394ea654a6d29aee744d60e489c48f38aaf9b1ab2fb444233  AGENT_HANDOFF.md
```

## 与上一版（2026-09-29，本技能 `original/` 存档）的实质差异

1. **Step 0.45 频率/ClinVar/重复区强制门控**（新增 `freq_evidence.py`、`freq_repeat_lookup.py`、`FREQUENCY_EVIDENCE.md`）：
   gnomAD 九态（FOUND / FOUND_FILTERED / ABSENT_CONFIRMED / ABSENT_LOW_COVERAGE / ABSENT_COVERAGE_UNVERIFIED / REPRESENTATION_MISMATCH / CONFLICT / INVALID_INPUT / NOT_QUERIED）；PM2 用 grpmax AF，BA1/BS1 用 grpmax FAF95；输入 REF 核对 + 左对齐 + ±60 bp 等价写法扫描；结论扣留闸门。
2. **废止“间接推断赋 PM2”**（旧 Layer 3）：查询未命中不得写“未检出 / novel”。
3. **PM4/BP3 重复区强制核查**（CUL7 c.4126_4128del 事故）：rmsk/simpleRepeat 软屏蔽 + 蛋白同残基连续串 ≥4；未核查则 PM4/BP3 都不赋。
4. **VCEP 频率阈值自动拉取**（CSpec API）：`freq_evidence.py --gene` 输出 PM2/BA1/BS1/BS2/PS4/PM3 原文，VCEP 优先于通用阈值。
5. **BA1 豁免清单扩充**（Ghosh 2018 Table 1，9 个变异）与“BA1/BS1 触发 + ClinVar P/LP ≥2★ 强制冲突复核”。
6. **BS2 产前默认封顶 BS2_Supporting**；gnomAD 来源 BS2 需早发、完全外显、非亚效、非 CHIP 基因。
7. **本地 dbNSFP 5.4a 接入**（2026-10-09）：hg38 坐标本地 tabix 查询，REVEL/AlphaMissense/BayesDel/MetaRNN/PrimateAI/VARITY_R/ESM1b/CADD 覆盖在线值；SIFT/PolyPhen 不覆盖。

## 已知问题（本次核对发现）

- 上游 SKILL.md 的输入格式示例 `NM_000527.5:c.1183C>T` 与当前参考序列不符：ClinGen Allele Registry 返回 `IncorrectReferenceAllele`（该位点 REF=G，实际等位基因为 `c.1183G>A` p.Val395Met）。该行仅作格式示例，不影响规则；本地版已把冒烟测试示例改为 `NM_000527.5:c.1183G>A`。
- `AGENT_HANDOFF.md` §3 的验证命令同样使用该示例；照此执行 `genebe_fields.py` 会得到一张全 ❌ 的空卡（不报错），容易被误读为“取数引擎不可用”。

## 更新方式

上游发布后，整包替换本目录并在 `references/UPSTREAM_SYNC.md` 登记新哈希与差异；不要只改本目录内的副本（本目录是档案，不是执行源）。
