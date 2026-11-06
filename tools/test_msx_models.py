from pathlib import Path
import hashlib
import json
import shutil
import tempfile
import unittest
from zipfile import ZipFile

from extension_tools import ROOT, validate_platform
from build_msx_models import build
from retromao import pack


class MsxPlatformTest(unittest.TestCase):
    def test_msx_has_real_models_licensed_icons_and_stable_identity_in_one_installable_package(self):
        source=ROOT/'examples/msx'
        manifest=validate_platform(source)
        self.assertEqual('msx',manifest['platform']['id'])
        self.assertTrue(manifest['tintLogo'])
        self.assertEqual('CARTRIDGE',manifest['models']['gameMedia']['kind'])
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'pack'; shutil.copytree(source,target)
            original={path.name:path.read_bytes() for path in (target/'models').glob('*.glb')}
            build(target)
            self.assertEqual(original,{path.name:path.read_bytes() for path in (target/'models').glob('*.glb')})
            entry=pack(target,Path(directory)/'dist','msx-1.1.0')
            with ZipFile(Path(directory)/'dist'/entry['fileName']) as archive:
                self.assertTrue({'models/msx_box_jp.glb','models/msx_cartridge_jp.glb','licenses/platform-pixels-cc-by-4.0.txt'} <= set(archive.namelist()))
            self.assertEqual('1.0.32',entry['minAppVersion'])
        for name,expected in [('logo.png','49da8dbc396199ede0e604395d55bd0add7b7c92'),('pixel.png','f855b158aa6cc6c418ca00980880394a00213da1')]:
            data=(source/'assets'/name).read_bytes()
            self.assertEqual(expected,hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest())


if __name__=='__main__': unittest.main()
