"""Durable Modal GPU render service. Deploy; invoke with Function.from_name().spawn()."""
import modal
from pathlib import Path

APP_NAME='vl-execu-20260905-prod'
VOLUME_NAME='vl-execu-20260905-data'
ROOT=Path(__file__).resolve().parents[1]
app=modal.App(APP_NAME)
volume=modal.Volume.from_name(VOLUME_NAME,create_if_missing=True)
image=(modal.Image.debian_slim(python_version='3.11')
    .apt_install('ffmpeg','curl','xz-utils','libgl1','libegl1','libxi6','libxrender1','libxkbcommon0','libsm6','libxfixes3','libxxf86vm1','libxext6','libx11-6','libfontconfig1','libdbus-1-3','libasound2')
    .pip_install('Pillow==11.3.0')
    .run_commands('curl -fsSL https://download.blender.org/release/Blender5.2/blender-5.2.1-linux-x64.tar.xz -o /tmp/blender.tar.xz',
                  "python -c \"import hashlib; assert hashlib.sha256(open('/tmp/blender.tar.xz','rb').read()).hexdigest() == 'a31f524fa99a527d3d52b7f5aaa68c34e1a19d5a1c9473f79c5cc610fd5b10e9'\"",
                  'mkdir -p /opt/blender && tar -xJf /tmp/blender.tar.xz -C /opt/blender --strip-components=1 && rm /tmp/blender.tar.xz')
    .add_local_dir(str(ROOT/'src'),'/opt/vl/src')
    .add_local_dir(str(ROOT/'assets'),'/opt/vl/assets'))

# Modal resource prices verified 2026-09-05; estimates, not provider invoices.
RATE_PER_SECOND=.000542+2*.0000131+8*.00000222

