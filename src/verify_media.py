"""Verify delivered media and build timestamped contact sheets from encoded masters."""
from pathlib import Path
import argparse,json,subprocess,tempfile,math,hashlib
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
def file_hash(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
def frame(p,t,out):
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=640:360',str(out)],check=True)
def run(masters,out):
    out.mkdir(parents=True,exist_ok=True);reports={};font=ImageFont.truetype(str(ROOT/'assets/Barlow-Regular.ttf'),19)
    bold=ImageFont.truetype(str(ROOT/'assets/Barlow-SemiBold.ttf'),32)
    for chapter in ['cell','heart','dna']:
        m=json.loads((ROOT/'storyboards'/f'{chapter}.json').read_text());p=masters/(chapter+'.mp4');info=probe(p)
        v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio');expected=sum(s['frames'] for s in m['shots'])
        checks=dict(h264=v['codec_name']=='h264',aac=a['codec_name']=='aac',resolution=(v['width'],v['height'])==(1920,1080),fps=v['r_frame_rate']=='24/1',frame_count=int(v.get('nb_frames',-1))==expected,duration=abs(float(info['format']['duration'])-expected/24)<.12,audio_sample_rate=int(a['sample_rate'])==48000)
        if not all(checks.values()):raise RuntimeError({chapter:checks})
        reports[chapter]=dict(checks=checks,expected_frames=expected,duration=expected/24,bytes=p.stat().st_size,sha256=file_hash(p),streams=info['streams'])
        indices=list(range(len(m['shots']))) if chapter!='cell' else [round(i*(len(m['shots'])-1)/23) for i in range(24)]
        sheet=Image.new('RGB',(1944,6*398+95),(7,17,24));d=ImageDraw.Draw(sheet);d.text((26,23),m['title']+' | MASTER CONTACT SHEET',font=bold,fill='white')
        with tempfile.TemporaryDirectory() as tmp:
            for k,i in enumerate(indices):
                s=m['shots'][i];t=s['start']+s['duration']*.5;img=Path(tmp)/f'{k}.png';frame(p,t,img)
                x=8+(k%3)*646;y=90+(k//3)*398
                # Contact layout grows to eight rows for 24 representative shots.
                if y+390>sheet.height:
                    bigger=Image.new('RGB',(1944,y+398),(7,17,24));bigger.paste(sheet,(0,0));sheet=bigger;d=ImageDraw.Draw(sheet)
                sheet.paste(Image.open(img),(x,y));title=s['title'].replace('→','>');d.text((x+7,y+365),f'{int(t//60):02d}:{t%60:05.2f}  {title[:48]}',font=font,fill=(190,210,218))
        sheet.save(out/(chapter+'-contact-sheet.jpg'),quality=94)
    (out/'media-verification.json').write_text(json.dumps(reports,indent=2));print({k:all(v['checks'].values()) for k,v in reports.items()})
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--masters',required=True);p.add_argument('--output',required=True);a=p.parse_args();run(Path(a.masters),Path(a.output))
