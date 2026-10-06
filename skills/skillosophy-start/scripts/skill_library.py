#!/usr/bin/env python3
"""Search skill sources, inspect immutable packages, and prepare reviewed selections."""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import stat
import tempfile
import urllib.parse
import urllib.request
import zipfile
from project_skills import (SetupError, canonical, digest, download_archive, extract_skill,
                            relative, validate_skill, load_catalog, CATALOG_PATH, NAME)

LIBRARY = Path(__file__).resolve().parents[1] / 'references/library.json'
REPO = re.compile(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z')
SHA = re.compile(r'[0-9a-f]{40}\Z')

def now(): return datetime.now(timezone.utc).isoformat()
def clean(value):
    return ''.join(c for c in str(value) if ord(c)>=32 and ord(c)!=127)[:2000]

def fetch_json(url):
    request=urllib.request.Request(url,headers={'User-Agent':'Skillosophy/0.3.0','Accept':'application/json'})
    with urllib.request.urlopen(request,timeout=30) as response:
        data=response.read(16*1024*1024+1)
    if len(data)>16*1024*1024: raise SetupError('Discovery response exceeds size limit')
    return json.loads(data)

def check_repo(repo):
    if not REPO.fullmatch(repo) or any(part in ('.','..') for part in repo.split('/')): raise SetupError('Use a GitHub owner/repository, not a URL or shell command')

def resolve_revision(repo, revision=None, fetch=fetch_json):
    check_repo(repo)
    if revision and SHA.fullmatch(revision): return revision
    if revision and not re.fullmatch(r'[A-Za-z0-9_.\-/]+',revision): raise SetupError('Invalid ref')
    ref=urllib.parse.quote(revision or 'HEAD',safe='')
    sha=fetch(f'https://api.github.com/repos/{repo}/commits/{ref}')['sha']
    if not SHA.fullmatch(sha): raise SetupError('GitHub returned no immutable commit')
    return sha

def frontmatter(text):
    parts=text.split('---',2)
    if len(parts)!=3 or parts[0].strip(): raise SetupError('Missing skill frontmatter')
    fields={}
    lines=parts[1].splitlines()
    for i,line in enumerate(lines):
        match=re.match(r'^(name|description|license):\s*(.*)$',line)
        if not match: continue
        key,value=match.groups()
        if value.strip() in ('>','|','>-','|-'):
            tail=[]
            for following in lines[i+1:]:
                if following and not following[0].isspace(): break
                tail.append(following.strip())
            value=' '.join(tail)
        fields[key]=clean(value.strip().strip('"\''))
    if not NAME.fullmatch(fields.get('name','')) or not fields.get('description'): raise SetupError('Invalid skill metadata')
    return fields

def archive_layout(data):
    archive=zipfile.ZipFile(io.BytesIO(data))
    members={};roots=set()
    for item in archive.infolist():
        relative(item.filename.rstrip('/'))
        roots.add(item.filename.split('/')[0])
        if item.filename in members: raise SetupError('Duplicate archive member')
        members[item.filename]=item
    if len(roots)!=1: raise SetupError('Unexpected archive root')
    return archive,next(iter(roots)),members

def identifier(repo,path): return 'community-'+hashlib.sha256((repo+'\n'+path).encode()).hexdigest()[:20]

def index_archive(repo,revision,data):
    check_repo(repo)
    if not SHA.fullmatch(revision): raise SetupError('Index requires a pinned commit')
    archive,root,members=archive_layout(data)
    entries=[];skipped=[]
    with archive:
        for member,item in sorted(members.items()):
            if not member.endswith('/SKILL.md'): continue
            path=member[len(root)+1:-len('/SKILL.md')]
            if not path: continue
            if item.file_size>256*1024 or stat.S_ISLNK(item.external_attr>>16):
                skipped.append({'path':path,'reason':'Unsupported entrypoint'});continue
            try: meta=frontmatter(archive.read(item).decode('utf-8'))
            except (SetupError,UnicodeError) as error:
                skipped.append({'path':path,'reason':str(error)});continue
            entries.append({'id':identifier(repo,path),'name':meta['name'],'description':meta['description'],
                            'repo':repo,'revision':revision,'path':path,'provider':'github',
                            'source_url':f'https://github.com/{repo}/tree/{revision}/{urllib.parse.quote(path,safe="/")}',
                            'evidence':{'status':'unmeasured','note':'Discovery metadata; source, license, requirements and dependencies still need review.'},
                            'license_hint':meta.get('license'),'install_ready':False})
    return {'schema_version':1,'updated_at':now(),'sources':[{'repo':repo,'revision':revision}], 'entries':entries,'skipped':skipped}

def community_search(query,limit=20,fetch=fetch_json):
    if not 2<=len(query.strip())<=200: raise SetupError('Use 2–200 characters of public task keywords')
    url='https://skills.sh/api/search?'+urllib.parse.urlencode({'q':query,'limit':min(limit,20)})
    payload=fetch(url)
    if not isinstance(payload.get('skills'),list): raise SetupError('Community search response has an unsupported format')
    results=[]
    for item in payload['skills'][:20]:
        if not isinstance(item,dict): continue
        repo=item.get('source','');name=item.get('name','');slug=item.get('id','')
        if not isinstance(repo,str) or not REPO.fullmatch(repo) or not isinstance(name,str) or not NAME.fullmatch(name): continue
        installs=item.get('installs')
        results.append({'id':clean(slug),'name':name,'repo':repo,'provider':'skills.sh','installs':installs if isinstance(installs,int) and installs>=0 else None,
                        'directory_url':'https://skills.sh/'+urllib.parse.quote(str(slug),safe='/'),
                        'install_ready':False,'evidence':{'status':'unmeasured','note':'Install count is a popularity signal, not measured effectiveness. Resolve and inspect the GitHub skill before installation.'}})
    return results[:limit]

def search(query,offline=False,limit=20,library=LIBRARY,fetch=fetch_json):
    if not 2<=len(query.strip())<=200 or not 1<=limit<=100: raise SetupError('Use 2–200 public keyword characters and a limit of 1–100')
    snapshot=json.loads(Path(library).read_text());base=load_catalog();local=[]
    for e in base.values():
        s=e['source'];local.append({'id':e['id'],'name':e['install_name'],'description':e['description'],'category':e['category'],
                                  'provider':'curated','install_ready':True,'evidence':e['evidence'],'repo':s.get('repo'),'source_url':s.get('url')})
    tokens=set(re.findall(r'[a-z0-9]+',query.lower()))
    ranked=[]
    for e in local+snapshot['entries']:
        name=e['name'].lower();text=(name+' '+e.get('description','')+' '+e.get('category','')).lower()
        score=sum((5 if token in name else 1) for token in tokens if token in text)
        if score: ranked.append({**e,'keyword_fit':score})
    ranked.sort(key=lambda e:(-e['keyword_fit'],e['name'],e.get('repo') or ''))
    # Keep upstream versions separate from curated variants; they can have different guidance.
    result={'query':query,'snapshot_updated_at':snapshot['updated_at'],'offline_results':ranked[:limit],
            'community_results':[],'community_status':'not_requested' if offline else 'ok','warnings':[]}
    if not offline:
        try: result['community_results']=community_search(query,min(limit,20),fetch)
        except (OSError,ValueError,KeyError,SetupError) as error:
            result['community_status']='unavailable';result['warnings'].append(clean(error))
    return result

def inspect(repo,revision,path=None,name=None,output=None,data=None):
    check_repo(repo)
    if not SHA.fullmatch(revision): raise SetupError('Inspection requires a pinned commit')
    data=data if data is not None else download_archive(repo,revision)
    index=index_archive(repo,revision,data)
    choices=[e for e in index['entries'] if (path and e['path']==path) or (not path and name and e['name']==name)]
    if len(choices)!=1: raise SetupError('Skill missing or ambiguous; index the repository and provide an exact path')
    candidate=choices[0];path=candidate['path'];archive,root,members=archive_layout(data)
    license_repo_path=None
    with archive:
        current=Path(path)
        for folder in [current,*current.parents]:
            for filename in ['LICENSE.txt','LICENSE','LICENSE.md','COPYING']:
                relative_path=(folder/filename).as_posix().removeprefix('./')
                item=members.get(root+'/'+relative_path)
                if item and not item.is_dir() and not stat.S_ISLNK(item.external_attr>>16) and item.file_size<=1024*1024:
                    license_repo_path=relative_path;license_bytes=archive.read(item);break
            if license_repo_path: break
    if not license_repo_path: raise SetupError('No applicable license found; do not install an unlicensed source')
    inside=license_repo_path.startswith(path+'/')
    license_destination=license_repo_path[len(path)+1:] if inside else 'UPSTREAM-LICENSE.txt'
    source={'type':'github','repo':repo,'revision':revision,'path':path,'url':candidate['source_url'],
            'license_path':license_destination,'license_sha256':digest(license_bytes)}
    if not inside: source['license_repo_path']=license_repo_path
    with zipfile.ZipFile(io.BytesIO(data)) as notices:
        folder=Path(license_repo_path).parent
        for filename in ['NOTICE','NOTICE.txt','ThirdPartyNoticeText.txt']:
            repo_path=(folder/filename).as_posix().removeprefix('./')
            if root+'/'+repo_path in members:
                source.setdefault('attribution',[]).append({'repo_path':repo_path,'destination':'UPSTREAM-'+filename})
    target=Path(output)
    if target.exists() or target.is_symlink(): raise SetupError('Inspection destination must not already exist')
    target.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='skillosophy-inspect-',dir=target.parent) as temporary:
        stage=Path(temporary)/'skill';stage.mkdir();extract_skill(data,source,stage)
        hashes=validate_skill(stage,candidate['name']);source['review_sha256']=hashes
        instructions=(stage/'SKILL.md').read_text()
        links=re.findall(r'\]\(([^)]+)\)',instructions)
        unresolved=[link for link in links if '://' not in link and not link.startswith('#') and not (stage/link.split('#')[0]).exists()]
        report={'schema_version':1,'inspected_at':now(),'candidate':candidate,'source':source,'instruction_text':instructions,
                'files':[{'path':p,'sha256':h} for p,h in sorted(hashes.items())],
                'unresolved_local_links':unresolved,'status':'requires_agent_review','downloaded_code_executed':False}
        (Path(temporary)/'inspection.json').write_text(canonical(report));shutil.move(str(temporary),str(target))
    return report

