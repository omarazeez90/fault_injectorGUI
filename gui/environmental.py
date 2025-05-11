from core.config_editor import load_config
import cv2
import numpy as np
import time

config = load_config()

def _seed_random():
    np.random.seed((int(time.time() * 1_000_000) + np.random.randint(0, 9999)) % (2**32 - 1))


def blur(image, level):
    _seed_random()
    k = int(config.get("blur", {}).get(level, 7))
    k = max(3, k + (k % 2 == 0))  # Ensure odd kernel
    return cv2.GaussianBlur(image, (k, k), 0)

def brightness(image, level):
    _seed_random()
    factor = float(config.get("brightness", {}).get(level, 1.7)) + np.random.uniform(0.0, 0.2)
    return np.clip(image.astype(np.float32) * factor, 0, 255).astype(np.uint8)


def fog(image, level):
    _seed_random()
    alpha = float(config.get("fog", {}).get(level, 0.5)) + np.random.uniform(-0.05, 0.05)
    overlay = np.full_like(image, 200)
    return cv2.addWeighted(image, 1 - alpha, overlay, alpha, 0)


def glare(image, level):
    _seed_random()
    alpha = float(config.get("glare", {}).get(level, 0.4)) + np.random.uniform(-0.05, 0.05)
    overlay = image.copy()
    center = (overlay.shape[1] // 2, overlay.shape[0] // 2)
    radius = min(center) // 2
    mask = np.zeros_like(overlay, dtype=np.uint8)
    cv2.circle(mask, center, radius, (255, 255, 255), -1)
    return cv2.addWeighted(overlay, 1, mask, alpha, 0)


def raindrop(image, level):
    dummy = image.copy()
    cv2.putText(dummy, f"[TODO: Raindrop effect - {level}]", (30, dummy.shape[0] // 2),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    return dummy


def lens_dirt(image, level):
    dummy = image.copy()
    cv2.putText(dummy, f"[TODO: Lens Dirt effect - {level}]", (30, dummy.shape[0] // 2),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    return dummy
