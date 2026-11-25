#!/usr/bin/env python3
"""
freq_repeat_lookup.py — PM2 / BA1 / BS1 / PM4 / BP3 的结构化取数与门控（2026-09-28 新增）

⚠️ 2026-09-29 起频率（gnomAD 部分）以 freq_evidence.py 为准：本脚本不核对 REF、不做左对齐，
   对非左对齐写法或错误坐标会误报 ABSENT_CONFIRMED。本脚本只用于 ClinVar 与重复区/蛋白窗口，
   输入请用 freq_evidence.py 输出的归一化坐标。

动机（CUL7 c.4126_4128del 事故复盘）：
  旧流程用 HGVS 文字 web_search 查 gnomAD/ClinVar，indel 几乎搜不到 →
  "没查到" 被当成 "不存在" → 错赋 PM2_Supporting；
  PM4 以 "未检索到位于重复区的证据" 为由赋值，从未读取序列 → 漏判 (TCC)n 重复 / poly-Glu。
  实际：gnomAD v4 AC=77、EAS FAF95=6.34e-4；ClinVar VCV587529 VUS★★；RepeatMasker (TCC)n。

本脚本只用标准化坐标/rsID 查询结构化接口，并对每一路返回三态：
  FOUND / ABSENT_CONFIRMED（查询成功且确无记录）/ NOT_QUERIED（接口失败——绝不等同于"无"）

用法：
  python3 freq_repeat_lookup.py 6-43040321-TCTC-T --gene CUL7 --aa-pos 1376 --aa-ref E
  python3 freq_repeat_lookup.py chr6-43040321-TCTC-T --gene CUL7 --aa-pos 1376 --card
坐标须为 GRCh38（取自 VariantValidator / EV.coords.hg38），VCF 左对齐。
"""
import sys, json, ssl, argparse, re, subprocess, time, urllib.parse, urllib.request

GNOMAD = "https://gnomad.broadinstitute.org/api"
UCSC = "https://api.genome.ucsc.edu/getData"
CONTINENTAL = {"afr", "amr", "asj", "eas", "fin", "mid", "nfe", "sas", "ami", "remaining"}
COVER_OK = 0.9          # 该位点 ≥20x 样本比例 ≥90% 才认可 "gnomAD 确无"
FLANK_NT = 30
FLANK_AA = 10


def _http(url, data=None, timeout=40, retries=3):
    """带重试 + curl 回退（本机 Python 可能缺根证书；与 genebe_fields.py 同策略）。"""
    last = None
    for i in range(retries):
        try:
            return _http_once(url, data, timeout)
        except Exception as e:
            last = e
            if i < retries - 1:
                time.sleep(1.5 * (i + 1))
    raise last


