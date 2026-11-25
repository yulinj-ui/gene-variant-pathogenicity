#!/usr/bin/env python3
"""Two-source exon boundary check (NCBI GenBank vs Ensembl).

Why this exists
---------------
Exon length errors of one base (e.g. 306 vs 307) flip the reading frame and can
turn an in-frame exon skipping into a false frameshift/NMD. The common cause is
mixing coordinate conventions:

* NCBI GenBank ``exon`` features and Ensembl REST ``Exon`` coordinates are
  1-based, inclusive; length = end - start + 1.
* UCSC BED/genePred (``ncbiRefSeq``) coordinates are 0-based, half-open;
  length = end - start, and converting to 1-based requires start + 1.

This tool reads the same exon from two independent sources, prints the exon
table, and refuses a PASS when the exon count or any exon length differs.

CLI
---
    python3 exon_check.py NM_000214.3 2
    python3 exon_check.py NM_000214.3 2 --json
    python3 exon_check.py NM_000214.3 2 --fixture tests/fixtures/exon-check-jag1.json

The output is a card that can be pasted into ``pvs1_input.json`` as
``exon_check``. ``check(..., genbank_text=..., ensembl_data=...)`` is available
for offline tests.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from source_http import FetchError, fetch_bytes, get_json
except Exception:  # pragma: no cover - source_http is present in scripts/
    FetchError = RuntimeError  # type: ignore
    fetch_bytes = None  # type: ignore
    get_json = None  # type: ignore

NCBI_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
ENSEMBL_LOOKUP = "https://rest.ensembl.org/lookup/symbol/homo_sapiens/{symbol}?expand=1;content-type=application/json"
COORDINATE_NOTE = (
    "GenBank/Ensembl 使用 1-based 闭区间（长度 = end - start + 1）；"
    "UCSC BED/genePred 使用 0-based 半开区间（长度 = end - start，转 1-based 时 start + 1）。"
    "两者不可混用。"
)


class ExonCheckError(ValueError):
    """Invalid input or unparsable source response."""


def _safe_id(value: str, what: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+", value):
        raise ExonCheckError(f"invalid {what}: {value!r}")
    return value


def parse_genbank(text: str) -> Dict[str, Any]:
    """Parse a RefSeq mRNA GenBank record into exons and CDS coordinates.

    ``exon`` and ``CDS`` features are 1-based inclusive, in transcript order.
    """
    if not isinstance(text, str) or "LOCUS" not in text:
        raise ExonCheckError("not a GenBank record")
    locus = re.search(r"^LOCUS\s+(\S+)", text, re.M)
    version = re.search(r"^VERSION\s+(\S+)", text, re.M)
    gene = re.search(r'/gene="([^"]+)"', text)
    exons = [(int(a), int(b)) for a, b in re.findall(r"^     exon\s+(\d+)\.\.(\d+)\s*$", text, re.M)]
    cds = re.search(r"^     CDS\s+(\d+)\.\.(\d+)\s*$", text, re.M)
    if not exons:
        raise ExonCheckError("no exon features in GenBank record")
    if not cds:
        raise ExonCheckError("no CDS feature in GenBank record")
    return {
        "accession": locus.group(1) if locus else (version.group(1) if version else None),
        "version": version.group(1) if version else None,
        "gene": gene.group(1) if gene else None,
        "cds_start": int(cds.group(1)),
        "cds_end": int(cds.group(2)),
        "exons": exons,
    }


def _transcript_exons(transcript: Dict[str, Any]) -> List[Dict[str, Any]]:
    exons = transcript.get("Exon")
    if not isinstance(exons, list) or not exons:
        raise ExonCheckError("Ensembl transcript has no Exon list")
    strand = transcript.get("strand", 1)
    # Ensembl usually returns transcript order, but sort explicitly by strand.
    ordered = sorted(exons, key=lambda e: int(e["start"]), reverse=(strand == -1))
    out = []
    for exon in ordered:
        start, end = int(exon["start"]), int(exon["end"])
        out.append({
            "id": exon.get("id"),
            "start": start,
            "end": end,
            "length": end - start + 1,
            "strand": strand,
        })
    return out


def parse_ensembl_gene(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return protein-coding transcripts with transcript-ordered exons."""
    if not isinstance(data, dict) or not isinstance(data.get("Transcript"), list):
        raise ExonCheckError("not an Ensembl gene lookup response")
    out = []
    for transcript in data["Transcript"]:
        if not isinstance(transcript, dict):
            continue
        if transcript.get("biotype") not in (None, "protein_coding"):
            continue
        exons = _transcript_exons(transcript)
        translation = transcript.get("Translation") or {}
        out.append({
            "id": transcript.get("id"),
            "display_name": transcript.get("display_name"),
            "strand": transcript.get("strand", 1),
            "is_canonical": transcript.get("is_canonical") in (1, True),
            "translation_length": translation.get("length"),
            "exons": exons,
            "lengths": [e["length"] for e in exons],
        })
    if not out:
        raise ExonCheckError("no protein-coding transcripts in Ensembl response")
    return out


