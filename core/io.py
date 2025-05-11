from pathlib import Path
import json
import csv

def list_images(input_folder):
    input_path = Path(input_folder)
    return list(input_path.glob("*.jpg")) + list(input_path.glob("*.jpeg")) + \
           list(input_path.glob("*.png")) + list(input_path.glob("*.webp"))

def save_metadata_json(output_path, data, filename="global_metadata_summary.json"):
    with open(Path(output_path) / filename, 'w') as f:
        json.dump(data, f, indent=4)

def save_metadata_csv(output_path, data, filename="global_metadata_summary.csv"):
    with open(Path(output_path) / filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["base_name", "level", "timestamp", "filename", "fault_name", "category"])
        for entry in data:
            for fault in entry["faults"]:
                writer.writerow([
                    entry["base_name"],
                    entry["level"],
                    entry["timestamp"],
                    fault["filename"],
                    fault["type"],
                    fault.get("category", "unknown")
                ])
