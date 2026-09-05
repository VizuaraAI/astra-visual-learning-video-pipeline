"""Original teaching models: anatomically oriented heart and blood-flow set pieces."""
from geometry import *
import random
R=random.Random(2323)

def rbc_mesh(name,P,oxygen=True):
    m=Mesh();n=48;nr=14
    for side in [-1,1]:
        off=len(m.v)
        for j in range(nr+1):
            r=j/nr
            z=side*.5*sqrt(max(0,1-r*r))*(.207+2.003*r*r-1.123*r**4)
            for i in range(n+1):
                a=i*2*pi/n;m.v.append((r*cos(a),r*sin(a),z))
        for j in range(nr):
            for i in range(n):
                k=off+j*(n+1)+i
                m.f.append((k+n+1,k+n+2,k+1,k) if side>0 else (k,k+1,k+n+2,k+n+1))
    return m.obj(name,P['red'] if oxygen else P['deoxy'])

def vessel(P,name,pts,r,mat):
    p=curve_points(pts,64);m=Mesh().tube(p,r,24);m.f=m.f[:-2];o=solidify(m.obj(name,mat),r*.13)
    for j in [0,-1]:
        normal=(p[1]-p[0]) if j==0 else (p[-1]-p[-2])
        ring(name+' open rim',p[j],r*.89,r*.11,P['wall'],normal)
    return o