def pick_transcript(ncbi: Dict[str, Any], transcripts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Pick the Ensembl transcript matching the GenBank exon table.

    Exact exon-length matches win; canonical and translation-length matches break
    ties. A non-exact match is still returned so the mismatch can be reported.
    """
    ncbi_lengths = [end - start + 1 for start, end in ncbi["exons"]]
    protein_length = (ncbi["cds_end"] - ncbi["cds_start"] + 1) // 3
    exact = [t for t in transcripts if t["lengths"] == ncbi_lengths]
    if exact:
        exact.sort(key=lambda t: (not t["is_canonical"],
                                  t["translation_length"] != protein_length,
                                  t["id"] or ""))
        chosen = dict(exact[0])
        chosen["mapping"] = "exact_exon_lengths"
        chosen["ambiguous"] = len(exact) > 1
        return chosen
    same_count = [t for t in transcripts if len(t["lengths"]) == len(ncbi_lengths)]
    pool = same_count or transcripts
    pool.sort(key=lambda t: (not t["is_canonical"],
                             t["translation_length"] != protein_length,
                             t["id"] or ""))
    chosen = dict(pool[0])
    chosen["mapping"] = "exon_length_mismatch"
    chosen["ambiguous"] = len(same_count) > 1
    return chosen


def build_card(ncbi: Dict[str, Any], ensembl: Dict[str, Any], exon: int,
               transcript: Optional[str] = None) -> Dict[str, Any]:
    """Build the auditable exon card; raises ExonCheckError on bad input."""
    if not isinstance(exon, int) or exon < 1:
        raise ExonCheckError("exon must be a positive integer")
    if exon > len(ncbi["exons"]):
        raise ExonCheckError(
            f"exon {exon} out of range; {ncbi.get('version') or ncbi.get('accession')} has {len(ncbi['exons'])} exons")
    ncbi_exons = ncbi["exons"]
    ens_exons = ensembl["exons"]
    start, end = ncbi_exons[exon - 1]
    length = end - start + 1
    c_start = start - ncbi["cds_start"] + 1
    c_end = end - ncbi["cds_start"] + 1
    phase = (c_start - 1) % 3 if c_start >= 1 else None
    aa_start = None if c_end < 1 else max(1, (max(c_start, 1) + 2) // 3)
    aa_end = c_end // 3 if c_end >= 3 else None
    mod3 = length % 3

    if phase == 0:
        frame = f"exon starts at a codon boundary (phase 0); {length} mod 3 = {mod3} -> " + (
            "exon skipping is in-frame" if mod3 == 0 else "exon skipping shifts the reading frame")
    elif phase is None:
        frame = "exon starts at/before the CDS start; frame effect requires transcript-level translation"
    else:
        frame = (f"exon starts mid-codon (phase {phase}); length mod 3 = {mod3} alone is insufficient; "
                 "translate the mutant transcript")

    target_ens = ens_exons[exon - 1] if exon <= len(ens_exons) else None
    lengths_match = ensembl["lengths"] == [b - a + 1 for a, b in ncbi_exons]
    exon_count_match = len(ens_exons) == len(ncbi_exons)
    target_match = bool(target_ens and target_ens["length"] == length)
    passed = bool(lengths_match and target_match and exon_count_match)

    messages = []
    if not exon_count_match:
        messages.append(f"exon count mismatch: NCBI {len(ncbi_exons)} vs Ensembl {len(ens_exons)}")
    if not target_match:
        messages.append(
            f"target exon {exon} length mismatch: NCBI {length} nt vs Ensembl "
            f"{target_ens['length'] if target_ens else 'missing'} nt")
    if not lengths_match:
        diffs = []
        for i, (a, b) in enumerate(zip([b - a + 1 for a, b in ncbi_exons], ensembl["lengths"]), 1):
            if a != b:
                diffs.append(f"exon {i}: {a} vs {b}")
        messages.append("exon length differences: " + "; ".join(diffs[:8]))
    if not passed:
        messages.append("do not proceed with PVS1 until the coordinate convention is resolved")

    warnings = [COORDINATE_NOTE]
    if ensembl.get("ambiguous"):
        warnings.append("multiple Ensembl transcripts have identical exon lengths; canonical/first was chosen")

    return {
        "tool": "exon_check",
        "status": "PASS" if passed else "MISMATCH",
        "transcript": transcript or ncbi.get("version") or ncbi.get("accession"),
        "gene": ncbi.get("gene"),
        "exon": exon,
        "exon_count": len(ncbi_exons),
        "ncbi": {
            "accession": ncbi.get("accession"),
            "version": ncbi.get("version"),
            "gene": ncbi.get("gene"),
            "cds_start": ncbi["cds_start"],
            "cds_end": ncbi["cds_end"],
            "start": start,
            "end": end,
            "length": length,
            "c_start": c_start,
            "c_end": c_end,
            "phase": phase,
            "mod3": mod3,
            "aa_start": aa_start,
            "aa_end": aa_end,
            "frame": frame,
        },
        "ensembl": {
            "transcript": ensembl.get("id"),
            "display_name": ensembl.get("display_name"),
            "canonical": bool(ensembl.get("is_canonical")),
            "strand": ensembl.get("strand"),
            "start": target_ens["start"] if target_ens else None,
            "end": target_ens["end"] if target_ens else None,
            "length": target_ens["length"] if target_ens else None,
            "mapping": ensembl.get("mapping"),
        },
        "cross_check": {
            "passed": passed,
            "exon_count_match": exon_count_match,
            "all_exon_lengths_match": lengths_match,
            "target_length_match": target_match,
            "messages": messages,
        },
        "warnings": warnings,
    }


def fetch_genbank(transcript: str) -> str:
    transcript = _safe_id(transcript, "transcript")
    if fetch_bytes is None:
        raise ExonCheckError("source_http.py not available")
    url = f"{NCBI_EFETCH}?db=nuccore&id={urllib.parse.quote(transcript)}&rettype=gb&retmode=text"
    body, _ = fetch_bytes(url, kind="text", timeout=30)
    return body.decode("utf-8-sig")


def fetch_ensembl(gene: str) -> Dict[str, Any]:
    gene = _safe_id(gene, "gene symbol")
    if get_json is None:
        raise ExonCheckError("source_http.py not available")
    url = ENSEMBL_LOOKUP.format(symbol=urllib.parse.quote(gene))
    return get_json(url, timeout=30)


def check(transcript: str, exon: int, *, genbank_text: Optional[str] = None,
          ensembl_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Run the two-source check; network is used only for missing inputs."""
    ncbi = parse_genbank(genbank_text if genbank_text is not None else fetch_genbank(transcript))
    if ensembl_data is None:
        if not ncbi.get("gene"):
            raise ExonCheckError("GenBank record has no gene symbol; cannot query Ensembl")
        ensembl_data = fetch_ensembl(ncbi["gene"])
    transcripts = parse_ensembl_gene(ensembl_data)
    chosen = pick_transcript(ncbi, transcripts)
    return build_card(ncbi, chosen, exon, transcript=transcript)


def format_card(card: Dict[str, Any]) -> str:
    n = card["ncbi"]
    e = card["ensembl"]
    lines = [
        f"exon_check: {card['status']}",
        f"{card['transcript']} ({card.get('gene') or '—'}) exon {card['exon']}/{card['exon_count']}",
        f"NCBI   : {n['start']}..{n['end']} ({n['length']} nt; c.{n['c_start']}..{n['c_end']}; "
        f"phase {n['phase']}; {n['length']} mod 3 = {n['mod3']}; aa {n['aa_start']}-{n['aa_end']})",
        f"Ensembl: {e.get('transcript') or '—'} ({'canonical' if e.get('canonical') else 'non-canonical'}) "
        f"{e.get('start')}..{e.get('end')} ({e.get('length')} nt; strand {e.get('strand')})",
        f"cross-check: exon count {'OK' if card['cross_check']['exon_count_match'] else 'MISMATCH'}; "
        f"all exon lengths {'identical' if card['cross_check']['all_exon_lengths_match'] else 'DIFFER'}; "
        f"target {n['length']} vs {e.get('length')}",
        f"frame: {n['frame']}",
    ]
    if card["cross_check"]["messages"]:
        lines.append("messages: " + " | ".join(card["cross_check"]["messages"]))
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("transcript", help="RefSeq transcript, e.g. NM_000214.3")
    parser.add_argument("exon", type=int, help="exon number in transcript order (1-based)")
    parser.add_argument("--json", action="store_true", help="print the card as JSON")
    parser.add_argument("--fixture", help="JSON fixture with {genbank: str, ensembl: object} for offline checks")
    args = parser.parse_args(argv)

    try:
        if args.fixture:
            fixture = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
            card = check(args.transcript, args.exon,
                         genbank_text=fixture["genbank"], ensembl_data=fixture["ensembl"])
        else:
            card = check(args.transcript, args.exon)
    except (ExonCheckError, FetchError, KeyError, ValueError, OSError) as exc:
        error = {"tool": "exon_check", "status": "ERROR", "transcript": args.transcript,
                 "exon": args.exon, "error": f"{type(exc).__name__}: {exc}"}
        print(json.dumps(error, ensure_ascii=False) if args.json else f"exon_check: ERROR\n{error['error']}")
        return 2

    if args.json:
        print(json.dumps(card, ensure_ascii=False, indent=1))
    else:
        print(format_card(card))
    return 0 if card["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