def _http_once(url, data, timeout):
    headers = {"User-Agent": "gvp-freq-repeat/1.0", "Accept": "application/json"}
    body = json.dumps(data).encode() if data is not None else None
    if body is not None:
        headers["Content-Type"] = "application/json"
    try:
        req = urllib.request.Request(url, data=body, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as r:
            return r.read().decode()
    except Exception:
        cmd = ["curl", "-s", "-f", "-m", str(timeout), url, "-H", "Accept: application/json"]
        if body is not None:
            cmd += ["-H", "Content-Type: application/json", "--data-binary", body.decode()]
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        if out.returncode != 0 or not out.stdout.strip():
            raise RuntimeError(f"curl 失败(rc={out.returncode}): {out.stderr.strip() or 'empty'}")
        return out.stdout


def _gql(query):
    out = json.loads(_http(GNOMAD, {"query": query}))
    if out.get("errors"):
        raise RuntimeError(out["errors"][0].get("message"))
    return out["data"]


def parse_vid(s):
    m = re.match(r"^(?:chr)?([0-9XYM]+)[-:](\d+)[-:]([ACGTN]+)[-:>]([ACGTN]+)$", s.strip(), re.I)
    if not m:
        sys.exit(f"无法解析坐标 {s!r}；需 GRCh38 chr-pos-ref-alt")
    c, p, r, a = m.groups()
    return c.upper(), int(p), r.upper(), a.upper()


# ── gnomAD 频率 ──────────────────────────────────────────────
def gnomad_freq(chrom, pos, ref, alt, dataset="gnomad_r4"):
    vid = f"{chrom}-{pos}-{ref}-{alt}"
    q = ('{ variant(variantId:"%s", dataset:%s){ variant_id rsids '
         'exome{ac an homozygote_count hemizygote_count filters faf95{popmax popmax_population}} '
         'genome{ac an homozygote_count hemizygote_count filters faf95{popmax popmax_population}} '
         'joint{ac an homozygote_count hemizygote_count faf95{popmax popmax_population} '
         'populations{id ac an homozygote_count}} } }') % (vid, dataset)
    try:
        v = _gql(q)["variant"]
    except Exception as e:
        msg = str(e)
        if "not found" not in msg.lower():
            return {"state": "NOT_QUERIED", "error": msg, "variant_id": vid}
        v = None
    if v:
        j = v.get("joint") or {}
        pops = {p["id"]: p for p in (j.get("populations") or []) if p["id"] in CONTINENTAL}
        return {
            "state": "FOUND", "variant_id": vid, "dataset": dataset, "rsids": v.get("rsids") or [],
            "ac": j.get("ac"), "an": j.get("an"),
            "af": (j["ac"] / j["an"]) if j.get("an") else None,
            "homozygotes": j.get("homozygote_count"), "hemizygotes": j.get("hemizygote_count"),
            "grpmax_faf95": (j.get("faf95") or {}).get("popmax"),
            "grpmax_pop": (j.get("faf95") or {}).get("popmax_population"),
            "populations": {k: {"ac": p["ac"], "an": p["an"], "hom": p["homozygote_count"],
                                "af": p["ac"] / p["an"] if p["an"] else None} for k, p in pops.items()},
            "filters": {"exome": (v.get("exome") or {}).get("filters"),
                        "genome": (v.get("genome") or {}).get("filters")},
        }
    # 变异不在 gnomAD → 必须核查覆盖度才可称 "确无"
    cov = gnomad_coverage(chrom, pos, dataset)
    if cov.get("error"):
        return {"state": "NOT_QUERIED", "variant_id": vid,
                "error": "变异未返回且覆盖度查询失败：" + cov["error"]}
    ok = max(cov.get("exome_over_20") or 0, cov.get("genome_over_20") or 0) >= COVER_OK
    return {"state": "ABSENT_CONFIRMED" if ok else "ABSENT_LOW_COVERAGE",
            "variant_id": vid, "dataset": dataset, "coverage": cov}


def gnomad_coverage(chrom, pos, dataset="gnomad_r4"):
    q = ('{ region(chrom:"%s", start:%d, stop:%d, reference_genome:GRCh38){ coverage(dataset:%s){ '
         'exome{pos mean over_20} genome{pos mean over_20} } } }') % (chrom, pos, pos, dataset)
    try:
        c = _gql(q)["region"]["coverage"]
    except Exception as e:
        return {"error": str(e)}

    def at(rows):
        rows = [r for r in (rows or []) if r["pos"] == pos] or (rows or [])[:1]
        return (rows[0]["mean"], rows[0]["over_20"]) if rows else (None, None)
    em, eo = at(c.get("exome"))
    gm, go = at(c.get("genome"))
    return {"exome_mean": em, "exome_over_20": eo, "genome_mean": gm, "genome_over_20": go}


# ── ClinVar（按坐标，再按 rsID 回退）─────────────────────────
def clinvar(chrom, pos, ref, alt, rsids):
    vid = f"{chrom}-{pos}-{ref}-{alt}"
    q = ('{ clinvar_variant(variant_id:"%s", reference_genome:GRCh38){ clinvar_variation_id '
         'clinical_significance review_status last_evaluated '
         'submissions{clinical_significance last_evaluated submitter_name} } }') % vid
    try:
        cv = _gql(q)["clinvar_variant"]
        if cv:
            return {"state": "FOUND", "source": "gnomAD-ClinVar mirror", **cv}
        gnomad_ok = True
    except Exception as e:
        gnomad_ok = "not found" in str(e).lower()
        gnomad_err = str(e)
    # rsID → NCBI E-utilities 回退
    for rs in rsids or []:
        try:
            u = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&retmode=json&term="
                 + urllib.parse.quote(rs))
            ids = json.loads(_http(u))["esearchresult"]["idlist"]
            if ids:
                return {"state": "FOUND", "source": f"NCBI esearch {rs}", "clinvar_variation_id": ids[0],
                        "note": "仅取得 VariationID；分类/星级请 web_fetch ClinVar variation 页面补全"}
        except Exception:
            pass
    if gnomad_ok:
        return {"state": "ABSENT_CONFIRMED", "note": "gnomAD 镜像按坐标确无 ClinVar 记录（镜像有滞后，最新提交仍需 web 复核）"}
    return {"state": "NOT_QUERIED", "error": gnomad_err}


