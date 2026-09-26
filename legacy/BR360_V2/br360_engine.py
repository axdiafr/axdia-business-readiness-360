#!/usr/bin/env python3
import argparse,json,hashlib,os,glob
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def _load_json(path):
    with Path(path).open(encoding='utf-8') as fh:
        return json.load(fh)

def load_controls():
    out=[]
    for p in sorted((ROOT/'business-readiness-360'/'controls').glob('*.json')):
        out.extend(_load_json(p)['controls'])
    return out

def load_profiles():
    return {p['id']:p for p in _load_json(ROOT/'business-readiness-360'/'profiles'/'PROFILES.json')['profiles']}

def detect_project(path):
    p=Path(path); facts=set(); evidence=[]
    def hit(f,reason): facts.add(f); evidence.append({'fact':f,'reason':reason})
    names={x.name for x in p.iterdir()} if p.exists() and p.is_dir() else set()
    if 'package.json' in names:
        hit('language.javascript','package.json')
        try:
            pkg=_load_json(p/'package.json'); deps={**pkg.get('dependencies',{}),**pkg.get('devDependencies',{})}
            if any(x in deps for x in ['react','next','vue','svelte']): hit('has_web_ui','JS UI framework dependency')
            if any(x in deps for x in ['electron']): hit('has_desktop','electron dependency')
            if '@capacitor/core' in deps: hit('has_mobile','Capacitor dependency')
            if any(x in deps for x in ['openai','@anthropic-ai/sdk','anthropic']): hit('uses_ai','AI provider dependency')
            if any(x in deps for x in ['stripe']): hit('has_billing','billing dependency')
            if pkg.get('bin'): hit('has_cli','package.json bin')
        except Exception: pass
    if {'pyproject.toml','requirements.txt'} & names: hit('language.python','python manifest')
    if 'go.mod' in names: hit('language.go','go.mod')
    if 'Cargo.toml' in names: hit('language.rust','Cargo.toml')
    if 'index.html' in names or (p/'public').exists() or (p/'app').exists(): hit('has_human_ui','UI surface')
    if any((p/x).exists() for x in ['openapi.yaml','openapi.json']): hit('has_api','OpenAPI contract')
    if any((p/x).exists() for x in ['asyncapi.yaml','asyncapi.json']): hit('has_event_api','AsyncAPI contract')
    if (p/'.github'/'workflows').exists(): hit('has_ci','.github/workflows')
    if any((p/x).exists() for x in ['Dockerfile','docker-compose.yml','compose.yaml']): hit('has_containers','container config')
    if any((p/x).exists() for x in ['vercel.json','railway.json','render.yaml','fly.toml']): hit('production_service','hosting config')
    if (p/'android').exists() or (p/'ios').exists(): hit('has_mobile','native mobile directory')
    if (p/'src-tauri').exists(): hit('has_desktop','Tauri directory')
    if any((p/x).exists() for x in ['LICENSE','LICENSE.md','LICENSE.txt']): hit('open_source','license file')
    # conservative pattern facts
    text=''
    for fn in ['README.md','package.json','pyproject.toml']:
        q=p/fn
        if q.exists():
            try:text += q.read_text(errors='ignore')[:200000]
            except: pass
    low=text.lower()
    if any(k in low for k in ['tenant_id','organization_id','workspace_id']): hit('multi_tenant','tenant identifier pattern')
    if any(k in low for k in ['supabase','firebase','next-auth','authentication']): hit('has_auth','auth pattern')
    if any(k in low for k in ['entitlement','subscription','plan_id']): hit('has_entitlements','entitlement pattern')
    if any(k in low for k in ['api/','fastapi','express']): hit('has_api','API pattern')
    if 'uses_ai' in facts: hit('commercial_product','AI product candidate')
    if 'has_human_ui' in facts: facts.add('has_web_ui')
    if 'production_service' in facts or 'has_api' in facts: facts.add('has_backend')
    return {'facts':sorted(facts),'evidence':evidence}

def control_applicability(c,facts):
    r=c.get('applicability',{}); f=set(facts)
    anyf=r.get('facts_any',[]); allf=r.get('facts_all',[]); notf=r.get('not_facts',[])
    if notf and any(x in f for x in notf): return 'NOT_APPLICABLE','negative fact matched'
    if allf and not all(x in f for x in allf): return r.get('default','NOT_APPLICABLE'),'required facts absent'
    if anyf and not any(x in f for x in anyf): return r.get('default','NOT_APPLICABLE'),'no applicability fact matched'
    return 'REQUIRED' if anyf or allf else r.get('default','RECOMMENDED'),'applicability facts matched' if anyf or allf else 'default policy'

