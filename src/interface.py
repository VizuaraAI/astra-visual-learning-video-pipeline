"""Reproducible 1080p English interface layer and storyboard contact sheets."""
from pathlib import Path
import json,math,argparse
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
def font(size,bold=False):return ImageFont.truetype(str(ROOT/'assets'/('Barlow-SemiBold.ttf' if bold else 'Barlow-Regular.ttf')),size)
TEAL=(102,214,219,255);WHITE=(241,245,246,255);GOLD=(226,177,100,255)

def fit(draw,text,maxwidth,size=40,bold=True):
    while draw.textlength(text,font=font(size,bold))>maxwidth and size>23:size-=1
    return font(size,bold)

def panel(draw,xy,text,accent=TEAL):
    text=text.replace('→','>').replace('′',"'")
    x,y,w,h=xy
    draw.polygon([(x+10,y),(x+w,y),(x+w-10,y+h),(x,y+h)],fill=(10,28,39,225),outline=accent,width=2)
    f=fit(draw,text,w-36,30)
    draw.text((x+18,y+(h-f.size)/2-3),text,font=f,fill=WHITE)

def overlay(shot):
    shot={k:(v.replace('→',' > ').replace('′',"'").replace('₂','2').replace('₃','3') if isinstance(v,str) else v) for k,v in shot.items()}
    im=Image.new('RGBA',(1920,1080));d=ImageDraw.Draw(im)
    if shot['asset']=='outro':
        d.rectangle((0,0,1920,1080),fill=(6,14,20,255))
        d.rounded_rectangle((612,446,792,626),radius=55,fill=(118,46,195,255))
        d.line([(700,424),(812,536),(700,648),(588,536),(700,424)],fill=GOLD,width=6)
        d.text((651,487),'VL',font=font(64,True),fill=WHITE)
        d.text((844,457),'Visual',font=font(69,True),fill=WHITE)
        d.text((844,535),'Learning',font=font(69,True),fill=WHITE)
        return im
    accent={'cell':TEAL,'heart':(255,135,139,255),'dna':(139,205,236,255)}[shot['chapter']]
    # A quiet top and bottom scrim preserves the charcoal reference stage.
    for y in range(115):d.line((0,y,1920,y),fill=(4,12,18,round(135*(1-y/115))))
    for y in range(870,1080):d.line((0,y,1920,y),fill=(4,12,18,round(190*(y-870)/210)))
    chapter={'cell':'THE FUNDAMENTAL UNIT OF LIFE','heart':'HUMAN HEART AND CIRCULATION','dna':'DNA: FROM GENE TO PROTEIN'}[shot['chapter']]
    d.text((58,35),chapter,font=font(24,True),fill=(166,192,201,255))
    d.line((58,77,145,77),fill=accent,width=3)
    # Hand-built vector house mark, no raster model or unlicensed asset.
    x,y=1808,65;d.line([(x,y-32),(x+32,y),(x,y+32),(x-32,y),(x,y-32)],fill=GOLD,width=2)
    d.text((x-12,y-14),'VL',font=font(21,True),fill=GOLD)
    d.text((1697,112),'VISUAL LEARNING',font=font(15,True),fill=(175,173,161,255))
    d.text((58,112),shot['title'],font=fit(d,shot['title'],1470,49),fill=WHITE)
    # English definition plate follows the outlined navy grammar of the source.
    sub=shot['subtitle'];f=fit(d,sub,1740,32,False)
    d.rounded_rectangle((56,947,1864,1026),radius=7,fill=(9,28,40,227),outline=(*accent[:3],170),width=2)
    d.rectangle((56,947,61,1026),fill=accent)
    d.text((86,968),sub,font=f,fill=WHITE)
    d.text((58,1045),f"{shot['index']+1:02d}  /  {'83' if shot['chapter']=='cell' else '24'}",font=font(16,True),fill=(127,151,163,255))
    label='CLASS 9' if shot['chapter']=='cell' else 'CLASS 10' if shot['chapter']=='heart' else 'CLASS 10–12'
    d.text((1707,1045),label,font=font(16,True),fill=(127,151,163,255))
    asset=shot['asset']
    if asset=='heart_cut':
        for x,y,w,txt in [(235,377,245,'Right atrium'),(1315,377,245,'Left atrium'),(224,718,268,'Right ventricle'),(1312,718,268,'Left ventricle')]:panel(d,(x,y,w,53),txt,accent)
    if asset in ['circulation','heart_flow','alveoli']:
        d.ellipse((60,192,78,210),fill=(51,103,210,255));d.text((91,187),'Oxygen-poor',font=font(23),fill=WHITE)
        d.ellipse((60,226,78,244),fill=(226,72,81,255));d.text((91,221),'Oxygen-rich',font=font(23),fill=WHITE)
    if asset=='bilayer':
        panel(d,(123,376,340,62),'Hydrophilic heads');panel(d,(1290,620,410,62),'Hydrophobic tails');panel(d,(1300,294,360,62),'Membrane protein')
    if asset in ['cell','cell_full'] and shot['index'] not in [0,82]:
        panel(d,(205,425,245,56),'Nucleus');panel(d,(1322,650,300,56),'Cytoplasm');panel(d,(1250,309,350,56),'Plasma membrane')
    if asset=='mitochondria':
        panel(d,(123,297,340,56),'Outer membrane');panel(d,(1315,625,300,56),'Cristae');panel(d,(1280,329,330,56),'ATP synthase')
    if asset=='chloroplast':
        panel(d,(173,355,250,56),'Envelope');panel(d,(1325,359,260,56),'Grana');panel(d,(1330,709,260,56),'Stroma')
    if asset=='er':
        panel(d,(64,221,350,56),'Smooth ER',(246,153,94,255));panel(d,(64,293,350,56),'Rough ER',(223,117,163,255))
        d.ellipse((378,238,397,257),fill=(246,153,94,255));d.ellipse((378,310,397,329),fill=(223,117,163,255))
    if asset=='nucleus':panel(d,(233,381,270,56),'Nuclear pores');panel(d,(1280,690,270,56),'Chromatin')
    if asset in ['dna','mutation']:
        for i,(t,c) in enumerate([('A',TEAL),('T',(245,121,100,255)),('G',GOLD),('C',(170,124,233,255))]):
            d.rounded_rectangle((61,249+i*63,103,291+i*63),radius=7,fill=c);d.text((72,251+i*63),t,font=font(28,True),fill=(6,20,27,255))
        panel(d,(1270,340,250,56),'5′ → 3′');panel(d,(310,732,250,56),'3′ → 5′')
    if asset=='transcription':panel(d,(1200,520,430,56),'RNA polymerase');panel(d,(240,716,240,56),'New RNA')
    if asset=='ribosome':panel(d,(161,622,230,56),'mRNA');panel(d,(1370,320,340,56),'Polypeptide');panel(d,(234,341,270,56),'Ribosome')
    if asset=='central':
        for x,t in [(354,'DNA'),(908,'RNA'),(1410,'PROTEIN')]:d.text((x,785),t,font=font(35,True),fill=WHITE)
    if asset=='sequence':
        lines=[('CODING DNA',"5'  ATG   GCT   TTT   GAA   TGA  3'"),('mRNA',"5'  AUG   GCU   UUU   GAA   UGA  3'"),('AMINO ACIDS','Met     Ala      Phe      Glu      Stop')]
        for i,(label,seq) in enumerate(lines):
            y=310+i*180;d.rounded_rectangle((210,y,1710,y+136),radius=14,fill=(7,23,33,233),outline=(*accent[:3],150),width=2)
            d.text((241,y+18),label,font=font(22,True),fill=accent);d.text((523,y+50),seq,font=font(39,True),fill=WHITE)
    if shot['index']==0 and shot['chapter']=='cell':
        d.rounded_rectangle((310,236,1610,801),radius=14,fill=(6,31,49,231),outline=TEAL,width=2)
        d.rounded_rectangle((434,243,1486,313),radius=6,fill=(106,18,133,255));d.text((496,255),'The Fundamental Unit of Life',font=font(45,True),fill=WHITE)
        d.text((765,337),'Complete Chapter',font=font(33,True),fill=WHITE)
        for i,(t,tm) in enumerate([('1. Cell','00:19 – 02:35'),('2. Cell Structure','02:36 – 05:02'),('3. Cell Organelles','05:03 – 11:46'),('4. Nucleus and Cytoplasm','11:47 – 14:40')]):
            d.text((380,436+i*77),t,font=font(34,True),fill=WHITE);d.text((1210,436+i*77),tm,font=font(29),fill=WHITE)
    return im

