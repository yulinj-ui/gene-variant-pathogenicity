#!/usr/bin/env python3
"""
freq_evidence.py — PM2 / BA1 / BS1 / BS2 频率证据的取数、校验与门控（v2，2026-09-29 草案）

取代 freq_repeat_lookup.py 中的 gnomAD 部分（重复区/蛋白窗口部分仍用旧脚本）。
v1 已修复"取数失败 → 当作不存在"；v2 继续堵住三条会导致假 "ABSENT_CONFIRMED" 的通路：
  ① REF 与参考基因组不符（坐标写错 / hg19 当 hg38）→ 旧脚本仍报"确无，可赋 PM2"
  ② indel 未左对齐 / 等价写法（CUL7 6-43040322-CTCC-C 与 6-43040321-TCTC-T 是同一变异，
     后者 AC=77）→ 旧脚本对前者报"确无，可赋 PM2"
  ③ gnomAD GraphQL 单点故障 → 全部"未能查询"，结论扣留
v2 的做法：
  - 输入可以是 HGVS c./g.（经 ClinGen Allele Registry 解析，禁止心算坐标）或 GRCh38 VCF 坐标
  - 用 UCSC 参考序列核对 REF，本地左对齐；再用 Allele Registry 的 gnomAD_4 链接独立交叉核对
  - gnomAD 取数阶梯：GraphQL → 公共存储桶 joint VCF 远程 tabix（GCS → AWS 镜像，纯 Python 无依赖）
  - 无论命中与否，扫描 ±窗口内所有 gnomAD 记录，找等价写法 / 同位点其他等位 / 重叠 indel
  - "确无" 必须有覆盖证据：GraphQL 位点覆盖度；失败时用邻近变异的 AN 作代理
  - 自动拉取 ClinGen CSpec 该基因 VCEP 的 PM2/BA1/BS1/BS2/PS4/PM3 原文
  - 可选：按 Whiffin 2017 计算最大可信 AF 与最大容许 AC，给出 PM2/BS1/BA1 判定
  - 补充东亚参考：dbSNP 各研究频率（TOMMO / Korea4K / ChinaMAP 等，按 rsID）

用法：
  python3 freq_evidence.py --hgvs "NM_014780.5:c.4126_4128del" --gene CUL7 --moi AR --card
  python3 freq_evidence.py 6-43040322-CTCC-C --card               # 自动纠正为 6-43040321-TCTC-T
  python3 freq_evidence.py 19-11113268-G-A --gene LDLR --moi AD --prevalence 1/250 \
          --allelic 0.05 --penetrance 0.8 --card
状态语义见 FREQUENCY_EVIDENCE.md §3。退出码：0 正常；2 输入无效；3 gnomAD 未能查询。
"""
import argparse, gzip, json, math, os, re, struct, subprocess, sys, time, urllib.parse, zlib

GNOMAD_API = os.environ.get("GNOMAD_API", "https://gnomad.broadinstitute.org/api")  # 测试回退时可指向失效地址
VCF_MIRRORS = [
    "https://storage.googleapis.com/gcp-public-data--gnomad/release/4.1/vcf/joint/gnomad.joint.v4.1.sites.chr{c}.vcf.bgz",
    "https://gnomad-public-us-east-1.s3.amazonaws.com/release/4.1/vcf/joint/gnomad.joint.v4.1.sites.chr{c}.vcf.bgz",
]
UCSC = "https://api.genome.ucsc.edu/getData"
CAR = "https://reg.genome.network/allele"
CSPEC = "https://cspec.genome.network/cspec/api"
NC38 = {"1": "NC_000001.11", "2": "NC_000002.12", "3": "NC_000003.12", "4": "NC_000004.12",
        "5": "NC_000005.10", "6": "NC_000006.12", "7": "NC_000007.14", "8": "NC_000008.11",
        "9": "NC_000009.12", "10": "NC_000010.11", "11": "NC_000011.10", "12": "NC_000012.12",
        "13": "NC_000013.11", "14": "NC_000014.9", "15": "NC_000015.10", "16": "NC_000016.10",
        "17": "NC_000017.11", "18": "NC_000018.10", "19": "NC_000019.10", "20": "NC_000020.11",
        "21": "NC_000021.9", "22": "NC_000022.11", "X": "NC_000023.11", "Y": "NC_000024.10"}
