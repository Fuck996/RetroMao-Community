import hashlib
from io import BytesIO
import json
from pathlib import Path
import shutil
import struct
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

from PIL import Image

from build_msx_models import build
from extension_tools import ROOT, validate_platform
from retromao import pack


def model_content(path):
    glb = path.read_bytes()
    json_size = struct.unpack_from('<I', glb, 12)[0]
    json_end = 20 + json_size
    document = json.loads(glb[20:json_end])
    binary = memoryview(glb)[json_end + 8:]
    image_views = {image['bufferView'] for image in document['images']}
    contents = []
    # PNG compression changes the BIN size and subsequent view offsets.
    del document['buffers'][0]['byteLength']
    for index, view in enumerate(document['bufferViews']):
        offset = view.pop('byteOffset', 0)
        data = binary[offset:offset + view['byteLength']]
        if index in image_views:
            del view['byteLength']
            with Image.open(BytesIO(data)) as image:
                pixels = hashlib.sha256(image.tobytes()).hexdigest()
                contents.append((image.format, image.mode, image.size, image.info, pixels))
        else:
            contents.append(hashlib.sha256(data).hexdigest())
    return document, contents


class MsxPlatformTest(unittest.TestCase):
    def assert_model_matches(self, expected, actual):
        expected_document, expected_views = model_content(expected)
        actual_document, actual_views = model_content(actual)
        self.assertTrue(expected_document == actual_document, f'{actual.name}: glTF structure changed')
        for index, (expected_view, actual_view) in enumerate(zip(expected_views, actual_views, strict=True)):
            self.assertEqual(expected_view, actual_view, f'{actual.name}: bufferView {index} changed')

    def test_msx_has_real_models_licensed_icons_and_stable_identity_in_one_installable_package(self):
        source = ROOT / 'examples/msx'
        manifest = validate_platform(source)
        self.assertEqual('msx', manifest['platform']['id'])
        self.assertTrue(manifest['tintLogo'])
        self.assertEqual('CARTRIDGE', manifest['models']['gameMedia']['kind'])
        models = sorted(path.relative_to(source).as_posix() for path in (source / 'models').glob('*.glb'))
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'pack'
            shutil.copytree(source, target)
            build(target)
            self.assertEqual(models, sorted(path.relative_to(target).as_posix()
                                            for path in (target / 'models').glob('*.glb')))
            dist = Path(directory) / 'dist'
            entry = pack(target, dist, 'msx-1.1.0')
            package = dist / entry['fileName']
            self.assertEqual(entry['sizeBytes'], package.stat().st_size)
            self.assertEqual(entry['sha256'], hashlib.sha256(package.read_bytes()).hexdigest())
            with ZipFile(package) as archive:
                self.assertTrue({'models/msx_box_jp.glb', 'models/msx_cartridge_jp.glb',
                                 'licenses/platform-pixels-cc-by-4.0.txt'} <= set(archive.namelist()))
                for model in models:
                    self.assert_model_matches(source / model, target / model)
                    self.assertEqual(hashlib.sha256((target / model).read_bytes()).digest(),
                                     hashlib.sha256(archive.read(model)).digest(), model)
            self.assertEqual('1.0.32', entry['minAppVersion'])
        for name, expected in [('logo.png', '49da8dbc396199ede0e604395d55bd0add7b7c92'),
                               ('pixel.png', 'f855b158aa6cc6c418ca00980880394a00213da1')]:
            data = (source / 'assets' / name).read_bytes()
            self.assertEqual(expected, hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest())

    def test_model_comparison_accepts_png_recompression_and_detects_pixel_changes(self):
        original = ROOT / 'examples/msx/models/msx_box_jp.glb'
        save = Image.Image.save

        def save_without_compression(image, fp, format=None, **params):
            save(image, fp, format, **params, compress_level=0)

        def save_with_changed_pixel(image, fp, format=None, **params):
            image.putpixel((0, 0), (0, 0, 0))
            save_without_compression(image, fp, format, **params)

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            rebuilt = target / 'models' / original.name
            with patch.object(Image.Image, 'save', save_without_compression):
                build(target)
            self.assertNotEqual(hashlib.sha256(original.read_bytes()).digest(),
                                hashlib.sha256(rebuilt.read_bytes()).digest())
            self.assert_model_matches(original, rebuilt)

            with patch.object(Image.Image, 'save', save_with_changed_pixel):
                build(target)
            with self.assertRaisesRegex(AssertionError, 'bufferView 0 changed'):
                self.assert_model_matches(original, rebuilt)


if __name__ == '__main__':
    unittest.main()
