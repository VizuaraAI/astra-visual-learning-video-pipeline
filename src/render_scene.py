"""Blender entry point: deterministic frames without fcurve API dependencies."""
import sys,os,json,argparse,time,math
from pathlib import Path
SRC=Path(__file__).resolve().parent;sys.path.insert(0,str(SRC))
import bpy
from mathutils import Vector
from geometry import *
import assets as A
import heart_assets as H
import dna_assets as D
from cardiac_motion import cardiac_cycle

def reset():
    bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
    for coll in [bpy.data.meshes,bpy.data.curves,bpy.data.materials,bpy.data.cameras,bpy.data.lights]:
        for data in list(coll):
            if data.users==0:coll.remove(data)

def make_asset(shot,P):
    A.R.seed(1909);H.R.seed(2323);D.R.seed(1953)
    asset=shot['asset'];state=dict(shot=shot,movers=[],heartbeat=[],leaflets=[])
    if asset in ['cell','cell_full','outro']:A.cell(P,asset=='cell_full')
    elif asset=='nucleus':
        A.nucleus(P)
        if shot['chapter']=='dna' and shot['index']==12:
            obs,_=capture(D.rna,P,state,pts=[(-.7,0,0),(.7,0,0)],length=14)
            state['export_rna']=group('Exporting mRNA',obs,(0,-.7,.1),.5)
    elif asset=='mitochondria':A.mitochondrion(P)
    elif asset in ['er','golgi','lysosome'] and shot['chapter']=='cell':
        A.cell(P,True)
        close=shot['index']>=38
        state['context_focus']={'er':((-1.35,.35,.6),(.23 if close else .44)),
          'golgi':((1.45,.25,.7),(.28 if close else .39)),
          'lysosome':((.1,-1.8,.33),(.12 if close else .22))}[asset]
    elif asset=='er':A.er(P)
    elif asset=='golgi':A.golgi(P,state)
    elif asset=='lysosome':A.lysosome(P,state)
    elif asset=='chloroplast':A.chloroplast(P)
    elif asset in ['plastids','leucoplast']:
        obs,_=capture(A.chloroplast,P);group('Chloroplast',obs,(-2,0,0),.66)
        sphere('Storage plastid',(1.6,0,0),(1.25,1,1.05),P['teal'],64,36,cut=lambda p:p[1]<0 and p[2]>0)
        for p in [(1.3,-.2,.1),(1.9,.1,.2),(1.5,.4,.45)]:sphere('Starch granule',p,(.35,.28,.28),P['white'],32,20,lump=.07)
    elif asset in ['bilayer','membrane','osmosis','diffusion']:A.membrane(P,state,asset)
    elif asset=='cork':A.cork(P)
    elif asset=='cork_micro':A.cork(P,True)
    elif asset in ['onion','onion_peel','onion_cells']:A.onion(P,asset=='onion_peel',asset=='onion_cells')
    elif asset=='microscope':
        if 'electron' in shot['title'].lower():A.electron_microscope(P)
        else:A.microscope(P)
    elif asset in ['slide','stain']:A.slide(P,state,asset=='stain')
    elif asset=='bacteria':A.bacteria(P)
    elif asset=='comparison':
        obs,_=capture(A.bacteria,P);group('Prokaryote',obs,(-2.5,0,0),.6)
        obs,_=capture(A.cell,P,False);group('Eukaryote',obs,(2.3,0,0),.5)
    elif asset=='division':
        for x in [-1.9,1.9]:
            obs,_=capture(A.cell,P,False);group('Daughter cell',obs,(x,0,0),.45)
    elif asset in ['heart','heart_cut','heart_flow']:H.heart(P,state,asset!='heart',asset=='heart_flow')
    elif asset=='alveoli':H.alveoli(P,state)
    elif asset=='blood':H.blood(P,state)
    elif asset in ['circulation','lymph']:H.circulation(P,state,asset=='lymph')
    elif asset in ['capillary','vessels']:H.capillary(P,state,asset=='vessels')
    elif asset=='valve':H.valve(P,state)
    elif asset=='conduction':H.conduction(P,state)
    elif asset in ['dna','transcription','mutation']:
        obs,_=capture(D.dna,P,state,asset=='transcription',shot['index'] in [4,5])
        if asset!='transcription':group('Helix cinematic orientation',obs).rotation_euler.y=.8
    elif asset=='nucleotide':D.nucleotide(P)
    elif asset=='rna':D.rna_processing(P,state)
    elif asset=='ribosome':D.ribosome(P,state)
    elif asset=='trna':D.trna(P,state)
    elif asset=='protein':D.protein(P,state)
    elif asset=='central':D.central(P,state)
    elif asset=='chromosome':D.chromosome(P)
    elif asset=='sequence':D.rna(P,state)
    else:raise ValueError(asset)
    return state

