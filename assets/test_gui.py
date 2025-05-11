import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest
import tkinter as tk
from gui.interface import FaultInjectorApp
class TestGUIInitialization(unittest.TestCase):
    def test_gui_loads(self):
        root = tk.Tk()
        app = FaultInjectorApp(root)
        self.assertIsNotNone(app)
        root.destroy()

if __name__ == '__main__':
    unittest.main()
