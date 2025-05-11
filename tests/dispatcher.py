from faults.emi import flicker, color_shift, desaturation, rolling_shutter_skew, salt_pepper_noise
from faults.environmental import blur, brightness, fog, glare, raindrop, lens_dirt
from faults.hardware import blackout, frame_drop, dead_pixels, hot_pixels, line_dropout
from faults.ai_relevant import temporal_lag, spatial_jitter, random_patch_noise, warping

FAULT_FUNCTIONS = {
    # EMI
    "flicker": flicker,
    "color_shift": color_shift,
    "desaturation": desaturation,
    "rolling_shutter_skew": rolling_shutter_skew,
    "salt_pepper_noise": salt_pepper_noise,

    # Environmental
    "blur": blur,
    "brightness": brightness,
    "fog": fog,
    "glare": glare,
    "raindrop": raindrop,
    "lens_dirt": lens_dirt,

    # Hardware
    "blackout": blackout,
    "frame_drop": frame_drop,
    "dead_pixels": dead_pixels,
    "hot_pixels": hot_pixels,
    "line_dropout": line_dropout,

    # AI-Relevant
    "temporal_lag": temporal_lag,
    "spatial_jitter": spatial_jitter,
    "random_patch_noise": random_patch_noise,
    "warping": warping,
}


def apply_fault(image_rgb, fault_name, level):
    if fault_name not in FAULT_FUNCTIONS:
        raise ValueError(f"Fault '{fault_name}' is not implemented.")
    return FAULT_FUNCTIONS[fault_name](image_rgb, level)
