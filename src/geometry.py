"""Original procedural geometry. Blender 5.2; no downloaded models."""
import bpy, math, random
from mathutils import Vector
from math import sin, cos, pi, sqrt

def material(name,color,metal=0.,rough=.32,sub=.04,noise=0.,emission=0.,transmission=0.):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    n=m.node_tree.nodes;p=n.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    p.inputs['Subsurface Weight'].default_value=sub
    p.inputs['Coat Weight'].default_value=.18;p.inputs['Coat Roughness'].default_value=.22
    p.inputs['Transmission Weight'].default_value=transmission
    if emission:
        p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=emission
    if noise:
        t=n.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=22;t.inputs['Detail'].default_value=3.5;t.inputs['Roughness'].default_value=.7
        b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=noise;b.inputs['Distance'].default_value=.035
        m.node_tree.links.new(t.outputs['Fac'],b.inputs['Height']);m.node_tree.links.new(b.outputs['Normal'],p.inputs['Normal'])
    return m

class Mesh:
    def __init__(self):self.v=[];self.f=[]
    def sphere(self,c=(0,0,0),s=(1,1,1),nu=32,nv=20,lump=0.,cut=None):
        off=len(self.v)
        for j in range(nv+1):
            a=pi*j/nv
            for i in range(nu+1):
                b=2*pi*i/nu
                k=1+lump*(sin(5*b+2*a)*sin(a)**2+.4*sin(9*a-3*b))
                self.v.append((c[0]+s[0]*sin(a)*cos(b)*k,c[1]+s[1]*sin(a)*sin(b)*k,c[2]+s[2]*cos(a)*k))
        for j in range(nv):
            for i in range(nu):
                ids=[off+j*(nu+1)+i,off+j*(nu+1)+i+1,off+(j+1)*(nu+1)+i+1,off+(j+1)*(nu+1)+i]
                cent=tuple(sum(self.v[k][a] for k in ids)/4 for a in range(3))
                if not cut or not cut(cent):self.f.append(list(reversed(ids)))
        return self
    def tube(self,points,r=.05,sides=10,closed=False):
        pts=[Vector(p) for p in points];off=len(self.v);N=len(pts)
        for i,p in enumerate(pts):
            t=pts[min(i+1,N-1)]-pts[max(i-1,0)]
            if t.length<1e-6:t=Vector((0,0,1))
            t.normalize();ref=Vector((0,0,1)) if abs(t.z)<.9 else Vector((0,1,0))
            x=t.cross(ref).normalized();y=t.cross(x).normalized()
            rad=r[i] if isinstance(r,list) else r
            for j in range(sides):self.v.append(tuple(p+rad*(cos(j*2*pi/sides)*x+sin(j*2*pi/sides)*y)))
        for i in range(N-1):
            for j in range(sides):self.f.append((off+i*sides+j,off+i*sides+(j+1)%sides,off+(i+1)*sides+(j+1)%sides,off+(i+1)*sides+j))
        self.f.append(tuple(off+j for j in reversed(range(sides))));self.f.append(tuple(off+(N-1)*sides+j for j in range(sides)))
        return self
    def grid(self,fn,nu,nv):
        off=len(self.v)
        for i in range(nu+1):
            for j in range(nv+1):self.v.append(fn(i/nu,j/nv))
        for i in range(nu):
            for j in range(nv):
                k=off+i*(nv+1)+j;self.f.append((k,k+nv+1,k+nv+2,k+1))
        return self
    def obj(self,name,mat,smooth=True):
        me=bpy.data.meshes.new(name);me.from_pydata(self.v,[],self.f);me.update()
        ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob)
        if mat:me.materials.append(mat)
        if smooth:
            for p in me.polygons:p.use_smooth=True
        return ob

def sphere(name,c,s,mat,nu=48,nv=28,lump=0.,cut=None):return Mesh().sphere(c,s,nu,nv,lump,cut).obj(name,mat)
def tube(name,points,r,mat,sides=12):return Mesh().tube(points,r,sides).obj(name,mat)
def solidify(o,t=.06):
    m=o.modifiers.new('Membrane thickness','SOLIDIFY');m.thickness=t;m.offset=-.5
    m=o.modifiers.new('Soft cut edge','BEVEL');m.width=t*.35;m.segments=3
    return o
