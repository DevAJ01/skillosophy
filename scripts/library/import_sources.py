#!/usr/bin/env python3
"""Vendor immutable skill folders; preserve sources and never execute downloaded code."""
import argparse, hashlib, json, re, shutil, stat, sys, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'skills/skillosophy-start/scripts'))
from skill_library import frontmatter
from project_skills import relative, canonical
SOURCES=[('claude','alirezarezvani/claude-skills'),('awesome','sickn33/agentic-awesome-skills')]
PRIORITY=('engineering','product-team','research','project-management','productivity','marketing')
CORE=('react-patterns','react-best-practices','nextjs-best-practices','python-pro','typescript-pro','javascript-pro','rust-pro','golang-pro','docker-expert','kubernetes-architect','postgresql','sql-optimization-patterns','terraform-specialist','github-actions-templates','fastapi-pro','django-pro','nodejs-best-practices','api-design-principles','database-migration','systematic-debugging','accessibility','webapp-testing','prompt-engineering-patterns','rag-implementation','frontend-design','mobile-developer','unity-developer','data-engineer','data-scientist','machine-learning-ops','llm-application-dev','mcp-builder')
KEYWORDS=('python','react','typescript','postgres','database','api','test','docker','kubernetes','accessibility','debug','security','performance','data','design','git','rust','swift','mobile','research','document','workflow','agent','rag','llm','observability','migration','deploy','architecture')
def sha(data): return hashlib.sha256(data).hexdigest()
def build(cache,limit):
    dest=ROOT/'library/skills'
    if dest.exists(): raise SystemExit('Preserve existing library; choose a new import or review existing versions.')
    dest.mkdir(parents=True)
    entries=[];skipped=[];seen=set();source_records=[];families={}
    for label,repo in SOURCES:
      rev=(cache/(label+'-sha')).read_text().strip()
      if not re.fullmatch('[0-9a-f]{40}',rev): raise ValueError('Immutable source revision required')
      with zipfile.ZipFile(cache/(label+'.zip')) as z:
        root=z.namelist()[0].split('/')[0];license_bytes=z.read(root+'/LICENSE')
        source_records.append({'repo':repo,'revision':rev,'license':'MIT','license_sha256':sha(license_bytes)})
        candidates=[]
        for item in z.infolist():
          path=item.filename[len(root)+1:]
          if not path.endswith('/SKILL.md') or path.startswith(('.','plugins/')):continue
          if label=='awesome' and not path.startswith('skills/'):continue
          try:
            if item.file_size>256*1024:raise ValueError('Oversized entrypoint')
            metadata=frontmatter(z.read(item).decode())
            name=metadata['name']
            if len(name)>63:raise ValueError('Long name')
            if metadata.get('license') and not re.search(r'\bMIT\b',metadata['license'],re.I):raise ValueError('Different license declaration; requires separate review')
          except Exception as e:skipped.append({'repo':repo,'path':path,'reason':str(e)});continue
          rank=(0 if path.startswith(PRIORITY) else 1) if label=='claude' else (0 if name in CORE else 1 if any(k in name for k in KEYWORDS) else 2)
          candidates.append((rank,name,path,metadata))
        for _,name,path,metadata in sorted(candidates,key=lambda c:(c[0],sha(c[1].encode()))):
          if len(entries)>=limit:break
          if name in seen:continue
          family=name.split('-')[0]
          if label=='awesome' and family in ('azure','aws','gcp') and families.get(family,0)>=12:continue
          folder=path[:-len('/SKILL.md')];prefix=root+'/'+folder+'/'
          members=[i for i in z.infolist() if i.filename.startswith(prefix) and not i.is_dir()]
          if any(stat.S_ISLNK(i.external_attr>>16) or i.file_size>4*1024*1024 for i in members):continue
          if sum(i.file_size for i in members)>16*1024*1024:continue
          target=dest/name;target.mkdir()
          hashes={}
          for item in members:
            rel=item.filename[len(prefix):];relative(rel)
            if any(p in ('__pycache__','.git','node_modules') for p in Path(rel).parts) or rel.endswith('.pyc'):continue
            file=target/rel;file.parent.mkdir(parents=True,exist_ok=True)
            data=z.read(item);file.write_bytes(data);file.chmod(0o644);hashes[rel]=sha(data)
          (target/'UPSTREAM-LICENSE.txt').write_bytes(license_bytes)
          hashes['UPSTREAM-LICENSE.txt']=sha(license_bytes)
          links=re.findall(r'\]\(([^)]+)\)',(target/'SKILL.md').read_text())
          missing=[link for link in links if '://' not in link and not link.startswith('#') and not (target/link.split('#')[0]).exists()]
          record={'name':name,'description':metadata['description'],'path':'skills/'+name,'category':path.split('/')[0] if label=='claude' else 'practical',
                  'source':{'repo':repo,'revision':rev,'path':folder,'url':f'https://github.com/{repo}/tree/{rev}/{folder}','license':'MIT'},
                  'status':'upstream_candidate','effectiveness':'unmeasured','review':'pending','unresolved_entrypoint_links':missing,'file_sha256':hashes}
          (target/'skillosophy.json').write_text(canonical({k:v for k,v in record.items() if k!='file_sha256'}))
          hashes['skillosophy.json']=sha((target/'skillosophy.json').read_bytes())
          entries.append(record);seen.add(name);families[family]=families.get(family,0)+1
    (ROOT/'library/index.json').write_text(canonical({'schema_version':1,'entries':entries,'sources':source_records,'skipped':skipped,'downloaded_code_executed':False}))
    print(canonical({'actual_skill_folders':len(entries),'files':sum(len(e['file_sha256']) for e in entries),'bytes':sum(p.stat().st_size for p in dest.rglob('*') if p.is_file()),'sources':source_records,'skipped':len(skipped)}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cache',type=Path,required=True);p.add_argument('--limit',type=int,default=600);a=p.parse_args();build(a.cache,a.limit)