def review(report_path,note,license_label,prerequisites,dependencies,output):
    report=json.loads(Path(report_path).read_text());candidate=report['candidate'];source=report['source']
    if not note.strip() or not license_label.strip(): raise SetupError('Review needs license identification and substantive notes')
    if report.get('unresolved_local_links'): raise SetupError('Resolve missing local resources before approving installation')
    # Verify the inspection has not been edited or substituted since it was generated.
    hashes=validate_skill(Path(report_path).parent/'skill',candidate['name'])
    if hashes!=source.get('review_sha256'): raise SetupError('Inspected files changed; inspect again')
    source['license']=license_label
    entry={'id':candidate['id'],'install_name':candidate['name'],'description':candidate['description'],'category':'community',
           'source':source,'dependencies':dependencies,'prerequisites':prerequisites,
           'evidence':{'status':'reviewed_source_unmeasured','note':note,'reviewed_at':now()}}
    destination=Path(output)
    content=json.loads(destination.read_text()) if destination.exists() else {'schema_version':1,'entries':[]}
    if any(e['id']==entry['id'] or e['install_name']==entry['install_name'] for e in content['entries']): raise SetupError('Review catalog already contains this name; preserve existing review')
    content['entries'].append(entry)
    with tempfile.TemporaryDirectory(prefix='skillosophy-catalog-review-') as temporary:
        validation=Path(temporary)/'catalog.json';validation.write_text(canonical(content));load_catalog(validation, known_dependencies=load_catalog())
    destination.write_text(canonical(content))
    return entry