def box(name,c,s,mat,bevel=.12):
    bpy.ops.mesh.primitive_cube_add(size=1,location=c);o=bpy.context.object;o.name=name;o.scale=s
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if mat:o.data.materials.append(mat)
    if bevel:m=o.modifiers.new('Rounded edges','BEVEL');m.width=bevel;m.segments=4
    for p in o.data.polygons:p.use_smooth=True
    o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o
def ring(name,c,r,thick,mat,normal=(0,0,1)):
    n=Vector(normal).normalized();x=n.cross(Vector((0,0,1)) if abs(n.z)<.9 else Vector((0,1,0))).normalized();y=n.cross(x)
    return tube(name,[Vector(c)+r*(cos(i*2*pi/64)*x+sin(i*2*pi/64)*y) for i in range(65)],thick,mat)
def curve_points(points,steps=60):
    # Catmull-Rom curve through the supplied control points.
    p=[Vector(points[0])]+[Vector(q) for q in points]+[Vector(points[-1])];out=[]
    n=len(points)-1
    for k in range(steps+1):
        q=min(k/steps*n,n-1e-8);i=int(q);t=q-i;a,b,c,d=p[i:i+4]
        out.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
    return out
def path(name,points,r,mat):return tube(name,curve_points(points),r,mat,16)
def group(name,objects,c=(0,0,0),scale=1):
    e=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(e)
    for o in objects:o.parent=e
    e.location=c;e.scale=(scale,)*3 if isinstance(scale,(int,float)) else scale
    return e
def capture(fn,*args,**kwargs):
    before=set(bpy.data.objects);res=fn(*args,**kwargs);return [o for o in bpy.data.objects if o not in before],res

def palette():
    return dict(
      gold=material('Membrane | amber pearl',(.83,.39,.075),.17,.29,noise=.11),
      gel=material('Cytosol | blue porcelain',(.23,.55,.62),.03,.39,.13,noise=.15),
      purple=material('Nuclear envelope | violet',(.24,.075,.54),.15,.29,.08,noise=.16),
      lilac=material('Chromatin | lilac',(.61,.39,.91),.15,.31),
      darkpurple=material('Nucleolus | indigo',(.055,.027,.17),.2,.34,noise=.22),
      pink=material('Rough ER | rose',(.64,.13,.27),.13,.35,.11,noise=.12),
      coral=material('Golgi | persimmon',(.92,.25,.09),.12,.28,.1,noise=.08),
      green=material('Cristae | jade',(.055,.38,.2),.17,.3,.07,noise=.1),
      lime=material('Matrix | celadon',(.49,.68,.3),.05,.4),
      teal=material('Protein | lagoon',(.03,.49,.55),.3,.26,noise=.12),
      cyan=material('Signal | cyan',(.04,.68,.85),.25,.25,emission=.3),
      white=material('Ivory',(.85,.88,.8),.1,.34),
      red=material('Blood | oxygenated crimson',(.53,.014,.027),.05,.28,.14,noise=.09),
      deoxy=material('Blood | deoxygenated burgundy',(.16,.012,.028),.05,.29,.08),
      blue=material('Oxygen-poor flow convention',(.04,.19,.68),.18,.29),
      muscle=material('Myocardium | warm carmine',(.53,.055,.087),.09,.35,.14,noise=.25),
      wall=material('Myocardium cut | salmon',(.78,.2,.23),.04,.39,.12,noise=.16),
      vessel=material('Vessel wall',(.5,.1,.17),.07,.36,.08,noise=.12),
      glass=material('Laboratory glass',(.36,.69,.75),0,.1,transmission=.7),
      steel=material('Brushed steel',(.48,.55,.58),.85,.26),
      black=material('Equipment charcoal',(.024,.038,.046),.3,.3),
      phosph=material('Phosphate | gold',(.97,.52,.095),.35,.23),
      sugar=material('Deoxyribose | ivory',(.74,.8,.72),.2,.28),
      A=material('Adenine | turquoise',(.025,.58,.58),.18,.24),
      T=material('Thymine | coral',(.98,.22,.12),.18,.24),
      G=material('Guanine | gold',(.92,.62,.11),.18,.24),
      C=material('Cytosine | violet',(.4,.2,.8),.18,.24),
      rna=material('RNA | rose gold',(.94,.16,.39),.25,.26),
    )
