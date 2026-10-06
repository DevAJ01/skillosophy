#!/usr/bin/env python3
"""Shortlist repository skill metadata; inspect and install only reviewed selections."""
import argparse,collections,hashlib,json,math,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'skills/skillosophy-start/scripts'))
import project_skills as setup
INDEX=ROOT/'library/index.json'
from metadata_search import DOMAINS, tokens, domain_match, rank_metadata
def entries():return json.loads(INDEX.read_text())['entries']
def shortlist(query,limit=8,category=None,revised=False,domain=None):
 if not 1<=limit<=20 or not query.strip():raise setup.SetupError('Use a nonempty task and a shortlist limit of 1–20')
 es=[e for e in entries() if (not category or e['category']==category) and (not revised or e['status']=='skillosophy_candidate') and (not domain or domain_match(e,domain))]
 ranked=rank_metadata(es,query,limit)
 results=[{**{k:e[k] for k in ('name','description','category','score','matched_terms','status','effectiveness','review','source')},'path':'library/'+e['path'],'resource_issues':e['unresolved_entrypoint_links']} for e in ranked]
 return {'query':query,'domain':domain,'searched_metadata_entries':len(es),'skill_bodies_loaded':0,'results':results[:limit],'interpretation':'Textual relevance only; AI must assess fit, prerequisites and evidence. No popularity or performance rating.'}
def inspect(name):
 e=next((e for e in entries() if e['name']==name),None)
 if not e:raise setup.SetupError('Unknown repository skill')
 folder=ROOT/'library'/e['path'];hashes=setup.validate_skill(folder,name)
 if hashes!=e['file_sha256']:raise setup.SetupError('Library files differ from recorded hashes')
 return {'metadata':{k:v for k,v in e.items() if k!='file_sha256'},'instruction_text':(folder/'SKILL.md').read_text(),'files':sorted(hashes),'resource_review_required':True}
def install(names,project,note,apply):
 if not note.strip():raise setup.SetupError('Record actual source, license, compatibility and requirements review before installation')
 if not names or len(names)>5 or len(names)!=len(set(names)):raise setup.SetupError('Select 1–5 distinct skills; expand only after a concrete project need')
 selected={}
 for name in names:
  report=inspect(name);e=next(e for e in entries() if e['name']==name)
  if e['unresolved_entrypoint_links']:raise setup.SetupError('Missing entrypoint resources; resolve source dependencies before installing '+name)
  selected[name]={'id':name,'install_name':name,'description':e['description'],'category':e['category'],'dependencies':[],
                  'prerequisites':['Check source tools/runtime and sibling references in the inspected skill before use'],
                  'source':{'type':'bundled','path':e['path'],'license':'MIT','upstream':e['source'],'review_sha256':e['file_sha256']},
                  'evidence':{'status':'reviewed_source_unmeasured','note':note}}
 plan={'schema_version':1,'project':{'goal':'Equip the specified project with a minimal reviewed skill selection','deliverable':'Project-local skills, provenance and specialist role instructions','philosophy':{'priority':'Task fit and measured outcomes over catalog size','evidence':'Preserve source review and verify actual installation'}},'skills':names,
       'roles':[{'name':name+'-specialist' if len(name)<50 else name,'mission':selected[name]['description']+' Inherit project instructions and authorized scope.','skills':[name],'done_when':'The assigned deliverable has observable validation or explicitly recorded limitations.'} for name in names]}
 return setup.install(project,plan,selected,bundle_root=ROOT/'library',apply=apply)
def validate():
 es=entries();failures=[];issues=[];files=0
 if len({e['name'] for e in es})!=len(es):failures.append('Duplicate names')
 for e in es:
  try:
   report=inspect(e['name']);files+=len(report['files'])
   if e['unresolved_entrypoint_links']:issues.append({'name':e['name'],'links':e['unresolved_entrypoint_links']})
  except (OSError,ValueError,setup.SetupError) as error:failures.append({'name':e['name'],'error':str(error)})
 return {'skill_folders':len(es),'checked_files':files,'failures':failures,'entrypoint_resource_issues':issues,'authored_revisions':sum(e['status']=='skillosophy_candidate' for e in es),'behavioral_improvement_proven':False}
def main():
 p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='command',required=True)
 c=s.add_parser('search');c.add_argument('query');c.add_argument('--limit',type=int,default=8);c.add_argument('--category');c.add_argument('--revised',action='store_true');c.add_argument('--domain',choices=DOMAINS)
 c=s.add_parser('inspect');c.add_argument('name')
 c=s.add_parser('install');c.add_argument('--skill',action='append',required=True);c.add_argument('--project',type=Path,required=True);c.add_argument('--review-note',required=True);c.add_argument('--apply',action='store_true')
 c=s.add_parser('route');c.add_argument('--brief',type=Path,required=True);c.add_argument('--limit',type=int,default=5)
 s.add_parser('validate');a=p.parse_args()
 try:
  if a.command=='search':result=shortlist(a.query,a.limit,a.category,a.revised,a.domain)
  elif a.command=='inspect':result=inspect(a.name)
  elif a.command=='route':
   brief=json.loads(a.brief.read_text());capabilities=brief.get('capabilities')
   if not isinstance(capabilities,list) or not capabilities or len(capabilities)>10:raise setup.SetupError('Brief needs 1–10 distinct capability tasks')
   if any(not isinstance(c,dict) or c.get('domain') not in DOMAINS or not isinstance(c.get('task'),str) for c in capabilities):raise setup.SetupError('Each capability needs a task and supported domain')
   result={'goal':brief.get('goal'),'shortlists':[shortlist(c['task'],a.limit,domain=c['domain']) for c in capabilities],'next':'Inspect task-fit candidates, resolve prerequisites and overlaps, then record the minimal authorized installation plan.'}
  elif a.command=='install':result=install(a.skill,a.project,a.review_note,a.apply)
  else:result=validate()
  print(setup.canonical(result),end='')
  if a.command=='validate' and result['failures']:p.exit(1)
 except (OSError,ValueError,KeyError,setup.SetupError) as error:p.exit(1,str(error)+'\n')
if __name__=='__main__':main()
