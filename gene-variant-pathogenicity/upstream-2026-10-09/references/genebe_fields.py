#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
genebe_fields.py — gene-variant-pathogenicity 技能的三源取数引擎
================================================================
放置:gene-variant-pathogenicity/references/genebe_fields.py
被谁调用:SKILL.md 的 Step 0.4(见配套 Step_0.4_block.md)

作用:一条 HGVS(转录本:cDNA)→ 三源并跑 → 输出技能 ACMG 专家层可直接消费的"证据结构"。
  · VariantValidator : hg19+hg38 双坐标(权威互证) + 权威 HGVSp
  · GeneBe           : 变异自身 ClinVar 分类 + 自动 ACMG(对标) + AlphaMissense/BayesDel(补 Worker 缺)
  · dbNSFP 5.4a 本地  : T9 上的 tabix 库,REVEL/AlphaMissense/BayesDel/CADD 等优先于在线值(无外发);不可用时回落
  · 五源 Worker       : gnomAD 全局+EAS 精确 AC/AN + 约束 + 全预测(CADD/REVEL/phyloP/SIFT/PolyPhen/SpliceAI) + 同位点地形

命令行:
  python3 references/genebe_fields.py "NM_017780.4:c.2831G>A"            # 默认输出 evidence JSON(供技能)
  python3 references/genebe_fields.py "NM_017780.4:c.2831G>A" --card     # 人看的卡
  python3 references/genebe_fields.py "NM_017780.4:c.2831G>A" --raw      # 完整原始合并 JSON

配置(可选):
  $WORKER_URL / --worker      五源 Worker base URL(默认 DEFAULT_WORKER;你的 host 只存在浏览器,故用 env)
  $GENEBE_KEY / --genebe-key  GeneBe Basic Auth "email:apikey"(防 429)
  $NCBI_KEY                   传给 Worker 以稳住 ClinVar 同位点扫描(若 Worker 支持该参数)

铁律(与技能一致):每源独立容错,单源失败不拖垮;缺失即 None/❌,绝不臆造;
  预测只读 *_score;转录本锚定输入 NM;EAS 原始 AF 仅筛,BA1/BS1 的 FAF95 须另查 gnomAD。
