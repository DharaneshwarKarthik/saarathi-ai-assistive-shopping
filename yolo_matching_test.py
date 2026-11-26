
import cv2
import subprocess
from ultralytics import YOLO

from shopping_list import get_shopping_list, update_product_status


# Number of consecutive frames needed
REQUIRED_FRAMES = 5


# Possible object mappings
object_mapping = {
    "milk": ["bottle"],
    "biscuits": ["sandwich"],
    "coca-cola": ["bottle"],
    "sprite": ["bottle"],
    "curd": ["bowl"],
    "cake": ["cake"],
    "rice": ["bowl"],
    "bread": ["sandwich"],
    "sugar": ["bowl"],
    "oil": ["bottle"],
    "water": ["bottle"],
    "chips": ["packet"]
}


# Get saved shopping list
shopping_list = get_shopping_list()

print("\n========== SAVED SHOPPING LIST ==========")

if len(shopping_list) == 0:
    print("Your shopping list is empty.")
    exit()

for item in shopping_list:
    print(
        item["product"],
        "-",
        item["brand"],
        "-",
        item["status"]
    )


# Load YOLO model
print("\nLoading YOLOv8s model...")

model = YOLO("yolov8s.pt")

print("YOLO model loaded successfully.")


# Open camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera could not be opened.")
    exit()

print("\nCamera started.")
print("Show objects to the camera.")
print("Press Q to quit.")


# Track consecutive detections
detection_counts = {}

# Avoid repeated announcements
announced_products = set()


while True:

    ret, frame = camera.read()

    if not ret:
        print("Could not capture frame.")
        break

    # Run YOLO detection
    results = model.predict(
        source=frame,
        conf=0.40,
        verbose=False
    )

    detected_objects = []

    for box in results[0].boxes:

        class_id = int(box.cls[0])
        object_name = model.names[class_id]

        detected_objects.append(object_name)

    # Check each pending shopping-list item
    for item in shopping_list:

        product = item["product"]
        brand = item["brand"]

        if item["status"] != "Pending":
            continue

        possible_objects = object_mapping.get(
            product,
            [product]
        )

        found = False

        for detected in detected_objects:

            if detected in possible_objects:
                found = True
                break

        if found:

            if product not in detection_counts:
                detection_counts[product] = 0

            detection_counts[product] += 1

            if (detection_counts[product] >= REQUIRED_FRAMES
                    and product not in announced_products):

                message = (
                    "Possible match for "
                    + product
                    + " detected. Please verify the product."
                )

                print("\nASSISTANT:", message)

                subprocess.Popen(["say", message])

                update_product_status(
                    product,
                    brand,
                    "Possible match"
                )

                item["status"] = "Possible match"

                announced_products.add(product)

        else:

            detection_counts[product] = 0

    # Display YOLO results
    output = results[0].plot()

    cv2.imshow("AI Shopping Assistant", output)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# Stop camera
camera.release()
cv2.destroyAllWindows()

print("\nCamera stopped.")

print("\n========== SHOPPING PROGRESS ==========")

for item in get_shopping_list():

    print(
        item["product"],
        "-",
        item["status"]
    )
