"""Compare the owned reference and recreated master at identical 24 fps timestamps."""
from pathlib import Path
import argparse,json,subprocess,tempfile
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
TIMES=[23,39,70,105,135,182,245,272,315,360,448,492,559,615,681,720,761,785,826,869]
FONT=ROOT/'assets/Barlow-Regular.ttf'

def frame(path,t,out):
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(round(t*24)/24),'-i',str(path),'-frames:v','1','-vf','scale=800:450',str(out)],check=True)

def run(reference,master,out,video=False):
    out.mkdir(parents=True,exist_ok=True)
    font=ImageFont.truetype(str(FONT),28);small=ImageFont.truetype(str(FONT),23)
    with tempfile.TemporaryDirectory(prefix='vl-compare-') as td:
        td=Path(td);pairs=[]
        for i,t in enumerate(TIMES):
            pair=Image.new('RGB',(1600,495),'#071117');d=ImageDraw.Draw(pair)
            for j,p in enumerate([reference,master]):
                f=td/f'{i}-{j}.png';frame(p,t,f);pair.paste(Image.open(f),(800*j,45))
            stamp=f'{int(t)//60:02d}:{int(t)%60:02d}'
            d.text((16,7),f'{stamp}  |  OWNED REFERENCE',font=small,fill='#c2cbd0')
            d.text((816,7),f'{stamp}  |  PROCEDURAL RECREATION',font=small,fill='#78d5d4')
            pair.save(out/f'match-{i+1:02d}-{int(t):03d}s.jpg',quality=94);pairs.append(pair)
        for pg in range(4):
            sheet=Image.new('RGB',(1600,5*495+70),'#071117');d=ImageDraw.Draw(sheet)
            d.text((20,18),f'THE FUNDAMENTAL UNIT OF LIFE  /  TIMESTAMP COMPARISON {pg+1} OF 4',font=font,fill='white')
            for k,pair in enumerate(pairs[pg*5:pg*5+5]):sheet.paste(pair,(0,70+k*495))
            sheet.save(out/f'comparison-page-{pg+1:02d}.jpg',quality=94)
        overview=Image.new('RGB',(1600,10*248+60),'#071117');d=ImageDraw.Draw(overview)
        d.text((20,15),'REFERENCE / RECREATION — MATCHING TIMESTAMPS',font=font,fill='white')
        for i,pair in enumerate(pairs):overview.paste(pair.resize((800,248)),((i%2)*800,60+(i//2)*248))
        overview.save(out/'comparison-contact-sheet.jpg',quality=94)
        (out/'timestamps.json').write_text(json.dumps(dict(fps=24,timestamps=TIMES,reference=str(reference),master=str(master)),indent=2))
        if video:
            ov=Image.new('RGBA',(1920,1080),(0,0,0,0));d=ImageDraw.Draw(ov)
            title=ImageFont.truetype(str(FONT),44);body=ImageFont.truetype(str(FONT),31)
            d.text((58,73),'THE FUNDAMENTAL UNIT OF LIFE',font=title,fill='white')
            d.text((58,148),'Same source audio • Identical 24 fps timeline • Original 3D rebuilt',font=body,fill='#a8bac3')
            d.text((58,215),'OWNED REFERENCE',font=body,fill='#c2cbd0')
            d.text((1018,215),'PROCEDURAL RECREATION',font=body,fill='#78d5d4')
            d.text((58,875),'Visual interpretation: camera paths, models and interface differ from the reference.',font=body,fill='#a8bac3')
            d.text((58,928),'Scientific corrections appear in the recreated labels; reference narration is retained.',font=body,fill='#a8bac3')
            overlay=td/'overlay.png';ov.save(overlay)
            filt='[0:v]fps=24,scale=960:540,setsar=1[a];[1:v]fps=24,scale=960:540,setsar=1[b];[a][b]hstack=inputs=2,pad=1920:1080:0:270:color=0x071117[base];[base][2:v]overlay=0:0:format=auto,format=yuv420p[v]'
            cmd=['ffmpeg','-hide_banner','-loglevel','warning','-y','-i',str(reference),'-i',str(master),'-i',str(overlay),'-filter_complex',filt,'-map','[v]','-map','1:a:0','-c:v','h264_videotoolbox','-b:v','7M','-r','24','-c:a','copy','-t','891.083333','-movflags','+faststart',str(out/'cell-side-by-side.mp4')]
            subprocess.run(cmd,check=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--reference',type=Path,required=True);p.add_argument('--master',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--video',action='store_true');a=p.parse_args();run(a.reference,a.master,a.output,a.video)
