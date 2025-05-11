
import json
from pathlib import Path

CONFIG_PATH = Path("fault_level_config.json")

DEFAULTS = {
    "flicker": {"low": 8, "medium": 20, "extreme": 32},
    "blur": {"low": 3, "medium": 7, "extreme": 13},
    "brightness": {"low": 1.3, "medium": 1.7, "extreme": 2.2},
    "fog": {"low": 0.3, "medium": 0.5, "extreme": 0.7},
    "glare": {"low": 0.2, "medium": 0.4, "extreme": 0.6},
    "color_shift": {"low": 10, "medium": 30, "extreme": 60},
    "salt_pepper_noise": {"low": 0.002, "medium": 0.008, "extreme": 0.02},
    "rolling_shutter_skew": {"low": 5, "medium": 20, "extreme": 50},
    "desaturation": {"low": 0.5, "medium": 0.7, "extreme": 1.0},"resize_width": 320,
    "resize_height": 240,
}

def load_config():
    try:
        with CONFIG_PATH.open("r") as f:
            return json.load(f)
    except Exception:
        return DEFAULTS.copy()

def save_config(data):
    with CONFIG_PATH.open("w") as f:
        json.dump(data, f, indent=4)

def reset_to_defaults():
    save_config(DEFAULTS.copy())
