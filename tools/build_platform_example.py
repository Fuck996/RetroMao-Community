"""Build original fictional-console artwork for the format-3 tutorial, not a real product replica."""

import json
from pathlib import Path
import struct
from io import BytesIO
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]


def model(width, height, depth):
    vertices, normals, uvs = [], [], []
    w, h, d = width / 2, height / 2, depth / 2
    faces = [([(-w,-h,d),(w,-h,d),(w,h,d),(-w,h,d)], (0,0,1)),
             ([(w,-h,-d),(-w,-h,-d),(-w,h,-d),(w,h,-d)], (0,0,-1)),
             ([(w,-h,d),(w,-h,-d),(w,h,-d),(w,h,d)], (1,0,0)),
             ([(-w,-h,-d),(-w,-h,d),(-w,h,d),(-w,h,-d)], (-1,0,0)),
             ([(-w,h,d),(w,h,d),(w,h,-d),(-w,h,-d)], (0,1,0)),
             ([(-w,-h,-d),(w,-h,-d),(w,-h,d),(-w,-h,d)], (0,-1,0))]
    for points, normal in faces:
        for i in (0,1,2,0,2,3):
            vertices.extend(points[i]); normals.extend(normal); uvs.extend(((0,1),(1,1),(1,0),(0,0))[i])
    points = [(-w*.88,-h*.88,d+.001),(w*.88,-h*.88,d+.001),(w*.88,h*.88,d+.001),(-w*.88,h*.88,d+.001)]
    for i in (0,1,2,0,2,3):
        vertices.extend(points[i]); normals.extend((0,0,1)); uvs.extend(((0,1),(1,1),(1,0),(0,0))[i])
    arrays = [(vertices,3,'VEC3'), (normals,3,'VEC3'), (uvs,2,'VEC2')]
    binary, views, accessors = bytearray(), [], []
    for values, components, kind in arrays:
        offset = len(binary); binary.extend(struct.pack('<'+'f'*len(values), *values))
        views.append({'buffer':0,'byteOffset':offset,'byteLength':len(binary)-offset,'target':34962})
        for start, count in [(0,36),(36,6)]:
            accessor = {'bufferView':len(views)-1,'byteOffset':start*components*4,'componentType':5126,'count':count,'type':kind}
            if kind == 'VEC3' and len(views) == 1:
                rows = [values[j:j+3] for j in range(start*3,(start+count)*3,3)]
                accessor.update(min=[min(row[i] for row in rows) for i in range(3)], max=[max(row[i] for row in rows) for i in range(3)])
            accessors.append(accessor)
    image = BytesIO(); Image.new('RGBA', (1,1), 'white').save(image, format='PNG')
    offset = len(binary); binary.extend(image.getvalue())
    views.append({'buffer':0,'byteOffset':offset,'byteLength':len(binary)-offset})
    document = {'asset':{'version':'2.0','generator':'RetroMao original tutorial geometry'},'scene':0,
        'scenes':[{'nodes':[0,1]}], 'nodes':[{'name':'shell','mesh':0},{'name':'artwork_front','mesh':1}],
        'meshes':[{'primitives':[{'attributes':{'POSITION':0,'NORMAL':2,'TEXCOORD_0':4},'material':0}]},
                  {'primitives':[{'attributes':{'POSITION':1,'NORMAL':3,'TEXCOORD_0':5},'material':1}]}],
        'materials':[{'name':'Tutorial shell','pbrMetallicRoughness':{'baseColorFactor':[.12,.18,.24,1],'metallicFactor':0,'roughnessFactor':.45}},
                     {'name':'User artwork','pbrMetallicRoughness':{'baseColorFactor':[1,1,1,1],'baseColorTexture':{'index':0},'metallicFactor':0,'roughnessFactor':.7}}],
        'images':[{'bufferView':3,'mimeType':'image/png'}],'textures':[{'source':0}],
        'buffers':[{'byteLength':len(binary)}],'bufferViews':views,'accessors':accessors}
    text = json.dumps(document, separators=(',',':')).encode(); text += b' ' * (-len(text) % 4)
    binary += b'\0' * (-len(binary) % 4)
    return struct.pack('<III',0x46546C67,2,28+len(text)+len(binary)) + struct.pack('<II',len(text),0x4E4F534A)+text+struct.pack('<II',len(binary),0x004E4942)+binary


def build(destination):
    destination = Path(destination)
    (destination/'models').mkdir(parents=True, exist_ok=True)
    (destination/'assets').mkdir(exist_ok=True)
    (destination/'models/box.glb').write_bytes(model(1,1.4,.22))
    (destination/'models/cartridge.glb').write_bytes(model(1,.8,.16))
    for role, size in [('logo',(480,160)),('pixel',(128,128))]:
        image = Image.new('RGBA',size,(0,0,0,0)); draw = ImageDraw.Draw(image)
        w,h=size; draw.rounded_rectangle((w*.08,h*.15,w*.92,h*.85),radius=12,fill='#253D50')
        draw.rectangle((w*.22,h*.3,w*.6,h*.65),fill='#6DE5BA')
        draw.ellipse((w*.72,h*.4,w*.82,h*.6),fill='#FADE76')
        image.save(destination/f'assets/{role}.png')


if __name__ == '__main__':
    build(ROOT/'examples/platform-presentation')
