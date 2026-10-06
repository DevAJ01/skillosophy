#!/usr/bin/env python3
"""Install a reviewed, pinned selection into a Codex project. Never execute upstream code."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
import urllib.request
import zipfile

CATALOG_PATH = Path(__file__).resolve().parents[1] / 'references' / 'catalog.json'
BUNDLE_ROOT = Path(__file__).resolve().parents[2]
MAX_ARCHIVE = 64 * 1024 * 1024
MAX_SKILL = 32 * 1024 * 1024
NAME = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')

class SetupError(Exception):
    pass

def canonical(value):
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + '\n'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def relative(value):
    path = PurePosixPath(value)
    if not value or path.is_absolute() or any(x in ('.', '..') for x in value.split('/')) or '\\' in value or ':' in value or any(ord(c)<32 for c in value):
        raise SetupError(f'Unsafe source path: {value}')
    return path

def load_catalog(path=CATALOG_PATH, known_dependencies=()):
    data = json.loads(path.read_text())
    if data.get('schema_version') != 1:
        raise SetupError('Unsupported catalog schema')
    entries = {e['id']: e for e in data['entries']}
    if len(entries) != len(data['entries']):
        raise SetupError('Duplicate catalog identifiers')
    for key, e in entries.items():
        if not NAME.fullmatch(key) or not NAME.fullmatch(e['install_name']):
            raise SetupError('Invalid catalog skill name')
        if any(d not in entries and d not in known_dependencies for d in e['dependencies']):
            raise SetupError(f'Unknown dependency for {key}')
        source = e['source']; relative(source['path'])
        if source['type'] == 'github':
            if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', source['repo']):
                raise SetupError('Invalid GitHub repository')
            if not re.fullmatch(r'[0-9a-f]{40}', source['revision']):
                raise SetupError('External sources require an immutable commit')
            relative(source['license_path'])
            if source.get('license_repo_path'):
                relative(source['license_repo_path'])
            for notice in source.get('attribution',[]):
                relative(notice['repo_path']); relative(notice['destination'])
            if source.get('review_sha256') is not None:
                for file, sha in source['review_sha256'].items():
                    relative(file)
                    if not re.fullmatch(r'[0-9a-f]{64}',sha):
                        raise SetupError('Invalid reviewed file hash')
            if not re.fullmatch(r'[0-9a-f]{64}', source['license_sha256']):
                raise SetupError('Missing checked license digest')
        elif source['type'] != 'bundled':
            raise SetupError('Unsupported source type')
    if len({e['install_name'] for e in entries.values()}) != len(entries):
        raise SetupError('Catalog contains colliding install names')
    return entries

def selected_entries(ids, entries):
    selected = set(); queue = list(ids)
    while queue:
        key = queue.pop(0)
        if key not in entries:
            raise SetupError(f'Unknown skill: {key}')
        if key in selected:
            continue
        selected.add(key); queue.extend(entries[key]['dependencies'])
    return [entries[key] for key in sorted(selected)]

def validate_plan(plan, entries):
    if plan.get('schema_version') != 1:
        raise SetupError('Plan schema_version must be 1')
    project = plan.get('project')
    if not isinstance(project, dict) or not isinstance(project.get('goal'), str) or not project['goal'].strip():
        raise SetupError('Plan needs a project goal')
    if not isinstance(project.get('deliverable'), str) or not project['deliverable'].strip():
        raise SetupError('Plan needs a deliverable')
    philosophy = project.get('philosophy')
    if not isinstance(philosophy, dict) or not philosophy or any(not isinstance(v, str) or not v.strip() for v in philosophy.values()):
        raise SetupError('Plan needs a concrete working philosophy')
    ids = plan.get('skills')
    if not isinstance(ids, list) or not ids or any(not isinstance(v, str) for v in ids) or len(set(ids)) != len(ids):
        raise SetupError('Plan skills must be a nonempty list of unique catalog IDs')
    selected = selected_entries(ids, entries)
    available = {e['id'] for e in selected}
    roles = plan.get('roles', [])
    if not isinstance(roles, list):
        raise SetupError('Roles must be a list')
    names = set()
    for role in roles:
        if not isinstance(role, dict) or not isinstance(role.get('name'), str) or not NAME.fullmatch(role['name']) or role['name'] in names:
            raise SetupError('Role names must be unique simple identifiers')
        names.add(role['name'])
        for field in ['mission', 'done_when']:
            if not isinstance(role.get(field), str) or not role[field].strip():
                raise SetupError(f'Role needs {field}')
        if not isinstance(role.get('skills'), list) or not role['skills'] or any(s not in available for s in role['skills']):
            raise SetupError('Role skills must come from the selected installation')
    return selected

def check_directory(path):
    if path.is_symlink() or (path.exists() and not path.is_dir()):
        raise SetupError(f'Managed directory is not a plain directory: {path}')

def project_paths(project):
    project = Path(project).resolve(strict=True)
    if not project.is_dir():
        raise SetupError('Project must be an existing directory')
    for parts in [('.agents',), ('.agents', 'skills'), ('.skillosophy',)]:
        current = project
        for part in parts:
            current /= part; check_directory(current)
    return project, project / '.agents' / 'skills', project / '.skillosophy'

def tree_hashes(folder):
    if folder.is_symlink() or not folder.is_dir():
        raise SetupError(f'Skill source/destination is not a plain directory: {folder}')
    hashes = {}; size = 0
    for path in sorted(folder.rglob('*')):
        if any(part=='__pycache__' for part in path.relative_to(folder).parts) or path.suffix=='.pyc' or path.name=='.DS_Store':
            continue
        if path.is_symlink():
            raise SetupError(f'Symbolic link in skill: {path}')
        if path.is_dir():
            continue
        if not path.is_file():
            raise SetupError(f'Unsupported skill file: {path}')
        size += path.stat().st_size
        if size > MAX_SKILL:
            raise SetupError('Skill exceeds installation size limit')
        hashes[path.relative_to(folder).as_posix()] = digest(path.read_bytes())
    return hashes

def validate_skill(folder, name):
    hashes = tree_hashes(folder)
    entry = folder / 'SKILL.md'
    if not entry.is_file():
        raise SetupError('Selected folder has no SKILL.md')
    text = entry.read_text(encoding='utf-8')
    parts = text.split('---', 2)
    if len(parts) != 3 or parts[0].strip():
        raise SetupError('Skill needs YAML frontmatter')
    match = re.search(r'^name:\s*(.+?)\s*$', parts[1], re.M)
    actual = match[1].strip().strip('"\'') if match else ''
    if actual != name or not re.search(r'^description:\s*\S+', parts[1], re.M):
        raise SetupError('Skill frontmatter name or description does not match catalog')
    return hashes

def download_archive(repo, revision):
    url = f'https://codeload.github.com/{repo}/zip/{revision}'
    request = urllib.request.Request(url, headers={'User-Agent': 'Skillosophy/0.3.0'})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read(MAX_ARCHIVE + 1)
    if len(data) > MAX_ARCHIVE:
        raise SetupError('Upstream archive exceeds download size limit')
    return data

def extract_skill(data, source, target):
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        files = archive.infolist()
        roots = {f.filename.split('/')[0] for f in files if f.filename}
        if len(roots) != 1:
            raise SetupError('Unexpected archive root layout')
        prefix = next(iter(roots)) + '/' + source['path'].rstrip('/') + '/'
        total = 0; seen = set()
        for item in files:
            # Reject malicious member names even if outside the selected skill.
            relative(item.filename.rstrip('/'))
            if not item.filename.startswith(prefix):
                continue
            suffix = item.filename[len(prefix):]
            if not suffix:
                continue
            suffix = str(relative(suffix.rstrip('/')))
            if suffix in seen:
                raise SetupError('Duplicate archive destination')
            seen.add(suffix)
            mode = item.external_attr >> 16
            if stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR)):
                raise SetupError('Unsupported archive file type')
            path = target / suffix
            if item.is_dir():
                path.mkdir(parents=True, exist_ok=True); continue
            total += item.file_size
            if total > MAX_SKILL:
                raise SetupError('Selected archive skill exceeds size limit')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(archive.read(item))
            path.chmod(0o755 if mode & 0o111 else 0o644)
    if not (target / 'SKILL.md').is_file():
        raise SetupError('Selected upstream skill not found')
    if source.get('license_repo_path'):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            license_member = next(iter(roots)) + '/' + str(relative(source['license_repo_path']))
            item = archive.getinfo(license_member)
            if item.file_size > 1024 * 1024 or stat.S_ISLNK(item.external_attr >> 16):
                raise SetupError('Unsupported repository license')
            destination = target / str(relative(source['license_path']))
            if destination.exists() and destination.read_bytes() != archive.read(item):
                raise SetupError('Repository license would overwrite a skill file')
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(archive.read(item))
    for notice in source.get('attribution',[]):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            item = archive.getinfo(next(iter(roots)) + '/' + str(relative(notice['repo_path'])))
            if item.file_size > 1024 * 1024 or stat.S_ISLNK(item.external_attr >> 16):
                raise SetupError('Unsupported attribution file')
            destination = target / str(relative(notice['destination']))
            content = archive.read(item)
            if destination.exists() and destination.read_bytes() != content:
                raise SetupError('Attribution would overwrite a skill file')
            destination.parent.mkdir(parents=True, exist_ok=True); destination.write_bytes(content)
    license_path = target / source['license_path']
    if not license_path.is_file() or digest(license_path.read_bytes()) != source['license_sha256']:
        raise SetupError('Upstream license differs from reviewed catalog')

def stage_sources(selected, bundle_root, staging, fetch=download_archive):
    cache = {}; records = []
    for entry in selected:
        name = entry['install_name']; source = entry['source']; target = staging / name
        if source['type'] == 'bundled':
            origin = bundle_root / source['path']
            current = bundle_root
            for part in relative(source['path']).parts:
                current /= part
                if current.is_symlink():
                    raise SetupError('Bundled skill path contains a symlink')
            validate_skill(origin, name)
            shutil.copytree(origin, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
        else:
            pair = (source['repo'], source['revision'])
            if pair not in cache:
                cache[pair] = fetch(*pair)
            extract_skill(cache[pair], source, target)
        hashes = validate_skill(target, name)
        if source.get('review_sha256') is not None and hashes != source['review_sha256']:
            raise SetupError('Source files differ from the inspected review')
        records.append({'id': entry['id'], 'name': name, 'source': source, 'file_sha256': hashes})
    return records

def role_text(role, names=None):
    names = names or {}
    skills = '\n'.join('- Use $' + names.get(name, name) + ' when its method fits the assigned task.' for name in role['skills'])
    return f"# {role['name']}\n\nMission: {role['mission']}\n\n{skills}\n\nCompletion: {role['done_when']}\n\nThese are role instructions, not a registered or running subagent. Resolve skill resources from their installed project folders. Inherit the user's project constraints and authorization; defining this role does not authorize external actions.\n"

def install(project, plan, entries, bundle_root=BUNDLE_ROOT, apply=False, fetch=download_archive):
    selected = validate_plan(plan, entries)
    project, skill_root, metadata_root = project_paths(project)
    preview = {'project': str(project), 'mode': 'apply' if apply else 'dry-run',
               'skills': [{'id': e['id'], 'destination': str(skill_root/e['install_name']),
                           'source': e['source'], 'prerequisites': e['prerequisites']} for e in selected],
               'roles': [r['name'] for r in plan.get('roles', [])]}
    if not apply:
        return preview
    # Fetch and validate all sources before modifying the project.
    with tempfile.TemporaryDirectory(prefix='skillosophy-source-') as temp:
        staged = Path(temp)
        records = stage_sources(selected, Path(bundle_root).resolve(), staged, fetch)
        receipt = {'schema_version': 1, 'installer_version': '0.3.0', 'project': str(project), 'skills': records}
        setup_id = digest(canonical({'plan': plan, 'receipt': receipt}).encode())[:24]
        setup = metadata_root / ('setup-' + setup_id)
        metadata = {'project-plan.json': canonical(plan), 'skills.lock.json': canonical(receipt)}
        metadata.update({'roles/' + r['name'] + '.md': role_text(r, {e['id']:e['install_name'] for e in selected}) for r in plan.get('roles', [])})
        created_dirs = []
        for directory in [project/'.agents', skill_root, metadata_root]:
            check_directory(directory)
            if not directory.exists():
                directory.mkdir(); created_dirs.append(directory)
        lock = metadata_root / 'install.lock'
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            raise SetupError('Another setup holds the project installation lock')
        os.close(fd)
        created_skills = []; created_setup = False; unchanged = []
        try:
            project_paths(project)
            for record in records:
                destination = skill_root / record['name']
                if destination.exists() or destination.is_symlink():
                    if validate_skill(destination, record['name']) != record['file_sha256']:
                        raise SetupError(f'Existing skill differs; preserve and review it: {destination}')
                    unchanged.append(record['name'])
            if setup.exists() or setup.is_symlink():
                check_directory(setup)
                if tree_hashes(setup) != {name: digest(text.encode()) for name, text in metadata.items()}:
                    raise SetupError('Existing immutable setup record differs')
            # Stage on the destination filesystem; rename only complete folders.
            with tempfile.TemporaryDirectory(prefix='.skillosophy-stage-', dir=project/'.agents') as stage_temp:
                on_disk = Path(stage_temp)
                for record in records:
                    name = record['name']
                    if name not in unchanged:
                        shutil.copytree(staged/name, on_disk/name)
                for record in records:
                    name = record['name']
                    if name not in unchanged:
                        if (skill_root/name).exists() or (skill_root/name).is_symlink():
                            raise SetupError('Destination changed during setup')
                        os.rename(on_disk/name, skill_root/name); created_skills.append(skill_root/name)
                if not setup.exists():
                    temporary_setup = on_disk/'setup'; temporary_setup.mkdir()
                    for name, text in metadata.items():
                        path = temporary_setup/name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text, encoding='utf-8')
                    os.rename(temporary_setup, setup); created_setup = True
        except BaseException:
            if created_setup:
                shutil.rmtree(setup)
            for path in reversed(created_skills):
                shutil.rmtree(path)
            raise
        finally:
            lock.unlink()
            for directory in reversed(created_dirs):
                try: directory.rmdir()
                except OSError: pass
        preview.update({'installed': [p.name for p in created_skills], 'unchanged': unchanged,
                        'setup_record': str(setup), 'receipt': str(setup/'skills.lock.json')})
        return preview

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('catalog')
    cmd = commands.add_parser('install')
    cmd.add_argument('--project', required=True, type=Path)
    cmd.add_argument('--plan', required=True, type=Path)
    cmd.add_argument('--bundle-root', type=Path, default=BUNDLE_ROOT)
    cmd.add_argument('--apply', action='store_true')
    cmd.add_argument('--catalog', type=Path, help='Reviewed external catalog extension; does not replace bundled entries')
    args = parser.parse_args()
    try:
        entries = load_catalog()
        if args.command == 'catalog':
            print(canonical(list(entries.values())), end='')
        else:
            if args.catalog:
                extension = load_catalog(args.catalog, known_dependencies=entries)
                for key, entry in extension.items():
                    if entry['source']['type'] != 'github' or not entry['source'].get('review_sha256') or entry.get('evidence',{}).get('status') != 'reviewed_source_unmeasured':
                        raise SetupError('External catalog entries require inspected source hashes and review notes')
                    if key in entries or entry['install_name'] in {e['install_name'] for e in entries.values()}:
                        raise SetupError('External catalog collides with an existing skill')
                    entries[key] = entry
            plan = json.loads(args.plan.read_text())
            print(canonical(install(args.project, plan, entries, args.bundle_root, args.apply)), end='')
    except (SetupError, OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        parser.exit(1, f'Skillosophy: {error}\n')

if __name__ == '__main__':
    main()
