import json
import tempfile
import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runtime'))
import br360_engine as e


class BR360V3Tests(unittest.TestCase):
    def test_json_files_parse(self):
        for p in ROOT.rglob('*.json'):
            with self.subTest(p=p):
                with p.open(encoding='utf-8') as fh:
                    json.load(fh)

    def test_control_ids_unique_and_stable(self):
        cs = e.load_controls(); ids = [c['id'] for c in cs]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 100)
        for i in ids:
            self.assertRegex(i, r'^BR360-[A-Z0-9]+-[0-9]{3}$')

    def test_required_control_fields(self):
        req = {'id','title','domain','description','applicability','severity_default','evidence_required','automation','detectors','checks','manual_questions','pass_condition','partial_condition','fail_condition','not_applicable_condition','references'}
        for c in e.load_controls():
            self.assertTrue(req <= set(c), c['id'])

    def test_profiles_reference_domains(self):
        domains = {c['domain'] for c in e.load_controls()}
        for p in e.load_profiles().values():
            self.assertTrue(set(p['included_domains']) <= domains, p['id'])

    def test_na_handling(self):
        sel = e.select_controls(['open_source'], 'AUTO')
        a11y = [x for x in sel if x['domain'] == 'accessibility']
        self.assertTrue(a11y)
        self.assertTrue(all(x['applicability'] == 'NOT_APPLICABLE' for x in a11y))

    def test_scoring_real_world_gate(self):
        ev = [{'applicability':'REQUIRED','status':'PASS','evidence_level':'E2_TESTED','automation':'REAL_WORLD_REQUIRED'} for _ in range(10)]
        s = e.score(ev)
        self.assertEqual(s['real_world_evidence'], 0)
        self.assertLessEqual(s['readiness'], 6.5)

    def test_scoring_na_excluded(self):
        ev = [
            {'applicability':'NOT_APPLICABLE','status':'FAIL','evidence_level':'E0_CLAIM_ONLY','automation':'MANUAL'},
            {'applicability':'REQUIRED','status':'PASS','evidence_level':'E2_TESTED','automation':'AUTOMATED'},
        ]
        s = e.score(ev)
        self.assertEqual(s['implementation'], 10)

    def test_scoring_without_real_world_controls_renormalizes(self):
        ev = [{'applicability':'REQUIRED','status':'FAIL','evidence_level':'E0_CLAIM_ONLY','automation':'AUTOMATED'}]
        s = e.score(ev)
        self.assertEqual(s['implementation'], 0)
        self.assertEqual(s['verification'], 0)
        self.assertEqual(s['readiness'], 0)

    def test_golden_determinism_preserved(self):
        for p in sorted((ROOT / 'tests' / 'golden').glob('*.json')):
            with p.open(encoding='utf-8') as fh:
                g = json.load(fh)
            with (ROOT / 'tests' / 'fixtures' / g['fixture'] / 'project_facts.json').open(encoding='utf-8') as fh:
                f = json.load(fh)
            got = [{'control_id':x['control_id'],'applicability':x['applicability']} for x in e.select_controls(f['facts'], g['profile'])]
            self.assertEqual(g['selected'], got, g['fixture'])

    def test_manifest_v3_execution_commands(self):
        m = json.loads((ROOT / 'business-readiness-360.framework.json').read_text(encoding='utf-8'))
        self.assertEqual(m['version'], 3)
        self.assertIn('python3 runtime/br360_engine.py selftest', m['test_commands'])
        self.assertIn('business-readiness-360/detectors/CONTROL_DETECTORS.json', m['files'])

    def test_references_no_code_copy(self):
        refs = json.loads((ROOT / 'business-readiness-360' / 'references' / 'BR360_REFERENCES.json').read_text(encoding='utf-8'))['references']
        self.assertTrue(refs)
        self.assertTrue(all(r['code_copied'] is False for r in refs))

    def test_evidence_graph_chain(self):
        g = json.loads((ROOT / 'business-readiness-360' / 'evidence' / 'EVIDENCE_GRAPH.json').read_text(encoding='utf-8'))
        self.assertEqual(g['chain'], ['Requirement','Detector','Check','Observation','Evidence','Evaluation','Finding','Score','Decision','Action'])
        self.assertEqual(g['legacy_chain_v2'], ['Requirement','Detector','Check','Observation','Finding','Evidence','Score','Decision','Action'])

    def test_fingerprint_and_compare(self):
        f = {'audit_domain':'security','affected_asset':'api','control_id':'BR360-SEC-002','package_or_resource':'pkg','issue_identifier':'CVE-X','location':'x'}
        a = e.fingerprint(f); b = e.fingerprint(dict(f))
        self.assertEqual(a, b)
        f2 = dict(f); f2['location'] = 'y'
        self.assertNotEqual(a, e.fingerprint(f2))
        before = {'findings':[{'fingerprint':a}],'scores':{'readiness':4,'implementation':5,'verification':3,'real_world_evidence':1},'maturity':{'level':1}}
        after = {'findings':[{'fingerprint':e.fingerprint(f2)}],'scores':{'readiness':6,'implementation':7,'verification':5,'real_world_evidence':2},'maturity':{'level':3}}
        d = e.compare(before, after)
        self.assertEqual(d['new_findings'], [e.fingerprint(f2)])
        self.assertEqual(d['resolved_findings'], [a])
        self.assertEqual(d['score_delta']['readiness'], 2)
        self.assertEqual(d['maturity_delta'], 2)

    def test_adapters_are_candidates_and_network_explicit(self):
        ads = e.load_adapters()
        self.assertTrue(ads)
        self.assertEqual(len(ads), 11)
        for a in ads:
            self.assertEqual(a['build_command']['status'], 'CANDIDATE', a['id'])
            self.assertIn('network_intent', a)
            self.assertIn('network_required', a['network_intent'])
            self.assertIn('destination_type', a['network_intent'])
            self.assertIn('reason', a['network_intent'])
            self.assertIn('read_only', a['network_intent'])
            self.assertIn('cost_possible', a['network_intent'])

    def test_maturity_model_is_complete_and_ordered(self):
        m = json.loads((ROOT / 'business-readiness-360' / 'maturity' / 'MATURITY_MODEL.json').read_text(encoding='utf-8'))
        self.assertEqual([(x['level'],x['name']) for x in m['levels']], [(0,'ABSENT'),(1,'AD_HOC'),(2,'REPEATABLE'),(3,'DEFINED'),(4,'MEASURED'),(5,'OPTIMIZED')])
        self.assertIn('algorithm', m)

    def test_detector_smoke_v2_compatibility(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p/'package.json').write_text(json.dumps({'dependencies':{'next':'1','stripe':'1','openai':'1'}}))
            (p/'index.html').write_text('<html></html>')
            (p/'openapi.json').write_text('{}')
            (p/'vercel.json').write_text('{}')
            (p/'LICENSE').write_text('test')
            (p/'README.md').write_text('organization_id authentication entitlement')
            got = set(e.detect_project(p)['facts'])
            for fact in ['language.javascript','has_web_ui','has_human_ui','has_api','has_billing','uses_ai','production_service','open_source','multi_tenant','has_auth','has_entitlements','has_backend']:
                self.assertIn(fact, got)

    def test_all_automated_controls_have_builtin_detector(self):
        automated = [c for c in e.load_controls() if c['automation'] == 'AUTOMATED']
        self.assertEqual(len(automated), 15)
        self.assertTrue(all(c['detectors'] for c in automated))
        for c in automated:
            self.assertTrue(any(d in e.BUILTIN_CHECKS for d in c['detectors']), c['id'])

    def test_all_control_conditions_are_specific_not_v2_template(self):
        generic = 'Required evidence is present, current, scoped to the applicable project surface, and no material contradiction remains.'
        controls = e.load_controls()
        self.assertTrue(all(c['pass_condition'] != generic for c in controls))
        self.assertEqual(len({c['pass_condition'] for c in controls}), len(controls))

    def test_secret_scan_pass_and_fail(self):
        c = next(x for x in e.load_controls() if x['id'] == 'BR360-SEC-002')
        with tempfile.TemporaryDirectory() as d:
            p = Path(d); (p/'app.py').write_text('print("safe")')
            good = e.execute_control(p, c, 'RECOMMENDED', set())
            self.assertEqual(good['status'], 'PASS')
            (p/'config.js').write_text('const token="' + 'ghp_' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890' + '";')
            bad = e.execute_control(p, c, 'RECOMMENDED', set())
            self.assertEqual(bad['status'], 'FAIL')
            self.assertTrue(all('ghp_' not in json.dumps(x) for x in bad['evidence']))

    def test_api_contract_pass(self):
        c = next(x for x in e.load_controls() if x['id'] == 'BR360-API-001')
        with tempfile.TemporaryDirectory() as d:
            p = Path(d); (p/'openapi.json').write_text(json.dumps({'openapi':'3.1.0','paths':{}}))
            got = e.execute_control(p, c, 'REQUIRED', {'has_api'})
            self.assertEqual(got['status'], 'PASS')

    def test_dependency_inventory_partial_then_pass(self):
        c = next(x for x in e.load_controls() if x['id'] == 'BR360-SC-001')
        with tempfile.TemporaryDirectory() as d:
            p = Path(d); (p/'package.json').write_text('{}')
            self.assertEqual(e.execute_control(p,c,'RECOMMENDED',set())['status'], 'PARTIAL')
            (p/'package-lock.json').write_text('{}')
            self.assertEqual(e.execute_control(p,c,'RECOMMENDED',set())['status'], 'PASS')

    def test_license_control(self):
        c = next(x for x in e.load_controls() if x['id'] == 'BR360-LIC-001')
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            self.assertEqual(e.execute_control(p,c,'RECOMMENDED',set())['status'], 'FAIL')
            (p/'LICENSE').write_text('MIT')
            self.assertEqual(e.execute_control(p,c,'RECOMMENDED',set())['status'], 'PASS')

    def test_external_evidence_real_world(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p/'package.json').write_text(json.dumps({'dependencies':{'next':'1'}}))
            (p/'index.html').write_text('<html></html>')
            evfile = p/'evidence.json'
            evfile.write_text(json.dumps({'evaluations':[{
                'control_id':'BR360-PROD-005','status':'PASS','evidence_level':'E4_REAL_WORLD',
                'summary':'Interview + feedback loop evidence','source':'customer-interviews','authority':0.9,'confidence':0.9
            }]}))
            r = e.audit(p, evidence_path=str(evfile))
            row = next(x for x in r['evaluations'] if x['control_id']=='BR360-PROD-005')
            self.assertEqual(row['status'], 'PASS')
            self.assertEqual(row['evidence_level'], 'E4_REAL_WORLD')

    def test_audit_generates_evaluations_evidence_and_scores(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p/'package.json').write_text(json.dumps({'dependencies':{'next':'1'},'license':'MIT'}))
            (p/'package-lock.json').write_text('{}')
            (p/'index.html').write_text('<html></html>')
            (p/'LICENSE').write_text('MIT')
            (p/'vercel.json').write_text(json.dumps({'headers':[]}))
            r = e.audit(p)
            self.assertEqual(r['schema'], 'BR360-3')
            self.assertEqual(r['pack_version'], '3.0.0')
            self.assertTrue(r['evaluations'])
            self.assertIn('confidence', r['scores'])
            self.assertIn('evidence_strength', r['scores'])
            self.assertIn(r['maturity']['level'], range(6))
            self.assertIn(r['final']['status'], {'PASS','PARTIAL','FAIL','BLOCKED'})

    def test_preanalysis_still_does_not_claim_pass(self):
        with tempfile.TemporaryDirectory() as d:
            r = e.preanalyse(d)
            self.assertEqual(r['final']['status'], 'PARTIAL')
            self.assertEqual(r['findings'], [])
            self.assertEqual(r['evaluations'], [])


    def test_adapter_results_feed_control_evaluations(self):
        rows = [
            {'control_id':'BR360-SEC-002','domain':'security','title':'Secrets','applicability':'RECOMMENDED','automation':'AUTOMATED','status':'PASS','evidence_level':'E2_TESTED','evidence':[],'summary':'builtin','source_method':'builtin'},
            {'control_id':'BR360-SC-002','domain':'supply-chain','title':'SBOM','applicability':'RECOMMENDED','automation':'SEMI_AUTOMATED','status':'NOT_TESTED','evidence_level':'E0_CLAIM_ONLY','evidence':[],'summary':'missing','source_method':'builtin'},
        ]
        runs = [
            {'id':'gitleaks','status':'FINDINGS','summary':'gitleaks findings: 1','raw_output_digest':'abc'},
            {'id':'syft','status':'PASS','summary':'SBOM components: 12','raw_output_digest':'def'},
        ]
        out = e.apply_adapter_runs(rows, runs)
        sec = next(x for x in out if x['control_id']=='BR360-SEC-002')
        sbom = next(x for x in out if x['control_id']=='BR360-SC-002')
        self.assertEqual(sec['status'], 'FAIL')
        self.assertEqual(sec['evidence_level'], 'E2_TESTED')
        self.assertEqual(sbom['status'], 'PASS')
        self.assertEqual(sbom['evidence_level'], 'E2_TESTED')

    def test_selftest_passes(self):
        s = e.selftest()
        self.assertEqual(s['status'], 'PASS', s)
        self.assertEqual(s['counts']['automated_controls'], 15)
        self.assertEqual(s['counts']['builtin_detectors'], 15)

    def test_result_schema_is_v3(self):
        s = json.loads((ROOT/'BUSINESS_READINESS_360_RESULT.schema.json').read_text(encoding='utf-8'))
        self.assertEqual(s['properties']['schema']['const'], 'BR360-3')
        self.assertEqual(s['properties']['pack_version']['const'], '3.0.0')
        self.assertIn('evaluations', s['required'])
        self.assertIn('evidence', s['required'])

    def test_v2_snapshot_exists(self):
        self.assertTrue((ROOT/'legacy'/'BR360_V2'/'br360_engine.py').exists())
        self.assertTrue((ROOT/'legacy'/'BR360_V2'/'BUSINESS_READINESS_360_RESULT.schema.json').exists())


if __name__ == '__main__':
    unittest.main()
