
import cv2
import json
import matplotlib.pyplot as plt
from pathlib import Path

# Dataset paths
dataset_path = Path(
    "/Users/dharaneshwark/Downloads/sku110k_dataset/SKU110K_fixed"
)

image_name = "test_1765.jpg"

image_path = dataset_path / "images" / "test" / image_name
label_path = dataset_path / "labels" / "test" / "test_1765.txt"

prediction_path = Path(
    "runs/detect/submissao/final_evaluation/"
    "sku110k_test_standard/predictions.json"
)

# Read original image
image = cv2.imread(str(image_path))

if image is None:
    raise FileNotFoundError("Test image not found: " + str(image_path))

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

height, width = image.shape[:2]

# Create two copies
ground_truth_image = image.copy()
predicted_image = image.copy()

# Draw ground-truth boxes
gt_count = 0

with open(label_path, "r") as file:
    for line in file:
        values = line.strip().split()

        if len(values) < 5:
            continue

        class_id = int(values[0])

        x_center = float(values[1]) * width
        y_center = float(values[2]) * height
        box_width = float(values[3]) * width
        box_height = float(values[4]) * height

        x1 = int(x_center - box_width / 2)
        y1 = int(y_center - box_height / 2)
        x2 = int(x_center + box_width / 2)
        y2 = int(y_center + box_height / 2)

        cv2.rectangle(
            ground_truth_image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        gt_count += 1

# Read model predictions
with open(prediction_path, "r") as file:
    predictions = json.load(file)

confidence_threshold = 0.325
prediction_count = 0

for prediction in predictions:

    if prediction["file_name"] != image_name:
        continue

    confidence = prediction["score"]

    if confidence < confidence_threshold:
        continue

    x, y, box_width, box_height = prediction["bbox"]

    x1 = int(x)
    y1 = int(y)
    x2 = int(x + box_width)
    y2 = int(y + box_height)

    cv2.rectangle(
        predicted_image,
        (x1, y1),
        (x2, y2),
        (0, 100, 255),
        2
    )

    prediction_count += 1

# Display comparison
plt.figure(figsize=(18, 8))

plt.subplot(1, 2, 1)
plt.imshow(ground_truth_image)
plt.title("Ground Truth - Actual Annotations")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(predicted_image)
plt.title("YOLOv8n - Predicted Bounding Boxes")
plt.axis("off")

plt.suptitle(
    "Ground Truth vs YOLOv8n Predictions",
    fontsize=17
)

plt.tight_layout()

# Save high-resolution figure
output_path = "ground_truth_vs_prediction.png"

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Ground truth boxes:", gt_count)
print("Predicted boxes:", prediction_count)
print("Saved:", output_path)