def select_controls(facts,profile='AUTO'):
    profs=load_profiles(); p=profs.get(profile,profs['AUTO']); out=[]
    controls=load_controls()
    by_domain={}
    for c in controls:
        by_domain.setdefault(c['domain'],[]).append(c)
    for domain in p['included_domains']:
        for c in by_domain.get(domain,[]):
            status,reason=control_applicability(c,facts)
            out.append({'control_id':c['id'],'domain':c['domain'],'applicability':status,'reason':reason,'automation':c['automation']})
    return out

def score(evaluations):
    vals={'PASS':1.0,'PARTIAL':0.5,'FAIL':0.0}
    applicable=[e for e in evaluations if e.get('applicability')!='NOT_APPLICABLE']
    scored=[e for e in applicable if e.get('status') in vals]
    impl=10*sum(vals[e['status']] for e in scored)/len(applicable) if applicable else 0
    verified=[e for e in applicable if e.get('evidence_level') in ['E2_TESTED','E3_RUNTIME','E4_REAL_WORLD']]
    verification=10*len(verified)/len(applicable) if applicable else 0
    rw=[e for e in applicable if e.get('automation')=='REAL_WORLD_REQUIRED']
    rw_ok=[e for e in rw if e.get('evidence_level')=='E4_REAL_WORLD' and e.get('status') in ['PASS','PARTIAL']]
    real=10*len(rw_ok)/len(rw) if rw else 10
    coverage=len(scored)/len(applicable) if applicable else 0
    readiness=(.45*impl+.30*verification+.25*real) if rw else (.60*impl+.40*verification)
    if rw and real==0: readiness=min(readiness,6.5)
    if verification<5: readiness=min(readiness,7.5)
    if coverage<.70: readiness=min(readiness,8.0)
    return {'implementation':round(impl,2),'verification':round(verification,2),'real_world_evidence':round(real,2),'readiness':round(readiness,2),'coverage':round(coverage,4)}

def fingerprint(f):
    s='|'.join(str(f.get(k,'')) for k in ['audit_domain','affected_asset','control_id','package_or_resource','issue_identifier','location'])
    return hashlib.sha256(s.encode()).hexdigest()[:24]

def compare(a,b):
    A={x['fingerprint']:x for x in a.get('findings',[]) if x.get('fingerprint')}; B={x['fingerprint']:x for x in b.get('findings',[]) if x.get('fingerprint')}
    return {'new_findings':sorted(set(B)-set(A)),'resolved_findings':sorted(set(A)-set(B)),'persistent_findings':sorted(set(A)&set(B)),'score_delta':{k:b.get('scores',{}).get(k,0)-a.get('scores',{}).get(k,0) for k in ['implementation','verification','real_world_evidence','readiness']}}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--project',default='.'); ap.add_argument('--profile',default='AUTO'); ap.add_argument('--out')
    args=ap.parse_args(); det=detect_project(args.project); selected=select_controls(det['facts'],args.profile)
    result={'schema':'BR360-2','pack_version':'2.0.0','audit':{'id':'local-preanalysis','mode':'READ_ONLY','profile':args.profile,'created_at':None,'network_intent':[]},'project_profile':det,'applicability':{'controls':selected},'coverage':{'automated':0,'manual':0,'real_world':0,'overall':0},'scores':{'implementation':0,'verification':0,'real_world_evidence':0,'readiness':0,'confidence':0,'evidence_strength':0},'maturity':{'level':0,'name':'ABSENT'},'findings':[],'actions':[],'blockers':[],'audit_self_evaluation':{'audit_coverage':0,'audit_confidence':0,'missing_tools':[],'missing_access':[],'missing_real_world_data':[],'unverified_assumptions':['Pre-analysis only; no checks executed.'],'license_review_gaps':[]},'final':{'status':'PARTIAL','summary':'Pre-analysis only; selected controls are not evidence of PASS.'},'extensions':{}}
    s=json.dumps(result,indent=2)
    if args.out: Path(args.out).write_text(s+'\n')
    else: print(s)
if __name__=='__main__': main()
