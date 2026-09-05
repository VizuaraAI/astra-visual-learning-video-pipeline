"""Procedural scientific set pieces, built entirely from mathematical surfaces."""
import bpy, math, random
from math import sin,cos,pi,sqrt
from mathutils import Vector
from geometry import *

R=random.Random(1909)

def nucleus(P,pores=True):
    cut=lambda v:v[1]<0 and v[2]>-.13
    solidify(sphere('Double nuclear envelope',(0,0,0),(1.42,1.3,1.35),P['purple'],80,48,cut=cut),.09)
    solidify(sphere('Inner nuclear membrane',(0,0,0),(1.32,1.2,1.25),P['lilac'],72,40,cut=cut),.035)
    sphere('Nucleoplasm',(0,0,-.24),(1.2,1.09,.13),P['gel'])
    sphere('Nucleolus',(0,-.25,.05),(.52,.49,.51),P['darkpurple'],64,40,lump=.055)
    chrom=Mesh();beads=Mesh()
    for k in range(13):
        pts=[]
        for j in range(100):
            t=j/99*2*pi;r=.68+.19*sin(3*t+k)
            p=(r*cos(t+k*.48),r*sin(t+k*.48),-.13+.4*sin(2*t+k*1.3))
            pts.append(p)
            if j%6==0:beads.sphere(p,(.036,)*3,8,5)
        chrom.tube(pts,.014,6)
    chrom.obj('Chromatin fibres',P['lilac']);beads.obj('Nucleosome beads',P['phosph'])
    if pores:
        allp=Mesh()
        for i in range(72):
            z=1-2*(i+.5)/72;phi=i*2.399963;r=sqrt(1-z*z);p=Vector((1.44*r*cos(phi),1.32*r*sin(phi),1.37*z))
            if p.y<0 and p.z>-.16:continue
            n=p.normalized();x=n.cross(Vector((0,0,1))).normalized();y=n.cross(x)
            allp.tube([p+.072*(cos(t*2*pi/16)*x+sin(t*2*pi/16)*y) for t in range(17)],.021,6)
        allp.obj('Nuclear pore complexes',P['pink'])

def mitochondrion(P):
    cut=lambda v:v[2]>.12
    solidify(sphere('Outer mitochondrial membrane',(0,0,0),(2.1,.93,.57),P['gold'],96,40,lump=.025,cut=cut),.07)
    solidify(sphere('Inner boundary membrane',(0,0,.015),(1.99,.82,.49),P['green'],96,36,cut=cut),.03)
    sphere('Mitochondrial matrix',(0,0,-.05),(1.93,.77,.115),P['lime'],72,20)
    knobs=Mesh();stalk=Mesh()
    for k in range(11):
        x=(k-5)*.31;wid=.75*sqrt(max(.05,1-(x/1.9)**2))
        def fn(u,v):
            y=(v*2-1)*wid
            return(x+.12*sin(u*pi)+.045*sin(v*3*pi),y,.04+.43*sin(u*pi)*sin(v*pi)**.35)
        sheet=Mesh().grid(fn,12,28).obj('Crista fold %02d'%k,P['green']);solidify(sheet,.027)
        for j in range(12):
            v=(j+.5)/12;p=Vector(fn(.5,v));q=p+Vector((0,0,.08))
            stalk.tube([p,q],.012,6);knobs.sphere(q,(.046,)*3,9,6)
    knobs.obj('ATP synthase heads',P['phosph']);stalk.obj('ATP synthase stalks',P['cyan'])
    ring('Circular mitochondrial DNA',(1.45,0,.17),.18,.012,P['cyan'])
    speckles=Mesh()
    for i in range(170):
        x=R.uniform(-1.7,1.7);y=R.uniform(-.6,.6)
        if (x/1.9)**2+(y/.74)**2<1:speckles.sphere((x,y,.065),(.025,)*3,7,5)
    speckles.obj('Matrix ribosomes',P['darkpurple'])

def er(P):
    rib=Mesh()
    for k in range(6):
        def fn(u,v):return((u-.5)*3.5,(v-.5)*1.2+.13*sin(u*pi*2),k*.2+.17*sin(u*pi*2)+.12*cos(v*pi*2))
        o=Mesh().grid(fn,40,14).obj('RER cisterna %d'%k,P['pink']);solidify(o,.09)
        for j in range(70):
            u=R.random();v=R.random();p=Vector(fn(u,v))+Vector((0,0,.07))
            rib.sphere(p,(.044,.047,.039),9,6)
    rib.obj('RER bound ribosomes',P['darkpurple'])
    tubes=Mesh()
    for i in range(12):
        pts=[(-2.3+.33*cos(j*.15+i),-.6+i*.115,.08+j*.027) for j in range(55)]
        tubes.tube(pts,.085,12)
    for z in [.3,.7,1.1]:tubes.tube([(-2.3+.2*sin(i*.35),-.55+i*.024,z+.06*sin(i*.2)) for i in range(60)],.085,12)
    tubes.obj('Smooth ER tubular network',P['coral'])

