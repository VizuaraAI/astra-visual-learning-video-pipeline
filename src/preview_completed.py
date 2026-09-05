"""Make review pages from actual representative frames of completed cloud chunks."""
from pathlib import Path
import json,argparse,math
from PIL import Image,ImageDraw,ImageFont
import modal
from manage import VOL,ROOT

def run(run_id,metrics,output):
    output.mkdir(parents=True,exist_ok=True);v=modal.Volume.from_name(VOL);groups={}
    for p in sorted(metrics.glob('*.json')):
        m=json.loads(p.read_text())
        if m.get('status')!='complete' or 'stem' not in m:continue
        local=output/(m['stem']+'.jpg')
        if not local.exists():local.write_bytes(b''.join(v.read_file(f'/{run_id}/{m["chapter"]}/{local.name}')))
        groups.setdefault(m['chapter'],[]).append(m)
    f=ImageFont.truetype(str(ROOT/'assets/Barlow-Regular.ttf'),20)
    heading=ImageFont.truetype(str(ROOT/'assets/Barlow-SemiBold.ttf'),30)
    for chapter,shots in groups.items():
        for pg in range(math.ceil(len(shots)/24)):
            rows=shots[pg*24:pg*24+24];sheet=Image.new('RGB',(1940,80+math.ceil(len(rows)/4)*307),'#071117');d=ImageDraw.Draw(sheet)
            d.text((18,23),f'{chapter.upper()} / ACTUAL CLOUD FRAMES / PAGE {pg+1}',font=heading,fill='white')
            for i,s in enumerate(rows):
                x=5+(i%4)*485;y=80+(i//4)*307
                pic=Image.open(output/(s['stem']+'.jpg')).resize((480,270));sheet.paste(pic,(x,y))
                d.text((x+5,y+275),f'Shot {s["shot"]+1}  |  frames {s["start"]}–{s["end"]}',font=f,fill='#c2d1d8')
            sheet.save(output/f'{chapter}-review-{pg+1:02d}.jpg',quality=94)
    print({k:len(v) for k,v in groups.items()})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',default='v1');p.add_argument('--metrics',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();run(a.run,a.metrics,a.output)
