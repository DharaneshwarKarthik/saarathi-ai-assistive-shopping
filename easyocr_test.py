
import cv2
import easyocr
import threading


print("Loading EasyOCR...")

reader = easyocr.Reader(['en'], gpu=False)

print("EasyOCR loaded successfully.")


camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera could not be opened.")
    exit()


# Reduce camera resolution
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


print("\nOptimized EasyOCR test started.")
print("Show a book or product with text.")
print("Press Q to quit.")


# Shared variables
ocr_running = False
ocr_result = ""
lock = threading.Lock()


# Function to perform OCR in background
def perform_ocr(image):

    global ocr_running
    global ocr_result

    try:

        results = reader.readtext(
            image,
            detail=1,
            paragraph=False,
            decoder="greedy"
        )

        detected_words = []

        for result in results:

            text = result[1]
            confidence = result[2]

            if confidence >= 0.50:
                detected_words.append(text)

        final_text = " ".join(detected_words)

        with lock:
            ocr_result = final_text

    except Exception as error:

        print("OCR error:", error)

    finally:

        with lock:
            ocr_running = False


previous_text = ""


while True:

    ret, frame = camera.read()

    if not ret:
        print("Camera capture failed.")
        break

    # Display frame continuously
    cv2.imshow("Optimized EasyOCR", frame)

    # Start OCR only if previous OCR is complete
    if not ocr_running:

        with lock:
            ocr_running = True

        # Resize frame for faster OCR
        small_frame = cv2.resize(
            frame,
            (480, 360)
        )

        # Start background OCR thread
        thread = threading.Thread(
            target=perform_ocr,
            args=(small_frame.copy(),)
        )

        thread.daemon = True
        thread.start()

    # Read OCR output
    with lock:
        current_text = ocr_result

    if current_text != "" and current_text != previous_text:

        print("\nEASYOCR TEXT:")
        print(current_text)

        previous_text = current_text

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()

print("\nOptimized OCR test completed.")
