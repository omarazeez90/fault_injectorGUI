# START OF REFACTORED FAULT INJECTION TOOL

import cv2
import os
import numpy as np
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
from PIL import Image, ImageTk
import json
import csv

# Define extended fault categories and types
FAULT_CATEGORIES = {
    "EMI": {
        "salt_pepper_noise": "Simulates sensor noise",
        "color_shift": "Color processing interference",
        "flicker": "Frame flickering (intermittent visibility)",
        "desaturation": "Loss of color intensity",
        "rolling_shutter_skew": "Distorted timing on sensor rows"
    },
    "Environmental": {
        "blur": "Defocus or motion blur",
        "brightness": "Lighting changes",
        "fog": "Low visibility conditions",
        "raindrop": "Droplets on lens",
        "glare": "Bright light sources",
        "lens_dirt": "Obstruction on lens"
    },
    "Hardware": {
        "frame_drop": "Missing frames",
        "dead_pixels": "Stuck black pixels",
        "hot_pixels": "Stuck white pixels",
        "line_dropout": "Sensor line failure",
        "blackout": "Complete sensor failure"
    },
    "AI_Relevant": {
        "temporal_lag": "Old frame reuse",
        "spatial_jitter": "Pixel-level noise",
        "random_patch_noise": "Patch-based occlusion",
        "warping": "Distortion due to lens or transformation"
    }
}