# ── 序列上下文与重复注释（PM4 / BP3）────────────────────────
def repeat_context(chrom, pos, ref, alt):
    """VCF 左对齐坐标；受影响区间 = 首个锚定碱基之后的缺失/插入位点。"""
    start0 = pos - 1
    span_end = pos + max(len(ref), len(alt)) - 1
    ch = "chr" + chrom
    res = {"affected": f"{ch}:{pos + 1}-{span_end}" if len(ref) != len(alt) else f"{ch}:{pos}"}
    try:
        s = json.loads(_http(f"{UCSC}/sequence?genome=hg38;chrom={ch};start={start0 - FLANK_NT};end={span_end + FLANK_NT}"))
        seq = s["dna"]
        i = FLANK_NT
        res["context"] = seq[:i] + "[" + seq[i:i + len(ref)] + "]" + seq[i + len(ref):]
        res["softmasked_at_site"] = any(c.islower() for c in seq[i:i + len(ref)])
    except Exception as e:
        res["context_error"] = str(e)
    hits, errs = [], []
    for track in ("rmsk", "simpleRepeat"):
        try:
            d = json.loads(_http(f"{UCSC}/track?genome=hg38;track={track};chrom={ch};start={start0};end={span_end}"))
            for r in d.get(track, []):
                hits.append({"track": track, "start": r.get("genoStart", r.get("chromStart")) + 1,
                             "end": r.get("genoEnd", r.get("chromEnd")),
                             "name": r.get("repName") or r.get("sequence"),
                             "class": r.get("repClass") or f"period={r.get('period')}"})
        except Exception as e:
            errs.append(f"{track}: {e}")
    res["repeat_hits"] = hits
    if errs and not hits and "context" not in res:
        res["state"] = "NOT_QUERIED"
    elif hits or res.get("softmasked_at_site"):
        res["state"] = "IN_REPEAT"
    elif errs:
        res["state"] = "PARTIAL"      # 某轨道失败且未命中 → 不能断言 "非重复区"
    else:
        res["state"] = "NOT_IN_REPEAT"
    if errs:
        res["errors"] = errs
    return res


def protein_context(gene, aa_pos, aa_ref=None):
    try:
        u = ("https://rest.uniprot.org/uniprotkb/search?format=tsv&fields=accession,length,sequence&query="
             + urllib.parse.quote(f"gene_exact:{gene} AND organism_id:9606 AND reviewed:true"))
        rows = [r.split("\t") for r in _http(u).strip().splitlines()[1:]]
        acc, length, seq = rows[0]
    except Exception as e:
        return {"state": "NOT_QUERIED", "error": str(e)}
    i = aa_pos - 1
    if i >= len(seq):
        return {"state": "ISOFORM_MISMATCH", "uniprot": acc, "length": int(length),
                "note": "UniProt 典型异构体长度不足，编号与 MANE 不一致，须人工比对"}
    lo, hi = max(0, i - FLANK_AA), min(len(seq), i + FLANK_AA + 1)
    aa = seq[i]
    # 以变异残基为中心的同一氨基酸连续串长度
    l = i
    while l > 0 and seq[l - 1] == aa:
        l -= 1
    r = i
    while r + 1 < len(seq) and seq[r + 1] == aa:
        r += 1
    win = seq[lo:hi]
    res = {"uniprot": acc, "length": int(length), "residue": aa,
           "window": f"{lo + 1}:{win[:i - lo]}[{aa}]{win[i - lo + 1:]}:{hi}",
           "homopolymer": {"aa": aa, "start": l + 1, "end": r + 1, "len": r - l + 1},
           "low_complexity_window": len(set(win)) <= 5}
    if aa_ref and aa_ref.upper() != aa:
        res["state"] = "ISOFORM_MISMATCH"
        res["note"] = f"期望 {aa_ref} 实为 {aa}：UniProt 典型异构体与 MANE 编号不同，须人工比对"
    else:
        res["state"] = "IN_REPEAT" if (r - l + 1) >= 4 or res["low_complexity_window"] else "NOT_IN_REPEAT"
    return res


