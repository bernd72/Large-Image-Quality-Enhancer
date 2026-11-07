"""Regression tests for 2:1 panoramas and ordinary JPEG camera aspect ratios.

These tests use a fake DPRNet interpreter and a fake denoiser. They do not
verify the quality of real AI model output or replace a Windows EXE test.
"""
from __future__ import annotations

import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

import numpy as np
from PIL import Image

# Source module may be adjacent to this tests folder, or in its source/ child.
BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / "source" if (BASE / "source").is_dir() else BASE
sys.path.insert(0, str(SOURCE))

from x5_dprnet import (compute_gain_field, export_full, transform_region,
                       extract_original_xmp_segments, insert_xmp)
from x5_denoise import denoise_full_export


class FakeInterpreter:
    def __init__(self, model_path, num_threads):
        self.input_tensor = None

    def get_input_details(self):
        return [{"shape": np.array((1, 3, 512, 512)),
                 "dtype": np.float32, "index": 0}]

    def allocate_tensors(self):
        pass

    def set_tensor(self, index, value):
        assert index == 0
        assert value.shape == (1, 3, 512, 512)
        self.input_tensor = value

    def invoke(self):
        pass

    def get_output_details(self):
        return [{"index": 1}]

    def get_tensor(self, index):
        assert index == 1
        return np.clip(self.input_tensor * 1.2, 0.0, 1.0)


class AspectRatioTests(unittest.TestCase):
    @staticmethod
    def progress(*args):
        pass

    @staticmethod
    def never_cancel():
        return False

    def test_gain_field_keeps_camera_photo_geometry(self):
        root = types.ModuleType("ai_edge_litert")
        module = types.ModuleType("ai_edge_litert.interpreter")
        module.Interpreter = FakeInterpreter
        root.interpreter = module
        cases = {
            (1200, 600): (512, 512),   # 2:1 equirectangular panorama
            (1200, 800): (341, 512),   # 3:2 landscape
            (800, 600): (384, 512),    # 4:3 landscape
            (600, 800): (512, 384),    # 3:4 portrait
            (500, 1000): (512, 256),   # 1:2 portrait
            (600, 600): (512, 512),    # 1:1 square
        }
        with mock.patch.dict(sys.modules, {
            "ai_edge_litert": root,
            "ai_edge_litert.interpreter": module,
        }):
            for dimensions, expected_hw in cases.items():
                with self.subTest(dimensions=dimensions):
                    img = Image.new("RGB", dimensions, (70, 80, 90))
                    ratio = compute_gain_field(img, Path("fake.tflite"),
                                               0.4, 1.8, self.progress)
                    self.assertEqual(ratio.shape, (*expected_hw, 3))
                    self.assertTrue(np.isfinite(ratio).all())

    def test_full_export_preserves_non_panorama_dimensions(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            for dims in ((121, 80), (80, 121), (120, 60)):
                with self.subTest(dims=dims):
                    source = folder / "input.jpg"
                    target = folder / "output.jpg"
                    Image.new("RGB", dims, (50, 80, 120)).save(source)
                    gain = np.ones((64, 64, 3), dtype=np.float32)
                    export_full(source, gain, target, 1.0,
                                self.progress, self.never_cancel)
                    with Image.open(target) as output:
                        self.assertEqual(output.size, dims)

    def test_scunet_wraps_only_panorama_horizontal_borders(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            seen = []

            def fake_denoise(data, session, strength, sharpen, progress,
                             cancelled, wrap_horizontal=False):
                seen.append(wrap_horizontal)
                return data

            with mock.patch("x5_denoise.denoise_rgb", side_effect=fake_denoise):
                for dims, expect_wrap in (((120, 80), False),
                                          ((80, 120), False),
                                          ((120, 60), True)):
                    with self.subTest(dims=dims):
                        seen.clear()
                        source = folder / "input.jpg"
                        target = folder / "output.jpg"
                        Image.new("RGB", dims, (50, 80, 120)).save(source)
                        gain = np.ones((64, 64, 3), dtype=np.float32)
                        denoise_full_export(
                            source, gain, target, 1.0, object(), 0.5, 0.0,
                            transform_region, extract_original_xmp_segments,
                            insert_xmp, folder, self.progress,
                            self.never_cancel)
                        with Image.open(target) as output:
                            self.assertEqual(output.size, dims)
                        self.assertTrue(seen)
                        self.assertEqual(set(seen), {expect_wrap})


if __name__ == "__main__":
    unittest.main()
