
import cv2
import easyocr
import threading
import subprocess
from ultralytics import YOLO

from shopping_list import get_shopping_list, update_product_status
from brand_matching import check_brand


# ---------------- SETTINGS ----------------

YOLO_CONFIDENCE = 0.40
OCR_CONFIDENCE = 0.50
OCR_INTERVAL = 20

REQUIRED_MATCHES = 3

# -------------------------------------------


# Load shopping list
shopping_list = get_shopping_list()

if len(shopping_list) == 0:
    print("Shopping list is empty.")
    exit()

print("\n========== SAVED SHOPPING LIST ==========")

for item in shopping_list:
    print(
        item["product"],
        "-",
        item["brand"],
        "-",
        item["status"]
    )


# Load YOLO
print("\nLoading YOLOv8s model...")

model = YOLO("yolov8s.pt")

print("YOLO loaded successfully.")


# Load EasyOCR
print("\nLoading EasyOCR...")

reader = easyocr.Reader(["en"], gpu=False)

print("EasyOCR loaded successfully.")


# Open camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera could not be opened.")
    exit()

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# OCR thread variables
ocr_running = False
ocr_result = ""

ocr_lock = threading.Lock()

frame_count = 0

previous_ocr_text = ""

# Track repeated brand matches
brand_match_counts = {}

# Prevent repeated announcements
announced_products = set()


# ---------------- OCR FUNCTION ----------------

def perform_ocr(crops, full_frame):

    global ocr_running
    global ocr_result

    all_text = []

    try:

        # OCR on YOLO object crops
        for crop in crops:

            results = reader.readtext(
                crop,
                detail=1,
                paragraph=False,
                decoder="greedy"
            )

            for result in results:

                detected_text = result[1]
                confidence = result[2]

                if confidence >= OCR_CONFIDENCE:
                    all_text.append(detected_text)

        # Full-frame fallback
        if len(all_text) == 0:

            print("\nCrop OCR found no reliable text.")
            print("Running full-frame OCR...")

            results = reader.readtext(
                full_frame,
                detail=1,
                paragraph=False,
                decoder="greedy"
            )

            for result in results:

                detected_text = result[1]
                confidence = result[2]

                if confidence >= OCR_CONFIDENCE:
                    all_text.append(detected_text)

        final_text = " ".join(all_text)

        with ocr_lock:
            ocr_result = final_text

    except Exception as error:

        print("\nOCR ERROR:", error)

    finally:

        with ocr_lock:
            ocr_running = False


# ---------------- BRAND MATCHING ----------------

def process_brand_matches(text):

    for item in shopping_list:

        product = item["product"]
        brand = item["brand"]

        if item["status"] != "Pending":
            continue

        if product in announced_products:
            continue

        # Check OCR text against requested brand
        if check_brand(brand, text):

            if product not in brand_match_counts:
                brand_match_counts[product] = 0

            brand_match_counts[product] += 1

            print(
                "\nBrand match evidence:",
                brand_match_counts[product],
                "/",
                REQUIRED_MATCHES
            )

            if brand_match_counts[product] >= REQUIRED_MATCHES:

                message = (
                    "Possible match for "
                    + brand
                    + " "
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


# ---------------- MAIN PROGRAM ----------------

print("\nYOLO + EasyOCR + Brand Matching started.")

print("Show a product with visible brand text.")
print("Press Q to quit.")


while True:

    ret, frame = camera.read()

    if not ret:

        print("Camera capture failed.")
        break

    frame_count += 1

    # YOLO detection
    results = model.predict(
        source=frame,
        conf=YOLO_CONFIDENCE,
        verbose=False
    )

    detected_crops = []
    detected_objects = []

    for box in results[0].boxes:

        class_id = int(box.cls[0])

        object_name = model.names[class_id]

        detected_objects.append(object_name)

        x1, y1, x2, y2 = box.xyxy[0].tolist()

        x1 = max(0, int(x1))
        y1 = max(0, int(y1))
        x2 = min(frame.shape[1], int(x2))
        y2 = min(frame.shape[0], int(y2))

        if x2 > x1 and y2 > y1:

            crop = frame[y1:y2, x1:x2]

            if crop.size > 0:
                detected_crops.append(crop.copy())

    # Print YOLO detections
    if frame_count % 30 == 0:

        if len(detected_objects) > 0:

            print("\nYOLO DETECTED:", detected_objects)

        else:

            print("\nYOLO detected no objects.")

    # Start OCR periodically
    if frame_count % OCR_INTERVAL == 0:

        with ocr_lock:

            if not ocr_running:

                ocr_running = True

                small_frame = cv2.resize(
                    frame,
                    (480, 360)
                )

                thread = threading.Thread(
                    target=perform_ocr,
                    args=(
                        detected_crops,
                        small_frame.copy()
                    )
                )

                thread.daemon = True
                thread.start()

    # Get OCR result
    with ocr_lock:
        current_text = ocr_result

    if current_text != "" and current_text != previous_ocr_text:

        print("\n========== OCR TEXT ==========")

        print(current_text)

        previous_ocr_text = current_text

        process_brand_matches(current_text)

    # Display camera
    output = results[0].plot()

    cv2.imshow(
        "AI Shopping Assistant",
        output
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ---------------- CLEANUP ----------------

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
