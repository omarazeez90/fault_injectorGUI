import time
import cv2
from pathlib import Path
from datetime import datetime
from core import io
from faults import apply_fault
from core.config import FAULT_CATEGORIES

def run_generation(app, selected_levels, selected_faults, output_path,
    log_callback=None, progress_callback=None, in_memory=False, resize_dims=None, parallel=False,app, selected_levels, selected_faults, output_path,
    resize_dims=None, parallel=False, log_callback=None, progress_callback=None):
    cancel_flag = [False]
    app.cancel_flag = cancel_flag

    image_files = io.list_images(app.input_path.get())
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    global_summary = []
    total = len(image_files) * len(selected_levels) * sum(len(f) for f in selected_faults.values())
    current = 0

    
    results = []
    for img_path in image_files:
        if cancel_flag[0]:
            break

        img = cv2.imread(str(img_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        base_name = img_path.stem

        for level in selected_levels:
            faults_metadata = []
            for category, faults in selected_faults.items():
                for fault in faults:
                    if parallel:
                            from concurrent.futures import ThreadPoolExecutor
                            with ThreadPoolExecutor() as executor:
                                future = executor.submit(apply_fault, img_rgb, fault, level)
                                result = future.result()
                        else:
                            result = apply_fault(img_rgb, fault, level)
                    out_name = f"{base_name}_{fault}_{category}_{level}.jpg"
                    out_path = output_path / out_name
                    if in_memory:
                        results.append((out_path, result))
                    else:
                        cv2.imwrite(str(out_path), cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
                    faults_metadata.append({
                        "filename": out_name,
                        "type": fault,
                        "category": category
                    })

                    current += 1
                    if progress_callback:
                        progress_callback(current, total)

            global_summary.append({
                "base_name": base_name,
                "level": level,
                "timestamp": datetime.now().isoformat(),
                "faults": faults_metadata
            })

            if log_callback:
                log_callback(f"Processed: {base_name} - {level} ({len(faults_metadata)} faults)")

    return global_summary
