# Independent offline v0.2 review

Scope: synthetic migration fixtures only; no network, installation, clinical validation, or signing. Package unchanged. Ran package unittest suite with PYTHONDONTWRITEBYTECODE=1: 73 tests passed.

## Confirmed defects

1. Unsupported SNV codes silently receive point candidates. `unknown_snv.json` uses PS99=10 and `typo_strength.json` uses PP3_Strng=10. Both produce P, no blockers, accepted evidence, while the comparator alone says unavailable. Reproduce with `python3 PACKAGE/scripts/score.py REVIEW/unknown_snv.json`. The contract reserves custom codes for explicit TEST arithmetic; these accidental or unsupported codes are not TEST. Suggested fix: unknown code decoding must reject except an explicitly defined TEST namespace.
2. Evidence Markdown table is broken. Every output line is joined with two newlines, including table header, separator, and evidence rows. See `valid_snv-report.md`. A CommonMark/GFM table needs contiguous lines. Reproduce with `python3 PACKAGE/scripts/render_report.py REVIEW/valid_snv-report-input.json --output REVIEW/reproduced-report.md`. Group each table into a single multiline block before joining sections, or join normal lines once.

## Observed limitation requiring explicit wording

`cnv_snv_code.json` places PVS1=8 in a CNV_GAIN record/rule; scorer accepts it as P with no blockers. CNV rules are wholly caller supplied; the renderer explicitly says it does not assign or identify CNV items. Therefore this is a missing code-family/section audit rather than evidence that an implemented CNV rule is wrong. However, it demonstrates that framework strings alone cannot ensure SNV points were converted to an official CNV item. No official CNV range, section cap, or code validity is machine checked. Report this boundary clearly, or add structural validation if claiming independent CNV auditing.

## Successful paths

- Synthetic SNV PS1+PS3: points LP and 2015 P displayed separately; formal classification null.
- Synthetic Indel PVS1+PM2_Supporting: points LP, 2015 VUS; no silent restoration to Moderate.
- Synthetic CNV loss 2A=1: CNV P candidate, SNV comparator not applicable, formal classification null.
- Missing rule source: evidence excluded and candidate null.
- Empty evidence: candidate null, no_accepted_evidence (not VUS).
- Explicit mixed SNV/CNV evidence: framework mismatch excluded and entire candidate blocked.
- Annotation unavailable: unresolved gate, no protein consequence use, missing frequency remains null.
- Exact synthetic SNV and Indel annotation fixtures: verified usable consequence; one source: single_source and usable, not double crosschecked; transcript mismatch: unresolved; consequence disagreement: conflict and unusable.
- CNV equivalent one-based closed and zero-based half-open intervals: 100 bp overlap; build mismatch rejected without liftover.
- Reports contain ten modules, null/unknown states and no formal clinical classification; no citations produce null coverage.

## Disclosed limitations, not defects

Reviewed flags do not prove clinical applicability. Annotation real-service schemas are unvalidated; fixtures do not establish real database findings. No automated full CNV rubric, prenatal matrix completion, disease-specific validation, clinical rule review, reference-content verification or sample QC validation is promised. Clinical signing remains unavailable. Missing RULES_V2.md and case-v2.json observed during initial read are being authored by the parent and were not counted as defects.

## Reproduction files

`run.py` builds scoring inputs/results/reports and unavailable annotation checks. `annotation_checks.py` adds exact-matched SNV/Indel, single-source, mismatch and conflict cases. `summary.json` records results. All source/evidence assertions are synthetic.

## Final verification addendum after fixes

The findings above describe the initial package, not its current state. Reran the reproduction harness after the parent changed code, and inspected the changes. Package suite now passes **76/76 tests**.

- Unknown `PS99` and misspelled `PP3_Strng` are excluded with `unsupported_evidence_code`; point candidate is null. Explicit `TEST` and `TEST_ARITHMETIC` remain available only with synthetic applicability. Checked that removing synthetic applicability blocks them.
- CNV `PVS1=8` is excluded with `invalid_CNV_rubric_code`; candidate null. Also independently checked valid-looking `2A=1.01`: rejected as `CNV_item_points_outside_supported_range`.
- Evidence header, separator and two data rows are contiguous in regenerated Markdown. Ten-module structure remains intact. The reported table defect is fixed.
- Previously valid SNV, Indel and CNV arithmetic paths retain their expected candidates, and incomplete/mixed/empty inputs remain blocked.
- RULES_V2.md and case-v2.json now exist; read the new scope documentation and rendered the new case fixture successfully.

No unresolved defect remains from this review's reproduced issues. CNV validation still checks code shape and broad magnitude, not membership/applicability of each specific official rubric item or full section caps. This remains a limitation of the explicitly caller-reviewed arithmetic scope, not a claim of clinical rubric validation. Classification remains null.

`verify_fixes.py` contains the additional assertions. The initial reproduction result/report files were overwritten by the rerun and now represent fixed behavior. No package files were edited and no network used.
