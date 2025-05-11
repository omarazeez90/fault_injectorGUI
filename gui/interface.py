# Enhanced interface.py with scrollable configuration and polished layout
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from core import FAULT_CATEGORIES, FAULT_DESCRIPTIONS
from core.processing import run_generation
from core.io import save_metadata_json, save_metadata_csv
from core import config_editor
from PIL import Image, ImageTk
import cv2
import numpy as np
import threading
import time

class FaultInjectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Fault Injector")
        self.root.geometry("1000x720")

        import os
        default_input = os.path.join(os.path.dirname(__file__), '..', 'input')
        default_output = os.path.join(os.path.dirname(__file__), '..', 'output')
        os.makedirs(os.path.abspath(default_output), exist_ok=True)

        self.input_path = tk.StringVar(value=os.path.abspath(default_input).replace('\\', '/'))
        self.output_path = tk.StringVar(value=os.path.abspath(default_output).replace('\\', '/'))
        self.export_json = tk.IntVar(value=1)
        self.export_csv = tk.IntVar(value=1)
        self.resize_width = tk.IntVar(value=320)
        self.resize_height = tk.IntVar(value=240)
        self.config_resolution = {"resize_width": self.resize_width.get(), "resize_height": self.resize_height.get()}
        self.level_vars = {lvl: tk.IntVar(value=1 if lvl == 'medium' else 0) for lvl in ['low', 'medium', 'extreme']}
        self.fault_vars = {cat: {f: tk.IntVar() for f in faults} for cat, faults in FAULT_CATEGORIES.items()}

        self.create_widgets()

    def create_widgets(self):
        self.time_label = tk.Label(self.root, text="", font=("Arial", 9))
        self.time_label.grid(row=5, column=0, columnspan=3, pady=(0, 10))
        tk.Label(self.root, text="Input Folder:").grid(row=0, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.input_path, width=40).grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_input).grid(row=0, column=2)

        tk.Label(self.root, text="Output Folder:").grid(row=1, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.output_path, width=40).grid(row=1, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_output).grid(row=1, column=2)

        # Fault level checkboxes
        level_frame = tk.LabelFrame(self.root, text="Fault Intensity Level")
        level_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        for i, (lvl, var) in enumerate(self.level_vars.items()):
            tk.Checkbutton(level_frame, text=lvl.title(), variable=var).grid(row=0, column=i)

        notebook = ttk.Notebook(self.root)
        notebook.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        # Fault category tabs
        for category, faults in FAULT_CATEGORIES.items():
            frame = tk.Frame(notebook)
            cat_var = tk.IntVar()
            chk_all = tk.Checkbutton(frame, text=f"Select All {category}", variable=cat_var,
                                     command=lambda c=category, v=cat_var: self.toggle_category(c, v))
            chk_all.pack(anchor="w")
            notebook.add(frame, text=category)
            for fname in faults:
                desc = FAULT_DESCRIPTIONS.get(fname, "")
                chk = tk.Checkbutton(frame, text=f"{fname.replace('_', ' ').title()} - {desc}",
                                     variable=self.fault_vars[category][fname])
                chk.pack(anchor="w")

        # Scrollable configuration tab
        self.config_frame = tk.Frame(notebook)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        notebook.add(self.config_frame, text="Configuration")

        canvas = tk.Canvas(self.config_frame)
        scrollbar = tk.Scrollbar(self.config_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y")
        # Replace with reset + save row at top
        top_button_row = tk.Frame(scroll_frame)
        top_button_row.pack(pady=(10, 5), anchor="w")
        tk.Button(top_button_row, text="Reset All Intensities", command=self.reset_intensities, bg="orange", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        tk.Button(top_button_row, text="Save Changes", command=self.save_config, bg="lightgreen", font=("Arial", 10, "bold")).pack(side="left", padx=5)

        

        self.config_data = config_editor.load_config()
        self.config_sliders = {}

        for i, (fault, levels) in enumerate(self.config_data.items()):
            if not isinstance(levels, dict):
                continue
            tk.Label(scroll_frame, text=fault.replace('_', ' ').title(), font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 0))
            self.config_sliders[fault] = {}
            for lvl in ['low', 'medium', 'extreme']:
                var = tk.DoubleVar(value=levels[lvl])
                self.config_sliders[fault][lvl] = var
                frame = tk.Frame(scroll_frame)
                frame.pack(anchor="w", fill="x", padx=10)
                tk.Label(frame, text=f"{lvl.title():<8}", width=10).pack(side="left")
                tk.Scale(frame, from_=0, to=100, orient="horizontal", resolution=0.1, length=250, variable=var).pack(side="left")

        # Moved to top and bottom
        bottom_button_row = tk.Frame(scroll_frame)
        bottom_button_row.pack(pady=10, anchor="w")
        tk.Button(bottom_button_row, text="Reset All Intensities", command=self.reset_intensities, bg="orange", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        tk.Button(bottom_button_row, text="Save Changes", command=self.save_config, bg="lightgreen", font=("Arial", 10, "bold")).pack(side="left", padx=5)

        export_frame = tk.Frame(self.root)
        export_frame.grid(row=4, column=0, columnspan=3)
        tk.Checkbutton(export_frame, text="Export JSON", variable=self.export_json).pack(side="left", padx=10)
        tk.Checkbutton(export_frame, text="Export CSV", variable=self.export_csv).pack(side="left", padx=10)

        self.progress = ttk.Progressbar(self.root, length=400, mode='determinate')
        self.progress.grid(row=6, column=0, columnspan=3, pady=5)

        action_frame = tk.Frame(self.root)
        action_frame.grid(row=7, column=0, columnspan=3, pady=10)
        tk.Button(action_frame, text="Start", bg="green", fg="white", command=self.start).pack(side="left", padx=5)
        tk.Button(action_frame, text="Reset", bg="gray", fg="white", command=self.reset_form).pack(side="left", padx=5)
        tk.Button(action_frame, text="Select All", bg="lightblue", command=self.select_all_faults_levels).pack(side="left", padx=5)
        tk.Button(action_frame, text="Deselect All", bg="lightgray", command=self.deselect_all_faults_levels).pack(side="left", padx=5)
        resolution_frame = tk.LabelFrame(self.root, text="Output Image Resolution (for speed)")
        resolution_frame.grid(row=8, column=0, columnspan=3, pady=(5, 10))
        tk.Label(resolution_frame, text="Width:").pack(side="left")
        tk.Entry(resolution_frame, textvariable=self.resize_width, width=5).pack(side="left")
        tk.Label(resolution_frame, text="Height:").pack(side="left")
        tk.Entry(resolution_frame, textvariable=self.resize_height, width=5).pack(side="left")
        

    def toggle_category(self, category, var):
        for fname in self.fault_vars[category]:
            self.fault_vars[category][fname].set(var.get())

    def browse_input(self):
        path = filedialog.askdirectory()
        if path:
            self.input_path.set(path)

    def browse_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path.set(path)

    def reset_form(self):
        import os
        default_input = os.path.join(os.path.dirname(__file__), '..', 'input')
        default_output = os.path.join(os.path.dirname(__file__), '..', 'output')
        self.input_path.set(os.path.abspath(default_input).replace('\\', '/'))
        self.output_path.set(os.path.abspath(default_output).replace('\\', '/'))
        for var in self.level_vars.values():
            var.set(0)
        self.level_vars['medium'].set(1)
        for cat_vars in self.fault_vars.values():
            for var in cat_vars.values():
                var.set(0)
        self.export_json.set(1)
        self.export_csv.set(1)
        self.progress['value'] = 0

    def reset_intensities(self):
        defaults = config_editor.DEFAULTS
        for f, levels in defaults.items():
            if isinstance(levels, dict):
                for lvl, val in levels.items():
                    if f in self.config_sliders and lvl in self.config_sliders[f]:
                        self.config_sliders[f][lvl].set(val)
        if "resize_width" in defaults:
            self.resize_width.set(defaults["resize_width"])
        if "resize_height" in defaults:
            self.resize_height.set(defaults["resize_height"])
        config_editor.save_config(defaults)
        messagebox.showinfo("Reset", "All settings reset to default.")

    def save_config(self):
        updated = {f: {lvl: var.get() for lvl, var in lvls.items()} for f, lvls in self.config_sliders.items()}
        updated["resize_width"] = self.resize_width.get()
        updated["resize_height"] = self.resize_height.get()
        config_editor.save_config(updated)
        messagebox.showinfo("Saved", "Configuration updated successfully.")

    def preview(self):
        pass  # Preview disabled for faster dataset generation

    def select_all_faults_levels(self):
        for lvl_var in self.level_vars.values():
            lvl_var.set(1)
        for cat_vars in self.fault_vars.values():
            for var in cat_vars.values():
                var.set(1)

    def deselect_all_faults_levels(self):
        for lvl_var in self.level_vars.values():
            lvl_var.set(0)
        for cat_vars in self.fault_vars.values():
            for var in cat_vars.values():
                var.set(0)

    def start(self):
        selected_levels = [lvl for lvl, var in self.level_vars.items() if var.get() == 1]
        selected_faults = {cat: [f for f, var in faults.items() if var.get() == 1]
                           for cat, faults in self.fault_vars.items()}
        selected_faults = {k: v for k, v in selected_faults.items() if v}

        if not self.input_path.get() or not self.output_path.get():
            messagebox.showerror("Missing Path", "Please select both input and output folders.")
            return
        if not selected_levels or not selected_faults:
            messagebox.showerror("Missing Selection", "Select at least one fault and one intensity level.")
            return
        start = time.perf_counter()

        def progress_callback(current, total):
            elapsed = time.perf_counter() - start
            est_total = elapsed / max(current, 1) * total
            remaining = est_total - elapsed
            mins = int(remaining // 60)
            secs = int(remaining % 60)
            self.time_label.config(text=f"ETA: {mins}m {secs}s")
            percent = int((current / total) * 100)
            self.progress['value'] = percent
            self.progress.update_idletasks()
            self.root.title(f"Advanced Fault Injector - {percent}% complete")

        def run():
            import time
            start = time.perf_counter()
            from concurrent.futures import ThreadPoolExecutor
            summary = run_generation(self, selected_levels, selected_faults, self.output_path.get(),
                                     log_callback=None, progress_callback=progress_callback, resize_dims=(self.resize_width.get(), self.resize_height.get()), parallel=True)
            if self.export_json.get():
                save_metadata_json(self.output_path.get(), summary)
            if self.export_csv.get():
                save_metadata_csv(self.output_path.get(), summary)
            import time
            end = time.perf_counter()
            duration = round(end - start, 2)
            self.root.title("Advanced Fault Injector")
            messagebox.showinfo("Done", f"Fault injection complete in {duration} seconds.")

        threading.Thread(target=run).start()