"""

import sys, os, json, ssl, argparse, subprocess, urllib.parse, urllib.request

DEFAULT_WORKER = os.environ.get("WORKER_URL", "https://muddy-cake-9605.yulinj.workers.dev")
VV_BASE = "https://rest.variantvalidator.org/VariantValidator/variantvalidator"
GENEBE = "https://api.genebe.net/cloud/api-public/v1/variant"


# ============================================================ HTTP(curl 回退)
_RETRIES = int(os.environ.get("SRC_RETRIES", "3"))


def _get(url, auth=None, timeout=40):
    """带重试的取数。本机出境链路抖动较多，单次失败不代表源不可用。"""
    import time as _t
    last = None
    for _i in range(_RETRIES):
        try:
            return _get_once(url, auth=auth, timeout=timeout)
        except Exception as e:
            last = e
            if _i < _RETRIES - 1:
                _t.sleep(1.5 * (_i + 1))
    raise last


def _get_once(url, auth=None, timeout=40):
    headers = {"Accept": "application/json"}
    if auth:
        import base64
        headers["Authorization"] = "Basic " + base64.b64encode(auth.encode()).decode()
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as r:
            return json.loads(r.read().decode())
    except Exception:
        cmd = ["curl", "-s", "-m", str(timeout), url, "-H", "Accept: application/json"]
        if auth:
            cmd += ["-u", auth]
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        if out.returncode != 0 or not out.stdout.strip():
            raise RuntimeError(f"curl 失败: {out.stderr.strip() or 'empty'}")
        return json.loads(out.stdout)


# ============================================================ 源 1:VariantValidator
def src_variantvalidator(hgvs):
    enc = urllib.parse.quote(hgvs, safe="")
    d = _get(f"{VV_BASE}/GRCh38/{enc}/all")
    for _, val in d.items():
        if isinstance(val, dict) and "primary_assembly_loci" in val:
            loci = val["primary_assembly_loci"]

            def vcf(asm):
                v = (loci.get(asm) or {}).get("vcf")
                if isinstance(v, dict):
                    return dict(chr=str(v.get("chr")), pos=str(v.get("pos")),
                                ref=v.get("ref"), alt=v.get("alt"))
                if isinstance(v, str) and v.count("-") == 3:
                    c, p, r, a = v.split("-"); return dict(chr=c, pos=p, ref=r, alt=a)
                return None

            prot = val.get("hgvs_predicted_protein_consequence") or {}
            return {"hg19": vcf("grch37"), "hg38": vcf("grch38"),
                    "hgvs_c": val.get("hgvs_transcript_variant"),
                    "hgvs_p": prot.get("tlr") or prot.get("slr"),
                    "transcript": (val.get("hgvs_transcript_variant") or hgvs).split(":")[0]}
    raise RuntimeError("无 primary_assembly_loci(变异描述可能有误)")


# ============================================================ 源 2:GeneBe
def src_genebe(coord, transcript, auth=None):
    qs = urllib.parse.urlencode(dict(chr=coord["chr"], pos=coord["pos"], ref=coord["ref"],
                                     alt=coord["alt"], genome="hg38", useEnsembl="False"))
    d = _get(f"{GENEBE}?{qs}", auth=auth)
    v = (d.get("variants") or [d])[0] if isinstance(d, dict) else {}
    cons = v.get("consequences") or []
    pick = next((c for c in cons if (c.get("transcript") or c.get("feature")) == transcript),
                cons[0] if cons else {})
    by_gene = (v.get("acmg_by_gene") or [{}])[0]
    return {
        "hgvs_p": pick.get("hgvs_p"), "dbsnp": v.get("dbsnp"),
        "acmg_class": v.get("acmg_classification") or by_gene.get("verdict"),
        "acmg_criteria": v.get("acmg_criteria"), "acmg_score": v.get("acmg_score"),
        "clinvar_class": v.get("clinvar_classification"), "clinvar_stars": v.get("clinvar_review_status"),
        "clinvar_subs": v.get("clinvar_submissions_summary"), "clinvar_disease": v.get("clinvar_disease"),
        # 补 Worker 缺的预测(只读 *_score)
        "alphamissense": v.get("alphamissense_score"), "bayesdel_noaf": v.get("bayesdelnoaf_score"),
    }


# ============================================================ 源 4:本地 dbNSFP 5.4a(tabix)
# 完全本地查询(无外发)。库在 T9 外置盘；未挂载/无 tabix 时返回 None,由调用方回落在线源。
DBNSFP54_DEFAULT = "/Volumes/T9/genomics/refs/annot/dbNSFP/5.4a/dbNSFP5.4a_grch38.gz"
_DB54_FIELDS = ["REVEL_score", "AlphaMissense_score", "AlphaMissense_pred", "CADD_phred", "CADD_raw",
                "BayesDel_noAF_score", "BayesDel_addAF_score", "MetaRNN_score", "MetaRNN_pred",
                "PrimateAI_score", "SIFT_score", "SIFT_pred", "Polyphen2_HDIV_score", "Polyphen2_HDIV_pred",
                "Polyphen2_HVAR_score", "VARITY_R_score", "ESM1b_score", "ESM1b_pred",
                "gnomAD4.1_joint_AF", "gnomAD4.1_joint_AC", "gnomAD4.1_joint_AN", "gnomAD4.1_joint_POPMAX_AF"]
_DB54_MIN = {"SIFT_score"}                      # 越小越有害；其余数值取最大(最不利于良性)
_DB54_PRIO = {c: i for i, c in enumerate("DPATB")}


def _find_tabix():
    import shutil
    for c in (os.environ.get("TABIX_BIN"), shutil.which("tabix"),
              os.path.expanduser("~/miniforge3/envs/trio/bin/tabix")):
        if c and os.path.exists(c):
            return c
    return None


def src_dbnsfp_local(coord):
    db = os.environ.get("DBNSFP54_TABIX", DBNSFP54_DEFAULT)
    tabix = _find_tabix()
    if not (os.path.exists(db) and os.path.exists(db + ".tbi")):
        raise RuntimeError(f"dbNSFP 5.4a 不可用(T9 未挂载?): {db}")
    if not tabix:
        raise RuntimeError("找不到 tabix(设 TABIX_BIN 或装入 PATH)")
    chrom = str(coord["chr"]).replace("chr", ""); pos = int(coord["pos"])   # 5.4a contig 无 chr 前缀
    hdr = subprocess.run([tabix, "-H", db], capture_output=True, text=True, timeout=60).stdout.splitlines()[0]
    col = {n: i for i, n in enumerate(hdr.lstrip("#").split("\t"))}
    out = subprocess.run([tabix, db, f"{chrom}:{pos}-{pos}"], capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise RuntimeError(f"tabix 失败: {out.stderr.strip()[:100]}")
    rows = [r.split("\t") for r in out.stdout.splitlines()]
    rows = [r for r in rows if r[col["ref"]] == coord["ref"] and r[col["alt"]] == coord["alt"]]
    if not rows:
        return {"found": False, "note": "5.4a 无此等位记录(非错义/剪接位点 SNV,或为 indel,dbNSFP 不覆盖)"}
    res = {"found": True, "version": "5.4a"}
    for f in _DB54_FIELDS:
        vals = [v for r in rows for v in r[col[f]].split(";") if v not in (".", "")]
        if not vals:
            res[f] = None; continue
        if f.endswith("_pred"):
            known = [v for v in vals if v in _DB54_PRIO]
            res[f] = min(known, key=_DB54_PRIO.get) if known else vals[0]
            continue
        try:
            nums = [float(v) for v in vals]
            res[f] = min(nums) if f in _DB54_MIN else max(nums)
        except ValueError:
            res[f] = vals[0]
    return res


# ============================================================ 源 3:五源 Worker
def src_worker(hgvs, worker_url, dataset="gnomad_r4"):
    enc = urllib.parse.quote(hgvs, safe="")
    url = f"{worker_url.rstrip('/')}/annotate?hgvs={enc}&dataset={dataset}"
    if os.environ.get("NCBI_KEY"):
        url += f"&ncbi_key={os.environ['NCBI_KEY']}"   # 若 Worker 支持,稳住 ClinVar 扫描
    return _get(url)


# ============================================================ 编排
def annotate(hgvs, worker_url=DEFAULT_WORKER, genebe_auth=None, dataset="gnomad_r4"):
    err = {}
    try: wk = src_worker(hgvs, worker_url, dataset)
    except Exception as e: wk, err["worker"] = None, str(e)[:120]
    try: vv = src_variantvalidator(hgvs)
    except Exception as e: vv, err["variantvalidator"] = None, str(e)[:120]

    coord = (vv or {}).get("hg38")
    if not coord and wk and wk.get("coord"):
        w = wk["coord"]; coord = dict(chr=str(w["chr"]), pos=str(w["pos"]), ref=w["ref"], alt=w["alt"])
    transcript = (vv or {}).get("transcript") or hgvs.split(":")[0]
    if coord:
        try: gb = src_genebe(coord, transcript, auth=genebe_auth)
        except Exception as e: gb, err["genebe"] = None, str(e)[:120]
    else:
        gb, err["genebe"] = None, "无 hg38 坐标"

    if coord:
        try: db54 = src_dbnsfp_local(coord)
        except Exception as e: db54, err["dbnsfp54_local"] = None, str(e)[:120]
    else:
        db54, err["dbnsfp54_local"] = None, "无 hg38 坐标"

    return {"input": hgvs,
            "_sources": {k: ("ok" if v else f"❌ {err.get(k,'')}")
                         for k, v in [("variantvalidator", vv), ("genebe", gb), ("worker", wk),
                                      ("dbnsfp54_local", db54)]},
            "_raw": {"variantvalidator": vv, "genebe": gb, "worker": wk, "dbnsfp54_local": db54}}


# ============================================================ 预消化为技能证据结构
def to_evidence(card):
    """把三源合并结果映射为技能各模块直接可用的证据块。缺失即 None/❌,不臆造。"""
    vv = card["_raw"]["variantvalidator"] or {}
    gb = card["_raw"]["genebe"] or {}
    wk = card["_raw"]["worker"] or {}
    g = wk.get("gnomad") or {}
    coord = wk.get("coord") or {}

    # 预测:Worker 列表(去重,读 value) + GeneBe 补 AlphaMissense/BayesDel
    preds = {}
    for pr in (wk.get("merged_predictors") or []):
        preds.setdefault(pr.get("id"), {"value": pr.get("value"), "source": pr.get("source")})
    if gb.get("alphamissense") is not None:
        preds["ALPHAMISSENSE"] = {"value": gb["alphamissense"], "source": "GeneBe"}
    if gb.get("bayesdel_noaf") is not None:
        preds["BAYESDEL_NOAF"] = {"value": gb["bayesdel_noaf"], "source": "GeneBe"}

    # 本地 dbNSFP 5.4a 优先(同名键覆盖在线值；在线源仅作回落)。多转录本已归并为"最不利于良性"一端。
    d54 = card["_raw"].get("dbnsfp54_local") or {}
    if d54.get("found"):
        _m = {"REVEL": "REVEL_score", "ALPHAMISSENSE": "AlphaMissense_score",
              "BAYESDEL_NOAF": "BayesDel_noAF_score", "METARNN": "MetaRNN_score",
              "PRIMATEAI": "PrimateAI_score", "VARITY_R": "VARITY_R_score", "ESM1B": "ESM1b_score",
              "CADD_PHRED": "CADD_phred"}
        for k, f in _m.items():
            if d54.get(f) is not None:
                preds[k] = {"value": d54[f], "source": "dbNSFP5.4a(local)"}

    # 频率提示(仅筛)
    eas_af, glob_af = g.get("eas_af"), g.get("global_af")
    if eas_af is None:
        fhint = None
    elif eas_af >= 0.005:
        fhint = f"EAS AF={eas_af:.4%} 偏高 → 倾向 BS1(须以 gnomAD grpmax FAF95 确认;此为原始AF)"
    elif eas_af == 0 and glob_af in (0, None):
        fhint = "近缺失 → 倾向 PM2"
    else:
        fhint = f"EAS AF={eas_af:.4%}(原始AF,非FAF95)"

    return {
        # Step 0 蛋白强制验证门:VV 权威 HGVSp;GeneBe 交叉
        "protein_gate": {"transcript": vv.get("transcript"), "hgvs_c": vv.get("hgvs_c"),
                         "hgvs_p": vv.get("hgvs_p") or gb.get("hgvs_p"),
                         "hgvs_p_genebe": gb.get("hgvs_p"),
                         "source": "VariantValidator(权威)+GeneBe(交叉)",
                         "passed": bool(vv.get("hgvs_p") or gb.get("hgvs_p"))},
        # 坐标
        "coords": {"hg38": vv.get("hg38") or ({"chr": coord.get("chr"), "pos": coord.get("pos"),
                                               "ref": coord.get("ref"), "alt": coord.get("alt")} if coord else None),
                   "hg19": vv.get("hg19"), "hgvsg38": coord.get("hgvsg"),
                   "rsid": gb.get("dbsnp") or coord.get("rsid")},
        # Step 0.5 ClinVar 分流
        "clinvar": {"classification": gb.get("clinvar_class"), "stars": gb.get("clinvar_stars"),
                    "submissions": gb.get("clinvar_subs"), "disease": gb.get("clinvar_disease")},
        # Step 1.2 频率(EAS 原始 AC/AN;FAF95 须另查)
        "frequency": {"global": {"af": g.get("global_af"), "ac": g.get("global_ac"), "an": g.get("global_an")},
                      "eas": {"af": eas_af, "ac": g.get("eas_ac"), "an": g.get("eas_an")},
                      "hint": fhint,
                      "authority_note": "EAS 为原始 AF;BA1/BS1 的 grpmax FAF95 须查 gnomAD GraphQL/官网"},
        # Step 1.2 预测(读 value=*_score)
        "predictors": preds,
        # 本地 dbNSFP 5.4a 原始归并值(found=False 表示该等位不在库中；None=库不可用,已回落在线源)
        "dbnsfp54": ({"version": "5.4a", **{k: v for k, v in d54.items() if k not in ("found", "version")}}
                     if d54.get("found") else (d54 or None)),
        # 约束(PVS1/PM2/PP2/BP1 背景)
        "constraint": wk.get("constraint"),
        # PS1/PM5 同位点地形
        "codon_landscape": wk.get("codon_landscape"),
        # 模块5 外部对标(不覆盖专家层)
        "acmg_benchmark": {"tool": "GeneBe", "classification": gb.get("acmg_class"),
                           "criteria": gb.get("acmg_criteria"), "score": gb.get("acmg_score")},
        # 元信息
        "_sources": card["_sources"],
        "_warnings": wk.get("warnings"),
        "_needs_manual": ["grpmax FAF95(BA1/BS1)→ gnomAD GraphQL",
                          "中国人群频率(ChinaMAP/WBBC/NyuWa)→ 门户人工"],
        "_rules": {"freq": "EAS 原始 AF 仅筛;FAF95 另查", "pred": "读 *_score 值 + 技能阈值定 PP3/BP4",
                   "acmg": "GeneBe 判定仅对标,不替代技能专家评级",
                   "transcript": "以 VV/GeneBe 的 RefSeq NM 为准"},
    }


# ============================================================ 人看的卡(可选)
def render_card(card):
    ev = to_evidence(card); L = []
    pg, co, fr = ev["protein_gate"], ev["coords"], ev["frequency"]
    hg = lambda d: f"chr{d['chr']}:{d['pos']} {d['ref']}>{d['alt']}" if d else "❌"
    L += ["═" * 60, f"  变异卡 · {card['input']}", "═" * 60,
          f"  转录本  : {pg['transcript'] or '❌'}",
          f"  HGVSc   : {pg['hgvs_c'] or '❌'}",
          f"  HGVSp   : {pg['hgvs_p'] or '❌'}",
          f"  hg38    : {hg(co['hg38'])}    hg19 : {hg(co['hg19'])}",
          f"  rsID    : {co['rsid'] or '❌'}", "─" * 60,
          f"  gnomAD 全局: AF={fr['global']['af']} AC={fr['global']['ac']} AN={fr['global']['an']}",
          f"  gnomAD EAS : AF={fr['eas']['af']} AC={fr['eas']['ac']} AN={fr['eas']['an']}",
          f"  频率提示   : {fr['hint']}", "─" * 60, "  预测(*_score):"]
    for k, val in ev["predictors"].items():
        L.append(f"    {k:<18}{val['value']}  [{val['source']}]")
    L += ["─" * 60,
          f"  ClinVar     : {ev['clinvar']['classification'] or '❌'} ({ev['clinvar']['submissions'] or ''})",
          f"  GeneBe ACMG : {ev['acmg_benchmark']['classification'] or '❌'} "
          f"[{ev['acmg_benchmark']['criteria'] or ''}; {ev['acmg_benchmark']['score']}]",
          f"  同位点地形  : {ev['codon_landscape'] or '❌(见 warnings)'}",
          f"  取数状态    : {json.dumps(ev['_sources'], ensure_ascii=False)}"]
    if ev["_warnings"]: L.append(f"  警告        : {ev['_warnings']}")
    L.append("═" * 60)
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("hgvs")
    ap.add_argument("--worker", default=DEFAULT_WORKER)
    ap.add_argument("--genebe-key", default=os.environ.get("GENEBE_KEY"))
    ap.add_argument("--dataset", default="gnomad_r4")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--card", action="store_true", help="人看的卡")
    g.add_argument("--raw", action="store_true", help="完整原始合并 JSON")
    a = ap.parse_args()
    card = annotate(a.hgvs, a.worker, a.genebe_key, a.dataset)
    if a.card:
        print(render_card(card))
    elif a.raw:
        print(json.dumps(card, ensure_ascii=False, indent=2))
    else:  # 默认:供技能消费的 evidence JSON
        print(json.dumps(to_evidence(card), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
