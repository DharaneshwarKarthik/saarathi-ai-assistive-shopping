
import cv2
import pytesseract
from ultralytics import YOLO


print("Loading YOLOv8s...")
model = YOLO("yolov8s.pt")
print("YOLO loaded successfully.")

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera could not be opened.")
    exit()

print("\nDiagnostic test started.")
print("Show a book, bottle, or text on a screen.")
print("Press Q to quit.")

frame_count = 0
previous_text = ""

while True:

    ret, frame = camera.read()

    if not ret:
        print("Camera frame could not be captured.")
        break

    frame_count += 1

    # Run YOLO on the complete frame
    results = model.predict(
        source=frame,
        conf=0.25,
        verbose=False
    )

    # Draw all YOLO detections
    output = results[0].plot()

    # Print detected objects every 30 frames
    if frame_count % 30 == 0:

        detected_objects = []

        for box in results[0].boxes:
            class_id = int(box.cls[0])
            object_name = model.names[class_id]
            detected_objects.append(object_name)

        print("\nYOLO OBJECTS:", detected_objects)

    # Run OCR independently on the complete frame
    if frame_count % 10 == 0:

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.resize(
            gray,
            None,
            fx=2,
            fy=2,
            interpolation=cv2.INTER_CUBIC
        )

        text = pytesseract.image_to_string(
            gray,
            config="--psm 11"
        )

        text = text.strip()

        if text != "" and text != previous_text:

            print("\nOCR TEXT:")
            print(text)

            previous_text = text

    # Show annotated camera frame
    cv2.imshow("YOLO Diagnostic Test", output)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()

print("\nDiagnostic test completed.")
