# 外部取数与降级规范（0.6.5）

## 使用范围

`genebe_fields.py` 的线上取数已接入共享 `source_http.py`。其他临时脚本、浏览器、网页工具不会被自动拦截；使用它们时也须检查实际内容、失败状态和完整性。医学评分规则、默认 MD 报告结构均不改变。

## 本地人群数据库

人群频率取证默认先按 [LOCAL_T9.md](LOCAL_T9.md) 检查和查询 T9。它是本机的补充来源；不可用时继续其他来源，不将失败或损坏文件的空结果当作人群缺失。PM2 的判断仍遵循下文的可靠缺失原则。

## GeneBe / Worker 身份核对

- VariantValidator 先提供精确版本转录本、HGVS、坐标及 GRCh38 RefSeq genomic HGVS；缺少可靠锚点则阻断后续身份验证。
- GeneBe 响应不回显 genome 时，只接受绑定该 JSON 的请求记录：固定官方端点、显式 hg38/GRCh38、请求和响应等位基因均与 VV 一致，且精确转录本唯一。响应若明确回显错误版本，不得用请求版本覆盖。
- 当前 Worker 的 `query.hgvs`、`query.dataset` 必须与请求一致；除了坐标核对，还要求其带版本 RefSeq genomic HGVS 与 VV 的 GRCh38 结果一致。不能仅凭 `gnomad_r4` 标签推定参考版本。不同但可能等价的 indel 表达暂不自动放行，应另行规范化核实。
- 保留旧版明确回显 input/build 的离线输入契约；新响应不得伪装成旧版以省略核对。
- 请求记录包含 URL、时间及 canonical JSON SHA-256，只证明所存请求记录与响应绑定，不是数据库签名或第三方真实性认证。离线导入记录需来自完整、已核实的实际请求，不得为缺失证据补造元数据。
- 在线 `--raw` 输出包含 evidence 内的 `_request_metadata` 和原始 responses。离线重放可使用 `{ "responses": {...}, "request_metadata": {...} }`，保留原始取证日期。

## 部分成功

Worker `sources` 中每个上游分别检查。频率依赖 gnomad_variant，约束依赖 gnomad_gene，同位点扫描依赖 clinvar_codon；失败或状态缺失时清空相应块。预测分数只接收其已成功上游对应的数据；合法有限数值字符串可转换，仍校验范围。原始响应保留以供复核。

`_sources.worker=partial` 表示部分数据可用，不能改写为全部成功。`_upstream_status` 和 `_field_status` 提供具体状态，`_fetch_status` 描述传输结果。传输成功、身份核实、字段齐备及医学适用是不同层次。

GeneBe 自动 ACMG 仅作对标。FAF、过滤状态、覆盖及版本等未返回字段保持未知；多个聚合平台转引同一原始数据不能重复算独立证据。

## PM2_Supporting：可靠缺失，不要求所有字段齐全

按适用VCEP的基因、疾病和遗传方式要求优先判断；没有适用专病规范时，依据ClinGen SVI的PM2降为Supporting建议进行逐例审核。

- 可以采纳：变异身份及参考版本已核实，指定人群数据库查询成功、未观察到目标等位基因，并有足够依据认为该区域对此类变异有可靠检出能力。记录数据库版本、查询日期、来源及判断依据。
- 检出能力可以由位点或区域覆盖资料、可检出范围说明、附近位点的有效等位基因数等共同支持。附近资料是辅助依据，不能代替对目标位置低覆盖、低复杂度或难比对问题的判断；Indel等困难类型需额外考虑其检出局限。
- **不要求每例同时取得AN、FAF、各祖源频率和逐项过滤字段。** 无记录变异可能没有专属AN或FAF；缺某一字段不自动否决PM2_Supporting，也不应成为整例停工理由。保留未知字段，并说明现有证据为何足够或不足。
- 不能采纳：仅有网页/接口错误、未加载、第三方AF=null/空字符串，或未说明来源的“0”；以及有实际低覆盖/检出困难而无法解释的情况。成功查询无记录与未取得数据分开记录，不将空值补为AF=0。
- 无记录通常可支持PM2_Supporting，但不是无条件自动赋值；有少量记录也可能符合适用专病的极低频阈值。不得自创统一AN、覆盖深度或祖源样本数门槛，不把BA1的样本量条件套用于PM2。

