"""Integration checks for project writes, immutable sources, and preservation boundaries."""
import copy
import importlib.util
import io
import json
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('project_skills', ROOT/'skills/skillosophy-start/scripts/project_skills.py')
setup = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(setup)

def plan(skills=None):
    selected = skills or ['skillosophy-project-brief', 'skillosophy-acceptance-review']
    return {'schema_version':1,'project':{'goal':'Build a local CSV checker','deliverable':'A CLI and row audit','philosophy':{'priority':'Preserve originals','evidence':'Reconcile row counts'}},'skills':selected,'roles':[{'name':'reviewer','mission':'Check the requested behavior','skills':[selected[-1]],'done_when':'Important input cases have recorded evidence'}]}

def archive(entries):
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w') as z:
        for name,content,mode in entries:
            info=zipfile.ZipInfo(name);info.external_attr=mode<<16;z.writestr(info,content)
    return stream.getvalue()

class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.project=Path(self.temp.name)/'project';self.project.mkdir()
        (self.project/'AGENTS.md').write_text('User-owned instructions')
        self.catalog=setup.load_catalog()
    def tearDown(self):self.temp.cleanup()
    def install(self,p=None,**kw):return setup.install(self.project,p or plan(),self.catalog,apply=True,**kw)
    def test_dry_run_has_no_writes_or_download(self):
        before=sorted(str(p.relative_to(self.project)) for p in self.project.rglob('*'))
        result=setup.install(self.project,plan(['pdf']),self.catalog,fetch=lambda *a: self.fail('Dry run fetched source'))
        self.assertEqual(before,sorted(str(p.relative_to(self.project)) for p in self.project.rglob('*')))
        self.assertEqual(result['mode'],'dry-run')
    def test_install_plan_roles_receipt_and_preserve_guidance(self):
        result=self.install(); record=Path(result['setup_record'])
        self.assertEqual(set(result['installed']),set(plan()['skills']))
        self.assertEqual((self.project/'AGENTS.md').read_text(),'User-owned instructions')
        self.assertFalse((self.project/'.codex').exists())
        self.assertEqual(json.loads((record/'project-plan.json').read_text()),plan())
        self.assertIn('$skillosophy-acceptance-review',(record/'roles/reviewer.md').read_text())
        receipt=json.loads(Path(result['receipt']).read_text())
        self.assertEqual(len(receipt['skills']),2)
        self.assertTrue(all(len(v)==64 for r in receipt['skills'] for v in r['file_sha256'].values()))
    def test_repeat_install_is_noop(self):
        first=self.install();second=self.install()
        self.assertEqual(second['installed'],[])
        self.assertEqual(set(second['unchanged']),set(plan()['skills']))
        self.assertEqual(first['setup_record'],second['setup_record'])
    def test_modified_skill_conflict_preserves_all_content(self):
        self.install(); entry=self.project/'.agents/skills/skillosophy-project-brief/SKILL.md';entry.write_text(entry.read_text()+'\nUSER EDIT\n')
        with self.assertRaisesRegex(setup.SetupError,'Existing skill differs'):self.install()
        self.assertTrue(entry.read_text().endswith('USER EDIT\n'))
        self.assertFalse((self.project/'.skillosophy/install.lock').exists())
    def test_conflict_prevents_install_of_other_selected_skill(self):
        self.install();p=plan(['skillosophy-project-brief','skillosophy-delivery-plan'])
        entry=self.project/'.agents/skills/skillosophy-project-brief/SKILL.md';entry.write_text(entry.read_text()+'\nUSER EDIT\n')
        with self.assertRaises(setup.SetupError):self.install(p)
        self.assertFalse((self.project/'.agents/skills/skillosophy-delivery-plan').exists())
    def test_failure_during_commit_rolls_back_only_created_skills(self):
        real=setup.os.rename;calls=[]
        def fail_second(src,dst):
            calls.append((src,dst))
            if len(calls)==2:raise OSError('Injected rename failure')
            return real(src,dst)
        with patch.object(setup.os,'rename',side_effect=fail_second):
            with self.assertRaises(OSError):self.install()
        self.assertFalse(list(self.project.glob('.agents/skills/*')))
        self.assertEqual((self.project/'AGENTS.md').read_text(),'User-owned instructions')
    def test_symlinked_skill_root_is_rejected(self):
        outside=Path(self.temp.name)/'outside';outside.mkdir();(self.project/'.agents').symlink_to(outside,target_is_directory=True)
        with self.assertRaises(setup.SetupError):self.install()
        self.assertEqual(list(outside.iterdir()),[])
    def test_symlinked_existing_skill_is_rejected(self):
        destination=self.project/'.agents/skills';destination.mkdir(parents=True)
        (destination/'skillosophy-project-brief').symlink_to(ROOT/'skills/skillosophy-project-brief',target_is_directory=True)
        with self.assertRaises(setup.SetupError):self.install()
    def test_install_lock_blocks_competing_setup(self):
        meta=self.project/'.skillosophy';meta.mkdir();(meta/'install.lock').write_text('Other installer')
        with self.assertRaisesRegex(setup.SetupError,'lock'):self.install()
        self.assertEqual((meta/'install.lock').read_text(),'Other installer')
    def test_immutable_setup_record_is_not_overwritten(self):
        r=self.install();entry=Path(r['setup_record'])/'project-plan.json';entry.write_text('User edit')
        with self.assertRaisesRegex(setup.SetupError,'immutable'):self.install()
        self.assertEqual(entry.read_text(),'User edit')
    def test_dependency_closure_installs_complete_council_bundle(self):
        result=self.install(plan(['philosopher-council']))
        self.assertEqual(len(result['installed']),12)
        reference=self.project/'.agents/skills/philosopher-selector/references/catalog.md'
        self.assertTrue(reference.exists())
        self.assertTrue((reference.parent/'../../philosopher-popper/SKILL.md').resolve().exists())
    def test_role_cannot_reference_an_unselected_skill(self):
        p=plan();p['roles'][0]['skills']=['pdf']
        with self.assertRaises(setup.SetupError):self.install(p)
        self.assertFalse((self.project/'.agents').exists())
    def test_invalid_and_unknown_selection_rejected(self):
        for ids in [['../escape'],['missing'],['pdf','pdf']]:
            with self.subTest(ids=ids):
                with self.assertRaises(setup.SetupError):self.install(plan(ids))
    def test_catalog_rejects_mutable_revision(self):
        data=json.loads(setup.CATALOG_PATH.read_text());external=next(e for e in data['entries'] if e['source']['type']=='github');external['source']['revision']='main'
        path=Path(self.temp.name)/'catalog.json';path.write_text(json.dumps(data))
        with self.assertRaises(setup.SetupError):setup.load_catalog(path)
    def test_source_failure_occurs_before_project_mutation(self):
        with self.assertRaises(OSError):self.install(plan(['pdf']),fetch=lambda *args: (_ for _ in ()).throw(OSError('Network unavailable')))
        self.assertEqual([p.name for p in self.project.iterdir()],['AGENTS.md'])
    def test_external_skill_preserves_license_helpers_and_does_not_execute(self):
        license_text=b'Checked fixture license'; source={'type':'github','repo':'owner/repo','revision':'1'*40,'path':'skills/example','license_path':'LICENSE.txt','license_sha256':setup.digest(license_text)}
        data=archive([('repo-root/skills/example/SKILL.md',b'---\nname: example\ndescription: Example\n---\nInstructions',0o100644),('repo-root/skills/example/LICENSE.txt',license_text,0o100644),('repo-root/skills/example/scripts/helper.py',b'raise RuntimeError("Do not execute")',0o100755)])
        entry={'id':'example','install_name':'example','source':source,'dependencies':[],'prerequisites':[]}
        r=setup.install(self.project,plan(['example']),{'example':entry},apply=True,fetch=lambda *args:data)
        dest=self.project/'.agents/skills/example'
        self.assertEqual((dest/'LICENSE.txt').read_bytes(),license_text)
        self.assertTrue((dest/'scripts/helper.py').exists())
        self.assertEqual(r['installed'],['example'])
    def test_archive_path_traversal_and_symlink_rejected(self):
        source={'path':'skills/example','license_path':'LICENSE.txt','license_sha256':'0'*64}
        for name,mode in [('repo-root/../escape',0o100644),('repo-root/skills/example/link',0o120777),('/escape',0o100644)]:
            with self.subTest(name=name):
                target=Path(self.temp.name)/'extract';target.mkdir(exist_ok=True)
                with self.assertRaises(setup.SetupError):setup.extract_skill(archive([(name,b'x',mode)]),source,target)
    def test_changed_external_license_rejected(self):
        source={'path':'skills/example','license_path':'LICENSE.txt','license_sha256':'0'*64}
        data=archive([('repo-root/skills/example/SKILL.md',b'---\nname: example\ndescription: Example\n---',0o100644),('repo-root/skills/example/LICENSE.txt',b'Changed license',0o100644)])
        with self.assertRaisesRegex(setup.SetupError,'license'):setup.extract_skill(data,source,Path(self.temp.name)/'extract')

if __name__=='__main__':unittest.main()
