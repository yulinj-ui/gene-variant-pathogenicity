# v0.8.2-local 变更与验收（2026-11-24）

## 触发案例

JAG1 `NM_000214.3:c.82-2A>G`：网页报告把 exon 2 写成 **307 nt**（c.82–388），据此判移码、PTC、NMD，PVS1 路径 S01（Very Strong）→ G2 Strong，最终 LP（6 分）。实际：

- NM_000214.3 exon 2 = 转录本 551..856 = **c.82..387 = 306 nt**；
- Ensembl ENST00000254958 exon 2 = **306 nt**；
- 306 mod 3 = 0 → exon 2 skipping 为 **in-frame**（p.Val28_Pro129del），不是移码；
- 307 的来源：UCSC `ncbiRefSeq` 的 exon 2 是 0-based 半开 `10672700..10673006`（306 nt），报告误当 1-based 闭区间，多算 1 个碱基（c.388，intron 2 首碱基）。

## 变更清单

| 文件 | 变更 |
|---|---|
| `scripts/exon_check.py` | 新增两源 exon 校验工具：NCBI GenBank + Ensembl，输出 exon 表、c. 坐标、phase、mod3、aa 区间、PASS/MISMATCH；支持 `--fixture` 离线回归 |
| `tests/test_exon_check.py` + `tests/fixtures/exon-check-jag1.json` | 新增 4 项回归：JAG1 exon 2 = 306/PASS；off-by-one 307/MISMATCH；合成 3-exon PASS；合成 mismatch |
| `SKILL.md` | 版本 0.8.2-local；Step 2 / Step 4-PVS1 增加 exon 两源核对强制规则；§12 增加 exon_check 入口 |
| `references/PVS1_V5.md` | 输入契约增加 `exon_check`；新增“exon 两源核对”专节 |
| `references/ACMG_CRITERIA.md` | §1.3 坐标陷阱补充 exon 长度/相位规则 |
| `variant-clinic/skill_adapter.py`（网页端） | `pvs1_review_from_summary` 对 `canonical_splice` 强制要求 `exon_check`/`exon_number`；PASS 才进入 pvs1_review，MISMATCH/缺失直接 blocked |
| `variant-clinic/app.py`（网页端） | PVS1 通知中显示 exon_check 状态与拦截原因 |
| `variant-clinic/agent_runner.py`（网页端） | prompt 增加 splice/exon PVS1 必跑 exon_check 的指令 |

## 规则

- splice/exon PVS1：先 `exon_check.py <transcript> <exon>`；NCBI 与 Ensembl 的 exon 数/长度必须一致。
- 1-based 闭区间（GenBank/Ensembl）长度 = `end - start + 1`；0-based 半开（UCSC BED/genePred）长度 = `end - start`，转 1-based 时 `start + 1`。
- 不一致 → `status=MISMATCH`，不得赋 PVS1，报告须写“坐标未核实”。

## 验收

| 项 | 结果 |
|---|---|
| `python3 scripts/run_offline_tests.py` | 全量通过（原 461 + 新增 4） |
| `python3 scripts/validate_package.py` | PASS（version 0.8.2-local） |
| JAG1 回归 | exon 2 = 306/PASS；c.82..387；phase 0；mod3 0；in-frame |
| off-by-one 回归 | Ensembl 307 vs NCBI 306 → MISMATCH |
| 网页端 | canonical_splice 缺 exon_check → blocked `exon_check_required`；MISMATCH → blocked；PASS → 正常进入 pvs1_review |

## 未解决 / 后续

- 工具当前支持 RefSeq mRNA（NM_/NR_ 等）；非 RefSeq 转录本需先映射。
- 仅对 canonical_splice 硬门控；deletion 的 exon-based 场景可按同一卡片逐步接入。
- JAG1 现有 LP 报告需按 306 nt 重算（PVS1 不再是 S01/Strong；默认 S09→Supporting，VUS）。
