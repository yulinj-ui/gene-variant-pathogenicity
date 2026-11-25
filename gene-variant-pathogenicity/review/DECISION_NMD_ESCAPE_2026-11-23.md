# 决策记录：NMD 逃逸变异不因下游 P/LP 变异升级为 PVS1 原级

- 日期：2026-11-23
- 状态：已采纳；同时回退 v0.9.0 的 `region_upgrade` 实验
- 适用范围：本技能包的**通用 PVS1 树**；VCEP/正式基因特异性政策优先，不在本记录限制内

## 触发案例

FOXC2 `NM_005251.3:c.443del`（p.Leu148ArgfsTer53），产前颈部淋巴水囊瘤/水肿。FOXC2 为单外显子基因，
PTC 在 codon 200，下游无外显子-外显子连接 → NMD 不预期；同一单外显子内存在下游 P/LP 截短变异
（c.563_584del p.Pro188fs P、c.595dup p.His199fs P 多提交者、c.1238_1253del p.Gln413fs LP、c.1298del p.Asn433fs LP）。

曾据此在 v0.9.0 加入 `region_upgrade`，允许把 PVS1 从 Strong 升为 Very Strong（PVS1 原级）。经复核最新通用树后回退。

## 决定

1. **通用树（2018 SVI / Abou Tayoun）**：NMD 逃逸（末外显子、单外显子、倒数第二外显子末 50 bp）且截短区为关键功能域时，
   下游 P/LP 截短变异是支持 **PVS1_Strong** 的证据，不是升级为 Very Strong 的依据。
2. **不采用 `region_upgrade`**；不因“下游有明确致病变异”把 Strong 升为原级。
3. **有 VCEP/正式基因特异性政策时，按该政策执行；没有时按通用树。** 基因特异性替代不走本技能的通用引擎
   （`pvs1_review.py` 的 `vcep_policy` 仅接受 `reviewed_generic_applicable`，否则阻断并要求 separate engine）。
4. FOXC2 无 VCEP（CSpec 检索无）→ 通用树：`PVS1_Strong`；Table 1 机制档 G2 再降为 `PVS1_Moderate`；
   `PVS1_Moderate 2 + PM2_Supporting 1 = 3 分` → **VUS**。

## 依据

- **2018 SVI 原文**：NMD 不预期时，截短区关键性“often indicated by … pathogenic variants downstream of the new stop codon”，
  由此估计至少 **~19:1** 致病几率，**consistent with PVS1_Strong assignment**（不是 Very Strong）。
- **PTEN 先例**：last-exon PTC 在 codon 375 5' 被 PTEN working group 提议 PVS1 Very Strong；这是 **working group/VCEP 的基因特异性做法**。
- **SVI 表态**：“elected to **retain the current PVS1 evidence strength levels** … differences … represent the appropriate application of
  **disease and gene-level specifications**.” 即通用树不采纳该上调。
- **2025 ClinGen General SOP v3.2** 仍以 2018 树为通用框架，并把这类差异定位为 VCEP/gene-specific specification。
- FOXC2 目前**无 VCEP**；因此只能走通用树。

## 实施与守卫

- v0.9.0 的 `region_upgrade` 代码、文档、测试与变更记录已全部回退；`pvs1_review.py` 恢复为 2018 通用树。
- 报告层面：NMD 逃逸 + 下游 P/LP 变异只可写 `PVS1_Strong`（再按 Table 1 降级），**不得写 `PVS1_VeryStrong`**，
  除非适用 VCEP/正式基因特异性政策。
- 未来若再次提议 `region_upgrade`，必须先满足其一：① 有明确的 VCEP/正式基因特异性政策；② 官方 SVI 发布新的通用 PVS1 树并给出原文依据。
  否则不得加入。
- 本记录不改变 VCEP 优先原则：查 CSpec 有适用规范时，按规范全文逐条赋分；无适用规范才回退通用树。

## 参考

- Abou Tayoun AN, et al. 2018. Recommendations for interpreting the loss of function PVS1 ACMG/AMP variant criterion. *Hum Mutat* 39(11):1517-1524. PMID 30192042. [原文](https://pmc.ncbi.nlm.nih.gov/articles/PMC6185798/)
- ClinGen General Sequence Variant Curation SOP v3.2（2025-07）. [PDF](https://submit.ncbi.nlm.nih.gov/api/2.0/files/o5ekfuov/clingen_variant_curation_sop_v3.2_classification_guidance_july2025.pdf)
- PTEN VCEP ACMG Specifications v3.1.0. [PDF](https://ftp.ncbi.nlm.nih.gov/pub/clinvar/ClinGen/expert_panels/ClinGen_PTEN/ClinGen_PTEN_ACMG_Specifications_PTEN_v3.1.0.pdf)
- FOXN1 VCEP ACMG Specifications v2.0.0. [PDF](https://submit.ncbi.nlm.nih.gov/api/2.0/files/cz1u8bne/clingen_scid_acmg_specifications_foxn1_v2.0.0.pdf)