@app.function(image=image,gpu=['L40S','A10','L4'],cpu=2,memory=8192,timeout=6000,max_containers=18,scaledown_window=2,volumes={'/data':volume})
def render_chunk(chapter:str,shot_index:int,start:int,end:int,run_id:str='v1',samples:int=48,max_seconds:int=1800,use_gpu:bool=True,cpu_threads:int=2,resource_rate:float|None=None):
    import os,json,time,subprocess,tempfile,shutil,hashlib,sys
    from pathlib import Path
    t0=time.time();volume.reload()
    gpu_name=subprocess.check_output(['nvidia-smi','--query-gpu=name','--format=csv,noheader'],text=True).strip() if use_gpu else f'CPU ({cpu_threads} cores)'
    gpu_rate=.000542 if 'L40S' in gpu_name else (.000306 if 'A10' in gpu_name else .000222)
    rate=resource_rate if resource_rate is not None else gpu_rate+2*.0000131+8*.00000222
    # A lower-priced fallback receives more wall time within the same dollar reservation.
    max_seconds=min(5700,int(max_seconds*RATE_PER_SECOND/rate))
    base=Path('/data')/run_id/chapter
    base.mkdir(parents=True,exist_ok=True)
    stem=f'{chapter}_{shot_index:03d}_{start:06d}_{end:06d}'
    mp4=base/(stem+'.mp4');metric=base/(stem+'.json')
    if mp4.exists() and metric.exists():return json.loads(metric.read_text())
    manifest=Path('/data/manifests')/(chapter+'.json');shot=json.loads(manifest.read_text())['shots'][shot_index]
    if end>shot['frames'] or end<=start:raise ValueError('Frame range outside manifest')
    tmp=Path(tempfile.mkdtemp(prefix='vl-'));frames=tmp/'frames';frames.mkdir()
    log=tmp/'blender.log'
    cmd=['/opt/blender/blender','-b','--factory-startup','-t',str(cpu_threads),'--python','/opt/vl/src/render_scene.py','--','--manifest',str(manifest),'--shot',str(shot_index),'--output',str(frames),'--width','1920','--samples',str(samples),'--threads',str(cpu_threads),'--start',str(start),'--end',str(end)]
    if use_gpu:cmd.append('--gpu')
    try:
        with log.open('w') as f:subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=max(60,max_seconds-70))
        rendered=sorted(frames.glob('*.png'))
        if len(rendered)!=end-start:raise RuntimeError(f'Expected {end-start} frames; got {len(rendered)}')
        render_seconds=time.time()-t0
        sys.path.insert(0,'/opt/vl/src');from interface import overlay
        ov=tmp/'overlay.png';overlay(shot).save(ov)
        filt='[0:v][1:v]overlay=0:0:format=auto,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p'
        if chapter!='cell':
            if start==0:filt+=',fade=t=in:st=0:d=0.208333'
            if end==shot['frames']:filt+=f',fade=t=out:st={max(0,(end-start-5)/24)}:d=0.208333'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate','24','-start_number',str(start),'-i',str(frames/'%06d.png'),'-i',str(ov),'-filter_complex',filt,'-frames:v',str(end-start),'-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','-r','24','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-movflags','+faststart','-threads','4',str(tmp/'chunk.mp4')],check=True,timeout=65)
        shutil.copyfile(tmp/'chunk.mp4',mp4)
        # Retain one actual frame per chunk for provenance and visual checks.
        from PIL import Image
        frame=Image.open(rendered[len(rendered)//2]).convert('RGBA');frame=Image.alpha_composite(frame,overlay(shot));frame.convert('RGB').save(base/(stem+'.jpg'),quality=93)
        elapsed=time.time()-t0
        result=dict(stem=stem,chapter=chapter,shot=shot_index,start=start,end=end,frames=end-start,render_seconds=render_seconds,elapsed_seconds=elapsed,estimated_usd=elapsed*rate,gpu=gpu_name,rate_per_second=rate,samples=samples,bytes=mp4.stat().st_size,sha256=hashlib.sha256(mp4.read_bytes()).hexdigest(),status='complete')
        (base/(stem+'.log')).write_text(log.read_text()[-12000:])
        metric.write_text(json.dumps(result,indent=2));volume.commit()
        return result
    except Exception as exc:
        elapsed=time.time()-t0
        err=dict(stem=stem,status='failed',elapsed_seconds=elapsed,estimated_usd=elapsed*rate,gpu=gpu_name,rate_per_second=rate,error=str(exc),log=log.read_text()[-9000:] if log.exists() else '')
        (base/(stem+'.failed.json')).write_text(json.dumps(err,indent=2));volume.commit();raise
    finally:shutil.rmtree(tmp,ignore_errors=True)

@app.function(image=image,cpu=32,memory=16384,timeout=6000,max_containers=8,scaledown_window=2,volumes={'/data':volume})
def render_chunk_cpu(chapter:str,shot_index:int,start:int,end:int,run_id:str='v1',samples:int=48,max_seconds:int=1800):
    return render_chunk.local(chapter,shot_index,start,end,run_id,samples,max_seconds,False,32,32*.0000131+16*.00000222)

@app.function(image=image,cpu=2,memory=4096,timeout=3600,max_containers=2,scaledown_window=2,volumes={'/data':volume})
def assemble(chapter:str,run_id:str='v1'):
    import subprocess,json,time,hashlib
    from pathlib import Path
    t0=time.time();volume.reload();base=Path('/data')/run_id/chapter
    manifest=json.loads((Path('/data/manifests')/(chapter+'.json')).read_text());entries=[]
    for shot in manifest['shots']:
        metrics=sorted(base.glob(shot['id']+'_*.json'))
        cursor=0
        for path in metrics:
            if path.name.endswith('failed.json'):continue
            m=json.loads(path.read_text())
            if m['status']!='complete':continue
            if m['start']!=cursor:raise RuntimeError(f'Missing or overlapping frames: {shot["id"]} expected {cursor}, got {m["start"]}')
            cursor=m['end'];entries.append(base/(m['stem']+'.mp4'))
        if cursor!=shot['frames']:raise RuntimeError(f'Incomplete shot: {shot["id"]}: {cursor}/{shot["frames"]}')
    listing=base/'concat.txt';listing.write_text('\n'.join("file '"+str(p)+"'" for p in entries))
    out=Path('/data/masters');out.mkdir(exist_ok=True);master=out/(chapter+'.mp4')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-i',f'/data/audio/{chapter}.wav','-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-t',str(sum(s['frames'] for s in manifest['shots'])/24),str(master)],check=True)
    result=dict(chapter=chapter,elapsed_seconds=time.time()-t0,bytes=master.stat().st_size,sha256=hashlib.sha256(master.read_bytes()).hexdigest())
    (out/(chapter+'.json')).write_text(json.dumps(result,indent=2));volume.commit();return result
