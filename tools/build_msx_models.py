"""Build the Japanese MSX cartridge and closed Konami-style case from documented references.

Geometry is original. Dimensions/reference photographs and artwork credits are in examples/msx/README.md.
Outputs use the host's existing glTF artwork, shell-variant and PBR contracts.
"""

import json
from io import BytesIO
from math import atan2, cos, pi, sin, sqrt
from pathlib import Path
from random import Random
import struct
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def outline(w, h, radius, steps=8):
    return [(cx + radius*cos(angle), cy + radius*sin(angle))
        for cx,cy,start in [(w/2-radius,-h/2+radius,-pi/2),(w/2-radius,h/2-radius,0),
                            (-w/2+radius,h/2-radius,pi/2),(-w/2+radius,-h/2+radius,pi)]
        for angle in [start + j*pi/2/steps for j in range(steps+1)]]


class Model:
    def __init__(self):
        self.binary=bytearray()
        self.doc={'asset':{'version':'2.0','generator':'RetroMao MSX model authoring'},'scene':0,
            'scenes':[{'nodes':[]}],'nodes':[],'meshes':[],'materials':[], 'buffers':[{}],
            'bufferViews':[],'accessors':[],'images':[],'textures':[],
            'samplers':[{'magFilter':9729,'minFilter':9987,'wrapS':10497,'wrapT':10497}]}
        white=self.image(Image.new('RGB',(1,1),'white'))
        rng=Random(1983); normal=Image.new('RGB',(128,128)); normal.putdata([
            (128+rng.randrange(-8,9),128+rng.randrange(-8,9),255) for _ in range(128*128)])
        self.normal=self.image(normal)
        self.art=self.material('User artwork',(.95,.95,.95),.66)
        pbr=self.doc['materials'][self.art]['pbrMetallicRoughness']; pbr['baseColorTexture']={'index':white}
        self.doc['materials'][self.art]['extensions']={'KHR_materials_clearcoat':{'clearcoatFactor':.36,'clearcoatRoughnessFactor':.22}}
        self.doc['extensionsUsed']=['KHR_materials_clearcoat']

    def view(self,data):
        self.binary.extend(b'\0'*(-len(self.binary)%4)); index=len(self.doc['bufferViews'])
        self.doc['bufferViews'].append({'buffer':0,'byteOffset':len(self.binary),'byteLength':len(data)})
        self.binary.extend(data); return index

    def image(self,image):
        data=BytesIO(); image.save(data,format='PNG')
        image_index=len(self.doc['images']); self.doc['images'].append({'bufferView':self.view(data.getvalue()),'mimeType':'image/png'})
        self.doc['textures'].append({'source':image_index,'sampler':0}); return len(self.doc['textures'])-1

    def material(self,name,color,roughness=.45,metallic=0,grain=False):
        value={'name':name,'pbrMetallicRoughness':{'baseColorFactor':[*color,1], 'roughnessFactor':roughness,'metallicFactor':metallic}}
        if grain: value['normalTexture']={'index':self.normal,'scale':.2}
        self.doc['materials'].append(value); return len(self.doc['materials'])-1

    def shell(self):
        self.opaque=self.material('MSX shell',(.021,.024,.028),grain=True)
        self.translucent=self.material('MSX translucent shell',(.021,.024,.028),.08,grain=True)
        self.doc['materials'][self.translucent]['extensions']={
            'KHR_materials_transmission':{'transmissionFactor':.72},
            'KHR_materials_volume':{'thicknessFactor':.0013,'attenuationDistance':.05,'attenuationColor':[.5,.55,.6]},
            'KHR_materials_ior':{'ior':1.5}}
        self.doc['extensionsUsed'] += ['KHR_materials_transmission','KHR_materials_volume','KHR_materials_ior','KHR_materials_variants']
        self.doc['extensions']={'KHR_materials_variants':{'variants':[{'name':'shell-opaque'},{'name':'shell-translucent'}]}}
        return self.opaque

    def accessor(self,rows,kind,indices=False):
        components={'VEC3':3,'VEC2':2,'SCALAR':1}[kind]; flat=[v for row in rows for v in row]
        if indices: payload=struct.pack('<'+'I'*len(flat),*flat)
        else: payload=struct.pack('<'+'f'*len(flat),*flat)
        item={'bufferView':self.view(payload),'componentType':5125 if indices else 5126,'count':len(rows),'type':kind}
        if kind=='VEC3': item.update(min=[min(row[i] for row in rows) for i in range(components)],max=[max(row[i] for row in rows) for i in range(components)])
        self.doc['accessors'].append(item); return len(self.doc['accessors'])-1

    def mesh(self,name,points,normals,uvs,triangles,material):
        primitive={'attributes':{'POSITION':self.accessor([[v*.001 for v in p] for p in points],'VEC3'),
            'NORMAL':self.accessor(normals,'VEC3'),'TEXCOORD_0':self.accessor(uvs,'VEC2')},
            'indices':self.accessor([[v] for triangle in triangles for v in triangle],'SCALAR',True),'material':material}
        if material==getattr(self,'opaque',None):
            primitive['extensions']={'KHR_materials_variants':{'mappings':[
                {'material':self.opaque,'variants':[0]},{'material':self.translucent,'variants':[1]}]}}
        index=len(self.doc['meshes']); self.doc['meshes'].append({'name':name,'primitives':[primitive]})
        self.doc['scenes'][0]['nodes'].append(len(self.doc['nodes'])); self.doc['nodes'].append({'name':name,'mesh':index})

    def block(self,name,w,h,d,center,mat,r=1,bevel=.4):
        b=min(bevel,d*.48,r*.95); levels=[]
        for angle in [0,pi/6,pi/3,pi/2]:
            levels.append((-d/2+b*(1-cos(angle)), b*(1-sin(angle)),sin(angle),-cos(angle)))
        for angle in [pi/2,pi/3,pi/6,0]:
            levels.append((d/2-b*(1-cos(angle)), b*(1-sin(angle)),sin(angle),cos(angle)))
        points=[]; normals=[]; uvs=[]; faces=[]
        for z,inset,xy,nz in levels:
            ring=outline(w-2*inset,h-2*inset,max(.01,r-inset)); count=len(ring)
            for i,(x,y) in enumerate(ring):
                a,c=ring[(i-1)%count],ring[(i+1)%count]; nx,ny=c[1]-a[1],a[0]-c[0]; length=sqrt(nx*nx+ny*ny)
                points.append((x+center[0],y+center[1],z+center[2])); normals.append((nx/length*xy,ny/length*xy,nz)); uvs.append((x/w+.5,y/h+.5))
        for layer in range(len(levels)-1):
            for i in range(count):
                a=layer*count+i; c=layer*count+(i+1)%count; faces.extend([(a,c,c+count),(a,c+count,a+count)])
        for layer,nz in [(0,-1),(len(levels)-1,1)]:
            middle=len(points); points.append((center[0],center[1],levels[layer][0]+center[2])); normals.append((0,0,nz)); uvs.append((.5,.5))
            for i in range(count):
                a,c=layer*count+i,layer*count+(i+1)%count
                faces.append((middle,a,c) if nz==1 else (middle,c,a))
        self.mesh(name,points,normals,uvs,faces,mat)

    def artwork(self,w,h,center,r=1):
        ring=outline(w,h,r); p=[center]+[(x+center[0],y+center[1],center[2]) for x,y in ring]
        self.mesh('artwork_front',p,[(0,0,1)]*len(p),[(.5,.5)]+[(x/w+.5,y/h+.5) for x,y in ring],
            [(0,i+1,(i+1)%len(ring)+1) for i in range(len(ring))],self.art)

    def ring(self,name,radius,width,center,mat):
        points=[]; normals=[]; uvs=[]; faces=[]; n=48
        for r,z in [(radius,center[2]),(radius-width,center[2]-.28)]:
            for i in range(n):
                a=i*2*pi/n; points.append((center[0]+r*cos(a),center[1]+r*sin(a),z)); normals.append((0,0,1)); uvs.append((.5+cos(a)*.5,.5+sin(a)*.5))
        for i in range(n): j=(i+1)%n; faces.extend([(i,j,j+n),(i,j+n,i+n)])
        self.mesh(name,points,normals,uvs,faces,mat)

    def save(self,path):
        self.doc['buffers'][0]['byteLength']=len(self.binary)
        data=json.dumps(self.doc,separators=(',',':')).encode(); data+=b' '*(-len(data)%4)
        self.binary+=b'\0'*(-len(self.binary)%4)
        result=struct.pack('<III',0x46546C67,2,28+len(data)+len(self.binary))+struct.pack('<II',len(data),0x4E4F534A)+data+struct.pack('<II',len(self.binary),0x004E4942)+self.binary
        path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(result)


