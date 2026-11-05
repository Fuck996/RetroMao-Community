"""Platform model validation shared by check, pack and publish; no renderer or network."""

import json
import math
import struct


def validate_models(manifest):
    platform, models = manifest['platform'], manifest.get('models') or {}
    if manifest['schemaVersion'] < 3 and (manifest.get('models') is not None or
            not platform.get('hasPackaging', True) or platform.get('medium') == 'NONE'):
        raise ValueError('Models and physical availability require platform format 3')
    media = models.get('gameMedia', {'kind': 'NONE'})
    kind = platform.get('medium', 'CARTRIDGE')
    if not platform.get('hasPackaging', True) and any(models.get(key) for key in
            ('packaging', 'packagingVariantLabel', 'packagingVariants')):
        raise ValueError('A platform without packaging cannot declare packaging models')
    if media['kind'] not in ('NONE', kind):
        raise ValueError('Model medium differs from platform medium')
    if kind == 'NONE' and media['kind'] != 'NONE':
        raise ValueError('A platform without physical media cannot declare a medium model')
    if media['kind'] == 'NONE' and any(value is not None for key, value in media.items() if key != 'kind'):
        raise ValueError('NONE cannot carry a model, shell, label or artwork ratio')
    shell = media.get('shell')
    if shell and (not media.get('model') or media['kind'] in ('DISC', 'NONE') or shell['name'] == shell['translucentMaterial']):
        raise ValueError('Shell customization requires a modeled non-disc medium and distinct materials')
    def finite(value):
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError('Model numbers must be finite')
        if isinstance(value, dict):
            for item in value.values(): finite(item)
        elif isinstance(value, list):
            for item in value: finite(item)
    finite(models)
    result = {}
    if models.get('packaging'): result[models['packaging']] = None
    for variant in models.get('packagingVariants', {}).values(): result[variant['model']] = None
    if media.get('model'): result[media['model']] = shell
    return result


