#!/usr/bin/env python3
"""Render a ten-section offline draft from an audited score input, never sign a report."""
import argparse
import json
from pathlib import Path
from score import score
from report_audit import citation_coverage, sample_qc
from review_helpers import pm3, pp1pp4, functional
from locus_review import calculate as locus_calculate
from pvs1_review import evaluate as pvs1_evaluate


def clean(value):
    if value is None: return '未提供/未评估'
    return str(value).replace('|','\\|').replace('\n','；').replace('\r',' ')


def render(data):
    assisted=None
    if 'assisted_case' in data:
        if any(k in data for k in ['case_pipeline','cnv_pipeline','scoring','review_calculations']):raise ValueError('assisted_case owns the evidence pipeline')
        from assisted_case import run as assisted_run
        assisted=assisted_run(data['assisted_case'])
        case=data['assisted_case']['case']
        if data['assisted_case']['framework']=='CNV':case=dict(case,review_mode='autonomous_assist')
        key='cnv_pipeline' if data['assisted_case']['framework']=='CNV' else 'case_pipeline'
        data={**data,key:case}
    pipeline=None
    if 'case_pipeline' in data or 'cnv_pipeline' in data:
        if 'case_pipeline' in data and 'cnv_pipeline' in data:raise ValueError('SNV and CNV pipelines cannot coexist')
        key='cnv_pipeline' if 'cnv_pipeline' in data else 'case_pipeline'
        if key=='cnv_pipeline':
            from cnv_case import run
        else:
            from case_pipeline import run
        if data.get('review_calculations') or 'scoring' in data:raise ValueError('pipeline owns scoring and helper admission; do not provide parallel inputs')
        pipeline=run(data[key])
        if data.get('variant_id')!=data[key].get('identity',{}).get('variant_id'):raise ValueError('pipeline report variant mismatch')
        data=dict(data,scoring=pipeline['assembled_scoring'])
        result=dict(pipeline['score_comparison'])
        result['point_candidate']=pipeline['authoritative_candidate']
        if pipeline['blockers']:
            result.update(point_candidate=None,sandbox_partition=None,blockers=pipeline['blockers'])
        result['primary_framework']=pipeline['authoritative_framework']
        if assisted and assisted['blockers']:
            result.update(point_candidate=None,sandbox_partition=None,blockers=assisted['blockers'],acmg_2015_comparison=dict(candidate=None,status='blocked',reasons=assisted['blockers']))
            pipeline=dict(pipeline,authoritative_candidate=None,blockers=assisted['blockers'])
    else:
        result = score(data['scoring'])
        if result['framework'] != 'SNV':
            result.update(point_candidate=None,sandbox_partition=None,blockers=result['blockers']+['CNV_manual_review_pipeline_required'])
    citations = data.get('citations',[])
    coverage = citation_coverage(citations)
    helper_inputs=data.get('review_calculations',{})
    if not isinstance(helper_inputs,dict): raise ValueError('review_calculations must be an object')
    handlers={'pm3':pm3,'pp1pp4':pp1pp4,'functional':functional,'locus_review':locus_calculate,'pvs1':pvs1_evaluate}
    if set(helper_inputs)-set(handlers): raise ValueError('unsupported review calculation')
    helper_results={k:handlers[k](v) for k,v in helper_inputs.items()}
    if 'locus_review' in helper_results:
        if 'pp1pp4' in helper_results:
            raise ValueError('legacy PP1/PP4 helper and locus packets cannot coexist')
        packets=helper_results['locus_review']['packets']
        if not data.get('variant_id') or not data.get('subject_id'):
            raise ValueError('locus report requires explicit variant_id and subject_id')
        if not any(data['variant_id'] in p['variant_ids'] for p in packets):
            raise ValueError('report variant not present in locus packets')
        if any(p['subject_id']!=data['subject_id'] for p in packets):
            raise ValueError('locus subject mismatch')
        basis={b for p in packets for b in p['basis_ids']}
        for row in data['scoring'].get('evidence',[]):
            if basis & set(row.get('basis_ids',[])):
                raise ValueError('locus evidence overlaps main score; duplicate counting forbidden')
            if str(row.get('code','')).split('_')[0] in ('PP1','PP4','BS4'):
                raise ValueError('locus audit and PP1/PP4/BS4 main evidence cannot coexist in this version')
    if 'pvs1' in helper_inputs:
        p=helper_inputs['pvs1']
        if not data.get('variant_id') or data['variant_id']!=p.get('identity',{}).get('variant_id'):
            raise ValueError('PVS1 report variant identity mismatch')
        basis=set(p.get('basis_ids',[]))
        for row in data['scoring'].get('evidence',[]):
            if basis & set(row.get('basis_ids',[])):
                raise ValueError('PVS1 audit overlaps main evidence')
            if str(row.get('code','')).split('_')[0] in ('PVS1','PM4','PP3'):
                raise ValueError('PVS1 audit cannot coexist with PVS1/PM4/PP3 main evidence in this test version')
    cnv = result['framework'] != 'SNV' 
    if cnv and helper_inputs: raise ValueError('SNV helpers cannot be attached to a CNV score report')
    comparator = result['acmg_2015_comparison']
    lines = ['# 遗传变异致病性分析（v0.6.0-assist 辅助复核）',
        '## 模块 1：Classification Hero',
        '- 正式分类：未完成实验室签发；本输出为独立辅助复核。',
        '- 本次独立辅助评级：'+clean(assisted['independent_classification'] if assisted else None),
        '- 变异：'+clean(data.get('variant')),
        '- 优先核查框架：'+result['primary_framework'],
        '- 测试候选分区：'+clean(result['point_candidate']),
        ('- 已审核条目算术小计（流程阻断时不是完整总分）：' if cnv else '- 积分：')+clean(result['net_points']),
        '- 2015组合对照：'+('不适用（CNV独立框架）' if cnv else clean(comparator.get('candidate'))),
        '- 对照状态：'+clean(comparator.get('status')),
        '- 框架差异：'+clean(result['framework_disagreement']),
        '- 基因—疾病关联：'+clean(data.get('gene_disease_validity')),
        '- 本样本检出可信度：'+clean(data.get('sample_detection_confidence')),
        '- 报告位置：仅建议；待本机构政策审核。',
        '## 模块 2：Molecular Profile',
        clean(data.get('molecular_profile')),
        '样本质控：'+json.dumps(sample_qc(data.get('sample',{})),ensure_ascii=False),
        '## 模块 3：'+('CNV五段式证据链' if cnv else 'ACMG证据链'),
        '| 证据ID | 代码 | 分值 | 原因 |','|---|---|---|---|']
    for r in result['accepted']:
        lines.append('| '+' | '.join(clean(r.get(k)) for k in ('id','code','points','rationale'))+' |')
    if pipeline:
        lines += ['按适用规则审核的候选：'+clean(pipeline['authoritative_candidate']),
                  '通用积分对照（不得覆盖专病结论或流程阻断）：'+clean(None if cnv and pipeline['blockers'] else pipeline['score_comparison']['point_candidate']),
                  '逐例规则检索、辅助重算及审核接入轨迹：','```json',
                  json.dumps({k:pipeline.get(k) for k in ('routing','admission_audit','ba1_exception_check','ba1_threshold_check','blockers')},ensure_ascii=False,indent=2),'```']
    if assisted:
        lines += ['自主证据取舍与外院对照：','```json',json.dumps(assisted['assessment'],ensure_ascii=False,indent=2),'```']
    if helper_results:
        lines += ['辅助计算（未导入主积分；正式证据代码为空）：',
                  '```json',json.dumps(helper_results,ensure_ascii=False,indent=2),'```']
    lines += ['排除项：'+json.dumps(result['excluded'],ensure_ascii=False),
              '阻断项：'+json.dumps(result['blockers'],ensure_ascii=False),
              '组合命中/限制：'+json.dumps(comparator,ensure_ascii=False),
              '## 模块 4：临床数据库综合查询',clean(data.get('database_findings')),
              '## 模块 5：External Benchmarking',clean(data.get('external_benchmarks')),
              '## 模块 6：判读决策报告',
              '积分优先显示，2015组合按已审核强度独立对照；结果不一致时不自动取较高等级。' if not cnv else 'CNV使用独立总分；Section2按已审核事实选择条目，其余各段必须完成逐项人工审核。',
              clean(result['difference_note']),
              '## 模块 7：关联遗传病画像',clean(data.get('disease_profile')),
              '## 模块 8：临床证据补充与产前说明',
              '保留家系、相位、第二打击和随访需求；本草稿不生成个体预后百分比或再发风险数值。',
              clean(data.get('follow_up')),
              '## 模块 9：References',
              '实际核验：'+json.dumps(coverage,ensure_ascii=False)]
    for r in citations:
        lines.append('- '+clean(r.get('id'))+'：'+clean(r.get('citation')))
    lines += ['## 模块 10：局限性声明',
              'AI辅助迁移测试报告；规则适用性、来源和最终结论需专业审核。离线测试不证明临床有效性。',
              'Re-evaluation triggers：新表型、家系、功能数据、数据库或规则版本变化。',
              'Evidence snapshot：'+clean(data.get('snapshot_id'))]
    # Separate paragraphs while preserving contiguous table rows and list items.
    out=[]
    for line in lines:
        if out and not (line.startswith('|') and out[-1].startswith('|')) and not (line.startswith('- ') and out[-1].startswith('- ')):
            out.append('')
        out.append(line)
    return '\n'.join(out)+'\n'

if __name__ == '__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('json_file');ap.add_argument('--output',required=True);a=ap.parse_args()
    Path(a.output).write_text(render(json.loads(Path(a.json_file).read_text())))
