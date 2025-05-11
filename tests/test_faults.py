import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest
import numpy as np
from faults import apply_fault

class TestFaultFunctions(unittest.TestCase):
    def setUp(self):
        self.image = np.zeros((100, 100, 3), dtype=np.uint8)

    def test_all_faults_run(self):
        faults = [
            'flicker', 'color_shift', 'desaturation', 'rolling_shutter_skew', 'salt_pepper_noise',
            'blur', 'brightness', 'fog', 'glare',
            'blackout', 'frame_drop', 'dead_pixels', 'hot_pixels', 'line_dropout',
            'spatial_jitter', 'random_patch_noise', 'warping'
        ]
        for fault in faults:
            with self.subTest(fault=fault):
                out = apply_fault(self.image, fault, 'medium')
                self.assertEqual(out.shape, self.image.shape)

if __name__ == '__main__':
    unittest.main()
