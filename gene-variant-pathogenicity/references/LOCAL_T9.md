# T9 本地人群频率查询

## 默认行为

用户已授权在今后的 SNV/Indel 人群频率取证中，默认检查并查询外接 T9 的适用数据库。先确认 `/Volumes/T9` 挂载和参考资料可读；只需检查 `genomics/refs/`，不遍历其他病例的原始数据或结果。T9 未挂载、工具缺失或数据库不可用时，记录原因并继续可用的在线或其他本地来源，不因缺盘阻断整例。用户明确指定仅在线、仅离线或另一数据路径时遵循当次要求。

查询为只读；输入、日志和输出写入当前病例工作目录，不写入 T9，不自动下载、修复、重建大库索引或更改流水线。以下路径是本机已确认配置，换机时先核实，不假定存在。

## 已确认资料（2026-09-27）

| 资料 | 路径（相对 `/Volumes/T9/genomics/refs/`） | 用途与局限 |
|---|---|---|
| gnomAD r3.0 genomes，slivar 派生库 | `GRCh38/gnomad.hg38.genomes.v3.fix.zip` | 内嵌 `sli.var/args.txt` 注明源 `gnomad.genomes.r3.0.sites.vcf.gz`；创建日期 2019-11-15。含 `gnomad_popmax_af`、`gnomad_nhomalt`，不是完整 VCF，也不提供目标 AN 或覆盖。 |
| dbNSFP 5.3.1a | `annot/dbNSFP5.3.1a_grch38.gz` 及 `.tbi` | 旧副本：表头含 gnomAD4.1_joint 频率列，但存在截断或索引不匹配问题，已由 5.4a 取代，不再用于任何证据。 |
| dbNSFP 5.4a（现行） | `annot/dbNSFP/5.4a/dbNSFP5.4a_grch38.gz` 及 `.tbi`（57,202,197,810 字节，2026-10-08） | 已由 `scripts/genebe_fields.py` 接入：REVEL/AlphaMissense/BayesDel/MetaRNN/PrimateAI/VARITY_R/ESM1b/CADD 走本地值并标注 `dbNSFP5.4a(local)`；不覆盖 SIFT/PolyPhen；不覆盖 indel。文件完整性与索引见同目录 `SHA256SUMS.local`、`installation.json`。 |
| ANNOVAR dbNSFP 4.7a | `dbsnfp/hg38_dbnsfp47a.txt` | 已检查表头没有人群频率列，不能从这个副本查询 gnomAD AF。 |

已确认工具：`/Users/peter/miniforge3/envs/trio/bin/slivar`（查询时版本 0.3.4）、同目录 `tabix`。优先使用现有工具；路径不存在时再查可用安装，不自动安装整套测序环境。

## 查询与解释

1. 先核实变异的参考版本、染色体、1-based 坐标和 REF/ALT。上述 gnomAD 库为 GRCh38；GRCh37 输入需先可靠转换。Indel 要核对规范化、左对齐及等价表达，不能直接把表示不匹配判为缺失。
2. 读取 ZIP 内 `sli.var/args.txt`、`fields.txt`、`message.txt` 核对实际来源，勿仅凭文件名推定版本。构建仅含目标等位基因的最小 VCF，保存于病例目录，以 slivar 查询：

```bash
/Users/peter/miniforge3/envs/trio/bin/slivar expr \
  --vcf /absolute/case/query.vcf \
  --gnotate /Volumes/T9/genomics/refs/GRCh38/gnomad.hg38.genomes.v3.fix.zip \
  --info true \
  --out-vcf /absolute/case/gnomad_r3_local.vcf
```

上述路径为示例，替换病例输入输出路径。检查退出码、stderr、输出记录数及 REF/ALT 身份；发生读取、解压或记录缺失异常时记录失败，不继续解释为频率缺失。

3. 官方 slivar 文档将未收录等位基因的默认输出记为 `-1`。成功查询得到 `-1` 应表述为“此本地版本未收录”，不得改写为 AF=0。实际 AF=0、正频率及非 PASS 标记分别保留；`popmax_af` 是人群组最大频率，不能充当总体 AF 或 FAF。纯合计数也不能当作 AC。
4. 可查询附近已收录等位基因作为技术核对，确认查询和区域定位有效；附近频率不能倒推出目标 AN 或覆盖。必要时结合区域检出能力资料评估缺失可靠性。遵循 SOURCE_ACCESS 的 PM2 原则，不要求每例凑齐所有字段，也不因本地未收录自动赋 PM2。
5. 该旧版 genomes 派生库的结果与较新的 exomes/joint 数据分别记录；旧版缺失不代表新版缺失，多平台转载同一数据不重复计证据。有版本差异时解释差异，不能选择较有利的结果。

格式说明：[slivar gnotate 官方文档](https://github.com/brentp/slivar/wiki/gnotate)。

## dbNSFP 5.3.1a 已知问题

2026-09-27 检查发现：文件长度为 10,810,949,632 字节，而 TBI 指向 chr1:102939051 的压缩偏移为 23,155,360,293 字节，超出 EOF。tabix 同时提示索引早于数据文件，以及 `EOF marker is absent. The input may be truncated`。此时即使退出码为 0、查询返回空，也不能当作 gnomAD4.1 无记录。

这是该本地副本的历史问题，不是对所有 dbNSFP 文件的结论。文件更新后重新核对版本、完整性和索引配对；修复后才可用其结果。仅索引时间较旧不单独证明损坏，但未解决的越界偏移或截断问题会使缺失判断失效。

## 留痕

记录查询日期、数据库路径与版本、工具版本、规范化位点、输入和原始输出、退出码及警告。区分 `observed`（有记录）、`absent_from_local_dataset`（可靠查询未收录）、`unavailable`（不可用）和 `query_failed`（查询失败）。结果用于辅助审核，不自动改写评分输入；采用 PM2 时明确其依据及适用范围。

## 2026-10-18 更新：dbNSFP 5.4a 可用

`annot/dbNSFP/5.4a/dbNSFP5.4a_grch38.gz` 与 `.tbi` 已在位（57.2 GB，2026-10-08 安装），tabix 查询实测正常（chr19:11111636 G>A 命中 REVEL 0.492 等 23 个字段）。
使用要点：

- 查询由 `scripts/genebe_fields.py` 在拿到 hg38 坐标后自动执行；`--no-dbnsfp54` 关闭，`--dbnsfp54 PATH` 换库。
- 5.4a 的 contig 无 `chr` 前缀，脚本已处理；同目录必须有 `.tbi`，否则按"库不可用"回落在线源并在报告注明。
- 5.4a 不覆盖 indel 与非 SNV：`EV.dbnsfp54.found=false` 只表示库内无记录，不能解释为预测良性。
- 频率仍以 `scripts/freq_evidence.py` 为准；5.4a 的 `gnomAD4.1_joint_*` 列只作核对参考，不作为 PM2/BA1/BS1 判据。