# gnomAD v4：grpmax / FAF 排除瓶颈人群 ami/asj/fin/remaining（genome 另排除 mid）
CONTINENTAL = ["afr", "amr", "eas", "mid", "nfe", "sas"]
BOTTLENECK = ["ami", "asj", "fin", "remaining"]
AUTOSOME_FULL_AN = 1_614_240           # v4.1 joint 常染色体满 AN（807,120 人 × 2）
COVER_OK = 0.90                         # 位点 ≥20× 样本比例
PROXY_OK = 0.80                         # 覆盖度代理：邻近变异 AN / 满 AN
WINDOW = 60                             # 等价写法扫描窗口（bp，两侧）
BA1_EXCEPTIONS = {                      # Ghosh 2018 (PMID 30311383) Table 1；以 ClinGen 在线清单为准
    ("ACAD9", "c.-44_-41dup"), ("ACADS", "c.511C>T"), ("BTD", "c.1330G>C"), ("GJB2", "c.109G>A"),
    ("HFE", "c.187C>G"), ("HFE", "c.845G>A"), ("MEFV", "c.1105C>T"), ("MEFV", "c.1223G>A"),
    ("PIBF1", "c.1214G>A")}
EAS_STUDIES = ("TOMMO", "Korea4K", "KOREAN", "ChinaMAP", "Vietnamese", "PAGE_STUDY", "1000Genomes",
               "1000Genomes_30X", "ALFA", "GnomAD_exomes", "GnomAD_genomes", "TOPMED", "ExAC")


# ── HTTP（curl：本机 Python 常缺根证书；带重试）──────────────────────────
def http(url, data=None, rng=None, timeout=45, retries=3, binary=False):
    last = None
    for i in range(retries):
        cmd = ["curl", "-s", "-f", "-L", "-m", str(timeout), url, "-H", "User-Agent: gvp-freq/2.0"]
        if data is not None:
            cmd += ["-H", "Content-Type: application/json", "--data-binary", json.dumps(data)]
        if rng:
            cmd += ["-r", f"{rng[0]}-{rng[1]}"]
        r = subprocess.run(cmd, capture_output=True, timeout=timeout + 10)
        if r.returncode == 0 and r.stdout:
            return r.stdout if binary else r.stdout.decode()
        # gnomAD 对 "Variant not found" 返回 200+errors；curl -f 仅在 4xx/5xx 失败
        last = RuntimeError(f"curl rc={r.returncode} {url[:90]}")
        time.sleep(1.5 * (i + 1))
    raise last


