"""Dependency-free German/English translation tests for Python v3.3."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from x5_i18n import translate


class TranslationTests(unittest.TestCase):
    def test_default_german_unchanged(self):
        self.assertEqual(translate('de', 'Modell herunterladen'), 'Modell herunterladen')

    def test_model_download_buttons(self):
        self.assertEqual(translate('en', 'Modell herunterladen'), 'Download model')
        self.assertEqual(translate('en', 'SCUNet herunterladen'), 'Download SCUNet')

    def test_model_file_selection(self):
        self.assertEqual(
            translate('en', 'DPRNet_1024.tflite auswählen'),
            'Select DPRNet_1024.tflite')

    def test_model_download_progress(self):
        self.assertEqual(
            translate('en', 'KI-Modell herunterladen: 1.5 MB'),
            'Downloading AI model: 1.5 MB')

    def test_batch_button(self):
        self.assertEqual(
            translate('en', 'STAPELVERARBEITUNG STARTEN'),
            'START BATCH PROCESSING')

    def test_time_remaining(self):
        self.assertEqual(
            translate('en', 'Restzeit: ca. 45 Min.'),
            'Time remaining: approx. 45 min.')

    def test_status_with_filename(self):
        self.assertEqual(
            translate('en', 'Manuell hinzugefügtes KI-Modell: DPRNet_1024.tflite'),
            'Manually added AI model: DPRNet_1024.tflite')

    def test_unchanged_model_names(self):
        self.assertEqual(translate('en', 'scunet_color_real_psnr.onnx'),
                         'scunet_color_real_psnr.onnx')


if __name__ == '__main__':
    unittest.main()