def cartridge(path):
    m=Model(); shell=m.shell(); black=m.material('Connector shadow',(.004,.005,.006),.8)
    board=m.material('Cartridge PCB',(.025,.08,.045),.6); gold=m.material('Gold edge contacts',(.66,.43,.10),.26,.85)
    # The 109 x 69.4 x 16.8 mm envelope follows Sony/ASCII MSX Technical Data Book p.31.
    m.block('shell_front',109,69.4,1.4,(0,0,7.7),shell,2.5,.45)
    m.block('shell_back',109,69.4,1.4,(0,0,-7.7),shell,2.5,.45)
    for x in [-53.7,53.7]: m.block('shell_side',1.6,67.4,14.2,(x,0,0),shell,.6,.3)
    m.block('shell_top',106,1.6,14.2,(0,33.9,0),shell,.6,.3)
    for x in [-45.5,45.5]: m.block('shell_bottom_guide',15,2.3,14.2,(x,-33.2,0),shell,.6,.3)
    m.block('connector_mouth',75,7.8,.8,(0,-29.6,-1.0),black,.6,.15)
    m.block('board_connector',68,13,.8,(0,-27.2,0),board,.3,.12)
    for side in [-1,1]:
        for i in range(25): m.block('board_contact',1.48,6.2,.12,((i-12)*2.54,-30.0,side*.48),gold,.18,.04)
    m.block('front_label_recess',92,49,.25,(5.4,1.7,8.42),black,1.5,.08)
    m.artwork(89,46.5,(5.4,1.7,8.57),1.3)
    for y in [13,18,23]: m.block('front_grip_groove',9,.55,.2,(-47,y,8.48),black,.2,.05)
    m.ring('moulded_locator',2.7,.55,(-47,-20,8.48),shell)
    m.block('rear_moulding',84,48,.2,(0,0,-8.48),shell,1.8,.05)
    for y in [-26,26]: m.block('rear_seam',101,.35,.2,(0,y,-8.5),black,.1,.04)
    m.save(path)