def main():
    p=argparse.ArgumentParser();p.add_argument('--chapter');p.add_argument('--preview-dir');p.add_argument('--output',required=True);a=p.parse_args()
    out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    for name in [a.chapter] if a.chapter else ['cell','heart','dna']:
        m=json.loads((ROOT/'storyboards'/f'{name}.json').read_text());thumbs=[]
        for s in m['shots']:
            ov=overlay(s);ov.save(out/(s['id']+'-overlay.png'))
            if a.preview_dir:
                path=Path(a.preview_dir)/(s['id']+'.png')
                if not path.exists():continue
                img=Image.open(path).convert('RGBA');img=Image.alpha_composite(img,ov.resize(img.size,Image.Resampling.LANCZOS))
                img.convert('RGB').save(out/(s['id']+'.jpg'),quality=93)
                thumb=img.convert('RGB').resize((384,216));thumbs.append((s,thumb))
        if thumbs:
            rows=math.ceil(len(thumbs)/4);sheet=Image.new('RGB',(1600,rows*250+100),(7,17,24));d=ImageDraw.Draw(sheet)
            d.text((22,21),m['title']+' | LOCAL TEST FRAMES',font=font(30,True),fill='white')
            for i,(s,im) in enumerate(thumbs):
                x=16+(i%4)*396;y=85+(i//4)*250;sheet.paste(im,(x,y))
                title=s['title'].replace('→','>')
                d.text((x,y+218),f"{s['index']+1:02d} · {s['start']//60:02.0f}:{s['start']%60:05.2f} · {title[:34]}",font=font(15),fill=(171,194,201))
            sheet.save(out/f'{name}-test-contact-sheet.jpg',quality=90)
            for first in range(0,len(thumbs),24):
                batch=thumbs[first:first+24];pg=Image.new('RGB',(1600,math.ceil(len(batch)/4)*250+100),(7,17,24));pd=ImageDraw.Draw(pg)
                pd.text((22,21),m['title']+f' | SHOTS {first+1:02d}–{first+len(batch):02d}',font=font(28,True),fill='white')
                for j,(s,im) in enumerate(batch):
                    x=16+j%4*396;y=85+j//4*250;pg.paste(im,(x,y));title=s['title'].replace('→','>')
                    pd.text((x,y+218),f"{s['index']+1:02d} · {s['start']//60:02.0f}:{s['start']%60:05.2f} · {title[:34]}",font=font(15),fill=(171,194,201))
                pg.save(out/f'{name}-test-page-{first//24+1:02d}.jpg',quality=92)
    print('Interface assets complete')
if __name__=='__main__':main()
