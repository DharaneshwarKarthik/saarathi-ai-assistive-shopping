from ultralytics import YOLO
import torch
import csv
from pathlib import Path

model = YOLO("submissao/modelos/yolov8n_sku/weights.pt")

data_yaml = "/Users/dharaneshwark/shopping_assistant/data.yaml"

metrics = model.val(
    data=data_yaml,
    split="test",
    imgsz=640,
    batch=1,
    device="mps",
    workers=0,
    fraction=0.01,
    max_det=1000,
    plots=False,
    project="runs/val",
    name="sku110k_baseline_subset",
    exist_ok=True
)

results = {
    "Model": "YOLOv8n baseline",
    "Precision": metrics.box.mp,
    "Recall": metrics.box.mr,
    "mAP50": metrics.box.map50,
    "mAP50-95": metrics.box.map
}

print("\n--- BASELINE EVALUATION RESULTS ---")

for name, value in results.items():
    if isinstance(value, float):
        print(f"{name}: {value:.4f}")
    else:
        print(f"{name}: {value}")

output_file = Path("baseline_metrics.csv")

with output_file.open("w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Metric", "Value"])

    for name, value in results.items():
        writer.writerow([name, value])

print(f"\nMetrics saved to: {output_file.resolve()}")