def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    cmd=sub.add_parser('search');cmd.add_argument('query');cmd.add_argument('--offline',action='store_true');cmd.add_argument('--limit',type=int,default=20)
    cmd=sub.add_parser('browse');cmd.add_argument('--repo');cmd.add_argument('--limit',type=int,default=100)
    cmd=sub.add_parser('index');cmd.add_argument('--repo',required=True);cmd.add_argument('--revision');cmd.add_argument('--output',type=Path,required=True)
    cmd=sub.add_parser('inspect');cmd.add_argument('--repo',required=True);cmd.add_argument('--revision');pick=cmd.add_mutually_exclusive_group(required=True);pick.add_argument('--path');pick.add_argument('--name');cmd.add_argument('--output',type=Path,required=True)
    cmd=sub.add_parser('review');cmd.add_argument('--inspection',type=Path,required=True);cmd.add_argument('--note',required=True);cmd.add_argument('--license-label',required=True);cmd.add_argument('--prerequisite',action='append',default=[]);cmd.add_argument('--dependency',action='append',default=[]);cmd.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try:
        if args.command=='search':result=search(args.query,args.offline,args.limit)
        elif args.command=='browse':
            library=json.loads(LIBRARY.read_text());result={'updated_at':library['updated_at'],'sources':library['sources'],'entries':[e for e in library['entries'] if not args.repo or e['repo']==args.repo][:args.limit]}
        elif args.command=='index':
            revision=resolve_revision(args.repo,args.revision);result=index_archive(args.repo,revision,download_archive(args.repo,revision));args.output.write_text(canonical(result))
        elif args.command=='inspect':result=inspect(args.repo,resolve_revision(args.repo,args.revision),args.path,args.name,args.output)
        else:result=review(args.inspection,args.note,args.license_label,args.prerequisite,args.dependency,args.output)
        print(canonical(result),end='')
    except (OSError,ValueError,KeyError,TypeError,SetupError,zipfile.BadZipFile) as error:parser.exit(1,f'Skillosophy library: {clean(error)}\n')

if __name__=='__main__':main()