def setup(shot,args):
    reset();P=palette();state=make_asset(shot,P);scene=bpy.context.scene
    scene.render.engine='CYCLES';scene.cycles.samples=args.samples
    scene.render.use_persistent_data=bool(args.gpu)
    scene.cycles.use_denoising=True;scene.cycles.denoiser='OPENIMAGEDENOISE'
    if hasattr(scene.cycles,'denoising_use_gpu'):scene.cycles.denoising_use_gpu=bool(args.gpu)
    scene.cycles.max_bounces=6;scene.cycles.diffuse_bounces=3;scene.cycles.glossy_bounces=3
    scene.cycles.transmission_bounces=5;scene.cycles.transparent_max_bounces=4
    scene.cycles.adaptive_threshold=.02 if args.samples>=128 else .045;scene.render.threads_mode='FIXED';scene.render.threads=args.threads
    if args.gpu:
        pref=bpy.context.preferences.addons['cycles'].preferences
        pref.compute_device_type='CUDA';pref.get_devices()
        found=False
        for dev in pref.devices:dev.use=dev.type=='CUDA';found|=dev.use
        if not found:raise RuntimeError('No CUDA GPU exposed; refusing unexpected CPU cloud render')
        scene.cycles.device='GPU'
    else:scene.cycles.device='CPU'
    if hasattr(scene.render,'compositor_device'):scene.render.compositor_device='CPU'
    scene.use_nodes=False
    scene.render.resolution_x=args.width;scene.render.resolution_y=round(args.width*9/16);scene.render.resolution_percentage=100
    scene.render.fps=24;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.color_depth='8';scene.render.image_settings.compression=15
    scene.render.film_transparent=False
    scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=-.05
    world=bpy.data.worlds.new('Charcoal studio') if not bpy.data.worlds else bpy.data.worlds[0];scene.world=world;world.use_nodes=True
    world.node_tree.nodes.get('Background').inputs['Color'].default_value=(.026,.041,.052,1);world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.3
    # Fit the real mesh extents in the reserved picture area.
    bpy.context.view_layer.update();corners=[]
    for ob in bpy.context.scene.objects:
        if ob.type=='MESH':corners += [ob.matrix_world@Vector(c) for c in ob.bound_box]
    lo=Vector(tuple(min(c[i] for c in corners) for i in range(3)));hi=Vector(tuple(max(c[i] for c in corners) for i in range(3)))
    target=(lo+hi)/2
    flat=shot['asset'] in ['cork_micro','onion_cells','bilayer','membrane','osmosis','diffusion','mitochondria','chloroplast','slide','stain','valve','vessels','nucleotide']
    front=shot['asset'] in ['heart','heart_cut','heart_flow','conduction','circulation','lymph','central','dna','transcription','rna','sequence','ribosome','trna','protein','chromosome','mutation','comparison','division']
    direction=Vector((.24,-1,.9 if flat else (.18 if front else .54))).normalized()
    right=direction.cross(Vector((0,0,1))).normalized();up=right.cross(direction).normalized()
    data=bpy.data.cameras.new('Cinematic camera');cam=bpy.data.objects.new('Cinematic camera',data);bpy.context.collection.objects.link(cam);scene.camera=cam
    data.lens=55;data.sensor_width=36
    hfov=2*math.atan(36/(2*55));vfov=2*math.atan(math.tan(hfov/2)*9/16)
    needed=max(max(abs((p-target).dot(right))/math.tan(hfov/2),abs((p-target).dot(up))/math.tan(vfov/2)*1.22)+(p-target).dot(direction) for p in corners)
    dist=needed*(1.03 if flat else 1.07);state.update(camera=cam,target=target,dist=dist,direction=direction,base_positions={})
    if 'context_focus' in state:
        state['target']=Vector(state['context_focus'][0]);state['dist']*=state['context_focus'][1]
    if shot['asset']=='heart_flow':
        state['focus_to']=Vector({4:(-1,.1,1.2),5:(-.9,.05,-.65),6:(-.25,.0,2.3),9:(.9,.3,1.1),10:(.72,.02,-.85),11:(.8,.8,2.5)}.get(shot['index'],(0,0,.3)))
    # Three large softboxes create form; the backlight traces every cut edge.
    def light(name,p,energy,color,size):
        d=bpy.data.lights.new(name,'AREA');d.energy=energy;d.color=color;d.shape='DISK';d.size=size
        o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.location=p;o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
    extent=max((hi-lo).length/2,3);e=(extent/5)**2
    light('Warm key',target+Vector((-extent,-extent,extent*1.4)),1800*e,(1,.83,.64),extent*.95)
    light('Cool fill',target+Vector((extent,-extent*.5,extent*.6)),1050*e,(.48,.79,1),extent*.85)
    light('Pearl rim',target+Vector((extent*.4,extent*.7,extent*1.2)),2400*e,(.58,.87,1),extent*.65)
    light('Low warm rim',target+Vector((-extent*.7,extent*.4,-extent*.3)),550*e,(1,.36,.18),extent*.5)
    # A focus target is retained in the scene; mild DOF only on molecular close views.
    focus=bpy.data.objects.new('Focus plane',None);bpy.context.collection.objects.link(focus);focus.location=target
    data.dof.use_dof=False;data.dof.focus_object=focus;data.dof.aperture_fstop=9
    state['all_meshes']=[o for o in bpy.context.scene.objects if o.type=='MESH']
    return state

