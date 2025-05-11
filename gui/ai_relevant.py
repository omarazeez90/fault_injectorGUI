import cv2
import numpy as np
import time
from core.config_editor import load_config

config = load_config()

def _seed_random():
    np.random.seed((int(time.time() * 1_000_000) + np.random.randint(0, 9999)) % (2**32 - 1))


def temporal_lag(image, level):
    dummy = image.copy()
    cv2.putText(dummy, f"[TODO: Temporal Lag - {level}]", (30, dummy.shape[0] // 2),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    return dummy


def spatial_jitter(image, level):
    _seed_random()
    jitter = int(config.get("spatial_jitter", {}).get(level, 3))
    img = image.copy()
    jittered = np.zeros_like(img)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            dy = np.clip(y + np.random.randint(-jitter, jitter + 1), 0, img.shape[0] - 1)
            dx = np.clip(x + np.random.randint(-jitter, jitter + 1), 0, img.shape[1] - 1)
            jittered[y, x] = img[dy, dx]
    return jittered


def random_patch_noise(image, level):
    _seed_random()
    count = int(config.get("random_patch_noise", {}).get(level, 5))
    img = image.copy()
    h, w = img.shape[:2]
    for _ in range(count):
        ph = np.random.randint(10, 30)
        pw = np.random.randint(10, 30)
        y = np.random.randint(0, h - ph)
        x = np.random.randint(0, w - pw)
        patch = np.random.randint(0, 256, (ph, pw, 3), dtype=np.uint8)
        img[y:y+ph, x:x+pw] = patch
    return img


def warping(image, level):
    _seed_random()
    factor = int(config.get("warping", {}).get(level, 15))
    h, w = image.shape[:2]
    src = np.float32([[0, 0], [w - 1, 0], [0, h - 1]])
    dst = np.float32([
        [np.random.randint(0, factor), np.random.randint(0, factor)],
        [w - 1 - np.random.randint(0, factor), np.random.randint(0, factor)],
        [np.random.randint(0, factor), h - 1 - np.random.randint(0, factor)]
    ])
    matrix = cv2.getAffineTransform(src, dst)
    return cv2.warpAffine(image, matrix, (w, h))