# ── 参考序列、REF 校验、左对齐 ────────────────────────────────────────
class Ref:
    def __init__(self, chrom):
        self.chrom, self.cache = chrom, {}

    def seq(self, start1, end1):
        """1-based 闭区间，按 1 kb 块缓存。"""
        out = []
        for blk in range((start1 - 1) // 1000, (end1 - 1) // 1000 + 1):
            if blk not in self.cache:
                s0 = blk * 1000
                d = json.loads(http(f"{UCSC}/sequence?genome=hg38;chrom=chr{self.chrom};start={s0};end={s0 + 1000}"))
                self.cache[blk] = d["dna"].upper()
            out.append(self.cache[blk])
        base = ((start1 - 1) // 1000) * 1000
        s = "".join(out)
        return s[start1 - 1 - base:end1 - base]


def normalize(ref_obj, pos, ref, alt):
    """vt 式归一化：先去公共后缀并左移，再去公共前缀。返回 (pos, ref, alt)。"""
    while True:
        changed = False
        if ref and alt and ref[-1] == alt[-1] and not (len(ref) == 1 and len(alt) == 1):
            ref, alt, changed = ref[:-1], alt[:-1], True
        if not ref or not alt:
            pos -= 1
            b = ref_obj.seq(pos, pos)
            ref, alt, changed = b + ref, b + alt, True
        if not changed:
            break
    while len(ref) > 1 and len(alt) > 1 and ref[0] == alt[0]:
        ref, alt, pos = ref[1:], alt[1:], pos + 1
    return pos, ref, alt


def vcf_to_hgvs_g(chrom, pos, ref, alt):
    nc = NC38[chrom]
    if len(ref) == 1 and len(alt) == 1:
        return f"{nc}:g.{pos}{ref}>{alt}"
    if len(alt) == 1 and ref[0] == alt[0]:                       # 缺失
        s, e = pos + 1, pos + len(ref) - 1
        return f"{nc}:g.{s}del" if s == e else f"{nc}:g.{s}_{e}del"
    if len(ref) == 1 and alt[0] == ref[0]:                       # 插入
        return f"{nc}:g.{pos}_{pos + 1}ins{alt[1:]}"
    e = pos + len(ref) - 1
    return f"{nc}:g.{pos}_{e}delins{alt}" if e > pos else f"{nc}:g.{pos}delins{alt}"


def car_lookup(hgvs):
    """ClinGen Allele Registry：HGVS → CA ID、GRCh38 坐标、gnomAD_4 ID（若 gnomAD 收录）。"""
    try:
        d = json.loads(http(f"{CAR}?hgvs={urllib.parse.quote(hgvs, safe='')}", timeout=60))
    except Exception as e:
        return {"state": "NOT_QUERIED", "error": str(e)}
    if "errorType" in d:
        return {"state": "INVALID", "error": f"{d.get('errorType')}: {d.get('message', '')[:200]}"}
    g38 = next((a for a in d.get("genomicAlleles", []) if a.get("referenceGenome") == "GRCh38"), None)
    ext = d.get("externalRecords") or {}
    return {"state": "OK", "ca": d["@id"].rsplit("/", 1)[-1], "grch38": g38,
            "gnomad4_ids": [x["id"] for x in ext.get("gnomAD_4", [])],
            "gnomad2_ids": [x["id"] for x in ext.get("gnomAD_2", [])],
            "rsids": ["rs" + str(x["rs"]) for x in ext.get("dbSNP", []) if x.get("rs")]}


def car_to_vcf(ref_obj, g38):
    """CAR GRCh38 genomicAllele（0-based 半开，已 3' 右移）→ 左对齐 VCF。"""
    c = g38["coordinates"][0]
    start0, end0, refa, alta = c["start"], c["end"], c.get("referenceAllele", ""), c.get("allele", "")
    if refa and alta and len(refa) == len(alta) == 1:
        return start0 + 1, refa, alta
    anchor = ref_obj.seq(start0, start0)                      # start0 即锚定碱基的 1-based 位置
    return normalize(ref_obj, start0, anchor + refa, anchor + alta)


# ── gnomAD：GraphQL ─────────────────────────────────────────────────
def gql(query):
    out = json.loads(http(GNOMAD_API, {"query": query}))
    if out.get("errors"):
        raise LookupError(out["errors"][0].get("message", ""))
    return out["data"]


def gnomad_graphql(vid):
    pops = "populations{id ac an homozygote_count hemizygote_count}"
    blk = "ac an homozygote_count hemizygote_count filters faf95{popmax popmax_population}"
    q = ('{ variant(variantId:"%s", dataset:gnomad_r4){ variant_id rsids flags '
         'exome{%s flags} genome{%s flags} joint{%s %s} } }') % (vid, blk, blk, blk, pops)
    try:
        v = gql(q)["variant"]
    except LookupError as e:
        if "not found" in str(e).lower():
            return {"hit": False, "source": "graphql"}
        raise
    j = v.get("joint") or {}
    pop = {p["id"]: p for p in j.get("populations") or []}
    return {"hit": True, "source": "graphql", "variant_id": v["variant_id"], "rsids": v.get("rsids") or [],
            "ac": j.get("ac"), "an": j.get("an"), "hom": j.get("homozygote_count"),
            "hemi": j.get("hemizygote_count"),
            "faf95_grpmax": (j.get("faf95") or {}).get("popmax"),
            "faf95_grpmax_pop": (j.get("faf95") or {}).get("popmax_population"),
            "pops": {k: {"ac": pop[k]["ac"], "an": pop[k]["an"], "hom": pop[k]["homozygote_count"],
                         "hemi": pop[k]["hemizygote_count"]} for k in CONTINENTAL + BOTTLENECK if k in pop},
            "filters": {"exome": (v.get("exome") or {}).get("filters"),
                        "genome": (v.get("genome") or {}).get("filters")},
            "in_exome": v.get("exome") is not None, "in_genome": v.get("genome") is not None,
            "flags": v.get("flags") or []}


def gnomad_coverage(chrom, pos):
    q = ('{ region(chrom:"%s", start:%d, stop:%d, reference_genome:GRCh38){ coverage(dataset:gnomad_r4){ '
         'exome{pos mean over_20} genome{pos mean over_20} } } }') % (chrom, pos, pos)
    c = gql(q)["region"]["coverage"]

    def at(rows):
        rows = [r for r in (rows or []) if r["pos"] == pos] or (rows or [])[:1]
        return (rows[0]["mean"], rows[0]["over_20"]) if rows else (None, None)
    em, eo = at(c.get("exome"))
    gm, go = at(c.get("genome"))
    return {"method": "graphql", "exome_mean": em, "exome_over_20": eo, "genome_mean": gm, "genome_over_20": go,
            "ok": max(eo or 0, go or 0) >= COVER_OK}


# ── gnomAD：公共存储桶 joint VCF 远程 tabix（纯 Python）────────────────
_TBI = {}


def _load_tbi(url):
    b = gzip.decompress(http(url + ".tbi", binary=True, timeout=90))
    o = 4
    n_ref = struct.unpack_from("<i", b, o)[0]
    l_nm = struct.unpack_from("<i", b, o + 28)[0]
    o += 32
    names = b[o:o + l_nm].split(b"\0")[:-1]
    o += l_nm
    idx = {}
    for i in range(n_ref):
        nb = struct.unpack_from("<i", b, o)[0]; o += 4
        bins = {}
        for _ in range(nb):
            bn, nc = struct.unpack_from("<Ii", b, o); o += 8
            bins[bn] = [struct.unpack_from("<QQ", b, o + 16 * k) for k in range(nc)]
            o += 16 * nc
        ni = struct.unpack_from("<i", b, o)[0]; o += 4
        lin = struct.unpack_from(f"<{ni}Q", b, o); o += 8 * ni
        idx[names[i].decode()] = (bins, lin)
    return idx


def _reg2bins(beg0, end):
    end -= 1
    out = [0]
    for sh, off in ((26, 1), (23, 9), (20, 73), (17, 585), (14, 4681)):
        out += range(off + (beg0 >> sh), off + (end >> sh) + 1)
    return out


def tabix_rows(chrom, beg, end):
    """返回 joint VCF 中 [beg,end]（1-based）的记录行；依次尝试各镜像。"""
    errs = []
    for tmpl in VCF_MIRRORS:
        url = tmpl.format(c=chrom)
        try:
            if url not in _TBI:
                _TBI[url] = _load_tbi(url)
            bins, lin = _TBI[url][f"chr{chrom}"]
            b0 = beg - 1
            minoff = lin[b0 >> 14] if (b0 >> 14) < len(lin) else 0
            chunks = sorted(c for bn in _reg2bins(b0, end) for c in bins.get(bn, []) if c[1] > minoff)
            if not chunks:
                return [], url
            cs, ce = chunks[0][0] >> 16, (max(c[1] for c in chunks) >> 16) + 65536
            raw = http(url, rng=(cs, ce), binary=True, timeout=90)
            blocks, o = [], 0
            while o + 18 <= len(raw):
                bsize = struct.unpack_from("<H", raw, o + 16)[0] + 1
                if o + bsize > len(raw):
                    break
                blocks.append(zlib.decompress(raw[o + 18:o + bsize - 8], -15))
                o += bsize
            text = b"".join(blocks)[chunks[0][0] & 0xFFFF:]
            rows = []
            for line in text.split(b"\n"):
                f = line.split(b"\t", 8)
                if len(f) < 8 or f[0] != f"chr{chrom}".encode():
                    continue
                p = int(f[1])
                if p > end:
                    break
                if p >= beg:
                    rows.append(line.decode())
            return rows, url
        except Exception as e:
            errs.append(f"{url.split('/')[2]}: {e}")
    raise RuntimeError("; ".join(errs))


def _info(row):
    f = row.split("\t")
    info = dict(kv.split("=", 1) if "=" in kv else (kv, "1") for kv in f[7].split(";"))
    return f, info


def parse_vcf_record(row, chrom):
    f, info = _info(row)
    num = lambda k: (float(info[k]) if "." in info[k] or "e" in info[k] else int(info[k])) if k in info else None
    pops = {}
    for p in CONTINENTAL + BOTTLENECK:
        if f"AN_joint_{p}" in info:
            pops[p] = {"ac": num(f"AC_joint_{p}"), "an": num(f"AN_joint_{p}"), "hom": num(f"nhomalt_joint_{p}"),
                       "hemi": num(f"AC_joint_{p}_XY") if chrom == "X" else 0}
    return {"hit": True, "source": "tabix", "variant_id": f"{chrom}-{f[1]}-{f[3]}-{f[4]}",
            "rsids": [] if f[2] == "." else f[2].split(";"),
            "ac": num("AC_joint"), "an": num("AN_joint"), "hom": num("nhomalt_joint"),
            "hemi": num("AC_joint_XY") if chrom == "X" else 0,
            "faf95_grpmax": num("fafmax_faf95_max_joint"), "faf95_grpmax_pop": info.get("fafmax_faf95_max_gen_anc_joint"),
            "pops": pops, "filters": {"vcf_FILTER": f[6], "exome": info.get("exomes_filters"),
                                      "genome": info.get("genomes_filters")},
            "in_exome": "AN_exomes" in info, "in_genome": "AN_genomes" in info, "flags": []}


# ── 频率主流程 ───────────────────────────────────────────────────────
def gnomad_lookup(ref_obj, chrom, pos, ref, alt, car):
    vid = f"{chrom}-{pos}-{ref}-{alt}"
    res = {"variant_id": vid, "dataset": "gnomAD v4.1 joint", "attempts": []}
    rec = None
    # 1) GraphQL
    try:
        rec = gnomad_graphql(vid)
        res["attempts"].append("graphql:ok")
    except Exception as e:
        res["attempts"].append(f"graphql:FAIL({e})")
    # 2) 远程 tabix 窗口：命中回退 + 等价写法扫描 + 覆盖度代理
    span = max(len(ref), len(alt))
    window_rows = None
    try:
        window_rows, url = tabix_rows(chrom, pos - WINDOW, pos + span + WINDOW)
        res["attempts"].append(f"tabix:ok({url.split('/')[2]}, {len(window_rows)} rows)")
    except Exception as e:
        res["attempts"].append(f"tabix:FAIL({e})")
    if rec is None and window_rows is not None:
        hit = [r for r in window_rows if _info(r)[0][1] == str(pos) and _info(r)[0][3] == ref and _info(r)[0][4] == alt]
        rec = parse_vcf_record(hit[0], chrom) if hit else {"hit": False, "source": "tabix"}
    if rec is None:
        res.update(state="NOT_QUERIED", error="GraphQL 与远程 tabix 均失败")
        return res
    # 3) 等价写法 / 同位点 / 重叠变异
    equiv, same_pos, overlap = [], [], []
    if window_rows is not None:
        for r in window_rows:
            f, _ = _info(r)
            p, a, b = int(f[1]), f[3], f[4]
            if (p, a, b) == (pos, ref, alt):
                continue
            try:
                np_ = normalize(ref_obj, p, a, b)
            except Exception:
                np_ = (p, a, b)
            rid = f"{chrom}-{p}-{a}-{b}"
            if np_ == (pos, ref, alt):
                equiv.append(rid)
            elif p == pos:
                same_pos.append(rid)
            elif p <= pos + span - 1 and p + len(a) - 1 >= pos and (len(a) != len(b) or len(ref) != len(alt)):
                overlap.append(rid)
    res["equivalent_records"], res["same_position_other_alleles"], res["overlapping_indels"] = equiv, same_pos, overlap[:10]
    # 4) Allele Registry 交叉核对
    car_ids = (car or {}).get("gnomad4_ids") or []
    res["car_gnomad4_ids"] = car_ids
    if rec["hit"]:
        res.update(state="FOUND", **{k: v for k, v in rec.items() if k != "hit"})
        filt = rec["filters"]
        # 只有"所有收录该变异的数据集都未通过质控"才算 FOUND_FILTERED；一方 PASS 即可用
        if rec["source"] == "graphql":
            sets = {k: filt.get(k) for k, inn in (("exome", rec["in_exome"]), ("genome", rec["in_genome"])) if inn}
            flagged = sets and all(v for v in sets.values())
        else:
            sets = {k: filt.get(k) for k in ("exome", "genome") if filt.get(k)}
            flagged = sets and all(v != "PASS" for v in sets.values())
        if any(sets.values()) and not flagged:
            res["note"] = f"部分数据集质控未通过：{sets}（另一数据集 PASS，频率可用）"
        if flagged:
            res["state"] = "FOUND_FILTERED"
            res["note"] = f"gnomAD 质控未通过：{sets}——频率不可直接作良性证据，也不能当作'缺失'"
        return res
    if equiv:
        res.update(state="REPRESENTATION_MISMATCH",
                   error=f"查询写法未命中，但窗口内存在等价记录 {equiv}——必须改用等价记录重查")
        return res
    if car_ids and vid not in car_ids:
        res.update(state="CONFLICT", error=f"Allele Registry 显示 gnomAD_4 收录 {car_ids}，与本次'未命中'矛盾")
        return res
    # 5) 未命中 → 覆盖度
    try:
        cov = gnomad_coverage(chrom, pos)
    except Exception as e:
        cov = {"method": "graphql", "error": str(e)}
        if window_rows:
            ans = [int(_info(r)[1].get("AN_joint", 0)) for r in window_rows]
            frac = max(ans) / AUTOSOME_FULL_AN if chrom not in ("X", "Y") else None
            cov = {"method": "neighbor_AN_proxy", "max_neighbor_AN": max(ans), "fraction_of_full": frac,
                   "ok": bool(frac and frac >= PROXY_OK), "note": "GraphQL 覆盖度失败，用 ±60bp 内变异 AN 代理"}
    res["coverage"] = cov
    if cov.get("ok"):
        res["state"] = "ABSENT_CONFIRMED"
    elif "error" in cov and cov.get("method") == "graphql":
        res["state"] = "ABSENT_COVERAGE_UNVERIFIED"
    else:
        res["state"] = "ABSENT_LOW_COVERAGE"
    return res


# ── 补充来源 ────────────────────────────────────────────────────────
def dbsnp_freqs(rsid):
    try:
        d = json.loads(http(f"https://api.ncbi.nlm.nih.gov/variation/v0/refsnp/{rsid.lstrip('rs')}"))
    except Exception as e:
        return {"state": "NOT_QUERIED", "error": str(e)}
    out = {}
    for a in d["primary_snapshot_data"]["allele_annotations"]:
        for f in a.get("frequency", []):
            o = f["observation"]
            if o["deleted_sequence"] != o["inserted_sequence"]:
                out.setdefault(f["study_name"], []).append(
                    f"{o['deleted_sequence'] or '-'}>{o['inserted_sequence'] or '-'} {f['allele_count']}/{f['total_count']}")
    return {"state": "OK", "rsid": rsid, "studies": out}


def cspec_rules(gene):
    """ClinGen CSpec：该基因所有 VCEP 规范中频率相关证据的原文。"""
    try:
        specs = json.loads(http(f"{CSPEC}/svis?detail=high", timeout=90))["data"]
    except Exception as e:
        return {"state": "NOT_QUERIED", "error": str(e)}
    hits = [s for s in specs if any(g.get("label") == gene for rs in s.get("ruleSets", []) for g in rs.get("genes", []))]
    if not hits:
        return {"state": "NO_VCEP", "note": f"CSpec 无 {gene} 规范（含在研），按通用规则 + Whiffin 计算"}
    out = []
    for s in hits:
        sid = s["@id"].rsplit("/", 1)[-1]
        item = {"id": sid, "panel": s["affiliation"]["label"], "status": s.get("status"),
                "version": s.get("version"), "url": s.get("url"), "criteria": {}}
        try:
            d = json.loads(http(f"{CSPEC}/SequenceVariantInterpretation/id/{sid}?detail=high", timeout=90))
            for rs in d.get("ruleSets", []):
                for c in rs.get("criteriaCodes", []):
                    if c.get("label") in ("PM2", "BA1", "BS1", "BS2", "PS4", "PM3"):
                        item["criteria"][c["label"]] = [
                            f"[{e['label']}] {e.get('applicability', '')}: " + re.sub(r"\s*\n\s*", " ⏎ ", (e.get('description') or '').strip())
                            for e in c.get("evidenceStrengths", [])
                            if "not applicable" not in (e.get("applicability") or "").lower()] or ["该 VCEP 未启用此证据"]
        except Exception as e:
            item["error"] = str(e)
        out.append(item)
    return {"state": "FOUND", "specs": out}


# ── 阈值计算（Whiffin 2017, PMID 28518168）──────────────────────────
def frac(x):
    if x is None:
        return None
    if "/" in str(x):
        a, b = str(x).split("/")
        return float(a) / float(b)
    return float(x)


def max_credible_af(moi, prev, allelic, genetic, pen):
    if moi == "AD" or moi == "XLD":
        return prev / 2 * allelic * genetic / pen
    if moi in ("AR",):
        return math.sqrt(prev) * allelic * math.sqrt(genetic) / math.sqrt(pen)
    if moi == "XLR":                                  # 男性半合子：每例 1 条致病 X，按 prev（男性）近似
        return prev * allelic * genetic / pen
    raise ValueError(moi)


def poisson_upper_ac(an, af, conf=0.95):
    lam, k, cdf, p = an * af, 0, 0.0, math.exp(-an * af)
    while True:
        cdf += p
        if cdf >= conf:
            return k
        k += 1
        p *= lam / k


# ── 门控 ───────────────────────────────────────────────────────────
def gates(g, moi, maxaf, gene, hgvs_c, cspec):
    out = {}
    st = g["state"]
    has_vcep = cspec and cspec.get("state") == "FOUND"
    vcep_note = "（本基因有 VCEP 规范：以 CSpec 原文阈值为准，下述通用判定仅作参考）" if has_vcep else ""
    if st in ("NOT_QUERIED", "INVALID_INPUT", "CONFLICT", "REPRESENTATION_MISMATCH", "ABSENT_COVERAGE_UNVERIFIED"):
        msg = f"⛔ 无法评估（{st}）：PM2/BA1/BS1/BS2 均不赋值，模块1 扣留结论"
        return {"PM2": msg, "BA1": msg, "BS1": msg, "BS2": msg}
    if st == "ABSENT_LOW_COVERAGE":
        return {"PM2": "⛔ 不赋：位点覆盖不足，'未收录'不可信", "BA1": "不适用", "BS1": "不适用", "BS2": "不适用"}
    if st == "ABSENT_CONFIRMED":
        return {"PM2": "✅ 可赋 PM2_Supporting（gnomAD v4.1 未收录，位点覆盖充分）" + vcep_note,
                "BA1": "不满足", "BS1": "不满足", "BS2": "不满足（gnomAD 无携带者）"}
    # FOUND / FOUND_FILTERED
    faf, ac = g.get("faf95_grpmax") or 0.0, g.get("ac") or 0
    pops = g.get("pops", {})
    grpmax_af = max(((p["ac"] / p["an"]) for k, p in pops.items() if k in CONTINENTAL and p.get("an")), default=0)
    ba1_pop = [k for k, p in pops.items() if k in CONTINENTAL and (p.get("an") or 0) >= 2000 and p["ac"] / p["an"] > 0.05]
    exempt = gene and hgvs_c and any(gene == x and hgvs_c.split(":")[-1].startswith(y) for x, y in BA1_EXCEPTIONS)
    if exempt:
        out["BA1豁免"] = "⚠️ 命中 BA1 豁免名单（Ghosh 2018）：无论频率多高都不启用 BA1，按 VCEP/文献逐条评估"
    if st == "FOUND_FILTERED":
        out["PM2"] = "⛔ 不赋：gnomAD 有该变异但质控未通过——不能视为'缺失'，需人工看 AB/DP 后判断"
        out["BA1"] = out["BS1"] = "⛔ 不赋：质控未通过的频率不作良性证据"
        out["BS2"] = "⛔ 不赋：同上"
        return out
    out["BA1"] = ("⚠️ 频率 >5% 但属 BA1 豁免名单 → 不启用 BA1" if exempt else f"✅ BA1（{ba1_pop} AF>5%，AN≥2000）"
                  ) if ba1_pop else "不满足"
    if maxaf:
        tol_ac = poisson_upper_ac(pops.get(g.get("faf95_grpmax_pop") or "", {}).get("an") or g.get("an") or 0, maxaf)
        out["阈值"] = (f"最大可信 AF={maxaf:.3g}；grpmax FAF95={faf:.3g}（{g.get('faf95_grpmax_pop')}）；"
                      f"grpmax 点估计 AF={grpmax_af:.3g}；该人群 AN 下最大容许 AC≈{tol_ac}")
        out["BS1"] = "✅ BS1（grpmax FAF95 > 最大可信 AF）" + vcep_note if faf > maxaf else "不满足"
        if moi == "AD":
            out["PM2"] = ("✅ PM2_Supporting" if ac == 0 else
                          "⛔ 不赋（AD 默认要求 AC=0；外显不全/迟发病须 VCEP 或书面论证）") + vcep_note
        else:
            out["PM2"] = ("✅ PM2_Supporting（grpmax 点估计 AF < 最大可信 AF）" if grpmax_af < maxaf
                          else "⛔ 不赋（频率不低于阈值）") + vcep_note
        if not out["BS1"].startswith("✅") and not out["PM2"].startswith("✅"):
            out["PM2"] += "；处于 PM2 上限与 BS1 下限之间 → 两条都不赋"
    else:
        out["BS1"] = "⏸ 需阈值：提供 --moi/--prevalence/--allelic 或 VCEP 阈值后判定" + vcep_note
        out["PM2"] = ("⛔ 不赋（AD 且 AC>0）" if moi == "AD" else
                      "⏸ 需阈值：隐性病按 grpmax AF 与最大可信 AF 比较；未给阈值不得凭'很罕见'赋 PM2") + vcep_note
    hom, hemi = g.get("hom") or 0, g.get("hemi") or 0
    out["BS2"] = (f"候选：gnomAD 纯合 {hom} / 半合 {hemi}。仅当疾病早发、完全外显、非亚效等位，且 ≥2 例时考虑；"
                  "gnomAD 个体未做表型评估，产前默认最多作 BS2_Supporting 参考" if (hom or hemi) else "gnomAD 无纯合/半合")
    return out


# ── 主程序 ─────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vid", nargs="?", help="GRCh38 chr-pos-ref-alt")
    ap.add_argument("--hgvs", help="HGVS（NM_:c. 或 NC_:g.），经 Allele Registry 解析")
    ap.add_argument("--gene")
    ap.add_argument("--moi", choices=["AD", "AR", "XLD", "XLR"])
    ap.add_argument("--prevalence"); ap.add_argument("--allelic", type=float)
    ap.add_argument("--genetic", type=float, default=1.0); ap.add_argument("--penetrance", type=float, default=1.0)
    ap.add_argument("--no-cspec", action="store_true"); ap.add_argument("--card", action="store_true")
    a = ap.parse_args()

    out = {"input": a.hgvs or a.vid, "warnings": []}
    car = None
    if a.hgvs:
        car = car_lookup(a.hgvs)
        out["allele_registry"] = car
        if car["state"] != "OK":
            out["gnomad"] = {"state": "INVALID_INPUT" if car["state"] == "INVALID" else "NOT_QUERIED",
                             "error": car.get("error")}
            return emit(out, a, 2)
        chrom = car["grch38"]["chromosome"]
        ref_obj = Ref(chrom)
        pos, ref, alt = car_to_vcf(ref_obj, car["grch38"])
    else:
        m = re.match(r"^(?:chr)?([0-9XY]+)[-:](\d+)[-:]([ACGTN]+)[-:>]([ACGTN]+)$", (a.vid or "").strip(), re.I)
        if not m:
            sys.exit("需要 GRCh38 chr-pos-ref-alt 或 --hgvs")
        chrom, pos, ref, alt = m.group(1).upper(), int(m.group(2)), m.group(3).upper(), m.group(4).upper()
        ref_obj = Ref(chrom)
        try:
            real = ref_obj.seq(pos, pos + len(ref) - 1)
        except Exception as e:
            out["gnomad"] = {"state": "NOT_QUERIED", "error": f"参考序列获取失败，无法校验 REF：{e}"}
            return emit(out, a, 3)
        if real != ref:
            out["gnomad"] = {"state": "INVALID_INPUT",
                             "error": f"REF 不符：输入 {ref}，GRCh38 该处为 {real}（坐标错误或把 hg19 当 hg38）"}
            return emit(out, a, 2)
        n = normalize(ref_obj, pos, ref, alt)
        if n != (pos, ref, alt):
            out["warnings"].append(f"输入未归一化：{chrom}-{pos}-{ref}-{alt} → {chrom}-{n[0]}-{n[1]}-{n[2]}（已自动改用后者）")
            pos, ref, alt = n
        car = car_lookup(vcf_to_hgvs_g(chrom, pos, ref, alt))
        out["allele_registry"] = car
        if car["state"] != "OK":
            out["warnings"].append(f"Allele Registry 交叉核对未完成：{car.get('error')}")
            car = None
    out["normalized"] = f"{chrom}-{pos}-{ref}-{alt}"
    g = gnomad_lookup(ref_obj, chrom, pos, ref, alt, car)
    out["gnomad"] = g
    rs = (g.get("rsids") or []) or ((car or {}).get("rsids") or [])
    out["dbsnp"] = dbsnp_freqs(rs[0]) if rs else {"state": "NO_RSID"}
    cs = cspec_rules(a.gene) if a.gene and not a.no_cspec else None
    out["cspec"] = cs
    maxaf = None
    if a.moi and a.prevalence and a.allelic:
        maxaf = max_credible_af(a.moi, frac(a.prevalence), a.allelic, a.genetic, a.penetrance)
    out["max_credible_af"] = maxaf
    hgvs_c = a.hgvs if a.hgvs and ":c." in a.hgvs else None
    out["gates"] = gates(g, a.moi, maxaf, a.gene, hgvs_c, cs)
    return emit(out, a, 3 if g["state"] == "NOT_QUERIED" else 0)


def emit(out, a, code):
    if not a.card:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        sys.exit(code)
    g = out.get("gnomad", {})
    print("═══ 频率证据取数卡（freq_evidence v2）═══")
    print(f"输入        : {out['input']}")
    car = out.get("allele_registry") or {}
    if car.get("state") == "OK":
        print(f"Allele Reg. : {car['ca']}  gnomAD_4 链接: {car['gnomad4_ids'] or '无'}")
    for w in out.get("warnings", []):
        print(f"⚠️  {w}")
    print(f"归一化坐标  : {out.get('normalized', '—')} (GRCh38)")
    print(f"gnomAD 状态 : {g.get('state')}   尝试: {', '.join(g.get('attempts', [])) or '—'}")
    if g.get("state", "").startswith("FOUND"):
        print(f"  joint     : AC={g['ac']}/AN={g['an']}  hom={g['hom']}  hemi={g['hemi']}  "
              f"grpmax FAF95={g['faf95_grpmax']} ({g['faf95_grpmax_pop']})  来源={g['source']}")
        for k in CONTINENTAL + BOTTLENECK:
            p = g["pops"].get(k)
            if p and p["ac"]:
                tag = "（瓶颈人群，不入 grpmax）" if k in BOTTLENECK else ""
                print(f"  {k:9} : AC={p['ac']}/AN={p['an']}  AF={p['ac'] / p['an']:.3g}  hom={p['hom']}{tag}")
        print(f"  filters   : {g['filters']}  flags={g.get('flags')}")
    elif g.get("coverage"):
        print(f"  覆盖度    : {g['coverage']}")
    if g.get("error"):
        print(f"  错误      : {g['error']}")
    for k in ("equivalent_records", "same_position_other_alleles", "overlapping_indels"):
        if g.get(k):
            print(f"  {k}: {g[k]}")
    d = out.get("dbsnp") or {}
    if d.get("state") == "OK":
        eas = {k: v for k, v in d["studies"].items() if k in EAS_STUDIES}
        print(f"dbSNP {d['rsid']} : " + "; ".join(f"{k} {v[0]}" for k, v in eas.items()))
    cs = out.get("cspec")
    if cs:
        print(f"CSpec VCEP  : {cs['state']}")
        for s in cs.get("specs", []):
            print(f"  ▸ {s['id']} {s['panel']} v{s.get('version')} [{s.get('status')}] {s.get('url')}")
            for crit, lines in s.get("criteria", {}).items():
                for ln in lines:
                    print(f"      {crit}: {ln[:400]}")
        if cs.get("note"):
            print(f"  {cs['note']}")
    print("── 门控 ──")
    for k, v in (out.get("gates") or {}).items():
        print(f"  {k:5}: {v}")
    if g.get("state") in ("NOT_QUERIED", "INVALID_INPUT", "CONFLICT", "REPRESENTATION_MISMATCH"):
        print("  ⛔ 所有频率证据无法评估；模块1 扣留结论")
    sys.exit(code)


if __name__ == "__main__":
    main()