# GUI placeholder structure
class FaultInjectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Fault Injection Simulator")

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()

        self.level_vars = {lvl: tk.IntVar(value=1 if lvl == 'medium' else 0) for lvl in ['low', 'medium', 'extreme']}
        self.export_json = tk.IntVar(value=1)
        self.export_csv = tk.IntVar(value=1)
        self.fault_vars = {cat: {f: tk.IntVar() for f in faults} for cat, faults in FAULT_CATEGORIES.items()}

        self.create_widgets()

    def create_widgets(self):
        # Input/output controls
        tk.Label(self.root, text="Input Folder:").grid(row=0, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.input_path, width=40).grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_input).grid(row=0, column=2)

        tk.Label(self.root, text="Output Folder:").grid(row=1, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.output_path, width=40).grid(row=1, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_output).grid(row=1, column=2)

        # Fault level checkboxes
        level_frame = tk.LabelFrame(self.root, text="Fault Strength Level")
        level_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        for i, (lvl, var) in enumerate(self.level_vars.items()):
            tk.Checkbutton(level_frame, text=lvl.capitalize(), variable=var).grid(row=0, column=i)

        # Fault category tabs
        notebook = ttk.Notebook(self.root)
        notebook.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        for category, faults in FAULT_CATEGORIES.items():
            frame = tk.Frame(notebook)
            notebook.add(frame, text=category)
            for i, (fname, desc) in enumerate(faults.items()):
                chk = tk.Checkbutton(frame, text=f"{fname.replace('_',' ').title()} - {desc}", variable=self.fault_vars[category][fname])
                chk.pack(anchor="w")

        # Export options
        export_frame = tk.Frame(self.root)
        export_frame.grid(row=4, column=0, columnspan=3)
        tk.Checkbutton(export_frame, text="Export JSON", variable=self.export_json).pack(side="left", padx=10)
        tk.Checkbutton(export_frame, text="Export CSV", variable=self.export_csv).pack(side="left", padx=10)

        # Action buttons
        action_frame = tk.Frame(self.root)
        action_frame.grid(row=5, column=0, columnspan=3, pady=10)
        tk.Button(action_frame, text="Preview", bg="blue", fg="white", command=self.preview).pack(side="left", padx=5)
        tk.Button(action_frame, text="Start", bg="green", fg="white", command=self.start).pack(side="left", padx=5)

    def browse_input(self):
        path = filedialog.askdirectory()
        if path:
            self.input_path.set(path)

    def browse_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path.set(path)

    def preview(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp")])
        if not file_path:
            return
        image = cv2.imread(file_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        selected_level = next((lvl for lvl, var in self.level_vars.items() if var.get() == 1), 'medium')
        selected_faults = [(cat, fname) for cat, faults in self.fault_vars.items() for fname, var in faults.items() if var.get() == 1]

        if not selected_faults:
            messagebox.showwarning("Warning", "Please select at least one fault to preview.")
            return

        preview_fault = selected_faults[0]
        category, fault_name = preview_fault

        processed = self.apply_fault(image_rgb, fault_name, selected_level)

        if processed is None:
            messagebox.showerror("Error", f"No implementation for fault: {fault_name}")
            return

        from PIL import ImageTk, Image
        img_pil = Image.fromarray(processed)
        img_tk = ImageTk.PhotoImage(img_pil.resize((300, 300)))

        preview_win = tk.Toplevel(self.root)
        preview_win.title("Preview")
        tk.Label(preview_win, text=f"Fault: {fault_name.replace('_', ' ').title()} | Level: {selected_level}").pack(pady=5)
        tk.Label(preview_win, image=img_tk).pack()
        preview_win.mainloop()

    def apply_fault(self, image_rgb, fault_name, level):
        if fault_name == "salt_pepper_noise":
            amount = {"low": 0.01, "medium": 0.03, "extreme": 0.07}[level]
            noisy = image_rgb.copy()
            num_salt = int(amount * image_rgb.size * 0.5)
            num_pepper = int(amount * image_rgb.size * 0.5)
            coords = [np.random.randint(0, i - 1, num_salt) for i in image_rgb.shape[:2]]
            noisy[coords[0], coords[1], :] = 255
            coords = [np.random.randint(0, i - 1, num_pepper) for i in image_rgb.shape[:2]]
            noisy[coords[0], coords[1], :] = 0
            return noisy

        elif fault_name == "color_shift":
            shift = {"low": (10, -10), "medium": (30, -20), "extreme": (60, -40)}[level]
            r_shift, b_shift = shift
            b, g, r = cv2.split(image_rgb)
            r = np.clip(r.astype(np.int16) + r_shift, 0, 255).astype(np.uint8)
            b = np.clip(b.astype(np.int16) + b_shift, 0, 255).astype(np.uint8)
            return cv2.merge((b, g, r))

        elif fault_name == "blur":
            k = {"low": 3, "medium": 7, "extreme": 13}[level]
            return cv2.GaussianBlur(image_rgb, (k, k), 0)

        elif fault_name == "brightness":
            factor = {"low": 1.2, "medium": 1.5, "extreme": 1.8}[level]
            return np.clip(image_rgb.astype(np.float32) * factor, 0, 255).astype(np.uint8)

        elif fault_name == "desaturation":
            gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
            return cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

        elif fault_name == "fog":
            overlay = np.full_like(image_rgb, 200)
            alpha = {"low": 0.3, "medium": 0.5, "extreme": 0.7}[level]
            return cv2.addWeighted(image_rgb, 1 - alpha, overlay, alpha, 0)

        elif fault_name == "glare":
            overlay = image_rgb.copy()
            center = (overlay.shape[1] // 2, overlay.shape[0] // 2)
            radius = min(center) // 2
            mask = np.zeros_like(overlay, dtype=np.uint8)
            cv2.circle(mask, center, radius, (255, 255, 255), -1)
            alpha = {"low": 0.2, "medium": 0.4, "extreme": 0.6}[level]
            return cv2.addWeighted(overlay, 1, mask, alpha, 0)

                # Default for unimplemented faults
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = f"[To be implemented: {fault_name.replace('_', ' ').title()}]"
        dummy = image_rgb.copy()
        cv2.putText(dummy, text, (30, dummy.shape[0] // 2), font, 0.7, (255, 0, 0), 2, cv2.LINE_AA)
        return dummy

    def start(self):
        selected_levels = [lvl for lvl, var in self.level_vars.items() if var.get() == 1]
        selected_faults = {
            cat: [f for f, var in faults.items() if var.get() == 1]
            for cat, faults in self.fault_vars.items()
        }
        selected_faults = {k: v for k, v in selected_faults.items() if v}

        summary = f"Levels: {selected_levels}\nSelected Faults: {json.dumps(selected_faults, indent=2)}"
        messagebox.showinfo("Simulation Setup", summary)

if __name__ == '__main__':
    root = tk.Tk()
    app = FaultInjectorApp(root)
    root.mainloop()

# END OF GUI STUB
