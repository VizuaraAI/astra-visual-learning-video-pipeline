"""Wait for an explicitly selected repair, stage a new run, assemble and verify download."""
from pathlib import Path
import json,time,argparse
import modal
from manage import status,APP,ROOT
from monitor_production import observe

def run(cache,base_cache,masters,base='quality-v2',repair='valve-repair',final='quality-final'):
    cache.mkdir(parents=True,exist_ok=True);ledger=cache/'stage-call.json'
    shots=[5,10,13];manifest=json.loads((ROOT/'storyboards/heart.json').read_text())
    expected=sum(s['frames'] for s in manifest['shots'])
    repaired=sum(s['frames'] for s in manifest['shots'] if s['index'] in shots)
    while not ledger.exists():
        status(base,base_cache/'metrics');status(repair,cache/'metrics')
        a=json.loads((base_cache/'metrics/status.json').read_text()).get('heart',{})
        progress=cache/'metrics/status.json'
        b=json.loads(progress.read_text()).get('heart',{}) if progress.exists() else {}
        if b.get('failed'):raise RuntimeError('A repair worker failed; inspect its metrics')
        if a.get('frames')==expected and b.get('frames')==repaired:
            fc=modal.Function.from_name(APP,'stage_repaired_chapter').spawn('heart',base,repair,final,shots)
            ledger.write_text(json.dumps(dict(call_id=fc.object_id,complete=False),indent=2));break
        time.sleep(60)
    state=json.loads(ledger.read_text())
    while not state['complete']:
        try:result=modal.FunctionCall.from_id(state['call_id']).get(timeout=0)
        except (TimeoutError,modal.exception.TimeoutError):time.sleep(30);continue
        state.update(complete=True,result=result);ledger.write_text(json.dumps(state,indent=2))
    observe(final,cache/'final',masters,['heart'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cache',type=Path,required=True);p.add_argument('--base-cache',type=Path,required=True);p.add_argument('--masters',type=Path,required=True);a=p.parse_args();run(a.cache,a.base_cache,a.masters)
