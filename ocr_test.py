
import cv2
import pytesseract
from pytesseract import Output


camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera could not be opened.")
    exit()


print("\nImproved OCR test started.")
print("Show printed text or text on a screen.")
print("Press Q to quit.")

previous_text = ""


while True:

    ret, frame = camera.read()

    if not ret:
        print("Could not capture frame.")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Increase image size
    gray = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    # Improve contrast
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    gray = clahe.apply(gray)

    # Remove noise
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Perform OCR with confidence values
    results = pytesseract.image_to_data(
        gray,
        config="--psm 6",
        output_type=Output.DICT
    )

    current_text = []

    for i in range(len(results["text"])):

        word = results["text"][i].strip()

        try:
            confidence = float(results["conf"][i])
        except ValueError:
            confidence = -1

        if word != "" and confidence >= 50:
            current_text.append(word)

    extracted_text = " ".join(current_text)

    # Print only when recognized text changes
    if extracted_text != "" and extracted_text != previous_text:

        print("\nTEXT DETECTED:")
        print(extracted_text)

        previous_text = extracted_text

    # Show camera feed
    cv2.imshow("Improved OCR Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()

print("\nOCR test completed.")
