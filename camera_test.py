
import cv2
from ultralytics import YOLO

print("Loading YOLO model...")

model = YOLO("yolov8s.pt")

print("YOLO model loaded.")

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Camera could not open.")
    exit()

print("Camera opened successfully.")

while True:

    ret, frame = camera.read()

    if not ret:
        print("Frame capture failed.")
        break

    results = model.predict(
        source=frame,
        conf=0.40,
        verbose=False
    )

    print("Detected:", [
        model.names[int(box.cls[0])]
        for box in results[0].boxes
    ])

    output = results[0].plot()

    cv2.imshow("Camera Test", output)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

print("Camera stopped.")
