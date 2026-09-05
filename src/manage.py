"""Client-side production control. Credentials come only from Modal environment/config."""
import json,argparse,time,math,hashlib,os
from pathlib import Path
import modal
ROOT=Path(__file__).resolve().parents[1]
APP=os.environ.get('VL_APP','vl-execu-20260905-prod');VOL=os.environ.get('VL_VOLUME','vl-execu-20260905-data');RATE=.00058596

def upload(audio=None):
    v=modal.Volume.from_name(VOL,create_if_missing=True)
    with v.batch_upload(force=True) as b:
        b.put_directory(str(ROOT/'storyboards'),'/manifests')
        if audio:
            for name in ['cell','heart','dna']:
                p=Path(audio)/(name+'.wav')
                if p.exists():b.put_file(str(p),'/audio/'+p.name)
    print('Uploaded manifests'+(' and audio' if audio else ''))

def dispatch(run,chapter=None,chunk=240,benchmark=False,cache=Path('cache'),worker='gpu',samples=48):
    cache.mkdir(parents=True,exist_ok=True);path=cache/(run+'-calls.json')
    calls=json.loads(path.read_text()) if path.exists() else [];existing={(c['chapter'],c['shot'],c['start'],c['end']) for c in calls}
    f=modal.Function.from_name(APP,'render_chunk_cpu' if worker=='cpu' else 'render_chunk')
    chapters=[chapter] if chapter else ['cell','heart','dna']
    for name in chapters:
        m=json.loads((ROOT/'storyboards'/f'{name}.json').read_text());total=sum(s['frames'] for s in m['shots'])
        shots=[m['shots'][{'cell':44,'heart':2,'dna':9}[name]]] if benchmark else m['shots']
        nchunks=sum(math.ceil(s['frames']/chunk) for s in shots)
        # Allow scene construction even for a short tail; allocate remaining time by frame count.
        pass_seconds=135/RATE
        startup_seconds=120
        render_seconds=max(0,pass_seconds-startup_seconds*nchunks)
        for shot in shots:
            spans=[(0,min(48,shot['frames']))] if benchmark else [(st,min(st+chunk,shot['frames'])) for st in range(0,shot['frames'],chunk)]
            for st,en in spans:
                key=(name,shot['index'],st,en)
                if key in existing:continue
                # Reservations sum to at most USD 135/video, below the user's USD 150 cap.
                maxseconds=900 if benchmark else min(5700 if samples>=128 else 2700,math.floor(startup_seconds+render_seconds*(en-st)/total))
                fc=f.spawn(name,shot['index'],st,en,run,samples,maxseconds)
                calls.append(dict(chapter=name,shot=shot['index'],start=st,end=en,call_id=fc.object_id,max_seconds=maxseconds,reserved_usd=maxseconds*RATE,worker=worker,samples=samples))
                path.write_text(json.dumps(calls,indent=2));existing.add(key)
                print('QUEUED '+name+' '+str(shot['index'])+' '+str(st)+' '+str(en),flush=True)
    print(json.dumps(dict(run=run,calls=len(calls),worst_case_reserved_usd=sum(c['reserved_usd'] for c in calls))))

def status(run,cache,download=False):
    cache.mkdir(parents=True,exist_ok=True);v=modal.Volume.from_name(VOL);report={};allmetrics=[]
    try:entries=list(v.iterdir('/'+run,recursive=True))
    except Exception as e:print(str(e));return
    for ent in entries:
        p=ent.path
        if not p.endswith('.json'):continue
        local=cache/Path(p).name
        if not local.exists():local.write_bytes(b''.join(v.read_file(p)))
        m=json.loads(local.read_text());name=m.get('chapter',Path(p).parts[-2]);r=report.setdefault(name,dict(chunks=0,frames=0,failed=0,estimated_usd=0,elapsed_seconds=0))
        r['estimated_usd']+=m.get('estimated_usd',0);r['elapsed_seconds']+=m.get('elapsed_seconds',0)
        if m.get('status')=='complete':r['chunks']+=1;r['frames']+=m['frames']
        else:r['failed']+=1
        allmetrics.append(m)
        if download and m.get('status')=='complete':
            for suffix in ['.jpg','.mp4']:
                remote=str(Path(p).with_suffix(suffix));dest=cache/(m['stem']+suffix)
                if not dest.exists():dest.write_bytes(b''.join(v.read_file(remote)))
    (cache/'status.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['upload','dispatch','status','assemble','download-master']);p.add_argument('--run',default='v1');p.add_argument('--chapter');p.add_argument('--chunk',type=int,default=240);p.add_argument('--benchmark',action='store_true');p.add_argument('--cache',default='cache');p.add_argument('--audio');p.add_argument('--download',action='store_true');p.add_argument('--worker',choices=['gpu','cpu'],default='gpu');p.add_argument('--samples',type=int,default=48);a=p.parse_args();cache=Path(a.cache)
    if a.action=='upload':upload(a.audio)
    elif a.action=='dispatch':dispatch(a.run,a.chapter,a.chunk,a.benchmark,cache,a.worker,a.samples)
    elif a.action=='status':status(a.run,cache,a.download)
    elif a.action=='assemble':
        f=modal.Function.from_name(APP,'assemble');calls=[]
        for name in [a.chapter] if a.chapter else ['cell','heart','dna']:calls.append(dict(chapter=name,call_id=f.spawn(name,a.run).object_id))
        cache.mkdir(parents=True,exist_ok=True);(cache/'assembly-calls.json').write_text(json.dumps(calls,indent=2));print(calls)
    elif a.action=='download-master':
        cache.mkdir(parents=True,exist_ok=True);v=modal.Volume.from_name(VOL)
        for name in [a.chapter] if a.chapter else ['cell','heart','dna']:
            out=cache/(name+'.mp4')
            with out.open('wb') as f:
                for b in v.read_file('/masters/'+name+'.mp4'):f.write(b)
            print(name,out.stat().st_size)