def golgi(P,state=None):
    for k in range(7):
        def fn(u,v):
            x=(u-.5)*3.2;w=.78*sin(pi*u)**.35
            return(x,(v*2-1)*w+.13*(k-3),.22*k+.28*(x/1.6)**2+.06*sin(v*2*pi))
        solidify(Mesh().grid(fn,50,16).obj('Golgi cisterna %d'%k,P['coral']),.11)
    ves=Mesh()
    for k in range(34):
        a=R.random()*2*pi;rad=R.uniform(.08,.15)
        ves.sphere((R.choice([-1,1])*R.uniform(1.4,2.1),.6*sin(a),R.uniform(.15,1.8)),(rad,)*3,14,9)
    ves.obj('Golgi budding vesicles',P['gold'])
    if state is not None:
        for i in range(4):
            o=sphere('Cargo vesicle',(0,0,0),(.12,)*3,P['phosph'],20,12)
            state['movers'].append((o,curve_points([(1.5,0,1.25),(2.2,-.3,1.6),(2.6,-.8,.7),(3,-1,.5)]),i/4,7))

def chloroplast(P):
    solidify(sphere('Chloroplast envelope',(0,0,0),(2.1,1.12,.67),P['green'],80,40,cut=lambda v:v[2]>.05),.07)
    sphere('Stroma',(0,0,-.06),(1.98,1,.11),P['lime'],64,20)
    grana=[]
    for x,y in [(-1.25,-.35),(-.5,-.55),(.3,-.5),(1.15,-.3),(-1.1,.35),(-.25,.35),(.65,.38)]:
        for z in range(6):
            sphere('Thylakoid disc',(x,y,.065+z*.065),(.3,.3,.035),P['green'],28,12)
            ring('Thylakoid rim',(x,y,.065+z*.065),.285,.013,P['lime'])
        grana.append((x,y,.17))
    for a,b in zip(grana,grana[1:]):path('Stromal lamella',[a,((a[0]+b[0])/2,(a[1]+b[1])/2,.12),b],.035,P['green'])
    rub=Mesh()
    for _ in range(150):
        x=R.uniform(-1.8,1.8);y=R.uniform(-.8,.8)
        if (x/1.9)**2+(y/.9)**2<1:rub.sphere((x,y,.04),(.025,)*3,7,5)
    rub.obj('Stromal enzyme detail',P['phosph'])

def lysosome(P,state=None):
    solidify(sphere('Lysosomal membrane',(0,0,0),(1.6,1.45,1.4),P['green'],72,40,lump=.03,cut=lambda p:p[1]<-.08 and p[2]>.05),.085)
    enzymes=Mesh()
    for i in range(95):
        p=Vector((R.uniform(-1,1),R.uniform(-1,1),R.uniform(-1,1)))
        if p.length<1.1:enzymes.sphere(p,(.085,.07,.08),10,7,lump=.15)
    enzymes.obj('Digestive enzymes',P['lime'])
    o=sphere('Material being digested',(.1,-.55,.45),(.45,.2,.2),P['purple'],32,20,lump=.1)
    if state is not None:state['digest']=o

def cell(P,full=True):
    cut=lambda v:v[1]<0 and v[2]>-.12
    solidify(sphere('Cell membrane cutaway',(0,0,0),(3.8,3.05,2.72),P['gold'],112,64,lump=.022,cut=cut),.09)
    sphere('Cytosol cut surface',(0,0,-.17),(3.66,2.9,.15),P['gel'],96,32)
    cortex=Mesh()
    for i in range(380):
        x=R.uniform(-3.4,3.4);y=R.uniform(-2.5,2.5)
        if (x/3.5)**2+(y/2.7)**2<1:cortex.sphere((x,y,-.026),(.025,)*3,6,4)
    cortex.obj('Cytosolic molecular detail',P['cyan'])
    obs,_=capture(nucleus,P);group('Nucleus assembly',obs,(-.45,.65,.7),.8)
    if full:
        obs,_=capture(er,P);group('ER assembly',obs,(-1.05,.35,.15),.55)
        obs,_=capture(golgi,P);group('Golgi assembly',obs,(1.45,.25,.2),.62)
        for p,angle,s in [((-1.9,-1.35,.17),-.35,.42),((1.8,-1.4,.18),.4,.46),((.1,1.9,.3),1.2,.4)]:
            obs,_=capture(mitochondrion,P);g=group('Mitochondrion assembly',obs,p,s);g.rotation_euler.z=angle
        for p in [(-2.4,.6,.35),(.1,-1.8,.34),(2.2,1.1,.35)]:
            obs,_=capture(lysosome,P);group('Lysosome assembly',obs,p,.22)

