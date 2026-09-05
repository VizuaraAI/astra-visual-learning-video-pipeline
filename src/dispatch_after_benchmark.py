"""Keep a production chapter waiting for its accepted render-backend benchmark."""
import json,time,argparse,hashlib,subprocess
from pathlib import Path
from PIL import Image,ImageStat
import modal
from manage import dispatch,VOL,ROOT

def run(chapter,benchmark,cache,jobs,production='v1',worker='gpu'):
    cache.mkdir(parents=True,exist_ok=True);v=modal.Volume.from_name(VOL)
    index={'cell':44,'heart':2,'dna':9}[chapter];stem=f'{chapter}_{index:03d}_000000_000048'
    remote=f'/{benchmark}/{chapter}/{stem}'
    while True:
        try:raw=b''.join(v.read_file(remote+'.json'))
        except (modal.exception.NotFoundError,FileNotFoundError):
            try:failure=b''.join(v.read_file(remote+'.failed.json'))
            except (modal.exception.NotFoundError,FileNotFoundError):time.sleep(60);continue
            (cache/(stem+'.failed.json')).write_bytes(failure)
            raise RuntimeError('GPU benchmark failed; inspect its saved failure record')
        m=json.loads(raw);(cache/(stem+'.json')).write_bytes(raw)
        if m['status']!='complete':raise RuntimeError('Benchmark did not complete')
        for suffix in ['.jpg','.mp4']:
            p=cache/(stem+suffix)
            if not p.exists():p.write_bytes(b''.join(v.read_file(remote+suffix)))
        if hashlib.sha256((cache/(stem+'.mp4')).read_bytes()).hexdigest()!=m['sha256']:raise RuntimeError('Benchmark checksum mismatch')
        pic=Image.open(cache/(stem+'.jpg'));assert pic.size==(1920,1080)
        assert max(ImageStat.Stat(pic.convert('RGB')).stddev)>10,'Blank benchmark image'
        info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(cache/(stem+'.mp4'))]))
        vid=next(s for s in info['streams'] if s['codec_type']=='video')
        assert vid['r_frame_rate']=='24/1' and int(vid['nb_frames'])==48
        total=sum(s['frames'] for s in json.loads((ROOT/'storyboards'/f'{chapter}.json').read_text())['shots'])
        projection=m['estimated_usd']/m['frames']*total
        gate=dict(chapter=chapter,benchmark=benchmark,frame_checks=True,estimated_full_usd=projection,accepted=projection<=135)
        (cache/'benchmark-gate.json').write_text(json.dumps(gate,indent=2))
        if not gate['accepted']:raise RuntimeError(f'Projection ${projection:.2f} exceeds this pass budget')
        print('BENCHMARK ACCEPTED',gate,flush=True)
        dispatch(production,chapter,240,False,jobs,worker)
        return

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--chapter',required=True);p.add_argument('--benchmark',required=True);p.add_argument('--cache',type=Path,required=True);p.add_argument('--jobs',type=Path,required=True);p.add_argument('--production',default='v1');p.add_argument('--worker',default='gpu',choices=['cpu','gpu']);a=p.parse_args();run(a.chapter,a.benchmark,a.cache,a.jobs,a.production,a.worker)
