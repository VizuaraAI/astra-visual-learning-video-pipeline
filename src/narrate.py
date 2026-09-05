"""Cache ElevenLabs narration, create exact-length 48 kHz chapter tracks and SRTs."""
from pathlib import Path
import os,json,argparse,base64,time,subprocess,math,wave
import requests
ROOT=Path(__file__).resolve().parents[1]
VOICE='9FTUWXd0yHJL1ZiZ71RK'

def speech_text(t):
    import re
    names={'mRNA':'एम आर एन ए','tRNA':'टी आर एन ए','DNA':'डी एन ए','RNA':'आर एन ए','SA':'एस ए','AV':'ए वी',
           'ATG':'ए टी जी','GCT':'जी सी टी','TTT':'टी टी टी','GAA':'जी ए ए','TGA':'टी जी ए',
           'AUG':'ए यू जी','GCU':'जी सी यू','UUU':'यू यू यू','UGA':'यू जी ए','UAA':'यू ए ए','UAG':'यू ए जी'}
    return re.sub(r'\b('+ '|'.join(names)+r')\b',lambda m:names[m.group(0)],t)

def duration(path):
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(path)]))

def stamp(t):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'

def run(chapter,cache,allow=False):
    if not allow:raise RuntimeError('Use --generate only after all local shot test frames have been shown')
    key=os.environ['ELEVENLABS_API_KEY'];mp=ROOT/'storyboards'/f'{chapter}.json';m=json.loads(mp.read_text());cache.mkdir(parents=True,exist_ok=True)
    ledger=[];durations=[]
    for shot in m['shots']:
        out=cache/(shot['id']+'.mp3');meta=cache/(shot['id']+'.alignment.json')
        if not out.exists():
            payload=dict(text=speech_text(shot['narration']),model_id='eleven_multilingual_v2',language_code='hi',voice_settings=dict(stability=.62,similarity_boost=.86,style=.12,use_speaker_boost=True,speed=1.0),seed=seed_for(shot['id']))
            for attempt in range(5):
                r=requests.post(f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128',headers={'xi-api-key':key,'Content-Type':'application/json'},json=payload,timeout=180)
                if r.status_code!=429:break
                time.sleep(min(10,2**attempt))
            if not r.ok:raise RuntimeError(f'ElevenLabs HTTP {r.status_code}: {r.text[:600]}')
            data=r.json();out.write_bytes(base64.b64decode(data.pop('audio_base64')));data['requested_characters']=len(payload['text']);data['request_id']=r.headers.get('request-id');data['billed_characters']=r.headers.get('character-cost');meta.write_text(json.dumps(data,ensure_ascii=False))
            print('NARRATION '+shot['id'],flush=True)
        d=duration(out);durations.append(d);ledger.append(dict(shot=shot['id'],requested_characters=json.loads(meta.read_text())['requested_characters'],seconds=d))
    # Reserve short attentive holds. Target 8 min when it accommodates natural speech.
    # Pitch-preserving tempo correction after the edited script is generated.
    # The teacher voice is deliberately slow; cap correction at 26% and audit a sample.
    spoken=sum(durations);target=480.;speed=max(1.,min(1.26,spoken/(target-24*1.15)))
    adjusted=[d/speed for d in durations];target=max(480.,sum(adjusted)+24*1.15)
    gap=(target-sum(adjusted))/24
    cursor=0;srt=[];partfiles=[]
    for shot,d in zip(m['shots'],adjusted):
        shot['start']=cursor/24;shot['frames']=math.ceil((d+gap)*24);shot['duration']=shot['frames']/24;shot['narration_seconds']=d;shot['narration_offset']=.35
        part=cache/(shot['id']+'.wav');partfiles.append(part)
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(cache/(shot['id']+'.mp3')),'-af',f'atempo={speed:.7f},adelay=350:all=1,apad','-t',str(shot['duration']),'-ar','48000','-ac','2','-c:a','pcm_s16le',str(part)],check=True)
        align_data=json.loads((cache/(shot['id']+'.alignment.json')).read_text())
        align=align_data.get('normalized_alignment') or align_data['alignment'];chars=align['characters'];starts=align['character_start_times_seconds'];ends=align['character_end_times_seconds']
        begin=0;buf=''
        for i,c in enumerate(chars):
            buf+=c
            if c in ['।','!','?'] or (len(buf)>85 and c==' ') or i==len(chars)-1:
                if buf.strip():
                    st=shot['start']+.35+starts[begin]/speed;en=shot['start']+.35+ends[i]/speed
                    srt.append(f'{len(srt)+1}\n{stamp(st)} --> {stamp(en)}\n{buf.strip()}\n')
                buf='';begin=i+1
        cursor+=shot['frames']
    m['actual_duration']=cursor/24;m['narration_speed_factor']=speed;m['pause_per_shot']=gap
    mp.write_text(json.dumps(m,indent=2,ensure_ascii=False))
    listing=cache/(chapter+'-concat.txt');listing.write_text('\n'.join("file '"+str(p.resolve())+"'" for p in partfiles))
    master=cache/(chapter+'.wav')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-af','loudnorm=I=-16:TP=-1.5:LRA=7','-ar','48000','-ac','2','-c:a','pcm_s16le',str(master)],check=True)
    (ROOT/'scripts'/f'{chapter}.hi.srt').write_text('\n'.join(srt));(cache/(chapter+'-usage.json')).write_text(json.dumps(dict(chapter=chapter,characters=sum(x['requested_characters'] for x in ledger),spoken_seconds=spoken,speed_factor=speed,actual_duration=cursor/24,shots=ledger),indent=2))
    print(json.dumps(dict(chapter=chapter,duration=cursor/24,speed_factor=speed,characters=sum(x['requested_characters'] for x in ledger))))
def seed_for(t):return sum((i+1)*ord(c) for i,c in enumerate(t))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('chapter',choices=['heart','dna']);p.add_argument('--cache',required=True);p.add_argument('--generate',action='store_true');a=p.parse_args();run(a.chapter,Path(a.cache).resolve(),a.generate)