def membrane(P,state,mode='bilayer'):
    heads=Mesh();tails=Mesh()
    for i in range(24):
        for j in range(15):
            x=(i-11.5)*.235;y=(j-7)*.235;wav=.11*sin(x*1.8)*cos(y)
            if (x/.5)**2+(y/.65)**2<1.2:continue
            for sign in [-1,1]:
                z=sign*.46+wav;heads.sphere((x,y,z),(.12,)*3,10,7)
                for dx in [-.035,.035]:tails.tube([(x+dx,y,z-sign*.08),(x+dx+.03,y+.035,z-sign*.2),(x+dx-.025,y-.025,wav+sign*.04)],.025,6)
    heads.obj('Hydrophilic phosphate heads',P['gold']);tails.obj('Hydrophobic lipid tails',P['lime'])
    for i in range(7):
        a=i*2*pi/7;sphere('Transmembrane protein helix',(.47*cos(a),.47*sin(a),0),(.16,.16,.73),P['purple'],28,20,lump=.035)
    ring('Channel protein rim',(0,0,.62),.38,.08,P['lilac'])
    for i in range(13):
        x=R.uniform(-2.4,2.4);y=R.uniform(-1.5,1.5)
        if mode=='osmosis':x,y=R.uniform(-.13,.13),R.uniform(-.13,.13)
        o=sphere('Transport particle',(0,0,0),(.10,)*3,P['cyan'] if mode=='osmosis' else P['red'],16,10)
        state['movers'].append((o,curve_points([(x,y,2.3),(x+.1,y,1),(x,y,0),(x-.1,y,-1),(x,y,-2.1)]),i/13,6))

def cork(P,micro=False):
    corkmat=material('Procedural cork',(.52,.27,.09),0,.74,noise=.65)
    if not micro:
        ob=Mesh().tube([(0,0,-1.5),(0,0,1.5)],[1.1,1.3],72).obj('Cork stopper',corkmat)
        for face in ob.data.polygons[-2:]:face.use_smooth=False
        for z in [-1.3,-1,-.7,-.4,-.1,.2,.5,.8,1.1,1.4]:ring('Cork growth line',(0,0,z),1.2+z/15,.009,P['gold'])
    else:
        walls=Mesh();grain=Mesh()
        for i in range(-6,7):
            for j in range(-5,6):
                x=i*.67;y=j*.77+(i%2)*.385
                if x*x+y*y>15:continue
                pts=[(x+.43*cos(a*pi/3),y+.43*sin(a*pi/3),.05) for a in range(7)]
                walls.tube(pts,.055,8)
                for k in range(12):grain.sphere((x+R.uniform(-.27,.27),y+R.uniform(-.27,.27),-.15),(.07,.04,.035),7,4)
        walls.obj('Cork cell walls',P['gold']);grain.obj('Cork texture granules',corkmat)

def onion(P,peel=False,cells=False):
    if cells:
        walls=Mesh();nuc=Mesh()
        for i in range(-4,5):
            for j in range(-3,4):
                x=i*.9+(j%2)*.22;y=j*.9
                box('Epidermal cell interior',(x,y,-.05),(.86,.86,.18),P['pink'],.1)
                walls.tube([(x-.43,y-.43,.06),(x+.43,y-.43,.06),(x+.43,y+.43,.06),(x-.43,y+.43,.06),(x-.43,y-.43,.06)],.027,8)
                nuc.sphere((x+.2,y+.1,.1),(.09,.13,.05),12,8)
        walls.obj('Cellulose cell walls',P['lilac']);nuc.obj('Stained nuclei',P['purple'])
    else:
        for k in range(7):
            r=1.6-k*.18
            solidify(sphere('Onion scale leaf',(0,0,0),(r,r,r*1.1),P['pink'] if k%2==0 else P['white'],64,36,cut=lambda p:p[1]<-.2),.04)
        if peel:
            o=Mesh().grid(lambda u,v:((u-.5)*2.2,-1.2-.5*sin(u*pi),(v-.5)*1.6+.22*sin(u*4)),32,24).obj('Thin epidermal peel',P['lilac']);solidify(o,.016)

