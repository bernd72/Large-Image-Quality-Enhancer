"""Tests for the built-in GUI translations; no AI models or Tk display required."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'source'))
from x5_i18n import translate


class TranslationTests(unittest.TestCase):
    def test_german_is_default_and_unmodified(self):
        self.assertEqual(translate('de', '1. Original-JPG öffnen'), '1. Original-JPG öffnen')

    def test_main_button_english(self):
        self.assertEqual(translate('en', '1. Original-JPG öffnen'), '1. Open original JPEG')

    def test_batch_button_english(self):
        self.assertEqual(translate('en', 'STAPELVERARBEITUNG STARTEN'), 'START BATCH PROCESSING')

    def test_dynamic_progress_english(self):
        self.assertEqual(translate('en', 'Restzeit: ca. 45 Min.'), 'Time remaining: approx. 45 min.')

    def test_technical_error_preserves_dimensions(self):
        self.assertEqual(
            translate('en', 'Das Bild hat kein 2:1-Seitenverhältnis: 5000x3000'),
            'Image does not have a 2:1 aspect ratio: 5000x3000',
        )

    def test_english_selector_does_not_change_paths(self):
        src = 'KI-Bild in Originalauflösung gespeichert:\nC:\\Images\\photo.jpg'
        self.assertEqual(
            translate('en', src),
            'AI image saved at original resolution:\nC:\\Images\\photo.jpg',
        )


if __name__ == '__main__':
    unittest.main()
