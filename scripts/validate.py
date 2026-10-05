#!/usr/bin/env python3
"""Check portable package invariants; behavioral effectiveness needs separate evaluation."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

def validate(root=ROOT):
    errors=[]
    manifest=json.loads((root/'plugin.json').read_text())
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', manifest['name']):
        errors.append('Invalid package name')
    if not re.fullmatch(r'\d+\.\d+\.\d+',manifest['version']):
        errors.append('Version must be semantic')
    ui=manifest['extensions']['com.openai']['interface']
    if len(ui['shortDescription'])>30:
        errors.append('Plugin subtitle exceeds 30 characters')
    for prohibited in ['skills','mcpServers','apps','interface']:
        if prohibited in manifest:
            errors.append(f'Non-portable top-level field: {prohibited}')
    skills=list((root/'skills').glob('*/SKILL.md'))
    if not skills:
        errors.append('No skills')
    for entry in skills:
        content=entry.read_text()
        parts=content.split('---',2)
        if len(parts)!=3 or parts[0].strip():
            errors.append(f'{entry}: missing frontmatter');continue
        header=parts[1]
        name=re.search(r'^name: ([a-z0-9-]+)$',header,re.M)
        if not name or name[1]!=entry.parent.name:
            errors.append(f'{entry}: name mismatch')
        desc=re.search(r'^description: (.+)$',header,re.M)
        if not desc or not json.loads(desc[1]).strip():
            errors.append(f'{entry}: invalid description')
        if len(content.split())>1400:
            errors.append(f'{entry}: review oversized entrypoint')
        for target in re.findall(r'\]\(([^)]+)\)',content):
            if '://' not in target and not (entry.parent/target.split('#')[0]).exists():
                errors.append(f'{entry}: missing link {target}')
        metadata=(entry.parent/'agents'/'openai.yaml').read_text()
        for key in ['display_name','short_description','default_prompt']:
            match=re.search(rf'^  {key}: (.+)$',metadata,re.M)
            if not match:
                errors.append(f'{entry}: missing UI {key}');continue
            value=json.loads(match[1])
            if key=='short_description' and not 25<=len(value)<=64:
                errors.append(f'{entry}: UI description length')
            if key=='default_prompt' and '$'+entry.parent.name not in value:
                errors.append(f'{entry}: invocation missing')
    for md in (root/'skills').rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)',md.read_text()):
            if '://' not in target and not (md.parent/target.split('#')[0]).exists():
                errors.append(f'{md}: unresolved local link {target}')
    cases=json.loads((root/'evals'/'cases.json').read_text())
    ids=[c['id'] for c in cases]
    if len(ids)!=len(set(ids)):
        errors.append('Duplicate evaluation IDs')
    names={s.parent.name for s in skills}
    for case in cases:
        if case['skill'] not in names or len(case['criteria'])!=3:
            errors.append(f"Invalid case {case['id']}")
    for name in names:
        if {c['kind'] for c in cases if c['skill']==name}!={'application','regression'}:
            errors.append(f'{name}: needs application and regression coverage')
    return errors,len(skills),len(cases)

if __name__=='__main__':
    errors,skills,cases=validate()
    for error in errors:
        print(error,file=sys.stderr)
    if errors:
        sys.exit(1)
    print(f'Validated {skills} skills, {cases} evaluation cases, links, and manifest invariants.')
