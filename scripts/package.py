#!/usr/bin/env python3
"""Build a minimal, reproducible skills-only plugin ZIP from reviewed sources."""
from pathlib import Path
import sys
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import json
import argparse
import re
from validate import validate, ROOT

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--account-name', help='Preserve an existing account plugin machine identifier; visible branding stays unchanged')
args=parser.parse_args()
if args.account_name and not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',args.account_name):
    parser.error('Invalid account machine identifier')
errors,_,_=validate()
if errors:
    raise SystemExit('\n'.join(errors))
manifest=json.loads((ROOT/'plugin.json').read_text())
output=ROOT/'dist'/f"{manifest['name']}-{manifest['version']}{'-account' if args.account_name else ''}.zip"
package_name=args.account_name or manifest['name']
output.parent.mkdir(exist_ok=True)
paths=[ROOT/'plugin.json',ROOT/'LICENSE',ROOT/'.codex-plugin'/'plugin.json']+sorted((ROOT/'skills').rglob('*'))+sorted((ROOT/'assets').rglob('*'))
with ZipFile(output,'w',compression=ZIP_DEFLATED) as archive:
    for path in paths:
        if '__pycache__' in path.parts or path.suffix=='.pyc' or path.name=='.DS_Store':
            continue
        if not path.is_file():
            continue
        if path.is_symlink():
            raise SystemExit(f'Refusing symlink: {path}')
        relative=path.relative_to(ROOT)
        if any(part.startswith('.') and part!='.codex-plugin' for part in relative.parts):
            raise SystemExit(f'Review hidden package file: {relative}')
        info=ZipInfo(str(Path(package_name)/relative),(2026,10,5,0,0,0))
        info.compress_type=ZIP_DEFLATED
        info.external_attr=0o100644<<16
        data=path.read_bytes()
        if args.account_name and str(relative) in ('plugin.json','.codex-plugin/plugin.json'):
            compatibility=json.loads(data)
            compatibility['name']=args.account_name
            data=(json.dumps(compatibility,indent=2)+'\n').encode()
        archive.writestr(info,data)
with ZipFile(output) as archive:
    if archive.testzip():
        raise SystemExit('Corrupt archive')
    names=archive.namelist()
    assert all(n.startswith(package_name+'/') for n in names)
    assert len([n for n in names if n.endswith('/SKILL.md')])==len(list((ROOT/'skills').glob('*/SKILL.md')))
print(output)
