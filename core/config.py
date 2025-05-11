# Fault intensity levels
FAULT_LEVELS = ["low", "medium", "extreme"]

# Fault categories and mappings
FAULT_CATEGORIES = {
    "EMI": [
        "flicker",
        "color_shift",
        "desaturation",
        "rolling_shutter_skew",
        "salt_pepper_noise"
    ],
    "Environmental": [
        "blur",
        "brightness",
        "fog",
        "glare",
        "raindrop",
        "lens_dirt"
    ],
    "Hardware": [
        "blackout",
        "frame_drop",
        "dead_pixels",
        "hot_pixels",
        "line_dropout"
    ],
    "AI_Relevant": [
        "temporal_lag",
        "spatial_jitter",
        "random_patch_noise",
        "warping"
    ]
}

# Fault descriptions
FAULT_DESCRIPTIONS = {
    # EMI
    "flicker": "Simulates EMI-induced flickering lines and dimming",
    "color_shift": "Color processing distortion due to interference",
    "desaturation": "Signal degradation causing loss of saturation",
    "rolling_shutter_skew": "Row-wise distortion typical of CMOS sensors",
    "salt_pepper_noise": "Random black and white noise from EMI or ADC faults",

    # Environmental
    "blur": "Simulates motion or defocus blur",
    "brightness": "Overexposure or brightness shifts",
    "fog": "Reduced visibility due to haze",
    "glare": "High-intensity light artifacts",
    "raindrop": "Water droplets on lens (TODO)",
    "lens_dirt": "Static dirt on lens (TODO)",

    # Hardware
    "blackout": "Complete or partial frame loss",
    "frame_drop": "Simulates dropped or skipped frames",
    "dead_pixels": "Black (stuck-off) sensor pixels",
    "hot_pixels": "Bright (stuck-on) sensor pixels",
    "line_dropout": "Row/column failures from sensor readout issues",

    # AI-Relevant
    "temporal_lag": "Repeats old frame (TODO: needs sequence memory)",
    "spatial_jitter": "Pixel-level noise or motion shake",
    "random_patch_noise": "Random occlusion patches",
    "warping": "Perspective or lens-induced distortion"
}
