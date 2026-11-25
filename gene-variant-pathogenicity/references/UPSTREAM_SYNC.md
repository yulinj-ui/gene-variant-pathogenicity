# 上游同步记录

## 当前基线

| 项 | 值 |
|---|---|
| 上游版本 | gene-variant-pathogenicity 2026-10-09 包 |
| 分支/提交 | `claude/update-from-local-2026-10-09` / `83c2617fda`（PR #3，open） |
| 档案目录 | [`upstream-2026-10-09/`](../upstream-2026-10-09/PROVENANCE.md) |
| 同步日期 | 2026-10-18 |
| 本包版本 | 0.8.0-local |

## 文件映射

| 上游文件 | 本包位置 | 处理 |
|---|---|---|
| `SKILL.md` | `upstream-2026-10-09/SKILL.md.txt`（档案） | 仅追溯；执行文本已并入本包 `SKILL.md` |
| `references/ACMG_CRITERIA.md` | `references/ACMG_CRITERIA.md` | 逐字副本，可执行标准 |
| `references/FREQUENCY_EVIDENCE.md` | `references/FREQUENCY_EVIDENCE.md` | 逐字副本，频率权威参考 |
| `references/CNV_CRITERIA.md` | `references/CNV_CRITERIA_UPSTREAM.md` | 逐字副本 + 抬头说明；执行版仍为本包 `references/CNV_CRITERIA.md` |
| `references/genebe_fields.py` | `scripts/genebe_fields.py` | 已合并：保留本包离线 fixture/审核契约，加入 dbNSFP 5.4a 查询 |
| `references/freq_evidence.py` | `scripts/freq_evidence.py` | 逐字副本（可执行） |
| `references/freq_repeat_lookup.py` | `scripts/freq_repeat_lookup.py` | 逐字副本（可执行） |
| `AGENT_HANDOFF.md` | `upstream-2026-10-09/AGENT_HANDOFF.md` | 安装交接文档，仅参考 |

## 优先级

1. 适用 VCEP 的已发布规范（按基因/疾病/遗传方式，取全文与版本）
2. `references/ACMG_CRITERIA.md`、`references/FREQUENCY_EVIDENCE.md`（上游发布标准）
3. 本包 `SKILL.md` 的流程与门控
4. 本包 `references/` 的执行细则与脚本
5. `original/`（2026-09-28 档案）与 `review/` 历史记录：只作追溯，不自动生效

上游与本包冲突时：医学条文以上游为准并记录差异；脚本算术以本包 `tests/` 覆盖的行为为准。

## 更新步骤

1. 取上游新包（zip 或分支文件），**不要用 `main` 的旧 zip 覆盖**（main 目前仍是 2026-09-29 版）。
2. 新建 `upstream-YYYY-MM-DD/`，写入 `PROVENANCE.md`（提交、哈希、差异摘要）。
3. 同步 `references/ACMG_CRITERIA.md`、`references/FREQUENCY_EVIDENCE.md`、`references/CNV_CRITERIA_UPSTREAM.md`。
4. 逐项核对 `scripts/genebe_fields.py` 的上游改动是否并入；`freq_evidence.py`、`freq_repeat_lookup.py` 直接替换。
5. 更新本文件与 `SKILL.md` 的版本表、`review/CHANGELOG_V8.md` 的下一条目。
6. 运行 `python3 -m unittest discover -s tests`，并对 1 个阴性/1 个阳性已知变异做取数冒烟。

## 已知上游问题

- `SKILL.md` 与 `AGENT_HANDOFF.md` 的示例 `NM_000527.5:c.1183C>T` 与参考序列不符（该位点 REF=G）。本包示例已改为 `NM_000527.5:c.1183G>A`。若上游修正，删除本条目。