报告用语：“在〔数据库/版本〕未观察到该变异，〔位点或区域检出能力依据〕支持此次缺失结果可靠，采用PM2_Supporting。”若不足，具体说明是检出能力未明确还是查询失败，不笼统要求“所有人群字段完整”。自动注释缺字段时可通过有出处的人工证据审阅补足判断，不能修改原始响应或伪造数值。

依据：[ClinGen SVI PM2 v1.0（2020）](https://clinicalgenome.org/site/assets/files/5182/pm2_-_svi_recommendation_-_approved_sept2020.pdf)规定强度降为Supporting；[gnomAD解释指南（Gudmundsson等，2022）](https://pmc.ncbi.nlm.nih.gov/articles/PMC9160216/)说明覆盖和附近等位基因数的评估。以上是对缺失证据可靠性的操作澄清，不声称上述文献规定所有字段必须齐全。

## 统一取数

```bash
python3 /absolute/skill/scripts/genebe_fields.py 'NM_017780.4:c.2831G>A' --online --worker 'https://your-explicit-worker.example' --raw
python3 /absolute/skill/scripts/source_http.py 'https://public.example/data.csv' --format text --output data.csv --timeout 60 --expected-sha256 VERIFIED_HASH
```

示例域名和 VERIFIED_HASH 是占位，实际使用须替换。Worker 必须由调用者显式指定；本技能不内置个人 Worker 地址、不自动读取浏览器凭据。支持 Worker 基础 URL 或以 `/annotate` 结尾的 URL。GeneBe 认证优先用 `GENEBE_EMAIL` 加 `GENEBE_KEY`；兼容旧 `GENEBE_KEY=email:key`，密钥不写入请求 URL 或状态。

共享取数只接受 HTTPS，拒绝自动跳转（避免转发认证和变异信息）。如合法资源跳转，先核对目标，再明确请求最终 URL。默认最多尝试两次；429/部分 5xx/网络与下载截断可有限重试。尊重 Retry-After；超过等待上限则返回待重试状态，不提前重试，也不无限等待。不会通过更换身份绕过限流或验证码。

| 状态 | 处理 |
|---|---|
| rate_limited | 记录 HTTP 状态及 Retry-After，稍后按限制重试；不能判为无记录 |
| challenge_page / unexpected_html | 没有取得预期数据；可用获准浏览器处理，不把验证码或登录页当正文 |
| incomplete_download | 不写入目标文件，不覆盖已有完整文件；重新取数或降级 |
| checksum_mismatch / invalid_document | 拒绝作为有效证据 |
| api_error | JSON 内部 error/errors；不能因 HTTP 200 放行 |
| access_denied / redirect_blocked / not_found | 分别表示访问受限、跳转未跟随、HTTP 404；404 不等于变异不存在 |
| network_error | 网络/TLS/超时失败，不推导频率或预测结果 |
| file_too_large / unsupported_content_encoding | 调整经审核的获取方式或参数，不静默截断 |

## 下载完整性边界

下载先验证后原子写入，失败不发布残片。检查返回状态（拒绝 206）、Content-Length（如提供）、实际读取异常、大小上限和时间上限；可再要求预期大小或 SHA-256。JSON/XML 检查语法，PDF 检查文件头及 EOF，gzip 检查解压/CRC，ZIP 检查成员 CRC。格式检查不是医学内容审核，也不是全面文档语义校验。

对没有 Content-Length、校验和或预期行数的 CSV/TSV，正常传输结束仍不能证明服务器没有提前生成一个较短但语法完整的文件。返回 `transport_and_format_checked`，不得称权威全量已核实；大型数据集应再核对发布方哈希、行数、版本和分页完整性。下载完成但字段齐备性未知仍须如实记录。

## 回归与离线使用

`tests/fixtures/public-chd7-live-20260927.json` 是公开变异响应及取证元数据快照，不是患者资料，也不代表该变异已完成本技能评级。无网络时可重放；来源日期保持 2026-09-27。默认不上网，不配置 Worker 时明确降级。
