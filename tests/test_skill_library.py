"""Observable discovery, review, and installation checks with controlled upstream fixtures."""
import copy
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/skillosophy-start/scripts'))
import skill_library as lib
import project_skills as setup
from test_project_install import archive, plan

REPO='author/library';REVISION='a'*40
SKILL=b'---\nname: data-audit\ndescription: Audit database query performance\n---\nUse references/check.md.\n'
LICENSE=b'MIT fixture license'

def fixture(extra=()):
    return archive([('root/skills/data-audit/SKILL.md',SKILL,0o100644),('root/LICENSE',LICENSE,0o100644),
                    ('root/NOTICE',b'Attribution fixture',0o100644),('root/skills/data-audit/references/check.md',b'Check cardinality',0o100644),
                    ('root/skills/data-audit/scripts/helper.py',b'raise RuntimeError("Never execute while installing")',0o100755),*extra])

class LibraryTests(unittest.TestCase):
    def setUp(self):self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def inspection(self,data=None):return lib.inspect(REPO,REVISION,name='data-audit',output=self.root/'inspection',data=data or fixture())
    def reviewed(self,dependencies=None):
        self.inspection();return lib.review(self.root/'inspection/inspection.json','Reviewed full instructions and fixture helper; MIT permits copying, no runtime execution.', 'MIT',['Python for later helper execution'],dependencies or [],self.root/'reviewed.json')
    def test_index_pins_metadata_and_never_marks_installable(self):
        indexed=lib.index_archive(REPO,REVISION,fixture());e=indexed['entries'][0]
        self.assertEqual(e['name'],'data-audit');self.assertEqual(e['revision'],REVISION)
        self.assertFalse(e['install_ready']);self.assertEqual(e['evidence']['status'],'unmeasured')
    def test_multiline_frontmatter_discovery(self):
        meta=lib.frontmatter('---\nname: example\ndescription: >-\n  First line\n  second line\nlicense: MIT\n---\nBody')
        self.assertEqual(meta['description'],'First line second line')
    def test_same_name_in_multiple_paths_requires_exact_selection(self):
        data=fixture([('root/other/data-audit/SKILL.md',SKILL,0o100644)])
        with self.assertRaisesRegex(setup.SetupError,'ambiguous'):self.inspection(data)
        r=lib.inspect(REPO,REVISION,path='skills/data-audit',output=self.root/'exact',data=data)
        self.assertEqual(r['candidate']['path'],'skills/data-audit')
    def test_live_search_has_popularity_not_success_and_filters_bad_sources(self):
        calls=[]
        def fetch(url):
            calls.append(url);return {'skills':[{'id':'author/library/data-audit','name':'data-audit','source':REPO,'installs':123},
                                               {'id':'bad','name':'example','source':'https://evil.test','installs':99999}]}
        result=lib.community_search('database query',fetch=fetch)
        self.assertEqual(len(result),1);self.assertEqual(result[0]['installs'],123)
        self.assertFalse(result[0]['install_ready']);self.assertEqual(result[0]['evidence']['status'],'unmeasured')
        self.assertIn('q=database+query',calls[0])
    def test_offline_search_makes_no_request(self):
        index=lib.index_archive(REPO,REVISION,fixture());path=self.root/'library.json';path.write_text(json.dumps(index))
        result=lib.search('database audit',True,library=path,fetch=lambda *a:self.fail('Network called'))
        self.assertTrue(any(e['name']=='data-audit' for e in result['offline_results']))
        self.assertEqual(result['community_status'],'not_requested')
    def test_network_failure_keeps_local_results_and_reports_unavailable(self):
        index=lib.index_archive(REPO,REVISION,fixture());path=self.root/'library.json';path.write_text(json.dumps(index))
        result=lib.search('database audit',library=path,fetch=lambda *a:(_ for _ in ()).throw(OSError('Service unavailable')))
        self.assertTrue(result['offline_results']);self.assertEqual(result['community_status'],'unavailable');self.assertTrue(result['warnings'])
    def test_inspection_preserves_root_license_notice_and_helpers(self):
        r=self.inspection();folder=self.root/'inspection/skill'
        self.assertEqual((folder/'UPSTREAM-LICENSE.txt').read_bytes(),LICENSE)
        self.assertTrue((folder/'UPSTREAM-NOTICE').exists());self.assertTrue((folder/'scripts/helper.py').exists())
        self.assertFalse(r['downloaded_code_executed']);self.assertEqual(r['status'],'requires_agent_review')
    def test_repository_license_does_not_replace_existing_upstream_notice(self):
        data=fixture([('root/skills/data-audit/UPSTREAM-LICENSE.txt',b'Original author MIT notice',0o100644)])
        report=self.inspection(data);folder=self.root/'inspection/skill'
        self.assertEqual((folder/'UPSTREAM-LICENSE.txt').read_bytes(),b'Original author MIT notice')
        self.assertEqual((folder/'REPOSITORY-LICENSE.txt').read_bytes(),LICENSE)
        self.assertEqual(report['source']['license_path'],'REPOSITORY-LICENSE.txt')
    def test_unlicensed_source_cannot_be_inspected_as_installable(self):
        data=archive([('root/skills/data-audit/SKILL.md',SKILL,0o100644)])
        with self.assertRaisesRegex(setup.SetupError,'license'):self.inspection(data)
        self.assertFalse((self.root/'inspection').exists())
    def test_missing_local_resource_blocks_review(self):
        data=archive([('root/skills/data-audit/SKILL.md',SKILL+b'[Missing](../other/SKILL.md)',0o100644),('root/LICENSE',LICENSE,0o100644)])
        self.inspection(data)
        with self.assertRaisesRegex(setup.SetupError,'missing local'):lib.review(self.root/'inspection/inspection.json','Review','MIT',[],[],self.root/'reviewed.json')
        self.assertFalse((self.root/'reviewed.json').exists())
    def test_changed_inspection_blocks_review(self):
        self.inspection();(self.root/'inspection/skill/SKILL.md').write_bytes(SKILL+b'Unreviewed edit')
        with self.assertRaisesRegex(setup.SetupError,'changed'):lib.review(self.root/'inspection/inspection.json','Review','MIT',[],[],self.root/'reviewed.json')
    def test_review_to_install_enforces_hashes_and_real_role_invocation(self):
        e=self.reviewed();project=self.root/'project';project.mkdir();(project/'AGENTS.md').write_text('Keep my guidance')
        entries=setup.load_catalog(self.root/'reviewed.json');r=setup.install(project,plan([e['id']]),entries,apply=True,fetch=lambda *a:fixture())
        self.assertEqual(r['installed'],['data-audit']);self.assertEqual((project/'AGENTS.md').read_text(),'Keep my guidance')
        role=(Path(r['setup_record'])/'roles/reviewer.md').read_text()
        self.assertIn('$data-audit',role);self.assertNotIn('$community-',role)
        self.assertEqual(setup.tree_hashes(project/'.agents/skills/data-audit'),e['source']['review_sha256'])
    def test_changed_download_fails_before_any_project_write(self):
        e=self.reviewed();project=self.root/'project';project.mkdir()
        changed=fixture([('root/skills/data-audit/unreviewed.md',b'New instructions',0o100644)])
        with self.assertRaisesRegex(setup.SetupError,'differ from'):setup.install(project,plan([e['id']]),{e['id']:e},apply=True,fetch=lambda *a:changed)
        self.assertEqual(list(project.iterdir()),[])
    def test_invalid_dependency_does_not_corrupt_existing_catalog(self):
        self.inspection();path=self.root/'reviewed.json';path.write_text('{"schema_version":1,"entries":[]}');before=path.read_bytes()
        with self.assertRaises(setup.SetupError):lib.review(self.root/'inspection/inspection.json','Review','MIT',[],['missing'],path)
        self.assertEqual(path.read_bytes(),before)
    def test_bundled_dependency_can_be_recorded(self):
        e=self.reviewed(['philosopher-popper']);entries=setup.load_catalog(self.root/'reviewed.json',known_dependencies=setup.load_catalog())
        self.assertEqual(entries[e['id']]['dependencies'],['philosopher-popper'])
    def test_invalid_refs_and_query_bounds(self):
        for query in ['x','a'*201]:
            with self.assertRaises(setup.SetupError):lib.community_search(query,fetch=lambda *a:self.fail('Network called'))
        with self.assertRaises(setup.SetupError):lib.resolve_revision('https://evil.test')
        with self.assertRaises(setup.SetupError):lib.resolve_revision(REPO,'main?token=secret')

if __name__=='__main__':unittest.main()
