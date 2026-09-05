"""Resume-safe local observer: assemble each complete chapter and download its master."""
from pathlib import Path
import argparse,json,time,os,hashlib
import modal
from manage import status,APP,VOL,ROOT

def observe(run,cache,masters,chapters=None):
    cache.mkdir(parents=True,exist_ok=True);masters.mkdir(parents=True,exist_ok=True)
    ledgerpath=cache/'assembly-calls.json';ledger=json.loads(ledgerpath.read_text()) if ledgerpath.exists() else {}
    expected={name:sum(s['frames'] for s in json.loads((ROOT/'storyboards'/f'{name}.json').read_text())['shots']) for name in (chapters or ['cell','heart','dna'])}
    v=modal.Volume.from_name(VOL);f=modal.Function.from_name(APP,'assemble')
    while True:
        status(run,cache/'metrics')
        report_path=cache/'metrics/status.json'
        report=json.loads(report_path.read_text()) if report_path.exists() else {}
        state=dict(run=run,expected_frames=expected,chapters=report,downloaded=[])
        (cache/'production-state.json').write_text(json.dumps(state,indent=2))
        for name,n in expected.items():
            r=report.get(name,{})
            if r.get('frames')==n and name not in ledger:
                ledger[name]=dict(call_id=f.spawn(name,run).object_id,complete=False)
                ledgerpath.write_text(json.dumps(ledger,indent=2));print('ASSEMBLY QUEUED',name,flush=True)
            if name in ledger and not ledger[name]['complete']:
                try:result=modal.FunctionCall.from_id(ledger[name]['call_id']).get(timeout=0)
                except (TimeoutError,modal.exception.TimeoutError):continue
                ledger[name].update(complete=True,result=result);ledgerpath.write_text(json.dumps(ledger,indent=2))
            if name in ledger and ledger[name]['complete']:
                out=masters/(name+'.mp4')
                if not out.exists():
                    tmp=masters/(name+'.mp4.partial')
                    checksum=hashlib.sha256()
                    with tmp.open('wb') as stream:
                        for block in v.read_file('/masters/'+name+'.mp4'):
                            stream.write(block);checksum.update(block)
                    if checksum.hexdigest()!=ledger[name]['result']['sha256']:
                        raise RuntimeError('Downloaded master checksum mismatch: '+name)
                    tmp.replace(out);print('MASTER DOWNLOADED',name,out.stat().st_size,flush=True)
                state['downloaded'].append(name)
        (cache/'production-state.json').write_text(json.dumps(state,indent=2))
        if len(state['downloaded'])==len(expected):print('ALL MASTERS READY',flush=True);return
        time.sleep(60)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',default='v1');p.add_argument('--cache',type=Path,required=True);p.add_argument('--masters',type=Path,required=True);p.add_argument('--chapters',nargs='+');a=p.parse_args();observe(a.run,a.cache,a.masters,a.chapters)
