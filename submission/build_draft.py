#!/usr/bin/env python3
"""Prepare a public-review draft ZIP without changing private source or claiming submission."""
import hashlib
import json
from pathlib import Path
import struct
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
PREP = ROOT / 'submission'
manifest = json.loads((PREP / 'plugin.draft.json').read_text())
extension = manifest['extensions']['com.openai']
ui = extension['interface']
for field, limit in [('displayName', 30), ('shortDescription', 30), ('longDescription', 4000), ('developerName', 80)]:
    if field in ui and not 0 < len(ui[field]) <= limit:
        raise SystemExit(f'Invalid listing length: {field}')
prompts = ui['defaultPrompt'] if isinstance(ui['defaultPrompt'], list) else [ui['defaultPrompt']]
if not 1 <= len(prompts) <= 3 or any(not p.strip() or len(p)>128 or '\n' in p for p in prompts):
    raise SystemExit('Invalid default prompt')
if len({' '.join(p.split()) for p in prompts}) != len(prompts):
    raise SystemExit('Duplicate default prompts')
if manifest.get('apps') is not None or extension.get('apps') is not None:
    raise SystemExit('Public upload must not include private app bindings')

compatibility = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())
for field in ['name', 'version', 'description', 'author']:
    compatibility[field] = manifest[field]
compatibility['interface'] = {**ui, 'capabilities': []}
compatibility['extensions'] = {'com.openai': {k: v for k, v in extension.items() if k != 'interface'}}
files = {'plugin.json': (json.dumps(manifest, indent=2)+'\n').encode(),
         '.codex-plugin/plugin.json': (json.dumps(compatibility, indent=2)+'\n').encode(),
         'LICENSE': (ROOT / 'LICENSE').read_bytes()}
for path in sorted((ROOT / 'skills').rglob('*')):
    if path.is_symlink():
        raise SystemExit(f'Refusing symlink: {path}')
    if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc' and path.name != '.DS_Store':
        files[path.relative_to(ROOT).as_posix()] = path.read_bytes()
icons = []
for field in ['logo', 'composerIcon']:
    relative = ui[field].removeprefix('./')
    path = (PREP / relative).resolve()
    if not path.is_relative_to(PREP.resolve()):
        raise SystemExit('Icon outside submission folder')
    data = path.read_bytes()
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise SystemExit('Icon must be PNG')
    width, height = struct.unpack('>II', data[16:24])
    if width != height or width < (256 if field == 'logo' else 48) or len(data)>5*1024*1024:
        raise SystemExit('Invalid icon dimensions or size')
    files[relative] = data
    icons.append({'field': field, 'path': relative, 'width': width, 'height': height, 'bytes': len(data)})
onboarding = extension['onboardingSkill'].removeprefix('./')
if onboarding not in files or '.app.json' in files:
    raise SystemExit('Invalid public package inventory')

output = ROOT / 'dist' / f"{manifest['name']}-{manifest['version']}-submission-DRAFT.zip"
output.parent.mkdir(exist_ok=True)
with ZipFile(output, 'w', compression=ZIP_DEFLATED) as archive:
    for path, data in sorted(files.items()):
        info = ZipInfo(manifest['name']+'/'+path, (2026,10,6,0,0,0))
        info.compress_type = ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, data)
with ZipFile(output) as archive:
    assert archive.testzip() is None
    prefix = manifest['name']+'/'
    assert len([p for p in archive.namelist() if p.endswith('/SKILL.md')]) == 17
    assert json.loads(archive.read(prefix+'plugin.json')) == manifest
    assert json.loads(archive.read(prefix+'.codex-plugin/plugin.json')) == compatibility

missing_urls = [k for k in ['websiteURL','supportURL','privacyPolicyURL','termsOfServiceURL'] if not ui.get(k)]
verification_path = PREP / 'url-verification.json'
verified_urls = json.loads(verification_path.read_text())['verified'] if verification_path.exists() else []
urls_checked = all(any(v['field']==field and v['url']==ui[field] and v['correct_content_checked'] for v in verified_urls)
                   for field in ['websiteURL','supportURL','privacyPolicyURL','termsOfServiceURL'] if ui.get(field)) and not missing_urls
report = {'status': ('package prepared; not uploaded or submitted' if urls_checked else 'incomplete preparation; not uploaded or submitted'),
          'archive': str(output), 'archive_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
          'packaged_skills': 17, 'files': len(files), 'icons': icons,
          'missing_listing_urls': missing_urls, 'listing_urls_content_verified': urls_checked,
          'publication': {'publisher': 'Ashan Jeevanathan (individual)', 'country_restrictions': extension['publication'].get('countries'),
                          'commerce': extension.get('review',{}).get('commerce')},
          'pending': ['Portal organization and verified publisher selection', 'Portal validation',
                      'developer-completed legal/policy attestations', 'actual review and publication state']}
portal_path = ROOT / 'dist' / 'private-portal-status.json'
if portal_path.exists():
    portal = json.loads(portal_path.read_text())
    if portal.get('archive_sha256') == report['archive_sha256']:
        report['portal'] = {k: portal[k] for k in ['version', 'metadata_checks', 'skill_checks', 'review', 'publication']}
        report['status'] = 'draft uploaded; inspect recorded review and publication state'
        report['pending'] = ['remaining automated checks', 'developer-completed legal/policy attestations', 'submission and publication']
(PREP / 'validation.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
