"""Right-handed pedagogical B-DNA, RNA, ribosome and protein models."""
from geometry import *
import random
R=random.Random(1953)

def dna(P,state,bubble=False,short=False):
    count=22 if short else 31;rise=.27;rad=1.02;phase=2.45
    back=[Mesh(),Mesh()];sugar=Mesh();phosphate=Mesh();bonds=Mesh();bases={k:Mesh() for k in 'ATGC'}
    seq=('ATGGCTTTTGAATGA'+'GCGTAATCCGATGCTA')[:count]
    comp={'A':'T','T':'A','G':'C','C':'G'}
    strands=[[],[]]
    for i in range(count):
        z=(i-(count-1)/2)*rise;a=i*2*pi/10.5
        opening=max(0,1-(z/1.35)**2) if bubble else 0
        ps=[]
        for strand in [0,1]:
            angle=a+phase*strand
            p=Vector((rad*cos(angle)+(1 if strand else -1)*opening*.85,rad*sin(angle),z))
            strands[strand].append(p);ps.append(p)
            sugar.sphere(p,(.13,)*3,14,10)
            q=p+Vector((.065*cos(angle+.25),.065*sin(angle+.25),.12 if strand==0 else -.12))
            phosphate.sphere(q,(.095,)*3,12,9)
        if opening<.2:
            mid=(ps[0]+ps[1])/2;d=(ps[1]-ps[0]).normalized()
            bases[seq[i]].tube([ps[0]+d*.13,mid-d*.06],.095,10)
            bases[comp[seq[i]]].tube([mid+d*.06,ps[1]-d*.13],.095,10)
            n=2 if seq[i] in 'AT' else 3
            for j in range(n):
                dz=(j-(n-1)/2)*.042
                bonds.tube([mid-d*.065+Vector((0,0,dz)),mid+d*.065+Vector((0,0,dz))],.011,5)
        else:
            for side in [0,1]:
                p=ps[side];direction=Vector((1 if side==0 else -1,0,0))
                bases[seq[i] if side==0 else comp[seq[i]]].tube([p,p+direction*.48],.085,9)
    for i in [0,1]:back[i].tube(curve_points(strands[i],count*6),.062,10);back[i].obj('DNA sugar-phosphate backbone %d'%i,P['phosph'])
    sugar.obj('Deoxyribose sugars',P['sugar']);phosphate.obj('Phosphate groups',P['phosph']);bonds.obj('Hydrogen bonds',P['white'])
    for k,m in bases.items():m.obj('DNA base '+k,P[k])
    state['dna']=True
    if bubble:
        cluster=Mesh()
        for i in range(90):
            a=R.random()*2*pi;b=R.random()*pi
            cluster.sphere((1.2+1.25*sin(b)*cos(a),.6+.83*sin(b)*sin(a),.25+.8*cos(b)),(.13,.12,.11),10,7)
        cluster.obj('RNA polymerase molecular surface',P['teal'])
        sphere('RNA polymerase core',(1.2,.6,.25),(1.2,.78,.77),P['teal'],64,40,lump=.09)
        rna(P,state,pts=[(.2,-.2,.3),(-.5,-.7,.15),(-1.6,-1,.25),(-2.6,-1.1,1.1),(-3,-1,1.8)],length=24)

def nucleotide(P):
    sphere('Phosphate group',(-1.65,0,0),(.42,)*3,P['phosph'],48,32)
    pent=[(-.35+.55*cos(i*2*pi/5),.55*sin(i*2*pi/5),.0) for i in range(6)]
    tube('Deoxyribose sugar ring',pent,.13,P['sugar'],16)
    path('Phosphate-sugar bond',[(-1.25,0,0),(-.9,0,0)],.065,P['white'])
    hexagon=[(1.1+.55*cos(i*2*pi/6),.55*sin(i*2*pi/6),.0) for i in range(7)]
    tube('Nitrogenous base ring',hexagon,.13,P['A'],16)
    path('Glycosidic bond',[(.15,0,0),(.55,0,0)],.065,P['white'])
    for p in pent[:-1]:sphere('Sugar atom',p,(.16,)*3,P['sugar'],20,12)
    for i,p in enumerate(hexagon[:-1]):sphere('Base atom',p,(.16,)*3,P['A'] if i%2 else P['cyan'],20,12)
    for a in [0,2*pi/3,4*pi/3]:sphere('Phosphate oxygen',(-1.65+.5*cos(a),.5*sin(a),.05),(.15,)*3,P['coral'],20,12)

def rna(P,state,pts=None,length=35):
    pts=pts or [(-3.6,0,.3),(-2.5,.1,.15),(-1.2,-.12,.25),(0,.1,.1),(1.4,-.15,.3),(2.6,.12,.25),(3.7,0,.15)]
    curve=curve_points(pts,length*4);tube('RNA sugar-phosphate backbone',curve,.052,P['rna'],10)
    m=Mesh();base={k:Mesh() for k in 'AUGC'};seq='AUGGCUUUUGAAUGA'
    for i in range(length):
        p=curve[min(len(curve)-1,round(i/(length-1)*(len(curve)-1)))];m.sphere(p,(.075,)*3,10,7)
        base[seq[i%len(seq)]].tube([p,p+Vector((0,-.35,0))],.07,9)
    m.obj('RNA ribose sugars',P['sugar'])
    for k,mesh in base.items():mesh.obj('RNA base '+k,P['T'] if k=='U' else P[k])

