#!/usr/bin/env python3
"""Build a minimal, reproducible skills-only plugin ZIP from reviewed sources."""
from pathlib import Path
import sys
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import json
from validate import validate, ROOT

errors,_,_=validate()
if errors:
    raise SystemExit('\n'.join(errors))
manifest=json.loads((ROOT/'plugin.json').read_text())
output=ROOT/'dist'/f"{manifest['name']}-{manifest['version']}.zip"
output.parent.mkdir(exist_ok=True)
paths=[ROOT/'plugin.json',ROOT/'LICENSE']+sorted((ROOT/'skills').rglob('*'))
with ZipFile(output,'w',compression=ZIP_DEFLATED) as archive:
    for path in paths:
        if not path.is_file():
            continue
        if path.is_symlink():
            raise SystemExit(f'Refusing symlink: {path}')
        relative=path.relative_to(ROOT)
        if any(part.startswith('.') for part in relative.parts):
            raise SystemExit(f'Review hidden package file: {relative}')
        info=ZipInfo(str(Path(manifest['name'])/relative),(2026,10,5,0,0,0))
        info.compress_type=ZIP_DEFLATED
        info.external_attr=0o100644<<16
        archive.writestr(info,path.read_bytes())
with ZipFile(output) as archive:
    if archive.testzip():
        raise SystemExit('Corrupt archive')
    names=archive.namelist()
    assert all(n.startswith(manifest['name']+'/') for n in names)
    assert len([n for n in names if n.endswith('/SKILL.md')])==12
print(output)
