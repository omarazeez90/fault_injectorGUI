import cv2
import numpy as np
import time
from core.config_editor import load_config

config = load_config()

def _seed_random():
    np.random.seed((int(time.time() * 1_000_000) + np.random.randint(0, 9999)) % (2**32 - 1))


def blackout(image, level):
    _seed_random()
    strength = float(config.get("blackout", {}).get(level, 1.0))
    return (image * (1 - strength)).astype(np.uint8)


def frame_drop(image, level):
    _seed_random()
    visibility = float(config.get("frame_drop", {}).get(level, 0.1))
    return (image * visibility).astype(np.uint8)


def dead_pixels(image, level):
    _seed_random()
    img = image.copy()
    density = float(config.get("dead_pixels", {}).get(level, 0.001))
    num = int(img.shape[0] * img.shape[1] * density)
    for _ in range(num):
        y = np.random.randint(0, img.shape[0])
        x = np.random.randint(0, img.shape[1])
        img[y, x] = [0, 0, 0]
    return img


def hot_pixels(image, level):
    _seed_random()
    img = image.copy()
    density = float(config.get("hot_pixels", {}).get(level, 0.001))
    num = int(img.shape[0] * img.shape[1] * density)
    for _ in range(num):
        y = np.random.randint(0, img.shape[0])
        x = np.random.randint(0, img.shape[1])
        img[y, x] = [255, 255, 255]
    return img


def line_dropout(image, level):
    _seed_random()
    img = image.copy()
    lines = int(config.get("line_dropout", {}).get(level, 10))
    for _ in range(lines):
        if np.random.rand() > 0.5:
            row = np.random.randint(0, img.shape[0])
            img[row:row+2, :] = 0
        else:
            col = np.random.randint(0, img.shape[1])
            img[:, col:col+2] = 0
    return img
