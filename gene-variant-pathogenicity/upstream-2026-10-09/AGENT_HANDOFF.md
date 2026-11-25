# 交接文档：安装 `gene-variant-pathogenicity` 技能（给其他 Agent 读）

> 读者是任何需要把本技能装进自己 skills 目录的 Claude / Agent。
> 按下面步骤执行即可，无需再问技能作者。

## 1. 这是什么

`gene-variant-pathogenicity` 是一个基因变异致病性评级技能，遵循 ACMG/AMP 2015 + ClinGen SVI + ACGS 2024。
用户给出变异（HGVS、基因+蛋白、VCF 坐标、rsID、CNV 或自然语言）并要求评级时，它会自动触发。
详细说明见同仓库的 [README.md](README.md)。

| 项 | 值 |
|---|---|
| 仓库 | https://github.com/yulinj-ui/gene-variant-pathogenicity （公开，无需登录） |
| 安装包 | 仓库根目录的 `gene-variant-pathogenicity.zip` |
| 技能名（frontmatter `name`） | `gene-variant-pathogenicity` |
| 包内结构 | `gene-variant-pathogenicity/SKILL.md` + `references/`（3 份规则文档、3 个 Python 脚本） |
| 权威来源 | 作者本机 Dropbox 副本；GitHub 是发布渠道，以 `main` 分支为准 |

## 2. 安装

### 2.1 Claude Code（CLI / 桌面版 / Agent SDK）

技能放在 `~/.claude/skills/`（对所有项目生效），或项目内的 `.claude/skills/`（只对该项目生效）。

```bash
SKILLS_DIR="$HOME/.claude/skills"          # 或者：项目根目录/.claude/skills
TMP=$(mktemp -d)
curl -fL -o "$TMP/gvp.zip" \
  https://github.com/yulinj-ui/gene-variant-pathogenicity/raw/main/gene-variant-pathogenicity.zip
mkdir -p "$SKILLS_DIR"
unzip -o -q "$TMP/gvp.zip" -d "$SKILLS_DIR"
rm -rf "$TMP"
```

安装前先检查：如果 `$SKILLS_DIR/gene-variant-pathogenicity` 已存在并且是**符号链接**（作者本人的两台 Mac 就是这样，链接到 Dropbox），**不要覆盖**，直接停下并告诉用户。否则会把作者的权威副本改掉。

```bash
[ -L "$SKILLS_DIR/gene-variant-pathogenicity" ] && echo "已是符号链接，停止安装"
```

### 2.2 claude.ai（网页 / App）

1. 下载上面的 zip（不用解压）。
2. 打开 claude.ai → Settings → Capabilities → Skills，上传这个 zip。
3. 上传前如果已有旧版同名技能，先删掉旧版，再上传。

## 3. 验证

```bash
head -3 "$SKILLS_DIR/gene-variant-pathogenicity/SKILL.md"     # 应看到 name: gene-variant-pathogenicity
ls "$SKILLS_DIR/gene-variant-pathogenicity/references"
python3 "$SKILLS_DIR/gene-variant-pathogenicity/references/genebe_fields.py" "NM_000527.5:c.1183C>T" --card
```

最后一条需要联网。能打印出带坐标和预测分的卡片，就说明取数引擎可用。离线或沙箱环境跑不通也没关系，技能会回落到 web_search 流程。

在新会话里说一句「帮我评级 LDLR c.1183C>T」，技能应自动触发。

## 4. 运行依赖

| 依赖 | 用途 | 是否必需 |
|---|---|---|
| Python 3 | 运行 `references/*.py`，只用标准库，无需 pip 安装 | 建议 |
| 网络（VariantValidator、GeneBe、gnomAD、ClinVar 等） | 结构化取数 | 建议；没有时回落 web_search |
| `curl` | `freq_evidence.py` 的部分取数 | 建议 |
| `tabix` + 本地 dbNSFP 5.4a（GRCh38） | 本地预测分（可选） | 可选 |

可选环境变量：

| 变量 | 作用 |
|---|---|
| `GENEBE_KEY` | GeneBe Basic Auth，格式 `email:apikey`，用于避免限流（429）。**用你自己的，不要找作者要** |
| `WORKER_URL` | 五源 Worker 地址；不设就用默认地址 |
| `NCBI_KEY` | 稳定 ClinVar 查询 |
| `DBNSFP54_TABIX` | 本地 dbNSFP 5.4a 的 `.gz` 路径（同目录要有 `.tbi`）。默认指向作者本机外置盘，**别的机器必须自己设置，不设就自动回落在线源** |
| `TABIX_BIN` | `tabix` 不在 PATH 时用来指定路径 |

## 5. 更新

重新执行 2.1 的命令即可，`unzip -o` 会覆盖旧文件。claude.ai 上是删除旧版后重新上传。
最近的变更记录看 README 的「版本历史」一节。

## 6. 规矩

- **只读使用，不要在自己的副本里改规则**。发现问题请告诉技能作者（Peter，GitHub `yulinj-ui`），由作者改权威副本后再发布。
- 技能输出是**临床决策辅助**，结论必须经认证的临床遗传学家或遗传咨询师审核。
- 用技能分析真实病例时，不要把患者姓名、病历号写进任何对外发布的内容。
