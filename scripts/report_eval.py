#!/usr/bin/env python3
"""Validate saved judging records and derive auditable paired pilot summaries."""
import argparse
from collections import Counter
import json
from pathlib import Path
from statistics import mean

parser=argparse.ArgumentParser()
parser.add_argument('run_dir',type=Path)
args=parser.parse_args()
folder=args.run_dir
cases=json.loads((folder/'cases.json').read_text())
judgments=json.loads((folder/'judgments.json').read_text())
key=json.loads((folder/'key.json').read_text())
ids={c['id'] for c in cases}
assert len(ids)==len(cases)==len(judgments)
assert {j['id'] for j in judgments}==ids==set(key)
for condition in ['baseline','skilled']:
    records=json.loads((folder/f'{condition}.json').read_text())
    assert len(records)==len(ids) and {r['id'] for r in records}==ids
criteria={'correctness','evidence_handling','practical_usefulness','instruction_compliance','relevant_insight'}
rows=[]
for j in judgments:
    assert set(key[j['id']].values())=={'baseline','skilled'}
    scores={}
    for label in ['A','B']:
        assert set(j[label]['scores'])==criteria
        assert all(type(x) is int and 0<=x<=2 for x in j[label]['scores'].values())
        assert j[label]['total']==sum(j[label]['scores'].values())
        scores[key[j['id']][label]]=j[label]
    assert j['preference'] in ['A','B','tie']
    delta=scores['skilled']['total']-scores['baseline']['total']
    rows.append({'id':j['id'],'kind':next(c['kind'] for c in cases if c['id']==j['id']),
                 'baseline':scores['baseline']['total'],'skilled':scores['skilled']['total'],'delta':delta,
                 'preference':'tie' if j['preference']=='tie' else key[j['id']][j['preference']],
                 'baseline_failures':scores['baseline']['failures'],'skilled_failures':scores['skilled']['failures']})
def summarize(group):
    counts=Counter('win' if r['delta']>0 else 'loss' if r['delta']<0 else 'tie' for r in group)
    return {'n':len(group),'baseline_mean':mean(r['baseline'] for r in group),
            'skilled_mean':mean(r['skilled'] for r in group),'mean_paired_delta':mean(r['delta'] for r in group),
            'score_wins':counts['win'],'score_ties':counts['tie'],'score_losses':counts['loss'],
            'preference_counts':dict(Counter(r['preference'] for r in group)),
            'skilled_material_failure_cases':sum(bool(r['skilled_failures']) for r in group)}
summary={'overall':summarize(rows),'subsets':{kind:summarize([r for r in rows if r['kind']==kind]) for kind in sorted({r['kind'] for r in rows})},'cases':rows}
(folder/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
report=f'''# {folder.name.title()} exploratory evaluation

{len(rows)} paired tasks, independently generated baseline and skill-assisted answers, one blinded model judge. Scores are 0–10 under a coarse rubric. All agents inherited the same session model; exact sampling parameters and model revision were not independently recorded. This is not cross-model or human validation.

| Group | Baseline mean | Skill mean | Mean paired difference | Wins / ties / losses |
|---|---:|---:|---:|---|
'''
for label,value in [('Overall',summary['overall']),*summary['subsets'].items()]:
    report+=f"| {label} | {value['baseline_mean']:.2f} | {value['skilled_mean']:.2f} | {value['mean_paired_delta']:+.2f} | {value['score_wins']} / {value['score_ties']} / {value['score_losses']} |\n"
report+='\nBlind pairwise preferences: '+str(summary['overall']['preference_counts'])+'. These can differ from coarse score ties.\n'
report+='\n## Per-case evidence\n\n| Case | Baseline | Skill | Difference | Preference |\n|---|---:|---:|---:|---|\n'
for r in rows:
    report+=f"| {r['id']} | {r['baseline']} | {r['skilled']} | {r['delta']:+} | {r['preference']} |\n"
report+='''
## Interpretation limits

Read the actual answers and `judgments.json`, not just scores. Cases are a small non-random sample; scores are subjective and can saturate. Word limits match, but prompt lengths differ. Cases are batched, so there is possible context carryover. No repeated sampling, neutral equal-length control, human review, latency/cost measurement, or independent model family is included. Method-specific detail can influence a judge even without a clear improvement to the user's decision.

A tie means this judge did not distinguish quality at this resolution; a win does not prove general superiority. Any regression remains in the public record. Use this pilot to guide further testing, not as a success badge. See [the full protocol](../../README.md).
'''
(folder/'REPORT.md').write_text(report)
print(json.dumps(summary['overall'],indent=2))