# ── 门控结论 ──────────────────────────────────────────────
def gates(freq, cv, rep, prot, inframe):
    g = {}
    s = freq["state"]
    g["PM2"] = {
        "FOUND": "以 freq_evidence.py 门控为准（PM2 看 grpmax AF 点估计，BA1/BS1 看 FAF95）",
        "ABSENT_CONFIRMED": "可赋 PM2_Supporting（gnomAD 确无且位点覆盖充分）",
        "ABSENT_LOW_COVERAGE": "⛔ 不可赋：位点覆盖不足，'未检出' 不可信",
        "NOT_QUERIED": "⛔ 不可赋：gnomAD 未成功查询。缺数据 = 无法评估，不是 AF=0",
    }[s]
    g["ClinVar"] = {"FOUND": "有记录——必须写入模块4，禁止写 '无条目/novel'",
                    "ABSENT_CONFIRMED": "可写 '坐标查询无 ClinVar 记录'",
                    "NOT_QUERIED": "⛔ 只能写 '未能查询'，禁止写 '无条目/novel'"}[cv["state"]]
    if inframe:
        states = {rep.get("state"), prot.get("state") if prot else None}
        if "IN_REPEAT" in states:
            g["PM4"] = "⛔ 不可赋：位于重复/低复杂度区"
            g["BP3"] = "候选：重复区框内 indel；须再确认该区无已知功能（结构域/热点/保守性）"
        elif rep.get("state") == "NOT_IN_REPEAT" and (prot is None or prot.get("state") == "NOT_IN_REPEAT"):
            g["PM4"] = "可赋（单个氨基酸缺失/插入且非关键残基 → 考虑 PM4_Supporting）"
            g["BP3"] = "不适用"
        else:
            g["PM4"] = "⛔ 不可赋：序列上下文未完整核查（NOT_QUERIED/PARTIAL/ISOFORM_MISMATCH）"
            g["BP3"] = "⛔ 不可赋：同上"
    return g


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vid", help="GRCh38 chr-pos-ref-alt（VCF 左对齐）")
    ap.add_argument("--gene")
    ap.add_argument("--aa-pos", type=int, help="MANE 蛋白位置（框内 indel 必填）")
    ap.add_argument("--aa-ref", help="该位置期望氨基酸单字母，用于核对异构体编号")
    ap.add_argument("--dataset", default="gnomad_r4")
    ap.add_argument("--card", action="store_true")
    a = ap.parse_args()

    chrom, pos, ref, alt = parse_vid(a.vid)
    inframe = len(ref) != len(alt) and (len(ref) - len(alt)) % 3 == 0
    freq = gnomad_freq(chrom, pos, ref, alt, a.dataset)
    cv = clinvar(chrom, pos, ref, alt, freq.get("rsids"))
    rep = repeat_context(chrom, pos, ref, alt)
    prot = protein_context(a.gene, a.aa_pos, a.aa_ref) if (a.gene and a.aa_pos) else None
    out = {"input": a.vid, "inframe_indel": inframe, "gnomad": freq, "clinvar": cv,
           "repeat": rep, "protein": prot, "gates": gates(freq, cv, rep, prot, inframe)}

    if not a.card:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    f = freq
    print("═══ 频率 / ClinVar / 重复区 取数卡 ═══")
    print(f"变异       : {out['input']}  (GRCh38, {a.dataset})")
    if f["state"] == "FOUND":
        print(f"gnomAD     : FOUND  AC={f['ac']}/AN={f['an']}  hom={f['homozygotes']}  "
              f"grpmax FAF95={f['grpmax_faf95']} ({f['grpmax_pop']})  rs={','.join(f['rsids'])}")
        eas = f["populations"].get("eas")
        if eas:
            print(f"  EAS      : AC={eas['ac']}/AN={eas['an']}  AF={eas['af']:.3g}")
    else:
        print(f"gnomAD     : {f['state']}  {f.get('coverage') or f.get('error')}")
    print(f"ClinVar    : {cv['state']}  {cv.get('clinvar_variation_id', '')} "
          f"{cv.get('clinical_significance', '')} {cv.get('review_status', '')}")
    print(f"重复注释   : {rep.get('state')}  {rep.get('repeat_hits')}")
    if rep.get("context"):
        print(f"  序列     : {rep['context']}   (小写=RepeatMasker 屏蔽)")
    if prot:
        print(f"蛋白       : {prot.get('state')}  {prot.get('window', prot.get('error'))}  "
              f"同残基串长={prot.get('homopolymer', {}).get('len')}")
    print("── 门控 ──")
    for k, v in out["gates"].items():
        print(f"  {k:7}: {v}")


if __name__ == "__main__":
    main()