def animate(st,f):
    shot=st['shot'];u=f/max(1,shot['frames']-1);sec=f/24
    cam=st['camera'];d=st['direction'].copy();ang=(u-.5)*(.29 if shot['asset'] in ['dna','mitochondria','chloroplast','nucleus','protein','er'] else .16)
    x,y=d.x,d.y;d.x=x*math.cos(ang)-y*math.sin(ang);d.y=x*math.sin(ang)+y*math.cos(ang)
    eased=u*u*(3-2*u);zoom=1.07-.14*eased;target=st['target']
    if 'focus_to' in st:target=target.lerp(st['focus_to'],eased*.8);zoom*=1-.27*eased
    cam.location=target+d*st['dist']*zoom
    cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
    for ob,pts,phase,period in st['movers']:
        t=(sec/period+phase)%1;q=t*(len(pts)-1);j=min(int(q),len(pts)-2)
        ob.location=pts[j].lerp(pts[j+1],q-j)
        ob.rotation_euler=(.35*sin(sec+phase*6),.45*cos(sec*.7+phase*4),sec*.16+phase*6)
    contraction,av_open,semilunar_open=cardiac_cycle(sec)
    for ob in st['heartbeat']:
        pulse=1-.035*contraction;ob.scale=(pulse,pulse,1-.02*contraction)
    for ob,base in st['leaflets']:
        ob.location=base+Vector((0,0,.14*sin(sec*2*pi*.7)))
    for key,kind in st.get('valve_shapes',[]):
        key.value=semilunar_open if kind=='semilunar' else av_open
    if 'digest' in st:st['digest'].scale=(.8+.2*cos(sec*.45),)*3
    if 'coverslip' in st:st['coverslip'].location.z=.17+.3*(.5+.5*cos(min(1,u*2)*pi))
    if 'trna' in st:st['trna'].location.x=-.65+.13*sin(sec*.6)
    if 'mrna_track' in st:st['mrna_track'].location.x=-.22*(sec%4)
    if 'trna' in st:
        phase=(sec%4)/4
        st['trna'].location.x=-.65+1.2*(1-phase)**3
        st['trna'].location.z=.7+.45*(1-phase)**3
    if 'peptide' in st:
        # A growing chain during elongation; released as one continuous chain at termination.
        n=len(st['peptide']);reveal=max(4,round(n*(.2+.8*u))) if shot['index'] in [16,17] else n
        for i,o in enumerate(st['peptide']):o.hide_render=i>=reveal
        st['peptide_backbone'].hide_render=True
        for i,o in enumerate(st['peptide_bonds']):o.hide_render=i>=reveal-1
        if shot['index']==19:
            shift=max(0,u-.35)*1.7
            for o in st['peptide']:o.location.x=shift
            st['peptide_backbone'].location.x=shift
            for o in st['peptide_bonds']:o.location.x=shift
    if 'export_rna' in st:st['export_rna'].location.y=-.35-u*2.2
    if 'exons' in st:
        progress=max(0,min(1,(u-.3)/.4))
        for i,(o,p) in enumerate(st['exons']):o.location.x=p.x-(i-1)*.52*progress
        for o in st['introns']:o.location.z=progress*1.8;o.hide_render=progress>.97

def render_one(shot,args,start=0,end=None,preview=False):
    state=setup(shot,args);out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    frames=[shot['frames']//2] if preview else range(start,shot['frames'] if end is None else min(end,shot['frames']))
    t=time.time()
    for f in frames:
        path=out/(shot['id']+'.png' if preview else f'{f:06d}.png')
        if path.exists():continue
        bpy.context.scene.frame_set(f+1);animate(state,f);bpy.context.scene.render.filepath=str(path)
        bpy.ops.render.render(write_still=True)
    print('SHOT_RESULT '+json.dumps(dict(shot=shot['id'],seconds=time.time()-t,frames=len(frames))),flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--shot',type=int,default=0);p.add_argument('--output',required=True);p.add_argument('--width',type=int,default=1920);p.add_argument('--samples',type=int,default=48);p.add_argument('--threads',type=int,default=4);p.add_argument('--gpu',action='store_true');p.add_argument('--preview',action='store_true');p.add_argument('--all-previews',action='store_true');p.add_argument('--start',type=int,default=0);p.add_argument('--end',type=int)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);m=json.loads(Path(args.manifest).read_text())
    shots=m['shots'] if args.all_previews else [m['shots'][args.shot]]
    for shot in shots:render_one(shot,args,args.start,args.end,args.preview or args.all_previews)

if __name__=='__main__':main()