def trna(P,state,pos=(0,0,0),scale=1):
    before=set(bpy.data.objects)
    # L-shaped tertiary form, with a looped anticodon arm.
    pts=[(-.15,0,-1),(-.48,0,-.76),(-.48,0,-.35),(-.2,0,-.05),(-.45,.1,.35),(-.23,.15,.65),(.12,.12,.62),(.26,0,.26),(.56,0,.16),(1,.04,.5),(1.25,.07,.95)]
    traj=curve_points(pts,100);tube('tRNA folded backbone',traj,.083,P['lilac'],12)
    for i in range(0,len(traj),4):sphere('tRNA nucleotide',traj[i],(.098,)*3,P['purple'],12,9)
    for i,col in enumerate(['A','T','G']):sphere('Anticodon base',(-.38+i*.16,-.13,-.9),(.09,.14,.08),P[col],16,10)
    sphere('Attached amino acid',(1.29,.07,1.2),(.25,)*3,P['phosph'],32,24,lump=.06)
    path('Aminoacyl linkage',[(1.25,.07,.95),(1.29,.07,1.13)],.035,P['white'])
    return group('tRNA adaptor',list(set(bpy.data.objects)-before),pos,scale)

def ribosome(P,state):
    # An intentionally schematic molecular surface, not atomic-coordinate data.
    sphere('Large ribosomal subunit',(.15,.48,1.02),(2.05,1.4,1.28),P['teal'],96,64,lump=.085)
    sphere('Small ribosomal subunit',(0,.2,-.73),(1.8,1.05,.67),P['purple'],80,48,lump=.07)
    grains=Mesh()
    for i in range(430):
        z=1-2*(i+.5)/430;a=i*2.399963;r=sqrt(1-z*z)
        p=(.15+2.04*r*cos(a),.48+1.39*r*sin(a),1.02+1.27*z)
        grains.sphere(p,(.07,.075,.065),8,6)
    grains.obj('Ribosomal RNA and protein surface detail',P['cyan'])
    obs,_=capture(rna,P,state,pts=[(-4,-.95,-.18),(-2,-1,-.2),(0,-1,-.21),(2,-1,-.2),(4,-.8,-.17)],length=42)
    state['mrna_track']=group('mRNA translocation',obs)
    t=trna(P,state,(-.65,-1.15,.7),.72);state['trna']=t
    chain=[];state['peptide']=[]
    for i in range(22):
        a=i*.67;p=(1.1+.7*sin(a),-.5+.35*cos(a),1.5+i*.135)
        chain.append(p);state['peptide'].append(sphere('Growing polypeptide amino acid',p,(.12,)*3,P[['phosph','coral','pink','lime'][i%4]],16,10))
    state['peptide_backbone']=tube('Growing peptide backbone',curve_points(chain,150),.038,P['white'],8)
    state['peptide_bonds']=[tube('Peptide bond',[a,b],.038,P['white'],8) for a,b in zip(chain,chain[1:])]

def rna_processing(P,state):
    state['exons']=[];state['introns']=[]
    for k in range(3):
        obs,_=capture(rna,P,state,pts=[(-.85,0,.05),(.85,0,.05)],length=12)
        g=group('Exon %d'%(k+1),obs,((k-1)*2.3,0,0));state['exons'].append((g,g.location.copy()))
    for x in [-1.15,1.15]:
        pts=[(x-.4,0,.05),(x-.5,0,.8),(x,0,1.4),(x+.5,0,.8),(x+.4,0,.05)]
        ob=path('Intron loop',pts,.07,P['purple']);state['introns'].append(ob)
    sphere('Five prime cap',(-3.2,0,.05),(.22,)*3,P['phosph'])
    for i in range(12):sphere('Poly-A tail',(3.2+i*.085,0,.05),(.055,)*3,P['A'],10,7)

def protein(P,state):
    points=[]
    for i in range(350):
        t=i/349*8*pi
        p=(1.8*cos(t)*(.65+.22*sin(3*t)),1.45*sin(t)*(.65+.2*cos(4*t)),.12*t-1.5+.65*sin(t*1.5))
        points.append(p)
    tube('Folded polypeptide ribbon',points,.07,P['coral'],12)
    m=Mesh()
    for i,p in enumerate(points):
        if i%3==0:m.sphere(p,(.1,)*3,10,7)
    m.obj('Amino-acid sidechain representation',P['phosph'])
    for i in range(5):
        pts=[(-1.8+i*.55,.4+.3*sin(t*.12),-.9+t*.04+.18*sin(t*.5)) for t in range(50)]
        tube('Protein secondary-structure motif',pts,.09,P['teal'],12)

def chromosome(P):
    for x in [-.53,.53]:
        for side in [-1,1]:
            pts=curve_points([(x,0,0),(x+(.5 if x>0 else -.5),.02,side*1.1),(x+(.9 if x>0 else -.9),.1,side*2.1)])
            tube('Condensed sister chromatid arm',pts,.41,P['purple'],24)
            beads=Mesh()
            for i,p in enumerate(pts):
                if i%2==0:
                    for k in range(5):
                        a=k*2*pi/5+i*.4;beads.sphere(p+Vector((.42*cos(a),.42*sin(a),0)),(.085,)*3,8,6)
            beads.obj('Chromatin packing detail',P['lilac'])
    sphere('Centromere',(0,0,0),(.66,.42,.38),P['pink'])

def central(P,state):
    obs,_=capture(dna,P,state,False,True);group('DNA information',obs,(-3,0,.35),.43)
    obs,_=capture(rna,P,state);g=group('RNA information',obs,(0,0,.3),.34);g.rotation_euler.y=pi/2
    obs,_=capture(protein,P,state);group('Protein information',obs,(3,0,.1),.68)
    for x in [-1.4,1.5]:
        path('Information arrow',[(x-.37,-.1,.2),(x+.37,-.1,.2)],.045,P['cyan'])
        path('Arrow upper',[(x+.15,-.1,.4),(x+.37,-.1,.2),(x+.15,-.1,0)],.045,P['cyan'])