def packaging(path):
    m=Model(); plastic=m.material('MSX Japanese black case',(.014,.017,.021),.43,grain=True)
    seam=m.material('Case parting seam',(.003,.004,.005),.68)
    # Konami Japanese clamshell proportions are taken from the documented RC754 package photographs.
    m.block('case_rear_tray',118,172,12,(0,0,-6),plastic,2.5,.65)
    m.block('case_front_lid',118,172,11.7,(0,0,6.15),plastic,2.5,.65)
    m.block('case_lid_seam',116.8,170.8,.28,(0,0,.12),seam,2,.06)
    m.artwork(112,166,(0,0,12.05),1.15)
    for y in [-67,-39,0,39,67]: m.block('case_spine_hinge',3.1,15,20,(-58.6,y,0),plastic,1,.4)
    for y in [-51,51]: m.block('case_latch',2.1,12,7.4,(58.7,y,1.8),plastic,.6,.22)
    m.block('case_rear_inset',108,162,.35,(0,0,-12.15),plastic,1.6,.08)
    for x in [-52,52]: m.block('case_rear_edge',.65,154,.28,(x,0,-12.25),plastic,.2,.05)
    m.save(path)


def build(destination):
    cartridge(destination/'models/msx_cartridge_jp.glb')
    packaging(destination/'models/msx_box_jp.glb')


if __name__=='__main__': build(ROOT/'examples/msx')
