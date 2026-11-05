import copy
from pathlib import Path
import shutil
import tempfile
import unittest
from build_platform_example import build
from extension_tools import ROOT, read_json, write_json, validate_platform
from retromao import check_source, pack


class PlatformModelsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name)/'example'
        shutil.copytree(ROOT/'examples/platform-presentation', self.source)
        build(self.source)

    def test_complete_platform_is_packaged_with_its_own_models_and_icons(self):
        from zipfile import ZipFile
        validate_platform(self.source)
        entry = pack(self.source, Path(self.temp.name)/'dist', 'demo-1.0.0')
        self.assertEqual('1.0.32', entry['minAppVersion'])
        with ZipFile(Path(self.temp.name)/'dist'/entry['fileName']) as archive:
            self.assertTrue({'models/box.glb', 'models/cartridge.glb', 'assets/logo.png', 'assets/pixel.png'} <= set(archive.namelist()))
            self.assertNotIn('retromao-package.json', archive.namelist())

    def test_corrupt_models_missing_files_and_static_artwork_are_rejected(self):
        file = self.source/'models/box.glb'
        original = file.read_bytes()
        for content in (b'not a model', original.replace(b'artwork_front', b'invalid_front'), original.replace(b'User artwork', b'Fake artwork')):
            file.write_bytes(content)
            with self.subTest(content=content[:24]), self.assertRaises(ValueError): validate_platform(self.source)
        file.unlink()
        with self.assertRaises(ValueError): validate_platform(self.source)

    def test_none_and_package_only_are_valid_but_cannot_carry_inconsistent_models(self):
        original = read_json(self.source/'platform.json')
        for packaging in (True, False):
            manifest = copy.deepcopy(original)
            manifest['platform'].update(medium='NONE', hasPackaging=packaging)
            manifest['models'].pop('gameMedia')
            if not packaging: manifest['models'] = {}
            write_json(self.source/'platform.json', manifest)
            validate_platform(self.source)
        manifest['models'] = original['models']
        write_json(self.source/'platform.json', manifest)
        with self.assertRaises(ValueError): validate_platform(self.source)

    def test_old_host_is_rejected_before_packing_format_three(self):
        path = self.source/'retromao-package.json'
        metadata = read_json(path); metadata['minAppVersion'] = '1.0.31'; write_json(path, metadata)
        with self.assertRaises(ValueError): check_source(self.source)


if __name__ == '__main__': unittest.main()
