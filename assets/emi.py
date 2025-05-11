from core.config_editor import load_config
import cv2
import numpy as np
import time

config = load_config()

def _seed_random():
    np.random.seed((int(time.time() * 1_000_000) + np.random.randint(0, 9999)) % (2**32 - 1))


def flicker(image, level):
    _seed_random()
    num_stripes = int(config.get("flicker", {}).get(level, 20))
    flicker_img = image.copy()
    rows, cols, _ = flicker_img.shape
    for _ in range(num_stripes):
        orientation = np.random.choice(['horizontal', 'vertical'])
        alpha = np.random.uniform(0.2, 0.6)
        thickness = np.random.randint(3, 10)
        start = np.random.randint(0, rows if orientation == 'horizontal' else cols)
        if orientation == 'horizontal':
            flicker_img[start:start+thickness, :] = np.clip(flicker_img[start:start+thickness, :].astype(np.float32) * alpha, 1, 255).astype(np.uint8)
        else:
            flicker_img[:, start:start+thickness] = np.clip(flicker_img[:, start:start+thickness].astype(np.float32) * alpha, 1, 255).astype(np.uint8)
    return flicker_img


def color_shift(image, level):
    _seed_random()
    base_shift = int(config.get("color_shift", {}).get(level, 20))
    r_shift = base_shift + np.random.randint(-5, 5)
    b_shift = -base_shift + np.random.randint(-5, 5)
    b, g, r = cv2.split(image)
    r = np.clip(r.astype(np.int16) + r_shift, 0, 255).astype(np.uint8)
    b = np.clip(b.astype(np.int16) + b_shift, 0, 255).astype(np.uint8)
    return cv2.merge((b, g, r))


def desaturation(image, level):
    _seed_random()
    alpha = config.get("desaturation", {}).get(level, 0.7) + np.random.uniform(-0.05, 0.05)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray_rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    return cv2.addWeighted(image, 1 - alpha, gray_rgb, alpha, 0)


def rolling_shutter_skew(image, level):
    _seed_random()
    max_shift = int(config.get("rolling_shutter_skew", {}).get(level, 20))
    rows, cols, _ = image.shape
    skew_img = np.zeros_like(image)
    for i in range(rows):
        shift = int((np.sin(i / rows * np.pi * 2) + 1) / 2 * max_shift + np.random.randint(-2, 3))
        if shift >= 0:
            skew_img[i, shift:] = image[i, :cols - shift]
        else:
            skew_img[i, :cols + shift] = image[i, -shift:]
    return skew_img


def salt_pepper_noise(image, level):
    _seed_random()
    density = float(config.get("salt_pepper_noise", {}).get(level, 0.01))
    noisy = image.copy()
    num_salt = int(density * image.size * 0.5)
    num_pepper = int(density * image.size * 0.5)
    coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape[:2]]
    noisy[coords[0], coords[1], :] = 255
    coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape[:2]]
    noisy[coords[0], coords[1], :] = 0
    return noisy