def validate_glb(path, shell=None):
    """Read headers/JSON only, matching ThemePackageChecks and PlatformModelChecks."""
    size = path.stat().st_size
    with path.open('rb') as stream:
        def read(offset, length):
            stream.seek(offset)
            result = stream.read(length)
            if len(result) != length: raise ValueError('Truncated GLB')
            return result
        if size < 20 or struct.unpack('<III', read(0, 12)) != (0x46546C67, 2, size):
            raise ValueError('Require a complete binary glTF 2.0 model')
        offset, index, document, bin_size = 12, 0, None, -1
        while offset < size:
            if index >= 64 or offset + 8 > size: raise ValueError('Invalid GLB chunk header')
            length, kind = struct.unpack('<II', read(offset, 8))
            if offset + 8 + length > size: raise ValueError('GLB chunk exceeds file')
            if index == 0:
                if kind != 0x4E4F534A or not 0 < length <= 4 * 1024 * 1024: raise ValueError('Invalid GLB JSON chunk')
                text = read(offset + 8, length).decode('utf-8').rstrip(' \0')
                depth, string, escaped = 0, False, False
                for char in text:
                    if string:
                        if escaped: escaped = False
                        elif char == '\\': escaped = True
                        elif char == '"': string = False
                    elif char == '"': string = True
                    elif char in '{[':
                        depth += 1
                        if depth > 64: raise ValueError('GLB JSON nesting exceeds 64')
                    elif char in '}]': depth -= 1
                try: document = json.loads(text)
                except (ValueError, RecursionError) as error: raise ValueError('Invalid GLB JSON') from error
                if not isinstance(document, dict): raise ValueError('GLB JSON must be an object')
            elif index == 1 and kind == 0x004E4942: bin_size = length
            elif kind in (0x4E4F534A, 0x004E4942): raise ValueError('Duplicate GLB JSON or BIN chunk')
            offset += 8 + length
            index += 1
        def rows(key, limit):
            values = document.get(key, [])
            if not isinstance(values, list) or len(values) > limit or any(not isinstance(row, dict) for row in values):
                raise ValueError(f'Invalid GLB {key}')
            return values
        for key, limit in [('nodes', 8192), ('meshes', 2048), ('materials', 1024), ('textures', 512), ('samplers', 512),
                ('animations', 256), ('skins', 256), ('cameras', 64), ('scenes', 64)]: rows(key, limit)
        buffers = rows('buffers', 1)
        if any('uri' in row for row in buffers): raise ValueError('GLB buffers must be embedded')
        buffer_size = buffers[0].get('byteLength') if buffers else None
        if buffer_size is not None and not 0 <= buffer_size <= bin_size: raise ValueError('GLB buffer exceeds BIN')
        views = rows('bufferViews', 16384)
        for view in views:
            start, length, stride = view.get('byteOffset', 0), view.get('byteLength', 0), view.get('byteStride')
            if view.get('buffer') != 0 or buffer_size is None or not 0 <= start <= buffer_size or not 0 < length <= buffer_size - start:
                raise ValueError('GLB bufferView exceeds buffer')
            if stride is not None and not 4 <= stride <= 252: raise ValueError('Invalid GLB stride')
        widths = {5120: 1, 5121: 1, 5122: 2, 5123: 2, 5125: 4, 5126: 4}
        counts = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT2': 4, 'MAT3': 9, 'MAT4': 16}
        for accessor in rows('accessors', 32768):
            count, width, components = accessor.get('count', 0), widths.get(accessor.get('componentType')), counts.get(accessor.get('type'))
            if not 1 <= count <= 16777216 or not width or not components or 'sparse' in accessor: raise ValueError('Invalid GLB accessor')
            index = accessor.get('bufferView')
            if index is None: continue
            if not isinstance(index, int) or not 0 <= index < len(views): raise ValueError('Missing GLB bufferView')
            view, start, element = views[index], accessor.get('byteOffset', 0), width * components
            if not 0 <= start <= view['byteLength'] or (view.get('byteStride', element) * (count - 1) + element) > view['byteLength'] - start:
                raise ValueError('GLB accessor exceeds bufferView')
        for image in rows('images', 512):
            if 'uri' in image or not isinstance(image.get('bufferView'), int) or not 0 <= image['bufferView'] < len(views):
                raise ValueError('GLB images must be embedded')
        if document.get('asset', {}).get('version') != '2.0': raise ValueError('Require glTF asset version 2.0')
        meshes, materials = rows('meshes', 2048), rows('materials', 1024)
        artwork = []
        for node in rows('nodes', 8192):
            if not node.get('name', '').startswith('artwork_'): continue
            index = node.get('mesh', -1)
            if not isinstance(index, int) or not 0 <= index < len(meshes): continue
            for primitive in meshes[index].get('primitives', []):
                index = primitive.get('material', -1)
                if isinstance(index, int) and 0 <= index < len(materials) and materials[index].get('name', '').startswith('User artwork'):
                    artwork.append(primitive)
        if not artwork or any('TEXCOORD_0' not in item.get('attributes', {}) for item in artwork):
            raise ValueError('Require artwork_ nodes, User artwork materials and TEXCOORD_0 UVs')
        for primitive in artwork:
            texture = materials[primitive['material']].get('pbrMetallicRoughness', {}).get('baseColorTexture', {})
            if 'index' not in texture or texture.get('texCoord', 0) != 0:
                raise ValueError('User artwork requires a base-color texture using UV set 0')
        if shell:
            names = {row.get('name') for row in materials}
            variants = {row.get('name') for row in document.get('extensions', {}).get('KHR_materials_variants', {}).get('variants', [])}
            if not {shell['name'], shell['translucentMaterial']} <= names or not {'shell-opaque', 'shell-translucent'} <= variants:
                raise ValueError('Missing shell materials or variants')
