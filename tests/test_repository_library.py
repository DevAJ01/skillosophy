"""Verify full folders and real selector/installer behavior; no AI superiority claims."""
import importlib.util,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('repo_selector',ROOT/'scripts/library/select.py');lib=importlib.util.module_from_spec(spec);spec.loader.exec_module(lib)
class RepositoryLibraryTests(unittest.TestCase):
 def test_all_folders_match_recorded_files_and_license(self):
  r=lib.validate();self.assertGreaterEqual(r['skill_folders'],500);self.assertFalse(r['failures']);self.assertFalse(r['behavioral_improvement_proven'])
  for e in lib.entries():self.assertTrue((ROOT/'library'/e['path']/'UPSTREAM-LICENSE.txt').is_file())
 def test_discovery_reads_metadata_without_skill_bodies(self):
  original=Path.read_text
  def read(path,*args,**kwargs):
   if path.name in ('SKILL.md','UPSTREAM.md'):self.fail('Search loaded a skill body')
   return original(path,*args,**kwargs)
  with patch.object(Path,'read_text',read):r=lib.shortlist('RAG retrieval policy documents access permissions',8)
  self.assertEqual(r['skill_bodies_loaded'],0);self.assertTrue(any('rag' in e['name'] for e in r['results']))
 def test_domain_filter_excludes_unrelated_scaffolding(self):
  r=lib.shortlist('React TypeScript dashboard keyboard accessibility',8,domain='frontend')
  self.assertTrue(any(e['name']=='senior-frontend' for e in r['results']))
  self.assertFalse(any(e['name']=='mcp-server-builder' for e in r['results']))
  self.assertTrue(all(lib.domain_match(e,'frontend') for e in r['results']))
 def test_authored_notices_and_upstream_baselines_are_preserved(self):
  for e in lib.entries():
   if e['status']=='skillosophy_candidate':
    folder=ROOT/'library'/e['path'];self.assertEqual((folder/'SKILLOSOPHY-LICENSE.txt').read_bytes(),(ROOT/'LICENSE').read_bytes());self.assertTrue((folder/'UPSTREAM.md').is_file())
 def test_no_match_does_not_invent_a_selection(self):self.assertEqual(lib.shortlist('qzxvwunknownterm',8)['results'],[])
 def test_revised_filter_does_not_label_upstream_as_authored(self):
  r=lib.shortlist('React frontend dashboard',20,revised=True)
  self.assertTrue(r['results']);self.assertTrue(all(e['status']=='skillosophy_candidate' for e in r['results']))
 def test_limits_and_blank_queries(self):
  for query,limit in [('',8),('database',0),('database',21)]:
   with self.assertRaises(lib.setup.SetupError):lib.shortlist(query,limit)
 def test_missing_resources_block_before_project_mutation(self):
  e=next(e for e in lib.entries() if e['unresolved_entrypoint_links'])
  with tempfile.TemporaryDirectory() as t:
   with self.assertRaisesRegex(lib.setup.SetupError,'Missing'):lib.install([e['name']],Path(t),'Source review test',True)
   self.assertEqual(list(Path(t).iterdir()),[])
 def test_changed_reviewed_files_block_before_project_writes(self):
  es=lib.entries();e=next(e for e in es if e['name']=='api-design-reviewer');e['file_sha256']['SKILL.md']='0'*64
  with patch.object(lib,'entries',return_value=es),tempfile.TemporaryDirectory() as t:
   with self.assertRaisesRegex(lib.setup.SetupError,'hashes'):lib.install([e['name']],Path(t),'Source review test',True)
   self.assertEqual(list(Path(t).iterdir()),[])
 def test_actual_install_roles_receipt_repeat_and_instruction_preservation(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t);(root/'AGENTS.md').write_text('Preserve original data and our stack.')
   r=lib.install(['api-design-reviewer','senior-frontend'],root,'Reviewed entrypoints, preserved tools/resources, MIT notices and stack compatibility; no services or scripts executed.',False)
   self.assertEqual(r['mode'],'dry-run');self.assertEqual(len(list(root.iterdir())),1)
   r=lib.install(['api-design-reviewer','senior-frontend'],root,'Actual source review fixture',True)
   self.assertEqual(len(r['installed']),2);self.assertEqual((root/'AGENTS.md').read_text(),'Preserve original data and our stack.')
   receipt=json.loads(Path(r['receipt']).read_text())
   for skill in receipt['skills']:self.assertEqual(lib.setup.tree_hashes(root/'.agents/skills'/skill['name']),skill['file_sha256'])
   role=(Path(r['setup_record'])/'roles/api-design-reviewer-specialist.md').read_text();self.assertIn('$api-design-reviewer',role)
   again=lib.install(['api-design-reviewer','senior-frontend'],root,'Actual source review fixture',True);self.assertFalse(again['installed']);self.assertEqual(len(again['unchanged']),2)
if __name__=='__main__':unittest.main()