def microscope(P):
    box('Microscope base',(0,0,-1.7),(2.5,2.2,.35),P['white'])
    path('Microscope arm',[(0,.65,-1.6),(0,1,-.4),(0,1.05,1.1),(0,.45,1.9)],.28,P['white'])
    box('Mechanical stage',(0,-.1,-.15),(2.4,1.8,.18),P['black'],.08)
    box('Glass slide',(0,-.15,0),(1.2,.5,.045),P['glass'],.01)
    path('Body tube',[(0,.45,1.8),(0,.06,2.4),(0,-.3,2.85)],.25,P['black'])
    ring('Eyepiece rim',(0,-.3,2.85),.23,.03,P['steel'],(0,-.5,.8))
    sphere('Eyepiece glass',(0,-.32,2.87),(.19,.15,.04),P['cyan'])
    for x in [-.55,0,.55]:path('Objective',[(0,.2,1.5),(x,.1,1),(x,-.05,.45)],.12,P['steel'])
    for x in [-.6,.6]:sphere('Focus knob',(x,.8,.1),(.23,.28,.28),P['black'])
    sphere('Illuminator',(0,-.2,-1.3),(.45,.45,.2),P['steel']);sphere('Light aperture',(0,-.2,-1.08),(.3,.3,.025),P['white'])

def electron_microscope(P):
    box('TEM base',(0,0,-2.0),(3.2,2.4,.4),P['white'],.18)
    for z,r in [(-1.4,.9),(-.8,.78),(-.1,.58),(.6,.53),(1.3,.48),(2,.39),(2.7,.3)]:
        tube('Electron-optical vacuum column',[(0,0,z-.29),(0,0,z+.29)],r,P['steel'],48)
        ring('Electromagnetic lens housing',(0,0,z),r+.035,.065,P['black'])
    box('Specimen chamber',(0,0,.25),(1.65,1.25,.6),P['white'],.13)
    path('Specimen holder',[(.5,-.1,.3),(1.55,-.1,.3)],.075,P['steel'])
    box('Viewing chamber',(0,-.3,-1.25),(2.3,1.8,.75),P['white'],.18)
    sphere('Viewing window',(0,-1.23,-1.1),(.5,.025,.26),P['glass'])
    box('Control console',(2.3,-.55,-1.3),(1.45,1.1,1.4),P['black'],.12)
    screen=box('Instrument monitor',(2.3,-.65,-.1),(1.3,.16,.85),P['teal'],.06)
    path('Vacuum line',[(0,.5,-1.2),(-1.4,.8,-1.2),(-1.5,.8,-2)],.12,P['steel'])

def slide(P,state,stain=False):
    sphere('Watch glass',(-1.5,.4,0),(1.7,1.7,.17),P['glass'],64,28)
    box('Microscope glass slide',(1.3,-.3,.05),(2.5,1.15,.065),P['glass'],.04)
    for p in [(-1.5,.4,.2),(1.3,-.3,.12)]:solidify(Mesh().grid(lambda u,v:(p[0]+(u-.5)*.85,p[1]+(v-.5)*.65,p[2]+.025*sin(u*5)*sin(v*5)),22,16).obj('Onion peel',P['lilac']),.01)
    o=box('Cover slip',(1.3,-.3,.38),(1.08,1.02,.03),P['glass'],.01);state['coverslip']=o
    if stain:
        box('Staining bottle',(-1.6,1.8,.7),(.55,.55,1.15),P['white'],.16)
        path('Dropper',[(1.3,-.3,2.4),(1.3,-.3,1.4)],.075,P['glass'])
        o=sphere('Safranin drop',(1.3,-.3,.7),(.10,.10,.16),P['pink']);state['movers'].append((o,curve_points([(1.3,-.3,1.4),(1.3,-.3,.16)]),0,3))
    else:
        for dx in [-.08,.08]:path('Forceps prong',[(-1.45+dx,-.1,2),(-1.2+dx,.1,1),(-1.3+dx,.3,.4)],.035,P['steel'])

def bacteria(P):
    solidify(sphere('Bacterial envelope',(0,0,0),(2.4,1.15,1.05),P['teal'],80,40,cut=lambda p:p[1]<0 and p[2]>.0),.1)
    sphere('Bacterial cytoplasm',(0,0,-.06),(2.23,1,.09),P['lilac'])
    dna=Mesh()
    pts=[(1.35*cos(t*2*pi/220),.48*sin(t*2*pi/220),.3+.25*sin(t*8*pi/220)) for t in range(221)]
    dna.tube(pts,.045,9);dna.obj('Nucleoid DNA',P['purple'])
    b=Mesh()
    for _ in range(150):
        x=R.uniform(-2,2);y=R.uniform(-.8,.8)
        if (x/2.1)**2+(y/.9)**2<1:b.sphere((x,y,.06),(.04,)*3,8,6)
    b.obj('Bacterial ribosomes',P['darkpurple'])
    path('Flagellum',[(2.2,0,0),(2.8,.2,0),(3.5,-.3,.2),(4,.3,.4),(4.4,0,.7)],.04,P['teal'])
