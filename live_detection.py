
from ultralytics import YOLO
import cv2

# Load pretrained YOLOv8s model
model = YOLO("yolov8s.pt")

# Open MacBook camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera could not be opened")
    exit()

print("Camera started. Press Q to quit.")

while True:

    # Capture frame from camera
    ret, frame = camera.read()

    if not ret:
        print("Could not capture frame")
        break

    # Detect objects in the frame
    results = model.predict(
        source=frame,
        conf=0.25,
        verbose=False
    )

    # Draw bounding boxes and labels
    output = results[0].plot()

    # Display live camera output
    cv2.imshow("YOLOv8 Live Object Detection", output)

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera
camera.release()
cv2.destroyAllWindows()