def heart(P,state,cut=False,flow=False):
    parts=[]
    # Schematic frontal cutaway, anatomical right at negative X.
    # The LV has a substantially thicker wall and extends to the apex.
    chambers=[('Right atrium',(-1,.25,1.1),(.94,.7,.95),.11),('Left atrium',(.92,.52,1.15),(.84,.7,.83),.12),('Right ventricle',(-.88,.12,-.63),(1.02,.83,1.5),.15),('Left ventricle',(.72,.2,-.83),(.99,.88,1.8),.32)]
    # Merge the myocardium into a single continuous organic wall before cutting chambers.
    outers=[sphere(name+' outer mass',c,s,P['muscle'],56,36,lump=.018) for name,c,s,t in chambers]
    bpy.ops.object.select_all(action='DESELECT')
    for o in outers:o.select_set(True)
    bpy.context.view_layer.objects.active=outers[0];bpy.ops.object.join();body=bpy.context.object;body.name='Continuous myocardium'
    mod=body.modifiers.new('Unified muscular volume','REMESH');mod.mode='VOXEL';mod.voxel_size=.065;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
    mod=body.modifiers.new('Soft organic transitions','SMOOTH');mod.factor=1.1;mod.iterations=6;bpy.ops.object.modifier_apply(modifier=mod.name)
    body.data.materials.append(P['wall'])
    if cut:
        for name,c,s,t in chambers:
            inner=sphere('Temporary chamber cavity',c,tuple(a-t for a in s),None,56,36)
            mod=body.modifiers.new('Anatomical cavity','BOOLEAN');mod.operation='DIFFERENCE';mod.object=inner;mod.solver='EXACT';bpy.context.view_layer.objects.active=body;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(inner,do_unlink=True)
        cutter=box('Temporary frontal section cutter',(0,-5,0),(15,10,18),P['wall'],0)
        mod=body.modifiers.new('Frontal cutaway','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cutter;mod.solver='EXACT';bpy.context.view_layer.objects.active=body;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
        mod=body.modifiers.new('Soft cut rim','BEVEL');mod.width=.024;mod.segments=3
    parts.append(body)
    for name,c,s,thickness in chambers:
        if cut:
            inn=tuple(a-thickness for a in s)
            # Endocardial ridges (trabeculae) follow the chamber wall.
            for k in range(8):
                a=k*pi/7;pts=[]
                for j in range(31):
                    t=j*pi/30
                    pts.append((c[0]+inn[0]*.78*cos(a)*sin(t),c[1]+inn[1]*.86*sin(a)*sin(t),c[2]+inn[2]*.83*cos(t)))
                parts.append(tube(name+' trabecula',pts,.018,P['pink'],8))
    if cut:
        parts.append(path('Interventricular septum',[(0,.13,.55),(-.05,.16,-.2),(.13,.18,-1.35),(.62,.2,-2.45)],.14,P['wall']))
        for x,n in [(-1,3),(.8,2)]:
            ring('AV valve annulus',(x,-.02,.36),.46,.055,P['white'])
            for i in range(n):
                a=i*2*pi/n
                def fn(u,v,a=a,x=x,n=n):
                    angle=a+(v-.5)*2*pi/n;r=.46*(1-u)
                    return(x+r*cos(angle),-.02+r*sin(angle),.36-.3*sin(u*pi/2))
                ob=solidify(Mesh().grid(fn,14,18).obj('Valve leaflet',P['white']),.018)
                ob.shape_key_add(name='Closed');key=ob.shape_key_add(name='Open')
                for v in key.data:
                    dx=v.co.x-x;dy=v.co.y+.02;rad=sqrt(dx*dx+dy*dy);u=max(0,min(1,1-rad/.46));ang=math.atan2(dy,dx)
                    v.co=(x+.46*(1-u*.35)*cos(ang),-.02+.46*(1-u*.35)*sin(ang),.36-.55*u)
                state.setdefault('valve_shapes',[]).append((key,'av'))
                p=(x+.25*cos(a),.0+.25*sin(a),.2)
                path('Chordae tendineae',[p,(x+.15*cos(a),.12,-.2),(x+.25*cos(a),.15,-.6)],.014,P['white'])
                sphere('Papillary muscle',(x+.25*cos(a),.15,-.62),(.11,.12,.25),P['muscle'])
    vessel(P,'Aorta',[(.7,.45,.55),(.5,.75,1.6),(.35,.9,2.6),(1,.85,3.25),(1.7,.9,2.8),(1.75,1,1.6)],.31,P['red'])
    for i in range(3):vessel(P,'Aortic arch branch',[(.65+i*.35,.86,3.13),(.55+i*.4,.87,3.9)],.115,P['red'])
    vessel(P,'Pulmonary trunk',[(-.55,-.25,-.2),(-.4,-.4,1.2),(-.25,-.15,2.3),(-1.1,.1,2.65),(-2.35,.5,2.65)],.29,P['blue'])
    vessel(P,'Right pulmonary branch',[(-.3,.05,2.3),(.7,.2,2.5),(2.3,.5,2.5)],.21,P['blue'])
    vessel(P,'Superior vena cava',[(-1.25,.4,1.35),(-1.5,.4,2.3),(-1.5,.4,3.35)],.32,P['blue'])
    vessel(P,'Inferior vena cava',[(-1.2,.6,1),(-1.75,.75,-.2),(-1.8,.8,-1.4)],.3,P['blue'])
    for side in [-1,1]:
        for z in [.9,1.4]:vessel(P,'Pulmonary vein',[(.9,.7,z),(side*1.7,1,z+.1),(side*2.45,1.1,z+.3)],.16,P['red'])
    if not cut:
        path('Anterior interventricular coronary artery',[(.4,-.6,1.7),(.05,-.84,.8),(-.07,-.78,-.15),(.08,-.65,-1.2),(.48,-.3,-2.38)],.06,P['gold'])
        path('Right coronary artery',[(.35,-.63,1.7),(-.55,-.57,1.45),(-1.5,-.4,.8),(-1.75,-.2,.1)],.05,P['gold'])
        for k in range(7):
            z=.7-k*.39
            path('Coronary branch',[(.03,-.84,z),(.65,-.8,z-.12),(1.3,-.58,z-.34)],.025,P['gold'])
    state['heartbeat']=parts
    if flow:
        # Path selected from the actual narration step. Flows stay in the appropriate chambers.
        routes={4:[(-1.5,.4,3.3),(-1.35,.25,2),(-1,.05,1.1)],5:[(-1,.02,1.1),(-1,-.02,.36),(-.9,.02,-.65)],6:[(-.9,.02,-.65),(-.5,-.25,.3),(-.25,-.15,2.3),(-2.3,.5,2.65)],9:[(2.4,1.1,1.4),(1.6,.75,1.25),(.92,.35,1.1)],10:[(.92,.2,1.1),(.8,-.02,.36),(.72,.0,-.85)],11:[(.72,.0,-.85),(.7,.45,.55),(.35,.9,2.6),(1,.85,3.25),(1.75,1,1.6)]}
        pts=routes.get(state['shot']['index'],routes[11]);traj=curve_points(pts,100)
        tube('Highlighted blood route',traj,.045,P['cyan'],9)
        for i in range(8):
            o=rbc_mesh('Travelling red blood cell',P,state['shot']['index']>=9);o.scale=(.15,)*3
            state['movers'].append((o,traj,i/8,6))

def alveoli(P,state):
    shell=material('Alveolar tissue',(.76,.29,.34),0,.42,.18,noise=.25)
    for k in range(9):
        a=k*2*pi/9;p=(1.18*cos(a),.85*sin(a),.5+.25*sin(a*3))
        sphere('Alveolar air sac',p,(.8,.77,.75),shell,48,28,lump=.08)
        for j in range(3):
            pts=[]
            for t in range(61):
                u=t*2*pi/60;pts.append((p[0]+.81*cos(u),p[1]+.6*sin(u)*cos(j*.8),p[2]+.64*sin(u)*sin(j*.8)))
            tube('Alveolar capillary network',pts,.042,P['red'] if k>3 else P['deoxy'],8)
    path('Bronchiole',[(0,0,3),(0,0,1.8),(0,0,.8)],.4,shell)
    for i in range(20):
        x=R.uniform(-1.4,1.4);y=R.uniform(-.8,.8)
        o=sphere('Oxygen exchange',(0,0,0),(.06,)*3,P['cyan'],12,8)
        state['movers'].append((o,curve_points([(x,y,1.2),(x+.6,y-.7,.6),(x+1,y-1,.3)]),i/20,5))

def blood(P,state):
    # Cells all retain shades of red; no blue erythrocytes.
    for i in range(22):
        o=rbc_mesh('Red blood cell %d'%i,P,i%3!=0);o.scale=(.35,)*3
        pts=curve_points([(-4,R.uniform(-1.6,1.6),R.uniform(-1,1)),(0,R.uniform(-1,1),R.uniform(-.7,.7)),(4,R.uniform(-1.3,1.3),R.uniform(-1,1))])
        state['movers'].append((o,pts,i/22,14))
    sphere('White blood cell',(1.1,.25,.45),(.64,.6,.64),P['white'],64,44,lump=.08)
    for j in range(3):sphere('Lobed WBC nucleus',(1.1+.23*cos(j*2*pi/3),-.15,.4+.23*sin(j*2*pi/3)),(.24,.15,.21),P['purple'])
    for i in range(12):sphere('Platelet',(R.uniform(-3,3),R.uniform(-1.4,1.4),R.uniform(-1,1)),(.09,.07,.07),P['phosph'],16,12,lump=.12)

def circulation(P,state,lymph=False):
    obs,_=capture(heart,P,dict(state,heartbeat=[],leaflets=[]),False,False);group('Heart in circuit',obs,(0,0,.6),.38)
    for x in [-1.45,1.45]:sphere('Lung',(x,.65,2.45),(.92,.52,1.05),P['pink'],48,32,lump=.05)
    for x in [-2,-1,0,1,2]:sphere('Body tissue cell',(x,.35,-2.7),(.5,.38,.5),P['gel'],32,24,lump=.05)
    routes=[([(-.4,0,.4),(-2.3,-.1,1),(-2.5,0,2.7),(-1.5,0,3.15)],P['blue']),([(-1.4,0,3.1),(2.1,.1,3),(2.4,0,1.7),(.45,0,.65)],P['red']),([(.4,0,.3),(3,-.2,-.2),(3,-.2,-2.7),(0,-.1,-3.3)],P['red']),([(0,-.1,-3.3),(-3,-.2,-2.7),(-3,-.2,-.5),(-.4,0,.5)],P['blue'])]
    for j,(pts,mat) in enumerate(routes):
        traj=curve_points(pts,90);tube('Circulation route',traj,.11,mat,16)
        for i in range(5):
            o=sphere('Flow marker',(0,0,0),(.085,)*3,P['white'],12,8)
            state['movers'].append((o,traj,i/5,7))
    if lymph:
        traj=curve_points([(1,.2,-2.8),(2,.2,-1.7),(1.7,.4,-.3),(-1,.3,.7)])
        tube('Lymphatic return',traj,.1,P['green'],14)
        for i in range(5):sphere('Lymph node',traj[8+i*10],(.17,.12,.24),P['lime'],24,16)

def capillary(P,state,comparison=False):
    if comparison:
        for x,mat,thick in [(-1.7,P['red'],.24),(1.7,P['blue'],.09)]:
            pts=[(x,0,-2),(x,0,2)];tube('Blood vessel outer wall',pts,.85,mat,48)
            # Axial cross section is a visible annulus with a dark lumen.
            ring('Wall cross section',(x,0,2.02),.85-thick/2,thick/2,P['wall'])
            sphere('Lumen',(x,0,2.035),(.85-thick,.85-thick,.014),P['black'])
            if x>0:
                for sign in [-1,1]:path('Venous valve leaflet',[(x+sign*.7,0,.2),(x+sign*.25,0,.55),(x,0,.9)],.055,P['white'])
        return
    # An opened capillary segment with erythrocytes moving through the lumen.
    tube('Capillary endothelial wall',[(-4,.45,0),(4,.45,0)],.61,P['vessel'],32)
    # Expose lumen by using half cylindrical surface.
    ob=bpy.data.objects.get('Capillary endothelial wall');bpy.data.objects.remove(ob,do_unlink=True)
    solidify(Mesh().grid(lambda u,v:((u-.5)*8,.45+.61*sin(v*pi),.61*cos(v*pi)),60,26).obj('Thin endothelial wall',P['pink']),.025)
    for i in range(9):
        o=rbc_mesh('Capillary erythrocyte',P);o.scale=(.34,)*3
        state['movers'].append((o,curve_points([(-4,-.05,0),(4,-.05,0)]),i/9,12))
    for i in range(10):
        x=(i-4.5)*.75;sphere('Tissue cell',(x,1.8,-.1),(.47,.5,.45),P['gel'],32,20,lump=.055)
    for i in range(24):
        x=R.uniform(-3.5,3.5);o=sphere('Diffusing molecule',(0,0,0),(.055,)*3,P['cyan'] if i%2==0 else P['gold'],10,7)
        pts=[(x,0,.05),(x+.15,.8,.2),(x+.3,1.7,.2)]
        if i%2:pts.reverse()
        state['movers'].append((o,curve_points(pts),i/24,5))

def valve(P,state):
    ring('Valve annulus',(0,0,0),1.75,.19,P['wall'])
    for i in range(3):
        a=i*2*pi/3
        def fn(u,v):
            angle=a+(v-.5)*2*pi/3;r=1.65*(1-u*.94)
            return(r*cos(angle),r*sin(angle),-.42*sin(u*pi/2)+.08*sin(v*pi))
        o=solidify(Mesh().grid(fn,28,28).obj('Semilunar cusp',P['white']),.03)
        o.shape_key_add(name='Closed');key=o.shape_key_add(name='Open')
        for v in key.data:
            rad=sqrt(v.co.x*v.co.x+v.co.y*v.co.y);u=max(0,min(1,(1-rad/1.65)/.94));ang=math.atan2(v.co.y,v.co.x)
            v.co=(1.65*(1-u*.18)*cos(ang),1.65*(1-u*.18)*sin(ang),-1.1*u)
        state.setdefault('valve_shapes',[]).append((key,'semilunar'))
    for i in range(8):
        o=rbc_mesh('Blood through valve',P);o.scale=(.24,)*3
        state['movers'].append((o,curve_points([(.2,.2,-2),(.2,.2,0),(.3,.2,2.4)]),i/8,6))

def conduction(P,state):
    heart(P,state,cut=False)
    points=[(-1.2,-.46,1.8),(-.6,-.72,1),(-.12,-.75,.35),(.05,-.76,-.5),(.35,-.5,-1.9)]
    traj=curve_points(points);tube('Cardiac conduction pathway',traj,.032,P['cyan'],10)
    for p,r in [(points[0],.14),(points[2],.11)]:sphere('Conduction node',p,(r,)*3,P['phosph'])
    for sign in [-1,1]:path('Purkinje branch',[(.1,-.75,-.4),(sign*.7,-.65,-1.1),(sign*1.15,-.35,-1.7)],.022,P['cyan'])
    for i in range(4):
        o=sphere('Electrical impulse',(0,0,0),(.075,)*3,P['white'],16,12);state['movers'].append((o,traj,i/4,3))
